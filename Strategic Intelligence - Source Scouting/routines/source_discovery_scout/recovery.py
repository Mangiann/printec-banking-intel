"""Deterministic writer for the URL verify-and-repair pass (the recovery ladder's storage side).

An agent walks the recovery ladder in a REAL browser — load + wait for the page to settle + read; on a 404
read the nav/sitemap to find the moved page; on a site reorg use the site's search; on entity doubt research
the organisation (web/Wikipedia) for a rename/successor — and returns a STRUCTURED recovery result per failed
URL. This module applies those results to a run's candidates deterministically. The agent PROPOSES; code
DECIDES what gets written:

  outcome "verified" -> the URL is live as-is: mark url_verification verified (URL unchanged).
  outcome "repaired" -> moved: adopt the corrected URL (source_url + canonical_url) and mark verified,
                        recording `auto_repaired_from` provenance. A missing/unnormalizable corrected_url
                        FAILS CLOSED to "dead" — never mark a repair verified without a real replacement URL.
  outcome "dead"     -> genuinely gone: leave url_verification failed; record the grade-of-dead + any
                        successor lead in metadata (a live successor is surfaced for a new candidate).

Total + fail-closed: odd input never crashes and never fabricates a verified status. After repairs, within-run
dedupe is recomputed (a repaired URL may now collide with another candidate — keep the one-per-URL invariant).
"""
import copy

from runner import compute_dedupe, normalize_url

_VALID_OUTCOMES = {"verified", "repaired", "dead"}
_GRADES = {"moved_unknown", "rebranded", "merged", "wound_down", "defunct"}


def _s(v):
    """A trimmed non-empty string, else None."""
    return v.strip() if isinstance(v, str) and v.strip() else None


def _verified_uv(now, final_url, checked_by, http_status):
    return {"status": "verified", "verified_at": now,
            "http_status": http_status if isinstance(http_status, int) and not isinstance(http_status, bool) else None,
            "final_url": final_url, "error_message": None, "checked_by": checked_by}


def _record(r, now, outcome):
    return {"outcome": outcome, "method": _s(r.get("method")), "ladder_step": r.get("ladder_step"),
            "evidence": _s(r.get("evidence")), "recovered_at": now}


def apply_url_recovery(candidates, results, *, now, checked_by="browser_verify/recovery"):
    """Apply a list of recovery results to `candidates` (which are not mutated). Returns
    (updated_candidates, summary). Only a re-verified live/repaired URL is ever marked verified."""
    by_id = {}
    for r in results if isinstance(results, list) else []:
        r = r if isinstance(r, dict) else {}
        cid = r.get("candidate_id")
        if isinstance(cid, str) and cid and cid not in by_id:
            by_id[cid] = r

    cands = [copy.deepcopy(c) for c in candidates]
    summary = {"verified": 0, "repaired": 0, "dead": 0, "unchanged": 0, "repairs": [], "successors": []}

    for c in cands:
        if not isinstance(c, dict):
            summary["unchanged"] += 1
            continue
        cid = c.get("candidate_id")
        r = by_id.get(cid) if isinstance(cid, str) else None
        if not r:
            summary["unchanged"] += 1
            continue

        outcome = r.get("outcome") if r.get("outcome") in _VALID_OUTCOMES else "dead"
        corrected = normalize_url(_s(r.get("corrected_url")) or "") if _s(r.get("corrected_url")) else None
        meta = c.get("metadata") if isinstance(c.get("metadata"), dict) else {}

        if outcome == "repaired" and corrected:
            rec = _record(r, now, "repaired")
            rec["auto_repaired_from"] = c.get("canonical_url")
            c["source_url"] = corrected
            c["canonical_url"] = corrected
            c["url_verification"] = _verified_uv(now, corrected, checked_by, r.get("http_status"))
            meta["url_recovery"] = rec
            c["metadata"] = meta
            summary["repaired"] += 1
            summary["repairs"].append({"candidate_id": cid, "from": rec["auto_repaired_from"], "to": corrected})
        elif outcome == "verified":
            rec = _record(r, now, "verified")
            c["url_verification"] = _verified_uv(now, c.get("canonical_url"), checked_by, r.get("http_status"))
            meta["url_recovery"] = rec
            c["metadata"] = meta
            summary["verified"] += 1
        else:  # "dead" — includes a "repaired" outcome that lacked a usable corrected_url (fail closed)
            rec = _record(r, now, "dead")
            g = _s(r.get("grade_of_dead"))
            rec["grade_of_dead"] = g if g in _GRADES else "defunct"
            succ = r.get("successor") if isinstance(r.get("successor"), dict) else {}
            if _s(succ.get("url")) or _s(succ.get("name")):
                rec["successor"] = {"name": _s(succ.get("name")), "url": _s(succ.get("url"))}
                summary["successors"].append({"candidate_id": cid, **rec["successor"]})
            # url_verification stays 'failed' — a dead source is never marked verified
            meta["url_recovery"] = rec
            c["metadata"] = meta
            summary["dead"] += 1

    compute_dedupe([c for c in cands if isinstance(c, dict)])   # repaired URLs may now dup — keep the invariant
    return cands, summary
