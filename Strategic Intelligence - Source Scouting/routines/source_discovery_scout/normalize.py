"""Normalize a scout worker's COMPACT output into the full scout_output the runner ingests.

The live scout (Claude + web search) returns compact records that carry the intelligence but not the
full schema scaffolding. This module deterministically EXPANDS them into full-shaped records, snapping
enums to allowed values and applying the collection-safety clamps, so the deterministic runner can
validate / verify / dedupe / audit them. It performs NO validation (the runner is the validation gate),
NO I/O, and NO network — pure, dependency-free transformation.

Compact contract (per record; extra keys ignored, missing keys defaulted):
  candidate: source_name, source_url, domain, source_class(direct|indirect|pointer), source_subtype,
    primary_language, topics[], access_status, legal_status, collection_allowed, suggested_collection_method,
    credibility_score, usefulness_score, confidence_score, priority, why_relevant, known_limitations?,
    example_urls[]?, discovered_via_method?, queries_used[]?, local_language_terms_used[]?,
    blocked?, blocker_type?, observed_blocker?
  negative_finding: finding_type, description, why_it_matters, severity, language, source_class, topics[],
    queries_used[]?, method?, result_summary
  coverage_gap: gap_type, coverage_dimension, description, why_it_matters, severity, source_class, topics[],
    recommended_action, language
Top-level compact keys: candidates[], negative_findings[], coverage_gaps[], glossary[], actors[],
  search_attempts[], failed_searches[], errors[]?, raw_traces[]?, discovered_source_categories[],
  briefs[] (or brief:str).

Country/sector/workstream come from the run CONFIG (authoritative), not the compact records.
"""
import re

_LANG_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]*$")

ACCESS = {"public", "blocked", "requires_free_account", "requires_paid_subscription", "requires_manual_download",
          "requires_credentials", "requires_legal_review", "forbidden_do_not_collect", "unknown"}
LEGAL = {"allowed", "unclear", "restricted", "forbidden", "requires_review"}
CLASS3 = {"direct", "indirect", "pointer"}
CLASS5 = CLASS3 | {"unknown", "not_applicable"}
PRIORITY = {"low", "medium", "high", "critical"}
METHOD = {"api", "rss_feed", "sitemap", "static_html", "pdf_download", "dynamic_browser",
          "search_result_ingestion", "manual_upload", "transcript_ingestion", "none", "unknown"}
NF_TYPES = {"failed_search", "searched_no_result", "source_not_found", "blocked_source", "inaccessible_source",
            "dead_link", "missing_source_class", "local_language_blind_spot", "unexpanded_pointer_source",
            "weak_or_ambiguous_keyword", "out_of_scope_source", "duplicate_or_superseded_source",
            "legal_or_policy_block", "low_quality_source", "no_relevant_results"}
NF_METHOD = {"keyword_search", "local_language_search", "pointer_expansion", "snowball", "url_verification",
             "access_probe", "registry_check", "manual_review", "deterministic_check", "connector_fetch",
             "llm_reasoning", "other"}
GAP_TYPES = {"missing", "weak", "stale", "inaccessible", "legally_blocked", "under_searched",
             "unexpanded_pointer", "needs_human_review", "low_quality", "unknown"}
GAP_DIMS = {"country", "workstream", "topic", "source_class", "source_subtype", "language", "entity_set",
            "time_horizon", "refresh_cadence", "source_quality", "access_legal", "pointer_expansion",
            "field_intelligence"}
GAP_ACTIONS = {"expand_search", "expand_local_language_terms", "expand_pointer_source", "add_source_class",
               "find_alternative_sources", "schedule_refresh", "request_human_review",
               "request_access_or_legal_review", "accept_gap", "update_playbook", "no_action", "other"}
BLOCKERS = {"login_required", "free_registration_required", "paid_subscription_required", "captcha_or_bot_block",
            "manual_download_required", "file_not_directly_linked", "credentials_needed", "terms_of_use_unclear",
            "legal_review_needed", "geo_blocked", "broken_link", "forbidden_source", "unknown"}
_ACTION_BY_BLOCKER = {"free_registration_required": "create_free_account_if_allowed",
                      "paid_subscription_required": "confirm_subscription_access",
                      "manual_download_required": "download_document_manually",
                      "login_required": "provide_credentials_if_permitted",
                      "credentials_needed": "provide_credentials_if_permitted",
                      "terms_of_use_unclear": "check_terms_of_use", "legal_review_needed": "check_terms_of_use",
                      "forbidden_source": "mark_source_forbidden"}


