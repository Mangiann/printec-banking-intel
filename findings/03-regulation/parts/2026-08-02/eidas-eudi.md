# eIDAS 2 / EUDI Wallet & eID - Agent 3 (Regulation & Deadlines) - run 02/08/2026

Status: **complete**. 23 signals. Resumed from a partial checkpoint (12 signals kept) and closed the listed gaps.

## Key dates
- **24/12/2024** - first five wallet implementing acts (CIR 2024/2977, 2979, 2980, 2981, 2982) enter into force. Start of both clocks.
- **11/08/2026** - CIR (EU) 2026/1731 and 2026/1730 (OJ 22/07/2026) enter into force: updated wallet standards (SD-JWT VC, ISO mdoc, Token Status Lists, CTAP 2.3) and automated relying-party access certificates under ETSI TS 119 411-8.
- **24/12/2026** - every Member State must offer at least one EUDI Wallet (Art. 5a(1)); national relying-party registers start applying (CIR 2025/848).
- **01/06/2027** - **North Macedonia**: national law transposing Reg (EU) 2024/1183 starts to apply, including the private-sector acceptance duty naming banking and financial services.
- **24/12/2027** - EU banks above the micro/small threshold must accept EUDI Wallets on user request (Art. 5f(2)).

## Footprint readiness (fresh this pass)
| Market | Status | Tier |
|---|---|---|
| Greece | gov.gr Wallet, 13 documents, ~2.5m digital IDs | primary |
| North Macedonia | Law applies 01/06/2027, wallet + bank acceptance duty in statute | primary |
| Kosovo | Law 08/L-022 already mandates a Digital Identity Portfolio; acceptance permissive | primary |
| Albania | 2025 draft law aligned to Reg 2024/1183 with Art. 5f(2)-equivalent | primary (draft) |
| Romania | EUDIW-PACT project, CEI card as enrolment anchor | primary |
| Czechia | DIA: government has NOT chosen a delivery model | primary |
| Montenegro | NS eID under Sl. list CG 72/2019; no wallet duty | primary |
| Slovakia | NBU certification scheme EUDIW-SK effective 22/06/2026 | press |
| Croatia | certified wallet planned Q4-2026, private services integrated | press |
| Bulgaria | draft wallet law in consultation 17/02/2026; launch by Dec-2026 doubtful | press |
| Cyprus | Digital Citizen app; minister says all firms must accept digital documents | press |
| Slovenia | ministry signals end-2026 or early 2027 | press |
| Austria | ID Austria + eAusweise, strongest base; wallet route undecided | press |
| Hungary | 29/2024 MNB rendelet remote CDD + DAP eID | regulator |
| Ukraine | NBU Resolution No.1 of 08/01/2026 rebuilds BankID | regulator |
| Serbia | eID.gov.rs ConsentID + cloud QES, no wallet duty | primary |
| Bosnia & Herzegovina | IDDEEA PKI/QES, no wallet duty | press |

## Printec read-across
Every row lands on the same stack: a wallet-agnostic **verifier inside digital onboarding/eKYC (Namirial)**, **Thales HSM / remote key injection** for relying-party access certificates, **AML/KYC screening (IMTF Siron, FICO)** because wallet PID does not discharge full CDD, **document management** for retained identity evidence, and - where a national wallet is already in citizens' hands (GR, AT, SK, HR) - an identity-verified use case on **self-service kiosks and ATMs (NCR x-core)**.

## Honest gaps
- **AMLR Art. 22** (the provision linking EUDI wallets to customer due diligence) could not be verified: EUR-Lex returns zero-byte HTTP 202 for CELEX 32024R1624 on every route. Not asserted anywhere in the signals. Operator request raised.
- **No footprint central bank has issued supervisory guidance on wallet-based identification for AML purposes.** Searched across all 17; not found. The absence is the finding.
- **No eIDAS 2 enforcement action or fine exists anywhere yet.**
- Bulgarian **DV 55/2026** amendment from the previous run could not be corroborated; treated as a correction, not a fact.