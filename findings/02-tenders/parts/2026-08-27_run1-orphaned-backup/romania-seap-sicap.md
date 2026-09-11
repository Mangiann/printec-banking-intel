# Romania — SEAP/SICAP (e-licitatie.ro) — Agent 2 findings, run 27/08/2026

**Status:** complete. **Signals:** 24.

## Method (new routes found this run)

- `startPublicationDate` / `endPublicationDate` DO work on `GetCNoticeList` and `GetCANoticeList` — defeats the 3,000-row oldest-first cap. Pulled 17 weekly windows: 8,279 contract notices + 16,634 award notices (01/05–27/08/2026).
- Winners come from `POST /api-pub/{C|PC|DC|RFQ}_PUBLIC_CANotice/GetCANoticeContracts/`, discovered in the lazy module at `/js/pub/notices/ca-notice/service`. Needs the full filter object incl. `sortOrder:[]`.
- `DaAwardNoticeCommon/GetDaAwardNoticeList` honours a `contractObject` keyword filter — 41 queries, 802 unique below-threshold awards with named suppliers.

## Headline

- **No ATM, recycler, deposit machine or banknote sorter tender exists on SICAP in the window.** Romanian bank hardware demand is invisible here because commercial banks are not contracting authorities. CEC Bank publishes one stale item; BT/BRD/BCR publish nothing.
- **BNR HSM support winner named for the first time:** Digital Professional Services SRL (RO43040394), contract 44/P/2026, 18/05/2026, RON 335,000.
- **Treasury cash-machine service is fragmented across micro-vendors** — CA.DA GRUPP (Craiova), EUTRON INVEST ROMANIA (Cluj, 14 awards in August alone), OFFICE HQ (Bacău). Clear opening for a national managed-service framework.
- **Nothing at all** on fraud/transaction monitoring, card issuing/personalisation, or core banking/digital channels.

## Signals

### 1. Banca Naţională a României (National Bank of Romania, BNR) — M (19/05/2026)

AWARD: notice SCNA1133162 records 'Servicii de suport pentru echipamentele HSM' (support for hardware security modules — the tamper-proof boxes guarding payment/cryptographic keys). WINNER: Digital Professional Services SRL, fiscal code RO43040394, Bucharest. Contract 44/P/2026 dated 18/05/2026; published value RON 335,000. First time BNR's HSM support incumbent is named in this pipeline.

- **Implies:** Head-on with Printec line 9 (payment security, HSM/key management — Thales payShield, PCI-PIN, remote key injection). A small Romanian integrator holds the central bank's HSM support; Printec's route is displacement at renewal plus selling the same capability into BCR/BRD/CEC/BT.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP/SEAP award notice SCNA1133162 (caNoticeId 100620422) — https://www.e-licitatie.ro/pub/notices/ca-notices/view-c/v1/100620422
- **Follow-up:** Check ONRC filing and Thales/Utimaco partner status of Digital Professional Services SRL (RO43040394); size the BNR HSM estate ahead of the ~Q2-2027 successor notice.

### 2. Banca Naţională a României (BNR) — L (11/06/2026)

AWARD: CAN1169439 'Servicii de verificare şi întreţinere a sistemelor de securitate – sedii B.N.R.' (inspection/maintenance of security systems at BNR premises). WINNER: Regia Autonomă RASIROM R.A., RO 7061781 (state technical-security operator under the Romanian Intelligence Service). Contract 49/P/2026 of 29/05/2026, RON 2,676,424.64.

- **Implies:** Printec lines 8 (physical ATM/branch security) and 11 (managed/field services). RASIROM is the structural incumbent for physical security at Romanian state and central-bank sites — a barrier to any foreign security vendor bidding directly in RO public sector. Treat as channel partner, not target.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP/SEAP award notice CAN1169439 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Evaluate RASIROM as a Romanian delivery partner for anti-skimming / IBNS rather than a competitor to displace.

### 3. Banca Naţională a României (BNR) — L (06/08/2026)

STATUS OF CARRIED ITEM — CLOSED, AWARD PENDING: CN1093831 / TED 499473-2026, 'Furnizare si montaj sisteme de securitate Sedii BNR' (supply + installation of security systems at BNR premises), CPV 35120000, estimated RON 3,438,026.83. Bid deadline was 06/08/2026 15:00. As at 27/08/2026 SICAP procedure state is still 'In desfasurare' (in progress); no award notice published. NOT re-biddable.

