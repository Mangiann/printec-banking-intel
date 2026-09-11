# UniCredit Bulbank (Bulgaria) - bank disclosure findings, run 2026-08-27

**Slug:** unicredit-bulbank-bg  |  **Status:** complete  |  **Signals:** 23

## Headline
- The bank itself lists **'ICT & ICT Security Risks - ATM obsolescence'** as a 2026 non-financial risk driver (2025 Annual Report, p.111). That is the buying trigger for post-euro ATM replacement, and it lines up with the Group's dated plan to replace **more than half of its ATMs with latest-generation models by 2027**.
- The bank's own locator API gives exact, current counts: **761 ATM records, only 197 deposit-capable (~26%)**, and **32 of 162 branches flagged 'Cashless service'**. 30 of those 32 cashless branches have a deposit ATM within 500 m - so cashless conversion and deposit-ATM placement move together.
- 'Branch of the Future' as a phrase is **not used** by UniCredit Bulbank in any primary source found. The substance is real and documented ('development of self-service zones, agency branches'); the label is not.
- Free BGN exchange runs to **30/09/2026**; mandatory dual display ended **09/08/2026**; SEPA Instant live from **20/08/2026**.
- **PRIME** affluent model launched 18/05/2026 across nine CEE markets, with PRIME zones in every branch - a 162-site fit-out counterpart to removing cash desks.
- **Google Cloud** is the Group's primary AI and migration platform across **all 13 Group banks**, Bulbank included - an architectural qualifier for anything sold in.

## Signals

### 1. UniCredit Bulbank - Bank's own branch locator API flags 32 of 162 branches as 'Cashless service' (no teller cash handling) as at 2
- **Signal:** Bank's own branch locator API flags 32 of 162 branches as 'Cashless service' (no teller cash handling) as at 27/08/2026 - 5 in Sofia, 3 in Varna, the rest one-per-town in small municipalities (Kostenets, Svoge, Dulovo, Etropole, Mezdra, Popovo, General Toshevo, Chirpan, Peshtera etc.).
- **Source:** UniCredit Bulbank branch locator API (/en/api/locations/branches.json + nomenclatures.json), 27/08/2026 - https://www.unicreditbulbank.bg/en/api/locations/branches.json (primary)
- **Implies:** Cashless branch = the cash desk is removed and cash traffic must move to a machine. 130 branches remain to convert; each conversion is a cash-in/recycler placement plus assisted self-service.
- **Likelihood:** High - conversion already running, one-per-town pattern suggests a rolling programme | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Re-pull this JSON monthly; a rising 'Cashless service' count is the deployment signal. Ask UCB retail network head (Ekaterina Panayotova) for the conversion schedule.

### 2. UniCredit Bulbank - ATM locator API returns 761 ATM records (684 distinct addresses) of which only 197 carry the 'Has deposit func
- **Signal:** ATM locator API returns 761 ATM records (684 distinct addresses) of which only 197 carry the 'Has deposit functionality' flag - i.e. roughly 564 machines are cash-out only. 512 are 24/7 and 676 contactless.
- **Source:** UniCredit Bulbank ATM locator API (/en/api/locations/atms.json), 27/08/2026 - https://www.unicreditbulbank.bg/en/api/locations/atms.json (primary)
- **Implies:** Only ~26% of the fleet accepts deposits. After the euro changeover the deposit gap is the constraint on closing cash desks - direct recycler/cash-in retrofit or replacement opportunity.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** XL | **Win:** Medium | **New:** True
- **Follow-up:** Compare against UBB (246/738 deposit-capable) and Postbank (225/498) from the 30/07/2026 baseline; build a per-town deposit white-space map.

### 3. UniCredit Bulbank - Geo-matching the two feeds: 30 of the 32 cashless branches have a deposit-capable ATM within 500 m; only Sofia
- **Signal:** Geo-matching the two feeds: 30 of the 32 cashless branches have a deposit-capable ATM within 500 m; only Sofia 'Pametnik Levski' and Svoge do not.
- **Source:** UniCredit Bulbank locator APIs (branches.json + atms.json), own computation, 27/08/2026 - https://www.unicreditbulbank.bg/en/contacts/branches-and-atms/ (primary)
- **Implies:** Confirms the operating model: a cashless branch is paired with a deposit ATM. So the conversion pipeline for the remaining 130 branches converts almost 1:1 into deposit-ATM demand.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Quantify how many of the 130 still-cash branches already have a deposit ATM on site - those are the cheapest next conversions and the shortest sales cycle.

