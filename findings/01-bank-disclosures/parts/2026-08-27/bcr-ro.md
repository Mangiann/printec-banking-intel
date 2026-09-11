# BCR (Erste Group) — Romania — run 27/08/2026

**Slug:** `bcr-ro` · **Status:** complete · **Signals:** 15

## Headline

- BCR's own locator API (new source this run, pulled 27/08/2026): **1,100 cash-out-only ATMs + 568 deposit-capable MFMs = 1,668 machines**; only **34.1% of the self-service estate can take cash in**.

- **736 of 1,100 ATMs carry an `NCR`-prefixed asset id** in BCR's public feed — live corroboration of the NCR/Printec estate.

- **282 branches, 211 tagged CASHLESS (74.8%), only 71 with a manned teller** — matches BCR's own '74% cashless' disclosure.

- Erste H1-2026 deck: Romania **294 branches / 4,909 FTE** at 30/06/2026 vs **290 / 4,978** at 31/03/2026 — **branches up, headcount down**.

- Erste Note 31: Romanian Competition Council **ROBOR fine of RON 577,361,887 (~EUR 110m)** announced early June 2026; investigation report served 06/04/2026.

- **Correction:** NCR Atleos' '2,600 ATMs / 500 branches' page is dated **23/03/2018** — stale by ~36% and ~44% respectively.


## Signals

### 1. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** BCR's own machine-readable locator API returned, pulled 27/08/2026: 1,100 cash-dispense-only ATMs, 568 multifunctional machines (MFM) and 282 branches. Every one of the 568 MFMs carries both cash-deposit services (MFM_2/3/4: deposits to own account, to another BCR customer's account, and business cash-in in RON) and cash withdrawal (MFM_6), plus FX cash exchange EUR/USD->RON and MoneyGram send/receive (567 units). Deposit-capable share of the self-service estate is 568/1,668 = 34.1%. 1,061 of 1,100 ATMs are contactless; 422 are voice-guided.

**Implies (Printec).** Two thirds of BCR's self-service estate (1,100 units) still cannot take cash in. That is the largest quantified recycler/deposit-automation white space disclosed by any Romanian bank this run, and it sits on a fleet Printec already services. Secondary hardware trigger: 39 ATMs without contactless and 678 without voice guidance are accessibility-driven replacement candidates.

- Source: BCR locator API, MFM dataset (bcr.ro /bin/erstegroup/gemesgapi/locations) — https://www.bcr.ro/bin/erstegroup/gemesgapi/locations/gem_site_location_locations-ro-bcr?types=MFM&items=9000&page=0 (27/08/2026, *primary*)

- Likelihood: High over 6-12 months - BCR is adding branches while cutting staff, which only works if cash migrates to machines · Confidence: Medium · Opp size: XL · Win: High · New: True

- Follow-up: Re-pull the same three API calls monthly; a rising MFM count is the deployment signal. Ask Printec Romania how many of the 568 MFMs are true recyclers vs deposit-only, and which of the 1,100 dispensers are end-of-life.

### 2. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** 736 of BCR's 1,100 ATM records carry an 'NCR'-prefixed asset id in the bank's own public locator feed (ouId values such as NCR05960, exposed in the public detail URL /ro/retea-unitati1/unitati-atm/echipamente-bcr/details?id=NCR05960); the remaining 364 use a generic 'ATM' prefix. Machine-readable corroboration that NCR (now NCR Atleos) hardware still underpins roughly two thirds of the dispenser fleet.

**Implies (Printec).** Current, independent evidence that the NCR/Printec estate at BCR is live - not just the 2017/2018 vendor press release. Strengthens Printec's incumbency case for managed services, APTRA software upgrade and recycler replacement on the NCR-tagged units, and shows exactly which 364 units are the competitor-held or unbadged remainder.

- Source: BCR locator API, ATM dataset (ouId field) — https://www.bcr.ro/bin/erstegroup/gemesgapi/locations/gem_site_location_locations-ro-bcr?types=ATM&items=9000&page=0 (27/08/2026, *primary*)

- Likelihood: Already true · Confidence: Medium · Opp size: L · Win: High · New: True

- Follow-up: Have Printec Romania reconcile the 736 NCR-tagged ouIds against its own service-contract asset register to see which machines are and are not under Printec managed service, and identify the vendor behind the 364 generic-prefixed units.

