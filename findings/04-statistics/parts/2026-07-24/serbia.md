# Serbia (NBS) — Statistics run 2026-07-24

Primary sources this run: NBS "Overview of data on the provision of payment services and e-money issuance Q1 2026" (PDF, June 2026); NBS Q3-2025 payment-card press release (id=21110); NBS monetary table SBMS01 "Main monetary aggregates" (update 22/07/2026); NBS annual-2024 card press (id=20429, publ. 13/03/2025). Latest available payment-services quarter remains Q1-2026 (unchanged from 15/07 run); the genuinely fresh item is the June-2026 cash-in-circulation print.

## Confirmed exact device table (NBS Q1-2026 overview, Table I.1.2)
| Metric | Q1-2025 | Q1-2026 | y/y |
|---|---|---|---|
| POS terminals | 170,434 | 187,957 | +10.3% (+17,523) |
| Virtual POS | — | — | +20.2% |
| ATMs | 3,219 | ~3,335 (calc from 3,219 x 1.036; narrative +3.6%) | +3.6% |
| Cards issued | — | 13,343,642 | +8.0% |
| Card txns at SRB merchants | 164,460,435 | 195,192,834 | +18.7% |

(Q1-2025 table base, exact: POS 170,434; virtual POS 4,947; ATMs 3,219; +4.2% y/y then.)

## ATM fleet essentially FLAT while POS surges
- End-2024 annual: ATMs 3,218 (+4.5% vs 2023). Q3-2025: ATMs 3,197 (-0.4% y/y). Q1-2026: ~3,335 (+3.6%). Net: ATM count bouncing ~3,200-3,335, near-saturated; POS grew +10-21% same period. Branch count contracting (1,288 Q1-2026 vs 1,341 in 2023).

## Cash-in-circulation (SBMS01, RSD m, update 22/07/2026) — FRESH
Year-end series: 2020 266,725 | 2021 295,311 | 2022 310,873 | 2023 369,368 | 2024 399,414/430,183(Dec) | 2025 430,183
2026 monthly: Jan 408,649 | Feb 410,500 | Mar 398,650 | Apr 406,337 | May 412,593 | **Jun 404,025** (latest)
Cash in circulation stays high (RSD ~404bn) despite digital surge — cash-cycle automation still relevant.

## Withdrawal-value data (press, Low)
- 2025 full-year foreign-card ATM withdrawals in Serbia: RSD 80.5bn across 3.3m txns; foreign-card POS spend RSD 211.26bn across 59m txns (mondo/eupravozato citing NBS annual). Domestic ATM withdrawal-value series is image-only in NBS tables — not text-extractable this run; logged.

## Printec mapping
- ATM fleet flat + branch contraction (1,288) → branch-to-self-service migration, recyclers/intelligent-deposit, multivendor x-core (Raiffeisen Serbia ref), telemetry/managed services.
- POS +10.3% to 187,957 → Verifone/Castles terminals + TMS.
- Cards 13.34m (+8%), online purchases +39.7%, eKYC 139k (+49%), video-ID 34k → Namirial digital onboarding.
- IPS instant +30.8% (RSD 392.8bn, +33.3%) → INETCO transaction monitoring, HSM.
- Cash RSD ~404bn with fewer branches → OptiCash/TCR recyclers, cash-cycle automation.

## Access log
- All NBS PDFs/XLSX fetched via curl with desktop UA (HTTP 200); pdfminer.six used for text; SBMS01.xlsx parsed with openpyxl. Q1-2026 & Q1-2025 device tables are rasterised images — ATM/virtual-POS exact Q1-2026 values not machine-readable, computed from narrative %.