### 4. UniCredit Bulbank - Bank extended fee-free exchange of BGN banknotes AND coins for individuals across its branch network to 30 Sep
- **Signal:** Bank extended fee-free exchange of BGN banknotes AND coins for individuals across its branch network to 30 September 2026; declaration of source of funds required above EUR 5,000 under AML rules.
- **Source:** UniCredit Bulbank newsroom (BG), 24/06/2026 - https://www.unicreditbulbank.bg/bg/za-nas/media/novini/obmyana-na-levove-do-kraya-na-septemvri/ (primary)
- **Implies:** Keeps manual coin/note handling in branches through Q3-2026 - a dated cliff-edge. After 30/09/2026 that teller volume disappears and the cost case for removing cash desks (and for coin/note recycling equipment) sharpens.
- **Likelihood:** High - fixed date | **Confidence:** Medium | **Opp size:** M | **Win:** Medium | **New:** True
- **Follow-up:** Watch for an October 2026 branch-format announcement once free exchange ends. Also probe coin-handling equipment need through Sept.

### 5. UniCredit Bulbank - Mandatory BGN/EUR dual-display period ended 9 August 2026; from that date all amounts in the bank's digital ch
- **Signal:** Mandatory BGN/EUR dual-display period ended 9 August 2026; from that date all amounts in the bank's digital channels and documents show only in euro, with the website following in stages.
- **Source:** UniCredit Bulbank newsroom (BG), 12/08/2026 - https://www.unicreditbulbank.bg/bg/za-nas/media/novini/prikluchvane-period/ (primary)
- **Implies:** Euro-conversion project work on channels is closing out; budget and change capacity free up from Q4-2026 for the next wave (self-service, branch format).
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** Unscoped | **Win:** — | **New:** True
- **Follow-up:** Time vendor approach to the Q4-2026 planning cycle.

### 6. UniCredit Bulbank - Bank launched SEPA Instant Credit Transfer outbound/inbound from 20 August 2026, announced alongside the euro-
- **Signal:** Bank launched SEPA Instant Credit Transfer outbound/inbound from 20 August 2026, announced alongside the euro-transition measures.
- **Source:** UniCredit Bulbank newsroom (BG), 24/06/2026 - https://www.unicreditbulbank.bg/bg/za-nas/media/novini/obmyana-na-levove-do-kraya-na-septemvri/ (primary)
- **Implies:** Instant payments raise real-time fraud and sanctions-screening load and bring Verification of Payee obligations - transaction monitoring / AML screening scope.
- **Likelihood:** High - already live | **Confidence:** Medium | **Opp size:** M | **Win:** Medium | **New:** True
- **Follow-up:** Confirm the go-live actually happened on 20/08/2026 and whether VoP is in-house or vendor-supplied.

### 7. UniCredit Bulbank - PRIME affluent service model launched in Bulgaria and eight other CEE markets simultaneously (BG, BiH, HR, CZ,
- **Signal:** PRIME affluent service model launched in Bulgaria and eight other CEE markets simultaneously (BG, BiH, HR, CZ, HU, RO, RS, SK, SI) under the UniCredit Unlimited strategic plan. Bulgarian eligibility: assets above EUR 50,000, or regular income above EUR 3,100/month in Sofia and EUR 2,600 elsewhere. Includes dedicated PRIME zones in every branch and a PRIME section in Bulbank Mobile; 86% of affluent clients already use Bulbank Mobile.
- **Source:** UniCredit Bulbank newsroom (BG), 18/05/2026 - https://www.unicreditbulbank.bg/bg/za-nas/media/novini/unikredit-bulbank-prime/ (primary)
- **Implies:** 'PRIME zones in all branches' is a physical branch refit across 162 sites, and it is the counterpart to removing the cash desk - advisory space in, cash out. Also digital onboarding/identification for the PRIME journey.
- **Likelihood:** High - announced as launched | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Find the refit rollout schedule and whether fit-out is centrally tendered by UniCredit Group across the nine markets - that would be a nine-country deal, not a Bulgarian one.

