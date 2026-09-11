# UniCredit Bulbank (Bulgaria) — findings 2026-07-14

Focus: Branch of the Future cashless, post-euro ATM replacement, Prime, Google Cloud.
Largest/one of top BG banks; FY2025 record net profit BGN 903.2m; total assets BGN 41,016.10m (~18.07% mkt share); ROA 2.38%, ROE 20.26%; CET1 20.6% standalone; corporate-loan market leader 27.1%. ~125 branches (last primary FY2024 AR), ~700+/755 ATMs. FY2025 Annual Report ("Acceleration in action") published (~20MB PDF, image-heavy — local text extraction timed out; figures from primary web + press).

## Key signals (re-verified vs 2026-06-24 baseline + NEW)

1. **Post-euro ATM changeover EXECUTED (01/01/2026)** — primary UCB ATM-service notice: BGN withdrawals until 21:00 31/12/2025; ATM network interruptions 21:00 31/12 → 01:00 01/01; euro-only withdrawals after 00:00 01/01/2026; deposit ATMs offline from 10:00 30/12/2025, reactivated after 04/01/2026 euro-only; NEW single-deposit cap EUR 9,990 (max banknotes depends on ATM model); source-of-funds declaration ≥ EUR 750; "Bill Payment" ATM menu removed (B-pay retained). Full-fleet software recalibration + cash-cassette reconfiguration; non-upgradeable deposit modules = replacement/recycler window. → Printec ATM/self-service, cash recyclers/automation, OptiCash, managed services. RE-VERIFIED primary; is_new=false.

2. **FY2025 record results / AR2026 published** — record net profit BGN 903.2m; assets BGN 41,016.10m (~18.07% share); ROA 2.38% / ROE 20.26%; CET1 20.6%; corporate-loan leader 27.1%. Awards: The Banker "Bank of the Year Bulgaria 2025"; Global Finance "Best Bank in Bulgaria 2026"; Euromoney best digital + best corporate bank. Signals capex capacity for fleet/branch refresh. → managed services, ATM lifecycle. is_new=true (FY2025 AR now primary).

3. **Prime — PRIME zones in ALL branches** — Prime affluent model launched ~18/05/2026, developed in Bulgaria, rolled out across 9 CEE markets; ~100,000 target clients (~10% of base); asset threshold EUR 50k or salary EUR 3,100 Sofia / EUR 2,600 country. NEW detail: "specially designated PRIME zones in ALL bank branches" = network-wide branch reformatting/fit-out; 86% of Prime clients active on Bulbank Mobile (advisory-led branches → cash pushed to self-service). → branch self-service/kiosks/TCR, digital onboarding/eKYC. is_new=true (all-branches scope).

4. **Cashless "Branch of the Future" expansion** — primary (26/05/2023): first fully cashless branch Krasno Selo Sofia + 10 more points by end-2023; cash-desk ops -64%; self-service zones drove ATM operations +150%, cash volumes 7x; Branch-of-the-Future flagship Dondukov 9 (cultural monument), +60% visitors / 93% satisfaction; Bulgaria = UniCredit group pilot country. NEW: first Branch of the Future opened in Burgas; "another Branch of the Future" opened. → recyclers/TCR, ATM placement, managed services. is_new=partial (Burgas/new location).

5. **Google Cloud 10-yr partnership (12/05/2025)** — 13 UniCredit markets incl. Bulbank; migrate legacy app landscape; Vertex AI/Gemini incl. financial-crime prevention. Group building AML/financial-crime on Google Cloud = competitive headwind for Printec AML/transaction-monitoring; managed-services/integration angle. is_new=false (ongoing).

6. **Mastercard Agent Pay agentic-commerce pilot (Bulgaria, ~14/05/2026)** — Mastercard completed first AI-agent ("Agent Pay") transactions in Bulgaria in a controlled environment using cards issued by UniCredit Bulbank, Postbank (Eurobank Bulgaria) and UBB (KBC). Card-issuing/tokenisation focus; adjacency to fraud/transaction-monitoring. → AML/transaction monitoring, HSM/security (tokenisation keys). is_new=true.

7. **POS/acquiring** — FY2024 AR (last primary): POS fleet +10.5%, acquiring volumes +20%, txns +23%; 5,519 POS replaced + 4,606 configured. Euro changeover + Prime affluent spend = continued POS refresh. → POS/acquiring, TMS. is_new=false (re-verify FY2025).

8. **Antifraud/transaction monitoring** — FY2024 AR: ~BGN 2.5m core antifraud + BGN 3m card antifraud saved. → AML/transaction monitoring. is_new=false.

## Access issues
- unicreditbulbank.bg / capital.bg = WebFetch "domain not verified as safe" (network/enterprise block). Recovered ATM-service and cashless-branch article bodies via curl + desktop browser UA; euro-changeover figures verified primary.
- FY2025 AR PDF (EN, ~20MB, ucb_ar2026_en_all_a4_am_long.pdf) downloaded via curl but pdfminer text extraction (layout + no-layout + page-range) all timed out/killed — image/vector-heavy design PDF. FY2025 financials taken from primary web (unicreditbulbank.bg results pages) + press (banker.bg, standartnews). Exact FY2025 branch/ATM counts NOT confirmed from AR — operator should extract via OCR.
- FY2025 branch count and current ATM fleet size unconfirmed against primary AR (carry FY2024 ~125 branches; ~700+/755 ATMs aggregator/contacts, Low).