# The live LLM scout drifts off the controlled vocab (e.g. it writes access "open"/"accessible" and legal
# "public_official"/"public" instead of the schema's "public"/"allowed"). Left unmapped, _enum fail-closes
# those to "unknown"/"unclear", which then correctly-but-needlessly PAUSES otherwise-public sources at the
# activation gate. These synonym maps recover the intended canonical value; anything genuinely ambiguous
# still falls through to the safe default. Keys are lower-cased.
ACCESS_SYNONYMS = {
    "open": "public", "openly_accessible": "public", "open_access": "public", "public_open": "public",
    "partial_open": "public", "accessible": "public", "freely_accessible": "public", "free": "public",
    "free_access": "public", "partial": "public", "partially_accessible": "public", "open_data": "public",
    "registration_required": "requires_free_account", "requires_registration": "requires_free_account",
    "free_registration": "requires_free_account",
    "login_required": "requires_credentials", "login_or_subscription": "requires_credentials",
    "credentials_required": "requires_credentials", "requires_login": "requires_credentials",
    "paywall": "requires_paid_subscription", "partial_paywall": "requires_paid_subscription",
    "subscription_required": "requires_paid_subscription", "paid": "requires_paid_subscription",
    "legal_review": "requires_legal_review", "requires_review": "requires_legal_review",
    "restricted": "blocked", "restricted_technical": "blocked", "bot_defended": "blocked",
    "geo_blocked": "blocked",
}
LEGAL_SYNONYMS = {
    "public_official": "allowed", "public": "allowed", "official_public": "allowed", "official": "allowed",
    "open_licence_cc": "allowed", "open_licence_mit": "allowed", "open_licence": "allowed",
    "open_license": "allowed", "open_data": "allowed", "public_data": "allowed",
    "public_data_aggregated": "allowed", "public_aggregator_thirdparty": "allowed",
    "public_association": "allowed", "public_official_opendata": "allowed", "third_party_public": "allowed",
    "public_aggregator": "allowed",
    "open_licence_review": "requires_review", "review_terms": "requires_review",
    "terms_review": "requires_review",
}


# Government / central-bank / regulator sites publish registers, statistics, tenders and press FOR public use,
# so an over-cautious "unclear"/"requires_review" legal read should NOT pause them. is_official_domain matches
# gov TLDs plus a curated set of the operating countries' central banks + EU/EEA supervisors. Only unclear/
# requires_review are lifted to "allowed"; forbidden/restricted legal values are never touched.
_OFFICIAL_HOSTS = {
    "bankofalbania.org", "bankofgreece.gr", "bnb.bg", "hnb.hr", "centralbank.cy", "cnb.cz", "mnb.hu",
    "bqk-kos.org", "cbcg.me", "nbrm.mk", "bnr.ro", "nbs.rs", "nbs.sk", "bsi.si",
    "ecb.europa.eu", "eba.europa.eu", "esma.europa.eu", "eiopa.europa.eu", "europa.eu",
}


def _host_of(s):
    if not isinstance(s, str):
        return ""
    h = s.strip().lower()
    if "//" in h:
        h = h.split("//", 1)[1]
    return h.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0].split("@")[-1].split(":", 1)[0]


def is_official_domain(url_or_host):
    """True for a government / central-bank / regulator host (gov TLD or the curated institution set)."""
    h = _host_of(url_or_host)
    if not h:
        return False
    if ".gov." in h or h.endswith(".gov") or ".gob." in h or ".gouv." in h:
        return True
    return any(h == d or h.endswith("." + d) for d in _OFFICIAL_HOSTS)


def _as_list(v):
    return v if isinstance(v, list) else []


def _enum(v, allowed, default, synonyms=None):
    # isinstance(str) guard: every `allowed` set holds only strings, so this both snaps a wrong-typed
    # value (list/dict/number/None) to the safe default AND avoids `unhashable type` on a list/dict `v`.
    if isinstance(v, str):
        if v in allowed:
            return v
        low = v.strip().lower()
        if low in allowed:            # a case/whitespace variant of a canonical value ('FORBIDDEN' -> 'forbidden')
            return low                # CRITICAL for safety: else 'FORBIDDEN' would fail-closed to the *permissive*
        if synonyms:                  # default ('unclear') and the forbidden-collection clamp would miss it
            mapped = synonyms.get(low)
            if mapped in allowed:
                return mapped
    return default


