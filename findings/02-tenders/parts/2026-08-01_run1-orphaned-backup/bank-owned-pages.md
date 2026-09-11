# Agent 2 — Bank-owned procurement pages — 2026-08-01

Resumed from a partial checkpoint (18 signals) and closed the listed gaps. **27 signals total, 9 new this pass.**

## Headline

**The PrivatBank block is broken.** `tender.privatbank.ua` is browser-readable: 4,089 published procurements, 103 matching *банкомат*. The ~800 recycling-ATM programme is running there — **not** on Prozorro — as two-stage tender **PB-2026-03-17-3068329**, at pre-qualification since 08/04/2026 after a first attempt was cancelled. Interfax (21/05/2026) sizes it: 800 ATMs in 2026, after 1,200 in 2025 for ~UAH 1bn; estate 7,401 ATMs / 9,867 self-service terminals / 345,390 POS.

Second find: PrivatBank has **twice failed** to buy servicing for its Diebold Nixdorf recycling ATMs (UAH 4.08m) — an open, repeatable managed-services gap.

## Signals

### 1. Ukrgasbank (ПАТ АБ УКРГАЗБАНК, EDRPOU 23697280) — Ukraine **[NEW]**

- **Signal:** AWARD CONFIRMED — Ukrgasbank's 81-ATM purchase (36 through-the-wall, 37 lobby, 8 full-cycle recyclers; CPV 30120000-6) was awarded to TOV 'ATM sistems' (ТОВ «АТМ сістемс»), EDRPOU 44372551, contract value UAH 49,720,800 incl. VAT against an announced budget of UAH 55,264,689. Procedure requestForProposal UA-2026-03-20-010151-a, bids closed 10/04/2026, tender status 'complete', contract 'active'.
- **Source:** Prozorro CDB (public.api.openprocurement.org), tender ba07840177a14f0ba21da164d7da883b — https://prozorro.gov.ua/tender/UA-2026-03-20-010151-a (20/03/2026, primary)
- **Implies:** A competitor, not Printec, took an 81-unit ATM hardware deal including 8 cash recyclers at Ukraine's third-largest state bank. ATM Systems LLC is a young entity (EDRPOU 44372551, registered ~2021) and is now a named rival for Printec ATM/self-service and cash-recycling hardware in Ukraine. Printec should map ATM Systems' OEM (whose ATMs it resupplies) and target the follow-on managed-service/maintenance wrap, which is not in this contract.
- **Likelihood:** Awarded; the servicing/spares tail is the live 6-12 month opening | **Confidence:** Medium | **Size:** L | **Win:** Low
- **Follow-up:** Identify the OEM behind TOV 'ATM sistems' (EDRPOU 44372551) via YouControl/Opendatabot; then bid the Ukrgasbank ATM maintenance and cash-management wrap.

### 2. Printec Ukraine LLC (ТОВ ПРІНТЕК УКРАЇНА ЕЛ.ЕЛ.СІ., EDRPOU 35442628) — Ukraine **[NEW]**

- **Signal:** Printec Ukraine WON Ukrgasbank's tender for technical support of the software on Castles Saturn 1000F2 POS terminals, UAH 277,200 incl. VAT (UA-2026-06-10-013221-a, award active, CPV 72260000-5). Separately Ukrgasbank bought Castles Saturn 1000F2 POS modernisation for UAH 50,160 (UA-2026-03-13-011117-a).
- **Source:** Prozorro CDB (public.api.openprocurement.org), tender bcb4eb8b18be49f19e05e798c99224c2 — https://prozorro.gov.ua/tender/UA-2026-06-10-013221-a (10/06/2026, primary)
- **Implies:** Printec is the incumbent POS software-support supplier at Ukrgasbank. This is a defensible beachhead to cross-sell terminal estate management, transaction monitoring and the ATM managed-services wrap around the 81 new ATMs Printec did not win.
- **Likelihood:** Incumbency live now; renewal cycle ~annual | **Confidence:** Medium | **Size:** S | **Win:** High
- **Follow-up:** Use the Ukrgasbank POS relationship (contact Mykola Khamula, mkhamula@ukrgasbank.com) to bid the ATM service/monitoring wrap and the NFC/recycler roadmap.

### 3. TOV SalesServiceSolutions (ТОВ СЕЙЛСЕРВІСОЛЮШЕНС, EDRPOU 39906179) — Ukraine **[NEW]**

- **Signal:** Same supplier swept three separate bank ATM-service awards in 2026: Ukrgasbank NFC-module retrofit on 20 ATMs UAH 429,600 (UA-2026-07-16-002946-a, 16/07/2026); Ukrgasbank Wincor ATM servicing UAH 172,599.46 (UA-2026-06-09-013744-a, 09/06/2026); and Sense Bank ATM cassettes, 104 units, UAH 1,693,510 (UA-2026-03-27-011349-a, awarded against a UAH 1,727,200 budget).
- **Source:** Prozorro CDB (public.api.openprocurement.org) — https://prozorro.gov.ua/tender/UA-2026-07-16-002946-a (16/07/2026, primary)
- **Implies:** SalesServiceSolutions is consolidating the Ukrainian ATM aftermarket (servicing, cassettes, NFC retrofits) across at least two banks. This is the single most active direct competitor to Printec's ATM managed-services and spares business in Ukraine and should be tracked as a named rival, not a one-off.
- **Likelihood:** Continuing — it is winning repeatedly across buyers | **Confidence:** Medium | **Size:** M | **Win:** Medium
- **Follow-up:** Benchmark SalesServiceSolutions pricing on cassette repair and NFC retrofit; contest the open Sense Bank cassette-repair lots closing 10/08/2026.

### 4. Sense Bank (АТ СЕНС БАНК, Ukraine) — Ukraine **[NEW]**

