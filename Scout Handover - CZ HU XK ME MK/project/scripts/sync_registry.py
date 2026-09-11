#!/usr/bin/env python3
"""Auto-sync the review Excel INTO the registry — the human never runs a script.

For a run's review sheet, apply the EFFECTIVE decisions to the registry: the human's decision where they
edited a cell, else the LLM's default. So the master list stays current whether or not a human reviewed. The
scheduled harness calls this at the START of each cycle, so whoever runs next (scouter or data-collector)
always sees the human's latest edits. Safety gates still apply (a source only goes ACTIVE if public + legally
allowed + verified; risky ones stay paused / needs-access).

Example:
    python scripts/sync_registry.py --db data/promotion.db --run-id dr_gr_a2_live_002 \
        --review deliverables/dr_gr_a2_live_002/REVIEW_dr_gr_a2_live_002.xlsx
"""
import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "review"))
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))

from promotion import apply as promo_apply, db, validation  # noqa: E402
import crossrun  # noqa: E402
import excel  # noqa: E402
import master_export  # noqa: E402
import unreachable  # noqa: E402
import runner  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Apply a review sheet's effective decisions to the registry.")
    ap.add_argument("--db", required=True, help="path to the promotion (registry) SQLite database")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--review", required=True, help="the run's review .xlsx (may be human-edited)")
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--schemas", default=str(_ROOT / "schemas"))
    ap.add_argument("--config", default=str(_ROOT / "configs/discovery_runs/gr_a2_tenders_procurement.yaml"),
                    help="run config (names the deliverable that gets refreshed)")
    ap.add_argument("--out-dir", default=str(_ROOT / "deliverables"),
                    help="where the single master-list deliverable is (re)written")
    ap.add_argument("--default-owner", default="auto:pipeline",
                    help="owner attributed to LLM-default approvals (the accountable pipeline)")
    args = ap.parse_args(argv)

    candidates = crossrun.load_run_candidates(args.data_root, args.run_id)
    by_id = {c["candidate_id"]: c for c in candidates
             if isinstance(c, dict) and isinstance(c.get("candidate_id"), str)}
    imp = excel.import_effective_decisions(args.review, default_owner=args.default_owner)

    conn = db.connect(args.db)
    db.init_schema(conn)
    validators = validation.load_validators(args.schemas)
    out = promo_apply.apply_decisions(conn, validators, imp["decisions"], by_id)

    # refresh the ONE human deliverable so a human's edits (or the LLM defaults) show up immediately
    cfg = runner.load_config(args.config)
    deliverable, dcounts = master_export.export_from_project(args.data_root, args.db, args.out_dir, cfg)

    # ...and refresh the "check by hand" list: durable sources the recovery ladder could not reach, for the
    # human to resolve. One per country, regenerated every sync so it always reflects the current state.
    country = cfg.get("country_name") or cfg.get("country") or ""
    unreachable_path = n_unreachable = None
    if country:
        import re
        uname = re.sub(r'[<>:"/\\|?*]', "-", f"{country} - Sources to check by hand.xlsx")
        unreachable_path = str(Path(args.out_dir) / uname)
        n_unreachable = unreachable.export_unreachable_workbook(
            args.data_root, unreachable_path, registry_db=args.db, country_name=country)

    human = sum(1 for d in imp["decisions"] if d.get("decided_by") == "human")
    print(json.dumps({"run_id": args.run_id, "review": args.review,
                      "decisions": len(imp["decisions"]), "from_human": human,
                      "from_llm_default": len(imp["decisions"]) - human,
                      "import_errors": len(imp["errors"]), "summary": out["summary"],
                      "deliverable": deliverable, "deliverable_counts": dcounts,
                      "check_by_hand": unreachable_path, "check_by_hand_count": n_unreachable},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
