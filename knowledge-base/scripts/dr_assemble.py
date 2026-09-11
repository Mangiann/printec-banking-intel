#!/usr/bin/env python3
"""Assemble the per-window deep-read checkpoints into one consolidated digest per report.

The all-pages deep-read writes one checkpoint per 10-page window
(`knowledge-base/_deepread/<slug>/pSSSS-EEEE.md`). This concatenates them in page order into a single
`<slug>-deep.md` placed in the agent folders that the report serves, so an agent (or a human) can read or
grep the entire vision extraction in one file. The granular window files stay as the source of truth.

Run after `dr_plan.py` shows 0 missing (full coverage). Idempotent — safe to re-run.
"""
import glob
import os
import re

# ROOT resolves from this script's own location (…/knowledge-base/scripts/dr_assemble.py → repo root),
# so it is correct on Windows and macOS with no edit; override with the BANKING_ROOT env var if needed.
ROOT = os.environ.get("BANKING_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEEP = os.path.join(ROOT, "knowledge-base", "_deepread")
BYAGENT = os.path.join(ROOT, "knowledge-base", "by-agent")

DOCS = [
    {"slug": "rbr-cee-atm-2028", "title": "RBR Central & Eastern Europe — ATM Market & Forecasts to 2028",
     "orig": "RBR Reports - Central and Eastern Europe ATM Market and Forecasts to 2028 (NCR Atleos)[34] (1).pdf",
     "folders": ["agent-4-statistics", "agent-8-futurist"]},
    {"slug": "rbr-we-atm-2028", "title": "RBR Western Europe — ATM Market & Forecasts to 2028",
     "orig": "RBR Reports - Western Europe ATM Market and Forecasts to 2028 (NCR Atleos) (1).pdf",
     "folders": ["agent-8-futurist", "agent-4-statistics"]},
]


def win_start(path):
    m = re.search(r"p(\d+)-\d+\.md$", path)
    return int(m.group(1)) if m else 0


def main():
    for d in DOCS:
        files = sorted(glob.glob(os.path.join(DEEP, d["slug"], "p*.md")), key=win_start)
        if not files:
            print("skip (no windows):", d["slug"]); continue
        last_page = 0
        m = re.search(r"-(\d+)\.md$", files[-1])
        if m:
            last_page = int(m.group(1))
        parts = []
        for f in files:
            parts.append(open(f, encoding="utf-8").read().strip())
        header = (
            "# %s — full deep-read (vision, page-by-page)\n\n"
            "_Vision extraction of all ~%d pages across %d ten-page windows — body text, tables AND charts. "
            "Source: the licensed RBR report (INTERNAL USE ONLY — do not redistribute externally). "
            "Original: `knowledge-base/processed/%s`. Granular per-window files: `knowledge-base/_deepread/%s/`._\n\n"
            "---\n\n" % (d["title"], last_page, len(files), d["orig"], d["slug"])
        )
        body = header + "\n\n---\n\n".join(parts) + "\n"
        for folder in d["folders"]:
            out = os.path.join(BYAGENT, folder, d["slug"] + "-deep.md")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(body)
        print("assembled %-18s %d windows -> %d chars -> %s" %
              (d["slug"], len(files), len(body), ", ".join(d["folders"])))


if __name__ == "__main__":
    main()
