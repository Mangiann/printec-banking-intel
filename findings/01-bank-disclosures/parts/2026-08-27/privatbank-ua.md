# PrivatBank (Ukraine) - bank disclosure findings, run 2026-08-27

**Slug:** `privatbank-ua` | **Status:** complete | **Signals:** 17

## Headline

- Printec Ukraine LLC (EDRPOU 35442628) is confirmed by primary contract record as supplier of the **1,140 NCR recyclers** (800 SelfServ 2062 + 340 SelfServ 2064), UAH 838,639,173.73 incl. VAT, awarded 17/01/2025, delivered by 30/11/2025.
- **Correction:** there is no separate '800-unit 2026 lot'. The 800 units are a line inside that 2025 award. Zero new ATM/recycler hardware tenders in 2026.
- Printec also won **39,000 Castles Android POS** terminals (UAH 151.7m, 25/10/2025) - but lost ~57,810 portable POS to **Newland direct**.
- Fleet denominator from the bank's own 2025 annual report: **7,310 ATMs / 10,053 TSO / 345,234 POS / 1,055 branches**. Recycler penetration ~15.6%.
- Earliest replacement-cycle indicator: **1,000 technical-condition/defect assessments** of self-service equipment commissioned 03/08/2026.

## Signals

### 1. PrivatBank (Ukraine)

**Signal.** Prozorro award UA-2025-01-17-010779-a: PrivatBank contracted 1,140 NCR recycling ATMs in a single negotiated (Art.35 p.3 urgent-need) award dated 17/01/2025 - 800 x NCR SelfServ 2062 and 340 x NCR SelfServ 2064 - for UAH 838,639,173.73 incl. VAT (UAH 698,865,978.11 net), delivery deadline 30/11/2025. Winner: TOV 'PRINTEC UKRAINE EL.EL.SI.' (EDRPOU 35442628).

**Implies.** Primary-source proof of Printec's ATM/self-service and cash-recycling incumbency at PrivatBank, and the exact composition of the '1,140 recyclers' figure. Recyclers are ATMs that re-dispense notes customers deposit, so one machine does both cash-in and cash-out. Delivery completed 30/11/2025 means the whole fleet enters warranty expiry and managed-service renewal from late 2026 - Printec managed services and spare-parts/SLA renewal.

| | |
|---|---|
| Source | Prozorro CDB (public API), tender UA-2025-01-17-010779-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/91535417b84240648f1dabd4a3fd1e22 |
| Date | 17/01/2025 | 
| Tier | primary |
| Likelihood | Very high that a post-deployment service/warranty renewal decision falls due within 6-12 months |
| Opp size / Win | XL / High |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Obtain the signed contract annex (Dodatok do Dogovoru.pdf attached to the tender) to read the warranty term and SLA; then pitch the multi-year managed-service wrap before warranty lapse.

---

### 2. PrivatBank (Ukraine)

**Signal.** CORRECTION to prior brief: there is NO separate '800-unit 2026 recycler lot'. The 800 units are the NCR SelfServ 2062 line inside the single 17/01/2025 award; an exhaustive sweep of all 1,153 PrivatBank tenders published on Prozorro (search term 'tender.privatbank.ua', run 27/08/2026) returns zero new ATM or recycler hardware purchases dated 2026 - only spare parts, cassettes, cash-in-transit and consumables.

**Implies.** The hardware replacement cycle is currently PAUSED, not running. Printec should not plan 2026 revenue on a new box lot; the live money is in spares, service and the cash-cycle software layer. It also means a competitor cannot displace Printec on hardware this year - the contest is over service.

| | |
|---|---|
| Source | Prozorro search API, full enumeration of PrivatBank (EDRPOU 14360570) tenders |
| URL | https://prozorro.gov.ua/api/search/tenders |
| Date | 27/08/2026 | 
| Tier | primary |
| Likelihood | High that the next ATM hardware lot is a 2027 event |
| Opp size / Win | Unscoped / — |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Set a Prozorro watch on CPV 30123200-9 (Bankomaty) for EDRPOU 14360570 to catch the next lot the day it publishes.

