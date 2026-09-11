#!/usr/bin/env python3
"""Plan/track the ALL-PAGES vision deep-read.

Every page of each report must be vision-read. Pages are processed in fixed CHUNK-page
windows; each window's extraction is written to its own file (a checkpoint). This script
reports which windows are still missing — so the deep-read is fully resumable: re-running
only does the windows whose checkpoint file is absent, and coverage can be proven page-by-page.

    python dr_plan.py                          # human summary: done/total chunks per report
    python dr_plan.py --print-missing [--limit N]   # JSON of the next N missing windows
"""
import argparse
import json
import os
import fitz  # PyMuPDF

# ROOT resolves from this script's own location (…/knowledge-base/scripts/dr_plan.py → repo root),
# so it is correct on Windows and macOS with no edit; override with the BANKING_ROOT env var if needed.
ROOT = os.environ.get("BANKING_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROC = os.path.join(ROOT, "knowledge-base", "processed")
OUTBASE = os.path.join(ROOT, "knowledge-base", "_deepread")
CHUNK = 10

DOCS = [
    {"slug": "rbr-cee-atm-2028",
     "file": "RBR Reports - Central and Eastern Europe ATM Market and Forecasts to 2028 (NCR Atleos)[34] (1).pdf"},
    {"slug": "rbr-we-atm-2028",
     "file": "RBR Reports - Western Europe ATM Market and Forecasts to 2028 (NCR Atleos) (1).pdf"},
]


def page_count(path):
    d = fitz.open(path)
    if d.needs_pass:
        d.authenticate("")
    n = d.page_count
    d.close()
    return n


def chunk_file(slug, s, e):
    return os.path.join(OUTBASE, slug, "p%04d-%04d.md" % (s, e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print-missing", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    missing, summary = [], []
    for d in DOCS:
        path = os.path.join(PROC, d["file"])
        n = page_count(path)
        os.makedirs(os.path.join(OUTBASE, d["slug"]), exist_ok=True)
        chunks = [(s, min(s + CHUNK - 1, n)) for s in range(1, n + 1, CHUNK)]
        done = 0
        for (s, e) in chunks:
            f = chunk_file(d["slug"], s, e)
            if os.path.isfile(f) and os.path.getsize(f) > 0:
                done += 1
            else:
                missing.append({"slug": d["slug"], "path": path, "pages": "%d-%d" % (s, e), "out": f})
        summary.append({"slug": d["slug"], "pages": n, "chunks": len(chunks),
                        "done": done, "missing": len(chunks) - done})

    if args.print_missing:
        out = missing[:args.limit] if args.limit else missing
        print(json.dumps({"missing": out, "summary": summary, "total_missing": len(missing)}, ensure_ascii=False))
    else:
        for s in summary:
            print("%-18s %d/%d chunks done (%d pages), %d missing" %
                  (s["slug"], s["done"], s["chunks"], s["pages"], s["missing"]))
        print("TOTAL missing chunks:", len(missing))


if __name__ == "__main__":
    main()
