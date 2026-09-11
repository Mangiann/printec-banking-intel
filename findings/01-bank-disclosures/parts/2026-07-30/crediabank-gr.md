# CrediaBank (ex-Attica Bank) — Bank Disclosures, run 2026-07-30 (FINAL)

Slug: `crediabank-gr`. Greece's 5th pillar (Attica + Pancreta, rebranded 07/2025). CEO Eleni Vrettou, Chairman Konstantinos Herodotou. ATHEX: CREDIA. Q1-2026: **66 branches** (77 a year earlier, -14%), **1,204 group FTEs** (1,408, -14%), ~350k active customers, gross loans €4.9bn, deposits €6.8bn, CET1 16.6% / TCR 22.4% pro-forma for the €300m SCI.

## Headline for Printec

**Malta is the deal.** The new **Corporate Presentation – June 2026** — a deck no prior run had seen — says it in the bank's own words: *"HSBC Malta needs a 'restart'"*, *"Over a decade of operations under non-core status"*, *"Underinvested in IT and personnel"*, *"Reshape operational processes"*, with synergies from *"Cost and efficiency optimisation (in-sourcing, tech investments, modernisation, digitalisation)"*. HSBC Malta's own FY2025 accounts corroborate with hard accounting: a **€3.1m notable item for accelerated software amortisation "in anticipation of the prospective transfer to CrediaBank"**, repeated into Q1-2026 (+12% costs).

And the clock is explicit: **SPA Dec-2025 (done) → MFSA file Jan-2026 (done) → target operating model finalised Apr-2026 (done) → Q4-2026 MFSA + ECB change-of-control approval and operational readiness (ongoing) → April 2027 Legal Day 1.** The TOM is already written and operational readiness is the live workstream, so Malta technology procurement is happening **now**, not after Legal Day 1.

Caveat that sharpens the pitch: HSBC Malta **completed replacement of its ATM fleet across Malta and Gozo during 2025**. Malta is a software / cash-automation / AML / monitoring / managed-services opportunity, not new ATM boxes.

## What's NEW / CHANGED vs the 2026-07-24 file

1. **Corporate Presentation – June 2026** (new primary deck) — the "restart / underinvested in IT" language, the milestone-status Malta roadmap, the branch/FTE rebase, and *"Program launched, first deliveries expected in 3Q26"* for digital transformation.
2. **Thessaloniki New Experience branch, 04/02/2026, Tsimiski 8** — never captured before. Primary PDF names **TCR machines**, **card recognition at entry**, **CrediaConnect remote-service points**, and the **FORTH/ITE** interactive product-discovery system.
3. **Official New Experience branch locator now names eight live sites**: Skoufa & Panepistimiou (Athens), Tsimiski (Thessaloniki), Kalamata, Patra, Tripoli, 25is Avgoustou & Knossou (Heraklion). Chania (28/07/2026) is a ninth, not yet on the page. Deck: 8 done, 3 more shortly, **40% of 66 by end-2026** (≈26, so ~18 still to convert).
4. **Euronet transfer had NOT closed as at 30/07/2026** — Euronet's Q2-2026 release (8-K ex-99.1, SEC EDGAR) mentions neither CrediaBank nor Greece; PI segment 57,814 installed / 57,071 active ATMs.
5. **HSBC Malta board meets 04/08/2026** for H1 accounts (HSBC479). Nothing above HSBC479 published yet.
6. **EIB €100m Security & Defence facility, first €50m tranche, 20/07/2026** — first non-systemic bank in Europe in the programme → defence-sector EDD/sanctions screening pressure.
7. **BNP Paribas AM strategic partnership, 16/07/2026** — explicitly to enable "modern digital investment solutions" inside the digital-transformation strategy.
8. **eGov-KYC is live in production** as a customer self-service journey, plus a public **API Portal** — partly closes a pure Greek eKYC pitch, opens the AML/monitoring layer behind it.
9. **e-Banking/Mobile planned upgrade outage 07–08/02/2026** — small but concrete proof the replatforming is landing.
10. **Pantelakis Securities 70% SPA 11/05/2026**; **Thrivest ABB 15/07/2026** (16.7% placed, down to 24.0%); **H1-2026 results moved to 06/08/2026**; board change 30/07/2026.

## Printec read

- **XL / Malta:** channels, cards & ATM management software, digital onboarding for a non-eGov-KYC jurisdiction, AML/compliance, transaction monitoring, HSM/security, managed services. Enter via CrediaBank Athens (COO/CIO office), not Valletta. Deadline pressure: Q4-2026 approval, April 2027 Legal Day 1.
- **M / Greece branch concept:** ~18 further New Experience conversions in 2026, each with TCRs, card-based entry and VTS via CrediaConnect. **Incumbent OEM is unnamed in every public source** — standing identification task; visit Tsimiski 8 or Panepistimiou and read the badge.
- **M / compliance:** EIB defence lending + Pantelakis brokerage + Evropi insurance = three new regulated flows to screen and monitor, against a Bank of Greece 2026 priority of on-site inspection of transaction-monitoring systems.
- **Negative, now precisely dated:** 141 Greek ATMs (80 in-branch / 61 off-site) and merchant acquiring go to Euronet with 3-year payments/wallet exclusivity — agreed, guided Q3-2026, **not yet closed**. Establish before closing whether the 80 in-branch units sit inside the perimeter or stay with the bank as branches convert to TCR.

## Access log

- crediabank.com listings are JS-rendered; `/en/` paths broken (`/en/group/press-office/2026/` → **500**, `/en/group/investor-relations/.../corporate-presentations/` → **404**); Greek paths fine. Route: **sitemap.xml + desktop UA** → per-release page → `/media/*.pdf` → **pdfminer.six** in `/tmp/pdfvenv` (pdftotext absent).
- Malta Stock Exchange `borzamalta.com.mt/company-announcements` → **404** (both www and apex). Worked around via `cdn.borzamalta.com.mt/download/announcements/HSBC<NNN>.pdf`, probed 474–483; **480+ = 404 (not yet published)**. `hsbc.com.mt/investor-relations/` → 404.
- `euronet.com/newsroom` → **404**; `ir.euronetworldwide.com/news-releases` → **404**. Used **SEC EDGAR submissions API** (`data.sec.gov/submissions/CIK0001029199.json`) + Archives with a descriptive UA — a source environment not used in prior runs.
- Nothing dropped silently.