---

### 3. PrivatBank (Ukraine)

**Signal.** Prozorro award UA-2026-08-03-004344-a dated 03/08/2026: PrivatBank bought expert technical-condition assessments for self-service equipment - 700 'technical condition acts' plus 300 'defect lists' - for UAH 178,000, performed by TOV 'RENOME-SMART' (EDRPOU 32625525), running to 26/07/2027.

**Implies.** Commissioning ~1,000 formal condition/defect reports on self-service machines is the standard Ukrainian precursor to write-off and replacement of an ageing fleet. This is the earliest dated indicator that a NEW ATM/self-service replacement tender is being prepared, and it lands inside the August-2026 window. Printec ATM/self-service plus managed services.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2026-08-03-004344-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/6429a2fb6a5d4bee97032125404300f8 |
| Date | 03/08/2026 | 
| Tier | primary |
| Likelihood | Medium-high that a replacement or refurbishment lot follows within 6-12 months |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Engage PrivatBank's self-service engineering team now, before the specification is written, and offer refurbishment/trade-in economics against the 1,000 machines being assessed.

---

### 4. PrivatBank (Ukraine)

**Signal.** Diebold Nixdorf is an entrenched second ATM vendor at PrivatBank. Prozorro award UA-2025-12-15-023134-a (15/12/2025, UAH 13,192,718.10) and UA-2026-05-19-000673-a (19/05/2026, UAH 2,119,470) both went to TOV 'DIBOLD NIKSDORF' (EDRPOU 36353398) for CRS/RM3 recycler modules, Wincor L2.1-H81-mATX motherboards and CINEO C4040/C4560 monitors.

**Implies.** Printec's incumbency is not exclusive: a legacy Diebold Nixdorf/Wincor CINEO recycler estate is being kept alive with spare parts, and DN sells to PrivatBank directly through its Ukrainian entity. That legacy estate is the natural displacement target for Printec-supplied NCR recyclers, and its parts spend is a managed-service opportunity Printec is currently not capturing.

| | |
|---|---|
| Source | Prozorro CDB, tenders UA-2025-12-15-023134-a and UA-2026-05-19-000673-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/32a9432070494feb91a8c4bd2c72c039 |
| Date | 19/05/2026 | 
| Tier | primary |
| Likelihood | High - parts purchases recur roughly every 6 months |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Size the DN CINEO estate from the parts quantities (e.g. 70 Transfer Unit Safe 2 CRS modules, 60 customer-tray modules) and build a like-for-like swap-out business case.

---

### 5. PrivatBank (Ukraine)

**Signal.** Prozorro award UA-2026-06-15-012172-a dated 15/06/2026: 1,500 cash-dispense cassettes explicitly specified 'for ATMs manufactured by Diebold Nixdorf (Wincor Nixdorf)', UAH 7,211,025, won by TOV 'SERVUS SYSTEMS INTEGRATION' (EDRPOU 31089403), delivery to 13/06/2027. Companion lots the same reference bought CMD-V4 clamps (UA-2026-08-27-002880-a, UAH 5,940,000, 27/08/2026) and limb locks.

**Implies.** A 1,500-cassette order plus CMD-V4 clamps confirms the Wincor/DN CMD-V4 dispenser estate is still large and actively maintained - CMD-V4 is a cash-out-only dispenser, i.e. these are NOT recyclers. Quantified white space for converting cash-out-only machines to Printec recyclers.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2026-06-15-012172-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/1ce3f54d48204cbabe50420617785ca2 |
| Date | 15/06/2026 | 
| Tier | primary |
| Likelihood | High |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Cross-reference the 1,500-cassette and clamp volumes against the 1,140 recyclers delivered to estimate how much of the fleet is still dispense-only.

---

### 6. PrivatBank (Ukraine)

