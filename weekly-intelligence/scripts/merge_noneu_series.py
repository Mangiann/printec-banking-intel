#!/usr/bin/env python3
"""
merge_noneu_series.py - accumulate the researched non-EU structural series across runs.

WHY: the EU series (fetch_ecb.py) re-pulls the FULL multi-year history every run, so EU charts keep
their depth. The non-EU series is RESEARCHED by Agent 4's harness, which reports "what it found this
run" - which may be fewer historical points than a prior run. If each run simply OVERWROTE
structural_series_noneu.json, the charts would shrink whenever an agent re-found only the latest year.
So Agent 4 writes the harness output to structural_series_noneu.new.json and runs THIS script, which
MERGES it into the persistent structural_series_noneu.json: union of years per country+metric, so
history accumulates and a sparse run can only ADD or UPDATE points, never erase past ones.

Merge rule per (code, metric, year):
  - a NEW point updates the stored point for that year, EXCEPT a provisional new point does NOT
    overwrite a firm (non-provisional) stored point for the same year (don't let a later interim
    re-estimate clobber a confirmed year-end figure).
  - years present only in the old file are kept; years only in the new file are added.

Usage: python merge_noneu_series.py --data <intel-cache dir> [--new <path>] [--keep-new]
Defaults: --new = <data>/structural_series_noneu.new.json ; deletes it after a successful merge
unless --keep-new. First run (no existing file) just promotes the new file. No-op if neither exists.
"""
import argparse, json, os, sys

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def merge_points(old_pts, new_pts):
    by_year = {}
    for p in (old_pts or []):
        if isinstance(p.get("year"), int):
            by_year[p["year"]] = p
    for p in (new_pts or []):
        y = p.get("year")
        if not isinstance(y, int):
            continue
        prev = by_year.get(y)
        # a provisional new point must not overwrite a firm stored one for the same year
        if prev and p.get("provisional") and not prev.get("provisional"):
            continue
        by_year[y] = p
    return [by_year[y] for y in sorted(by_year)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--new")
    ap.add_argument("--keep-new", action="store_true")
    args = ap.parse_args()

    dest = os.path.join(args.data, "structural_series_noneu.json")
    new_path = args.new or os.path.join(args.data, "structural_series_noneu.new.json")

    new = load(new_path)
    if not new or not new.get("series"):
        print("merge_noneu_series: no new file (or empty) at", new_path, "- nothing to merge")
        return
    old = load(dest)

    if not old or not old.get("series"):
        # first run: promote the new file verbatim
        json.dump(new, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        added = sum(len(v) for m in new["series"].values() for v in m.values())
        print(f"merge_noneu_series: seeded {dest} ({len(new['series'])} countries, {added} points)")
    else:
        out = old
        out["series"] = old.get("series", {})
        added_pts = 0
        for cc, metrics in new["series"].items():
            dcm = out["series"].setdefault(cc, {})
            for mk, pts in metrics.items():
                before = {p["year"] for p in dcm.get(mk, []) if isinstance(p.get("year"), int)}
                merged = merge_points(dcm.get(mk), pts)
                dcm[mk] = merged
                added_pts += len([p for p in merged if p["year"] not in before])
        out["generated"] = new.get("generated", out.get("generated", ""))
        if new.get("source"):
            out["source"] = new["source"]
        json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        ncountries = len(out["series"])
        npoints = sum(len(v) for m in out["series"].values() for v in m.values())
        print(f"merge_noneu_series: merged into {dest} (+{added_pts} new-year points; "
              f"now {ncountries} countries, {npoints} points total)")

    if not args.keep_new:
        try:
            os.remove(new_path)
        except OSError:
            pass

if __name__ == "__main__":
    main()
