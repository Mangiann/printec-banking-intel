#!/usr/bin/env python3
"""product_critic.py - the product-line critic step (decision of 09/09/2026).

ingest.py tags a signal with EVERY product category whose keywords appear anywhere in its text.
A long signal that mentions ATMs, POS, onboarding and DORA in passing therefore lands in six or
seven categories, most of them not what the signal is about. This step hands each signal to an
LLM critic that reads the whole row and keeps only the categories the signal is really about
(one lead, at most three in total). The verdicts live in
weekly-intelligence/references/product_review.json; ingest.py applies them on every run, so the
critic only needs to look at signals it has not seen, or whose text has changed since.

Two sub-commands:

  batches  --root <BANKING> --work <dir> [--all] [--batch-size 24]
      Writes <dir>/TAXONOMY.md (the categories and the rules), <dir>/items/batchNN.json (the
      signals to judge, with the keyword tags for reference) and <dir>/manifest.json. Only
      signals without a current verdict are included unless --all is given.

  merge    --root <BANKING> --work <dir> [--week YYYY-MM-DD]
      Reads <dir>/out/batchNN.json (a JSON array of {"key","products","why"}), validates every
      verdict against product_map.json, and writes the accepted ones into product_review.json.
      Anything malformed is listed in <dir>/failed.json and left unreviewed.

Then re-run ingest.py (or run_weekly.py) so the verdicts reach the dashboard.
"""
import argparse, datetime, hashlib, json, os, re, sys

MAX_PRODUCTS = 3

def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default

def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s or "")
    return re.sub(r"[*_`]+", "", s).strip()

def text_hash(sig):
    blob = "\n".join(strip_md(sig.get(k) or "") for k in ("bank_theme", "signal", "implies", "follow_up"))
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]

def paths(root):
    skill = os.path.join(root, "weekly-intelligence")
    return {"signals": os.path.join(root, "intel-cache", "signals.json"),
            "product_map": os.path.join(skill, "references", "product_map.json"),
            "review": os.path.join(skill, "references", "product_review.json")}

def load_signals(p):
    raw = load(p["signals"], [])
    return raw if isinstance(raw, list) else raw.get("signals", [])

def taxonomy_md(product_map):
    lines = ["# Product-line taxonomy and the critic's rules", "",
             "Each signal in the batch file is a row from the Printec market-intelligence table. Decide which",
             "Printec product line or lines the signal is really about. Return the category ids only.", "",
             "## Categories", ""]
    for c in product_map["categories"]:
        lines.append("- `%s` — **%s**. Printec sells: %s" % (c["id"], c["label"], c.get("printec", "")))
    lines += ["", "## Rules", "",
              "1. Read the whole row: the theme, the signal text, what it implies and the recommended follow-up.",
              "2. Keep only the categories the signal creates demand for, or directly changes the market of.",
              "   A word that appears in passing is not a category. A bank's ATM count mentioned in an",
              "   annual report about card growth does not make the signal an ATM signal.",
              "3. Return one to %d categories. Put the lead category first. Most signals have one or two." % MAX_PRODUCTS,
              "4. The `keyword_products` field is what the keyword matcher found. It is a hint, not an answer.",
              "   Drop what is not relevant. You may add a category the keywords missed if the row clearly calls for it.",
              "5. A pure market or regulatory backdrop with no Printec line still gets its closest category",
              "   (for example a cash-usage statistic belongs to `atm_recycling`).",
              "6. Give a `why` of one short sentence in plain English. Do not restate the signal.",
              "", "## Output", "",
              "Write `<work>/out/<same batch name>.json` as a JSON array, one object per input item, same keys:",
              "", "```json", '[{"key": "<key>", "products": ["<lead id>", "<id>"], "why": "<one sentence>"}]', "```", ""]
    return "\n".join(lines)

def cmd_batches(args):
    p = paths(args.root)
    pm = load(p["product_map"])
    ids = {c["id"] for c in pm["categories"]}
    sigs = load_signals(p)
    review = (load(p["review"], {}) or {}).get("reviews", {})
    todo = []
    for s in sigs:
        h = text_hash(s)
        r = review.get(s["key"])
        if args.all or not r or r.get("text_hash") != h:
            todo.append(s)
    os.makedirs(os.path.join(args.work, "items"), exist_ok=True)
    os.makedirs(os.path.join(args.work, "out"), exist_ok=True)
    with open(os.path.join(args.work, "TAXONOMY.md"), "w", encoding="utf-8") as fh:
        fh.write(taxonomy_md(pm))
    n = args.batch_size
    batches = [todo[i:i + n] for i in range(0, len(todo), n)]
    manifest = []
    for i, b in enumerate(batches, 1):
        name = "batch%02d.json" % i
        items = [{"key": s["key"], "bank_theme": strip_md(s.get("bank_theme")),
                  "country": s.get("country_raw"), "signal": strip_md(s.get("signal")),
                  "implies": strip_md(s.get("implies")), "follow_up": strip_md(s.get("follow_up")),
                  "keyword_products": [x for x in (s.get("products") or []) if x in ids],
                  "text_hash": text_hash(s)} for s in b]
        with open(os.path.join(args.work, "items", name), "w", encoding="utf-8") as fh:
            json.dump(items, fh, ensure_ascii=False, indent=1)
        manifest.append({"batch": name, "n": len(items), "keys": [s["key"] for s in b]})
    with open(os.path.join(args.work, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"signals_total": len(sigs), "to_review": len(todo), "batches": manifest},
                  fh, ensure_ascii=False, indent=1)
    print("product critic: %d of %d signal(s) need a verdict -> %d batch(es) in %s"
          % (len(todo), len(sigs), len(batches), args.work))

