#!/usr/bin/env python3
"""
prev_summary.py - deterministically build the `prevSummary` (delta/baseline context) for a
collector agent from its most-recent findings file, instead of having the agent hand-write
it each run. Because every collector agent now emits the SAME harness format, one parser
serves all six: it lifts the prose summary, the ranked opportunities, the open-tender
pipeline (so deadlines get re-statused), and a COMPACT one-line-per-row digest of the
signal table (entity | country | signal | size/win/confidence).

Usage: python prev_summary.py --dir <findings folder> [--max-rows 120] [--max-chars 9000]
Prints the baseline text to stdout (empty string if there is no prior file). The agent's
SKILL captures stdout and passes it straight to the harness as `prevSummary`.
"""
import argparse, os, re, sys, glob

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})\.md$")


def latest_file(d):
    cands = []
    for p in glob.glob(os.path.join(d, "*.md")):
        m = DATE_RE.search(os.path.basename(p))
        if m and not os.path.basename(p).startswith(("_", ".")):
            cands.append((m.group(1), p))
    if not cands:
        return None, None
    cands.sort()
    return cands[-1]  # (date, path)


def split_sections(text):
    """Return {header_lower: body} split on '## ' headings."""
    sections, cur, buf = {}, "_preamble", []
    for line in text.splitlines():
        if line.startswith("## "):
            sections[cur] = "\n".join(buf).strip()
            cur = line[3:].strip().lower()
            buf = []
        else:
            buf.append(line)
    sections[cur] = "\n".join(buf).strip()
    return sections


def table_rows(body):
    """Yield cell-lists for each markdown data row in a section (skips header/separator)."""
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or set("".join(cells)) <= set("-: "):  # separator row
            continue
        if cells and cells[0].lower() in ("buyer", "bank/entity", "workstream", "deadline", "entity"):
            continue  # header row
        yield cells


def strip_link(s):
    m = re.match(r"\[([^\]]+)\]\([^)]*\)", s)
    return m.group(1) if m else s


def main():
    # Findings files contain arbitrary Unicode (em-dashes, → ↔ arrows, Greek/Cyrillic).
    # On Windows, stdout defaults to cp1252 and sys.stdout.write() would crash on any
    # character outside that codepage — so force UTF-8 before writing the baseline.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--max-rows", type=int, default=120)
    ap.add_argument("--max-chars", type=int, default=14000)
    args = ap.parse_args()

    date, path = latest_file(args.dir)
    if not path:
        sys.stdout.write("")  # no prior file - first run
        return

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    sec = split_sections(text)
    out = [f"BASELINE from the previous findings file ({date}). Re-verify and STATUS each of "
           f"these against primary sources this run (still-open / awarded / cancelled / changed); "
           f"report what is NEW or CHANGED, and capture any newly-named award winner.\n"]

    # PREFIX-match the lowercased heading so suffixes don't break the lookup. Older
    # hand-written files used headings like "Signal table - NEW or CHANGED since ..."
    # and "Top opportunities (ranked)"; the harness emits the bare heading. Both resolve.
    def find_section(*prefixes):
        for k in sec:
            if any(k.startswith(p) for p in prefixes):
                return k
        return None

    wc = find_section("what changed")
    if wc and sec.get(wc):
        out.append("=== WHAT CHANGED SINCE LAST RUN ===\n" + sec[wc])

    # KNOWN-STALE / contradicted-last-run block (added 2026-06-25): lift the adversarial pass's
    # "Corrected/contradicted" line from the prior file so this run does NOT waste cycles
    # rediscovering items already proven out-of-window/wrong (e.g. an old framework re-published,
    # a 2020 deal mis-dated as new). Placed high so it survives the max-chars truncation; capped
    # so one huge verifier line can't crowd out the rest. Re-report these only if GENUINELY changed.
    vn = find_section("verification notes")
    if vn and sec.get(vn):
        for line in sec[vn].splitlines():
            s = line.strip()
            if s.startswith("-") and "contradict" in s.lower():
                if len(s) > 1400:
                    s = s[:1400].rsplit(";", 1)[0] + "; ...[more in prior file]"
                out.append("=== KNOWN-STALE / CONTRADICTED LAST RUN — DO NOT RE-REPORT AS NEW "
                            "(only if genuinely changed) ===\n" + s)
                break

    topp = find_section("top opportunities")
    if topp and sec.get(topp):
        out.append("=== TOP OPPORTUNITIES (RANKED) ===\n" + sec[topp])

    # open-tender pipeline (tenders agent) - keep verbatim so deadlines are re-statused
    for key in list(sec):
        if key.startswith("open-tender pipeline"):
            out.append("=== OPEN-TENDER PIPELINE (status each deadline) ===\n" + sec[key])
            break

    # access issues / operator requests - small, time-sensitive block; carried before
    # the larger calendar/digest so the operator to-dos always survive truncation.
    for key in list(sec):
        if key.startswith("access issues"):
            out.append("=== ACCESS ISSUES & OPERATOR REQUESTS (carried) ===\n" + sec[key])
            break

    # rolling regulatory calendar (regulation agent) - keep verbatim so EVERY dated
    # obligation is carried for re-statusing. For a deadline-tracking agent this is the
    # single highest-value baseline block, so it sits ahead of the truncatable digest.
    for key in list(sec):
        if key.startswith("rolling regulatory calendar"):
            out.append("=== ROLLING REGULATORY CALENDAR (status each deadline) ===\n" + sec[key])
            break

    # compact signal-table digest (last - truncatable). Prefix match so the older
    # hand-written heading ("Signal table - NEW or CHANGED ...") also resolves.
    sig_key = find_section("signal table")
    sig = sec.get(sig_key, "") if sig_key else ""
    rows = list(table_rows(sig))[: args.max_rows]
    if rows:
        lines = ["=== SIGNAL TABLE (compact: entity | country | signal | size/win/conf) ==="]
        for c in rows:
            entity = strip_link(c[0]) if len(c) > 0 else ""
            country = c[1] if len(c) > 1 else ""
            signal = (c[2][:160]) if len(c) > 2 else ""
            size = c[8] if len(c) > 8 else ""
            win = c[9] if len(c) > 9 else ""
            conf = c[7] if len(c) > 7 else ""
            lines.append(f"- {entity} ({country}): {signal} [{size}/{win}/{conf}]")
        out.append("\n".join(lines))

    blob = "\n\n".join(out).strip()
    if len(blob) > args.max_chars:
        blob = blob[: args.max_chars].rsplit("\n", 1)[0] + "\n...[truncated]"
    sys.stdout.write(blob)


if __name__ == "__main__":
    main()