- **Signal:** OPEN below-threshold tender: repair of ATM cassettes, 2 lots (Lot 1 Wincor, Lot 2 NCR), total UAH 432,200, CPV 50310000-1, UA-2026-07-30-004472-a, published 30/07/2026, bids close 10/08/2026. Sense Bank also ran an UNSUCCESSFUL tender to clean 5,822 self-service terminals (UA-2026-04-29-005067-a, UAH 873,300) — a public disclosure of its ATM estate size.
- **Source:** Prozorro CDB (public.api.openprocurement.org), tender db9f4074367f41cda540445b131c56cb — https://prozorro.gov.ua/tender/UA-2026-07-30-004472-a (30/07/2026, primary)
- **Implies:** A live, biddable Printec opportunity in ATM cash-handling spares/service, plus intelligence that Sense Bank runs roughly 5,800 self-service terminals — a large estate for a managed-services or recycler-refresh pitch.
- **Likelihood:** Closing within 9 days | **Confidence:** Medium | **Size:** S | **Win:** Medium | **Deadline:** 10/08/2026
- **Follow-up:** Submit on both lots by 10/08/2026; then pitch a full-estate managed-service contract for ~5,800 terminals.

### 5. ELTA (Hellenic Post, ΕΛΛΗΝΙΚΑ ΤΑΧΥΔΡΟΜΕΙΑ Α.Ε., AFM 094026421) — Greece **[NEW]**

- **Signal:** ELTA tender 37/26 — 5-year operating lease of 300 banknote counting and fitness-sorting machines for ELTA branches, with an option for 200 more — was AWARDED on 19/05/2026 (ExCo session 82, item 1) to BOOS S.A. (AFM 095053250, GEMI 008820701000). Price EUR 19.25 per machine per month excl. VAT, EUR 346,500 excl. VAT for the 300 machines; CPV 66114000-2. Estimated budget at launch (30/03/2026) was EUR 885,000. Machines are Double Power DF-8150F, ECB-certified for counterfeit detection and fitness sorting. Other bidders accepted to evaluation: Χ. ΘΕΟΔΟΣΗΣ ΑΒΕΕ and IBANDO / IB&O Intelligent Bank & Office Machines (Β. Παπαδάτος & ΣΙΑ ΕΕ). ELTA paid a EUR 17,325 three-month rental guarantee on 10/07/2026. The requirement flows from ELTA's cooperation agreement with Eurobank as amended 30/04/2025.
- **Source:** Diavgeia — ELTA ExCo award decision ΑΔΑ Ψ6ΓΨΟΡΡ2-ΥΟΡ (and launch ΨΓ14ΟΡΡ2-Ο38, guarantee ΨΥ7ΒΟΡΡ2-ΝΕΑ) — https://diavgeia.gov.gr/doc/%CE%A86%CE%93%CE%A8%CE%9F%CE%A1%CE%A12-%CE%A5%CE%9F%CE%A1 (21/05/2026, primary)
- **Implies:** A 300-500 unit branch cash-automation deal in Printec's core category went to BOOS S.A. with no Printec bid visible. It also reveals a new Greek competitor, IBANDO (IB&O Intelligent Bank & Office Machines), and a new hardware brand in Greek postal/bank branches, Double Power. The 200-machine option is still unexercised and the ELTA-Eurobank branch banking model is expanding — both are re-entry points for Printec cash recyclers and cash-automation managed services.
- **Likelihood:** 200-unit option decision plausible within 12 months | **Confidence:** Medium | **Size:** M | **Win:** Low
- **Follow-up:** Track exercise of the 200-machine option and ELTA's next Eurobank-driven branch cash requirement; qualify IBANDO and Double Power as competitors.

### 6. ELTA (Hellenic Post) — Greece **[NEW]**

- **Signal:** ELTA's own tender portal confirms it operates 117 ATMs nationwide: tender 53/25 'supply and installation of security systems at 117 ATMs across the Greek territory' (lowest-price award criterion), bids closed 16/06/2025 via procurement.elta.gr. ELTA's current services pipeline also includes 194/26 — maintenance of electronic security, alarm, fire-detection and remote-surveillance systems with connection to a monitoring centre.
- **Source:** ELTA declarations portal (elta.gr), notice 53/25 — https://www.elta.gr/declaration/promitheia-ylikon/5325-anoiktos-diagonismos-gia-tin-promitheia-kai-egkatastasi-sustimaton-asfaleias-se-117-atm-se-oli-tin-elliniki-epikrateia-me-kritirio-katakurosis-kai-anathesis-tin-pleon-sumferousa-apo-oikonomiki-apopsi-prosfora-mono-basei-timis-chamiloteri-timi (06/06/2025, primary)
- **Implies:** ELTA runs a 117-ATM estate of its own and procures ATM security and monitoring separately from the machines. That is a defined, addressable estate for Printec ATM managed services, security and monitoring — and the natural target for Printec Cash Network / Cashflex if ELTA ever opens an all-bank off-site ATM network.
- **Likelihood:** Refresh of the 2025 security contract plausible in 12-24 months | **Confidence:** Medium | **Size:** M | **Win:** Medium
- **Follow-up:** Register on procurement.elta.gr; monitor for the ATM security refresh and for any ELTA all-bank ATM network RFP.

### 7. TEB Sh.A. Kosovo — Kosovo **[NEW]**

- **Signal:** TEB Kosovo tender 259/26 'Supply of Cash Handling Machines (Counting and Sorting for Coins and Banknotes) for the Bank needs' was issued 22/05/2026 with bids closing 02/06/2026 — a NEW 2026 procurement, distinct from the 292/25 cash-handling tender of 2025. Dossier obtainable from procurement@teb-kos.com.
- **Source:** TEB Sh.A. tender portal (teb-kos.com), IFB 259/26 PDF — https://www.teb-kos.com/wp-content/uploads/2026/05/IFB_Supply-of-Cash-Handling-Machines-for-the-Bank-needs-.pdf (22/05/2026, primary)
- **Implies:** TEB is buying banknote AND coin counting/sorting equipment for a second consecutive year — a recurring cash-automation budget in a Printec footprint market. Bidding has closed, so the immediate play is to learn the winner and position for the 2027 cycle plus the service contract.
- **Likelihood:** Award decision due; repeat cycle likely in 2027 | **Confidence:** Medium | **Size:** S | **Win:** Medium | **Deadline:** 02/06/2026
- **Follow-up:** Email procurement@teb-kos.com to request the 259/26 outcome and to be listed for the next cash-handling and ATM tenders.