- **Implies:** Printec line 8. The award will name the supplier of BNR's next-generation site security; given CAN1169439, RASIROM is the likely winner. Dedup key: TED notice id 499473-2026 = SICAP CN1093831.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notice CN1093831 (procedureId 100325976); TED notice 499473-2026 — https://ted.europa.eu/en/notice/499473-2026/pdf
- **Follow-up:** Re-check SICAP CAN feed against procedureId 100325976 next run; capture winner and value.

### 4. Banca Naţională a României (BNR) — L (03/06/2026)

AWARDS (payments core): CAN1168349 (25/05/2026) 'Upgrade sistem integrat STP', estimated RON 12,358,335, contract 186/P/2024 of 09/12/2024 for RON 2,471,667; and CAN1168935 (03/06/2026) 'Licențe și mentenanță user aplicație STP', estimated RON 14,292,750, contract 39/P/2026 of 26/05/2026 for RON 2,802,500. WINNER in both: Wall Street Systems Sweden AB (ION Group), VAT SE 556500855301. Separately CAN1167071 (05/05/2026) awarded call-off no. 2 of 04/05/2026 worth RON 477,840 to MONTRAN SRL, RO13018603, for development of functionality on a BNR payment system.

- **Implies:** Printec line 4 (payments modernization — instant payments, ISO 20022, RTGS, digital euro). BNR's payments/treasury stack belongs to ION/Wall Street Systems and Montran, both software principals. Printec's realistic angle is the bank-side ISO 20022 / instant-payments connectivity layer at commercial banks, not the BNR core.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices CAN1168349, CAN1168935, CAN1167071 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Map Montran's Romanian bank-side footprint (it supplies RTGS/ACH across CEE) as a partner-or-competitor question for Printec's payments-modernization offer.

### 5. Banca Naţională a României (BNR) — M (18/08/2026)

AWARD (cash-centre consumables): CAN1163728 'Saci ambalat' (packing/banknote bags), estimated RON 1,292,285.06, split between two named winners — Europrotect Safety SRL, RO 26194113, contract 26/P/2026 of 24/02/2026, RON 604,285.06; and WHYTE YNTACT PROTECTYON SRL, RO43777630, contract 19/P/2026 of 25/02/2026, RON 688,000.

- **Implies:** Romanian analogue of the Česká pošta security-bag framework in the baseline. Not a Printec product, but it names two cash-logistics consumables suppliers working inside BNR's cash centres — useful entry intelligence on BNR cash operations and Agent-6 competitor mapping.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notice CAN1163728 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** No Printec bid; log both firms as BNR cash-centre supply-chain incumbents.

### 6. Direcţia Generală Regională a Finanţelor Publice Craiova (Regional Public Finance Directorate, Craiova) — L (13/08/2026)

STATUS OF CARRIED ITEM — CLOSED, AWARD PENDING: CN1094258 'Acord Cadru servicii bancare pentru plata cu cardul prin intermediul terminalelor POS (2 loturi)' — framework agreement (a standing contract the buyer draws down from without re-tendering) for card-acceptance/POS banking services, 2 lots. CPV 66110000, estimated RON 1,218,000, published 09/07/2026, bids due 13/08/2026 15:00. As at 27/08/2026 SICAP still shows 'In desfasurare'; no award notice yet.

- **Implies:** Printec line 3 (POS/acquiring/terminal management). The winner will be an acquiring bank rolling POS estate across Trezoreria counters. The same buyer's earlier POS framework (CAN1152651) went to a bank; whoever wins needs terminals and a TMS behind it.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notice CN1094258 (procedureId 100326975) — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Re-check next run; when the acquiring bank is named, approach it on Verifone/Castles terminal supply plus x-pos/POSight terminal management.

### 7. Direcţia Generală Regională a Finanţelor Publice Craiova — S (20/07/2026)

AWARDS — CASH-COUNTING MACHINE SERVICE, DIRECT FIT: two SICAP award notices, SCNA1133486 (28/05/2026) and SCNA1135126 (20/07/2026), both for 'Servicii de Mentenanță, de întreținere și/sau reparații, pentru masini de numarat/legat bancnote si numarat monede' (maintenance/repair of banknote counting-and-strapping and coin-counting machines). WINNER in both: CA.DA GRUPP SRL, fiscal code 45744884. SCNA1133486 covers 5 contracts totalling RON 449,628 (latest 22/05/2026); SCNA1135126 covers 3 contracts totalling RON 199,600 (latest 17/07/2026). The underlying open procedure SCN1176462 (est. RON 199,600, bids due 02/07/2026) is now 'Atribuita'.

