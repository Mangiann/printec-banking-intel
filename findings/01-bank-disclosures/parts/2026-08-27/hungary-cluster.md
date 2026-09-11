# Hungary cluster - OTP, K&H, Erste HU, MBH

Run date 27/08/2026 - status: complete - 14 signals

## Headline

**The find of this run is the full statutory chain behind Hungary's ATM mandate, with a hard deadline four months out.** Act XVIII of 2025 (promulgated 12/05/2025) obliges payment service providers to guarantee cash withdrawal in *any* settlement, MNB-enforced with fines from HUF 2m to HUF 200m on a 30-month escalation ladder. Its two implementing decrees give the operational detail the baseline never had:

- **16/2025. (V. 29.) NGM rendelet** - an ATM in every settlement above **1,000 inhabitants by 31/12/2025** and above **500 inhabitants by 31/12/2026** (2022 census basis).
- **19/2025. (VI. 26.) MNB rendelet** - a statutory **cost-sharing formula** between banks (30% cards issued, 25% balance sheet, 20% cash-service revenue, 15% household HUF deposits, 10% consumer accounts), with contracting deadlines 20/07/2025 and 28/02/2026. Hungary has effectively legislated a **pooled rural ATM network**, the same structural move the baseline flagged in Croatia and Czechia.

**The second find is a precisely sized recycler retrofit pool**, taken from the banks' own machine-readable locator feeds pulled 27/08/2026:

| Bank | ATMs | Deposit-capable | Cash-out only | % deposit | Branches |
|---|---|---|---|---|---|
| OTP Hungary | 1,844 (locator) | 624 | 1,220 | 33.8% | - |
| MBH Bank | 1,285 | 256 | 1,029 | 19.9% | 398 + 132 mobile stops |
| Erste Bank Hungary | 505 | 268 | 237 | 53.1% | 97 |
| K&H | not obtainable (kh.hu 403) | - | - | - | 188 (via KBC) |

**Sharpest single target:** MBH still tags every ATM by predecessor brand - 803 legacy Takarekbank, 383 MKB, 99 Budapest Bank - and **not one of the 803 Takarekbank machines accepts a cash deposit**. All 256 deposit-capable units come from the MKB and Budapest Bank estates. The three heritages also still run three different quick-withdrawal preset sets, i.e. the ATM software estate is unharmonised three years post-merger.

**Counter-current worth naming:** OTP's own H1-2026 report shows the Hungarian ATM count *falling* from 1,987 to 1,929 in six months while the placement duty runs, and the MNB's latest payments report shows cash withdrawals down 4% in number and 4.5% in value. More mandated machines, less cash through them - the only reconciliation is lower cost per site, which is the managed-services and recycler argument.

## What could not be verified

No Hungarian AML fine is claimed in this run. The MNB decision register (hatarozatkereso.mnb.hu) is WAF-blocked, apps.mnb.hu denies access, and two MNB supervisory-news paths 404. Claude-in-Chrome escalation failed - no browser is connected to this account. K&H's own site is Akamai-blocked. Both are logged as operator requests.

## Signals

### 1. MBH Bank (Hungary) **[NEW]**

- **Signal:** MBH Bank's own branch/ATM locator API returns 1,285 fixed ATM points across 779 settlements, of which only 256 (19.9%) accept cash payments in (point_ATM_paying_type=Y) - i.e. 1,029 machines are cash-out only. 1,232 of the ATMs are 24/7. Separately 398 fixed branches, 132 mobile-branch stops and 8 university 'MBH Digitalis Zona' points; 525 of the 538 branch-type points still run a manned cash desk.
- **Source:** MBH Bank branch & ATM locator API (www.mbhbank.hu/apps/backend/branch-and-atm) - https://www.mbhbank.hu/apps/backend/branch-and-atm (27/08/2026, primary)
- **Implies:** Largest single recycler white space disclosed in Hungary this run: ~1,029 MBH ATMs would each need a deposit/recycling module to meet a cash-in obligation, and 525 manned cash desks are the cost line automation displaces.
- **Likelihood:** High - Act XVIII of 2025 already obliges cash-withdrawal coverage and the deposit gap is the next lever | **Confidence:** Medium | **Opp size:** XL | **Win:** Medium
- **Follow-up:** Re-pull the same endpoint monthly; a rise in point_ATM_paying_type=Y counts is the recycler-rollout tell. Ask MBH procurement who supplies the 256 deposit-capable units.

