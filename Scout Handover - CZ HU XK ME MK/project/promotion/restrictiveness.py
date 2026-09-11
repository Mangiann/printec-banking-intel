"""Deterministic restrictiveness resolver for merge/update safety tightening.

Implements the APPROVED access_status / legal_status orderings (docs/promotion_workflow.md
section 7). Used to pick the more-restrictive RECORDED value on a merge. Collection safety is
decided separately by a boolean AND (false always wins), so no ordering choice here can loosen
collection_allowed. Ties/non-comparable pairs escalate to human review; unrankable (unknown
future) values fail closed.
"""

# higher rank = more restrictive
ACCESS_RANK = {
    "forbidden_do_not_collect": 9,
    "requires_legal_review": 8,
    "requires_credentials": 7,
    "requires_paid_subscription": 6,
    "blocked": 5,
    "requires_manual_download": 4,
    "requires_free_account": 3,
    "unknown": 2,
    "public": 1,
}
LEGAL_RANK = {
    "forbidden": 5,
    "restricted": 4,
    "requires_review": 3,
    "unclear": 2,
    "allowed": 1,
}
ACCESS_INDETERMINATE = {"unknown"}
LEGAL_INDETERMINATE = {"requires_review", "unclear"}
ACCESS_HARD_STOP = "forbidden_do_not_collect"
LEGAL_HARD_STOP = "forbidden"


def resolve(kind, a, b):
    """Resolve two access/legal values for a merge.

    kind: 'access' or 'legal'. Returns a dict:
      value      -- the more-restrictive recorded value (None if unrankable)
      escalate   -- True when an indeterminate or unrankable conflict needs human review
      unrankable -- True when a value is not in the ordering table (fail closed)
      hard_stop  -- True when the chosen value is a hard stop (forces collection_allowed=false)
    """
    rank = ACCESS_RANK if kind == "access" else LEGAL_RANK
    indeterminate = ACCESS_INDETERMINATE if kind == "access" else LEGAL_INDETERMINATE
    hard = ACCESS_HARD_STOP if kind == "access" else LEGAL_HARD_STOP

    # Unrankable check FIRST: an out-of-table value (e.g. a future enum addition) must fail
    # closed even when target == candidate, rather than being treated as a benign tie.
    if a not in rank or b not in rank:
        return {"value": None, "escalate": True, "unrankable": True, "hard_stop": False}
    if a == b:
        return {"value": a, "escalate": False, "unrankable": False, "hard_stop": a == hard}
    chosen = a if rank[a] >= rank[b] else b
    return {"value": chosen,
            "escalate": (a in indeterminate or b in indeterminate),
            "unrankable": False,
            "hard_stop": chosen == hard}
