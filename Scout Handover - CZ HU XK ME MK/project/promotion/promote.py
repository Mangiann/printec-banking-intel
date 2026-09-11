"""promote_new orchestration: approved unique SourceCandidate -> new Source + audit.

Deterministic. One PromotionEvent is emitted per attempt (committed on success;
gate_failed / no_op / failed otherwise). The candidate + source + link + event
writes happen in a single BEGIN IMMEDIATE transaction, so a crash mid-write is
atomically rolled back by SQLite (no compensating recovery needed for this slice).

All events of one physical attempt (one promote_candidate call) share
(promotion_attempt_id, attempt_generation); attempt_generation increments per
physical attempt of a candidate, so each attempt pairs 1:1 with its terminal event.
"""
import copy
import json
import sqlite3

from . import db as dbmod
from . import util
from .gates import run_promote_new_gates
from .mapper import map_candidate_to_source
from .validation import ValidationError, validate

WORKFLOW_VERSION = "0.1.0-slice"
_ACTOR_TYPES = {"workflow", "human", "system"}
_EMPTY_REFS = {"candidate_ref": None, "candidate_hash": None, "source_ref": None, "source_hash": None}


class _NoOp(Exception):
    """Raised inside the transaction when the candidate was already promoted (concurrent case)."""


class AuditWriteError(RuntimeError):
    """The primary operation failed AND the failure audit event could not be written."""


# ---- store helpers -------------------------------------------------------

def insert_candidate(conn, validators, cand):
    """Validate then insert a SourceCandidate (used to seed the store)."""
    validate(validators, "source_candidate", cand)
    with dbmod.immediate_txn(conn):
        conn.execute("INSERT INTO source_candidate(candidate_id, doc) VALUES(?,?)",
                     (cand["candidate_id"], util.canonical_json(cand)))


def get_candidate(conn, candidate_id):
    row = conn.execute("SELECT doc FROM source_candidate WHERE candidate_id=?", (candidate_id,)).fetchone()
    return json.loads(row["doc"]) if row else None


def get_source(conn, source_id):
    row = conn.execute("SELECT doc FROM source WHERE source_id=?", (source_id,)).fetchone()
    return json.loads(row["doc"]) if row else None


# ---- internal helpers ----------------------------------------------------

def _require_valid_actor(actor):
    """Fail fast (before any DB work) if actor cannot populate a valid event.actor.

    Every PromotionEvent (success OR failure) requires a valid actor, so an invalid
    actor means no event could ever be audited -- reject it up front rather than
    crashing later mid-flight with a lost audit trail.
    """
    ok = (isinstance(actor, dict)
          and actor.get("actor_type") in _ACTOR_TYPES
          and isinstance(actor.get("actor_id"), str) and actor["actor_id"].strip() != ""
          and "human_actor_id" in actor
          and (actor["human_actor_id"] is None or isinstance(actor["human_actor_id"], str)))
    if not ok:
        raise ValueError(
            "invalid actor: need {actor_type in %s, non-empty str actor_id, human_actor_id key (str|null)}; got %r"
            % (sorted(_ACTOR_TYPES), actor))


def _rollup_lifecycle(cand):
    """Minimal deterministic lifecycle rollup for the promote_new case."""
    p = (cand.get("promotion") or {}).get("promotion_status")
    r = (cand.get("review") or {}).get("review_status")
    if p == "rejected" or r == "rejected":
        return "rejected"
    if p == "merged":
        return "merged"
    if p == "retired":
        return "retired"
    if r == "approved":            # promotion_status 'promoted' rolls up to approved
        return "approved"
    if r == "needs_review":
        return "needs_review"
    return "discovered"


def _apply_promotion(cand, source_id, now):
    c = copy.deepcopy(cand)
    c["promotion"]["promotion_status"] = "promoted"
    c["promotion"]["promoted_source_id"] = source_id
    c["promotion"]["promoted_at"] = now
    c["updated_at"] = now
    c["lifecycle_status"] = _rollup_lifecycle(c)
    return c


def _next_seq(conn):
    return conn.execute("SELECT COALESCE(MAX(seq),0)+1 AS n FROM promotion_event").fetchone()["n"]


def _next_attempt_generation(conn, attempt_id):
    row = conn.execute(
        "SELECT COALESCE(MAX(attempt_generation),0)+1 AS n FROM promotion_event WHERE promotion_attempt_id=?",
        (attempt_id,)).fetchone()
    return row["n"]


