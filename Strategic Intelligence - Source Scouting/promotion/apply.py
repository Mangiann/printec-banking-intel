"""Apply human review decisions to the promotion machinery — the review→promotion bridge.

Takes a list of decisions (the shape `review.excel.import_review_decisions` returns:
`{candidate_id, decision, owner, notes}`) plus the run's candidate docs, and for each:

  approve      -> seed the candidate as review_status=approved (reviewer/reviewed_at from the sheet's
                  owner + now, lifecycle rollup recomputed) -> promote_new.
  reject       -> seed the candidate as-is -> reject_candidate (sets promotion rejected + review rejected).
  needs_access -> HOLD: no store mutation (a human still owns resolving access; see the next increment).
  defer        -> HOLD: no store mutation (left for a later review pass).

Reviewer ACCESS feedback (can_access + access_note) rides along on an approve and is folded into the
candidate before promote: `do_not_collect` -> access forbidden + collection off (tighten, honored);
`yes` -> grant collection permission (UNLESS access/legal is forbidden — the safety machinery still forces
it off) while staying paused (a non-public source never auto-activates); `no`/blank -> no change. The
how-to note is stamped into the candidate's review_notes and carried in the apply report.

Deterministic. Each promotion op emits its own PromotionEvent; this module writes no events itself and
DECIDES nothing (the human already did). Candidates are seeded on demand because they live in JSONL, not the
promotion store; seeding is idempotent (skipped when the candidate row already exists) and the ops are
idempotent (an already-promoted candidate re-runs to no_op), so re-applying a decisions file is safe.

Out of scope (next increments): merge/update for within-run or registry duplicates (a within-run
`dedupe_status=duplicate` candidate correctly fails promote_new's G3 and is reported, not promoted);
reviewer access overrides; reactivation. This module reads no Excel (that is `review/excel.py`).
"""
import copy
from collections import Counter

from . import db, lifecycle, util
from .promote import _rollup_lifecycle, get_candidate, insert_candidate, promote_candidate
from .safety import ACCESS_FORBIDDEN, LEGAL_FORBIDDEN

HOLD_DECISIONS = {"needs_access", "defer"}


def _actor(owner):
    """A human made these calls when an owner is named; otherwise attribute to the apply workflow."""
    if isinstance(owner, str) and owner.strip():
        return {"actor_type": "human", "actor_id": owner, "human_actor_id": owner}
    return {"actor_type": "workflow", "actor_id": "review_apply", "human_actor_id": None}


def _approved_candidate(cand, owner, notes, now):
    """A deep copy of the scout candidate marked review-approved, ready for promote_new. Only the review
    sub-object + rollup are touched, so the record stays schema-valid (no if/then keys on review_status)."""
    c = copy.deepcopy(cand)
    r = c.setdefault("review", {})
    r["review_status"] = "approved"
    r["reviewer"] = owner
    r["reviewed_at"] = now
    if isinstance(notes, str) and notes.strip():
        r["review_notes"] = notes
    c["updated_at"] = now
    c["lifecycle_status"] = _rollup_lifecycle(c)   # keep the authoritative rollup consistent with the review
    return c


def _apply_access_override(cand, can_access, access_note, owner, now):
    """Fold the reviewer's access feedback into the (approved) candidate BEFORE promotion. Mutates `cand`.

    The promotion safety machinery still has the FINAL say: `derive_collection_allowed` forces collection
    off when access/legal is forbidden (so a legal prohibition beats a reviewer 'yes'), and
    `derive_active_status` keeps a non-public source 'paused' (so loosening records the route without
    auto-collecting). Here we only set the reviewer's structured intent + record the how-to note."""
    if can_access == "do_not_collect":                       # tighten — honored (S1 will keep collection off)
        cand["access_status"] = ACCESS_FORBIDDEN
        cand["collection_allowed"] = False
    elif can_access == "yes":                                # grant permission unless already forbidden
        if cand.get("access_status") != ACCESS_FORBIDDEN and cand.get("legal_status") != LEGAL_FORBIDDEN:
            cand["collection_allowed"] = True
    # 'no' / None -> no structured change; the scout's assessment stands
    if isinstance(access_note, str) and access_note.strip():
        r = cand.setdefault("review", {})
        stamp = f"[access:{can_access or 'note'} by {owner or 'reviewer'} @ {now}] " + access_note.strip()
        prev = r.get("review_notes")
        r["review_notes"] = (prev + " | " + stamp) if isinstance(prev, str) and prev else stamp
    return cand


