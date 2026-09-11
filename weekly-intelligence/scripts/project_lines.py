#!/usr/bin/env python3
"""project_lines.py — the second and third projection lines for the statistical baselines.

The baselines chart has always drawn ONE projection: the linear least-squares fit written by
forecast.py. The strategy call of 04/09/2026 asked for three lines, deliberately NOT fused, so the
eye can judge whether independent readings agree:

  1. statistical — forecast.py. Arithmetic on ECB / workbook actuals. No judgement enters it.
  2. by signals  — an analyst reading of the dated, cited weekly signals for that row.
  3. by patterns — the structural per-year rates stated in the KB patterns.

This script writes lines 2 and 3 into projection_lines.json. Line 1 is left where it is.

WHAT IS COMPUTED AND WHAT IS NOT
--------------------------------
Only line 3 is computed here, and only where a pattern actually states a rate: the rates are parsed
out of the pattern text, never invented. Line 2 cannot be computed at all — signals carry no numeric
field — so it is READ from signal_projections.json, which an analyst (or the orchestrator) writes with
the signal keys each figure rests on. Where neither file can speak for a row, this script records an
explicit gap with a reason, so the dashboard can say why a line is missing instead of silently
dropping it.

Two assumptions are made visible rather than buried:

  * DECAY. A pattern that says "Greece +15.3%" is reporting an OBSERVED move, not a forward rate.
    Compounded three years it reaches ~9,450 ATMs, far outside anything the ECB series supports.
    Observed country rates are therefore tapered by --decay each year (default 0.5, i.e. half the
    remaining rate per year) and the factor is carried on the row so the chart can state it.
    Rates the pattern states AS a forward/structural rate (a band, or a flat tier) are not tapered.
  * HORIZON. Each line ends on the same year as that row's statistical projection, so the three lines
    are always compared over the same window.

Usage:
  python project_lines.py --data <intel-cache> [--week YYYY-MM-DD] [--decay 0.5]
"""
import argparse, json, os, re, datetime

# ---------------------------------------------------------------- metric groups
# Which baseline metrics each rate-bearing pattern can legitimately speak for. A pattern about the
# ATM installed base says nothing about POS terminals, and pattern #1 is explicit that withdrawal
# VALUE behaves differently from withdrawal COUNT — so value metrics are deliberately absent.
ATM_METRICS  = ("ATMs", "ATM installed base")
CASH_METRICS = ("Cash withdrawals",)   # the count. The value / cash-in-circulation rows are not what pattern #1 measures

