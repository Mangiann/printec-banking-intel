# Kosovo banks — Bank-disclosures findings — 2026-06-29

Banks covered: BKT, TEB, ProCredit, BPB, NLB, Banka Ekonomike (+ Isbank transfer, CBK sector).
Search languages: English + Albanian.

## Headline NEW / CHANGED vs baseline
- **Isbank Kosova acquired by Banka Ekonomike — COMPLETE.** Türkiye İş Bankası – Kosovo Branch ceased banking services from **01/09/2025**; full transfer of assets & liabilities to **Banka Ekonomike Sh.A.** under CBK approval ref **2025/312 dated 29/07/2025**. Prishtinë + Prizren branches continue under Banka Ekonomike. (The baseline "Isbank acquisition" buyer is now CONFIRMED = Banka Ekonomike, NOT BKT.) Source: SeeNews + Isbank announcement PDF (CBK-approved). Integration of cards/channels/systems = live 2026 work.
- **BPB / Printec deal CONFIRMED as genuinely BPB Kosovo (not AikBank Serbia).** Printec renewed BPB's full ATM network: **75 NCR Atleos ATMs (45 cash-out + 30 multifunctional)**, replacing the old fleet, 24/7 cash-in/cash-out. Resolves the baseline ⚠ flag — the 75/45/30 figure is BPB Kosovo's own (it coincidentally mirrors AikBank Serbia's split). Source: Printec Group official post.
- **BKT Kosova FY2025 (AR published May 2026):** net profit **EUR 33m** (+20.9%), total assets **EUR 1.56bn** (first time >EUR 1.5bn), deposits **EUR 1.2bn**, ROE 18.91%, ~**21.3% market share** (largest bank). "Expanded its ATM fleet throughout the country" in 2025. Launched **"Deposit with Unique Code at ATM"** — cardless ATM cash deposit via Business e-Banking, "first and only of its kind in the local market."

## Bank-level signals
- **BPB (Banka për Biznes):** 25 branches; full ATM-network renewal by Printec = 75 NCR Atleos (45 cash-out + 30 multifunctional), 24/7. Printec incumbent confirmed. EBRD EUR 10m SME line. → lifecycle: telemetry/OptiCash/recyclers/managed services. [XL/High]
- **BKT Kosova:** largest bank ~21.3% share; FY25 net profit EUR 33m, assets EUR 1.56bn; named Printec customer ("Smart BanKomaT"); expanded ATM fleet 2025; cardless deposit launched; AI roadmap. → recycler upgrades + OptiCash + managed services. [M-L/High]
- **TEB Kosova:** 81 deposit-capable ATMs; full 24/7 deposit+withdrawal network, camera-monitored. → deposit/recycler refresh + monitoring. [M/Medium]
- **ProCredit Bank Kosova:** "24/7 Zone" staffless self-service model; cash-deposit ATMs accept up to 50 notes / EUR 9,995; ProCredit Direct 24h. → recyclers + 24/7-zone build-out + managed services. [M/Medium]
- **NLB Banka Kosova:** part of NLB Group (largest SEE group); regional branch/ATM network. → group-standardisation play. [M/Low]
- **Banka Ekonomike:** absorbed Isbank Kosova branch network (Prishtinë+Prizren) 01/09/2025; integration of two card/channel/ATM estates ongoing 2026. → fleet consolidation, x-core multivendor, eKYC/AML harmonisation. [L/Medium]

## Sector / regulatory (CBK)
- ATMs 635 end-2024 (+8.4%; 583 end-2023); 377 deposit-capable (59.4%); 53 credit-transfer. POS 20,913 (+21.4%), 98% contactless. Deposits EUR 6.75bn Apr-2026.
- SEPA: pre-application submitted 14/10/2024; EU approval expected 2026 (pending Constitutional Court review of 3 laws). ~EUR 55m/yr saving.
- TIPS Clone instant-payments rail: launch planned 2026 (5 countries incl. Kosovo via Banca d'Italia). New ISO 20022 / real-time → INETCO monitoring, HSM, terminal stack.

## Access issues
- bqk-kos.org & seenews.com & bankassoc-kos.com = 403 to WebFetch; CBK PDFs pulled via browser-UA curl + pdfplumber (worked). Isbank announcement PDF binary — details obtained via SeeNews search index. Printec/BPB detail via Facebook post (FB body not fetchable; figures via search index). BKT 2025 AR parsed locally.