def apply_decision(conn, validators, decision, cand, *, now):
    """Apply ONE decision. `cand` is the full scout candidate doc (or None if the id isn't in the run)."""
    cid = decision.get("candidate_id")
    dec = decision.get("decision")
    owner = decision.get("owner")
    notes = decision.get("notes")
    can_access = decision.get("can_access")
    access_note = decision.get("access_note")
    access = {"can_access": can_access, "access_note": access_note}

    if dec in HOLD_DECISIONS:
        return {"candidate_id": cid, "decision": dec, "action": "hold", "ok": True,
                "event_status": "held", "source_id": None,
                "reason": f"{dec}: held (no promotion — a human/next step owns it)", **access}

    if dec not in ("approve", "reject"):
        return {"candidate_id": cid, "decision": dec, "action": "none", "ok": False,
                "event_status": "skipped", "source_id": None, "reason": f"unknown decision {dec!r}", **access}

    if cand is None:
        return {"candidate_id": cid, "decision": dec, "action": "none", "ok": False,
                "event_status": "error", "source_id": None,
                "reason": "candidate_id not found among the run's candidates", **access}

    actor = _actor(owner)
    if dec == "approve":
        if get_candidate(conn, cid) is None:
            seed = _approved_candidate(cand, owner, notes, now)
            _apply_access_override(seed, can_access, access_note, owner, now)
            insert_candidate(conn, validators, seed)
        res = promote_candidate(conn, validators, cid, record_owner=owner, actor=actor, now=now)
        action = "promote_new"
    else:  # reject
        if get_candidate(conn, cid) is None:
            insert_candidate(conn, validators, cand)
        res = lifecycle.reject_candidate(conn, validators, cid, reason=notes, actor=actor, now=now)
        action = res.get("action", "reject")

    return {"candidate_id": cid, "decision": dec, "action": action, "ok": res["ok"],
            "event_status": res["event_status"], "source_id": res.get("source_id"),
            "active_status": res.get("active_status"), "event_id": res.get("event_id"),
            "reason": res.get("reason"), **access}


def _summarize(results):
    ev = Counter(r["event_status"] for r in results)
    dec = Counter(r["decision"] for r in results)
    promoted = [r["source_id"] for r in results
                if r.get("action") == "promote_new" and r.get("event_status") == "committed" and r.get("source_id")]
    rejected = sum(1 for r in results if r.get("action") == "reject" and r.get("event_status") == "committed")
    return {
        "total": len(results),
        "by_decision": dict(dec),
        "by_event_status": dict(ev),
        "promoted": len(promoted),
        "promoted_source_ids": promoted,
        "rejected": rejected,
    }


def apply_decisions(conn, validators, decisions, candidates_by_id, *, now=None):
    """Apply a list of decisions against the promotion store. Returns {results, summary}. Total: an
    unknown candidate_id or an odd decision becomes an error/skipped result, never a raise."""
    now = now or util.now_iso()
    results = []
    for d in decisions:
        d = d if isinstance(d, dict) else {}
        cand = candidates_by_id.get(d.get("candidate_id"))
        try:
            results.append(apply_decision(conn, validators, d, cand, now=now))
        except Exception as ex:  # noqa: BLE001 - one malformed candidate/decision must not abort the batch
            # a malformed upstream candidate doc (non-dict `review`, missing required field) can raise in
            # _approved_candidate / insert_candidate's schema validation; degrade that ONE row to an error
            # so every other decision (and the report) still lands.
            db.safe_rollback(conn)   # never leave a write lock held by a mid-transaction raise
            results.append({"candidate_id": d.get("candidate_id"), "decision": d.get("decision"),
                            "action": "none", "ok": False, "event_status": "error", "source_id": None,
                            "reason": f"apply raised: {ex}",
                            "can_access": d.get("can_access"), "access_note": d.get("access_note")})
    return {"results": results, "summary": _summarize(results)}
