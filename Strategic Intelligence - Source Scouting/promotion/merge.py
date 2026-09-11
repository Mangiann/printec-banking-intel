"""merge_into_existing: merge an approved duplicate SourceCandidate into its single
existing target Source (deterministic; no new Source created).

Reuses the shared event/transaction helpers from promote.py so the audit contract is
identical. Merge rules (docs/promotion_workflow.md section 8): arrays union; empty scalars
fill; populated scalars are never overwritten (conflicts flagged for human review);
access/legal tighten via the restrictiveness ordering; collection_allowed = AND, and
indeterminate/unrankable/hard-stop dispositions gate collection to false; active_status is
re-derived tighten-only (a paused target is never auto-activated).

The read-modify-write of the shared target Source happens ENTIRELY inside the BEGIN
IMMEDIATE write lock (the target is re-read under the lock), so concurrent merges into the
same Source cannot lose an update.

Scope: merge only. No update_existing / retire / deactivate.
"""
import copy
import json
import sqlite3

from . import util
from .db import immediate_txn, safe_rollback
from .enrich import enrich_metadata
from .gates import run_merge_gates
from .validation import ValidationError, validate
from .promote import (WORKFLOW_VERSION, _EMPTY_REFS, _NoOp, _insert_event, _make_event,
                      _next_attempt_generation, _require_valid_actor, _rollup_lifecycle,
                      get_candidate, get_source)

_BLOCKED_ACTIVE = {"retired", "disabled"}
_BLOCKED_REVIEW = {"rejected", "suspended", "superseded"}

class _Abort(Exception):
    """Raised inside the transaction to abort with a specific terminal event_status."""
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason
        super().__init__(reason)


def apply_merge(target, cand, now):
    """Merge candidate into target Source (ABSORB): append the candidate to the source's
    lineage, then enrich the metadata. Returns (merged, overrides, human_refs).

    The lineage append is what distinguishes merge_into_existing from update_existing.
    """
    m = copy.deepcopy(target)
    ids = m.setdefault("provenance", {}).setdefault("promoted_from_candidate_ids", [])
    if cand["candidate_id"] not in ids:
        ids.append(cand["candidate_id"])
    overrides, human_refs = enrich_metadata(m, cand, now)
    return m, overrides, human_refs


def _apply_merge_promotion(cand, target_id, now):
    c = copy.deepcopy(cand)
    c["promotion"]["promotion_status"] = "merged"
    c["promotion"]["promoted_source_id"] = target_id
    c["promotion"]["promoted_at"] = now
    c["updated_at"] = now
    c["lifecycle_status"] = _rollup_lifecycle(c)   # -> 'merged'
    return c


def _result(ok, event_status, source_id, active_status, event, candidate_id, reason, gates):
    return {"ok": ok, "action": "merge_into_existing", "event_status": event_status,
            "source_id": source_id, "active_status": active_status,
            "event_id": event["event_id"] if event else None,
            "candidate_id": candidate_id, "reason": reason, "gates": gates}