def _make_event(conn, *, candidate_id, action, event_status, target_source_id, actor,
                gates, overrides, failure_reason, before, after, now, attempt_id,
                attempt_generation, workflow_version):
    return {
        "event_id": util.new_id("evt"),
        "promotion_attempt_id": attempt_id,
        "attempt_generation": attempt_generation,
        "sequence": _next_seq(conn),
        "timestamp": now,
        "actor": actor,
        "workflow_version": workflow_version,
        "candidate_id": candidate_id,
        "action": action,
        "target_source_id": target_source_id,
        "event_status": event_status,
        "gates_evaluated": gates,
        "safety_overrides": overrides,
        "human_review_refs": [],
        "before_refs_or_hashes": before,
        "after_refs_or_hashes": after,
        "failure_reason": failure_reason,
        "rollback_actions": [],
    }


def _insert_event(conn, validators, ev):
    validate(validators, "promotion_event", ev)
    conn.execute("INSERT INTO promotion_event(seq, event_id, doc) VALUES(?,?,?)",
                 (ev["sequence"], ev["event_id"], util.canonical_json(ev)))


def _result(ok, event_status, source_id, active_status, event, candidate_id, reason, gates):
    return {
        "ok": ok, "action": "promote_new", "event_status": event_status,
        "source_id": source_id, "active_status": active_status,
        "event_id": event["event_id"] if event else None,
        "candidate_id": candidate_id, "reason": reason, "gates": gates,
    }


# ---- public entrypoint ---------------------------------------------------

