# Raiffeisen Bank Romania — findings 30/07/2026

## Headline: the fleet split is now RESOLVED

The bank's own live network-locator API (`/ro/home/retea/_jcr_content/root/container/map.maps.viewport.json`,
pulled 30/07/2026) returns 2,069 places. Breakdown:

| Class | Raiffeisen-branded | Euronet-branded | Total |
|---|---|---|---|
| Branches | 263 | — | 263 |
| `Bancomat` (cash-out ATM) | 548 | 414 | 962 |
| `Bancomat multifunctional EUR` | 603 | — | 603 |
| `Bancomat multifunctional` (RON deposit) | — | 181 | 181 |
| `Smart Cashbox` (RON/EUR/USD/GBP corporate deposit) | 60 | — | 60 |
| **Self-service total** | **1,211** | **595** | **1,806** |

This reconciles exactly with the audited FY2025 annual report ("peste 588 de masini
multifunctionale si 549 de ATM-uri", 61 Smart Cashbox) and kills the alternative
"~770 + 373" reading carried in the baseline. The MFM estate has grown 588 -> 603
and one Smart Cashbox has come off (61 -> 60) in seven months.

Sub-detail from the same feed: of the 603 `multifunctional EUR` units only **404**
advertise EUR cash *dispensing*; **130** dispense RON only, and 534 advertise RON+EUR
deposit. So true dual-currency recycling is roughly a third of the own fleet.

## Other material items

- **ROBOR cartel fine RON 442.49m** (Competition Council plenum, 07/06/2026; RON 3.73bn
  across 10 banks). Bank will appeal. Larger than Q1-2026 net profit (RON 367m).
- **Garanti BBVA Romania**: EUR 591m, signed 28/03/2026; target = EUR 4bn assets, ~2%
  share, 71 agencies (31/12/2024). CC review opened 15/06/2026; closing Q4-2026;
  integration completing **H2-2027**.
- **Cloud**: 64% of the bank's applications already in cloud at 31/12/2025 (group runs
  AWS + Azure).
- **Voice guidance under Law 232/2022** extended nationally on ATMs and MFMs (Q1-2026),
  but the public locator exposes **no** per-device accessibility attribute.
- **RoPay laggard**: only "RoPay Alias – Payment" live; peers (CEC, ING, BCR, BT, Libra,
  Vista) already run QR-at-POS, e-commerce and Business QR.
- **Branch trend**: 272 (18/06/2025) -> 266 (31/12/2025) -> 264 (31/03/2026) -> 263 (30/07/2026).
- **Acquiring**: 39,983 EPOS terminals at 31/12/2025; >42,000 at 31/03/2026;
  27,000+ merchants, RON 16bn+ volumes in 2025 (+8%).
- **Funding**: EUR 500m senior non-preferred MREL bond 20/01/2026 (4.136%, Baa2),
  9th EMTN series, ~EUR 1.6bn raised in total.

## Standing caveat

ATM and POS estate management has been outsourced end-to-end to **Euronet since 2003**;
595 Euronet devices sit inside the customer-facing network. Any Printec approach must be
either (a) via Garanti integration/harmonisation, (b) Smart Cashbox / corporate cash
automation, (c) EAA-2030 accessibility retrofit, or (d) software: eKYC, AML,
transaction monitoring.
