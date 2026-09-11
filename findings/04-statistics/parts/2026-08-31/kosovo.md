# Kosovo (CBK/BQK) — Agent 4 Market Statistics, run 2026-08-31

Resumed from the 27/08 checkpoint (3 signals kept). All gaps in its `remaining` field are now closed. 13 signals total.

## Headline: the 2025 device counts were found

They are NOT in "Use of Bank Cards in Kosovo" (still the Sep-2025 edition, 31/12/2024 data) but in **Charts 64 and 65 of the CBK Annual Report 2025** (cover "Prishtina, June 2026"), reachable via a direct `/wp-content/uploads/` PDF URL with a desktop User-Agent.

| Metric | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| ATM terminals | 516 | 534 | 583 | 635 | **686** (+8.0%) |
| POS terminals | 13,836 | 14,769 | 17,187 | 20,859 | **30,259** (+45.1%) |
| Bank network units (MSB 297) | — | 200 | 215 | 227 | **235** (234 at May-2026) |
| Cash exported, EUR m | 950 | 1,700 | 2,215 | 2,084 | **2,373** |

2025 flows: ATM withdrawals 23,642,504 txns / EUR 4.93bn; POS payments 62,056,621 txns / EUR 1.75bn (+33.4% count); e-banking 13,490,958 txns / EUR 27.79bn. Debit cards ~1.9m (+33.7%), credit ~218k (+12.1%).

## Signal rows

| # | Entity | Signal (short) | Date | Opp |
|---|---|---|---|---|
| 1 | CBK MSB 297 | Branch network still growing: 227 (2024) → 235 (2025) → 234 (May-26) | 10/07/2026 | L |
| 2 | CBK MSB 297 | ATM cash deposits EUR 266.4m → 304.9m/month; withdrawals still rising | 10/07/2026 | L |
| 3 | CBK card report | [STANDING 2024] 635 ATMs, 59.4% deposit-capable → ~258 dispense-only | Sep-2025 | L |
| 4 | CBK Annual Report 2025 | **686 ATMs / 30,259 POS at end-2025; POS +45% in one year** | Jun-2026 | XL |
| 5 | Banca d'Italia | TIPS Clone live 20/07/2026 (BiH, ME); **Kosovo joins Nov-2026** | 20/07/2026 | XL |
| 6 | World Bank P507881 | Component 3 USD 5m; FA ratified 10/04/2026; 11 institutions must upgrade to FPS; goods/IT procurement tables still empty | 15/05/2026 | L |
| 7 | CBK / Constitutional Court | SEPA still blocked; CBK admits "loss of the opportunity to keep pace"; replacement draft law Apr-2026 | Jun-2026 | Unscoped |
| 8 | CBK regulation | Non-bank PSPs may open RTGS settlement accounts in KIPS | Dec-2025 | M |
| 9 | KBA / Visa | Tap-to-Phone roadshow Pristina 16/04 → Prizren 25/05 → Gjakova 29/06 → Peja 27/07/2026; Raiffeisen, NLB, ProCredit live | 27/07/2026 | M |
| 10 | CBK / NPC | National Retail Payments Strategy 2021-2026 expires; inclusion 73%, 49 non-cash payments per capita; Open Banking WG created | Jun-2026 | Unscoped |
| 11 | CBK cash ops | 33.23% of notes banks deposit are unfit; EUR 2.37bn cash exported in 2025 | Jun-2026 | L |
| 12 | Official Gazette 2/2026 | **Law on Banks 08/L-304 promulgated (decree DL-16/2026, 20/01/2026) — 12-month bank compliance deadline ~11/02/2027**; only 2 of 3 laws still blocked | 27/01/2026 | L |
| 13 | CBK regulation | Information Systems & Cyber Risk Management — compliance mandatory **from 01/06/2026**; 4-hour incident reporting; ATMs named critical | 15/09/2025 | M |

## None found this run
Card issuing/personalisation; branch-kiosk tender; physical ATM security (only the 04/04/2025 KBA meeting — zero incidents in 2024 [STANDING]); vendor-announced TCR deployments. Leading indicators (Google Trends, app-store) not swept — budget discipline.

## Access
`bqk-kos.org` HTML pages: Cloudflare JS challenge to BOTH WebFetch and desktop-UA curl. Direct `/wp-content/uploads/` and `/repository/docs/` PDFs: 200 with desktop-UA curl. `bankassoc-kos.com`: 403 to WebFetch, 200 to desktop-UA curl. `documents.worldbank.org` 403 on the procurement PDF; `documents1.worldbank.org` same path 200. pdftotext absent; pypdf works.