def merge_candidate(conn, validators, candidate_id, *, actor, now=None, workflow_version=WORKFLOW_VERSION):
    _require_valid_actor(actor)
    now = now or util.now_iso()
    attempt_id = f"pa_{candidate_id}"

    def emit(event_status, target, gates, overrides, human_refs, failure_reason, before, after):
        if conn.in_transaction:
            safe_rollback(conn)
        with immediate_txn(conn):
            # attempt_generation MUST be read under the write lock (see promote.py) so concurrent
            # physical attempts sharing this promotion_attempt_id cannot collide on one generation.
            gen = _next_attempt_generation(conn, attempt_id)
            ev = _make_event(conn, candidate_id=candidate_id, action="merge_into_existing",
                             event_status=event_status, target_source_id=target, actor=actor,
                             gates=gates, overrides=overrides, failure_reason=failure_reason,
                             before=before, after=after, now=now, attempt_id=attempt_id,
                             attempt_generation=gen, workflow_version=workflow_version)
            ev["human_review_refs"] = human_refs
            _insert_event(conn, validators, ev)
        return ev

    # G1
    cand = get_candidate(conn, candidate_id)
    if cand is None:
        gates = [{"gate": "G1_candidate_loads", "passed": False, "detail": "candidate not found"}]
        ev = emit("gate_failed", None, gates, [], [], "candidate not found", _EMPTY_REFS, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, "candidate not found", gates)
    try:
        validate(validators, "source_candidate", cand)
    except ValidationError as e:
        gates = [{"gate": "G1_candidate_schema_valid", "passed": False, "detail": str(e)}]
        ev = emit("gate_failed", None, gates, [], [], str(e), _EMPTY_REFS, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, str(e), gates)
    gates = [{"gate": "G1_candidate_schema_valid", "passed": True, "detail": None}]
    before_cand = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(cand),
                   "source_ref": None, "source_hash": None}

    # G2..G4 candidate-side gates + target-id resolution (existence from a snapshot; re-checked in-txn)
    sources = {r["source_id"]: json.loads(r["doc"])
               for r in conn.execute("SELECT source_id, doc FROM source").fetchall()}
    ok, pre, target_id = run_merge_gates(cand, sources)
    gates += pre
    if not ok:
        reason = "; ".join(f"{g['gate']}: {g['detail']}" for g in pre if not g["passed"])
        g4 = any(g["gate"] == "G4_not_promoted" and not g["passed"] for g in pre)
        status = "no_op" if g4 else "gate_failed"
        ev = emit(status, None, gates, [], [], reason, before_cand, _EMPTY_REFS)
        return _result(False, status, None, None, ev, candidate_id, reason, gates)

    # Everything target-related runs INSIDE the write lock on freshly-read rows, so the
    # read-modify-write of the shared Source is atomic (no lost update under concurrency).
    overrides, human_refs = [], []
    merged = None
    try:
        with immediate_txn(conn):
            fresh_cand = get_candidate(conn, candidate_id)
            if (fresh_cand.get("promotion") or {}).get("promotion_status") != "not_promoted":
                raise _NoOp()
            target = get_source(conn, target_id)                      # re-read under the lock
            if target is None:
                gates.append({"gate": "G3_target_exists", "passed": False, "detail": "target vanished"})
                raise _Abort("gate_failed", "target source no longer exists")
            try:
                validate(validators, "source", target)                # G6 (target)
            except ValidationError as e:
                gates.append({"gate": "G6_target_valid", "passed": False, "detail": str(e)})
                raise _Abort("gate_failed", f"target invalid: {e}")
            gates.append({"gate": "G6_target_valid", "passed": True, "detail": None})
            blocked = (target.get("active_status") in _BLOCKED_ACTIVE
                       or target.get("review_status") in _BLOCKED_REVIEW)
            gates.append({"gate": "G7_target_not_blocked", "passed": not blocked,
                          "detail": None if not blocked else
                          f"target active_status={target.get('active_status')}, review_status={target.get('review_status')} "
                          "(retired/disabled/rejected/suspended/superseded require human reactivation)"})
            if blocked:
                raise _Abort("gate_failed", gates[-1]["detail"])

            merged, overrides, human_refs = apply_merge(target, fresh_cand, now)
            try:
                validate(validators, "source", merged)                # G6 (merged)
            except ValidationError as e:
                gates.append({"gate": "G6_merged_source_safety", "passed": False, "detail": str(e)})
                raise _Abort("gate_failed", str(e))
            gates.append({"gate": "G6_merged_source_safety", "passed": True, "detail": None})
            gates.append({"gate": "G9_activation", "passed": True, "detail": f"active_status={merged['active_status']}"})

            before = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(fresh_cand),
                      "source_ref": target_id, "source_hash": util.content_hash(target)}
            conn.execute("UPDATE source SET doc=? WHERE source_id=?",
                         (util.canonical_json(merged), target_id))
            cand_after = _apply_merge_promotion(fresh_cand, target_id, now)
            validate(validators, "source_candidate", cand_after)
            conn.execute("UPDATE source_candidate SET doc=? WHERE candidate_id=?",
                         (util.canonical_json(cand_after), candidate_id))
            if not conn.execute("SELECT 1 FROM source_candidate_link WHERE source_id=? AND candidate_id=?",
                                (target_id, candidate_id)).fetchone():
                conn.execute("INSERT INTO source_candidate_link(source_id, candidate_id, linked_at) VALUES(?,?,?)",
                             (target_id, candidate_id, now))
            # cross-record integrity: verify the PERSISTED rows agree
            p_cand = get_candidate(conn, candidate_id)
            p_src = get_source(conn, target_id)
            link = conn.execute("SELECT 1 FROM source_candidate_link WHERE source_id=? AND candidate_id=?",
                                (target_id, candidate_id)).fetchone()
            if (p_cand is None or p_src is None or link is None
                    or p_cand["promotion"]["promoted_source_id"] != target_id
                    or candidate_id not in p_src["provenance"]["promoted_from_candidate_ids"]):
                raise RuntimeError("cross-record integrity check failed (persisted rows disagree)")
            after = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(p_cand),
                     "source_ref": target_id, "source_hash": util.content_hash(p_src)}
            gen = _next_attempt_generation(conn, attempt_id)   # under the write lock
            ev = _make_event(conn, candidate_id=candidate_id, action="merge_into_existing",
                             event_status="committed", target_source_id=target_id, actor=actor,
                             gates=gates, overrides=overrides, failure_reason=None, before=before,
                             after=after, now=now, attempt_id=attempt_id, attempt_generation=gen,
                             workflow_version=workflow_version)
            ev["human_review_refs"] = human_refs
            _insert_event(conn, validators, ev)
        return _result(True, "committed", target_id, merged["active_status"], ev, candidate_id, None, gates)
    except _NoOp:
        gates.append({"gate": "G4_not_promoted_recheck", "passed": False, "detail": "already promoted/merged"})
        ev = emit("no_op", target_id, gates, [], [], "already promoted/merged", before_cand, _EMPTY_REFS)
        return _result(False, "no_op", None, None, ev, candidate_id, "already promoted/merged", gates)
    except _Abort as ab:
        ev = emit(ab.status, target_id, gates, overrides, human_refs, ab.reason, before_cand, _EMPTY_REFS)
        return _result(False, ab.status, None, None, ev, candidate_id, ab.reason, gates)
    except sqlite3.IntegrityError as e:
        gates.append({"gate": "write_integrity", "passed": False, "detail": str(e)})
        ev = emit("gate_failed", target_id, gates, overrides, human_refs, f"integrity: {e}", before_cand, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, f"integrity: {e}", gates)
    except Exception as e:  # noqa: BLE001
        gates.append({"gate": "write", "passed": False, "detail": str(e)})
        try:
            ev = emit("failed", target_id, gates, overrides, human_refs, f"write failed: {e}", before_cand, _EMPTY_REFS)
        except Exception as audit_err:  # noqa: BLE001
            safe_rollback(conn)
            raise RuntimeError(f"merge failed AND audit write failed: primary={e!r}; audit={audit_err!r}") from e
        return _result(False, "failed", None, None, ev, candidate_id, f"write failed: {e}", gates)