### 2. Hungary (legislature / MNB) (Hungary) **[NEW]**

- **Signal:** Act XVIII of 2025 'az automata bankjegykiado gepek telepiteserol' (on the installation of automated banknote dispensers) was promulgated 12/05/2025 and entered into force on the third day after promulgation. It obliges payment service providers to ensure cash withdrawal for consumer account holders in ANY settlement, primarily via ATM or branch counter; municipalities must provide a site free of charge; the MNB enforces, with fines of HUF 2m-200m escalating (from HUF 5m up to HUF 200m) over a 30-month non-compliance ladder reviewed at 3-month intervals. The rollout SCHEDULE is delegated to a ministerial decree.
- **Source:** Nemzeti Jogszabalytar / Wolters Kluwer Jogtar - 2025. evi XVIII. torveny - https://net.jogtar.hu/jogszabaly?docid=A2500018.TV (12/05/2025, primary)
- **Implies:** A statutory, fine-backed nationwide ATM placement duty - direct demand for through-the-wall/lobby ATMs, site-hardening, cash-in-transit-light designs and managed services in low-volume rural settlements where banks will not staff a branch.
- **Likelihood:** High - already in force, enforcement ladder running | **Confidence:** Medium | **Opp size:** XL | **Win:** High
- **Follow-up:** Find and read the implementing ministerial (NGM) decree that sets the utemezes - it carries the settlement thresholds and the dated milestones. Then map uncovered settlements against each bank's locator feed.

### 3. OTP Bank (OTP Core, Hungary) (Hungary) **[NEW]**

- **Signal:** OTP's H1-2026 report (published 05/08/2026) shows OTP Core (Hungary) at 299 branches, 1,929 ATMs and 149,868 POS at 30/06/2026, down from 301 branches, 1,987 ATMs and 150,158 POS at 31/12/2025 - a net reduction of 58 ATMs (-2.9%) in six months. Group totals: 1,177 branches, 5,619 ATMs, 287,188 POS and 41,089 FTE at 30/06/2026 (vs 1,196 / 5,622 / 288,771 / 40,846 at 31/12/2025).
- **Source:** OTP Bank Nyrt., Feleves Jelentes - 2026. elso feleves eredmeny (p.42) - https://www.otpbank.hu/portal/hu/ir-jelentesek (05/08/2026, primary)
- **Implies:** OTP is shrinking its Hungarian ATM count while a statutory placement duty runs - the reconciliation gap is either exemptions, shared-ATM arrangements or a swap to fewer/richer machines. Either reading is a replacement/upgrade cycle, not a fleet exit.
- **Likelihood:** Medium-High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium
- **Follow-up:** Get OTP's Q2-2026 analyst tables (OTP_Bank_analyst_tables_2Q2026.xlsm) and ask whether the -58 is decommissioning or migration to deposit-capable units.

### 4. OTP Group (Hungary (group-wide)) **[NEW]**

- **Signal:** OTP signed a share purchase agreement on 20/07/2026 to buy 100% of Luminor Holding (Baltics) from Blackstone-managed funds and DNB Bank; on Q1-2026 pro forma figures the deal would lift OTP Group total assets 16%, gross loans 29%, mortgages 13% and leasing 30%, and raise the euro-area share of net loans from 42% to 50%. Closing awaits regulatory approvals.
- **Source:** OTP Bank Nyrt., Feleves Jelentes - 2026. elso feleves eredmeny (p.7) - https://www.otpbank.hu/portal/hu/ir-jelentesek (05/08/2026, primary)
- **Implies:** Post-close estate integration (ATM/POS/channel harmonisation) across three new euro-area markets; OTP explicitly praises Luminor's IT modernisation, signalling appetite for platform consolidation spend group-wide.
- **Likelihood:** Medium - subject to regulatory approval | **Confidence:** Medium | **Opp size:** L | **Win:** Low
- **Follow-up:** Track closing date and whether OTP standardises the Baltic self-service estate onto its CEE stack.

### 5. OTP Bank (OTP Core, Hungary) (Hungary) **[NEW]**

