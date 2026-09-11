"""Shared deterministic Source metadata enrichment, used by BOTH merge_into_existing and
update_existing.

Unions array fields; fills empty scalars only (never overwrites a populated scalar);
tightens access/legal via the approved restrictiveness ordering; re-derives
collection_allowed (AND, with hard-stop / indeterminate / unrankable dispositions all
gating collection to false); re-derives active_status TIGHTEN-ONLY.

It does NOT touch lineage (provenance.promoted_from_candidate_ids) or links -- that is the
caller's responsibility: merge appends lineage, update_existing does not.
"""
from .restrictiveness import resolve
from .safety import ACCESS_FORBIDDEN

# (source scalar field, extractor from the candidate)
_SCALAR_FILL = [
    ("country_name", lambda c: c.get("country_name")),
    ("region", lambda c: c.get("region")),
    ("source_owner", lambda c: c.get("source_owner")),
    ("source_publisher_type", lambda c: c.get("source_publisher_type")),
    ("bias_profile", lambda c: c.get("bias_profile")),
    ("coverage_notes", lambda c: c.get("coverage_notes")),
    ("expected_update_pattern", lambda c: c.get("expected_update_pattern")),
    ("access_review_task_id", lambda c: c.get("access_review_task_id")),
    ("reason_to_track", lambda c: (c.get("discovery_basis") or {}).get("why_relevant")),
]


def union(existing, incoming):
    out = list(existing or [])
    for v in (incoming or []):
        if v not in out:
            out.append(v)
    return out


def conflict_flag(msg):
    return {"review_type": "scalar_conflict_resolution", "reviewer": "system-flagged",
            "decided_at": None, "decision": None, "notes": msg}


def enrich_metadata(m, cand, now):
    """Mutate the Source dict `m` in place with the candidate's metadata.

    Returns (overrides, human_refs). Does NOT modify provenance/lineage or links.
    `m` must be the working copy of the target (its original collection_allowed /
    active_status are read as the pre-enrichment baseline).
    """
    overrides, human_refs = [], []
    orig_ca = m.get("collection_allowed")
    orig_active = m.get("active_status")

    # 1) union array fields
    m["workstreams"] = union(m.get("workstreams"), [cand["workstream"]])
    m["topics"] = union(m.get("topics"), cand.get("topics"))
    for field, cval in (("related_entities", cand.get("related_entities")), ("tags", cand.get("tags"))):
        if cval is not None:
            m[field] = union(m.get(field), cval)

    # 2) fill empty scalars only; flag (never overwrite) populated conflicts
    for field, getter in _SCALAR_FILL:
        cval = getter(cand)
        if cval is None:
            continue
        tval = m.get(field)
        if tval is None:
            m[field] = cval
        elif tval != cval:
            human_refs.append(conflict_flag(
                f"scalar conflict on '{field}': kept target {tval!r}, candidate had {cval!r} (needs human review)"))

    # 3) safety tightening: access & legal restrictiveness ordering.
    #    Hard-stop, indeterminate, or unrankable dispositions all gate collection to false.
    force_false = False
    for kind, field in (("access", "access_status"), ("legal", "legal_status")):
        r = resolve(kind, m.get(field), cand.get(field))
        if r["unrankable"]:
            force_false = True
            human_refs.append(conflict_flag(
                f"unrankable {field} pair (target={m.get(field)!r}, candidate={cand.get(field)!r}); "
                "failing closed (collection disabled) pending human review"))
            continue  # keep target's recorded value
        if r["value"] != m.get(field):
            overrides.append({"field": field, "forced_value": str(r["value"]),
                              "reason": f"enrichment tightened {field} to the more-restrictive value"})
            m[field] = r["value"]
        if r["hard_stop"]:
            force_false = True
        if r["escalate"]:
            force_false = True   # indeterminate conflict -> collection stays gated (section 7 rule 4)
            human_refs.append(conflict_flag(
                f"indeterminate {field} conflict resolved conservatively to {m.get(field)!r}; "
                "collection disabled pending human review"))

    # 4) collection_allowed = AND(target, candidate), then hard-stops. Never loosens the target.
    merged_ca = bool(orig_ca) and bool(cand.get("collection_allowed"))
    if force_false or m.get("access_status") == ACCESS_FORBIDDEN or m.get("legal_status") == "forbidden":
        merged_ca = False
    if merged_ca != orig_ca:
        overrides.append({"field": "collection_allowed", "forced_value": str(merged_ca).lower(),
                          "reason": "re-derived collection_allowed (AND + hard-stops/indeterminate gating)"})
    m["collection_allowed"] = merged_ca

    # 5) active_status re-derived TIGHTEN-ONLY: a paused target is never auto-activated.
    still_ok = (merged_ca is True and m.get("access_status") == "public"
                and m.get("legal_status") == "allowed" and m.get("review_status") == "approved"
                and m.get("access_review_task_id") is None)
    new_active = "active" if (orig_active == "active" and still_ok) else "paused"
    if new_active != orig_active:
        overrides.append({"field": "active_status", "forced_value": new_active,
                          "reason": "re-derived active_status (G9 predicate; tighten-only)"})
    m["active_status"] = new_active

    m["updated_at"] = now
    return overrides, human_refs
