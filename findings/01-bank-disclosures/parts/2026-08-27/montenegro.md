# Montenegro — bank disclosures, run 2026-08-27

**Status:** complete · **Signals:** 24 · Market was NEVER researched in the previous run — full sweep.

## Headline

- **CBCG Q1-2026 device census (07/05/2026): 664 ATMs, only 126 deposit-capable, 23,250 POS.** ~538 machines are cash-out only.

- **ATM deposit transactions +47% YoY** (Q1-2026 127,719 / EUR 42.7m) while withdrawals grew only 5% — demand outrunning a 126-machine estate.

- **EUR 709m of cash deposits still crossed the branch counter in Q1-2026 alone**, vs EUR 42.7m at ATMs (~6%).

- **Montenegro went live on TIPS Clone instant payments 20/07/2026** — the baseline only knew about Bosnia and Kosovo. All 11 banks live. Fee capped at 5 cents up to EUR 200 (17/07/2026 CBCG decision) explicitly to kill counter traffic.

- **Prva banka installed 17 multifunctional cash-in ATMs on 09/06/2026 and calls it 'the start of a broader transformation'** — highest-intent opportunity in the country.

- **CKB took cash off the counter at its Podgorica Business Point on 24/07/2026**, six-month transition ends ~24/01/2027.

- **Hipotekarna advertised a dedicated ATM specialist on 17/06/2026** whose remit explicitly includes vendor contracts and *planning ATM network expansion*.


## Published fleet reconciliation (bank locators vs CBCG)

| Bank | ATM locations | Deposit-capable | Branches |
|---|---|---|---|
| NLB Banka Podgorica | 153 | 29 | 20 |
| CKB (OTP) | 117 | 30 | ~25 |
| Prva banka CG | 109 | 17 (from 09/06/2026) | ~30 |
| Lovcen banka | 101 (78 Euronet-branded) | 0 | 18 |
| Erste Podgorica | 81 | 14 | 18 |
| Hipotekarna | 49 | 0 | 24 |
| Addiko | 20 | 12 | 13 |
| Universal Capital Bank | 7 | n/d | n/d |
| Adriatic Bank | 5 | 0 | 8 |
| **Total published** | **642** | **~102** | |
| *CBCG census 31/03/2026* | *664* | *126* | |

## Signals

### 1. Montenegro banking sector (all PSPs) — 07/05/2026 (L)
**Signal:** CBCG payment-device census: 664 ATMs in Montenegro at 31/03/2026, of which only 126 have a cash-DEPOSIT function and 620 are cash-withdrawal; 197 offer credit transfer. Deposit-capable ATMs were 106 at Q1-2025 and just 22 at Q1-2023. POS terminals 23,250 (from 19,405 at Q1-2025, +19.8% YoY). File updated 07/05/2026.

**Implies:** ~538 of 664 Montenegrin ATMs are cash-out-only. Direct addressable base for Printec cash recyclers / deposit-capable ATM upgrades and the managed services to run them.

