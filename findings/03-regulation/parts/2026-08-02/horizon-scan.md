# Horizon scan — emerging regulation beyond the watchlist
**Agent 3 — Regulation & Deadlines · run 02/08/2026 · status: complete · 15 signals**

## Headline

**Access to cash is hardening from politics into binding law across the footprint, simultaneously.** This is the single strongest emerging theme and it is not on the current ten-workstream watchlist. Five national instruments and one EU regulation are moving in the same direction inside twelve months:

| Jurisdiction | Instrument | Hard date |
|---|---|---|
| EU (euro area) | Regulation on legal tender of euro banknotes and coins, 2023/0208(COD) — trilogues opened 13/07/2026, political agreement targeted end-2026 | — |
| Hungary | MNB Decree 19/2025 (VI.26.) — compulsory ATMs, settlements >500 inhabitants | 31/12/2026 |
| Slovenia | Draft Act on accessibility of cash + free basic payment services — 5 km coverage rule, 5 free out-of-network withdrawals/month | consultation closes 17/08/2026 |
| Slovenia | Constitutional Art. 74.a (UZ74a), Uradni list RS 98/25 | 02/12/2025 (standing) |
| Romania | Bill B409/2026 — personalised ATM withdrawal amounts for any bank's card, fines RON 50k–100k | at Senate, 24/06/2026 |
| Greece | 2025 interbank ATM fee ban, EUR 1.50 cap on third-party ATMs | standing |

**Recommendation to the Orchestrator: promote "Access to cash / legal tender" to its own workstream (XL, footprint-wide ATM driver).**

Second promotion candidate: **"AI Act + supervisory AI expectations"** — Regulation (EU) 2026/1744 (OJ 24/07/2026) delaying Annex III high-risk obligations to 02/12/2027, plus the ESAs frontier-AI statement of 31/07/2026 and the already-captured ECB letter SSM-2026-0301 (JST action plan due 31/10/2026).

## Signals

1. **Hungary — MNB Decree 19/2025 (VI.26.), compulsory ATM installation.** 80 settlement packages allocated to PSPs by weighted formula; contracting deadline 28/02/2026, MNB notification 16/03/2026; press-reported installation deadlines 31/12/2025 (>1,000 inhabitants) and 31/12/2026 (>500). **L / execution-phase.** Printec: NCR Atleos dispensers, x-core, telemetry, OptiCash, field services. Primary: net.jogtar.hu.
2. **Slovenia — draft cash-accessibility law, consultation to 17/08/2026.** 5 km cash point from settlement centre (>1,000 inhabitants), continuous operation, 5 free monthly out-of-network ATM withdrawals. **M.** Printec: recyclers/TCRs, x-core, monitoring, OptiCash.
3. **Slovenia — constitutional Art. 74.a (UZ74a), UL RS 98/25.** [STANDING — dated 2025] Makes cash de-commissioning legally hard. Adoption date needs verification on pisrs.si.
4. **Ukraine — NBU Resolution No. 67 of 16/06/2026, in force 26/06/2026.** New points 124¹–124⁴: mandatory mobile-number entry + OTP verification for ANY cash-in at a PTKS self-service terminal regardless of amount; full number on the receipt; anti-OTP-sharing measures. Also creates the new "bank of financial inclusion" licence. ~22,930 terminals + 15,750 ATMs. **M.** Printec: x-core/kiosk screen flows, telemetry, INETCO/Siron for mule detection. **Primary PDF verified locally.**
5. **Ukraine — new UAH 2,000 banknote enters circulation 04/09/2026.** 38,690 devices to reconfigure (15,750 ATMs + 22,930 PTKS); NBU providing configuration capability free of charge. **S / win High** — pure field-services and note-set rollout window, closing in ~5 weeks.
6. **Romania — bill B409/2026 (Senate, 24/06/2026)**, amending Legea 209/2019: personalised withdrawal amounts at all ATMs for all cards; RON 50k–100k fines. **S.** Printec: x-core screen-flow change across mixed estates + OptiCash denomination re-tuning. Press-sourced — needs senat.ro primary.
7. **EU — Regulation (EU) 2026/1744 "Digital Omnibus on AI"**, OJ 24/07/2026, in force 27/07/2026. Annex III high-risk (incl. creditworthiness scoring) now applies 02/12/2027; Annex I 02/08/2028. Qualification burden on Printec's AI-bearing products (Siron, FICO, INETCO, Namirial). **Primary: EUR-Lex.**
8. **EU — legal tender of cash Regulation, 2023/0208(COD).** ECON report Nov-2025 (46-4-8); Council position Dec-2025 requiring Member States to monitor and safeguard cash access/acceptance; trilogues opened 13/07/2026. **L, promotion candidate.**
9. **EU — FiDA, 2023/0205(COD).** Still in trilogue; Commission non-paper circulated as WK 5041/2026 INIT, 06/04/2026. No adoption or application date exists. **Watch slot, Low confidence.**
10. **EU — EBA DGSD3 first four consultations, 23/07/2026, comments close 23/10/2026.** Depositor-information ITS, information-exchange ITS, client-funds RTS, DGS investment guidelines. **M.** Printec: document management, eKYC delivery of the depositor sheet, customer-data remediation.
11. **EU — ESAs joint call on ICT risks from frontier AI models, 31/07/2026** (following ESAs support for the ESRB warning, 07/07/2026). DORA CTPP oversight to be updated. Converges with ECB SSM-2026-0301 (action plan 31/10/2026) into a legacy-replacement driver — and an obligation on Printec as an ICT third party.
12. **Austria — FMA becomes the financial-sanctions supervisor from 01/01/2026**, taking over from the OeNB and combining AML/CFT and sanctions supervision with coordinated audit cycles. **M.** Printec: IMTF Siron, FICO, INETCO. New regulator + new source environment (fma.gv.at).
13. **North Macedonia — single register of accounts at the Central Register by 01/12/2026**; six systemically important banks named 30/10/2025 with systemic buffers fully implemented by 30/09/2026. **S, aggregator-only / Low** — needs nbrm.mk primary.
14. **PCI — no new 2026 cliff.** [STANDING] v4.0.1 is the only version; all v4.x future-dated requirements effective since 31/03/2025 and fully in scope for 2026 assessments; PCI PIN remains v3.1 (no v4); TR-31 Phase 3 passed 31/12/2024. RFC on v4.0.1 closed 20/07/2026 — watch for the next revision. Recorded as a negative finding.
15. **Bulgaria — post-euro** [STANDING]: ATMs dispense euro only from 01/01/2026 and there is **no obligation** to accept lev at deposit-capable self-service machines — pushing residual lev volume to tellers, which is a TCR argument. Belongs to the euro-adoption workstream; recorded to confirm no *new* Bulgarian cash-access mandate exists.