- **Implies:** Closest direct competitive fit on this portal to Printec line 1 (cash automation — banknote/coin counting and sorting, Glory/Sesami/Consillion). A single small Romanian firm holds the Craiova Treasury's counting-machine service. Printec's managed/field-service model (500+ engineers) is the differentiator against firms of this size.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices SCNA1133486 and SCNA1135126; contract notice SCN1176462 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Profile CA.DA GRUPP SRL (45744884) — brands serviced, engineer count; build a multi-DGRFP national service proposition rather than bidding region by region.

### 8. Direcţia Generală Regională a Finanţelor Publice Cluj-Napoca — S (25/08/2026)

AWARDS — SUSTAINED CASH-MACHINE SERVICE STREAM: 14 direct-acquisition awards published 04/08/2026-25/08/2026, all to EUTRON INVEST ROMANIA SRL, fiscal code RO 4096491, totalling RON 25,463.94. Each covers repair, fault assessment or servicing of RIBAO BCS 160 banknote-counting machines at named Treasury offices (Cluj-Napoca, Turda, Huedin, Salonta, Marghita, Aleșd, Baia Mare, Sighetu Marmației, Vișeu de Sus, Satu Mare, Bistrița Năsăud, Sângeorz Băi, Șinleu Silvaniei). Largest single: DAN2832998, 17/08/2026, RON 5,852.45. A separate award, DAN2753453 (12/05/2026), gave Municipiul Bacău's counting-machine maintenance to OFFICE HQ SRL, RO32152007, RON 24,297.78.

