#!/usr/bin/env python3
"""budget_2027.py - a 2027 budget proposal from the 2026 budget and the market evidence.

For every budget cell (market x product line) the 2026 target is carried forward with a growth rate
built from three visible parts:
  market  - the 2027 outlook for the cell's metric (mean of the patterns and signals readings on the
            Charts tab); the stretch case uses the upper end of the readings (mean + one std dev)
  share   - what Printec can take beyond the market: the open opportunities in the cell, weighted by
            deal band (XL 3, L 2, M 1, S/unscoped 0.5 points, one point = one percent of new revenue).
            Base counts only opportunities with a dated trigger; stretch counts all of them. Capped.
  threat  - a haircut for recorded competitor wins and for high-threat rivals beyond the second.
            The stretch case takes half the haircut.
New revenue (hardware + software) takes the full rate. Recurring revenue (services + outsourcing) moves
with half the market rate, loses only where a loss is recorded, and gains 2 points in the stretch case
for price and scope. Margins are held at the 2026 cell margin. Subcategories inside a cell scale
together. Lines the market tool does not cover (retail, "other") are carried flat and flagged.
Every cell records its parts, so a number can be traced and challenged. Nothing here is a forecast of
actuals: the base year is the 2026 TARGET, because no actuals file exists yet.

  python3 budget_2027.py --root <BANKING>          (needs intel-cache/dashboard-data.json with DASH.budget)
"""
import argparse, json, os, sys
from collections import defaultdict