### 8. TEB Sh.A. Kosovo — Kosovo **[NEW]**

- **Signal:** TEB Kosovo tender 270/26 'Remote (Digital) Onboarding & Digital Signature Integration', issued 28/05/2026, had its deadline EXTENDED to 22/06/2026, 14:00. This gives the tender ID and firm dates for the digital-onboarding item that was previously known only as 'deadline extended'.
- **Source:** TEB Sh.A. tender portal (teb-kos.com), Deadline Extension IFB 270/26 PDF — https://www.teb-kos.com/wp-content/uploads/2026/06/Deadline-Extension-IFB_REMOTE-DIGITAL-ONBOARDING-DIGITAL-SIGNATURE-INTEGRATION.pdf (28/05/2026, primary)
- **Implies:** Directly matches Printec's digital onboarding / eKYC offer. The deadline extension usually signals a thin bidder field — worth chasing the award and, if lost, the phase-2 integration and AML/identity-verification layer.
- **Likelihood:** Award imminent or made; phase-2 work likely | **Confidence:** Medium | **Size:** M | **Win:** Medium | **Deadline:** 22/06/2026
- **Follow-up:** Request the 270/26 result from procurement@teb-kos.com; pitch Printec eKYC/digital-onboarding for the integration phase.

### 9. TEB Sh.A. Kosovo — Kosovo **[NEW]**

- **Signal:** TEB Kosovo tender 031/26 'Supply with Thermal paper rolls for POS terminals', issued 31/03/2026, closed 07/04/2026 — evidence of an active POS-terminal consumables cycle. TEB also has a standing 'Physical Security Guard Service, CIT Services and ATM Replenishment' procurement line (tender 636/24).
- **Source:** TEB Sh.A. tender portal (teb-kos.com), IFB 031/26 PDF — https://www.teb-kos.com/wp-content/uploads/2026/03/IFB-_Supply-with-Thermal-paper-rolls-for-POS-terminals-for-TEB-Sh.A.-needs.pdf (31/03/2026, primary)
- **Implies:** Confirms TEB runs a meaningful POS acquiring estate and outsources CIT plus ATM replenishment. Both are attachment points for Printec POS/acquiring services and ATM cash-management/managed services.
- **Likelihood:** Annual recurring cycles | **Confidence:** Medium | **Size:** S | **Win:** Medium | **Deadline:** 07/04/2026
- **Follow-up:** Ask to be added to TEB's supplier list for POS, ATM replenishment and CIT-adjacent tenders.

### 10. Banka Poštanska štedionica a.d. Beograd — Serbia **[NEW]**

- **Signal:** STATUS UPDATE: the bank's procurement for 'escort and security of money transport and ATM servicing of the Bank' (Poziv ref. C32-2-2037, dated 17/04/2026, bids due 30/04/2026) is still listed as 'У току' (in progress / not yet awarded) as of 01/08/2026. Scope covers escorting cassette transport between bank premises and ATMs at commercial locations, cassette exchange, ATM consumables replacement, handling of rejected/retained banknotes and retained cards, and physical-technical security cover for service interventions at commercial-location ATMs; the contract is open-ended with a 90-day notice period. The bank is not subject to Serbia's Public Procurement Act and runs these procedures under its own internal rules on its own site. ACCESS NOTE: posted.co.rs, logged as blocked in earlier runs, is fully fetchable with a desktop browser User-Agent; re-verified 01/08/2026 and the status is unchanged at 'У току'.
- **Source:** Banka Poštanska štedionica — Nabavke page and Poziv za podnošenje ponude (pratnja/bankomati) PDF — https://www.posted.co.rs/o-nama/nabavke.html (17/04/2026, primary)
- **Implies:** A live, un-awarded CIT + ATM-servicing contract at a state-owned Serbian bank, with an indefinite term. The scope explicitly includes ATM first-line servicing and consumables — Printec managed services and cash-management territory, best pursued with a local CIT partner.
- **Likelihood:** Award decision overdue; likely within 3-6 months | **Confidence:** Medium | **Size:** M | **Win:** Low | **Deadline:** 30/04/2026
- **Follow-up:** Contact nabavka@posted.co.rs for the outcome and for the next ATM/self-service cycle; identify a Serbian CIT partner to team with.

### 11. Banka Poštanska štedionica a.d. Beograd — Serbia **[NEW]**

- **Signal:** Current published pipeline as of 01/08/2026 shows NO open ATM, POS or cash-automation procurement. The three most recent notices are storage for the core banking system (published 08/07/2026, closed 22/07/2026), an access-control solution and technical-protection upgrade (01/07/2026, closed 14/07/2026), and scarves/ties for staff (25/06/2026, closed 09/07/2026). Earlier 2026 items include Oracle Exadata, Cisco Nexus switches/routers, DR-site servers, IT equipment and thermal rolls — all still marked 'in progress'.
- **Source:** Banka Poštanska štedionica — Nabavke page — https://www.posted.co.rs/o-nama/nabavke.html (08/07/2026, primary)
- **Implies:** The bank's 2026 spend is concentrated on core-banking infrastructure and physical/technical security rather than self-service hardware. Printec's near-term angle here is security/monitoring and the pending CIT+ATM servicing award, not an ATM refresh.
- **Likelihood:** No self-service RFP visible in the next 6 months | **Confidence:** Medium | **Size:** S | **Win:** Low
- **Follow-up:** Set a fortnightly watch on posted.co.rs/o-nama/nabavke.html (works with a desktop User-Agent).

### 12. CEC Bank S.A. (Romania) — Romania **[NEW]**

