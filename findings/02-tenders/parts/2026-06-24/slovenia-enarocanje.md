# Slovenia — e-narocanje (enarocanje.si / e-JN) — ATM / Self-Service / POS tenders

Run date: 2026-06-24. Slug: slovenia-enarocanje. First dedicated Slovenia pass (no prior baseline file found).

## Portal map
- enarocanje.si = official public-procurement notice portal (Uradni list / Portal javnih narocil). Notice display URL pattern: https://www.enarocanje.si/Obrazci/?id_obrazec=NNNNNN
- ejn.gov.si / e-JN = the electronic bidding system (Aktualna javna narocila: https://ejn.gov.si/ponudba/pages/aktualno/aktualna_javna_narocila.xhtml — JS-heavy)
- Banka Slovenije (central bank, Eurosystem member) publishes via enarocanje.si.

## Context
Slovenia is in the euro area; ATM/cash-handling demand driven by commercial banks (NLB, SKB/OTP, Nova KBM/OTP-merged, Intesa Sanpaolo Bank, UniCredit, SID, Delavska hranilnica, Gorenjska/DBS) + Banka Slovenije cash centre. Most commercial banks are PRIVATE -> they do NOT tender publicly; their ATM/POS sourcing is invisible on enarocanje.si. Public-sector hits = Banka Slovenije + state-owned entities.

## Key findings
1. ATM (bankomat) procurement is NOT publicly tendered in Slovenia. CPV 30123600 (cash dispensers) on the openprocurements mirror = "Ni arhiviranih javnih narocil" (no archived tenders). Commercial banks (NLB, Nova KBM/SKB-OTP, Intesa Sanpaolo Bank SI, UniCredit, Delavska hranilnica, Gorenjska/DBS) are private and buy ATMs off-portal -> invisible on e-narocanje. THIS IS THE FINDING, not a gap.
2. UJP POS terminal tender (PUBLIC, open-tendered): Ministrstvo za finance — Uprava RS za javna placila (UJP), "Najem in vzdrzevanje POS terminalov ter zagotavljanje placila obveznih dajatev" — 26 POS terminals + portable units for tax-payment desks. Contract value 108,547.12 EUR incl VAT. enarocanje id_obrazec=338440; e-JN zadevaId=15443. Small-value, recurring. Maps to Printec Verifone/Castles + TMS. Winner not retrieved (ASP.NET page JS-blocked to tools).
3. Posta Slovenije: 1,600+ POS terminals deployed across counters + mail carriers (SmartPOS app on carrier phones), acquiring partner = OTP banka (cards: Visa/Mastercard/Maestro/Diners). Large installed POS base -> maintenance/refresh/TMS angle. Posta also tendered ECB-tested euro banknote-counting machines (enarocanje id_obrazec=124911) — maps to Printec Glory/NCR cash automation.
4. Nova KBM + SKB (both OTP-owned) merged ATM networks into a shared ~450-ATM fleet (2023). Consolidated fleet -> rationalisation/refresh + multivendor software (x-core) angle; sourced privately, pursue OTP group directly.
5. Posta Slovenije modernisation: self-service points, digital displays, 24/7 access at branches + 450 Direct4.me smart parcel lockers (113 locations) — adjacent self-service/kiosk relevance (note: locker network press was 2020; modernisation ongoing).

## Access issues
- enarocanje.si /Obrazci/?id_obrazec=NNN pages are ASP.NET/JS — WebFetch returns only the "Portal javnih narocil" shell; bodies read only via Google snippets. /api/datoteka/get?id=... PDF route is GET-readable but needs the base64 doc id.
- ejn.gov.si (e-JN active tenders) = JSF/JS-only.
- openprocurements.com mirror IS WebFetch-readable for buyer/supplier/CPV pages — best route; but recent (2025-26) rows sparsely indexed.
- No connected Chrome browser this run -> Claude-in-Chrome unavailable.
- OPERATOR: confirm winner + current status of UJP POS tender (id 338440) and whether a 2025/26 re-tender exists; POST e-JN expert-search would unblock.

## Signals — see structured rows.
