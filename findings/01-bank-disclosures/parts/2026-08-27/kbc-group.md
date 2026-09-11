# KBC Group (CZ/SK/HU/BG) — bank disclosures, run 27/08/2026

**Status:** complete. First-ever coverage (KBC was a genuine blank in the 30/07/2026 run).

## Headline

- **Branch time series, built from KBC's own quarterly company presentations** (30/06/2025 / 31/12/2025 / 31/03/2026 / 30/06/2026):

  | Market | 30/06/25 | 31/12/25 | 31/03/26 | 30/06/26 | y-o-y |
  |---|---|---|---|---|---|

  | Belgium | 427 | 424 | 421 | 420 | -7 |

  | Czech Republic | 197 | 197 | 197 | 196 | -1 |

  | Slovakia (excl 365.bank) | 97 | 97 | 97 | 97 | 0 |

  | Hungary | 193 | 191 | 189 | 188 | -5 |

  | Bulgaria | 174 | 170 | 170 | 170 | -4 |

- **UBB Bulgaria locator re-pull 27/08/2026:** 737 ATM sites, **244 deposit-capable (33%)**, ~490 cash-out-only, 704 open 24/7; 172 offices incl. 34 euro-hub, 5 cashless-service, 5 joint KBC/UBB. Baseline (late Jul) was 738/246 — **flat: no post-euro recycler rollout has started.**

- **ČSOB Slovakia deposit-ATM list 27/08/2026:** 124 entries at 99 addresses, 66 coin+note, 58 note-only.

- **Kate AI at 2Q2026:** 6.2m users, ~75% autonomy (77% BE / 75% CZ), 484k converted leads in 12 months, >400 FTE of displaced workload. Kate 2.0 (LLM) live in **BE and CZ only**.

- **Dated trigger:** 11/02/2027 topical investor event on KBC's digital transformation, with **new financial and non-financial guidance**.

- KBC discloses **no ATM figure at all** in any 2Q2026 document — 'ATM' appears zero times.


## Signals

### 1. ČSOB Czech Republic (KBC Czech Republic BU) — Czech Republic [L / win Medium / Medium]

KBC's own 2Q2026 company presentation puts the Czech branch count at 196 at 30/06/2026, against 197 at 31/03/2026, 197 at 31/12/2025 and 197 at 30/06/2025 (client base flat at 4.3m, 24% of group assets, EUR 46bn loans / EUR 55bn deposits). Czechia is therefore KBC's only core market where the branch network is essentially frozen rather than shrinking — one net closure in twelve months.

*Source:* KBC Group 2Q2026 company presentation (slide 'Company profile | Well-defined core markets') — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-company-presentation.pdf (06/08/2026, primary)

*Implies:* A stable 196-branch estate serving 4.3m clients means throughput per branch keeps rising, which is the classic trigger for in-branch cash automation (recyclers/TCRs) and assisted self-service rather than closures. Printec cash automation + ATM/self-service + managed services.

*Likelihood:* High that ČSOB CZ invests in per-branch automation rather than closures over 6-12 months; procurement route unconfirmed

*Follow-up:* Compare with 1Q2026 deck (https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/1q2026/1q2026-company-presentation.pdf) and 4Q2025 deck (https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/4q2025/4q2025-company-presentation.pdf); then obtain ČSOB CZ's own ATM/deposit-ATM counts — csob.cz is fully bot-walled to non-browser fetchers (see access_issues).

### 2. K&H Bank Hungary (KBC International Markets BU) — Hungary [L / win Medium / Medium]

KBC discloses 188 Hungarian branches at 30/06/2026, down from 189 at 31/03/2026, 191 at 31/12/2025 and 193 at 30/06/2025 — a steady -5 branches (-2.6%) year-on-year while client numbers hold at 1.7m. Hungary is the fastest-shrinking network in the group's International Markets BU.