def load(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default

# ---------------------------------------------------------------- pattern rate parsing
# "GROWING — Hungary +18.6% (mandate), Greece +15.3% ...; STABLE — Bulgaria, Slovenia ...;
#  DECLINING — Austria -4.6%/2yr, Czechia -3.7%."
_TIER_SPLIT = re.compile(r"\b(GROWING|STABLE|DECLINING)\b\s*[—:-]", re.I)
# A country name (possibly multiword), then a signed percentage. A small, CLOSED set of filler words
# is allowed between the two ("Serbia back to +3.6%") — deliberately not "any words", which would let
# a rate bind to whichever country happened to be named earlier in the sentence.
_FILLER = r"(?:\s+(?:back|now|at|to|around|about|roughly|still|only))*"
_COUNTRY_RATE = re.compile(r"([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)" + _FILLER +
                           r"\s*(?:\(([^)]*)\)\s*)?([+-]\s*\d+(?:\.\d+)?)\s*%(\s*/\s*\d+\s*yr)?")
# The patterns are written in prose and use the short-form country names; the footprint is the
# authority on the name a baseline row is keyed by.
_ALIAS = {"Czechia": "Czech Republic", "Czech": "Czech Republic",
          "Bosnia": "Bosnia & Herzegovina", "Herzegovina": "Bosnia & Herzegovina",
          "Macedonia": "North Macedonia"}
_BARE_COUNTRY = re.compile(r"\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)\b")
# "~3-4%/yr", "3 to 4 %/yr", "-1.8%/yr"
_BAND = re.compile(r"~?\s*([+-]?\d+(?:\.\d+)?)\s*(?:[-–]|to)\s*(\d+(?:\.\d+)?)\s*%\s*/\s*(?:yr|year)", re.I)
_SINGLE_RATE = re.compile(r"~?\s*([+-]?\d+(?:\.\d+)?)\s*%\s*/\s*(?:yr|year)", re.I)


def parse_country_rates(text, names):
    """Pull per-country rates out of a tiered pattern sentence. Returns {country: (rate_pct, tier)}.

    Only names in `names` (the live footprint) are kept, so an out-of-scope market named in the
    evidence never produces a line. A country listed under STABLE without a figure gets 0.0.
    """
    out = {}
    parts = _TIER_SPLIT.split(text)
    # parts = [prefix, TIER, body, TIER, body, ...]
    for i in range(1, len(parts) - 1, 2):
        tier, body = parts[i].upper(), parts[i + 1]
        # stop the body at the next sentence break so tiers do not bleed into each other
        body = body.split(";")[0]
        claimed = set()
        for m in _COUNTRY_RATE.finditer(body):
            name, rate, per = m.group(1).strip(), m.group(3), m.group(4)
            name = _ALIAS.get(name, name)
            if name not in names:
                continue
            val = float(rate.replace(" ", ""))
            if per:                                   # "-4.6%/2yr" -> annualise crudely, and say so
                n = float(re.search(r"\d+", per).group())
                if n > 0:
                    val = round(val / n, 2)
            out[name] = (val, tier)
            claimed.add(name)
        if tier == "STABLE":
            for m in _BARE_COUNTRY.finditer(body):
                name = _ALIAS.get(m.group(1).strip(), m.group(1).strip())
                if name in names and name not in claimed:
                    out[name] = (0.0, tier)
    return out


# The dashboard shows the patterns grouped by theme, in this order, and numbers them in THAT order.
# The engine must say "Pattern #9" only if the screen says "Pattern #9" — so the same order is used here.
_GROUP_ORDER = ["Cash & ATM economics", "Branches & channel shift", "Operating model & vendor landscape",
                "Payments & regulation", "Digital & identity", "Macro & country divergence",
                "Procurement & demand cadence"]

def display_numbers(patterns):
    """file index -> the number the dashboard shows for that pattern."""
    order = sorted(range(len(patterns)),
                   key=lambda i: (_GROUP_ORDER.index(patterns[i].get("group"))
                                  if patterns[i].get("group") in _GROUP_ORDER else len(_GROUP_ORDER), i))
    return {i: n + 1 for n, i in enumerate(order)}

def pattern_rules(patterns, names):
    """Turn the KB patterns into rate rules. Returns a list of dicts; each knows which metrics it
    covers, what rate it states, whether that rate is an observation (taper it) or structural."""
    rules = []
    shown = display_numbers(patterns)
    for fidx, p in enumerate(patterns):
        idx = shown[fidx]
        head = str(p.get("pattern") or "")
        ev = str(p.get("evidence") or "")
        blob = head + " " + ev
        group = str(p.get("group") or "")
        cites = p.get("citations") or []
        src = "Pattern #%d — %s" % (idx, group) if group else "Pattern #%d" % idx

        # (a) tiered per-country ATM rates
        tiers = parse_country_rates(blob, names)
        if tiers and re.search(r"\bATM", blob):
            rules.append({"kind": "country", "metrics": ATM_METRICS, "rates": tiers,
                          "pattern_no": idx, "source": src, "claim": head.strip(),
                          "citations": cites, "observed": True})

        # (b) a footprint-wide band, e.g. "transactional use erodes ~3-4%/yr"
        band = _BAND.search(head) or _BAND.search(ev)
        if band and re.search(r"cash", blob, re.I) and re.search(r"erod|fall|declin|shrink", blob, re.I):
            lo, hi = float(band.group(1)), float(band.group(2))
            lo, hi = -abs(lo), -abs(hi)
            rules.append({"kind": "band", "metrics": CASH_METRICS, "band": (max(lo, hi), min(lo, hi)),
                          "pattern_no": idx, "source": src, "claim": head.strip(),
                          "citations": cites, "observed": False})
    return rules


# ---------------------------------------------------------------- projection maths
def walk(base, years, rate_pct, decay):
    """Compound `rate_pct` from `base` across `years`, tapering by `decay` each step when asked."""
    out, v, r = [], float(base), rate_pct / 100.0
    for y in years:
        v = v * (1.0 + r)
        if decay is not None:
            r *= decay
        out.append({"year": y, "value": round(max(0.0, v), 1)})
    return out


def anchor_point(f):
    """The starting point of every projection line (asked 09/09/2026).

    The last year with any REPORTED point for the row — the row's own series or another
    organisation's readings of the same thing, measured or provisional; never a projected point.
    When that year holds more than one reading, the mean of them is the start value. Returns
    {year, value, n, points} or None when the row has no reported point at all.
    """
    by_year = {}
    for h in f.get("history") or []:
        if h.get("value") is None:
            continue
        by_year.setdefault(h["year"], []).append({"source": f.get("source") or "recorded series",
                                                  "value": float(h["value"]),
                                                  "provisional": bool(h.get("provisional"))})
    for a in f.get("alt_series") or []:
        for pt in a.get("points") or []:
            if pt.get("value") is None:
                continue
            by_year.setdefault(pt["year"], []).append({"source": a.get("source") or "other source",
                                                       "value": float(pt["value"]),
                                                       "provisional": bool(pt.get("provisional"))})
    if not by_year:
        return None
    year = max(by_year)
    pts = by_year[year]
    return {"year": year, "value": round(sum(x["value"] for x in pts) / len(pts), 1),
            "n": len(pts), "points": pts,
            "provisional": all(x["provisional"] for x in pts)}

def _anchor_words(a):
    """'the last reported 6,167 (2024)' or 'the mean of 2 readings for 2025 (7,421)'."""
    if a["n"] > 1:
        return "the mean of %d readings for %d (%s)" % (a["n"], a["year"], _fmt(a["value"]))
    return "the last reported %s (%d)" % (_fmt(a["value"]), a["year"])

def build_pattern_lines(forecasts, rules, decay, names, target_year):
    lines, gaps = [], []
    for f in forecasts:
        country, metric = f["country"], f["metric"]
        a = anchor_point(f)
        if not a or a["year"] >= target_year:
            continue
        proj_years = list(range(a["year"] + 1, target_year + 1))
        base, base_year = a["value"], a["year"]

        rule = hit = None
        for r in rules:
            if metric not in r["metrics"]:
                continue
            if r["kind"] == "country" and country in r["rates"]:
                rule, hit = r, r["rates"][country]; break
            if r["kind"] == "band":
                rule, hit = r, r["band"]; break
        if not rule:
            gaps.append({"country": country, "metric": metric, "origin": "patterns",
                         "reason": "no pattern states a per-year rate for %s" % metric})
            continue

        row = {"country": country, "metric": metric, "origin": "patterns",
               "pattern_no": rule["pattern_no"], "source": rule["source"],
               "claim": rule["claim"], "citations": rule["citations"],
               "from_year": base_year, "from_value": base, "anchor": a}

        end_year = proj_years[-1]
        mlow = metric if metric[:2].isupper() else (metric[:1].lower() + metric[1:])
        if rule["kind"] == "band":
            hi, lo = hit
            row["rate_pct"] = round((hi + lo) / 2.0, 2)
            row["band_pct"] = [hi, lo]
            row["decay"] = None
            row["basis"] = ("footprint-wide band stated as a forward rate — drawn as a band, "
                            "not tapered")
            row["projection"] = walk(base, proj_years, row["rate_pct"], None)
            row["band"] = {"high": walk(base, proj_years, hi, None),
                           "low": walk(base, proj_years, lo, None)}
            # plain words, for THIS country: what the pattern says, how it is applied, where it lands
            row["explain"] = (
                "Pattern #%d says %s fall by about %g%% to %g%% a year across the footprint, applied here from "
                "%s's %s."
                % (rule["pattern_no"], mlow, abs(hi), abs(lo), country, _anchor_words(a))
                )
        else:
            rate, tier = hit
            taper = decay if (rule["observed"] and abs(rate) > 0) else None
            row["rate_pct"] = rate
            row["tier"] = tier
            row["decay"] = taper
            row["basis"] = ("rate named for this market in the pattern (%s tier)%s"
                            % (tier.lower(),
                               "" if taper is None else
                               "; an observed move, so tapered by %g per year" % taper))
            row["projection"] = walk(base, proj_years, rate, taper)
            end_val = row["projection"][-1]["value"]
            if abs(rate) < 1e-9:
                row["explain"] = (
                    "Pattern #%d lists %s as stable for %s, so the line stays flat at %s."
                    % (rule["pattern_no"], country, mlow, _anchor_words(a))
                    )
            else:
                how = ("We apply that rate from %s and %s each year, because a move "
                       "like that does not keep its full pace." % (_anchor_words(a),
                       "halve it" if taper == 0.5 else ("cut it by %d%%" % round((1 - taper) * 100)) if taper else "keep it"))
                if taper is None:
                    how = "We apply that rate from %s." % _anchor_words(a)
                row["explain"] = (
                    "Pattern #%d lists %s as %s for %s: %s%g%% a year, an observed move. %s"
                    % (rule["pattern_no"], country, tier.lower(), mlow, "+" if rate > 0 else "", rate, how)
                    )
        lines.append(row)
    return lines, gaps


# ---------------------------------------------------------------- signals line (read, never computed)
def read_signal_lines(data_dir, forecasts):
    """Load the analyst-written signals projections and keep only rows that match a live baseline.

    Each entry must carry the signal keys it rests on — a figure with no cited signal is dropped,
    loudly, because the whole point of this line is that it is traceable to dated evidence.
    """
    raw = load(os.path.join(data_dir, "signal_projections.json"), {})
    entries = raw.get("projections", []) if isinstance(raw, dict) else (raw or [])
    live = {(f["country"], f["metric"]): f for f in forecasts}
    out, dropped = [], []
    for e in entries:
        key = (e.get("country"), e.get("metric"))
        f = live.get(key)
        if not f:
            dropped.append("%s / %s — no such baseline row" % key); continue
        if not e.get("cite_signals"):
            dropped.append("%s / %s — no cite_signals" % key); continue
        pts = [p for p in (e.get("projection") or []) if p.get("year") is not None]
        if not pts:
            dropped.append("%s / %s — no projection points" % key); continue
        row = dict(e)
        row["origin"] = "signals"
        a = anchor_point(f)
        row["anchor"] = a
        row["from_year"] = a["year"] if a else f.get("last_year")
        row["from_value"] = a["value"] if a else f.get("last_value")
        pts = sorted(pts, key=lambda p: p["year"])
        row["projection"] = pts
        # The analyst wrote the line from the row's own series as it stood (last_year/last_value).
        # When the anchor is a newer or different reported point (another source, a provisional
        # year), the line is re-based on it (asked 10/09/2026): the analyst's implied yearly rate
        # is kept and applied from the anchor. The written points are kept on the row for reference.
        base_year, base = f.get("last_year"), f.get("last_value")
        end = pts[-1]
        if (a and base and base_year is not None and end["year"] > a["year"]
                and (a["year"], round(float(a["value"]), 1)) != (base_year, round(float(base), 1))
                and end["year"] > base_year):
            rate = (float(end["value"]) / float(base)) ** (1.0 / (end["year"] - base_year)) - 1.0
            row["analyst_projection"] = pts
            row["projection"] = [{"year": y, "value": round(a["value"] * (1.0 + rate) ** (y - a["year"]), 1)}
                                 for y in range(a["year"] + 1, end["year"] + 1)]
            row["rebased"] = {"base_year": base_year, "base_value": base, "rate_pct": round(rate * 100, 2),
                              "written_end": {"year": end["year"], "value": end["value"]},
                              "note": ("The analyst wrote this line from %s (%d), the row's own series at the time. "
                                       "It implies %s%.1f%% a year. Applied from %s, that puts %d at about %s."
                                       % (_fmt(base), base_year, "+" if rate >= 0 else "", rate * 100,
                                          _anchor_words(a), end["year"], _fmt(row["projection"][-1]["value"])))}
        out.append(row)
    return out, dropped


# ---------------------------------------------------------------- the signal-based point for next year
# Asked for on 08/09/2026: for every baseline, ONE estimate for next year (2027) read from the existing
# signals, explained simply, and drawn as a point so the eye gets a feel for where the year is going.
#
# Signals carry no numeric field, so this cannot be a measured figure. It is a RULE-BASED TILT on the
# statistical trend, and every input to the rule is written onto the row so the dashboard can state it:
#   * which current signals bind to the row (same market + product binding as the explainer),
#   * which way each one leans for THIS metric, read from its own words with a small per-metric list,
#   * the net lean, weighted by signal strength, in [-1, +1],
#   * the size of the move, which is the series' OWN typical yearly change — the MEDIAN |Δ| between
#     consecutive recorded, non-provisional years — so the magnitude comes from the data, never from
#     a number picked by hand, and a single freak year or a part-year provisional point cannot inflate it,
#   * point = last recorded value + lean × typical move × (years from that record to the target).
# The point is anchored on the last RECORDED value, not on the statistical projection, on purpose: the
# team asked for three readings that are never fused, and a fit through 2016-2025 can drift far from
# where a flattened series actually sits (Cyprus branches: trend 54 for 2027 against 193 recorded).
# The trend value is kept on the row only so the sentence can say whether the signals sit above or
# below it. Where an analyst has written a signals projection for the row, that value wins and is
# labelled so. A row with no directional signal, or too little history to size a move, gets no point
# and a written reason.

_METRIC_PRODUCTS = {
    "ATMs": ("atm_recycling", "managed_services"),
    "ATM installed base": ("atm_recycling", "managed_services"),
    "Cash withdrawals": ("atm_recycling", "managed_services"),
    "Cash withdrawals — annual value (USD)": ("atm_recycling", "managed_services"),
    "Cash in circulation (value)": ("atm_recycling", "managed_services"),
    "Banknotes exported (value)": ("atm_recycling", "managed_services"),
    "Counter cash deposits and withdrawals (value)": ("atm_recycling", "managed_services"),
    "Cash withdrawn from accounts (value)": ("atm_recycling", "managed_services"),
    "Cash withdrawals (local measure)": ("atm_recycling", "managed_services"),
    "Bank branches": ("self_service", "managed_services"),
    "Bank employees": ("self_service", "managed_services"),
    "POS terminals": ("pos_acquiring",),
}

# Direction cues per metric family. Deliberately short and literal: a cue has to say the thing is
# growing or shrinking, not merely mention it. Both directions present -> the side with more cues
# wins; a tie is neutral.
_CUES = {
    "atm": (re.compile(r"\b(deploy|roll-?out|install(?:ed|ing|s)?|new atms?|additional atms?|expan\w*|"
                       r"grow\w*|deposit-capable|recycler|cash-in|mandate|in every settlement|build-?out|"
                       r"added|rising|increas\w*|fleet renewal|more atms)\b", re.I),
            re.compile(r"\b(decommission\w*|remov\w* (?:of )?atms?|clos(?:e|ing|ure)s?|shrink\w*|freeze|"
                       r"consolidat\w*|fewer atms|reduc\w* (?:the )?(?:fleet|estate|atms?)|cut(?:s|ting)? (?:the )?(?:fleet|atms?))\b", re.I)),
    "branch": (re.compile(r"\b(open(?:s|ed|ing)? (?:a |new )?branch\w*|new branch\w*|branch expansion|"
                          r"hiring|recruit\w*|more branches)\b", re.I),
               re.compile(r"\b(branch clos\w*|closure\w*|consolidat\w*|rationali[sz]\w*|shrink\w*|"
                          r"cut(?:s|ting)?|reduc\w*|layoff\w*|redundan\w*|fewer branch\w*|cashless branch)\b", re.I)),
    "pos": (re.compile(r"\b(mandate|obligat\w*|roll-?out|acceptance|new terminals?|terminals? added|"
                       r"expan\w*|grow\w*|soft-?pos|tap to pay|free terminals?|more terminals)\b", re.I),
            re.compile(r"\b(declin\w*|shrink\w*|removal|reduc\w*|fewer terminals?)\b", re.I)),
    "cash": (re.compile(r"\b(cash demand|cash resilien\w*|withdrawals? (?:grow|ris|up)\w*|cash-in|"
                        r"more cash|cash (?:use|usage) (?:grow|ris)\w*|record cash|cash still)\b", re.I),
             re.compile(r"\b(cashless|declin\w* (?:in )?cash|cash (?:use|usage) (?:fall|declin|erod)\w*|"
                        r"instant payments?|cards? (?:payments? )?(?:overtook|overtake|overtaking)|"
                        r"fewer withdrawals?|withdrawals? (?:fall|declin|down)\w*)\b", re.I)),
}

def _family(metric):
    m = metric.lower()
    if "pos" in m: return "pos"
    if "branch" in m or "employee" in m: return "branch"
    if "withdraw" in m or "cash" in m or "banknote" in m: return "cash"
    return "atm"

_CONF_W = {"High": 1.0, "Medium-High": 0.9, "Medium": 0.75, "Medium-Low": 0.6, "Low": 0.5}

def _lean(sig, fam):
    up_re, dn_re = _CUES[fam]
    blob = " ".join(str(sig.get(k) or "") for k in ("bank_theme", "signal", "implies"))
    u, d = len(up_re.findall(blob)), len(dn_re.findall(blob))
    if u == d: return 0
    return 1 if u > d else -1

def signal_points(forecasts, signals, code_by_name, analyst_lines, target_year):
    """One signal-based point per row for `target_year`. Returns (points, gaps)."""
    points, gaps = [], []
    by_analyst = {(l["country"], l["metric"]): l for l in analyst_lines}
    for f in forecasts:
        country, metric = f["country"], f["metric"]
        a = anchor_point(f)
        if not a or a["year"] >= target_year:
            gaps.append({"country": country, "metric": metric, "origin": "signals_point",
                         "reason": "no reported point before %d to start from" % target_year}); continue

        # an analyst-written value for the year wins outright
        al = by_analyst.get((country, metric))
        if al:
            av = next((p for p in al["projection"] if p["year"] == target_year), None)
            if av:
                points.append({"country": country, "metric": metric, "origin": "signals_point",
                               "year": target_year, "value": av["value"], "anchor": a,
                               "method": "analyst",
                               "explain": ("Taken from the analyst's signals projection for this row: %s. %s"
                                           % (al.get("direction") or "see the signals line",
                                              (al.get("rebased") or {}).get("note") or "")).strip(),
                               "cite_signals": al.get("cite_signals", [])})
                continue

        code = code_by_name.get(country)
        prods = _METRIC_PRODUCTS.get(metric, ())
        if not code or not prods:
            gaps.append({"country": country, "metric": metric, "origin": "signals_point",
                         "reason": "no product binding for this metric"}); continue

        bound = [s for s in signals if s.get("is_current")
                 and code in (s.get("countries") or [])
                 and (s.get("primary_product") in prods or any(p in prods for p in (s.get("products") or [])))]
        fam = _family(metric)
        ups, downs = [], []
        for s in bound:
            l = _lean(s, fam)
            w = float(s.get("strength") or 1.0) * _CONF_W.get(s.get("confidence") or "", 0.75)
            if l > 0: ups.append((w, s))
            elif l < 0: downs.append((w, s))
        su, sd = sum(w for w, _ in ups), sum(w for w, _ in downs)
        if su + sd == 0:
            gaps.append({"country": country, "metric": metric, "origin": "signals_point",
                         "reason": "%d signal(s) bind to this row but none says whether %s are growing or shrinking here"
                                   % (len(bound), metric.lower())}); continue
        lean = (su - sd) / (su + sd)

        # recorded, non-provisional points only: a part-year value is not a year's move
        hist = sorted((h["year"], h["value"]) for h in (f.get("history") or []) if not h.get("provisional"))
        if len(hist) < 2:
            gaps.append({"country": country, "metric": metric, "origin": "signals_point",
                         "reason": "fewer than two completed years on record — nothing to size a move against"}); continue
        deltas = sorted(abs(hist[i+1][1] - hist[i][1]) / max(1, hist[i+1][0] - hist[i][0]) for i in range(len(hist)-1))
        typical = deltas[len(deltas)//2] if len(deltas) % 2 else (deltas[len(deltas)//2 - 1] + deltas[len(deltas)//2]) / 2.0
        anchor_year, anchor = a["year"], a["value"]
        years = max(1, target_year - anchor_year)
        value = round(max(0.0, anchor + lean * typical * years), 1)

        top = max(ups + downs, key=lambda t: t[0])[1]
        flat = abs(lean) <= 0.15
        dirword = "up" if lean > 0.15 else "down" if lean < -0.15 else "balanced"
        if flat:
            explain = ("%d signal(s) lean up and %d lean down for %s in %s — balanced, so the signals give no reason "
                       "to move off %s. That puts %d at ~%s. "
                       "Strongest voice: %s."
                       % (len(ups), len(downs), metric.lower(), country, _anchor_words(a),
                          target_year, _fmt(value), top.get("bank_theme") or top.get("key")))
        else:
            explain = ("%d signal(s) lean up and %d lean down for %s in %s; weighted by strength, the balance is %s. "
                       "Starting from %s, and a typical move of ~%s a year over the %d year%s to %d, "
                       "the signals put %d at ~%s. Strongest voice: %s."
                       % (len(ups), len(downs), metric.lower(), country, dirword,
                          _anchor_words(a), _fmt(typical), years, "" if years == 1 else "s", target_year,
                          target_year, _fmt(value), top.get("bank_theme") or top.get("key")))
        points.append({"country": country, "metric": metric, "origin": "signals_point",
                       "year": target_year, "value": value, "anchor": a, "method": "rule",
                       "anchor_year": anchor_year, "anchor_value": anchor, "years": years,
                       "lean": round(lean, 2), "n_up": len(ups), "n_down": len(downs),
                       "n_bound": len(bound), "typical_move": round(typical, 1),
                       "top_signal": top.get("key"), "top_signal_title": top.get("bank_theme"),
                       "cite_signals": [s.get("key") for _, s in sorted(ups + downs, key=lambda t: -t[0])][:8],
                       "explain": explain})
    return points, gaps


# ---------------------------------------------------------------- the consensus reading for next year
_ORIGIN_NAME = {"patterns": "By patterns", "signals": "By signals", "signals_point": "By signals (rule)"}

def consensus(forecasts, lines, target_year):
    """One reading per row: the mean and spread of every projection we hold for `target_year`.

    Asked on 09/09/2026: the map and the table showed the fitted trend alone, which is one source.
    This pools the projections drawn on the chart — the patterns line, the analyst's signals line
    and the rule-based signals point; no trend fit — and states them the same way: the change per
    year from the row's anchor (the last reported point, see anchor_point) to `target_year`,
    annualised. The numbers are then averaged, and the sample standard deviation says how far the
    readings sit apart. Nothing is fused into the lines themselves; this is a summary of them.

    The rule-based signals point is skipped when it merely copies the analyst's line
    (method == 'analyst'), so one reading is not counted twice.
    """
    by_row = {}
    for l in lines:
        by_row.setdefault((l["country"], l["metric"]), []).append(l)
    out = []
    for f in forecasts:
        a = anchor_point(f)
        if not a:
            continue
        anchor_year, anchor = a["year"], a["value"]
        if anchor <= 0 or target_year <= anchor_year:
            continue
        n_years = target_year - anchor_year
        readings = []
        def add(origin, value, note=""):
            try:
                v = float(value)
            except (TypeError, ValueError):
                return
            if v <= 0:
                return
            g = ((v / anchor) ** (1.0 / n_years) - 1.0) * 100.0
            readings.append({"origin": origin, "name": _ORIGIN_NAME.get(origin, origin),
                             "value": round(v, 1), "growth_pct": round(g, 1), "note": note})
        for l in by_row.get((f["country"], f["metric"]), []):
            o = l["origin"]
            if o in ("patterns", "signals"):
                pt = next((p for p in (l.get("projection") or []) if p["year"] == target_year), None)
                if pt:
                    add(o, pt["value"], (l.get("source") or "") if o == "patterns" else (l.get("direction") or ""))
            elif o == "signals_point" and l.get("year") == target_year and l.get("method") != "analyst":
                add(o, l.get("value"), l.get("explain") or "")
        if not readings:
            continue
        g = [r["growth_pct"] for r in readings]
        mean = sum(g) / len(g)
        std = (sum((x - mean) ** 2 for x in g) / (len(g) - 1)) ** 0.5 if len(g) > 1 else None
        out.append({"country": f["country"], "metric": f["metric"], "year": target_year,
                    "anchor_year": anchor_year, "anchor_value": anchor, "anchor_n": a["n"],
                    "anchor_provisional": a["provisional"],
                    "n": len(readings), "mean_pct": round(mean, 1),
                    "std_pct": None if std is None else round(std, 1),
                    "low_pct": round(min(g), 1), "high_pct": round(max(g), 1),
                    "readings": readings})
    return out

def _fmt(v):
    try:
        v = float(v)
    except Exception:
        return str(v)
    return ("{:,}".format(int(round(v)))) if abs(v) >= 100 else ("%.1f" % v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="intel-cache folder")
    ap.add_argument("--week", default=None)
    ap.add_argument("--decay", type=float, default=0.5,
                    help="per-year taper applied to an OBSERVED pattern rate (0 = drop to flat "
                         "immediately, 1 = compound the observed rate unchanged). Default 0.5.")
    args = ap.parse_args()
    week = args.week or datetime.date.today().isoformat()
    D = args.data

    fc = load(os.path.join(D, "forecast.json"), {})
    forecasts = fc.get("forecasts", [])
    if not forecasts:
        raise SystemExit("no forecasts in %s/forecast.json — run forecast.py first" % D)

    footprint = load(os.path.join(D, "..", "weekly-intelligence", "references", "footprint.json"), {})
    if not footprint.get("countries"):
        footprint = load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      "references", "footprint.json"), {})
    names = {c["name"] for c in footprint.get("countries", [])} or {f["country"] for f in forecasts}

    kb = load(os.path.join(D, "patterns_kb.json"), [])
    patterns = kb if isinstance(kb, list) else kb.get("patterns", [])
    rules = pattern_rules(patterns, names)

    run_year = int(week[:4])
    plines, gaps = build_pattern_lines(forecasts, rules, args.decay, names, run_year + 1)
    slines, dropped = read_signal_lines(D, forecasts)

    for msg in dropped:
        print("signals line dropped: %s" % msg)

    covered = {(l["country"], l["metric"]) for l in slines}
    for f in forecasts:
        if (f["country"], f["metric"]) not in covered:
            gaps.append({"country": f["country"], "metric": f["metric"], "origin": "signals",
                         "reason": "no analyst signals projection written for this row yet"})

    # the one-year signal-based point (see signal_points): read the signals + footprint, next year
    raw_sig = load(os.path.join(D, "signals.json"), [])
    signals = raw_sig if isinstance(raw_sig, list) else raw_sig.get("signals", [])
    code_by_name = {c["name"]: c["code"] for c in footprint.get("countries", [])}
    spoints, sgaps = signal_points(forecasts, signals, code_by_name, slines, run_year + 1)
    gaps.extend(sgaps)
    print("signal-based %d points: %d rule-based, %d from analyst lines | %d without a point"
          % (run_year + 1, sum(1 for p in spoints if p["method"] == "rule"),
             sum(1 for p in spoints if p["method"] == "analyst"), len(sgaps)))

    cons = consensus(forecasts, plines + slines + spoints, run_year + 1)
    print("%d consensus reading(s) for %d: %s"
          % (len(cons), run_year + 1,
             ", ".join("%d row(s) with %d reading(s)" % (sum(1 for c in cons if c["n"] == k), k)
                       for k in sorted({c["n"] for c in cons}))))

    payload = {"generated_week": week, "decay": args.decay,
               "lines": plines + slines + spoints, "gaps": gaps,
               "consensus": cons,
               # the starting point of every line on a row: last reported point, mean when several
               "anchors": [dict(country=f["country"], metric=f["metric"], **anchor_point(f))
                           for f in forecasts if anchor_point(f)],
               "rules": [{"pattern_no": r["pattern_no"], "kind": r["kind"], "source": r["source"],
                          "metrics": list(r["metrics"]),
                          "markets": sorted(r["rates"]) if r["kind"] == "country" else None,
                          "band_pct": list(r["band"]) if r["kind"] == "band" else None}
                         for r in rules]}
    out = os.path.join(D, "projection_lines.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)

    print("projection_lines.json: %d pattern line(s) from %d rule(s), %d signals line(s) | %d gap(s)"
          % (len(plines), len(rules), len(slines), len(gaps)))
    for r in rules:
        if r["kind"] == "country":
            print("  pattern #%d -> %d market(s): %s" % (r["pattern_no"], len(r["rates"]),
                                                         ", ".join("%s %+g%%" % (k, v[0])
                                                                   for k, v in sorted(r["rates"].items()))))
        else:
            print("  pattern #%d -> band %g%%..%g%%/yr on %s"
                  % (r["pattern_no"], r["band"][0], r["band"][1], ", ".join(r["metrics"])))


if __name__ == "__main__":
    main()