- **Signal:** OTP's H1-2026 report attributes the modest 3% y/y rise in net fees partly to the increase, effective February 2026, of the monthly free-of-charge retail cash withdrawal ceiling, alongside the retail fee freeze committed from April 2025 to mid-2026.
- **Source:** OTP Bank Nyrt., Feleves Jelentes - 2026. elso feleves eredmeny - https://www.otpbank.hu/portal/hu/ir-jelentesek (05/08/2026, primary)
- **Implies:** Policy is pushing free ATM cash-out volume up while capping fee recovery - banks respond by cutting cost per transaction (recyclers, remote monitoring, outsourced cash management), which is Printec's managed-services pitch.
- **Likelihood:** High - already in force | **Confidence:** Medium | **Opp size:** M | **Win:** Medium
- **Follow-up:** Quantify the new free-withdrawal ceiling from the underlying Hungarian regulation and model the ATM transaction-volume uplift.

### 6. Erste Bank Hungary (Hungary) **[NEW]**

- **Signal:** Erste Bank Hungary's own GEM location API returns 505 ATMs across 276 settlements and 97 branches across 72 settlements (pulled 27/08/2026). Of the 505 ATMs, 268 (53%) carry the service tag 'Keszpenzbefizetesre alkalmas ATM' (cash-deposit capable) - 237 are cash-out only. 504 of 505 accept contactless cards; 334 are tagged fully accessible; 450 dispense the 1,000/5,000/10,000/20,000 HUF denomination set.
- **Source:** Erste Bank Hungary branch & ATM locator API (erstebank.hu/bin/erstegroup/gemesgapi/locations) - https://www.erstebank.hu/bin/erstegroup/gemesgapi/locations/gem_site_location_locations-hu-ebh?types=ERSTE-ATM&items=5000&page=0&language=hu (27/08/2026, primary)
- **Implies:** Erste HU is the most deposit-ready of the four (53% vs OTP 34% and MBH 20%) but still has 237 cash-out-only machines to upgrade, on a very thin 97-branch base - the classic profile for recycler + managed-services outsourcing rather than more branches.
- **Likelihood:** Medium-High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium
- **Follow-up:** Re-pull quarterly and watch the atmDeposit tag count. Check whether Erste HU's 505 ATMs are self-operated or already on a third-party managed-services contract.

### 7. OTP Bank (Hungary) (Hungary) **[NEW]**

- **Signal:** OTP Hungary's own ATM locator API returns 1,844 ATM points (27/08/2026). Detail records show only 624 (33.8%) are cash-deposit capable; 1,220 are cash-out only. 1,622 are contactless, 1,600 flagged accessible, 1,498 available 7/24. At least 376 of the sites are hosted in municipal or community premises (Onkormanyzat, Polgarmesteri Hivatal, Muvelodesi Haz, Kozossegi Haz and similar).
- **Source:** OTP Bank branch & ATM locator API (otpbank.hu/apps2/branch-atm-locator/atm/list + /atm/details) - https://www.otpbank.hu/portal/hu/kapcsolat/fiokkereso (27/08/2026, primary)
- **Implies:** Two Printec hooks: (a) ~1,220 OTP machines without a cash-in path is the single biggest recycler retrofit pool in Hungary; (b) the 376 municipality-hosted sites are exactly the Act XVIII delivery model (councils supply the site free) and are typically low-volume rural units where remote monitoring/managed services beat in-house field service.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** XL | **Win:** Medium
- **Follow-up:** Reconcile the 1,844 locator points against the 1,929 ATMs OTP reports at 30/06/2026 - the gap is likely decommissioned/planned units (the feed contains entries labelled 'megszunt OTP' and 'uzemen kivul').

### 8. K&H Bank (KBC Group) (Hungary) **[NEW]**

