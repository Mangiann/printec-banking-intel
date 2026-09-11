# North Macedonia (NBRM/NBRSM) — Payment Statistics, ATM/POS/Card, e-payments
Run date: 2026-06-24 | Analyst subagent

## Summary
Primary source = National Bank of the Republic of North Macedonia (NBRSM). The bank's own
statistics pages (nbrm.mk/platiezhna_statistika.nspx, /platiezhni_kartichki.nspx) 403-blocked
WebFetch this run, and no Chrome browser was connected for escalation — logged as access gap.
Figures below are sourced from NBRSM data reported in Macedonian press + the e-commerce
association's NBRSM-based analysis.

### Hardware fleet (end-Dec 2024, NBRSM, via MAKTEL)
- ATMs: 1,041 nationwide (up ~20 from ~1,021 end-2023 — fleet GROWING, against EU trend).
  Skopje 475 (Centar municipality 243); Bitola 46; Kumanovo 33; Shtip 29; Strumica 25;
  Shuto Orizari 0. -> Confirms the baseline gap (press release omitted unit counts).
- POS terminals: 34,864 nationwide (end-Dec 2024).

### Flow data 2025 (NBRSM annual, baseline-confirmed + extended)
- 249m non-cash transactions (+7.1% y/y); value MKD 9,719bn (+36.4%).
- Card transactions +8.4%, = 69.1% of all non-cash payments.
- >71% (71.7%) of electronic credit transfers initiated via mobile devices.
- Cash withdrawn at ATMs: EUR 3.6bn — 53% MORE than EUR 2.3bn spent at POS. Cash still dominant.
- Online (Macedonian cards home+abroad + foreign cards): 9M-2025 value MKD 42,626.6m / EUR 693.1m
  (+30% vs EUR 533m 9M-2024); 21m txns (+30.2%); avg EUR 33; 175 new e-merchants.

### Q1 2026 (NBRSM, via Kurir/Alfa) — newest
- Continued growth of non-cash payments and digital channels; complaints down; FX reserves up.
  (Detailed Q1-2026 unit figures not extracted — article 403; reported qualitatively.)

### NEW this run (2026-06-24)
- SEPA: N.Macedonia entered SEPA geographical scope 06/03/2025 (EPC); Operational Readiness Date
  05/10/2025; FULL implementation started 07/10/2025 (with Albania/Montenegro/Moldova).
  Instant ("fast") payments expected to launch LATER IN 2026 (World Bank, EPC). -> instant-rails buildout.
- Cards end-2025: ~2 million payment cards; 98.7% contactless-enabled; 97.4% of POS terminals
  contactless-ready (NBRNM Annual Info on Payments 2025). >1 card/resident, >3 per household.
- Q3-2025 (NBRNM): card txns +9.9% number / +12.4% value; physical-POS payments +9.9%; online +9.3%;
  digital-channel e-payments +19.0% volume / +29.3% value; 71.8% of e-initiated txns via mobile apps;
  credit transfers +7.0% number / +15.3% value.
- FX reserves EUR 5,249m end-Mar 2026 (Q1-2026 NBRNM Council).
- NBRNM stats pages still 403 to WebFetch; figures via Mac press citing NBRNM annual/quarterly tables.

## Signal rows — see structured output.

## Access log
- nbrm.mk (both MK + EN statistics/cards pages): HTTP 403 to WebFetch. No connected Chrome to escalate.
- maktel.mk, telma.com.mk, kurir.mk, republika.mk: 403 to WebFetch; data recovered via search snippets.
- ecommerce.mk/en analysis: fetched OK (full table).
