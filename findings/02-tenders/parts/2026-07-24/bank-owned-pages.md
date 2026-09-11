# Bank-owned procurement pages — findings (run 2026-07-24)

Scope: banks/central banks running their own RFP portals + adjacent bank-own plans/awards revealing winners. Fresh entry points this run: **NBS Serbia 2026 procurement plan (primary PDF, opened & text-extracted)**, Erste Bank Serbia nabavke, Raiffeisen Bank Ukraine procurement, CBBH Bosnia, plus TEB Kosovo refresh and PrivatBank carry-forward.

## NEW primary — National Bank of Serbia (NBS) 2026 procurement plan, v6 (adopted ~25/06/2026)
Source: https://www.nbs.rs/export/sites/NBS_site/documents/propisi/propisi-tend/2026/plan_nabavki_2026_v6.pdf (extracted locally with pdfminer). Column values are misaligned in extraction — do NOT quote per-line figures without operator confirmation. Relevant lines confirmed present:
- **Nabavka stonih mašina za brojanje i sortiranje novčanica** (desktop banknote counting/sorting machines) — Otvoreni postupak (open procedure), Q1. → Printec cash automation / counters.
- **Mašina za brojanje i pakovanje kovanica sa jednim tunelom** + Reducir mašina (coin counting/packaging machine, single tunnel) — open procedure, Q1. → Printec cash automation.
- **Mašina za brojanje novčanica** (CPV 30132200) listed among devices. → cash automation.
- **„HSM" uređaji** (HSM devices) line under services, alongside RTGS/IPS/Kliring/MMK maintenance. → Printec HSM/security.
- **Rešenje za kontinuirano nadgledanje, ranu detekciju i efikasan odgovor na napredne pretnje usmerene na digitalna dobra** (continuous monitoring / early detection / response to advanced threats on digital assets — EDR/threat) + **Zanavljanje sistema za bezbednost i video nadzor** (security & video-surveillance renewal). → Printec transaction monitoring / security / managed services.
- **Competitor/incumbent intel:** plan includes "Adaptacija softvera na sistemu za obradu novčanica 'Glory'" and "Demontaža, montaža i preseljenje sistema za obradu novčanica 'BPS M7'" (Giesecke+Devrient Banknote Processing System M7). → NBS large banknote-processing is **G+D + Glory** locked; only desktop counters/coin machines are contestable.

## TEB Kosovo (teb-kos.com/en/tenders) — refreshed, NEW refs
Continuing: Cash-Handling Machines 292-25, ATM Kiosk production/assembly 375-25, Remote/Digital Onboarding + Digital Signature (repeatedly extended), Physical Security+CIT+ATM Replenishment 636-24, Security Monitoring-room supervision 281-26, Electronic Security Systems 590-24 (re-tender). NEW this run: **E-Archive project 311-26**, **Firepower Threat Defense + FMC renewal 298-26**, Website Development 318-25, Data Warehouse 047-24. TEB never publishes winners. → self-service, eKYC/onboarding, security, managed services.

## Carried-forward / status
- **PrivatBank UA 800 ATMs 2026**: still PRE-TENDER (open4business plan; ~7,401 ATMs as of Q1-2026, replacing dispense-only with recyclers). tender.privatbank.ua & uub mirror = SPA/blocked; zakupivli.pro award page (UA-2025-07-08-007672-a "Комплектуючі для АТМ/ТСО") = Cloudflare JS challenge. Prozorro openprocurement bulk API reachable but search-filter-by-buyer not resolvable. Printec incumbent. Not materially changed.
- **Erste Bank Serbia** (erstebank.rs/sr/o-nama/nabavke): "Trenutno nemamo aktivnih nabavki" — no active tenders. Logged.
- **Raiffeisen Bank Ukraine** (raiffeisen.ua/en/about/procurement): no active ATM/cash/security tenders; only historical. Logged.

## Competitor
- **Diebold Nixdorf** won 3× 2026 Global Banking & Finance Awards incl. "Best ATM Services Europe 2026" (05/03/2026). Brand-visibility signal, Low.

## Access blocked (logged)
- cbbh.ba/procurement: HTTP 500 (WebFetch) and 302 redirect loop (desktop-UA curl) — CBBH Bosnia procurement listing not retrieved; escalate to operator.
- zakupivli.pro tender page: Cloudflare "Just a moment" JS challenge (desktop UA).
- tender.privatbank.ua / uub.com.ua / prozorro.gov.ua search: SPA / API filter-by-buyer not resolvable via public search endpoint.
- nbs.rs/sr/tenderi live tenders route through jnportal.ujn.gov.rs (Serbia UJN portal) — covered by serbia-ujn part.
