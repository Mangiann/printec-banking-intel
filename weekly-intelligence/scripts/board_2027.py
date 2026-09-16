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
import argparse, json, os, sys, datetime
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["packet", "reconcile", "finalize", "publicize", "mandate", "plan"])
    ap.add_argument("--phase", default="numbers")
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    if a.cmd == "plan":
        cmd_plan(os.path.abspath(a.root), a.phase)
    else:
        {"packet": cmd_packet, "reconcile": cmd_reconcile, "finalize": cmd_finalize, "publicize": cmd_publicize, "mandate": cmd_mandate}[a.cmd](os.path.abspath(a.root))
