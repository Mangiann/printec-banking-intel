# DORA (Digital Operational Resilience) — Findings 2026-07-15

**Workstream:** DORA / digital operational resilience. **Confidence capped at Medium (single agent).**
**Baseline:** 2026-07-14 run (1 day prior). Report ONLY what is NEW or CHANGED, or citations the prior file never held.

## Plain-language note
- **DORA** (Reg. EU 2022/2554, in force 17/01/2025): EU rulebook forcing banks/PSPs to manage ICT risk, report major ICT incidents, keep a register of ICT third-party contracts, and test resilience.
- **DORA Directive** (Dir. EU 2022/2556): companion directive amending sectoral laws; separate transposition track from the Regulation.
- **RoI** (Register of Information, Art. 28/29): annual xBRL-CSV register of every ICT third-party contract.
- **TLPT** (threat-led penetration testing, Art. 26/27): red-team simulations on the largest entities under TIBER-EU, at least every 3 years.
- **CTPP** (Art. 31): ICT providers designated by the ESAs as systemically critical, placed under direct EU oversight (Lead Overseer + Joint Examination Teams).

## NEW / CHANGED since 2026-07-14

1. **NEW enforcement wave — EC July-2026 infringements package (08/07/2026) targets the DORA *Regulation* itself.** Letters of formal notice to **Spain (INFR(2026)2141), France (INFR(2026)2142), Latvia (INFR(2026)2144)** for failing to notify measures under **Art. 53 of Reg (EU) 2022/2554** — i.e. Chapter VII national rules on **administrative penalties/remedial measures and competent-authority powers** (deadline was 17/01/2025). Two months to respond; reasoned opinion may follow. Primary: EC press corner inf_26_1376. This is distinct from the 27/03/2025 letters over the DORA *Directive* (2022/2556) to 13 MS incl. BG/SI/GR/RO. None of ES/FR/LV are Printec footprint, but it shows even the Regulation's sanctions regime is still un-notified in major MS.
   - CORRECTION to an aggregator snippet: BG and SI did NOT receive DORA reasoned opinions in the 08/07/2026 package (their July items were waste/AML/EAW, not DORA). The BG/SI DORA-Directive transposition gap remains at the letter-of-formal-notice stage per baseline; no escalation confirmed.

2. **Enrichment — exact TLPT RTS citation (new to findings): Commission Delegated Regulation (EU) 2025/1190**, the Joint RTS specifying elements of threat-led penetration testing under Art. 26/27, published in OJ, application/entry-into-force **08/07/2025**. Covers **pooled/joint TLPT** (entities sharing the same ICT third-party may run a joint test, split costs, with all supervisors' agreement) and use of external testers. Primary: EBA single-rulebook TLPT RTS page. Prior findings referenced TLPT generically but never carried this Del-Reg number or the pooled-TLPT mechanism. Directly serves the threat-led-pen-testing focus.

## RE-VERIFIED (unchanged — log, do not surface as new)
- **CTPP designations: still 19, designated 18/11/2025; NO second designation round as of 15/07/2026.** ESMA CTPP page latest content is a 10/07/2026 Q&A publication (no new designations). List unchanged (AWS/Microsoft/Google Cloud/Oracle/SAP/IBM/FIS/Equinix/Accenture/Capgemini/Colt/Deutsche Telekom/Bloomberg/Kyndryl/InterXion/LSEG/NTT DATA/Orange/TCS). First comprehensive JET examinations + recommendations expected during 2026.
- **RoI cycle-3 reference date 31/12/2026** (submissions early 2027); validation tightened vs 2024 dry-run (6.5% pass) — already captured 14/07.
- **Subcontracting RTS Del Reg (EU) 2025/532**, in force 22/07/2025 — already captured.
- **ESAs first report on major ICT incidents (03/06/2026, 3,383 incidents)** — already captured in 2026-06-24 run; NOT new.

## Printec mapping
- July infringement wave / sanctions-regime uncertainty → Printec compliance positioning; low direct product pull (non-footprint MS).
- TLPT RTS 2025/1190 / pooled TLPT → Printec offers no red-teaming, but its ATM/self-service estate sits inside the test perimeter; where footprint banks share Printec as a common ICT third-party, pooled-TLPT scoping pulls in Printec device telemetry/monitoring as evidence.
- CTPP oversight (19 designated) → Printec not a CTPP but rides several (AWS/Microsoft/Oracle) — indirect assurance / due-diligence talking point.

## Signal rows — see structured output.

## Follow-ups
- Confirm whether a NEW Joint DORA Q&A was published 10/07/2026 (ESMA/EBA Joint Q&A register) and whether it adds pooled-TLPT operational guidance.
- Monitor for a reasoned opinion on BG/SI DORA-Directive transposition (next infringement package ~Oct-2026) and for any ES/FR/LV response closing the Art. 53 gap.
- Watch for a second CTPP designation round (none dated yet).
