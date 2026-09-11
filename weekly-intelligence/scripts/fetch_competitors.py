#!/usr/bin/env python3
"""
fetch_competitors.py — pull ANNUAL revenue for the US-listed competitors/partner from SEC EDGAR
(company-facts XBRL, public, no auth) and write intel-cache/competitor_series.json. Real filings only —
nothing invented. build_dashboard.py serves it to the Competition-tab competitor chart.

Covers NCR Atleos (Printec's partner), Diebold Nixdorf, Euronet, Brink's. European/Japanese names
(Worldline, Nexi, Glory, Loomis) are not on EDGAR — add them from their annual reports later.

Usage: python fetch_competitors.py --data <intel-cache>
"""
import argparse, json, os, re, datetime, urllib.request, urllib.error

UA = "Printec Market Intelligence research@printecgroup.example"
# display name -> (CIK, ticker)
COMPS = {
    "NCR Atleos":      ("0001974138", "NATL"),
    "Diebold Nixdorf": ("0000028823", "DBD"),
    "Euronet":         ("0001029199", "EEFT"),
    "Brink's":         ("0000078890", "BCO"),
}
REV_TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax"]

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))

def annual_from_concept(cik, tag):
    """Return {year: value} of CALENDAR-YEAR annual revenue from one us-gaap concept."""
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"
    try:
        d = get_json(url)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return {}
    out = {}
    for u in d.get("units", {}).get("USD", []):
        fr = u.get("frame", "")
        if re.fullmatch(r"CY\d{4}", fr):                    # canonical full-year value
            out[int(fr[2:])] = u["val"]
    if not out:                                             # fallback: 10-K full-year periods
        for u in d.get("units", {}).get("USD", []):
            if u.get("form", "").startswith("10-K") and u.get("fp") == "FY" and u.get("start") and u.get("end"):
                try:
                    s = datetime.date.fromisoformat(u["start"]); e = datetime.date.fromisoformat(u["end"])
                except ValueError:
                    continue
                if 350 <= (e - s).days <= 380:
                    out.setdefault(e.year, u["val"])
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--start", type=int, default=2018)
    args = ap.parse_args()
    series = {}
    for name, (cik, tic) in COMPS.items():
        merged = {}
        for tag in REV_TAGS:
            for y, v in annual_from_concept(cik, tag).items():
                merged.setdefault(y, v)        # first tag that has the year wins
        pts = [{"year": y, "value": round(v / 1e6, 1)} for y, v in sorted(merged.items()) if y >= args.start]
        if pts:
            series[name] = {"revenue": pts, "ticker": tic}
        print(f"  {name:16} ({tic}) -> {len(pts)} annual revenue points"
              + (f" {pts[0]['year']}-{pts[-1]['year']}" if pts else " (none)"))
    payload = {
        "generated": datetime.date.today().isoformat(),
        "source": "SEC EDGAR company facts (us-gaap revenue), annual; values in USD millions",
        "meta": {"revenue": {"label": "Total revenue (USD m)", "unit": "USD m"}},
        "series": series,
    }
    os.makedirs(args.data, exist_ok=True)
    out = os.path.join(args.data, "competitor_series.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"competitor_series.json: {len(series)} competitors -> {out}")

if __name__ == "__main__":
    main()
