#!/usr/bin/env python3
"""plain_retry.py — build a retry batch from what plain_merge.py refused.

Reads <work>/failed.json and the original items, and writes <work>/items/retryNN.json holding only the
fields that failed, each with the reason attached to its note so the second pass knows what went wrong.

  python plain_retry.py --work <dir> [--max-chars 40000]
"""
import argparse, json, os, io

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--work", required=True); ap.add_argument("--max-chars", type=int, default=40000)
    a = ap.parse_args()
    f = json.load(io.open(os.path.join(a.work, "failed.json"), encoding="utf-8"))
    orig = {}
    for fn in sorted(os.listdir(os.path.join(a.work, "items"))):
        if fn.startswith("batch"):
            for it in json.load(io.open(os.path.join(a.work, "items", fn), encoding="utf-8")):
                orig[it["id"]] = it
    want = {}
    for x in f.get("failed", []):
        it = orig.get(x["id"])
        if not it or x["field"] not in it["fields"]:
            continue
        w = want.setdefault(x["id"], {"id": it["id"], "kind": it["kind"], "title": it["title"], "fields": {}, "note": it.get("note", "")})
        w["fields"][x["field"]] = it["fields"][x["field"]]
        why = x.get("why", "")
        if x.get("lost_facts"):
            why += " — these must appear exactly as in the original: " + ", ".join(k for k, _, _ in x["lost_facts"][:12])
        if x.get("lost_links"):
            why += " — these link URLs must stay: " + ", ".join(k for k, _, _ in x["lost_links"][:6])
        w["note"] = (w["note"] + " | PREVIOUS ATTEMPT FAILED on '%s': %s" % (x["field"], why)).strip(" |")
    for iid in f.get("missing", []):
        it = orig.get(iid)
        if it:
            want[iid] = dict(it)
    items = list(want.values())
    out, cur, size = [], [], 0
    for it in sorted(items, key=lambda x: (x["kind"], x["id"])):
        s = sum(len(v) for v in it["fields"].values())
        if cur and size + s > a.max_chars:
            out.append(cur); cur, size = [], 0
        cur.append(it); size += s
    if cur:
        out.append(cur)
    man = []
    for i, bt in enumerate(out):
        p = os.path.join(a.work, "items", f"retry{i:02d}.json")
        json.dump(bt, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        man.append({"file": p, "kind": "retry", "n": len(bt)})
    json.dump({"batches": man}, io.open(os.path.join(a.work, "retry_manifest.json"), "w", encoding="utf-8"), indent=1)
    print("retry items:", len(items), "| batches:", len(out))

if __name__ == "__main__":
    main()
