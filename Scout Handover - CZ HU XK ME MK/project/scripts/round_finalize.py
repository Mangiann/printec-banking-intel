#!/usr/bin/env python3
"""FINALIZE a round — one deterministic command the orchestrator calls after browser-repair + labeling.

  1. merge the labeling swarm's slices into role_verdicts.json + decision_suggestions.json (validated/clamped);
  2. run the full pipeline (fold in recovery + roles + suggestions) -> machine artifacts + the master deliverable;
  3. sync the run into the registry (safety-gated) and refresh the deliverable;
  4. print the convergence report (new / seen_prior / in_registry) + the deliverable path.

    python scripts/round_finalize.py --run-id dr_gr_a2_live_004 --config <cfg> --promotion-db data/promotion.db
"""
import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))
sys.path.insert(0, str(_ROOT / "review"))
sys.path.insert(0, str(_ROOT / "scripts"))

import prelabel  # noqa: E402
import crossrun  # noqa: E402
import run_pipeline  # noqa: E402
import sync_registry  # noqa: E402


def merge_label_slices(label_dir):
    """Merge the labeling swarm's slice files -> one list of {candidate_id, role, decision, priority, rationale}.
    Dedup by candidate_id (first wins). TOTAL: an unparseable slice is skipped."""
    out, seen = [], set()
    d = Path(label_dir)
    for f in sorted(d.glob("*.json")) if d.exists() else []:
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for r in rows if isinstance(rows, list) else []:
            if not isinstance(r, dict):
                continue
            cid = r.get("candidate_id")
            if isinstance(cid, str) and cid not in seen:
                seen.add(cid)
                out.append(r)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge labels, run the pipeline, sync, and report.")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--config", default=str(_ROOT / "configs/discovery_runs/gr_a2_tenders_procurement.yaml"))
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--schemas", default=str(_ROOT / "schemas"))
    ap.add_argument("--promotion-db", default=str(_ROOT / "data/promotion.db"))
    ap.add_argument("--out-dir", default=str(_ROOT / "deliverables"))
    ap.add_argument("--label-dir", default=None, help="default: data/run_logs/<run>/agent_inputs/label_slices")
    args = ap.parse_args(argv)

    ai = Path(args.data_root) / "run_logs" / args.run_id / "agent_inputs"
    label_dir = args.label_dir or str(ai / "label_slices")

    cands = [json.loads(l) for l in (Path(args.data_root) / "source_candidates" / f"{args.run_id}.jsonl")
             .read_text(encoding="utf-8").splitlines() if l.strip()]
    valid_ids = {c["candidate_id"] for c in cands if isinstance(c.get("candidate_id"), str)}

    labels = merge_label_slices(label_dir)
    roles = prelabel.normalize_roles([{"candidate_id": r.get("candidate_id"), "verdict": r.get("role")}
                                      for r in labels], valid_ids)
    sugg = prelabel.normalize_suggestions([{"candidate_id": r.get("candidate_id"),
                                            "suggested_decision": r.get("decision"),
                                            "suggested_priority": r.get("priority"),
                                            "rationale": r.get("rationale")} for r in labels], valid_ids)
    roles_path = ai / "role_verdicts.json"
    sugg_path = ai / "decision_suggestions.json"
    roles_path.write_text(json.dumps([{"candidate_id": k, "verdict": v} for k, v in roles.items()],
                                     ensure_ascii=False), encoding="utf-8")
    sugg_path.write_text(json.dumps([{"candidate_id": k, **v} for k, v in sugg.items()],
                                    ensure_ascii=False), encoding="utf-8")

    recovery = ai / "recovery_results.json"
    pipe = ["--run-id", args.run_id, "--config", args.config, "--data-root", args.data_root,
            "--schemas", args.schemas, "--roles", str(roles_path), "--suggestions", str(sugg_path),
            "--promotion-db", args.promotion_db, "--out-dir", args.out_dir]
    if recovery.exists():
        pipe += ["--recovery-results", str(recovery)]
    run_pipeline.main(pipe)

    review_sheet = Path(args.data_root) / "run_logs" / args.run_id / "artifacts" / f"REVIEW_{args.run_id}.xlsx"
    sync_registry.main(["--db", args.promotion_db, "--run-id", args.run_id, "--review", str(review_sheet),
                        "--config", args.config, "--data-root", args.data_root, "--schemas", args.schemas,
                        "--out-dir", args.out_dir])

    _cls, summ = crossrun.compute_review_delta(args.data_root, args.run_id, registry_db=args.promotion_db)
    print(json.dumps({"run_id": args.run_id, "labels_merged": len(labels), "roles": len(roles),
                      "suggestions": len(sugg), "convergence": summ}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