### 3. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** Of BCR's 282 branch records, 211 are tagged CASHLESS (no manned cash desk; cash handled only by in-branch equipment) and only 71 carry a GHISEU (manned teller counter) tag - 74.8% cashless. This matches BCR's own H1-2026 disclosure verbatim: '284 de unitati retail ... dintre care 74% sunt unitati unde operatiunile cu numerar se efectueaza doar la echipamente (cashless)'.

**Implies (Printec).** BCR has already converted three quarters of its branches to teller-less operation. All 211 depend on in-lobby cash automation staying available, which makes uptime-based managed services (SLA, first- and second-line maintenance, cash forecasting, incident management) contractually critical rather than discretionary. The 71 remaining GHISEU branches are a named, finite conversion pipeline for lobby recyclers / teller cash recyclers.

- Source: BCR locator API (BRANCH dataset) cross-checked against BCR 'Rezultate financiare Sem I 2026' PDF, p.'Despre BCR' — https://cdn.erstegroup.com/content/dam/ro/bcr/www_bcr_ro/Investitori/Informatii-financiare/2026/BCR-rezultate-financiare-Sem-I-2026.pdf (30/07/2026, *primary*)

- Likelihood: Already true; conversion of the residual 71 likely to continue through 2026-27 · Confidence: Medium · Opp size: L · Win: High · New: True

- Follow-up: Build the named list of the 71 GHISEU branches from the API and pitch a teller-cash-recycler conversion programme priced per unit.

### 4. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** Reconciliation gap: BCR's own H1-2026 boilerplate claims 'o retea nationala extinsa de ATM-uri si masini multifunctionale (1.750 de echipamente)', but the bank's live locator returns 1,668 machines (1,100 ATM + 568 MFM) on 27/08/2026 - a shortfall of 82 units, about 4.7%.

**Implies (Printec).** Either ~82 machines sit inside branches and are not published to the public map (typical of in-lobby teller-assist units), or the boilerplate is stale. Both readings matter commercially: the first is a hidden in-branch equipment population worth ~5% more addressable estate; the second means the fleet is shrinking faster than BCR's public messaging admits.

- Source: BCR 'Rezultate financiare Sem I 2026' PDF vs BCR locator API — https://cdn.erstegroup.com/content/dam/ro/bcr/www_bcr_ro/Investitori/Informatii-financiare/2026/BCR-rezultate-financiare-Sem-I-2026.pdf (30/07/2026, *primary*)

- Likelihood: Resolvable in one conversation · Confidence: Medium · Opp size: S · Win: Medium · New: True

- Follow-up: Ask BCR Operations directly whether the 1,750 figure includes non-published in-branch equipment. Do NOT quote 1,750 and 1,668 as if they were the same measure.

### 5. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** Erste Group's H1-2026 conference deck gives Romania 294 branches, 4,909 FTE and 3.0m customers at 30/06/2026 (retail loan share 17.3%, retail deposit share 12.4%), against 290 branches and 4,978 FTE at 31/03/2026 in the Q1-2026 deck. BCR ADDED 4 branches and CUT 69 FTE in one quarter.

**Implies (Printec).** Confirms the Romanian pattern already documented at CEC Bank: the network is not shrinking, staff per branch is. Growth-plus-automation is the best possible demand shape for Printec - new and relocated branches need self-service fit-out, and the headcount cut has to be absorbed by machines and managed services rather than by branch closures.

- Source: Erste Group, Presentation Teleconference H1 2026 (p.32) and Q1 2026 (p.31) — https://cdn.erstegroup.com/content/dam/at/eh/www_erstegroup_com/en/Investor_Relations/2026/presentations/IR_Pres_CC_260730_H126.pdf (30/07/2026, *primary*)

- Likelihood: High - consistent across two consecutive quarters · Confidence: Medium · Opp size: L · Win: Medium · New: True

- Follow-up: Track the branch/FTE pair every quarter from the Erste deck. Ask BCR Retail Distribution for the self-service fit-out standard per new or relocated unit (units of MFM per branch).

### 6. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** BCR H1-2026 (published 30/07/2026): net profit RON 1,205m (EUR 234m) vs RON 1,473m in H1-2025; operating result RON 2,116m (EUR 412m), +1.6% yoy; net fee and commission income RON 632m (EUR 123m), +15.5% yoy; net interest income RON 2,365m (EUR 460m), marginally down; cost/income 36.2% on BCR's own basis. Risk cost jumped to RON 352m (EUR 68m) from RON 104m. NPL 2.9% at Jun-2026, coverage 133%, total capital ratio 24.0%. Erste's Romania segment view shows operating expenses +3.1% to EUR 233m and cost/income worsening from 40.0% to 42.3%.

