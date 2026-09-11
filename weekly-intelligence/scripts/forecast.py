#!/usr/bin/env python3
"""
forecast.py - Deterministic trend projection over the history-workbook metrics (Phase 2: foresight).

Reads intel-cache/timeseries.json (long-format workbook Metrics), builds annual sector series per
(country, metric), fits a linear least-squares trend, and projects `--horizon` years forward. It also
maintains a predictions ledger (predictions.json): each projection is logged once with the week it was
made, then RESOLVED automatically when the workbook later carries the actual for that year — giving an
honest forecast-accuracy track record (MAPE).

CRITICAL: this NEVER invents a value. Every projection is a transparent extrapolation of the existing
dated series, labelled with its method and fit quality. It is code (not an LLM) precisely so a projected
number can never be confused with a sourced fact — the dashboard renders these as "projection".

Usage:
  python forecast.py --data <intel-cache> [--week YYYY-MM-DD] [--horizon 2] [--min-points 3]

Projections are anchored to the calendar, so nothing is ever presented as a "forecast" for a year that
has already happened. Every series reaches run_year+1; a series earns a second year (run_year+2) only
if it still has a data point from run_year-1 or later AND its trend fit is not Low. Each forecast
carries `horizon_reason` explaining where its line stops and why.
"""
import argparse, json, os, re, datetime