**Signal.** Printec Ukraine also holds PrivatBank's POS hardware: Prozorro award UA-2025-10-25-000676-a dated 25/10/2025 gave TOV 'PRINTEC UKRAINE EL.EL.SI.' 39,000 Castles Saturn 1000 S1F3CT stationary Android POS terminals with HAL API software for UAH 151,734,960 incl. VAT, delivery by 20/02/2026.

**Implies.** Printec's PrivatBank relationship spans both ATM and POS/acquiring estates, and the bank standardises on an Android POS platform with a HAL API (a hardware-abstraction layer that lets the bank run its own app across different terminal makes). That HAL API standard is the strategic hook - whoever supplies it controls terminal choice. Printec POS/acquiring and managed services.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2025-10-25-000676-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/1a3b2546398a40f8a0e6afef92129d8d |
| Date | 25/10/2025 | 
| Tier | primary |
| Likelihood | High - 39,000 units delivered Feb 2026 need estate management now |
| Opp size / Win | XL / High |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Convert the 39,000-unit delivery into a terminal-estate-management/TMS managed service before the bank builds it in-house.

---

### 7. PrivatBank (Ukraine)

**Signal.** COMPETITIVE LOSS: Newland Payment Technology (H.K.) Company Limited won PrivatBank's portable Android POS business DIRECTLY, without a local integrator - 37,810 Newland N950 units for USD 2,797,561.90 on 04/11/2025 (UA-2025-11-04-015711-a) and a further 20,000 units for USD 2,180,000 on 11/06/2026 (UA-2026-06-11-013572-a), the latter delivering by 08/09/2026.

**Implies.** A tier-1 Asian OEM is selling direct into Printec's largest CEE/SEE bank account and has now repeated the win, taking ~57,810 portable terminals across two awards. Printec keeps the stationary POS line but is being squeezed out of portable. Defensive priority for Printec POS/acquiring.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2026-06-11-013572-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/7805262bd1e84268bffdbbfd978766ea |
| Date | 11/06/2026 | 
| Tier | primary |
| Likelihood | High that a third Newland lot follows in 2027 |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Build a value case Newland cannot match on price alone - estate management, key injection, PCI compliance and field service - and target the next portable refresh.

---

### 8. PrivatBank (Ukraine)

**Signal.** HSM refresh under way. PrivatBank bought 3 Thales payShield 10000 units (PS10-RPM-X Premium, 2500 cps) for EUR 282,450 from Apius Technologies SA on 23/05/2026 (UA-2026-05-23-000548-a); 2 more payShield 10000 units (PS10-RPM-L, 25 cps) plus 6 remote-management readers and a smart-card set for UAH 4,282,350 from TOV 'IT PARK' on 26/06/2026 (UA-2026-06-26-006043-a); and support renewals of EUR 130,526.31 (01/05/2026) and UAH 3,919,068 for three serial-numbered units (26/11/2025).

**Implies.** PrivatBank is still buying and renewing support on payShield 10000, a platform Thales has been succeeding with payShield 10K. An HSM is the tamper-proof box that guards PIN and card keys. The bank is buying HSMs piecemeal from at least two different resellers (Apius, IT Park), which means no single partner owns the security estate. Direct fit for Printec HSM/security and managed services.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2026-05-23-000548-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/5ab4aff25a384d5392c8f19d9a5a16ea |
| Date | 23/05/2026 | 
| Tier | primary |
| Likelihood | High - purchases in three consecutive quarters |
| Opp size / Win | M / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Approach with a consolidated payShield estate refresh plus managed key-management service, positioned against the fragmented reseller pattern.

---

### 9. PrivatBank (Ukraine)

**Signal.** Prozorro award UA-2026-07-03-004713-a dated 03/07/2026: PrivatBank engaged TOV 'McKinsey & Company Ukraine' (EDRPOU 34818665) for EUR 295,900 to run an external maturity assessment of its compliance, financial-monitoring (AML) and risk-management functions, deliverable by 07/08/2026.

