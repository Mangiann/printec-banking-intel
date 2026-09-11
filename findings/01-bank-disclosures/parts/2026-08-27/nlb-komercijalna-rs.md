# NLB Komercijalna banka (Serbia) - bank disclosure scan, run 27/08/2026

**Slug:** `nlb-komercijalna-rs` | **Status:** complete | **Signals:** 15

## Headline

- Live locator API returns **305 ATMs**, **129 branches**, **95 CDS** devices, 1,627 merchant locations (27/08/2026).
- **203 of 305** ATMs take cash in; **102 are cash-out-only**. Only **105** dispense EUR.
- Branches: 162 (Dec-24) -> 139 (Dec-25) -> **129** (Jun-26 and today). Staff 2,329 -> 2,153.
- Audited AR2025: 299 newer-generation ATMs, 48 24/7 zones, 6 DNT, **72 CDS** -> live 95 CDS (**+32% in 8 months**).
- NBS: Serbia **3,412 ATMs / 195,121 POS** at 30/06/2026 (was 3,336/187,957 at Q1). NLB KB ~8.9% of fleet vs 10.5% asset share.
- NBS: ATM **cash-in value +53.6% YoY** in Q2-2026 vs withdrawals +15.7%. Deposit/withdrawal value ratio now 31.5%.
- NLB Group H1-2026: NLB KB PAT EUR 66.0m, assets EUR 6,506.1m, CIR 44.2%, 49% of Strategic Foreign Markets pre-tax profit.

> **Caution for the Orchestrator:** the brief's '>90% of services off-branch' figure could NOT be verified in any primary source this run. The '300-machine multifunction replacement' is consistent with the 305/299 counts but **no replacement decision, budget or vendor is disclosed anywhere**.

## Signals

### 1. NLB Komercijalna banka (27/08/2026, NEW)

**Signal.** NLB Komercijalna banka's own branch/ATM locator API returns exactly 305 live ATM records on 27/08/2026, standing at 234 distinct coordinates (so ~71 sites host more than one machine). 151 of the 305 machines sit at a branch address and 154 stand off-branch. The same feed returns 129 branches, 95 CDS (Cash Deposit System) merchant cash-in devices and 1,627 merchant/acceptance locations. Endpoint is an unauthenticated AEM servlet returning full JSON with per-machine capability flags.

**Implies for Printec.** A ~305-machine estate is exactly the size band described as due for multifunction replacement. Printec ATM/self-service hardware plus managed services (first/second-line maintenance, cash forecasting, monitoring) can bid the whole fleet; the 154 off-branch machines are the ones that carry the highest service cost and are the natural managed-services wedge.

**Likelihood.** High that a fleet refresh decision falls inside 6-12 months given the 2030 digital-first strategy and the branch-count decline; procurement route (group-level NLB framework vs local RFP) unconfirmed.  |  **Size.** XL  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Establish whether ATM procurement is run by NLB Group in Ljubljana under a group framework agreement or locally by NLB KB Belgrade; identify the incumbent hardware vendor and the maintenance contract expiry.

**Source.** NLB Komercijalna banka locator API (branchsearch.facilities.json) - <https://www.nlbkb.rs/content/nlbbanks/nlbkb/sr/poslovnice/_jcr_content/root/container/container/branchsearch.facilities.json>

### 2. NLB Komercijalna banka (27/08/2026, NEW)

**Signal.** Per-machine capability counts from the same live feed (27/08/2026): 305 of 305 dispense RSD; 303 accept QR-code bill payment; 203 accept cash-in of RSD and EUR from individuals; 131 accept merchant daily takings ('uplata pazara') from legal entities; only 105 dispense EUR (dual-currency). So 102 of 305 machines (33%) are still cash-out-only with no deposit function, and 200 of 305 (66%) cannot dispense EUR.

**Implies for Printec.** A quantified recycler/deposit-automation white space of ~102 machines inside this bank alone, plus ~200 machines that could be upgraded to dual-currency dispensing. Printec cash automation / recyclers and multifunction ATMs map directly; dual-currency EUR dispense is a distinctive Serbian requirement (households hold EUR savings) that favours vendors with proven multi-cassette recycling.

