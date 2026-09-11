# Romania — SEAP/SICAP (e-licitatie) — Tenders findings (2026-06-24, 5th pass)

## Structural finding (the core takeaway, unchanged & re-confirmed)
Romania's big commercial banks — **BCR, BRD, Banca Transilvania** — are **privately owned** and do **NOT** procure ATM/self-service/POS/security equipment through SICAP/e-licitatie. Searches for these banks on SICAP return only branch/ATM-locator pages and foreclosure-auction portals (vanzari.bcr.ro, vanzari.brd.ro, vanzari.bancatransilvania.ro) — these are debt-recovery asset sales, not procurement. **This zero result is the finding, not a failure.** Pursue these banks directly (private RFPs), not via SICAP.

Only **state-linked entities** surface on SICAP for banking-tech relevant scope:
- **CEC Bank** (state-owned) — but procures on its OWN portal/anunturi, and cec.ro returns **403 to all tools** (4th+ consecutive run blocked). Info SMS IT-messaging re-tender was active into spring 2026.
- **BNR** (central bank) — cash/banknote-processing equipment maintenance (last live tender Oct 2024, closed).
- **Posta Romana** (state postal co) — Tezaur government-securities card-payment/banking services (awarded to CEC Bank, sole bidder, 2025).

## Status of carried-forward items
- **CEC Bank Info SMS IT-messaging re-tender** — CHANGED/deepened. Clarifications PDF dated **03/03/2026**; deadline EXTENDED from 13/03/2026 to **23/04/2026 17:00**. No public award (cec.ro 403). Adjacent (messaging, not core ATM/POS). Status: deadline passed, award pending/unknown.
- **Posta Romana Tezaur card-processing** — re-confirmed AWARDED to CEC Bank (sole bidder), ~19.98M lei banking services, deadline 21/08/2025. CLOSED.
- **CEC Bank MFM fleet programme** — ~1,100 new-gen ATMs/MFMs, ~80% of network modernised, ~EUR 2.6M investment (programme dates to May 2023, now ~complete per baseline "over 1,400"). Residual maintenance/managed-services opportunity. Supplier never publicly named.

## Access issues this run
- cec.ro entire domain = 403 (all pages + hosted PDFs). 4th+ run.
- e-licitatie.ro = JS-only SPA; WebFetch returns bare "SEAP". Notice IDs known but pages not text-extractable via WebFetch.
- sicap.ai aggregator = 429 (rate-limited).
- **No Chrome browser connected** → Claude-in-Chrome escalation UNAVAILABLE this run. e-licitatie live portal + cec.ro remain unreadable.

## NEW this run
- CEC Info SMS deadline extension to 23/04/2026 + 03/03/2026 clarifications (CHANGED vs baseline which had deadline 23/04 already passed — confirms it ran through spring).
- Re-confirmed BCR/BRD/BT private → no SICAP ATM tenders (structural, not new but explicitly re-verified for the named focus banks).