- **Signal:** KBC's 2Q2026 analyst presentation (06/08/2026) puts K&H Hungary at 188 branches and 1.7m clients, 4% of KBC group assets, EUR 9bn loans and EUR 12bn deposits. KBC booked +EUR 53m of additional Hungarian national bank taxes in 2Q26 and a EUR -42m impairment for modification losses tied to the uncertain lifetime extension of the Hungarian mortgage interest-cap regulation; group bank & insurance taxes are guided up 10% y/y to EUR 730m in 2026.
- **Source:** KBC Group, 2Q 2026 analyst presentation (slides 34 and network overview) - https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-analysts-presentation.pdf (06/08/2026, primary)
- **Implies:** Hungarian levies plus interest-cap losses squeeze K&H's cost base - the standard response is channel cost-out (self-service migration, cash automation, outsourced ATM estate), which is Printec's core sell. 188 branches is a large manned footprint to automate.
- **Likelihood:** Medium-High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium
- **Follow-up:** Get K&H's own Hungarian annual report for the ATM count - kh.hu is Akamai-blocked to non-Hungarian IPs, so route via an operator or the MNB Golden Book sector statistics.

### 9. Hungary (Ministry for National Economy / NGM) (Hungary) **[NEW]**

- **Signal:** 16/2025. (V. 29.) NGM rendelet 'az automata bankjegykiado gepek 2025-ben kezdodo, gyorsitott telepitesevel kapcsolatos egyes kerdesekrol' sets the rollout schedule under Act XVIII of 2025, keyed to the 2022 census: an ATM had to be operating in every settlement above 1,000 inhabitants by 31/12/2025, and in every settlement above 500 inhabitants by 31/12/2026.
- **Source:** Nemzeti Jogszabalytar / Jogtar - 16/2025. (V. 29.) NGM rendelet - https://net.jogtar.hu/jogszabaly?docid=A2500016.NGM (29/05/2025, primary)
- **Implies:** A hard, dated ATM-placement deadline of 31/12/2026 - four months out. Every settlement in the 500-1,000 inhabitant band still needs a machine, cash replenishment, connectivity and monitoring. These are exactly the low-volume rural sites where a vendor-neutral managed-services / ATM-as-a-service model wins over in-house operation.
- **Likelihood:** High - statutory deadline inside the next two quarters | **Confidence:** Medium | **Opp size:** XL | **Win:** High | **Deadline:** 31/12/2026
- **Follow-up:** Obtain the official list of settlements in the 500-1,000 band still uncovered (MNB holds the notifications) and cross-match against the OTP/MBH/Erste locator feeds pulled this run to size the residual gap.

### 10. Magyar Nemzeti Bank (MNB) (Hungary) **[NEW]**

- **Signal:** 19/2025. (VI. 26.) MNB rendelet sets the criteria for siting the mandated ATMs and the statutory formula for sharing the cost between payment service providers, weighted: 30% cards issued with cash-withdrawal capability, 25% balance sheet total, 20% revenue from cash payment services, 15% non-zero household forint deposits, 10% consumer payment accounts held. Phase-1 contracting deadline was 20/07/2025 and phase-2 contracting deadline 28/02/2026, with notifications to the MNB by 31/07/2025 and 16/03/2026.
- **Source:** Nemzeti Jogszabalytar / Jogtar - 19/2025. (VI. 26.) MNB rendelet - https://net.jogtar.hu/jogszabaly?docid=A2500019.MNB (26/06/2025, primary)
- **Implies:** Hungary has legislated a cost-shared, effectively pooled rural ATM network - the same structural move the baseline flagged in Croatia and Czechia. A shared estate is normally procured centrally and run by one operator, which is the highest-value single opportunity shape for Printec (deploy + monitor + cash-manage a multi-bank fleet).
- **Likelihood:** High - phase-2 contracting deadline already passed 28/02/2026 | **Confidence:** Medium | **Opp size:** XL | **Win:** High
- **Follow-up:** Find who won the phase-1 and phase-2 contracts and whether the banks pooled procurement or each contracted separately. The MNB notification filings of 31/07/2025 and 16/03/2026 should name the operators.

### 11. MBH Bank (Hungary) **[NEW]**