**Likelihood.** Medium-high that deposit-capability extension continues through 2026-27; the bank is already extending it machine by machine.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Ask the bank what share of its RSD cash-in volume is recycled back out versus emptied by CIT; a recycling ratio below ~40% is the standard business case for swapping deposit-only modules for full recyclers.

**Source.** NLB Komercijalna banka locator API (branchsearch.facilities.json) - <https://www.nlbkb.rs/content/nlbbanks/nlbkb/sr/poslovnice/_jcr_content/root/container/container/branchsearch.facilities.json>

### 3. NLB Komercijalna banka (26/08/2026, NEW)

**Signal.** The bank re-published its four ATM-capability location lists as PDFs on 26/08/2026 (HTTP Last-Modified), generated 25/08/2026 (PDF creation timestamps). Row counts in those files: 183 machines accepting RSD/EUR cash-in, 234 with QR bill payment, 114 accepting merchant takings, 99 dispensing EUR. Every count is LOWER than the live API returned two days later (203 / 303 / 131 / 105), i.e. the public PDFs already lag the live estate.

**Implies for Printec.** A dated in-window trigger: the bank was actively editing its ATM capability inventory in the last days of August 2026. The gap between PDF and API (+20 deposit-capable, +69 QR, +17 merchant-deposit, +6 EUR-dispense) is the recent rollout rate, i.e. roughly 20 machines gaining deposit capability per publication cycle.

**Likelihood.** Continuous rollout is already happening; a bulk replacement decision would be the step change.  |  **Size.** M  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Re-pull all four PDFs and the API monthly; a jump of >30 machines in one cycle signals a hardware programme rather than firmware enablement.

**Source.** NLB Komercijalna banka - 'Funkcionalnosti na bankomatima' capability PDFs - <https://www.nlbkb.rs/stanovnistvo/pomoc-i-alati/funkcionalnosti-na-bankomatima>

### 4. NLB Komercijalna banka (31/12/2025, NEW)

**Signal.** The audited 2025 annual report (KPMG opinion, report dated March 2026) states the network held '299 bankomata novije generacije' (299 newer-generation ATMs), 48 self-service 24/7 zones, 6 day-night safes (DNT), 72 CDS merchant cash-deposit devices, 32 QMS and 50 aQMS queue-management units, plus 600 new branch monitors distributed. Against the live feed of 27/08/2026 (305 ATMs, 52 branches with a 24/7 zone, 95 CDS) that is +6 ATMs, +4 24/7 zones and +23 CDS units (+32%) in roughly eight months.

**Implies for Printec.** CDS is the fastest-growing device class in the estate (+32% in 8 months) while the ATM count is nearly flat - the bank is buying cash-in capacity for businesses faster than it is buying ATMs. Printec cash automation/recyclers and merchant cash-deposit devices are the direct fit; the flat ATM count is the argument that the existing 305 are ageing rather than expanding, which is what precedes a replacement cycle.

**Likelihood.** High that CDS expansion continues; ATM replacement is the open question.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Confirm the CDS vendor and whether CDS and ATM sit under one maintenance contract; a split estate is easier to attack device-class by device-class.

**Source.** NLB Komercijalna banka - Revizorski izvestaj 2025 (audited annual report incl. management report) - <https://www.nlbkb.rs/content/dam/nlb/nlbkb-rs-serbia/documents/prate%C4%8De-stranice/finansijski-izvestaji/revizorski-izvestaj/Revizorski%20izve%C5%A1taj%202025.%20godine.pdf>

### 5. NLB Komercijalna banka (30/06/2026, NEW)

**Signal.** Branch network contraction is steep and continuing: 162 branches at 31/12/2024, 139 at 31/12/2025 (audited note 1), 129 at 30/06/2026 (NLB Group H1-2026 presentation, Serbia column) and 129 in the live locator on 27/08/2026. Headcount fell from 2,329 to 2,153 over 2025. The ATM-per-branch ratio has therefore risen to 2.36 (305/129).

**Implies for Printec.** 33 branches closed in 18 months (-20%). Every closed branch shifts cash and routine servicing onto self-service, which is the demand driver for multifunction ATMs, recyclers and 24/7 zones. Printec self-service plus managed services, and digital onboarding/eKYC for the services that leave the counter entirely.

**Likelihood.** Further closures highly likely in H2-2026 given the 2030 'reduce operational complexity' target stated by the CEO.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Ask which of the remaining 129 branches are earmarked for closure and whether each closure is paired with an off-branch machine deployment - that pairing is the ATM order pipeline.

