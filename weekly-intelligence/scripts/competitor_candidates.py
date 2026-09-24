#!/usr/bin/env python3
"""
competitor_candidates.py - close the hand-over gap between the agents and the competitor watchlist.

Why: on 18/09/2026 the user found that Novidea (installer of Eurobank's 450+ GRGBanking recyclers in
Greece) was never a competitor on the dashboard. The bank-disclosures agent had named it twice, in its
own findings, but only the vendor agent adds names to references/competitors.json, and it never reads
the other agents' findings. This script scans EVERY agent's findings for vendor-like names that the
watchlist does not know and writes a candidate list for the vendor agent to triage each week.

It is deliberately generous (recall over precision): a human or the vendor agent decides; this script
only makes sure nothing named as a competitor, incumbent, integrator, installer, supplier or winner
stays buried in a findings file.

Usage:
  python competitor_candidates.py [--root <BANKING>] [--since YYYY-MM-DD]
Writes intel-cache/competitor_candidates.json and intel-cache/COMPETITOR_CANDIDATES.md
"""
import argparse, glob, json, os, re, sys, datetime
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# a name is a candidate only when it sits right after a cue that says who supplies, integrates, installs,
# maintains, wins or competes ("integrator = X", "maintenance by X", "awarded to X", "incumbent X (…)")
CUE_NAME = re.compile(r"\b(competitors?|incumbents?|integrators?|installers?|installation|install|maintenance|maintained|supplied|suppliers?|vendors?|awarded to|won by|winners?|displac\w+|rivals?|operated by|provided by|deployed by|delivered by|contracted to|contract (?:to|with)|partnered with|subcontract\w*)"
                      r"[^A-Za-z0-9\n]{0,6}(?:=|:|is|was|by|of|are|were|include[sd]?|named|being)?\s*"
                      r"([A-Z][\w&+\-\.]{1,}(?:\s+(?:[A-Z][\w&+\-\.]+|SEE|AG|AD|SA|S\.A\.|d\.o\.o\.|Kft\.|Zrt\.|s\.r\.o\.|Ltd|LLC|Group)){0,3})")
# the same, name before the cue: "Novidea (local installer)", "GRGBanking incumbent"
NAME_CUE = re.compile(r"([A-Z][\w&+\-\.]{2,}(?:\s+[A-Z][\w&+\-\.]+){0,2})\s*(?:\(|,|\s)\s*(?i:(?:is |the |a |an )?(?:local |direct |current |new )?(?:competitor|incumbent|integrator|installer|rival|supplier|vendor|winner))\b")
CUES = re.compile(r"\b(competitor|incumbent|integrator|installer|install|maintenance|supplier|vendor|awarded to|won by|winner|displace|rival|operated by|provided by|deployed by|delivered by|contracted to|contract to|contract with|partnered with|subcontract)\w*", re.I)
# words that look like names but are not vendors
STOP = set("""The This That These Those Bank Banks Group Greece Bulgaria Romania Serbia Croatia Slovenia Slovakia Hungary Cyprus Ukraine Albania Kosovo Montenegro Bosnia Herzegovina Macedonia North Czech Czechia Republic Europe European EU ECB EBA NBG NBU NBS MNB HNB BNB CNB CBBiH ATM ATMs POS CIT AML KYC HSM ISO SEPA IBAN Verification Payee Instant Payments Regulation Q1 Q2 Q3 Q4 H1 H2 FY January February March April May June July August September October November December Monday Tuesday Wednesday Thursday Friday NEW UPDATE STANDING RESOLVED CORRECTED Low Medium High XL Source Sources Confidence Printec Agent Signal Signals Vendor Vendors Competitor Competitors Incumbent Integrator Tender Tenders Award Awards Contract Notice Deadline Board Branch Branches Digital Mobile Online Web App Note Notes Table Row Rows Yes No Not None See Also And Or Of In On At To For With From By Per Via A An As Is Are Was Were Be Been Greek Serbian Croatian Romanian Slovenian Slovak Bulgarian Hungarian Cypriot Ukrainian Albanian Kosovar Montenegrin Bosnian Macedonian Czech Implies Follow-up Confirm Prozorro EDRPOU TED Unscoped AWARDED WINNER HTTP HTTPS PDF URL Lot Lots Phase Stage Status Verified Primary Secondary Date Dated Value Values EUR USD UAH RON BGN RSD HRK CZK HUF Total Yes Unknown TBD If Then When Where Which Who What Why How Local Direct Current Existing Same Other Another All Any Each Every Both Two Three Four Five One First Second Third Last Next Prior Previous""".split())
COUNTRY_ADJ = re.compile(r"^(Polish|Greek|Serbian|Croatian|Romanian|Slovenian|Slovak|Bulgarian|Hungarian|Cypriot|Ukrainian|Albanian|Kosovar|Montenegrin|Bosnian|Macedonian|Czech|European|Austrian|German|Italian|Turkish|Chinese|Korean|Japanese|American|British)\b")

def load_watchlist(refs):
    with open(os.path.join(refs, "competitors.json"), encoding="utf-8") as f:
        W = json.load(f)
    toks = set()
    for v in W.get("vendors", []):
        toks.add(v["name"].lower())
        for d in v.get("detect", []):
            toks.add(str(d).lower())
    return W, toks

def known(name, toks):
    n = name.lower()
    return any(t and (t in n or n in t) for t in toks)

