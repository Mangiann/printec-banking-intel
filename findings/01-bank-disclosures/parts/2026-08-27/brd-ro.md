# BRD - Groupe Societe Generale (Romania) — run 27/08/2026

**Status:** complete · 16 signals · window: H1/Q2-2026 August reporting cluster

## Headline

BRD's H1-2026 disclosures (30/07/2026) confirm the shape the previous run saw — 334 branches, RON 118m/112m investment — but three genuinely new things emerged this run:

1. **BRD itself now publishes the self-service gap.** 268 of 334 locations have a 24H cash self-service zone. 66 sites do not.
2. **The dead "~1,400 ATMs" figure is replaced with live data.** Driving BRD's own locator endpoint on 27/08/2026 gives **1,174 ATM records vs 303 deposit-capable MBA records** — only **20.5%** of self-service points take cash in — and **322 of 335 agencies still run a manned cash desk** (only 11 "cashless").
3. **A2A QR payment went live at the physical POS.** BRD launched **RoPay Instant merchant payments on 06/08/2026**, and **Law 239/15.12.2025** made app-based account-to-account payment a legally recognised "modern payment mean" alongside cards.

## The cash-automation arithmetic

| Measure | Value | Date |
|---|---|---|
| Branches | 334 (347 Dec-25, 357 Jun-25) | 30/06/2026 |
| Locations with 24H cash self-service | 268 → **66-site gap** | 30/06/2026 |
| ATM records (cash-out only) | 1,174 | 27/08/2026 |
| MBA records (deposit RON/EUR/USD) | 303 | 27/08/2026 |
| Cash agencies / cashless agencies | 322 / **11** | 27/08/2026 |
| Bank active employees | 4,641 (4,965 Dec-25) | 30/06/2026 |
| Cash in tills, vaults and ATMs | RON 2,647.7m (−8.3% vs Dec-25) | 30/06/2026 |

Staff is being cut ~3x faster than branches (−6.5% vs −3.7% in six months) while 96% of branches still run a manned cash desk. That gap is the recycler case.

## The budget constraint (new)

H1-2026 intangible additions **RON 82.9m** vs IT/office equipment brought into service **RON 9.1m**. Forward capital commitments: intangibles **RON 21.4m** vs tangibles **RON 7.7m**. BRD is funding software, not machines — so lead with **managed service / hardware-as-a-service**, not a capex purchase. Watch construction-in-progress (RON 29.0m added in H1) as the leading indicator of a funded hardware programme.

## Payments / POS

- **06/08/2026** — RoPay Instant to merchants live in YOU BRD: QR at POS, static in-store QR, e-commerce QR + deep link, zero commission, RON only, TRANSFOND rail.
- **178.2m acquiring transactions** in H1-2026 — flagged NEW in BRD's own deck.
- **Law 239/15.12.2025** — A2A app payments count as "modern payment means" → merchants may satisfy acceptance obligations with a QR instead of a card POS. Threat to card-POS volumes, opening for QR/softPOS.
- **04/08/2026** — phishing campaign against BRD clients, credential harvest + transaction authorisation. New instant irrevocable rail + APP fraud = transaction-monitoring spend.

## Safetech — the honest answer

Safetech Innovations' current report 34/2026 (22/07/2026) discloses a **EUR 2.728m, 36-month** cybersecurity contract, but the beneficiary is **explicitly confidential** ("entitate din Romania neafiliata Companiei"). **No BRD link exists in public filings.** Reported as market context only, Low confidence.

## Access notes

- bvb.ro PDFs time out on curl → routed via WebFetch + local pdfminer.
- `Agentii_inchise_3.pdf` (closed-branch list) returns an HTML 404 — unavailable.
- BRD has no working press-release index; August items were recovered from `sitemap.xml` lastmod dates.
- BNR payment statistics sit behind a JS interactive database — **not obtained** (operator request filed).
- Locator data recovered by reading the Drupal footer bundle for `loadLocationsUrl` and calling `POST /en/load/locations` directly. No Chrome escalation required.

## Caveat on the locator numbers

These are **locator records / geo-sites**, not certified machine counts. A site may host more than one machine. Re-pull monthly: a rising MBA count, or the "cashless" count moving off 11, is the earliest observable trigger that a programme has started.