**Source.** NLB Komercijalna banka Revizorski izvestaj 2025 note 1 + NLB Group Presentation 1H 2026 - <https://www.nlbgroup.com/content/dam/nlb/nlb-group/documents/investor-relations/financial-reports/2026/h1/NLB-Group-Presentation-1H-2026.pdf>

### 6. NLB Komercijalna banka (27/08/2026, NEW)

**Signal.** Only 88 of the 129 branches carry a CDS device, only 52 of 129 have a '24/7 zone' (out-of-hours self-service lobby), only 6 have a day-night safe and 77 of 129 offer EUR cash-out. 112 of 129 branches have an attached ATM that accepts RSD/EUR cash-in.

**Implies for Printec.** 77 branches (60% of the network) still have no 24/7 self-service zone and 41 have no CDS. Printec 24/7 lobby build-out - recycler plus QMS plus access control - is a repeatable per-site package here, and it is the physical mechanism by which the bank moves services off the counter.

**Likelihood.** Medium-high over 6-12 months; the bank added 4 zones in 8 months, so a step change requires a programme decision.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Price a standard '24/7 zone in a box' per-site bundle and put it against the 77 branches without one.

**Source.** NLB Komercijalna banka locator API (branchsearch.facilities.json), branch service flags - <https://www.nlbkb.rs/content/nlbbanks/nlbkb/sr/poslovnice/_jcr_content/root/container/container/branchsearch.facilities.json>

### 7. NLB Komercijalna banka (30/06/2026, NEW)

**Signal.** National Bank of Serbia payment-system statistics updated 19/08/2026 give Serbia 3,412 ATMs and 195,121 POS terminals at 30/06/2026, up from 3,336 ATMs / 187,957 POS at 31/03/2026 and 3,196 ATMs / 177,185 POS at 30/06/2025. Serbian ATM count grew +216 YoY (+6.8%) and POS +17,936 YoY (+10.1%).

**Implies for Printec.** Serbia's ATM estate is GROWING, against the Western European trend - this is an expansion market, not a rationalisation market. NLB KB's 305 machines are ~8.9% of the national fleet while the bank holds ~10.5% of banking assets, so it is under-indexed on self-service and has headroom to add machines rather than only replace them. POS growth of 10% YoY also supports Printec's POS/acquiring line.

**Likelihood.** Trend is established across five consecutive quarters.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** regulator

**Follow-up.** Break the 3,412 down by bank via each bank's locator feed to size the true competitive gap; this run confirmed NLB KB's slice at 305.

**Source.** Narodna banka Srbije - Prihvatna mreza (acceptance network) statistics - <https://www.nbs.rs/export/sites/NBS_site/documents/platni-sistem/statistika/el_novac/prihvatna_mreza.xlsx>

### 8. NLB Komercijalna banka (30/06/2026, NEW)

**Signal.** NBS transaction statistics updated 19/08/2026: cash PLACED INTO ATMs in Serbia by domestically issued cards reached 3,406,129 transactions worth RSD 173,936m in Q2-2026, versus 2,582,157 transactions / RSD 113,237m in Q2-2025 - +31.9% by count and +53.6% by value YoY. ATM cash WITHDRAWALS over the same period rose only +4.5% by count and +15.7% by value (27,288,350 txns / RSD 552,239m). ATM deposit value is now equal to 31.5% of ATM withdrawal value, up from 23.7% a year earlier.

**Implies for Printec.** This is the single strongest recycler argument in the Serbian market: money going INTO ATMs is growing three and a half times faster in value than money coming out. At a 31.5% deposit-to-withdrawal ratio, recycling machines start displacing CIT (cash-in-transit) journeys and vault holdings, which is the hard-money part of a Printec cash-automation business case. Directly supports recyclers, cash forecasting and managed services.

**Likelihood.** Trend is accelerating quarter on quarter; the business case only strengthens.  |  **Size.** XL  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** regulator

**Follow-up.** Model CIT-journey savings for NLB KB at the national deposit/withdrawal ratio applied to its 203 deposit-capable machines; that is the number a Serbian CFO responds to.