def bank_names(root):
    """banks and buyers the findings name most (so they are not proposed as competitors)."""
    out = set()
    p = os.path.join(root, "intel-cache", "dashboard-data.json")
    if os.path.exists(p):
        try:
            D = json.load(open(p, encoding="utf-8"))
            for s in D.get("signals", []):
                t = (s.get("bank_theme") or "").split(" — ")[0].split(" - ")[0].strip()
                if 2 < len(t) < 60:
                    out.add(t.lower())
        except Exception:
            pass
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--since", default=None, help="only findings files dated on/after this day (YYYY-MM-DD)")
    a = ap.parse_args()
    refs = os.path.join(a.root, "weekly-intelligence", "references")
    W, toks = load_watchlist(refs)
    banks = bank_names(a.root)
    files = sorted(glob.glob(os.path.join(a.root, "findings", "**", "*.md"), recursive=True))
    if a.since:
        files = [f for f in files if re.search(r"\d{4}-\d{2}-\d{2}", f) and re.search(r"\d{4}-\d{2}-\d{2}", f).group(0) >= a.since]
    cand = defaultdict(lambda: {"count": 0, "files": set(), "cues": set(), "examples": []})
    # ordinary words: anything that also appears in lower case in the corpus is a word, not a name
    corpus = " ".join(open(f, encoding="utf-8", errors="ignore").read() for f in files)
    lower_words = set(re.findall(r"(?<![A-Za-z])[a-z][a-z\-]{2,}(?![A-Za-z])", corpus))
    for f in files:
        agent = os.path.relpath(f, os.path.join(a.root, "findings")).split(os.sep)[0]
        try:
            text = open(f, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for line in text.splitlines():
            if not CUES.search(line):
                continue
            found = [m.group(2) for m in CUE_NAME.finditer(line)] + [m.group(1) for m in NAME_CUE.finditer(line)]
            for raw in found:
                name = raw.strip(" .,;:()")
                name = re.sub(r"\s+(?:is|was|has|have|had|will|and|or|for|with|in|on|at|to|of)$", "", name)
                words = name.split()
                if len(name) < 4 or len(words) > 4 or not words or not words[0][0].isupper() or words[0] in STOP or all(w in STOP for w in words) or COUNTRY_ADJ.match(name):
                    continue
                if known(name, toks) or any(b.startswith(name.lower()) or name.lower().startswith(b) for b in banks if len(b) > 3) or re.search(r"\b(bank|banka|banca|banque|post|posta|pošta|ministry|agency|authority|central|university|municipality|city|county|fund)\b", name, re.I):
                    continue
                if name.isupper() and len(name) <= 3:
                    continue
                if len(words) == 1 and (name.lower() in lower_words or name.lower().rstrip("s") in lower_words):
                    continue      # "Capture", "AWARD", "Standing" are words, not vendors
                if re.search(re.escape(name) + r"\s*(?:\(|,)?\s*(?:bank|banka|banca|banque|bankë|štedionica|d\.d\.)\b", line, re.I):
                    continue      # "Zagrebačka banka", "SZRB, bank": a bank, not a vendor
                c = cand[name]
                c["count"] += 1; c["files"].add(os.path.relpath(f, a.root)); c["cues"].add(CUES.search(line).group(1).lower())
                if len(c["examples"]) < 2:
                    c["examples"].append(re.sub(r"\s+", " ", line.strip())[:220])
    # rank: named in several files or with strong cues first
    strong = {"competitor", "incumbent", "integrator", "installer", "winner", "won by", "awarded to", "displace", "rival"}
    rows = []
    for name, c in cand.items():
        score = c["count"] + 3 * len(c["files"]) + (5 if c["cues"] & strong else 0)
        rows.append({"name": name, "score": score, "mentions": c["count"], "files": sorted(c["files"]), "cues": sorted(c["cues"]), "examples": c["examples"]})
    rows.sort(key=lambda r: -r["score"])
    rows = [r for r in rows if r["score"] >= 5][:120]
    out = {"generated": datetime.date.today().isoformat(), "watchlist_size": len(W.get("vendors", [])), "files_scanned": len(files), "candidates": rows,
           "note": "Candidates only. The vendor agent decides: add real Printec competitors with scripts/add_competitor.py, ignore banks, buyers, regulators and partners."}
    cdir = os.path.join(a.root, "intel-cache"); os.makedirs(cdir, exist_ok=True)
    with open(os.path.join(cdir, "competitor_candidates.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    L = ["# Competitor candidates not on the watchlist (%s)" % out["generated"], "",
         "Scanned %d findings files from every agent; watchlist has %d vendors. Each name below was written next to a cue such as "
         "competitor, incumbent, integrator, installer, supplier or winner and is NOT matched by any watchlist detect token. "
         "Triage each one: add real Printec competitors with `scripts/add_competitor.py`; ignore banks, buyers, regulators and partners." % (len(files), out["watchlist_size"]), "",
         "| # | Name | Mentions | Files | Cues | Example |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        L.append("| %d | %s | %d | %s | %s | %s |" % (i, r["name"], r["mentions"], "; ".join(os.path.basename(x) for x in r["files"][:3]), ", ".join(r["cues"][:3]), (r["examples"][0] if r["examples"] else "").replace("|", "/")[:160]))
    with open(os.path.join(cdir, "COMPETITOR_CANDIDATES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("scanned %d files; %d candidates -> intel-cache/COMPETITOR_CANDIDATES.md" % (len(files), len(rows)))
    for r in rows[:15]:
        print("  %-40s %2d mentions  %s" % (r["name"][:40], r["mentions"], ", ".join(r["cues"][:3])))

if __name__ == "__main__":
    main()