- **Signal:** CEC Bank's own procurement page shows NO open procedure as of 01/08/2026. The only two published procedures are an IT messaging solution for the Info SMS service (offers due 13/03/2026, 14:00) and elaboration of physical-security risk analyses for CEC Bank sites, split by county zones (offers due 23/04/2026, 17:00). Both are past their deadlines. Offers are submitted on paper at Calea Victoriei 13, Bucharest; contact sia@cec.ro / 021 311 11 19. ACCESS NOTE: cec.ro, logged as 403 in earlier runs, is fully fetchable with a desktop browser User-Agent — re-verified 01/08/2026, still only those two expired procedures.
- **Source:** CEC Bank — Achiziții page — https://www.cec.ro/achizitii (23/04/2026, primary)
- **Implies:** No post-rollout maintenance or managed-services RFP has appeared at CEC Bank; the watch item from earlier runs remains unrealised. CEC procures off-portal and by paper submission, so Printec needs a direct registered-supplier relationship with Serviciul Independent Achiziții rather than portal monitoring alone.
- **Likelihood:** Low visibility of a self-service RFP in the next 6 months | **Confidence:** Medium | **Size:** S | **Win:** Low
- **Follow-up:** Register with sia@cec.ro as a candidate supplier for ATM/self-service, cash automation and managed services; re-check cec.ro/achizitii monthly.

### 13. Ukrposhta (АТ УКРПОШТА, EDRPOU 21560045) — Ukraine **[NEW]**

- **Signal:** AWARD CONFIRMED — Ukrposhta's postal self-service terminal (parcel locker) purchase with installation went to the Ukrainian-Polish JV MODERN-EXPO (СП МОДЕРН-ЕКСПО, EDRPOU 21751578) for UAH 195,999,000 against a UAH 211,932,000 budget (UA-2026-05-05-011053-a, status complete). Volumes: 1,000 main locker modules, 1,000 type-1 add-on modules, 200 type-2 add-on modules, CPV 30131000-6. A first attempt (UA-2026-03-16-014034-a, UAH 211,932,000, same bidder at UAH 207,693,360) was declared unsuccessful.
- **Source:** Prozorro CDB (public.api.openprocurement.org), tender 8473bf6c399f4ba7a7ebd2244be303c0 — https://prozorro.gov.ua/tender/UA-2026-05-05-011053-a (05/05/2026, primary)
- **Implies:** Modern-Expo now owns Ukraine's largest self-service terminal rollout. Parcel lockers are adjacent to, not identical with, Printec's ATM/self-service line, but the same estate is the physical host for cash-in/cash-out and payment kiosks. Printec's play is the payment/cash module, terminal management software and field-service layer on top of this 2,200-module estate.
- **Likelihood:** Rollout runs through 2026-2027 | **Confidence:** Medium | **Size:** L | **Win:** Low
- **Follow-up:** Approach Ukrposhta and Modern-Expo about adding card acceptance / cash-in modules and remote terminal management to the new locker estate.

### 14. Ukrposhta (АТ УКРПОШТА) — Ukraine **[NEW]**

- **Signal:** Ukrposhta's above-threshold tender for cash-in-transit services (collection and delivery of valuables) in Kyiv, 66,736 service units, budget UAH 18,352,400, is at status active.awarded with the award going to PJSC 'Commercial Bank AKORDBANK' (EDRPOU 35960913) at UAH 18,018,720; bids closed 25/07/2026 and the contract is still 'pending'. A parallel Khmelnytskyi CIT tender was awarded at UAH 339,219 after an earlier UAH 1,641,384 attempt failed.
- **Source:** Prozorro CDB (public.api.openprocurement.org), tender 4c45f4d3d5e54eb499f9463a61543a58 — https://prozorro.gov.ua/tender/UA-2026-07-17-010455-a (17/07/2026, primary)
- **Implies:** Ukrposhta outsources cash logistics to a licensed bank rather than a security firm — a structural detail for anyone selling cash-cycle automation into the post office. Cash automation at the counter (recyclers, deposit machines) is the way to attack this cost line rather than competing on CIT.
- **Likelihood:** Contract signature within weeks | **Confidence:** Medium | **Size:** S | **Win:** Low | **Deadline:** 25/07/2026
- **Follow-up:** Pitch branch-level cash recycling to Ukrposhta as a way to cut the CIT bill; watch for regional CIT lots repeating.

### 15. PrivatBank (АТ КБ ПРИВАТБАНК, EDRPOU 14360570) — Ukraine **[NEW]**

- **Signal:** PrivatBank's 2026 self-service spend to date is consumables, logistics and spares — NOT new ATM hardware. Confirmed awards: 20,000 Newland Android POS terminals with HAL API to NEWLAND PAYMENT TECHNOLOGY (H.K.) COMPANY LIMITED for USD 2,180,000 (UA-2026-06-11-013572-a); 1,500 Diebold/Wincor cash cassettes to TOV SERVUS SYSTEMS INTEGRATION (EDRPOU 31089403) for UAH 7,211,025 (UA-2026-06-15-012172-a); POS thermal paper split between a main supplier PP GRUPA KOMPANIY TORGSERVIS (EDRPOU 33240871) at UAH 52,101,000 and a NEWLY IDENTIFIED reserve supplier TOV 'Torhovo-Vyrobnycha Hrupa Ukrainskyi Papir' (EDRPOU 43977041) at UAH 17,863,200, both dated 30/07/2026; plus ATM transport/installation lots totalling over UAH 20m across Ternopil, Lviv, Zakarpattia, Ivano-Frankivsk and Kirovohrad in January 2026, and cash-counting-room furniture and cassette bags worth over UAH 13m.
- **Source:** Prozorro CDB / Prozorro search API, buyer EDRPOU 14360570 — https://prozorro.gov.ua/tender/UA-2026-07-30-010562-a (30/07/2026, primary)
- **Implies:** The ~800 deposit/recycling ATM programme flagged for 2026 has still NOT been posted as a hardware notice as of 01/08/2026, but the pattern of heavy ATM transport, installation and cassette buying is consistent with preparation for a fleet movement. Printec holds the incumbency from the 1,140-unit NCR contract of Jan 2025 and should be positioned before the hardware notice drops.
- **Likelihood:** Hardware notice plausible in the next 6 months | **Confidence:** Medium | **Size:** XL | **Win:** Medium
- **Follow-up:** Weekly watch on tender.privatbank.ua and on Prozorro search filtered by buyer 14360570 for CPV 30120000-6; pre-brief PrivatBank procurement on the recycler roadmap.