def _num01(v):
    try:
        return max(0.0, min(1.0, float(v)))
    except (TypeError, ValueError):
        return 0.5


def _lang(v):
    return v if isinstance(v, str) and _LANG_RE.match(v) else "el"


def _str(v, default=""):
    return v if isinstance(v, str) and v.strip() else default


def _strlist(v):
    return [x for x in v if isinstance(x, str)] if isinstance(v, list) else []


def _topics(v):
    out = [t for t in v if isinstance(t, str) and t.strip()] if isinstance(v, list) else []
    return out or ["procurement"]


def _scope(config):
    ws = (config.get("workstreams") or ["A2"])
    return config.get("country", "ZZ"), config.get("sector", "both"), (ws[0] if ws else "A2")


def expand_candidate(c, config, now, cid):
    country, sector, workstream = _scope(config)
    access = _enum(c.get("access_status"), ACCESS, "unknown", ACCESS_SYNONYMS)
    legal = _enum(c.get("legal_status"), LEGAL, "unclear", LEGAL_SYNONYMS)
    coll = bool(c.get("collection_allowed", True))
    # official public-sector domains: lift an over-cautious legal read so they aren't paused for no reason
    # (the forbidden_source clamp below still wins for anything genuinely flagged forbidden).
    if legal in ("unclear", "requires_review") and is_official_domain(c.get("source_url") or c.get("domain")):
        legal = "allowed"
    # a scout-flagged forbidden source must never be emitted collectable, and its legal must agree with the
    # paired AccessReviewTask (expand_access_task forces requires_review for blocker_type=forbidden_source).
    if c.get("blocked") and _enum(c.get("blocker_type"), BLOCKERS, "unknown") == "forbidden_source":
        if legal not in ("forbidden", "requires_review"):
            legal = "requires_review"
        coll = False
    if access == "forbidden_do_not_collect" or legal == "forbidden":
        coll = False   # safety clamp S1/S2 (the candidate schema also enforces this)
    url = _str(c.get("source_url"), "https://example.invalid/")
    return {
        "candidate_id": cid,
        "lifecycle_status": "discovered",
        "source_name": _str(c.get("source_name"), "unnamed source"),
        "source_url": url,
        "canonical_url": url,   # runner recomputes from source_url
        "domain": _str(c.get("domain"), "unknown"),
        "country": country, "sector": sector, "workstream": workstream,
        "source_class": _enum(c.get("source_class"), CLASS3, "indirect"),
        "source_subtype": _str(c.get("source_subtype"), "unknown"),
        "primary_language": _lang(c.get("primary_language")),
        "topics": _topics(c.get("topics")),
        "access_status": access, "legal_status": legal, "collection_allowed": coll,
        "suggested_collection_method": _enum(c.get("suggested_collection_method"), METHOD, "unknown"),
        "credibility_score": _num01(c.get("credibility_score")),
        "usefulness_score": _num01(c.get("usefulness_score")),
        "confidence_score": _num01(c.get("confidence_score")),
        "priority": _enum(c.get("priority"), PRIORITY, "medium"),
        "discovery_basis": {
            "why_relevant": _str(c.get("why_relevant"), "worth tracking for procurement signals"),
            "observed_source_behavior": "", "expected_information_value": "",
            "known_limitations": _str(c.get("known_limitations"), ""),
            "example_urls": _strlist(c.get("example_urls")), "sample_evidence_snippets": [],
        },
        "discovered_via": {
            "method": _str(c.get("discovered_via_method"), "keyword_search"),
            "queries_used": _strlist(c.get("queries_used")),
            "pointer_source_candidate_ids": [], "pointer_source_urls": [],
            "local_language_terms_used": _strlist(c.get("local_language_terms_used")),
            "discovered_at": now,
        },
        "dedupe": {"dedupe_status": "not_checked", "possible_duplicate_candidate_ids": [],
                   "possible_duplicate_source_ids": [], "canonicalization_notes": None},
        "review": {"review_status": "not_reviewed", "reviewer": None, "reviewed_at": None,
                   "review_notes": None, "rejection_reason": None, "human_review_required": bool(c.get("blocked"))},
        "promotion": {"promotion_status": "not_promoted", "promoted_source_id": None,
                      "promoted_at": None, "promotion_notes": None},
    }


