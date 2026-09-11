# BCR (Erste) Romania — run 2026-07-30 — COMPLETE

## Headline

**The single most valuable thing this run produced is a live, exact device census.** BCR's branch/ATM locator is JS-rendered, but it sits on an undocumented JSON API (`/bin/erstegroup/gemesgapi/locations/...`). Paging it in full on 30/07/2026 returned:

| | count | notes |
|---|---|---|
| ATMs (cash-out) | **1,096** | 1,023 contactless, **only 376 with voice guidance**, 320 dispense EUR |
| MFMs (deposit-capable) | **573** | all contactless, 572 voice, 572 MoneyGram, 13 dispense EUR |
| **Total devices** | **1,669** | vs BCR's own rounded "1,750" |
| Branches | **284** | matches BCR's H1 2026 PDF exactly — validates the API |
| — cashless | 212 (74.6%) | |
| — still with a teller counter (GHISEU) | **72** | the TCR conversion pipeline |
| — with 24/7 self-service zone | 236 | |
| — with business cash deposit (ADN, RON only) | **62** | 222 branches have none |
| — with video advisory | 27 | |

Derived (coordinate matching, approximate): **~782 off-site ATMs** and ~169 off-site MFMs, across 383 and 173 towns respectively vs 157 towns with a branch.

## What changed since the baseline

| | FY2025 (AR, 30/03/2026) | H1 2026 (BCR PDF, 30/07/2026) | Δ |
|---|---|---|---|
| Retail units | 290 | 284 | −6 |
| % cashless | 73% | 74% | +1pp |
| Corporate business centres | 20 | 19 | −1 |
| Corporate mobile offices | 18 | 15 | −3 |
| ATM + MFM devices | ~2,000 | 1,750 | **−250 (−12.5%)** |

Meanwhile the **national** estate grew: BNR reported 11,136 ATMs in Romania at 31/12/2025, up 1,108 vs June 2025. BCR is ceding physical cash-access share.

**Baseline corrections:** drop "~2,000 machines / ~955 ATMs / 290 branches". Drop the 2016-vintage 1,927/79/529/160 breakdown for good — it is now replaced by a live census.

## Other material signals

- **Accessibility deadline with a number attached.** 720 of 1,096 ATMs have no audio guidance. Law 232/2022 lets pre-28/06/2025 terminals stay in service only to **28/06/2030**. Raiffeisen Romania finished national voice guidance in Q1 2026 — BCR is visibly behind a peer.
- **ROBOR fine: RON 577,361,887 (~EUR 110m)**, 6.1875% of 2025 turnover, disclosed in Erste's own H1 2026 interim report note 31. Investigation report served 06/04/2026; reasoned decision not yet served; BCR will contest.
- **H1 2026:** net profit RON 1,205m (−18.2%), opex +6.0%, CIR 36.2%. Erste's Romania segment CIR deteriorated 40.0% → 42.3%.
- **Headcount:** BCR Group average FTE 5,138 → 4,966 (−3.3% y/y).
- **APTRA OptiSuite/OptiCash + Printec** incumbency re-verified on NCR Atleos' live newsroom page (23/03/2018) — but **no public re-confirmation exists for 2019–2026**. Treat as a defensive priority.
- **George Business:** legacy eBCR/24Banking decommissioned end-2025; 11,000+ clients, EUR 12bn/month, 8,800 on FX Pro.
- **IT capitalisation:** intangible additions RON 149.76m in 2025 (+12.9% y/y), ~EUR 29m.

## Standing gaps

The **ATM/MFM hardware OEM at BCR remains unidentified** in any public source — the only vendor evidence anywhere is the 2018 NCR/Printec software project. No 2026 branch-modernisation statement exists (latest are 2018 and 2020). BCR publishes no tenders (private bank, not in SEAP).

## Access notes

`consiliulconcurentei.ro` → 503. `bcr.ro` press index and locator are JS-only → routed via `sitemap.xml` and the GEM JSON API. `bcr.ro/en/sitemap.xml` → 404. English "Our company" page carries stale figures (318 units / 63% cashless) — do not use. Both large PDFs extracted locally with pdfminer.
