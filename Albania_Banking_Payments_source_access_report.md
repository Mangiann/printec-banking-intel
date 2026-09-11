# Albania — Banking & Payments: Source-Access Audit Report

_Generated 2026-07-22_

## Scope

- **Input workbook:** `Albania - Banking & Payments Sources.xlsx` (in `/Users/mangian/Downloads/BANKING/`, unmodified).
- **Sources processed:** 1220 unique rows (`All sources` + `Pending`). A1–A6 tabs are the same rows split by workstream (not double-counted).
- **Domains:** 471 unique; 180 source rows reuse domain findings already tested for Greece (shared orgs: ECB, EBA, TED, Eurostat, LinkedIn, Workable…).
- Paused/inactive/pending sources **processed, not skipped** (565 rows).

## Headline results

- **Fully validated:** 941/1220 (77.1%).
- Accessible: 443 · Better resource: 116 · Download tested: 216 · API tested: 163 · JS tested: 3.
- Partially validated: 83 · Manual validation: 189 · Unavailable: 4 · Irrelevant: 3.

## Highest-volume domains

| Domain | Sources | Access status | Recommended method |
|---|---|---|---|
| bankofalbania.org | 102 | Accessible and validated | Direct HTTP GET scraping with a normal browser User-Agent header (the site 403s  |
| aab.al | 29 | Download found and tested | Static WordPress site. Scrape https://aab.al/en/data/ HTML and regex-extract hre |
| financa.gov.al | 27 | Manual validation required | Site sits behind Imperva/Incapsula bot protection: plain curl, WebFetch and the  |
| al.linkedin.com | 26 | API found and tested | For A5 (hiring/early-intent): poll the guest jobs endpoint per keyword (banking/ |
| amf.gov.al | 22 | Partially validated | Site is behind a Cloudflare managed challenge (cf-mitigated: challenge) that blo |
| bkt.com.al | 21 | Download found and tested | Scrape the four investor-relations index pages (annual-reports, audited-reports, |
| linkedin.com | 19 | Manual validation required | Authenticated browser session required. HEAD on company URLs returns HTTP 200 bu |
| caa.gov.al | 18 | API found and tested | Hybrid: (a) Poll https://caa.gov.al/wp-json/wp/v2/posts?per_page=100&page=N (and |
| raiffeisen.al | 17 | API found and tested | For A1 media/A2 tenders: poll the newslist JSON servlet page-by-page (pagenumber |
| facebook.com | 17 | Manual validation required | Not reproducible outside an authenticated session. Use Facebook Graph API with a |
| instat.gov.al | 16 | Better resource found | Two-tier: (1) For structured time-series data use the PX-Web databank on port 80 |
| asd.gov.al | 15 | Download found and tested | Scrape the Open Data page (https://asd.gov.al/en/home/news/open-data/) and the A |
| openprocurement.al | 15 | Accessible and validated | Two options. (1) HTML scrape of openprocurement.al directly: pages are fully ser |
| monitor.al | 14 | Accessible and validated | Poll the RSS feeds on a schedule: main feed https://monitor.al/feed/ and topic f |
| bankacredins.com | 13 | Download found and tested | Site was rebuilt on Webflow (assets on cdn.prod.website-files.com). For A1/A3 di |
| qkb.gov.al | 12 | API found and tested | For company-level A1/A6 data: automate an HTTP POST to https://format.qkb.gov.al |
| idp.al | 11 | Accessible and validated | Scrape the static HTML index pages (vendime-2, udhezime-mbrojtja, en/data-protec |
| app.gov.al | 11 | Accessible and validated | Scrape the paginated public notice listings (njoftimi-i-fituesit, njoftimi-i-kon |
| intesasanpaolobank.al | 11 | Download found and tested | Use a headless-browser / browser-like fetcher (WebFetch worked; plain curl is bl |
| otpbank.al | 11 | Accessible and validated | Static HTML scraping of the media sub-pages (news, tenders, publications, career |

## Main failure reasons

- Blocked: Imperva/Incapsula JS bot challenge (HTTP 200 but bo — 27
- HTTP 403 Cloudflare managed challenge (cf-mitigated: challen — 22
- unspecified — 21
- Auth wall / login required (company pages GET body = Sign in — 19
- JS-only, login-walled; anonymous access blocked — 17
- HTTP 403 (Cloudflare cf-mitigated: challenge) on all URLs in — 8
- paywall (subscription required for full data/exports) — 6
- 403 Forbidden (Akamai bot protection) on www.mastercard.com  — 5
- blocked (Incapsula/Imperva bot-protection JS challenge; HTTP — 5
- HTTP 403 Cloudflare bot management (Attention Required chall — 4

## Recommended approach for later collection

1. Prefer tested APIs/downloads (see `API_and_Dynamic_Sources`).
2. Scrape the specific data/reports page in `Best resource URL`, not the homepage.
3. Route browser-session sources (national e-procurement, dashboards) through an interactive step.
4. Work the `Unavailable_Resources` queue before collection.
5. Cluster by domain to reuse one access method across all its rows.

## Independent verification (post-audit spot-check)

A random sample of **20** rows claiming *API tested* or *download tested* was re-hit directly (curl, browser UA, redirects), independent of the investigating agents.

- **18/20 verified live + correct content-type.**
- Non-passes: 1× Live but bot-blocked to curl (browser session needed); 1× Possible dead link — recheck.
- Most non-passes are anti-bot 403s (endpoint real, needs a browser), endpoints needing params/auth, or URLs my own test truncated at a template placeholder; genuine dead-link over-claims are flagged 'recheck' in the sheet.
- This verifies **reachability and format, not content relevance**. Full evidence: `Verification_Sample` sheet in the workbook.