def expand_access_task(c, config, cid, tid):
    country, sector, workstream = _scope(config)
    access = _enum(c.get("access_status"), ACCESS, "unknown", ACCESS_SYNONYMS)
    legal = _enum(c.get("legal_status"), LEGAL, "unclear", LEGAL_SYNONYMS)
    blocker = _enum(c.get("blocker_type"), BLOCKERS, "unknown")
    if blocker == "forbidden_source" and legal not in ("forbidden", "requires_review"):
        legal = "requires_review"   # allOf: forbidden_source => legal forbidden/requires_review
    action = _ACTION_BY_BLOCKER.get(blocker, "clarify_access_route")
    return {
        "task_id": tid, "candidate_id": cid, "task_status": "open",
        "priority": _enum(c.get("priority"), PRIORITY, "medium"),
        "country": country, "sector": sector, "workstream": workstream,
        "source_name": _str(c.get("source_name"), "unnamed source"),
        "source_url": _str(c.get("source_url"), "https://example.invalid/"),
        "target_urls": _strlist(c.get("example_urls")),
        "access_status": access, "legal_status": legal, "blocker_type": blocker,
        "observed_blocker": _str(c.get("observed_blocker"), "access appears blocked"),
        "automated_attempts": [], "requested_human_actions": [action], "requested_actions_notes": None,
        "human_review": {"review_status": "not_reviewed", "reviewer": None, "reviewed_at": None,
                         "review_notes": None, "legal_notes": None, "credentials_notes": None,
                         "redistribution_notes": None},
        "resolution": {"resolution_status": "unresolved", "resolved_at": None, "resolved_by": None,
                       "outcome_summary": None, "linked_uploaded_document_ids": [],
                       "updated_candidate_id": None, "updated_source_id": None,
                       "follow_up_required": False, "follow_up_notes": None},
    }


def expand_negative_finding(n, config, now, fid):
    country, sector, workstream = _scope(config)
    ft = _enum(n.get("finding_type"), NF_TYPES, "no_relevant_results")
    no_local = ft == "local_language_blind_spot"    # waive the local-terms requirement (schema allOf)
    if ft == "unexpanded_pointer_source":
        ft = "no_relevant_results"                  # no pointer ids to satisfy the allOf
    return {
        "finding_id": fid, "finding_status": "open", "finding_type": ft,
        "country": country, "sector": sector, "workstream": workstream,
        "source_class": _enum(n.get("source_class"), CLASS5, "not_applicable"),
        "topics": _topics(n.get("topics")), "language": _lang(n.get("language")),
        "description": _str(n.get("description"), "search did not yield a usable source"),
        "searched_or_tested": {
            "method": _enum(n.get("method"), NF_METHOD, "keyword_search"),
            "queries_used": _strlist(n.get("queries_used")), "urls_checked": [],
            "pointer_source_candidate_ids": [], "pointer_source_urls": [],
            "local_language_terms_used": [], "entities_tested": [], "searched_at": now,
            "no_local_terms_known": no_local,
        },
        "result": {"result_summary": _str(n.get("result_summary"), "no usable result"), "result_count": 0,
                   "candidate_ids_created": [], "source_ids_matched": [], "access_review_task_ids_created": [],
                   "error_messages": [], "artifact_paths": []},
        "why_it_matters": _str(n.get("why_it_matters"), "records the dead end to avoid repeating it"),
        "severity": _enum(n.get("severity"), PRIORITY, "low"), "confidence_score": 0.7,
        "follow_up": {"follow_up_required": n.get("severity") in ("high", "critical"),
                      "recommended_action": "retry_later", "assigned_to": None, "due_at": None,
                      "follow_up_notes": None, "linked_coverage_gap_ids": [], "superseded_by_finding_id": None},
    }


