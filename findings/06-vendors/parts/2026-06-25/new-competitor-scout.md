# New-Competitor Discovery Scout — 2026-06-25

Cross-footprint discovery run. READ references/competitors.json (156 tracked names) first, then mined this week's tender winners (ted_notices.json fresh awards; prozorro_notices.json awarded UA), app stores / soft-POS press, and "who beat Printec" angles.

## Method / coverage
- TED ted_notices.json: 186 notices; 69 fresh awards (is_award & not modification & not framework_drawdown) with a named winner. Filtered to banking-relevant CPV (ATM 30123x, POS 30142x, cash 30144x, banknote/sensors 35125100) + ATM/banknote/POS keywords; cross-checked each winner against the 156-name roster. Most 35125100 hits were lab/scientific/security false positives (Greek education-equipment lots, Czech RAID arrays, Romanian RT-PCR, etc.) — discarded.
- Prozorro: PrivatBank/Oschadbank. Two June-2026 awarded PB commercial tenders (Android POS PB-2026-01-30 / UA-2026-06-11-013572-a; ATM modules "Cash-кассета" PB-2026-01-29 / UA-2026-06-15-012172-a). Cache has NO supplier field; OCDS public-api 404s on these (commercial-bank "звіт про укладення договору" reports). Supplier resolvable only via tender.privatbank.ua (JS, needs Chrome/operator). NOT asserting an unseen winner. -> operator request.
- competitor_news.json covers 9 already-tracked names only — no new entities.
- Soft-POS app/press sweep: payabl. Tap to Pay (CY), Pale Blue "Paid" (CY) — BOTH already tracked. Phos (BG SoftPOS powering BORICA) = acquired by Ingenico Mar-2023 -> sub-brand of tracked Ingenico, NOT a new roster name.

## GENUINELY NEW NAME (is_new=true)
**Giesecke+Devrient Currency Technology GmbH (G+D)** — global, banknote/cash OEM.
- TED award 436046-2026 (published 25/06/2026; contract concluded 22/06/2026). Buyer = БЪЛГАРСКА НАРОДНА БАНКА (Bulgarian National Bank). Subject: "Доставка и инсталиране на модули и М-сензори за обработка на евробанкноти за банкнотообработващи машини BPS C5/C7" (supply + install of modules and M-sensors for euro-banknote processing on BPS C5/C7 machines). Awarded value EUR 181,000.
- Not in competitors.json. Tier: global. Printec line touched: cash automation / banknote-processing ecosystem (Glory/Sesami TCRs, NCR cash processing, NCR APTRA OptiCash). G+D's BPS are high-end central-bank/CIT banknote sorters — adjacent to, not identical with, Printec's branch TCR offer; relevant as the incumbent at the BNB euro-changeover cash chain.
- Confidence: Medium (primary TED award). Drivers: BG euro adoption (01/01/2026) is refreshing the whole BG cash-processing fleet.

## Notes / non-new
- Phos (BG SoftPOS) = Ingenico (tracked) since Mar-2023. Flag only.
- PrivatBank June POS/ATM-module winners UNRESOLVED — operator to open tender.privatbank.ua in Chrome.
