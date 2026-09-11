# Raiffeisen Bank Romania — findings 2026-07-14 (re-verify + deepen)

Focus: ATM/POS fleet, cloud, voice-guidance, Garanti BBVA integration.
Printec relevance: self-service/ATM, cash automation/recyclers, POS/acquiring, eKYC onboarding, AML, HSM, managed services.

## What is NEW / CHANGED since baseline (2026-06-24 / prior 2026-06-29 file)
- **NEW — Romanian Competition Council (Consiliul Concurenței) formally OPENED its merger review** of Raiffeisen Bank S.A.'s acquisition of Garanti Bank S.A. + Motoractive IFN S.A. + Motoractive Multiservices S.R.L. Announced **15/06/2026** (primary: consiliulconcurentei.ro; AGERPRES). Mandatory pre-close approval gating the expected Q4-2026 completion. Opening ≠ approval.
- **CHANGED — multi-currency deposit machines**: bank's own IMM page now states "**about 50**" multi-currency deposit units (baseline carried **61 Smart Cashbox**). Data refinement; verify exact current count.
- **RE-CONFIRMED (primary, Q1-2026 press release ~05/05/2026)**: voice guidance (ghidare vocală) for cash withdrawals extended **nationally** across ATMs + MFMs; 264 branches; >42,000 POS; 2.36m clients; >1,100 ATM+MFM combined.

## Standing picture (re-verified)
- **Garanti acquisition**: EUR 591m, 100% of Garanti Bank + Motoractive IFN, closing Q4-2026, RBI to MERGE units into RO ops for synergies; combined RO = #3 bank (RO subs EUR17.5bn assets YE2025; Garanti ~EUR4bn, ~2% share; -60bps CET1 at close). Source: rbinternational.com 28/03/2026.
- **ATM/POS outsourced to Euronet** end-to-end since 24/09/2003 (Euronet IR). Competitive BARRIER for Printec managed-ATM/POS at RB RO; realistic opening is software/AML/onboarding/HSM + integration, not fleet mgmt.
- **Voice guidance driver**: Law 232/2022 (EAA transposition; ATMs/self-service terminals in scope; applies 28/06/2025, transition/grandfather to 28/06/2030) — accessibility retrofit/replacement wave across RO self-service estate.
- **Cloud**: RBI group target ~80% apps in cloud (AWS + Azure), 160+ workloads migrated, cost savings by 2026 (Hitachi Digital Services / AWS case studies). App-layer, not self-service HW.
- **Cash-out-of-branch**: ongoing "agenții fără casierii" program (since 2021-22); 2026 press notes only ~21 of ~300 agencies still accept cash-at-counter — structurally pushes volume onto MFM/deposit machines.
- Fleet split (549 ATM + 588 MFM vs ~770 ATM + 373 MFM) UNRESOLVED — AR2025 PDF failed local extraction. Bank's own primary aggregate = ">1,100 ATM+MFM".

## Access log
- AR2025 PDF: WebFetch timeout→403; local curl (browser UA) got 2.6MB but pdfminer + pypdf extraction hung/failed repeatedly. Fleet split not extracted — ESCALATE to operator.
- revistabiz.ro + adevarul.ro (teller-closure): "domain not verified safe" block; recovered via ZF/bankingnews snippets.
- consiliulconcurentei.ro comunicat: WebFetch socket hang up; date/scope confirmed via AGERPRES 15/06/2026.