*Source:* KBC Group 2Q2026 company presentation (Company profile — International Markets BU) — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-company-presentation.pdf (06/08/2026, primary)

*Implies:* A shrinking manned network with a flat client base forces cash and simple transactions onto machines: deposit/recycling ATMs, assisted self-service kiosks and remote/video advisory. Printec ATM/self-service, cash recyclers, managed services.

*Likelihood:* Continued single-digit annual branch attrition through 2027 is likely on this four-point trend

*Follow-up:* Get K&H's own ATM and deposit-ATM counts — kh.hu is Akamai-blocked (403) to both curl-with-desktop-UA and WebFetch; try MNB payment-statistics tables or a Chrome-session pull of kh.hu/fiokkereso.

### 3. UBB (United Bulgarian Bank), KBC Bulgaria — Bulgaria [L / win Medium / Medium]

KBC reports 170 Bulgarian branches at 30/06/2026 — unchanged from 31/03/2026 and 31/12/2025, but down from 174 at 30/06/2025. UBB's own public locator feed pulled on 27/08/2026 returns 172 offices, of which 34 are flagged 'euro-hub', 5 'cashless service' branches and 5 joint KBC/UBB offices.

*Source:* KBC Group 2Q2026 company presentation + UBB public branch/ATM locator feed — https://ubb.bg/en/locations/pins/desktop:1 (27/08/2026, primary)

*Implies:* UBB has stopped closing branches during the euro changeover and instead created 34 dedicated 'euro hub' sites plus 5 explicitly cashless branches. Cashless branches only work if the cash they displace lands on a machine — direct pull for recyclers/deposit ATMs and assisted self-service. Printec cash automation + ATM/self-service.

*Likelihood:* Medium-High that the cashless-branch format is extended beyond 5 sites once the euro dual-circulation workload subsides

*Follow-up:* Ask UBB how the 5 'cashless-service' branches handle cash today, and whether the 34 euro hubs revert to standard format; re-pull the locator monthly — count changes are themselves the signal.

### 4. UBB (United Bulgarian Bank), KBC Bulgaria — Bulgaria [XL / win Medium / Medium]

Fresh pull of UBB's public locator feed on 27/08/2026 returns 737 ATM sites, of which only 244 carry the 'ATM money deposit' feature (249 are flagged bunch-note-acceptor) and 704 are 24/7. That leaves roughly 490 cash-out-only machines. Against the late-July 2026 baseline of 738 sites / 246 deposit-capable, the fleet is flat: no post-euro recycler rollout has begun.

*Source:* UBB public branch/ATM locator JSON feed (ubb.bg/en/locations/pins/desktop:1) — https://ubb.bg/en/locations/pins/desktop:1 (27/08/2026, primary)

*Implies:* ~490 machines in Bulgaria's second-largest network still cannot take a deposit, one month further into euro operation. Every one is a candidate for recycler upgrade or swap-out, and the deposit-capable share (33%) is the single hardest number in the Bulgarian pipeline. Printec cash recyclers, ATM/self-service, managed services.

*Likelihood:* A recycler upgrade programme in the next 6-12 months is plausible but not yet evidenced; UBB is still absorbing Raiffeisenbank Bulgaria integration costs

*Follow-up:* Re-pull monthly and diff the deposit-capable set; cross-check against BNB payment-infrastructure statistics; ask UBB for its post-euro branch-counter vs deposit-ATM volume split (the BGN 406m vs BGN 2.3bn figures in the previous run were for the first five months of euro operation and need a fresh, primary restatement).

### 5. ČSOB Slovakia (KBC International Markets BU) — Slovakia [M / win Medium / Medium]

ČSOB Slovakia's own published deposit-ATM list, retrieved 27/08/2026, contains 124 deposit-ATM entries at 99 distinct addresses; 66 entries accept coins and notes ('mince a bankovky') and 58 notes only ('bankovky'). KBC separately reports 97 Slovak branches at 30/06/2026 (excluding 365.bank) — i.e. deposit acceptance is almost entirely branch-attached.

