#!/usr/bin/env python3
"""
add_competitor.py - safely append a NEWLY-DISCOVERED competitor to references/competitors.json.

Determinism-in-plumbing split: Agent 6 does the JUDGEMENT (is this a real, new competitor? what
tier/products/countries?), this script does the safe JSON WRITE + DEDUP so an LLM never hand-edits
the roster and never adds a duplicate. Idempotent: if the name OR any detect token already matches
an existing vendor, it is a no-op (prints EXISTS), so it is safe to call for every candidate.

Usage:
  python add_competitor.py --file <competitors.json> --name "FooPay" \
     --tier local-peer --countries RO,BG --products pos_acquiring,payments_instant \
     --detect "foopay,foo pay srl" --latest "Won X bank SoftPOS tender (source, DD/MM/YYYY)" \
     --source-title "ZF" --source-url "https://..." --origin agent6-2026-06-25

Roles: competitor|partner|both|oem|software (default competitor). Tier: global|regional|local-peer.
If --detect is omitted it is derived from the name. Exit 0 on add OR on dedup no-op; non-zero only
on bad input / write error (so a weekly batch never aborts mid-loop).
"""
import argparse, json, io, os, re, sys

VALID_ROLE = {"competitor", "partner", "both", "oem", "software"}
VALID_TIER = {"global", "regional", "local-peer"}


def toks(s):
    return [t.strip().lower() for t in (s or "").split(",") if t.strip()]


def name_variants(name):
    n = name.strip().lower()
    out = {n}
    out.add(re.sub(r"\s*\([^)]*\)", "", n).strip())          # drop "(...)"
    out.add(re.sub(r"[.,]", "", n).strip())                    # drop punctuation
    return {v for v in out if v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--role", default="competitor")
    ap.add_argument("--tier", default="local-peer")
    ap.add_argument("--threat", default="Medium")
    ap.add_argument("--countries", default="")
    ap.add_argument("--products", default="")
    ap.add_argument("--detect", default="")
    ap.add_argument("--latest", default="")
    ap.add_argument("--source-title", default="")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--origin", default="agent6")
    a = ap.parse_args()

    if a.role not in VALID_ROLE:
        print(f"BAD role {a.role!r} (use {sorted(VALID_ROLE)})"); return 2
    if a.tier not in VALID_TIER:
        print(f"BAD tier {a.tier!r} (use {sorted(VALID_TIER)})"); return 2
    if not os.path.exists(a.file):
        print(f"BAD file {a.file}"); return 2

    doc = json.load(io.open(a.file, encoding="utf-8"))
    vendors = doc.get("vendors", [])

    detect = toks(a.detect) or sorted(name_variants(a.name))
    cand_keys = set(detect) | name_variants(a.name)

    # DEDUP: match against existing names + detect tokens
    for v in vendors:
        existing = name_variants(v.get("name", "")) | {d.strip().lower() for d in v.get("detect", [])}
        if cand_keys & existing:
            print(f"EXISTS: '{a.name}' already covered by '{v.get('name')}' (overlap: {sorted(cand_keys & existing)[:3]}) - no change")
            return 0

    entry = {
        "name": a.name.strip(),
        "role": a.role,
        "threat": a.threat,
        "tier": a.tier,
        "detect": detect,
        "countries": [c.upper() for c in toks(a.countries)],
        "products": toks(a.products),
        "latest": a.latest.strip(),
        "origin": a.origin,
    }
    if a.source_url:
        entry["sources"] = [{"title": a.source_title or a.name, "url": a.source_url}]

    vendors.append(entry)
    out = json.dumps(doc, ensure_ascii=False, indent=2)
    json.loads(out)  # validate
    io.open(a.file, "w", encoding="utf-8", newline="\n").write(out + "\n")
    print(f"ADDED: {a.name} (role={a.role}, tier={a.tier}, countries={entry['countries']}) -> vendors now {len(vendors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
