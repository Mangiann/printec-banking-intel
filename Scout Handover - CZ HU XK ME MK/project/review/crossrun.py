"""Cross-run / registry novelty check — the review-prep layer that turns a scout run into a DELTA.

The scout re-finds the same sources every run, so a reviewer should only see what is NEW. This module
classifies each candidate of a run by its normalized `canonical_url` against the accumulated corpus:

  - "in_registry"     : the URL is already an authoritative Source Registry record (already known).
  - "seen_prior_run"  : the URL already appeared as a candidate in an earlier run (already in the worklist).
  - "new"             : the URL is novel -> belongs in the review delta.

Read-only and deterministic: it reads the scout's data/ candidate files and (optionally) the promotion
registry, and produces a re-computable worklist. It NEVER mutates a run's records, NEVER promotes, and
does NOT import the promotion write path. Match is on the exact stored `canonical_url` (the runner already
normalized it), so a match is only ever a true same-URL match — a genuinely new source is never hidden.

NOTE: "prior" currently counts any earlier candidate regardless of its (not-yet-tracked) human review
outcome; once the review round-trip exists, rejected/decided candidates can refine what counts as known.
"""
import json
import sqlite3
from collections import Counter
from pathlib import Path

from _safe import dget, sstr


def load_run_candidates(data_root, run_id):
    p = Path(data_root) / "source_candidates" / f"{run_id}.jsonl"
    if not p.exists():
        return []
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]


def build_prior_index(data_root, exclude_run_id):
    """{canonical_url -> first-seen candidate_id} across ALL runs except `exclude_run_id`."""
    idx = {}
    folder = Path(data_root) / "source_candidates"
    if not folder.exists():
        return idx
    for f in sorted(folder.glob("*.jsonl")):
        if f.stem == exclude_run_id:
            continue
        for ln in f.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                c = json.loads(ln)
            except ValueError:
                continue
            u = c.get("canonical_url")
            if isinstance(u, str) and u not in idx:
                idx[u] = c.get("candidate_id")
    return idx


def build_registry_index(registry_db):
    """{canonical_url -> source_id} from the promotion registry (read-only). Empty when no db exists.

    Reads the `source` table's canonical_url via a read-only SQLite connection — a thin, decoupled read
    (no import of the promotion write path)."""
    idx = {}
    if not registry_db or not Path(registry_db).exists():
        return idx
    conn = sqlite3.connect(f"file:{Path(registry_db)}?mode=ro", uri=True)
    try:
        rows = conn.execute("SELECT source_id, json_extract(doc, '$.canonical_url') FROM source").fetchall()
    except sqlite3.Error:
        return idx     # no source table / unreadable -> treat registry as empty
    finally:
        conn.close()
    for sid, url in rows:
        if isinstance(url, str) and url not in idx:
            idx[url] = sid
    return idx


def classify(candidates, prior_by_url, registry_by_url):
    """Classify each candidate's novelty. A registry match takes precedence over a prior-candidate match."""
    out = []
    for c in candidates:
        c = c if isinstance(c, dict) else {}   # TOTAL: a non-dict jsonl line degrades to neutral, never raises
        u = c.get("canonical_url")
        key = sstr(u)                       # only a str can key the url indexes; None can't match -> "new"
        sid = registry_by_url.get(key)
        pid = prior_by_url.get(key)
        if sid is not None:
            novelty, ms, mc = "in_registry", sid, None
        elif pid is not None:
            novelty, ms, mc = "seen_prior_run", None, pid
        else:
            novelty, ms, mc = "new", None, None
        out.append({
            "candidate_id": c.get("candidate_id"),
            "source_name": c.get("source_name"),
            "canonical_url": u,
            "source_class": c.get("source_class"),
            "access_status": c.get("access_status"),
            "priority": c.get("priority"),
            "url_verification": dget(c.get("url_verification"), "status"),
            "within_run_dedupe": dget(c.get("dedupe"), "dedupe_status"),
            "why_relevant": dget(c.get("discovery_basis"), "why_relevant"),
            "novelty": novelty,
            "matched_source_id": ms,
            "matched_candidate_id": mc,
        })
    return out


def summarize(classification):
    c = Counter(x["novelty"] for x in classification)
    return {"total": len(classification), "new": c.get("new", 0),
            "seen_prior_run": c.get("seen_prior_run", 0), "in_registry": c.get("in_registry", 0)}


def compute_review_delta(data_root, run_id, *, registry_db=None):
    """Return (classification, summary) for `run_id` against the prior corpus + registry."""
    cands = load_run_candidates(data_root, run_id)
    prior = build_prior_index(data_root, run_id)
    registry = build_registry_index(registry_db)
    classification = classify(cands, prior, registry)
    return classification, summarize(classification)


def write_review_delta(data_root, run_id, classification):
    """Persist the classification (the review worklist) as JSONL under the run's log folder."""
    d = Path(data_root) / "run_logs" / run_id
    d.mkdir(parents=True, exist_ok=True)
    fpath = d / "review_delta.jsonl"
    fpath.write_text("".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in classification),
                     encoding="utf-8")
    return str(fpath)