*Source:* ČSOB Slovakia — Zoznam vkladových bankomatov (official deposit-ATM list) — https://www.csob.sk/kontakty/pobocky-a-bankomaty/vkladove-bankomaty/zoznam (27/08/2026, primary)

*Implies:* Coin-accepting deposit machines are relatively rare in CEE and point to installed recycler/coin-module hardware nearing refresh; 99 deposit locations against a national footprint is thin off-branch coverage. Printec cash recyclers, ATM/self-service, managed services.

*Likelihood:* Medium — refresh/extension likely to be bundled into the 365.bank integration programme rather than run standalone

*Follow-up:* Establish ČSOB SK's total ATM count (the deposit list is only the deposit subset) and whether 365.bank's Slovak Post-based network carries its own machines.

### 6. ČSOB Slovakia / 365.bank — Slovakia [L / win Low / Medium]

KBC confirms in its 2Q2026 quarterly report that the 98.45% acquisition of 365.bank has closed and is consolidated (EUR 4.4bn carrying value at 30/06/2026; EUR 3,647m added to the Slovak loan portfolio in 1H2026), that the combination targets ~20% market share in Slovak retail mortgages and other customer loans, and that goodwill is justified partly by 'significant cost synergies related to the branch network and head office in Slovakia'. 365.bank's distribution rests on a long-standing partnership with Slovak Post. Integration costs for 365.bank and Business Lease are booked as exceptional opex items in 2Q2026.

*Source:* KBC Group 2Q2026 Quarterly Report, Note 6.6 (business combinations) and exceptional-items slide — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-quarterly-report-en.pdf (06/08/2026, primary)

*Implies:* An explicitly branch-network cost-synergy case means two overlapping estates and two self-service fleets to rationalise, plus a postal-counter channel that has to be brought onto one platform. That is exactly a managed-services / ATM-estate-consolidation and multivendor-software engagement. Printec ATM/self-service, managed services, cash automation, POS.

*Likelihood:* High that a Slovak network and channel rationalisation programme runs through 2026-2027; vendor decisions likely tied to ČSOB/KBC group frameworks

*Follow-up:* Track the integration/migration timetable and whether 365.bank's Slovak Post counters are retained; identify the incumbent ATM vendor on each of the two fleets.

### 7. KBC Group (Kate AI assistant) — Belgium/Czech Republic/Slovakia/Hungary/Bulgaria [M / win Low / Medium]

At 2Q2026 KBC reports Kate has reached 6.2 million customers across its core markets, resolves on average ~75% of customer queries autonomously (77% Belgium, 75% Czech Republic), converted 484,000 leads in the last 12 months, and now displaces a workload equivalent to over 400 full-time commercial employees. KBC states Kate has 'recently been further upgraded in Belgium and the Czech Republic' to Kate 2.0 using an LLM.

*Source:* KBC Group 2Q2026 press release, CEO statement (Johan Thijs) — https://wcmassets.kbc.be/content/dam/kbccom/doc/newsroom/pressreleases/2026/2q2026-pb-en.pdf (06/08/2026, primary)

*Implies:* Kate 2.0 is live only in BE and CZ; Slovakia, Hungary and Bulgaria are still on Kate 1.0. The AI front end raises, not lowers, the need for straight-through fulfilment behind it — remote identity proofing, eKYC and automated document handling. Printec digital onboarding/eKYC and transaction monitoring.

*Likelihood:* High that Kate 2.0 extends to SK/HU/BG within 12 months

*Follow-up:* Watch for a Kate 2.0 launch announcement in K&H (HU) and UBB (BG); those launches are the natural moment for an eKYC/onboarding refresh.

### 8. KBC Group — Belgium/Czech Republic/Slovakia/Hungary/Bulgaria [M / win Medium / Medium]

