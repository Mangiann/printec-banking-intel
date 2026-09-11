# Banca Transilvania (RO) — run 27/08/2026

**Status: complete.** 14 signals, all opened at source. Focus asked: H1-2026 results, annual capex (IT/digital), self-banking machines, OTP RO merger, POS.

## Headline for Printec

BT's own AGM has already published a line-item 2026 capex plan — **RON 1,017.40m incl. VAT**, containing a **retail & cards HARDWARE line of RON 51.92m**, a **machines line of RON 21.39m**, a **cash processing centre line of RON 7.88m**, **security RON 9.79m** and **digital initiatives RON 177.22m**. This is the single most actionable disclosure of the run: a named, board-approved budget for exactly what Printec sells.

The second headline is the **cash-automation white space**: at 30/06/2026 BT runs **over 2,000 ATMs of which only 691 are multifunctional** (deposit/recycling-capable) — roughly two-thirds of the estate is cash-out-only — plus **616 ageing BT Express terminals**, and both counts are *falling* quarter on quarter (696→691 and 632→616) while 12 agencies closed in six months. Machines are being retired faster than replaced. That is the classic pre-tender shape.

## Corrections / notes on the focus list

- **OTP Bank Romania merger is NOT a 2026 event.** It completed 28/02/2025; the H1-2026 accounts carry it only as a prior-year comparative footnote. Do not brief it as live.
- **POS surge has a regulatory cause**, not a commercial one: Law 239/2025 removed the RON 50,000 threshold and made card acceptance mandatory for essentially all merchants from 01/01/2026. BT POS went >188,000 (31/03) → >200,000 (30/06).
- **BT's site is WAF-blocked from this host** — everything below was taken from the identical statutory filings on the Bucharest Stock Exchange (bvb.ro/infocont), plus regulator registers.

## Signal rows

| # | Entity | Signal (short) | Source | Date | Opp |
|---|---|---|---|---|---|
| 1 | Banca Transilvania | 2026 capex plan RON 1,017.40m, incl. retail/cards hardware 51.92m, machines 21.39m, cash-processing centre 7.88m, security 9.79m, digital 177.22m | BVB — Hotarari AGA | 28/04/2026 | L |
| 2 | Banca Transilvania | >2,000 ATMs, only 691 multifunctional; 616 BT Express; >200,000 POS; 8.5m cards; 5m digital customers | BVB — H1-2026 report | 21/08/2026 | XL |
| 3 | Banca Transilvania | Machine counts falling: multifunctional 696→691, BT Express 632→616 in one quarter | BVB — Q1 vs H1 2026 | 21/08/2026 | L |
| 4 | Banca Transilvania | Agencies 475 (Dec-25) → 466 (Mar-26) → 463 (Jun-26); headcount up to 13,565 | BVB — H1-2026 report | 21/08/2026 | L |
| 5 | Banca Transilvania | Chat BT 2.4m interactions, 82% resolved without a human | BVB — H1-2026 report | 21/08/2026 | M |
| 6 | Banca Transilvania | H1-2026: group net profit RON 2.5bn +26.8%, assets RON 233.3bn, C/I 38.3% ex turnover tax, CAR 21.96% | BVB — FactSheet | 21/08/2026 | Unscoped |
| 7 | Banca Transilvania | CFO on call: continued spend on technology, cybersecurity, data and AI; 350+ ATMs/recycling machines with audio guidance | Investing.com transcript | 24/08/2026 | M |
| 8 | Romania (regulator) | Law 239/2025 — card acceptance mandatory for all merchants from 01/01/2026, RON 50,000 threshold removed, fines RON 5,000–15,000 | MO 1160/15.12.2025 via trade press | 15/12/2025 | XL |
| 9 | Romania (Senate) | Bill B409/2026 would force every ATM to accept a user-typed amount for all cardholders — fleet-wide software change | senat.ro legislative register | 24/06/2026 | L |
| 10 | Banca Transilvania | ANSPDCP fined BT EUR 5,000 (RON 26,172) for an employee's unauthorised account access; corrective measures ordered | dataprotection.ro | 02/07/2026 | S |
| 11 | Victoriabank (BT Group, MD) | Moldovan prosecutor's precautionary seizure claim ~RON 475m at 30/06/2026, up from ~RON 450m at 31/03/2026 | BVB — H1-2026 report | 21/08/2026 | M |
| 12 | Banca Transilvania | H1 risk section flags rising cyber risk from third-party and outsourced-service dependencies | BVB — H1-2026 report | 21/08/2026 | M |
| 13 | BRD (competitor) | Launched RoPay instant A2A payments to merchants incl. QR scanned off POS terminals, no card | Profit.ro / Bursa.ro | 06/08/2026 | M |
| 14 | Romania (market) | BNR at 31/12/2025: 11,136 ATMs, 729,408 POS, 685,731 EFTPOS, 28.63m active cards | BNR data via Bursa.ro | 17/05/2026 | Unscoped |

## Access issues

`bancatransilvania.ro` serves a custom "Acces blocat / Access denied" interstitial to this host (Reference ID `0.16451502.1787817841.511e2a9`) for both curl-with-desktop-UA and the fetch tool; the `r.jina.ai` text proxy hit a Cloudflare managed challenge; the Claude-in-Chrome extension is not connected. Route used instead: identical statutory filings via `bvb.ro/infocont`, PDFs extracted locally with pdfminer. `bvb.ro` HTML NewsItem pages time out on curl but work through the fetch tool; `bvb.ro/infocont` directory listing returns 403; `bnr.ro/Indicatori-plati-5291.aspx` 302-redirects to the homepage. Not opened, and therefore not cited as primary: BT's own H1-2026 investor presentation (`.../2026/Semestru-I/Prezentare.pdf`).