BAND_PTS = {"XL": 3.0, "L": 2.0, "M": 1.0, "S": 0.5, "Unscoped": 0.5}
CAP = {"base": {"market": (-10.0, 15.0), "share": 8.0, "loss": 3.0, "loss_max": 6.0, "rival": 1.0, "rival_max": 4.0,
                "new": (-15.0, 35.0), "rec": (-10.0, 12.0), "rec_bonus": 0.0},
       "stretch": {"market": (-10.0, 20.0), "share": 15.0, "loss": 1.5, "loss_max": 3.0, "rival": 0.5, "rival_max": 2.0,
                   "new": (-15.0, 50.0), "rec": (-10.0, 15.0), "rec_bonus": 2.0}}

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def load(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default

def read_budget_rows(root, bmap):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from budget_actions import read_budget
    return read_budget(os.path.join(root, "budget", "budget_clean.xlsx"), bmap)

def cell_growth(x, sigs_by_key, case):
    """The three parts and the two rates for one budget cell, in one scenario."""
    C = CAP[case]
    ol = x.get("outlook") or {}
    m = ol.get("mean_pct")
    if m is None:
        market, market_note = 0.0, "no market projection for this line; market part set to 0"
    else:
        sd = ol.get("std_pct") or 0.0
        raw = m + (sd if case == "stretch" else 0.0)
        market = clamp(raw, *C["market"])
        market_note = "%s outlook %s %+.1f%% a year%s" % (ol.get("metric"), ol.get("year"), m,
                       (" plus one standard deviation (%.1f) for the stretch" % sd) if case == "stretch" and sd else "")
    pts, used, single = 0.0, [], None
    for o in x.get("opportunities", []):
        s = sigs_by_key.get(o["key"], {})
        dated = bool(s.get("has_future_trigger")) or bool(o.get("future_date"))
        if case == "base" and not dated:
            continue
        p = BAND_PTS.get(o.get("size_band") or "Unscoped", 0.5)
        pts += p; used.append({"key": o["key"], "title": o.get("title"), "band": o.get("size_band"), "points": p, "dated": o.get("future_date")})
    share = min(C["share"], pts)
    if used:
        top = max(used, key=lambda u: u["points"])
        if top["points"] >= 0.5 * pts and top["points"] >= 2.0:
            single = top["title"]
    n_lost, n_high = x.get("n_lost", 0), x.get("n_high_threat", 0)
    threat = min(C["loss_max"], C["loss"] * n_lost) + min(C["rival_max"], C["rival"] * max(0, n_high - 2))
    new_rate = clamp(market + share - threat, *C["new"])
    rec_rate = clamp(market / 2.0 - min(C["loss_max"], C["loss"] * n_lost) + C["rec_bonus"], *C["rec"])
    return {"market_pct": round(market, 1), "market_note": market_note, "share_pct": round(share, 1), "share_points": round(pts, 1),
            "share_items": used, "threat_pct": round(threat, 1), "n_lost": n_lost, "n_high_threat": n_high,
            "new_rate_pct": round(new_rate, 1), "recurring_rate_pct": round(rec_rate, 1), "single_point": single}

def compute(root, D, B=None):
    B = B or D.get("budget")
    if not B:
        return None
    bmap = load(os.path.join(root, "weekly-intelligence", "references", "budget_map.json"))
    rows = read_budget_rows(root, bmap)
    sigs = {s["key"]: s for s in D.get("signals", [])}
    cells = {(c["code"], c["line"]): c for c in B["cells"]}
    retail = set(bmap["retail"])
    out_cells, lines_out = [], []
    for (cc, line), x in cells.items():
        g = {case: cell_growth(x, sigs, case) for case in ("base", "stretch")}
        rec = {}
        for case in ("base", "stretch"):
            new27 = x["new"] * (1 + g[case]["new_rate_pct"] / 100.0)
            rec27 = x["recurring"] * (1 + g[case]["recurring_rate_pct"] / 100.0)
            t27 = new27 + rec27
            rec[case] = {"new": round(new27, 2), "recurring": round(rec27, 2), "target": round(t27, 2),
                         "rp": round(t27 * x["margin_pct"] / 100.0, 2),
                         "growth_pct": round((t27 / x["target"] - 1) * 100, 1) if x["target"] else 0.0, **g[case]}
        out_cells.append({"code": cc, "country": x["country"], "line": line, "line_label": x["line_label"],
                          "target_2026": x["target"], "new_2026": x["new"], "recurring_2026": x["recurring"],
                          "rp_2026": x["rp"], "margin_pct": x["margin_pct"], "base": rec["base"], "stretch": rec["stretch"]})
    # subcategory rows in the file's own layout, scaled by their cell's rate (new or recurring)
    rate = {(c["code"], c["line"]): c for c in out_cells}
    for r in rows:
        cc = r["code"]
        if not cc:
            continue
        line = bmap["lines"].get(r["sub"])
        if r["cat"] == "OUT" and line is None and r["sub"] not in retail:
            line = "managed_services"
        c = rate.get((cc, line)) if line else None
        kind = "new" if r["cat"] in ("HW", "SW") else "recurring"
        row = {"entity": r["entity"], "code": cc, "cat": r["cat"], "sub": r["sub"], "line": line,
               "rev_2026": round(r["rev"], 2), "rp_2026": round(r["rp"], 2),
               "margin_pct": round(r["rp"] / r["rev"] * 100, 1) if r["rev"] else 0.0, "covered": bool(c)}
        for case in ("base", "stretch"):
            rt = c[case][kind + "_rate_pct"] if c else 0.0
            v = r["rev"] * (1 + rt / 100.0)
            row[case] = {"rate_pct": rt, "rev": round(v, 2), "rp": round(v * (r["rp"] / r["rev"]) if r["rev"] else 0.0, 2)}
        row["note"] = "" if c else ("retail line, outside the market tool: carried flat" if r["sub"] in retail else "no product line: carried flat")
        lines_out.append(row)
    def tot(case, key="rev"):
        return sum(l[case][key] for l in lines_out)
    t26 = sum(l["rev_2026"] for l in lines_out); rp26 = sum(l["rp_2026"] for l in lines_out)
    by_country = defaultdict(lambda: {"rev_2026": 0.0, "base": 0.0, "stretch": 0.0, "rp_2026": 0.0, "rp_base": 0.0, "rp_stretch": 0.0})
    by_line = defaultdict(lambda: {"rev_2026": 0.0, "base": 0.0, "stretch": 0.0})
    for l in lines_out:
        d = by_country[l["code"]]; d["rev_2026"] += l["rev_2026"]; d["base"] += l["base"]["rev"]; d["stretch"] += l["stretch"]["rev"]
        d["rp_2026"] += l["rp_2026"]; d["rp_base"] += l["base"]["rp"]; d["rp_stretch"] += l["stretch"]["rp"]
        k = l["line"] or ("retail" if l["sub"] in retail else "other")
        e = by_line[k]; e["rev_2026"] += l["rev_2026"]; e["base"] += l["base"]["rev"]; e["stretch"] += l["stretch"]["rev"]
    name = D.get("code2name", {}); labels = D.get("prod_label", {})
    pc = lambda a, b: round((a / b - 1) * 100, 1) if b else 0.0
    payload = {"generated": D.get("week"), "base_year": 2026, "target_year": 2027,
               "method": {"market": "2027 outlook of the cell's metric (mean of patterns and signals); stretch = mean + one std dev; capped",
                          "share": "open opportunities weighted by deal band (XL 3, L 2, M 1, S/unscoped 0.5 points, one point = one percent of new revenue); base counts dated ones only; capped at %s%% base / %s%% stretch" % (CAP["base"]["share"], CAP["stretch"]["share"]),
                          "threat": "minus %s pts per recorded competitor win (max %s) and %s pt per high-threat rival beyond two (max %s); stretch takes half" % (CAP["base"]["loss"], CAP["base"]["loss_max"], CAP["base"]["rival"], CAP["base"]["rival_max"]),
                          "recurring": "half the market rate, minus the loss haircut; +2 pts in the stretch for price and scope",
                          "margin": "held at the 2026 margin of each budget line", "uncovered": "retail and 'other' lines carried flat",
                          "base_is_target": "no actuals file: the 2026 TARGET is the base, not the 2026 outturn"},
               "totals": {"rev_2026": round(t26, 2), "rp_2026": round(rp26, 2),
                          "base": round(tot("base"), 2), "base_growth_pct": pc(tot("base"), t26), "rp_base": round(tot("base", "rp"), 2),
                          "stretch": round(tot("stretch"), 2), "stretch_growth_pct": pc(tot("stretch"), t26), "rp_stretch": round(tot("stretch", "rp"), 2)},
               "by_country": [{"code": cc, "country": name.get(cc, cc), "rev_2026": round(v["rev_2026"], 2), "base": round(v["base"], 2), "base_growth_pct": pc(v["base"], v["rev_2026"]),
                               "stretch": round(v["stretch"], 2), "stretch_growth_pct": pc(v["stretch"], v["rev_2026"]), "rp_2026": round(v["rp_2026"], 2), "rp_base": round(v["rp_base"], 2), "rp_stretch": round(v["rp_stretch"], 2)}
                              for cc, v in sorted(by_country.items(), key=lambda kv: -kv[1]["rev_2026"])],
               "by_line": [{"line": k, "line_label": labels.get(k, k), "rev_2026": round(v["rev_2026"], 2), "base": round(v["base"], 2), "base_growth_pct": pc(v["base"], v["rev_2026"]),
                            "stretch": round(v["stretch"], 2), "stretch_growth_pct": pc(v["stretch"], v["rev_2026"])}
                           for k, v in sorted(by_line.items(), key=lambda kv: -kv[1]["rev_2026"])],
               "cells": sorted(out_cells, key=lambda c: -c["target_2026"]), "rows": lines_out}
    return payload

def _m(v):
    return round(v / 1e6, 2)

def write_workbook(P, path):
    """The proposal in Excel, in the 2026 file's own layout plus summary sheets."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = openpyxl.Workbook()
    H = Font(bold=True); FILL = PatternFill("solid", fgColor="EDE7D8")
    def sheet(title, header, rows, widths=None):
        ws = wb.create_sheet(title)
        ws.append(header)
        for c in ws[1]: c.font = H; c.fill = FILL; c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows: ws.append(r)
        ws.freeze_panes = "A2"
        for i, w in enumerate(widths or [], 1): ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
        return ws
    wb.remove(wb.active)
    T = P["totals"]
    ws = sheet("Summary", ["Item", "2026 budget (EUR m)", "2027 base (EUR m)", "Base growth %", "2027 stretch (EUR m)", "Stretch growth %"],
               [["Revenue", _m(T["rev_2026"]), _m(T["base"]), T["base_growth_pct"], _m(T["stretch"]), T["stretch_growth_pct"]],
                ["Revenue profit", _m(T["rp_2026"]), _m(T["rp_base"]), round((T["rp_base"] / T["rp_2026"] - 1) * 100, 1), _m(T["rp_stretch"]), round((T["rp_stretch"] / T["rp_2026"] - 1) * 100, 1)]],
               [26, 20, 18, 14, 20, 16])
    ws.append([]); ws.append(["Method"]); ws["A%d" % ws.max_row].font = H
    for k, v in P["method"].items(): ws.append([k, v])
    ws.append([]); ws.append(["Generated from the dashboard build of %s. Base year values are the 2026 targets (second submission)." % P["generated"]])
    sheet("By country", ["Country", "2026 (EUR m)", "2027 base", "Base %", "2027 stretch", "Stretch %", "Profit 2026", "Profit base", "Profit stretch"],
          [[c["country"], _m(c["rev_2026"]), _m(c["base"]), c["base_growth_pct"], _m(c["stretch"]), c["stretch_growth_pct"], _m(c["rp_2026"]), _m(c["rp_base"]), _m(c["rp_stretch"])] for c in P["by_country"]],
          [24, 14, 12, 10, 14, 10, 12, 12, 14])
    sheet("By product line", ["Product line", "2026 (EUR m)", "2027 base", "Base %", "2027 stretch", "Stretch %"],
          [[l["line_label"], _m(l["rev_2026"]), _m(l["base"]), l["base_growth_pct"], _m(l["stretch"]), l["stretch_growth_pct"]] for l in P["by_line"]],
          [46, 14, 12, 10, 14, 10])
    rows = []
    for x in P["cells"]:
        for case in ("base", "stretch"):
            g = x[case]
            rows.append([x["country"], x["line_label"], case, _m(x["target_2026"]), _m(g["target"]), g["growth_pct"], _m(x["new_2026"]), _m(g["new"]), g["new_rate_pct"],
                         _m(x["recurring_2026"]), _m(g["recurring"]), g["recurring_rate_pct"], x["margin_pct"], _m(g["rp"]),
                         g["market_pct"], g["market_note"], g["share_pct"], g["share_points"], "; ".join("%s (%s)" % (u["title"], u["band"]) for u in g["share_items"]),
                         g["threat_pct"], g["n_lost"], g["n_high_threat"], g["single_point"] or ""])
    sheet("Cells", ["Country", "Product line", "Case", "2026 target", "2027 target", "Growth %", "New 2026", "New 2027", "New rate %", "Recurring 2026", "Recurring 2027", "Recurring rate %",
                    "Margin % (held)", "Profit 2027", "Market part %", "Market evidence", "Share part %", "Share points", "Opportunities counted", "Threat part %", "Competitor wins", "High-threat rivals", "Single-point dependence"],
          rows, [20, 34, 9, 12, 12, 10, 11, 11, 10, 13, 13, 12, 12, 12, 12, 40, 12, 11, 60, 12, 10, 10, 40])
    sheet("Budget lines 2027", ["Entity", "Category", "Subcategory", "Product line", "2026 revenue", "2026 profit", "Margin %", "2027 base revenue", "Base rate %", "2027 base profit", "2027 stretch revenue", "Stretch rate %", "2027 stretch profit", "Note"],
          [[r["entity"], r["cat"], r["sub"], r["line"] or "", r["rev_2026"], r["rp_2026"], r["margin_pct"], r["base"]["rev"], r["base"]["rate_pct"], r["base"]["rp"], r["stretch"]["rev"], r["stretch"]["rate_pct"], r["stretch"]["rp"], r["note"]] for r in P["rows"]],
          [20, 9, 34, 22, 14, 13, 10, 16, 11, 15, 17, 12, 16, 40])
    wb.save(path)

def write_memo(P, path):
    T = P["totals"]
    lv = sorted(P["cells"], key=lambda x: -(x["stretch"]["target"] - x["target_2026"]))[:20]
    sp = [(x, case) for x in P["cells"] for case in ("base", "stretch") if x[case]["single_point"]]
    L = ["# Budget 2027 proposal — built from the 2026 budget and the market evidence", "",
         "Prepared %s from the dashboard build of %s. Plain-English summary; the figures are in budget_2027_proposal.xlsx." % (P["generated"], P["generated"]), "",
         "## The proposal in one paragraph", "",
         "The 2026 budget is EUR %.1fm of revenue and EUR %.1fm of revenue profit. Carried into 2027 on the market evidence alone, it grows to EUR %.1fm (%+.1f%%). "
         "Stressed on the same evidence, it reaches EUR %.1fm (%+.1f%%), with profit of EUR %.1fm at the 2026 margins. We propose the stressed figure as the 2027 budget and the base figure as the committed floor. "
         "Every line can be traced to its three parts: the market's outlook, the opportunities already on the table, and the competitive threat."
         % (T["rev_2026"] / 1e6, T["rp_2026"] / 1e6, T["base"] / 1e6, T["base_growth_pct"], T["stretch"] / 1e6, T["stretch_growth_pct"], T["rp_stretch"] / 1e6), "",
         "## Two limits to keep in mind", "",
         "- The base year is the 2026 target, not the 2026 outturn. No actuals file exists yet. A line that is behind its 2026 target is stretched from a number it has not reached.",
         "- Retail lines and budget with no product name (EUR %.1fm together) are outside the market tool and are carried flat. They dilute the group growth by about one point." % (sum(l["rev_2026"] for l in P["by_line"] if l["line"] in ("retail", "other")) / 1e6), "",
         "## How each line grows", ""]
    for k, v in P["method"].items(): L.append("- **%s**: %s" % (k, v))
    L += ["", "## By country", "", "| Country | 2026 | 2027 base | Base % | 2027 stretch | Stretch % |", "|---|---|---|---|---|---|"]
    for c in P["by_country"]: L.append("| %s | %.1f | %.1f | %+.1f%% | %.1f | %+.1f%% |" % (c["country"], c["rev_2026"] / 1e6, c["base"] / 1e6, c["base_growth_pct"], c["stretch"] / 1e6, c["stretch_growth_pct"]))
    L += ["", "## By product line", "", "| Line | 2026 | 2027 base | Base % | 2027 stretch | Stretch % |", "|---|---|---|---|---|---|"]
    for l in P["by_line"]: L.append("| %s | %.1f | %.1f | %+.1f%% | %.1f | %+.1f%% |" % (l["line_label"], l["rev_2026"] / 1e6, l["base"] / 1e6, l["base_growth_pct"], l["stretch"] / 1e6, l["stretch_growth_pct"]))
    L += ["", "## The twenty largest growth levers (stretch case)", ""]
    for x in lv:
        g = x["stretch"]
        L.append("- **%s, %s**: EUR %.1fm to EUR %.1fm (%+.1f%%). Market %+.1f%%, share %.1f%% from %d opportunities, threat %.1f%%.%s"
                 % (x["country"], x["line_label"], x["target_2026"] / 1e6, g["target"] / 1e6, g["growth_pct"], g["market_pct"], g["share_pct"], len(g["share_items"]), g["threat_pct"],
                    (" Depends mostly on one item: %s." % g["single_point"]) if g["single_point"] else ""))
    L += ["", "## Where the number rests on a single deal", "", "These cells take at least half their share part from one opportunity. If it is lost, the growth largely goes with it.", ""]
    for x, case in sp: L.append("- %s, %s (%s): %s" % (x["country"], x["line_label"], case, x[case]["single_point"]))
    L += ["", "## What would improve this proposal", "",
          "- A 2026 actuals file (year to date, or the expected outturn) to replace the target as the base.",
          "- The 2025 actuals, so the 2026 growth assumption can be seen and the 2027 one judged against it.",
          "- Finance's breakdown of the 'Other' lines (EUR %.1fm), so they can be mapped and grown with their line." % (sum(l["rev_2026"] for l in P["by_line"] if l["line"] == "other") / 1e6), ""]
    with open(path, "w", encoding="utf-8") as fh: fh.write("\n".join(L))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--data", default=None)
    args = ap.parse_args()
    data = args.data or os.path.join(args.root, "intel-cache")
    D = load(os.path.join(data, "dashboard-data.json"))
    bdir = os.path.join(args.root, "budget")
    B = load(os.path.join(bdir, "budget_actions.json"))
    if not D or not B:
        raise SystemExit("run build_dashboard.py with the budget file in place first (it writes budget/budget_actions.json)")
    P = compute(args.root, D, B)
    with open(os.path.join(bdir, "budget_2027.json"), "w", encoding="utf-8") as fh:
        json.dump(P, fh, ensure_ascii=False, indent=1)
    write_workbook(P, os.path.join(bdir, "budget_2027_proposal.xlsx"))
    write_memo(P, os.path.join(bdir, "BUDGET_2027_PROPOSAL.md"))
    print("wrote budget/budget_2027_proposal.xlsx and budget/BUDGET_2027_PROPOSAL.md")
    T = P["totals"]
    print("budget 2027: 2026 EUR %.1fm -> base EUR %.1fm (%+.1f%%) | stretch EUR %.1fm (%+.1f%%); profit %.1f -> %.1f / %.1f"
          % (T["rev_2026"] / 1e6, T["base"] / 1e6, T["base_growth_pct"], T["stretch"] / 1e6, T["stretch_growth_pct"], T["rp_2026"] / 1e6, T["rp_base"] / 1e6, T["rp_stretch"] / 1e6))
    return 0

if __name__ == "__main__":
    sys.exit(main())