KBC's non-financial scorecard at 1H2026 shows digital sales of banking products at 60% against a 65% target for 2026, digital sales of insurance at 29% against a 35% target, and a straight-through-processing score of 77% against an 83% target. All three sit below the 2026 target with two quarters left.

*Source:* KBC Group 2Q2026 company presentation, 'KBC's non-financial targets (2023-2026)' — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-company-presentation.pdf (06/08/2026, primary)

*Implies:* Three quantified, publicly committed gaps that must close in 2H2026. The STP and digital-sales gaps are process-automation and remote-identity problems. Printec digital onboarding/eKYC, AML/compliance automation, managed services.

*Likelihood:* High that 2H2026 spend is steered at closing these three metrics

*Follow-up:* Position eKYC/remote-onboarding as the STP lever; the 11/02/2027 investor event will reset these targets — see next signal.

### 9. KBC Group — Belgium/Czech Republic/Slovakia/Hungary/Bulgaria [Unscoped / win Medium / Medium]

KBC announced on 06/08/2026 that it will extend its 4Q/FY2026 results conference call with a topical event on Thursday 11 February 2027 dedicated to the digital transformation of the group, 'leading to new financial and non-financial guidance'.

*Source:* KBC Group 2Q2026 press release, CEO statement — https://wcmassets.kbc.be/content/dam/kbccom/doc/newsroom/pressreleases/2026/2q2026-pb-en.pdf (06/08/2026, primary)

*Implies:* A dated capital-markets-style reset of KBC's distribution and digital strategy. New non-financial guidance normally means new digital-sales/STP/branch-format targets — the moment vendor frameworks for the next cycle get shaped. Printec should be in front of the relevant CIO/COO teams before that date.

*Likelihood:* Certain (announced date); content unknown

*Follow-up:* Diary 11/02/2027; pre-position with ČSOB CZ, K&H and UBB channel teams in 4Q2026.

### 10. UBB (United Bulgarian Bank), KBC Bulgaria — Bulgaria [L / win Medium / Medium]

KBC's 2Q2026 exceptional-items disclosure still carries a Bulgarian line 'BG – Opex – Integration costs Raiffeisenbank Bulgaria', and the group notes a higher contribution to deposit guarantee schemes 'mainly in Bulgaria' in the quarter. Separately, the drag on group net interest income from central-bank minimum reserve requirements fell to -65m EUR in 1H2026 from -88m EUR in 1H2025, which KBC attributes mainly to the euro adoption in Bulgaria.

*Source:* KBC Group 2Q2026 Quarterly Report (p.25) and 2Q2026 company presentation, exceptional items — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-quarterly-report-en.pdf (06/08/2026, primary)

*Implies:* Bulgaria is absorbing two structural programmes at once — Raiffeisenbank Bulgaria integration and the euro changeover. Both are moments when ATM/cash and payment estates get re-platformed, but they also compete for the same budget, which explains the flat recycler count. Printec cash automation, ATM/self-service, managed services.

*Likelihood:* Medium — capex likely freed once RBBG integration costs roll off

*Follow-up:* Confirm the RBBG integration end-date and whether the acquired ATM fleet has been migrated onto UBB's platform.

### 11. KBC Group — Belgium/Czech Republic/Slovakia/Hungary/Bulgaria [M / win Medium / Medium]

KBC upgraded its FY2026 guidance on 06/08/2026 (total income approx. +11.0% y-o-y, NII approx. EUR 7.05bn) while holding organic operating-expense growth to approximately +3.4% y-o-y and targeting a cost/income ratio of approximately 40% with jaws of approximately +3.3%. 1H2026 cost/income was 43% excluding certain non-operating items. Higher ICT costs are named as a driver of both the q-o-q and y-o-y cost increase.

*Source:* KBC Group 2Q2026 company presentation, 'FY26 financial guidance' and opex commentary — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-company-presentation.pdf (06/08/2026, primary)

