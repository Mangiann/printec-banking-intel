# Serbia — UJN portal (jnportal.ujn.gov.rs) — bank & public ATM/self-service/POS tenders + winners

Run date: 2026-06-24 (5th pass). Slug: serbia-ujn.

## Method / access
- UJN portal search is ASP.NET postback (JS), not crawlable by WebFetch; site: search returns only nav pages. Individual `tender-eo/<id>` pages ARE WebFetch-readable but need IDs.
- Claude-in-Chrome unavailable this run (no connected browser — list_connected_browsers returned []). Could not drive the portal search interactively.
- javne-nabavke.com aggregator = login/paywalled (0 rows returned without account).
- posted.co.rs (Banka Poštanska štedionica own portal) reads fine via www.
- danas.rs = 403.

## Key structural finding (the "zero" IS the finding)
Serbia's commercial banks (Raiffeisen, Banca Intesa, UniCredit, OTP, etc.) are PRIVATE and do NOT tender on UJN — their ATM/POS sourcing is private RFP. The only public/state buyers touching ATM/self-service on/near UJN are:
- **Banka Poštanska štedionica (BPŠ)** — state-owned, but publishes on its OWN portal posted.co.rs, not UJN. 600+ ATM fleet.
- **Pošta Srbije (Post of Serbia)** — public buyer ON UJN; ~90+ Post ATMs; jointly expanding/renewing ATM network with BPŠ.

## Status of carried-forward items (BPŠ, posted.co.rs)
All three past deadline, still NO published award/winner (in evaluation). BPŠ does not publish winners publicly.
- "Usluge pratnje i obezbeđenja transporta novca + opsluge bankomata" (CIT escort + ATM servicing) — deadline 30/04/2026, deadline-extension notice attached, now ~8wk past, no award. STILL IN EVALUATION.
- "Cisco svičevi i ruteri" — deadline 10/06/2026, in evaluation.
- "Cisco Secure Network Analytics (Stealthwatch)" — deadline 10/06/2026, in evaluation.
- "Termni rolni" (thermal rolls) — deadline 01/06/2026, in evaluation.
No NEW BPŠ notices published in June 2026 (latest = 28/05/2026).

## NEW / competitor intel this run
- Pošta Srbije + BPŠ ATM-network renewal/expansion programme reaffirmed (orig. agreement 2023, Đorđević/Čortan/Sekulović; "obnova Poštinih bankomata" over ~1 year). Pre-tender — watch Pošta Srbije UJN notices. Maps to NCR ATMs + x-core + managed/field services.
- Banca Intesa Serbia (private; not UJN) — replacing 200 ATMs with Diebold Nixdorf Cineo, some cash-RECYCLERS; Payten = integrator/maintainer (owns-fleet model 15+ yrs). First-class competitor intel for Agent 6: Payten/Asseco + Diebold Nixdorf entrenched in RS self-service.
- Chip Card + Payten — unattended POS terminals rollout in Serbia (Q4 2024 onward); Payten paketomat w/ integrated unattended POS (D Express). Payten/Asseco dominate RS POS/self-service.

## Operator asks
- POST UJN expert-search for naručilac "JP Pošta Srbije" + CPV ATM/self-service (30123430 / 30200000) to retrieve open notices + award IDs.
- Email nabavka@posted.co.rs for BPŠ CIT/ATM-servicing award outcome.
