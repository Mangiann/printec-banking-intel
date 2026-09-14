#!/usr/bin/env python3
"""budget_actions.py - set the 2026 group budget beside the market intelligence, cell by cell.

Reads budget/budget_clean.xlsx (target revenue, revenue profit and margin by country, category and
product subcategory), maps it onto the dashboard's markets and product lines (references/budget_map.json)
and joins each cell with what the dashboard knows: open opportunities, dated items inside the budget
year, competitor threats, lost and held positions, and the market outlook. Writes
intel-cache/budget_actions.json for build_dashboard.py. Deterministic; no text generation.

The pipeline is never turned into a euro ratio against the target: the tool's deal sizes are bands for
whole contracts, often multi-year, and a deal touching two lines is counted under both. Opportunities are
shown as a count and a list.

  python3 budget_actions.py --root <BANKING> [--budget budget/budget_clean.xlsx] [--year 2026]
"""
import argparse, datetime, json, os, sys
from collections import defaultdict

def load(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default

def read_budget(path, bmap):
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    cats = {"HW", "SW", "SV", "OUT"}
    recs, country, cat = [], None, None
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        n = str(r[0]).strip()
        if n.startswith("Printec"):
            country, cat = n, None; continue
        if n in cats:
            cat = n; continue
        if n == "TOTAL" or n.startswith("Source") or country is None or cat is None:
            continue
        recs.append({"entity": country, "code": bmap["countries"].get(country), "cat": cat, "sub": n,
                     "rev": float(r[1] or 0), "rp": float(r[2] or 0)})
    return recs

def compute(root, D, year=2026, bpath=None):
    """The whole join, on an in-memory dashboard payload. Returns the budget payload, or None
    when there is no budget file (the dashboard then simply has no budget tab)."""
    class A: pass
    args = A(); args.year = year
    refs = os.path.join(root, "weekly-intelligence", "references")
    bpath = bpath or os.path.join(root, "budget", "budget_clean.xlsx")
    if not os.path.exists(bpath):
        return None
    bmap = load(os.path.join(refs, "budget_map.json"))
    week = D.get("week") or datetime.date.today().isoformat()
    year_end = "%d-12-31" % args.year
    labels = D.get("prod_label", {})
    name = D.get("code2name", {})
    recs = read_budget(bpath, bmap)
    retail = set(bmap["retail"])

    # ---- the budget by cell -------------------------------------------------------------------
    cells = defaultdict(lambda: {"new": 0.0, "rec": 0.0, "rp": 0.0, "subs": defaultdict(float)})
    uncovered = defaultdict(lambda: {"retail": 0.0, "other": 0.0, "retail_rp": 0.0, "other_rp": 0.0})
    for r in recs:
        cc = r["code"]
        if not cc:
            continue
        line = bmap["lines"].get(r["sub"])
        if r["cat"] == "OUT" and line is None and r["sub"] not in retail:
            line = "managed_services"
        if line is None:
            k = "retail" if r["sub"] in retail else "other"
            uncovered[cc][k] += r["rev"]; uncovered[cc][k + "_rp"] += r["rp"]; continue
        c = cells[(cc, line)]
        c["new" if r["cat"] in ("HW", "SW") else "rec"] += r["rev"]
        c["rp"] += r["rp"]; c["subs"][r["sub"] + " (" + r["cat"] + ")"] += r["rev"]

    # group margin per line, revenue-weighted, for the "high margin" test
    line_tot = defaultdict(lambda: [0.0, 0.0])
    for (cc, line), c in cells.items():
        line_tot[line][0] += c["new"] + c["rec"]; line_tot[line][1] += c["rp"]
    line_margin = {l: (v[1] / v[0] if v[0] else 0.0) for l, v in line_tot.items()}

    # ---- what the dashboard knows, per cell --------------------------------------------------
    sigs = D.get("signals", [])
    comps = D.get("competitors", [])
    cons = {(c["country"], c["metric"]): c for c in D.get("projection_consensus", [])}
    deadlines = D.get("deadlines", [])

    def sig_brief(s):
        return {"key": s.get("key"), "title": s.get("bank_theme"), "size_band": s.get("size_band"),
                "pot_value": s.get("pot_value", 0), "dev_date": s.get("dev_date"), "future_date": s.get("future_date"),
                "confidence": s.get("confidence"), "lane": s.get("lane")}

    out_cells = []
    for (cc, line), c in cells.items():
        target = c["new"] + c["rec"]
        margin = c["rp"] / target if target else 0.0
        mine = [s for s in sigs if cc in (s.get("countries") or []) and line in (s.get("products") or [])]
        opps = [s for s in mine if s.get("is_opportunity")]
        lost = [s for s in mine if s.get("lane") == "lost"]
        held = [s for s in mine if s.get("lane") == "installed_base"]
        # dated items inside the budget year: deadlines for this market and line, and opportunities with a trigger date
        dated = []
        for d in deadlines:
            if cc in (d.get("geography") or []) and line in (d.get("products") or []) and week <= str(d.get("date") or "") <= year_end:
                dated.append({"date": d["date"], "title": d.get("title"), "type": d.get("type"), "url": d.get("url")})
        for s in opps:
            fd = str(s.get("future_date") or "")
            if fd and week <= fd <= year_end:
                dated.append({"date": fd, "title": s.get("bank_theme"), "type": "opportunity trigger", "key": s.get("key")})
        dated.sort(key=lambda x: x["date"])
        rivals = [v for v in comps if cc in (v.get("countries") or []) and line in (v.get("products") or [])]
        high = [v for v in rivals if v.get("threat") == "High"]
        metric = bmap["metric_for_outlook"].get(line)
        ol = cons.get((name.get(cc), metric)) if metric else None
        outlook = {"metric": metric, "year": ol["year"], "mean_pct": ol["mean_pct"], "std_pct": ol["std_pct"], "n": ol["n"]} if ol else None

        # ---- the action, from explicit tests; every test that fires is kept as a reason ----------
        reasons, flags = [], []
        big_new, big_rec = c["new"] >= 1e6, c["rec"] >= 1e6
        if big_new and not opps:
            flags.append("find"); reasons.append("EUR %.1fm of new hardware and software revenue is budgeted, and the tool holds no open opportunity in this market and line." % (c["new"] / 1e6))
        if big_new and opps and (dated or len(opps) >= 3):
            flags.append("win"); reasons.append("%d open opportunit%s and %d dated item%s before the end of %d stand behind EUR %.1fm of new revenue." % (len(opps), "y" if len(opps) == 1 else "ies", len(dated), "" if len(dated) == 1 else "s", args.year, c["new"] / 1e6))
        if big_rec and (lost or len(high) >= 3):
            flags.append("defend"); reasons.append("EUR %.1fm of recurring revenue sits where %d competitor win%s %s recorded and %d high-threat rival%s compete%s." % (c["rec"] / 1e6, len(lost), "" if len(lost) == 1 else "s", "is" if len(lost) == 1 else "are", len(high), "" if len(high) == 1 else "s", "s" if len(high) == 1 else ""))
        if margin >= line_margin.get(line, 0) + 0.10 and high and target >= 1e6:
            flags.append("protect margin"); reasons.append("The margin here is %.0f%% against %.0f%% for the line across the group, and %d high-threat rival%s %s present." % (margin * 100, line_margin[line] * 100, len(high), "" if len(high) == 1 else "s", "is" if len(high) == 1 else "are"))
        if outlook and outlook["mean_pct"] >= 5 and len(opps) >= 3 and c["new"] < 2e6:
            flags.append("stretch"); reasons.append("The market is growing about %+.1f%% a year and %d opportunities are open, against a new-revenue target of only EUR %.1fm." % (outlook["mean_pct"], len(opps), c["new"] / 1e6))
        if outlook and outlook["mean_pct"] <= -3 and big_new:
            flags.append("market risk"); reasons.append("The market for %s is shrinking about %.1f%% a year while EUR %.1fm of new revenue is budgeted." % (metric.lower(), outlook["mean_pct"], c["new"] / 1e6))
        # the primary action is the fired test with the most money behind it
        stakes = {"defend": c["rec"], "win": c["new"], "find": c["new"], "protect margin": c["rp"], "market risk": c["new"], "stretch": c["new"]}
        action = max(flags, key=lambda a: stakes[a]) if flags else "watch"
        if action == "watch":
            reasons.append("No dated item, no recorded threat and no test fires for this cell this week.")
        stake = {"defend": c["rec"], "win": c["new"], "find": c["new"], "protect margin": c["rp"], "market risk": c["new"], "stretch": c["new"]}.get(action, target)

        out_cells.append({"code": cc, "country": name.get(cc, cc), "line": line, "line_label": labels.get(line, line),
                          "target": round(target, 2), "new": round(c["new"], 2), "recurring": round(c["rec"], 2),
                          "rp": round(c["rp"], 2), "margin_pct": round(margin * 100, 1), "line_margin_pct": round(line_margin.get(line, 0) * 100, 1),
                          "subcategories": dict(sorted(c["subs"].items(), key=lambda x: -x[1])),
                          "n_opps": len(opps), "opportunities": [sig_brief(s) for s in sorted(opps, key=lambda s: -(s.get("pot_value") or 0))],
                          "n_lost": len(lost), "lost": [sig_brief(s) for s in lost], "n_held": len(held), "held": [sig_brief(s) for s in held],
                          "dated": dated, "n_rivals": len(rivals), "n_high_threat": len(high),
                          "high_threat": [{"name": v.get("name"), "role": v.get("role"), "latest": v.get("latest")} for v in high],
                          "outlook": outlook, "action": action, "flags": flags, "reasons": reasons, "stake": round(stake, 2)})
    out_cells.sort(key=lambda x: -x["stake"])

    total = sum(r["rev"] for r in recs if r["code"]); total_rp = sum(r["rp"] for r in recs if r["code"])
    covered = sum(x["target"] for x in out_cells)
    by_country = defaultdict(lambda: {"target": 0.0, "rp": 0.0, "covered": 0.0})
    for r in recs:
        if r["code"]:
            by_country[r["code"]]["target"] += r["rev"]; by_country[r["code"]]["rp"] += r["rp"]
    for x in out_cells:
        by_country[x["code"]]["covered"] += x["target"]
    by_line = defaultdict(lambda: {"target": 0.0, "rp": 0.0, "cells": 0})
    for x in out_cells:
        by_line[x["line"]]["target"] += x["target"]; by_line[x["line"]]["rp"] += x["rp"]; by_line[x["line"]]["cells"] += 1
    payload = {
        "generated": week, "year": args.year, "budget_file": os.path.basename(bpath), "sheet": "BGT 2026 - 2nd Submission",
        "columns": {"target": "Revenue (TR_REV_Total)", "rp": "RP_Total (revenue profit)", "margin": "RM% = RP_Total / Revenue"},
        "totals": {"target": round(total, 2), "rp": round(total_rp, 2), "margin_pct": round(total_rp / total * 100, 1) if total else 0,
                   "covered": round(covered, 2), "covered_pct": round(covered / total * 100, 1) if total else 0,
                   "new": round(sum(x["new"] for x in out_cells), 2), "recurring": round(sum(x["recurring"] for x in out_cells), 2)},
        "by_country": [{"code": cc, "country": name.get(cc, cc), "target": round(v["target"], 2), "rp": round(v["rp"], 2),
                        "margin_pct": round(v["rp"] / v["target"] * 100, 1) if v["target"] else 0, "covered": round(v["covered"], 2),
                        "retail": round(uncovered[cc]["retail"], 2), "other": round(uncovered[cc]["other"], 2)}
                       for cc, v in sorted(by_country.items(), key=lambda x: -x[1]["target"])],
        "by_line": [{"line": l, "line_label": labels.get(l, l), "target": round(v["target"], 2), "rp": round(v["rp"], 2),
                     "margin_pct": round(v["rp"] / v["target"] * 100, 1) if v["target"] else 0, "cells": v["cells"]}
                    for l, v in sorted(by_line.items(), key=lambda x: -x[1]["target"])],
        "uncovered": {"retail": round(sum(v["retail"] for v in uncovered.values()), 2), "other": round(sum(v["other"] for v in uncovered.values()), 2),
                      "retail_lines": sorted(retail), "note": "Retail lines are outside the banking market tool; 'other' is budget with no product name."},
        "actions_legend": {
            "win": "New revenue is budgeted and open opportunities or dated items exist to go after.",
            "find": "New revenue is budgeted but the tool holds no open opportunity for it yet.",
            "defend": "Recurring revenue sits where competitors have won or several high-threat rivals compete.",
            "protect margin": "The margin is well above the line's group average and strong rivals are present.",
            "market risk": "New revenue is budgeted in a market the projections show shrinking.",
            "stretch": "The market grows and opportunities are open against a small new-revenue target.",
            "watch": "Nothing dated, nothing threatening; no test fires this week."},
        "cells": out_cells}
    return payload

def summary_line(payload):
    from collections import Counter
    return ("budget: %d cells, EUR %.1fm target (%.1f%% covered by the 12 lines) | actions: %s"
            % (len(payload["cells"]), payload["totals"]["target"] / 1e6, payload["totals"]["covered_pct"],
               dict(Counter(x["action"] for x in payload["cells"]))))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--budget", default=None)
    ap.add_argument("--year", type=int, default=2026)
    ap.add_argument("--data", default=None)
    args = ap.parse_args()
    data = args.data or os.path.join(args.root, "intel-cache")
    D = load(os.path.join(data, "dashboard-data.json"))
    if not D:
        raise SystemExit("run build_dashboard.py first: dashboard-data.json is needed for the join")
    payload = compute(args.root, D, args.year, args.budget)
    if payload is None:
        print("budget_actions: no budget file - nothing written"); return 0
    out = os.path.join(data, "budget_actions.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(summary_line(payload))
    return 0

if __name__ == "__main__":
    sys.exit(main())
