# Raiffeisen Bank Romania - bank disclosures, run 2026-08-27

Fresh full run. 11 verified signals. Focus: ATM/POS fleet, cloud, voice guidance, Garanti BBVA integration, H1-2026.

## Headlines

- **Fleet reconciled two ways.** Disclosed 264 branches / 1,150 ATM+MFM / ~45,000 POS at 30/06/2026. The bank's own locator JSON returns 1,151 owned machines: **603 deposit-capable MFM + 548 withdrawal-only** - i.e. **48% of the fleet cannot take cash**. Plus 60 corporate 'Smart Cashbox' units and 595 Euronet partner ATMs.
- **Garanti integration now has dates.** Closing Q4/2026, **data migration and rebranding through 2027**, legal merger Q4/2027, one-off integration cost c. EUR 70m mainly 2027.
- **Voice guidance is a statutory retrofit**, not a marketing feature: EAA / Law 232/2022, fleet-wide, and the bank's own page still shows the end-2025 target in future tense.
- **No Romania-specific cloud disclosure exists** in any 2026 primary source - reported as a gap, not padded with group-level AWS/Azure material.

## Signals

### 1. Raiffeisen Bank Romania (Romania) - XL / win Medium / Medium
**Signal.** H1-2026 results release (31/07/2026): network of 264 branches, 1,150 ATMs and multifunctional machines (MFM) and nearly 45,000 POS terminals at merchants; ~2.4m customers, net profit RON 849m, total assets RON 91.8bn (+10% y/y), opex +5%.
**Implies.** Concrete addressable installed base for ATM/self-service supply, cash automation and POS/acquiring managed services; growing opex base argues for outsourced ATM/POS estate management.
**Source.** Raiffeisen Bank Romania press release, S1 2026 results, 31/07/2026 - https://www.raiffeisen.ro/ro/despre-noi/comunicate-de-presa/2026/raiffeisen-bank-romania-rezultate-s1-2026-clienti-noi-retail-si-imm.html (primary)
**Follow-up.** Ask IR for the ATM-vs-MFM split and the current ATM hardware vendor/service contract expiry.

### 2. Raiffeisen Bank Romania (Romania) - XL / win Medium / Medium
**Signal.** Machine-readable branch/ATM locator feed (map.maps.viewport.json, pulled 27/08/2026) returns 2,069 places: 263 BRANCH and 1,806 ATM records. Excluding 595 Euronet-branded partner machines, the bank's own estate is 1,151 machines = 603 'Bancomat multifunctional EUR' (deposit-capable, RON+EUR, 06:00-23:30) + 548 withdrawal-only 'Bancomat', plus 60 'Smart Cashbox' corporate deposit units (EUR/USD/RON/GBP). 1,151 reconciles exactly with the disclosed '1,150 ATM and MFM'. Only 534 machines actually list the cash-deposit service.
**Implies.** ~548 machines (48% of the owned fleet) are cash-out-only with no deposit function - a quantified recycler/deposit-automation white space. Direct fit for Printec cash automation/recyclers and ATM/self-service upgrade or replacement.
**Source.** Raiffeisen Bank Romania branch/ATM locator JSON feed, 27/08/2026 - https://www.raiffeisen.ro/ro/home/retea/_jcr_content/root/container/map.maps.viewport.json (primary)
**Follow-up.** Re-pull this feed monthly; a change in the 603/548 split is itself the buying signal. Establish which of the 548 sit at branches (in-branch recycler candidates).

### 3. Raiffeisen Bank Romania / Euronet (Romania) - L / win Low / Medium
**Signal.** The bank's own locator carries 595 Euronet-branded ATMs as part of the customer-facing network: 414 offering withdrawal only and 181 'Bancomat multifunctional' also accepting RON deposits to own accounts. Raiffeisen Romania has outsourced ATM and POS management to Euronet since a 2003 outsourcing agreement (Euronet then managed 600 ATMs and 2,700 EFTPOS).
**Implies.** Euronet is the entrenched incumbent for ATM/POS managed services here - a competitive barrier for Printec managed services, but also a displacement target and a route in via hardware/recycler supply and accessibility retrofit rather than full estate outsourcing. [STANDING] the 600/2,700 figures are 2003-vintage and must not be used as current.
**Source.** Raiffeisen Bank Romania locator JSON feed; Euronet Worldwide investor release (historic context), 27/08/2026 - https://ir.euronetworldwide.com/news-releases/news-release-details/raiffeisen-bank-romania-signs-atm-and-pos-outsourcing-agreement (primary)
**Follow-up.** Establish the current Euronet contract scope and renewal date; identify which machines are bank-owned vs Euronet-owned.

