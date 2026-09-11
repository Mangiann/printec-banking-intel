# Croatia — Banking & Payments: Source-Access Audit Report

_Generated 2026-07-22_

## Scope

- **Input workbook:** `Croatia - Banking & Payments Sources.xlsx` (in `/Users/mangian/Downloads/BANKING/`, unmodified).
- **Sources processed:** 1281 unique rows (`All sources` + `Pending`). A1–A6 tabs are the same rows split by workstream (not double-counted).
- **Domains:** 505 unique; 219 source rows reuse domain findings already tested for Greece (shared orgs: ECB, EBA, TED, Eurostat, LinkedIn, Workable…).
- Paused/inactive/pending sources **processed, not skipped** (341 rows).

## Headline results

- **Fully validated:** 1087/1281 (84.9%).
- Accessible: 331 · Better resource: 165 · Download tested: 351 · API tested: 238 · JS tested: 2.
- Partially validated: 86 · Manual validation: 104 · Unavailable: 0 · Irrelevant: 4.

## Highest-volume domains

| Domain | Sources | Access status | Recommended method |
|---|---|---|---|
| hnb.hr | 108 | Download found and tested | Server-side HTTP scraping: fetch each landing page (curl returns full static HTM |
| hanfa.hr | 41 | Download found and tested | Scrape the server-rendered index pages (/statistika/mjesecna-izvjesca/, /publika |
| fina.hr | 31 | Partially validated | For public workstreams (A2/A3/A4/A5/A6): plain HTTP GET / WebFetch on www.fina.h |
| hub.hr | 24 | Download found and tested | Plain HTTP GET (curl/requests, no JS, no auth). Poll the RSS feed(s) at /hr/taxo |
| hr.linkedin.com | 23 | API found and tested | For jobs (A5): poll the public jobs-guest seeMoreJobPostings/search endpoint wit |
| zaba.hr | 21 | Download found and tested | Scrape the static HTML sections (investitori/financijski-izvjestaji, investitori |
| eho.zse.hr | 17 | API found and tested | Poll the JSON feeds directly with a plain HTTP GET (curl/requests), no browser o |
| bankingsupervision.europa.eu | 16 | API found and tested | For statistics (A4): GET SDMX API https://data-api.ecb.europa.eu/service/data/SU |
| hpb.hr | 15 | Download found and tested | Scrape the /322 financial-reports page (and its 'Arhiva' archive section) for an |
| data.gov.hr | 15 | API found and tested | Harvest via CKAN Action API: page through package_search (rows=1000,start=...) t |
| pbz.hr | 14 | Download found and tested | Fetch HTML index pages (financial-reports.html and per-year pages e.g. /en/gradj |
| erstebank.hr | 14 | Download found and tested | Scrape the financial-reports-and-announcements page (both /en and /hr) for stati |
| hgk.hr | 14 | Download found and tested | Server-rendered CMS: fetch the HTML hub pages (analize-i-publikacije, odabrani-m |
| otpbanka.hr | 13 | Download found and tested | Static HTTP GET. Crawl HTML section pages (godisnja-izvjesca, priopcenja, javni- |
| rba.hr | 13 | Download found and tested | Scrape the financial-indicators.html and investors.html pages (both EN and HR, e |
| podaci.dzs.hr | 13 | API found and tested | For structured time series, use the PxWeb JSON API at web.dzs.hr/PxWeb/api/v1/{e |
| data.ecb.europa.eu | 12 | API found and tested | GET the SDMX REST API at https://data-api.ecb.europa.eu/service/data/{DATASET}/{ |
| mfin.gov.hr | 12 | Download found and tested | Scrape the section index pages (server-rendered HTML, no JS) and harvest anchor  |
| aircash.eu | 11 | Accessible and validated | HTTP GET on server-rendered pages: /press (EN newsroom) and /hr-HR/novosti (Croa |
| eba.europa.eu | 11 | API found and tested | For registers: hit the EUCLID JSON API directly with curl - GET https://euclid.e |

## Main failure reasons

- unspecified — 53
- Auth wall / login required (company pages GET body = Sign in — 10
- 403 Forbidden (Akamai bot protection) on www.mastercard.com  — 9
- DNS ENOTFOUND for corp.pbz.hr from this environment (curl an — 5
- WebFetch homepage returned HTTP 403 (bot protection); severa — 5
- JS-only rendering for live figures; guessed export endpoint  — 4
- HTTP 500 on /procurements-public (server error 'Object refer — 3
- HTTP 403 (Cloudflare bot protection) on all requests to onli — 3
- JS-only (Blazor/FluentUI SPA); /ECon/Dashboard 301-redirects — 2
- HTTP 403 (AkamaiGHost bot protection) on all pages via curl  — 2

## Recommended approach for later collection

1. Prefer tested APIs/downloads (see `API_and_Dynamic_Sources`).
2. Scrape the specific data/reports page in `Best resource URL`, not the homepage.
3. Route browser-session sources (national e-procurement, dashboards) through an interactive step.
4. Work the `Unavailable_Resources` queue before collection.
5. Cluster by domain to reuse one access method across all its rows.

## Independent verification (post-audit spot-check)

A random sample of **20** rows claiming *API tested* or *download tested* was re-hit directly (curl, browser UA, redirects), independent of the investigating agents.

- **15/20 verified live + correct content-type.**
- Non-passes: 1× Inconclusive (truncated/templated URL in my test); 3× Endpoint live; needs params/auth; 1× Live but bot-blocked to curl (browser session needed).
- Most non-passes are anti-bot 403s (endpoint real, needs a browser), endpoints needing params/auth, or URLs my own test truncated at a template placeholder; genuine dead-link over-claims are flagged 'recheck' in the sheet.
- This verifies **reachability and format, not content relevance**. Full evidence: `Verification_Sample` sheet in the workbook.
