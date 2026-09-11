# UniCredit Bulbank (Bulgaria) — run 2026-07-30

## Headline

The two open questions from the last run are now **closed against primary sources**:

- **Branches: 161** "branches and remote locations" at 31/12/2025 (audited separate financial statements). The live locator returns **162** records on 30/07/2026, of which **31 carry a "Cashless service" flag** — the first hard count of the Branch-of-the-Future cashless model.
- **ATMs: 762** live units on 30/07/2026, pulled from the bank's own public locations API. Only **196 (25.7%) accept deposits**; 512 are 24/7; 673 contactless; c.448 are off-site at retail hosts (Kaufland 106+, Fantastiko 44+).

The single strongest new lead: UniCredit Bulbank's own FY2025 report names **"ICT & ICT Security Risks — ATM obsolescence"** as a 2026 risk driver it will monitor, while simultaneously **extending the accounting useful life of ATMs from 5 to 7 years** on the strength of "improved maintenance practices". Group-level, UniCredit is **replacing more than half of its ATMs with latest-generation models by 2027**.

## What is new vs the 2026-07-14 baseline

| Item | Status |
|---|---|
| 762 ATMs / 196 deposit-capable / 512 24/7 | NEW — replaces "~700+/755 (Low)" |
| 161 branches at 31/12/2025 (audited) | NEW — replaces "~125 (FY2024)" |
| 31 cashless branches | NEW — quantifies Branch of the Future |
| ATM obsolescence named as 2026 ICT risk | NEW |
| ATM useful life 5 → 7 years (IAS 8) | NEW |
| Group ATM renewal: >50% replaced by 2027 | NEW |
| Cash in hand/ATM BGN 390m (+44%), cash in transit BGN 423m (+100%) | NEW |
| SAS FM anti-fraud extension, Safer Payments, new Digital Onboarding solution | NEW — names the incumbent fraud stack |
| PRIME launched 18/05/2026 across 9 CEE countries, EUR 50k / EUR 3,100-2,600 thresholds | DEEPENED |
| Free lev exchange extended to 30/09/2026; SEPA Instant from 20/08/2026 | NEW |
| Google Cloud = all 13 Group banks, Vertex AI/Gemini, financial-crime prevention | RE-VERIFIED against the annual report (the "10-year" term is **not** stated there) |
| FTEs 3,038 bank / 3,455 consolidated (from 3,134 / 3,582) | NEW |
| POS fleet +6%, merchants +13.6%, acquiring volumes +13.5% | NEW |
| BNB: 5,031 ATMs / 210,861 POS in Bulgaria at 31/12/2025 | NEW market context |
| BORICA + OpenWay Way4 awards, 23/07/2026 | NEW vendor mapping |
| UniCredit–Alpha Bank partnership, Bulgaria focus, 09/07/2026 | NEW |

## Still unresolved

**The ATM OEM / maintenance incumbent at UniCredit Bulbank is still not identified.** Four search angles (English + Bulgarian, vendor press, procurement wording, bank site) returned nothing. This remains the standing task.

## Access notes

`unicreditbulbank.bg` 403s default fetch agents; a desktop Chrome User-Agent via `curl` defeats it cleanly. The 20 MB FY2025 annual-report PDF had to be text-extracted in a background pdfminer job. `unicreditgroup.eu` 403s WebFetch but serves PDFs to curl with a browser UA.