**Implies.** A board-level, externally-benchmarked AML maturity review completed in August 2026 almost always produces a remediation roadmap with technology line items - transaction monitoring, screening, case management. The report landed inside this reporting window, so the budget cycle it feeds is the 2027 plan being written now. Printec AML/compliance and transaction monitoring.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2026-07-03-004713-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/c87029125f8b401f8ee3aa1337ae4694 |
| Date | 03/07/2026 | 
| Tier | primary |
| Likelihood | High that AML technology gaps become funded projects within 6-12 months |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Time an AML/transaction-monitoring approach to PrivatBank's 2027 budget build (Sep-Nov 2026), referencing the McKinsey maturity review as the trigger.

---

### 10. PrivatBank (Ukraine)

**Signal.** Prozorro award UA-2026-05-19-000121-a dated 19/05/2026: PrivatBank purchased 500 TEST licences of 'VerifEye' for UAH 264,000, valid to 05/05/2027.

**Implies.** A 500-seat TEST licence is a pilot, not a rollout - the classic 12-month window in which an incumbent can still be displaced before the production tender. The product name and the size point to an identity-verification/screening pilot, adjacent to Printec digital onboarding/eKYC. Treat the product's exact function as unconfirmed until the technical annex is read.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2026-05-19-000121-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/413e079c01764df483576f0c6f5d45f1 |
| Date | 19/05/2026 | 
| Tier | primary |
| Likelihood | Medium that a production licence tender follows within 12 months |
| Opp size / Win | M / Low |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Confirm what VerifEye does and who the vendor behind FOP Bauer L.O. is, then position Printec eKYC/onboarding against it before the pilot converts.

---

### 11. PrivatBank (Ukraine)

**Signal.** Self-service consumables and validator spend confirms a large non-recycling terminal (TSO) estate: Prozorro award UA-2025-12-13-001452-a dated 13/12/2025, UAH 73,114,042.08 to TOV 'TK MAITEK' (EDRPOU 37674571), covering 1,500 assembled '1200' bill acceptors, 500 CUSTOM VKP80III printers and tens of thousands of MEI validator gears/rollers, delivery to 10/12/2026.

**Implies.** A UAH 73m one-year spend on MEI/CPI bill-acceptor and receipt-printer parts is the signature of an ageing cash-in terminal fleet being repaired rather than replaced - 1,500 replacement bill acceptors is a very large number. This is the strongest quantified case for a Printec cash-automation/recycler upgrade proposal, framed as parts spend avoided.

| | |
|---|---|
| Source | Prozorro CDB, tender UA-2025-12-13-001452-a |
| URL | https://public-api.prozorro.gov.ua/api/2.5/tenders/0f0375309de649ada6ac8537f1c31f30 |
| Date | 13/12/2025 | 
| Tier | primary |
| Likelihood | High - recurs annually |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Model total-cost-of-ownership: annual MEI parts spend vs. replacing the oldest TSO cohort with recyclers.

---

### 12. PrivatBank (Ukraine)

**Signal.** PrivatBank 2025 Integrated (Annual) Report, published on privatbank.ua: network at end-2025 was 1,055 branches, 7,310 ATMs, 10,053 self-service terminals (TSO) and 345,234 POS terminals, with 17,100 staff. The report's narrative section gives slightly different ATM/TSO counts on the same reporting date - 7,338 ATMs and 10,086 TSO - so treat 7,310/10,053 as the infographic figure and 7,338/10,086 as the narrative figure.

**Implies.** This is the denominator Printec needs. The 1,140 recyclers Printec delivered represent only about 15.6% of a 7,310-machine ATM fleet, so roughly 6,170 ATMs are still cash-dispense-only, plus a separate 10,053-unit self-service terminal estate. That is the single largest quantified cash-recycling white space in PrivatBank's own numbers, and it is the biggest ATM fleet in Ukraine.

