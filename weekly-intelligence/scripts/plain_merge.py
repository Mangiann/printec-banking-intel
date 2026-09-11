#!/usr/bin/env python3
"""plain_merge.py — write plain-English rewrites back, but only where every fact survived.

Reads <work>/items/batchNN.json (originals) and <work>/out/batchNN.json (rewrites), checks each field
with plain_check (numbers, dates, money, URLs, links), and writes the passing fields back into the
source files. Failing fields are left as they were and listed in <work>/failed.json so a second pass
can redo just those. Nothing is written for a field that lost a single figure.

  python plain_merge.py --root <BANKING> --work <dir> [--dry-run]
"""
import argparse, json, os, io, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plain_check import lost_facts, lost_links

PROSE_COLS = {"signal": "Signal", "implies": "What it implies", "follow_up": "Recommended follow-up"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--work", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    D = os.path.join(a.root, "intel-cache")
    orig, new = {}, {}
    for fn in sorted(os.listdir(os.path.join(a.work, "items"))):
        for it in json.load(io.open(os.path.join(a.work, "items", fn), encoding="utf-8")):
            orig[it["id"]] = it
    outdir = os.path.join(a.work, "out")
    for fn in sorted(os.listdir(outdir)) if os.path.isdir(outdir) else []:
        try:
            for it in json.load(io.open(os.path.join(outdir, fn), encoding="utf-8")):
                new[it["id"]] = it.get("fields", {})
        except Exception as e:
            print("unreadable result file:", fn, e)

    ok, failed, missing = {}, [], []
    for iid, it in orig.items():
        if iid not in new:
            missing.append(iid); continue
        good = {}
        for k, old in it["fields"].items():
            nw = new[iid].get(k)
            if not isinstance(nw, str) or not nw.strip():
                failed.append({"id": iid, "field": k, "why": "no rewrite returned"}); continue
            if it["kind"] == "signal" and ("|" in nw or "\n" in nw):
                failed.append({"id": iid, "field": k, "why": "table cell contains '|' or a line break"}); continue
            lf, ll = lost_facts(old, nw), lost_links(old, nw)
            if lf or ll:
                failed.append({"id": iid, "field": k, "why": "lost facts", "lost_facts": lf[:12], "lost_links": ll[:6]}); continue
            # a short title may grow when a headline becomes a plain description ("The endgame" ->
            # "Who operates the shared infrastructure"); long prose may not balloon
            limit = 3.0 if len(old) < 120 else 1.6
            if len(nw) > len(old) * limit:
                failed.append({"id": iid, "field": k, "why": "much longer than the original (%d -> %d chars)" % (len(old), len(nw))}); continue
            good[k] = nw
        if good:
            ok[iid] = good
    print("items: %d | with a usable rewrite: %d | fields failed: %d | items with no result: %d"
          % (len(orig), len(ok), len(failed), len(missing)))
    json.dump({"failed": failed, "missing": missing}, io.open(os.path.join(a.work, "failed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.dry_run:
        return

    # ---- write back ----
    w = {"rows": 0, "fields": 0}
    def put(iid, key, text):
        w["fields"] += 1
    # master table
    rows = {int(i.split(":")[1]): f for i, f in ok.items() if i.startswith("row:")}
    if rows:
        p = os.path.join(a.root, "master-signal-table.md")
        L = io.open(p, encoding="utf-8").read().split("\n")
        hdr_i = next(i for i, l in enumerate(L) if l.startswith("|") and "Bank / Theme" in l)
        hdr = [c.strip() for c in L[hdr_i].strip().strip("|").split("|")]
        col = {h: i for i, h in enumerate(hdr)}
        for li, f in rows.items():
            cells = [c.strip() for c in L[li].strip().strip("|").split("|")]
            if len(cells) != len(hdr):
                continue
            for k, txt in f.items():
                cells[col[PROSE_COLS[k]]] = txt.strip(); put(li, k, txt)
            L[li] = "| " + " | ".join(cells) + " |"; w["rows"] += 1
        io.open(p, "w", encoding="utf-8").write("\n".join(L))
    def upd_json(path, apply):
        d = json.load(io.open(path, encoding="utf-8")); apply(d)
        json.dump(d, io.open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    def split_pts(s): return [x.strip() for x in re.split(r"\n\s*\n", s) if x.strip()]
    # outlooks
    def ap_fn(d):
        for kind, arr in (("outlook", d.get("outlooks", [])), ("product_outlook", d.get("product_outlooks", []))):
            for o in arr:
                f = ok.get(f"{kind}:{o['oid']}")
                if not f: continue
                for k, v in f.items():
                    if k == "drivers":
                        pts = split_pts(v)
                        if len(pts) == len(o.get("drivers", [])): o["drivers"] = pts; put(o['oid'], k, v)
                    else: o[k] = v; put(o['oid'], k, v)
    if any(i.startswith(("outlook:", "product_outlook:")) for i in ok): upd_json(os.path.join(D, "forecast_narrative.json"), ap_fn)
    def ap_fu(d):
        for c in d.get("futures", []):
            f = ok.get(f"future:{c['oid']}")
            if not f: continue
            for k, v in f.items():
                if k == "drivers":
                    pts = split_pts(v)
                    if len(pts) == len(c.get("drivers", [])): c["drivers"] = pts; put(c['oid'], k, v)
                else: c[k] = v; put(c['oid'], k, v)
        b = d.get("board_view", {})
        bl = b.get("bottom_line") or {}
        f = ok.get("bottom:main")
        if f and bl:
            for k, v in f.items():
                if k == "picture":
                    bl["picture"] = split_pts(v); put("bottom", k, v)
                else: bl[k] = v; put("bottom", k, v)
        for sec in ("drivers", "gems"):
            for j, g in enumerate(bl.get(sec) or []):
                f = ok.get(f"bottom:{sec}:{j}")
                if f:
                    for k, v in f.items(): g[k] = v; put(sec, k, v)
        for j, r in enumerate(bl.get("endstate_2030") or []):
            f = ok.get(f"bottom:endstate:{j}")
            if f:
                for k, v in f.items(): r[k] = v; put("endstate", k, v)
        for k, tk in (("money", "note"), ("competition", "note"), ("threats", "note"), ("timeline", "event")):
            for j, r in enumerate(b.get(k) or []):
                f = ok.get(f"board:{k}:{j}")
                if f and tk in f: r[tk] = f[tk]; put(k, tk, f[tk])
    if any(i.startswith(("future:", "board:", "bottom:")) for i in ok): upd_json(os.path.join(D, "futures_narrative.json"), ap_fu)
    def ap_kb(d):
        arr = d if isinstance(d, list) else d.get("patterns", [])
        for j, p in enumerate(arr):
            f = ok.get(f"pattern:{j}")
            if f:
                for k, v in f.items(): p[k] = v; put(j, k, v)
    if any(i.startswith("pattern:") for i in ok): upd_json(os.path.join(D, "patterns_kb.json"), ap_kb)
    def ap_cp(d):
        for j, v in enumerate(d.get("vendors", [])):
            f = ok.get(f"competitor:{j}")
            if f and "latest" in f: v["latest"] = f["latest"]; put(j, "latest", f["latest"])
    if any(i.startswith("competitor:") for i in ok): upd_json(os.path.join(a.root, "weekly-intelligence", "references", "competitors.json"), ap_cp)
    def ap_dv(d):
        arr = d if isinstance(d, list) else d.get("derived", d)
        for j, x in enumerate(arr or []):
            f = ok.get(f"derived:{j}")
            if f:
                for k, v in f.items(): x[k] = v; put(j, k, v)
    if any(i.startswith("derived:") for i in ok): upd_json(os.path.join(D, "derived_opportunities.json"), ap_dv)
    if "brief:0" in ok:
        def ap_cb(d):
            if isinstance(d, dict): d["brief"] = ok["brief:0"]["brief"]; put(0, "brief", "")
        upd_json(os.path.join(D, "competition_brief.json"), ap_cb)
    def ap_sp(d):
        for j, e in enumerate(d.get("projections", [])):
            f = ok.get(f"sigproj:{j}")
            if not f: continue
            for k, v in f.items():
                if k == "anchors":
                    pts = split_pts(v)
                    if len(pts) == len(e.get("anchors", [])): e["anchors"] = pts; put(j, k, v)
                else: e[k] = v; put(j, k, v)
    if any(i.startswith("sigproj:") for i in ok): upd_json(os.path.join(D, "signal_projections.json"), ap_sp)
    print("written back: %d master-table rows, %d fields in total" % (w["rows"], w["fields"]))

if __name__ == "__main__":
    main()
