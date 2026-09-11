# TED (EU-wide) — Tenders findings — 2026-07-24 (Greece filter)

Slug: ted-eu. Source: TED / Supplement to the EU Official Journal. This run: read pre-fetched cache `intel-cache/ted_notices.json` (TED Search API v3, POST, no auth; generated 2026-07-23; 30-day window; 193 in-scope notices across 10 CEE/SEE footprint countries) and **filtered to Greece (GRC) = 25 notices**. Enriched 4 notices by pulling the TED EN/EL PDF and extracting text locally with pdfminer.six (fetch/Read PDF extractor unreliable — pdfminer worked). Languages: English + Greek. Confidence capped at Medium.

## Method / angles this run
- Cache CPV set: 30123000 / 30144400 / 30142000 (accounting/cash/counting machines) + 35120000 (surveillance/security) + 50310000 / 50312000 (IT maintenance/repair). Greek subset skews municipal digital-transformation + physical security + IT maintenance rather than pure ATM/cash.
- Enriched full Greek-language "Description" blocks for the two largest municipal digital-transformation projects (Αμαρούσι €1.18M, Άβδηρα €396k) and the G-Cloud maintenance notice, to map smart-city / e-payment / cybersecurity modules to Printec.
- Cross-checked framework_drawdown / is_modification flags: several Greek awards are contract MODIFICATIONS (cont-modif), NOT fresh competitor wins — flagged accordingly per cache note.

## Access route map
- TED /pdf route: `curl` with desktop User-Agent → HTTP 200, PDF binary OK. Local `pdfminer.six` extract → full Greek + English text (confirmed on 448960, 448525, 512593, 437788). No block encountered. Claude-in-Chrome not needed.
- No 403/JS/CAPTCHA hit this run (worked off cache + direct PDF).

## Key Greece signals (Printec-relevant subset of the 25)
1. **448525-2026 — Ministry of Digital Governance, G-Cloud central computing infra maintenance/support (Lot 5), €700,000, deadline 03/08/2026 (LIVE).** Managed services / IT-outsourcing lead. Printec managed services.
2. **483191-2026 (re-pub of 477653 / 475593) — Ministry of Citizen Protection, portable thermal-imaging cameras, €2,920,687, deadline 03/08/2026 (LIVE).** Physical-security/surveillance; specialised thermal — adjacent to Printec physical security.
3. **448960-2026 — Δήμος Αβδήρων smart-city digital transformation, €396,434.61, deadline 02/07/2026 (CLOSED).** Description lists an "electronic-payments management system" (module 4) + cyber-security infra (firewall/endpoint, module 6). Maps to Printec payment facilitators + security. Rebid/award watch.
4. **437788-2026 (AWARD) — Δήμος Αλμυρού digital transformation, awarded €367,344.85 (est. €393,756), winners EVOLUTION PROJECTS A.E. + ΕΓΚΡΙΤΟΣ GROUP – ΣΥΝΕΡΓΑΣΙΑ Α.Ε.** Includes 48730000 security software + 35125100 sensors. Competitor win.
5. **498210-2026 (AWARD) — Δήμος Ιάσμου digital transformation, awarded €220,876.63, winners EVOLUTION PROJECTS A.E. + Open Technology Services (ΥΠΗΡΕΣΙΕΣ ΑΝΟΙΚΤΗΣ ΤΕΧΝΟΛΟΓΙΑΣ).** (501879-2026 is a subsequent contract-modification of the same, not a new win.) EVOLUTION PROJECTS = recurring rival in Greek ΟΤΑ digital-transformation.
6. **486444-2026 (AWARD) — Police Dir. of NE Attica, CCTV + alarm upgrade & support 2026–2031, awarded €240,000, winner MEGA SPRINT GUARD ELECTRONIC SYSTEMS Α.Ε.** Physical security managed-services pattern.
7. **512593 / 513012-2026 (contract MODIFICATION, not fresh win) — Δήμος Αμαρουσίου digital transformation Subproject 1, €1,177,120 (total budget €1.477M incl VAT).** Smart-city: sensors, car-park control (34926000), telemetry/surveillance (32441100/200), facilities-mgmt software. Printec: SmartPay/self-service payment kiosks, digital signage. Large municipal smart-city buyer to track for next-phase tenders.
8. **476392-2026 — Ministry of Culture, IT services (incl. network equipment 32561000, maintenance), €299,193.55, deadline 10/08/2026 (LIVE).** Managed services, low-fit.

Non-matches noted (excluded): 434970 photocopiers (Thessaly), 437759 printer-fleet leasing (Δ.Φυλής, won OLYMPIA TELECOM), 446549 landfill operation, 446679/476391 lab equipment, 498817 minibuses, 450111/451797/496347 reprographic maintenance, 458621 migration surveillance modification, 480521/501257 network/rail-IoT modifications.

Competitor incumbents to flag for Agent 6: **EVOLUTION PROJECTS A.E.** (2 Greek municipal digital-transformation wins this window — Almyros + Iasmos), ΕΓΚΡΙΤΟΣ GROUP, Open Technology Services, MEGA SPRINT GUARD (police CCTV), OLYMPIA TELECOM (print-fleet leasing).
