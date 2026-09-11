#!/usr/bin/env python3
"""
fetch_prozorro.py - Tier-0 sweep of Ukraine's Prozorro for Printec-relevant bank tenders
& awards, via the public search API (POST https://prozorro.gov.ua/api/search/tenders,
no auth). Writes intel-cache/prozorro_notices.json. Real notices only; nothing invented.

Closes the standing Ukraine blind spot: tender.privatbank.ua is an Angular SPA and every
Prozorro mirror 403s to WebFetch, so the agent cannot reach this data interactively. The
public search API answers a POST and a script cannot misread it.

Two sweeps:
  1. TARGET ENTITIES (PrivatBank, Oschadbank by EDRPOU) x ATM/cash keywords - the precise
     in-scope tenders of the banks Printec sells to / defends incumbency at. (Multi-word
     `text` ANDs the terms, so "<edrpou> банкомат" returns only that buyer's ATM tenders.)
  2. FOOTPRINT KEYWORD SWEEP - each ATM/cash keyword alone, first pages, to surface ANY
     Ukrainian buyer's ATM/self-service tenders and (via status) which are awarded.

NOTE on winners: the search result carries tenderID/title/value/status but NOT the winner
name, and the winner CANNOT be scripted from the friendly tenderID - the portal search omits
the tender UUID, there is no public friendly-ID->UUID resolver, and the CDB
(public.api.openprocurement.org/api/2.5/tenders/<UUID>) needs the UUID (verified 2026-06-25).
`status` in (complete, active.awarded) means an award exists. So each awarded row now carries
the route to the supplier instead: `pb_platform_id` / `pb_platform_url` (the bank's own
tender.privatbank.ua page extracted from the title - the authoritative place the supplier is
published), the prozorro `link`, and `buyer_email`. Reading the winner is an operator/Chrome
step by design. Agent 2 captures those winners for Agent 6.

Usage: python fetch_prozorro.py --data <intel-cache> [--pages 8] [--sweep-pages 5]
Best-effort: on any network/HTTP error the previously cached file is kept and the run
still succeeds (mirrors fetch_ecb.py / fetch_competitors.py).
"""
import argparse, json, os, re, time, datetime, urllib.request, urllib.error

API = "https://prozorro.gov.ua/api/search/tenders"
# Many bank tenders embed the bank's own commercial-platform ID in the title, e.g.
# "...(ID тендера на 'tender.privatbank.ua': PB-2026-01-29-3067524)". That platform page is the
# AUTHORITATIVE place the winning supplier is published (the Prozorro public search/CDB expose the
# friendly tenderID but NOT a UUID, and there is no public friendly->UUID resolver, so the winner
# name cannot be scripted from the friendly ID alone). Extracting the PB-* id gives the agent/operator
# the direct link to read the supplier, instead of a dead "open the Prozorro page" instruction.
PB_ID_RE = re.compile(r"\bPB-\d{4}-\d{2}-\d{2}-\d+\b")
PB_PLATFORM_URL = "https://tender.privatbank.ua/commercial/tender/{}"
UA = "Printec Market Intelligence research@printecgroup.example"
TENDER_URL = "https://prozorro.gov.ua/tender/{}"

# Target buyers by EDRPOU (only the codes documented in the Agent-2 brief - not invented).
# Add more EDRPOUs here to widen the entity sweep.
TARGETS = {
    "14360570": "PrivatBank",
    "00032129": "Oschadbank",
}

# ATM / cash-automation / self-service keywords (Ukrainian + Latin). Each is ANDed with the
# EDRPOU for the entity sweep, and run alone for the footprint sweep.
KEYWORDS = [
    "банкомат",                # банкомат (ATM - also catches "ресайклінгові банкомати", i.e. recycler ATMs)
    "самообслуговув",  # самообслуговув (self-service)
    "кіоск",                    # кіоск (kiosk)
    "платіжний термінал",  # платіжний термінал (payment terminal)
]
# NB: bare recycler words are DELIBERATELY excluded - they are ambiguous in Ukrainian
# procurement: "ресайклер" = asphalt road-recycler, "рециркулятор" = air recirculator,
# "ресайклінг" = recycling-art/waste. Recycler ATMs are reliably caught by "банкомат"
# (they are titled "ресайклінгові банкомати"). A bare Latin "ATM" was likewise dropped
# (it fuzzy-matched road-repair tenders).

AWARDED_STATUSES = {"complete", "active.awarded"}