- **Implies:** Printec line 1 (banknote counting/sorting) and line 11 (field maintenance). Reveals the real Romanian Treasury cash-machine estate: low-cost Chinese RIBAO BCS 160 counters serviced piecemeal by micro-vendors at a few hundred lei per call. That fragmentation is the opening — a single national managed-service framework (Printec's model) beats 14 separate direct awards.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP direct-acquisition award notices DAN2823746/DAN2823769/DAN2824187-DAN2839421 series; DAN2753453 — https://www.e-licitatie.ro/pub/da-award-notices/list/0
- **Follow-up:** Pitch ANAF/DGRFP centrally on a national counting-machine managed-service framework plus a fleet upgrade to Glory/Sesami; name EUTRON INVEST (RO 4096491) and OFFICE HQ (RO32152007) as incumbents.

### 9. C.N. Poşta Română S.A. (Romanian Post) — L (19/08/2026)

OPEN TENDER: CN1095543 'Servicii de transport valori (numerar lei și valută convertibilă) de la Casieriile Județene către Oficii Poștale/Oficii Zonale Poștale nereședință de județ' (cash-in-transit of RON and convertible currency from county cash offices to non-county-seat post offices), CPV 60100000, estimated RON 7,737,840, published 19/08/2026, bids due 21/09/2026 15:00.

- **Implies:** Printec's cash-in-transit adjacency and line 1 (cash automation). Romanian Post runs a nationwide cash network — the CIT tender confirms a large physical cash flow through post offices, the same profile as the Greek ELTA/Printec Cash Network fee-free-ATM concept and the Poșta Română counterpart of the ELTA BOOS banknote-counter lease.
- **Deadline:** 21/09/2026 | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notice CN1095543 — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Not a Printec bid (pure CIT), but use it to size Poșta Română's cash volumes and pitch counting/recycling automation plus off-site ATMs into the post-office network.

### 10. C.N. Poşta Română S.A. — M (11/08/2026)

CARRIED/CLOSED: SCN1176522 'Saci medii și mari pentru procesare numerar' (medium and large bags for cash processing), estimated RON 1,122,960, bids due 06/07/2026 — as at 27/08/2026 still 'In desfasurare', no award. Also CN1092504 'Servicii de întreţinere şi reparaţii a sistemelor electronice de securitate' (maintenance/repair of electronic security systems — intruder detection, CCTV, access control), estimated RON 3,662,000, bids due 29/06/2026, likewise still 'In desfasurare'. AWARD: CAN1172504 (11/08/2026) 'Servicii de monitorizare GPS a flotei CNPR si dispecerizare transport valori' (GPS fleet monitoring and cash-transport dispatch), 3-year framework, estimated RON 992,550 — WINNERS (joint): Vodafone România S.A., RO 8971726, and Romanian Security Systems S.A., 4381862; contracts 140/1510 and 140/1511 of 23/07/2026, RON 2,977,650 and RON 992,550.

- **Implies:** Printec lines 8 (physical security) and 11 (managed services). Confirms Poșta Română is actively re-contracting its whole cash-security stack in 2026 — bags, electronic security, CIT and CIT dispatch — a coherent window to enter with cash automation before the next cycle.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP notices SCN1176522, CN1092504, CAN1172504 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Track both pending awards; approach Poșta Română procurement on cash-processing automation for county cash offices.

### 11. C.N. Poşta Română S.A. — XL (11/08/2026)

AWARD (branch automation adjacency): CAN1147177 (11/08/2026) 'Sisteme de sortare automată a trimiterilor poștale de tip colete poștale' (automatic parcel-sorting systems), estimated RON 27,515,000. WINNER: Isitec International, registration 442336079 (French), three contracts of 15/05/2025 — 140/1078 RON 12,425,000, 140/1079 RON 2,665,000, 140/1080 RON 12,425,000.

- **Implies:** Adjacent to Printec's self-service/parcel-locker line (Printec S.I. d.o.o. supplies Pošta Slovenije parcel lockers). Confirms Poșta Română is spending at scale on logistics automation and buys from foreign specialists — a precedent that a non-Romanian vendor can win big at CNPR.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notice CAN1147177 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Use the Pošta Slovenije parcel-locker reference to approach CNPR on the last-mile/locker phase.

### 12. CEC Bank S.A. (state-owned commercial bank) — as public-sector acquirer — XL (24/08/2026)

CEC Bank (RO361897) is the single most-awarded card-acquiring provider on SICAP this quarter, named winner in at least eight separate award notices: CAN1145748 DGRFP Bucharest (27/05/2026, 8 contracts, RON 2,926,882.55); CAN1162613 Oficiul Naţional al Registrului Comerţului EFT-POS (12/06/2026, 5 contracts, RON 2,289,600.48); CAN1151682 DGRFP (10/06/2026, 8 contracts, RON 2,055,793.87); CAN1167371 DGRFP (03/07/2026, 4 contracts, RON 2,302,498.40); SCNA1134431 DGITL Sector 1 (01/07/2026, RON 1,151,778.33); SCNA1129839 Municipiul Bacău SNEP (14/07/2026, 6 contracts, RON 1,014,500); CAN1172870 DGRFP treasury-cashier framework (14/08/2026, RON 4,457,700); CAN1156763 Poşta Română TEZAUR online card processing (07/08/2026, RON 10,756,800); and CAN1173223 Loteria Română electronic transaction processing (24/08/2026, RON 3,755,529.65).

- **Implies:** Printec line 3 (POS/acquiring/TMS) and line 12 (digital channels). CEC Bank is winning Romanian public-sector acquiring wholesale and therefore must be deploying and managing a rapidly growing POS/self-service estate. It is the single highest-value Romanian acquiring prospect for terminal supply, terminal management (x-pos/POSight/TMS), softPOS and key injection.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices CAN1145748, CAN1162613, CAN1151682, CAN1167371, SCNA1134431, SCNA1129839, CAN1172870, CAN1156763, CAN1173223 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Direct approach to CEC Bank cards/acquiring on terminal supply + TMS + remote key injection, evidencing the nine public-sector wins above as estate growth.

### 13. CEC Bank S.A. — own procurement channel — Unscoped (25/02/2026)

NEGATIVE/ACCESS FINDING: CEC Bank's public procurement page cec.ro/achizitii (reachable with a desktop Chrome User-Agent; blocked to a default agent) lists exactly ONE procedure across all pages — 'Procedura de achiziție prin licitație organizată în vederea achizitiei solutiei IT de servicii de mesagerie tip Info SMS' (IT SMS-messaging solution), posted 25/02/2026, offers to the Central Registry at Calea Victoriei 13, deadline 13.03.2026 14:00 — long past. Page 1 returns 'Nu sunt rezultate'. Separately, CEC Bank does NOT appear as a contracting authority in the SICAP contract-notice or award feeds for 01/05/2026-27/08/2026, nor do Eximbank, Banca Transilvania, BRD or BCR. [STANDING — pattern dated 2026]

- **Implies:** Confirms the structural point for Romania: commercial-bank ATM, self-service and POS buying is NOT visible on SEAP/SICAP because those banks are not contracting authorities under Law 98/2016 for their own commercial activity. Even state-owned CEC Bank publishes almost nothing. Printec cannot pipeline Romanian bank hardware from this portal — it must be direct sales, with SICAP used only to read state-sector demand and competitor identities.
- **Deadline:** — | **Win:** — | **Confidence:** Medium | **New:** False
- **Source:** cec.ro/achizitii (retrieved with desktop UA); SICAP api-pub buyer sweep over 8,279 contract notices and 16,634 award notices — https://www.cec.ro/achizitii
- **Follow-up:** Do not scope Romanian bank ATM/POS demand from SICAP. Track BCR/BRD/BT/Raiffeisen/ING via IR reports, ARB/BNR statistics and direct contact instead; keep cec.ro/achizitii on a monthly desktop-UA poll.

### 14. SelfPay (Netopia/SelfPay, RO26067497) + Salt Bank (RO10318789) — L (03/07/2026)

COMPETITOR WINS — UNATTENDED SELF-SERVICE PAYMENT TERMINALS: the SelfPay/Salt Bank pairing won at least three Romanian local-tax buyers this quarter. CAN1161203 DGITL Sector 1 Bucharest (03/07/2026) 'Servicii de colectare plăți prin intermediul terminalelor de plată neasistate, precum și servicii de închiriere terminale de plată neasistate' (payment collection via unattended payment terminals plus terminal rental), 7 contracts, RON 6,110,317.82, latest 29/05/2026. SCNA1133771 Direcţia Fiscală Timişoara (08/06/2026), 2 contracts, RON 1,144,328, latest 02/06/2026. CAN1166131 Direcţia Fiscală Braşov (30/06/2026), 4 contracts, RON 352,317.50 alongside Banca Transilvania on other lots. Also DAN2782089 (17/06/2026), Direcţia Fiscală Locală Târgu Mureș rented a SelfPay self-service terminal for RON 8,204.

- **Implies:** Direct competition with Printec line 2 (self-service kiosks) and line 3 (unattended acceptance). SelfPay operates the terminal estate as a service and bundles the acquiring through Salt Bank — an operating model Printec can match through Printec Cash Network (the Greek Cashflex/KEA vehicle already runs ~850 off-site ATMs as a service).
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices CAN1161203, SCNA1133771, CAN1166131; direct-acquisition award DAN2782089 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Assess a Romanian terminal-as-a-service vehicle mirroring Printec Cash Network; target the local-tax buyers SelfPay has not yet taken (Municipiul Arad CN1095003 below).

### 15. Municipiul Arad — L (03/08/2026)

OPEN TENDER — SELF-SERVICE STATIONS: CN1095003 'Acord-cadru de servicii de incasari impozite, taxe si alte venituri bugetare locale prin statii de tip self-service' (framework for collecting local taxes and other budget revenue through self-service stations), CPV 66110000, estimated RON 1,536,964, published 03/08/2026, bids due 10/09/2026 15:00. The same buyer also has CN1094319, an SNEP electronic-payments framework, estimated RON 1,741,728, bids due 17/08/2026 (now closed, still 'In desfasurare'). A comparable open item is SCN1175047, Municipiul Oneşti, 'Servicii de colectare amenzi, impozite și taxe locale ... prin intermediul terminalelor de tip self-service', estimated RON 800,540 (bids were due 25/05/2026, still 'In desfasurare').

- **Implies:** Printec line 2 (self-service kiosks and branch transformation, x-visio) plus line 3. Romanian municipalities are systematically outsourcing counter cash/card collection to self-service estates — a repeatable, tenderable segment where Printec's kiosk + cash-recycling combination is stronger than SelfPay's card-only terminals.
- **Deadline:** 10/09/2026 | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notices CN1095003, CN1094319, SCN1175047 — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Bid or partner on CN1095003 before 10/09/2026; build a reusable Romanian municipal self-service reference from it.

### 16. Banca Transilvania (RO 5022670) — XL (27/08/2026)

COMPETITOR WINS — CARD ACCEPTANCE: CAN1167036 and CAN1167026, Municipiul Cluj-Napoca (both 05/05/2026), e-commerce/SNEP card acceptance RON 445,000 and assisted-POS card acceptance RON 310,000, contract 443192/444151 of 02/04/2026. CAN1165049 Municipiul Baia Mare (18/08/2026) 'Servicii bancare pentru încasarea online a impozitelor şi taxelor locale prin platforma Globalpay', 4 contracts totalling RON 4,990,000, latest 10/08/2026. CAN1166131 Direcţia Fiscală Braşov (30/06/2026), 4 contracts, RON 1,032,525. Plus direct award DAN2841294 (27/08/2026) Comuna Bucerdea Grânoasă, SNEP card acceptance, RON 1,500.

- **Implies:** Printec line 3. BT is Romania's largest POS acquirer (roughly 30% of the national POS estate per Romanian banking press) and is winning municipal acquiring on its Globalpay platform. Its terminal estate growth is the largest single Romanian POS-hardware and TMS opportunity.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices CAN1167036, CAN1167026, CAN1165049, CAN1166131; DAN2841294 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Direct approach to Banca Transilvania cards/acquiring on Verifone/Castles terminals, TMS and softPOS; use the Globalpay municipal wins as the estate-growth evidence.

### 17. Banca Comercială Română (BCR, 361757) and Garanti Bank (25394008) — L (10/08/2026)

COMPETITOR WINS — PUBLIC-SECTOR BANKING/ACQUIRING: BCR won CAN1168584 Ministerul Dezvoltării (28/05/2026) banking-fee services RON 350,000; CAN1171655 DGRFP Craiova (30/07/2026) financial-banking services for the Caracal and other Treasury units, 6 contracts, RON 825,654; CAN1131180 DGRFP (10/08/2026), 10 contracts, RON 743,804; plus recurring monthly POS acquiring direct awards to Jandarmeria Română (DAN2808333/DAN2808335/DAN2808344, 14/07/2026) and Ministerul Justiţiei (DAN2746843, 04/05/2026, RON 33,333.28). Garanti Bank won CAN1089500 ANCPI (04/06/2026) 'Servicii de procesare a plăţilor electronice online cu card bancar', 50 contracts totalling RON 3,854,878.86. BRD Groupe Société Générale (361579) won CAN1169628 Municipiul Bucureşti (15/06/2026) current-account services, RON 44,736.

- **Implies:** Printec line 3 and line 12. BCR is a named Printec APTRA reference already; these wins confirm BCR and Garanti are expanding public-sector card acceptance and therefore terminal estate. Reinforces that the Romanian opportunity is bank-side, not tender-side.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices CAN1168584, CAN1171655, CAN1131180, CAN1089500, CAN1169628; direct awards DAN2808333/5/44, DAN2746843 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Leverage the existing BCR APTRA relationship into terminal management and cash-recycling conversations off the back of its public-sector acquiring growth.

### 18. Compania Naţională de Administrare a Infrastructurii Rutiere (CNAIR) and SNTFC CFR Călători — XL (21/07/2026)

CLOSED, AWARD PENDING — LARGE PAYMENT-ACCEPTANCE TENDERS: CN1093434 CNAIR 'Servicii de plata on-line (tip e-commerce) in vederea desfasurarii activitatilor de comert electronic', CPV 66110000, estimated RON 27,966,000, bids were due 21/07/2026 — as at 27/08/2026 still 'In desfasurare', no winner. CN1093496 CFR Călători 'Servicii de plată a legitimațiilor de călătorie cumpărate cu card bancar contactless prin dispozitivele CFR Călători' (payment services for tickets bought by contactless bank card on CFR devices), estimated RON 1,400,000, bids were due 16/07/2026 — also still 'In desfasurare'. A comparable award already landed: CAN1171048 Transport Public S.A. (09/07/2026) account-based-ticketing system integrated with contactless card payment at dual validators — WINNER RADCOM S.A., RO 3939511, contract 1919 of 03/07/2026, RON 3,956,994.

- **Implies:** Printec line 3 (acceptance/terminal management) in the open-loop transit segment — the Romanian counterpart of the unresolved HAC Croatia open-loop card-acceptance tender in the baseline. CNAIR at RON ~28m is the largest single acceptance opportunity found on this portal this run.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notices CN1093434, CN1093496; award notice CAN1171048 — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Chase the CNAIR award and name the acquirer; assess whether Printec can supply the validator/terminal and key-management layer behind whichever acquirer wins.

### 19. Autoritatea Naţională pentru Administrare şi Reglementare în Comunicaţii (ANCOM) — M (27/07/2026)

STATUS OF CARRIED ITEM — STILL OPEN: CN1094796, framework for the supply of access-control systems ('sisteme de control acces'), estimated RON 1,289,016, published 27/07/2026, bids due 31/08/2026 15:00; SICAP state 'In desfasurare' as at 27/08/2026. Confirms the baseline entry.

- **Implies:** Printec line 8 (physical security). Small and peripheral to banking, but it is the carried baseline item and it is genuinely still biddable.
- **Deadline:** 31/08/2026 | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notice CN1094796 (procedureId 100328213) — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Confirm the outcome next run; low priority for Printec.

### 20. Distribuţie Energie Electrică România S.A. (DEER) — XL (22/07/2026)

CANCELLED: 'Sistem securizare contoare PKI-HSM' (PKI/HSM meter-security system), CPV 48000000, estimated RON 27,049,693.92. Contract notice CN1094028 published 02/07/2026 with bids due 30/07/2026; cancellation confirmed by award notice CAN1171744 published 22/07/2026 — SICAP procedure state 'Anulata' on both records.

- **Implies:** Printec line 9 (HSM/key management). The largest HSM-scale opportunity visible in Romania this quarter — roughly EUR 5.4m — was cancelled before bids closed. It is very likely to be re-tendered with revised requirements, as happened with the PrivatBank recycler procedure in the baseline.
- **Deadline:** — | **Win:** Medium | **Confidence:** Medium | **New:** True
- **Source:** SICAP contract notice CN1094028 and cancellation notice CAN1171744 — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Set a watch on DEER (RO14476722) for the re-issued PKI-HSM notice; prepare a Thales payShield / key-management position for smart-metering PKI, which is adjacent to but distinct from payment HSM.

### 21. Romanian e-signature / digital-identity market (CERTSIGN, DIGISIGN, Centrul de Calcul, Insight Group) — M (27/08/2026)

HIGH-FREQUENCY DIRECT AWARDS: the SICAP direct-acquisition feed for 01/05/2026-27/08/2026 returns 151 hits for 'semnătură electronică' (electronic signature). Repeat named winners across public buyers include CERTSIGN S.A. (RO18288250 — e.g. DAN2747217, DAN2747507, DAN2749108, DAN2750720), DIGISIGN S.A. (RO 17544945, DAN2748797), Centrul de Calcul S.A. (RO 2163993, DAN2745702 CNAIR qualified-signature kit RON 7,000; DAN2745851), Insight Group (RO 16674319) and GO SERV (RO 6919950). Individual values are tiny (RON 95-7,000 per certificate/kit).

- **Implies:** Printec line 5 (digital identity, onboarding, e-signature — Namirial, eIDAS/EUDI). Romania has an entrenched domestic qualified-trust-service duopoly (CertSign, DigiSign) selling at commodity prices to the public sector. Printec's differentiation is not certificates but the eIDAS/EUDI-wallet onboarding and remote-signing workflow sold into banks, where CertSign/DigiSign are the incumbents to partner with or displace.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP direct-acquisition award feed, contractObject='semnatura electronica' (151 results) — https://www.e-licitatie.ro/pub/da-award-notices/list/0
- **Follow-up:** Position Namirial-based remote onboarding/e-signature at Romanian banks, treating CertSign/DigiSign as the certificate layer; do not chase public-sector certificate direct awards.

### 22. Romanian self-service kiosk and queue-management niche (ANDAN IMPEX, Romflex Sistem) — S (15/07/2026)

COMPETITOR WINS — QUEUE MANAGEMENT AND KIOSKS: SCNA1134637 (03/07/2026) DGRFP Timişoara, 'Achizitie Sistem de management al cozilor pentru sediul AJFP Hunedoara' (queue-management system for the AJFP Hunedoara office) — WINNER ANDAN IMPEX SRL, RO 18130402, contract 6344 of 25/06/2026, RON 38,850 (published from open procedure SCN1175905, est. RON 40,000). The same firm won DAN2753688 (12/05/2026) Municipiul Bacău, 'Inchiriere Printer Kiosk si sistem electronic de dirijare si monitorizare' (printer kiosk plus electronic queue-direction and monitoring rental), RON 30,960. Also DAN2808879 (15/07/2026), Ministry of Defence unit, interactive electronic noticeboards and indoor touch kiosk totems — WINNER Romflex Sistem SRL, RO 16277637, RON 24,300. Open now: SCN1178795, Palatul Culturii Teodor Costescu, 'Echipamente de tip INFOCHIOȘC', est. RON 303,000, bids due 31/08/2026.

- **Implies:** Direct competition with Printec line 2 (x-visio queue management, videobanking, phygital branch). Romanian public buyers are buying queue management at RON 30-40k per site from micro-vendors; the bank-branch equivalent is a far larger, unaddressed market where Printec has no Romanian reference visible on this portal.
- **Deadline:** 31/08/2026 | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notice SCNA1134637; direct awards DAN2753688, DAN2808879; open notice SCN1178795 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Build a Romanian x-visio reference — either via the open INFOCHIOȘC notice or directly at BCR/BT branch-transformation programmes.

### 23. Romanian cash-in-transit and cash-logistics market (Brink's, NEI Divizia de Securitate, RASIROM, NGGS) — M (25/08/2026)

COMPETITOR/PARTNER MAP — CIT: DAN2838872 (25/08/2026) Municipiul Oradea awarded cash transport plus consumable bags to BRINK'S CASH SOLUTIONS (RO) SRL, 14715188, RON 54,014.40. CAN1170835 (03/07/2026) Universitatea din Bucureşti awarded call-off no. 7 for cash transport to NEI DIVIZIA DE SECURITATE S.R.L., RO31718222, RON 126,360 (call-off no. 6 under CAN1167507, RON 42,120, 11/05/2026). CAN1171088 (09/07/2026) Hale şi Pieţe S.A. Ploieşti awarded guarding/monitoring/cash transport to DIRECTOR SPECIAL TROOPS – D.S.T. SRL, 34693246, RON 5,709,250.46. DAN2760730 (20/05/2026) Municipiul Bistriţa to PAZA SI INTERVENTIE S.R.L., 43834956, RON 74,200. DAN2840274 (26/08/2026) ACET Suceava to NGGS SECURITY, 28110550.

- **Implies:** Printec's cash-in-transit adjacency and line 1. Brink's is the only international CIT operator visible; the rest are small domestic guarding firms. CIT operators are the natural channel partners for cash recyclers and smart safes in Romania, since they carry the cash-handling relationship the banks have outsourced.
- **Deadline:** — | **Win:** Low | **Confidence:** Medium | **New:** True
- **Source:** SICAP award notices CAN1170835, CAN1167507, CAN1171088; direct awards DAN2838872, DAN2760730, DAN2840274 — https://www.e-licitatie.ro/pub/notices/ca-notices-c
- **Follow-up:** Approach Brink's Cash Solutions Romania as a channel for recyclers/smart safes; log the domestic firms for Agent 6.

### 24. SEAP/SICAP portal (e-licitatie.ro) — coverage verdict for cash automation — Unscoped (27/08/2026)

NEGATIVE FINDING, DELIBERATELY SEARCHED: across 8,279 contract notices and 16,634 award notices published 01/05/2026-27/08/2026, plus 802 direct-acquisition awards retrieved by 41 Romanian and English keywords, SEAP/SICAP contains NO tender or award for an ATM, cash recycler, intelligent-deposit machine, banknote sorter or teller cash recycler. Every cash-equipment record found is either maintenance of low-cost RIBAO BCS 160 counters at State Treasury offices (CA.DA GRUPP, EUTRON INVEST, OFFICE HQ) or consumables (cash bags at BNR and Poşta Română). A CPV sweep of 30123600/30123620/30123630/30132xxx/42961xxx returned only parcel sorting, e-ticketing and access control. Searched terms included bancomat, ATM, mașină de numărat bancnote, numărare numerar, recycler, depunere numerar, sortare bancnote, terminale POS, ghișeu automat, chioșc/kiosk, self-service, HSM, criptograf, personalizare card.

- **Implies:** Confirms and sharpens the structural verdict for Romania: ATM/recycler demand sits entirely with private commercial banks that are not contracting authorities, so it is invisible to this portal. Printec should treat SEAP/SICAP as a competitor-identification and state-sector (Treasury, BNR, Poşta Română, municipalities) channel only, and pipeline Romanian bank hardware exclusively through direct sales.
- **Deadline:** — | **Win:** — | **Confidence:** Medium | **New:** False
- **Source:** SICAP api-pub NoticeCommon/GetCNoticeList + GetCANoticeList + DaAwardNoticeCommon/GetDaAwardNoticeList, full 01/05/2026-27/08/2026 window — https://www.e-licitatie.ro/pub/notices/c-notices
- **Follow-up:** Reduce SICAP effort to a monthly delta scan on the four proven endpoints; reallocate Romanian research effort to BNR/ARB statistics, bank IR reports and direct bank contact.
