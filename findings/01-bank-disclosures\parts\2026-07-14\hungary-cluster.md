# Hungary banking cluster — findings 2026-07-14

Focus: Act XVIII ATM mandate, OTP eMACH.ai core, MBH integration, AML fines.
Baseline compared: 2026-06-29 (disclosures) + 2026-07-14 (EKR tenders).

## HEADLINE NEW/CHANGED this run
- NEW PRIMARY — MNB decision H-KPL-I-B-5/2026 vs MBH Bank, dated 07/05/2026 (mnb.hu PDF, extracted locally). MNB fined MBH 15,000,000 HUF and imposed cash-machine/ATM obligations after an on-site inspection of its cash-handling and ATM network:
  - From 01/07/2026: banknotes may be recirculated through ATMs/customer-operated cash machines ONLY if authenticity/fitness is checked by a note-validator that is on the MNB list with the exact required HW/SW version (implies MBH ran non-listed/outdated validators).
  - From 01/07/2026: free acceptance of <=50%-damaged forint notes and forwarding to MNB; A-category notes flagged on re-check must be surrendered, not recirculated.
  - From 01/08/2026: guarantee >=98% annual-average availability across its cash-machine network (ex force-majeure/seasonal).
  - Extraordinary reporting: availability action-plan by 30/06/2026; training evidence by 15/07/2026; monthly availability data (Aug-Oct) by 10/11/2026, split deposit vs withdrawal, with downtime cause.
  - PRINTEC-CRITICAL: recyclers with MNB-certified note validators, cash automation, ATM managed-services / uptime SLA, transaction/availability monitoring.
- NEW theme — sector-wide 98% ATM-availability + MNB-listed note-validator rule under MNB rendelet 1/2023 (I.17.) as amended, binding on ALL cash-machine operators in 2026. MBH first named enforcement; OTP/K&H/Erste exposed to same standard as Phase-2 fleets scale.
- NEW — OTP + Mastercard executed Hungary's first live AI-agent-initiated transaction (Agent Pay), ~06/05/2026. Signals OTP digital momentum; no confirmed eMACH.ai/IDC core go-live (contract 08/12/2023, parallel OTP HU + DSK BG).
- RE-VERIFIED — MBH IT integration completing 2026; accounts unified from 01/01/2026 (post 31/12/2025-04/01/2026 bankszunnap). Feb-2026 systems outage. Channel/ATM-driver integration window persists.
- RE-VERIFIED — Act XVIII / MNB decree 19/2025 (VI.26.): Phase-1 (>1,000 pop) MET 31/12/2025; Phase-2 (>500 pop) due 31/12/2026 (~5.5 months). 1,039 net-new ATMs (~4.156bn HUF). AB complaint pending, rollout continues.
- Fleet (Origo 15/01/2026): OTP ~2,000; MBH 1,200; K&H 639; Erste 491; UniCredit 195; CIB 156. New Act XVIII units: MBH 316, OTP 128, K&H 92, CIB 38, Erste 36, UniCredit 17. Deposit-capable: OTP 536, K&H 448, Erste 260, MBH 252, UniCredit 94, CIB 70.
- Competitive flag — Erste HU POS/SoftPOS/vPOS locked to Teya (25/03/2026); closes Erste acquiring to Printec POS.

## AML fines (RE-VERIFIED, not new; Jan-2025)
OTP 28.125m HUF, MBH 15m HUF (07/01/2025 MNB); K&H 20.5m HUF (separate). Not re-fined for AML in 2026 (the 2026 MBH fine is cash-handling, not AML).

## Access / coverage
- mnb.hu, otpbank.hu, fintechzone.hu, uzletem.hu blocked to WebFetch -> curl desktop-UA + local pdfminer. Logged.
- Snippet claimed OTP "H-KPL-I-3/2026" cash-machine fine; NOT confirmable on OTP felugyeleti-hatarozatok (only H-FK consumer decisions). Likely conflation with MBH case -> NOT reported. Operator to verify on mnb.hu hatosagi-dontesei.

## Signal rows -> see structured output.
