#!/usr/bin/env python3
"""
fetch_ted.py - Tier-0 sweep of TED (Tenders Electronic Daily) for Printec-relevant
public tenders & awards across the EU footprint, via the public TED Search API v3
(POST https://api.ted.europa.eu/v3/notices/search, no auth). Writes
intel-cache/ted_notices.json: every in-scope notice with publication-number, buyer,
country, CPVs, deadline, value, winner and the canonical notice PDF/HTML/XML links -
so Agent 2's /pdf-read pipeline can triage each one deterministically. Real notices
only; nothing invented.

This closes the standing TED blind spot: the v3 search API is POST-only (a GET 405s)
and the web UI is JS-rendered, so neither WebFetch nor a site: search can enumerate
notices. A POST from this script can - and a script cannot misread a value the way an
agent reading a PDF can.

Usage: python fetch_ted.py --data <intel-cache> [--days 30] [--max 3000] [--week YYYY-MM-DD]
Best-effort: on any network/HTTP error the previously cached file is left in place and
the run still succeeds (mirrors fetch_ecb.py / fetch_competitors.py).
"""
import argparse, json, os, math, datetime, urllib.request, urllib.error

API = "https://api.ted.europa.eu/v3/notices/search"
UA = "Printec Market Intelligence research@printecgroup.example"

# Footprint EU member states (TED uses ISO-3166 alpha-3). Non-EU footprint
# (RS, UA, AL, BA, XK, ME, MK) is NOT on TED - it is covered by the national portals.
COUNTRIES = ["GRC", "ROU", "BGR", "HRV", "SVN", "CZE", "SVK", "HUN", "CYP", "AUT"]

# Targeted CPV roots (TED matches an 8-digit root against its whole family). Deliberately
# NARROW: the broad roots 48000000 (all software), 72000000 (all IT services) and
# 66000000 (all financial/insurance services) flood the feed with thousands of
# irrelevant notices (~5,100 vs ~450), so they are excluded here; Printec relevance is
# recovered with KEYWORDS below (which only TAG rows - nothing in-scope is dropped).
CPV = [
    "30123000",  # automatic teller machines / office & business machinery (covers 30123200 ATMs)
    "30144400",  # automatic fare-collection / payment machines
    "30142000",  # accounting machines & cash registers (POS-adjacent)
    "35120000",  # surveillance & security systems (ATM / branch physical security)
    "50310000",  # maintenance & repair of office machinery (ATM maintenance)
    "50312000",  # maintenance & repair of IT / computer equipment
]

# Title keywords flagging HIGH relevance (EN + local langs). Used ONLY to set
# relevant=true on a row; every in-scope notice is still written out.
KEYWORDS = [
    "atm", "automated teller", "cash recycl", "cash machine", "self-service", "self service",
    "kiosk", "cash deposit", "cash dispens", "banknote", "bank note", "coin", "pos terminal",
    "payment terminal", "card terminal", "cash-in-transit", "cash in transit",
    "bancomat", "bankomat", "samoobsluzn", "samopostrezn",
    "банкомат",          # банкомат (BG/SR/UK/MK)
    "самообслуж",  # самообслуж (BG)
    "τραπεζομηχαν",  # τραπεζομηχάν (GR ATM)
    "αυτόματ",                 # αυτόματ (GR self-service)
]

FIELDS = [
    "publication-number", "notice-title", "organisation-name-buyer", "organisation-country-buyer",
    "classification-cpv", "deadline-receipt-tender-date-lot", "tender-value", "total-value-cur",
    "winner-name", "links", "publication-date", "notice-type",
    # framework / drawdown detection (added 2026-06-25): a contract-award notice can be a
    # CALL-OFF / recurring drawdown under a pre-existing framework, where the headline value is
    # the framework CEILING (e.g. 13m CZK) and the winner was chosen years earlier - NOT a fresh
    # win. These fields let the script flag that so the agent never folds a ceiling in as a new win.
    "form-type", "contract-framework-agreement", "framework-notice-id",
    "result-framework-maximum-value-notice", "result-framework-maximum-value-cur-notice",
    "total-value", "contract-conclusion-date", "winner-decision-date",
]