### 4. Raiffeisen Bank Romania / Garanti BBVA Romania (Romania) - XL / win Medium / Medium
**Signal.** RBI Q2-2026 investor presentation (31/07/2026) sets a dated integration roadmap: EUR 591m purchase at 1.28x P/B; regulatory filings and approvals through Q3-Q4/2026; closing expected Q4/2026; 'Data migration and rebranding' running through 2027; legal merger expected Q4/2027; synergies visible from 2028; one-off integration cost c. EUR 70m mainly in 2027; c. -60bps CET1 impact at closing.
**Implies.** A named, budgeted 2027 data-migration and rebranding programme: ATM/MFM re-signage and software re-branding, POS re-terminalisation and TMS merge, card re-issuance, and consolidation of two AML/KYC and transaction-monitoring stacks into one. Printec's ATM/self-service, POS, AML/compliance, transaction monitoring and managed-services lines all map onto the EUR 70m one-off budget.
**Source.** RBI Q2/2026 Results Presentation (slide: Acquisition of Garanti BBVA Romania on Track), 31/07/2026 - https://www.rbinternational.com/content/dam/rbi/ho/investors/events-and-presentation/presentation-and-webcast/conference-call-presentations/2026-07-31%20Q2%20Presentation%20RBI.pdf.coredownload.pdf (primary)
**Follow-up.** Time outreach to the post-closing integration PMO (Q4/2026-Q1/2027), before the 2027 migration work is scoped.

### 5. Raiffeisen Bank Romania / Garanti BBVA Romania (Romania) - L / win Medium / Medium
**Signal.** Same deck: Garanti adds c. EUR 4.3bn total assets and c. EUR 2.7bn loans, taking the combined bank to EUR 17.5bn assets, EUR 9.9bn loans and EUR 13.6bn deposits and third place in Romania by assets. RBI's Romania country table shows business outlets 267 at 30/06/2026, down from 269 at 31/12/2025 and 275 at 30/06/2025, with 4,738 employees (-3.8% y/y).
**Implies.** Branch count is falling only ~3% a year while headcount falls faster - the same 'automate inside a retained network' pattern seen at CEC Bank. That favours in-branch cash recyclers, teller automation and assisted self-service over branch closure. Garanti's own branches arrive as a second estate to rationalise or re-equip.
**Source.** RBI Q2/2026 Results Presentation, Country Financials (SEE) - Romania, 31/07/2026 - https://www.rbinternational.com/content/dam/rbi/ho/investors/events-and-presentation/presentation-and-webcast/conference-call-presentations/2026-07-31%20Q2%20Presentation%20RBI.pdf.coredownload.pdf (primary)
**Follow-up.** Get Garanti BBVA Romania's own branch/ATM counts - not disclosed on its website or in RBI filings; see operator_requests.

### 6. Raiffeisen Bank Romania (Romania) - L / win Medium / Medium
**Signal.** Accessibility statement commits the whole ATM/MFM fleet to assisted voice support for the full cash-withdrawal journey, with audio guidance via the customer's own headphones and raised tactile symbols, under Directive (EU) 2019/882 (European Accessibility Act) as transposed by Romanian Law 232/2022. The page still states the rollout is phased 'until the end of 2025' ('Etapizat, pana la sfarsitul anului 2025'), i.e. the wording has not been updated to confirm completion. Braille card embossing has been live since 15/05/2024.
**Implies.** A statutory accessibility retrofit across ~1,151 machines: audio-jack/voice-guidance software, tactile keypads and, where the hardware cannot be retrofitted, replacement. Direct ATM/self-service and managed-services work, and the same obligation lands on the Garanti estate at integration.
**Source.** Raiffeisen Bank Romania - Accesibilitate, 27/08/2026 - https://www.raiffeisen.ro/ro/despre-noi/accesibilitate.html (primary)
**Follow-up.** Ask how many of the 1,151 machines are certified accessible today and whether the Euronet-managed units are in scope.

