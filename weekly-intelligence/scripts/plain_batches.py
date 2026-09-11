#!/usr/bin/env python3
"""plain_batches.py — collect every reader-facing text into batches for the plain-English editor.

Reads the content files the agents write and produces <work>/items/batchNN.json (a JSON array of
{id, kind, title, fields, note}) plus <work>/manifest.json and <work>/STYLE.md. plain_merge.py writes
the rewritten fields back. Ids are stable addresses into the source files, e.g. "row:412" is line 412
of master-signal-table.md, "outlook:17" is oid 17 in forecast_narrative.json.

  python plain_batches.py --root <BANKING> --work <dir> [--max-chars 60000] [--since YYYY-MM-DD]

--since limits the master-table rows to those whose Date cell mentions a date on/after that day —
the weekly editor uses it so only the new week's rows are rewritten, not the whole table again.
"""
import argparse, json, os, re, io
from collections import Counter

def style_text(root):
    """The shared writing policy IS the style guide the agents read. A short model passage follows it."""
    pol = open(os.path.join(root, "WRITING_POLICY.md"), encoding="utf-8").read()
    model = """

## The level to write at — a model passage

There is a clear growth opportunity, and for the first time there is a free, regularly updated map published by the regulator that shows where the opportunity is.

The Croatian National Bank's cash-point registry, downloaded in full on 27 August 2026, contains 6,852 records with provider names, tax numbers, addresses and coordinates. These include 3,841 cash-withdrawal-only ATMs, 901 machines that allow both deposits and withdrawals, 85 deposit-only machines, 126 coin-deposit machines, 1,860 bank branches and 39 cashless branches ([HNB cash-point registry, devices endpoint](https://www.hnb.hr/o/info-cash-point/v1.0/devices?page=1&pageSize=20000)).

Zagrebacka banka has the largest ATM network in Croatia. It has 562 withdrawal-only ATMs, compared with 137 machines that accept deposits. Out of 95 branches, only five are cashless.

Regulatory pressure is also increasing. A change to the law, published as Narodne novine 105/2025 on 23 July 2025, allows consumers to request a free basic banking package. This includes free cash deposits at a bank counter or ATM and free withdrawals from their own bank. From 1 January 2027, customers using this package, as well as vulnerable customers with basic accounts, will also be able to make two free withdrawals per month from ATMs operated by other Croatian banks.

The main message is simple: use the Croatian National Bank registry as the account and opportunity map; sell cash-recycling machines as a way for banks to reduce the cost of providing free deposits; and position coin automation as a product that can generate revenue, rather than simply as a compliance expense.

## For THIS job (an edit, not new writing)
- Keep every number, percentage, money amount, date, year, count, name, citation tag such as (A1) and URL exactly as written. Markdown link text may be simplified; the URL may not change.
- Same facts, same order, same structure. Similar length. Table cells: no "|" and no line breaks; use " · " or a full stop where the original had a break.
- Where an item's "note" gives extra rules (e.g. patterns: rate phrases word for word), those rules win.
- Titles ("scope", "title", pattern headlines): a short DESCRIPTIVE title of what the item is about, not a headline. Keep any rate figure that was in it.
"""
    return pol + model

PROSE_COLS = {"Signal": "signal", "What it implies": "implies", "Recommended follow-up": "follow_up"}

def load(p, default):
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception:
        return default

