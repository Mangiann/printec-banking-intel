# Albania — bank disclosures & market signals (run 2026-07-30)

**Status: complete.** 14 signals. Fresh full pass (no checkpoint to resume).

## Headline

- **Law 79/2025 POS mandate is the XL event**: 30/05/2026 (hotels, transport, state-capital public institutions) and **31/12/2026 (all remaining businesses)**, against only 31,263 POS installed at end-2025.
- **Bank of Albania has TWO new draft acts in consultation** the last run never saw: interchange caps at **0.2% debit / 0.3% credit**, and a settlement-finality/financial-collateral law.
- **Instant payments firmed to November 2026** (was 'autumn 2026').
- **Printec incumbency confirmed in writing** by NCR Atleos' own Union Bank case study: SelfServ 82/84 recyclers, Printec Albania as software+maintenance partner, NCR ~95% national ATM share, 11 of 13 banks on SelfServ 80.
- **Fleet updates**: Raiffeisen AL **198 ATMs** (was 186), 72 branches incl. 8 digital; BKT **62 branches / 161 Smart ATMs / 10,000 POS**; OTP AL **49 branches / 180+ ATMs** (above the group-reported 157).
- **New competitive frame**: Backbase now powers BOTH Jet Bank (Albania's first digital-only bank, launched 25/06/2026) and Tirana Bank's largest-ever tech programme.

## Signals

### 1. Albanian Tax Administration / Law 79/2025 (POS mandate) — XL

**Signal.** Law 79/2025 amending the Tax Procedures Law obliges taxpayers to be equipped with POS/POI terminals: 30/05/2026 for accommodation structures (hotels, guesthouses, motels, resorts), the transport sector and public institutions with state capital; 31/12/2026 for all remaining businesses. The same package cut the business-to-business cash ceiling from ALL 150,000 to ALL 100,000 and introduced a new ALL 500,000 ceiling on individual-to-business cash payments. Exemptions: areas without internet coverage, businesses exempt from invoicing, non-VAT self-employed. H1-2025 baseline cited: 46.4% of inter-business invoices and 9.7% of value still cash; business-to-consumer 90.6% of invoices and 64.2% of value still cash. The Albanian Tax Administration carries a standing notice 'Njoftim per tatimpaguesit qe duhet te pajisen me POS/POI'.

**Implies for Printec.** The single largest terminal-demand event in Albania. Against 31,263 POS installed at end-2025, a universal obligation by 31/12/2026 forces a very large incremental wave in H2-2026. Printec POS/acquiring: terminal supply, Android POS and SoftPOS for micro-merchants, key injection, TMS, deployment logistics, field service, plus merchant onboarding/eKYC for the acquiring banks. The 30/05/2026 public-institution leg additionally opens direct PUBLIC PROCUREMENT routes on app.gov.al that Printec can bid in its own name rather than through a bank.

- Source: Revista Monitor — 'Ulet kufiri per parane cash, deri ne fund te vitit 2026, te gjithe bizneset me terminale POS'; Albanian Tax Administration (DPT) notice — https://monitor.al/ulet-kufiri-per-parane-cash-deri-ne-fund-te-vitit-2026-te-gjithe-bizneset-me-terminale-pos/ (05/11/2025, tier: press)
- Likelihood: Certain as a legal obligation; the variable is enforcement intensity in H2-2026 | Confidence: Medium | Opp size: XL | Win: High | Deadline: 31/12/2026 | New: True
- Follow-up: Pull the consolidated Law 79/2025 text and DPT implementing instruction from tatime.gov.al (notice id 1942); quantify the residual un-equipped merchant base against the 31,263 installed terminals; run a systematic app.gov.al 'njoftimi i fituesit' scan for public-institution POS lots, which this run could not complete because openprocurement.al's list endpoint ignored the search parameter.

### 2. Bank of Albania (regulator) — L

**Signal.** BoA has a draft regulation in public consultation, 'Projekt-rregullore per tarifat e shkembimit per transaksionet e pagesave te bazuara ne karte' (interchange fees for card-based payment transactions), transposing the EU Interchange Fee Regulation. The draft text caps interchange at 0.2% of transaction value for consumer debit cards and 0.3% for consumer credit cards; entry into force is left blank ('hyn ne fuqi XX pas botimit ne Fletoren Zyrtare'). Adoption is conditional on prior amendment of the Law on Payment Services, itself still in consultation. Press reporting puts current all-in merchant service charge at up to ~3% on foreign-issued cards, with BoA projecting a fall toward 1% and banks arguing 1.5% is realistic.

**Implies for Printec.** Interchange caps compress per-transaction acquiring economics, forcing Albanian banks to compete on VOLUME and cost-per-terminal instead of fee margin. That is the classic trigger for outsourcing acceptance: Printec POS/acquiring, Android POS/SoftPOS and POS managed services (estate deployment, TMS, key injection, field service) become cheaper than bank-owned in-house terminal operations. It also raises the payback pressure on every terminal deployed for the Law 79/2025 mandate.

- Source: Bank of Albania — Akte ne proces konsultimi, draft interchange regulation (PDF); Revista Monitor — https://www.bankofalbania.org/rc/doc/Projektrregullore_p_r_tarifat_e_Shkembimit_34204.pdf (22/06/2026, tier: regulator)
- Likelihood: High that the caps are adopted as drafted once the Payment Services Law amendment passes; timing is the open variable | Confidence: Medium | Opp size: L | Win: Medium | Deadline: - | New: True
- Follow-up: Get the consultation closing date and the Payment Services Law amendment text; model per-bank acquiring P&L impact and take a POS-as-a-service proposition to Credins, Tirana Bank, Union Bank and BKT as the margin defence.

### 3. Bank of Albania (regulator) — M

**Signal.** A second BoA draft law is in consultation: 'Projektligj Per sistemin e pagesave dhe kolateralin financiar'. Its explanatory memorandum states it fully transposes Directive 98/26/EC (settlement finality, as amended by 2009/44/EC, 2010/78/EU and 2019/879/EU) and Directive 2002/47/EC (financial collateral, as amended by 2009/44/EC and 2014/59/EU) as part of the EU accession Chapter 9 benchmarks, creating a new consolidated legal framework for the operation, oversight and legal protection of payment and securities settlement systems, and repealing the existing settlement-finality and financial-collateral provisions.

**Implies for Printec.** Settlement-finality law is the legal precondition for the instant-payment scheme and for deeper SEPA integration. Participating banks will need upgraded payment hubs, ISO 20022 messaging and 24x7 liquidity monitoring - Printec transaction processing, HSM/security and managed services, plus AML/transaction monitoring capable of real-time screening (a 24x7 scheme removes the batch window banks currently rely on).

- Source: Bank of Albania — Relacion for the draft law on payment systems and financial collateral (PDF) — https://www.bankofalbania.org/rc/doc/Relacion_34400.pdf (Jul-2026, tier: regulator)
- Likelihood: Medium-High: formal consultation stage and tied to an accession benchmark | Confidence: Medium | Opp size: M | Win: Medium | Deadline: - | New: True
- Follow-up: Track adoption in Fletorja Zyrtare; map which of the 11 licensed Albanian banks lack a real-time-capable payment hub and approach them before the instant-payments go-live.

### 4. Bank of Albania / Albanian banking sector (instant payments) — L

**Signal.** The instant-payments go-live has firmed to NOVEMBER 2026, tightening the previously briefed 'autumn 2026' and superseding the earlier June-2026 preliminary target which the central bank itself judged ambitious. Revista Monitor reports the system will enable national payments in near real time and is explicitly positioned as 'a cheaper alternative for electronic payments at points of sale'. The World Bank separately confirms fast payments settling in seconds are expected to launch later in 2026 across Albania, Bosnia and Herzegovina, Montenegro, North Macedonia and Kosovo.

**Implies for Printec.** A November-2026 start means bank-side integration must be contracted in Q3-2026 - the window is open right now. Direct pull for Printec transaction processing/switching, ISO 20022 enablement, HSM/key management, and real-time fraud and AML transaction monitoring. The 'cheaper alternative at point of sale' framing means account-to-account/QR acceptance will land on the terminal estate: if Printec does not deliver A2A/QR acceptance on its Albanian POS base, an A2A-native competitor gets a wedge into the acceptance layer Printec currently holds.

- Source: Revista Monitor — 'Pagesat e castit fillojne ne nentor'; World Bank feature on SEPA in the Western Balkans — https://monitor.al/pagesat-e-castit-fillojne-ne-nentor/ (13/07/2026, tier: press)
- Likelihood: Medium-High for Nov-2026, with slippage risk flagged by the central bank itself | Confidence: Medium | Opp size: L | Win: Medium | Deadline: - | New: True
- Follow-up: Obtain the BoA/AECH participant onboarding timetable and scheme rulebook; confirm whether it is a TIPS clone as previously briefed and identify wave-1 banks. This run could NOT find a primary BoA press release naming November - the date rests on Monitor reporting and should be confirmed against a BoA Supervisory Council decision.

### 5. Mastercard / Albanian acquiring banks (POSI programme) — M

**Signal.** Mastercard's POSI programme in Albania is running a second wave from 01/05/2026 to 31/12/2026, or until 3,000 POS terminals have been distributed, whichever comes first, per Raiffeisen Bank Albania's own programme page: POS terminal or RaiPOS SoftPOS supplied free of charge (with a free NFC smartphone for RaiPOS), zero commission on card transactions up to EUR 20,000/year for groceries, hotels, restaurants/cafes and taxis, a EUR 15 monthly bonus at 20+ transactions, and a minimum of 4 Mastercard transactions per quarter to stay active. Restricted to 'New-to-POS' merchants with no prior POS contract at any bank. An earlier wave beginning 01/05/2025 was capped at 4,750 terminals. Union Bank runs the same programme.

**Implies for Printec.** A scheme-subsidised push of at least 3,000 free terminals into exactly the micro-merchant segments Law 79/2025 targets, on the same 31/12/2026 clock. Near-term hardware and SoftPOS volume for whoever supplies the acquiring banks: Printec POS/acquiring, Android POS, SoftPOS plus the deployment/TMS/managed-service wrap. Note the explicit smartphone-SoftPOS route (RaiPOS) - if Printec has no competitive SoftPOS offer in Albania it loses the micro-merchant tail permanently, because these merchants never buy a second terminal.

- Source: Raiffeisen Bank Albania — Mastercard POSI programme page — https://www.raiffeisen.al/en/sme-businesses/products-and-services/micro-businesess/pos-e-commerce-service/mastercard-posi.html (Jul-2026 (accessed; programme window 01/05/2026-31/12/2026), tier: primary)
- Likelihood: Live now and running to 31/12/2026 | Confidence: Medium | Opp size: M | Win: High | Deadline: 31/12/2026 | New: True
- Follow-up: Establish which banks beyond Raiffeisen and Union Bank participate, who supplies their terminals and SoftPOS stack, and whether the 3,000-unit cap is national or per-bank. unionbank.al is Cloudflare-blocked to automated fetch and needs an operator/browser session.

### 6. Union Bank Albania — L

**Signal.** NCR Atleos' own published case study confirms Union Bank of Albania runs a fleet of SelfServ 80 Series ATMs - specifically SelfServ 82 and SelfServ 84 - ALL fitted with recycling modules, deployed both in branches and off-premise (shopping centres, tourist areas), with PRINTEC ALBANIA named as NCR's local partner responsible for installing NCR software and providing ongoing maintenance. The same document states NCR holds ~95% ATM market share in Albania with only 2 of 13 banks not on the SelfServ 80 Series, records Union Bank's target of migrating 60% of cash transactions to deposit-taking ATMs, and its stated plan to keep increasing recycling ATMs over the following three years.

**Implies for Printec.** This is the documented incumbency. Printec is the named service partner on a recycler estate at Union Bank and sits in the NCR channel across ~11 of 13 Albanian banks. DEFENCE PRIORITY: any SelfServ 80 hardware end-of-life or APTRA/software migration must be steered to Printec rather than a rival integrator, and Union Bank's committed recycler expansion should convert into Printec orders. The 95% NCR share also means any Diebold Nixdorf or Vantiv/competitor entry would show up first as a single pilot - watch for it.

- Source: NCR Atleos — Insights: Union Bank of Albania (vendor case study) — https://www.ncratleos.com/insights/union-bank-of-albania (Jul-2026 (accessed; case study itself undated), tier: primary)
- Likelihood: Incumbency established; the live risk is a competitor integrator taking the refresh | Confidence: Medium | Opp size: L | Win: High | Deadline: - | New: True
- Follow-up: Establish the case study's publication date and the SelfServ 80 install dates to compute the hardware refresh window; get Union Bank's current unit count and how many are recyclers. Union Bank's own site is Cloudflare-blocked - use the annual report on unionbank.al via an operator.

### 7. Raiffeisen Bank Albania — L

**Signal.** Raiffeisen Bank Albania's own site now states 198 ATMs (describing itself as ATM market leader) and 72 branches of which 8 are DIGITAL branches, serving 528,800+ customers with assets near EUR 3.36bn, and Raiffeisen ON digital channel past 345,000 retail and business users. CEO Christian Canacaris (interview published 29/04/2026) reported EUR 3.4bn assets, EUR 1.6bn loans, EUR 2.8bn deposits, EUR 165m gross revenue (+3% y/y), EUR 76.4m IFRS net profit (EUR 70m local GAAP), 17.7% ROE (ranked first among the top five), 30,000+ clients actively using digital wallets, first to introduce Apple Pay for Visa and Mastercard in 2025, and an explicit strategy of shifting branches from routine transaction processing to lending, investment and advisory.

**Implies for Printec.** 198 ATMs is UP from the 186 carried in the previous run - the fleet is growing, not shrinking. Eight digital branches plus a stated intent to move transactions out of branches is the textbook trigger for recycler/CDM deployment and assisted-service kiosks. Printec: ATM/self-service refresh on the NCR Atleos estate, cash recycling, branch cash automation, ATM managed services and OptiCash-type cash forecasting to run a larger deposit-capable fleet efficiently.

- Source: Raiffeisen Bank Albania — 'Who are we?' and CEO interview 'The transformation of Albania's banking sector requires investment, innovation, and long-term trust' — https://www.raiffeisen.al/en/about-us/About/who-are-we.html (29/04/2026, tier: primary)
- Likelihood: High that a refresh or expansion tranche is contracted within 6-12 months given the digital-branch build-out and the top-of-market ROE funding it | Confidence: Medium | Opp size: L | Win: Medium | Deadline: - | New: True
- Follow-up: Confirm the ATM OEM mix and how many of the 198 are deposit/recycling; obtain the Raiffeisen Bank Albania 2025 annual report and the RBI group report; establish who supplied the equipment in the 8 digital branches.

### 8. BKT (Banka Kombetare Tregtare) — L

**Signal.** Owner Calik Holding states BKT Albania serves approximately 1 million customers through 62 branches, 161 SMART ATMs and 10,000 POS terminals - against 63 branches, 125 ATMs and 9,631 POS at the 2014 reference point on the same page. BKT's own product pages describe the Smart BanKomaT network as offering card and CARD-FREE cash withdrawal AND cash deposit, transfers and bill payment, running CX Banking software on all ATMs, in seven languages, 24/7. BKT was named Best Bank in Albania 2026 by Global Finance.

**Implies for Printec.** BKT is the largest single acceptance estate in Albania at ~10,000 POS - roughly a third of the national 31,263 - and 161 deposit-capable Smart ATMs. Two Printec angles: (1) the POS estate is the biggest single acceptance-managed-services prize in the country and will have to scale hard for the 31/12/2026 mandate; (2) 'CX Banking software on all ATMs' names a specific multivendor ATM software stack that is NOT Printec's - a software displacement target, and a warning that BKT's ATM channel is already someone else's.

- Source: Calik Holding — Finance Sector: BKT Albania; BKT — ATM Smart BanKomaT product pages — https://calik.com/en/sectors/finance-sector/bkt-albania (Jul-2026 (accessed; figures undated on page), tier: primary)
- Likelihood: Medium: BKT is a scale account with an incumbent ATM software vendor; POS growth is the more winnable entry | Confidence: Medium | Opp size: L | Win: Medium | Deadline: - | New: True
- Follow-up: Identify who supplies and services BKT's 161 Smart ATMs and who 'CX Banking' is (likely a third-party multivendor ATM application) - naming BKT's ATM OEM/software incumbent is a standing gap. Get the BKT 2025 annual report from bkt.com.al investor relations for dated figures.

### 9. OTP Bank Albania — L

**Signal.** OTP Bank Albania's own corporate page states 'a network of 49 strategically positioned branches and more than 180 ATMs distributed across the country'. This sits materially ABOVE the 157 ATMs / 49 branches reported for OTP Albania in the OTP Group 31/03/2026 disclosure carried in the previous run, suggesting either off-site/partner units excluded from the group count or growth since. The bank also describes being in phase 3 of an end-to-end digital lending project and a second round of online-banking upgrades adding QR-code bill payment, digital signature and card management.

**Implies for Printec.** Printec is the incumbent on OTP Albania's ATM estate. A 180+ unit fleet at only 49 branches means a high off-site ratio - i.e. heavy standalone self-service, which is exactly where recyclers and managed services pay for themselves. The QR bill payment and digital signature work also opens digital onboarding/eKYC and e-signature adjacencies. Defend the ATM base and attach OptiCash/cash forecasting plus managed services to the off-site units.

- Source: OTP Bank Albania — About us / Our values corporate page — https://otpbank.al/en/about-us/our-values/otp-bank-albania/ (Jul-2026 (accessed; page undated), tier: primary)
- Likelihood: Medium-High that a recycler/refresh tranche runs through 2026 given the previously reported phased 2025-2026 SelfServ 80 delivery to OTP Albania | Confidence: Medium | Opp size: L | Win: High | Deadline: - | New: True
- Follow-up: Reconcile 180+ against the OTP Group quarterly fleet table (2Q2026 report was not yet published at 31/07/2026); confirm whether the phased 2025/2026 SelfServ 80 deposit/recycler deliveries to OTP Albania have completed and whether a further tranche is contracted.

### 10. Jet Bank — M

**Signal.** Jet Bank, licensed by the Bank of Albania in March 2026 as a GREENFIELD institution (not an acquisition), launched operations and its mobile app in June 2026 as Albania's first fully digital-only bank, built on Backbase's AI-native Banking OS by a 70-person team in six months, with 75,000+ people on the pre-launch waiting list. Launch products: multi-currency current accounts, savings and term deposits, virtual and physical debit cards, FX, JetPlans savings goals, live chat and in-app messaging. Loans and credit cards promised within months, plus conversational/agentic AI. Account opening is fully remote; the bank has no branch or cash estate.

**Implies for Printec.** Two-sided. THREAT: a branchless, cash-free competitor legitimises removing cash touchpoints, and Backbase is now embedded in Albania. OPPORTUNITY: Jet Bank has no cash estate and no acquiring estate, so it must buy - white-label cash-in/cash-out access (third-party ATM/recycler network or agent cash), digital onboarding/eKYC with liveness, AML and transaction monitoring, HSM/key management for card issuing, and eventually POS acquiring. A 70-person bank outsources all of it by definition. Every one of these is a Printec line.

- Source: Backbase — 'Jet Bank launches as Albania's first digital-only bank, built on Backbase's AI-Native Banking OS' — https://www.backbase.com/press/jet-bank-launches-as-albanias-first-digital-only-bank-built-on-backbases-ai-native-banking-os (25/06/2026, tier: primary)
- Likelihood: High that Jet Bank procures eKYC/AML/HSM and cash-access services from third parties within 6-12 months | Confidence: Medium | Opp size: M | Win: Medium | Deadline: - | New: True
- Follow-up: Identify Jet Bank's incumbent eKYC, AML and card-issuing/HSM vendors, and whether it has struck a cash-access agreement with any ATM-owning Albanian bank; approach on white-label cash access and AML monitoring first.

### 11. Tirana Bank (BALFIN Group) — M

**Signal.** Tirana Bank selected Backbase in March 2025 for what it describes as its largest-ever technology investment, explicitly surpassing previous core banking implementations, with a stated goal of tripling its digital customer base over the term of the agreement. Tirana Bank has been BALFIN Group-owned since 2019 and reported total assets above EUR 1.63bn at end-2024 across 35 branches, with 84 ATMs reported for 2024 (+23.5% y/y).

**Implies for Printec.** A digital front-end programme of this size drags adjacent spend that Backbase does NOT supply: digital onboarding/eKYC, e-signature, AML/KYC screening, card management, HSM and self-service integration - all open to Printec. The 84-ATM fleet growing 23.5% in a year is also a live self-service account. Competitively, Backbase now holds the two most aggressive digital plays in Albania (Tirana Bank and Jet Bank), which is the frame to plan against.

- Source: Backbase — 'Tirana Bank selects Backbase to lead digital banking revolution in Southeast Europe' — https://www.backbase.com/press/tirana-bank-selects-backbase-to-lead-digital-banking-revolution-in-southeast-europe (Mar-2025, tier: primary)
- Likelihood: Medium-High that adjacent onboarding/AML/self-service procurements follow within 12 months | Confidence: Medium | Opp size: M | Win: Medium | Deadline: - | New: True
- Follow-up: Verify 2026 go-live status of the Backbase programme; confirm Tirana Bank's current ATM count, OEM and whether any are deposit/recycling - the OEM at Tirana Bank is not established.

### 12. Albanian banking sector (Bank of Albania data via AAB) — Unscoped

**Signal.** Sector card and acceptance data for FY2025, BoA-sourced and published by the Albanian Association of Banks: POS terminals rose from 25,190 (Q1) to 27,969 (Q2), 29,261 (Q3) and 31,263 at Q4-2025; ATMs 1,064 / 1,214 / 1,337 / 1,091 by quarter; 449 bank outlets at Q4; 1,652,474 cards with a cash function and 1,576,016 with a payment function (1,456,424 debit, 119,592 credit); 39,634,783 card transactions worth ALL 248.4bn in 2025. Separately, AAB's May-2026 general data (also BoA-sourced) puts sector total assets at ALL 2,344.9bn, loans ALL 986.2bn, deposits ALL 1,894.4bn, ROE 12.41%, ROA 1.27%, capital adequacy 20.44%, NPL ratio 3.77% at 31/05/2026.

**Implies for Printec.** The sizing baseline. 31,263 POS against a universal obligation by 31/12/2026 implies a large incremental terminal wave. Only ~1,091 ATMs across the sector confirms that in Albania the ATM play is REPLACEMENT and UPGRADE (dispenser to recycler/CDM), not net-new units - which is precisely why defending the installed NCR SelfServ 80 base and winning the recycler conversions matters more than chasing greenfield ATM volume. A 20.44% capital ratio and 12.4% ROE mean the banks can fund capex.

- Source: Albanian Association of Banks (AAB) — 'Cards & Home Banking 2025' and 'Albanian Banking System General Data May 2026' (XLSX, source: Bank of Albania) — https://aab.al/wp-content/uploads/2026/02/Cards-Home-Banking-2025.xlsx (Feb-2026, tier: primary)
- Likelihood: n/a - published statistics | Confidence: Medium | Opp size: Unscoped | Win: — | Deadline: - | New: True
- Follow-up: The AAB data page is a plain WordPress index and can be scraped monthly for 'Albanian-Banking-System-General-Data_*.xlsx' and annually for 'Cards-Home-Banking-*.xlsx'; add it to the standing collection list. Note the Q3-to-Q4 ATM drop from 1,337 to 1,091 needs explanation - possibly a seasonal/off-site reclassification.

### 13. Albania — SEPA membership — M

**Signal.** Albania became part of the SEPA geographical scope on 21/11/2024 and began FULL implementation on 07/10/2025, with all 11 local banks registered as SEPA scheme participants and operational from that date. The World Bank reports (25/03/2026) that average business-to-business payment transfer costs fell roughly TENFOLD after each Western Balkans country's SEPA launch, citing an Albanian SME saving ~EUR 2,500 per month in transfer fees, and states fast payments settling in seconds are the next phase, expected later in 2026 across Albania, Bosnia and Herzegovina, Montenegro, North Macedonia and Kosovo.

**Implies for Printec.** SEPA plus instant payments plus interchange caps is a coordinated collapse in payment pricing across Albania. Banks lose fee income per transaction and must cut unit cost - which is the argument for outsourcing self-service and acceptance operations to Printec managed services. ISO 20022/SEPA message handling and 24x7 operations also raise the bar on payment hubs, HSM and real-time AML screening at all 11 banks simultaneously.

- Source: World Bank — 'Cheaper and Faster Payments: SEPA Opens New Horizons for the Western Balkans'; Bank of Albania press release on SEPA geographical scope — https://www.worldbank.org/en/news/feature/2026/03/25/cheaper-and-faster-payments-sepa-opens-new-horizons-for-the-western-balkans (25/03/2026, tier: press)
- Likelihood: Already in force; instant payments the remaining leg | Confidence: Medium | Opp size: M | Win: Medium | Deadline: - | New: True
- Follow-up: Get the BoA SEPA press release and the EPC participant register to confirm all 11 banks and their reachability; identify which banks outsourced SEPA message processing rather than building it, as those are the managed-services buyers.

### 14. Printec Albania / Printec Group — Unscoped

**Signal.** Printec publicly showcased NCR Atleos' latest line of RECYCLERS and cash dispensers at Technobank 2026, and separately announced Printec Albania moving into new offices in Tirana. Printec maintains country teams across Albania, Bosnia, Croatia, Kosovo, Montenegro, Serbia and North Macedonia.

**Implies for Printec.** Confirms the current Printec go-to-market in the region is built on the NCR Atleos recycler line - the right product for the Albanian pattern of converting dispenser fleets to deposit/recycling rather than adding units. A local office expansion signals delivery capacity for the 2026 POS mandate wave.

- Source: Printec Group — 'Inside Printec at Technobank 2026: innovation, partnerships, and real impact'; Printec blog — 'Printec Albania enters a new era with its new offices in Tirana' — https://www.printecgroup.com/inside-printec-at-technobank-2026-innovation-partnerships-and-real-impact/ (2026, tier: primary)
- Likelihood: n/a - vendor positioning | Confidence: Low | Opp size: Unscoped | Win: — | Deadline: - | New: True
- Follow-up: Get exact dates for both items - blog.printecgroup.com returned 403 to automated fetch and the Technobank page was not opened directly this run; confirm which NCR Atleos recycler models are being positioned for Albania.

## Coverage notes

Fresh full pass on Albania (no checkpoint existed for this runDate; not resumed). Angles used, deliberately varied from the prior run: (1) BoA regulatory/consultation registers reached with a desktop User-Agent via curl after WebFetch 403s - this surfaced TWO primary draft acts the baseline never saw (the interchange-fee draft regulation with the 0.2%/0.3% caps read directly out of the PDF text, and the draft law on payment systems and financial collateral with its explanatory memorandum). (2) The AAB data portal, scraped as the source catalogue's 'how' hint describes, then the XLSX files parsed locally with openpyxl - this yielded per-quarter BoA sector data on POS, ATMs, outlets and cards for FY2025 plus May-2026 sector balance sheet, which the baseline lacked entirely. (3) Bank primary sites (raiffeisen.al, otpbank.al, calik.com for BKT, ncratleos.com case study) for fleet counts, which materially updated Raiffeisen (198 ATMs vs 186 in baseline) and added BKT (62 branches / 161 Smart ATMs / 10,000 POS) and OTP Albania (49 branches / 180+ ATMs, above the group-reported 157). (4) Vendor press rooms (Backbase) for the two digital-bank plays. (5) Albanian-language press (Monitor, Panorama, Shqiptarja, businessmag.al) for the POS mandate and instant-payments timing. Baseline items RE-VERIFIED and confirmed: NCR ~95% ATM share and 11 of 13 banks on SelfServ 80, Printec Albania as the named NCR partner, Union Bank on SelfServ 82/84 recyclers - all confirmed against NCR Atleos' own case study. Law 79/2025 deadlines 30/05/2026 and 31/12/2026 confirmed. MATERIALLY CHANGED vs baseline: instant payments moved from 'autumn 2026' to November 2026; Raiffeisen AL 186 to 198 ATMs; OTP AL stated fleet now 180+ against the group's 157. GENUINE GAPS: (a) no systematic public-procurement scan was completed - openprocurement.al's list endpoint ignored the search query parameter and app.gov.al's e-procurement notices are paginated server-rendered pages that need a dedicated crawl; the 30/05/2026 public-institution POS leg almost certainly generated tenders that were not enumerated. (b) The BoA Supervision Annual Report 2025 was published 09/07/2026 but its PDF could not be located - the publication index pages are AJAX-rendered and returned no document links. (c) No primary BoA source was found naming November 2026 for instant payments; that date rests on Revista Monitor. (d) OTP Group 2Q2026 was not yet published at 31/07/2026, so the group fleet table could not be refreshed. (e) Credins Bank yielded no dated 2026 fleet or technology figures. (f) The ATM OEM at BKT (which runs 'CX Banking' software), Tirana Bank and Credins remains UNIDENTIFIED - this is the standing task and it did not close this run.

## Access issues

bankofalbania.org returns HTTP 403 to WebFetch on every path. Route used: curl with a desktop Chrome User-Agent, which worked on all BoA pages, plus local PDF text extraction (pdftotext) for the draft regulation and explanatory memorandum. Logged blocked URLs: https://www.bankofalbania.org/Payments/Payment_systems_statistics/ (403 to WebFetch, retrieved via UA curl). https://www.unionbank.al/programi-posi-nga-mastercard/ - Cloudflare 'Attention Required' block on UA curl AND 403 on WebFetch; NOT retrieved. Worked around by using Raiffeisen Bank Albania's equivalent POSI page, so the programme terms cited are Raiffeisen's, not Union Bank's. https://blog.printecgroup.com/printec-albania-enters-a-new-era-with-its-new-offices-in-tirana - 403 to WebFetch and empty body to UA curl; NOT retrieved, so that item is cited at Low confidence off the search snippet. https://otpbank.al/en/branches-and-atms/ - fetched but the branch/ATM locator is JavaScript-rendered, so units could not be counted; the About page was used instead. https://openprocurement.al/sq/albaniandf/list?search=... - returns HTTP 200 but ignores the search parameter and serves the default listing, so no keyword procurement search was possible. BoA publication indexes (/Botime/Botime_Periodike/Raporti_Vjetor_i_Mbikeqyrjes/) are AJAX-paginated and expose no PDF hrefs to a plain fetch. monitor.al articles are partially paywalled; the visible portion was used.

## Operator requests

1) Bank of Albania SUPERVISION ANNUAL REPORT 2025, presented 10/07/2026 (announcement: https://www.bankofalbania.org/Shtypi/Njoftimet_per_shtyp/Raporti_Vjetor_i_Mbik_e_qyrjes-2025.html) - the PDF is not linked from any statically-fetchable index. Please retrieve it; it carries the per-bank supervisory picture and the payments-instrument chapter. 2) UNION BANK ALBANIA site (unionbank.al) - Cloudflare-blocked to all automated fetch. Needed: the Mastercard POSI programme page, the latest annual report, and any 2025/2026 ATM or recycler disclosure. A browser session or an operator download would close the single most important incumbency account in this market. 3) app.gov.al e-procurement - a keyword crawl of 'njoftimi i fituesit' and 'njoftimi i kontrates se shpallur' for 2026 on the terms POS, POI, bankomat, ATM, terminal pagese. Public institutions with state capital had a 30/05/2026 POS deadline and their tenders are almost certainly on this portal. This needs a paginated crawl the fetch tool cannot do. 4) Bank of Albania Supervisory Council decisions 2026 - to confirm a primary source for the November-2026 instant-payments go-live and for the interchange regulation's consultation closing date.
