"""Deterministic, fail-closed validation gates for the promote_new path.

Covers G2 (review approved / human-reviewed), G3 (dedupe unique), G4 (idempotency),
G5 (record_owner assigned). G1 (schema-valid load) and G6 (mapped Source satisfies
the safety schema) are enforced in promote.py; G9 (activation) is computed in mapper.py.
Merge/update gates (G7) are out of scope for this slice.
"""


def run_promote_new_gates(cand, record_owner):
    """Return (ok, gates) where gates is a list of {gate, passed, detail}."""
    gates = []
    ok = True

    def g(name, passed, detail=None):
        nonlocal ok
        passed = bool(passed)
        gates.append({"gate": name, "passed": passed, "detail": detail})
        ok = ok and passed

    review = cand.get("review") or {}
    rs = review.get("review_status")
    g("G2_review_approved", rs == "approved", None if rs == "approved" else f"review_status={rs}")

    if review.get("human_review_required"):
        has = bool(review.get("reviewer")) and bool(review.get("reviewed_at"))
        g("G2_human_reviewed", has,
          None if has else "human_review_required but reviewer/reviewed_at missing")

    ds = (cand.get("dedupe") or {}).get("dedupe_status")
    g("G3_dedupe_unique", ds == "unique",
      None if ds == "unique" else f"dedupe_status={ds} (promote_new requires unique)")

    ps = (cand.get("promotion") or {}).get("promotion_status")
    g("G4_not_promoted", ps == "not_promoted",
      None if ps == "not_promoted" else f"promotion_status={ps}")

    valid_owner = isinstance(record_owner, str) and record_owner.strip() != ""
    g("G5_record_owner", valid_owner,
      None if valid_owner else "record_owner must be a non-empty string (mandatory human assignment)")

    return ok, gates


def run_merge_gates(cand, sources):
    """Gates for merge_into_existing. Returns (ok, gates, target_id).

    target_id is the single resolved duplicate source_id, or None if G3 fails.
    G7 (target not blocked) is checked by the caller once the target is loaded.
    """
    gates = []
    ok = True

    def g(name, passed, detail=None):
        nonlocal ok
        passed = bool(passed)
        gates.append({"gate": name, "passed": passed, "detail": detail})
        ok = ok and passed

    review = cand.get("review") or {}
    rs = review.get("review_status")
    g("G2_review_approved", rs == "approved", None if rs == "approved" else f"review_status={rs}")
    if review.get("human_review_required"):
        has = bool(review.get("reviewer")) and bool(review.get("reviewed_at"))
        g("G2_human_reviewed", has, None if has else "human_review_required but reviewer/reviewed_at missing")

    dd = cand.get("dedupe") or {}
    ds = dd.get("dedupe_status")
    g("G3_dedupe_duplicate", ds == "duplicate",
      None if ds == "duplicate" else f"dedupe_status={ds} (merge requires 'duplicate')")

    ids = dd.get("possible_duplicate_source_ids") or []
    valid = [i for i in ids if i in sources]
    single_valid = len(ids) == 1 and len(valid) == 1
    g("G3_single_valid_target", single_valid,
      None if single_valid else
      f"possible_duplicate_source_ids must contain exactly one valid source_id "
      f"(have {len(ids)} id(s), {len(valid)} valid)")

    ps = (cand.get("promotion") or {}).get("promotion_status")
    g("G4_not_promoted", ps == "not_promoted",
      None if ps == "not_promoted" else f"promotion_status={ps}")

    return ok, gates, (valid[0] if single_valid else None)


def run_update_gates(cand, sources):
    """Gates for update_existing. Returns (ok, gates, target_id).

    Like merge but accepts dedupe_status 'possible_duplicate' OR 'duplicate' (update_existing
    contributes metadata without asserting the candidate is a confirmed source-defining
    duplicate). G7 (target not blocked) is checked by the caller once the target is loaded.
    """
    gates = []
    ok = True

    def g(name, passed, detail=None):
        nonlocal ok
        passed = bool(passed)
        gates.append({"gate": name, "passed": passed, "detail": detail})
        ok = ok and passed

    review = cand.get("review") or {}
    rs = review.get("review_status")
    g("G2_review_approved", rs == "approved", None if rs == "approved" else f"review_status={rs}")
    if review.get("human_review_required"):
        has = bool(review.get("reviewer")) and bool(review.get("reviewed_at"))
        g("G2_human_reviewed", has, None if has else "human_review_required but reviewer/reviewed_at missing")

    dd = cand.get("dedupe") or {}
    ds = dd.get("dedupe_status")
    g("G3_dedupe_possible_or_duplicate", ds in ("possible_duplicate", "duplicate"),
      None if ds in ("possible_duplicate", "duplicate") else
      f"dedupe_status={ds} (update_existing requires 'possible_duplicate' or 'duplicate')")

    ids = dd.get("possible_duplicate_source_ids") or []
    valid = [i for i in ids if i in sources]
    single_valid = len(ids) == 1 and len(valid) == 1
    g("G3_single_valid_target", single_valid,
      None if single_valid else
      f"possible_duplicate_source_ids must contain exactly one valid source_id "
      f"(have {len(ids)} id(s), {len(valid)} valid)")

    ps = (cand.get("promotion") or {}).get("promotion_status")
    g("G4_not_promoted", ps == "not_promoted",
      None if ps == "not_promoted" else f"promotion_status={ps}")

    return ok, gates, (valid[0] if single_valid else None)
