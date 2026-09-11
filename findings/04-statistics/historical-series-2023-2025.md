# Historical series 2023–2025 — Agent 4 reference dataset

**Compiled:** 2026-06-12 | **Companion to:** `2026-06-12.md`
**Sources:** ECB Data Portal API (PTN = terminal counts, half-yearly; SSI = bank offices, annual), pulled 2026-06-12; NBS and NBU figures from their official releases/press citing them. Every figure below is as published — no interpolation or estimates.
**Caveats:** 2025-S1 ECB values are provisional ("P"). Known series breaks flagged per country. POS counts can include multi-acquiring double counting.

## 1. ATMs — half-yearly (ECB PTN, terminals provided by resident PSPs)

Source: [ECB PTN ATM series, all 10 EU footprint countries](https://data-api.ecb.europa.eu/service/data/PTN/H.GR+CY+AT+HR+SI+SK+BG+RO+HU+CZ.W0.2221._T.PN?format=csvdata&startPeriod=2023)

| Country | 2023-S1 | 2023-S2 | 2024-S1 | 2024-S2 | 2025-S1 (prov.) | 2-yr change (S1'23→S1'25) | Reading |
|---|---|---|---|---|---|---|---|
| Greece | 6,161 | 6,165 | 6,032 | 6,260 | **7,104** | **+15.3%** | Decline reversed sharply in 2024-S2 → deployment wave underway |
| Hungary | 4,535 | 4,563 | 5,033 | 5,140 | **5,378** | **+18.6%** | Steady climb since 2024 — ATM mandate effect; national data show >5,500 by Dec 2025 |
| Romania | 10,244 | 10,229 | 10,229 | 10,242 | 10,028 | −2.1% | Flat for 2 years, then BNR reports 11,136 at end-2025 (+1,108 in H2'25) — expansion is new |
| Bulgaria | 5,114 | 5,159 | 5,102 | 5,121 | 5,103 | −0.2% | Stable through euro prep; post-changeover rationalisation is the thing to watch |
| Czechia | 5,197 | 5,088 | 5,092 | 5,034 | 5,004 | −3.7% | Slow steady shrink → consolidation/replacement market |
| Slovakia | 3,231 | 3,314 | 3,309 | 3,277 | 3,346 | +3.6% | Mildly growing |
| Austria | 13,847 | 13,456 | 13,084 | 13,388 | 13,215 | −4.6% | Slow decline from high density |
| Slovenia | 1,274 | 1,309 | 1,297 | 1,284 | 1,273 | −0.1% | Flat |
| Croatia | 5,325 | 4,277 | 5,124 | 3,978 | 4,509 | −15.3%* | *ECB series noisy — RESOLVED with HNB primary data: official end-year ATM counts 4,894 (2020) → 4,692 (2021) → 4,184 (2022) → 4,277 (2023) → **3,978 (2024, −7.0% y/y)**. Fleet genuinely shrinking; only 48% (1,926) contactless-capable; 1,132 under video surveillance, 677 in secure locations; EFTPOS 142,354 ([HNB "Payment Cards and Card Transactions 2024"](https://www.hnb.hr/c/document_library/get_file?uuid=5a268502-3a88-07f7-cf4e-fcb33627ac2a&groupId=20182)) |
| Cyprus | 401 | 398 | 397 | 398 | 405 | +1.0% | Flat |
| **Euro area (U2)** | 264,225 | 261,251 | 256,692 | 251,804 | 249,281 | **−5.7%** | Structural decline ~3%/yr — replacement + pooling pressure ([U2 series](https://data-api.ecb.europa.eu/service/data/PTN/H.U2.W0.2221+2222._T.PN?format=csvdata&startPeriod=2023)) |

## 2. POS terminals — half-yearly (ECB PTN)

Source: [ECB PTN POS series](https://data-api.ecb.europa.eu/service/data/PTN/H.BG+RO+HU+CZ+GR+CY+AT+HR+SI+SK.W0.2222._T.PN?format=csvdata&startPeriod=2023)

| Country | 2023-S1 | 2023-S2 | 2024-S1 | 2024-S2 | 2025-S1 (prov.) | 2-yr change | Reading |
|---|---|---|---|---|---|---|---|
| Romania | 408,315 | 447,292 | 490,174 | 529,862 | **568,012** | **+39.1%** | Fastest-growing estate in footprint; BNR reports 729,408 at end-2025 — acceleration |
| Slovakia | 133,501 | 143,260 | 159,126 | 171,839 | **182,225** | **+36.5%** | Consistent double-digit growth |
| Bulgaria | 359,903* | 148,882 | 162,981 | 173,232 | 195,577 | +31.4% (vs S2'23) | *2023-S1 value is a series break (double-counting correction); growth from S2'23 is real and strong |
| Greece | 1,091,815 | 1,184,025 | 1,207,077 | 1,324,916 | **1,350,906** | +23.7% | Huge estate (incl. soft-POS); IRIS mandate now forces software upgrades across it |
| Croatia | 131,423 | 133,299 | 140,848 | 144,948 | 154,407 | +17.5% | Steady tourism-driven growth |
| Slovenia | 41,150 | 42,552 | 43,637 | 47,235 | 47,092 | +14.4% | Steady |
| Czechia | 246,351 | 254,298 | 266,179 | 268,142 | 276,858 | +12.4% | Steady |
| Hungary | 280,812 | 285,795 | 299,543 | 305,266 | 307,086 | +9.4% | Moderate; qvik QR acceptance may shift the mix |
| Austria | 160,964 | 159,861 | 156,852 | 152,063 | 165,912 | +3.1% | Dip through 2024, rebound in 2025-S1 |
| Cyprus | 133,728 | 142,532 | 152,674 | 151,399 | 106,311* | −20.5%* | *2025-S1 drop of ~30% vs prior period looks like a reporting break — verify with Central Bank of Cyprus before using |
| **Euro area (U2)** | 18.51m | 19.13m | 19.96m | 20.60m | 24.74m | **+33.7%** | Includes double counting + soft-POS proliferation; direction is unambiguous |

## 2b. Cash withdrawals using cards — half-yearly, millions of transactions (ECB PAY, series CW1)

Source: [ECB PAY CW1 series](https://data-api.ecb.europa.eu/service/data/PAY/H.GR+CY+AT+HR+SI+SK+BG+RO+HU+CZ.W0.CW1.1._Z.N.PN?format=csvdata&startPeriod=2023), pulled 2026-06-12. Resolves the earlier "cash trend n/a" entries.

| Country | 2023-S1 | 2023-S2 | 2024-S1 | 2024-S2 | 2025-S1 (prov.) | 2-yr change | Reading |
|---|---|---|---|---|---|---|---|
| Romania | 128.2 | 133.1 | 129.3 | 131.3 | 128.9 | **+0.5% — flat** | Cash withdrawals NOT declining while POS grows +39% → cash resilient in absolute terms = recycler demand strongest here |
| Croatia | 46.4 | 48.0 | 47.2 | 47.1 | 45.0 | −3.0% | Mildest decline after RO — tourism cash economy |
| Austria | 103.0 | 107.8 | 101.9 | 105.3 | 97.0 | −5.9% | Slow erosion from a high base |
| Greece | 65.3 | 66.1 | 63.3 | 66.0 | 61.0 | −6.6% | Withdrawals falling while ATMs +17.8% → more machines chasing fewer withdrawals = deployment is deposit/offsite/IAD-driven, not withdrawal-driven |
| Slovenia | 23.3 | 23.9 | 22.8 | 22.7 | 21.4 | −7.9% | Steady decline |
| Bulgaria | 69.0 | 69.4 | 67.3 | 65.3 | 62.9 | −8.8% | Falling pre-changeover; watch post-euro behaviour |
| Hungary | 44.8 | 45.4 | 43.4 | 43.4 | 40.6 | −9.4% | Withdrawals down while ATM fleet mandated to GROW → rural ATMs will run low volumes = outsourcing/low-cost ops pitch |
| Slovakia | 37.3 | 38.4 | 36.1 | 36.5 | 33.5 | −10.1% | Faster decline |
| Czechia | 77.8 | 80.2 | 74.8 | 76.3 | 68.2 | −12.3% | Confirms ČNB commentary; utilisation pressure on flat fleet |
| Cyprus | 7.70 | 7.90 | 7.27 | 7.37 | 6.71 | −12.9% | Fastest cash decline in footprint |

## 3. Bank branches (offices) — annual (ECB SSI, credit institutions)

Source: [ECB SSI series](https://data-api.ecb.europa.eu/service/data/SSI/A.GR+CY+AT+HR+SI+SK+BG+RO+HU+CZ.122C.N40.1.A1.Z0Z.Z?format=csvdata&startPeriod=2023); EU aggregate from [ECB press release 2026-06-12](https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260612~ab34769159.en.html)

| Country | 2023 | 2024 | 2025 | 2-yr change | Reading |
|---|---|---|---|---|---|
| Bulgaria | 5,088 | 5,171 | 4,542 | **−10.7%** | All of the cut came in 2025 (euro-prep year) — sharpest consolidation in EU |
| Slovenia | 410 | 374 | 365 | −11.0% | Front-loaded in 2024 |
| Hungary | 1,436 | 1,401 | 1,300 | −9.5% | Accelerating (−2.4% then −7.2%) while ATMs grow — classic channel-shift |
| Romania | 3,549 | 3,495 | 3,288 | −7.4% | Accelerating (−1.5% then −5.9%) |
| Czechia | 1,366 | 1,309 | 1,272 | −6.9% | Steady |
| Slovakia | 910 | 882 | 850 | −6.6% | Steady |
| Greece | 1,414 | 1,387 | 1,352 | −4.4% | Slow grind down; self-service absorbs the load |
| Austria | 3,185 | 3,140 | 3,046 | −4.4% | Steady |
| Cyprus | 198 | 193 | 193 | −2.5% | Bottomed out |
| Croatia | 799 | 784 | 792 | −0.9% | Only footprint country to ADD branches in 2025 |
| **EU total** | — | — | 122,889 | −2.62% in 2025 | Decline in 23 of 27 member states |

## 4. Serbia — national series (NBS)

| Indicator | End-2023 | End-2024 | 2025 (latest) | Source |
|---|---|---|---|---|
| ATMs | (base year) | 3,218 (+4.5% y/y) | 3,197 at end-Sep 2025 (−0.4% y/y) | [NBS mid-2025 release](https://www.nbs.rs/sr/scripts/showcontent/index.html?id=20429); [Tanjug citing NBS](https://www.tanjug.rs/ekonomija/srbija/223428/narodna-banka-srbije-u-trecem-tromesecju-2025-ips-platni-sistem-obradio-273-miliona-instant-placanja/vest) |
| POS solutions | (base year) | >160,000 (+17.7% y/y) | >180,000 active at end-Q3 2025 (+17% y/y) | same NBS releases |
| IPS instant payments (volume) | — | value +45.5% vs 2023; 4 daily records broken (peak 444,994 on 15 Nov 2024) | 109.3m payments in 2025 (+~25% y/y; 4.4× the 25.1m of 2020), value RSD 1.4tn | [Biznis.rs citing NBS](https://biznis.rs/novac/banke/instant-placanja-u-srbiji-porasla-za-cetvrtinu-u-2025/) |

Reading: two consecutive years of ~17–18% POS growth = sustained acquiring/terminal demand; ATM fleet plateaued in 2025 after 2024 growth → watch for replacement-cycle tenders; IPS compounding ~25–45%/yr → fraud-monitoring need grows with it. SEPA accession (ORD May 2026) adds scheme-integration work.

## 5. Ukraine — national series (NBU)

| Indicator | End-2023 | End-2024 | 2025 (latest) | Source |
|---|---|---|---|---|
| Operating ATMs | 15,800 (+~2% y/y) | 15,700 (≈flat) | 15.6k at Sep 2025 (−0.6% YTD) | [NBU 2023 release](https://bank.gov.ua/en/news/all/drugiy-rik-povnomasshtabnoyi-viyni-obsyagi-bezgotivkovih-rozrahunkiv-zrostayut); [NBU 2024 release](https://bank.gov.ua/en/news/all/bezgotivkovi-rozrahunki-u-2024-rotsi-suttyevo-perevajali-sered-operatsiy-z-platijnimi-kartkami); [Mezha citing NBU](https://mezha.net/eng/bukvy/ukraine-s-cashless-payment-card-transactions-rise-11-7-in-2025/) |
| Payment terminals (retail) | 449,500 (+25.1% y/y) | 496,600 (+10.5% y/y; 97.5% contactless) | 558,600 (+12.5% in 2025; ~85% contactless) | same NBU releases |
| Cashless share of card txns (count) | — | dominant (2024 release) | 95.5% in 2025 | same |
| Bank branches (operating) | 5,138 at 1 Jan 2024 (i.e., end-2023; −198 in 2023) | ~5,032 at 1 Jan 2025 | 4,934 at 1 Oct 2025 (−98 YTD); 744 more "temporarily suspended" | [RBC-Ukraine citing NBU, Oct 2025](https://www.rbc.ua/rus/news/minus-100-pochatku-roku-ukrayinski-banki-1760425258.html), [Jan 2025](https://www.rbc.ua/rus/news/ukrayinski-banki-rik-skorotili-ponad-100-1736508087.html) — found via Ukrainian-language search |

Reading: ATM fleet has been remarkably stable (~15.6–15.8k) through three war years — banks are maintaining, not expanding → service/security/parts demand. Terminal estate grew ~24% over two years → sustained POS demand even in wartime.

## 6. Cross-country picture, 2023→2025 (two-year view)

- **ATM expansion markets:** Hungary (+18.6%, mandate-driven), Greece (+15.3%, offsite wave), Romania (flat then +1,108 in H2'25). These three are where new-unit and managed-services money is moving now.
- **ATM stable markets (replacement/recycling pitch):** Bulgaria, Slovenia, Cyprus, Slovakia, Serbia, Ukraine.
- **ATM decline markets (consolidation/pooling pitch):** euro area overall (−5.7%), Austria, Czechia.
- **POS growth is universal** — every footprint country except break-affected Cyprus grew, with RO/SK/BG >30% in two years.
- **Branches fell everywhere except Croatia**, with the steepest cuts coming in the most recent year (BG −12.2%, HU −7.2%, RO −5.9% in 2025) — the channel-shift to self-service is accelerating, not slowing.

## 5b. Western Balkans — what the local-language sweep recovered

| Country | Indicator | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| Kosovo | ATMs | 534 | 583 (+9.2%) | n/a yet | n/a yet | [CBK card-usage report](https://bqk-kos.org/wp-content/uploads/2025/01/Use-of-bank-cards-in-Kosovo-2023-FINAL.pdf) |
| Kosovo | POS transactions | — | (base) | +43% y/y | n/a yet | [CBK NPC minutes](https://bqk-kos.org/wp-content/uploads/2025/06/ENG_Minutat-e-takimit-te-KKP_Final_17062025.pdf?lang=en) |
| Albania | Deposit-enabled ATMs | — | — | ~394 (derived base) | 430 (+9%) | [Monitor.al citing Bank of Albania](https://monitor.al/depozitimet-automatike-te-parase-ne-atm-u-rriten-me-110-ne-2025/) |
| Albania | POS terminals | — | — | ~24,500 (stated +27.7% to 31,263) | 31,263 | [Monitor.al](https://monitor.al/pagesat-me-karte-arriten-rekord-te-ri-ne-2025-per-here-te-pare-kaluan-terheqjet-cash-ne-atm/) |
| N. Macedonia | Cashless transactions | — | — | ~232m (base for +7.1%) | 249m | [Plusinfo citing NBRNM](https://plusinfo.mk/lani-se-napraveni-249-milioni-bezgotovinski-platezhni-transakcii-pove-e-od-71-od-pla-a-ata-se-izvrsheni-preku-elektronski-uredi/) |
| BiH | Payment-system transactions | — | 50.8m / KM 163.1bn | n/a yet | n/a yet | [CBBH](https://cbbh.ba/content/read/915) — portal pull needed |
| Montenegro | All payment indicators | — | — | — | — | [CBCG portal](https://www.cbcg.me/me/statistika) — no press-release figures; portal pull needed |

Notes: "~" values are the published bases implied by the cited y/y percentages, shown only for orientation — use primary tables before quoting. Czechia ATM history is in Section 1 (ECB PTN); ČNB commentary confirms ~5.0k with multi-year mild decline and H1 2025 withdrawal counts slightly down ([Kurzy.cz citing ČNB](https://zpravy.kurzy.cz/842378-pocet-vetsiny-typu-odeslanych-plateb-se-pravidelne-zvysuje-pocty-vyberu-hotovosti-mirne-poklesly/)).

## Gaps (not available in this compilation — no figures invented)

- Pre-2023 history (playbook asked 2 years; deeper history available from same ECB series on demand).
- Serbia end-2023 absolute ATM/POS counts (only y/y % published) and exact branch counts — NBS quarterly Banking Sector Report ([nbs.rs reports page](https://www.nbs.rs/sr/finansijske-institucije/banke/izvestaji-i-analize/)); web search in Serbian didn't surface the figures, the report PDFs must be opened directly. Secondary cross-check: [EY Serbia Banking Sector Pulse 2025 PDF](https://www.ey.com/content/dam/ey-unified-site/ey-com/sr-rs/insights/strategy-transactions/documents/ey-serbia-banking-sector-pulse-2025.pdf).
- BiH: CBBH aggregate ATM/POS counts sit behind a login-gated statistics dashboard (Panorama Necto) — not web-fetchable; next-best: CBBH Quarterly Bulletin PDFs and banking-agency (FBA/ABRS) quarterly reports.
- Montenegro: CBCG publishes monthly RTGS/DNS system transaction stats (e.g., Jun 2025: 1.38m transactions, €2.43bn) but no terminal counts in releases — CBCG annual payment-system report PDF is the route.
- ~~Cash-withdrawal volumes per country~~ — **RESOLVED**: ECB PAY series key is `CW1` (PAY.H.<cc>.W0.CW1.1._Z.N.PN); full table now in Section 2b.
- ~~Croatia noisy ATM series~~ — **RESOLVED** with HNB primary publication (see Section 1 note).