def promote_candidate(conn, validators, candidate_id, *, record_owner, actor,
                      refresh_cadence="on_demand", now=None, source_id=None,
                      workflow_version=WORKFLOW_VERSION):
    _require_valid_actor(actor)                 # fail fast: no valid actor -> no auditable event
    now = now or util.now_iso()
    attempt_id = f"pa_{candidate_id}"

    def emit(event_status, target, gates, overrides, failure_reason, before, after):
        # Best-effort ensure no dangling txn before opening our own (defence in depth).
        if conn.in_transaction:
            dbmod.safe_rollback(conn)
        with dbmod.immediate_txn(conn):
            # attempt_generation MUST be read under the write lock so two concurrent physical
            # attempts sharing this promotion_attempt_id cannot compute the same generation and
            # emit two terminal events colliding on (promotion_attempt_id, attempt_generation).
            attempt_generation = _next_attempt_generation(conn, attempt_id)
            ev = _make_event(conn, candidate_id=candidate_id, action="promote_new",
                             event_status=event_status, target_source_id=target, actor=actor,
                             gates=gates, overrides=overrides, failure_reason=failure_reason,
                             before=before, after=after, now=now, attempt_id=attempt_id,
                             attempt_generation=attempt_generation, workflow_version=workflow_version)
            _insert_event(conn, validators, ev)
        return ev

    # --- G1: load + schema-validate the candidate ---
    cand = get_candidate(conn, candidate_id)
    if cand is None:
        gates = [{"gate": "G1_candidate_loads", "passed": False, "detail": "candidate not found"}]
        ev = emit("gate_failed", None, gates, [], "candidate not found", _EMPTY_REFS, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, "candidate not found", gates)
    try:
        validate(validators, "source_candidate", cand)
    except ValidationError as e:
        gates = [{"gate": "G1_candidate_schema_valid", "passed": False, "detail": str(e)}]
        ev = emit("gate_failed", None, gates, [], str(e), _EMPTY_REFS, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, str(e), gates)

    gates = [{"gate": "G1_candidate_schema_valid", "passed": True, "detail": None}]
    before = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(cand),
              "source_ref": None, "source_hash": None}

    # --- G2..G5 ---
    ok, pre = run_promote_new_gates(cand, record_owner)
    gates += pre
    if not ok:
        reason = "; ".join(f"{g['gate']}: {g['detail']}" for g in pre if not g["passed"])
        # An already-promoted candidate is the idempotent case: workflow section 5 -> no_op, not gate_failed.
        g4_idempotent = any(g["gate"] == "G4_not_promoted" and not g["passed"] for g in pre)
        status = "no_op" if g4_idempotent else "gate_failed"
        ev = emit(status, None, gates, [], reason, before, _EMPTY_REFS)
        return _result(False, status, None, None, ev, candidate_id, reason, gates)

    # --- map + G6 (safety via Source schema) + G9 (activation decision) ---
    sid = source_id or util.new_id("src")
    has_open_task = cand.get("access_review_task_id") is not None
    src, overrides = map_candidate_to_source(
        cand, source_id=sid, record_owner=record_owner, refresh_cadence=refresh_cadence,
        actor=actor, now=now, has_open_access_task=has_open_task)
    try:
        validate(validators, "source", src)
    except ValidationError as e:
        gates.append({"gate": "G6_source_safety_schema", "passed": False, "detail": str(e)})
        ev = emit("gate_failed", None, gates, overrides, str(e), before, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, str(e), gates)
    gates.append({"gate": "G6_source_safety_schema", "passed": True, "detail": None})
    gates.append({"gate": "G9_activation", "passed": True, "detail": f"active_status={src['active_status']}"})

    # --- transactional promote_new (candidate + source + link + event) ---
    try:
        with dbmod.immediate_txn(conn):
            fresh = get_candidate(conn, candidate_id)
            if (fresh.get("promotion") or {}).get("promotion_status") != "not_promoted":
                raise _NoOp()
            conn.execute("INSERT INTO source(source_id, doc) VALUES(?,?)",
                         (sid, util.canonical_json(src)))
            cand_after = _apply_promotion(cand, sid, now)
            validate(validators, "source_candidate", cand_after)
            conn.execute("UPDATE source_candidate SET doc=? WHERE candidate_id=?",
                         (util.canonical_json(cand_after), candidate_id))
            conn.execute("INSERT INTO source_candidate_link(source_id, candidate_id, linked_at) VALUES(?,?,?)",
                         (sid, candidate_id, now))
            # cross-record integrity (workflow safety rule 4): verify the PERSISTED rows agree,
            # not the in-memory dicts we just built.
            p_cand = get_candidate(conn, candidate_id)
            p_src = get_source(conn, sid)
            link = conn.execute(
                "SELECT 1 FROM source_candidate_link WHERE source_id=? AND candidate_id=?",
                (sid, candidate_id)).fetchone()
            if (p_cand is None or p_src is None or link is None
                    or p_cand["promotion"]["promoted_source_id"] != sid
                    or candidate_id not in p_src["provenance"]["promoted_from_candidate_ids"]):
                raise RuntimeError("cross-record integrity check failed (persisted rows disagree)")
            after = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(p_cand),
                     "source_ref": sid, "source_hash": util.content_hash(p_src)}
            attempt_generation = _next_attempt_generation(conn, attempt_id)   # under the write lock
            ev = _make_event(conn, candidate_id=candidate_id, action="promote_new",
                             event_status="committed", target_source_id=sid, actor=actor,
                             gates=gates, overrides=overrides, failure_reason=None,
                             before=before, after=after, now=now, attempt_id=attempt_id,
                             attempt_generation=attempt_generation, workflow_version=workflow_version)
            _insert_event(conn, validators, ev)
        return _result(True, "committed", sid, src["active_status"], ev, candidate_id, None, gates)
    except _NoOp:
        gates.append({"gate": "G4_not_promoted_recheck", "passed": False, "detail": "already promoted (in-txn)"})
        ev = emit("no_op", None, gates, overrides, "already promoted", before, _EMPTY_REFS)
        return _result(False, "no_op", None, None, ev, candidate_id, "already promoted", gates)
    except sqlite3.IntegrityError as e:
        gates.append({"gate": "G8_unique_canonical_url", "passed": False, "detail": str(e)})
        ev = emit("gate_failed", None, gates, overrides, f"integrity: {e}", before, _EMPTY_REFS)
        return _result(False, "gate_failed", None, None, ev, candidate_id, f"integrity: {e}", gates)
    except Exception as e:  # noqa: BLE001 - defensive: any write/commit failure -> audited 'failed'
        gates.append({"gate": "write", "passed": False, "detail": str(e)})
        try:
            ev = emit("failed", None, gates, overrides, f"write failed: {e}", before, _EMPTY_REFS)
        except Exception as audit_err:  # noqa: BLE001
            dbmod.safe_rollback(conn)   # never leave the lock held
            raise AuditWriteError(
                f"promotion failed AND the failure audit could not be written: "
                f"primary={e!r}; audit={audit_err!r}") from e
        return _result(False, "failed", None, None, ev, candidate_id, f"write failed: {e}", gates)