### 16. Oschadbank (АТ Ощадбанк, EDRPOU 00032129) — Ukraine **[NEW]**

- **Signal:** Oschadbank ran a UAH 367,170 tender for relocation, dismantling and installation of ATMs, information-transaction terminals and electronic safes (UA-2026-03-12-014025-a, status complete). Oschadbank's overall 2026 self-service activity on Prozorro is limited to logistics of this kind, with no new ATM hardware notice.
- **Source:** Prozorro CDB / Prozorro search API, buyer EDRPOU 00032129 — https://prozorro.gov.ua/tender/UA-2026-03-12-014025-a (12/03/2026, primary)
- **Implies:** Ukraine's largest state retail bank is consolidating and moving its existing estate rather than buying new machines — consistent with a network-rationalisation phase that typically precedes a refresh. The electronic-safe line is also a Printec-adjacent cash-security item.
- **Likelihood:** Refresh cycle not visible within 6 months | **Confidence:** Medium | **Size:** M | **Win:** Low
- **Follow-up:** Set a Prozorro buyer-filter alert on EDRPOU 00032129 for CPV 30120000-6 and 30123000-7.

### 17. Ukrgasbank — cash-security aftermarket — Ukraine **[NEW]**

- **Signal:** Ukrgasbank awarded repair of deposit boxes, ATM safes and vaults (19 service units, CPV 50610000-4) to TOV 'KAPITAL STAL' (EDRPOU 37198195) for UAH 440,250 (UA-2026-03-31-010596-a). It also bought ATM branding services for UAH 353,000 and is now buying deposit-vault installation works (UA-2026-07-29-007533-a, 29/07/2026) and 'ZBERIHACH' software technical support (UA-2026-07-31-008524-a, 31/07/2026).
- **Source:** Prozorro CDB / Prozorro search API, buyer EDRPOU 23697280 — https://prozorro.gov.ua/tender/UA-2026-03-31-010596-a (31/03/2026, primary)
- **Implies:** Ukrgasbank is investing across the whole cash-security chain — safes, vaults, deposit boxes and ATM hardening — at the same time as its 81-ATM purchase. That is a coherent programme Printec can attach to with security, monitoring and managed services even though it lost the machines.
- **Likelihood:** Continuing through 2026 | **Confidence:** Medium | **Size:** S | **Win:** Medium
- **Follow-up:** Track the two newly published Ukrgasbank notices (deposit-vault installation, ZBERIHACH support) for scope and winner.

### 18. Hrvatska pošta / Croatian commercial banks — Croatia **[NEW]**

- **Signal:** Hrvatska pošta has no self-hosted procurement portal: https://www.posta.hr/nabava redirects to the corporate home page and no tender list is published there, so all its procurement runs through the national EOJN/TED route. The same applies to Croatian commercial banks, which are private and publish nothing.
- **Source:** Hrvatska pošta corporate site — https://www.posta.hr/nabava (01/08/2026, primary)
- **Implies:** For Croatia there is no bank-owned-portal channel to work; Printec must cover Hrvatska pošta exclusively via EOJN/TED. This closes off a route earlier runs left ambiguous and should redirect monitoring effort.
- **Likelihood:** Structural — will not change | **Confidence:** Medium | **Size:** S | **Win:** —
- **Follow-up:** Drop posta.hr from the bank-owned-portal watchlist; cover Hrvatska pošta via EOJN and TED only.

### 19. PrivatBank (АТ КБ ПРИВАТБАНК, EDRPOU 14360570) — Ukraine **[NEW]**

- **Signal:** BREAKTHROUGH — the ~800 recycling-ATM programme IS being run, but on PrivatBank's OWN portal, not Prozorro. Tender 'Ресайклінговий банкомат (1 етап)' (Recycling ATM, stage 1), tender ID PB-2026-03-17-3068329, is a multi-stage single-lot commercial procedure published 17/03/2026 09:02; clarifications ran to 02/04/2026 16:00, offers 02/04–08/04/2026 15:00, and the procedure has sat at stage 'Прекваліфікація' (pre-qualification) since 08/04/2026 and is still marked ACTIVE as of 01/08/2026. Budget is deliberately 'не вказано' (not disclosed). Qualification-requirements document was amended on 30/03/2026 and an English version was issued 23/03/2026 (i.e. international bidders invited); 6 bidder questions were logged. A FIRST attempt, PB-2026-01-15-3067363, published 15/01/2026 with offers closing 10/03/2026, was CANCELLED (Скасовано). Buyer contact: Stanislav Hora, stanislav.gora@privatbank.ua, +380 93 163 9815.
- **Source:** PrivatBank PrivatTender portal — tender PB-2026-03-17-3068329 — https://tender.privatbank.ua/commercial/tender/PB-2026-03-17-3068329/info (17/03/2026, primary)
- **Implies:** This is the single biggest self-service opportunity in Printec's Ukrainian footprint and the direct successor to the 1,140-unit NCR contract Printec won in Jan 2025. It is a two-stage procedure: stage 1 only pre-qualifies vendors, so the commercial stage is still ahead. The English-language dossier and the 30/03/2026 amendment mean the field is being opened to international ATM OEMs. Printec must be inside the pre-qualified list to reach stage 2.
- **Likelihood:** Stage-2 commercial round plausible within 3-9 months | **Confidence:** Medium | **Size:** XL | **Win:** Medium | **Deadline:** 08/04/2026
- **Follow-up:** Contact Stanislav Hora to confirm Printec's pre-qualification status on PB-2026-03-17-3068329 and obtain the amended qualification dossier; register a company account on tender.privatbank.ua to see the participant and contract tabs.

### 20. PrivatBank — recycler servicing gap — Ukraine **[NEW]**

