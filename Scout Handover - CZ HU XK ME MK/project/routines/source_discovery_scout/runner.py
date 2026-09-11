"""Source Discovery Scout (R2) runner skeleton — the deterministic guardrail around the scout.

This is the EXECUTION HARNESS, not scout intelligence. Per docs/source_discovery_scout_routine.md
the scout is "imaginative in discovery, strict in storage": Claude drafts record CONTENT; the
deterministic runner (this file) owns URL-verification init, dedup flags, counts, schema
validation, run-manifest assembly, and persistence. In this skeleton the scout's output is
supplied by a STUB adapter (no live web search); a real adapter would call Claude + web search and
return the identical `scout_output` shape.

Responsibilities implemented here:
  1-2. load a discovery-run config + the routine prompt and referenced playbooks
  3.   create a discovery_run_id
  4.   assemble a DiscoveryRunManifest
  5.   accept scout output from a stubbed/fixture adapter
  6.   validate every emitted object against its schema (SourceCandidate/AccessReviewTask/
       NegativeFinding/CoverageGap/DiscoveryRunManifest)
  7.   write valid records to the correct data/ folders (one folder <-> one schema)
  8.   write invalid records to a rejected artifact WITH their validation errors
  9.   compute manifest OUTPUT counts deterministically from the actual written records
  10.  enforce that every emitted record's discovery_run_id matches the run (mismatch => rejected)
  11.  initialize runner-owned fields: url_verification.status=not_checked, dedupe_status=not_checked,
       and FORCE a globally-unique candidate_id (identity is runner-owned, never trusted -- see
       _scope_candidate_id)
  12.  NEVER promote sources and NEVER write to the Source Registry (this module imports no
       promotion code and touches no data/source_registry path).

Self-contained: stdlib + jsonschema only. It deliberately does NOT import the `promotion` package.
"""
import copy
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from jsonschema import Draft202012Validator, FormatChecker

_REPO_ROOT = str(Path(__file__).resolve().parents[2])
_SAMPLE_TS = "2026-07-03T09:00:00Z"   # timestamp used only by the sample/stub record builders

# scout_output key -> (schema name, id field, id prefix, data/ folder). Insertion order = the
# deterministic processing/reporting order.
_RECORD_TYPES = {
    "source_candidates":   {"schema": "source_candidate",   "id_field": "candidate_id", "id_prefix": "cand", "folder": "source_candidates"},
    "access_review_tasks": {"schema": "access_review_task", "id_field": "task_id",      "id_prefix": "art",  "folder": "access_review_tasks"},
    "negative_findings":   {"schema": "negative_finding",   "id_field": "finding_id",   "id_prefix": "nf",   "folder": "negative_findings"},
    "coverage_gaps":       {"schema": "coverage_gap",       "id_field": "gap_id",       "id_prefix": "cg",   "folder": "coverage_gaps"},
}

_SCHEMA_FILES = {
    "source_candidate":       "source_candidate.schema.json",
    "access_review_task":     "access_review_task.schema.json",
    "negative_finding":       "negative_finding.schema.json",
    "coverage_gap":           "coverage_gap.schema.json",
    "discovery_run_manifest": "discovery_run_manifest.schema.json",
}

_RUN_LOG_REF_KEYS = ["search_attempts_ref", "failed_searches_ref", "errors_ref", "raw_traces_ref",
                     "glossary_ref", "discovered_source_categories_ref", "workstream_brief_ref"]

# The canonical runner-initialized url_verification (the scout must NEVER assert 'verified').
_NOT_CHECKED_UV = {"status": "not_checked", "verified_at": None, "http_status": None,
                   "final_url": None, "error_message": None, "checked_by": None}


# ---- small utilities -------------------------------------------------------