def collect(root, since=None):
    items = []
    # 1. master table rows (one line each)
    t = io.open(os.path.join(root, "master-signal-table.md"), encoding="utf-8").read().split("\n")
    hdr_i = next(i for i, l in enumerate(t) if l.startswith("|") and "Bank / Theme" in l)
    hdr = [c.strip() for c in t[hdr_i].strip().strip("|").split("|")]
    col = {h: i for i, h in enumerate(hdr)}
    for i, l in enumerate(t):
        if not l.startswith("| **"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) != len(hdr):
            continue
        if since:
            dates = re.findall(r"(\d{2})/(\d{2})/(\d{4})", cells[col.get("Date", 0)])
            if not any(f"{y}-{m}-{d}" >= since for d, m, y in dates):
                continue
        f = {k: cells[col[h]] for h, k in PROSE_COLS.items() if h in col and len(cells[col[h]]) > 60}
        if f:
            items.append({"id": f"row:{i}", "kind": "signal", "title": cells[col["Bank / Theme"]][:80], "fields": f,
                          "note": "Markdown table cells: keep [A1](path) style source tags and links exactly; no '|' and no line breaks."})
    D = os.path.join(root, "intel-cache")
    # 2. outlooks
    fn = load(os.path.join(D, "forecast_narrative.json"), {})
    for kind, arr in (("outlook", fn.get("outlooks", [])), ("product_outlook", fn.get("product_outlooks", []))):
        for o in arr:
            f = {k: o[k] for k in ("scope", "summary", "projected", "rationale") if isinstance(o.get(k), str) and len(o[k]) > (10 if k == "scope" else 60)}
            if isinstance(o.get("drivers"), list) and o["drivers"]:
                f["drivers"] = "\n\n".join(o["drivers"])
            if f:
                items.append({"id": f"{kind}:{o['oid']}", "kind": kind, "title": str(o.get("scope") or o.get("label"))[:80], "fields": f,
                              "note": "'drivers' is several bullet points separated by a blank line; return the same number of points, in the same order, separated by a blank line."})
    # 3. futures + board
    fu = load(os.path.join(D, "futures_narrative.json"), {})
    for c in fu.get("futures", []):
        f = {k: c[k] for k in ("scope", "projected", "rationale") if isinstance(c.get(k), str) and len(c[k]) > (10 if k == "scope" else 60)}
        if isinstance(c.get("drivers"), list) and c["drivers"]:
            f["drivers"] = "\n\n".join(c["drivers"])
        if f:
            items.append({"id": f"future:{c['oid']}", "kind": "future", "title": str(c.get("scope"))[:80], "fields": f,
                          "note": "'drivers' is several bullet points separated by a blank line; same number, same order."})
    b = fu.get("board_view", {})
    bl = b.get("bottom_line") or {}
    if bl:
        f = {k: bl[k] for k in ("headline", "thesis") if isinstance(bl.get(k), str) and bl[k]}
        if bl.get("picture"): f["picture"] = "\n\n".join(bl["picture"])
        if f:
            items.append({"id": "bottom:main", "kind": "bottom", "title": "Bottom line", "fields": f,
                          "note": "'picture' is several paragraphs separated by a blank line; you may split a paragraph into more paragraphs, but keep the order and every fact. 'headline' is a descriptive title, not a headline."})
        for sec in ("drivers", "gems"):
            for j, g in enumerate(bl.get(sec) or []):
                f = {k: g[k] for k in ("title", "detail") if isinstance(g.get(k), str) and g[k]}
                if f: items.append({"id": f"bottom:{sec}:{j}", "kind": "bottom", "title": g.get("title", "")[:80], "fields": f, "note": "'title' is a short descriptive title."})
        for j, r in enumerate(bl.get("endstate_2030") or []):
            f = {k: r[k] for k in ("now", "then", "note") if isinstance(r.get(k), str) and r[k]}
            if f: items.append({"id": f"bottom:endstate:{j}", "kind": "bottom", "title": r.get("metric", "")[:80], "fields": f, "note": "Short table cells; keep every figure."})
    for k, tk in (("money", "note"), ("competition", "note"), ("threats", "note"), ("timeline", "event")):
        for j, r in enumerate(b.get(k) or []):
            if isinstance(r.get(tk), str) and len(r[tk]) > 40:
                items.append({"id": f"board:{k}:{j}", "kind": "board", "title": str(r.get("segment") or r.get("shift") or r.get("threat") or r.get("when"))[:80], "fields": {tk: r[tk]}, "note": ""})
    # 4. patterns — the engine parses rate phrases out of these, so they must survive verbatim
    kb = load(os.path.join(D, "patterns_kb.json"), [])
    kb = kb if isinstance(kb, list) else kb.get("patterns", [])
    for j, p in enumerate(kb):
        items.append({"id": f"pattern:{j}", "kind": "pattern", "title": p.get("pattern", "")[:80],
                      "fields": {k: p[k] for k in ("pattern", "evidence", "implication") if isinstance(p.get(k), str)},
                      "note": "STRICT: any phrase giving a rate or growth ('~3-4%/yr', 'Hungary +18.6%', 'GROWING — ...; STABLE — ...; DECLINING — ...') must be kept word for word, including the words GROWING/STABLE/DECLINING and the country-rate pairs. A machine reads them. Simplify the rest."})
    # 5. competitors, derived, brief, signal projections
    cp = load(os.path.join(root, "weekly-intelligence", "references", "competitors.json"), {})
    for j, v in enumerate(cp.get("vendors", [])):
        if isinstance(v.get("latest"), str) and len(v["latest"]) > 80:
            items.append({"id": f"competitor:{j}", "kind": "competitor", "title": v["name"], "fields": {"latest": v["latest"]}, "note": ""})
    dv = load(os.path.join(D, "derived_opportunities.json"), [])
    dv = dv if isinstance(dv, list) else dv.get("derived", dv)
    for j, d in enumerate(dv or []):
        f = {k: d[k] for k in ("title", "claim", "why_not_visible_in_one_signal", "falsifier", "trigger") if isinstance(d.get(k), str) and len(d[k]) > (10 if k == "title" else 40)}
        if f:
            items.append({"id": f"derived:{j}", "kind": "derived", "title": d.get("title", "")[:80], "fields": f, "note": ""})
    cb = load(os.path.join(D, "competition_brief.json"), {})
    brief = cb.get("brief") if isinstance(cb, dict) else cb
    if isinstance(brief, str) and brief.strip():
        items.append({"id": "brief:0", "kind": "brief", "title": "Competition brief", "fields": {"brief": brief}, "note": "Markdown; keep headings, bullets and links."})
    sp = load(os.path.join(D, "signal_projections.json"), {})
    for j, e in enumerate(sp.get("projections", [])):
        f = {k: e[k] for k in ("mechanism", "judgement", "contrast") if isinstance(e.get(k), str)}
        if e.get("anchors"):
            f["anchors"] = "\n\n".join(e["anchors"])
        items.append({"id": f"sigproj:{j}", "kind": "sigproj", "title": f"{e.get('country')} {e.get('metric')}", "fields": f, "note": "'anchors' is several points separated by a blank line; same number, same order."})
    return items