### 8. UniCredit Bulbank - Bank details its corporate payment automation stack: European Gate (single Group access point, pain.001.001.09
- **Signal:** Bank details its corporate payment automation stack: European Gate (single Group access point, pain.001.001.09 and pain.001.001.03) and Host-to-Host direct API integration between client ERP and Bulbank Online, incl. SEBRA/budget payments; camt.053 statements, with pain.002 payment status and newest camt versions on the near-term roadmap.
- **Source:** UniCredit Bulbank newsroom (BG), interview with Izabela Dzhonicheva, Director Payment Solutions, 28/04/2026 - https://www.unicreditbulbank.bg/bg/za-nas/media/novini/ucb-integrirani-resheniya-za-avtomatizaciya/ (primary)
- **Implies:** Named, dated roadmap items (pain.002, camt upgrade, new payment authorisation methods) - integration/managed-services and HSM/authentication adjacency.
- **Likelihood:** Medium | **Confidence:** Medium | **Opp size:** M | **Win:** Low | **New:** True
- **Follow-up:** 'New payment authorisation methods for full automation' is the hook - probe whether that means certificate/HSM-based corporate signing.

### 9. UniCredit Bulbank - The bank names 'ICT & ICT Security Risks - ATM obsolescence' as one of the non-financial risk drivers it will 
- **Signal:** The bank names 'ICT & ICT Security Risks - ATM obsolescence' as one of the non-financial risk drivers it will focus on and closely monitor in 2026, in the Risk Management chapter of its 2025 Annual Report.
- **Source:** UniCredit Bulbank 2025 Annual Report and Accounts, Risk Management chapter (p.111), 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** The bank has itself declared its ATM estate obsolete as a 2026 risk. This is the single clearest buying trigger for ATM replacement / recycler upgrade and managed services - it is a board-level risk item, not an aspiration.
- **Likelihood:** High - self-declared 2026 risk driver | **Confidence:** Medium | **Opp size:** XL | **Win:** High | **New:** True
- **Follow-up:** Get in front of the COO / Digital and Information Office now with a fleet-refresh and managed-services proposition; ask whether replacement will be tendered locally or drawn from the Group ATM renewal plan.

### 10. UniCredit Bulbank - Same 2026 risk-driver list names 'coverage extension of the Anti-Fraud system (SAS FM Tool)', 'monitoring of S
- **Signal:** Same 2026 risk-driver list names 'coverage extension of the Anti-Fraud system (SAS FM Tool)', 'monitoring of Safer Payments system enhancements' and a 'New Digital Onboarding solution' as 2026 conduct-and-fraud focus items.
- **Source:** UniCredit Bulbank 2025 Annual Report and Accounts, Risk Management chapter (p.111), 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Names the incumbents in transaction monitoring (SAS Fraud Management) and payment fraud (Safer Payments) - so those two are defended. The NEW digital onboarding solution is the open slot: eKYC/identity is being procured or built in 2026.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Establish whether the new digital onboarding solution is a Group-mandated platform or a local selection; if local, this is a live 2026 opportunity for eKYC.

### 11. UniCredit Bulbank - Bank completed migration of its entire ATM fleet for euro adoption during 2025, with BGN dispensing until the 
- **Signal:** Bank completed migration of its entire ATM fleet for euro adoption during 2025, with BGN dispensing until the last hours of 2025 and EUR banknotes from 1 January 2026; it states it holds the No.1 market share in amounts deposited via ATM network, with deposited amounts up about 20% year on year.
- **Source:** UniCredit Bulbank 2025 Annual Report, Retail and Private Banking / Activity Review, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Deposit-ATM volumes are strategically important to the bank and it defends a leading position - but only ~197 of 761 machines accept deposits. Volume leadership on a minority-deposit fleet is a capacity argument for recyclers.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Pair this claim with the 197/761 locator count in the pitch: leadership is being carried by a quarter of the estate.

