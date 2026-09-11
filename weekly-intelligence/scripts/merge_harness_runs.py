#!/usr/bin/env python3
"""Rebuild a collector agent's findings file from one or more research-harness runs.

WHY THIS EXISTS
---------------
research-harness.workflow.js guarantees a deterministic table -- but only for the units that
survive its own pipeline. Twice running (31/07/2026 and 01/08/2026) an Agent-2 run lost agents
to `Connection closed mid-response` / session limits and either published nothing at all or
reported units as EMPTY that had in fact ALREADY written their research checkpoint to
parts/<runDate>/<slug>.json and then died while RETURNING. The data was on disk; only the
assembly was lost. On 01/08/2026 that was 151 researched signals across 7 units.

The recovery pattern this script completes:
  1. back up parts/<runDate>/ BEFORE re-running anything (the next pass overwrites it)
  2. re-invoke the harness scoped to ONLY the failed units, each unit's `focus` naming its own
     backup checkpoint with a recover-verify-extend mandate (cheaper than re-researching, and
     it still gets the adversarial verify). Do NOT use resumeFromRunId -- failed agents are not
     cached, so they re-research from scratch anyway.
  3. merge the passes with THIS script.

It ports research-harness.workflow.js's renderTable / renderTenderPipeline / renderAccessOps /
coverage renderers exactly (verified byte-identical against a real run), so the table stays
machine-rendered and can never be silently truncated. It adds two things the harness does not
do, both of which the Agent-2 brief asks the PARENT to do:
  * DEDUP of the same notice found by two units -- on STRONG identity only (TED notice id,
    Prozorro UA id). Never on a shared URL: a portal search page, an XML/CSV API endpoint or a
    procurement-plan PDF is a ROUTE, not a tender. An early attempt keyed on URL silently
    deleted 24 real notices (distinct CNB / OeNB / NBRM / HNB-plan lines collapsed into one).
  * DEADLINE BANDING of the open-tender pipeline (<=30 days / later / already closed), because a
    flat ascending sort buries the urgent rows under already-closed ones.

The narrative (prose only -- never the table) is supplied via --narrative.

USAGE
  python3 merge_harness_runs.py \
      --journal <run1-transcript-dir>/journal.jsonl \
      --journal <run2-transcript-dir>/journal.jsonl \
      --units-json ../workflows/agent-units.json --agent-key 2 \
      --agent-label "Tenders & Procurement" --run-date 2026-08-01 --today 02/08/2026 \
      --extra slovenia-enarocanje=v1.json,v2.json,v3.json \
      --narrative narrative.md --out .../findings/02-tenders/2026-08-01.md

Later --journal files win over earlier ones for the same unit, so pass the recovery run LAST.
--extra wins over every journal: use it for a unit verified outside the harness in batches,
which is the fix when a unit is too rich to re-emit under the 32k output-token cap (a unit
returning >20 signals will hit it -- verify ~10 at a time).
"""
import json, argparse, os, re

UNITS = []              # [(slug, display name)] -- filled from --units-json
UNIT_NOUN = "entity"
RUN_DATE = "UNDATED"
AGENT_NO = ""
AGENT_LABEL = ""


def load_journal(path):
    """-> (verified_by_slug, research_by_slug). Later lines win (gap-fill overrides)."""
    ver, res = {}, {}
    if not os.path.exists(path):
        return ver, res
    for line in open(path, encoding="utf-8"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") != "result":
            continue
        r = d.get("result")
        if not isinstance(r, dict) or not r.get("slug"):
            continue
        slug = r["slug"]
        if isinstance(r.get("verified_signals"), list):
            keep = [s for s in r["verified_signals"] if s.get("keep") is not False]
            if keep:
                ver[slug] = keep
        elif isinstance(r.get("signals"), list):
            res[slug] = r
    return ver, res


# ---- ports of the harness's JS renderers (must stay byte-compatible) --------
def cell(s):
    if s is None:
        return ""
    return re.sub(r"\r?\n+", " ", str(s)).replace("|", "\\|").strip()


SIZE_RANK = {"XL": 0, "L": 1, "M": 2, "S": 3, "Unscoped": 4}
WIN_RANK = {"High": 0, "Medium": 1, "Low": 2, "—": 3}


def value_rank(s):
    return SIZE_RANK.get(s.get("opp_size"), 9) * 10 + WIN_RANK.get(s.get("win"), 9)


def source_link(s):
    name = cell(s.get("source_name")) or "source"
    url = cell(s.get("source_url"))
    return "[%s](%s)" % (name, url) if url else name


def render_table(signals):
    head = ("| Buyer | Country | Signal | Source (link) | Date | What it implies | "
            "6-12 mo likelihood | Confidence | Opp. size | Win | Recommended follow-up |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|")
    rows = []
    for s in signals:
        v = s.get("verification")
        tag = " [%s]" % v if v and v != "confirmed" else ""
        rows.append("| %s | %s | %s%s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            cell(s.get("entity")), cell(s.get("country")), cell(s.get("signal")), tag,
            source_link(s), cell(s.get("source_date")), cell(s.get("implies")),
            cell(s.get("likelihood")), cell(s.get("confidence")), cell(s.get("opp_size")),
            cell(s.get("win")), cell(s.get("followup"))))
    return head + "\n" + "\n".join(rows)