## Negative findings (do not re-research)

- No new PCI DSS / PCI PIN deadline in 2026.
- No revision of the Interchange Fee Regulation: consumer caps stay 0.2% debit / 0.3% credit, inter-regional tourist rates to 2029; attention has shifted to scheme-fee transparency, not new caps.
- No new Czech or Bulgarian cash-access mandate found.
- No new Serbian NBS cash-access decision beyond an exchange-operations decision of 12/03/2026 (applied 16/03/2026) and a June-2026 ATM daily-limit notice.

## Gaps

Kosovo (BQK), Montenegro (CBCG), Bosnia & Herzegovina (CBBH + entity agencies) and Albania (Bank of Albania) returned nothing horizon-relevant outside the instant-payments workstream — they need a dedicated Albanian / Bosnian-Croatian-Serbian / Montenegrin pass next run. Cyprus (CBC) and Croatia (HNB) likewise. Visa/Mastercard CEMEA operating bulletins are a structural blind spot (not openly published).

## Access

- `consilium.europa.eu` 19/12/2025 press release — 403; substituted by the EP Legislative Train primary page; desktop-UA retry logged for next run.
- `bank.gov.ua` news pages — 403; **route used:** `site:` search to find the primary PDF, then `curl` with a desktop Chrome UA + local `pdfminer` extraction (pdftotext not installed). This works reliably for NBU law and should be the default route.
- `fma.gv.at` (EN and DE) — 403; Austria row rests on the search index, not a fully opened page.
- `nbrm.mk` not opened (known 403); North Macedonia row is aggregator-tier.

## Operator requests

1. Visa CEMEA / Mastercard Europe-CEMEA 2026 operating-regulation bulletins (acquirer portal access needed).
2. senat.ro file for legislative initiative **B409/2026** + attached PDF.
3. Slovenian MoF draft **"Zakon o dostopnosti gotovine in brezplačnih osnovnih plačilnih storitvah"** from e-uprava.gov.si / eDemokracija.
4. Annex to Hungarian **NGM Decree 16/2025 (V.29.)** settlement list + the MNB per-PSP allocation table.
