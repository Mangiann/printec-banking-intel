# Bulgaria — Banking & Payments: Source-Access Audit Report

_Generated 2026-07-22_

## Scope

- **Input workbook:** `Bulgaria - Banking & Payments Sources.xlsx` (in `/Users/mangian/Downloads/BANKING/`, unmodified).
- **Sources processed:** 1300 unique rows (`All sources` + `Pending`). A1–A6 tabs are the same rows split by workstream (not double-counted).
- **Domains:** 508 unique; 261 source rows reuse domain findings already tested for Greece (shared orgs: ECB, EBA, TED, Eurostat, LinkedIn, Workable…).
- Paused/inactive/pending sources **processed, not skipped** (668 rows).

## Headline results

- **Fully validated:** 1045/1300 (80.4%).
- Accessible: 321 · Better resource: 211 · Download tested: 267 · API tested: 245 · JS tested: 1.
- Partially validated: 78 · Manual validation: 173 · Unavailable: 2 · Irrelevant: 2.

## Highest-volume domains

| Domain | Sources | Access status | Recommended method |
|---|---|---|---|
| bnb.bg | 103 | Download found and tested | Server-rendered classic site (.htm pages) with stable URL scheme; no JS or auth  |
| bg.linkedin.com | 39 | API found and tested | For A5 (jobs/early-intent): poll the jobs-guest seeMoreJobPostings/search endpoi |
| borica.bg | 31 | Download found and tested | Direct HTTP GET (curl/requests, no JS, no auth). Scrape the Documents & Resource |
| fsc.bg | 22 | API found and tested | Primary: poll WordPress REST API https://www.fsc.bg/wp-json/wp/v2/posts?per_page |
| dev.bg | 20 | Accessible and validated | HTTP scrape of server-rendered HTML: crawl the fintech filter page /company/sele |
| jobs.bg | 18 | Manual validation required | Collect via a real/headless browser session that solves the Cloudflare managed c |
| minfin.bg | 18 | Manual validation required | Site is fully public to human browsers but sits behind a Cloudflare 'managed cha |
| capital.bg | 16 | API found and tested | Poll the RSS feeds on a schedule with a browser-like User-Agent: main /rss/ for  |
| ec.europa.eu | 16 | API found and tested | A4 statistics: GET Eurostat dissemination API per dataset code, format=JSON (JSO |
| abanksb.bg | 14 | Download found and tested | Static HTML site (WordPress). Scrape hub pages (/en/banking-system/, /en/bulleti |
| data.ecb.europa.eu | 14 | API found and tested | GET the SDMX REST API at https://data-api.ecb.europa.eu/service/data/{DATASET}/{ |
| linkedin.com | 13 | Manual validation required | Authenticated browser session required. HEAD on company URLs returns HTTP 200 bu |
| investor.bg | 12 | Better resource found | Poll the category RSS feeds (Banks & Insurance c/539 and Finance c/536 as primar |
| strategy.bg | 12 | Better resource found | Scrape the server-rendered list at https://www.strategy.bg/bg/public-consultatio |
| bankingsupervision.europa.eu | 12 | API found and tested | For statistics (A4): GET SDMX API https://data-api.ecb.europa.eu/service/data/SU |
| dskbank.bg | 11 | Download found and tested | Static HTTP GET. Scrape the /документи (EN: /en/individual-clients/about-us/docu |
| bbr.bg | 11 | Download found and tested | Crawl the annual-reports landing page (EN: /en/public-information-bbr/annual-rep |
| eba.europa.eu | 11 | API found and tested | For registers: hit the EUCLID JSON API directly with curl - GET https://euclid.e |
| eur-lex.europa.eu | 11 | API found and tested | Use SPARQL at https://publications.europa.eu/webapi/rdf/sparql (Accept: applicat |
| fibank.bg | 10 | Download found and tested | Scrape the IR sub-pages (financial-information, general-meetings-of-shareholders |

## Main failure reasons

- unspecified — 34
- HTTP 403, cf-mitigated: challenge (Cloudflare managed/Turnst — 18
- HTTP 403 Cloudflare managed challenge ('Just a moment...' /  — 18
- Auth wall / login required (company pages GET body = Sign in — 13
- download.bse-sofia.bg rules PDF returned HTTP 403 to plain c — 9
- 403 Forbidden (Akamai bot protection) on www.mastercard.com  — 6
- HTTP 403 Forbidden (anti-bot protection) on homepage and all — 6
- JS-only SPA; API auth-gated (400 missing token / 405) and CO — 6
- HTTP 403 Cloudflare bot management (Attention Required chall — 4
- HTTP 403 Cloudflare bot challenge (blocked for curl and WebF — 4

## Recommended approach for later collection

1. Prefer tested APIs/downloads (see `API_and_Dynamic_Sources`).
2. Scrape the specific data/reports page in `Best resource URL`, not the homepage.
3. Route browser-session sources (national e-procurement, dashboards) through an interactive step.
4. Work the `Unavailable_Resources` queue before collection.
5. Cluster by domain to reuse one access method across all its rows.

## Independent verification (post-audit spot-check)

A random sample of **20** rows claiming *API tested* or *download tested* was re-hit directly (curl, browser UA, redirects), independent of the investigating agents.

- **18/20 verified live + correct content-type.**
- Non-passes: 1× Live but bot-blocked to curl (browser session needed); 1× Inconclusive (network timeout my side).
- Most non-passes are anti-bot 403s (endpoint real, needs a browser), endpoints needing params/auth, or URLs my own test truncated at a template placeholder; genuine dead-link over-claims are flagged 'recheck' in the sheet.
- This verifies **reachability and format, not content relevance**. Full evidence: `Verification_Sample` sheet in the workbook.
