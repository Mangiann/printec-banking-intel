# PSD3 / PSR — Findings 2026-06-24

**Workstream:** PSD3 (Third Payment Services Directive) + PSR (Payment Services Regulation).
**Baseline:** 2026-06-15 ("awaiting OJ publication, expected Jun/Jul 2026, may slip to Sep").
**Confidence:** capped Medium (single-agent). Specialist-legal sources used where EUR-Lex/EP primary not yet final (file not yet in OJ).

## Plain-language jargon (first use)
- **PSR** = directly-applicable EU Regulation (no national transposition needed) carrying the conduct-of-business payment rules (fraud, VoP, open banking, SCA). **PSD3** = the accompanying Directive (licensing/authorisation of PSPs), which each member state must transpose into national law.
- **VoP (Verification of Payee) / IBAN-name check** = before a transfer, the payer's bank checks the payee name matches the IBAN and warns the payer on mismatch.
- **APP fraud / spoofing** = authorised push-payment fraud, where a scammer tricks the customer into authorising a payment (e.g. by impersonating the bank).
- **SCA** = Strong Customer Authentication (two-factor). **AISP/PISP** = open-banking account-information / payment-initiation providers.

## Status (re-verified this run — MATERIAL CHANGE vs baseline)
- Provisional political agreement EP+Council: **21/11/2025**. COREPER endorsement **22/04/2026**; final compromise texts published **23/04/2026**.
- **ECON committee approved the agreed 2nd-reading text 05/05/2026** (roll-call 50–3–5).
- **As of this run (per official EP Legislative Train, version 22/05/2026): NOT yet adopted by plenary, NOT adopted by Council, NOT published in the Official Journal.** Next step = formal Parliament plenary vote + Council adoption, then OJ. The baseline's "expected Jun/Jul" OJ date is therefore **still pending / not yet occurred** — no confirmed OJ date exists yet.
- Application clock: PSR generally applies **~18 months** after entry into force (one specialist source says 21 months after OJ); **VoP / payee-name verification and the related liability provisions carry a longer ~24-month** transition (Norton Rose). PSD3 national transposition ~18 months; targeted market readiness H2-2027 → Q2/Q3-2028.

## Content confirmed
- **Fraud liability shifts to PSPs/ecosystem:** spoofing/impersonation treated as unauthorised → full PSP reimbursement (if customer reports to police + notifies PSP); **online platforms** liable to reimbursing PSPs if told of fraudulent content and fail to remove it; **telecoms/device makers** must give payment apps non-discriminatory data access; technical service providers & scheme operators face SCA-failure liability.
- **VoP mandatory** across all credit transfers (mismatch → warn/refuse).
- **Open banking:** PSD2 architecture broadly retained; dedicated APIs with performance parity, permissions dashboards, prohibited-obstacles list, **fallback interface replaced by structured contingency/supervisory mechanism**; AISP re-authentication every 180 days.
- **SCA:** extended to tokenised instruments; PSPs must offer multiple SCA means free of charge.

## Printec mapping
- Fraud-liability shift + mandatory VoP → strong pull for **transaction monitoring (INETCO), AML/fraud (FICO, IMTF Siron)**, real-time payee-verification/fraud-scoring tooling. Banks now financially own APP-fraud losses → measurable ROI for fraud analytics.
- SCA expansion + acquiring conduct rules → **POS/TMS (Verifone/Castles), SoftPOS**, authentication on self-service/kiosks.
- Open-banking API parity + contingency → integration/monitoring; **device telemetry/monitoring** ties to DORA resilience evidence.
- Budgets commit ~6–12 mo before application → with OJ likely H2-2026 and ~18-mo clock, **fraud/VoP budget commitments land H2-2026 → 2027**.

## Signals — see structured rows. is_new flags the procedural change (ECON-approved, still pre-OJ) vs the 15/06 "awaiting OJ".

## Access / gaps
- Lexology final-compromise-text article returned HTTP 403 (logged; substituted EP press release + Norton Rose + Worldline + Freshfields + EP Legislative Train).
- No confirmed OJ date exists yet; staggered per-provision calendar dates cannot be pinned to primary text until OJ publication. Re-check EP plenary agenda + EUR-Lex next run.