def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mint(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _scope_candidate_id(run_id, cid):
    """Namespace a candidate id with its run so it is GLOBALLY unique. IDEMPOTENT + TOTAL.

    The scout numbers its finds per-run (c_001, c_002, ...) and restarts at 1 on EVERY run, so the raw
    id is unique only within a run and collides ACROSS runs. candidate_id is the SourceCandidate's
    identity in a global, cross-run keyed store (the registry's candidate table is keyed on it), so a
    later run's `c_001` resolved to an EARLIER run's already-promoted candidate: gate G4_not_promoted
    failed and the new source was silently dropped as no_op "already promoted". Identity is therefore
    RUNNER-OWNED -- forced, never trusted -- exactly like discovery_run_id / canonical_url /
    url_verification / dedupe.
    """
    if not isinstance(cid, str) or not cid:
        return cid
    prefix = f"{run_id}__"
    return cid if cid.startswith(prefix) else prefix + cid


def _remap_candidate_ids(obj, fn):
    """Rewrite EVERY candidate-id-bearing field through `fn`, recursively, so the in-run cross-references
    survive re-identification: AccessReviewTask.candidate_id, CoverageGap.basis.linked_candidate_ids,
    NegativeFinding.attempt.candidate_ids_created / .pointer_source_candidate_ids, and
    SourceCandidate.dedupe.possible_duplicate_candidate_ids. Matches any key CONTAINING 'candidate_id'.
    TOTAL: a value that is not a str (or a list of str) passes through untouched."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str) and "candidate_id" in k:
                if isinstance(v, str):
                    out[k] = fn(v)
                    continue
                if isinstance(v, list):
                    out[k] = [fn(x) if isinstance(x, str) else x for x in v]
                    continue
            out[k] = _remap_candidate_ids(v, fn)
        return out
    if isinstance(obj, list):
        return [_remap_candidate_ids(x, fn) for x in obj]
    return obj


def _dumps(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _dumps_log(obj):
    """Lenient serializer for FREE-FORM run-log / rejected payloads (never schema-validated): a
    non-JSON-native value (datetime, set, bytes, ...) is stringified via default=str rather than
    raising and aborting the run before the manifest is written."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


# ---- config + prompt/playbook loading (responsibilities 1-2) ---------------

def _parse_scalar(s):
    s = s.strip()
    if s in ("", "null", "~", "None"):
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _parse_value(val):
    """Parse an inline value: a flow list `[a, b, c]` or a scalar."""
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        return [] if inner == "" else [_parse_scalar(x) for x in inner.split(",")]
    return _parse_scalar(val)


def _load_flat_yaml(text):
    """Minimal loader for the controlled config subset: `key: scalar`, `key: [a, b, c]`, and ONE
    level of nesting (a bare `key:` with 2-space-indented `subkey: value` children, e.g.
    `url_verification:` / `  enabled: false`). No block sequences. Used only when PyYAML is absent.
    NOTE: a top-level `key:` with an empty value starts a nested block (it is not treated as null)."""
    data = {}
    current = None                          # the top-level key currently accepting nested children
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        indent = len(raw) - len(raw.lstrip())
        key, _, val = raw.strip().partition(":")
        key = key.strip()
        if "#" in val:                      # strip inline comment (no '#' occurs inside values here)
            val = val[:val.index("#")]
        val = val.strip()
        if indent >= 2 and current is not None:
            data[current][key] = _parse_value(val)
            continue
        current = None
        if val == "":                       # a bare `key:` opens a one-level nested map
            data[key] = {}
            current = key
        else:
            data[key] = _parse_value(val)
    return data


def load_config(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml   # optional; preferred when installed
        cfg = yaml.safe_load(text)
    except ImportError:
        cfg = _load_flat_yaml(text)
    if not isinstance(cfg, dict):
        raise ValueError(f"config {path} did not parse to a mapping")
    for req in ("country", "sector", "workstreams", "topics", "languages"):
        if not cfg.get(req):
            raise ValueError(f"config {path} missing required key '{req}'")
    return cfg


def load_prompt_and_playbooks(config, repo_root=_REPO_ROOT):
    prompt_path = config.get("prompt_path")
    if not prompt_path:
        raise ValueError("config missing 'prompt_path'")
    prompt = (Path(repo_root) / prompt_path).read_text(encoding="utf-8")
    playbooks = {}
    for rel in (config.get("playbooks") or []):
        p = Path(repo_root) / rel
        if not p.exists():
            raise FileNotFoundError(f"referenced playbook not found: {rel}")
        playbooks[rel] = p.read_text(encoding="utf-8")
    return {"prompt": prompt, "playbooks": playbooks}


# ---- schema validation (self-contained; no promotion coupling) -------------

def load_validators(schemas_dir):
    fc = FormatChecker()
    out = {}
    for name, fn in _SCHEMA_FILES.items():
        schema = json.loads((Path(schemas_dir) / fn).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        out[name] = Draft202012Validator(schema, format_checker=fc)
    return out


def validate_record(validators, name, record):
    """Return a list of human-readable error strings (empty list == valid)."""
    errs = sorted(validators[name].iter_errors(record), key=lambda e: list(e.path))
    return [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errs[:8]]


# ---- deterministic URL normalization / verification / dedupe ---------------

_DEFAULT_PORTS = {"http": "80", "https": "443"}


def normalize_url(url):
    """Return a canonical URL string, or None for a URL we refuse to canonicalize (fail closed).

    Deterministic canonicalization: lowercase scheme + host, drop userinfo, drop the default port,
    remove the fragment, empty path -> '/'. It PRESERVES the query and any non-root path verbatim
    (including non-root trailing slashes) -- 'normalize trailing slash where safe' is applied only
    to the root, since '/a' vs '/a/' can differ on real servers. Fails closed (None) for a non-string,
    empty, non-http(s), or host-less URL."""
    if not isinstance(url, str) or not url.strip():
        return None
    try:
        parts = urlsplit(url.strip())
        host = parts.hostname
        port = parts.port          # .hostname and .port are parsed LAZILY here; a bad/out-of-range
    except ValueError:             # port raises ValueError on access -> fail closed, not crash
        return None
    scheme = parts.scheme.lower()
    if scheme not in ("http", "https") or not host:
        return None
    host = host.lower()
    if ":" in host:                          # IPv6 literal -> re-bracket
        host = f"[{host}]"
    netloc = host
    if port is not None and str(port) != _DEFAULT_PORTS.get(scheme):
        netloc = f"{host}:{port}"
    path = parts.path or "/"
    return urlunsplit((scheme, netloc, path, parts.query, ""))   # fragment dropped


def _uv(status, *, verified_at=None, http_status=None, final_url=None, error_message=None, checked_by=None):
    return {"status": status, "verified_at": verified_at, "http_status": http_status,
            "final_url": final_url, "error_message": error_message, "checked_by": checked_by}


def verify_candidate_url(url, verifier, now):
    """Runner-owned URL verification -> a url_verification dict. Fails CLOSED to 'failed' on an
    un-normalizable URL, a missing verifier, or any verifier error. The scout can never set 'verified'
    -- only this deterministic path does, and only when the injected verifier reports reachable."""
    checked_by = getattr(verifier, "checked_by", "url_verifier") if verifier is not None else "url_verifier"
    canon = normalize_url(url)
    if canon is None:
        return _uv("failed", error_message=f"invalid or non-http(s) URL: {url!r}", checked_by=checked_by)
    if verifier is None:
        return _uv("failed", error_message="url verification enabled but no verifier configured",
                   checked_by=checked_by)
    try:
        res = verifier.check(canon)
    except Exception as e:  # noqa: BLE001 - a misbehaving verifier must not crash the run
        return _uv("failed", error_message=f"verifier error: {e}", checked_by=checked_by)
    if res.get("reachable"):
        return _uv("verified", verified_at=now, http_status=res.get("http_status"),
                   final_url=res.get("final_url") or canon, checked_by=checked_by)
    return _uv("failed", http_status=res.get("http_status"), final_url=res.get("final_url"),
               error_message=res.get("error") or "unreachable", checked_by=checked_by)


class HttpUrlVerifier:
    """The live (network) verifier, isolated behind this seam -- NOT used by tests (which inject a
    mock) and NOT used by the default offline config. Best-effort HEAD via stdlib urllib."""
    checked_by = "http_url_verifier/urllib"

    def __init__(self, timeout=10):
        self.timeout = timeout

    def check(self, url):
        import urllib.request
        import urllib.error
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "printec-scout-runner/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return {"reachable": True, "http_status": getattr(resp, "status", None),
                        "final_url": resp.geturl(), "error": None}
        except urllib.error.HTTPError as e:
            return {"reachable": 200 <= e.code < 400, "http_status": e.code,
                    "final_url": url, "error": f"HTTP {e.code}"}
        except Exception as e:  # noqa: BLE001
            return {"reachable": False, "http_status": None, "final_url": None, "error": str(e)}


def _dedupe_survivor_key(c):
    """Sort key electing the canonical survivor of a same-URL group: highest (credibility, usefulness)
    score, with candidate_id as the deterministic tiebreak. `min()` over this key picks the survivor."""
    def num(v):
        return v if isinstance(v, (int, float)) and not isinstance(v, bool) else -1.0
    return (-num(c.get("credibility_score")), -num(c.get("usefulness_score")), str(c.get("candidate_id")))


def compute_dedupe(candidates):
    """Deterministic within-run dedupe by normalized canonical_url. Mutates each candidate's `dedupe`
    (dedupe_status + possible_duplicate_candidate_ids) in place. Does NOT compare against the Source
    Registry and makes NO promotion/merge decision. Only dedupe fields change (both enum values are
    schema-valid), so callers may run this AFTER validation without re-validating.

    Invariant: EXACTLY ONE representative per URL, never zero. Within a same-URL group one canonical
    survivor stays `unique` (highest (credibility, usefulness) score; candidate_id tiebreak); the rest are
    `duplicate` and point at the survivor. (Marking every member `duplicate` would leave the group with no
    promotable candidate — promote_new's G3 requires `unique` — and silently drop the source.)"""
    groups = {}
    for c in candidates:
        groups.setdefault(c.get("canonical_url"), []).append(c)
    for group in groups.values():
        if len(group) == 1:
            dd = group[0]["dedupe"]
            dd["dedupe_status"] = "unique"
            dd["possible_duplicate_candidate_ids"] = []
        else:
            survivor_id = min(group, key=_dedupe_survivor_key)["candidate_id"]
            for c in group:
                dd = c["dedupe"]
                if c["candidate_id"] == survivor_id:
                    dd["dedupe_status"] = "unique"
                    dd["possible_duplicate_candidate_ids"] = []
                else:
                    dd["dedupe_status"] = "duplicate"
                    dd["possible_duplicate_candidate_ids"] = [survivor_id]   # the canonical to merge into


def _cfg_flag(config, section, key, default):
    """Read config[section][key] as a bool; fall back to `default` if the section/key is absent."""
    sect = config.get(section)
    if isinstance(sect, dict) and isinstance(sect.get(key), bool):
        return sect[key]
    return default


# ---- discovery_run_id (responsibility 3) -----------------------------------

def new_run_id(config, now):
    ws = "-".join(config.get("workstreams") or [])
    compact = "".join(ch for ch in (now or "") if ch.isalnum())
    return f"dr_{config.get('country', 'ZZ')}_{ws}_{compact}_{uuid.uuid4().hex[:8]}"


# ---- scout adapter (responsibility 5; LLM/web isolated behind this seam) ----

class ScoutAdapter:
    """Isolation boundary for the scout worker. In this skeleton there is NO live web search;
    a live adapter would call Claude + web search and return the SAME scout_output shape:
    {source_candidates, access_review_tasks, negative_findings, coverage_gaps,
     search_summary, glossary_summary, discovered_source_categories, run_log_refs}."""

    def generate(self, config, prompt, playbooks):
        raise NotImplementedError


class StubScoutAdapter(ScoutAdapter):
    """Deterministic placeholder so the harness runs end-to-end without an LLM."""

    def generate(self, config, prompt, playbooks):
        return stub_scout_output(config)


# ---- sample/stub record builders (valid record BODIES the scout would draft) ----
# These omit runner-owned bookkeeping (discovery_run_id, created_at/updated_at, and — for a
# candidate — url_verification); the runner fills those. Tests reuse these as a valid baseline.

def sample_candidate(config, cid="c1", **over):
    base = f"https://{cid}.example.gr"
    rec = {
        "candidate_id": cid,
        "lifecycle_status": "discovered",
        "source_name": f"Source {cid}",
        "source_url": base,
        "canonical_url": base + "/",
        "domain": f"{cid}.example.gr",
        "country": config["country"],
        "sector": config["sector"],
        "workstream": config["workstreams"][0],
        "source_class": "direct",
        "source_subtype": "procurement_portal",
        "primary_language": config["languages"][0],
        "topics": list(config["topics"]),
        "access_status": "public",
        "legal_status": "allowed",
        "collection_allowed": True,
        "suggested_collection_method": "static_html",
        "credibility_score": 0.8,
        "usefulness_score": 0.7,
        "confidence_score": 0.6,
        "priority": "medium",
        "discovery_basis": {
            "why_relevant": "publishes public procurement notices",
            "observed_source_behavior": "", "expected_information_value": "",
            "known_limitations": "", "example_urls": [], "sample_evidence_snippets": [],
        },
        "discovered_via": {
            "method": "keyword_search", "queries_used": [], "pointer_source_candidate_ids": [],
            "pointer_source_urls": [], "local_language_terms_used": [], "discovered_at": _SAMPLE_TS,
        },
        "dedupe": {"dedupe_status": "not_checked", "possible_duplicate_candidate_ids": [],
                   "possible_duplicate_source_ids": [], "canonicalization_notes": None},
        "review": {"review_status": "not_reviewed", "reviewer": None, "reviewed_at": None,
                   "review_notes": None, "rejection_reason": None, "human_review_required": False},
        "promotion": {"promotion_status": "not_promoted", "promoted_source_id": None,
                      "promoted_at": None, "promotion_notes": None},
        # url_verification intentionally omitted -> the runner initializes it (responsibility 11)
    }
    rec.update(over)
    return rec


def sample_access_task(config, tid="t1", candidate_id="c2", **over):
    base = f"https://{candidate_id}.example.gr"
    rec = {
        "task_id": tid,
        "candidate_id": candidate_id,
        "task_status": "open",
        "priority": "high",
        "country": config["country"],
        "sector": config["sector"],
        "workstream": config["workstreams"][0],
        "source_name": f"Source {candidate_id}",
        "source_url": base,
        "target_urls": [],
        "access_status": "requires_free_account",
        "legal_status": "allowed",
        "blocker_type": "free_registration_required",
        "observed_blocker": "a free account signup blocks the report list",
        "automated_attempts": [],
        "requested_human_actions": ["create_free_account_if_allowed"],
        "requested_actions_notes": None,
        "human_review": {"review_status": "not_reviewed", "reviewer": None, "reviewed_at": None,
                         "review_notes": None, "legal_notes": None, "credentials_notes": None,
                         "redistribution_notes": None},
        "resolution": {"resolution_status": "unresolved", "resolved_at": None, "resolved_by": None,
                       "outcome_summary": None, "linked_uploaded_document_ids": [],
                       "updated_candidate_id": None, "updated_source_id": None,
                       "follow_up_required": False, "follow_up_notes": None},
    }
    rec.update(over)
    return rec


def sample_negative_finding(config, fid="n1", **over):
    rec = {
        "finding_id": fid,
        "finding_status": "open",
        "finding_type": "searched_no_result",
        "country": config["country"],
        "sector": config["sector"],
        "workstream": config["workstreams"][0],
        "source_class": "not_applicable",
        "topics": list(config["topics"]),
        "language": config["languages"][0],
        "description": "search ran but returned zero results",
        "searched_or_tested": {
            "method": "keyword_search", "queries_used": ["public procurement portal"],
            "urls_checked": [], "pointer_source_candidate_ids": [], "pointer_source_urls": [],
            "local_language_terms_used": [], "entities_tested": [], "searched_at": _SAMPLE_TS,
            "no_local_terms_known": False,
        },
        "result": {"result_summary": "no results returned", "result_count": 0,
                   "candidate_ids_created": [], "source_ids_matched": [],
                   "access_review_task_ids_created": [], "error_messages": [], "artifact_paths": []},
        "why_it_matters": "records the dead end so the same query is not repeated",
        "severity": "low",
        "confidence_score": 0.8,
        "follow_up": {"follow_up_required": False, "recommended_action": "retry_later",
                      "assigned_to": None, "due_at": None, "follow_up_notes": None,
                      "linked_coverage_gap_ids": [], "superseded_by_finding_id": None},
    }
    rec.update(over)
    return rec


def sample_coverage_gap(config, gid="g1", **over):
    rec = {
        "gap_id": gid,
        "gap_status": "open",
        "gap_type": "missing",
        "coverage_dimension": "source_class",
        "severity": "medium",
        "confidence_score": 0.7,
        "country": config["country"],
        "sector": config["sector"],
        "workstream": config["workstreams"][0],
        "topics": list(config["topics"]),
        "source_class": "direct",
        "language": config["languages"][0],
        "description": "no direct-procurement visibility for private systemic banks",
        "why_it_matters": "a coverage blind spot that would hide procurement activity",
        "basis": {"linked_negative_finding_ids": [], "linked_candidate_ids": [],
                  "linked_source_ids": [], "linked_access_review_task_ids": [], "example_urls": []},
        "follow_up": {"follow_up_required": True, "recommended_action": "find_alternative_sources",
                      "assigned_to": None, "due_at": None, "follow_up_notes": None},
        "resolution": {"resolution_ref": None, "resolution_reason": None, "resolved_at": None,
                       "resolved_by": None, "superseded_by_gap_id": None},
    }
    rec.update(over)
    return rec


def sample_search_summary(**over):
    s = {"queries_run": 4, "english_queries": 2, "local_language_queries": 2, "failed_searches": 0,
         "pointer_sources_found": 1, "pointer_sources_expanded": 0, "urls_verified": 0, "urls_failed": 0}
    s.update(over)
    return s


def sample_glossary():
    """A sample glossary log: term entries with a tag and a validated flag."""
    return [
        {"term": "ΕΣΗΔΗΣ", "tag": "official", "validated": True},
        {"term": "ΚΗΜΔΗΣ", "tag": "acronym_alias", "validated": True},
        {"term": "διαγωνισμός", "tag": "common_search", "validated": False},
        {"term": "tender", "tag": "english_in_local", "validated": True},
        {"term": "προμήθεια", "tag": "noisy_risky", "validated": True},
    ]


def sample_actors():
    return ["Bank of Greece", "Hellenic Bank Association", "ATHEX", "ESIDIS portal operator"]


def sample_run_logs():
    """Sample raw run-log payloads (free-form logs, NOT schema-validated records)."""
    return {
        "glossary": sample_glossary(),
        "actors": sample_actors(),
        "search_attempts": [
            {"query": "greece public procurement portal", "language": "en"},
            {"query": "δημόσιοι διαγωνισμοί τραπεζών", "language": "el"},
        ],
        "failed_searches": [],
        "errors": [],
        "raw_traces": [],
        "discovered_source_categories": [
            {"category": "central_bank_tenders", "candidate_count": 1},
            {"category": "vendor_pressrooms", "candidate_count": 1},
            {"category": "athex_disclosures", "candidate_count": 0},
        ],
        "workstream_brief": ("# Greece / A2 — Tenders & Procurement\n\n"
                             "Systemic banks are private, so their procurement bypasses public portals; "
                             "only the Bank of Greece publishes real tenders.\n"),
    }


def stub_scout_output(config):
    """A minimal, schema-valid scout output: the four record types + the raw run-log payloads.
    glossary_summary and the discovered-category COUNT are DERIVED by the runner from these logs,
    not supplied here (so the manifest numbers can never be inflated by the scout)."""
    out = {
        "source_candidates": [
            sample_candidate(config, "c1"),
            sample_candidate(config, "c2", source_name="Blocked Source c2",
                             access_status="requires_free_account"),
        ],
        "access_review_tasks": [sample_access_task(config, "t1", "c2")],
        "negative_findings": [sample_negative_finding(config, "n1")],
        "coverage_gaps": [sample_coverage_gap(config, "g1")],
        "search_summary": sample_search_summary(),
    }
    out.update(sample_run_logs())
    return out


# ---- normalization + validation (responsibilities 6, 10, 11) ---------------

def _prepare_record(spec, rec, run_id, now):
    """Bookkeeping normalization common to every record type: reject a non-dict; enforce
    discovery_run_id (stamp when absent, ACCEPT when equal, REJECT on mismatch -- never silently
    overwrite a cross-run value); mint an id if absent; stamp timestamps. Returns
    (normalized_record, error_or_None)."""
    if not isinstance(rec, dict):
        return rec, "record is not a JSON object"
    norm = copy.deepcopy(rec)
    drid = norm.get("discovery_run_id")
    if drid is not None and drid != run_id:
        return norm, f"discovery_run_id mismatch: record has '{drid}', run is '{run_id}'"
    norm["discovery_run_id"] = run_id
    idf = spec["id_field"]
    if not norm.get(idf):
        norm[idf] = _mint(spec["id_prefix"])
    norm.setdefault("created_at", now)
    norm["updated_at"] = now
    return norm, None


def _apply_candidate_url_fields(norm, uv_enabled, verifier, now):
    """Set the runner-owned URL fields on a SourceCandidate (responsibility 11), FORCED not trusted:
    compute canonical_url from source_url; leave dedupe_status neutral (set later by compute_dedupe);
    and set url_verification -- not_checked when verification is disabled, else the deterministic
    verifier result (never a scout-asserted 'verified')."""
    src = norm.get("source_url")
    canon = normalize_url(src)
    # canonical_url is FULLY runner-owned and drives dedupe, so it must NEVER be the scout-supplied
    # value: use the normalized form when normalizable, else the raw source_url. (If source_url is
    # absent/empty this yields a value the schema rejects -> the candidate fails closed. Two distinct
    # source_urls therefore never collapse into one dedupe group.)
    norm["canonical_url"] = canon if canon is not None else src

    dd = norm.get("dedupe")
    if not isinstance(dd, dict):
        dd = {}
    dd.setdefault("possible_duplicate_candidate_ids", [])
    dd.setdefault("possible_duplicate_source_ids", [])
    dd["canonicalization_notes"] = ("normalized from source_url" if canon is not None
                                    else "source_url not normalizable; canonical_url = raw source_url")
    dd["dedupe_status"] = "not_checked"
    norm["dedupe"] = dd

    if not uv_enabled:
        norm["url_verification"] = copy.deepcopy(_NOT_CHECKED_UV)
    else:
        norm["url_verification"] = verify_candidate_url(src, verifier, now)


# ---- run-log artifacts + derived summaries (audit scaffolding) -------------

_GLOSSARY_TAGS = ("official", "common_search", "english_in_local", "acronym_alias", "noisy_risky")

# (scout_output key, filename under run_logs/<run_id>/, run_log_refs key or None, format).
_RUN_LOG_ARTIFACTS = [
    ("glossary", "glossary.jsonl", "glossary_ref", "jsonl"),
    ("actors", "actors.jsonl", None, "jsonl"),                          # counted into glossary_summary; no ref slot
    ("search_attempts", "search_attempts.jsonl", "search_attempts_ref", "jsonl"),
    ("failed_searches", "failed_searches.jsonl", "failed_searches_ref", "jsonl"),
    ("errors", "errors.jsonl", "errors_ref", "jsonl"),
    ("raw_traces", "raw_traces.jsonl", "raw_traces_ref", "jsonl"),
    ("discovered_source_categories", "discovered_source_categories.jsonl",
     "discovered_source_categories_ref", "jsonl"),
    ("workstream_brief", "workstream_brief.md", "workstream_brief_ref", "md"),
]


def _as_list(x):
    return x if isinstance(x, list) else []


def _derive_glossary_summary(scout_output):
    """RE-COUNT the glossary_summary deterministically from the raw glossary/actors logs (never
    trusting a scout-asserted summary): terms_total, terms_validated, per-tag counts, actors."""
    by_tag = {t: 0 for t in _GLOSSARY_TAGS}
    validated = 0
    glossary = _as_list(scout_output.get("glossary"))
    for e in glossary:
        if not isinstance(e, dict):
            continue
        tag = e.get("tag")
        if isinstance(tag, str) and tag in by_tag:   # isinstance guard: a list/dict tag is unhashable
            by_tag[tag] += 1
        if e.get("validated") is True:
            validated += 1
    return {"terms_total": len(glossary), "terms_validated": validated,
            "terms_by_tag": by_tag, "actors_identified": len(_as_list(scout_output.get("actors")))}


def _write_run_logs(run_log_dir, run_id, scout_output):
    """Persist the run's free-form work-log artifacts and return the run_log_refs index. Each log is
    written only when the scout produced a non-empty payload; otherwise a stale file from a prior
    same-run_id run is removed and its ref stays null (so the folder mirrors this run)."""
    refs = {k: None for k in _RUN_LOG_REF_KEYS}
    for key, fname, ref_key, fmt in _RUN_LOG_ARTIFACTS:
        payload = scout_output.get(key)
        fpath = run_log_dir / fname
        produced = False
        if fmt == "md":
            if isinstance(payload, str) and payload.strip():
                fpath.write_text(payload, encoding="utf-8")
                produced = True
        else:
            items = _as_list(payload)
            if items:
                fpath.write_text("".join(_dumps_log(x) + "\n" for x in items), encoding="utf-8")
                produced = True
        if not produced:
            fpath.unlink(missing_ok=True)
        if produced and ref_key:
            refs[ref_key] = f"run_logs/{run_id}/{fname}"
    return refs


# ---- manifest assembly (responsibilities 4, 9) -----------------------------

def _build_manifest(config, scout_output, run_id, now, started_at, actor, written, rejected,
                    run_status, rejected_rel, uv_counts, dedup_applied, run_log_refs):
    outputs = {
        "source_candidates": len(written["source_candidates"]),
        "access_review_tasks": len(written["access_review_tasks"]),
        "negative_findings": len(written["negative_findings"]),
        "coverage_gaps": len(written["coverage_gaps"]),
        # RE-COUNTED by the runner from the discovered_source_categories log (never scout-asserted).
        "discovered_source_categories": len(_as_list(scout_output.get("discovered_source_categories"))),
    }

    # search_summary is scout-REPORTED, EXCEPT urls_verified/urls_failed which are RUNNER-owned
    # counts (routine doc §8/§10/§14: "counts are runner-computed, never LLM-asserted"). Override them
    # with the runner's actual verification tally (0/0 when verification is disabled), never trusting
    # a scout-asserted count. A missing/non-dict summary is left as-is so the manifest schema rejects
    # it (-> failed run) instead of the runner crashing.
    search_summary = scout_output.get("search_summary")
    if isinstance(search_summary, dict):
        search_summary = dict(search_summary)
        search_summary["urls_verified"] = uv_counts["verified"]
        search_summary["urls_failed"] = uv_counts["failed"]

    manifest = {
        "discovery_run_id": run_id,
        "routine": {
            "routine_id": config.get("routine_id", "R2"),
            "routine_name": config.get("routine_name", "source_discovery_scout"),
            "routine_version": config.get("routine_version", "0.0.0"),
        },
        "actor": actor,
        "created_at": now,
        "started_at": started_at,
        "completed_at": now,
        "run_status": run_status,
        "failure_reason": None,
        "scope": {
            "country": config["country"],
            "country_name": config.get("country_name"),
            "sector": config["sector"],
            "workstreams": list(config["workstreams"]),
            "topics": list(config["topics"]),
            "languages": list(config["languages"]),
        },
        "glossary_summary": _derive_glossary_summary(scout_output),   # RE-COUNTED from the glossary log
        "search_summary": search_summary,
        "outputs": outputs,
        "run_log_refs": run_log_refs,
        "validation": {
            "all_outputs_schema_valid": (len(rejected) == 0),
            "validation_errors": len(rejected),
            "dedup_by_normalized_url_applied": bool(dedup_applied),
        },
    }
    # Rejected records are a runner artifact (not a scout run-log), referenced via metadata so the
    # manifest still indexes them; errors_ref is reserved for the scout's own errors log.
    if rejected_rel is not None:
        manifest["metadata"] = {"rejected_records_ref": rejected_rel}
    return manifest


# ---- core execution (responsibilities 6-11) --------------------------------

def execute_run(config, scout_output, *, run_id, now, data_root, schemas_dir=None,
                validators=None, actor=None, started_at=None, verifier=None):
    """Normalize, (verify + dedupe), validate, persist scout_output and assemble the manifest.
    Returns a result dict. NEVER promotes and NEVER writes to data/source_registry.

    URL verification and dedupe are deterministic, runner-owned, and gated by config flags
    (url_verification.enabled / dedupe.enabled; both default OFF, so status stays not_checked unless
    explicitly enabled). Verification uses the injected `verifier` (fails closed to 'failed' when
    enabled but no verifier is supplied); it never lets the scout assert 'verified'."""
    if validators is None:
        if schemas_dir is None:
            raise ValueError("execute_run needs schemas_dir or validators")
        validators = load_validators(schemas_dir)
    actor = actor or {"actor_type": "workflow", "actor_id": "source_discovery_scout_runner",
                      "human_actor_id": None}
    started_at = started_at or now
    data_root = Path(data_root)
    uv_enabled = _cfg_flag(config, "url_verification", "enabled", False)
    dd_enabled = _cfg_flag(config, "dedupe", "enabled", False)

    # Phase 0: FORCE globally-unique candidate identity (responsibility 11). Scout ids restart at c_001
    # every run, so they collide ACROSS runs on the registry's candidate key and a new source gets
    # silently dropped as an "already promoted" no_op. Scope every candidate_id AND every in-run
    # reference to one with the run_id. Idempotent (a re-run/already-scoped id is left alone) + total.
    if isinstance(scout_output, dict):
        scout_output = dict(scout_output)
        for rt in _RECORD_TYPES:
            recs = scout_output.get(rt)
            if isinstance(recs, list):
                scout_output[rt] = [
                    _remap_candidate_ids(r, lambda c: _scope_candidate_id(run_id, c))
                    if isinstance(r, dict) else r
                    for r in recs
                ]

    # Phase 1: bookkeeping normalization; candidates also get canonical_url + url_verification.
    prepared = {rt: [] for rt in _RECORD_TYPES}
    rejected = []
    for rt, spec in _RECORD_TYPES.items():
        for rec in (scout_output.get(rt) or []):
            norm, err = _prepare_record(spec, rec, run_id, now)
            if err:
                rejected.append({"record_type": rt, "errors": [err], "record": norm})
                continue
            if rt == "source_candidates":
                _apply_candidate_url_fields(norm, uv_enabled, verifier, now)
            prepared[rt].append(norm)

    # Phase 2: schema-validate every prepared record -> written / rejected.
    written = {rt: [] for rt in _RECORD_TYPES}
    for rt, spec in _RECORD_TYPES.items():
        for norm in prepared[rt]:
            errs = validate_record(validators, spec["schema"], norm)
            if errs:
                rejected.append({"record_type": rt, "errors": errs, "record": norm})
            else:
                written[rt].append(norm)

    # Verification tally is computed from the WRITTEN candidates (mirroring the outputs counts and
    # dedupe), so the manifest never reports a verification for a record that was schema-rejected.
    uv_counts = {"verified": 0, "failed": 0, "not_checked": 0}
    for c in written["source_candidates"]:
        st = (c.get("url_verification") or {}).get("status")
        if st in uv_counts:
            uv_counts[st] += 1

    # Phase 3: dedupe over the WRITTEN candidates only (mutates schema-valid dedupe fields, so no
    # re-validation is needed). Rejected candidates never influence another candidate's dedupe state.
    if dd_enabled:
        compute_dedupe(written["source_candidates"])

    # (7) persist valid records: one JSONL file per run per type, in the type's own folder
    run_log_dir = data_root / "run_logs" / run_id
    run_log_dir.mkdir(parents=True, exist_ok=True)
    # The per-run file set is authoritative: a type with 0 records this run must NOT keep a stale
    # <run_id>.jsonl from a prior same-run_id run (that would diverge from the manifest counts).
    paths = {}
    for rt, spec in _RECORD_TYPES.items():
        recs = written[rt]
        fpath = data_root / spec["folder"] / f"{run_id}.jsonl"
        if recs:
            fpath.parent.mkdir(parents=True, exist_ok=True)
            fpath.write_text("".join(_dumps(r) + "\n" for r in recs), encoding="utf-8")
            paths[rt] = str(fpath)
        else:
            fpath.unlink(missing_ok=True)
            paths[rt] = None

    # (8) persist invalid records with their validation errors; clear a stale artifact when clean
    rejected_path, rejected_rel = None, None
    if rejected:
        rp = run_log_dir / "rejected.jsonl"
        # rejected records hold untrusted scout content -> lenient serializer (fail closed, not crash)
        rp.write_text("".join(_dumps_log(r) + "\n" for r in rejected), encoding="utf-8")
        rejected_path = str(rp)
        rejected_rel = f"run_logs/{run_id}/rejected.jsonl"
    else:
        (run_log_dir / "rejected.jsonl").unlink(missing_ok=True)

    # Persist the run's free-form work-log artifacts (glossary/searches/errors/categories/brief) and
    # index them in run_log_refs. Deterministic; nothing here is scout-asserted intelligence.
    run_log_refs = _write_run_logs(run_log_dir, run_id, scout_output)

    # (4, 9) manifest with runner-computed counts; validate it against its schema
    run_status = "completed" if not rejected else "completed_with_errors"
    manifest = _build_manifest(config, scout_output, run_id, now, started_at, actor, written,
                               rejected, run_status, rejected_rel, uv_counts, dd_enabled, run_log_refs)
    manifest_errors = validate_record(validators, "discovery_run_manifest", manifest)

    if manifest_errors:
        # A manifest that fails its schema (a run-quality guardrail -- failed searches or zero
        # local-language queries with no NegativeFinding -- or a missing/malformed summary block)
        # is a hard run failure: do NOT emit it as a valid manifest; record it as rejected. Mark the
        # stored copy self-consistently as failed, and clear any stale manifest.json.
        manifest["run_status"] = "failed"
        manifest["failure_reason"] = "manifest failed schema validation: " + "; ".join(manifest_errors[:3])
        mpath = run_log_dir / "manifest_rejected.json"
        mpath.write_text(json.dumps({"manifest": manifest, "validation_errors": manifest_errors},
                                    indent=2, ensure_ascii=False), encoding="utf-8")
        (run_log_dir / "manifest.json").unlink(missing_ok=True)
        final_status, manifest_valid = "failed", False
    else:
        mpath = run_log_dir / "manifest.json"
        mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        (run_log_dir / "manifest_rejected.json").unlink(missing_ok=True)
        final_status, manifest_valid = run_status, True

    return {
        "discovery_run_id": run_id,
        "run_status": final_status,
        "manifest_valid": manifest_valid,
        "manifest_errors": manifest_errors,
        "manifest_path": str(mpath),
        "manifest": manifest,
        "written": {rt: len(written[rt]) for rt in _RECORD_TYPES},
        "rejected": len(rejected),
        "rejected_records": rejected,
        "rejected_path": rejected_path,
        "paths": paths,
        "data_root": str(data_root),
    }


def run(config_path, *, data_root, schemas_dir, adapter=None, run_id=None, now=None,
        actor=None, repo_root=_REPO_ROOT, verifier=None):
    """High-level entry (used by the CLI): load config -> prompt/playbooks -> adapter -> execute.
    When the config enables url_verification and no verifier is injected, uses the live
    HttpUrlVerifier (the only place live network is wired in; the default config keeps it off)."""
    now = now or _now_iso()
    config = load_config(config_path)
    bundle = load_prompt_and_playbooks(config, repo_root)
    adapter = adapter or StubScoutAdapter()
    scout_output = adapter.generate(config, bundle["prompt"], bundle["playbooks"])
    run_id = run_id or new_run_id(config, now)
    validators = load_validators(schemas_dir)
    if verifier is None and _cfg_flag(config, "url_verification", "enabled", False):
        verifier = HttpUrlVerifier()
    return execute_run(config, scout_output, run_id=run_id, now=now, data_root=data_root,
                       validators=validators, actor=actor, verifier=verifier)
