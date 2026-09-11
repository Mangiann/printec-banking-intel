"""Controlled negative lifecycle: reject / retire a candidate, and deactivate a Source.

Deterministic. Three public entrypoints, mapping 1:1 onto three PromotionEvent actions:

  reject_candidate(cid)  -> if the candidate is un-promoted: set its terminal disposition
                            (promotion_status=rejected, review rejected), no Source; action=reject.
  retire_candidate(cid)  -> if un-promoted: promotion_status=retired, no Source; action=retire.
  deactivate_source(sid) -> operationally deactivate a Source; action=deactivate_source.

CASE 3 (locked decision -- CASCADE-ONLY): when reject/retire targets a candidate that has
ALREADY been promoted/merged (promotion_status in {promoted, merged}), the candidate's
historical promotion row, its source_candidate_link, and its membership in the Source's
provenance.promoted_from_candidate_ids are ALL left intact (immutable audit history). The
operation instead cascades to deactivate_source on the promoted Source and audits it as
action=deactivate_source. The Source's active_status is the operational kill-switch.

Deactivation end-states (locked decision 2), all forcing collection_allowed=false and all
re-validated against the Source schema (so R5/R6/S1/S2 do the enforcing):
  retire  -> active_status=retired  (end-of-life; review_status untouched)
  disable -> active_status=disabled (kill-switch; review_status untouched)
  reject  -> active_status=disabled + review_status=rejected (governance kill)

Human-confirmation gate (locked decision 3): a deactivation that touches a risky Source
requires a caller-supplied `confirmation` human-review-ref. When required-but-absent, NOTHING
is written and a PromotionEvent(event_status=awaiting_human) is emitted with the reason in
human_review_refs. Confirmation is required when the Source is high/critical priority, or has a
sensitive access/legal disposition, or has multiple lineage candidates -- EXCEPT when the
Source is already forbidden (deactivation only tightens safety, so it proceeds freely).

The read-modify-write of the Source (and of the candidate, cases 1/2) happens ENTIRELY inside
the BEGIN IMMEDIATE write lock -- the target is re-read under the lock and all gates re-checked
-- so concurrent writers cannot lose an update or bypass the confirmation gate.

Scope: reject / retire / deactivate only. No reactivation, no rollback/reconciler, no scout.
"""
import copy
import sqlite3
from datetime import datetime

from . import util
from .db import immediate_txn, safe_rollback
from .merge import _Abort
from .safety import ACCESS_FORBIDDEN, LEGAL_FORBIDDEN
from .validation import ValidationError, validate
from .promote import (WORKFLOW_VERSION, _EMPTY_REFS, _insert_event, _make_event,
                      _next_attempt_generation, _require_valid_actor, _rollup_lifecycle,
                      get_candidate, get_source)

_MODES = {"retire", "disable", "reject"}
_FAIL_STATES = {"failed", "gate_failed", "rolling_back", "rolled_back", "rollback_failed"}
_SENSITIVE_ACCESS = {"requires_legal_review", "requires_credentials", "requires_paid_subscription"}
_SENSITIVE_LEGAL = {"restricted", "unclear", "requires_review"}
_REVIEW_TYPES = {"candidate_approval", "legal_or_access_clearance", "merge_confirmation",
                 "registry_field_entry", "reactivation", "segregation_of_duties",
                 "scalar_conflict_resolution", "manual_reconciliation", "other"}

# Sentinel audit candidate_id for the rare direct-deactivate of a source that does not exist
# and for which the caller gave no candidate_id. PromotionEvent.candidate_id is required and
# non-empty; this only ever lands on a gate_failed event (never a committed/source-writing one),
# which the auditor does not cross-check for candidate existence. See decision 4.
_AUDIT_SOURCE_ONLY = "__source_only__"


# ---- end-state + predicates -------------------------------------------------

def _target_end_state(mode):
    if mode == "retire":
        return {"active_status": "retired"}
    if mode == "disable":
        return {"active_status": "disabled"}
    if mode == "reject":
        return {"active_status": "disabled", "review_status": "rejected"}
    raise ValueError(f"invalid mode {mode!r}; expected one of {sorted(_MODES)}")


