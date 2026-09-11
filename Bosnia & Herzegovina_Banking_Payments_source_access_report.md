# Bosnia & Herzegovina — Banking & Payments: Source-Access Audit Report

_Generated 2026-07-22_

## Scope

- **Input workbook:** `Bosnia & Herzegovina - Banking & Payments Sources.xlsx` (in `/Users/mangian/Downloads/BANKING/`, unmodified).
- **Sources processed:** 1249 unique rows (`All sources` + `Pending`). A1–A6 tabs are the same rows split by workstream (not double-counted).
- **Domains:** 523 unique; 150 source rows reuse domain findings already tested for Greece (shared orgs: ECB, EBA, TED, Eurostat, LinkedIn, Workable…).
- Paused/inactive/pending sources **processed, not skipped** (554 rows).

## Headline results

- **Fully validated:** 1007/1249 (80.6%).
- Accessible: 443 · Better resource: 177 · Download tested: 251 · API tested: 124 · JS tested: 12.
- Partially validated: 90 · Manual validation: 145 · Unavailable: 6 · Irrelevant: 1.

## Highest-volume domains

| Domain | Sources | Access status | Recommended method |
|---|---|---|---|
| cbbh.ba | 74 | Accessible and validated | HTTP GET with a browser User-Agent. IMPORTANT: use GET, never HEAD (HEAD request |
| abrs.ba | 52 | Download found and tested | For market statistics (A4): scrape https://abrs.ba/en/banks-3/ and the MCO quart |
| fba.ba | 28 | Download found and tested | Static HTTP crawl with curl/requests (server-rendered HTML, no JS or auth needed |
| linkedin.com | 20 | Manual validation required | Authenticated browser session required. HEAD on company URLs returns HTTP 200 bu |
| ba.linkedin.com | 17 | Manual validation required | For firmographics: fetch individual company /company/<slug> 'About' pages, which |
| komvp.gov.ba | 14 | Better resource found | Scrape with a plain HTTP GET client (curl/requests) sending a real browser User- |
| apif.net | 14 | Partially validated | HTTP GET the Joomla pages with a real browser User-Agent header (mandatory: defa |
| mft.gov.ba | 13 | Download found and tested | Server-rendered HTML — collect with plain HTTP GET, but a browser User-Agent hea |
| ubbih.ba | 13 | Accessible and validated | Static HTML scraping. Crawl section landing pages (news /bs/novosti/kratke-vijes |
| bbi.ba | 12 | Download found and tested | Scrape the financial-reports HTML page (bs: https://bbi.ba/o-nama/finansijski-iz |
| sluzbenilist.ba | 11 | JavaScript request found and tested | Server-rendered scrape, no browser required. For each nivoIzdavanja_FK (1,2,5,7) |
| unicredit.ba | 11 | Download found and tested | HTTP GET with a real browser User-Agent header (default UAs are 403'd by Akamai  |
| mastercard.com | 11 | Partially validated | For corporate/financial disclosures: GET investor.mastercard.com RSS feed (200,  |
| akta.ba | 10 | Better resource found | Scrape server-rendered HTML section pages (no JS needed): /tenderi and /Tenderi/ |
| bamcard.ba | 10 | API found and tested | Poll WordPress REST API GET https://bamcard.ba/wp-json/wp/v2/posts?per_page=100& |
| blberza.com | 10 | Better resource found | Poll the NewsRss.aspx RSS feeds (Channel=korp for issuer disclosures, fin for fi |
| raiffeisenbank.ba | 10 | Download found and tested | Static HTTP scrape via curl/requests. Site runs Adobe Experience Manager: report |
| sase.ba | 10 | Accessible and validated | Primary: GET the issuer list at /v1/Tr%C5%BEi%C5%A1te/Emitenti/Spisak-emitenata  |
| ebrd.com | 10 | Better resource found | Use updated notices page with Location=Greece filter (public); it is JS/filter-d |
| intesasanpaolobanka.ba | 10 | Download found and tested | Fetch pages server-side (WebFetch / headless browser with a real browser User-Ag |

## Main failure reasons

- unspecified — 41
- Auth wall / login required (company pages GET body = Sign in — 20
- curl default User-Agent blocked with HTTP 403 (bot filter);  — 14
- 403 Forbidden (Akamai bot protection) on www.mastercard.com  — 11
- 403 Forbidden on all imf.org and elibrary.imf.org HTML/PDF p — 7
- HTTP 403 (Cloudflare bot protection / JS challenge) on all U — 6
- HTTP 403 (Cloudflare bot protection) on curl -sSIL and on We — 6
- HTTP 403 Cloudflare challenge (cf-chl / challenge-platform i — 5
- paywall (membership-gated content); SPA renders empty to non — 5
- HTTP 403 Forbidden (AkamaiGHost bot mitigation) — 4

## Recommended approach for later collection

1. Prefer tested APIs/downloads (see `API_and_Dynamic_Sources`).
2. Scrape the specific data/reports page in `Best resource URL`, not the homepage.
3. Route browser-session sources (national e-procurement, dashboards) through an interactive step.
4. Work the `Unavailable_Resources` queue before collection.
5. Cluster by domain to reuse one access method across all its rows.

## Independent verification (post-audit spot-check)

A random sample of **20** rows claiming *API tested* or *download tested* was re-hit directly (curl, browser UA, redirects), independent of the investigating agents.

- **15/20 verified live + correct content-type.**
- Non-passes: 1× Possible dead link — recheck; 1× Live but bot-blocked to curl (browser session needed); 2× Inconclusive (truncated/templated URL in my test); 1× Check.
- Most non-passes are anti-bot 403s (endpoint real, needs a browser), endpoints needing params/auth, or URLs my own test truncated at a template placeholder; genuine dead-link over-claims are flagged 'recheck' in the sheet.
- This verifies **reachability and format, not content relevance**. Full evidence: `Verification_Sample` sheet in the workbook.