### 12. UniCredit Bulbank - Bank waived the cash deposit fee at branches AND ATMs for June-December 2025 to pull BGN cash in ahead of the 
- **Signal:** Bank waived the cash deposit fee at branches AND ATMs for June-December 2025 to pull BGN cash in ahead of the changeover, producing a 40% increase in the number of customer cash deposits.
- **Source:** UniCredit Bulbank 2025 Annual Report, Retail deposits section, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** A 40% jump in deposit transactions on a fleet where only ~26% of machines take deposits is a hard throughput constraint - the strongest quantified case for cash recyclers.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Ask for per-machine deposit transaction volumes at the busiest sites to size recycler need.

### 13. UniCredit Bulbank - Network contraction disclosed: 121 branches and 3,038 employees at 31/12/2025 unconsolidated (from 125 branche
- **Signal:** Network contraction disclosed: 121 branches and 3,038 employees at 31/12/2025 unconsolidated (from 125 branches / 3,134 employees a year earlier); consolidated 130 branches and 3,455 employees (from 134 / 3,582).
- **Source:** UniCredit Bulbank 2025 Annual Report, Financial Highlights (Unconsolidated and Consolidated), 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Slow physical contraction (-4 branches, -96 staff in one year) alongside cashless conversion - the Bulgarian play, like CEC Bank's in Romania, is automation inside a broadly retained network rather than mass closure.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** Unscoped | **Win:** — | **New:** True
- **Follow-up:** Reconcile the disclosed 121/130 branch figure against the 162 records in the public locator - the gap is probably agency-model outlets and non-branch sites; worth confirming.

### 14. UniCredit Bulbank - Real Estate function lists 'development of self-service zones, agency branches, optimization of spaces for bus
- **Signal:** Real Estate function lists 'development of self-service zones, agency branches, optimization of spaces for business purposes' among business-priority initiatives, and states it provided 'the necessary equipment for money processing as part of the Euro adoption project' in 2025. Retail chapter separately names expansion of the Agent model as a key 2025 network-transformation priority for smaller towns and remote locations.
- **Source:** UniCredit Bulbank 2025 Annual Report, Chief Operating Office - Focus on Real Estate; Retail Network Transformation, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Self-service zones and agency branches are the named vehicle for the branch format change. Agency/small-town outlets are exactly where an assisted self-service device replaces a teller.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Ask what 'money processing equipment' was bought for the euro project and from whom - that reveals the incumbent and the refresh cycle.

### 15. UniCredit Bulbank - Procurement chapter states that 'all necessary activities for the upgrade of ATM and POS devices were duly con
- **Signal:** Procurement chapter states that 'all necessary activities for the upgrade of ATM and POS devices were duly contracted' for the euro programme, following negotiations with core banking providers, application vendors, BORICA as authorisation centre, and international partners, with DORA obligations addressed.
- **Source:** UniCredit Bulbank 2025 Annual Report, Focus on Procurement, Cost & Third Party Management, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Confirms ATM and POS estate work was contracted for the euro upgrade in 2025 - and confirms DORA third-party requirements now sit inside any vendor contract. The 2026 'ATM obsolescence' risk shows the 2025 upgrade was a euro patch, not a fleet renewal.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** L | **Win:** Medium | **New:** True
- **Follow-up:** Identify who won the 2025 ATM/POS upgrade contracts; that vendor is the incumbent to displace or partner with on the renewal.

### 16. UniCredit Bulbank - Transaction growth in 2025: ATM transactions +4%, POS transactions +12%, debit card transactions +15%, credit 
- **Signal:** Transaction growth in 2025: ATM transactions +4%, POS transactions +12%, debit card transactions +15%, credit card transactions +19%, domestic payments +12.7%, international +13.2%; KYC workloads rose 30% for both SME and Corporate (onboarding and reviews). Absorbed without a proportional resource increase.
- **Source:** UniCredit Bulbank 2025 Annual Report, Focus on Operations - Growth Absorption, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** POS growing three times faster than ATM, and a 30% KYC workload jump absorbed on flat headcount - both are automation pressure points (acquiring/terminal estate; eKYC and periodic-review automation).
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** M | **Win:** Medium | **New:** True
- **Follow-up:** KYC +30% on flat staff is the cleanest AML/onboarding automation hook - lead with it into Compliance.