**Implies (Printec).** Profit down a fifth and risk cost more than tripled, but capital is very strong at 24.0% and fee income is accelerating. A worsening cost/income ratio driven by personnel, legal/consultancy and business-operation costs is exactly the trigger for outsourcing branch cash logistics and ATM operations - sell the managed-service case on opex reduction and headcount substitution, not on capex.

- Source: BCR press release and 'Rezultate financiare Sem I 2026' PDF; Erste Group Interim Report H1 2026, Romania segment — https://www.bcr.ro/ro/presa/informatii-de-presa/2026/07/30/grupul-bcr-semestrul-1-2026-partener-de-incredere-si-stabilitate-pentru-oameni-si-economie (30/07/2026, *primary*)

- Likelihood: High · Confidence: Medium · Opp size: M · Win: Medium · New: True

- Follow-up: Build a cost-per-cash-transaction model (teller vs MFM vs fully managed ATM) framed explicitly against the 42.3% segment cost/income ratio and the 69-FTE quarterly run-rate reduction.

### 7. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** Erste's H1-2026 interim report, Note 31, discloses that on 06/04/2026 BCR received an investigation report from the Romanian Competition Council alleging coordinated fixing of the ROBOR reference rate among the ten panel banks since November 2018, and that at the beginning of June 2026 the Council publicly announced a fine on BCR of 6.1875% of its 2025 turnover = RON 577,361,887 (~EUR 110m). The reasoned decision had not been served on BCR as at 30/07/2026; BCR will contest it. Separately the Romanian banking levy on Erste rose to EUR 39m from EUR 20m.

**Implies (Printec).** A ~EUR 110m competition fine plus a doubled banking levy squeezes discretionary capex through FY2026-27 - price and structure proposals as opex/managed service or phased multi-year rollouts rather than large up-front hardware purchases. It also lifts board-level appetite for demonstrable compliance tooling (transaction monitoring, surveillance, immutable audit trails), a direct Printec AML/compliance angle. Because all ten ROBOR panel banks are implicated, this is a sector-wide compliance-spend trigger in Romania, not a BCR-only one.

- Source: Erste Group Interim Report H1 2026, Note 31 'Contingent liabilities - legal proceedings' — https://cdn.erstegroup.com/content/dam/at/eh/www_erstegroup_com/en/Investor_Relations/2026/reports/IR_Interim_Report_EG_H126.pdf (30/07/2026, *primary*)

- Likelihood: High that capex discipline tightens; the cash outflow itself depends on appeal timing · Confidence: Medium · Opp size: M · Win: Medium · New: True

- Follow-up: Watch for publication of the Competition Council's reasoned decision and BCR's appeal to the Bucharest Court of Appeal; confirm which of the other nine panel banks were fined and at what level - that sizes the Romanian compliance-spend wave.

### 8. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** BCR H1-2026 digital disclosure: 2.38m active George mobile users; over 1 million retail products sold on a 100% digital flow in H1-2026; more than 40% of BCR mortgage customers took the loan through the fully digital George flow, up from 17% in H1-2025, with property documents uploaded from the phone and validated instantly, cutting time-to-loan to as little as 5 working days; 98% of retail investment trades digital; 98% of Pillar III pension enrolments digital; 93% of new insurance sales digital.

**Implies (Printec).** A 100%-digital mortgage flow that more than doubled its share in twelve months means BCR already runs an industrialised remote-identification, document-verification and e-signature stack in production at scale. That closes a greenfield eKYC/onboarding sale, but opens the adjacent ones: identity-document authentication and liveness at higher volume, fraud and transaction monitoring on the digital channel, and QES/HSM signing capacity as signing volumes grow.

- Source: BCR 'Rezultate financiare Sem I 2026' PDF (bcr.ro / cdn.erstegroup.com) — https://cdn.erstegroup.com/content/dam/ro/bcr/www_bcr_ro/Investitori/Informatii-financiare/2026/BCR-rezultate-financiare-Sem-I-2026.pdf (30/07/2026, *primary*)

- Likelihood: High · Confidence: Medium · Opp size: M · Win: Low · New: True

- Follow-up: Establish who supplies BCR's remote identification and qualified e-signature today (Erste group-level platform vs local vendor) before pitching. Lead with digital-channel fraud/transaction monitoring and HSM capacity, not with onboarding.

### 9. BCR / George Business — Romania

