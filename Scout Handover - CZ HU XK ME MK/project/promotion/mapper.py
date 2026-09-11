"""Pure mapping: an approved unique SourceCandidate -> a new Source draft.

Direct carries + the workstream->workstreams shape transform + workflow-computed
fields + conservative registry defaults (Q4) + safety-derived collection_allowed /
active_status. See docs/promotion_workflow.md section 6/7.
"""
from .safety import derive_collection_allowed, derive_active_status

# candidate field -> source field, carried verbatim when present (same names)
_OPTIONAL_CARRIES = [
    "country_name", "region", "source_owner", "source_publisher_type",
    "related_entities", "bias_profile", "coverage_notes", "tags",
    "expected_update_pattern", "access_review_task_id",
]


def map_candidate_to_source(cand, *, source_id, record_owner, refresh_cadence,
                            actor, now, has_open_access_task):
    """Return (source_dict, safety_overrides). Deterministic and side-effect-free."""
    overrides = []
    access = cand["access_status"]
    legal = cand["legal_status"]

    collection_allowed, forced = derive_collection_allowed(access, legal, cand["collection_allowed"])
    if forced:
        overrides.append({
            "field": "collection_allowed", "forced_value": "false",
            "reason": f"access_status={access} / legal_status={legal} forbids collection (S1/S2)",
        })

    review_status = "approved"  # only approved candidates promote in
    uv_status = (cand.get("url_verification") or {}).get("status", "not_checked")
    active_status = derive_active_status(
        collection_allowed=collection_allowed, access_status=access, legal_status=legal,
        review_status=review_status, url_verification_status=uv_status,
        has_open_access_task=has_open_access_task,
    )
    if active_status != "active":
        overrides.append({
            "field": "active_status", "forced_value": active_status,
            "reason": ("G9 activation predicate not satisfied "
                       f"(collection_allowed={collection_allowed}, access={access}, legal={legal}, "
                       f"url_verification={uv_status}, open_access_task={has_open_access_task})"),
        })

    review = cand.get("review") or {}
    src = {
        "source_id": source_id,
        "provenance": {
            "origin": "promoted_from_candidate",
            "promoted_from_candidate_ids": [cand["candidate_id"]],
            "promoted_by": actor.get("actor_id"),
            "promoted_at": now,
            "origin_discovery_run_id": cand.get("discovery_run_id"),
        },
        "created_at": now,
        "updated_at": now,
        "name": cand["source_name"],
        "url_or_endpoint": cand["source_url"],
        "canonical_url": cand["canonical_url"],
        "domain": cand["domain"],
        "source_class": cand["source_class"],
        "source_subtype": cand["source_subtype"],
        "country": cand["country"],
        "global_scope": False,
        "sector": cand["sector"],
        "workstreams": [cand["workstream"]],           # shape transform (single -> array)
        "topics": list(cand["topics"]),
        "primary_language": cand["primary_language"],
        "credibility_score": cand["credibility_score"],
        "usefulness_score": cand["usefulness_score"],
        "priority": cand["priority"],
        "reason_to_track": cand["discovery_basis"]["why_relevant"],
        "collection_method": cand["suggested_collection_method"],
        "refresh_cadence": refresh_cadence,
        "collection_allowed": collection_allowed,
        "access_status": access,
        "legal_status": legal,
        "redistribution_allowed": False,               # Q4 conservative default
        "retention_policy": None,                       # Q4 default
        "monitoring_state": {
            "last_checked_at": None, "next_check_at": None,
            "last_successful_ingestion_at": None, "failure_count": 0,
        },
        "review_status": review_status,
        "active_status": active_status,
        "reviewer": review.get("reviewer"),
        "reviewed_at": review.get("reviewed_at"),
        "record_owner": record_owner,                   # mandatory human input (G5)
        # confidence_score intentionally dropped (candidate-assessment only)
    }
    for key in _OPTIONAL_CARRIES:
        val = cand.get(key)
        if val is not None:
            src[key] = val
    return src, overrides