| | |
|---|---|
| Source | PrivatBank 2025 Integrated Report (Richnyy zvit 2025), PDF on static.privatbank.ua |
| URL | https://static.privatbank.ua/files/0000005651711873.pdf |
| Date | 31/12/2025 | 
| Tier | primary |
| Likelihood | High that further recycler conversion is budgeted once the hardware cycle restarts |
| Opp size / Win | XL / High |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Build the conversion business case on the ~6,170 non-recycling ATMs; note the bank's public 'about' page still says ~5,000 ATMs, which is stale - always quote the annual report figure.

---

### 13. PrivatBank (Ukraine)

**Signal.** Same 2025 Integrated Report: PrivatBank states the average availability of its self-service network was 76% during peak energy blackouts in 2025, and that acquiring field-service teams drove almost 3.7 million km to keep the terminal estate running. Financials: UAH 88bn pre-tax profit, UAH 29bn net profit, UAH 59bn profit tax, 19m active clients and 14m Privat24 users.

**Implies.** A self-disclosed 76% uptime is a weak number that the bank itself has chosen to publish, and 3.7m km of field driving is an expensive way to hold a network together. Both are direct openings for Printec managed services - remote monitoring, predictive maintenance and power-resilient self-service - sold on availability rather than on hardware. Profitability of UAH 29bn net means the money to fix it exists.

| | |
|---|---|
| Source | PrivatBank 2025 Integrated Report |
| URL | https://static.privatbank.ua/files/0000005651711873.pdf |
| Date | 31/12/2025 | 
| Tier | primary |
| Likelihood | High - energy attacks recur each winter, so the Sep-Nov 2026 budget round will fund resilience |
| Opp size / Win | L / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Pitch an availability-based managed-service SLA before the 2026/27 heating season, benchmarked against the bank's own published 76%.

---

### 14. PrivatBank (Ukraine)

**Signal.** PrivatBank Group consolidated interim statements for Q1-2026, note 8: the net book value of 'computer equipment' more than doubled year on year, from UAH 939,708 thousand at 01/01/2025 to UAH 1,985,266 thousand at 01/01/2026, while total property and equipment rose from UAH 3,876,829 thousand to UAH 5,713,577 thousand. Additions to computer equipment in Q1-2026 alone were UAH 410,005 thousand.

**Implies.** Independent balance-sheet corroboration that the 2025 hardware wave (the 1,140 Printec-supplied recyclers plus 39,000 POS) actually landed and was capitalised. It also shows the spend did not stop at year-end - a further UAH 410m of computer equipment was added in Q1-2026 - so the bank remains in an investment posture even without a new ATM box tender.

| | |
|---|---|
| Source | PrivatBank Group, consolidated interim condensed financial statements, 3 months to 31/03/2026 |
| URL | https://static.privatbank.ua/files/consolidatedfinzvit-1kv2026.pdf |
| Date | 31/03/2026 | 
| Tier | primary |
| Likelihood | High |
| Opp size / Win | Unscoped / — |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Track the same note in the H1-2026 interim when it publishes to see whether the additions run-rate holds.

---

### 15. PrivatBank (Ukraine)

**Signal.** Same Q1-2026 interim statements: PrivatBank recognised a provision of UAH 551,264 thousand against impaired cash balances held in branches, ATMs and terminals to which access is restricted by occupation and hostilities, plus UAH 2,462 thousand of FX revaluation losses on those balances.

**Implies.** Roughly half a billion hryvnia of cash is stranded inside inaccessible machines. That is a quantified argument for cash-cycle optimisation - recyclers, remote cash monitoring and forecasting reduce how much cash sits in the field in the first place. Printec cash automation and managed services.

| | |
|---|---|
| Source | PrivatBank Group consolidated interim statements to 31/03/2026 |
| URL | https://static.privatbank.ua/files/consolidatedfinzvit-1kv2026.pdf |
| Date | 31/03/2026 | 
| Tier | primary |
| Likelihood | High - the provision recurs while the war continues |
| Opp size / Win | M / Medium |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Frame recycler conversion partly as working-capital release, using the bank's own provision figure.