**Signal.** George Business, BCR's SME and large-corporate platform (which completed the replacement of eBCR and 24Banking at end-2025), has over 11,000 corporate clients and ~24,000 active users and processes about EUR 12bn of transactions per month - BCR states this is roughly 3% of Romania's annual GDP. From Q2-2026 more than 8,800 of those clients have FX Pro, negotiated-rate FX for 66 currency pairs inside the platform; in June 2026 about 85% of FX volumes ordered in George Business went through FX Pro.

**Implies (Printec).** EUR 12bn a month of corporate payment flow now runs through a single self-service channel with straight-through FX execution. That concentration is the classic trigger for corporate payment-fraud controls, sanctions/AML screening at the payment-initiation point and behavioural transaction monitoring - all Printec AML/compliance and transaction-monitoring territory. It also implies rising HSM and key-management load for corporate authorisation and signing.

- Source: BCR 'Rezultate financiare Sem I 2026' PDF and BCR Q1-2026 press release — https://cdn.erstegroup.com/content/dam/ro/bcr/www_bcr_ro/Investitori/Informatii-financiare/2026/BCR-rezultate-financiare-Sem-I-2026.pdf (30/07/2026, *primary*)

- Likelihood: Medium-High over 6-12 months · Confidence: Medium · Opp size: M · Win: Medium · New: True

- Follow-up: Ask BCR Corporate Operations what screening and payment-fraud controls sit behind George Business initiation, and whether FX Pro's straight-through path is covered by real-time monitoring.

### 10. Erste Group (BCR parent) — Austria / CEE

**Signal.** Erste Group H1-2026 group figures for context on BCR: 23.2m customers, 55,231 employees and 2,065 branches at 30/06/2026; more than 11.8 million users onboarded to George across all markets except Poland; overall digital sales share on straight-through-process criteria reached 73%; George Business roll-out group-wide reached ~85,000 clients onboarded, up 12% year-to-date.

**Implies (Printec).** BCR's 294 branches are 14% of Erste's 2,065 and its ~11,000 George Business clients are ~13% of the group's ~85,000 - so BCR is a proportionate, not outsized, part of the group. Practical consequence for Printec: self-service and channel decisions at BCR are increasingly taken inside an Erste group-wide platform frame, so a Romania-only pitch risks being routed to Vienna. Position offers that can be replicated across Erste's CEE footprint (CZ, SK, HU, HR, RS, RO) rather than as a single-country deal.

- Source: Erste Group, Presentation Teleconference H1 2026 — https://cdn.erstegroup.com/content/dam/at/eh/www_erstegroup_com/en/Investor_Relations/2026/presentations/IR_Pres_CC_260730_H126.pdf (30/07/2026, *primary*)

- Likelihood: Structural · Confidence: Medium · Opp size: Unscoped · Win: Medium · New: True

- Follow-up: Map which self-service/cash-automation decisions BCR takes locally vs which are set by Erste Group Procurement in Vienna, and whether Printec has a group-frame relationship with Erste at all.

### 11. Romania - all merchants (POS acceptance mandate) — Romania

**Signal.** Law 239/2025 amended OUG 193/2002 (art.1 para.12-13) so that, from 01/01/2026, every entity registered with the Trade Register that takes payment from customers must accept electronic payment - the previous RON 50,000 annual cash-collection threshold and the sectoral exceptions were removed. The only exemption is entities whose collections and payments run 100% through bank accounts. Accepting institutions are obliged to install a terminal on request (reported 30-day maximum) with acquisition, installation and connection costs regulated in the merchant's favour. Reported ANAF fines: RON 20,000-50,000 for failing to provide electronic acceptance and RON 5,000-7,500 for refusing a card payment.

**Implies (Printec).** A universal, fine-backed POS acceptance mandate with the terminal cost pushed onto the acquirer is the single biggest volume driver for POS estate expansion in Romania - the same shape as Albania's acceptance obligation already in the baseline. For Printec it is a terminal-supply, deployment, and terminal-estate-management (TMS, key injection, field service) opportunity, most likely at very low unit margin given the free-to-merchant model, so managed estate services matter more than box sales.

- Source: incasez.ro legal explainer on Law 239/2025 / OUG 193/2002 (secondary; primary text not retrievable this run) — https://incasez.ro/blog/obligativitate-pos-2026-plata-card-exceptii-amenzi (01/01/2026, *press*)

- Likelihood: Already in force; enforcement ramp through 2026 · Confidence: Low · Opp size: L · Win: Medium · New: True

