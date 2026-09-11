# Instant Payments & SEPA — Findings 2026-06-24

Workstream: SCT Inst, VoP, SEPA accession, IPR non-euro deadlines, Western Balkans TIPS-clone, national instant schemes (IRIS, RoPay, Serbia SCT Inst). Baseline: 2026-06-15. Confidence capped at Medium (single-agent).

## Jargon (plain language)
- **SCT / SCT Inst** — SEPA Credit Transfer (standard euro transfer) vs SEPA Instant Credit Transfer (settles in <10 seconds, 24/7).
- **VoP (Verification of Payee)** — free pre-payment check that the payee name matches the IBAN, to cut fraud/misdirection. Governed by the EPC VoP scheme rulebook.
- **IPR** — Instant Payments Regulation (EU) 2024/886; mandates banks offer instant euro transfers at no extra cost, with VoP and daily sanctions screening.
- **TIPS clone** — a copy of the Eurosystem's TIPS instant-settlement engine, run by Banca d'Italia for non-EU Western-Balkans central banks.

## Complete current picture (verified vs primary/official sources)

### IPR deadline ladder (ECB IPR page, primary) — CONFIRMED
- Euro area: receive + equal-charges 09/01/2025 (done); send + VoP 09/10/2025 (done).
- Non-euro EU (CZ, HU, RO): RECEIVE + equal-charges 09/01/2027; SEND from EUR accounts + VoP 09/07/2027; SEND from local-currency accounts 09/06/2028 (later tail).
- Non-bank PSPs: receive/send (euro area) 09/04/2027; send (non-euro area) 09/07/2027.
- Sanctions screening: daily since 09/01/2025.

### Bulgaria Art.5a — GAP RESOLVED
BNB Payment Supervision Director (Mihail Dimov, via BTA): Bulgaria has one year after euro adoption — until **01/01/2027** — to implement IPR provisions. (Euro adopted 01/01/2026; on TIPS via BORICA since Dec 2024.)

### SEPA accession / Western Balkans TIPS clone
- North Macedonia: SEPA geographical scope 06/03/2025; PSP operational readiness 05/10/2025; live via 9 banks from 07/10/2025, remaining 3 by end Q1 2026. NM signed TIPS-clone LoI Oct 2025 (now IN, not "later").
- Albania: SEPA accession Nov 2025; 11 banks; 363k SEPA transfers / EUR 4.3bn in first 6 months (BIS, Holta Zaçaj keynote 19/05/2026).
- TIPS clone (AL, BA, XK, ME, MK): "later this year" (2026) per World Bank 25/03/2026; mid-2026 per ECB; no firm bank go-live yet. Banca d'Italia builds the central switch; Printec-addressable layer = bank-side connectivity, onboarding, acceptance.

### National instant schemes
- Serbia: 05/05/2026 go-live is SCT (standard) only; SCT Inst "expected in the coming period" (NBS FAQ) — no firm date. Record 609,155 domestic IPS payments/day 18/05/2026.
- Greece IRIS: now MANDATORY for all businesses; 4.25m users; 1.2m POS terminals + ~70k e-shops; P2P EUR 1,000/day + EUR 5,000/month cap (from 15/01/2026); connected to EuroPA/EPI (ES/IT/PT). ~EUR 11bn projected annual value.
- Romania RoPay 2.0 (eff. 01/09/2025): UniCredit live 02/02/2026; Vista Bank full integration 03/03/2026; ING + bill-pay 23/01/2026. UniCredit no longer a laggard vs baseline.
- Ukraine: SEP 4.1 instant since 01/12/2024; UETR tracking mandatory for all SEP participants 01/04/2026; SEPA bill renumbered **14327-d**, must pass by July 2026 (World Bank DPO condition).

### EPC VoP rulebook
- v1.0 in force 05/10/2025; v1.1 published 16/03/2026, effective **20/09/2026**; v2.0 public consultation 01/04–30/06/2026, publication **end Nov 2026**.

See structured signals[] for the row-level detail and Printec mapping.