**Source.** Narodna banka Srbije - Payment transactions in the acceptance network by device type - <https://www.nbs.rs/export/sites/NBS_site/documents/platni-sistem/statistika/el_novac/trans_prihvatna_mreza.xlsx>

### 9. NLB Komercijalna banka (30/06/2026, NEW)

**Signal.** NLB Group H1-2026 results (published 06/08/2026): NLB Komercijalna banka Beograd on a stand-alone basis reported result after tax EUR 66.0m, total assets EUR 6,506.1m, RoE 15.6%, net interest margin 3.60%, cost/income 44.2%, NPL 0.8% and 129 branches at 30/06/2026. It contributed 49% of the Strategic Foreign Markets segment's pre-tax profit and grew gross loans to individuals +21% YoY, the highest in the Group.

**Implies for Printec.** The bank is highly profitable, has the Group's best retail growth, and is running a 44.2% cost/income ratio it wants lower. That combination funds capex and makes an efficiency-led self-service pitch land: this is a buyer with money and a stated cost agenda, not a distressed cost-cutter.

**Likelihood.** Capacity to invest is not in question over 6-12 months.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Time the approach to the NLB Group budget cycle - group capex for the following year is typically locked in Q4.

**Source.** NLB Group Presentation 1H 2026 / NLB Group Interim Report January-June 2026 - <https://www.nlbgroup.com/content/dam/nlb/nlb-group/documents/investor-relations/financial-reports/2026/h1/NLB-Group-Interim-Report-January%E2%80%93June-2026.pdf>

### 10. NLB Komercijalna banka (30/06/2026, NEW)

**Signal.** NLB Group's 1H-2026 presentation puts Group digital penetration at 65% at 30/06/2026 (from 62% at 12-2025, 57% at 12-2024, 50% at 12-2023) against a stated 2030 target of >80%, and confirms 'accelerating our digitalisation is the core of our 2030 strategy'. The Group also flags a relaunch of the NLB Klik digital banking app in Serbia during 2026 and real-time digital card issuance across the group.

**Implies for Printec.** A hard, dated group-level digitalisation target (>80% by 2030) is the mandate under which a Serbian branch-to-self-service shift gets funded. Printec digital onboarding/eKYC, digital card issuance/instant issuance and transaction monitoring all attach to this programme; the Serbia app relaunch in 2026 is a concrete in-year workstream.

**Likelihood.** Programme is already in delivery.  |  **Size.** M  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Find out whether instant/digital card issuance in Serbia is done in-branch on a card printer (Printec instant-issuance opportunity) or purely virtual.

**Source.** NLB Group Presentation 1H 2026 - <https://www.nlbgroup.com/content/dam/nlb/nlb-group/documents/investor-relations/financial-reports/2026/h1/NLB-Group-Presentation-1H-2026.pdf>

### 11. NLB Komercijalna banka (31/12/2025, NEW)

**Signal.** The 2025 annual report describes a running branch-transformation programme: 10 branches renovated during 2025, 3 under adaptation at year-end, 51 branches adapted in total since the project began; digital FX-rate displays installed in 88 branches during 2025; safe-deposit-box service withdrawn from 5 locations and consolidated into one branch under NLB Group security standards; probate processing centralised into back office saving 5 FTE and cutting handling time from 6 months to 15 days.

**Implies for Printec.** A live, funded branch refit programme with a per-site works package - the moment when self-service hardware, queue management and cash devices are specified. 78 of the 129 branches have still not been through the refit. Printec self-service, QMS and branch cash automation attach to each remaining site.

**Likelihood.** Programme continues in 2026 at roughly 10 sites/year unless accelerated.  |  **Size.** M  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Get the 2026 refit site list and the standard equipment specification for a refitted branch.

**Source.** NLB Komercijalna banka - Revizorski izvestaj 2025 (management report) - <https://www.nlbkb.rs/content/dam/nlb/nlbkb-rs-serbia/documents/prate%C4%8De-stranice/finansijski-izvestaji/revizorski-izvestaj/Revizorski%20izve%C5%A1taj%202025.%20godine.pdf>

### 12. NLB Komercijalna banka (31/12/2025, NEW)