- Follow-up: Retrieve the Law 239/2025 text from Monitorul Oficial / legislatie.just.ro to confirm the 30-day installation deadline and the exact fine bands before quoting them to a client. Then size the incremental Romanian terminal demand.

### 12. BCR merchant acquiring (via Global Payments) — Romania

**Signal.** BCR's card acceptance is delivered through Global Payments Inc., which BCR's own business page says serves over 8,000 partner merchants in Romania and manages a network of over 15,000 payment terminals. Product set: Android touchscreen POS terminals, GP Tom softPOS (phone-as-terminal, contactless Visa/Mastercard) and GP Webpay online payments.

**Implies (Printec).** Important routing correction for Printec's POS/acquiring line: BCR does not own its merchant acquiring estate - Global Payments does. Any POS terminal, softPOS or terminal-management opportunity tied to the 2026 acceptance mandate has to be sold to Global Payments Romania, not to BCR. Selling POS into BCR directly will not reach the decision maker.

- Source: BCR business site, 'Servicii acceptare plata cu cardul bancar' — https://www.bcr.ro/ro/business/general/conturi-si-servicii/solutii-de-plata-si-colectare/servicii-acceptare-carduri (27/08/2026, *primary*)

- Likelihood: Structural · Confidence: Medium · Opp size: M · Win: Low · New: True

- Follow-up: Confirm whether Global Payments Romania sources terminals and terminal-management centrally or locally, and whether Printec has any existing relationship with it. Do not route BCR POS opportunities through BCR.

### 13. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** CORRECTION / [STANDING]: NCR Atleos's customer-story page for BCR - the source of the widely repeated 'more than 2,600 ATMs ... with the help of NCR Corporation and its channel partner Printec' line, alongside 'more than 500 branches' and cash pickup/delivery for 'more than 1,500 corporate locations' at ~2,000 orders/day - is dated 23/03/2018. BCR's live locator shows 1,668 machines and 282 branches on 27/08/2026.

**Implies (Printec).** The 2,600-ATM and 500-branch figures are eight years stale and must not be quoted as current - the fleet is down ~36% and the branch network down ~44% since. What survives from that page is the vendor relationship itself (NCR + Printec, APTRA Cash Management Suite / OptiSuite for cash forecasting and replenishment), which the 736 NCR-tagged ouIds in today's locator independently corroborate.

- Source: NCR Atleos newsroom, 'Banca Comerciala Romana Improves Cash Management Efficiency with NCR Software' — https://www.ncratleos.com/news/banca-comerciala (23/03/2018, *primary*)

- Likelihood: n/a - correction · Confidence: Medium · Opp size: Unscoped · Win: — · New: True

- Follow-up: Purge '2,600 ATMs' and '500 branches' from all BCR collateral. Confirm with Printec Romania whether the APTRA OptiSuite/OptiCash cash-management deployment from 2017 is still in production and on what release.

### 14. BCR (Banca Comerciala Romana, Erste Group) — Romania

**Signal.** BCR's rural and small-urban financial-inclusion programme operates two mobile branches, one of them fully electric. The caravan has covered 30,000 km and reached 60 communities, serving over 8,000 people; in H1-2026 alone it reached 10 localities and covered 3,000 km. BCR separately maintains 15 corporate mobile offices and 19 business centres.

**Implies (Printec).** A small but genuine mobile/portable banking niche: mobile branches need ruggedised, connectivity-tolerant self-service and card-issuance-at-point equipment, and the electric unit implies a low-power hardware spec. Reaching 10 localities in six months is a slow rate - if BCR wants to widen rural coverage without fixed branches, deployable unattended kiosks/recyclers are the alternative to more vans.

- Source: BCR 'Rezultate financiare Sem I 2026' PDF — https://cdn.erstegroup.com/content/dam/ro/bcr/www_bcr_ro/Investitori/Informatii-financiare/2026/BCR-rezultate-financiare-Sem-I-2026.pdf (30/07/2026, *primary*)

- Likelihood: Medium · Confidence: Medium · Opp size: S · Win: Medium · New: True

- Follow-up: Pitch a low-power deployable kiosk/recycler option against the cost per community of the mobile-agency model; ask BCR for the caravan's 2027 coverage target.

### 15. BCR Leasing — Romania

**Signal.** BCR Leasing financed 37% more clients in H1-2026 than H1-2025, driven by micro-enterprises and SMEs, with heavy commercial vehicle financing up 45%. Interactions with its LEA virtual assistant rose 35% yoy and its Self Service platform passed 13,100 active users.

