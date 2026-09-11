# Diebold Nixdorf — Agent 6 vendor findings — 2026-07-15

Competitor tier: **global** OEM (ATM/self-service, Vynamic software, DN AllConnect / SMART Managed Services, Branch Automation Solutions). Direct threat to Printec's NCR ATM/recycler lines, x-core multivendor software, ATM telemetry/monitoring, and managed/field services.

## Headline (NEW this run)
- **VERIFIED — Diebold Nixdorf Ukraine (EDRPOU 36353398 = "ДІБОЛД НІКСДОРФ") won PrivatBank recycler spare-parts tender UA-2026-05-19-000673-a = 2,119,470 UAH (VAT incl), status COMPLETE.** Confirmed live via prozorro.gov.ua search API (procuring entity = АТ КБ "ПРИВАТБАНК", EDR 14360570; title = "Запчастини для АТМ Recycler (VS-Модуль): направляюча корзини права/ліва; модуль Escrow RM3"; internal tender.privatbank.ua ref PB-2025-12-11-3066705) and EDRPOU→name via clarity-project.info/edr/36353398. Proves DN has an **installed VS-Module (Wincor/DN) recycler base inside PrivatBank** — a Printec/NCR reference account with a MIXED fleet — and is capturing the spare-parts/maintenance annuity on those units. Threat to Printec NCR-recycler + managed/field-services + parts revenue within a flagship reference customer.
- **DN Q2 2026 investor call = 29/07/2026 (before NYSE open)** — announced 08/07/2026. Forward catalyst; watch EMEA/SEE banking + SMART Managed Services commentary and any footprint recycler/BAS win. (Financials are SCRIPTED via EDGAR — do not re-key.)

## Footprint context (STANDING — verify/deepen, not new news)
- **Piraeus Bank (GREECE) DN Series migration** [STANDING — 2024]: 928 additional DN Series ATMs bought since 2021 (~400 in 2024), replacing >1,200 in-branch self-service devices with DN cash recyclers by end-2024; powered by DN AllConnect Data Engine + NFC across fleet. Major Greek footprint loss for Printec/NCR. (PR Newswire 302279915)
- **Payten (Asseco SEE) = DN's local banking partner in footprint** [STANDING — 2021]: delivers DN ATMs/recyclers to Zagrebačka Bank (HR), Raiffeisenbank Croatia recycler project, and holds a Romania banking partnership. DN reaches SEE/CEE banks via the Payten channel — combined Payten+DN offer competes with Printec NCR + x-core + services.

## Product / positioning (context)
- **DN Series 300 & 350** launched 02/12/2025 (DM7V dispense module, shared cassette infra, DN AllConnect, ~40% greater availability; recyclers >40% of DN Series shipments in select EMEA). Competes with NCR dispense/recycling. [STANDING]
- **FOREX (Nordic, out of footprint) went live 02/04/2026** with DN Branch Automation Solutions + **SMART Managed Services** (end-to-end mgmt of ~90 ATMs across SE/NO/FI/DK, Vynamic Connection Points/Security/Acquiring). Reusable EMEA proof point for DN's managed-services push vs Printec managed/field services + x-core.
- **DN 2026 Global Banking & Finance Awards** (05/03/2026): Best ATM Services Europe, Best Banking Tech Solutions Provider Europe (6th consecutive), Payment Tech Innovation Europe; Helena Müller = SVP Banking Europe. EMEA BAS/managed-services marketing.
- Sales-engine reshape [STANDING]: Joe Myers CRO (eff. 01/01/2026), Raj Singh CIO (18/05/2026). No 2026 M&A found (Tracxn: 0 acquisitions 2026 YTD).

## Access notes
- prozorro.gov.ua tender HTML = JS SPA (empty to fetch) and OpenProcurement CDB rejected the human-readable tenderID — resolved via prozorro.gov.ua POST /api/search/tenders (returns entity/title/value/status) + clarity-project EDR lookup for supplier name.
- payten.com pages returned TLS cert errors to WebFetch; dated via WebSearch snippets + futurebanking.ro.
- No local pdftotext binary; DN Q1/Q4 PDFs not re-parsed (financials scripted).