### 17. UniCredit Bulbank - 2025 completions include the rollout of a new anti-money-laundering solution, plus DORA, AnaCredit and SAF-T i
- **Signal:** 2025 completions include the rollout of a new anti-money-laundering solution, plus DORA, AnaCredit and SAF-T initiatives; fraud prevention measures prevented EUR 3.5 mln of losses in 2025; an AI-powered EUR Chatbot was deployed in December 2025, and DigiMate (AI assistant built on Bulgaria's national BgGPT model) in July 2025.
- **Source:** UniCredit Bulbank 2025 Annual Report, Chief Operating Office - Regulatory, Infrastructure and Risk Management / Digital Innovation, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** The core AML platform was just replaced, so that door is closed for now; the open adjacencies are monitoring coverage extension, case management and eKYC. Local AI adoption (BgGPT) shows willingness to buy locally-fitted technology.
- **Likelihood:** Medium | **Confidence:** Medium | **Opp size:** M | **Win:** Low | **New:** True
- **Follow-up:** Identify the new AML vendor before pitching anything AML-adjacent.

### 18. UniCredit Bulbank - Bank states it delivered 16% of the nationwide euro cash supply to customers around the changeover, and ran th
- **Signal:** Bank states it delivered 16% of the nationwide euro cash supply to customers around the changeover, and ran the transition through an 'EUR Tracker' tool integrating thousands of activities into more than 90 structured milestones; SEPA Instant and BLINK were fully operational immediately after the switch (<=10s, 24/7/365).
- **Source:** UniCredit Bulbank 2025 Annual Report, Euro adoption programme, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** A 16% share of national cash distribution means cash logistics and cash-centre capacity are material to this bank - cash automation and cash-cycle managed services are relevant, not just branch devices.
- **Likelihood:** Medium | **Confidence:** Medium | **Opp size:** M | **Win:** Medium | **New:** True
- **Follow-up:** Probe whether cash processing is in-house or outsourced, and to whom, post-changeover.

### 19. UniCredit Group (parent of UniCredit Bulbank) - Group discloses a major ATM renewal plan 'replacing more than half of our machines with latest-generation mode
- **Signal:** Group discloses a major ATM renewal plan 'replacing more than half of our machines with latest-generation models by 2027', alongside BancoSmart 2.0, the new UniCredit ATM interface, which reached withdrawal-only ATMs in 2025, is being distributed to Advanced (deposit-capable) ATMs, and reaches Quick Cash Desks in 2026. Almost 90% of UniCredit branches have been upgraded.
- **Source:** UniCredit 2025 Annual Reports and Accounts, Strategic Review - Channels (p.51), reproduced in UniCredit Bulbank's 2025 Annual Report, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** A dated, Group-wide fleet replacement commitment running to 2027 that must include the Bulgarian estate - and it coincides exactly with Bulbank's own 'ATM obsolescence' 2026 risk flag. Devices, software rollout and deployment services all in scope.
- **Likelihood:** High - dated Group commitment to 2027 | **Confidence:** Medium | **Opp size:** XL | **Win:** Medium | **New:** True
- **Follow-up:** Determine whether the renewal is a Group frame agreement (single vendor) or executed per country - this decides whether the Bulgarian conversation is worth having locally.

### 20. UniCredit Group (parent of UniCredit Bulbank) - Group Google Cloud partnership (announced May 2025) migrates large parts of the application landscape, includi
- **Signal:** Group Google Cloud partnership (announced May 2025) migrates large parts of the application landscape, including legacy systems, to Google Cloud across ALL 13 Group banks, and makes Google Cloud the primary platform for AI workloads (Vertex AI, Gemini). Named application areas include financial crime prevention; potential extension to Google Maps platform for customer journeys.
- **Source:** UniCredit 2025 Annual Reports and Accounts, Digital and Data chapter, reproduced in UniCredit Bulbank's 2025 Annual Report, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Bulbank is one of the 13 banks in scope. Any system sold into Bulbank from here must be cloud-deployable on GCP and fit a Group AI platform - a hard architectural qualifier for ATM management software, monitoring and compliance tooling.
- **Likelihood:** High | **Confidence:** Medium | **Opp size:** Unscoped | **Win:** — | **New:** True
- **Follow-up:** Confirm the Bulgarian migration wave and timing; check whether ATM/self-service management platforms are in the migration scope.

### 21. UniCredit Bulbank - Q4-2025 launch of a Virtual Mortgage Center offering a remote end-to-end mortgage process from first consultat
- **Signal:** Q4-2025 launch of a Virtual Mortgage Center offering a remote end-to-end mortgage process from first consultation through digital signing and disbursement, plus 'Comfort by UniCredit' rebrand of the remote servicing model with a personal remote banker; mobile app fully redesigned with new self-service capabilities.
- **Source:** UniCredit Bulbank 2025 Annual Report, Retail and Private Banking / Digital Innovation, 14/05/2026 - https://www.unicreditbulbank.bg/media/filer_public/00/18/00187e6b-6f5f-45e9-a40f-9e9160680f20/ucb_ar2026_en_all_a4_am_long.pdf (primary)
- **Implies:** Remote end-to-end mortgage with digital signing requires qualified remote identification and e-signature - digital onboarding/eKYC scope, and it dovetails with the separately flagged 'New Digital Onboarding solution' for 2026.
- **Likelihood:** Medium | **Confidence:** Medium | **Opp size:** M | **Win:** Medium | **New:** True
- **Follow-up:** Find which QES/remote-identification provider underpins the Virtual Mortgage Center.

### 22. UniCredit Bulbank - Bank added Garmin Pay for its Mastercard debit and credit cards, extending wearable/tokenised contactless paym
- **Signal:** Bank added Garmin Pay for its Mastercard debit and credit cards, extending wearable/tokenised contactless payment alongside Apple Pay and Google Pay.
- **Source:** UniCredit Bulbank newsroom (BG), quoting Georgi Hvorev, Senior Manager Card and POS Solutions, 15/06/2026 - https://www.unicreditbulbank.bg/bg/za-nas/media/novini/plashane-s-chasovnik-garmin-pay/ (primary)
- **Implies:** Continued tokenisation build-out; incremental for Printec but identifies the named owner of the card and POS estate (Georgi Hvorev) as the entry point for acquiring/terminal conversations.
- **Likelihood:** High - live | **Confidence:** Medium | **Opp size:** S | **Win:** Low | **New:** True
- **Follow-up:** Use Hvorev as the named contact for POS/terminal estate discussions.

### 23. UniCredit Bulbank - Bank publicly offers corporate customers ATM installation inside their retail outlets, deploying either lobby 
- **Signal:** Bank publicly offers corporate customers ATM installation inside their retail outlets, deploying either lobby or through-the-wall machines after a site survey, positioning it as footfall generation plus bill payment.
- **Source:** UniCredit Bulbank corporate cash-management ATM page (EN), 27/08/2026 - https://www.unicreditbulbank.bg/en/corporate-clients/cash-management/terminals/atms/ (primary)
- **Implies:** An active off-premise ATM deployment channel: fleet growth is driven partly by retail-partner sites, which need through-the-wall/lobby hardware plus remote monitoring and cash-in-transit scheduling - managed services fit.
- **Likelihood:** Medium - standing offer, growth rate unknown | **Confidence:** Medium | **Opp size:** M | **Win:** Medium | **New:** True
- **Follow-up:** Ask how many of the 761 machines are off-premise partner sites; those have the shortest replacement cycle and the weakest incumbency.

## Coverage notes

Fresh run, no checkpoint existed. WebSearch budget for this session was exhausted (200/200) before the first query, so ALL research was done by direct HTTP fetching of primary sources with a desktop browser User-Agent - no search-engine discovery was possible. Angles used: (1) UniCredit Bulbank sitemap.xml (2,548 URLs) to enumerate the site; (2) the bank's machine-readable locator APIs at /en/api/locations/{atms,branches,nomenclatures,services}.json - undocumented but open, and the single most valuable find, because nomenclatures.json exposes the 'Cashless service' branch flag and the 'Has deposit functionality' ATM flag, allowing exact counts and a geo-join between the two; (3) the full Bulgarian newsroom (3 list pages, all 30 articles downloaded and parsed, dates taken from the <time datetime> tag); (4) the 2025 Annual Report PDF (19.5 MB, published 14/05/2026 per PDF creation metadata), text-extracted locally and read in full for the Bulbank Activity Review, Risk Management, COO, Real Estate, Procurement and Security chapters, plus the Group Strategic Review sections it reproduces; (5) the corporate cash-management terminal/ATM product pages; (6) the euro information hub; (7) five Bulgarian/regional press and fintech RSS feeds; (8) the LinkedIn jobs-guest feed; (9) Association of Banks in Bulgaria review PDFs. GENUINE GAPS: 'Branch of the Future' - this exact label does NOT appear anywhere in UniCredit Bulbank's own 2025 Annual Report or newsroom, nor in the Group sections reproduced there. The underlying reality is nonetheless documented and quantified here (32 of 162 locator branches flagged Cashless service; AR names 'development of self-service zones, agency branches'), but the phrase itself is unverified against a primary source and should not be attributed to the bank. UniCredit Group's 2Q26/1H26 results were not obtained: the Group press-release and financial-reporting listings are JavaScript-rendered and the direct PDF URL patterns returned 404, so no Bulgaria-level H1-2026 data point was retrieved and no group/country fleet reconciliation was possible. UniCredit Bulbank has published no 2026 interim report on either the EN or BG IR page as at 27/08/2026 - the newest bank-level disclosure remains the FY2025 Annual Report of 14/05/2026, so the August reporting-window prioritisation yielded locator data and newsroom items rather than a fresh interim. Association of Banks in Bulgaria has no 2026 quarterly review published (2026-Q1/Q2 URLs 404). No local-press cross-check was achievable: none of the five Bulgarian/regional feeds polled carried any UniCredit mention in their current window.

## Access issues

BLOCKED/UNAVAILABLE, all logged rather than dropped: (1) bnb.bg payment-system statistics - four candidate paths (/PaymentSystem/PSPaymentOversight/PSPOStatistics/, /PaymentSystem/PSStatistics/, /Statistics/StPaymentSystem/, /PaymentSystem/PSOversight/PSOStatistics/) all returned HTTP 200 but served an identical 16,803-byte generic template with no statistics links, and the /bnbweb/groups/public/documents/ direct-document path returned 404. Retried with a desktop Chrome User-Agent - same result. No BNB ATM/POS series obtained this run. (2) unicreditgroup.eu press-release and financial-press-release listings return HTTP 200 but the article lists are client-side rendered; only the FY2025 report and Pillar III PDFs are hard-linked. Three guessed 2Q26 PDF paths returned 404. Escalation to Claude-in-Chrome was not attempted because the browser tools were deferred and the remaining gap was group-level rather than bank-level. (3) unicreditbulbank.bg site search: /bg/tarsene/?q=... returns 404 and /en/search/?q=... returns a shell with no server-rendered results; no search API endpoint was discoverable in the page source, so keyword sweeps of the bank's own site were not possible. (4) The EN newsroom carries only 11 items versus 30 in Bulgarian - the Bulgarian newsroom is the authoritative feed and was used. (5) abanksb.bg 2026-Q1/Q2 review PDFs: 404. (6) WebSearch: hard budget exhaustion (200/200) at the start of this subagent's turn - this is the dominant constraint on this run and materially reduced discovery of third-party and press sources.

## Operator requests

(1) UniCredit Group 1H26/2Q26 results - press release, presentation and the CEE/Bulgaria divisional data pack from unicreditgroup.eu/en/investors/financial-reporting.html; the listing is JavaScript-rendered so an operator with a real browser should download the 2Q26 PDFs and confirm whether the 'replace more than half of our ATMs with latest-generation models by 2027' plan has a stated progress figure or a per-country breakdown. (2) Any UniCredit Group Capital Markets Day / 'UniCredit Unlimited' plan material describing the branch format and self-service investment envelope by country. (3) BNB payment-system oversight statistics (number of ATMs and POS terminals in Bulgaria, and ATM cash-deposit volumes) for Q4-2025 through Q2-2026 - needs a real browser session on bnb.bg. (4) Confirmation of the vendor(s) behind UniCredit Bulbank's 2025 ATM and POS device euro upgrade, its new AML solution, and the SAS FM / Safer Payments anti-fraud stack - likely only obtainable via trade press, vendor case studies or direct contact. (5) Verification of whether 'Branch of the Future' is a real UniCredit programme name; if the brief's term came from a conference talk or interview, the operator should supply the source so it can be cited properly.
