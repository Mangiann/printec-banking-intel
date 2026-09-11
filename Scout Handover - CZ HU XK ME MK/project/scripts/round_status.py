#!/usr/bin/env python3
"""Scout-round CHECKPOINT / RESUME status — so a session that hit the usage window never loses its place.

Every stage of a scout round writes a durable artifact to disk. This tool reads those artifacts for a
run_id and reports which stages are DONE vs PENDING, then prints the exact command to resume from the
first pending stage. It mutates nothing — safe to run any time, in any session.

    python scripts/round_status.py --run-id dr_gr_a2_live_003 [--promotion-db data/promotion.db]

The guarantee: heavy discovery runs in the background (survives interrupts); each later stage is a durable
checkpoint; the deterministic stages are idempotent (re-running resumes, never double-charges finished work).
"""
import argparse
import json
import sqlite3
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


def _exists_nonempty(p):
    return p.exists() and p.stat().st_size > 0


def _count_jsonl(p):
    if not _exists_nonempty(p):
        return 0
    try:
        return sum(1 for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip())
    except OSError:
        return 0


def _run_urls(candidates_path):
    """The set of canonical_urls in a run's candidate file (the stable key for 'was this synced?')."""
    urls = set()
    if not _exists_nonempty(candidates_path):
        return urls
    for ln in candidates_path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        try:
            c = json.loads(ln)
        except ValueError:
            continue
        u = c.get("canonical_url") if isinstance(c, dict) else None
        if isinstance(u, str):
            urls.add(u)
    return urls


def _registry_has_run(db, run_urls):
    """How many of this run's candidate URLs are already in the registry (i.e. the run was synced). Match on
    canonical_url — candidate_ids (c_001) carry no run_id, and promoted docs keep lineage under provenance,
    so a URL overlap is the only reliable signal."""
    if not db or not Path(db).exists():
        return None
    if not run_urls:
        return 0
    try:
        conn = sqlite3.connect(f"file:{Path(db)}?mode=ro", uri=True)
    except sqlite3.Error:
        return None
    try:
        reg = {u for (u,) in conn.execute("SELECT json_extract(doc,'$.canonical_url') FROM source")
               if isinstance(u, str)}
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    return len(run_urls & reg)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Report a scout round's checkpoint/resume status.")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--config", default=str(_ROOT / "configs/discovery_runs/gr_a2_tenders_procurement.yaml"))
    ap.add_argument("--promotion-db", default=str(_ROOT / "data/promotion.db"))
    ap.add_argument("--deliverables", default=str(_ROOT / "deliverables"))
    args = ap.parse_args(argv)

    rid = args.run_id
    data = Path(args.data_root)
    ai = data / "run_logs" / rid / "agent_inputs"
    artifacts = data / "run_logs" / rid / "artifacts"      # machine zone (review sheet, ledgers, grouped)

    scout_output = ai / "scout_output.json"
    candidates = data / "source_candidates" / f"{rid}.jsonl"
    recovery = ai / "recovery_results.json"
    roles = ai / "role_verdicts.json"
    suggestions = ai / "decision_suggestions.json"
    review_sheet = artifacts / f"REVIEW_{rid}.xlsx"        # the pipeline's stage-6 output (not a deliverable)
    delta = data / "run_logs" / rid / "review_delta.jsonl"

    # (stage, kind[agent|deterministic], done?, detail, resume-hint)
    stages = []
    stages.append(("1 discovery", "agent", _exists_nonempty(scout_output),
                   f"{scout_output}" if _exists_nonempty(scout_output) else "MISSING scout_output.json",
                   "Workflow(discovery_workflow.js) -> save result to agent_inputs/scout_output.json"))
    ncand = _count_jsonl(candidates)
    stages.append(("2 ingest", "deterministic", ncand > 0,
                   f"{ncand} candidates in {candidates.name}" if ncand else "not ingested",
                   f"run_pipeline.py --run-id {rid} --compact {scout_output} --config <cfg> --verify --promotion-db <db>"))
    stages.append(("3 recovery", "agent", _exists_nonempty(recovery),
                   f"{recovery.name}" if _exists_nonempty(recovery) else "no browser recovery results yet",
                   "spawn the browser-recovery Agent (SCOUT_ROUTINE step 3) -> recovery_results.json"))
    stages.append(("4 labeling", "agent", _exists_nonempty(roles) and _exists_nonempty(suggestions),
                   f"roles={_exists_nonempty(roles)} suggestions={_exists_nonempty(suggestions)}",
                   "run the labeling passes (SCOUT_ROUTINE step 4) -> role_verdicts.json + decision_suggestions.json"))
    stages.append(("5 pipeline", "deterministic", _exists_nonempty(review_sheet),
                   f"{review_sheet.name}" if _exists_nonempty(review_sheet) else "deliverables not built",
                   f"run_pipeline.py --run-id {rid} --config <cfg> --recovery-results ... --roles ... --suggestions ... --promotion-db <db>"))
    promoted = _registry_has_run(args.promotion_db, _run_urls(candidates))
    stages.append(("6 sync", "deterministic", bool(promoted),
                   (f"{promoted} of this run's URLs are in the registry" if promoted else "not synced")
                   if promoted is not None else "registry unreadable",
                   f"sync_registry.py --db <db> --run-id {rid} --review {review_sheet}"))
    stages.append(("7 report", "deterministic (read-only)", _exists_nonempty(delta),
                   "convergence delta computed" if _exists_nonempty(delta) else "not computed",
                   f"crossrun.compute_review_delta('data','{rid}',registry_db=<db>)"))

    print(f"\n=== Scout round checkpoint: {rid} ===")
    first_pending = None
    for name, kind, done, detail, hint in stages:
        mark = "DONE " if done else "PENDING"
        print(f"  [{mark}] {name:<14} ({kind}) — {detail}")
        if not done and first_pending is None:
            first_pending = (name, kind, hint)

    print()
    if first_pending is None:
        print("All stages complete. Nothing to resume.")
    else:
        name, kind, hint = first_pending
        tag = "AGENT step — an agent must run it" if kind.startswith("agent") else "deterministic — safe to re-run"
        print(f"RESUME AT -> {name}  ({tag})")
        print(f"   {hint}")
    print("\nNothing above is ever lost to a window/token limit: discovery runs in the background and every")
    print("stage persists a durable artifact; the deterministic stages are idempotent, so resuming re-runs safely.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
