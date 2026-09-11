#!/usr/bin/env python3
"""
fetch_ecb.py — pull the multi-year structural series for the EU footprint from the ECB Data Portal API
and write intel-cache/structural_series.json. ingest.py merges this into series.json/timeseries.json so
the dashboard charts a trend per country/metric (and forecast.py projects them).

Public API, no auth. Half-yearly series (ATMs/POS/cash) are reduced to ONE annual point per year
(the latest half available, S2 preferred). Every value is copied straight from ECB — nothing invented;
provisional ECB observations (OBS_STATUS P/E) are flagged so the engine marks them ◇.

Usage: python fetch_ecb.py --data <intel-cache> [--start 2016]
"""
import argparse, json, os, csv, io, datetime, urllib.request, urllib.error

COUNTRIES = ["GR", "CY", "AT", "HR", "SI", "SK", "BG", "RO", "HU", "CZ"]   # ECB-covered EU footprint

# metric -> (dataflow, key-template with {cc}, granularity, label, unit)
METRICS = {
    "atms":     ("PTN", "H.{cc}.W0.2221._T.PN",            "half",   "ATMs",            "terminals"),
    "pos":      ("PTN", "H.{cc}.W0.2222._T.PN",            "half",   "POS terminals",   "terminals"),
    "branches": ("SSI", "A.{cc}.122C.N40.1.A1.Z0Z.Z",      "annual", "Bank branches",   "offices"),
    # a FLOW, not a stock: the two half-years are added to make the year (see to_annual); the ECB
    # reports the count in millions, so the unit says so
    "cash":     ("PAY", "H.{cc}.W0.CW1.1._Z.N.PN",         "half-sum", "Cash withdrawals","million card cash withdrawals per year"),
}
BASE = "https://data-api.ecb.europa.eu/service/data"

def fetch_csv(flow, key, start):
    url = f"{BASE}/{flow}/{key}?format=csvdata&startPeriod={start}"
    req = urllib.request.Request(url, headers={"User-Agent": "printec-intel/1.0", "Accept": "text/csv"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8"), url

def parse_rows(text):
    """yield (country_code, period, value, provisional) from an ECB csvdata response."""
    rd = csv.DictReader(io.StringIO(text))
    for row in rd:
        cc = row.get("REF_AREA"); per = row.get("TIME_PERIOD"); raw = row.get("OBS_VALUE")
        if not cc or not per or raw in (None, "", "NaN"):
            continue
        try:
            val = float(raw)
        except ValueError:
            continue
        prov = (row.get("OBS_STATUS") or "").strip().upper() in ("P", "E", "B")
        yield cc, per, val, prov

def to_annual(rows, granularity):
    """Collapse to one point per (country, year).
    - "annual":   the year's own value.
    - "half":     a STOCK (ATMs, terminals) — the latest half available (S2 over S1).
    - "half-sum": a FLOW (withdrawals) — S1 + S2 added; a year with only one half so far is kept but
                  flagged provisional, because half a year of withdrawals is not a year of withdrawals.
    Returns {cc: [(year, value, provisional), ...]} sorted by year."""
    acc = {}   # (cc, year) -> {rank: (value, prov)}
    for cc, per, val, prov in rows:
        if granularity == "annual":
            if not per.isdigit():
                continue
            year, rank = int(per), 0
        else:
            if "-S" not in per:
                continue
            y, sh = per.split("-S")
            if not y.isdigit():
                continue
            year, rank = int(y), int(sh) if sh.isdigit() else 0
        acc.setdefault((cc, year), {})[rank] = (val, prov)
    out = {}
    for (cc, year), halves in acc.items():
        if granularity == "half-sum":
            value = sum(v for v, _ in halves.values())
            provisional = any(p for _, p in halves.values()) or (len(halves) < 2)
        else:
            rank = max(halves)
            value, provisional = halves[rank]
        out.setdefault(cc, []).append({"year": year, "value": round(value, 3), "provisional": bool(provisional)})
    for cc in out:
        out[cc].sort(key=lambda p: p["year"])
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--start", default="2016")
    args = ap.parse_args()

    series = {cc: {} for cc in COUNTRIES}
    meta = {}
    cc_join = "+".join(COUNTRIES)
    for mkey, (flow, tmpl, gran, label, unit) in METRICS.items():
        key = tmpl.format(cc=cc_join)
        try:
            text, url = fetch_csv(flow, key, args.start)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  WARN {mkey}: fetch failed ({e}) — skipped")
            continue
        annual = to_annual(parse_rows(text), gran)
        n = 0
        for cc, pts in annual.items():
            if cc in series and pts:
                series[cc][mkey] = pts
                n += len(pts)
        meta[mkey] = {"label": label, "unit": unit, "flow": flow,
                      "source_url": f"{BASE}/{flow}/{tmpl.format(cc=cc_join)}?format=csvdata&startPeriod={args.start}"}
        cc_with = sum(1 for cc in series if mkey in series[cc])
        print(f"  {mkey:9} {label:16} -> {cc_with} countries, {n} annual points")

    payload = {
        "generated": datetime.date.today().isoformat(),
        "source": "ECB Data Portal (data-api.ecb.europa.eu)",
        "note": "Annual points: stocks (ATMs, POS) = latest half-year per year (S2 preferred); flows (cash withdrawals) = S1 + S2 added, a year with one half so far flagged provisional. Provisional ECB obs (P/E) flagged.",
        "meta": meta,
        "series": {cc: m for cc, m in series.items() if m},
    }
    os.makedirs(args.data, exist_ok=True)
    out = os.path.join(args.data, "structural_series.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    tot = sum(len(p) for cc in payload["series"].values() for p in cc.values())
    print(f"structural_series.json: {len(payload['series'])} countries, "
          f"{sum(len(v) for v in payload['series'].values())} series, {tot} points -> {out}")

if __name__ == "__main__":
    main()
