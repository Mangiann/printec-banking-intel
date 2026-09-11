#!/usr/bin/env python3
"""Single-command source pipeline: scout output -> deliverables, chaining EVERY stage.

Deterministic stages run inline. The LLM/agent stages (discovery, URL-recovery, role-labeling) are consumed
as INPUT ARTIFACTS the automation harness supplies (--compact / --recovery-results / --roles); when an
artifact is absent, a deterministic fallback runs, so the pipeline ALWAYS completes end-to-end.

  1. ingest      : normalize a compact scout output + run it through the runner (validate/verify/dedupe/manifest).
                   Omit --compact to post-process an EXISTING run's candidates.
  2. recover     : apply browser-agent URL-recovery results (--recovery-results) if given, else skip.
  3. group       : consolidate.group_candidates (entity grouping).
  4. role        : role verdicts from --roles (LLM/panel) else prelabel.source_role (deterministic fallback).
  5. route       : route.route -> durable list + evidence/pointer/marginal ledgers.
  6. deliverables: FINAL_durable_sources.xlsx + REVIEW_grouped.xlsx + REVIEW.xlsx + the ledgers.
  7. promote     : (optional, HUMAN-GATED) if --apply <reviewed sheet .xlsx | decisions .jsonl> is given,
                   import the human's decisions and promote them into --promotion-db. WITHOUT --apply the
                   pipeline stops at deliverables — the registry is never updated from unreviewed sources.

Full loop:  run_pipeline (stages 1-6) -> a HUMAN reviews REVIEW_<run>.xlsx -> run_pipeline --apply <that sheet> (stage 7).

Examples:
    # full run from a saved scout output, over the network:
    python scripts/run_pipeline.py --run-id dr_x --compact scout.json --config configs/discovery_runs/gr_a2_tenders_procurement.yaml --verify
    # post-process an existing run with agent artifacts:
    python scripts/run_pipeline.py --run-id dr_gr_a2_live_002 --recovery-results recov.json --roles roles.json --promotion-db data/promotion.db
"""
import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))                                   # for `from promotion import ...`
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))
sys.path.insert(0, str(_ROOT / "review"))

import runner  # noqa: E402
import crossrun  # noqa: E402
import consolidate  # noqa: E402
import prelabel  # noqa: E402
import route  # noqa: E402
import recovery  # noqa: E402
import excel  # noqa: E402