def cmd_merge(args):
    p = paths(args.root)
    pm = load(p["product_map"])
    ids = [c["id"] for c in pm["categories"]]
    sigs = {s["key"]: s for s in load_signals(p)}
    rev = load(p["review"], None) or {
        "_note": ("Product-line verdicts from the LLM critic (agent-briefs/10-product-critic.md). ingest.py "
                  "replaces the keyword-matched product list of a signal with the verdict here, lead first, "
                  "when the key is present. text_hash is the signal text the verdict was made on; when the "
                  "text changes, product_critic.py batches lists the signal again. Edit by hand only to "
                  "correct a verdict; keep products to taxonomy ids from product_map.json."),
        "reviews": {}}
    reviews = rev.setdefault("reviews", {})
    week = args.week or datetime.date.today().isoformat()
    items_dir, out_dir = os.path.join(args.work, "items"), os.path.join(args.work, "out")
    failed, accepted, changed, no_out = [], 0, 0, []
    for name in sorted(os.listdir(items_dir)):
        if not name.endswith(".json"):
            continue
        items = {it["key"]: it for it in load(os.path.join(items_dir, name), [])}
        out = load(os.path.join(out_dir, name), None)
        if out is None:
            no_out.append(name); continue
        if isinstance(out, dict):
            out = out.get("items") or out.get("results") or []
        seen = set()
        for o in out:
            key = (o or {}).get("key")
            it = items.get(key)
            if not it or key in seen:
                failed.append({"batch": name, "key": key, "reason": "unknown or duplicate key"}); continue
            seen.add(key)
            prods = [x for x in (o.get("products") or []) if isinstance(x, str)]
            bad = [x for x in prods if x not in ids]
            uniq = []
            for x in prods:
                if x in ids and x not in uniq:
                    uniq.append(x)
            if bad or not uniq or len(uniq) > MAX_PRODUCTS:
                failed.append({"batch": name, "key": key, "products": prods,
                               "reason": ("unknown id(s) %s" % bad) if bad else
                                         ("no products" if not uniq else "more than %d products" % MAX_PRODUCTS)})
                continue
            why = strip_md(str(o.get("why") or "")).strip()
            before = it.get("keyword_products") or []
            reviews[key] = {"products": uniq, "primary_product": uniq[0], "why": why,
                            "keyword_products": before, "text_hash": it["text_hash"], "reviewed": week}
            accepted += 1
            if uniq != before:
                changed += 1
        missing = [k for k in items if k not in seen]
        for k in missing:
            failed.append({"batch": name, "key": k, "reason": "no verdict in the output file"})
    with open(p["review"], "w", encoding="utf-8") as fh:
        json.dump(rev, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(args.work, "failed.json"), "w", encoding="utf-8") as fh:
        json.dump(failed, fh, ensure_ascii=False, indent=1)
    # a short account of what the critic did, for the run note
    from collections import Counter
    n_before = Counter(len(r["keyword_products"]) for r in reviews.values())
    n_after = Counter(len(r["products"]) for r in reviews.values())
    print("product critic: %d verdict(s) accepted, %d differ from the keyword tags, %d refused, %d batch(es) without output"
          % (accepted, changed, len(failed), len(no_out)))
    if no_out:
        print("  no output for: %s" % ", ".join(no_out))
    print("  categories per signal, keyword matcher: %s" % dict(sorted(n_before.items())))
    print("  categories per signal, after the critic: %s" % dict(sorted(n_after.items())))
    print("  %d verdict(s) on file in %s" % (len(reviews), p["review"]))
    return 1 if no_out else 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("batches"); b.add_argument("--root", required=True); b.add_argument("--work", required=True)
    b.add_argument("--all", action="store_true", help="re-judge every signal, not only the unreviewed ones")
    b.add_argument("--batch-size", type=int, default=24)
    m = sub.add_parser("merge"); m.add_argument("--root", required=True); m.add_argument("--work", required=True)
    m.add_argument("--week", default=None)
    args = ap.parse_args()
    if args.cmd == "batches":
        cmd_batches(args)
    else:
        sys.exit(cmd_merge(args))

if __name__ == "__main__":
    main()