**Source:** [Central Bank of Montenegro (CBCG) - Uredjaji za prihvatanje platnih kartica, Q1-2026 XLSX](https://www.cbcg.me/slike_i_fajlovi/fajlovi/fajlovi_platni_promet/usluge_e-novac/2026/broj_uredjaja_prihvatanje_platnih_kartica_q1-2026.zip) · tier=regulator · likelihood=High - deposit-capable count has grown every year since 2023; banks are actively converting · confidence=Medium · win=Medium · new=True

**Follow-up:** Pull the Q2-2026 file when CBCG publishes (~early Nov 2026) and split the 126 deposit ATMs by bank via each bank's locator.

### 2. Montenegro banking sector (all PSPs) — 07/05/2026 (L)
**Signal:** ATM cash-deposit transactions (domestic cards, domestic terminals) reached 127,719 worth EUR 42,689,944 in Q1-2026, up from 86,798 / EUR 28,851,907 in Q1-2025 (+47% by count, +48% by value). Full-year 2025 was 449,299 / EUR 169,240,750 vs 288,495 / EUR 113,884,868 in 2024. ATM cash withdrawals grew far slower (Q1-2026 2,012,703 / EUR 309,444,540 vs Q1-2025 1,916,327 / EUR 284,345,490, +5.0% by count).

**Implies:** Deposit demand is growing ~9x faster than withdrawal demand while being carried by only 126 machines - a capacity squeeze that recyclers (which net deposits against withdrawals and cut CIT runs) solve directly.

**Source:** [CBCG - Platne transakcije izvrsene platnim karticama po vrsti terminala, Q1-2026 XLSX](https://www.cbcg.me/slike_i_fajlovi/fajlovi/fajlovi_platni_promet/usluge_e-novac/2026/platne_transak_izvr_plat_kart_vrste_terminal_q1-2026.zip) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Model deposit-per-machine load (127,719 / 126 = ~1,014 deposits per machine per quarter) into a recycler ROI case per bank.

### 3. Montenegro banking sector (all PSPs) — 07/05/2026 (L)
**Signal:** Cash still overwhelmingly crosses the branch counter: Q1-2026 counter cash orders totalled 1,197,753 worth EUR 1,175,236,997 (deposits EUR 709,156,264 + withdrawals EUR 466,080,733). Against that, ATM cash deposits were only EUR 42.7m in the same quarter - roughly 6% of counter deposit value. Counter order volume is falling (1,197,753 in Q1-2026 vs 1,274,754 in Q1-2025, -6.0%; FY2025 5,478,745 vs FY2024 5,900,153).

**Implies:** Mirrors the quantified Bulgaria/UBB counter-vs-ATM gap. Teller cash recyclers (TCR) plus lobby deposit ATMs are the migration path; Printec cash automation plus managed services.

**Source:** [CBCG - Platne transakcije uplate i isplate gotovog novca, Q1-2026 XLSX](https://www.cbcg.me/slike_i_fajlovi/fajlovi/fajlovi_platni_promet/usluge_e-novac/2026/platne_transak_uplate_isplate_got_novca_q1-2026.zip) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Ask each bank for its own counter-vs-ATM deposit split to size TCR need per branch.

### 4. Central Bank of Montenegro (CBCG) — 20/07/2026 (L)
**Signal:** CBCG introduced EU instant payments into domestic payment traffic via the TIPS Clone system on 20 July 2026, in cooperation with Banca d'Italia, under ECB auspices and with World Bank support. CBCG has published bank-by-bank video guides and an FAQ for the new rails.

**Implies:** Same 20/07/2026 go-live already logged for Bosnia and Kosovo - Montenegro is the third TIPS Clone country and the baseline never saw it. Instant rails drive real-time fraud/transaction monitoring, AML screening and HSM refresh across all Montenegrin banks.

**Source:** [CBCG - Instant placanja (TIPS Clone)](https://www.cbcg.me/me/kljucne-funkcije/platni-promet/instant-placanja-tips-clone) · tier=regulator · likelihood=High - live now, bank-side hardening follows · confidence=Medium · win=Medium · new=True

**Follow-up:** Identify which of the 10 Montenegrin banks appear in the CBCG video-guide list (indicates who is already live) and target the laggards.

### 5. Montenegro banking sector (acquiring) — 07/05/2026 (M)
**Signal:** Foreign-issued cards at Montenegrin terminals generated 24,080,174 POS transactions worth EUR 951,222,774 in FY2025 and 3,040,799 worth EUR 95,739,405 in Q1-2026 alone; foreign-card ATM withdrawals added 1,035,488 transactions worth EUR 320,965,968 in FY2025.

**Implies:** Tourism-heavy inbound acquiring. Printec POS/acquiring, terminal estate management and DCC-capable ATM software have a clear seasonal-capacity story here.

**Source:** [CBCG - Platne transakcije izvrsene platnim karticama po vrsti terminala, Q1-2026 XLSX](https://www.cbcg.me/slike_i_fajlovi/fajlovi/fajlovi_platni_promet/usluge_e-novac/2026/platne_transak_izvr_plat_kart_vrste_terminal_q1-2026.zip) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Get Q3 seasonality: FY2025 foreign-card POS value peaked in Q3 (EUR 491.1m of the EUR 951.2m).

### 6. Montenegro banking sector (all PSPs) — 07/05/2026 (M)
**Signal:** The Montenegrin ATM fleet is strongly seasonal - 751 ATMs at 31/12/2025 and 737 at 30/09/2025 but only 664 at 31/03/2026; the same pattern recurs every year (623 at Q1-2025 vs 737 at Q3-2025).

**Implies:** ~90 machines are deployed and withdrawn each season - a managed-services / deploy-and-service annuity rather than a one-off hardware sale.

**Source:** [CBCG - Uredjaji za prihvatanje platnih kartica, Q1-2026 XLSX](https://www.cbcg.me/slike_i_fajlovi/fajlovi/fajlovi_platni_promet/usluge_e-novac/2026/broj_uredjaja_prihvatanje_platnih_kartica_q1-2026.zip) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Confirm which banks/ISOs run the seasonal coastal fleet.

### 7. Crnogorska komercijalna banka (CKB, OTP Group) — 27/08/2026 (L)
**Signal:** CKB's own published maps show 117 ATM locations nationwide but only 30 cash-in (deposit) locations - 25.6% of the fleet. Cash-in is concentrated in Podgorica (13 of 30). Branch map shows ~25 branches/sub-branches, 10 of them in Podgorica. CKB markets itself as 'the largest ATM network in the country'.

**Implies:** 87 CKB machines are cash-out-only at the country's largest deployer. Recycler/deposit-module retrofit is the single biggest addressable line in Montenegro; Printec cash automation plus ATM managed services.

**Source:** [CKB - Mapa bankomata / Mapa Cash-in bankomata / Mapa filijala (PDF, bank's own locator page)](https://www.ckb.me/upload/Mapa-Cash-in-bankomata-2.pdf.pdf) · tier=primary · likelihood=High - CKB is actively pushing counter-to-ATM deposit migration (see cash-in incentive campaign) · confidence=Medium · win=Medium · new=True

**Follow-up:** Confirm CKB's incumbent ATM vendor and service contract expiry; the full ATM map is at https://www.ckb.me/upload/Mapa-bankomata.pdf

### 8. Crnogorska komercijalna banka (CKB, OTP Group) — 24/07/2026 (L)
**Signal:** On 24/07/2026 CKB reopened its Podgorica 'Business Point' (Moskovska 2D) as a specialised micro/small-business centre in which CASH TRANSACTIONS ARE NO LONGER AVAILABLE AT THE COUNTER; non-cash transfers continue only through a six-month transition period. Clients are directed to ATMs for withdrawal and to cash-in devices for free deposit of daily takings ('pazar'), with a free cash-in card issued in branch.

**Implies:** A dated, concrete branch-cash-out template CKB can replicate across its ~25-branch network. Every converted branch needs at least one deposit-capable/recycling machine plus lobby self-service - core Printec cash automation and managed services.

**Source:** [CKB - 'Business Point ponovo otvoren u novom ruhu i sa novim konceptom'](https://www.ckb.me/opste/novosti-detalj?nid=723) · tier=primary · likelihood=High - the six-month transition period ends around 24/01/2027, a dated trigger · confidence=Medium · win=Medium · new=True

**Follow-up:** Ask CKB how many further branches are slated for the same conversion before the transition window closes.

### 9. Crnogorska komercijalna banka (CKB, OTP Group) — 27/08/2026 (M)
**Signal:** CKB ran a cash-in incentive campaign paying EUR 20 to the first 500 customers who made at least two ATM cash deposits and made NO counter deposit during the campaign, which ran to 23 July. The bank is explicitly paying customers to stop using the teller.

**Implies:** Confirms deposit-ATM capacity is the constraint CKB is managing. Demand-side push against a 30-location cash-in estate makes the recycler business case self-evident.

**Source:** [CKB - 'CKB cash-in bankomati'](https://www.ckb.me/gradjani/usluge/cash-in-bankomati) · tier=primary · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Confirm campaign year (page does not state it) and get post-campaign deposit-migration numbers.

### 10. Hipotekarna banka AD Podgorica — 17/06/2026 (M)
**Signal:** On 17/06/2026 Hipotekarna advertised a dedicated 'ATM specialist' post in its Payment Card Acceptance Service (EFTPOS, ATM and e-commerce), applications closing 23/06/2026. The job description explicitly covers configuring new and monitoring existing ATMs, tracking ATM installation and de-installation, managing the validity of contracts with landlords AND VENDORS, liaising with vendors and card schemes on new projects, certifications and mandates, and PARTICIPATING IN PLANNING THE EXPANSION OF THE ATM NETWORK.

**Implies:** A bank publicly staffing for ATM fleet expansion, vendor contract renewal and scheme certification/mandate work is the clearest possible buying signal for Printec ATM supply, EMV/scheme certification and ATM managed services (monitoring, availability SLA, cash control).

**Source:** [Hipotekarna banka - 'Oglas za posao - ATM specijalista u Sluzbi za prihvat platnih kartica (EFTPOS, ATM i ECOMMERCE)'](https://hipotekarnabanka.com/oglas-za-posao-atm-specijalista-u-sluzbi-za-prihvat-platnih-kartica-eftpos-atm-i-ecommerce/) · tier=primary · likelihood=High - hiring is a funded commitment · confidence=Medium · win=High · new=True

**Follow-up:** Approach Hipotekarna's Payment Card Acceptance Service directly; ask which vendor contracts are up for renewal.

### 11. Hipotekarna banka AD Podgorica — 16/06/2026 (M)
**Signal:** Hipotekarna relocated its Budva branch to Jadranski put 26 on 15/06/2026 and installed 'two modern Cash Out ATMs' there - explicitly withdrawal-only - while keeping its 24/7 self-service 'Zona' at Mediteranska 4 and machines at the Blue Star and Splendid hotels. It also relocated its Tivat branch (24/04/2026).

**Implies:** As late as mid-2026 Hipotekarna is still buying cash-OUT-only machines. Straight recycler/deposit-module upsell, and the '24/7 Zona' self-service lobby concept is a repeatable Printec build.

**Source:** [Hipotekarna banka - 'Filijala Budva na novoj lokaciji'](https://hipotekarnabanka.com/filijala-budva-na-novoj-lokaciji/) · tier=primary · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Confirm the make of the two new Budva machines.

### 12. Hipotekarna banka AD Podgorica — 27/08/2026 (M)
**Signal:** Hipotekarna's own locator feed returns 49 ATM locations and 24 branch/office locations (Podgorica 14 ATMs, Budva 5, Herceg Novi 4, Kotor 4). The feed exposes no cash-in/deposit attribute at all, consistent with a withdrawal-only estate. Machine-readable endpoint: https://hipotekarnabanka.com/wp-admin/admin-ajax.php?action=hb_business_locations_list&api_lang=sr_ME&api_ver=4.0.0 (proxies https://hbklik.me/hb-mw/cms).

**Implies:** Second-largest quantified fleet in Montenegro after CKB and apparently 100% cash-out. Pair with the ATM-specialist hire for a combined recycler + managed-services pitch.

**Source:** [Hipotekarna banka - business locations AJAX feed](https://hipotekarnabanka.com/filijale-i-bankomati/) · tier=primary · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Re-pull this feed each run; a changed count is itself the signal (same method as the Bulgaria locator counts).

### 13. Lovcen banka AD Podgorica — 16/06/2026 (M)
**Signal:** Lovcen banka's own ATM locator API (https://app-cms-api.lovcenbanka.me/v1/atms) returns 101 ATM locations against only 18 branches/counters. 78 of the 101 are EURONET-BRANDED machines, and they were loaded into the feed in a tight burst - 2 on 26/05/2026, 26 on 29/05/2026, 4 on 15/06/2026 and 46 on 16/06/2026. Only 23 carry Lovcen's own 'Bankomat <CITY>' naming. The estate is overwhelmingly coastal: Budva 32, Kotor 18, Bar 14, Podgorica 9.

**Implies:** Lovcen has scaled ATM reach in mid-2026 through an independent deployer (Euronet) rather than its own hardware - a competitive route Printec is bidding against, and a reason the CBCG sector ATM count keeps rising while deposit-capable share stays low (ISO fleets are typically cash-out only). Position Printec managed services as the alternative to an ISO deal, and note Lovcen has NO published deposit-capable machine.

**Source:** [Lovcen banka - ATM and branch locator API](https://www.lovcenbanka.me/stanovnistvo/lokacije) · tier=primary · likelihood=Medium - reading the feed as an owned/branded partnership needs confirmation; it may list acceptance partners · confidence=Medium · win=Low · new=True

**Follow-up:** Confirm with Lovcen whether the 78 Euronet machines are an outsourced own-fleet, a white-label deal or merely fee-free acceptance partners. This determines whether it is a lost deal or an open one.

### 14. Prva banka Crne Gore AD Podgorica — 09/06/2026 (L)
**Signal:** On 09/06/2026 Prva banka CG launched a Cash-In service, announcing it had INSTALLED 17 MULTIFUNCTIONAL (deposit-and-withdrawal) ATMs giving retail customers 24/7 deposit to current, foreign-currency and savings accounts with immediate crediting, for all its Mastercard and Visa debit and credit cards. Vinka Nenezic, Director of the Digital Transformation Sector, is quoted saying 'this phase represents the START OF A BROADER TRANSFORMATION we plan in the coming period'. The 17 sites are named (15 in branches): Podgorica x4, Niksic, Cetinje, Budva x2, Kotor x2, Tivat, Bar, Ulcinj, Bijelo Polje, Berane, Rozaje, Pljevlja.

**Implies:** An explicitly PHASE-ONE deposit-ATM rollout at a bank that has just proved the business case internally. Phase two is stated bank policy, not speculation - the single highest-intent recycler/deposit-ATM opportunity found in Montenegro this run. Also a services and monitoring annuity.

**Source:** [Prva banka CG - 'Prva banka CG od danas omogucava i uplatu novca direktno na bankomatima'](https://www.prvabankacg.com/saopstenja_detalji.php?id=244) · tier=primary · likelihood=High - bank states further phases are planned · confidence=Medium · win=High · new=True

**Follow-up:** Contact Vinka Nenezic (Sektor za digitalnu transformaciju) for phase-two scope and the incumbent supplier of the first 17 machines.

### 15. Prva banka Crne Gore AD Podgorica — 27/08/2026 (M)
**Signal:** Prva banka's business-network page publishes 109 distinct ATM locations and roughly 30 branches/counters. Against the 17 cash-in machines announced 09/06/2026, that leaves about 92 cash-out-only machines (~84% of the fleet). Its estate is unusually retail-partner heavy - machines sit in IDEA markets, souvenir shops, bus stations, the Debeli Brijeg border crossing and a Perast car park.

**Implies:** Large off-premise fleet with heavy seasonal/tourist exposure - a natural fit for Printec ATM managed services (availability SLA, cash forecasting, CIT coordination) alongside the deposit-ATM phase two.

**Source:** [Prva banka CG - Poslovna mreza (Bankomati tab)](https://www.prvabankacg.com/poslovna_mreza.php) · tier=primary · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Re-pull this page each run to track how fast the 17 cash-in machines grow.

### 16. NLB Banka AD Podgorica — 27/08/2026 (L)
**Signal:** NLB Montenegro's own locator API returns 153 ATM locations - the largest published fleet in the country - against only 20 branches/counters. Only 29 of the 153 carry the service flag 'Uplata EUR' (EUR cash deposit); the other 124 (81%) are cash-out only. Deposit capability is concentrated in Podgorica (12 of 29). The bank also still publishes 11 DAY/NIGHT SAFES (dnevno-nocni trezori) as a separate location type. Endpoint: https://www.nlb.me/content/nlbbanks/nlbme/sr_me/stanovnistvo/lokacije/jcr:content/root/container/container/branchsearch.facilities.json?kind=atm

**Implies:** Biggest single recycler white space in Montenegro (124 machines) at a bank running only 20 branches - the ATM IS the network. The 11 surviving day/night safes are manual overnight cash drops that a smart safe / deposit recycler replaces outright; that is a self-contained, easily quantified Printec pitch.

**Source:** [NLB Banka Podgorica - branch/ATM facilities API](https://www.nlb.me/stanovnistvo/lokacije) · tier=primary · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Cross-check NLB Group's H1-2026 disclosure for a Montenegro ATM/branch figure and reconcile against these 153/20 counts.

### 17. Erste Bank AD Podgorica — 27/08/2026 (M)
**Signal:** Erste Montenegro's locator API publishes 81 ATM records and 18 branches. Feature tagging shows 69 withdrawal-only ATMs, only 14 unique 'uplatno-isplatni' (deposit-and-withdrawal) sites, 7 day/night-safe sites, and a distinct named service 'ERSTE SMART CASH' present at 11 unique sites (Podgorica x3, Bar x2, Rozaje, Pljevlja, Budva, Ulcinj, Bijelo Polje, Niksic). Endpoint: https://www.erstebank.me/bin/erstegroup/gemesgapi/locations/gem_site_location_locations-me-ebmn?types=ATM&items=500&page=0

**Implies:** Mirrors the Erste Croatia pattern already logged (666 ATMs / 199 deposit-capable at 31/07/2026): the group deploys deposit capability sparingly. 'Erste Smart Cash' is a discrete branded self-service cash concept at only 11 sites - a rollout in progress, and the reference design Printec should be quoted against for the remaining branches.

**Source:** [Erste Bank Podgorica - GEM locations API and me-locations-features.json](https://www.erstebank.me/sr_ME/stanovnistvo/Alati/filijale-i-bankomati) · tier=primary · likelihood=Medium · confidence=Medium · win=Medium · new=True

**Follow-up:** Establish exactly what 'Erste Smart Cash' hardware is and who supplies it; that determines whether this is an incumbency to displace or a template to extend.

### 18. Addiko Bank AD Podgorica — 27/08/2026 (S)
**Signal:** Addiko Montenegro publishes 13 branches/counters and 20 ATM locations, of which 12 are deposit-and-withdrawal ('uplatno-isplatni') - 7 branded 'Zona 24/7' (Podgorica, Budva, Niksic, Herceg Novi/Sutorina, Bijelo Polje, Pljevlja, Bar) plus 5 more on restricted hours. The machines accept COINS as well as notes (up to 150 banknotes per transaction) and support SME daily-takings ('pazar') deposit with a date and organisational-unit tag, via a dedicated Addiko Business Debit Mastercard. Page last modified 27/08/2026.

**Implies:** At ~60% deposit-capable Addiko has by far the highest deposit share of any Montenegrin bank and is the market's reference build for SME cash-in (coin handling plus OJ tagging). Use it as the benchmark spec when quoting CKB, NLB, Hipotekarna and Prva - and note the 'Zona 24/7' branding shows self-service lobbies are already an accepted format here.

**Source:** [Addiko Bank Crna Gora - 'Uplatno-isplatni bankomati - Zona 24/7' and 'Ekspoziture i bankomati'](https://www.addiko.me/uplatno-isplatni-bankomati-zona-24-7/) · tier=primary · likelihood=High · confidence=Medium · win=Low · new=True

**Follow-up:** Identify the vendor behind Addiko's coin-and-note deposit machines - that is the incumbent Printec must beat on every other Montenegrin deal.

### 19. Central Bank of Montenegro (CBCG) — 17/07/2026 (L)
**Signal:** On 17/07/2026 the CBCG Council adopted a Decision capping the fee on domestic instant credit transfers: a maximum of 5 CENTS on instant payments up to EUR 200 made through mobile or internet banking (and the same cap on receiving), against a current average fee of 32 cents. CBCG states the explicit purpose is to push users off paper orders and COUNTER SERVICES onto electronic channels, estimating annual savings of about EUR 1m now rising to EUR 2.8m. The per-transaction ceiling is EUR 3,000, which CBCG says covers nearly 80% of all transactions.

**Implies:** A regulator-imposed price floor that makes teller-initiated payments structurally uneconomic. Every Montenegrin bank now has a costed reason to move counter traffic to self-service and digital - the demand driver behind the recycler, kiosk and eKYC lines. It also forces real-time fraud/AML screening at instant speed.

**Source:** [CBCG - 'Zaokruzen regulatorni okvir za pocetak instant placanja u Crnoj Gori...'](https://www.cbcg.me/me/javnost-rada/aktuelno/saopstenja/zaokruzen-regulatorni-okvir-za-pocetak-instant-placanja-u-crnoj-gori-od-20-jula-placanja-za-nekoliko-sekundi-do-200-eura-za-najvise-5-centi?id=3087) · tier=regulator · likelihood=High - in force · confidence=Medium · win=Medium · new=True

**Follow-up:** Track whether banks respond with branch-format changes (CKB's Business Point is the first visible case).

### 20. Montenegrin banking sector (11 credit institutions) — 27/08/2026 (M)
**Signal:** CBCG's TIPS Clone page publishes bank-by-bank instant-payment video guides covering ALL ELEVEN Montenegrin banks: Addiko, Adriatic, CKB, Erste, Hipotekarna, Lovcen, NLB, Prva banka, Universal Capital Bank, Zapad banka and Ziraat Bank Montenegro. Every one was live at or shortly after the 20/07/2026 go-live.

**Implies:** A complete, verified target list for instant-payments-driven work: real-time transaction monitoring, sanctions/AML screening at instant speed, HSM refresh and 24/7 managed services. Nobody is a laggard on connectivity, so the sell is on the risk and operations layer, not the rails.

**Source:** [CBCG - 'Video uputstva banaka' (Instant placanja / TIPS Clone)](https://www.cbcg.me/me/kljucne-funkcije/platni-promet/instant-placanja-tips-clone/video-uputstva-banaka) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Ask each of the eleven what real-time screening they put behind TIPS Clone and whether it was built or bought.

### 21. Montenegrin banking sector (all banks) — 27/08/2026 (XL)
**Signal:** Bottom-up reconciliation of every Montenegrin bank's own published locator against the CBCG census: NLB 153, CKB 117, Prva banka 109, Lovcen 101 (78 of them Euronet-branded), Erste 81, Hipotekarna 49, Addiko 20, Universal Capital Bank 7, Adriatic Bank 5 = 642 published ATM locations, against CBCG's 664 ATMs at 31/03/2026. Published deposit-capable machines total roughly 102 (NLB 29, CKB 30, Prva 17 from 09/06/2026, Erste 14, Addiko 12) versus CBCG's 126 at Q1-2026. Branch/counter totals: Prva ~30, CKB ~25, NLB 20, Hipotekarna 24, Erste 18, Lovcen 18, Addiko 13, Adriatic 8.

**Implies:** The country-level fleet figure reconciles to within ~3% of the bottom-up bank count - so the ~540 cash-out-only machine estimate is robust, not an artefact. It also shows the recycler gap is concentrated: NLB (124 cash-out-only) + CKB (87) + Prva (92) + Erste (67) + Hipotekarna (49) account for essentially all of it.

**Source:** [Own reconciliation of CBCG Q1-2026 device census against nine banks' published locators](https://www.cbcg.me/me/kljucne-funkcije/platni-promet/statistika-platnog-prometa/podaci-o-platnim-uslugama-i-elektronskom-novcu) · tier=primary · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Rebuild this table every run from the same nine endpoints; deltas are the leading indicator for Montenegro.

### 22. Central Bank of Montenegro (CBCG) — 02/06/2026 (L)
**Signal:** CBCG's 2025 Annual Report (adopted by the Council 02/06/2026) records that Montenegro joined SEPA with first transactions on 07/10/2025, delivering estimated savings of about EUR 4.8m in the first seven months; total banking-sector assets exceeded EUR 7.9bn, loans grew 14.24% and NPLs fell to a record-low 2.67%. CBCG's contribution allowed the provisional closing of EU accession Chapter 4 (free movement of capital), with Montenegro targeting the close of accession negotiations by end-2026.

**Implies:** SEPA (Oct-2025) then TIPS Clone (Jul-2026) then euro-convergence preparation is a three-stage payments-infrastructure programme with EU-accession deadlines attached. Each stage forces bank-side scheme certification, message-format migration, HSM and AML-screening work - a multi-year Printec compliance and security pipeline, and the same sequence Bulgaria has just been through.

**Source:** [CBCG - 'Savjet CBCG usvojio Izvjestaj o radu 2025...'](https://www.cbcg.me/me/javnost-rada/aktuelno/saopstenja/savjet-cbcg-usvojio-izvjestaj-o-radu-2025-godinu-obiljezili-evropsko-uskladjivanje-sepa-i-stabilnost-bankarskog-sektora?id=3056) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Watch for a dated euro-convergence roadmap; if Montenegro (already euroised unilaterally) formalises a path, it triggers exactly the note-recycler and cash-handling refresh cycle seen in Bulgaria and Croatia.

### 23. Montenegrin banking sector (macro backdrop) — 31/07/2026 (M)
**Signal:** CBCG Bulletin 7/2026 (June 2026 data) reports bank balance-sheet total +8.61% year on year, total capital +14.21%, loans +12.35%, total deposits +6.02% and RETAIL deposits +13.45% year on year. Tourism in January-June 2026 grew: arrivals +5.71%, overnight stays +6.47%, foreign arrivals +6.18%. Employment rose 4.67% year on year.

**Implies:** Retail deposits growing at double the rate of total deposits, on a tourism season up ~6%, means more physical cash reaching branches and coastal ATMs precisely where deposit capability is thinnest. Underwrites the recycler and seasonal managed-services case with an official, dated growth number.

**Source:** [CBCG - Bilten 7/2026](https://www.cbcg.me/slike_i_fajlovi/fajlovi/fajlovi_publikacije/biltencbcg/2026/bilten_7-2026.pdf) · tier=regulator · likelihood=High · confidence=Medium · win=Medium · new=True

**Follow-up:** Pull Bilten 8/2026 and 9/2026 for the peak-season months.

### 24. Adriatic Bank AD Podgorica — 27/08/2026 (S)
**Signal:** Adriatic Bank publishes only 8 offices (HQ Podgorica, Budva, Bar, plus Porto Montenegro Tivat, Lustica Bay Tivat, Boka Place Tivat and Portonovi) and 5 standalone ATMs (Lustica, Ulcinj, Bijelo Polje, Risan, Budva). Its network sits almost entirely inside high-end coastal resort developments.

**Implies:** Too small for a cash-automation play, but its resort/non-resident client base makes it a candidate for digital onboarding/eKYC and enhanced AML and transaction monitoring - the compliance side of the Printec catalogue rather than the hardware side.

**Source:** [Adriatic Bank - 'Filijale i ATM'](https://adriaticbank.com/me/filijale-atm) · tier=primary · likelihood=Medium · confidence=Medium · win=Low · new=True

**Follow-up:** Check CBCG AML supervision findings for banks serving non-resident/resort clients.


## Coverage notes
Full sweep completed for Montenegro - the market was NEVER researched in the previous run, so everything here is new ground. Primary regulator layer: CBCG quarterly payment-device and payment-transaction XLSX files (Q1-2026, published 07/05/2026) downloaded and parsed in full; CBCG Bulletin 7/2026 PDF text-extracted; CBCG press releases and the TIPS Clone pages read directly. Bank layer: nine of the eleven Montenegrin banks quantified from their OWN published sources - CKB (three locator PDFs plus press), NLB (AEM facilities.json API, with per-machine deposit service flags), Erste (Erste Group GEM locations API, with per-machine feature flags), Hipotekarna (WordPress REST posts plus a business-locations AJAX feed proxying hbklik.me), Lovcen (app-cms-api.lovcenbanka.me/v1/atms and /branches, with created_at timestamps), Prva banka (poslovna_mreza.php plus dated press releases), Addiko, Universal Capital Bank and Adriatic Bank (rendered locator pages). Zapad banka and Ziraat Bank Montenegro were checked but publish no usable ATM inventory - both are confirmed TIPS Clone participants and are genuine gaps on fleet data. Four machine-readable endpoints are now captured and should be re-pulled every run as a Bulgaria-style locator tracker: NLB, Erste, Hipotekarna and Lovcen. Genuine gaps: (1) no bank published an H1-2026 management report with ATM/branch/employee counts - CKB's newest interim disclosure (10/08/2026) is a Pillar 3 capital document only; (2) no vendor is named anywhere in Montenegrin bank disclosures, so no incumbency was established; (3) what 'Erste Smart Cash' physically is remains unresolved; (4) whether Lovcen's 78 Euronet-branded ATMs are an outsourced own-fleet or merely fee-free acceptance partners is unconfirmed and materially changes that signal; (5) Zapad banka and Ziraat fleet sizes.

## Access issues
WebSearch budget for this session was exhausted (200/200 calls) before a single Montenegro query could run, so NO keyword search was possible - the entire sweep was done by direct curl with a desktop User-Agent against primary domains, plus API/endpoint discovery from each site's own JavaScript. This is a coverage risk: local-language press (Vijesti, Pobjeda, Dan, Bankar.me) was NOT searched at all this run. www.cbcg.me and www.ckb.me both fail TLS chain verification through the fetch tool (curl -k required). cbcg.me returns its 404 page for /sitemap.xml and /robots.txt and its navigation is not reachable by ordinary link-following, so section URLs had to be recovered from raw href scraping of the search page. BLOCKED/UNREAD: https://www.ckb.me/upload/Konsolidovani-finansijski-izvjestaji-2025.pdf - 151 pages, 8.5MB, a pure SCANNED image with no text layer; pdfminer returned 151 characters. Not read; would need OCR. Erste Montenegro's site search API (https://www.erstebank.me/bin/erstegroup/gemesgapi/quick/gem_site_me_www-erstebank-me-me-es7) returns the same unfiltered 1,867-item result set for every query, so the Erste news feed could not be mined. https://www.zapadbanka.me/me/filijale returns 404.

## Operator requests
1) OCR of CKB's 2025 consolidated financial statements (https://www.ckb.me/upload/Konsolidovani-finansijski-izvjestaji-2025.pdf, 151 scanned pages) - the only place a CKB ATM/branch/employee count and IT/intangibles capex line is likely to be stated. 2) A WebSearch-enabled pass over Montenegrin press (Vijesti, Pobjeda, Dan, Bankar.me, CdM) for Q2/H1-2026 bank results and any ATM/self-service tenders - this run had zero search capability. 3) Raise CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION before the next Montenegro run.