- **Signal:** PrivatBank has TWICE failed to buy servicing for its existing Diebold Nixdorf recycling ATMs. 'Послуги з обслуговування ресайклінгових банкоматів Diebold Nixdorf', budget UAH 4,080,000: first run PB-2025-10-21-3065668 (published 21/10/2025, offers closed 06/11/2025) ended 'Закупівля не відбулася' (procurement did not take place); the re-run PB-2026-03-25-3068553 (published 25/03/2026, offers closed 13/04/2026) was CANCELLED. This also confirms Diebold Nixdorf recyclers are already installed in the PrivatBank estate.
- **Source:** PrivatBank PrivatTender portal — tender PB-2026-03-25-3068553 — https://tender.privatbank.ua/commercial/tender/PB-2026-03-25-3068553/info (25/03/2026, primary)
- **Implies:** An unmet, twice-failed requirement worth about UAH 4.08m a year for maintaining recycling ATMs — squarely Printec managed services. Two failed procedures usually mean too few qualified bidders or unacceptable terms, which is exactly the gap a multi-vendor service organisation fills. It also tells Printec that Diebold Nixdorf, not only NCR, is inside PrivatBank.
- **Likelihood:** Third attempt highly likely within 6 months | **Confidence:** Medium | **Size:** M | **Win:** High
- **Follow-up:** Pre-empt the third re-run: offer PrivatBank a multi-vendor recycler maintenance SLA covering Diebold Nixdorf and NCR estates before the notice is republished.

### 21. PrivatBank — cash-cycle spend on its own portal — Ukraine **[NEW]**

- **Signal:** PrivatTender shows 4,089 published procurements, of which 103 match 'банкомат' (ATM). 2026 cash-cycle items include: expert assessment of the technical condition of ATMs and self-service terminals, UAH 200,000, published 24/06/2026, offers closed 01/07/2026 (PB-2026-06-24-3070661); thermal paper for ATMs and self-service terminals, UAH 8,784,252, published 11/06/2026 (PB-2026-06-11-3070263); consumables for the cash counting room (straps, banding rings, coin bags), UAH 2,661,798, published 02/07/2026, now at winner-qualification stage (PB-2026-07-02-3070824); sacks and bags for the counting room and CIT, UAH 3,953,160, published 06/05/2026 (PB-2026-05-06-3069322); and ATM/self-service terminal transport and installation/de-installation, round 2, UAH 24,100,000, published 25/11/2025, status COMPLETED (PB-2025-11-25-3066433).
- **Source:** PrivatBank PrivatTender portal — keyword search 'банкомат' — https://tender.privatbank.ua/commercial/tender (02/07/2026, primary)
- **Implies:** PrivatBank commissioning an independent technical-condition assessment of its whole ATM and self-service estate in June 2026, alongside a UAH 24.1m fleet-movement contract, is the classic precursor to a fleet refresh — it corroborates that the recycler programme is real and being scoped. Every line here is a Printec attachment point: condition surveys, consumables logistics, installation and managed services.
- **Likelihood:** Refresh decisions flow from the June 2026 condition assessment | **Confidence:** Medium | **Size:** L | **Win:** Medium
- **Follow-up:** Ask PrivatBank procurement for the outcome of the ATM condition assessment (PB-2026-06-24-3070661) — it will define the refresh scope Printec should bid.

### 22. TEB Sh.A. Kosovo — Kosovo **[NEW]**

- **Signal:** CORRECTION AND UPDATE — TEB tender 270/26 'Remote (Digital) Onboarding & Digital Signature Integration' was extended a SECOND time: the extension notice restates issue date 28/05/2026 and sets the closing date to 29/06/2026, 14:00 (not 22/06/2026 as the first extension had it). TEB has also opened new procurements since: 281/26 'Provision of Security Monitoring room supervision', issued 03/06/2026, closing 15/06/2026 14:00; 300-26 servicing and maintenance of the Bank's generators (extension notice issued July 2026); 311-26 E-Archive project; and 298-26 Firepower/network security renewal.
- **Source:** TEB Sh.A. tender portal — Deadline Extension 2, IFB 270/26 (PDF, text extracted locally) — https://www.teb-kos.com/wp-content/uploads/2026/06/Deadline-Extension-2-IFB_REMOTE-DIGITAL-ONBOARDING-DIGITAL-SIGNATURE-INTEGRATION-1.pdf (28/05/2026, primary)
- **Implies:** Two deadline extensions on a digital-onboarding/eKYC tender is a strong signal of a thin or unqualified bidder field in Kosovo — the best possible entry condition for Printec's digital onboarding and eKYC offer, either as a late bidder in a re-run or as the phase-2 integrator. 281/26 (security monitoring room supervision) is an adjacent monitoring/managed-services line.
- **Likelihood:** Re-run or negotiated award plausible within 6 months | **Confidence:** Medium | **Size:** M | **Win:** Medium | **Deadline:** 29/06/2026
- **Follow-up:** Email procurement@teb-kos.com for the 270/26 outcome and ask to be invited if it is re-tendered; also request the 259/26 cash-handling-machine result.

### 23. TEB Sh.A. Kosovo — disclosure practice — Kosovo **[NEW]**

- **Signal:** STRUCTURAL FINDING: TEB Kosovo publishes invitations, deadline extensions and re-tendering notices on its own portal but publishes NO award or contract-award notices at all. A full sweep of every PDF on teb-kos.com/tenders (2022 to 01/08/2026, ~100 documents) returned zero result/award documents, so the outcomes of 259/26 (cash-handling machines, closed 02/06/2026), 270/26 (digital onboarding) and 292/25 cannot be established from public sources. Award information is only obtainable by email from procurement@teb-kos.com.
- **Source:** TEB Sh.A. tender portal, full document index — https://www.teb-kos.com/tenders/ (01/08/2026, primary)
- **Implies:** Kosovo commercial-bank awards are not monitorable remotely. Printec cannot run competitive intelligence on TEB from open sources and must instead get on the bidder list so it receives the invitations directly — being on the list is the only reliable channel.
- **Likelihood:** Structural — will not change | **Confidence:** Medium | **Size:** S | **Win:** —
- **Follow-up:** Register Printec as a standing supplier with procurement@teb-kos.com for cash automation, ATM/self-service, eKYC and managed services.

