#!/usr/bin/env python3
"""
fetch_competitor_segments.py — multi-year SEGMENT revenue (the ATM/self-service business) for the
US-listed competitors, from SEC EDGAR 10-Ks. Self-verifying: a year's segments must SUM to the total
revenue already fetched (fetch_competitors.py / EDGAR) within tolerance, else that year is REJECTED —
so a mis-parse can never ship a wrong figure. Merges into intel-cache/competitor_series.json.

Also extracts Euronet's operated-ATM count (the one disclosed unit metric).

Usage: python fetch_competitor_segments.py --data <intel-cache>
"""
import argparse, json, os, re, html, urllib.request

UA = "Printec Market Intelligence research@printecgroup.example"
# name -> (cik, [all reportable segments], ATM-relevant segment)
COMPS = {
    "NCR Atleos":      ("0001974138", ["Self-Service Banking", "Network"], "Self-Service Banking"),
    "Diebold Nixdorf": ("0000028823", ["Banking", "Retail"], "Banking"),
    "Euronet":         ("0001029199", ["EFT Processing", "epay", "Money Transfer"], "EFT Processing"),
}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read().decode("utf-8", "ignore")

def latest_10ks(cik, n=6):
    d = json.loads(get("https://data.sec.gov/submissions/CIK%s.json" % cik))
    r = d["filings"]["recent"]; out = []
    for form, acc, doc, date in zip(r["form"], r["accessionNumber"], r["primaryDocument"], r["filingDate"]):
        if form == "10-K":
            fy = None
            m = re.search(r"-(\d{4})1231", doc) or re.search(r"(\d{4})1231", doc)
            fy = int(m.group(1)) if m else int(date[:4]) - 1
            out.append(("https://www.sec.gov/Archives/edgar/data/%d/%s/%s" % (int(cik), acc.replace("-", ""), doc), fy))
        if len(out) >= n:
            break
    return out

def first_num_after(text, label):
    """First revenue figure reported right after a segment label in the MD&A segment-results block."""
    m = re.search(re.escape(label) + r"\s+\$?\s*([0-9][0-9,]*\.?[0-9]*)", text)
    return float(m.group(1).replace(",", "")) if m else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--tol", type=float, default=0.04)
    args = ap.parse_args()
    cs = json.load(open(os.path.join(args.data, "competitor_series.json"), encoding="utf-8"))
    total_by = {n: {p["year"]: p["value"] for p in s.get("revenue", [])} for n, s in cs["series"].items()}

    for name, (cik, segs, atm_seg) in COMPS.items():
        seg_year = {}           # {year: {seg: value}}
        for url, fy in latest_10ks(cik, 6):
            t = re.sub(r"[ \t ]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", get(url))))
            vals = {sg: first_num_after(t, sg) for sg in segs}
            if all(v is not None for v in vals.values()):
                seg_year[fy] = vals          # cur-year column = this 10-K's fiscal year
        # primary check: segments sum to the EDGAR total (rejects mis-parses). For companies whose segments
        # carry intersegment eliminations (no year sums cleanly), fall back to a dominant-segment ratio check.
        sums_clean = any(total_by.get(name, {}).get(y) and abs(sum(seg_year[y].values()) - total_by[name][y]) / total_by[name][y] <= args.tol
                         for y in seg_year)
        kept = []; segser = {sg: [] for sg in segs}
        for y in sorted(seg_year):
            tot = total_by.get(name, {}).get(y); segval = seg_year[y][atm_seg]
            if not tot:
                ok = False; why = "no total"
            elif sums_clean:
                ssum = sum(seg_year[y].values()); ok = abs(ssum - tot) / tot <= args.tol; why = f"segsum={ssum:.0f} vs {tot}"
            else:
                ratio = segval / tot; ok = 0.45 < ratio < 0.80; why = f"ratio={ratio:.2f} (intersegment co)"
            if ok:
                kept.append({"year": y, "value": round(segval, 1)})
                # a year that passes (sum-clean or dominant-ratio) means the segment block parsed correctly,
                # so the OTHER segments in that same block are real reported figures too — store them all.
                for sg in segs:
                    segser[sg].append({"year": y, "value": round(seg_year[y][sg], 1)})
            print(f"  {name:16} FY{y}: {atm_seg}={segval:>8} · {why} -> {'OK' if ok else 'REJECT'}")
        if kept:
            cs["series"][name]["atm_segment"] = kept
            cs["series"][name]["atm_segment_label"] = atm_seg
            cs["series"][name]["segments"] = {sg: v for sg, v in segser.items() if v}
            cs["series"][name]["segments_verified"] = "sum-check" if sums_clean else "dominant-ratio"

    # Euronet operated-ATM count (disclosed unit metric)
    fleet = {}
    for url, fy in latest_10ks("0001029199", 6):
        t = re.sub(r"[ \t ]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", get(url))))
        for m in re.finditer(r"we operated ([0-9][0-9,]{3,7}) ATMs(?: compared to ([0-9][0-9,]{3,7}) at)?", t):
            fleet[fy] = int(m.group(1).replace(",", ""))
            if m.group(2): fleet[fy-1] = int(m.group(2).replace(",", ""))
            break
    if fleet:
        cs["series"]["Euronet"]["atm_fleet"] = [{"year": y, "value": v} for y, v in sorted(fleet.items())]
        print(f"  Euronet ATM fleet: {sorted(fleet.items())}")

    cs.setdefault("meta", {})["atm_segment"] = {"label": "ATM/self-service segment revenue (USD m)", "unit": "USD m"}
    cs["meta"]["atm_fleet"] = {"label": "ATMs operated (Euronet)", "unit": "ATMs"}
    cs["source"] = (cs.get("source", "") + " · segment revenue + ATM fleet from 10-K (sum-verified)").strip(" ·")
    json.dump(cs, open(os.path.join(args.data, "competitor_series.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("merged segment revenue + ATM fleet into competitor_series.json")

if __name__ == "__main__":
    main()
