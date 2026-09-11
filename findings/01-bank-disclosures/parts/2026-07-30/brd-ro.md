# BRD – Groupe Société Générale (Romania) — run 2026-07-30

**Status: complete.** Fresh full run (no prior checkpoint for this runDate).

BRD published its H1-2026 results on the morning of **30/07/2026**, so this run is built almost
entirely on same-day primary disclosure, downloaded and text-extracted locally.

## Headline picture

| Metric | Value | As of | Source |
|---|---|---|---|
| Branches | **334** (347 at Dec-25, 357 at Jun-25, 388 at Dec-24) | 30/06/2026 | BRD H1-2026 BoD report |
| Branches with 24H self-service **cash** zone | **268** (266 at 31/03/2026) | 30/06/2026 | BRD H1-2026 presentation |
| ATMs | "approximately 1,400" (undated site statement) | live 30/07/2026 | brd.ro |
| Investments (capex) | **RON 118m** Group / RON 112m Bank (vs ~RON 100m H1-25) | H1-2026 | BRD H1-2026 BoD report |
| Group active headcount | **5,124** (5,840 at Dec-24, −12.3%) | 31/12/2025 | BRD AR2025 (audited) |
| Staff expenses | **−8.3% YoY** (−10.5% in Q2) | H1-2026 | BRD H1-2026 presentation |
| Acquiring transactions | **178.2m** (first-ever disclosure) | H1-2026 | BRD H1-2026 presentation |
| YOU BRD users | 1.96m (+11%), 22m txns, RON 35.2bn | 30/06/2026 | BRD H1-2026 |
| Net profit | RON 784m (+2.5%), C/I 49.6% | H1-2026 | BRD H1-2026 |

## The Printec story in one line

BRD is explicitly substituting **technology for people and property** — 41 branches closed in 2025,
13 more in H1-2026, headcount down 12.3%, staff costs down 8.3%, "reduced real estate footprint
costs" — while 80% of the remaining network already has a 24/7 cash zone. The opportunity has
shifted from **building** self-service zones (nearly saturated, +2/quarter) to **upgrading** them:
recyclers replacing withdrawal-only ATMs, plus managed services. Capex is tight (RON ~236m
annualised vs BT's RON 1,017m), so lead with a **no-capex device-as-a-service** structure.

## What's new / changed vs the previous file

- Self-service cash zones **266 → 268**; branches confirmed at **334** at 30/06/2026 (was 31/03).
- **RON 118m H1-2026 capex** disclosed (+18% YoY) — a hard number the baseline never had.
- **Headcount −716 (−12.3%)** in 2025 — the single strongest automation driver at BRD.
- **eID (chip CEI) live in remote onboarding** from Q2-2026 — eKYC reference point for Romania.
- **178.2m acquiring transactions** — first time BRD has published acquiring scale.
- **CIT One S.A.** — BRD/BCR/Raiffeisen 33.33% each cash-transport-and-processing JV, confirmed in
  the audited accounts. Cash-cycle decisions are effectively made three-banks-at-once.
- **Safetech current report 34/2026 (22/07/2026)**: EUR 2,728,000, 36 months, cybersecurity +
  own monitoring platform, beneficiary **confidential**. Timing fits the flagged ~Sep-2026 BRD SOC
  renewal — but the client is NOT named and must not be briefed as BRD.
- **The Safetech BRD SOC case study is now a 404.** The ~Sep-2026 renewal date has no live source.
- **ASF fined BRD RON 67,100** (June-2026) over client-asset safeguarding and internal
  trading/back-office flows — *not* AML, despite some press framing.
- **Competition Council ROBOR decision 07/06/2026**; BRD filed a current report 08/06/2026 saying it
  will contest it by all legal means.
- **BNR FSR June-2026**: 15 major operational + 1 major security incident reported by 9 PSPs in
  H2-2025 under DORA, with ATM/POS card unavailability (withdrawal *and deposit*) named as an
  impact. Strong framing for an availability-SLA managed-services pitch.

## Still open (honest gaps)

1. **No ATM/MBA fleet count in any BRD filing.** ~1,400 is an undated website figure; the split
   between cash-out ATMs and deposit-capable MBAs is unpublished.
2. **Fleet OEM still unidentified** — targeted vendor searches (Diebold Nixdorf, NCR Atleos, GRG,
   Wincor) returned nothing tying any of them to BRD. Standing task.
3. POS terminal / merchant counts unpublished.
4. H1-2026 headcount not disclosed (only audited FY2025).
5. No BRD 2025 sustainability report on its reporting page (latest listed: 2023).

**Deliberately not carried:** the "SG hires JP Morgan to sell BRD" story — it dates to 01/02/2024,
was denied by SG, and no 2026 development surfaced.

## Access issues

- `consiliulconcurentei.ro` — HTTP 503 + JS browser-check even with a desktop UA and `ro` locale.
- `safetechinnovations.com/soc-services-for-one-of-europes-largest-banks` — HTTP 404.
- BRD BoD PDF and BRD current report defeated the fetch tool's PDF parser → downloaded with a
  desktop UA and extracted locally with pdfminer.
- `asfromania.ro` June-2026 sanctions article not locatable by URL pattern → cited to an aggregator,
  marked Low.
- `bnr.ro` "Indicatori plăți" returns navigation chrome only → no system-level RO ATM/POS counts.
