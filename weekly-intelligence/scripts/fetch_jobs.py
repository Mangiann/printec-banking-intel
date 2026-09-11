#!/usr/bin/env python3
"""
fetch_jobs.py - Tier-0 cache of footprint bank JOB-BOARD / ATS listings for Agent 5
(Early Intent: Jobs + Leadership) and Agent 1 (Bank Disclosures). Writes
intel-cache/jobs_listings.json: per bank-source the role COUNT, role titles,
locations, posting/deadline dates and apply URLs - pulled by a plain server-side
HTTP request (no browser).

WHY THIS EXISTS (root-cause of the recurring Agent-5 blind spot):
  Agent 5 lives on career pages + job boards, but the highest-signal ones are JS-
  rendered or anti-bot-gated, so a headless run could only read snippet-level role
  *counts* (or nothing). The 24/06/2026 run logged JS/403 blocks on Piraeus/Eurobank
  ATSs, ALL six robota.ua company IDs (UA), Raiffeisen Kosovo, kosovajob.com, jobs.bg
  and karrier.otpbank.hu. Role counts are NUMBERS - and per the playbook ("script the
  numbers, fan out the research") numbers belong in a Tier-0 script, not in an agent's
  snippet-guessing.

WHAT IT IS / IS NOT (the design rule: determinism in plumbing only, never in sourcing):
  This is PLUMBING. It makes blocked listings REACHABLE and caches them raw for a
  research agent to read; it does NOT decide relevance, score signals, or replace the
  agent's free market sweep (LinkedIn, leadership press, local-language boards). It is
  the Jobs-agent analog of fetch_ted.py / fetch_prozorro.py under the standing 24/06/2026
  Chrome decision (close the deterministic blind spots; keep exploration free).

ENDPOINTS (verified reachable by a bare request, 24/06/2026 recon):
  - robota.ua          JSON  GET api.robota.ua/companies/{id}/published-vacancies  (UA x6)
  - Workable           JSON  GET apply.workable.com/api/v1/widget/accounts/{slug}   (Piraeus, Raiffeisen UA)
  - Banca Transilvania JSON  GET cariere.bancatransilvania.ro/hrscapi/...           (RO)
  - SuccessFactors/Erste HTML (server-rendered)  Alpha, NBG, BCR, OTP-HU(first page)
  - poslovi.infostud   HTML  oglasi-za-posao-{slug}                                 (RS x5)
  - FledgeHR           HTML  otpbanka.fledgehr.com/jobs                             (OTP SI)
  - profesia.sk        HTML  profesia.sk/praca/?company_id={id}                     (SK x4)
  - dev.bg             HTML  dev.bg/company/{slug}/                                 (DSK BG)
  BROWSER-ONLY (NOT scripted - left as honest Operator-requests, see BROWSER_ONLY):
  jobs.bg (DataDome+Cloudflare), Bank of Cyprus CSB, NLB Cornerstone, Eurobank GR CSB.

Usage: python fetch_jobs.py --data <intel-cache> [--week YYYY-MM-DD] [--only board] [--debug]
Best-effort: a failing source is recorded with ok=false + error and never aborts the run;
on a total wipe the previous cache is kept (mirrors fetch_ted.py / fetch_prozorro.py).
"""
import argparse, json, os, re, html, datetime, http.cookiejar, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 PrintecMarketIntel/1.0"

# Cookie-aware opener: some ATSs (e.g. FledgeHR) 302-redirect and set a culture
# cookie that the follow-up request must carry, else the redirect loops/errors.
_OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

# ---- HTTP helpers (stdlib only) -------------------------------------------
def _open(url, method="GET", body=None, headers=None, timeout=45):
    h = {"User-Agent": UA, "Accept-Language": "en,el,ro,sr,uk,hu,sk,bg;q=0.7"}
    if headers:
        h.update(headers)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h.setdefault("Content-Type", "application/json")
        h.setdefault("Accept", "application/json")
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with _OPENER.open(req, timeout=timeout) as r:
        return r.read()

def get_text(url, headers=None):
    return _open(url, headers=headers).decode("utf-8", "replace")

def get_json(url, headers=None):
    return json.loads(_open(url, headers=headers).decode("utf-8", "replace"))

