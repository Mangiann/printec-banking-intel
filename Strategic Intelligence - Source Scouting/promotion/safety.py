"""Deterministic safety derivation for the Source record produced by promotion.

These functions compute collection_allowed and active_status so the resulting
Source satisfies the Source schema's safety rules (S1/S2/S3 and the G9 activation
predicate from docs/promotion_workflow.md section 7). No LLM reasoning here.
"""

ACCESS_FORBIDDEN = "forbidden_do_not_collect"
LEGAL_FORBIDDEN = "forbidden"


def derive_collection_allowed(access_status, legal_status, candidate_collection_allowed):
    """Return (collection_allowed, was_forced_false).

    Forbidden access/legal force collection_allowed=False (Source rules S1/S2).
    Otherwise carry the candidate's value. Intermediate access_status values
    (requires_*, blocked, unknown) describe difficulty, NOT prohibition, and do
    not force the permission (that is a human/workflow decision recorded upstream).
    """
    if access_status == ACCESS_FORBIDDEN or legal_status == LEGAL_FORBIDDEN:
        return False, (candidate_collection_allowed is not False)
    return bool(candidate_collection_allowed), False


def derive_active_status(*, collection_allowed, access_status, legal_status,
                         review_status, url_verification_status, has_open_access_task):
    """G9 activation predicate. 'active' only if EVERY condition holds; else 'paused'.

    A source may be registered (and even scheduled for access/legal re-review) while
    paused; it just must not be actively collected until fully cleared.
    """
    active = (
        collection_allowed is True
        and access_status == "public"
        and legal_status == "allowed"
        and review_status == "approved"
        and url_verification_status == "verified"
        and not has_open_access_task
    )
    return "active" if active else "paused"