- **Signal:** MBH's locator data still tags every point by predecessor brand: of its 1,285 fixed ATMs, 803 are legacy Takarekbank (TB), 383 legacy MKB and 99 legacy Budapest Bank (BB). Critically, NONE of the 803 Takarekbank-heritage machines accept cash deposits - all 256 deposit-capable ATMs come from the MKB (170) and Budapest Bank (86) estates. The three heritages also still run three different quick-withdrawal presets (TB 4,000/9,000/19,000...; MKB 5,000/10,000/20,000...; BB 1,000/20,000/40,000...), i.e. the ATM software/configuration estate is not yet harmonised.
- **Source:** MBH Bank branch & ATM locator API, point_predecessor / point_ATM_paying_type / point_quick_amount fields - https://www.mbhbank.hu/apps/backend/branch-and-atm (27/08/2026, primary)
- **Implies:** The sharpest-edged target in this cluster: 803 identified machines, one legacy brand, zero deposit capability, and an unharmonised software estate. That is simultaneously a recycler retrofit deal, a multivendor ATM-software consolidation deal and a managed-services deal - and MBH has to solve it while the Act XVIII coverage clock runs.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** XL | **Win:** High
- **Follow-up:** Confirm the hardware makes on the 803 TB-heritage sites (Takarekbank ran a very mixed rural estate) and whether MBH has an existing multivendor software contract. Re-pull the feed quarterly and watch the predecessor tags disappear - that marks the harmonisation programme starting.

### 12. OTP / MBH / Erste Hungary (combined) (Hungary) **[NEW]**

- **Signal:** Cross-matching the three banks' own locator feeds pulled 27/08/2026, their ATM estates between them cover 1,217 distinct settlements (OTP 764, MBH 779, Erste 276), but only 195 settlements have all three present - 368 settlements are served by OTP alone, 392 by MBH alone and 50 by Erste alone. (Analyst computation over the three primary feeds cited in the rows above.)
- **Source:** Computed from the OTP, MBH and Erste Bank Hungary locator APIs (all cited above) - https://www.mbhbank.hu/apps/backend/branch-and-atm (27/08/2026, primary)
- **Implies:** Rural Hungary is overwhelmingly a single-bank-per-village ATM market, which is precisely why the legislator wrote a cost-sharing decree rather than an each-bank-for-itself duty. It also means the residual 500-1,000-inhabitant settlements due by 31/12/2026 will be served by one shared machine, not four - a consolidated, operator-run fleet.
- **Likelihood:** Medium-High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **Deadline:** 31/12/2026
- **Follow-up:** Add K&H's estate once kh.hu is reachable, then subtract the union from the official settlement register to produce the definitive uncovered-settlement list.

### 13. OTP Bank / Intellect Design Arena (Hungary (group)) **[NEW]**

- **Signal:** Intellect Design Arena's own eMACH.ai product page lists OTP Bank among its customers. eMACH.ai is Intellect's Events-Microservices-API-Cloud-Headless architecture, marketed with ~2,000 open APIs and a headless/composable core. No implementation date, scope, entity or go-live is disclosed on the page, and Intellect's 2025-2026 newsroom items reachable this run named no Hungarian or CEE deployment.
- **Source:** Intellect Design Arena, eMACH.ai product page (customer list) - https://www.intellectdesign.com/emach-ai/ (27/08/2026, primary)
- **Implies:** If OTP is genuinely moving core/adjacent platforms onto a composable, API-first stack, the integration surface for channel and self-service software widens (headless means the ATM/kiosk front end is decoupled and separately procurable). Treat as an unconfirmed lead, not a programme.
- **Likelihood:** Low-Medium - vendor logo claim only | **Confidence:** Low | **Opp size:** Unscoped | **Win:** Low
- **Follow-up:** Escalate to an operator: ask Intellect IR / OTP whether any eMACH.ai module is live at OTP, in which entity and since when. Check Intellect's quarterly investor decks (Q1 FY27 was published in 2026) for a named CEE win.

### 14. Magyar Nemzeti Bank (MNB) (Hungary)

- **Signal:** MNB's Payment Systems Report of July 2025 (latest edition published - no 2026 edition exists on the MNB site as at 27/08/2026) records for 2024: over 2.5bn electronic payments, nearly 2bn card purchases (+10% y/y), POS terminals at merchant acceptance points +4.3%, online acceptance points +17.8% to nearly 60,000, and cash withdrawals DOWN 4% in number and almost HUF 600bn (-4.5%) in value. The cash-withdrawal transaction duty rose from 0.6% to 0.9% and the general transaction duty from 0.30% to 0.45% (cap doubled to HUF 20,000).
- **Source:** Magyar Nemzeti Bank, Fizetesi rendszer jelentes 2025 (July 2025) - https://www.mnb.hu/letoltes/mnb-fizetesi-rendszer-jelentes-2025-hun-digitalis-vegleges.pdf (31/07/2025, regulator)
- **Implies:** Cash withdrawal volume and value are falling while the state simultaneously mandates more ATMs - so the economics per machine worsen and the only way to hold the mandate is lower cost per site: recyclers that cut CIT runs, remote monitoring, and shared/outsourced operation. That is the whole Printec argument in one chart.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** M | **Win:** Medium
- **Follow-up:** Watch for the 2026 edition (the 2025 one came out in July); it will be the first to measure the Act XVIII fleet expansion against falling withdrawal volumes.

