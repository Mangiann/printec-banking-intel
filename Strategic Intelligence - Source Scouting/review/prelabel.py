"""Pre-labeling — a first-pass RECOMMENDATION per new candidate, to speed the human review.

The LLM assistant (orchestrated separately) suggests, per candidate, a decision + a one-line rationale; the
human still confirms/overrides in the sheet. This module is the DETERMINISTIC guardrail around that:
  - `labeling_input(candidates)`  -> the compact per-candidate summaries the assistant labels.
  - `normalize_suggestions(raw, valid_ids)` -> validate/clamp untrusted assistant output (snap the decision
       & priority to allowed values or None; drop suggestions for unknown/hallucinated candidate_ids; one
       per candidate). Pure and TOTAL — never raises on odd input.
  - `heuristic_suggestions(candidates)` -> a deterministic rule-based baseline (offline fallback / test
       baseline). The assistant refines this; both feed the Excel export's suggestion columns.

Suggestions NEVER decide or promote — they only fill the agent-suggestion columns; the human-decision
column is authoritative.
"""
import re

from _safe import dget, sstr

SUGGEST_DECISIONS = {"approve", "reject", "needs_access", "defer"}
PRIORITIES = {"low", "medium", "high", "critical"}
_BLOCKED_ACCESS = {"requires_free_account", "requires_paid_subscription", "requires_manual_download",
                   "requires_credentials", "requires_legal_review", "blocked"}

# --- source ROLE: is this a durable monitoring endpoint, or evidence / a pointer / marginal? ---
SOURCE_ROLES = {"durable_source", "evidence", "pointer", "marginal"}
# a URL whose shape screams "one article" (dated path, long slug, press-release) -> evidence, not a source
_ARTICLE_RE = re.compile(r"(/(?:19|20)\d\d/|press-release|/case-stud|success-stor|/article/|"
                         r"/news/[a-z0-9%-]{20,}|[a-z0-9%-]{45,})")
_POINTER_SUB = ("director", "member", "_list", "catalog", "roster", "portfolio", "registry_of")
_EVIDENCE_SUB = ("case_study", "press_release", "success_story", "customer_case", "customer_story", "_article")


def source_role(c):
    """Deterministic source-role baseline: durable_source | evidence | pointer | marginal. Total (any odd
    input -> 'marginal'). A cheap first pass the LLM/analyst refines — the URL shape + subtype + scores are
    strong signals for 'is this a place that keeps producing signals, or a one-off / a directory'."""
    if not isinstance(c, dict):
        return "marginal"
    url = (c.get("canonical_url") if isinstance(c.get("canonical_url"), str) else "").lower()
    sub = (c.get("source_subtype") if isinstance(c.get("source_subtype"), str) else "").lower()
    if c.get("source_class") == "pointer" or any(k in sub for k in _POINTER_SUB):
        return "pointer"
    if _ARTICLE_RE.search(url) or any(k in sub for k in _EVIDENCE_SUB):
        return "evidence"

    def _num(v):
        return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.5
    if _num(c.get("credibility_score")) + _num(c.get("usefulness_score")) < 0.9:   # both weak
        return "marginal"
    return "durable_source"


# --- the STANDING role method is the LLM labeling pass; this guardrail validates its untrusted output ---
ROLE_VERDICTS = {"keep", "fold_into_parent", "evidence_not_source", "pointer_once", "marginal"}


def normalize_roles(raw, valid_ids):
    """Validate untrusted LLM role verdicts -> {candidate_id: verdict}. Accepts a list or {"verdicts":[...]}.
    Drops unknown/hallucinated candidate_ids and invalid verdicts; first-wins on duplicates. Pure and TOTAL."""
    if isinstance(raw, dict) and "verdicts" in raw:
        raw = raw.get("verdicts")
    items = raw if isinstance(raw, list) else []
    valid = set(valid_ids)
    out = {}
    for v in items:
        if not isinstance(v, dict):
            continue
        cid = v.get("candidate_id")
        if not isinstance(cid, str) or cid not in valid or cid in out:
            continue
        verdict = v.get("verdict")
        if isinstance(verdict, str) and verdict in ROLE_VERDICTS:
            out[cid] = verdict
    return out


