#!/usr/bin/env python3
"""Post-discovery INGEST — one deterministic command the orchestrator calls after the discovery swarm.

The discovery scouts each write a compact slice file to `agent_inputs/scout_slices/`. This step:
  1. merges the slices into one scout_output.json (dedup candidates by url; skip any unparseable slice);
  2. runs the strict ingest (normalize -> runner: validate, HEAD-verify URLs, dedup, count) via run_pipeline;
  3. writes failed_urls.json (the input to the browser link-repair stage);
  4. builds the labeling batch files (the input to the labeling swarm).
Deterministic + total: a malformed slice is skipped with a warning, never crashes the round.

    python scripts/round_ingest.py --run-id dr_gr_a2_live_004 --config <cfg> --promotion-db data/promotion.db
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))
sys.path.insert(0, str(_ROOT / "review"))
sys.path.insert(0, str(_ROOT / "scripts"))

import prelabel  # noqa: E402
import consolidate  # noqa: E402
import run_pipeline  # noqa: E402
import recheck_failed_urls as recheck  # noqa: E402
import recheck_tier2 as recheck2  # noqa: E402


_ARRAY_KEYS = ["candidates", "negative_findings", "coverage_gaps", "glossary", "actors",
               "search_attempts", "failed_searches", "discovered_source_categories"]


def merge_slices(slice_dir):
    """Merge every scout slice into one compact dict. Dedup candidates by exact source_url. TOTAL: an
    unparseable / non-dict slice is skipped (counted), never fatal."""
    merged = {k: [] for k in _ARRAY_KEYS}
    merged["briefs"] = []
    seen, raw, skipped = set(), 0, 0
    d = Path(slice_dir)
    for f in sorted(d.glob("*.json")) if d.exists() else []:
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            skipped += 1
            continue
        if not isinstance(s, dict):
            skipped += 1
            continue
        for c in s.get("candidates") or []:
            raw += 1
            u = c.get("source_url", "").strip() if isinstance(c, dict) and isinstance(c.get("source_url"), str) else ""
            if u and u in seen:
                continue
            if u:
                seen.add(u)
            merged["candidates"].append(c)
        for k in _ARRAY_KEYS:
            if k == "candidates":
                continue
            v = s.get(k)
            if isinstance(v, list):
                merged[k].extend(v)
        b = s.get("brief")
        if isinstance(b, str) and b.strip():
            merged["briefs"].append(b)
    return merged, {"raw_candidates": raw, "unique_candidates": len(merged["candidates"]), "slices_skipped": skipped}


def build_label_batches(data_root, run_id, n_batches=12):
    """Write the labeling batch files from the ingested candidates (the labeling swarm reads them)."""
    cf = Path(data_root) / "source_candidates" / f"{run_id}.jsonl"
    cands = [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()] if cf.exists() else []
    items = prelabel.labeling_input(cands)
    dom_counts = Counter(consolidate.registrable_domain(c.get("canonical_url") or c.get("source_url") or "")
                         for c in cands)
    dom_by_id = {c.get("candidate_id"): consolidate.registrable_domain(c.get("canonical_url") or c.get("source_url") or "")
                 for c in cands}
    for it in items:
        dom = dom_by_id.get(it["candidate_id"], "")
        it["domain"] = dom
        it["siblings_on_domain"] = max(0, dom_counts.get(dom, 1) - 1)
    bdir = Path(data_root) / "run_logs" / run_id / "agent_inputs" / "label_batches"
    bdir.mkdir(parents=True, exist_ok=True)
    for old in bdir.glob("batch_*.json"):
        old.unlink()
    size = max(1, math.ceil(len(items) / n_batches)) if items else 1
    paths = []
    for i in range(0, len(items), size):
        p = bdir / f"batch_{i // size:02d}.json"
        p.write_text(json.dumps(items[i:i + size], ensure_ascii=False), encoding="utf-8")
        paths.append(str(p).replace("\\", "/"))
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge discovery slices, ingest, and prep the labeling batches.")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--config", default=str(_ROOT / "configs/discovery_runs/gr_a2_tenders_procurement.yaml"))
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--schemas", default=str(_ROOT / "schemas"))
    ap.add_argument("--promotion-db", default=str(_ROOT / "data/promotion.db"))
    ap.add_argument("--slice-dir", default=None, help="default: data/run_logs/<run>/agent_inputs/scout_slices")
    args = ap.parse_args(argv)

    ai = Path(args.data_root) / "run_logs" / args.run_id / "agent_inputs"
    ai.mkdir(parents=True, exist_ok=True)
    slice_dir = args.slice_dir or str(ai / "scout_slices")

    merged, msum = merge_slices(slice_dir)
    scout_output = ai / "scout_output.json"
    scout_output.write_text(json.dumps(merged, ensure_ascii=False), encoding="utf-8")

    # strict ingest via the existing orchestrator (normalize -> runner: validate/verify/dedup/count + deliverable)
    run_pipeline.main(["--run-id", args.run_id, "--compact", str(scout_output), "--config", args.config,
                       "--verify", "--data-root", args.data_root, "--schemas", args.schemas,
                       "--promotion-db", args.promotion_db])

    cands = [json.loads(l) for l in (Path(args.data_root) / "source_candidates" / f"{args.run_id}.jsonl")
             .read_text(encoding="utf-8").splitlines() if l.strip()]
    failed = [{"candidate_id": c["candidate_id"], "source_url": c.get("source_url")}
              for c in cands if (c.get("url_verification") or {}).get("status") == "failed"]
    (ai / "failed_urls.json").write_text(json.dumps(failed, ensure_ascii=False), encoding="utf-8")

    # --- MANDATORY deterministic URL recovery -- the CODE rungs of the ladder (never depend on an agent for
    # what code can do). The runner's URL check is HEAD-only, so 403 (bot-defended but LIVE), 405 (HEAD
    # refused), 429 (we were impolite) and transient timeouts all land as "failed" -- and a failed URL means
    # the safety gate refuses to ACTIVATE the source and the pre-labeller defers it. The browser ladder used
    # to be the ONLY rung, and it is an AGENT step: when Chrome was unavailable it silently did nothing, and
    # 35 of 37 rounds shipped with every false-dead intact (~1,381 durable sources locked out). So BOTH cheap
    # rungs are code and run unconditionally, here:
    #   rung 1  plain browser-UA GET               (recheck_failed_urls)
    #   rung 2  WAF handshake: warm cookies on root, retry deep url with full browser headers (recheck_tier2)
    # They only ever emit verified/repaired; whatever neither settles is left in remaining_failures.json for
    # the AGENT browser rung (full_round_workflow.js), and after that the human "check by hand" list.
    if failed:
        for tier, mod, name in ((1, recheck, "GET re-check"), (2, recheck2, "WAF-handshake re-check")):
            try:
                mod.main(["--data-root", args.data_root, "--run-id", args.run_id])
            except Exception as e:  # noqa: BLE001 - a recovery tier must never abort the round
                print(f"[round_ingest] !! WARNING - code rung {tier} ({name}) failed ({e})")
        # fold the accumulated verdicts into the run ONCE, BEFORE labeling, so the pre-labeller judges the
        # candidates on their TRUE liveness rather than deferring live sources it thinks are dead.
        rr_path = ai / "recovery_results.json"
        if rr_path.exists() and json.loads(rr_path.read_text(encoding="utf-8")):
            run_pipeline.main(["--run-id", args.run_id, "--config", args.config,
                               "--data-root", args.data_root, "--schemas", args.schemas,
                               "--promotion-db", args.promotion_db,
                               "--recovery-results", str(rr_path)])
            cands = [json.loads(l) for l in (Path(args.data_root) / "source_candidates" /
                                             f"{args.run_id}.jsonl").read_text(encoding="utf-8").splitlines()
                     if l.strip()]

    still_failed = sum(1 for c in cands if (c.get("url_verification") or {}).get("status") == "failed")
    batches = build_label_batches(args.data_root, args.run_id)

    print(json.dumps({"run_id": args.run_id, "merged": msum, "ingested": len(cands),
                      "failed_urls": len(failed), "failed_after_code_recovery": still_failed,
                      "needs_browser_rung": still_failed > 0, "label_batches": len(batches),
                      "scout_output": str(scout_output)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