## Coverage notes

Fresh run, no checkpoint existed. WebSearch budget was already exhausted (200/200) when this task started, so ZERO keyword discovery was possible - every source below was reached by direct primary-source fetch, URL inference and API reverse-engineering from the banks' own front-end JavaScript. COVERED: (1) the statutory ATM mandate chain end-to-end - Act XVIII of 2025 plus BOTH implementing decrees (16/2025 NGM schedule and 19/2025 MNB cost-sharing formula), which is the material new find and carries a hard 31/12/2026 deadline; (2) OTP - H1-2026 report (05/08/2026) read from the PDF locally, plus a full locator pull with per-machine detail records (1,844 ATMs, cashDeposit flag on every one); (3) MBH - full machine-readable locator pull including the legacy-brand (point_predecessor) and deposit-capability fields; (4) Erste Bank Hungary - full GEM locations API pull for ATMs and branches; (5) K&H - via KBC Group's 2Q2026 primary disclosures only, because kh.hu is hard-blocked. GENUINE GAPS: (a) K&H's own ATM/branch estate - kh.hu returns Akamai 403 to every route including full browser headers, so no K&H locator or Hungarian-language disclosure could be opened; (b) MNB supervisory decisions and AML fines - the decision register hatarozatkereso.mnb.hu is behind a WAF that rejects all requests ('Request Rejected'), apps.mnb.hu is denied, and two MNB supervisory-news paths 404, so NO Hungarian AML fine could be verified this run and none is claimed; (c) MBH's H1-2026 report - the IR site renders client-side and its publications endpoint could not be located, so MBH financials are absent (the locator dataset substitutes and is arguably stronger for our purposes); (d) eMACH.ai at OTP is a vendor logo claim only, marked Low confidence; (e) no 2026 MNB Payment Systems Report exists yet, so the sector ATM/POS series is 2024-vintage. Every figure here was read from the source named in its row; nothing is carried forward from the baseline unverified. The baseline's Hungarian items were not re-derivable because the baseline never covered Hungary directly (OTP Group was one of the eight never-researched units).

## Access issues

WebSearch budget exhausted at start of run (200/200) - all discovery done by direct primary-source fetch, so no keyword discovery was possible. www.kh.hu returns HTTP 403 (Akamai 'Access Denied', ref #18.3f451502) to every route tried including full desktop browser headers - K&H's own site could not be opened this run; substituted KBC Group primary disclosure. www.mbhbank.hu/befektetoknek returned 403 to the fetch tool, recovered with a desktop User-Agent via curl. mnb.hu/felugyelet/hirek-aktualitasok/felugyeleti-hirek and /hirek both 404. html.duckduckgo.com served a CAPTCHA - not solved, not used.

## Operator requests

1) www.kh.hu - Akamai 403 from this environment (support ref #18.3f451502.1787820125). Need a Hungarian-IP browser session to pull K&H's fiokkereso ATM/branch estate and any K&H Hungarian-language disclosure. 2) hatarozatkereso.mnb.hu - the MNB supervisory-decision register is WAF-blocked ('Request Rejected'); apps.mnb.hu returns 'No Access - denied URL'. Claude-in-Chrome escalation was attempted but list_connected_browsers returned an empty list, so no browser was available. Need an operator to run the register for 2025-2026 enforcement decisions against hitelintezetek, filtering for penzmosas/AML, and to capture decision numbers, dates and HUF fine amounts. 3) MBH Bank H1-2026 report - the IR site is client-side rendered; need an operator to download the 2026 feleves jelentes PDF from mbhbank.hu/befektetoi/befektetoknek and the phase-1/phase-2 Act XVIII contracting filings. 4) Intellect Design Arena - confirm whether any eMACH.ai module is actually live at OTP Bank, in which entity and since when.