def load(p, d=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return d if d is not None else {}

def _is_provisional(rec):
    conf = str(rec.get("confidence") or "").lower()
    note = (str(rec.get("notes") or "") + " " + str(rec.get("source") or "")).lower()
    return conf == "low" or any(w in note for w in ("provisional", "estimate", "obs_status", "(p)", "preliminary"))

def build_series(timeseries):
    """(country, metric) -> sorted [(year, value, provisional)] for sector/benchmark annual numeric rows."""
    series = {}
    for rec in timeseries:
        scope = rec.get("scope") or ""
        if "Sector" not in scope and "benchmark" not in scope.lower():
            continue
        country, metric = rec.get("country"), rec.get("metric")
        if not country or not metric:
            continue
        per = str(rec.get("period") or "").strip()
        if not re.fullmatch(r"(19|20)\d{2}", per):
            continue
        v = rec.get("value")
        if not isinstance(v, (int, float)):
            continue
        series.setdefault((country, metric), {})[int(per)] = (float(v), _is_provisional(rec))
    return {k: [(y, val, prov) for y, (val, prov) in sorted(d.items())] for k, d in series.items()}

def _short_unit(u):
    """'terminals (end-Q4-2019)' -> 'terminals'; 'RSD million withdrawn from payment accounts (full year 2021)'
    -> 'RSD million withdrawn from payment accounts'. The full string is kept separately as unit_note."""
    u = str(u or "").strip()
    for cut in (" (", ","):
        if cut in u:
            u = u.split(cut, 1)[0].strip()
    return u

def _short_source(src):
    """'CBK Annual Report 2025, Chart 88 (re-verified 31/08/2026)' -> 'CBK Annual Report 2025, Chart 88'."""
    src = str(src or "").strip()
    if " (" in src:
        src = src.split(" (", 1)[0].strip()
    return src[:80]

def build_sources(timeseries):
    """(country, metric) -> most common source wording for the rows build_series keeps. Shown on the chart
    beside the recorded line, so a reader sees WHO published the numbers without opening anything."""
    from collections import Counter
    seen = {}
    for rec in timeseries:
        scope = rec.get("scope") or ""
        if "Sector" not in scope and "benchmark" not in scope.lower():
            continue
        country, metric, src = rec.get("country"), rec.get("metric"), rec.get("source")
        if not country or not metric or not src:
            continue
        if not re.fullmatch(r"(19|20)\d{2}", str(rec.get("period") or "").strip()):
            continue
        seen.setdefault((country, metric), Counter())[_short_source(src)] += 1
    return {k: c.most_common(1)[0][0] for k, c in seen.items()}

_DATED = re.compile(r"(19|20)\d{2}|\bend-|\bas at\b|\bfull year\b|\bQ[1-4]\b|\bH[12]\b|\bprovisional\b|\binterim\b|\bhalf-year\b|\bpart-year\b|\bpub\.|\bref\.", re.I)

def _clean_note(full):
    """Keep the wording that says WHAT the numbers are; drop the parts that say WHEN one point was read.
    'million lek (currency outside depository corporations, end-Dec-2023)' -> 'million lek (currency outside
    depository corporations)'; 'RSD million withdrawn from payment accounts (full year 2021)' -> 'RSD million
    withdrawn from payment accounts'. A note that ends up identical to the short unit is dropped."""
    _POINTY = re.compile(r"\d|\brounds? to\b|\bonly\b|\bincl\.|\bpartial\b|\bquarter\b|\by/y\b|\bcontactless\b|\bseasonal\b|\bsuspended\b|\bchart value\b|\btable\b", re.I)
    def keep_clause(x):
        x = x.strip()
        return bool(x) and not _DATED.search(x) and not _POINTY.search(x)
    def fix_paren(m):
        keep = [x for x in m.group(1).split(", ") if keep_clause(x)]
        return (" (" + ", ".join(keep) + ")") if keep else ""
    text = re.sub(r"\s*\(([^)]*)\)", fix_paren, str(full or ""))
    # outside brackets: clauses split by ";" or ", " — keep only those that describe the thing itself
    clauses = []
    for part in re.split(r";", text):
        sub = [x for x in re.split(r",\s", part) if keep_clause(x)]
        if sub:
            clauses.append(", ".join(x.strip() for x in sub))
    out = "; ".join(clauses)
    out = re.sub(r"\s{2,}", " ", out).strip().rstrip(",;")
    return out

def build_units(timeseries):
    """(country, metric) -> (short unit, most common full unit string) for the same rows build_series keeps.
    Units differ by SOURCE, not only by metric: the ECB series are counts of card cash withdrawals, while
    several non-EU central banks publish a value in local currency — or cash in circulation, which is not
    a withdrawal at all. The chart must say which, so every row carries its own unit."""
    from collections import Counter
    seen = {}
    for rec in timeseries:
        scope = rec.get("scope") or ""
        if "Sector" not in scope and "benchmark" not in scope.lower():
            continue
        country, metric, unit = rec.get("country"), rec.get("metric"), rec.get("unit")
        if not country or not metric or not unit:
            continue
        if not re.fullmatch(r"(19|20)\d{2}", str(rec.get("period") or "").strip()):
            continue
        seen.setdefault((country, metric), Counter())[str(unit).strip()] += 1
    out = {}
    for k, c in seen.items():
        # vote on the SHORT form: "RSD million withdrawn from payment accounts (full year 2021)" and
        # "... (full year 2022)" are one unit, not two. Then keep the longest full wording for the note.
        by_short = Counter()
        fulls = {}
        for full, n in c.items():
            sh = _short_unit(full)
            by_short[sh] += n
            fulls.setdefault(sh, []).append(full)
        sh = by_short.most_common(1)[0][0]
        # the note should describe the SERIES, not any one point: drop the dated qualifiers from the
        # most descriptive wording, and show no note at all if nothing beyond the unit survives
        note = _clean_note(max(fulls[sh], key=len))
        out[k] = (sh, note if note and note.lower() != sh.lower() else sh)
    return out

def retitle_cash_rows(series, units, sources):
    """The non-EU "Cash withdrawals" rows are not withdrawals: each central bank publishes something else
    under that heading — cash in circulation, a value withdrawn in local currency, banknotes exported.
    Give them their true names, so "Cash withdrawals" means one thing (a count, in millions) everywhere
    and RBR's count can carry that name where the ECB has no series. Returns {old_key: new_key}."""
    ren = {}
    for (c, m), (u, note) in list(units.items()):
        if m != "Cash withdrawals" or str(u).startswith("million card cash"):
            continue
        blob = (str(u) + " " + str(note)).lower()
        if "circulation" in blob or "currency outside" in blob or " m0" in blob or "—m0" in blob or "m0," in blob:
            new = "Cash in circulation (value)"
        elif "banknotes exported" in blob:
            new = "Banknotes exported (value)"
        elif "deposits+withdrawals" in blob or "deposits and withdrawals" in blob:
            new = "Counter cash deposits and withdrawals (value)"
        elif "withdraw" in blob:
            new = "Cash withdrawn from accounts (value)"
        else:
            new = "Cash withdrawals (local measure)"
        ren[(c, m)] = (c, new)
    for old, new in ren.items():
        for d in (series, units, sources):
            if old in d:
                d[new] = d.pop(old)
    if ren:
        print("retitled %d local-currency cash row(s): %s" % (len(ren), "; ".join("%s -> %s" % (o[0], n[1]) for o, n in sorted(ren.items()))))
    return ren

def make_coverage(series, min_points):
    """Every series the workbook has, with point count + whether it's projectable — to show data gaps."""
    cov = [{"country": c, "metric": m, "points": len(pts),
            "last_year": pts[-1][0] if pts else None, "projectable": len(pts) >= min_points}
           for (c, m), pts in series.items()]
    cov.sort(key=lambda x: (-x["points"], x["country"], x["metric"]))
    return cov

def linfit(pts):
    n = len(pts); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    sx, sy = sum(xs), sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    denom = n*sxx - sx*sx
    if denom == 0:
        return None
    slope = (n*sxy - sx*sy) / denom
    intercept = (sy - slope*sx) / n
    ybar = sy / n
    ss_tot = sum((y-ybar)**2 for y in ys) or 1e-9
    ss_res = sum((y-(slope*x+intercept))**2 for x, y in zip(xs, ys))
    return slope, intercept, max(0.0, 1 - ss_res/ss_tot)

def cagr(pts):
    (y0, v0), (y1, v1) = pts[0], pts[-1]
    return (v1/v0)**(1/(y1-y0)) - 1 if (v0 > 0 and y1 > y0) else None

def inflection(pts):
    """Compare the recent half's slope to the earlier half's -> accelerating/decelerating/reversing."""
    if len(pts) < 4:
        return ""
    mid = len(pts) // 2
    early, late = linfit(pts[:mid+1]), linfit(pts[mid:])
    if not early or not late or early[0] == 0:
        return ""
    se, sl = early[0], late[0]
    if (se > 0) != (sl > 0):
        return "reversing"
    if abs(sl) > 1.6*abs(se):
        return "accelerating"
    if abs(sl) < 0.6*abs(se):
        return "decelerating"
    return ""

def fit_quality(r2):
    return "High" if r2 >= 0.9 else "Medium" if r2 >= 0.7 else "Low"

def make_forecasts(series, run_year, horizon, min_points, units=None, sources=None):
    out = []
    units = units or {}
    sources = sources or {}
    for (country, metric), pts in series.items():
        if len(pts) < min_points:
            continue
        yv = [(y, v) for (y, v, _p) in pts]
        fit = linfit(yv)
        if not fit:
            continue
        slope, intercept, r2 = fit
        last_year, last_value = yv[-1]
        # The projection window is anchored to the CALENDAR, not to where the series happens to stop.
        # Anchoring to last_year+horizon produced "projections" for years that had already elapsed —
        # a series ending 2022 projected 2023-2024, both in the past, presented as a forecast.
        # Decision (strategy call, 04/09/2026): every series projects through to run_year+1, so a
        # 2022 series answers "what does the 2022 trend imply for 2027?". `horizon` is now only the
        # fallback for a series that already reaches the target year.
        #
        # Refinement (07/09/2026): the extra year to run_year+2 is EARNED, not given. The tab's
        # "6-12 months" label describes the analyst outlooks, not these annual series, so the horizon
        # is set by data quality alone. A series gets the second year only if it still has a recent
        # data point (run_year-1 or later) AND its trend actually fits. That keeps the stretch at
        # <=3 years for the series that earn it, instead of carrying a 2022 reading six years forward.
        fq = fit_quality(r2)
        fresh = last_year >= run_year - 1
        earns_extra = fresh and fq != "Low"
        target_year = run_year + (2 if earns_extra else 1)
        end_year = target_year if target_year > last_year else last_year + horizon
        if earns_extra:
            horizon_reason = f"data through {last_year} and {fq.lower()} trend fit — carried to {end_year}"
        elif not fresh and fq == "Low":
            horizon_reason = f"last data point is {last_year} and the trend fit is low — stops at {end_year}"
        elif not fresh:
            horizon_reason = f"last data point is {last_year} — stops at {end_year}"
        else:
            horizon_reason = f"trend fit is low — stops at {end_year}"
        projection = [{"year": yr, "value": round(max(0.0, slope*yr + intercept), 1)}
                      for yr in range(last_year+1, end_year+1)]
        g = cagr(yv)
        out.append({
            "country": country, "metric": metric,
            # what the numbers ARE, from the source row — shown on the chart's axis. unit_note keeps the
            # full wording where the short label would hide the concept (e.g. "cash in circulation")
            "unit": (units.get((country, metric)) or ("", ""))[0] or None,
            "unit_note": ((units.get((country, metric)) or ("", ""))[1] or None),
            "source": sources.get((country, metric)) or None,
            "history": [{"year": y, "value": v, "provisional": p} for (y, v, p) in pts],
            "projection": projection,
            "last_year": last_year, "last_value": last_value,
            "slope_per_year": round(slope, 1),
            "cagr_pct": round(g*100, 1) if g is not None else None,
            "fit_quality": fq, "r2": round(r2, 3),
            "inflection": inflection(yv),
            "projection_to": end_year,
            # how many years beyond the last real data point the line is carried — 1 is routine,
            # 5 means a stale series is being stretched across the whole gap and should be read with care
            "extrapolation_years": end_year - last_year,
            # why the line ends where it does — shown to the reader so a short projection reads as a
            # deliberate limit on a weak series, not as missing data
            "horizon_reason": horizon_reason,
            "method": f"linear least-squares, {len(pts)} pts {pts[0][0]}-{pts[-1][0]}",
        })
    out.sort(key=lambda f: (-abs(f["cagr_pct"] or 0), f["country"], f["metric"]))
    return out

def update_predictions(data_dir, forecasts, series, week):
    """Log each projection once; resolve it when the actual for that year appears in the workbook."""
    path = os.path.join(data_dir, "predictions.json")
    led = load(path, [])
    seen = {(p["country"], p["metric"], p["target_year"]) for p in led}
    for f in forecasts:
        for pr in f["projection"]:
            key = (f["country"], f["metric"], pr["year"])
            if key not in seen:
                led.append({"country": f["country"], "metric": f["metric"], "target_year": pr["year"],
                            "projected_value": pr["value"], "made_on_week": week, "method": f["method"],
                            "resolved": False, "actual_value": None, "abs_pct_error": None, "resolved_week": None})
                seen.add(key)
    actual = {(c, m, y): v for (c, m), pts in series.items() for (y, v, _p) in pts}
    for p in led:
        if p["resolved"]:
            continue
        a = actual.get((p["country"], p["metric"], p["target_year"]))
        if a is not None:
            p["actual_value"] = a; p["resolved"] = True; p["resolved_week"] = week
            p["abs_pct_error"] = round(abs(a - p["projected_value"]) / abs(a) * 100, 1) if a else None
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(led, fh, ensure_ascii=False, indent=2)
    resolved = [p for p in led if p["resolved"] and p["abs_pct_error"] is not None]
    mape = round(sum(p["abs_pct_error"] for p in resolved) / len(resolved), 1) if resolved else None
    return {"total": len(led), "resolved": len(resolved), "mape": mape}

ATM_NAME = {"GR":"Greece","RO":"Romania","BG":"Bulgaria","HU":"Hungary","CZ":"Czech Republic",
            "SK":"Slovakia","HR":"Croatia","SI":"Slovenia","AT":"Austria","CY":"Cyprus","RS":"Serbia",
            "UA":"Ukraine","AL":"Albania","BA":"Bosnia & Herzegovina","MK":"North Macedonia",
            "ME":"Montenegro","XK":"Kosovo"}
# Headline RBR series to fold into the deterministic baselines (the rest of the RBR data lives in the
# Products ATM-market section, with RBR's own forecasts). Keep this list tight so the baselines stay a
# focused reference, not a 200-row dump.
ATM_BASELINE_METRICS = { "Cash withdrawals — annual number",
                        "Cash withdrawals — annual value (USD)"}   # "ATM installed base" left out on purpose (08/09/2026): RBR's ATM count is now drawn ON the ATMs chart as another source, so a second ATM row per market would show the same thing twice

def merge_atm_baselines(series, data_dir, units=None, sources=None):
    """Fold the headline RBR ATM-market history (per country) into the forecast input so the baselines also
    cover the knowledge-base data — never overriding an existing workbook (country, metric)."""
    data = load(os.path.join(data_dir, "atm_market.json"), {})
    arr = data.get("series", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    added = 0
    for s in arr:
        if s.get("metric") not in ATM_BASELINE_METRICS:
            continue
        key = (ATM_NAME.get(s.get("country"), s.get("country")), s.get("metric"))
        if key in series:                      # never clobber a workbook series
            continue
        # RBR's annual withdrawal count is the same thing the ECB counts, once the ECB halves are added
        # up — so where an ECB cash row exists it goes ON that chart as another source (attach_alt_series)
        # instead of standing as a second row. It stays its own row only where there is no ECB series.
        if s.get("metric") == "Cash withdrawals — annual number":
            if (key[0], "Cash withdrawals") in series:
                continue                      # the ECB counts it there; RBR goes on that chart as another source
            key = (key[0], "Cash withdrawals")   # no ECB series: RBR's count is the row, under the one shared name
        pts = sorted((int(p["year"]), float(p["value"]), False)
                     for p in (s.get("history") or []) if isinstance(p.get("value"), (int, float)))
        if len(pts) < 3:
            continue
        series[key] = pts
        if units is not None and s.get("unit"):
            units[key] = (str(s["unit"]), str(s["unit"]))
            if key[1] == "Cash withdrawals":
                units[key] = ("million withdrawals per year", "million ATM cash withdrawals per year (RBR)")
        if sources is not None:
            sources[key] = "RBR ATM Market & Forecasts to 2028"
        added += 1
    if added:
        print(f"merged {added} RBR ATM baseline series from atm_market.json")
    return series

# Other organisations' readings of the same thing, shown as points beside the recorded line. Only where
# the units mean the same: an RBR "ATM installed base" and an ECB "ATMs" are both counts of machines, an
# RBR "Bank branches" and an ECB "Bank branches" both counts of offices. RBR's cash-withdrawal series are
# in millions per year and USD billions — not the same axis as the ECB per-period counts — so they stay off.
_ALT_RBR = {"ATM installed base": "ATMs", "Bank branches": "Bank branches",
            "Cash withdrawals — annual number": "Cash withdrawals"}   # only onto ECB count rows, see below
_ALT_ECB = {"atms": "ATMs", "branches": "Bank branches"}
_ALT_RBR_SOURCE = "RBR ATM Market & Forecasts to 2028"
_ALT_ECB_SOURCE = "ECB Data Portal"

def load_atm_extra_sources(data_dir):
    """The extra ATM sources the Products tab plots, read from dashboard-web/atm-sources.js
    (`window.ATM_EXTRA_SOURCES = {...};`). Returns {} when the file is not there."""
    cands = [os.path.join(data_dir, "..", "dashboard-web", "atm-sources.js"),
             os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                          "dashboard-web", "atm-sources.js")]
    for path in cands:
        try:
            with open(path, encoding="utf-8") as fh:
                txt = fh.read()
        except FileNotFoundError:
            continue
        m = re.search(r"ATM_EXTRA_SOURCES\s*=\s*(\{.*?\})\s*;?\s*$", txt, re.S | re.M)
        if not m:
            return {}
        try:
            return json.loads(m.group(1))
        except ValueError:
            # the object may not end at the first line end; take everything to the last brace
            try:
                return json.loads(txt[txt.index("{", txt.index("ATM_EXTRA_SOURCES")):txt.rindex("}") + 1])
            except ValueError:
                return {}
    return {}

def attach_alt_series(forecasts, data_dir, code2name):
    """forecast row -> row['alt_series'] = [{source, unit, points:[{year,value,provisional}]}], one per other
    organisation that measured the same thing for that market. The row's own source is never repeated."""
    rows = {(f["country"], f["metric"]): f for f in forecasts}
    for f in forecasts:
        f["alt_series"] = []
    # RBR
    am = load(os.path.join(data_dir, "atm_market.json"), {})
    for sr in (am.get("series", []) if isinstance(am, dict) else []):
        tgt = _ALT_RBR.get(sr.get("metric"))
        if not tgt:
            continue
        f = rows.get((ATM_NAME.get(sr.get("country"), sr.get("country")), tgt))
        if not f:
            continue
        own = (f.get("source") or "").startswith("RBR")     # RBR IS the recorded line on this row
        if sr.get("metric") == "Cash withdrawals — annual number" and not own \
           and not str(f.get("unit") or "").startswith("million card cash"):
            continue   # a value-in-local-currency or cash-in-circulation row is not the same axis
        pts = [] if own else [{"year": int(p["year"]), "value": float(p["value"]), "provisional": False}
                              for p in (sr.get("history") or []) if isinstance(p.get("value"), (int, float))]
        # RBR's OWN forecast (to 2028), drawn dashed from the end of its history — asked for on 08/09/2026
        fc_pts = [{"year": int(p["year"]), "value": float(p["value"])}
                  for p in (sr.get("forecast") or []) if isinstance(p.get("value"), (int, float))]
        if pts or fc_pts:
            f["alt_series"].append({"source": _ALT_RBR_SOURCE, "unit": sr.get("unit") or "ATMs",
                                    "points": pts, "projection": fc_pts, "own": own})
    # ECB — only where the row's recorded line comes from somewhere else (e.g. Greece from the HBA workbook)
    ecb = load(os.path.join(data_dir, "structural_series.json"), {})
    meta = ecb.get("meta", {}) if isinstance(ecb, dict) else {}
    for cc, metrics in (ecb.get("series", {}) if isinstance(ecb, dict) else {}).items():
        for mkey, tgt in _ALT_ECB.items():
            pts_raw = metrics.get(mkey) or []
            f = rows.get((code2name.get(cc, cc), tgt))
            if not f or not pts_raw or (f.get("source") or "").startswith("ECB"):
                continue
            pts = [{"year": int(p["year"]), "value": float(p["value"]), "provisional": bool(p.get("provisional"))}
                   for p in pts_raw if isinstance(p.get("value"), (int, float))]
            if pts:
                f["alt_series"].append({"source": _ALT_ECB_SOURCE, "unit": (meta.get(mkey) or {}).get("unit") or "",
                                        "points": pts})
    # National sources and the World Bank / IMF FAS — the same extra sources the Products tab plots on its
    # "ATM numbers and forecast to 2028" chart (dashboard-web/atm-sources.js). Asked 10/09/2026: every
    # source a Products chart shows must also be on the Charts tab, so the anchor sees every reported point.
    extra = load_atm_extra_sources(data_dir)
    n_extra = 0
    for code, lst in extra.items():
        name = code2name.get(code)
        f = rows.get((name, "ATMs")) or rows.get((name, "ATM installed base"))
        if not f or not name:
            continue
        own_hist = {int(h["year"]): float(h["value"]) for h in (f.get("history") or [])}
        have = {a.get("source") for a in f["alt_series"]}
        for sx in lst:
            pts = [{"year": int(p["year"]), "value": float(p["value"]), "provisional": False}
                   for p in (sx.get("rec") or []) if isinstance(p.get("value"), (int, float))]
            if not pts or sx.get("src") in have:
                continue
            # the same numbers as the row's own line (e.g. the HBA series on the Greek row) are not another reading
            overlap = [pt for pt in pts if pt["year"] in own_hist]
            if len(overlap) >= 2 and all(abs(own_hist[pt["year"]] - pt["value"]) < 0.5 for pt in overlap):
                continue
            proj = [{"year": int(p["year"]), "value": float(p["value"])}
                    for p in (sx.get("proj") or []) if isinstance(p.get("value"), (int, float))]
            f["alt_series"].append({"source": sx.get("src"), "unit": "ATMs", "points": pts,
                                    "projection": proj, "url": sx.get("url"), "tier": sx.get("tier")})
            have.add(sx.get("src")); n_extra += 1
    if n_extra:
        print(f"national / World Bank ATM sources attached from atm-sources.js: {n_extra}")
    n = sum(len(f["alt_series"]) for f in forecasts)
    npj = sum(1 for f in forecasts for a in f["alt_series"] if a.get("projection"))
    print(f"other-source overlays attached: {n} across {sum(1 for f in forecasts if f['alt_series'])} rows; "
          f"{npj} carry the source's own projection")
    return forecasts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    ap.add_argument("--horizon", type=int, default=2,
                    help="fallback window (years) for a series that already reaches its target year; "
                         "normally the projection ends at run_year+1, or run_year+2 when the series "
                         "has recent data and a non-Low fit")
    ap.add_argument("--min-points", type=int, default=3)
    args = ap.parse_args()

    _ts = load(os.path.join(args.data, "timeseries.json"), [])
    series = build_series(_ts)
    units = build_units(_ts)
    sources = build_sources(_ts)
    retitle_cash_rows(series, units, sources)
    series = merge_atm_baselines(series, args.data, units, sources)
    run_year = datetime.date.fromisoformat(args.week).year
    forecasts = make_forecasts(series, run_year, args.horizon, args.min_points, units, sources)
    _fp = load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "footprint.json"), {})
    attach_alt_series(forecasts, args.data, {c["code"]: c["name"] for c in _fp.get("countries", [])})
    accuracy = update_predictions(args.data, forecasts, series, args.week)

    payload = {"generated_week": args.week, "horizon": args.horizon,
               "accuracy": accuracy, "forecasts": forecasts,
               "coverage": make_coverage(series, args.min_points)}
    with open(os.path.join(args.data, "forecast.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"forecast.json: {len(forecasts)} projections | predictions ledger: "
          f"{accuracy['total']} ({accuracy['resolved']} resolved, MAPE={accuracy['mape']})")

if __name__ == "__main__":
    main()
