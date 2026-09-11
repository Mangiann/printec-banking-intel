# UniCredit Bank Romania — run 30/07/2026

**Status: complete. 18 signals, 16 new/materially changed.**

## Headline

The Alpha Bank Romania merger is done and the bank is now in the *shrink-and-refit* phase. The
network has gone from ~300 branches at merger completion (18/08/2025) to **253 at 31/12/2025**
(bank's own disclosure) with a stated target of **~200 by end-2026** — and the bank is explicitly
recycling the savings into **branch refits**: from 2 units with "Prime corners" today to **40 within
a year**. Headcount is down 12.2% year-on-year to 4,261. That combination — fewer branches, fewer
staff, a growing loan book and a funded refit programme — is the single best Printec opening at this
bank in years, on the cash-automation / in-branch self-service / managed-services lines.

Two constraints to respect: (1) **Euronet** is the entrenched free-of-charge off-site ATM extension,
confirmed in the tariff schedule in force from 03/07/2026, so a pure off-site ATM pitch competes
with an existing partner network; (2) the group is buying **KYC, transaction monitoring and AML
automation centrally** on Google Cloud/Vertex with IBM and Accenture as infrastructure partners —
do not pitch a competing central engine.

## What is new since the last run

| # | Signal | Date | Why it matters |
|---|---|---|---|
| 1 | 253 branches / 4,475 staff at 31/12/2025 (bank's own "at a glance") | 31/12/2025 | ~47 branches closed in 4.5 months post-merger |
| 2 | "~200 branches" target by end-2026 (statement to ZF) | 25/05/2026 | ~50 more closures inside 2026 |
| 3 | Prime corners 2 → 40 units in a year, funded by post-merger consolidation; Dorobanti branch opened with 2 Prime offices; Prime clients 25k → 50-60k | 14/07/2026 | A dated, funded refit programme — the moment in-branch cash gets re-specified |
| 4 | Prime launched across 9 CEE markets with "Prime zones in selected branches" | 13/05/2026 | Group-mandated branch format, replicable pitch across BG/RS/HR/BiH |
| 5 | ROBOR fine: RON 431.03m on UniCredit, RON 3.73bn across 10 banks; bank will litigate | 07/06/2026 | Pushes procurement to opex/as-a-service; funds compliance tooling |
| 6 | Group flagged ~EUR 140m extraordinary hit (Banca Progetto + ROBOR Romania) | 28/07/2026 | Exposure ring-fenced; RO investment budget looks protected |
| 7 | H1-2026: net profit EUR 158m, costs -11%, C/I 35.7, FTE 4,261 (-12.2%) | 24/07/2026 | Cost-out is real and continuing |
| 8 | Group tech agenda: IBM + Accenture IT infra operating model; Google Cloud migration; AI on KYC / Corporate Lending / Transaction Monitoring; Qivalis € stablecoin; Digital Euro pilot | 28/07/2026 | Competitive read-across — sell the edge, not the central platform |
| 9 | RoPay live in Mobile + Business Mobile, implemented with **Montran**; QR + phone alias | 09/02/2026 | QR acceptance at a bank with a big Micro book → POS/softPOS demand |
| 10 | Tariff CD102 rev.32 (in force 03/07/2026): free RON withdrawals at bank ATMs **and Euronet**; cash-in by card at BNA multifunctional units is a standard included operation | 03/07/2026 | Euronet is the off-site incumbent; the bank's own estate carries the deposit volume |
| 11 | ShopSmart extended to Micro segment in Business Mobile (500k+ retail users) | 13/07/2026 | Merchant-side data play → acquiring conversation |
| 12 | In-app / website chat launched, positioned as call-centre deflection | 06/07/2026 | Same deflection logic that justifies assisted self-service in branch |
| 13 | RON 600m bond issue | 02/03/2026 | Funding in place for a multi-year programme |
| 14 | TotalSoft harmonised ERP/HR (Charisma) over ~6 months for 4,800 staff, ~300 branches, 900 ATMs | 11/11/2025 | Back office done; the ATM layer is the one with no named vendor |
| 15 | CEO: "consolidation period", grow above market, keep investing in technology and retail CX; #3 in lending | 03/06/2026 | Names the budget line |
| 16 | Market: Romania 11,136 ATMs at 31/12/2025 (+1,108 in 6 months), 729,408 POS (+161,396), 28.63m active cards | 17/05/2026 | Machines substituting for counters nationally; UniCredit ≈ 8% of the ATM base |

Re-verified, not new: the 10-year Google Cloud MoU (12/05/2025, 13 markets, Vertex AI/Gemini,
financial-crime prevention named) and the 100%-online account opening flow with video selfie + OCR + AI.

## Standing gaps

- **ATM OEM and field-service provider for the ~900-unit fleet: still unidentified.** No public
  source names them. The bank's locator runs in a third-party iframe with no queryable API, so the
  fleet could not even be recounted independently.
- No post-merger ATM count later than the 900 quoted on 18/08/2025; no cash-out vs deposit-capable
  (BNA) split.
- No published Romanian IT/technology capex figure (unlike Banca Transilvania and CEC Bank).
- UniCredit Bank S.A.'s standalone H1-2026 IFRS interim report was not located — H1 figures rest on
  press reporting of the group disclosure.

## Access notes

- `unicredit.ro` 403s the fetch tool. Defeated with a desktop Chrome UA via curl. The full press
  archive is reachable at `POST https://www.unicredit.ro/show.pws.pressrelease.html` with
  `Referer` + `X-Requested-With: XMLHttpRequest` and params
  `_charset_, number, keywords, datefrom, dateto, lang=ro, appName=cee2020-pws-ro`.
- `consiliulconcurentei.ro` returned **503** — the primary ROBOR decision could not be opened.
- `bnr.ro/Indicatori-plati-5291.aspx` returned **302** to both the fetch tool and desktop-UA curl.
- `economedia.ro` 403s the fetch tool (solved with curl); `wall-street.ro` 403s curl (solved with the
  fetch tool).
- PDFs (tariff schedule, 2Q26 group deck and PR) were downloaded and parsed locally with pdfminer.
