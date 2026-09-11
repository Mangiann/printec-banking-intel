#!/usr/bin/env python3
"""plain_check.py — did a plain-English rewrite keep every fact?

Compares an original text with its rewrite and reports anything that went missing: numbers,
percentages, money amounts, dates, years, URLs and markdown link targets. Wording may change freely;
figures may not. Used after the one-off rewrite (09/09/2026) and by the weekly editing step.

  from plain_check import lost_facts
  lost_facts(old, new) -> list of (token, count_in_old, count_in_new); [] means nothing was lost
"""
import re
from collections import Counter

# What counts as a FACT that must survive a rewrite: numbers, dates, URLs, and currency codes that sit
# next to an amount. A currency code on its own is not a fact — and treating the Albanian lek code "ALL"
# as one made every emphatic "ALL" look like a lost figure, exactly where the writing policy tells the
# editor to remove ALL-CAPS emphasis.
_TOK = re.compile(
    r"https?://[^\s)\]>\"']+"                                   # URLs
    r"|\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b"                          # 27/08/2026, 1.1.2027
    r"|\b\d[\d,.]*\s?(?:%|[bB][nN]|[mM]\b|[kK]\b|[mM]illion|[bB]illion|[tT]housand)?"   # numbers, %, money-ish suffixes
    r"|(?:(?<=\d\s)|(?<=\d))(?:EUR|USD|GBP|RSD|UAH|HRK|RON|BGN|HUF|CZK|PLN|ALL|MKD|KM|lek)\b"   # 5m EUR
    r"|\b(?:EUR|USD|GBP|RSD|UAH|HRK|RON|BGN|HUF|CZK|PLN|ALL|MKD|KM|lek)(?=\s?\d)")               # EUR 5m
# "(1)", "(2)" opening a clause are list markers, not facts — the policy asks for them to become bullets.
# A reference glued to what precedes it, like "Article 5(1)", is a fact and is left alone.
_LIST_MARKER = re.compile(r"(?:(?<=^)|(?<=[\s(\[.;:—-]))\(\d{1,2}\)")

def _norm(t):
    t = t.strip().strip(".,;:")
    t = re.sub(r"\s+", "", t)
    return t.lower()

def facts(text):
    t = _LIST_MARKER.sub(" ", text or "")
    return Counter(_norm(x) for x in _TOK.findall(t) if _norm(x))

def lost_facts(old, new):
    co, cn = facts(old), facts(new)
    return [(k, co[k], cn[k]) for k in co if cn[k] < co[k]]

def links(text):
    return Counter(re.findall(r"\]\((https?://[^)\s]+)\)", text or ""))

def lost_links(old, new):
    co, cn = links(old), links(new)
    return [(k, co[k], cn[k]) for k in co if cn[k] < co[k]]

if __name__ == "__main__":
    import sys, json
    a, b = open(sys.argv[1], encoding="utf-8").read(), open(sys.argv[2], encoding="utf-8").read()
    print(json.dumps({"lost_facts": lost_facts(a, b), "lost_links": lost_links(a, b)}, indent=1))