def _already_deactivated(src, mode):
    """True when the Source is already in `mode`'s exact end-state (idempotency)."""
    end = _target_end_state(mode)
    if src.get("active_status") != end["active_status"]:
        return False
    if src.get("collection_allowed") is not False:
        return False
    if "review_status" in end and src.get("review_status") != end["review_status"]:
        return False
    return True


def _already_forbidden(src):
    return src.get("access_status") == ACCESS_FORBIDDEN or src.get("legal_status") == LEGAL_FORBIDDEN


def _confirmation_reasons(src):
    """Reasons human confirmation is required to deactivate `src` (empty => not required).

    Exception (decision 3): an already-forbidden Source deactivates freely -- turning off a
    source whose collection is already prohibited only tightens safety, never loosens it.
    """
    if _already_forbidden(src):
        return []
    reasons = []
    if src.get("priority") in ("high", "critical"):
        reasons.append(f"priority={src.get('priority')} (high/critical)")
    if src.get("access_status") in _SENSITIVE_ACCESS:
        reasons.append(f"access_status={src.get('access_status')} (sensitive access)")
    if src.get("legal_status") in _SENSITIVE_LEGAL:
        reasons.append(f"legal_status={src.get('legal_status')} (sensitive legal state)")
    ids = (src.get("provenance") or {}).get("promoted_from_candidate_ids") or []
    if len(ids) > 1:
        reasons.append(f"{len(ids)} lineage candidates (full deactivation needs confirmation)")
    return reasons


def _is_valid_confirmation(confirmation):
    """A confirmation counts as a REAL human sign-off only when it is a dict naming a reviewer.

    Gating on this (not on `is None`) closes the bypass where a falsy-but-not-None value
    ({}, False, 0, "", [], "yes") would otherwise be treated as a supplied confirmation.
    """
    return (isinstance(confirmation, dict)
            and isinstance(confirmation.get("reviewer"), str)
            and confirmation["reviewer"].strip() != "")