### 7. Raiffeisen Bank Romania (Romania) - L / win Medium / Medium
**Signal.** Acceptance estate grew fast inside H1-2026: 'over 42,000' POS terminals at merchants at 31/03/2026 (Q1 release, 05/05/2026) rising to 'nearly 45,000' at 30/06/2026 - roughly +3,000 terminals in one quarter. Customers rose from 2.36m to ~2.4m over the same quarter.
**Implies.** A ~7% quarterly increase in deployed terminals means continuous POS hardware supply, terminal management, key injection and field service demand - Printec POS/acquiring and managed services.
**Source.** Raiffeisen Bank Romania Q1-2026 press release (compared with S1-2026 release), 05/05/2026 - https://www.raiffeisen.ro/ro/despre-noi/comunicate-de-presa/2026/rezultate-raiffeisen-bank-t1-2026-crestere-acelerata.html (primary)
**Follow-up.** Identify the current POS hardware vendors and whether deployment/field service is Euronet-run.

### 8. Garanti BBVA Romania (Raiffeisen acquisition target) (Romania) - M / win Medium / Medium
**Signal.** On 14/04/2026 Garanti BBVA Romania launched in-app onboarding using the Romanian electronic identity card: selfie, NFC read of the eID chip ('data is taken directly from the document, without image processing'), and a liveness test, allowing full remote current-account opening and in-app lending. It cites over 1.3 million electronic ID cards already issued in Romania.
**Implies.** Romania's eID rollout has become a live eKYC trigger, and the acquirer will have to decide in 2027 whether to keep, replace or extend this NFC/liveness stack across the merged bank. Direct fit for Printec digital onboarding/eKYC (and for eID reading at ATMs and branch counters).
**Source.** Garanti BBVA Romania press release, 14/04/2026 - https://www.garantibbva.ro/en/comunicate-de-presa/garanti-bbva-simplifies-digital-onboarding-and-in-app-lending-for-electronic-id-card-holders/ (primary)
**Follow-up.** Find the vendor behind Garanti's NFC/liveness flow (not named in the release) and Raiffeisen's own eID onboarding roadmap.

### 9. Raiffeisen Bank Romania (Romania) - Unscoped / win — / Medium
**Signal.** On 20/08/2026 the bank raised EUR 600m via a 6.4-year eurobond (maturity January 2033) at 4.626% p.a. to the January 2032 call, order book above EUR 1.3bn, 90+ international investors, rated Baa2 (one notch above sovereign), listed in Luxembourg; proceeds stated for MREL and financing the Romanian economy. It had also issued RON-denominated bonds on 13/08/2026 and EUR bonds on 20/01/2026.
**Implies.** Funding and capital headroom is being built immediately ahead of the Q4/2026 Garanti closing and the ~EUR 70m 2027 integration spend - the capex to re-equip and merge two estates is being pre-funded, which de-risks a 2027 technology bid.
**Source.** Raiffeisen Bank Romania press release, 20/08/2026 - https://www.raiffeisen.ro/ro/despre-noi/comunicate-de-presa/2026/emisiune-euroobligatiuni-600-milioane-euro-raiffeisen-bank-2026.html (primary)
**Follow-up.** Watch for further issuance around closing as a proxy for integration budget release.

### 10. Raiffeisen Bank Romania (Romania) - L / win Medium / Medium
**Signal.** MFM cash-deposit service is offered only between 06:00 and 23:30 daily and is described as deposit of RON (and EUR on the multifunctional EUR units) to own or third-party accounts, free of charge; no coin handling and no cash recycling is disclosed anywhere on the product page or in the locator service list. The SME product page states the bank operates 'peste 1100' ATMs and MFMs.
**Implies.** Deposit-only (non-recycling) machines with a nightly service window mean cash is still trucked and re-counted rather than recirculated in-machine. Classic case for cash recyclers plus 24/7 availability - Printec cash automation and managed services, with a measurable CIT-cost argument.
**Source.** Raiffeisen Bank Romania - ATM si multifunctionale (SME), 27/08/2026 - https://www.raiffeisen.ro/ro/imm/produse-si-servicii/servicii-electronice/atm-si-multifunctionale.html (primary)
**Follow-up.** Quantify the bank's cash-in-transit and cash-processing cost line to size the recycler business case.