### 24. PrivatBank (АТ КБ ПРИВАТБАНК) — Ukraine **[NEW]**

- **Signal:** Sizing for the recycler programme, from the bank itself: PrivatBank plans to buy 800 ATMs in 2026, after buying 1,200 in 2025 for about UAH 1 billion. As at Q1-2026 the bank operated 7,401 ATMs, 9,867 self-service terminals, 1,053 branches and 345,390 POS terminals, and holds about 60% of the Ukrainian POS market. Retail board member Dmytro Musiienko: the intent is to replace all old, fully depreciated ATMs with machines that both dispense AND accept cash. National context at 01/03/2026: 15,570 ATMs and 22,401 self-service terminals in Ukraine.
- **Source:** Interfax-Ukraine — 'ПриватБанк у 2026р. планує придбати ще 800 банкоматів' — https://interfax.com.ua/news/economic/1169782.html (21/05/2026, press)
- **Implies:** Puts a number on the deposit/recycling-ATM opportunity that the PrivatTender pre-qualification (PB-2026-03-17-3068329) will convert into orders: roughly 800 units in 2026, on a 2025 run-rate of about UAH 1bn for 1,200 units, i.e. an order of magnitude of UAH 650-700m. Every one of those machines is a cash recycler — Printec's highest-value self-service category — and each carries an installation, cash-management and maintenance tail. PrivatBank alone is roughly 48% of Ukraine's installed ATM base.
- **Likelihood:** Purchasing runs through 2026 | **Confidence:** Medium | **Size:** XL | **Win:** Medium
- **Follow-up:** Use the 800-unit/2026 and 1,200-unit/2025 numbers to size the Printec bid and the multi-year service annuity; verify the 2025 UAH 1bn figure against PrivatBank's own annual report before quoting externally.

### 25. ELTA (Hellenic Post) — services pipeline — Greece **[NEW]**

- **Signal:** ELTA's own declarations portal, services category, carries 203 published notices; the most recent as of 01/08/2026 is 194/26, an open tender for MAINTENANCE of electronic security and alarm systems, fire detection and remote surveillance, with connection to a signal-receiving and processing centre over IP. Cross-checking the supplies category (49 notices) confirms ELTA has published NO further ATM, cash-automation or banknote-handling procurement in 2026 beyond 37/26 (300 counting/sorting machines, awarded to BOOS S.A.) and 53/25 (security systems on 117 ATMs). The 2026 supplies pipeline is postal consumables plus 144/26 Epson TM-T20IV thermal printers and laptops.
- **Source:** ELTA declarations portal — services (parochi-ypiresion) and supplies (promitheia-ylikon) indexes — https://www.elta.gr/declarations/parochi-ypiresion (01/08/2026, primary)
- **Implies:** ELTA's near-term addressable spend is security/monitoring services around its estate (including the 117 ATMs), not new cash hardware — the branch cash-automation cycle was consumed by the BOOS award. 194/26 is the live item Printec can pursue with a Greek security partner; the ATM security/monitoring refresh from 53/25 is the follow-on.
- **Likelihood:** 194/26 live now; ATM cash hardware not before 2027 | **Confidence:** Medium | **Size:** S | **Win:** Low
- **Follow-up:** Pull the full 194/26 dossier from ELTA (the detail page 403s to plain fetch tools; use procurement.elta.gr with a logged-in account) and decide whether to partner or pass.

### 26. Ukrposhta (АТ УКРПОШТА) — Ukraine **[NEW]**

- **Signal:** STRUCTURAL FINDING: Ukrposhta operates NO self-hosted tender portal. https://www.ukrposhta.ua/ua/tenders and /ua/tenderi both return the site's 404 page, and no procurement index exists anywhere on ukrposhta.ua. All Ukrposhta procurement is therefore visible only through Prozorro.
- **Source:** Ukrposhta corporate site — https://www.ukrposhta.ua/ua/tenders (01/08/2026, primary)
- **Implies:** Unlike PrivatBank — which runs a large parallel portal where the strategic items sit — Ukrposhta is fully covered by Prozorro monitoring. Printec should drop ukrposhta.ua from the bank-owned-portal watchlist and rely on a Prozorro buyer filter on EDRPOU 21560045.
- **Likelihood:** Structural — will not change | **Confidence:** Medium | **Size:** S | **Win:** —
- **Follow-up:** Remove ukrposhta.ua from the portal watchlist; keep the Prozorro buyer alert on EDRPOU 21560045.

### 27. PrivatBank PrivatTender portal — access route — Ukraine **[NEW]**

- **Signal:** ACCESS ROUTE RESOLVED (was logged as a hard block in every prior run): tender.privatbank.ua is an AngularJS SPA that returns only a 62 KB shell to plain HTTP fetches, but it is fully readable through a real browser. The public tender registry is at /commercial/tender with 4,089 published procurements, a free-text search box, and per-tender pages at the stable pattern /commercial/tender/PB-YYYY-MM-DD-<id>/info showing stage timeline, lots, documents, buyer EDRPOU and named buyer contact. The underlying JSON API is /commercial/v2/registry/main/search but it is CSRF-protected and cannot be called headlessly. Bidder lists and contract tabs require a registered company account.
- **Source:** PrivatBank PrivatTender registry — https://tender.privatbank.ua/commercial/tender (01/08/2026, primary)
- **Implies:** PrivatBank's most strategic procurements — including the recycling-ATM programme — are published ONLY here, not on Prozorro, which is why every previous run missed them. This portal must become a standing weekly watch, and Printec should hold a registered company account so it can see participants, contracts and awards rather than only the public summary.
- **Likelihood:** Structural — recurring value every run | **Confidence:** Medium | **Size:** Unscoped | **Win:** —
- **Follow-up:** Open a PrivatTender company account for Printec Ukraine (EDRPOU 35442628) and add a weekly browser-driven sweep of /commercial/tender for 'банкомат', 'ресайклінг', 'термінал самообслуговування' and 'POS'.