def post_json(url, body, headers=None):
    return json.loads(_open(url, method="POST", body=body, headers=headers).decode("utf-8", "replace"))

def clean(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(s or "")))).strip()

def first(d, *keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", []):
            return v
    return None


# ---- per-board fetchers (each returns (total:int|None, roles:list[dict])) --
def fetch_bt(_t):
    d = get_json("https://cariere.bancatransilvania.ro/hrscapi/api/CareersSite/jobOpenings?currentPage=1&itemsPerPage=200")
    roles = []
    for j in (d.get("jobOpenings") or []):
        locs = ", ".join(clean(l.get("name")) for l in (j.get("locations") or []) if l.get("name"))
        roles.append({"title": clean(j.get("title")), "location": locs,
                      "dept": clean((j.get("domain") or {}).get("name")),
                      "seniority": ", ".join(j.get("seniorityLevels") or []),
                      "url": "https://cariere.bancatransilvania.ro/jobs/" + (j.get("postSlug") or "")})
    return d.get("totalItems"), roles

def fetch_robota(t):
    cid = t["id"]
    url = f"https://api.robota.ua/companies/{cid}/published-vacancies?page=0&count=60"
    d = get_json(url, headers={"Accept": "application/json"})
    arr = first(d, "filteredVacancies", "documents", "vacancies") or []
    roles = []
    for v in arr:
        vid = first(v, "id", "vacancyId", "notebookId")
        roles.append({"title": clean(first(v, "name", "title")),
                      "location": clean(first(v, "cityName", "city", "regionName") or ""),
                      "date": first(v, "publicationDate", "date", "lastModified"),
                      "url": f"https://robota.ua/company{cid}/vacancy{vid}" if vid else f"https://robota.ua/company{cid}"})
    return first(d, "totalVacanciesCount", "total", "count"), roles

def fetch_workable(t):
    slug = t["slug"]
    d = get_json(f"https://apply.workable.com/api/v1/widget/accounts/{slug}")
    roles = []
    for j in (d.get("jobs") or []):
        roles.append({"title": clean(j.get("title")),
                      "location": clean(first(j, "location", "city", "country") or ""),
                      "dept": clean(j.get("department") or ""),
                      "url": first(j, "url", "shortlink") or (f"https://apply.workable.com/{slug}/j/" + (j.get("shortcode") or ""))})
    return len(roles), roles

# generic server-rendered "career site" anchor scraper (SuccessFactors / Erste)
_CNT_PATTERNS = [
    r'[Rr]esults?[^<]*?of\s+([\d.,]+)',           # SF EN "Results 21-38 of 38"
    r'απ[όο]\s+([\d.,]+)',                          # SF GR "... από 38"
    r'a\(z\)\s+([\d.,]+)\s*[áa]ll',                 # OTP HU "a(z) 133 állásajánlat"
    r'([\d.,]+)\s*(?:rezultat|ponúk|ponuk|offers|nabídek|nabidek)',  # RS/SK/CZ
    r'jobs-number-in-heading[^>]*>\s*\(?\s*([\d]+)',  # dev.bg
]
def parse_count(htmltext):
    for pat in _CNT_PATTERNS:
        m = re.search(pat, htmltext)
        if m:
            try:
                return int(re.sub(r"[^\d]", "", m.group(1)))
            except ValueError:
                pass
    return None

def scrape_anchors(htmltext, base, href_substr, idre=r"/(\d{4,})/?(?:[?#].*)?$"):
    roles, seen = [], set()
    for m in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', htmltext, re.I | re.S):
        href, inner = m.group(1), m.group(2)
        if href_substr not in href:
            continue
        title = clean(inner)
        if not title or len(title) < 3 or len(title) > 200:
            continue
        idm = re.search(idre, href.split("?")[0])
        key = idm.group(1) if idm else title
        if key in seen:
            continue
        seen.add(key)
        url = href if href.startswith("http") else base.rstrip("/") + "/" + href.lstrip("/")
        roles.append({"title": title, "url": url, "id": idm.group(1) if idm else None})
    return roles

def fetch_sf(t):
    """Paginated server-rendered SAP SuccessFactors / Erste career-site HTML."""
    parsed, roles, seen = None, [], set()
    for url in t["urls"]:
        try:
            txt = get_text(url)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if not roles:
                raise
            break
        if parsed is None:
            parsed = parse_count(txt)
        for r in scrape_anchors(txt, t.get("base", url), t.get("href", "/job/")):
            k = r["id"] or r["title"]
            if k not in seen:
                seen.add(k)
                roles.append(r)
        if t.get("partial"):
            break
    # for a fully-paginated source the enumerated count IS the total (header counts like
    # "page 1 of 2" mis-parse); only fall back to the header count when we stop early.
    total = parsed if t.get("partial") else (len(roles) or parsed)
    return total, roles

def fetch_infostud(t):
    """RS - poslovi.infostud.com company page (HTML). Job links are /posao/<slug>
    (the anchor text is empty - the title lives in the slug). The page pads with
    unrelated employers, so keep only ad-blocks whose window matches the bank keyword."""
    url = f"https://poslovi.infostud.com/oglasi-za-posao-{t['slug']}"
    txt = get_text(url)
    kw = t.get("match", "").lower()
    roles, seen = [], set()
    anchors = list(re.finditer(r'<a\b[^>]*href="((?:https://poslovi\.infostud\.com)?/posao/([^"/?]+)[^"]*)"[^>]*>(.*?)</a>', txt, re.I | re.S))
    for i, m in enumerate(anchors):
        href, slug, inner = m.group(1), m.group(2), m.group(3)
        if slug in seen:
            continue
        window = txt[m.start(): (anchors[i + 1].start() if i + 1 < len(anchors) else m.start() + 1500)]
        if kw and kw not in window.lower() and kw not in slug.lower():
            continue
        seen.add(slug)
        title = clean(inner) or clean(slug.replace("-", " ")).title()
        dl = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', window)
        roles.append({"title": title,
                      "url": href if href.startswith("http") else "https://poslovi.infostud.com" + href,
                      "deadline": dl.group(1) if dl else None})
    return len(roles), roles

def fetch_fledge(t):
    """OTP SI - FledgeHR. The /jobs/{id} anchors are 'view' buttons (not titles), so we
    report the reliable id-derived COUNT + each job URL; titles live on the detail page."""
    base = f"https://{t['tenant']}.fledgehr.com"
    txt = get_text(base + "/jobs")
    ids = []
    for m in re.finditer(r'href="/jobs/(\d+)"', txt):
        if m.group(1) not in ids:
            ids.append(m.group(1))
    roles = [{"title": None, "id": i, "url": f"{base}/jobs/{i}"} for i in ids]
    return len(ids), roles

def fetch_profesia(t):
    url = f"https://www.profesia.sk/praca/?company_id={t['id']}"
    txt = get_text(url)
    total = parse_count(txt)
    roles = scrape_anchors(txt, "https://www.profesia.sk", "/job-offer/")
    if not roles:
        roles = scrape_anchors(txt, "https://www.profesia.sk", "/praca/", idre=r"/O(\d+)")
    return total, roles

def fetch_devbg(t):
    url = f"https://dev.bg/company/{t['slug']}/"
    txt = get_text(url)
    total = parse_count(txt)
    roles, seen = [], set()
    # each role is an <a> to /company/<slug>/job-ad/... or a job-list-item with data-job-id + a title
    for m in re.finditer(r'data-job-id="(\d+)".*?<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', txt, re.I | re.S):
        jid, href, inner = m.group(1), m.group(2), m.group(3)
        title = clean(inner)
        if jid in seen or not title or len(title) < 3:
            continue
        seen.add(jid)
        roles.append({"title": title, "id": jid,
                      "url": href if href.startswith("http") else "https://dev.bg" + href})
    if total is None:
        total = len(roles)
    return total, roles


FETCHERS = {"bt": fetch_bt, "robota": fetch_robota, "workable": fetch_workable, "sf": fetch_sf,
            "infostud": fetch_infostud, "fledge": fetch_fledge, "profesia": fetch_profesia, "devbg": fetch_devbg}

# ---- target registry (verified IDs/slugs, 24/06/2026 recon) ----------------
def _sf(base_search, n, step):
    return [f"{base_search}{'&' if '?' in base_search else '?'}startrow={i}" for i in range(0, n * step, step)]

TARGETS = [
    # UA - robota.ua public API (closes the Ukraine blind spot)
    {"bank": "PrivatBank", "country": "UA", "board": "robota.ua", "kind": "robota", "id": 203681},
    {"bank": "Oschadbank", "country": "UA", "board": "robota.ua", "kind": "robota", "id": 234100},
    {"bank": "PUMB / FUIB", "country": "UA", "board": "robota.ua", "kind": "robota", "id": 1020},
    {"bank": "monobank", "country": "UA", "board": "robota.ua", "kind": "robota", "id": 127046},
    {"bank": "Raiffeisen Bank Ukraine", "country": "UA", "board": "robota.ua", "kind": "robota", "id": 1037},
    {"bank": "OTP Bank Ukraine", "country": "UA", "board": "robota.ua", "kind": "robota", "id": 1042},
    # GR / UA - Workable widget
    {"bank": "Piraeus Bank", "country": "GR", "board": "Workable", "kind": "workable", "slug": "piraeus-bank"},
    {"bank": "Raiffeisen Bank Ukraine", "country": "UA", "board": "Workable", "kind": "workable", "slug": "raiffeisen-ukraine"},
    # RO - Banca Transilvania JSON
    {"bank": "Banca Transilvania", "country": "RO", "board": "hrscapi", "kind": "bt"},
    # GR / RO / HU - SuccessFactors & Erste server-rendered HTML
    {"bank": "Alpha Bank", "country": "GR", "board": "SuccessFactors", "kind": "sf",
     "urls": _sf("https://careers.alpha.gr/search/?q=&sortColumn=referencedate&sortDirection=desc", 5, 20),
     "base": "https://careers.alpha.gr"},
    {"bank": "BCR (Erste)", "country": "RO", "board": "Erste", "kind": "sf",
     "urls": _sf("https://erstegroup-careers.com/bcr/search/?q=", 4, 25), "base": "https://erstegroup-careers.com"},
    {"bank": "OTP Bank Hungary", "country": "HU", "board": "SuccessFactors", "kind": "sf",
     "urls": ["https://karrier.otpbank.hu/go/Minden-allasajanlat/1167001/"], "base": "https://karrier.otpbank.hu",
     "href": "/job/", "partial": True},
    # RS - poslovi.infostud.com
    {"bank": "Raiffeisen banka", "country": "RS", "board": "infostud", "kind": "infostud", "slug": "raiffeisen-banka", "match": "raiffeisen"},
    {"bank": "OTP banka Srbija", "country": "RS", "board": "infostud", "kind": "infostud", "slug": "otp-banka", "match": "otp"},
    {"bank": "NLB Komercijalna banka", "country": "RS", "board": "infostud", "kind": "infostud", "slug": "nlb-komercijalna-banka", "match": "nlb"},
    {"bank": "Banca Intesa Beograd", "country": "RS", "board": "infostud", "kind": "infostud", "slug": "banca-intesa", "match": "intesa"},
    {"bank": "AikBank", "country": "RS", "board": "infostud", "kind": "infostud", "slug": "aik-bank", "match": "aik"},
    # SI - FledgeHR
    {"bank": "OTP banka Slovenija", "country": "SI", "board": "FledgeHR", "kind": "fledge", "tenant": "otpbanka"},
    # BG - dev.bg (server-side COUNT only; titles are JS-rendered placeholders)
    {"bank": "DSK Bank", "country": "BG", "board": "dev.bg", "kind": "devbg", "slug": "dsk-bank",
     "note": "role titles are JS-rendered on dev.bg; 'total' is the reliable server-side count - open the page or dev.bg/company/dsk-bank for titles"},
]

# Documented browser-only sources (NOT scriptable - surface as Operator-requests, never a silent gap)
BROWSER_ONLY = [
    {"bank": "DSK Bank / UniCredit Bulbank", "board": "jobs.bg", "country": "BG",
     "reason": "DataDome + Cloudflare challenge returns HTTP 403 to every bare request; no JSON/RSS/sitemap. (DSK is covered via dev.bg instead.)",
     "url": "https://www.jobs.bg/en/company/unicreditbulbank/jobs"},
    {"bank": "NBG", "board": "SuccessFactors / nbg.gr", "country": "GR",
     "reason": "the nbg.gr careers list hydrates job rows via JavaScript (a bare GET returns only nav links + Outlook-safelink 'View job' wrappers); apply links go to career2.successfactors.eu company=national05.",
     "url": "https://www.nbg.gr/en/group/human-resources/career-opportunities/jobs-nbg"},
    {"bank": "Tatra / Slovenska sporitelna / VUB / CSOB SK", "board": "profesia.sk", "country": "SK",
     "reason": "profesia.sk now renders the offer list client-side (a bare GET returns only login/region-filter links, no enumerable offers). A JSON search endpoint may exist - future work.",
     "url": "https://www.profesia.sk/praca/?company_id=565"},
    {"bank": "Bank of Cyprus", "board": "SuccessFactors CSB", "country": "CY",
     "reason": "career55.sapsf.eu/career?company=bankofcypr is a JS Career-Site-Builder shell; no public JSON/RSS feed.",
     "url": "https://career55.sapsf.eu/career?company=bankofcypr"},
    {"bank": "NLB", "board": "Cornerstone (csod)", "country": "SI",
     "reason": "nlb.csod.com search needs a JWT bearer token extracted from the rendered page (POST /services/x/career-site).",
     "url": "https://nlb.csod.com"},
    {"bank": "Eurobank", "board": "SuccessFactors CSB", "country": "GR",
     "reason": "careers.eurobank.gr renders jobs via JavaScript (bare GET returns 0).",
     "url": "https://careers.eurobank.gr/go/All-Jobs/827502/"},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    ap.add_argument("--only", help="run only targets whose board/bank contains this substring (testing)")
    ap.add_argument("--debug", action="store_true", help="print first raw role per source")
    args = ap.parse_args()

    os.makedirs(args.data, exist_ok=True)
    out_path = os.path.join(args.data, "jobs_listings.json")

    targets = TARGETS
    if args.only:
        s = args.only.lower()
        targets = [t for t in TARGETS if s in t["board"].lower() or s in t["bank"].lower() or s in t["kind"].lower()]

    sources, ok, failed, total_roles = [], 0, 0, 0
    for t in targets:
        rec = {"bank": t["bank"], "country": t["country"], "board": t["board"], "kind": t["kind"]}
        # ONLY the network/parse call is guarded; prints happen after, so a console
        # encoding error (UnicodeEncodeError IS a ValueError) can never mark a source failed.
        try:
            total, roles = FETCHERS[t["kind"]](t)
            rec.update({"ok": True, "total": total, "fetched": len(roles), "roles": roles, "error": None})
            ok += 1
            total_roles += len(roles)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, KeyError, OSError) as e:
            rec.update({"ok": False, "total": None, "fetched": 0, "roles": [], "error": f"{type(e).__name__}: {e}"})
            failed += 1
        if t.get("note"):
            rec["note"] = t["note"]
        if t.get("partial"):
            rec["note"] = "first page only (rest loads via AJAX) - 'total' is the true count, 'roles' is a sample"
        sources.append(rec)
        if rec["ok"]:
            print(f"  ok  {t['bank']:28.28} [{t['board']:14.14}] total={rec['total']} fetched={rec['fetched']}")
            if args.debug and rec["roles"]:
                print("       e.g.", json.dumps(rec["roles"][0])[:170])  # ensure_ascii=True -> console-safe
        else:
            print(f"  FAIL {t['bank']:28.28} [{t['board']:14.14}] {str(rec['error'])[:80]}")

    if ok == 0 and os.path.exists(out_path) and not args.only:
        print("fetch_jobs: every source failed - keeping existing cache.")
        return

    payload = {
        "generated": args.week,
        "source": "fetch_jobs.py - Tier-0 job-board/ATS listing cache (PLUMBING: makes blocked listings reachable; agents still explore LinkedIn/leadership press/local boards freely)",
        "note": "Counts/roles are point-in-time snapshots from public postings (title/location/date/url only - NO applicant data per Printec policy). Cross-check titles against the bank's own page when citing. 'partial' sources report the true total but a sampled role list.",
        "scripted_sources_ok": ok,
        "scripted_sources_failed": failed,
        "total_roles_cached": total_roles,
        "browser_only": BROWSER_ONLY,
        "sources": sources,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\njobs_listings.json: {ok} source(s) ok, {failed} failed, {total_roles} roles cached -> {out_path}")
    print(f"  (+{len(BROWSER_ONLY)} browser-only sources documented as Operator-requests)")


if __name__ == "__main__":
    main()