*Implies:* Revenue rising far faster than costs, with ICT the accepted growth line — the profile that funds automation and outsourced/managed operations rather than headcount. Managed services and as-a-service ATM models fit the stated jaws discipline. Printec managed services.

*Likelihood:* High — cost discipline explicitly guided for FY26

*Follow-up:* Frame ATM/self-service proposals as opex-neutral managed service, not capex.

### 12. KBC Group — Belgium/Czech Republic/Slovakia/Hungary/Bulgaria [M / win Low / Medium]

In its 2Q2026 risk statement KBC names cyber risk as one of the main threats, explicitly citing 'AI-driven vulnerability discovery' from recent frontier-AI developments and heightened threats to large US technology suppliers of critical digital infrastructure to the financial sector, and states it has already acted to increase vigilance and capacity for an expected rise in zero-day vulnerabilities. AML regulation and enhanced consumer protection are named as dominant sector themes.

*Source:* KBC Group 2Q2026 press release, 'Statement of risk' section — https://wcmassets.kbc.be/content/dam/kbccom/doc/newsroom/pressreleases/2026/2q2026-pb-en.pdf (06/08/2026, primary)

*Implies:* A board-level, publicly stated cyber and AML posture across all five core markets. Supports HSM/key-management, endpoint and ATM security hardening, and AML/transaction-monitoring modernisation. Printec HSM/security, AML/compliance, transaction monitoring.

*Likelihood:* High that security and AML budgets are protected in 2H2026

*Follow-up:* Target the group CISO/security function for HSM and ATM-endpoint security; note KBC's own AML tooling is likely group-standardised, so entry is more likely at the ATM/self-service endpoint layer.

### 13. K&H Bank Hungary (KBC International Markets BU) — Hungary [M / win Medium / Medium]

KBC booked a -42m EUR modification loss in Hungary in 2Q2026 arising from the lifetime extension of the interest-rate cap, listed among exceptional items for the International Markets BU, alongside Hungarian NII corrections for a loan interest subsidy and a legal case, and a temporary extra windfall/DGS bank and insurance tax.

*Source:* KBC Group 2Q2026 company presentation, exceptional items — BU International Markets — https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-company-presentation.pdf (06/08/2026, primary)

*Implies:* Regulated margin compression plus extra bank taxes in Hungary is the classic setup for accelerated branch-cost removal and channel automation — consistent with the -5 branches y-o-y already observed. Printec ATM/self-service, cash automation, managed services.

*Likelihood:* Medium-High that Hungarian cost-out accelerates in 2H2026

*Follow-up:* Confirm the Hungarian interest-cap extension's statutory end-date from MNB/Magyar Közlöny; check K&H's own 1H2026 Hungarian-language release for a branch/ATM figure.