def labeling_input(candidates):
    """The compact per-candidate view handed to the labeling assistant."""
    return [{
        "candidate_id": c.get("candidate_id"),
        "source_name": c.get("source_name"),
        "canonical_url": c.get("canonical_url"),
        "source_class": c.get("source_class"),
        "source_subtype": c.get("source_subtype"),
        "access_status": c.get("access_status"),
        "legal_status": c.get("legal_status"),
        "url_verification": dget(c.get("url_verification"), "status"),
        "priority": c.get("priority"),
        "credibility_score": c.get("credibility_score"),
        "usefulness_score": c.get("usefulness_score"),
        "why_relevant": dget(c.get("discovery_basis"), "why_relevant"),
    } for c in candidates if isinstance(c, dict)]


def heuristic_suggestions(candidates):
    """Deterministic baseline suggestions keyed by candidate_id (no LLM)."""
    out = {}
    for c in candidates:
        if not isinstance(c, dict):
            continue
        cid = c.get("candidate_id")
        if not isinstance(cid, str) or not cid:
            continue     # a non-string/empty id can't key `out` (and is a malformed record) -> skip
        uv = dget(c.get("url_verification"), "status")
        # sstr() -> str-or-None so the set-membership tests below never hash an unhashable value
        access, legal, pri = sstr(c.get("access_status")), sstr(c.get("legal_status")), sstr(c.get("priority"))
        if access == "forbidden_do_not_collect" or legal == "forbidden":
            dec, why = "reject", "forbidden to collect (access/legal)."
        elif uv == "failed":
            dec, why = "defer", "URL verification failed — confirm reachability before approving."
        elif access in _BLOCKED_ACCESS:
            dec, why = "needs_access", f"access blocked ({access}) — needs an access decision."
        elif uv == "verified" and access == "public" and legal == "allowed" and pri in ("high", "critical"):
            dec, why = "approve", f"verified public {c.get('source_class', '')} source, {pri} priority."
        else:
            dec, why = "defer", "reachable but marginal/lower-priority — confirm value."
        out[cid] = {"suggested_decision": dec,
                    "suggested_priority": pri if pri in PRIORITIES else None,
                    "rationale": why}
    return out


def normalize_suggestions(raw, valid_ids):
    """Validate/clamp untrusted assistant output -> {candidate_id -> {suggested_decision, suggested_priority,
    rationale}}. Unknown/hallucinated candidate_ids are dropped; invalid decision/priority become None; the
    rationale is coerced to a trimmed string. Total: any odd `raw` yields {}."""
    if isinstance(raw, dict) and "suggestions" in raw:
        raw = raw.get("suggestions")
    items = raw if isinstance(raw, list) else []
    valid = set(valid_ids)
    out = {}
    for s in items:
        if not isinstance(s, dict):
            continue
        cid = s.get("candidate_id")
        cid = cid if isinstance(cid, str) else (str(cid) if cid is not None else None)
        if not cid or cid not in valid or cid in out:
            continue     # drop unknown/hallucinated ids and duplicate suggestions (first wins)
        dec, pri, rat = s.get("suggested_decision"), s.get("suggested_priority"), s.get("rationale")
        out[cid] = {
            # isinstance(str) guard: a list/dict value would be unhashable in `in <set>`
            "suggested_decision": dec if isinstance(dec, str) and dec in SUGGEST_DECISIONS else None,
            "suggested_priority": pri if isinstance(pri, str) and pri in PRIORITIES else None,
            "rationale": rat.strip()[:300] if isinstance(rat, str) and rat.strip() else None,
        }
    return out
