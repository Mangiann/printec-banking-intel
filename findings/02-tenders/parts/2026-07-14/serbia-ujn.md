# Serbia — UJN portal (jnportal.ujn.gov.rs) — bank & public ATM/self-service/POS tenders + winners

Run date: 2026-07-14 (6th pass). Slug: serbia-ujn.

## Method / access
- UJN portal search is ASP.NET/JS postback — not crawlable by WebFetch; site: search returns only nav pages.
- Individual `tender-eo/<id>` pages ARE WebFetch-readable but require known IDs; the two IDs surfaced by search (79455, 293944) were unrelated (fuel / electricity, old years) — dead ends.
- UJN public API `/api/tender/public/search?query=bankomat` returns HTTP 401 Unauthorized (logged).
- Claude-in-Chrome NOT available this run (no browser tool surfaced via ToolSearch) — could not drive portal search interactively.
- posted.co.rs (Banka Poštanska štedionica own portal) reads fine — `/o-nama/nabavke.html` gives current notice list.
- posta.rs javne-nabavke page lists only PLAN documents (no line-item detail without opening each PDF).
- danas.rs = 403 (logged). javne-nabavke.com aggregator = 0 rows without login.

## Key structural finding (unchanged, re-verified)
Serbia's commercial banks (Raiffeisen, Banca Intesa, UniCredit, OTP, AIK, etc.) are PRIVATE → they do NOT tender ATM/POS on UJN; sourcing is private RFP. Only public/state buyers touching self-service near UJN:
- **Banka Poštanska štedionica (BPŠ)** — state-owned, publishes on OWN portal posted.co.rs (NOT UJN). 190 branches, 600+ ATMs.
- **Pošta Srbije** — public buyer on UJN; ~50 Post ATMs; joint ATM renewal programme with BPŠ (agreement Sept 2023).

## Status of carried-forward / re-statused items
- **BPŠ CIT cash-transport & escort** ("Nabavka usluge vršenja poslova pratnje i obezbeđenja transporta i prenosa novca") — deadline 30/04/2026, STILL IN PROGRESS / evaluation ~10 weeks past deadline, NO award published. (Last run titled it CIT escort + ATM servicing.) posted.co.rs/o-nama/nabavke.html. Maps to Printec managed services / CIT / ATM cash servicing.
- **BPŠ thermal rolls (termalne rolne)** — deadline 22/10/2025, still "in progress", no award. Consumables for ATM/POS receipts. Minor.

## NEW this run (BPŠ open notices)
- **BPŠ "Access control & technical security enhancement"** (unapređenje sistema kontrole pristupa i tehničke zaštite) — deadline 14/07/2026, OPEN. Maps to Printec physical/branch security + managed services. is_new.
- **BPŠ "Storage solution for main banking system"** — deadline 22/07/2026, OPEN. Core-banking storage/IT infra — outside Printec core offer (noted, low relevance).
- **New BPŠ ATM installed** at MZ Bošnjace (22/05/2026) — evidence ATM network still actively expanding → pre-tender demand signal (ATM hardware + field services).
- **SEPA payments live 05/05/2026** for BPŠ clients (euro credit transfers) — payment-rails modernization; peripheral to Printec.

## Winners / awards
- NONE disclosed. BPŠ does not publish winners publicly; UJN award search not accessible this run. No new award captured.

## Operator asks
- Drive UJN expert-search (naručilac "JP Pošta Srbije" + CPV 30123430 ATM / 30200000) for open notices + award IDs — needs interactive browser.
- Email nabavka@posted.co.rs for BPŠ CIT/ATM-servicing (30/04/2026) award outcome.