def expand_coverage_gap(g, config, gid):
    country, sector, workstream = _scope(config)
    return {
        "gap_id": gid, "gap_status": "open",
        "gap_type": _enum(g.get("gap_type"), GAP_TYPES, "unknown"),
        "coverage_dimension": _enum(g.get("coverage_dimension"), GAP_DIMS, "source_class"),
        "severity": _enum(g.get("severity"), PRIORITY, "medium"), "confidence_score": 0.7,
        "country": country, "sector": sector, "workstream": workstream,
        "topics": _topics(g.get("topics")), "source_class": _enum(g.get("source_class"), CLASS5, "not_applicable"),
        "language": _lang(g.get("language")),
        "description": _str(g.get("description"), "coverage weakness identified"),
        "why_it_matters": _str(g.get("why_it_matters"), "affects coverage completeness"),
        "basis": {"linked_negative_finding_ids": [], "linked_candidate_ids": [], "linked_source_ids": [],
                  "linked_access_review_task_ids": [], "example_urls": []},
        "follow_up": {"follow_up_required": True,
                      "recommended_action": _enum(g.get("recommended_action"), GAP_ACTIONS, "find_alternative_sources"),
                      "assigned_to": None, "due_at": None, "follow_up_notes": None},
        "resolution": {"resolution_ref": None, "resolution_reason": None, "resolved_at": None,
                       "resolved_by": None, "superseded_by_gap_id": None},
    }


def _derive_search_summary(search_attempts, failed_searches, candidates):
    sa = [a for a in search_attempts if isinstance(a, dict)]
    eng = sum(1 for a in sa if str(a.get("language", "")).lower().startswith("en"))
    return {"queries_run": len(sa), "english_queries": eng, "local_language_queries": len(sa) - eng,
            "failed_searches": len([f for f in failed_searches if isinstance(f, dict)]),
            "pointer_sources_found": sum(1 for c in candidates if c["source_class"] == "pointer"),
            "pointer_sources_expanded": 0, "urls_verified": 0, "urls_failed": 0}


def normalize_scout_output(compact, config, *, now, id_prefix="c"):
    """Expand a compact scout output into the full scout_output dict the runner ingests.

    Deterministic and TOTAL: any odd input (non-dict compact, wrong-typed keys/values) is coerced to a
    safe default rather than raised. Non-dict record entries are skipped; ids are assigned stably so a
    blocked candidate and its generated AccessReviewTask stay linked (both keyed on the same index)."""
    if not isinstance(compact, dict):
        compact = {}
    raw_c = [c for c in _as_list(compact.get("candidates")) if isinstance(c, dict)]
    candidates, tasks = [], []
    for i, c in enumerate(raw_c, 1):
        cid = f"{id_prefix}_{i:03d}"
        cand = expand_candidate(c, config, now, cid)
        if c.get("blocked"):
            tid = f"art_{i:03d}"
            cand["access_review_task_id"] = tid
            tasks.append(expand_access_task(c, config, cid, tid))
        candidates.append(cand)

    negs = [expand_negative_finding(n, config, now, f"nf_{i:03d}")
            for i, n in enumerate([x for x in _as_list(compact.get("negative_findings")) if isinstance(x, dict)], 1)]
    gaps = [expand_coverage_gap(g, config, f"cg_{i:03d}")
            for i, g in enumerate([x for x in _as_list(compact.get("coverage_gaps")) if isinstance(x, dict)], 1)]

    search_attempts = [a for a in _as_list(compact.get("search_attempts")) if isinstance(a, dict)]
    failed_searches = [f for f in _as_list(compact.get("failed_searches")) if isinstance(f, dict)]

    briefs = compact.get("briefs")
    if not isinstance(briefs, list):
        briefs = [compact["brief"]] if isinstance(compact.get("brief"), str) else []
    brief_md = "\n\n".join(b for b in briefs if isinstance(b, str))

    return {
        "source_candidates": candidates,
        "access_review_tasks": tasks,
        "negative_findings": negs,
        "coverage_gaps": gaps,
        "search_summary": _derive_search_summary(search_attempts, failed_searches, candidates),
        "glossary": _as_list(compact.get("glossary")),
        "actors": _as_list(compact.get("actors")),
        "search_attempts": search_attempts,
        "failed_searches": failed_searches,
        "errors": _as_list(compact.get("errors")),
        "raw_traces": _as_list(compact.get("raw_traces")),
        "discovered_source_categories": _as_list(compact.get("discovered_source_categories")),
        "workstream_brief": brief_md,
    }
