#!/usr/bin/env python3
"""Fold a human-completed 'Sources to check by hand' workbook back into the system.

The last rung of URL recovery is a person: they open the links the automatic ladder could not reach and tell
us what they found. This applies their answers exactly like any other recovery rung — deterministically, and
through the SAME machinery (recovery.apply_url_recovery for liveness, the decision-suggestion file for the
keep/hold call, then the normal re-file + activation), so a by-hand fix lands in the registry identically to
an automatic one.

    works        -> the link is fine: mark it verified, and approve the source
    moved        -> repaired to working_url: adopt it, verified, approve
    dead         -> genuinely gone: record it dead, reject the source
    needs_login  -> real but gated: set access=requires_credentials, hold as needs_access (manual upload later)
    not_relevant -> not a source we want: reject

Safety is unchanged: a repaired/verified source still only ACTIVATES if it is public + legally allowed
(activate_recovered_sources re-derives G9); a needs_login source stays paused by construction.

    python scripts/apply_manual_url_checks.py --file "deliverables/Greece - Sources to check by hand.xlsx"
    python scripts/apply_manual_url_checks.py --file <xlsx> --dry-run
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "review"))
sys.path.insert(0, str(_ROOT / "scripts"))
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))

import unreachable  # noqa: E402
import recovery  # noqa: E402
import runner  # noqa: E402
import backfill_candidate_ids as backfill  # noqa: E402
import activate_recovered_sources as activate  # noqa: E402

# status -> (recovery outcome or None, decision or None, access_status override or None)
_MAP = {
    "works":        ("verified", "approve", None),
    "moved":        ("repaired", "approve", None),
    "dead":         ("dead",     "reject", None),
    "needs_login":  (None,       "needs_access", "requires_credentials"),
    "not_relevant": (None,       "reject", None),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Apply a completed 'check by hand' workbook.")
    ap.add_argument("--file", required=True, help="the human-completed 'Sources to check by hand' .xlsx")
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--schemas", default=str(_ROOT / "schemas"))
    ap.add_argument("--out-dir", default=str(_ROOT / "deliverables"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    now = runner._now_iso()

    imp = unreachable.import_unreachable_checks(args.file)
    if imp["errors"]:
        print("[apply] input warnings:")
        for e in imp["errors"]:
            print(f"[apply]   - {e}")
    checks = imp["checks"]
    if not checks:
        print(json.dumps({"applied": 0, "note": "no filled rows found", "errors": imp["errors"]}, indent=2))
        return 0

    # group by run so each run's candidate file + label file is touched once
    by_run = defaultdict(list)
    for c in checks:
        run = c.get("run_id") or _run_of(args.data_root, c["candidate_id"])
        if run:
            by_run[run].append(c)
        else:
            imp["errors"].append(f"{c['candidate_id']}: could not find its run")

    from collections import Counter
    tally = Counter()
    countries = set()
    for run, rows in by_run.items():
        countries.add(run.split("_")[1].upper())
        cf = Path(args.data_root) / "source_candidates" / f"{run}.jsonl"
        if not cf.exists():
            continue
        cands = [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()]
        by_id = {c.get("candidate_id"): c for c in cands}

        rec_entries, sugg_updates = [], {}
        for row in rows:
            cid, status = row["candidate_id"], row["status"]
            outcome, decision, access = _MAP[status]
            tally[status] += 1
            if outcome == "verified":
                rec_entries.append({"candidate_id": cid, "outcome": "verified", "ladder_step": "human",
                                    "evidence": row.get("notes") or "confirmed by hand"})
            elif outcome == "repaired":
                rec_entries.append({"candidate_id": cid, "outcome": "repaired",
                                    "corrected_url": row["working_url"], "ladder_step": "human",
                                    "evidence": row.get("notes") or "corrected by hand"})
            elif outcome == "dead":
                rec_entries.append({"candidate_id": cid, "outcome": "dead", "grade_of_dead": "moved_unknown",
                                    "ladder_step": "human", "evidence": row.get("notes") or "confirmed gone by hand"})
            if access and cid in by_id:            # needs_login: tighten access on the candidate
                by_id[cid]["access_status"] = access
                by_id[cid]["updated_at"] = now
            if decision:
                sugg_updates[cid] = decision

        if args.dry_run:
            continue

        # 1. liveness verdicts through the SAME deterministic writer as every other rung
        if rec_entries:
            healed, _ = recovery.apply_url_recovery(cands, rec_entries, now=now)
            hb = {c.get("candidate_id"): c for c in healed}
            for cid, c in by_id.items():           # carry the needs_login access edit onto the healed set
                if cid in hb and c.get("access_status") != hb[cid].get("access_status"):
                    hb[cid]["access_status"] = c["access_status"]
            cands = healed
        cf.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cands), encoding="utf-8")

        # 2. the keep/hold decision, merged into the run's suggestion file (re-file reads it)
        _merge_decisions(Path(args.data_root) / "run_logs" / run / "agent_inputs" / "decision_suggestions.json",
                         sugg_updates)

    print(f"[apply] by-hand verdicts: {dict(tally)}")
    if args.dry_run:
        print(json.dumps({"dry_run": True, "would_apply": len(checks), "by_status": dict(tally)}, indent=2))
        return 0

    # 3. re-file + activate each affected country through the normal machinery
    for iso in sorted(countries):
        print(f"[apply] re-filing {iso} ...")
        backfill.main(["--refile", "--only", iso, "--data-root", args.data_root, "--out-dir", args.out_dir])
        activate.main(["--data-root", args.data_root, "--schemas", args.schemas,
                       "--db", str(Path(args.data_root) / "registries" / f"{iso}.db")])

    print(json.dumps({"applied": len(checks), "by_status": dict(tally),
                      "countries": sorted(countries), "errors": imp["errors"]},
                     indent=2, ensure_ascii=False))
    return 0


def _run_of(data_root, candidate_id):
    """Fallback: find which run a candidate_id belongs to (its id is namespaced <run>__<id>)."""
    if isinstance(candidate_id, str) and "__" in candidate_id:
        run = candidate_id.split("__", 1)[0]
        if (Path(data_root) / "source_candidates" / f"{run}.jsonl").exists():
            return run
    return None


def _merge_decisions(path, updates):
    if not updates:
        return
    cur = []
    if path.exists():
        try:
            cur = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            cur = []
    by_id = {c.get("candidate_id"): c for c in cur if isinstance(c, dict)}
    for cid, decision in updates.items():
        row = by_id.get(cid, {"candidate_id": cid})
        row["suggested_decision"] = decision
        by_id[cid] = row
    path.write_text(json.dumps(list(by_id.values()), ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
