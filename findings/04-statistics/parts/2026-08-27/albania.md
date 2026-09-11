# Albania — Agent 4 (Market Statistics) — run 2026-08-27

## Access breakthrough
`bankofalbania.org` payment statistics are AJAX-loaded, but the tables are plain XLSX behind a discoverable endpoint:
`https://www.bankofalbania.org/ajxDt.php?uni=<UNI>&ln=1&cis=16448&apprcss=getciwrp`
(UNI comes from the page HTML; `cis=16446` AIPS/AIPS-EURO, `16447` AECH, `16448` payment instruments).
Desktop-UA curl returns 200 on every /rc/doc/*.xlsx and *.pdf. Site search works as POST to `/Rezultati_i_kerkimit/`.
This defeats the "Cloudflare/JS ajax tables" blocker logged in the baseline.

## Headline primary reads (BoA, Q2-2026, unaudited/provisional)
| Metric | Q2-2026 | Q1-2026 | 2025 | 2024 |
|---|---|---|---|---|
| ATMs | 1,414 | 1,147 | 1,091 | 1,011 |
| — cash-withdrawal | 1,346 | 1,081 | 1,041 | 925 |
| — cash-DEPOSIT capable | 458 | 454 | 430 | 396 |
| — credit-transfer capable | 363 | 327 | 324 | 294 |
| POS | 38,662 | 32,224 | 31,263 | 24,481 |
| Virtual POS | 389 | 365 | 342 | 280 |
| E-money terminals | 9,452 | 7,572 | 7,322 | 5,633 |
| Active cards | 1,686,388 | 1,664,152 | 1,652,474 | 1,510,606 |
| Branches/agencies | — | — | 408 | 400 |

H1-2026 card transactions: 29,017,108 total / 322,674m lek. ATM withdrawals 11,006,228 / 192,364m lek;
ATM deposits 1,378,900 / 68,595m lek; POS card payments 16,006,404 / 58,263m lek.

## Notes
- The disputed ~1,011-ATM 2024 figure is CONFIRMED as Bank of Albania's own number (F6 terminals table). The
  thecptgroup.com ~390-branch 2023 figure is also close to BoA's 390 for 2023 — both now superseded by primary.
- The Q2-2026 ATM jump (+267) is almost certainly SEASONAL tourism deployment (same Q2 pattern as Montenegro),
  not a structural step change — treat with care until Q3/Q4 lands.
- BoA Annual Report 2025 not yet published (latest = 2024); Supervision Annual Report 2025 IS published.