def _is_date_time(value):
    """True only for an ISO-8601 date-time string WITH a time component (rejects a plain date).

    Guards the human_review_refs.decided_at 'date-time' format so a caller-supplied plain date
    (e.g. '2026-07-03') can never make the committed PromotionEvent schema-invalid.
    """
    if not isinstance(value, str) or ("T" not in value and "t" not in value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00").replace("z", "+00:00"))
        return True
    except ValueError:
        return False


def _await_ref(detail):
    """A human_review_refs entry flagging a deactivation that is blocked pending confirmation."""
    return {"review_type": "other", "reviewer": "system-flagged", "decided_at": None,
            "decision": None, "notes": f"deactivation requires human confirmation: {detail}"}


def _confirmation_ref(confirmation, detail):
    """Normalize a caller-supplied confirmation into a GUARANTEED schema-valid human_review_refs
    entry. Every field is coerced (not passed through): a malformed decided_at/decision/notes must
    never turn an authorized deactivation into a spurious 'failed' event."""
    c = confirmation if isinstance(confirmation, dict) else {}
    rt = c.get("review_type")
    reviewer = c.get("reviewer")
    decided_at = c.get("decided_at")
    decision = c.get("decision")
    notes = c.get("notes")
    return {
        "review_type": rt if rt in _REVIEW_TYPES else "other",
        "reviewer": reviewer if (isinstance(reviewer, str) and reviewer.strip()) else "unknown",
        "decided_at": decided_at if _is_date_time(decided_at) else None,
        "decision": decision if isinstance(decision, str) else "confirmed",
        "notes": notes if isinstance(notes, str) else f"confirmed deactivation for: {detail}",
    }


def _overrides_for(mode):
    end = _target_end_state(mode)
    ov = [{"field": "active_status", "forced_value": end["active_status"],
           "reason": f"deactivate_source mode={mode}"},
          {"field": "collection_allowed", "forced_value": "false",
           "reason": "a deactivated Source cannot collect (Source rule R6)"}]
    if "review_status" in end:
        ov.append({"field": "review_status", "forced_value": end["review_status"],
                   "reason": "governance reject: review stop-state (Source rule R5)"})
    return ov


def _lineage0(src):
    ids = (src.get("provenance") or {}).get("promoted_from_candidate_ids") or []
    return ids[0] if ids else None


def _result(action, ok, event_status, source_id, active_status, event, candidate_id, reason, gates):
    return {"ok": ok, "action": action, "event_status": event_status,
            "source_id": source_id, "active_status": active_status,
            "event_id": event["event_id"] if event else None,
            "candidate_id": candidate_id, "reason": reason, "gates": gates}


# ---- deactivate_source (cases 3 cascade target + 4 direct) ------------------

def deactivate_source(conn, validators, source_id, *, mode, actor, confirmation=None,
                      candidate_id=None, now=None, workflow_version=WORKFLOW_VERSION):
    _require_valid_actor(actor)
    if mode not in _MODES:
        raise ValueError(f"invalid mode {mode!r}; expected one of {sorted(_MODES)}")
    now = now or util.now_iso()
    attempt_id = f"deact_{source_id}"

    def emit(event_status, gates, human_refs, failure_reason, before, after, ev_cid):
        if conn.in_transaction:
            safe_rollback(conn)
        with immediate_txn(conn):
            gen = _next_attempt_generation(conn, attempt_id)   # under the write lock: no cross-attempt collision
            ev = _make_event(conn, candidate_id=ev_cid, action="deactivate_source",
                             event_status=event_status, target_source_id=source_id, actor=actor,
                             gates=gates, overrides=[], failure_reason=failure_reason,
                             before=before, after=after, now=now, attempt_id=attempt_id,
                             attempt_generation=gen, workflow_version=workflow_version)
            ev["human_review_refs"] = human_refs
            _insert_event(conn, validators, ev)
        return ev

    # G3: source exists?
    src0 = get_source(conn, source_id)
    if src0 is None:
        cid = candidate_id or _AUDIT_SOURCE_ONLY
        gates = [{"gate": "G3_source_exists", "passed": False, "detail": "source not found"}]
        ev = emit("gate_failed", gates, [], "source not found", _EMPTY_REFS, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, "gate_failed", source_id, None, ev, cid, "source not found", gates)

    cid = candidate_id or _lineage0(src0) or _AUDIT_SOURCE_ONLY
    cref = None if cid == _AUDIT_SOURCE_ONLY else cid

    # G6: the CURRENT source must itself be schema-valid; we refuse to operate on an already
    # invalid/corrupt Source (that is the reconciler's job, a later increment).
    try:
        validate(validators, "source", src0)
    except ValidationError as e:
        gates = [{"gate": "G6_source_valid", "passed": False, "detail": str(e)}]
        before = {"candidate_ref": cref, "candidate_hash": None, "source_ref": source_id,
                  "source_hash": util.content_hash(src0)}
        ev = emit("gate_failed", gates, [], f"source invalid: {e}", before, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, "gate_failed", source_id, None, ev, cid, f"source invalid: {e}", gates)
    gates = [{"gate": "G6_source_valid", "passed": True, "detail": None}]
    before0 = {"candidate_ref": cref, "candidate_hash": None, "source_ref": source_id,
               "source_hash": util.content_hash(src0)}

    # A committed (state-changing) event MUST name a real candidate. If the target Source has no
    # lineage and the caller gave no candidate_id, we cannot attribute the deactivation -- fail
    # closed rather than fabricate the sentinel onto a committed event. (Decision 4: lineage-less
    # manual_seed/imported Sources need an explicit candidate_id or a future source-only event
    # path; the sentinel stays confined to non-committed gate_failed events, per its own invariant.)
    if cid == _AUDIT_SOURCE_ONLY:
        gates.append({"gate": "G_audit_candidate", "passed": False,
                      "detail": "lineage-less Source requires an explicit candidate_id to attribute the deactivation"})
        ev = emit("gate_failed", gates, [], "lineage-less source requires an explicit candidate_id",
                  before0, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, "gate_failed", source_id, None, ev, cid,
                       "lineage-less source requires an explicit candidate_id", gates)

    # idempotency: already in this mode's end-state?
    if _already_deactivated(src0, mode):
        gates.append({"gate": "idempotency", "passed": False, "detail": f"source already in '{mode}' end-state"})
        ev = emit("no_op", gates, [], f"already {mode}", before0, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, "no_op", source_id, src0.get("active_status"), ev, cid,
                       f"already {mode}", gates)

    # human-confirmation gate (a real sign-off is required; a falsy/garbage value is NOT one)
    reasons = _confirmation_reasons(src0)
    confirmed_href = []
    if reasons and not _is_valid_confirmation(confirmation):
        detail = "; ".join(reasons)
        gates.append({"gate": "human_confirmation", "passed": False, "detail": detail})
        ev = emit("awaiting_human", gates, [_await_ref(detail)], None, before0, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, "awaiting_human", source_id, src0.get("active_status"), ev, cid,
                       detail, gates)
    if reasons:
        confirmed_href = [_confirmation_ref(confirmation, "; ".join(reasons))]
        gates.append({"gate": "human_confirmation", "passed": True,
                      "detail": "confirmation supplied for: " + "; ".join(reasons)})
    else:
        gates.append({"gate": "human_confirmation", "passed": True, "detail": "no confirmation required"})

    # transactional deactivation: re-read + re-check ALL gates under the write lock.
    try:
        with immediate_txn(conn):
            fresh = get_source(conn, source_id)
            if fresh is None:
                raise _Abort("gate_failed", "source vanished under the lock")
            try:
                validate(validators, "source", fresh)
            except ValidationError as e:
                raise _Abort("gate_failed", f"source invalid under the lock: {e}")
            if _already_deactivated(fresh, mode):
                raise _Abort("no_op", f"already {mode} (under the lock)")
            fresh_reasons = _confirmation_reasons(fresh)
            if fresh_reasons and not _is_valid_confirmation(confirmation):
                raise _Abort("awaiting_human", "; ".join(fresh_reasons))

            new_src = copy.deepcopy(fresh)
            end = _target_end_state(mode)
            new_src["active_status"] = end["active_status"]
            new_src["collection_allowed"] = False
            if "review_status" in end:
                new_src["review_status"] = end["review_status"]
            new_src["updated_at"] = now
            validate(validators, "source", new_src)      # G6 safety on the deactivated record
            gates.append({"gate": "G6_deactivated_source_safety", "passed": True,
                          "detail": f"active_status={new_src['active_status']}, "
                                    f"review_status={new_src['review_status']}, collection_allowed=false"})

            before = {"candidate_ref": cref, "candidate_hash": None, "source_ref": source_id,
                      "source_hash": util.content_hash(fresh)}
            conn.execute("UPDATE source SET doc=? WHERE source_id=?",
                         (util.canonical_json(new_src), source_id))
            p_src = get_source(conn, source_id)
            if p_src is None or util.content_hash(p_src) != util.content_hash(new_src):
                raise RuntimeError("source deactivation did not persist correctly")
            after = {"candidate_ref": cref, "candidate_hash": None, "source_ref": source_id,
                     "source_hash": util.content_hash(p_src)}
            gen = _next_attempt_generation(conn, attempt_id)   # under the write lock: no cross-attempt collision
            ev = _make_event(conn, candidate_id=cid, action="deactivate_source", event_status="committed",
                             target_source_id=source_id, actor=actor, gates=gates, overrides=_overrides_for(mode),
                             failure_reason=None, before=before, after=after, now=now, attempt_id=attempt_id,
                             attempt_generation=gen, workflow_version=workflow_version)
            ev["human_review_refs"] = confirmed_href
            _insert_event(conn, validators, ev)
        return _result("deactivate_source", True, "committed", source_id, new_src["active_status"], ev, cid, None, gates)
    except _Abort as ab:
        if ab.status == "awaiting_human":
            hrefs, fr = [_await_ref(ab.reason)], None
        elif ab.status in _FAIL_STATES:
            hrefs, fr = [], ab.reason
        else:  # no_op
            hrefs, fr = [], ab.reason
        ev = emit(ab.status, gates, hrefs, fr, before0, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, ab.status, source_id, None, ev, cid, ab.reason, gates)
    except sqlite3.IntegrityError as e:
        gates.append({"gate": "write_integrity", "passed": False, "detail": str(e)})
        ev = emit("gate_failed", gates, [], f"integrity: {e}", before0, _EMPTY_REFS, cid)
        return _result("deactivate_source", False, "gate_failed", source_id, None, ev, cid, f"integrity: {e}", gates)
    except Exception as e:  # noqa: BLE001
        gates.append({"gate": "write", "passed": False, "detail": str(e)})
        try:
            ev = emit("failed", gates, [], f"write failed: {e}", before0, _EMPTY_REFS, cid)
        except Exception as audit_err:  # noqa: BLE001
            safe_rollback(conn)
            raise RuntimeError(f"deactivate failed AND audit write failed: primary={e!r}; audit={audit_err!r}") from e
        return _result("deactivate_source", False, "failed", source_id, None, ev, cid, f"write failed: {e}", gates)


# ---- reject / retire candidate (cases 1/2 direct, case 3 cascade) ----------

def reject_candidate(conn, validators, candidate_id, *, actor, reason=None, confirmation=None,
                     now=None, workflow_version=WORKFLOW_VERSION):
    return _dispose_candidate(conn, validators, candidate_id, disposition="rejected", action="reject",
                              source_mode="reject", reason=reason, actor=actor, confirmation=confirmation,
                              now=now, wv=workflow_version)


def retire_candidate(conn, validators, candidate_id, *, actor, confirmation=None,
                     now=None, workflow_version=WORKFLOW_VERSION):
    return _dispose_candidate(conn, validators, candidate_id, disposition="retired", action="retire",
                              source_mode="retire", reason=None, actor=actor, confirmation=confirmation,
                              now=now, wv=workflow_version)


def _dispose_candidate(conn, validators, candidate_id, *, disposition, action, source_mode,
                       reason, actor, confirmation, now, wv):
    _require_valid_actor(actor)
    now = now or util.now_iso()
    attempt_id = f"{action}_{candidate_id}"

    def emit(event_status, gates, failure_reason, before, after):
        if conn.in_transaction:
            safe_rollback(conn)
        with immediate_txn(conn):
            gen = _next_attempt_generation(conn, attempt_id)   # under the write lock: no cross-attempt collision
            ev = _make_event(conn, candidate_id=candidate_id, action=action, event_status=event_status,
                             target_source_id=None, actor=actor, gates=gates, overrides=[],
                             failure_reason=failure_reason, before=before, after=after, now=now,
                             attempt_id=attempt_id, attempt_generation=gen, workflow_version=wv)
            _insert_event(conn, validators, ev)
        return ev

    # G1: load + schema-validate the candidate
    cand = get_candidate(conn, candidate_id)
    if cand is None:
        gates = [{"gate": "G1_candidate_loads", "passed": False, "detail": "candidate not found"}]
        ev = emit("gate_failed", gates, "candidate not found", _EMPTY_REFS, _EMPTY_REFS)
        return _result(action, False, "gate_failed", None, None, ev, candidate_id, "candidate not found", gates)
    try:
        validate(validators, "source_candidate", cand)
    except ValidationError as e:
        gates = [{"gate": "G1_candidate_schema_valid", "passed": False, "detail": str(e)}]
        ev = emit("gate_failed", gates, str(e), _EMPTY_REFS, _EMPTY_REFS)
        return _result(action, False, "gate_failed", None, None, ev, candidate_id, str(e), gates)
    gates = [{"gate": "G1_candidate_schema_valid", "passed": True, "detail": None}]
    before_c = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(cand),
                "source_ref": None, "source_hash": None}

    ps = (cand.get("promotion") or {}).get("promotion_status")

    # already terminally disposed -> idempotent no_op
    if ps in ("rejected", "retired"):
        gates.append({"gate": "idempotency", "passed": False, "detail": f"candidate already {ps}"})
        ev = emit("no_op", gates, f"already {ps}", before_c, _EMPTY_REFS)
        return _result(action, False, "no_op", None, None, ev, candidate_id, f"already {ps}", gates)

    # CASE 3 (cascade-only): already promoted/merged -> deactivate the Source; DO NOT mutate
    # the candidate row, its link, or the Source's provenance lineage (locked decision 1).
    if ps in ("promoted", "merged"):
        sid = (cand.get("promotion") or {}).get("promoted_source_id")
        if not sid:
            gates.append({"gate": "G_cascade_target", "passed": False,
                          "detail": f"candidate promotion_status={ps} but promoted_source_id is null"})
            ev = emit("gate_failed", gates, "promoted candidate has no promoted_source_id", before_c, _EMPTY_REFS)
            return _result(action, False, "gate_failed", None, None, ev, candidate_id,
                           "promoted candidate has no promoted_source_id", gates)
        # Delegate to deactivate_source, tagging the event with THIS candidate for audit linkage.
        return deactivate_source(conn, validators, sid, mode=source_mode, actor=actor,
                                 confirmation=confirmation, candidate_id=candidate_id,
                                 now=now, workflow_version=wv)

    # CASE 1/2: un-promoted candidate -> set its terminal disposition. No Source, no confirmation
    # gate (there is no Source whose safety could be affected).
    try:
        with immediate_txn(conn):
            fresh = get_candidate(conn, candidate_id)          # re-read under the lock
            if fresh is None:
                raise _Abort("gate_failed", "candidate vanished under the lock")
            fps = (fresh.get("promotion") or {}).get("promotion_status")
            if fps in ("rejected", "retired"):
                raise _Abort("no_op", f"already {fps} (under the lock)")
            if fps in ("promoted", "merged"):
                # concurrently promoted between our snapshot and the lock: the un-promoted path is
                # no longer correct (case 3 cascade is), so bail as no_op and let the caller re-run.
                raise _Abort("no_op", "candidate was concurrently promoted; re-run to cascade to the Source")
            if fps != "not_promoted":
                raise _Abort("gate_failed", f"unexpected promotion_status={fps}")

            new_c = copy.deepcopy(fresh)
            new_c["promotion"]["promotion_status"] = disposition
            if action == "reject":
                new_c["review"]["review_status"] = "rejected"
                new_c["review"]["rejection_reason"] = reason or "rejected via reject_candidate"
            new_c["updated_at"] = now
            new_c["lifecycle_status"] = _rollup_lifecycle(new_c)
            validate(validators, "source_candidate", new_c)
            gates.append({"gate": "candidate_disposition_valid", "passed": True,
                          "detail": f"promotion_status={disposition}, lifecycle_status={new_c['lifecycle_status']}"})
            before = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(fresh),
                      "source_ref": None, "source_hash": None}
            conn.execute("UPDATE source_candidate SET doc=? WHERE candidate_id=?",
                         (util.canonical_json(new_c), candidate_id))
            p_cand = get_candidate(conn, candidate_id)
            if p_cand is None or util.content_hash(p_cand) != util.content_hash(new_c):
                raise RuntimeError("candidate disposition did not persist correctly")
            after = {"candidate_ref": candidate_id, "candidate_hash": util.content_hash(p_cand),
                     "source_ref": None, "source_hash": None}
            gen = _next_attempt_generation(conn, attempt_id)   # under the write lock: no cross-attempt collision
            ev = _make_event(conn, candidate_id=candidate_id, action=action, event_status="committed",
                             target_source_id=None, actor=actor, gates=gates, overrides=[],
                             failure_reason=None, before=before, after=after, now=now,
                             attempt_id=attempt_id, attempt_generation=gen, workflow_version=wv)
            _insert_event(conn, validators, ev)
        return _result(action, True, "committed", None, None, ev, candidate_id, None, gates)
    except _Abort as ab:
        fr = ab.reason if ab.status in _FAIL_STATES or ab.status == "no_op" else None
        ev = emit(ab.status, gates, fr, before_c, _EMPTY_REFS)
        return _result(action, False, ab.status, None, None, ev, candidate_id, ab.reason, gates)
    except Exception as e:  # noqa: BLE001
        gates.append({"gate": "write", "passed": False, "detail": str(e)})
        try:
            ev = emit("failed", gates, f"write failed: {e}", before_c, _EMPTY_REFS)
        except Exception as audit_err:  # noqa: BLE001
            safe_rollback(conn)
            raise RuntimeError(f"{action} failed AND audit write failed: primary={e!r}; audit={audit_err!r}") from e
        return _result(action, False, "failed", None, None, ev, candidate_id, f"write failed: {e}", gates)