**Signal.** Property and equipment note in the 2025 accounts: equipment net book value RSD 1,965,389k at 31/12/2025 (from RSD 1,880,262k), and 'investicije u toku' (assets under construction / capex in progress) RSD 946,282k at 31/12/2025, up 15.7% from RSD 817,933k a year earlier. Separately the income-statement note discloses 2025 costs of RSD 207,841k for maintenance of electronic-banking equipment (from RSD 159,052k, +30.7% YoY) and RSD 168,763k for management and maintenance of the POS network and card equipment.

**Implies for Printec.** Capex in progress up 15.7% and e-banking equipment maintenance up 30.7% YoY is the classic signature of an ageing estate costing more to keep alive. That maintenance line is precisely the budget a Printec managed-services contract displaces, and it is the number to quote back to the bank.

**Likelihood.** Rising maintenance cost strengthens a replacement case each year it persists.  |  **Size.** L  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Ask for the split of the RSD 207.8m e-banking maintenance line between ATM hardware, software licensing and network; the hardware slice is the addressable figure.

**Source.** NLB Komercijalna banka - Revizorski izvestaj 2025, notes on property/equipment and operating expenses - <https://www.nlbkb.rs/content/dam/nlb/nlbkb-rs-serbia/documents/prate%C4%8De-stranice/finansijski-izvestaji/revizorski-izvestaj/Revizorski%20izve%C5%A1taj%202025.%20godine.pdf>

### 13. NLB Komercijalna banka (26/08/2026, NEW)

**Signal.** The bank's own ATM services page confirms the multifunction feature set already live on the estate: EUR withdrawal from FX accounts (minimum EUR 50, daily cap EUR 1,000 per FX account, no fee, primary cardholder only), RSD and EUR cash deposit to personal accounts, merchant daily-takings deposit for legal entities, and QR-code bill payment. Access is by card plus PIN.

**Implies for Printec.** The functional specification for any replacement fleet is already public and is genuinely multifunction: dual-currency dispense, dual-currency deposit, bulk merchant deposit and QR payment on one machine. Any Printec bid must clear that bar; equally it confirms the bank buys full-function machines rather than cash dispensers, which raises the per-unit value of the 305-machine estate.

**Likelihood.** Standing requirement.  |  **Size.** M  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Confirm note/coin capacity and cassette configuration per machine model, and whether EUR and RSD share a recycling cassette set.

**Source.** NLB Komercijalna banka - Funkcionalnosti na bankomatima - <https://www.nlbkb.rs/stanovnistvo/pomoc-i-alati/funkcionalnosti-na-bankomatima>

### 14. NLB Komercijalna banka (27/08/2026, NEW)

**Signal.** ATM geographic reach exceeds branch reach substantially: the 305 ATMs cover 132 distinct Serbian towns/cities while the 129 branches cover only 84. Merchant/acceptance locations in the same feed total 1,627.

**Implies for Printec.** 48 towns are served by an ATM with no branch behind it. Those are the machines where downtime is most expensive and where remote monitoring, predictive maintenance and cash forecasting earn their fee - the core Printec managed-services proposition rather than a hardware sale.

**Likelihood.** Structural.  |  **Size.** M  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Quantify current SLA and uptime on the branchless sites; if the bank cannot state it, that is the opening.

**Source.** NLB Komercijalna banka locator API (branchsearch.facilities.json) - <https://www.nlbkb.rs/content/nlbbanks/nlbkb/sr/poslovnice/_jcr_content/root/container/container/branchsearch.facilities.json>

### 15. NLB Komercijalna banka (27/08/2026, carried)

**Signal.** Corporate profile page states balance-sheet total above EUR 6.5bn, total loans above EUR 4bn, total deposits above EUR 5bn, market share 10.5% and more than one million active clients, and describes the bank as holding 'one of the largest networks of ATMs and branches in Serbia'.

**Implies for Printec.** Confirms scale and self-declared network leadership - the bank positions its ATM estate as a competitive asset, which makes a fleet-modernisation pitch a brand argument as well as a cost argument.

**Likelihood.** Standing positioning.  |  **Size.** S  |  **Win.** Medium  |  **Confidence.** Medium  |  **Tier.** primary

**Follow-up.** Use the bank's own 'largest ATM network' claim against the finding that only 66% of its machines take deposits.

**Source.** NLB Komercijalna banka - O nama / About Us - <https://www.nlbkb.rs/o-nama>

## Coverage notes

