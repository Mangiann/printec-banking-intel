#!/usr/bin/env python3
"""board_2027.py - the budget board for 2027: packet, reconciliation and the final board file.

The board is a team of agents that plays the company's budget board (briefs in agent-briefs/board/).
This script is the deterministic part around them:

  packet     build the evidence packet from budget/budget_2027.json and the dashboard signals, one
             markdown file per seat plus a group summary and a machine index  -> budget/board/packet/
  reconcile  merge the seats' JSON outputs (round 1 papers, round 2 challenges, responses, capacity)
             into one board table with floor / commit / upside per cell and the open disputes
             -> budget/board/reconciliation.json + .md
  finalize   apply the chair's decision and the votes, write budget/budget_2027_board.json for the
             dashboard (encrypted with the rest of the budget by artifact/build_artifact.py) and
             budget/BOARD_2027_DECISION.md

Rules the script enforces mechanically (the briefs state them; this is where they bite):
  - an evidence key that is not in the packet's signal index is dropped and logged
  - the chair may only decide a dispute with a number that is already on the table
  - a "no" from the delivery adviser caps a cell's commit at the stretch case
  - the floor never sits above the base case

  python3 board_2027.py packet    --root <BANKING>
  python3 board_2027.py reconcile --root <BANKING>
  python3 board_2027.py finalize  --root <BANKING>
  python3 board_2027.py publicize --root <BANKING>   (after the neutral-voice rewrite of round4/texts_public.json)
"""
import argparse, json, os, sys, datetime, re
from collections import defaultdict

LINES_ATM = ["atm_recycling", "physical_security"]
LINES_POS = ["pos_acquiring", "card_issuing", "fraud_monitoring"]
LINES_SVC = ["self_service", "managed_services", "compliance_resilience", "digital_onboarding", "core_digital"]
CODES_CORE = ["RO", "GR", "BG"]
CODES_GROWTH = ["AL", "RS", "BA", "XK", "ME", "MK"]
CODES_EAST = ["UA", "HR", "SI", "SK", "CY", "HU"]

SEATS = {
    "chair":    {"title": "Chief Executive (chair)", "camp": "chair", "votes": False, "scope": "all"},
    "cco":      {"title": "Chief Commercial Officer", "camp": "growth", "votes": True, "scope": "all"},
    "atm":      {"title": "Head of ATM & cash automation", "camp": "growth", "votes": True, "lines": LINES_ATM},
    "pos":      {"title": "Head of Payments & POS", "camp": "growth", "votes": True, "lines": LINES_POS},
    "services": {"title": "Head of Services & software", "camp": "growth", "votes": True, "lines": LINES_SVC},
    "core":     {"title": "Regional head, core markets", "camp": "growth", "votes": True, "codes": CODES_CORE},
    "growthm":  {"title": "Regional head, growth markets", "camp": "growth", "votes": True, "codes": CODES_GROWTH},
    "east":     {"title": "Regional head, east & central", "camp": "swing", "votes": True, "codes": CODES_EAST},
    "cfo":      {"title": "Chief Financial Officer", "camp": "sceptic", "votes": True, "scope": "all"},
    "cro":      {"title": "Chief Risk & Strategy Officer", "camp": "sceptic", "votes": True, "scope": "all"},
    "ned":      {"title": "Independent non-executive", "camp": "sceptic", "votes": True, "scope": "all"},
    "analyst":  {"title": "Budget analyst (Agent 11)", "camp": "staff", "votes": False, "scope": "all"},
    "ops":      {"title": "Head of Operations & delivery", "camp": "staff", "votes": False, "scope": "all"},
}
GROWTH_SEATS = [s for s, v in SEATS.items() if v["camp"] in ("growth", "swing")]
SCEPTIC_SEATS = [s for s, v in SEATS.items() if v["camp"] == "sceptic"]
MIN_CELL = 5e4   # cells under this 2026 target are not shown on the tab and not put to the board


