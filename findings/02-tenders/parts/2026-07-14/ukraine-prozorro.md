# Ukraine — Prozorro (prozorro.gov.ua + tender.privatbank.ua)

Run 2026-07-14. Focus: PrivatBank 800-ATM 2026 lot, Oschadbank, ATM/SST/IT lots + winners.

## Access situation this run
- prozorro.gov.ua UI + /api = JS shell / "Method Not Allowed" / "Not Found" to WebFetch and curl. public-api.prozorro.gov.ua has no text/buyer filter (firehose only).
- BREAKTHROUGH: aggregator tender.uub.com.ua (403s to WebFetch) serves FULL server-rendered HTML to curl with a desktop User-Agent — company lists (company-14360570 PrivatBank, company-00032129 Oschadbank), CPV category pages (dk021-30123200-9 ATMs) AND per-tender detail pages (/tender/UA-.../ showing winner EDRPOU, bid, expected value, status, contract dates). This yielded verified WINNERS for Agent 6.
- tender.privatbank.ua = SPA / 302 redirect, no server-rendered tender text.

## Key confirmed facts (this run)
- PrivatBank 800-ATM 2026 plan STILL PRE-TENDER as of 14/07/2026. Live Prozorro feed (uub company-14360570 = 195 notices; ATM CPV 30123200-9) shows ONLY spare-parts / consumables / modules notices — NO bulk multifunction/recycler ATM lot. #1 watch unchanged. Printec incumbent (16/01/2025, 838.64M UAH, 1,140 NCR SelfServ recyclers). Re-corroborated by NV.ua (23/01/2025) and open4business/finclub (22/05/2026 board comment, Musienko).
- WINNERS captured (all "Завершена закупівля"): Oschadbank cash-bags UA-2026-05-12-011684-a -> PP "СТРІЛА" 2,324,460 UAH (was in-eval last run, now AWARDED); PrivatBank ATM cash-cassette modules UA-2026-06-15-012172-a -> Servus Systems Integration (31089403) 7,211,025 UAH; PrivatBank ATM card-reader consumables UA-2026-07-01-004760-a -> Servus Systems Integration 3,923,400.50 UAH; PrivatBank ATM Recycler VS-module parts UA-2026-05-19-000673-a -> Diebold Nixdorf Ukraine (36353398) 2,119,470 UAH (MIXED FLEET signal); PrivatBank AML/fin-monitoring/risk maturity assessment UA-2026-07-03-004713-a -> McKinsey Ukraine 295,900 EUR.
- Oschadbank: NO ATM/SST hardware tenders this window; only IT/insurance (DELL servers 1.74M USD UA-2026-06-23-010335-a; Check Point support 8.57M USD UA-2026-06-09-011245-a; medical insurance 153.9M UAH).
- PrivatBank armored CIT vehicles UA-2026-07-08-005714-a -> TOV "REFORM" 543.49M UAH (cash-logistics, not Printec).

## Signal rows — see structured output
