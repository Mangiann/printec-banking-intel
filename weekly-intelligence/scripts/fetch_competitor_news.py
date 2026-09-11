#!/usr/bin/env python3
"""
fetch_competitor_news.py - Tier-0 cache of competitor newsroom posts from vendor sites that
expose a no-auth WordPress REST feed (.../wp-json/wp/v2/posts). Writes
intel-cache/competitor_news.json.

This is a FLOOR, not a ceiling. It exists because some competitors' GLOBAL sites are pure JS
with no API (e.g. mellongroup.com - verified no wp-json / no /api / no __NEXT_DATA__), yet
their COUNTRY sites are WordPress and expose full article bodies as clean JSON (mellon.rs,
mellon.bg, mellon.hr, mellon.ro - verified 2026-06-25). A script can't be JS-blocked the way
WebFetch can, so caching these guarantees the known machine-readable feeds are NEVER missed.

DELIBERATELY belt-and-suspenders (per the operator's 2026-06-25 decision): the deterministic
cache here does NOT replace Agent 6's free research - the agent STILL sweeps every newsroom +
local press every run (new sites, new players, and JS-only globals like mellongroup.com via
Chrome are not covered here). Deterministic where we KNOW a feed exists, AND free search on top.

Config-driven: add a competitor + its WordPress base URL(s) to SITES to extend (any vendor site
where .../wp-json/wp/v2/posts returns JSON qualifies). tier/threat/latest stay in
references/competitors.json; this is purely the sourcing map.

Usage: python fetch_competitor_news.py --data <intel-cache> [--days 180] [--per-site 30] [--week YYYY-MM-DD]
Best-effort: a failing site is skipped; the previously cached file is kept if NOTHING succeeds
(mirrors fetch_ted.py / fetch_prozorro.py).
"""
import argparse, json, os, re, html, time, datetime, urllib.request, urllib.error

# A browser UA is harmless and avoids the rare default-UA block; wp-json works without it too.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# Known competitor newsrooms that expose a WordPress REST feed (.../wp-json/wp/v2/posts).
# Verified live 2026-06-25 by probing the whole watchlist. Extend freely: any vendor site where
# that endpoint returns JSON posts qualifies. The OEMs/globals (NCR Atleos, Diebold, Glory,
# Worldline, Euronet, KEBA, Loomis, Brink's) and several local players (BORICA, myPOS, JCC,
# Viva.com, Paynetics, Evrotrust, Datecs, IBA Group, Uni Systems, Qualco, PayPoint RO, PayU,
# Sirma, ADACOM) are NOT WordPress -> they stay free-search only. AllSecure was skipped (its
# feed is just the default "Hello world!" placeholder, no real news).
SITES = {
    "Mellon Group": [
        {"country": "RS", "base": "https://www.mellon.rs"},   # richest feed (OTP QMS, ProCredit POS, Raiffeisen POS)
        {"country": "BG", "base": "https://mellon.bg"},
        {"country": "HR", "base": "https://mellon.hr"},
        {"country": "RO", "base": "https://mellon.ro"},        # /posts mostly older; recent RO news via free search/press
    ],
    "Asseco SEE / Payten": [
        {"country": "SEE", "base": "https://asee.io"},          # DIRECT competitor; authoritative (e.g. "SEPA for 14 banks in Serbia")
    ],
    "Netopia Payments": [
        {"country": "RO", "base": "https://netopia-payments.com"},   # live RO payments news incl. leadership changes
    ],
    "DAAC digital": [
        {"country": "RO", "base": "https://daacdigital.com"},   # Diebold partner / RO-MD ATM field-service rival
    ],
    "Profile Software": [
        {"country": "GR", "base": "https://www.profilesw.com"},  # GR banking-software competitor
    ],
    "SelfPay (ZebraPay)": [
        {"country": "RO", "base": "https://selfpay.ro"},        # RO self-service/kiosk; feed mixes consumer SEO + corporate news
    ],
    "EuPlatesc (Eupay)": [
        {"country": "RO", "base": "https://www.euplatesc.ro"},  # RO gateway; feed is marketing-heavy
    ],
    "Vpayments": [
        {"country": "CY", "base": "https://vpayments.com.cy"},  # CY acquiring (Worldline partner)
    ],
    "Force1": [
        {"country": "RO", "base": "https://force1.ro"},         # RO CIT (small feed)
    ],
}

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean(s):
    if not s:
        return ""
    return WS_RE.sub(" ", html.unescape(TAG_RE.sub(" ", s))).strip()