---

### 16. PrivatBank (Ukraine)

**Signal.** As at 27/08/2026 PrivatBank has NOT published H1-2026 interim financial statements: the newest documents on its financial-reporting page are the Q1-2026 consolidated and separate interim statements. The most recent narrative disclosure of network size remains the 2025 Integrated Report.

**Implies.** For this August reporting window there is no fresh H1-2026 fleet or capex disclosure to mine for PrivatBank - the procurement record on Prozorro is currently a fresher and more granular source than the bank's own reporting. Plan a re-check when the H1 interim lands.

| | |
|---|---|
| Source | PrivatBank financial reporting page |
| URL | https://privatbank.ua/about/finansovaja-otchetnost |
| Date | 27/08/2026 | 
| Tier | primary |
| Likelihood | High that H1-2026 interims publish in Sep-Oct 2026 |
| Opp size / Win | Unscoped / — |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Re-pull https://privatbank.ua/about/finansovaja-otchetnost in late Sep 2026 for the H1-2026 interim.

---

### 17. PrivatBank (Ukraine)

**Signal.** Negative finding from an exhaustive sweep of all 1,153 PrivatBank tenders on Prozorro: PrivatBank procures NO digital-onboarding/eKYC, transaction-monitoring or AML software externally. The only adjacent 2026 buys are a 500-seat VerifEye TEST licence, the McKinsey AML maturity review, a phishing-awareness tool (UAH 238,600, 19/08/2026) and DLP software Endpoint Protector (UAH 100,077,300, 24/07/2026).

**Implies.** PrivatBank builds its onboarding, fraud and AML stack in-house (Privat24 plus state Diia integration), so Printec's eKYC/AML/transaction-monitoring lines have no procurement route into this account today. Printec should not resource an AML pursuit here except through the remediation roadmap the McKinsey review may create. Conversely the bank DOES buy security infrastructure externally, which is where Printec's HSM/security line fits.

| | |
|---|---|
| Source | Prozorro search API, full enumeration of PrivatBank tenders |
| URL | https://prozorro.gov.ua/api/search/tenders |
| Date | 27/08/2026 | 
| Tier | primary |
| Likelihood | Low that an eKYC/AML product tender appears within 6-12 months |
| Opp size / Win | S / Low |
| Confidence | Medium |
| New? | yes |

**Follow-up.** Deprioritise eKYC/AML product pursuit at PrivatBank; concentrate on ATM/self-service, cash automation, POS estate services and HSM.

---

## Coverage notes

