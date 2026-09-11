# Greece — Banking & Payments: Source-Access Audit Report

_Generated 2026-07-18_

## Scope

- **Input workbook:** `Greece - Banking & Payments Sources.xlsx` (moved to `/Users/mangian/Downloads/BANKING/`).
- **Sources processed:** 2027 unique source rows (1,928 in `All sources` + 99 in `Pending - needs access`). The A1–A6 tabs are the same rows split by workstream and were not double-counted.
- **Domains investigated:** 775 unique domains (access method is a property of the org/domain, so findings were clustered by domain and applied to every source row on that domain).
- Paused/inactive/pending sources were **processed, not skipped** (609 such rows).

## Headline results

- **Fully validated:** 1712 / 2027 (84.5%).
- Accessible & validated: 463 · Better resource found: 284 · Download tested: 440 · API tested: 499 · JS request tested: 26.
- Partially validated: 89 · Manual validation required: 216 · Unavailable: 6 · Irrelevant: 4.
- Domains exposing a **tested API**: 155. Domains needing a **browser/JS session**: counted in API sheet.

## Highest-volume domains (where collection effort concentrates)

| Domain | Sources | Access status | Recommended method |
|---|---|---|---|
| bankofgreece.gr | 102 | Download found and tested | Primary: GET the DCAT catalog https://www.bankofgreece.gr/OpenDataSetsCatalog/ca |
| hba.gr | 54 | Download found and tested | Scrape server-rendered HTML list pages (ASP.NET MVC, Microsoft-IIS) at https://w |
| aade.gr | 31 | Download found and tested | HTTP GET, no auth, no JS. (A4) Scrape https://www.aade.gr/en/open-data/KPIs for  |
| nbg.gr | 28 | Download found and tested | Scrape the IR sub-pages (financial-statements-annual-interim, /presentations, /r |
| hcmc.gr | 27 | Download found and tested | Scrape over plain HTTP GET (site is HTTP-only; port 443 refused, do NOT force HT |
| eba.europa.eu | 26 | API found and tested | For registers: hit the EUCLID JSON API directly with curl - GET https://euclid.e |
| gr.linkedin.com | 25 | API found and tested | For A5 jobs: GET the guest jobs API https://www.linkedin.com/jobs-guest/jobs/api |
| alpha.gr | 24 | Download found and tested | Scrape the IR sub-pages (Financial-Statements-Bank-and-Group, financial-results- |
| linkedin.com | 23 | Manual validation required | Authenticated browser session required. HEAD on company URLs returns HTTP 200 bu |
| athexgroup.gr | 22 | Better resource found | Scrape the server-rendered HTML announcement table at https://athens.euronext.co |
| athens.euronext.com | 22 | JavaScript request found and tested | Primary: scrape the server-rendered HTML listing at /en/market-data/announcement |
| diavgeia.gov.gr | 21 | API found and tested | GET JSON API https://diavgeia.gov.gr/luminapi/opendata/search.json — no auth, no |
| data.ecb.europa.eu | 18 | API found and tested | GET the SDMX REST API at https://data-api.ecb.europa.eu/service/data/{DATASET}/{ |
| bankingsupervision.europa.eu | 17 | API found and tested | For statistics (A4): GET SDMX API https://data-api.ecb.europa.eu/service/data/SU |
| dias.com.gr | 17 | Accessible and validated | Scrape server-rendered HTML statistics pages (https://www.dias.com.gr/en/statist |
| viva.com | 15 | Download found and tested | Scrape the server-rendered HTML of https://www.viva.com/en-gr/financial-statemen |
| apply.workable.com | 15 | API found and tested | POST JSON to https://apply.workable.com/api/v3/accounts/{account-slug}/jobs with |
| ec.europa.eu | 15 | API found and tested | A4 statistics: GET Eurostat dissemination API per dataset code, format=JSON (JSO |
| europeanpaymentscouncil.eu | 14 | Download found and tested | GET the per-scheme CSV register directly, e.g. https://www.europeanpaymentscounc |
| eurobank.gr | 14 | Download found and tested | Scrape the HTML index pages (financial-results, presentations, grafeio-tupou, es |
| ted.europa.eu | 14 | API found and tested | Primary: POST JSON to https://api.ted.europa.eu/v3/notices/search with query='bu |
| piraeusgroup.gr | 14 | Download found and tested | Scrape the server-rendered HTML pages (financial-results, annual-reports, oikono |
| ecb.europa.eu | 14 | API found and tested | For payments statistics (A4): GET the ECB SDMX API at https://data-api.ecb.europ |
| profilesw.com | 13 | Download found and tested | Two-part collection. (1) Financial-report PDFs: static assets under /wp-content/ |
| worldline.com | 13 | Better resource found | GET https://worldline.com/sitemap.xml with a real browser User-Agent header (e.g |

## APIs & dynamic sources found

207 domains exposed an API; full endpoint/method/params in the `API_and_Dynamic_Sources` sheet. Notable examples:

- **2027.anaptyxi.gov.gr** — `https://anaptyxi.gov.gr/GetData.ashx` (GET, JSON (also CSV/HTML for list queries)), tested: Yes. GET JSON API https://anaptyxi.gov.gr/GetData.ashx?queryType=projects_v2&outputFo
- **2522.syzefxis.gov.gr** — `https://diavgeia.gov.gr/api/search` (GET, JSON), tested: No. Old 2522.syzefxis portal is dead — do not use. Scrape the region's Tender Index 
- **2dype.gov.gr** — `https://www.2dype.gov.gr/wp-json/wp/v2/posts` (GET, JSON), tested: Yes. Poll RSS https://www.2dype.gov.gr/category/nea/diagonismoi-promitheies/feed/ (HT
- **5518.syzefxis.gov.gr** — `https://diavgeia.gov.gr/opendata/search.json (Diavgeia OpenData) — AEPP acts also at https://diavgeia.gov.gr/f/aepp` (GET, JSON), tested: Yes. For back-catalogue scrape HTML tables of the legacy Joomla portal (www.5518.syze
- **aade.gr** — `https://mydata.aade.gov.gr/ (myDATA REST API; docs: https://www.aade.gr/sites/default/files/2023-02/myDATA%20API%20Documentation_v1.0.6_eng.pdf)` (POST/GET, XML), tested: No. HTTP GET, no auth, no JS. (A4) Scrape https://www.aade.gr/en/open-data/KPIs for 
- **acci.gr** — `https://acci.gr/category/anakoinwseis-gemh-ae/feed/ (RSS); https://acci.gr/wp-json/wp/v2/posts (REST)` (GET, RSS/XML; WP REST JSON), tested: Yes. GET category RSS https://acci.gr/category/anakoinwseis-gemh-ae/feed/ for GEMI an
- **aftodioikisi.gr** — `https://www.aftodioikisi.gr/feed/ and https://www.aftodioikisi.gr/category/<slug>/feed/` (GET, RSS/XML), tested: Yes. Poll category RSS feeds: GET https://www.aftodioikisi.gr/category/proslipseis/fe
- **aml-authority.gov.gr** — `https://www.aml-authority.gov.gr/en/feed/` (GET, RSS/XML), tested: Yes. GET RSS /en/feed/ (tested valid) for announcements/A3; scrape /en/annual-reports
- **api.ted.europa.eu** — `https://api.ted.europa.eu/v3/notices/search` (POST, JSON), tested: Yes. POST JSON to https://api.ted.europa.eu/v3/notices/search, no auth, Content-Type:
- **app.diavgeia.gov.gr** — `https://diavgeia.gov.gr/opendata/search.json` (GET, JSON), tested: Yes. GET JSON from https://diavgeia.gov.gr/opendata/search.json?org=<orgUID>&size=100
- **apply.workable.com** — `https://apply.workable.com/api/v3/accounts/{account-slug}/jobs` (POST, JSON), tested: Yes. POST JSON to https://apply.workable.com/api/v3/accounts/{account-slug}/jobs with
- **apps.apple.com** — `https://itunes.apple.com/lookup?id=<appId>&country=gr  AND  https://itunes.apple.com/gr/rss/customerreviews/id=<appId>/sortBy=mostRecent/page=<n>/json` (GET, JSON), tested: Yes. GET JSON: use lookup API for aggregate rating/version/metadata; use customerrevi
- **apps.ekapy.gov.gr** — `https://apps.ekapy.gov.gr/api/v1/ (base; e.g. v1/Procurements, v1/ExportExcelProcurements)` (GET/POST, JSON (Excel export for ExportExcelProcurements)), tested: Yes. Browser session needed: open /procurementsEkapy/overview and capture the exact X
- **apps.interconsult.gr** — `https://cerpp.eprocurement.gov.gr/khmdhs-opendata (POST /notice for προκηρύξεις/διακηρύξεις; POST /auction for αναθέσεις; plus contracts; GET document PDF by ADAM referenceNumber)` (POST (search) + GET (PDF by ΑΔΑΜ), JSON (documents as PDF via GET)), tested: Yes. Use the official KIMDIS OpenData API directly (not the interconsult UI): POST JS
- **athens.euronext.com** — `https://athens.euronext.com/en/views/ajax` (POST, JSON (Drupal AJAX command array: 'settings' + 'insert' commands whose 'data' field contains the HTML fragment of announcement rows with node/<id> links)), tested: Yes. Primary: scrape the server-rendered HTML listing at /en/market-data/announcement

## Main failure reasons

- unspecified — 47
- Auth wall / login required (company pages GET body = Sign in — 23
- HTTP 403 Cloudflare bot management (Attention Required chall — 12
- 403 Forbidden (Akamai bot protection) on www.mastercard.com  — 8
- HTTP 403 (anti-bot block) on all listing and /cmp company pa — 7
- HTTP 403 (Cloudflare bot block) on homepage and all Job/Jobs — 6
- HTTP 403 (Cloudflare bot management; server=cloudflare, ki-e — 5
- JS-only SPA + reCAPTCHA v3 on the search app (publicity.busi — 4
- Tender detail content behind free-registration/login wall — 4
- HTTP 403 Forbidden (WAF/bot protection) — 3
- JS-rendered table; exact admin-ajax action/params not reprod — 3
- HTTP 403 Forbidden (Cloudflare bot protection) on curl and W — 3

## Sources requiring manual validation

305 sources are flagged for manual validation (login/paywall/CAPTCHA/JS-portal or ambiguous). See the `Unavailable_Resources` sheet for per-source instructions. This matches the prior note (F6) that JS-only Greek portals (ΕΣΗΔΗΣ/ΚΗΜΔΗΣ/Diavgeia) need a browser session.

## Recommended approach for later data collection

1. **Prefer tested APIs/downloads first** — see `API_and_Dynamic_Sources`; these reproduce outside a browser and are cheapest to automate.
2. **HTML/statistics portals** — scrape the specific data/reports page identified in `Best resource URL`, not the generic homepage.
3. **Browser-session sources** (Greek e-procurement, some dashboards) — route through an interactive browser step; batch them.
4. **Manual-validation queue** — work the `Unavailable_Resources` sheet before the next collection run.
5. Cluster collection by domain to reuse one access method across all its source rows.

## Independent verification (post-audit spot-check)

To test whether the fleet's "tested" flags were trustworthy, a reproducible random sample (seed=42) of **30 rows** claiming *API tested* or *download tested* was **re-hit directly** (curl, browser UA, follow redirects, real POST bodies), independent of the agents.

- **Result: 30 / 30 PASS** — every endpoint was live and returned the **content-type matching its claim** (JSON APIs → JSON, PDF downloads → application/pdf, XLSX → openxml spreadsheet, RSS → rss+xml; POST APIs TED/Workable reachable & parsing).
- This validates **reachability and format**, not content relevance. A few live rows are generic WordPress `wp-json/posts` feeds — valid JSON, relevance judged separately at collection time.
- Only rows with a concrete GET/POST-able URL were in the sampling frame (~200 of ~939 tested rows); templated endpoints (`{DATASET}`, `{slug}`) weren't spot-checked.
- Full evidence: `Verification_Sample` sheet in the audit workbook.