def flat_localized(v):
    """notice-title / org-name / winner-name arrive as {lang:[...]} or list - flatten to one string."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, list):
        return "; ".join(s for s in (flat_localized(x) for x in v) if s)
    if isinstance(v, dict):
        for k in ("eng", "ENG", "en", "ENGLISH"):
            if v.get(k):
                return flat_localized(v[k])
        for vv in v.values():
            s = flat_localized(vv)
            if s:
                return s
    return str(v)


def dedup(seq):
    out = []
    for x in seq:
        if x and x not in out:
            out.append(x)
    return out


def first_date(v):
    if isinstance(v, list):
        v = v[0] if v else ""
    if isinstance(v, str):
        return v.split("+")[0].split("T")[0]
    return ""


def num(v):
    """tender/total/framework value may arrive as a scalar, a list, '' or None - to float|None."""
    if isinstance(v, list):
        v = v[0] if v else None
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def year_of(date_str):
    return date_str[:4] if date_str and date_str[:4].isdigit() else ""


def fw_truthy(v):
    """contract-framework-agreement is an eForms code: 'none' = not a framework; anything else
    (fa-mo / fa-wo-rc / fa-w-rc ...) = IS a framework. Tolerate str/list/dict/bool shapes."""
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        return v.strip().lower() not in ("", "none", "false", "no", "0", "n/a")
    if isinstance(v, list):
        return any(fw_truthy(x) for x in v)
    if isinstance(v, dict):
        return any(fw_truthy(x) for x in v.values())
    return bool(v)


def pick_link(links, kind):
    d = (links or {}).get(kind) or {}
    if not isinstance(d, dict):
        return ""
    return d.get("ENG") or d.get("MUL") or (next(iter(d.values())) if d else "")


def post(body):
    req = urllib.request.Request(
        API, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--days", type=int, default=30, help="publication-date window, days back from --week")
    ap.add_argument("--max", type=int, default=3000, help="safety cap on notices collected")
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    try:
        week = datetime.date.fromisoformat(args.week)
    except ValueError:
        week = datetime.date.today()
    cutoff = (week - datetime.timedelta(days=args.days)).strftime("%Y%m%d")

    query = (f"classification-cpv IN ({' '.join(CPV)}) "
             f"AND organisation-country-buyer IN ({' '.join(COUNTRIES)}) "
             f"AND publication-date >= {cutoff}")

    os.makedirs(args.data, exist_ok=True)
    out_path = os.path.join(args.data, "ted_notices.json")

    LIMIT = 100
    notices, total, page = [], None, 1
    try:
        while len(notices) < args.max:
            body = {"query": query, "fields": FIELDS, "page": page, "limit": LIMIT,
                    "scope": "ALL", "paginationMode": "PAGE_NUMBER"}
            d = post(body)
            if total is None:
                total = d.get("totalNoticeCount") or d.get("total") or 0
                print(f"TED: {total} in-scope notice(s) since {cutoff} for {len(COUNTRIES)} countries x {len(CPV)} CPV families")
            batch = d.get("notices") or []
            if not batch:
                break
            notices.extend(batch)
            if total and len(notices) >= total:
                break
            page += 1
            if page > 200:  # hard safety
                break
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as e:
        detail = ""
        if isinstance(e, urllib.error.HTTPError):
            try:
                detail = " | " + e.read().decode("utf-8")[:300]
            except Exception:
                pass
        print(f"warn: TED fetch failed ({type(e).__name__}: {e}){detail} - keeping existing cache if present.")
        if os.path.exists(out_path):
            return
        # write an empty-but-valid cache so downstream code never crashes
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"generated": week.isoformat(), "source": API, "query": query,
                       "error": str(e), "count": 0, "notices": []}, f, ensure_ascii=False, indent=2)
        return

    rows = []
    for n in notices[:args.max]:
        title = flat_localized(n.get("notice-title"))
        buyer = flat_localized(n.get("organisation-name-buyer"))
        winner = flat_localized(n.get("winner-name"))
        cpvs = dedup(n.get("classification-cpv") or [])
        countries = dedup(n.get("organisation-country-buyer") or [])
        hay = (title + " " + buyer).lower()

        notice_type = n.get("notice-type", "") or ""
        form_type = flat_localized(n.get("form-type"))
        published = first_date(n.get("publication-date"))
        # framework / drawdown detection ---------------------------------------------------
        framework = (fw_truthy(n.get("contract-framework-agreement"))
                     or bool(flat_localized(n.get("framework-notice-id")))
                     or num(n.get("result-framework-maximum-value-notice")) is not None)
        framework_max = num(n.get("result-framework-maximum-value-notice"))
        framework_max_cur = (dedup(n.get("result-framework-maximum-value-cur-notice") or []) or [""])[0]
        awarded_value = num(n.get("total-value"))                       # actual value awarded IN THIS notice
        conclusion_date = first_date(n.get("contract-conclusion-date"))
        winner_decision = first_date(n.get("winner-decision-date"))
        is_award = notice_type.startswith("can") or "result" in (form_type or "").lower()
        is_modification = "modif" in notice_type.lower() or "modif" in (form_type or "").lower()
        # The award DECISION/contract predates this notice's publication YEAR -> recurring drawdown,
        # not a fresh win (catches the Albacon/Ceska posta case: winner chosen 2023, notice 2026).
        py = year_of(published)
        stale_award = bool(py and ((year_of(winner_decision) and year_of(winner_decision) < py)
                                   or (year_of(conclusion_date) and year_of(conclusion_date) < py)))
        # the key flag: treat the headline framework value as a CEILING, not a fresh win.
        framework_drawdown = bool(is_award and (framework or is_modification) and
                                  (stale_award or (framework_max and awarded_value
                                                   and awarded_value < 0.5 * framework_max)))

        rows.append({
            "id": n.get("publication-number"),
            "title": title,
            "buyer": buyer,
            "country": countries[0] if countries else "",
            "cpv": cpvs,
            "deadline": first_date(n.get("deadline-receipt-tender-date-lot")),
            "value": dedup([str(x) for x in (n.get("tender-value") or [])]),
            "currency": dedup(n.get("total-value-cur") or []),
            "winner": winner,
            "notice_type": notice_type,
            "form_type": form_type,
            "published": published,
            # framework / drawdown flags (added 2026-06-25) -------------------------------
            "is_award": is_award,
            "is_modification": is_modification,
            "framework": framework,
            "framework_max_value": framework_max,        # the CEILING - NOT a fresh-award amount
            "framework_max_cur": framework_max_cur,
            "awarded_value": awarded_value,              # actual value awarded in THIS notice
            "contract_conclusion_date": conclusion_date,
            "winner_decision_date": winner_decision,
            "stale_award": stale_award,
            "framework_drawdown": framework_drawdown,     # True => call-off/recurring, do NOT log as a new win
            "pdf_en": pick_link(n.get("links"), "pdf"),
            "html_en": pick_link(n.get("links"), "html"),
            "xml": pick_link(n.get("links"), "xml"),
            "relevant": any(k in hay for k in KEYWORDS),
        })

    rows.sort(key=lambda r: (not r["relevant"], r["deadline"] or "9999", r["country"]))
    relevant = sum(1 for r in rows if r["relevant"])
    drawdowns = sum(1 for r in rows if r.get("framework_drawdown"))
    payload = {
        "generated": week.isoformat(),
        "source": "TED Search API v3 (POST notices/search), public, no auth",
        "query": query,
        "window_days": args.days,
        "countries": COUNTRIES,
        "cpv": CPV,
        "total_in_scope": total,
        "count": len(rows),
        "keyword_relevant": relevant,
        "note": ("framework_drawdown=true means a contract-award notice is a CALL-OFF / recurring "
                 "drawdown under a PRE-EXISTING framework (winner chosen earlier; see "
                 "winner_decision_date / contract_conclusion_date) - the framework_max_value is a "
                 "CEILING, NOT a fresh award. Do NOT report such a notice as a new competitor win; "
                 "use awarded_value for the actual amount in THIS notice. is_modification=true is a "
                 "contract change, also not a new win."),
        "notices": rows,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"ted_notices.json: {len(rows)} notices written ({relevant} keyword-relevant) -> {out_path}")
    awards = [r for r in rows if r["winner"]]
    if awards:
        fresh = [r for r in awards if not r.get("framework_drawdown")]
        print(f"  ...incl. {len(awards)} with a named winner ({len(fresh)} fresh awards, "
              f"{len(awards) - len(fresh)} framework drawdowns/modifications) -> pass FRESH ones to Agent 6")


if __name__ == "__main__":
    main()