Full fresh run, no checkpoint existed. WebSearch was unavailable (session budget 200/200 already consumed before this subagent's first query), so ALL research was done by direct HTTP against primary sources with a desktop User-Agent. Angles used, deliberately different from prior runs: (1) the Prozorro CDB search API (POST https://prozorro.gov.ua/api/search/tenders), reverse-engineered from the portal's own front-end bundle, then the full public OpenProcurement API (public-api.prozorro.gov.ua/api/2.5/tenders/{uuid}) for award-level records - this yields supplier names, EDRPOU codes, unit quantities, model numbers and delivery dates that no press source carries; (2) an exhaustive enumeration of PrivatBank's entire procurement book by searching the string 'tender.privatbank.ua', which appears in every one of its tender titles - 1,153 tenders retrieved, then keyword-filtered, which is what makes the negative findings trustworthy; (3) PrivatBank's own 2025 Integrated Report and Q1-2026 consolidated interim statements, both of which are CAdES/PKCS#7-signed PDFs that had to be unwrapped to the embedded %PDF stream before pdfminer could read them. Confirmed and quantified: Printec Ukraine (EDRPOU 35442628) is the supplier of record for the 1,140 NCR recyclers (800 SelfServ 2062 + 340 SelfServ 2064) and for 39,000 Castles Android POS terminals. Corrections to the brief: the '800-unit 2026 lot' does not exist as a separate 2026 procurement - it is the SelfServ 2062 line inside the single 17/01/2025 award; and the bank's public 'about' page figure of ~5,000 ATMs is stale against the 7,310 in its own annual report. Genuine gaps: (a) NBU sector-wide ATM/POS infrastructure statistics could not be located - bank.gov.ua/ua/statistic/payment-system returns 404 and the dataset index is JavaScript-rendered, so Ukraine market totals are absent and PrivatBank's share is unquantified; (b) PrivatBank's own ATM locator API (api.privatbank.ua/p24api/infrastructure) has been closed since 31/08/2022, so a deposit-capable-vs-dispense-only split cannot be derived from a live feed the way it was for the Bulgarian and Croatian banks - the 15.6% recycler penetration is inferred from the award quantity over the annual-report fleet, not directly disclosed; (c) no H1-2026 interim financials exist yet; (d) tender.privatbank.ua, the bank's own tender portal, is an AngularJS application whose backend API was not identified, so the underlying tender documentation (technical annexes, warranty and SLA terms) was not read; (e) Ukrainian-language press was not swept, because WebSearch was unavailable and the primary record proved richer. The source catalogue at references/source_catalogue_A1.json covers only Greece, Albania, Bosnia, Bulgaria and Croatia, so it does not apply to Ukraine and was not used. All confidence values are capped at Medium per the rules, even where the evidence is a signed primary contract record.

## Access issues

WebSearch: unavailable for the whole run - the session's 200-call budget was exhausted before this subagent issued its first query. Every finding below therefore comes from a URL fetched directly. https://bank.gov.ua/ua/statistic/payment-system - HTTP 404; the NBU statistics index renders its dataset list in JavaScript, so the payment-infrastructure series was not reached. Retried with a desktop User-Agent (bank.gov.ua itself returns 200, so this is a routing/JS issue, not a 403 block). Logged, not silently dropped. https://api.privatbank.ua/p24api/infrastructure - returns HTTP 200 with body 'The service is closed since August 31, 2022'; the public ATM/branch locator feed no longer exists. https://zakupki.prom.ua/gov/tenders/... and https://e-tender.ua/tender/... - HTTP 403 (bot protection). Not needed, as the primary Prozorro API succeeded. https://tender.privatbank.ua - serves an AngularJS shell; its backend API was not identified, so tender technical documentation was not retrieved. clarity-project.info was used ONLY as an index to resolve tenderID to the Prozorro internal UUID; every substantive figure was then re-read from the primary public-api.prozorro.gov.ua record and is cited to that primary URL. Both PrivatBank PDFs are PKCS#7-signed containers, not plain PDFs; text was extracted locally with pdfminer after slicing the embedded PDF from the signature envelope.

## Operator requests

1) 'Dodatok do Dogovoru.pdf' - the signed contract annex attached to Prozorro tender UA-2025-01-17-010779-a (the 1,140-recycler award). It sits behind a signed public-docs.prozorro.gov.ua URL with an expiring Signature query parameter and should carry the warranty term, SLA and per-unit pricing. Retrieve from https://prozorro.gov.ua/tender/UA-2025-01-17-010779-a and download the contract documents. This is the single highest-value document outstanding. 2) The technical annex for tender UA-2026-08-03-004344-a (the 700 technical-condition acts plus 300 defect lists, RENOME-SMART, 03/08/2026) - it should name which machine models are being assessed, which would tell us exactly which cohort is heading for replacement. 3) NBU payment-infrastructure statistics (nationwide ATM and POS counts, latest quarter). The dataset index at bank.gov.ua is JavaScript-rendered; an operator with a real browser should retrieve the current XLSX from bank.gov.ua so PrivatBank's 7,310 ATMs can be expressed as a market share. 4) Identify the vendor behind 'VerifEye' and the principal represented by FOP Bauer L.O. (tender UA-2026-05-19-000121-a) - needed to judge whether this pilot touches Printec's eKYC territory.