def batch(items, max_chars):
    out, cur, size = [], [], 0
    for it in sorted(items, key=lambda x: (x["kind"], x["id"])):
        s = sum(len(v) for v in it["fields"].values())
        if cur and (size + s > max_chars or cur[0]["kind"] != it["kind"]):
            out.append(cur); cur, size = [], 0
        cur.append(it); size += s
    if cur:
        out.append(cur)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--work", required=True)
    ap.add_argument("--max-chars", type=int, default=60000); ap.add_argument("--since", default=None)
    a = ap.parse_args()
    os.makedirs(os.path.join(a.work, "items"), exist_ok=True); os.makedirs(os.path.join(a.work, "out"), exist_ok=True)
    io.open(os.path.join(a.work, "STYLE.md"), "w", encoding="utf-8").write(style_text(a.root))
    items = collect(a.root, a.since)
    batches = batch(items, a.max_chars)
    man = []
    for i, bt in enumerate(batches):
        p = os.path.join(a.work, "items", f"batch{i:02d}.json")
        json.dump(bt, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        man.append({"file": p, "kind": bt[0]["kind"], "n": len(bt)})
    json.dump({"batches": man}, io.open(os.path.join(a.work, "manifest.json"), "w", encoding="utf-8"), indent=1)
    print("items:", len(items), "| chars:", sum(len(v) for it in items for v in it["fields"].values()) // 1000, "k",
          "| batches:", len(batches), dict(Counter(b[0]["kind"] for b in batches)))

if __name__ == "__main__":
    main()