**Implies (Printec).** Secondary but real: a leasing subsidiary scaling 37% on self-service and virtual-assistant channels needs identity verification and contract e-signature at volume, and its SME customer base is exactly the population now caught by the 01/01/2026 POS acceptance mandate. Useful as a cross-sell wedge into the BCR group rather than as a standalone deal.

- Source: BCR 'Rezultate financiare Sem I 2026' PDF — https://cdn.erstegroup.com/content/dam/ro/bcr/www_bcr_ro/Investitori/Informatii-financiare/2026/BCR-rezultate-financiare-Sem-I-2026.pdf (30/07/2026, *primary*)

- Likelihood: Medium · Confidence: Medium · Opp size: S · Win: Low · New: True

- Follow-up: Check whether BCR Leasing's Self Service platform and e-signature run on the same stack as George, or on a separate one that could be addressed independently.


## Coverage notes

Fresh run - no checkpoint existed for 2026-08-27. Primary-first: (1) discovered and pulled BCR's own machine-readable locator API (www.bcr.ro/bin/erstegroup/gemesgapi/locations/gem_site_location_locations-ro-bcr, types ATM/MFM/BRANCH) with a desktop UA on 27/08/2026 - this is a NEW source the baseline never saw and it yields exact deposit-capable vs cash-out-only counts, the NCR asset-id prefix evidence, and the cashless/manned-teller branch split; (2) downloaded and text-extracted locally (pdfminer) Erste Group's Interim Report H1 2026 and both the H1-2026 and Q1-2026 teleconference decks, giving the Romania segment P&L, the 294-branch/4,909-FTE point and the previous-quarter comparison, plus the ROBOR Competition Council fine in Note 31; (3) recovered BCR's own H1-2026 press release and its results PDF after the obvious URL slug 404'd (working slug uses 'semestrul-1', not 'semestrul-i'). Angles varied vs prior runs: locator API, Erste group deck quarter-over-quarter delta, legal-proceedings note, merchant-acquiring product page, and the Romanian POS mandate. GENUINE GAPS: (a) BNR's payment-indicator statistics (national ATM/POS counts) are behind a JavaScript SPA and could not be retrieved even with a desktop UA - no Romanian national fleet baseline this run; (b) the ECB Data Portal API blocked the request outright, so the EU-harmonised alternative also failed; (c) the primary text of Law 239/2025 could not be retrieved from legislatie.just.ro, so the POS-mandate signal rests on a secondary legal explainer and is marked Low; (d) BCR is privately held with no Romanian public-procurement footprint, so no tender pipeline exists to search; (e) the WebSearch budget for this session was exhausted mid-run (200/200), after which all further work was done via direct HTTP/PDF retrieval, which limited discovery of August-2026 Romanian-language press items published after 30/07/2026.


## Access issues

bnr.ro StatisticsReportHTML.aspx?icid=800&table=1387 and bnr.ro/Indicatori-plati-5291.aspx both return a 200 JS shell with zero table rows even with a desktop Chrome UA - JS-rendered SPA, not a 403; not escalated to Claude-in-Chrome this run. ECB Data Portal (data-api.ecb.europa.eu, PSS dataset) returned HTTP 400 'Your access has been blocked due to security concerns'. legislatie.just.ro RezultateCautare timed out (curl exit 000) over both http and https. www.bcr.ro/ro/presa/informatii-de-presa listing is JS-rendered and exposes no article URLs in the served HTML; the gemesgapi 'quick' search endpoint accepts a query but ignores it and returns generic pages, so the press archive could not be enumerated - the H1 release was reached by slug-guessing. www.bcr.ro/ro/retea-unitati1/... 301-redirects to /ro/retea-unitati. No source was silently dropped.


## Operator requests

1) A human with a browser should open BNR's payment indicators (https://www.bnr.ro/Indicatori-plati-5291.aspx, and the interactive table at https://bnr.ro/StatisticsReportHTML.aspx?column=&icid=800&table=1387) and export the ATM and POS terminal counts for Romania for the latest available quarters - it is the only way to place BCR's 1,668 machines against the national fleet. 2) Someone should fetch the consolidated text of Legea 239/2025 (amending OUG 193/2002) from Monitorul Oficial or legislatie.just.ro to confirm the terminal-installation deadline and the exact fine bands before those figures are used with a client. Nothing is paywalled - both are free but machine-unreachable from this run.