Fresh run, no checkpoint existed. WebSearch quota for the session was already exhausted at 200/200 before this bank started, so ALL findings here come from direct primary-source fetching with a desktop User-Agent and local PDF/XLSX parsing - no search engine was used. Angles worked: (1) the bank's own AEM locator, where I recovered an unauthenticated machine-readable endpoint (.../branchsearch.facilities.json, also .filters.json?kind=atm|branch) that returns all 2,156 facilities with per-machine capability flags - this is a NEW reusable source not in the baseline and is the single best asset from this run, worth adding to the source catalogue; (2) the four 'Funkcionalnosti na bankomatima' capability PDFs, parsed by column geometry for exact row counts; (3) the audited 2025 annual report (KPMG), which carries the only vendor-independent device inventory the bank publishes (299 ATMs / 48 zones / 6 DNT / 72 CDS / 32 QMS / 50 aQMS); (4) NLB Group H1-2026 interim report and presentation for the Serbia column; (5) NBS payment-system statistics, refreshed 19/08/2026, for national ATM/POS counts and ATM deposit-vs-withdrawal volumes. BASELINE RECONCILIATION: the baseline's NBS figure (Serbia 3,336 ATMs / 187,957 POS at Q1-2026) is now superseded - Q2-2026 is 3,412 ATMs / 195,121 POS. The baseline listed 'Groups OTP/Intesa Sanpaolo CEE/NLB/UniCredit' as never researched; the NLB group-level Serbia disclosure is now reconciled against the country-level locator count for the first time (129 branches in the group presentation matches 129 in the live locator exactly). GENUINE GAPS: (a) I could NOT verify the '>90% of services off-branch' figure named in the brief - it appears in neither the 2025 annual report, the NLB Group H1-2026 report/presentation, nor anywhere on nlbkb.rs that I could reach; it may come from a Serbian press interview I could not search for. Treat it as UNVERIFIED and do not carry it forward without a source. The closest verifiable proxies I did establish are NLB Group digital penetration 65% at H1-2026 against a >80% 2030 target, and the 129-branch/305-ATM ratio. (b) No public tender document exists - NLB KB is a private bank and does not procure through the Serbian public-procurement portal, so there is no RFP to cite and no deadline to report. (c) I did not benchmark competitor Serbian bank fleets (Banca Intesa Beograd, OTP Serbia, AIK, Raiffeisen) this run - out of scope for a single-bank task, but the same AEM locator pattern is worth testing on them. (d) The '300-machine multifunction ATM replacement' framing in the brief is CONSISTENT with what I found (305 live machines, 299 'newer generation' per the annual report) but I found no disclosure of an actual replacement decision, budget or vendor - the replacement is an inference from fleet age and capability gaps, not a disclosed fact. Flagged so the Orchestrator does not promote it.

## Access issues

www.nlb.rs returned HTTP 406 to every fetch even with a desktop User-Agent - it is the Slovenian-domain redirect shell, not the Serbian site; the correct primary host is www.nlbkb.rs, which served everything without blocks. www.ekapija.com returned 403 to the fetch tool (Serbian business-press paywall/bot wall) - logged, not silently dropped; I did not escalate to Claude-in-Chrome because no specific ekapija article had been identified to retrieve. html.duckduckgo.com returned HTTP 202 anti-bot pages and www.bing.com returned a results page with all outbound links stripped, so no search-engine fallback was available once the WebSearch quota was gone. nbs.rs served everything over plain curl with a desktop UA - no 403, contrary to the standing warning. One NBS file, platne_kartice/broj_i_promet_bankomati.xls, is a legacy .xls whose internal Last-Saved timestamp is 2016 and which no available parser could read; I did not use it, and the equivalent current data came from el_novac/trans_prihvatna_mreza.xlsx instead. AEM component endpoints only respond under the /content/... path with _jcr_content (not jcr:content, which returns HTTP 400 from the front-end proxy).

## Operator requests

No paywalled or gated PDF blocked this run - every document cited was fetched successfully. Two operator asks, both optional: (1) a web search or ekapija.com/kamatica.com/biznis.rs retrieval for any 2026 Serbian-language interview with NLB Komercijalna banka management quoting a share of services performed outside branches - this is the one figure in the brief I could not source; (2) if anyone has access, the NLB Group procurement or supplier register would settle whether ATM hardware is bought centrally in Ljubljana or locally in Belgrade, which determines who Printec should be selling to.