### 11. Raiffeisen Bank Romania (Romania) - M / win Low / Low
**Signal.** Legal/compliance overhang confirmed in RBI's own semi-annual report: on 06/04/2026 Raiffeisen Bank S.A. received the preliminary report in the Romanian Competition Council investigation (Order 1267/24.10.2022) into alleged concerted practice in ROBOR setting; the bank published its position on the Council's decision on 08/06/2026. Romanian tax assessments produced an extraordinary burden of c. RON 158m (EUR 30m), and the ANPC dispute over instalment treatment remains in court.
**Implies.** Sustained regulatory pressure on conduct and reporting raises the value of auditable transaction monitoring and compliance tooling, and makes clean data lineage a stated requirement of the 2027 Garanti data migration. Indirect but supportive of Printec AML/compliance and transaction-monitoring positioning.
**Source.** RBI Semi-Annual Financial Report as at 30 June 2026, 31/07/2026 - https://www.rbinternational.com/content/dam/rbi/ho/investors/results-reports/semi-annual-report/2026-07-31%20Q2%20Report%20RBI.pdf.coredownload.pdf (primary)
**Follow-up.** Track the Competition Council's final decision and any remedial IT commitments.

## Coverage notes

Fresh full run (no checkpoint existed). Primary-first: (1) the bank's own 2026 press-release archive was enumerated exhaustively via its AEM JSON API (newslist.newssearch.{page}.json, 8 pages, Jan-Aug 2026, ~70 releases) rather than the JS-rendered HTML list - confirming there is NO standalone 2026 release on ATMs, cash automation or cloud, so all fleet data comes from the quarterly results releases and the locator; (2) the branch/ATM locator was pulled as raw JSON (map.maps.viewport.json, 1.7MB, 2,069 places) and counted programmatically, giving the deposit-capable split the bank does not publish and an exact reconciliation to its own '1,150 ATM and MFM' claim; (3) RBI group primary documents (Semi-Annual Financial Report and Q2/2026 investor presentation) were downloaded and text-extracted locally with pdfminer, which is where the dated Garanti integration roadmap and the Romania country table (267 outlets, 4,738 staff at 30/06/2026) came from - this is the country-vs-group reconciliation the baseline flagged as never done; (4) the target-side view was taken from Garanti BBVA Romania's own site and its Yoast sitemaps. GENUINE GAPS: cloud is unresolved at country level - RBI group has a Cloud Migration Acceleration Program and states >50% of technology assets on AWS/Azure, but no Romania-specific cloud, core-banking or data-centre disclosure exists in any 2026 primary source I opened, so no cloud signal is reported rather than a weak one; Garanti BBVA Romania publishes no branch, ATM or POS counts anywhere on its site, has no machine-readable locator, and RBI's filings give only balance-sheet aggregates, so the acquired estate size remains unknown; the bank's FY2025 IFRS statements were downloaded and searched but the PDF's table layout could not be parsed reliably enough to attribute an IT/intangibles capex figure, so none is quoted. Baseline items re-verified: the '1,150 ATM/MFM' figure is confirmed by two independent primary routes; the Garanti deal is confirmed and materially advanced with a dated 2027 migration phase that the 30/07/2026 baseline did not have. All confidence capped at Medium (Low where noted) per the rules.

## Access issues

raiffeisen.ro press-release index and network pages are JS-rendered and return no links to WebFetch; defeated by calling the underlying AEM JSON endpoints directly with a desktop User-Agent (documented in coverage_notes) - nothing was dropped. https://www.raiffeisen.ro/ro/despre-noi/comunicate-de-presa/2026.html returns HTTP 404 (no per-year page exists); the year filter is client-side only. raiffeisen.ro/sitemap.xml is stale - it contains no 2026 press releases and is not a reliable index. garantibbva.ro returns HTTP 200 with a soft-404 body for several guessed locator paths (/ro/utile/retea-sucursale-si-atm etc.); resolved by reading its Yoast sitemap index, which shows no branch/ATM locator page exists. The WebSearch budget for the session (200 calls) was exhausted mid-run, so the last third of the research was done entirely via direct WebFetch/curl against primary domains and sitemaps; no aggregator was substituted for a primary source. RBI's Q2 presentation PDF was too large/complex for the fetch tool and was extracted locally with pdfminer.

## Operator requests

none - no paywalled or gated PDF blocked this run. Two open information requests that need a human rather than an operator fetch: (a) Garanti BBVA Romania branch/ATM/POS counts, which are not published anywhere - best obtained from the BNR/Romanian Banking Association or from the transaction prospectus at closing; (b) Raiffeisen Bank Romania's accessible-ATM certification count against the Law 232/2022 deadline, which is an IR question.