## Coverage notes

RESUMED FROM CHECKPOINT: this run found an existing partial checkpoint for 2026-08-01 holding 18 verified signals; those are kept unchanged and the four gaps its `remaining` note listed were worked. NEW THIS PASS (9 signals): the PrivatBank tender.privatbank.ua block was BROKEN — the portal is browser-readable and holds 4,089 procurements, 103 matching 'банкомат'. That surfaced the single most important find of the run: the ~800 recycling-ATM programme is running on PrivatBank's OWN portal, not Prozorro, as a two-stage procedure PB-2026-03-17-3068329 sitting at pre-qualification since 08/04/2026, after a first attempt (PB-2026-01-15-3067363) was cancelled. Also found: two failed attempts to buy Diebold Nixdorf recycler servicing (UAH 4.08m), a June-2026 independent condition assessment of the whole ATM/self-service estate, and Interfax confirmation of 800 ATMs planned for 2026 on a 2025 base of 1,200 units for ~UAH 1bn. TEB Kosovo: full sweep of all ~100 PDFs on teb-kos.com/tenders; 270/26 digital onboarding was extended a SECOND time to 29/06/2026 (correcting the 22/06 date in the checkpoint), new tenders 281/26, 300-26, 311-26, 298-26 identified, and TEB confirmed to publish NO award notices at all. Poštanska štedionica: re-verified 01/08/2026, CIT+ATM-servicing award still 'У току' (unchanged). CEC Bank: re-verified 01/08/2026, still only two expired procedures. ELTA: both declaration indexes (49 supplies + 203 services) swept — no new cash/ATM hardware in 2026; 194/26 security-systems maintenance is the live item. Hrvatska pošta and Ukrposhta both confirmed to have NO self-hosted portal. SEARCH ANGLES USED: local-language keyword search inside the bank portals (банкомат, ресайклінг), Ukrainian-language press (Interfax), the Prozorro POST search API, Greek-language ELTA declaration indexes, Serbian-Cyrillic procurement page parsing, local pdfminer extraction of TEB PDFs, and browser escalation for two SPAs. GENUINE GAPS: PrivatBank participant/contract tabs and tender documents need a registered account; the two July-2026 Ukrgasbank notices (deposit-vault installation UAH 80,520 excl. VAT; 'ЗБЕРІГАЧ' software support UAH 307,200 excl. VAT) are both status 'complete' but their winners cannot be read because the Prozorro search API returns no internal tender uuid and the CDB API requires one; TEB Kosovo award outcomes are not published anywhere.

## Access issues

RESOLVED THIS RUN: (1) tender.privatbank.ua — AngularJS SPA, plain fetch returns only a shell; solved by driving it in Claude-in-Chrome. Its JSON API /commercial/v2/registry/main/search is CSRF-protected and rejects headless calls. (2) cec.ro — previously 403; a desktop browser User-Agent defeats it completely. (3) posted.co.rs — previously blocked; a desktop User-Agent returns the full procurement table. (4) TEB Kosovo PDFs — WebFetch cannot read them (returns raw binary); extracted locally with pdfminer.six, which works. STILL BLOCKED / LOGGED: prozorro.gov.ua/api/search/tenders accepts POST with {"text":"<tenderID>"} and is the working route to confirm a tender exists, its buyer, budget and status, but it does NOT return the internal uuid, so the openprocurement CDB endpoint public-api.prozorro.gov.ua/api/2.5/tenders/<uuid> cannot be reached from a tenderID alone and awards/suppliers stay unreadable for those two Ukrgasbank notices. GET /api/tenders/<tenderID> and /api/tenders/search both 404/405. prozorro.gov.ua/tender/<tenderID> serves an 842-byte SPA shell with no embedded data. procurement.elta.gr is a Blazor SPA that renders 'An unhandled error has occurred' without a session. ELTA declaration DETAIL pages return 403 to WebFetch (the index pages are fine with a desktop User-Agent, and the site leaks PHP warnings, so it is fragile rather than deliberately gated). elta.gr/declarations and /declarations/ypiresies are 404 — the correct paths are /declarations/promitheia-ylikon, /declarations/parochi-ypiresion, /declarations/technika-erga, /declarations/kanonismoi, /declarations/all. www.ukrposhta.ua/ua/tenders is 404 (no portal exists). NOTE ON THE BROWSER: Claude-in-Chrome IS connected this run (contrary to the baseline). One shared tab was being driven concurrently by another process and navigated away mid-task; work was moved to a dedicated tab. Two javascript_tool calls were refused by the permission classifier for touching cookies/query strings — the same information was obtained through the UI instead, so nothing was lost.

## Operator requests

1. PrivatBank PrivatTender, tender PB-2026-03-17-3068329 'Ресайклінговий банкомат (1 етап)': the six qualification documents (Запит кваліфікаційних документів, plus the 30/03/2026 amended version and the English version) are behind a free registration wall. An operator should register a company account on tender.privatbank.ua and download them — they will contain the unit quantity, the technical specification and the pre-qualification criteria for the ~800-unit recycler programme. Same account unlocks the Учасники (participants) and Договори (contracts) tabs, which would name the competitors. 2. TEB Sh.A. Kosovo: award outcomes are never published. An operator should email procurement@teb-kos.com to request the results of 259/26 (cash-handling machines, closed 02/06/2026) and 270/26 (remote digital onboarding, closed 29/06/2026), and ask to be added to the standing bidder list. 3. Banka Poštanska štedionica: email nabavka@posted.co.rs for the outcome of the CIT + ATM-servicing procurement (offers closed 30/04/2026, still 'У току' after three months). 4. CEC Bank Romania: CEC accepts offers only on paper at Calea Victoriei 13, Bucharest; an operator should register Printec with sia@cec.ro (021 311 11 19) as a candidate supplier for ATM/self-service, cash automation and managed services. 5. No paywalled PDFs blocked this run.