HEAD = ("| Deadline | Buyer | Country | Tender | Value/scope | Source |\n|---|---|---|---|---|---|")


def _dl_key(s):
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", cell(s.get("deadline")))
    return m.group(3) + m.group(2) + m.group(1) if m else "99999999"


def _rows(sigs):
    return "\n".join("| %s | %s | %s | %s | %s | %s |" % (
        cell(s.get("deadline")), cell(s.get("entity")), cell(s.get("country")),
        cell(s.get("signal")), cell(s.get("opp_size")), source_link(s)) for s in sigs)


def _plus_30_days(y, m, d):
    """YYYYMMDD 30 days on. datetime is avoided so the whole file stays date-pure:
    every date in the output comes from the data or from --today, never from the clock."""
    days = [31, 29 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d += 30
    while d > days[m - 1]:
        d -= days[m - 1]
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return "%04d%02d%02d" % (y, m, d)


def _fmt(ymd):
    return "%s/%s/%s" % (ymd[6:8], ymd[4:6], ymd[0:4])


def render_pipeline(signals, today, plus30, plus30_label):
    """Three bands, because a flat ascending sort buries the urgent rows under
    already-closed ones. The SKILL requires the <=30-day band to lead."""
    open_ = sorted([s for s in signals if cell(s.get("deadline"))], key=_dl_key)
    if not open_:
        return ""
    soon = [s for s in open_ if today <= _dl_key(s) <= plus30]
    later = [s for s in open_ if _dl_key(s) > plus30]
    past = [s for s in open_ if _dl_key(s) < today]
    out = "\n## Open-tender pipeline (by deadline; closing soonest first)\n"
    if soon:
        out += ("\n### ⚠ Closing within 30 days (by %s) — %d tender(s)\n\n" % (
            plus30_label, len(soon))) + HEAD + "\n" + _rows(soon) + "\n"
    if later:
        out += "\n### Later deadlines — %d tender(s)\n\n" % len(later) + HEAD + "\n" + _rows(later) + "\n"
    if past:
        out += ("\n### Deadline passed — in evaluation / awaiting award (%d)\n\n"
                "These are tracked because the award (and its winner) is the next event.\n\n" % len(past)
                + HEAD + "\n" + _rows(past) + "\n")
    return out


def meaningful(x):
    t = cell(x)
    return bool(t) and not re.match(
        r"^(none|n/a|na|-|null|nan|no issues?|no access issues?|no operator requests?)\.?$", t, re.I)


def render_access_ops(research):
    items = []
    for slug, name in UNITS:
        r = research.get(slug)
        if not r:
            continue
        items.append((name,
                      cell(r.get("access_issues")) if meaningful(r.get("access_issues")) else "",
                      cell(r.get("operator_requests")) if meaningful(r.get("operator_requests")) else ""))
    ai = [i for i in items if i[1]]
    op = [i for i in items if i[2]]
    if not ai and not op:
        return ""
    s = "\n## Access issues & operator requests (per %s)\n" % UNIT_NOUN
    if ai:
        s += "\n| %s | Access issue / what failed & the fallback used |\n|---|---|\n" % UNIT_NOUN
        s += "\n".join("| %s | %s |" % (cell(n), a) for n, a, _ in ai) + "\n"
    if op:
        s += "\n**Operator requests — gated / paywalled / blocked sources to fetch or verify manually:**\n"
        s += "\n".join("- **%s:** %s" % (cell(n), o) for n, _, o in op) + "\n"
    return s


# ---- parent-side reduce: dedup the same notice found by two units ----------
# The brief makes this the parent's job ("dedup the same notice appearing in both TED
# and a national portal"). Key on the notice identity (TED id / Prozorro UA id / exact
# document URL), keep the row with the most detail, and fold the dropped row's URL into
# the kept row as a cross-reference so no citation is lost.
# ONLY a strong notice identity (TED notice id, Prozorro UA id) may auto-merge. A shared
# GENERIC url (a portal search page, an XML/CSV API endpoint, a procurement-plan PDF) means
# "found via the same route", NOT "the same tender" -- several distinct CNB, OeNB, NBRM and
# HNB-plan tenders share one URL, and merging on that silently deletes real notices.
SAME_TENDER_URL = {
    # Banka Slovenije sorter maintenance: the national notice and the TED notice are one tender
    "https://www.enarocanje.si/pregled-objav/1130477": "TED:495378-2026",
}
# URLs where a cross-unit duplicate was manually eyeballed and confirmed to be one item.
MANUAL_DUP_URLS = {
    "https://diavgeia.gov.gr/doc/%ce%a86%ce%93%ce%a8%ce%9f%ce%a1%ce%a12-%ce%a5%ce%9f%ce%a1",
    "https://www.cec.ro/achizitii",
    "https://www.posted.co.rs/o-nama/nabavke.html",
    "https://www.teb-kos.com/wp-content/uploads/2026/05/ifb_supply-of-cash-handling-machines-for-the-bank-needs-.pdf",
    "https://www.teb-kos.com/wp-content/uploads/2026/06/deadline-extension-2-ifb_remote-digital-onboarding-digital-signature-integration.pdf",
}


def dedup_key(s):
    u = cell(s.get("source_url"))
    bare = re.sub(r"[#?].*$", "", u).rstrip("/")
    if bare in SAME_TENDER_URL:
        return SAME_TENDER_URL[bare]
    m = re.search(r"ted\.europa\.eu/\w+/notice/(\d+-\d{4})", u)
    if m:
        return "TED:" + m.group(1)
    m = re.search(r"(UA-\d{4}-\d{2}-\d{2}-\d+-\w)", cell(s.get("signal")) + " " + u)
    if m:
        return "UA:" + m.group(1)
    return "URL:" + bare.lower()


def _tokens(e):
    return {t for t in re.split(r"[^0-9a-zA-Zа-яА-ЯёЁͰ-Ͽ]+", (e or "").lower())
            if len(t) > 3}


def dedup(all_sig):
    groups, order = {}, []
    for s in all_sig:
        k = dedup_key(s)
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append(s)
    kept, dropped = [], []
    for k in order:
        g = groups[k]
        if len(g) == 1:
            kept.append(g[0])
            continue
        if k.startswith("URL:"):
            # never merge on a generic/shared URL unless it is on the manually-verified list,
            # and even then only across DIFFERENT units with overlapping entity names
            if k[4:] not in MANUAL_DUP_URLS:
                kept.extend(g)
                continue
            base = g[0]
            merged, extras = [base], []
            for s in g[1:]:
                if (s.get("_unit") != base.get("_unit")
                        and _tokens(s.get("entity")) & _tokens(base.get("entity"))):
                    merged.append(s)
                else:
                    extras.append(s)
            g = merged
        else:
            extras = []
        g_sorted = sorted(g, key=lambda s: len(cell(s.get("signal"))), reverse=True)
        best, others = g_sorted[0], g_sorted[1:]
        if others:
            urls, names = [], []
            for o in others:
                ou = cell(o.get("source_url"))
                if ou and ou != cell(best.get("source_url")) and ou not in urls:
                    urls.append(ou)
                    names.append(cell(o.get("source_name")) or "second source")
                dropped.append((k, cell(o.get("entity"))))
            if urls:
                best = dict(best)
                best["signal"] = cell(best.get("signal")) + " [Also published as: " + "; ".join(
                    "%s — %s" % (n, u) for n, u in zip(names, urls)) + "]"
        kept.append(best)
        kept.extend(extras)
    return kept, dropped


def main():
    global UNITS, UNIT_NOUN, RUN_DATE, AGENT_NO, AGENT_LABEL
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal", action="append", required=True,
                    help="a run's journal.jsonl; repeatable. LATER runs win per unit, "
                         "so pass the recovery pass last.")
    ap.add_argument("--units-json", required=True, help="path to agent-units.json")
    ap.add_argument("--agent-key", required=True, help='key in agent-units.json, e.g. "2"')
    ap.add_argument("--run-date", required=True, help="YYYY-MM-DD (never derived)")
    ap.add_argument("--today", required=True, help="DD/MM/YYYY, for the <=30-day pipeline band")
    ap.add_argument("--extra-unit", action="append", default=[],
                    help="slug=Display Name -- a unit added to the work-list this run but not "
                         "yet in agent-units.json")
    ap.add_argument("--narrative", required=True, help="path to the prose narrative markdown")
    ap.add_argument("--out", required=True)
    ap.add_argument("--run-note", default="", help="one line on how this run was assembled")
    ap.add_argument("--extra", action="append", default=[],
                    help="slug=file.json[,file2.json] -- verified signals recovered OUTSIDE the "
                         "harness; wins over every journal. Use when a unit is too rich to "
                         "re-emit under the 32k output-token cap and had to be verified in batches.")
    args = ap.parse_args()

    cfg = json.load(open(args.units_json, encoding="utf-8"))[args.agent_key]
    UNITS = [(u["slug"], u.get("name", u["slug"])) for u in cfg["units"]]
    known = {s for s, _ in UNITS}
    for spec in args.extra_unit:
        slug, _, name = spec.partition("=")
        if slug not in known:
            UNITS.append((slug, name or slug))
    UNIT_NOUN = cfg.get("unitNoun", "entity")
    RUN_DATE = args.run_date
    AGENT_NO = args.agent_key
    AGENT_LABEL = cfg.get("agentLabel", "")

    verified, research = {}, {}
    for jp in args.journal:
        v, r = load_journal(jp)
        verified.update(v)      # later journal wins
        research.update(r)

    # batch-verified recoveries (outside the harness) win over everything
    for spec in args.extra:
        slug, _, files = spec.partition("=")
        sigs = []
        for f in files.split(","):
            f = f.strip()
            if not f:
                continue
            batch = json.load(open(f, encoding="utf-8"))
            sigs.extend([s for s in batch if s.get("keep") is not False])
        if sigs:
            verified[slug] = sigs
            print("extra: %s <- %d verified signals" % (slug, len(sigs)))

    all_sig, per_unit = [], {}
    for slug, _ in UNITS:
        for s in verified.get(slug, []):
            s = dict(s)
            s["_unit"] = slug
            all_sig.append(s)
    raw_total = len(all_sig)
    all_sig, dropped = dedup(all_sig)
    for slug, _ in UNITS:
        per_unit[slug] = sum(1 for s in all_sig if s.get("_unit") == slug)
    all_sig.sort(key=value_rank)
    print("dedup: %d -> %d signals (%d duplicate rows merged)" % (raw_total, len(all_sig), len(dropped)))
    for k, ent in dropped:
        print("   merged: %-28s %s" % (k, ent[:60]))

    covered = sum(1 for s, _ in UNITS if per_unit[s] > 0)
    empty = [s for s, _ in UNITS if per_unit[s] == 0]

    header = (
        "# Agent %s — %s — Findings %s\n\n"
        "(Method: shared research harness — one agent per %s, adversarial per-claim verification, "
        "completeness gate, DETERMINISTIC table render. %d %s(s) targeted, %d returned signals, "
        "%d verified signals. Confidence capped at Medium per single-agent playbook. Table rows ordered "
        "by Printec value (size x win), biddable first.)\n"
        % (AGENT_NO, AGENT_LABEL, RUN_DATE, UNIT_NOUN, len(UNITS), UNIT_NOUN, covered, len(all_sig)))
    if args.run_note:
        header += "(Run note: %s)\n" % args.run_note
    if empty:
        header += ('\n> **COVERAGE WARNING:** these %s(s) returned NO signals even after gap-fill and a '
                   'recovery pass — treat as genuine gaps, not "nothing happening": **%s**.\n'
                   % (UNIT_NOUN, ", ".join(empty)))

    narrative = open(args.narrative, encoding="utf-8").read().strip()

    contradicted = [s for s in all_sig if s.get("verification") == "contradicted"]
    unconfirmed = [s for s in all_sig if s.get("verification") == "unconfirmed"]
    verif = ""
    if contradicted or unconfirmed:
        verif = ("\n## Verification notes\n"
                 "- **Corrected/contradicted by the adversarial pass (%d):** %s\n"
                 "- **Unconfirmed (single/weak source, kept at Low) (%d):** %s\n" % (
                     len(contradicted),
                     "; ".join("%s — %s" % (s.get("entity"), cell(s.get("verifier_note")))
                               for s in contradicted[:40]) or "none",
                     len(unconfirmed),
                     ", ".join(str(s.get("entity")) for s in unconfirmed[:60]) or "none"))

    coverage = ("\n## Coverage (per %s, honest)\n\n| %s | signals |\n|---|---|\n" % (UNIT_NOUN, UNIT_NOUN)
                + "\n".join("| %s | %d%s |" % (cell(n), per_unit[s], " ⚠ EMPTY" if per_unit[s] == 0 else "")
                            for s, n in UNITS) + "\n")

    dd, mm, yyyy = args.today.split("/")
    today = yyyy + mm + dd
    d30 = _plus_30_days(int(yyyy), int(mm), int(dd))
    md = "\n".join([header, narrative, render_pipeline(all_sig, today, d30, _fmt(d30)),
                    "\n## Signal table\n", render_table(all_sig), verif,
                    render_access_ops(research), coverage])
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)

    print("units=%d covered=%d signals=%d empty=%s" % (len(UNITS), covered, len(all_sig), empty or "none"))
    print("per-unit: " + ", ".join("%s=%d" % (s, per_unit[s]) for s, _ in UNITS))
    print("open-tender rows=%d  contradicted=%d unconfirmed=%d"
          % (len([s for s in all_sig if cell(s.get('deadline'))]), len(contradicted), len(unconfirmed)))
    print("wrote %s (%d chars)" % (args.out, len(md)))


if __name__ == "__main__":
    main()