def load(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default


def save(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def m(v):
    return "EUR %.2fm" % (v / 1e6)


def pc(a, b):
    return round((a / b - 1) * 100, 1) if b else 0.0


def cell_key(c):
    return "%s|%s" % (c["code"], c["line"])


def in_scope(seat, c):
    s = SEATS[seat]
    if s.get("scope") == "all":
        return True
    if "lines" in s:
        return c["line"] in s["lines"]
    if "codes" in s:
        return c["code"] in s["codes"]
    return False


# ------------------------------------------------------------------ packet ------------------------
def clip(t, n):
    t = (t or "").replace("\n", " ").strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " ..."


def signal_block(s):
    src = "; ".join("%s: %s" % (x.get("text"), x.get("url")) for x in s.get("sources", []))
    L = ["#### %s  `%s`" % (s.get("bank_theme"), s["key"]),
         "- Countries: %s · Band: %s · Confidence: %s · Recency: %s · Agents: %s · Lane: %s" % (
             ", ".join(s.get("countries") or []), s.get("size_band"), s.get("confidence"), s.get("recency"),
             "+".join(s.get("agents") or []), s.get("lane")),
         "- Date: %s" % clip(s.get("date"), 260),
         "- Trigger date: %s · Likelihood: %s" % (s.get("future_date") or "none", clip(s.get("likelihood"), 200)),
         "- Signal: %s" % clip(s.get("signal"), 700),
         "- What it implies: %s" % clip(s.get("implies"), 450),
         "- Sources: %s" % src, ""]
    return "\n".join(L)


def cell_block(c, A):
    """One budget cell for the packet: the 2026 base, both model cases and their parts."""
    a = A.get(cell_key(c), {})
    L = ["### %s × %s  `%s`" % (c["country"], c["line_label"], cell_key(c)),
         "2026 target %s (new revenue %s, recurring %s, margin %.1f%%)." % (m(c["target_2026"]), m(c["new_2026"]), m(c["recurring_2026"]), c["margin_pct"]),
         "", "| Case | 2027 | Growth | Market | Share (points) | Threat | New-revenue rate | Recurring rate | Single point |", "|---|---|---|---|---|---|---|---|---|"]
    for case in ("base", "stretch"):
        g = c[case]
        L.append("| %s | %s | %+.1f%% | %+.1f%% | +%.1f%% (%.1f) | -%.1f%% | %+.1f%% | %+.1f%% | %s |" % (
            case, m(g["target"]), g["growth_pct"], g["market_pct"], g["share_pct"], g["share_points"], g["threat_pct"],
            g["new_rate_pct"], g["recurring_rate_pct"], g["single_point"] or "-"))
    L.append("")
    L.append("Market part: %s." % c["stretch"]["market_note"])
    ol = a.get("outlook") or {}
    if ol:
        L.append("Outlook readings: metric %s, year %s, mean %s%%, std %s, %s reading(s)." % (ol.get("metric"), ol.get("year"), ol.get("mean_pct"), ol.get("std_pct"), ol.get("n")))
    opps = c["stretch"]["share_items"]
    if opps:
        L.append("Opportunities counted (stretch list; the base counts only the dated ones):")
        for u in opps:
            L.append("- `%s` %s · %s · %s pt%s" % (u["key"], u["title"], u.get("band") or "unscoped", u["points"], (" · dated " + u["dated"]) if u.get("dated") else " · no trigger date"))
    else:
        L.append("No open opportunities in this cell.")
    lost = a.get("lost") or []
    if lost:
        L.append("Competitor wins recorded (%d): %s" % (len(lost), "; ".join("`%s` %s" % (x["key"], x["title"]) for x in lost)))
    ht = a.get("high_threat") or []
    if ht:
        L.append("High-threat rivals (%d): %s" % (len(ht), ", ".join(x.get("name", "?") for x in ht)))
    if a.get("action"):
        L.append("2026 action on this cell: %s (%s)." % (a["action"], ", ".join(a.get("flags") or [])))
    L.append("")
    return "\n".join(L)


def group_summary(P, single):
    T = P["totals"]
    unc = sum(l["rev_2026"] for l in P["by_line"] if l["line"] in ("retail", "other"))
    L = ["# Board packet: the 2027 budget on the evidence (dashboard build of %s)" % P["generated"], "",
         "The 2026 budget is %s of revenue and %s of revenue profit (%.1f%% margin). It is the second submission and it is a TARGET, not an outturn: no actuals file exists." % (m(T["rev_2026"]), m(T["rp_2026"]), T["rp_2026"] / T["rev_2026"] * 100),
         "Carried into 2027 on the market evidence alone (base): %s (%+.1f%%), profit %s." % (m(T["base"]), T["base_growth_pct"], m(T["rp_base"])),
         "Stressed on the same evidence (stretch): %s (%+.1f%%), profit %s at held margins." % (m(T["stretch"]), T["stretch_growth_pct"], m(T["rp_stretch"])),
         "Retail lines and budget with no product name (%s) are outside the market tool and carried flat in both cases." % m(unc), "",
         "## How the model grows each cell", ""]
    for k, v in P["method"].items():
        L.append("- **%s**: %s" % (k, v))
    L += ["", "## By country", "", "| Country | 2026 | 2027 base | Base % | 2027 stretch | Stretch % |", "|---|---|---|---|---|---|"]
    for c in P["by_country"]:
        L.append("| %s (%s) | %.1f | %.1f | %+.1f%% | %.1f | %+.1f%% |" % (c["country"], c["code"], c["rev_2026"] / 1e6, c["base"] / 1e6, c["base_growth_pct"], c["stretch"] / 1e6, c["stretch_growth_pct"]))
    L += ["", "## By product line", "", "| Line | id | 2026 | 2027 base | Base % | 2027 stretch | Stretch % |", "|---|---|---|---|---|---|---|"]
    for l in P["by_line"]:
        L.append("| %s | `%s` | %.1f | %.1f | %+.1f%% | %.1f | %+.1f%% |" % (l["line_label"], l["line"], l["rev_2026"] / 1e6, l["base"] / 1e6, l["base_growth_pct"], l["stretch"] / 1e6, l["stretch_growth_pct"]))
    if P.get("parts"):
        L += ["", "## Where the model's growth comes from (EUR m, group)", "", "| Case | Named deals (signals) | Market outlook | Competitor threat | Recurring revenue |", "|---|---|---|---|---|"]
        for case in ("base", "stretch"):
            q = P["parts"][case]
            L.append("| %s | %.2f | %.2f | %.2f | %.2f |" % (case, q["named_deals"] / 1e6, q["market_outlook"] / 1e6, q["threat"] / 1e6, q["recurring"] / 1e6))
        oc = P["parts"]["stretch"]["outlook_cells"]
        L += ["", "The market outlook is the mean of the dashboard's readings for the cell's metric: %d cells rest on patterns and signals readings together, %d on signals readings only, %d on patterns only, %d have no outlook (market part 0). There is no statistical trend fit anywhere." % (oc["patterns_and_signals"], oc["signals_only"], oc["patterns_only"], oc["none"])]
    L += ["", "## Cells where one deal carries at least half the share part", ""]
    for ck, case, title in single:
        L.append("- `%s` (%s): %s" % (ck, case, title))
    L += ["", "## Two rules of the model changed on 14/09/2026 after the first board", "",
          "- A footprint-wide item (a regulation, a group-wide programme) is counted once per country, in its lead product line, at half weight. In other cells it is listed with 0 points and the cell where it is counted.",
          "- For self-service and branch transformation a falling branch count is read as conversion demand: the branch outlook enters as its absolute value. Closing branches does not stop transformation; it concentrates it in the branches that stay and moves cash to machines.", "",
          "## New business", "",
          "Country x product combinations with open opportunities in the signals but no 2026 budget (or under EUR 50k). The model puts no euro on them. Seats price them as cells with key `CC|line`, 2026 = 0, and the same rules: a number needs a named opportunity, a labelled conversion assumption, and a capacity yes. Two product areas here sit outside the twelve budget lines: payments modernisation (instant / ISO 20022) and payment security (HSM).", ""]
    L += ["", "## Board rules that bind every seat", "",
          "1. Every figure you quote must be in this packet, quoted with its cell key or signal key. Anything else is dropped by the analyst.",
          "2. A judgment the evidence does not give (for example a conversion rate on a named deal) is allowed only as a labelled board assumption: deal key, date, percentage. The dashboard never states win odds as fact.",
          "3. The base year is the 2026 target, not the 2026 outturn.",
          "4. A commit above the stretch case needs a named opportunity with a trigger date inside 2027, a labelled conversion assumption, and a yes from the delivery adviser.",
          "5. In a single-deal cell the commit counts that deal at half unless its date is inside 2027.",
          "6. Evidence beats votes; judgment goes to a vote. The chair cannot invent a number.",
          "7. Plain English: short sentences, one idea per sentence, no dramatic phrasing. Numbers, dates, names and keys never change in editing.", ""]
    return "\n".join(L)


def cmd_packet(root):
    P = load(os.path.join(root, "budget", "budget_2027.json"))
    B = load(os.path.join(root, "budget", "budget_actions.json"))
    D = load(os.path.join(root, "intel-cache", "dashboard-data.json"))
    if not (P and B and D):
        sys.exit("need budget/budget_2027.json, budget/budget_actions.json and intel-cache/dashboard-data.json")
    sigs = {s["key"]: s for s in D.get("signals", [])}
    A = {cell_key(c): c for c in B["cells"]}
    cells = [c for c in P["cells"] if c["target_2026"] >= MIN_CELL]
    NB = [e for e in P.get("new_business", []) if e["n_opps"] >= 2]
    single = [(cell_key(c), case, c[case]["single_point"]) for c in cells for case in ("base", "stretch") if c[case]["single_point"]]
    out = os.path.join(root, "budget", "board", "packet")
    os.makedirs(out, exist_ok=True)
    G = group_summary(P, single)
    with open(os.path.join(out, "group.md"), "w", encoding="utf-8") as fh:
        fh.write(G)
    index = {}
    for seat in SEATS:
        mine = [c for c in cells if in_scope(seat, c)]
        keys = []
        for c in mine:
            for u in c["stretch"]["share_items"]:
                keys.append(u["key"])
            for x in (A.get(cell_key(c), {}).get("lost") or []):
                keys.append(x["key"])
        nb_mine = [e for e in NB if in_scope(seat, e)]
        for e in nb_mine:
            for u in e["opportunities"]:
                keys.append(u["key"])
        keys = [k for k in dict.fromkeys(keys) if k in sigs]
        L = [G, "", "# Cells in the scope of this seat: %s (%d cells, %s of 2026 revenue)" % (SEATS[seat]["title"], len(mine), m(sum(c["target_2026"] for c in mine))), ""]
        for c in sorted(mine, key=lambda x: (x["code"], -x["target_2026"])):
            L.append(cell_block(c, A))
        if nb_mine:
            L += ["", "# New business in the scope of this seat (%d combinations with two or more opportunities; 2026 budget = 0)" % len(nb_mine), ""]
            for e in nb_mine:
                L.append("### %s × %s  `%s|%s`  (new business, %d opportunities%s)" % (e["country"], e["line_label"], e["code"], e["line"], e["n_opps"], "" if e["in_budget_lines"] else "; product area outside the twelve budget lines"))
                for u in e["opportunities"]:
                    L.append("- `%s` %s · %s · %s%s" % (u["key"], u["title"], u.get("band") or "unscoped", ("dated " + u["dated"]) if u.get("dated") else "no trigger date", " · footprint-wide" if u.get("footprint_wide") else ""))
                L.append("")
        L += ["", "# Evidence: the signals behind the opportunities and competitor wins above (%d)" % len(keys), "",
              "Quote a signal by its key in backticks. The dashboard links the key to the full signal and its sources.", ""]
        for k in keys:
            L.append(signal_block(sigs[k]))
        with open(os.path.join(out, "%s.md" % seat), "w", encoding="utf-8") as fh:
            fh.write("\n".join(L))
        index[seat] = {"cells": [cell_key(c) for c in mine], "new_business": ["%s|%s" % (e["code"], e["line"]) for e in nb_mine], "signals": keys}
        print("packet %-9s %3d cells %3d signals %6.0f kB" % (seat, len(mine), len(keys), len("\n".join(L).encode()) / 1e3))
    allkeys = sorted({k for v in index.values() for k in v["signals"]})
    save(os.path.join(out, "signals_index.json"), {k: {"title": sigs[k]["bank_theme"], "countries": sigs[k].get("countries"), "band": sigs[k].get("size_band"),
                                                       "future_date": sigs[k].get("future_date"), "confidence": sigs[k].get("confidence")} for k in allkeys})
    save(os.path.join(out, "seats.json"), {"seats": {s: {**SEATS[s], **index[s]} for s in SEATS}, "generated": P["generated"],
                                            "cells": {cell_key(c): {"country": c["country"], "line_label": c["line_label"], "target_2026": c["target_2026"],
                                                                    "base": c["base"]["target"], "stretch": c["stretch"]["target"]} for c in cells},
                                            "new_business": {"%s|%s" % (e["code"], e["line"]): {"country": e["country"], "line_label": e["line_label"], "n_opps": e["n_opps"]} for e in NB}})
    print("packet written to %s (%d cells, %d signals)" % (out, len(cells), len(allkeys)))


# ------------------------------------------------------------------ reconcile ---------------------
def rd_json(p):
    obj = load(p)
    if obj is None:
        return None
    return obj


def cmd_reconcile(root):
    bdir = os.path.join(root, "budget", "board")
    P = load(os.path.join(root, "budget", "budget_2027.json"))
    S = load(os.path.join(bdir, "packet", "seats.json"))
    sigidx = load(os.path.join(bdir, "packet", "signals_index.json"))
    cells = {cell_key(c): c for c in P["cells"] if c["target_2026"] >= MIN_CELL}
    nb_keys = set()
    for e in P.get("new_business", []):
        k = "%s|%s" % (e["code"], e["line"])
        cells[k] = {"code": e["code"], "country": e["country"], "line": e["line"], "line_label": e["line_label"], "target_2026": 0.0,
                    "base": {"target": 0.0}, "stretch": {"target": 0.0}, "new_business": True}
        nb_keys.add(k)
    log = []

    def evid(keys):
        ok = [k for k in (keys or []) if k in sigidx]
        bad = [k for k in (keys or []) if k not in sigidx]
        for k in bad:
            log.append("dropped evidence key not in the packet: %s" % k)
        return ok

    # round 1
    growth = {}     # cell -> seat -> {commit, upside, reason, evidence, assumptions, conditions}
    sceptic = {}    # cell -> seat -> {cut_to, reason, condition, evidence}
    targets = {}    # seat -> growth target %
    r1 = os.path.join(bdir, "round1")
    for seat in GROWTH_SEATS + SCEPTIC_SEATS:
        J = rd_json(os.path.join(r1, "%s.json" % seat))
        if not J:
            log.append("round 1: no paper from %s" % seat); continue
        targets[seat] = J.get("growth_target_pct")
        for x in J.get("cells", []):
            ck = x.get("cell")
            if ck not in cells:
                log.append("%s: unknown cell %s ignored" % (seat, ck)); continue
            if SEATS[seat]["camp"] in ("growth", "swing"):
                if x.get("commit") is None:
                    continue
                growth.setdefault(ck, {})[seat] = {"commit": float(x["commit"]), "upside": float(x.get("upside") or x["commit"]),
                                                   "reason": x.get("reason", ""), "evidence": evid(x.get("evidence")),
                                                   "assumptions": x.get("assumptions") or [], "conditions": x.get("conditions") or []}
            else:
                if x.get("cut_to") is None:
                    continue
                sceptic.setdefault(ck, {})[seat] = {"cut_to": float(x["cut_to"]), "reason": x.get("reason", ""),
                                                    "condition": x.get("condition_to_restore", ""), "evidence": evid(x.get("evidence"))}
    # round 2: challenges, responses, capacity
    r2 = os.path.join(bdir, "round2")
    challenges = defaultdict(list)   # cell -> [{sceptic, target_seat, proposed, challenge}]
    for seat in SCEPTIC_SEATS:
        J = rd_json(os.path.join(r2, "%s.json" % seat))
        if not J:
            log.append("round 2: no challenges from %s" % seat); continue
        for x in J.get("challenges", []):
            if x.get("cell") in cells and x.get("proposed") is not None:
                challenges[x["cell"]].append({"sceptic": seat, "target_seat": x.get("target_seat"), "proposed": float(x["proposed"]), "challenge": x.get("challenge", "")})
    responses = defaultdict(list)    # cell -> [{seat, from, outcome, commit, reason}]
    for seat in GROWTH_SEATS:
        J = rd_json(os.path.join(r2, "%s-response.json" % seat))
        if not J:
            continue
        for x in J.get("responses", []):
            if x.get("cell") in cells:
                responses[x["cell"]].append({"seat": seat, "from": x.get("from"), "outcome": x.get("outcome"), "commit": float(x["commit"]) if x.get("commit") is not None else None, "reason": x.get("reason", "")})
                if seat in growth.get(x["cell"], {}) and x.get("commit") is not None and x.get("outcome") in ("conceded", "adjusted"):
                    growth[x["cell"]][seat]["commit"] = float(x["commit"])
    capacity = {}
    J = rd_json(os.path.join(r2, "ops.json"))
    if J:
        for x in J.get("verdicts", []):
            if x.get("cell") in cells:
                capacity[x["cell"]] = {"verdict": x.get("verdict"), "reason": x.get("reason", "")}
    else:
        log.append("round 2: no capacity note from ops")

    out_cells, disputes = [], []
    for ck, c in cells.items():
        base, stretch = c["base"]["target"], c["stretch"]["target"]
        gp = growth.get(ck, {})
        if ck in nb_keys and not any(v["commit"] > 0 for v in gp.values()):
            continue      # new business nobody priced stays off the table
        if gp:
            proposer = min(gp, key=lambda s: gp[s]["commit"])
            commit = gp[proposer]["commit"]
            upside = max(max(v["upside"] for v in gp.values()), commit)
        else:
            proposer, commit, upside = "model", stretch, stretch
        cap = capacity.get(ck)
        capped = False
        if cap and cap["verdict"] == "no" and commit > stretch:
            commit, capped = stretch, True
            upside = max(upside, commit)
        sp = sceptic.get(ck, {})
        s_low = None
        cand = [(v["cut_to"], s, v["reason"]) for s, v in sp.items()] + [(x["proposed"], x["sceptic"], x["challenge"]) for x in challenges.get(ck, [])]
        if cand:
            s_low = min(cand, key=lambda t: t[0])
        floor = min(base, s_low[0]) if s_low else base
        floor = min(floor, commit)
        dispute = None
        if s_low and s_low[0] < commit - 1:
            outcomes = [r["outcome"] for r in responses.get(ck, []) if r.get("from") == s_low[1]]
            if "conceded" not in outcomes:
                dispute = {"cell": ck, "country": c["country"], "line_label": c["line_label"], "commit": commit, "proposer": proposer,
                           "sceptic": s_low[1], "sceptic_number": s_low[0], "gap": commit - s_low[0], "sceptic_reason": s_low[2],
                           "growth_reason": gp.get(proposer, {}).get("reason", ""), "outcome": outcomes[0] if outcomes else "no response"}
                disputes.append(dispute)
        evidence = list(dict.fromkeys(k for v in gp.values() for k in v["evidence"]))
        conditions = list(dict.fromkeys(x for v in gp.values() for x in v["conditions"] if x))
        assumptions = [a for v in gp.values() for a in v["assumptions"]]
        out_cells.append({"cell": ck, "code": c["code"], "country": c["country"], "line": c["line"], "line_label": c["line_label"],
                          "target_2026": c["target_2026"], "base": base, "stretch": stretch,
                          "floor": floor, "commit": commit, "upside": upside, "proposer": proposer,
                          "reason": gp.get(proposer, {}).get("reason", "") if gp else "no seat proposed a number; the model's stretch case stands",
                          "proposals": {s: v["commit"] for s, v in gp.items()}, "upsides": {s: v["upside"] for s, v in gp.items()},
                          "sceptic_number": s_low[0] if s_low else None, "sceptic": s_low[1] if s_low else None, "sceptic_reason": s_low[2] if s_low else "",
                          "capacity": cap, "capped_by_capacity": capped, "evidence": evidence, "conditions": conditions, "assumptions": assumptions,
                          "responses": responses.get(ck, []), "dispute": bool(dispute), "new_business": ck in nb_keys})
    disputes.sort(key=lambda d: -d["gap"])
    T = P["totals"]
    unc = T["base"] - sum(c["base"]["target"] for c in P["cells"])   # retail + other + tiny cells, flat
    small = sum(c["base"]["target"] for c in P["cells"] if c["target_2026"] < MIN_CELL)
    unc += small
    tot = lambda k: sum(x[k] for x in out_cells) + unc
    nbt = lambda k: sum(x[k] for x in out_cells if x["new_business"])
    R = {"generated": datetime.date.today().isoformat(), "built_from": P["generated"], "uncovered_flat": unc,
         "totals": {"rev_2026": T["rev_2026"], "base": T["base"], "stretch": T["stretch"],
                    "floor": tot("floor"), "commit": tot("commit"), "upside": tot("upside"),
                    "new_business_commit": nbt("commit"), "new_business_upside": nbt("upside")},
         "growth_targets_round1": targets, "cells": out_cells, "disputes": disputes, "log": log}
    for k in ("floor", "commit", "upside"):
        R["totals"][k + "_growth_pct"] = pc(R["totals"][k], T["rev_2026"])
    save(os.path.join(bdir, "reconciliation.json"), R)
    write_reconciliation_md(R, P, os.path.join(bdir, "reconciliation.md"))
    print("reconciled %d cells, %d disputes; floor %s (%+.1f%%), commit %s (%+.1f%%), upside %s (%+.1f%%)" % (
        len(out_cells), len(disputes), m(R["totals"]["floor"]), R["totals"]["floor_growth_pct"], m(R["totals"]["commit"]), R["totals"]["commit_growth_pct"], m(R["totals"]["upside"]), R["totals"]["upside_growth_pct"]))
    for l in log:
        print("  note:", l)


def write_reconciliation_md(R, P, path):
    T = R["totals"]
    L = ["# Reconciliation: the board table before the vote", "",
         "Built %s from the round-1 papers, the round-2 challenges and responses, and the delivery adviser's capacity note. Model build of %s." % (R["generated"], R["built_from"]), "",
         "| | 2027 | Growth on 2026 |", "|---|---|---|",
         "| 2026 budget | %s | |" % m(T["rev_2026"]),
         "| Model base | %s | %+.1f%% |" % (m(T["base"]), pc(T["base"], T["rev_2026"])),
         "| Model stretch | %s | %+.1f%% |" % (m(T["stretch"]), pc(T["stretch"], T["rev_2026"])),
         "| **Floor** (lowest number on the table per cell) | %s | %+.1f%% |" % (m(T["floor"]), T["floor_growth_pct"]),
         "| **Commit** (growth camp's number after challenges) | %s | %+.1f%% |" % (m(T["commit"]), T["commit_growth_pct"]),
         "| **Upside** (largest number on the table per cell) | %s | %+.1f%% |" % (m(T["upside"]), T["upside_growth_pct"]), "",
         "New business priced by the seats (inside the totals above): commit %s, upside %s." % (m(T.get("new_business_commit", 0)), m(T.get("new_business_upside", 0))), "",
         "Retail, 'other' and cells under EUR 50k are carried flat at %s in every row." % m(R["uncovered_flat"]), "",
         "Growth targets asked for in round 1: " + ", ".join("%s %s%%" % (s, v) for s, v in R["growth_targets_round1"].items() if v is not None), "",
         "## Open disputes, largest gap first", "",
         "A dispute is a cell where a sceptic's number sits below the commit and the growth seat did not concede. The chair decides each one with a number already on the table.", ""]
    for i, d in enumerate(R["disputes"], 1):
        L.append("%d. `%s` %s × %s: commit %s (%s) versus %s (%s), gap %s. Growth: %s Sceptic: %s Outcome so far: %s." % (
            i, d["cell"], d["country"], d["line_label"], m(d["commit"]), d["proposer"], m(d["sceptic_number"]), d["sceptic"], m(d["gap"]),
            clip(d["growth_reason"], 300), clip(d["sceptic_reason"], 300), d["outcome"]))
    nb = [x for x in R["cells"] if x.get("new_business")]
    if nb:
        L += ["", "## New business priced by the seats (2026 budget = 0)", "", "| Cell | Commit | Upside | Proposer | Sceptic low | Capacity | Dispute |", "|---|---|---|---|---|---|---|"]
        for x in sorted(nb, key=lambda x: -x["commit"]):
            L.append("| `%s` %s × %s | %.2f | %.2f | %s | %s | %s | %s |" % (x["cell"], x["country"], x["line_label"], x["commit"] / 1e6, x["upside"] / 1e6, x["proposer"],
                     ("%.2f (%s)" % (x["sceptic_number"] / 1e6, x["sceptic"])) if x["sceptic_number"] is not None else "-", (x["capacity"] or {}).get("verdict", "-"), "yes" if x["dispute"] else ""))
    L += ["", "## Every cell", "", "| Cell | 2026 | Base | Stretch | Floor | Commit | Upside | Proposer | Sceptic low | Capacity | Dispute |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in sorted([x for x in R["cells"] if not x.get("new_business")], key=lambda x: -x["target_2026"]):
        L.append("| `%s` | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %s | %s | %s | %s |" % (
            x["cell"], x["target_2026"] / 1e6, x["base"] / 1e6, x["stretch"] / 1e6, x["floor"] / 1e6, x["commit"] / 1e6, x["upside"] / 1e6, x["proposer"],
            ("%.2f (%s)" % (x["sceptic_number"] / 1e6, x["sceptic"])) if x["sceptic_number"] is not None else "-",
            (x["capacity"] or {}).get("verdict", "-"), "yes" if x["dispute"] else ""))
    L += ["", "## Conditions and assumptions attached by the growth seats", ""]
    for x in R["cells"]:
        if x["conditions"] or x["assumptions"]:
            L.append("- `%s`: %s%s" % (x["cell"], "; ".join(x["conditions"]),
                                        (" · assumptions: " + "; ".join("%s %s%% by %s" % (a.get("deal"), a.get("conversion_pct"), a.get("date")) for a in x["assumptions"])) if x["assumptions"] else ""))
    if R["log"]:
        L += ["", "## Analyst notes", ""] + ["- " + l for l in R["log"]]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


# ------------------------------------------------------------------ finalize ----------------------
def cmd_finalize(root):
    bdir = os.path.join(root, "budget", "board")
    P = load(os.path.join(root, "budget", "budget_2027.json"))
    R = load(os.path.join(bdir, "reconciliation.json"))
    Dc = load(os.path.join(bdir, "round4", "decision.json"))
    sigidx = load(os.path.join(bdir, "packet", "signals_index.json"))
    if not (P and R and Dc):
        sys.exit("need reconciliation.json and round4/decision.json")
    votes = []
    vdir = os.path.join(bdir, "round4", "votes")
    if os.path.isdir(vdir):
        for f in sorted(os.listdir(vdir)):
            if f.endswith(".json"):
                v = load(os.path.join(vdir, f))
                if v:
                    votes.append({"seat": v.get("seat"), "title": SEATS.get(v.get("seat"), {}).get("title", v.get("seat")), "camp": SEATS.get(v.get("seat"), {}).get("camp"),
                                  "vote": v.get("vote"), "reason": v.get("reason", ""), "minority_report": v.get("minority_report", "")})
    log = list(R.get("log", []))
    decisions = {d["cell"]: d for d in Dc.get("disputes", [])}
    cells_model = {cell_key(c): c for c in P["cells"]}
    cmargin = {c["code"]: (c["rp_2026"] / c["rev_2026"] * 100 if c["rev_2026"] else 0.0) for c in P["by_country"]}
    out, out_nb = [], []
    for x in R["cells"]:
        nb = bool(x.get("new_business"))
        c = cells_model.get(x["cell"]) if not nb else {"stretch": {"target": 0.0, "new": 0.0, "recurring": 0.0}, "base": {"target": 0.0}, "margin_pct": round(cmargin.get(x["code"], 0.0), 1)}
        commit, decided, dreason = x["commit"], False, ""
        d = decisions.get(x["cell"])
        if d and d.get("decision") is not None:
            on_table = sorted({x["commit"], x["floor"], x["upside"], x["base"], x["stretch"]} | set(x["proposals"].values()) | ({x["sceptic_number"]} if x["sceptic_number"] is not None else set()))
            want = float(d["decision"])
            pick = min(on_table, key=lambda v: abs(v - want))
            if abs(pick - want) > 1:
                log.append("chair's number %s for %s was not on the table; nearest on-table number %s used" % (want, x["cell"], pick))
            commit, decided, dreason = pick, True, d.get("reason", "")
        commit = max(commit, x["floor"])
        upside = max(x["upside"], commit)
        ratio = commit / c["stretch"]["target"] if c["stretch"]["target"] else 1.0
        new = c["stretch"]["new"] * ratio if not nb else commit
        rec = c["stretch"]["recurring"] * ratio if not nb else 0.0
        # where the board's number comes from: the model's market-outlook and recurring parts of the case
        # the number sits in (base if at or below the base, else stretch); the rest is named deals net of threat
        if nb:
            parts = {"market_outlook": 0.0, "recurring": 0.0, "named_deals_net": round(commit, 2), "case": "new"}
        else:
            case = "base" if commit <= c["base"]["target"] + 1 else "stretch"
            gg = c[case]
            mk = c["new_2026"] * gg["market_pct"] / 100.0; rc = c["recurring_2026"] * gg["recurring_rate_pct"] / 100.0
            parts = {"market_outlook": round(mk, 2), "recurring": round(rc, 2), "named_deals_net": round(commit - x["target_2026"] - mk - rc, 2), "case": case,
                     "outlook_origins": gg.get("outlook_origins") or {}}
        dissent = None
        if x["sceptic_number"] is not None and x["sceptic_number"] < commit - 1:
            dissent = {"seat": x["sceptic"], "number": x["sceptic_number"], "reason": x["sceptic_reason"]}
        (out_nb if nb else out).append({"code": x["code"], "country": x["country"], "line": x["line"], "line_label": x["line_label"],
                    "target_2026": x["target_2026"], "base": x["base"], "stretch": x["stretch"], "new_business": nb,
                    "board": {"target": round(commit, 2), "floor": round(x["floor"], 2), "upside": round(upside, 2), "parts": parts,
                              "growth_pct": pc(commit, x["target_2026"]) if not nb else None, "floor_growth_pct": pc(x["floor"], x["target_2026"]) if not nb else None, "upside_growth_pct": pc(upside, x["target_2026"]) if not nb else None,
                              "new": round(new, 2), "recurring": round(rec, 2), "rp": round(commit * c["margin_pct"] / 100.0, 2), "margin_pct": c["margin_pct"],
                              "proposer": x["proposer"], "proposer_title": SEATS.get(x["proposer"], {}).get("title", x["proposer"]),
                              "reason": x["reason"], "evidence": [k for k in x["evidence"] if k in sigidx],
                              "conditions": x["conditions"], "assumptions": x["assumptions"],
                              "capacity": x["capacity"], "capped_by_capacity": x["capped_by_capacity"],
                              "dissent": dissent, "decided_by_chair": decided, "chair_reason": dreason,
                              "above_stretch": commit > x["stretch"] + 1}})
    unc = R["uncovered_flat"]
    T = P["totals"]
    tot = lambda k: sum(o["board"][k] for o in out + out_nb) + unc
    rp = lambda k: sum(o["board"][k] * o["board"]["margin_pct"] / 100.0 for o in out + out_nb) + (T["rp_base"] - sum(c["base"]["rp"] for c in P["cells"]))
    totals = {"rev_2026": T["rev_2026"], "rp_2026": T["rp_2026"], "base": T["base"], "stretch": T["stretch"],
              "floor": round(tot("floor"), 2), "commit": round(tot("target"), 2), "upside": round(tot("upside"), 2),
              "rp_floor": round(rp("floor"), 2), "rp_commit": round(rp("target"), 2), "rp_upside": round(rp("upside"), 2),
              "new_business_commit": round(sum(o["board"]["target"] for o in out_nb), 2), "new_business_upside": round(sum(o["board"]["upside"] for o in out_nb), 2),
              "commit_existing": round(sum(o["board"]["target"] for o in out) + unc, 2)}
    totals["parts"] = {"named_deals_net": round(sum(o["board"]["parts"]["named_deals_net"] for o in out), 2),
                       "market_outlook": round(sum(o["board"]["parts"]["market_outlook"] for o in out), 2),
                       "recurring": round(sum(o["board"]["parts"]["recurring"] for o in out), 2),
                       "new_business": totals["new_business_commit"], "flat": 0.0,
                       "outlook_cells": (P.get("parts") or {}).get("stretch", {}).get("outlook_cells")}
    for k in ("floor", "commit", "upside"):
        totals[k + "_growth_pct"] = pc(totals[k], T["rev_2026"])
    by_c, by_l = defaultdict(lambda: defaultdict(float)), defaultdict(lambda: defaultdict(float))
    name = {c["code"]: c["country"] for c in P["by_country"]}
    label = {l["line"]: l["line_label"] for l in P["by_line"]}
    for o in out + out_nb:
        for k in ("floor", "target", "upside"):
            by_c[o["code"]][k] += o["board"][k]; by_l[o["line"]][k] += o["board"][k]
    # flat parts per country / line come from the model's base minus the covered cells
    cov_c, cov_l = defaultdict(float), defaultdict(float)
    for c in P["cells"]:
        cov_c[c["code"]] += c["base"]["target"]; cov_l[c["line"]] += c["base"]["target"]
    by_country, by_line = [], []
    for c in P["by_country"]:
        flat = c["base"] - cov_c[c["code"]]
        v = by_c[c["code"]]
        by_country.append({"code": c["code"], "country": c["country"], "rev_2026": c["rev_2026"], "base": c["base"], "stretch": c["stretch"],
                           "floor": round(v["floor"] + flat, 2), "commit": round(v["target"] + flat, 2), "upside": round(v["upside"] + flat, 2),
                           "floor_growth_pct": pc(v["floor"] + flat, c["rev_2026"]), "commit_growth_pct": pc(v["target"] + flat, c["rev_2026"]), "upside_growth_pct": pc(v["upside"] + flat, c["rev_2026"])})
    for l in P["by_line"]:
        flat = l["base"] - cov_l[l["line"]]
        v = by_l[l["line"]]
        by_line.append({"line": l["line"], "line_label": l["line_label"], "rev_2026": l["rev_2026"], "base": l["base"], "stretch": l["stretch"],
                        "floor": round(v["floor"] + flat, 2), "commit": round(v["target"] + flat, 2), "upside": round(v["upside"] + flat, 2),
                        "floor_growth_pct": pc(v["floor"] + flat, l["rev_2026"]), "commit_growth_pct": pc(v["target"] + flat, l["rev_2026"]), "upside_growth_pct": pc(v["upside"] + flat, l["rev_2026"])})
    rep = Dc.get("report") or {}
    for sec in rep.get("sections", []):
        sec["evidence"] = [k for k in (sec.get("evidence") or []) if k in sigidx]
    for lv in rep.get("levers", []):
        lv["evidence"] = [k for k in (lv.get("evidence") or []) if k in sigidx]
        cell = next((o for o in out + out_nb if "%s|%s" % (o["code"], o["line"]) == lv.get("cell")), None)
        if cell:
            lv.update({"country": cell["country"], "line_label": cell["line_label"], "target_2026": cell["target_2026"], "commit": cell["board"]["target"], "upside": cell["board"]["upside"],
                       "commit_growth_pct": cell["board"]["growth_pct"], "upside_growth_pct": cell["board"]["upside_growth_pct"]})
    n_for = sum(1 for v in votes if v["vote"] == "for"); n_against = sum(1 for v in votes if v["vote"] == "against")
    # the largest growth the evidence supports: the chair's number (dated 2027 events with a capacity yes),
    # capped at the upside on the table; without a chair figure the upside total stands
    LR = Dc.get("largest_reachable") or {}
    reach = min(float(LR.get("eur") or totals["upside"]), totals["upside"])
    totals["reachable"] = round(reach, 2); totals["reachable_growth_pct"] = pc(reach, T["rev_2026"])
    totals["rp_reachable"] = round(totals["rp_commit"] + (totals["rp_upside"] - totals["rp_commit"]) * ((reach - totals["commit"]) / (totals["upside"] - totals["commit"]) if totals["upside"] > totals["commit"] else 0.0), 2)
    F = {"generated": datetime.date.today().isoformat(), "built_from": P["generated"], "growth_target_pct": totals["commit_growth_pct"],
         "largest_reachable_pct": totals["reachable_growth_pct"], "largest_reachable_basis": LR.get("basis", ""), "largest_reachable_cells": LR.get("cells", []),
         "totals": totals, "by_country": by_country, "by_line": by_line, "cells": out, "new_business": out_nb,
         "new_business_unpriced": [{"code": e["code"], "country": e["country"], "line": e["line"], "line_label": e["line_label"], "n_opps": e["n_opps"], "keys": [u["key"] for u in e["opportunities"]]}
                                   for e in P.get("new_business", []) if "%s|%s" % (e["code"], e["line"]) not in {"%s|%s" % (o["code"], o["line"]) for o in out_nb}],
         "model_parts": P.get("parts"), "branch_rule": (P.get("method") or {}).get("branches", ""), "footprint_rule": (P.get("method") or {}).get("footprint_wide", ""),
         "report": rep, "votes": votes, "vote_count": {"for": n_for, "against": n_against},
         "minority_report": "\n\n".join(v["minority_report"] for v in votes if v.get("minority_report")),
         "seats": [{"seat": s, **{k: v for k, v in SEATS[s].items() if k in ("title", "camp", "votes")}} for s in SEATS],
         "disputes_decided": len(decisions), "log": log}
    save(os.path.join(root, "budget", "budget_2027_board.json"), F)
    write_decision_md(F, os.path.join(root, "budget", "BOARD_2027_DECISION.md"))
    print("board file written: commit %s (%+.1f%%), floor %s (%+.1f%%), largest reachable on the evidence %s (%+.1f%%), upside on the table %s (%+.1f%%); votes %d for, %d against" % (
        m(totals["commit"]), totals["commit_growth_pct"], m(totals["floor"]), totals["floor_growth_pct"], m(totals["reachable"]), totals["reachable_growth_pct"], m(totals["upside"]), totals["upside_growth_pct"], n_for, n_against))
    for l in log:
        print("  note:", l)


def write_decision_md(F, path):
    T, rep = F["totals"], F["report"]
    L = ["# Budget 2027: the board's decision", "",
         "Decided %s on the dashboard build of %s. Prepared by the budget board agents; every figure traces to the board packet." % (F["generated"], F["built_from"]), "",
         "## The numbers", "",
         "| | 2027 | Growth on 2026 | Profit at held margins |", "|---|---|---|---|",
         "| Floor | %s | %+.1f%% | %s |" % (m(T["floor"]), T["floor_growth_pct"], m(T["rp_floor"])),
         "| **Budget (commit)** | **%s** | **%+.1f%%** | %s |" % (m(T["commit"]), T["commit_growth_pct"], m(T["rp_commit"])),
         "| Largest reachable on the evidence | %s | %+.1f%% | %s |" % (m(T["reachable"]), T["reachable_growth_pct"], m(T["rp_reachable"])),
         "| Upside on the table (every seat's highest number) | %s | %+.1f%% | %s |" % (m(T["upside"]), T["upside_growth_pct"], m(T["rp_upside"])), "",
         ("Vote: %d for, %d against." % (F["vote_count"]["for"], F["vote_count"]["against"])) if F.get("vote_count") else "", ""]
    if F.get("largest_reachable_basis"):
        L += ["How the largest reachable figure is built: " + F["largest_reachable_basis"], ""]
    q = T.get("parts") or {}
    if q:
        L += ["## Where the budget's growth comes from", "", "| Part | EUR m |", "|---|---|",
              "| Named deals in the signals, net of the competitor threat | %.2f |" % (q["named_deals_net"] / 1e6),
              "| Market outlook (patterns and signals readings) | %.2f |" % (q["market_outlook"] / 1e6),
              "| Recurring revenue | %.2f |" % (q["recurring"] / 1e6),
              "| New business (no 2026 budget) | %.2f |" % (q["new_business"] / 1e6), ""]
    if F.get("new_business"):
        L += ["## New business the board priced", "", "| Country × product | Budget | Largest reachable | Proposed by |", "|---|---|---|---|"]
        for o in sorted(F["new_business"], key=lambda o: -o["board"]["target"]):
            L.append("| %s × %s | %s | %s | %s |" % (o["country"], o["line_label"], m(o["board"]["target"]), m(o["board"]["upside"]), o["board"]["proposer_title"]))
        L.append("")
    if rep.get("headline"):
        L += ["## " + rep["headline"], ""]
    for sec in rep.get("sections", []):
        L += ["### " + sec.get("title", ""), "", sec.get("text", ""), ""]
        if sec.get("evidence"):
            L.append("Evidence: " + ", ".join("`%s`" % k for k in sec["evidence"]))
            L.append("")
    if rep.get("levers"):
        L += ["## The levers behind the largest reachable growth", ""]
        for lv in rep["levers"]:
            L.append("- **%s × %s**: %s to %s committed, %s reachable. %s Evidence: %s" % (
                lv.get("country"), lv.get("line_label"), m(lv.get("target_2026", 0)), m(lv.get("commit", 0)), m(lv.get("upside", 0)), lv.get("why", ""), ", ".join("`%s`" % k for k in lv.get("evidence", []))))
        L.append("")
    if rep.get("conditions"):
        L += ["## Conditions attached to the budget", ""] + ["- " + x for x in rep["conditions"]] + [""]
    if rep.get("change_our_mind"):
        L += ["## What would change our mind", ""] + ["- " + x for x in rep["change_our_mind"]] + [""]
    L += ["## By country", "", "| Country | 2026 | Floor | Budget | Budget % | Largest reachable | % |", "|---|---|---|---|---|---|---|"]
    for c in F["by_country"]:
        L.append("| %s | %.1f | %.1f | %.1f | %+.1f%% | %.1f | %+.1f%% |" % (c["country"], c["rev_2026"] / 1e6, c["floor"] / 1e6, c["commit"] / 1e6, c["commit_growth_pct"], c["upside"] / 1e6, c["upside_growth_pct"]))
    L += ["", "## By product line", "", "| Line | 2026 | Floor | Budget | Budget % | Largest reachable | % |", "|---|---|---|---|---|---|---|"]
    for l in F["by_line"]:
        L.append("| %s | %.1f | %.1f | %.1f | %s | %.1f | %s |" % (l["line_label"], l["rev_2026"] / 1e6, l["floor"] / 1e6, l["commit"] / 1e6,
                 ("%+.1f%%" % l["commit_growth_pct"]) if l.get("commit_growth_pct") is not None else "new", l["upside"] / 1e6,
                 ("%+.1f%%" % l["upside_growth_pct"]) if l.get("upside_growth_pct") is not None else "new"))
    if F.get("votes"):
        L += ["", "## Votes", ""]
        for v in F["votes"]:
            L.append("- %s (%s): **%s**. %s" % (v["title"], v["camp"], v["vote"], v["reason"]))
    if F.get("minority_report"):
        L += ["", "## Minority report", "", F["minority_report"]]
    if F.get("dissent_views"):
        L += ["", "## The views that would set a lower number", ""] + ["- **%s**: %s %s" % (v["title"], v.get("reason", ""), v.get("text", "")) for v in F["dissent_views"]]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


# ------------------------------------------------------------------ publicize ---------------------
VIEW = {"cco": "Commercial view", "atm": "ATM line view", "pos": "POS line view", "services": "Services view",
        "core": "Core-markets view", "growthm": "Growth-markets view", "east": "East-and-central view",
        "cfo": "Finance view", "cro": "Risk view", "ned": "Outside view", "chair": "The review",
        "model": "The model", "ops": "Delivery check", "analyst": "Analysis"}


def cmd_publicize(root):
    """Replace every board-voiced text in budget_2027_board.json with the neutral third-person version in
    round4/texts_public.json, map seats to views, and drop the votes. The readers asked (14/09/2026) for no
    reference to the agent board while keeping every explanation. The internal file is kept beside it."""
    bdir = os.path.join(root, "budget")
    F = load(os.path.join(bdir, "budget_2027_board.json"))
    TP = load(os.path.join(bdir, "board", "round4", "texts_public.json"))
    if not (F and TP):
        sys.exit("need budget/budget_2027_board.json and budget/board/round4/texts_public.json")
    save(os.path.join(bdir, "budget_2027_board.internal.json"), F)
    R = F["report"]
    for k in ("headline", "executive_summary_md", "conditions", "change_our_mind"):
        if k in TP:
            R[k] = TP[k]
    R.pop("executive_summary", None)
    if "sections" in TP and len(TP["sections"]) == len(R["sections"]):
        for a, b in zip(R["sections"], TP["sections"]):
            a["title"], a["text"] = b["title"], b["text"]
    if "levers" in TP:
        why = {l["cell"]: l["why"] for l in TP["levers"]}
        for l in R["levers"]:
            if l["cell"] in why:
                l["why"] = why[l["cell"]]
    if TP.get("largest_reachable_basis"):
        F["largest_reachable_basis"] = TP["largest_reachable_basis"]
    cells = {c["cell"]: c for c in TP.get("cells", [])}
    n = 0
    for o in F["cells"] + F["new_business"]:
        b = o["board"]; t = cells.get("%s|%s" % (o["code"], o["line"]))
        b["proposer_title"] = VIEW.get(b["proposer"], b["proposer_title"])
        if not t:
            continue
        n += 1
        b["reason"] = t.get("reason", b["reason"]); b["chair_reason"] = t.get("chair_reason", b["chair_reason"])
        if b.get("dissent"):
            b["dissent"]["reason"] = t.get("dissent_reason") or b["dissent"]["reason"]
            b["dissent"]["view"] = VIEW.get(b["dissent"]["seat"], b["dissent"]["seat"])
        if b.get("capacity") and t.get("capacity_reason"):
            b["capacity"]["reason"] = t["capacity_reason"]
        for a, txt in zip(b.get("assumptions", []), t.get("assumptions", [])):
            a["text"] = txt
        if t.get("conditions") and len(t["conditions"]) == len(b.get("conditions", [])):
            b["conditions"] = t["conditions"]
    F["seats"] = [{"seat": x["seat"], "title": VIEW.get(x["seat"], x["title"]), "camp": x["camp"], "votes": x["votes"]} for x in F["seats"]]
    F["dissent_views"] = [{"title": d.get("title") or VIEW.get(d.get("seat"), d.get("seat")), "reason": d.get("reason", ""), "text": d.get("minority_report", "")} for d in TP.get("dissent", [])]
    F["n_views"] = len([v for v in F.get("votes", [])]); F["n_lower_views"] = len(F["dissent_views"])
    F.pop("votes", None); F.pop("vote_count", None); F.pop("minority_report", None)
    F["public"] = True
    save(os.path.join(bdir, "budget_2027_board.json"), F)
    print("public board file written: %d cell texts replaced, %d lower views, seats mapped to views" % (n, len(F["dissent_views"])))


# ------------------------------------------------------------------ mandate -----------------------
def cmd_mandate(root):
    """The third sitting (the Chairman's mandate): validate the chair's decision, sum the actions and write
    budget/budget_2027_mandate.json for the dashboard plus budget/BUDGET_2027_MANDATE.md."""
    bdir = os.path.join(root, "budget")
    F = load(os.path.join(bdir, "budget_2027_board.json"))
    P = load(os.path.join(bdir, "budget_2027.json"))
    Dc = load(os.path.join(bdir, "board", "mandate", "decision.json"))
    sigidx = load(os.path.join(bdir, "board", "packet", "signals_index.json"))
    if not (F and P and Dc):
        sys.exit("need budget_2027_board.json, budget_2027.json and board/mandate/decision.json")
    cells = {"%s|%s" % (o["code"], o["line"]): o for o in F["cells"] + F["new_business"]}
    nbmeta = {"%s|%s" % (e["code"], e["line"]): e for e in P.get("new_business", [])}
    name = {c["code"]: c["country"] for c in P["by_country"]}; label = {l["line"]: l["line_label"] for l in P["by_line"]}
    for k, v in (D_ := load(os.path.join(root, "intel-cache", "dashboard-data.json")) or {}).get("prod_label", {}).items():
        label.setdefault(k, v)
    log = []
    def cellinfo(k):
        if k in cells:
            o = cells[k]; return o["country"], o["line_label"], o["board"]["floor"], o["board"]["target"], o["board"]["upside"], bool(o.get("new_business"))
        if k in nbmeta:
            e = nbmeta[k]; return e["country"], e["line_label"], 0.0, 0.0, 0.0, True
        cc, ln = (k.split("|") + [""])[:2]
        return name.get(cc, cc), label.get(ln, ln), 0.0, 0.0, 0.0, True
    actions = []
    for a in Dc.get("actions", []):
        k = a.get("cell", "")
        if "|" not in k:
            log.append("action without a cell dropped: %s" % a.get("what", "")[:60]); continue
        cc, ll, fl, tg, up, nb = cellinfo(k)
        ev = [x for x in (a.get("evidence") or ([a["deal"]] if a.get("deal") else [])) if x in sigidx]
        if a.get("deal") and a["deal"] not in sigidx:
            log.append("deal key not in the packet on %s: %s" % (k, a["deal"]))
        actions.append({"cell": k, "code": k.split("|")[0], "line": k.split("|")[1], "country": cc, "line_label": ll, "new_business": nb,
                        "what": a.get("what", ""), "kind": a.get("kind", ""), "deal": a.get("deal", "") if a.get("deal") in sigidx else "",
                        "deal_title": sigidx.get(a.get("deal", ""), {}).get("title", ""), "by": a.get("by", ""), "owner": a.get("owner", ""),
                        "eur_floor": float(a.get("eur_floor") or 0), "eur_budget": float(a.get("eur_budget") or 0), "evidence": ev,
                        "floor_now": fl, "budget_now": tg, "upside_now": up})
    actions.sort(key=lambda a: -(a["eur_floor"] + a["eur_budget"]))
    def agg(key):
        d = defaultdict(lambda: {"eur_floor": 0.0, "eur_budget": 0.0, "n": 0})
        for a in actions:
            x = d[a[key] or "other"]; x["eur_floor"] += a["eur_floor"]; x["eur_budget"] += a["eur_budget"]; x["n"] += 1
        return sorted([{key: k, **v} for k, v in d.items()], key=lambda r: -(r["eur_floor"] + r["eur_budget"]))
    T = F["totals"]
    # the ladder may come as a list of steps or as a dict keyed by step id
    LABEL = {"floor_today": "Floor today", "floor_dd": "Floor, double digits", "budget": "Budget", "maximum": "Maximum on the table"}
    raw = Dc.get("ladder") or []
    steps = [dict(v, step=k) for k, v in raw.items()] if isinstance(raw, dict) else raw
    order = {k: i for i, k in enumerate(LABEL)}
    steps.sort(key=lambda st: order.get(st.get("step", ""), 99))
    ladder = []
    for st in steps:
        e = float(st.get("eur") or 0)
        ladder.append({"step": st.get("step", ""), "label": st.get("label") or LABEL.get(st.get("step", ""), st.get("step", "")), "eur": e,
                       "pct": pc(e, T["rev_2026"]) if e else None, "by": st.get("by") or st.get("date", ""), "conditions": st.get("conditions") or [],
                       "text": st.get("text", ""), "meets_double_digit": st.get("meets_double_digit"), "shortfall_eur": st.get("shortfall_eur"),
                       "gap_closers": st.get("gap_closers") or [], "reached_by": st.get("reached_by") or []})
    rawd = Dc.get("delivery_ask") or []
    da = rawd.get("entries", []) if isinstance(rawd, dict) else rawd
    da_summary = {k: v for k, v in rawd.items() if k != "entries"} if isinstance(rawd, dict) else {}
    for d in da:
        d["cost_eur"] = float(d.get("cost_eur") or 0); d["eur_at_stake"] = float(d.get("eur_at_stake") or 0)
    steps_out = []
    for x in Dc.get("next_steps") or []:
        steps_out.append(("%s (by %s)" % (x.get("step", ""), x.get("by"))) if isinstance(x, dict) and x.get("by") else (x.get("step", "") if isinstance(x, dict) else str(x)))
    M = {"generated": datetime.date.today().isoformat(), "built_from": F.get("built_from"), "base_2026": T["rev_2026"],
         "double_digit_floor": round(T["rev_2026"] * 1.10, 2),
         "floor_now": T["floor"], "budget_now": T["commit"], "reachable_now": T.get("reachable"), "upside_now": T["upside"],
         "headline": Dc.get("headline", ""), "onepager_md": Dc.get("onepager_md", ""),
         "ladder": ladder, "focus": Dc.get("focus") or {}, "actions": actions,
         "actions_by_kind": agg("kind"), "actions_by_country": agg("country"), "actions_by_owner": agg("owner"),
         "totals": {"eur_floor": round(sum(a["eur_floor"] for a in actions), 2), "eur_budget": round(sum(a["eur_budget"] for a in actions), 2), "n_actions": len(actions),
                    "delivery_cost_budget": round(sum(d["cost_eur"] for d in da if d.get("for") == "budget"), 2),
                    "delivery_cost_maximum": round(sum(d["cost_eur"] for d in da if d.get("for") == "maximum"), 2)},
         "capability": Dc.get("capability") or [], "delivery_ask": da, "restructuring": Dc.get("restructuring", ""),
         "delivery_summary": da_summary, "view_conditions": Dc.get("sceptic_conditions") or Dc.get("view_conditions") or [], "next_steps": steps_out, "log": log}
    save(os.path.join(bdir, "budget_2027_mandate.json"), M)
    L = ["# Budget 2027: the Chairman's mandate", "", "Prepared %s on the model build of %s." % (M["generated"], M["built_from"]), "",
         "## The ladder", "", "| Step | 2027 | Growth | By | Conditions |", "|---|---|---|---|---|"]
    for st in ladder:
        L.append("| %s | %s | %s | %s | %s |" % (st["label"], m(st["eur"]) if st["eur"] else "-", ("%+.1f%%" % st["pct"]) if st["pct"] is not None else "-", st["by"], "; ".join(st["conditions"])))
    L += ["", Dc.get("onepager_md", ""), "", "## The actions (%d, %s to the floor, %s to the budget)" % (len(actions), m(M["totals"]["eur_floor"]), m(M["totals"]["eur_budget"])), "",
          "| Cell | Action | Kind | By | Owner | Floor EUR m | Budget EUR m |", "|---|---|---|---|---|---|---|"]
    for a in actions:
        L.append("| %s x %s | %s | %s | %s | %s | %.2f | %.2f |" % (a["country"], a["line_label"], a["what"], a["kind"], a["by"], a["owner"], a["eur_floor"] / 1e6, a["eur_budget"] / 1e6))
    if da:
        L += ["", "## The delivery ask", "", "| Country | Lines | People | Skills | By | Cost EUR m | At stake EUR m | Case |", "|---|---|---|---|---|---|---|---|"]
        for d in da:
            L.append("| %s | %s | %s | %s | %s | %.2f | %.2f | %s |" % (d.get("country"), ", ".join(d.get("lines") or []), d.get("people"), d.get("skills"), d.get("by"), d["cost_eur"] / 1e6, d["eur_at_stake"] / 1e6, d.get("for")))
    if M["restructuring"]:
        L += ["", "## What the restructuring should give delivery", "", M["restructuring"]]
    with open(os.path.join(bdir, "BUDGET_2027_MANDATE.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("mandate file written: %d actions, %s to the floor, %s to the budget; ladder %s" % (len(actions), m(M["totals"]["eur_floor"]), m(M["totals"]["eur_budget"]), ", ".join("%s %s" % (st["label"], m(st["eur"])) for st in ladder)))
    for l in log:
        print("  note:", l)


# ------------------------------------------------------------------ plan --------------------------
GAP_CLOSERS = {"RO|atm_recycling": 1300000.0, "GR|atm_recycling": 900000.0, "BG|atm_recycling": 840000.0}   # the three facts (15/09/2026)


def cmd_plan(root, phase):
    """Make the plan's numbers the tab's numbers (decision of 15/09/2026): every cell's floor, budget and
    maximum become its current number plus the euros of the plan's actions, the three facts that close the
    gap to a double-digit floor are added to the floor, and the reviewed numbers are kept per cell as
    "today's evidence". Phase "numbers" writes budget/board/plan/numbers.json and a brief for the writer;
    phase "texts" merges budget/board/plan/texts_plan.json into the final budget/budget_2027_board.json."""
    bdir = os.path.join(root, "budget"); pdir = os.path.join(bdir, "board", "plan")
    F = load(os.path.join(bdir, "budget_2027_board.today.json")) or load(os.path.join(bdir, "budget_2027_board.json"))
    M = load(os.path.join(bdir, "budget_2027_mandate.json"))
    P = load(os.path.join(bdir, "budget_2027.json"))
    if not (F and M and P):
        sys.exit("need budget_2027_board.json, budget_2027_mandate.json and budget_2027.json")
    if not os.path.exists(os.path.join(bdir, "budget_2027_board.today.json")):
        save(os.path.join(bdir, "budget_2027_board.today.json"), F)     # the reviewed numbers, kept once
    F = json.loads(json.dumps(F))
    acts = defaultdict(list)
    for a in M["actions"]:
        acts[a["cell"]].append(a)
    known = {"%s|%s" % (o["code"], o["line"]) for o in F["cells"] + F["new_business"]}
    # new-business combinations the plan opens that are not in the file yet
    cmargin = {c["code"]: (c["rp_2026"] / c["rev_2026"] * 100 if c["rev_2026"] else 0.0) for c in P["by_country"]}
    name = {c["code"]: c["country"] for c in P["by_country"]}
    label = {l["line"]: l["line_label"] for l in P["by_line"]}
    for k, v in (load(os.path.join(root, "intel-cache", "dashboard-data.json")) or {}).get("prod_label", {}).items():
        label.setdefault(k, v)
    # maximum-case new business the delivery ask reverses: euros at stake per cell, for cells with no plan budget
    max_nb = defaultdict(float)
    for d in M.get("delivery_ask", []):
        if d.get("for") == "maximum":
            for k in d.get("cells") or []:
                max_nb[k] += d.get("eur_at_stake", 0.0) / max(1, len(d.get("cells") or []))
    for k in list(acts) + [k for k in max_nb if k not in acts]:
        if k not in known and "|" in k:
            cc, ln = k.split("|")
            known.add(k)
            F["new_business"].append({"code": cc, "country": name.get(cc, cc), "line": ln, "line_label": label.get(ln, ln), "target_2026": 0.0, "base": 0.0, "stretch": 0.0, "new_business": True,
                                      "board": {"target": 0.0, "floor": 0.0, "upside": 0.0, "parts": {"market_outlook": 0.0, "recurring": 0.0, "named_deals_net": 0.0, "case": "new"},
                                                "growth_pct": None, "floor_growth_pct": None, "upside_growth_pct": None, "new": 0.0, "recurring": 0.0, "rp": 0.0,
                                                "margin_pct": round(cmargin.get(cc, 0.0), 1), "proposer": "plan", "proposer_title": "The plan", "reason": "", "evidence": [],
                                                "conditions": [], "assumptions": [], "capacity": None, "capped_by_capacity": False, "dissent": None, "decided_by_chair": False, "chair_reason": "", "above_stretch": False}})
    for o in F["cells"] + F["new_business"]:
        k = "%s|%s" % (o["code"], o["line"]); b = o["board"]; A = acts.get(k, [])
        today = {"floor": b["floor"], "target": b["target"], "upside": b["upside"], "reason": b.get("reason", ""), "proposer_title": b.get("proposer_title", "")}
        fl = b["floor"] + sum(a["eur_floor"] for a in A) + GAP_CLOSERS.get(k, 0.0)
        tg = b["target"] + sum(a["eur_budget"] for a in A)
        tg = max(tg, fl)
        up = max(b["upside"], tg)
        if o.get("new_business") and tg <= 0 and max_nb.get(k):
            up = max(up, max_nb[k])
        ratio = tg / b["target"] if b["target"] else 1.0
        b.update({"today": today, "floor": round(fl, 2), "target": round(tg, 2), "upside": round(up, 2),
                  "growth_pct": pc(tg, o["target_2026"]) if o["target_2026"] else None, "floor_growth_pct": pc(fl, o["target_2026"]) if o["target_2026"] else None,
                  "upside_growth_pct": pc(up, o["target_2026"]) if o["target_2026"] else None,
                  "new": round((b.get("new") or 0) * ratio if b["target"] else tg, 2), "recurring": round((b.get("recurring") or 0) * ratio if b["target"] else 0.0, 2),
                  "rp": round(tg * b["margin_pct"] / 100.0, 2),
                  "plan_actions": [{"what": a["what"], "kind": a["kind"], "by": a["by"], "owner": a["owner"], "eur_floor": a["eur_floor"], "eur_budget": a["eur_budget"],
                                    "deal": a.get("deal", ""), "deal_title": a.get("deal_title", ""), "evidence": a.get("evidence", [])} for a in A],
                  "gap_closer_eur": GAP_CLOSERS.get(k, 0.0), "plan_floor_delta": round(fl - today["floor"], 2), "plan_budget_delta": round(tg - today["target"], 2)})
        if o.get("new_business"):
            b["parts"] = {"market_outlook": 0.0, "recurring": 0.0, "named_deals_net": round(tg, 2), "case": "new"}
        b["evidence"] = list(dict.fromkeys(b.get("evidence", []) + [e for a in A for e in a.get("evidence", [])]))
    # totals and breakdowns: covered cells plus the flat lines, anchored on the model's flat part as before
    T = F["totals"]; unc = T["commit_existing"] - sum(o["board"]["today"]["target"] for o in F["cells"])
    cells_all = F["cells"] + F["new_business"]
    def tot(key): return sum(o["board"][key] for o in cells_all) + unc
    def rp(key): return sum(o["board"][key] * o["board"]["margin_pct"] / 100.0 for o in cells_all) + (T["rp_2026"] - sum(c["rp_2026"] for c in P["cells"])) * 1.0
    today_totals = {k: T[k] for k in ("floor", "commit", "upside", "reachable", "floor_growth_pct", "commit_growth_pct", "upside_growth_pct", "reachable_growth_pct", "rp_floor", "rp_commit", "rp_upside", "rp_reachable") if k in T}
    T.update({"floor": round(tot("floor"), 2), "commit": round(tot("target"), 2), "upside": round(tot("upside"), 2),
              "rp_floor": round(rp("floor"), 2), "rp_commit": round(rp("target"), 2), "rp_upside": round(rp("upside"), 2),
              "new_business_commit": round(sum(o["board"]["target"] for o in F["new_business"]), 2), "new_business_upside": round(sum(o["board"]["upside"] for o in F["new_business"]), 2),
              "commit_existing": round(sum(o["board"]["target"] for o in F["cells"]) + unc, 2), "today": today_totals,
              "supported_today": today_totals.get("reachable"), "supported_today_growth_pct": today_totals.get("reachable_growth_pct")})
    for k in ("floor", "commit", "upside"):
        T[k + "_growth_pct"] = pc(T[k], T["rev_2026"])
    T["reachable"], T["reachable_growth_pct"], T["rp_reachable"] = T["upside"], T["upside_growth_pct"], T["rp_upside"]
    T["parts"] = {"named_deals_net": round(sum(o["board"]["parts"]["named_deals_net"] for o in F["cells"]), 2), "market_outlook": round(sum(o["board"]["parts"]["market_outlook"] for o in F["cells"]), 2),
                  "recurring": round(sum(o["board"]["parts"]["recurring"] for o in F["cells"]), 2), "new_business": T["new_business_commit"], "flat": 0.0,
                  "outlook_cells": (T.get("parts") or {}).get("outlook_cells"),
                  "plan_by_kind": M.get("actions_by_kind", []), "gap_closers": round(sum(GAP_CLOSERS.values()), 2)}
    T["parts"]["plan_actions"] = round(sum(a["eur_budget"] for a in M["actions"]), 2)
    # the named-deals part of the plan: what the actions add on top of today's split
    T["parts"]["named_deals_net"] = round(T["parts"]["named_deals_net"] + sum(a["eur_budget"] for a in M["actions"] if a["kind"] in ("date", "share", "capability", "hire") and a["cell"] in {"%s|%s" % (o["code"], o["line"]) for o in F["cells"]}), 2)
    T["parts"]["recurring"] = round(T["parts"]["recurring"] + sum(a["eur_budget"] for a in M["actions"] if a["kind"] in ("pricing", "efficiency") and a["cell"] in {"%s|%s" % (o["code"], o["line"]) for o in F["cells"]}), 2)
    by_c, by_l = defaultdict(lambda: defaultdict(float)), defaultdict(lambda: defaultdict(float))
    for o in cells_all:
        for key in ("floor", "target", "upside"):
            by_c[o["code"]][key] += o["board"][key]; by_l[o["line"]][key] += o["board"][key]
    cov_c, cov_l = defaultdict(float), defaultdict(float)
    for o in F["cells"]:
        cov_c[o["code"]] += o["board"]["today"]["target"]; cov_l[o["line"]] += o["board"]["today"]["target"]
    for c in F["by_country"]:
        flat = c["commit"] - cov_c[c["code"]] - sum(o["board"]["today"]["target"] for o in F["new_business"] if o["code"] == c["code"])
        v = by_c[c["code"]]
        c.update({"floor": round(v["floor"] + flat, 2), "commit": round(v["target"] + flat, 2), "upside": round(v["upside"] + flat, 2)})
        for key, kk in (("floor", "floor"), ("commit", "commit"), ("upside", "upside")):
            c[key + "_growth_pct"] = pc(c[kk], c["rev_2026"])
    seen = {l["line"] for l in F["by_line"]}
    for l in F["by_line"]:
        flat = l["commit"] - cov_l[l["line"]] - sum(o["board"]["today"]["target"] for o in F["new_business"] if o["line"] == l["line"])
        v = by_l[l["line"]]
        l.update({"floor": round(v["floor"] + flat, 2), "commit": round(v["target"] + flat, 2), "upside": round(v["upside"] + flat, 2)})
        for key in ("floor", "commit", "upside"):
            l[key + "_growth_pct"] = pc(l[key], l["rev_2026"])
    for ln, v in by_l.items():
        if ln not in seen and (v["target"] or v["upside"]):
            F["by_line"].append({"line": ln, "line_label": label.get(ln, ln), "rev_2026": 0.0, "base": 0.0, "stretch": 0.0, "floor": round(v["floor"], 2), "commit": round(v["target"], 2), "upside": round(v["upside"], 2),
                                 "floor_growth_pct": None, "commit_growth_pct": None, "upside_growth_pct": None})
    F["largest_reachable_cells"] = sorted({a["cell"] for a in M["actions"]} | set(GAP_CLOSERS))
    F["plan"] = {"ladder": M["ladder"], "capability": M["capability"], "delivery_ask": M["delivery_ask"], "delivery_summary": M.get("delivery_summary", {}),
                 "view_conditions": M["view_conditions"], "next_steps": M["next_steps"], "restructuring": M["restructuring"], "focus": M["focus"],
                 "actions_by_kind": M["actions_by_kind"], "n_actions": len(M["actions"]), "gap_closers": GAP_CLOSERS,
                 "delivery_cost_budget": M["totals"]["delivery_cost_budget"], "delivery_cost_maximum": M["totals"]["delivery_cost_maximum"]}
    F["generated"] = datetime.date.today().isoformat(); F["plan_based"] = True
    os.makedirs(pdir, exist_ok=True)
    if phase == "numbers":
        save(os.path.join(pdir, "numbers.json"), F)
        # a compact brief for the writer: the new numbers by line and country, and the top cells with their actions
        top = sorted(F["cells"] + F["new_business"], key=lambda o: -(o["board"]["target"] - o["board"]["today"]["target"]))[:30]
        L = ["# The 2027 plan numbers (for the writer)", "",
             "| | 2027 | Growth on 2026 (EUR %.2fm) |" % (T["rev_2026"] / 1e6), "|---|---|---|",
             "| Lowest acceptable (floor) | EUR %.2fm | %+.1f%% |" % (T["floor"] / 1e6, T["floor_growth_pct"]),
             "| 2027 budget | EUR %.2fm | %+.1f%% |" % (T["commit"] / 1e6, T["commit_growth_pct"]),
             "| Maximum on the table | EUR %.2fm | %+.1f%% |" % (T["upside"] / 1e6, T["upside_growth_pct"]),
             "| What the evidence supports today (reference) | EUR %.2fm | %+.1f%% |" % ((T["supported_today"] or 0) / 1e6, T["supported_today_growth_pct"] or 0),
             "| Reviewed budget before the plan (reference) | EUR %.2fm | %+.1f%% |" % (today_totals["commit"] / 1e6, today_totals["commit_growth_pct"]),
             "| Profit at held margins: floor / budget / maximum | EUR %.2fm / %.2fm / %.2fm | |" % (T["rp_floor"] / 1e6, T["rp_commit"] / 1e6, T["rp_upside"] / 1e6), "",
             "New business in the budget: EUR %.2fm. The three facts added to the floor: %s (EUR %.2fm together)." % (T["new_business_commit"] / 1e6, ", ".join("%s +%.2fm" % (k, v / 1e6) for k, v in GAP_CLOSERS.items()), sum(GAP_CLOSERS.values()) / 1e6), "",
             "## By product line", "", "| Line | 2026 | Floor | Budget | Budget % | Maximum |", "|---|---|---|---|---|---|"]
        for l in sorted(F["by_line"], key=lambda x: -x["commit"]):
            L.append("| %s | %.2f | %.2f | %.2f | %s | %.2f |" % (l["line_label"], l["rev_2026"] / 1e6, l["floor"] / 1e6, l["commit"] / 1e6, ("%+.1f%%" % l["commit_growth_pct"]) if l["commit_growth_pct"] is not None else "new", l["upside"] / 1e6))
        L += ["", "## By market", "", "| Market | 2026 | Floor | Budget | Budget % | Maximum |", "|---|---|---|---|---|---|"]
        for c in sorted(F["by_country"], key=lambda x: -x["commit"]):
            L.append("| %s | %.2f | %.2f | %.2f | %+.1f%% | %.2f |" % (c["country"], c["rev_2026"] / 1e6, c["floor"] / 1e6, c["commit"] / 1e6, c["commit_growth_pct"], c["upside"] / 1e6))
        L += ["", "## The thirty cells that move most (today's budget -> plan budget), with their actions", ""]
        for o in top:
            b = o["board"]
            L.append("### %s x %s: EUR %.2fm today -> floor %.2fm, budget %.2fm, maximum %.2fm" % (o["country"], o["line_label"], b["today"]["target"] / 1e6, b["floor"] / 1e6, b["target"] / 1e6, b["upside"] / 1e6))
            for a in b["plan_actions"]:
                L.append("- [%s, by %s, %s, +%.2fm budget] %s%s" % (a["kind"], a["by"], a["owner"], a["eur_budget"] / 1e6, a["what"], (" (" + a["deal_title"] + ")") if a["deal_title"] else ""))
            if b.get("gap_closer_eur"):
                L.append("- [fact added to the floor, +%.2fm] one of the three facts that close the gap to a double-digit floor" % (b["gap_closer_eur"] / 1e6))
            L.append("")
        with open(os.path.join(pdir, "NUMBERS_BRIEF.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(L))
        print("plan numbers: floor %s (%+.1f%%), budget %s (%+.1f%%), maximum %s (%+.1f%%); supported today %s; new cells %d" % (
            m(T["floor"]), T["floor_growth_pct"], m(T["commit"]), T["commit_growth_pct"], m(T["upside"]), T["upside_growth_pct"], m(T["supported_today"] or 0), len(F["new_business"])))
        return
    TP = load(os.path.join(pdir, "texts_plan.json"))
    if not TP:
        sys.exit("phase texts needs budget/board/plan/texts_plan.json")
    R = F["report"]
    for k in ("headline", "executive_summary_md", "conditions", "change_our_mind", "sections", "levers"):
        if k in TP:
            R[k] = TP[k]
    sigidx = load(os.path.join(bdir, "board", "packet", "signals_index.json")) or {}
    for sec in R.get("sections", []):
        sec["evidence"] = [k for k in (sec.get("evidence") or []) if k in sigidx]
    cellmap = {"%s|%s" % (o["code"], o["line"]): o for o in F["cells"] + F["new_business"]}
    for lv in R.get("levers", []):
        lv["evidence"] = [k for k in (lv.get("evidence") or []) if k in sigidx]
        o = cellmap.get(lv.get("cell"))
        if o:
            lv.update({"country": o["country"], "line_label": o["line_label"], "target_2026": o["target_2026"], "commit": o["board"]["target"], "upside": o["board"]["upside"],
                       "commit_growth_pct": o["board"]["growth_pct"], "upside_growth_pct": o["board"]["upside_growth_pct"]})
    if TP.get("largest_reachable_basis"):
        F["largest_reachable_basis"] = TP["largest_reachable_basis"]
    if TP.get("dissent_views"):
        F["dissent_views"] = TP["dissent_views"]
    cells_t = {c["cell"]: c for c in TP.get("cells", [])}
    n = 0
    for o in F["cells"] + F["new_business"]:
        t = cells_t.get("%s|%s" % (o["code"], o["line"]))
        if t and t.get("reason"):
            o["board"]["reason"] = t["reason"]; o["board"]["proposer_title"] = t.get("set_by", "The plan"); n += 1
    save(os.path.join(bdir, "budget_2027_board.json"), F)
    write_decision_md(F, os.path.join(bdir, "BUDGET_2027_PLAN.md"))
    print("plan board file written: %d cell texts, floor %s, budget %s, maximum %s" % (n, m(T["floor"]), m(T["commit"]), m(T["upside"])))


# ---------------------------------------------------------------------------------------------------
# target: the budget set at the maximum on the table, no floor, no hires (decision of 17/09/2026)
# ---------------------------------------------------------------------------------------------------
ADJ_NAMES = {"Albania", "Bosnia & Herzegovina", "Bosnia", "Bulgaria", "Croatia", "Cyprus", "Greece", "Hungary", "Kosovo", "Montenegro", "North Macedonia", "Romania", "Serbia", "Slovakia", "Slovenia", "Ukraine", "Czech Republic"}
ADJ = {"AL": "Albanian", "BA": "Bosnian", "BG": "Bulgarian", "HR": "Croatian", "CY": "Cypriot", "GR": "Greek", "HU": "Hungarian", "XK": "Kosovar",
       "ME": "Montenegrin", "MK": "North Macedonian", "RO": "Romanian", "RS": "Serbian", "SK": "Slovak", "SI": "Slovenian", "UA": "Ukrainian", "CZ": "Czech"}
TARGET_BANNED = ["floor", "lowest acceptable", "closing fact", "double digit", "double-digit", "hire", "hiring", "delivery ask", "delivery cost",
                 "174.32", "163.76", "163.8", "174.3", "179.99", "maximum on the table", "board", "chair", "mandate", "seat", "vote", "sceptic"]

def _owner(o, cc):
    if o.startswith("sales "):
        return "%s sales" % ADJ.get(o.split()[1], o.split()[1])
    return {"group": "the group", "delivery": "delivery", "finance": "finance", "partner": "a partner", "services": "services"}.get(o, o)

def _date(d):
    mm = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", str(d or ""))
    if not mm:
        return str(d or "")
    MO = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return "%d %s %s" % (int(mm.group(3)), MO[int(mm.group(2)) - 1], mm.group(1))

def _act_phrase(a, cc):
    title = a.get("deal_title") or ""
    who = title.split(" — ")[0].split(" - ")[0].strip()
    on = False
    if who in ADJ_NAMES or len(who) < 3:
        who = title.strip().replace(" — ", ", ").replace(" – ", ", "); on = True
    what = a.get("what", "").strip().rstrip(".")
    what = re.split(r";|\.\s", what)[0]
    if len(what) > 120:
        what = what[:120].rsplit(" ", 1)[0] + "…"
    if a["kind"] == "date":
        head = ("a dated 2027 order or tender %s %s" % ("on" if on else "at", who)) if who and len(who) > 2 else "a dated 2027 order (%s)" % what[:90]
    elif a["kind"] == "share":
        head = ("a share win %s %s" % ("on" if on else "at", who)) if who and len(who) > 2 else "a share win (%s)" % what[:90]
    elif a["kind"] == "capability":
        head = "a capability decision (%s)" % (what[0].lower() + what[1:])
    elif a["kind"] == "pricing":
        head = "a price step (%s)" % (what[0].lower() + what[1:])
    else:
        head = "an efficiency step (%s)" % (what[0].lower() + what[1:])
    return "%s (+EUR %.2fm, %s, by %s)" % (head, a["eur_budget"] / 1e6, _owner(a["owner"], cc), _date(a["by"]))

def _view(title):
    v = (title or "the review").strip()
    low = lambda x: (x[0].lower() + x[1:]) if len(x) > 1 and x[1].islower() else x
    if v.lower().startswith("the "): return low(v)
    return "the " + low(v)

def _reason(o):
    """The cell's explanation with the budget as the only 2027 number (no reviewed, model or lower figures)."""
    b = o["board"]; cc = o["code"]; t = b.get("today") or {}
    A = sorted(b.get("plan_actions", []), key=lambda a: -a["eur_budget"])
    main = [a for a in A if a["kind"] in ("date", "share", "capability")]
    supp = [a for a in A if a["kind"] in ("pricing", "efficiency")]
    staff = b.get("staffing") or []
    parts = []
    if o.get("new_business"):
        parts.append("This is a combination with no 2026 budget. The 2027 budget for it is EUR %.2fm." % (b["target"] / 1e6))
    else:
        parts.append("Against a 2026 target of EUR %.2fm, the 2027 budget for this line is EUR %.2fm%s." % (o["target_2026"] / 1e6, b["target"] / 1e6, (" (%+.1f%%)" % b["growth_pct"]) if b.get("growth_pct") is not None else ""))
    if A:
        tot = sum(a["eur_budget"] for a in A) / 1e6
        if main:
            parts.append("The plan's %d action%s carry EUR %.2fm of it, led by %s." % (len(A), "" if len(A) == 1 else "s", tot, "; ".join(_act_phrase(a, cc) for a in main[:4])))
            if supp:
                parts.append("The supporting step%s: %s." % ("s are" if len(supp) > 1 else " is", "; ".join(_act_phrase(a, cc) for a in supp[:3])))
        else:
            parts.append("The plan's %d action%s carry EUR %.2fm of it: %s." % (len(A), "" if len(A) == 1 else "s", tot, "; ".join(_act_phrase(a, cc) for a in supp[:3])))
    extra = b["target"] - ((t.get("target") or 0) + sum(a["eur_budget"] for a in A) + sum(a["eur_budget"] for a in staff))
    if extra > 5000 and o.get("new_business"):
        parts.append("EUR %.2fm of it is new business that the capability decisions open." % (extra / 1e6))
    elif extra > 5000:
        parts.append("A further EUR %.2fm is the highest estimate the evidence carries for this line." % (extra / 1e6))
    return " ".join(parts)

ONLY_PAT = re.compile(r"165\.09|156\.22|8\.87m|reviewed|supports today|already supports|evidence supports|base case|stretch case|model.s stretch|model.s base|lower number", re.I)

def _only_target_text(t):
    """Remove every reference to a 2027 number other than the budget (decision of 17/09/2026: EUR 180.0m is the one number)."""
    if not isinstance(t, str):
        return t
    t = re.sub(r",? while the evidence already supports EUR [\d.]+m today", "", t)
    t = re.sub(r" to the reviewed budget( of EUR [\d.]+m)?", "", t)
    t = re.sub(r", up from EUR [\d.]+m in the reviewed budget", "", t)
    t = t.replace("from the reviewed number to the highest estimate", "to the highest estimate")
    t = t.replace("The plan removes those objections cell by cell with", "The plan works cell by cell with")
    t = re.sub(r"would set a lower number than EUR 180\.0m until", "supports EUR 180.0m once", t)
    t = re.sub(r"The highest estimate of EUR [\d,.]+m? needs", "The budget needs", t)
    out = []
    for para in t.split("\n\n"):
        sents = re.split(r"(?<=[.])\s+(?=[A-Z*])", para)
        kept = [x for x in sents if not ONLY_PAT.search(x)]
        if kept:
            out.append(" ".join(kept))
    return "\n\n".join(out)

def _drivers(F, sigidx):
    """The four drivers of the growth, for the opening of the executive report: amount, share, one plain sentence on
    what it is, one on what proves it, what is inside (so price and efficiency steps, share wins and capability
    decisions are visibly counted once), the largest names and the signals behind them. All computed from the file."""
    T = F["totals"]; growth = T["commit"] - T["rev_2026"]
    ex, nb = F["cells"], F["new_business"]
    def kinds(cells):
        d = defaultdict(lambda: [0, 0.0])
        for o in cells:
            for a in o["board"].get("plan_actions", []):
                d[a["kind"]][0] += 1; d[a["kind"]][1] += a["eur_budget"]
            for a in o["board"].get("staffing", []):
                d["staffing"][0] += 1; d["staffing"][1] += a["eur_budget"]
        return d
    ke, kn = kinds(ex), kinds(nb)
    model = {k: sum((o["board"].get("parts") or {}).get(k, 0.0) or 0.0 for o in ex) for k in ("named_deals_net", "market_outlook", "recurring")}
    P = T["parts"]
    A26 = load(os.path.join(F.get("_root", ""), "budget", "budget_actions.json")) if F.get("_root") else None
    base_new = ((A26 or {}).get("totals") or {}).get("new") or 0.0
    base_rec = ((A26 or {}).get("totals") or {}).get("recurring") or 0.0
    base_cov = ((A26 or {}).get("totals") or {}).get("covered") or 0.0
    def top_deals(cells, n=5):
        d = defaultdict(lambda: [0.0, ""])
        for o in cells:
            for a in o["board"].get("plan_actions", []):
                if a["kind"] in ("date", "share") and a.get("deal_title"):
                    nm = a["deal_title"].split(" — ")[0].strip()
                    if nm in ADJ_NAMES: continue
                    d[nm][0] += a["eur_budget"]; d[nm][1] = d[nm][1] or a.get("deal", "")
        rows = sorted(d.items(), key=lambda x: -x[1][0])[:n]
        return [{"name": k, "eur": round(v[0], 2)} for k, v in rows], [v[1] for k, v in rows if v[1] in sigidx]
    names_e, ev_e = top_deals(ex); names_n, ev_n = top_deals(nb, 4)
    oc = P.get("outlook_cells") or {}
    with_reading = (oc.get("patterns_and_signals") or 0) + (oc.get("signals_only") or 0) + (oc.get("patterns_only") or 0); no_reading = oc.get("none") or 0
    by_line = defaultdict(float)
    for o in nb: by_line[o["line_label"]] += o["board"]["target"]
    nb_lines = sorted(by_line.items(), key=lambda x: -x[1])[:4]
    nb_actions = sum(v[1] for v in kn.values())
    nb_priced = sum(((o["board"].get("today") or {}).get("target") or 0.0) for o in nb)
    nb_opened = P["new_business"] - nb_actions - nb_priced
    M = lambda v: "EUR %.2fm" % (v / 1e6)
    # the model's recurring growth is presented inside the price and efficiency steps, split in their proportion
    # (decision 22/09/2026: the sales team is asked for price and efficiency, not for a market rate)
    _pr = sum(a["eur_budget"] for o in ex for a in o["board"].get("plan_actions", []) if a["kind"] == "pricing")
    _ef = sum(a["eur_budget"] for o in ex for a in o["board"].get("plan_actions", []) if a["kind"] == "efficiency")
    _mr = P["recurring"] - _pr - _ef
    rec_price = _pr + (_mr * _pr / (_pr + _ef) if (_pr + _ef) else _mr); rec_eff = _ef + (_mr * _ef / (_pr + _ef) if (_pr + _ef) else 0.0)
    # what the new business is: by product line, with the countries
    _nbl = defaultdict(lambda: {"eur": 0.0, "countries": set()})
    for o in nb:
        _nbl[o["line_label"]]["eur"] += o["board"]["target"]; _nbl[o["line_label"]]["countries"].add(o["country"])
    nb_rows = [{"line": k, "eur": round(v["eur"], 2), "countries": sorted(v["countries"])} for k, v in sorted(_nbl.items(), key=lambda x: -x[1]["eur"]) if v["eur"] >= 5000]
    short = lambda l: l.split(" / ")[0].split(",")[0].split(" (")[0].strip().lower().replace("atm", "ATM").replace("pos", "POS")
    D = [
        {"key": "named_deals", "title": "Named deals", "eur": round(P["named_deals_net"], 2),
         "what": "Purchases that banks and post offices have already announced: tenders, fleet programmes, mergers and dated rollouts.",
         "proof": "%d dated orders and tenders, %d share wins and %d capability decisions, each with a bank name, a date and an owner. The largest are %s." % (
             ke["date"][0], ke["share"][0], ke["capability"][0], ", ".join(x["name"] for x in names_e[:-1]) + " and " + names_e[-1]["name"] if len(names_e) > 1 else (names_e[0]["name"] if names_e else "in the table below")),
         "inside": [["Dated orders and tenders", round(ke["date"][1], 2)], ["Share taken from competitors", round(ke["share"][1], 2)], ["Capability decisions", round(ke["capability"][1], 2)],
                    ["Deals the market model already counts, after what competitors are expected to win", round(P["named_deals_net"] - ke["date"][1] - ke["share"][1] - ke["capability"][1], 2)]],
         "names": names_e, "evidence": ev_e},
        {"key": "market_outlook", "title": "Market outlook", "eur": round(P["market_outlook"], 2),
         "what": "The markets themselves grow. Where a country's ATMs, POS terminals or self-service branches grow, our sales of that line grow with them.",
         "proof": "Read from the dashboard's market readings for %d of the %d country and product lines. The other %d have no reading and count as zero. No statistical forecast is used." % (with_reading, with_reading + no_reading, no_reading),
         "inside": [], "names": [], "evidence": [], "show_rate": True, "rate_pct": round(P["market_outlook"] / base_cov * 100.0, 2) if base_cov else None, "rate_of": "2026 revenue", "base_eur": round(base_cov, 2)},
        {"key": "recurring", "title": "Recurring revenue", "eur": round(P["recurring"], 2),
         "what": "Service and outsourcing contracts we already hold, repriced at renewal and delivered at lower cost.",
         "proof": "%d price steps at renewal and %d efficiency steps, each with an owner and a date. They are counted here and nowhere else." % (ke["pricing"][0], ke["efficiency"][0]),
         "inside": [["Better pricing at renewal", round(rec_price, 2)], ["Efficiency", round(rec_eff, 2)]],
         "names": [], "evidence": [], "show_rate": True, "rate_pct": round(P["recurring"] / base_rec * 100.0, 2) if base_rec else None, "rate_of": "2026 recurring revenue", "base_eur": round(base_rec, 2)},
        {"key": "new_business", "title": "New business", "eur": round(P["new_business"], 2),
         "what": "Products we do not yet sell in a country, where the signals show banks buying.",
         "proof": "%d country and product combinations in %d countries. The largest are %s. %s of it depends on capability decisions Printec has yet to take." % (
             len(nb), len({o["code"] for o in nb}), ", ".join("%s (%s)" % (short(k), M(v)) for k, v in nb_lines), M(nb_opened + kn["capability"][1])),
         "inside": [["Business the capability decisions open", round(nb_opened + kn["capability"][1], 2)], ["Dated orders and tenders", round(kn["date"][1] + kn["share"][1], 2)],
                    ["First contracts already priced from the signals", round(nb_priced + kn["staffing"][1], 2)]],
         "lines": nb_rows, "names": names_n, "evidence": ev_n},
    ]
    for d in D:
        d["share_pct"] = round(d["eur"] / growth * 100.0, 1) if growth else 0.0
        d["inside"] = [x for x in d["inside"] if abs(x[1]) >= 5000]
    # ---- the levers: every step of the growth with the rate behind it, who owns it and by when, so the sales
    #      and delivery teams can see how each euro is reached (asked 17/09/2026) ----
    def acts_of(cells, kind):
        out = []
        for o in cells:
            src = o["board"].get("staffing", []) if kind == "staffing" else [a for a in o["board"].get("plan_actions", []) if a["kind"] == kind]
            for a in src:
                out.append(dict(a, country=o["country"], line=o["line_label"]))
        return sorted(out, key=lambda a: -a["eur_budget"])
    OWN = {"group": "the group", "finance": "finance", "delivery": "delivery", "partner": "a partner"}
    def who(L):
        c = defaultdict(int)
        for a in L:
            c["country sales teams" if a["owner"].startswith("sales ") else OWN.get(a["owner"], a["owner"])] += 1
        top = [k for k, v in sorted(c.items(), key=lambda x: -x[1])[:2]]
        return " and ".join(top)
    def when(L):
        ds = sorted(a["by"] for a in L if a.get("by"))
        if not ds: return ""
        return _date(ds[-1]) if ds[0] == ds[-1] else "%s to %s" % (_date(ds[0]), _date(ds[-1]))
    def due(L, d):
        return sum(1 for a in L if a.get("by") and a["by"] <= d)
    def example(L):
        if not L: return ""
        w = re.split(r";|\.\s", L[0]["what"].strip().rstrip("."))[0]
        return "%s: %s." % (L[0]["country"], w[:200])
    pc1 = lambda v, b: (v / b * 100.0) if b else None
    e_date, e_share, e_cap, e_staff, e_pr, e_eff = [acts_of(ex_cells, k) for ex_cells, k in ((ex, "date"), (ex, "share"), (ex, "capability"), (ex, "staffing"), (ex, "pricing"), (ex, "efficiency"))]
    n_date, n_cap, n_staff = acts_of(nb, "date") + acts_of(nb, "share"), acts_of(nb, "capability"), acts_of(nb, "staffing")
    sm = lambda L: sum(a["eur_budget"] for a in L)
    model_deals = P["named_deals_net"] - sm(e_date) - sm(e_share) - sm(e_cap) - sm(e_staff)
    base_growth = P["recurring"] - sm(e_pr) - sm(e_eff)
    LV = [
        {"driver": "named_deals", "label": "Dated orders and tenders", "eur": sm(e_date), "n": len(e_date), "rate": pc1(sm(e_date), base_new), "rate_of": "2026 hardware and software sales",
         "how": "Turn each announced purchase into a signed 2027 order by its date. %d of the %d are due by 30 June 2027." % (due(e_date, "2027-06-30"), len(e_date)), "who": who(e_date), "when": when(e_date), "example": example(e_date)},
        {"driver": "named_deals", "label": "Share taken from competitors", "eur": sm(e_share), "n": len(e_share), "rate": pc1(sm(e_share), base_new), "rate_of": "2026 hardware and software sales",
         "how": "Win estates a competitor serves today, mostly where a fleet is consolidated or re-tendered.", "who": who(e_share), "when": when(e_share), "example": example(e_share)},
        {"driver": "named_deals", "label": "Capability decisions", "eur": sm(e_cap), "n": len(e_cap), "rate": pc1(sm(e_cap), base_new), "rate_of": "2026 hardware and software sales",
         "how": "Build or certify what a tender asks for before it closes.", "who": who(e_cap), "when": when(e_cap), "example": example(e_cap)},
        {"driver": "named_deals", "label": "Deals the market model already counts", "eur": model_deals + sm(e_staff), "n": None, "rate": pc1(model_deals + sm(e_staff), base_new), "rate_of": "2026 hardware and software sales",
         "how": "Close the open opportunities at the usual rate, after what competitors are expected to win. Delivered by the existing teams.", "who": "country sales teams", "when": "through 2027", "example": ""},
        {"driver": "market_outlook", "label": "Growth of the markets", "eur": P["market_outlook"], "n": None, "rate": pc1(P["market_outlook"], base_cov), "rate_of": "2026 revenue",
         "how": "Hold our share where ATMs, POS terminals and self-service grow. No action beyond keeping the share.", "who": "country sales teams", "when": "through 2027", "example": ""},
        {"driver": "recurring", "label": "Better pricing", "eur": rec_price, "n": len(e_pr), "rate": pc1(rec_price, base_rec), "rate_of": "2026 recurring revenue",
         "how": "Take about %.1f points of price at renewal across the recurring base: the %d price steps, plus the growth of the contracts we hold as the estates grow." % (pc1(rec_price, base_rec) or 0.0, len(e_pr)), "who": who(e_pr), "when": when(e_pr), "example": example(e_pr)},
        {"driver": "recurring", "label": "Efficiency", "eur": rec_eff, "n": len(e_eff), "rate": pc1(rec_eff, base_rec), "rate_of": "2026 recurring revenue",
         "how": "Resolve more calls remotely, price on uptime instead of visits and keep every renewal: worth about %.1f%% of the recurring base." % (pc1(rec_eff, base_rec) or 0.0), "who": who(e_eff), "when": when(e_eff), "example": example(e_eff)},
        {"driver": "new_business", "label": "New business the capability decisions open", "eur": nb_opened + sm(n_cap), "n": len(n_cap) or None, "rate": None, "rate_of": "",
         "how": "Take the capability decisions first. This revenue exists only if they are taken.", "who": who(n_cap) or "the group", "when": when(n_cap), "example": example(n_cap)},
        {"driver": "new_business", "label": "New business: dated orders and tenders", "eur": sm(n_date), "n": len(n_date), "rate": None, "rate_of": "",
         "how": "First orders for products we do not yet sell in that country.", "who": who(n_date), "when": when(n_date), "example": example(n_date)},
        {"driver": "new_business", "label": "New business already priced from the signals", "eur": nb_priced + sm(n_staff), "n": None, "rate": None, "rate_of": "",
         "how": "First contracts the signals already support, priced line by line and delivered by the existing teams.", "who": "country sales teams", "when": "through 2027", "example": ""},
    ]
    LV = [dict(x, eur=round(x["eur"], 2), rate=(round(x["rate"], 2) if x["rate"] is not None else None)) for x in LV if abs(x["eur"]) >= 5000]
    # ---- every signal behind each driver, with the euros of the actions that rest on it (an action's euros go to
    #      its deal signal, or are split equally across its evidence keys); the market outlook lists readings ----
    def signals_for(cells, kinds_, staffing=False):
        d = defaultdict(lambda: [0.0, 0])
        for o in cells:
            src = list(a for a in o["board"].get("plan_actions", []) if a["kind"] in kinds_) + (list(o["board"].get("staffing", [])) if staffing else [])
            for a in src:
                keys = [a["deal"]] if a.get("deal") in sigidx else [k for k in (a.get("evidence") or []) if k in sigidx]
                if not keys: continue
                for k in keys:
                    d[k][0] += a["eur_budget"] / len(keys); d[k][1] += 1
        rows = sorted(d.items(), key=lambda x: -x[1][0])
        return [{"key": k, "eur": round(v[0], 2), "n": v[1]} for k, v in rows]
    sig = {"named_deals": signals_for(ex, ("date", "share", "capability"), True),
           "recurring": signals_for(ex, ("pricing", "efficiency")),
           "new_business": signals_for(nb, ("date", "share", "capability"), True)}
    try:
        P27 = load(os.path.join(F.get("_root", ""), "budget", "budget_2027.json")) if F.get("_root") else None
        pk = {c["code"] + "|" + c["line"]: c for c in (P27 or {}).get("cells", [])}
    except Exception:
        pk = {}
    readings = []
    for o in ex:
        e = (o["board"].get("parts") or {}).get("market_outlook", 0.0) or 0.0
        if e < 5000: continue
        note = ((pk.get(o["code"] + "|" + o["line"], {}).get("stretch") or {}).get("market_note") or "")
        note = re.sub(r"\s*plus one standard deviation \([\d.]+\) for the stretch", "", note)
        readings.append({"country": o["country"], "line": o["line_label"], "eur": round(e, 2), "note": note})
    readings.sort(key=lambda x: -x["eur"])
    REST = {"named_deals": "the rest is the deals the market model already counts", "recurring": "the rest is the growth of the contracts we hold, shown inside the price and efficiency steps",
            "new_business": "the rest is the business the capability decisions open and the first contracts already priced"}
    for d in D:
        if d["key"] in sig:
            d["signals"] = sig[d["key"]]; d["signals_total"] = round(sum(x["eur"] for x in sig[d["key"]]), 2); d["rest_note"] = REST.get(d["key"], "")
            d["evidence"] = [x["key"] for x in sig[d["key"]][:5]]
        if d["key"] == "market_outlook":
            d["readings"] = readings; d["readings_total"] = round(sum(x["eur"] for x in readings), 2)
    return {"growth": round(growth, 2), "from": round(T["rev_2026"], 2), "to": round(T["commit"], 2), "items": D, "levers": LV,
            "bases": {"new": round(base_new, 2), "recurring": round(base_rec, 2), "covered": round(base_cov, 2)},
            "note": "The four drivers add up to the whole growth. Price steps, efficiency steps, share wins and capability decisions are each counted once, inside the driver shown."}

PLAIN_REPL = [
    (r",? set at the highest estimate in every line with every named deal counted as won and (EUR [\d.]+m of new business included)", r", resting on the deals in the signals and \1"),
    (r"It is set at the highest estimate: every named deal is counted as won and the new business the capability decisions open is included, at (\*\*EUR [\d.]+m\*\*|EUR [\d.]+m)\.", r"It rests on the deals in the signals and on \1 of new business that the capability decisions open."),
    (r"every named deal (is )?counted as won and ", ""),
    (r"with every named deal counted as won", "on the deals in the signals"),
    (r"every named deal (is )?counted as won", "the deals in the signals"),
    (r"counted as won", "in the signals"),
    (r"existing Printec staff sharing the work", "the existing teams"),
    (r"delivered by existing Printec staff", "delivered by the existing teams"),
    (r"existing Printec staff", "the existing teams"),
]

def cmd_target(root, phase):
    """Set the 2027 budget at the maximum on the table (EUR 180.0m), remove the lowest acceptable number and
    the hires (decision of 17/09/2026). Starts from the plan file (kept as budget_2027_board.plan174.json).
    Phase "numbers": budget/board/target/numbers.json + TARGET_BRIEF.md for the writer, cell reasons rewritten
    mechanically. Phase "texts": merges budget/board/target/texts_target.json and writes budget_2027_board.json."""
    bdir = os.path.join(root, "budget"); tdir = os.path.join(bdir, "board", "target"); os.makedirs(tdir, exist_ok=True)
    keep = os.path.join(bdir, "budget_2027_board.plan174.json")
    if phase == "numbers":
        F = load(keep) if os.path.exists(keep) else load(os.path.join(bdir, "budget_2027_board.json"))
        if not (F and F.get("plan_based")):
            sys.exit("need the plan-based budget_2027_board.json")
        if not os.path.exists(keep):
            save(keep, F)
        F = json.loads(json.dumps(F))
        T = F["totals"]
        for o in F["cells"] + F["new_business"]:
            b = o["board"]
            hires = [a for a in b.get("plan_actions", []) if a["kind"] == "hire"]
            b["plan_actions"] = [a for a in b.get("plan_actions", []) if a["kind"] != "hire"]
            b["staffing"] = hires
            old = b["target"]
            b["target"] = b["upside"]; b["floor"] = b["upside"]
            b["growth_pct"] = b.get("upside_growth_pct"); b["floor_growth_pct"] = b.get("upside_growth_pct")
            ratio = (b["target"] / old) if old else 1.0
            b["new"] = round((b.get("new") or 0) * ratio if old else b["target"], 2); b["recurring"] = round((b.get("recurring") or 0) * ratio if old else 0.0, 2)
            b["rp"] = round(b["target"] * b["margin_pct"] / 100.0, 2)
            b["gap_closer_eur"] = 0.0; b["plan_floor_delta"] = None
            b["plan_budget_delta"] = round(b["target"] - ((b.get("today") or {}).get("target") or 0), 2)
            b["conditions"] = [c for c in b.get("conditions", []) if not any(w in c.lower() for w in ("hire", "floor", "closing fact", "double"))]
            cap = b.get("capacity")
            if cap and cap.get("verdict") == "yes-with-hire":
                cap["verdict"] = "yes"; cap["reason"] = "Delivered with existing Printec staff sharing the work, with no new staff."
            if o.get("new_business"):
                b["parts"] = {"market_outlook": 0.0, "recurring": 0.0, "named_deals_net": round(b["target"], 2), "case": "new"}
            b["dissent"] = None
            b["conditions"] = [x for x in (_only_target_text(c) for c in b["conditions"]) if x]
            b["reason"] = _reason(o); b["proposer_title"] = "The plan"
        # totals
        old_commit = T["commit"]
        T["commit"] = T["upside"]; T["floor"] = T["upside"]; T["rp_commit"] = T["rp_upside"]; T["rp_floor"] = T["rp_upside"]
        T["commit_growth_pct"] = T["upside_growth_pct"]; T["floor_growth_pct"] = T["upside_growth_pct"]
        T["new_business_commit"] = T["new_business_upside"]
        T["commit_existing"] = round(T["commit"] - T["new_business_commit"], 2)
        P = T["parts"]
        P["new_business"] = T["new_business_commit"]
        P["plan_by_kind"] = [k for k in P.get("plan_by_kind", []) if k.get("kind") != "hire"]
        P["gap_closers"] = 0.0
        P["plan_actions"] = round(sum(a["eur_budget"] for o in F["cells"] + F["new_business"] for a in o["board"]["plan_actions"]), 2)
        P["staffing"] = round(sum(a["eur_budget"] for o in F["cells"] + F["new_business"] for a in o["board"].get("staffing", [])), 2)
        P["named_deals_net"] = round(T["commit"] - T["rev_2026"] - P["market_outlook"] - P["recurring"] - P["new_business"] - P.get("flat", 0.0), 2)
        for c in F["by_country"] + F["by_line"]:
            c["commit"] = c["upside"]; c["floor"] = c["upside"]; c["commit_growth_pct"] = c.get("upside_growth_pct"); c["floor_growth_pct"] = c.get("upside_growth_pct")
        pl = F.get("plan") or {}
        pl.update({"ladder": [], "delivery_ask": [], "delivery_summary": {}, "gap_closers": {}, "delivery_cost_budget": 0.0, "delivery_cost_maximum": 0.0,
                   "actions_by_kind": [k for k in pl.get("actions_by_kind", []) if k.get("kind") != "hire"],
                   "n_actions": sum(len(o["board"]["plan_actions"]) for o in F["cells"] + F["new_business"])})
        F["plan"] = pl
        F["single_number"] = True; F["only_target"] = True
        T["supported_today"] = None; T["supported_today_growth_pct"] = None
        F["target_note"] = "The 2027 budget is set at the highest estimate the evidence carries for each line (decision of 17/09/2026), with the new business the capability decisions open included. There is no separate lowest acceptable number. No new staff are planned; the existing teams deliver the plan."
        F["generated"] = datetime.date.today().isoformat()
        save(os.path.join(tdir, "numbers.json"), F)
        # the brief for the writer
        top = sorted(F["cells"] + F["new_business"], key=lambda o: -(o["board"]["target"] - ((o["board"].get("today") or {}).get("target") or 0)))[:30]
        L = ["# The 2027 budget at EUR 180.0m (for the writer)", "",
             "| | 2027 | Growth on 2026 (EUR %.2fm) |" % (T["rev_2026"] / 1e6), "|---|---|---|",
             "| 2027 budget (write it as EUR 180.0m) | EUR %.2fm | %+.1f%% |" % (T["commit"] / 1e6, T["commit_growth_pct"]),
             "| What the evidence supports today (reference) | EUR %.2fm | %+.1f%% |" % ((T["supported_today"] or 0) / 1e6, T["supported_today_growth_pct"] or 0),
             "| Reviewed budget before the plan (reference) | EUR %.2fm | %+.1f%% |" % (T["today"]["commit"] / 1e6, T["today"]["commit_growth_pct"]),
             "| Profit at held margins (2026: EUR %.2fm) | EUR %.2fm | |" % (T["rp_2026"] / 1e6, T["rp_commit"] / 1e6), "",
             "The budget equals the previous maximum on the table: every named deal counted as won, plus EUR %.2fm of new business the capability decisions open. There is no lowest acceptable number any more. No hires: EUR %.2fm of revenue that 34 hire actions were to deliver is now delivered by existing Printec staff sharing the work. Plan actions left: %d (dated orders and tenders, share wins, capability decisions, price and efficiency steps) adding EUR %.2fm on the reviewed numbers." % (T["new_business_commit"] / 1e6, P["staffing"] / 1e6, F["plan"]["n_actions"], P["plan_actions"] / 1e6), "",
             "Where the growth of EUR %.2fm comes from: named deals net of threat EUR %.2fm, market outlook EUR %.2fm, recurring revenue EUR %.2fm, new business EUR %.2fm." % ((T["commit"] - T["rev_2026"]) / 1e6, P["named_deals_net"] / 1e6, P["market_outlook"] / 1e6, P["recurring"] / 1e6, P["new_business"] / 1e6),
             "By action: " + "; ".join("%d %s EUR %.2fm" % (k["n"], k["kind"], k["eur_budget"] / 1e6) for k in P["plan_by_kind"]) + ".", "",
             "## By product line", "", "| Line | 2026 | Budget | Growth |", "|---|---|---|---|"]
        for l in sorted(F["by_line"], key=lambda x: -x["commit"]):
            L.append("| %s | %.2f | %.2f | %s |" % (l["line_label"], l["rev_2026"] / 1e6, l["commit"] / 1e6, ("%+.1f%%" % l["commit_growth_pct"]) if l["commit_growth_pct"] is not None else "new"))
        L += ["", "## By market", "", "| Market | 2026 | Budget | Growth |", "|---|---|---|---|"]
        for c in sorted(F["by_country"], key=lambda x: -x["commit"]):
            L.append("| %s | %.2f | %.2f | %+.1f%% |" % (c["country"], c["rev_2026"] / 1e6, c["commit"] / 1e6, c["commit_growth_pct"]))
        L += ["", "## The thirty cells that move most (reviewed number today -> budget), with their actions", ""]
        for o in top:
            b = o["board"]
            L.append("### %s x %s: EUR %.2fm today -> budget EUR %.2fm" % (o["country"], o["line_label"], ((b.get("today") or {}).get("target") or 0) / 1e6, b["target"] / 1e6))
            for a in b["plan_actions"]:
                L.append("- [%s, by %s, %s, +%.2fm] %s%s" % (a["kind"], a["by"], a["owner"], a["eur_budget"] / 1e6, a["what"], (" (" + a["deal_title"] + ")") if a["deal_title"] else ""))
            L.append("")
        with open(os.path.join(tdir, "TARGET_BRIEF.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(L))
        print("target numbers: budget %s (%+.1f%%), profit %s, new business %s, staffing (former hires) %s, actions %d; cells %d + new %d" % (
            m(T["commit"]), T["commit_growth_pct"], m(T["rp_commit"]), m(T["new_business_commit"]), m(P["staffing"]), F["plan"]["n_actions"], len(F["cells"]), len(F["new_business"])))
        return
    F = load(os.path.join(tdir, "numbers.json")); TP = load(os.path.join(tdir, "texts_target.json"))
    if not (F and TP):
        sys.exit("phase texts needs budget/board/target/numbers.json and texts_target.json")
    R = F["report"]
    for k in ("headline", "executive_summary_md", "conditions", "change_our_mind", "sections", "levers"):
        if k in TP:
            R[k] = TP[k]
    R.pop("minority_report", None)
    sigidx = load(os.path.join(bdir, "board", "packet", "signals_index.json")) or {}
    for sec in R.get("sections", []):
        sec["evidence"] = [k for k in (sec.get("evidence") or []) if k in sigidx]
    cellmap = {"%s|%s" % (o["code"], o["line"]): o for o in F["cells"] + F["new_business"]}
    for lv in R.get("levers", []):
        lv["evidence"] = [k for k in (lv.get("evidence") or []) if k in sigidx]
        o = cellmap.get(lv.get("cell"))
        if o:
            lv.update({"country": o["country"], "line_label": o["line_label"], "target_2026": o["target_2026"], "commit": o["board"]["target"], "upside": o["board"]["upside"],
                       "commit_growth_pct": o["board"]["growth_pct"], "upside_growth_pct": o["board"]["upside_growth_pct"]})
    if TP.get("largest_reachable_basis"):
        F["largest_reachable_basis"] = TP["largest_reachable_basis"]
    if TP.get("dissent_views"):
        F["dissent_views"] = TP["dissent_views"]
    F["_root"] = root
    F["drivers"] = _drivers(F, sigidx)
    F.pop("_root", None)
    SP = load(os.path.join(tdir, "summary_plain.json"))
    if SP and SP.get("executive_summary_md"):
        R["executive_summary_md"] = SP["executive_summary_md"]
        if SP.get("headline"): R["headline"] = SP["headline"]
    def _plain(t):
        if not isinstance(t, str): return t
        for a, b in PLAIN_REPL: t = re.sub(a, b, t)
        return t
    for k in ("headline", "executive_summary_md"): R[k] = _plain(R.get(k, ""))
    for sec in R.get("sections", []): sec["text"] = _plain(sec["text"])
    for lv in R.get("levers", []): lv["why"] = _plain(lv["why"])
    R["conditions"] = [_plain(c) for c in R.get("conditions", [])]; R["change_our_mind"] = [_plain(c) for c in R.get("change_our_mind", [])]
    F["largest_reachable_basis"] = _plain(F.get("largest_reachable_basis", ""))
    for v in F.get("dissent_views", []): v["reason"] = _plain(v.get("reason", "")); v["text"] = _plain(v.get("text", ""))
    for o in F["cells"] + F["new_business"]:
        o["board"]["reason"] = _plain(o["board"]["reason"]); o["board"]["conditions"] = [_plain(c) for c in o["board"].get("conditions", [])]
    # one number only: strip every reference to the reviewed, supported-today and model figures
    for k in ("headline", "executive_summary_md"):
        R[k] = _only_target_text(R.get(k, ""))
    for sec in R.get("sections", []):
        sec["text"] = _only_target_text(sec["text"])
        if "supports today" in sec["title"].lower():
            sec["title"] = "What the plan adds"
    for lv in R.get("levers", []):
        lv["why"] = _only_target_text(lv["why"])
    R["conditions"] = [x for x in (_only_target_text(c) for c in R.get("conditions", [])) if x]
    R["change_our_mind"] = [x for x in (_only_target_text(c) for c in R.get("change_our_mind", [])) if x]
    F["largest_reachable_basis"] = _only_target_text(F.get("largest_reachable_basis", ""))
    for v in F.get("dissent_views", []):
        v["reason"] = _only_target_text(v.get("reason", "")); v["text"] = _only_target_text(v.get("text", ""))
    left = [k for k, v in (("headline", R["headline"]), ("summary", R["executive_summary_md"]), ("basis", F["largest_reachable_basis"])) if ONLY_PAT.search(v)]
    left += ["section:" + x["title"] for x in R["sections"] if ONLY_PAT.search(x["text"])] + ["cell:" + o["code"] + "|" + o["line"] for o in F["cells"] + F["new_business"] if ONLY_PAT.search(o["board"]["reason"])]
    if left:
        print("WARNING other-number references left in:", left)
    # mechanical check: no banned words in any reader-facing text
    blob = json.dumps({"r": R, "b": F["largest_reachable_basis"], "d": F["dissent_views"], "c": [o["board"]["reason"] for o in F["cells"] + F["new_business"]]}, ensure_ascii=False).lower()
    hits = {w: len(re.findall(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", blob)) for w in TARGET_BANNED}; hits = {w: n for w, n in hits.items() if n}
    if hits:
        print("WARNING banned words in texts:", hits)
    save(os.path.join(bdir, "budget_2027_board.json"), F)
    write_decision_md(F, os.path.join(bdir, "BUDGET_2027_PLAN.md"))
    print("target board file written: budget %s (%+.1f%%)" % (m(F["totals"]["commit"]), F["totals"]["commit_growth_pct"]))


# ---------------------------------------------------------------------------------------------------
# stretch: the budget taken to EUR 200.0m from new business and the payments industry only
# (asked 22/09/2026). The named deals of the plan are never touched.
# ---------------------------------------------------------------------------------------------------
STRETCH_TARGET = 200_000_000.0
PAY_LINES = ["pos_acquiring", "payments_instant", "fraud_monitoring", "digital_onboarding", "payment_security_hsm", "card_issuing"]
POT_EUR = {"XL": 7.5e6, "L": 3.0e6, "M": 0.6e6, "S": 0.1e6, "Unscoped": 0.1e6}
# the payments industry's growth to 2030, from the Future outlook (findings/08-futurist/2026-09-01.md), one year of it
PAY_GROWTH = {"digital_onboarding": (15.4, "EU Digital Identity wallet: the identity verification market grows at about 15.4% a year to 2030; acceptance becomes binding on 24 December 2027"),
              "fraud_monitoring": (18.0, "Financial crime: anti-money-laundering solutions grow at 18.0% a year to 2031"),
              "payment_security_hsm": (15.3, "Post-quantum cryptography: hardware security modules grow at 15.3% a year, on Swift's timetable"),
              "payments_instant": (15.0, "Instant payments: euro-area instant transfers rise from 25% to 35 to 45% of credit transfers by 2028; the Western Balkans get instant systems by 2028")}

def _stretch_reason(kind, **kw):
    if kind == "nb":
        return "Priced the way the plan priced its own new business: %.1f%% of the opportunity value in the signals%s." % (kw["rate"] * 100, " (a 2027-dated opportunity)" if kw.get("dated") else "")
    return "A payments combination: priced at %.1f%% of its opportunity value, the higher conversion the stretch asks for, still under the %.0f%% the plan's best third converted at." % (kw["rate"] * 100, kw["best"] * 100)

def cmd_stretch(root, phase):
    """Phase numbers: build budget/budget_2027_stretch.json + STRETCH_BRIEF.md. Phase texts: merge stretch_texts.json."""
    bdir = os.path.join(root, "budget"); sdir = os.path.join(bdir, "board", "stretch"); os.makedirs(sdir, exist_ok=True)
    if phase == "texts":
        S = load(os.path.join(bdir, "budget_2027_stretch.json")); T = load(os.path.join(sdir, "stretch_texts.json"))
        if not (S and T): sys.exit("need budget_2027_stretch.json and stretch_texts.json")
        for k in ("headline", "summary_md", "conditions", "risks"):
            if k in T: S["texts"][k] = T[k]
        blob = json.dumps(S["texts"], ensure_ascii=False).lower()
        hits = {w: len(re.findall(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", blob)) for w in TARGET_BANNED}; hits = {w: n for w, n in hits.items() if n}
        if hits: print("WARNING banned words in stretch texts:", hits)
        save(os.path.join(bdir, "budget_2027_stretch.json"), S); print("stretch texts merged"); return
    F = load(os.path.join(bdir, "budget_2027_board.json")); P = load(os.path.join(bdir, "budget_2027.json"))
    D = load(os.path.join(root, "intel-cache", "dashboard-data.json"))
    if not (F and P and D): sys.exit("need budget_2027_board.json, budget_2027.json and intel-cache/dashboard-data.json")
    sig = {x["key"]: x for x in D["signals"]}; label = {l["line"]: l["line_label"] for l in F["by_line"]}
    for k, v in (D.get("prod_label") or {}).items(): label.setdefault(k, v)
    name = {c["code"]: c["country"] for c in F["by_country"]}
    T = F["totals"]; start = T["commit"]; gap = STRETCH_TARGET - start
    priced = {"%s|%s" % (o["code"], o["line"]): o for o in F["new_business"]}
    def pot(c): return sum(POT_EUR.get(o.get("band") or "S", 1e5) * (0.5 if o.get("footprint_wide") else 1.0) for o in c["opportunities"])
    def dated(c): return [o for o in c["opportunities"] if str(o.get("dated") or "")[:4] == "2027"]
    # the plan's own new-business pricing rates: with and without a 2027-dated opportunity
    dt = dp = ut = up = 0.0; ratios = []
    for c in P["new_business"]:
        k = "%s|%s" % (c["code"], c["line"]); pv = pot(c)
        if k in priced and pv > 0:
            t = priced[k]["board"]["target"]; ratios.append(t / pv)
            if dated(c): dt += t; dp += pv
            else: ut += t; up += pv
    rate_d = dt / dp if dp else 0.05; rate_u = ut / up if up else 0.035
    ratios.sort(reverse=True); best_third = sum(ratios[:max(1, len(ratios) // 3)]) / max(1, len(ratios[:max(1, len(ratios) // 3)]))
    # ---- layer 1: the 66 unpriced combinations at the plan's own rate ----
    L1 = []
    for c in P["new_business"]:
        k = "%s|%s" % (c["code"], c["line"])
        if k in priced: continue
        pv = pot(c); r = rate_d if dated(c) else rate_u; eur = pv * r
        if eur < 5000: continue
        L1.append({"code": c["code"], "country": c["country"], "line": c["line"], "line_label": label.get(c["line"], c["line_label"]), "pot": round(pv, 2), "rate": round(r, 4),
                   "eur": round(eur, 2), "dated": len(dated(c)), "payments": c["line"] in PAY_LINES, "signals": [o["key"] for o in c["opportunities"] if o.get("key") in sig],
                   "largest": max(c["opportunities"], key=lambda o: POT_EUR.get(o.get("band") or "S", 1e5)).get("title", ""), "reason": _stretch_reason("nb", rate=r, dated=bool(dated(c)))})
    l1 = sum(x["eur"] for x in L1)
    # ---- layer 2: payments waves counted in every payments line they touch, at full weight ----
    L2 = []
    for c in P["cells"]:
        if c["line"] not in PAY_LINES: continue
        g = c["stretch"]; e = 0.0; items = []
        for it in g.get("share_items", []):
            if not it.get("footprint_wide"): continue
            pts = {"XL": 3, "L": 2, "M": 1}.get(it.get("band"), 0.5)
            add = c["new_2026"] * (pts if (it.get("counted_in") and it["counted_in"] != c["line"]) else pts / 2.0) / 100.0
            if add > 0: e += add; items.append(it.get("key"))
        if e >= 5000: L2.append({"code": c["code"], "country": name.get(c["code"], c["code"]), "line": c["line"], "line_label": label.get(c["line"]), "eur": round(e, 2), "signals": [k for k in items if k in sig]})
    l2 = sum(x["eur"] for x in L2)
    # ---- layer 3: acquiring estates grow at the full terminal-market rate ----
    L3 = []
    for c in P["cells"]:
        if c["line"] != "pos_acquiring": continue
        g = c["stretch"]; e = c["recurring_2026"] * max(0.0, g.get("market_pct", 0) - g.get("recurring_rate_pct", 0)) / 100.0
        if e >= 5000: L3.append({"code": c["code"], "country": name.get(c["code"], c["code"]), "line": c["line"], "line_label": label.get(c["line"]), "eur": round(e, 2), "market_pct": g.get("market_pct"), "note": g.get("market_note", "")})
    l3 = sum(x["eur"] for x in L3)
    # ---- layer 4: one year of the payments industry's growth to 2030 on the payments software lines ----
    L4 = []
    for o in F["cells"] + F["new_business"]:
        cg = PAY_GROWTH.get(o["line"])
        if not cg: continue
        e = o["board"]["target"] * cg[0] / 100.0
        if e >= 5000: L4.append({"code": o["code"], "country": o["country"], "line": o["line"], "line_label": o["line_label"], "eur": round(e, 2), "pct": cg[0], "why": cg[1]})
    l4 = sum(x["eur"] for x in L4)
    # ---- layer 5: payments combinations convert at a higher rate, up to the target ----
    rest = gap - (l1 + l2 + l3 + l4)
    pay_pot = sum(x["pot"] for x in L1 if x["payments"])
    uplift = max(0.0, rest / pay_pot) if pay_pot else 0.0
    capped = False
    if uplift + rate_u > best_third:
        uplift = max(0.0, best_third - rate_u); capped = True
    L5 = []
    for x in L1:
        if x["payments"] and uplift > 0:
            e = x["pot"] * uplift; x["eur_stretch_extra"] = round(e, 2); x["rate_total"] = round(x["rate"] + uplift, 4)
            L5.append({"code": x["code"], "country": x["country"], "line": x["line"], "line_label": x["line_label"], "eur": round(e, 2), "rate_total": x["rate_total"], "signals": x["signals"]})
            x["reason"] = _stretch_reason("nb_pay", rate=x["rate"] + uplift, best=best_third)
    l5 = sum(x["eur"] for x in L5)
    total = start + l1 + l2 + l3 + l4 + l5; unsupported = max(0.0, STRETCH_TARGET - total)
    # ---- per-cell view: existing cells get L2/L3/L4, new combinations get L1 (+L5) ----
    inc = defaultdict(float)
    for L in (L2, L3, L4):
        for x in L: inc["%s|%s" % (x["code"], x["line"])] += x["eur"]
    cells = []
    for o in F["cells"] + F["new_business"]:
        k = "%s|%s" % (o["code"], o["line"]); v = o["board"]["target"] + inc.get(k, 0.0)
        cells.append({"code": o["code"], "line": o["line"], "budget": o["board"]["target"], "stretch": round(v, 2), "extra": round(inc.get(k, 0.0), 2), "new_business": bool(o.get("new_business"))})
    new_cells = [{"code": x["code"], "country": x["country"], "line": x["line"], "line_label": x["line_label"], "stretch": round(x["eur"] + x.get("eur_stretch_extra", 0.0), 2), "budget": 0.0,
                  "pot": x["pot"], "rate": x.get("rate_total", x["rate"]), "dated": x["dated"], "payments": x["payments"], "signals": x["signals"], "largest": x["largest"], "reason": x["reason"]} for x in L1]
    by_c = defaultdict(lambda: 0.0); by_l = defaultdict(lambda: 0.0)
    for c in F["by_country"]: by_c[c["code"]] = c["commit"]
    for l in F["by_line"]: by_l[l["line"]] = l["commit"]
    for x in cells:
        by_c[x["code"]] += x["extra"]; by_l[x["line"]] += x["extra"]
    for x in new_cells:
        by_c[x["code"]] += x["stretch"]; by_l[x["line"]] += x["stretch"]
    lines_nb = defaultdict(lambda: {"eur": 0.0, "countries": set(), "n": 0})
    for x in new_cells:
        lines_nb[x["line_label"]]["eur"] += x["stretch"]; lines_nb[x["line_label"]]["countries"].add(x["country"]); lines_nb[x["line_label"]]["n"] += 1
    nb_rows = [{"line": k, "eur": round(v["eur"], 2), "n": v["n"], "countries": sorted(v["countries"])} for k, v in sorted(lines_nb.items(), key=lambda z: -z[1]["eur"])]
    M = lambda v: "EUR %.2fm" % (v / 1e6)
    layers = [
        {"key": "nb_plan_rate", "title": "New business, priced the way the plan priced its own", "eur": round(l1, 2), "n": len(L1),
         "what": "%d country and product combinations where the signals show banks buying but the plan set no number. Each is priced by the same rule the base budget used for its own 29 new-business combinations: what the plan set, divided by the opportunity value of the signals behind it. That gives %.1f%% of the opportunity value where an opportunity is dated inside 2027 and %.1f%% where none is." % (len(L1), rate_d * 100, rate_u * 100),
         "proof": "%d of them are payments combinations: instant payments, fraud monitoring, digital identity, key management, card issuing and acquiring. %d carry an opportunity dated inside 2027." % (sum(1 for x in L1 if x["payments"]), sum(1 for x in L1 if x["dated"])),
         "items": sorted(L1, key=lambda x: -x["eur"])},
        {"key": "pay_waves", "title": "Regulations and industry changes counted in every payments line they affect", "eur": round(l2, 2), "n": len(L2),
         "what": "Some signals are not one bank\u2019s purchase but a change that hits every bank at once: the digital euro specifications for terminals, the EU digital identity wallet and its bank acceptance duty, the anti-money-laundering rules, the DORA testing scope. Such a change creates work in several product lines of a country. The base budget counts it in one line only, at half weight, to avoid double counting; the stretch counts it in every payments line it affects, at full weight.",
         "proof": "%d payments lines in the existing budget, on the footprint-wide signals already in the table. The smallest layer; it is here for completeness." % len(L2), "items": sorted(L2, key=lambda x: -x["eur"])},
        {"key": "pos_full_rate", "title": "Acquiring estates at the full terminal-market rate", "eur": round(l3, 2), "n": len(L3),
         "what": "Terminal management and acquiring revenue grows with the number of terminals. The plan grows it at half the market rate; the stretch takes the full rate of the market readings on this page.",
         "proof": "%d POS cells; the Future outlook expects terminal numbers in mandate-driven CEE markets to grow 17 to 21%% a year." % len(L3), "items": sorted(L3, key=lambda x: -x["eur"])},
        {"key": "pay_growth", "title": "One year of the payments industry's growth", "eur": round(l4, 2), "n": len(L4),
         "what": "The payments software lines have no market reading in the model. The stretch gives them one year of the growth the Future outlook expects to 2030: identity verification 15.4%, anti-money-laundering 18.0%, key management 15.3%, instant payments 15.0%.",
         "proof": "Applied to the 2027 budget of digital identity, fraud monitoring, key management and payments modernisation lines, existing and new.", "items": sorted(L4, key=lambda x: -x["eur"])},
        {"key": "pay_convert", "title": "Payments new business converting at a higher rate", "eur": round(l5, 2), "n": len(L5),
         "what": "The payments combinations of layer one priced at %.1f%% of their opportunity value instead of the plan's %.1f%%. The plan's own best third converted at %.0f%%, so the rate stays inside what the plan has already accepted." % ((rate_u + uplift) * 100, rate_u * 100, best_third * 100) if L5 else "Not needed: the first four layers reach the target.",
         "proof": "%d payments combinations in %d countries." % (len(L5), len({x["code"] for x in L5})) if L5 else "", "items": sorted(L5, key=lambda x: -x["eur"]), "capped": capped}]
    # signals per layer, largest first
    for L in layers:
        d = defaultdict(float)
        for x in L["items"]:
            ks = [k for k in x.get("signals", []) if k in sig]
            for k in ks: d[k] += x["eur"] / len(ks)
        L["signals"] = [{"key": k, "eur": round(v, 2)} for k, v in sorted(d.items(), key=lambda z: -z[1])]
        for x in L["items"]: x.pop("signals", None) if L["key"] != "nb_plan_rate" else None
    futures = [{"scope": f.get("scope"), "direction": f.get("direction"), "confidence": f.get("confidence"), "projected": (f.get("projected") or "")[:400], "oid": f.get("oid")} for f in D.get("futures", [])
               if any(w in (f.get("scope") or "").lower() for w in ("instant", "identity", "financial crime", "post-quantum", "payment acceptance", "western balkans", "open finance"))]
    caps = [{"area": c.get("area"), "decision": c.get("decision"), "by": c.get("by"), "owner": c.get("owner"), "opens": c.get("opens", []), "text": c.get("text", "")} for c in (F.get("plan") or {}).get("capability", [])]
    S = {"generated": datetime.date.today().isoformat(), "built_from": F.get("generated"), "target": STRETCH_TARGET, "start": round(start, 2), "total": round(total, 2), "growth_pct": round((total / T["rev_2026"] - 1) * 100, 1),
         "unsupported": round(unsupported, 2), "rates": {"dated": round(rate_d, 4), "undated": round(rate_u, 4), "best_third": round(best_third, 4), "payments_uplift": round(uplift, 4), "capped": capped},
         "layers": layers, "cells": cells, "new_cells": new_cells, "new_business_lines": nb_rows,
         "by_country": [{"code": c, "country": name.get(c, c), "budget": round(F["by_country"][[x["code"] for x in F["by_country"]].index(c)]["commit"], 2) if c in [x["code"] for x in F["by_country"]] else 0.0, "stretch": round(v, 2)} for c, v in sorted(by_c.items(), key=lambda z: -z[1])],
         "by_line": [{"line": l, "line_label": label.get(l, l), "budget": round(by_l0, 2), "stretch": round(v, 2)} for l, v, by_l0 in sorted(((l, v, next((x["commit"] for x in F["by_line"] if x["line"] == l), 0.0)) for l, v in by_l.items()), key=lambda z: -z[1])],
         "futures": futures, "capabilities": caps,
         "rp_stretch": round(T["rp_commit"] + (total - start) * 0.55, 2),
         "profit_note": "Profit on the stretch is estimated at the group's 2026 margin of 55% on the added revenue, on top of the budget's profit at held margins.",
         "texts": {"headline": "", "summary_md": "", "conditions": [], "risks": []}}
    save(os.path.join(bdir, "budget_2027_stretch.json"), S)
    # the brief for the writer
    L = ["# The stretch to EUR 200.0m (for the writer)", "",
         "The 2027 budget is EUR %.2fm (+21.1%% on 2026). The stretch takes it to EUR %.2fm (%+.1f%% on 2026) from NEW BUSINESS and the PAYMENTS INDUSTRY only. Not one named deal of the plan is changed. Unsupported remainder: EUR %.2fm." % (start / 1e6, total / 1e6, S["growth_pct"], unsupported / 1e6), "",
         "| Layer | EUR m | Items |", "|---|---|---|"] + ["| %s | %.2f | %d |" % (x["title"], x["eur"] / 1e6, x["n"]) for x in layers] + ["",
         "Rates: the plan priced its first 29 new-business combinations at %.1f%% of opportunity value where a 2027-dated opportunity exists and %.1f%% otherwise; its best third converted at %.0f%%. Layer five prices the payments combinations at %.1f%%%s." % (rate_d * 100, rate_u * 100, best_third * 100, (rate_u + uplift) * 100, " (capped at the best third)" if capped else ""), "",
         "## What the new business is (all new combinations, existing 29 not included)", ""] + ["- %s: EUR %.2fm in %d countries (%s)" % (r["line"], r["eur"] / 1e6, r["n"], ", ".join(r["countries"])) for r in nb_rows] + ["",
         "## The ten largest new combinations", ""] + ["- %s x %s: EUR %.2fm (%s; %d dated 2027; largest signal: %s)" % (x["country"], x["line_label"], x["stretch"] / 1e6, "payments" if x["payments"] else "other", x["dated"], x["largest"]) for x in sorted(new_cells, key=lambda z: -z["stretch"])[:10]] + ["",
         "## Capability decisions the plan already names (they open the new business)", ""] + ["- %s (%s, by %s, %s): %s" % (c["area"], c["decision"], c["by"], c["owner"], c["text"][:300]) for c in caps] + ["",
         "## The Future outlook themes behind the payments industry", ""] + ["- %s (%s, confidence %s): %s" % (f["scope"], f["direction"], f["confidence"], f["projected"][:300]) for f in futures]
    with open(os.path.join(sdir, "STRETCH_BRIEF.md"), "w", encoding="utf-8") as fh: fh.write("\n".join(L))
    print("stretch: %s -> %s (%+.1f%%); layers %s; unsupported %s; uplift %.1f%% capped=%s" % (M(start), M(total), S["growth_pct"], ", ".join("%s %.2f" % (x["key"], x["eur"] / 1e6) for x in layers), M(unsupported), uplift * 100, capped))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["packet", "reconcile", "finalize", "publicize", "mandate", "plan", "target", "stretch"])
    ap.add_argument("--phase", default="numbers")
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    if a.cmd == "plan":
        cmd_plan(os.path.abspath(a.root), a.phase)
    elif a.cmd == "target":
        cmd_target(os.path.abspath(a.root), a.phase)
    elif a.cmd == "stretch":
        cmd_stretch(os.path.abspath(a.root), a.phase)
    else:
        {"packet": cmd_packet, "reconcile": cmd_reconcile, "finalize": cmd_finalize, "publicize": cmd_publicize, "mandate": cmd_mandate}[a.cmd](os.path.abspath(a.root))
