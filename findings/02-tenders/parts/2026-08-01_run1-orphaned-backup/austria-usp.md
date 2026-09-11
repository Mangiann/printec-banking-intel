# Austria — ausschreibungen.usp.gv.at (OeNB & public buyers) — 01/08/2026

## Headline

1. **GELDSERVICE AUSTRIA is running a EUR 9,100,000 procurement for combined deposit/withdrawal devices (cash + coin recyclers)** — TED 305531-2026, CPV 30123200, participation deadline was 08/06/2026, invitations to tender dispatched ~25/06/2026, contract start 02/11/2026. Award criteria are weighted on banknote recycling (100 pts), coin recycling (74), coin depositors/hoppers (32). Delivery locations include Austria, Slovenia and Bavaria. **This is the single biggest Printec-shaped opportunity in Austria and the participation stage has already closed.**
2. **The OeNB rural-ATM framework is running out of money.** TED 511414-2025 confirms the true ceiling is **EUR 5,544,425.60** (the EUR 55.4m figure was an admitted typo — "Tippfehler"). Twelve call-off notices between 16/06/2025 and 22/06/2026 total **EUR 4,045,406.80** (≈73% drawn). OeNB has 66 ATMs live (06/07/2026) and targets **up to 120 by end-2026** — the remaining headroom will not cover that. A re-tender or framework expansion is highly likely inside 12 months.
3. **Austria's whole cash cycle is a Giesecke+Devrient / GZT-Geldzähltechnik duopoly.** G+D holds OeNB, GSA and OeBS note processing; GZT holds GSA coin equipment and Österreichische Post's automatic cash safes. Both mostly via direct award / single-bid procedures.

## Access route (important, reusable)

The USP list page is DataTables/JS and returns no rows to a plain fetch. The **server-side JSON endpoint works without auth**:

```
GET https://ausschreibungen.usp.gv.at/at.gv.bmdw.eproc-p/public/api/tenderlist
    ?draw=1&start=0&length=100&orderColumn=2&orderDir=desc&q=<searchterm>
```
Returns `{recordsFiltered, recordsTotal, data:[[title, org, published, deadline, objectId, isNotice, …]]}`.
Detail pages are plain HTML: `/at.gv.bmdw.eproc-p/public/tender-detail?object=<objectId>`.
Portal holds 169,236 records; last refresh stamp 31/07/2026 22:35.

## Signals

| # | Entity | Signal | Value | Date | New |
|---|---|---|---|---|---|
| 1 | GELDSERVICE AUSTRIA | Combined deposit/withdrawal devices (recyclers) for cash & voucher logistics, TED 305531-2026 | EUR 9,100,000 (5 yr) | 05/05/2026 | yes |
| 2 | OeNB | Rural-ATM framework ceiling EUR 5,544,425.60, 73% drawn, 66/120 ATMs live | — | 05/08/2025 / 06/07/2026 | yes |
| 3 | OeNB | 12 ATM call-offs to PSA, all single-bid | EUR 4,045,406.80 | 16/06/2025–22/06/2026 | yes |
| 4 | GSA | G+D BPS M segment upgrade, 6 machines, no prior publication | EUR 615,135.40 | 11/12/2025 | yes |
| 5 | GSA | Multi-vendor cash + voucher software platform + 4 yr maintenance → Data Engineering GmbH (direct award) | EUR 109,200.00 | 10/12/2025 | yes |
| 6 | GSA | EFESO study: operating process/cost review + site concept | EUR 137,000.00 | 20/04/2026 | yes |
| 7 | GSA | Coin-roll packers → GZT-Geldzähltechnik | EUR 661,057.35 | 17/11/2025 | yes |
| 8 | GSA | Full-service maintenance of 17 SCAN COIN ICP-9 coin counters (6 sites) → GZT | EUR 510,650.08 | 01/04/2025 | yes |
| 9 | OeNB | Banknote-processing machine modernisation → G+D, no prior publication | EUR 237,900.00 | 03/11/2025 | yes |
| 10 | OeBS | Banknote-processing spare parts → G+D | EUR 54,294.91 | 28/05/2025 | yes |
| 11 | Österreichische Post AG | Automatic cash safes (AKT) framework of 04/08/2015 → GZT, still generating call-offs in 2026 | EUR 270,923.05 + 128,486.26 + 60,487.68 | 2025–2026 | yes |
| 12 | OeNB | Verification of Payee (IBAN name-check) → BAWAG P.S.K., 48 months | EUR 130,700.00 | 15/01/2026 | yes |
| 13 | OeNB | Gold value transports London→continent → Brink's Global Services Deutschland | EUR 433,235.00 | 25/11/2025 | yes |
| 14 | Münze Österreich | OPEN: automated weighing line for coin blanks, 2nd attempt | not stated | deadline 01/09/2026 | yes |

## Action

- Chase GSA on TED 305531-2026 immediately — if Printec is not among the ≥3 invited candidates, the fallback is subcontract/service positioning before the 02/11/2026 start.
- Register on ANKÖ (gv.vergabeportal.at) so future GSA/OeNB notices arrive at bid-preparation lead time, not after.
- Prepare an ATM + managed-services offer against the OeNB framework's exhaustion (expected re-tender H1-2027 at the latest).
- Profile GZT-Geldzähltechnik GmbH (FN 98239w) as the Austrian incumbent channel; Österreichische Post's 2015 cash-safe framework is 11 years old and overdue for renewal.