## Coverage notes
Fresh run (no checkpoint existed). KBC Group was a genuine blank in the 30/07/2026 run — this is first coverage. WebSearch was unavailable for the entire task: the session's 200/200 web-search budget was already exhausted before my first query, so ALL work was done by direct primary-URL fetching, local PDF text extraction (pdfminer) and locator-API pulls. Angles used: (1) KBC Group IR asset host wcmassets.kbc.be — 2Q2026 quarterly report, 2Q2026 press release and 2Q2026 company presentation, plus the 1Q2026, 4Q2025 and 2Q2025 company presentations pulled specifically to build a four-point branch-count time series (this is the reconciliation the baseline said had never been done: BE 427/424/421/420, CZ 197/197/197/196, SK 97/97/97/97 excl 365.bank, HU 193/191/189/188, BG 174/170/170/170 at 30/06/2025, 31/12/2025, 31/03/2026, 30/06/2026). (2) UBB Bulgaria's undocumented public locator JSON (GET https://ubb.bg/en/locations/pins/desktop:1 — POST is 411-blocked at the Akamai edge; GET works) re-pulled 27/08/2026 and parsed by feature slug, which both re-verifies and slightly revises the late-July baseline (738->737 ATM sites, 246->244 deposit-capable) and surfaces new branch-format detail (34 euro-hub, 5 cashless-service, 5 joint KBC/UBB offices). (3) ČSOB Slovakia's official published deposit-ATM table (HTML table scraped and counted: 124 rows, 99 distinct addresses, 66 coin+note vs 58 note-only). GENUINE GAPS: KBC Group discloses NO ATM or self-service figures anywhere in its 2Q2026 quarterly report, press release or company presentation — 'ATM' does not appear once in any of the three documents. Any KBC-market fleet number must therefore be built bottom-up from local-entity locators or central-bank statistics; there is no group-level figure to reconcile country data against. Czech Republic is the main hole: ČSOB CZ ATM/deposit-ATM counts, the four-bank Czech shared ATM network progress and ČSOB's H1-2026 local release could not be obtained (see access_issues). Hungary (K&H) locator likewise unobtained. Bulgarian post-euro branch-counter vs deposit-ATM volume split was not restated this run — the BGN 406m / BGN 2.3bn figures from the previous run are NOT carried forward here. No Croatian/Serbian exposure applies to KBC. Source catalogue A1 covers Bulgaria; the UBB locator route used here is fresher and machine-readable, so it was preferred.

## Access issues
BLOCKED, with the route actually attempted logged for each: (1) https://www.csob.cz/pobocky-bankomaty , /o-nas , /tiskove-zpravy , /o-nas/vysledky-hospodareni , /sitemap.xml — all return a ~5-7KB JS bot-challenge shell to curl with a desktop Chrome User-Agent AND full navigate headers, and HTTP 500 to WebFetch. csob.cz is comprehensively bot-walled; no primary Czech figure could be extracted. (2) https://api.csob.cz/webapi/api/general/v1/atms and /branches — HTTP 500 GATEWAY_INTERFACE_EXCEPTION policyResult 'Falsified' (API key required); https://api.csob.cz/api/general/v1/atms — 403. (3) https://www.kh.hu/fiokkereso and https://www.kh.hu/en/about-us — HTTP 403 Akamai 'Access Denied' to both desktop-UA curl (with hu-HU Accept-Language) and WebFetch. (4) https://www.csob.sk/pobocky-bankomaty — intermittently served ČSOB's own 'Ľutujeme, stránka je momentálne nedostupná' error page; the deposit-ATM sub-page /kontakty/pobocky-a-bankomaty/vkladove-bankomaty/zoznam did resolve and was used. (5) https://ubb.bg/en/locations/pins/desktop:1 via POST — HTTP 411 at the Akamai edge; GET succeeds (this is the working route). (6) https://www.ubb.bg/en/about-us/news and https://ubb.bg/en/about/news — 404; UBB's news index path not found. (7) ESCALATION TO CLAUDE-IN-CHROME ATTEMPTED AND UNAVAILABLE: mcp__claude-in-chrome__list_connected_browsers returned an empty list — no Chrome extension instance is connected to this account, so the prescribed final fallback for csob.cz and kh.hu could not be executed. (8) WebSearch: 200/200 session budget already consumed before this task began; zero searches available.

## Operator requests
1) Run csob.cz in a real browser session (Claude-in-Chrome or manual) and capture: total ČSOB CZ ATM count, deposit/recycling ATM count, and the H1-2026 Czech results press release — csob.cz is fully bot-walled to headless fetchers. 2) Same for kh.hu/fiokkereso (K&H Hungary branch/ATM locator) — Akamai 403 to all non-browser routes. 3) Obtain a ČSOB CZ PSD2/open-banking API key if one is issuable, to unlock https://api.csob.cz/webapi/api/general/v1/atms (currently 'Falsified' policy result). 4) Raise CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION — this task ran with zero web searches available, which is the single largest constraint on discovery breadth here. 5) If available, pull the Czech Banking Association / CNB statistics on the four-bank shared ATM network to close the Czech gap independently of csob.cz.