def post(body):
    req = urllib.request.Request(
        API, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def row(t):
    pe = (t.get("procuringEntity") or {})
    ident = pe.get("identifier") or {}
    contact = pe.get("contactPoint") or {}
    addr = pe.get("address") or {}
    val = t.get("value") or {}
    tid = t.get("tenderID", "")
    title = (t.get("title") or "").strip()
    status = t.get("status", "")
    m = PB_ID_RE.search(title)
    pb_id = m.group(0) if m else ""
    return {
        "tenderID": tid,
        "title": title,
        "buyer": ident.get("legalName") or pe.get("name") or "",
        "buyer_edrpou": ident.get("id") or "",
        # buyer contact + region (the portal search already returns these) so the operator can
        # chase the award outcome directly instead of re-deriving who to contact.
        "buyer_email": contact.get("email") or "",
        "buyer_phone": contact.get("telephone") or "",
        "buyer_region": addr.get("region") or "",
        "value": val.get("amount"),
        "currency": val.get("currency"),
        "status": status,
        "awarded": status in AWARDED_STATUSES,
        "link": TENDER_URL.format(tid) if tid else "",
        # the bank's own platform id + link = where the winning supplier is actually published
        "pb_platform_id": pb_id,
        "pb_platform_url": PB_PLATFORM_URL.format(pb_id) if pb_id else "",
    }


def collect(text, max_pages, only_edrpou=None, seen=None):
    """Paginate a text search; return list of rows (optionally only this buyer's EDRPOU)."""
    out, page = [], 1
    while page <= max_pages:
        try:
            d = post({"text": text, "page": page})
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"  warn: query {text!r} page {page} failed ({type(e).__name__}: {e})")
            break
        data = d.get("data") or []
        if not data:
            break
        for t in data:
            r = row(t)
            if only_edrpou and r["buyer_edrpou"] != only_edrpou:
                continue
            if seen is not None:
                if r["tenderID"] in seen:
                    continue
                seen.add(r["tenderID"])
            out.append(r)
        total = d.get("total") or 0
        if page * d.get("per_page", 20) >= total:
            break
        page += 1
        time.sleep(0.2)  # be polite to the public API
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--pages", type=int, default=8, help="max pages per entity x keyword query")
    ap.add_argument("--sweep-pages", type=int, default=5, help="max pages per footprint keyword query")
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    os.makedirs(args.data, exist_ok=True)
    out_path = os.path.join(args.data, "prozorro_notices.json")

    entities = {}
    footprint = []
    any_success = False
    try:
        # 1. target-entity sweep (EDRPOU AND keyword)
        for edrpou, name in TARGETS.items():
            seen = set()
            rows = []
            for kw in KEYWORDS:
                rows.extend(collect(f"{edrpou} {kw}", args.pages, only_edrpou=edrpou, seen=seen))
            rows.sort(key=lambda r: (not r["awarded"], r["tenderID"]), reverse=False)
            entities[name] = {"edrpou": edrpou, "count": len(rows),
                              "awarded": sum(1 for r in rows if r["awarded"]), "tenders": rows}
            any_success = True
            print(f"Prozorro {name} ({edrpou}): {len(rows)} ATM/cash tenders ({entities[name]['awarded']} awarded)")

        # 2. footprint keyword sweep (any UA buyer)
        seen = set(r["tenderID"] for e in entities.values() for r in e["tenders"])
        for kw in KEYWORDS:
            footprint.extend(collect(kw, args.sweep_pages, seen=seen))
            any_success = True
        footprint.sort(key=lambda r: (not r["awarded"], r["tenderID"]))
        print(f"Prozorro footprint sweep: {len(footprint)} further ATM/cash tenders across UA buyers "
              f"({sum(1 for r in footprint if r['awarded'])} awarded)")
    except Exception as e:
        print(f"warn: Prozorro sweep error ({type(e).__name__}: {e})")

    if not any_success and os.path.exists(out_path):
        print("Prozorro: no data fetched - keeping existing cache.")
        return

    payload = {
        "generated": args.week,
        "source": "Prozorro public search API (POST api/search/tenders), no auth",
        "note": ("winner name is NOT available from the public search and CANNOT be scripted from the "
                 "friendly tenderID: the portal search omits the tender UUID and there is no public "
                 "friendly-ID->UUID resolver, while the CDB (public.api.openprocurement.org) needs the "
                 "UUID. status complete/active.awarded => an award exists. To read the WINNING SUPPLIER: "
                 "(1) prefer `pb_platform_url` when present (the bank's own tender.privatbank.ua page, the "
                 "authoritative source) - load it with Claude-in-Chrome / desktop browser; (2) else open "
                 "`link` (prozorro.gov.ua/tender/<id>) in Chrome; (3) the buyer_email is a direct route to "
                 "ask. This is an operator/Chrome step by design, not a script gap."),
        "targets": TARGETS,
        "keywords": KEYWORDS,
        "entities": entities,
        "footprint_other_buyers": footprint,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"prozorro_notices.json -> {out_path}")


if __name__ == "__main__":
    main()
