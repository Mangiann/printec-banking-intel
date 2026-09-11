# CEC Bank (Romania) — findings 2026-06-29

State-owned, #3 Romanian bank by assets. ~1,000+ branches, 2m+ customers. Heavy multi-year digital/self-service transformation. Printec-relevant: huge mixed ATM/MFM self-service fleet, ATM/POS fleet-monitoring app, Digital Agencies (self-service + videobanking), Temenos core migration in progress.

## What changed / NEW vs baseline (2026-06-24)
- **Creatio cloud CRM now confirmed LIVE** — Romania's first banking-sector cloud CRM, rolled out across 1,000+ branches and ~4,000 customer-facing employees; go-live event in Bucharest, announced ~07/04/2026 (staged rollout continuing). Baseline only had "Creatio live ~Apr 2026 (date unstated)" — now firmed with scope. [citybiz, EIN]
- **Digital Agencies primary detail** confirmed: 5 pilot units (Simeria/Hunedoara, Tibanesti/Iasi, Mioveni/Arges, Jurilovca/Tulcea, Floresti/Cluj), launched 05/06/2026; self-service (cash in/out, FX, payments, transfers, data updates) + remote videobanking (account opening, lending, e-signature). Pilot → analyse → extend. Videobanking/self-service VENDOR UNDISCLOSED. [ZF, NoCash]
- FY2025 figures firmed: Group net profit RON 815.1m (+18.5%), Group assets RON 107.7bn; **1,220 ATMs + 264 MFMs = 1,484 self-service**; POS network +25.8%; POS volumes +49% count / +88% value; card tx +27%. [cec.ro FY2025 via aggregators]
- **RON ~235m digital infrastructure investment in 2025** re-confirmed. [ghiseulbancar]
- Fleet-modernisation: ~1,100 ATM/MFM replaced with next-gen (large touchscreen + contactless + QR), **>80% of fleet modernised**; multi-year programme continues until full fleet renewed. Contactless withdrawal launched (550→~900 ATMs). [cec.ro / ZF / NoCash]

## Key signals (Printec mapping)
- 1,484 self-service fleet, mixed vendors, ongoing multi-year replacement → ATM/MFM hardware, recyclers, managed services, OptiCash cash optimisation. XL.
- Aurachain low-code ATM/POS/BNA **fleet-monitoring & incident app** already in place (real-time map + ticketing) — a Printec transaction-monitoring/managed-services competitor reference; complicates a pure monitoring pitch but recyclers/cash-automation still open. (3-project Aurachain partnership originally 2021: monitoring + SME onboarding + trade finance.)
- Temenos core (with Tech Mahindra + SoftCentric) selected Jan 2025; migration in progress; opens post-CBS channel-integration/self-service integration work. Go-live date still unstated.
- Digital Agencies model = videobanking + self-service kiosks → recyclers/TCRs, videobanking kiosks, eKYC onboarding; scale potential across 1,000+ branches.
- Procurement: cec.ro/achizitii live (currently Info SMS, ProfiTAP comms gear); no 2026 ATM/self-service tender surfaced this pass.

## Access issues
- cec.ro (all /presa, /achizitii, Digital Agencies release) = HTTP 403 to WebFetch; no browser connected for Claude-in-Chrome. Primary figures corroborated via ZF, NoCash, Economica, ghiseulbancar, citybiz, Aurachain, Temenos PR.
- citybiz Creatio articles = 403 to WebFetch (read via search summaries).

## Sources
- cec.ro FY2025 results; cec.ro Digital Agencies release (05/06/2026, 403); ZF 23168062; NoCash; ghiseulbancar; Temenos PR 15/01/2025; Aurachain blog; citybiz 863307 / 829652.