def _log(msg):
    print(f"[pipeline] {msg}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run the whole source pipeline as one command.")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--schemas", default=str(_ROOT / "schemas"))
    ap.add_argument("--compact", default=None, help="compact scout output JSON (stage 1 ingest)")
    ap.add_argument("--config", default=str(_ROOT / "configs/discovery_runs/gr_a2_tenders_procurement.yaml"))
    ap.add_argument("--verify", action="store_true", help="verify URLs over the network during ingest")
    ap.add_argument("--recovery-results", default=None, help="browser-agent URL-recovery results JSON (stage 2)")
    ap.add_argument("--roles", default=None, help="LLM/panel role verdicts JSON [{candidate_id, verdict}] (stage 4)")
    ap.add_argument("--suggestions", default=None, help="LLM decision pre-labels JSON for the review sheet (stage 6)")
    ap.add_argument("--promotion-db", default=None, help="registry DB for the review delta")
    ap.add_argument("--apply", default=None,
                    help="a HUMAN-reviewed sheet (.xlsx) or decisions .jsonl -> promote into --promotion-db (stage 7)")
    ap.add_argument("--out-dir", default=str(_ROOT / "deliverables"),
                    help="where the human-facing outputs go (default: <project>/deliverables)")
    args = ap.parse_args(argv)
    now = runner._now_iso()
    config = runner.load_config(args.config)   # scope drives the deliverable's name + stage 1 ingest

    # --- stage 1: ingest (or post-process an existing run) ---
    if args.compact:
        import normalize
        compact = json.loads(Path(args.compact).read_text(encoding="utf-8"))
        if isinstance(compact, dict) and "candidates" in (compact.get("result") or {}):
            compact = compact["result"]
        if args.verify:
            config["url_verification"] = {"enabled": True}
        scout_output = normalize.normalize_scout_output(compact, config, now=now)
        verifier = runner.HttpUrlVerifier(timeout=8) if args.verify else None
        res = runner.execute_run(config, scout_output, run_id=args.run_id, now=now, data_root=args.data_root,
                                 schemas_dir=args.schemas, verifier=verifier)
        ss = res["manifest"]["search_summary"]
        _log(f"1 ingest: {res['written']['source_candidates']} candidates written, "
             f"{ss['urls_verified']} verified / {ss['urls_failed']} failed")
    else:
        _log(f"1 ingest: skipped (post-processing existing run {args.run_id})")

    cands = crossrun.load_run_candidates(args.data_root, args.run_id)

    # --- stage 2: URL-recovery (deterministic GET re-check + browser-agent artifact) ---
    # The crude HEAD verifier over-reports "dead" by ~5x (403=bot-defended-but-live, 405=HEAD-refused,
    # 429=we were impolite, timeout=slow). A source whose URL reads "failed" is refused ACTIVATION by the
    # safety gate and deferred by the pre-labeller -- so skipping recovery SILENTLY LOCKS LIVE SOURCES OUT.
    # It must therefore never be a quiet no-op: if this run has failed URLs and no recovery artifact, say so
    # loudly and count them, so a round can never look clean while it is throwing away live sources.
    _failed_now = sum(1 for c in cands
                      if (c.get("url_verification") or {}).get("status") == "failed")
    if args.recovery_results:
        rr = json.loads(Path(args.recovery_results).read_text(encoding="utf-8"))
        cands, rsum = recovery.apply_url_recovery(cands, rr, now=now)
        jpath = Path(args.data_root) / "source_candidates" / f"{args.run_id}.jsonl"
        jpath.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cands), encoding="utf-8")
        left = sum(1 for c in cands if (c.get("url_verification") or {}).get("status") == "failed")
        _log(f"2 recover: {rsum['verified']} verified, {rsum['repaired']} repaired, {rsum['dead']} dead "
             f"(healed run written; {left} still failed)")
        if left:
            _log(f"2 recover: !! WARNING - {left} URL(s) still 'failed' -> those sources CANNOT activate. "
                 f"Run the browser ladder over data/run_logs/{args.run_id}/agent_inputs/remaining_failures.json")
    elif _failed_now:
        _log(f"2 recover: !! WARNING - NO recovery artifact, but {_failed_now} URL(s) are marked 'failed' by "
             f"the crude HEAD check. Those sources will be PAUSED/DEFERRED and never collected, and most of "
             f"them are probably LIVE (403/405/429/timeout). Run: python scripts/recheck_failed_urls.py "
             f"--only <ISO>   then re-run with --recovery-results.")
    else:
        _log("2 recover: skipped (no failed URLs in this run - nothing to recover)")

    # --- stage 3: group ---
    groups = consolidate.group_candidates(cands)
    _log(f"3 group: {len(cands)} candidates -> {len(groups)} entities")

    # --- stage 4: role (STANDING method = the LLM labeling pass, via --roles; heuristic is emergency fallback) ---
    valid_ids = {c["candidate_id"] for c in cands
                 if isinstance(c, dict) and isinstance(c.get("candidate_id"), str)}
    if args.roles:
        raw = json.loads(Path(args.roles).read_text(encoding="utf-8"))
        role_by_id = prelabel.normalize_roles(raw, valid_ids)
        _log(f"4 role: {len(role_by_id)} validated LLM verdicts from {Path(args.roles).name}")
    else:
        role_by_id = {cid: prelabel.source_role(next(c for c in cands if c.get("candidate_id") == cid))
                      for cid in valid_ids}
        _log("4 role: !! WARNING - deterministic ~57% fallback. Pass --roles from the LLM labeling pass "
             "for production-quality roles.")

    # --- stage 5: route ---
    routed = route.route(cands, role_by_id, groups)
    _log(f"5 route: {routed['summary']}")

    # --- stage 6: per-run artifacts (MACHINE zone under data/, NOT a human deliverable) ---
    # These feed the promotion step and downstream layers. The ONE human deliverable is the master-list
    # Excel written in stage 8; deliverables/ never gets a per-run subfolder.
    machine = Path(args.data_root) / "run_logs" / args.run_id / "artifacts"
    machine.mkdir(parents=True, exist_ok=True)
    route.write_ledgers(routed, str(machine))
    route.write_durable_workbook(routed, cands, str(machine / f"durable_sources_{args.run_id}.xlsx"))
    consolidate.write_grouped_workbook(cands, groups, str(machine / f"grouped_{args.run_id}.xlsx"),
                                       role_by_id=role_by_id)
    # the promote-review sheet holds only the durable KEEP CHANNELS (each a monitoring source). Evidence/
    # pointers/marginal are in their ledgers; folded endpoints stay tucked under their entity (NOT separate
    # registry sources) - so the registry never re-fragments into many rows per entity.
    durable_ids = {cid for dd in routed["durable"] for cid in dd["channel_ids"]}
    new, _summary = excel.new_candidates(args.data_root, args.run_id, registry_db=args.promotion_db,
                                         only_ids=durable_ids)
    if args.suggestions:                                   # STANDING method = LLM decision labels
        raw = json.loads(Path(args.suggestions).read_text(encoding="utf-8"))
        sug = prelabel.normalize_suggestions(raw, {c.get("candidate_id") for c in new})
        _log(f"6 review sheet: {len(new)} durable new sources, {len(sug)} LLM decision labels")
    else:
        sug = prelabel.heuristic_suggestions(new)
        _log(f"6 review sheet: {len(new)} durable new sources; !! WARNING heuristic decision fallback")
    review_path = machine / f"REVIEW_{args.run_id}.xlsx"   # the promotion step's input, not a deliverable
    excel.export_review_workbook(args.data_root, args.run_id, str(review_path),
                                 registry_db=args.promotion_db, suggestions=sug, only_ids=durable_ids)
    _log(f"6 machine artifacts + review sheet -> {machine}")

    # --- stage 7 (optional, HUMAN-GATED): promote a reviewed sheet's decisions into the registry ---
    promote_summary = None
    if args.apply:
        if not args.promotion_db:
            _log("7 promote: skipped (--apply needs --promotion-db)")
        else:
            from promotion import apply as promo_apply, db as promo_db, validation as promo_val
            if str(args.apply).lower().endswith(".xlsx"):
                imp = excel.import_effective_decisions(args.apply)   # human edit if present, else LLM default
                decisions = imp["decisions"]
                if imp["errors"]:
                    _log(f"7 promote: {len(imp['errors'])} import warning(s)")
            else:
                decisions = [json.loads(ln) for ln in Path(args.apply).read_text(encoding="utf-8").splitlines()
                             if ln.strip()]
            conn = promo_db.connect(args.promotion_db); promo_db.init_schema(conn)
            validators = promo_val.load_validators(args.schemas)
            by_id = {c["candidate_id"]: c for c in cands
                     if isinstance(c, dict) and isinstance(c.get("candidate_id"), str)}
            promote_summary = promo_apply.apply_decisions(conn, validators, decisions, by_id)["summary"]
            _log(f"7 promote: {promote_summary}")
    else:
        _log("7 promote: skipped (no --apply; the registry is updated ONLY from a human-reviewed sheet)")

    # --- stage 8: THE human deliverable — the whole source list as ONE Excel in deliverables/ ---
    # A single, plainly-named file listing EVERY source with the run that added it. Regenerated each run so it
    # always reflects the current master list. deliverables/ holds this one file — no per-run folders.
    deliverable_path = None
    if args.promotion_db:
        import master_export
        deliverable_path, mcounts = master_export.export_from_project(
            args.data_root, args.promotion_db, args.out_dir, config)
        _log(f"8 master list (the ONE human file) -> {deliverable_path} "
             f"({mcounts['sources']} sources, {mcounts['pending']} pending)")
    else:
        _log("8 master list: skipped (needs --promotion-db)")

    print(json.dumps({"run_id": args.run_id, "entities": len(groups), "route": routed["summary"],
                      "promote": promote_summary, "deliverable": deliverable_path}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