def rendered(field):
    """WP fields arrive as {'rendered': '...'} (or occasionally a bare string)."""
    if isinstance(field, dict):
        return field.get("rendered", "") or ""
    return field or ""


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def fetch_site(base, per_site, cutoff):
    """Pull recent NEWS items (the WP /posts feed only) from a site. We deliberately do NOT fall
    back to /pages: pages are static/nav content (Home, Contact, product blurbs) that would
    pollute the news cache. A site with no current posts simply contributes nothing - the agent's
    free search covers the rest. Returns a list of normalised rows (may be empty)."""
    url = (f"{base}/wp-json/wp/v2/posts?per_page={per_site}"
           f"&_fields=date,modified,link,title,excerpt&orderby=date&order=desc")
    try:
        data = json.loads(get(url))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    rows = []
    for p in data:
        date = (p.get("date") or "")[:10]
        mod = (p.get("modified") or "")[:10]
        # filter on the PUBLISH date (a stale post merely re-saved shouldn't resurface as news)
        if cutoff and date and date < cutoff:
            continue
        rows.append({
            "date": date,
            "modified": mod,
            "title": clean(rendered(p.get("title"))),
            "excerpt": clean(rendered(p.get("excerpt")))[:600],
            "link": p.get("link", ""),
        })
    rows.sort(key=lambda r: (r["date"] or r["modified"] or ""), reverse=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--days", type=int, default=180, help="keep posts whose PUBLISH date is within this many days")
    ap.add_argument("--per-site", type=int, default=30)
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    try:
        week = datetime.date.fromisoformat(args.week)
    except ValueError:
        week = datetime.date.today()
    cutoff = (week - datetime.timedelta(days=args.days)).isoformat()

    os.makedirs(args.data, exist_ok=True)
    out_path = os.path.join(args.data, "competitor_news.json")

    competitors = {}
    any_success = False
    for name, sites in SITES.items():
        posts = []
        for s in sites:
            rows = fetch_site(s["base"], args.per_site, cutoff)
            for r in rows:
                r["country"] = s["country"]
                r["source_site"] = s["base"]
            if rows:
                any_success = True
            posts.extend(rows)
            time.sleep(0.3)  # be polite
        posts.sort(key=lambda r: (r["modified"] or r["date"] or ""), reverse=True)
        competitors[name] = {"sites": [s["base"] for s in sites], "count": len(posts), "posts": posts}
        print(f"competitor_news {name}: {len(posts)} post(s) since {cutoff} across {len(sites)} site(s)")

    if not any_success and os.path.exists(out_path):
        print("competitor_news: nothing fetched - keeping existing cache.")
        return

    payload = {
        "generated": week.isoformat(),
        "source": "Competitor WordPress REST feeds (.../wp-json/wp/v2/posts), public, no auth",
        "note": ("FLOOR, not ceiling: caches KNOWN machine-readable competitor newsrooms so they are never "
                 "missed (esp. where the GLOBAL site is JS-only but the COUNTRY sites are WordPress, e.g. "
                 "Mellon: mellongroup.com is JS with no API, but mellon.rs/.bg/.hr/.ro expose wp-json). "
                 "Agent 6 must STILL do free newsroom + local-press search on top - new sites, new players, "
                 "and JS-only globals (mellongroup.com via Chrome) are NOT covered here."),
        "window_days": args.days,
        "competitors": competitors,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    total = sum(c["count"] for c in competitors.values())
    print(f"competitor_news.json: {total} post(s) across {len(competitors)} competitor(s) -> {out_path}")


if __name__ == "__main__":
    main()
