# North Macedonia (NBRSM) — Payment Statistics, ATM/POS/Card, e-payments
Run date: 2026-07-27 | Analyst subagent

## Summary
Primary source = National Bank of the Republic of North Macedonia (NBRSM). The bank's own
statistics pages (nbrm.mk/platiezhna_statistika-en.nspx, /platiezhni_kartichki-en.nspx) are
behind a Cloudflare JS challenge — WebFetch returns HTTP 403 and a desktop User-Agent curl
still hits "Just a moment... Enable JavaScript" (5.7KB challenge page). No connected Chrome to
escalate this run — logged. Hard figures recovered from NBRSM data reported in Macedonian press
(pari.com.mk, makfax, skopjeinfo) and the e-commerce association (ecommerce.mk / AETM), which
publishes NBRSM-sourced tables.

### Fleet & cards — end-Dec 2025 (NBRSM, via pari.com.mk 06/04/2026)
- ATMs: 1,132 (+8.74% y/y). Fleet GROWING strongly, against EU decline trend.
- POS terminals: 36,095 (+3.53% y/y).
- E-commerce (virtual) points: 2,240 (+11.11%).
- Payment cards in circulation: 2,004,681 (+2.98%); citizens 1,940,904, business 63,777 (+12.81%).
  1.09 cards/resident; 3.35 cards/household. Debit 1,722,740 (+4.31%); credit 264,999 (-4.00%).
  Visa 1,160,121; Mastercard 807,640.
- Contactless cards: 1,961,662 (+3.22%) = ~97.9% of all cards.
- Mobile-payment-enabled (tokenized/digitalized) cards: 290,202 (+120.27% y/y) — doubling+.

### Q1 2026 flow growth (NBRSM, via makfax/skopjeinfo, publ. ~01/07/2026)
- Card txns +12.2% number / +14.5% value.
- Physical-POS payments +11.7%; online card payments +18.7%.
- Digital-channel e-payments +21.9% number / +23% value.
- Mobile apps = 72.8% of all electronically-initiated txns (+25.9% y/y).
- Digitalized cards = 17.9% of all issued cards; ~4 mobile txns per digitalized card.
- Credit transfers (platni nalozi) +10.3% number / +14.6% value.

### E-commerce Q1 2026 (AETM / ecommerce.mk, NBRSM data, publ. 14/07/2026)
- Total online value EUR 265.95m (+18.1% y/y); 7,662.7k txns (+16.4%); avg EUR 34.7.
- Domestic merchants EUR 156.24m (+16.5%); foreign merchants EUR 109.71m (+20.3%).
- 59 new e-merchants registered in the quarter.
- FY2025 online spend EUR 950m (+32%) per AETM annual assembly.

### Instant / SEPA rails
- Full SEPA implementation started 07/10/2025 (9 banks live on SEPA credit transfers) — NBRM/EPC.
- TIPS-clone (Banca d'Italia-led, Western Balkans) go-live scheduled 2026; instant "fast payments"
  settling in seconds expected later in 2026 (World Bank 25/03/2026).

### Cash automation
- Stopanska Banka: 60 cash-in (deposit-only, up to 100 notes) ATMs (stb.com.mk, 07/11/2023 — dated).
- NLB Banka: 24/7 self-service zones w/ deposit ATMs + CDS cash-deposit machines for legal entities.

## Access log
- nbrm.mk EN + MK statistics/cards pages: Cloudflare JS challenge -> HTTP 403 to WebFetch AND to
  desktop-UA curl. No Chrome connected to escalate. Logged.
- telma.com.mk, mkd.mk, kurir.mk: 403 to WebFetch; figures recovered via search snippets + ecommerce.mk primary.

## Signal rows — see structured output.
