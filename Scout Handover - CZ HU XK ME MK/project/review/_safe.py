"""Tiny total-function helpers for reading possibly-malformed on-disk records.

Candidate records are loaded straight from JSONL (crossrun.load_run_candidates) with no schema
enforcement, so a malformed row — a scalar where the schema declares an object, or a list where a string
enum belongs — can reach the review layer. These helpers keep the readers TOTAL (never raising): one bad
record degrades to blank/neutral fields instead of aborting a whole suggestion batch or export.
"""


def dget(obj, key, default=None):
    """`obj.get(key)` when obj is a dict, else `default`. Safe nested access on malformed records.

    Note `(obj or {}).get(key)` is NOT equivalent: `or {}` only substitutes for FALSY values, so a
    truthy non-dict (a bare string, a non-empty list) slips through and `.get` raises."""
    return obj.get(key, default) if isinstance(obj, dict) else default


def sstr(v):
    """`v` when it is a string, else None — so it is always safe as a dict key or in set membership.
    An unhashable value (list/dict) used in `x in <set>` or as a dict key raises TypeError otherwise."""
    return v if isinstance(v, str) else None
