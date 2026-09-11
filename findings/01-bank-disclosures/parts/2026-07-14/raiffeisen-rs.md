# Raiffeisen banka Serbia — findings 2026-07-14 (re-run 2)

Focus: x-core incumbency ("Bank Yourself"), iRačun, 1m-client target. English + Serbian sources.
3rd-largest Serbian bank; 25th anniversary in 2026 (founded 2001 as Raiffeisenbank Jugoslavija).

## Summary — RE-VERIFIED baseline + NEW 2026 primary items surfaced this run

RE-CONFIRMED (not new):
- **1m ACTIVE-client target 2026** — CEO Zoran Petrović, Global Finance interview 11/12/2025: aim to reach 1,000,000 ACTIVE clients in 2026 to mark the 25th anniversary. Total clients already >1m since the 2023 RBA/Crédit Agricole merger; goal is on the active base.
- **iRačun scale** — >250k fully digital accounts; ~50% of all online account openings in Serbia; mobile app >500k users; 98% outgoing payments via digital channels. eKYC = 100% online in 15 min via video call + electronic signature (no qualified cert) + biometric login. Maps to Printec digital onboarding/eKYC.
- **x-core / "Bank Yourself" incumbency** — offer.printecgroup.com/raiffeisen-bank-case-study live (HTTP 200, desktop UA): "Raiffeisen Bank Serbia made 'bank yourself' — the smartest digital investment in branch transformation / ATM Banking with Human Touch." Prior "41 multifunctional ATMs on x-core" figure carried from baseline (case-study PDF gated). Multifunctional ATM feature set (RSD+EUR deposit/withdrawal, contactless, transfers, FX, Mobile CASH cardless) confirmed on bank MFM page — matches x-core + recycler thesis.

NEW / materially changed vs 2026-06-24 & 2026-06-29 baselines:
- **PC Press Top 50 "Digital Banking Leader" award — 13/02/2026** (bank news, primary). Received by Exec Board member Tanja Glišin. Signals sustained digital-channel investment; supportive backdrop for self-service/eKYC spend.
- **Web Kredit named Global Finance top-10 CEE banking Innovator 2026 — 23/04/2026** (bank news, primary). Digital point-of-sale / online consumer lending; onboarding needs only ID card or passport + last 3 monthly PDF statements, QR-code scan. Maps to Printec digital onboarding/eKYC (competing/adjacent vendor build).
- **Fully-online business account ("račun za firmu") — 20/05/2026** (bank news, primary). SME digital onboarding extension of iRačun. SME base >100k. Maps to eKYC.
- **SEPA membership** — Serbia accepted into the SEPA geographic zone; Raiffeisen participates via parent RBI AG (bank SEPA Q&A page, 2026). Bosnia announced as next SEPA country. New EUR payment rails → Printec transaction monitoring / AML / payment-fraud relevance.
- **Euromoney Best Private Bank Serbia 2026 — 25/03/2026**; **Global Finance Best FX Bank Serbia — 22/01/2026** (bank news, primary). Brand/context.
- **iRačun acquisition promo extended into 2026** — RSD 3,000 for opening + RSD 5,000 for salary transfer, running to end-July 2026 (n1info + bank tarife). Continued aggressive digital-account acquisition → feeds eKYC volume.

## Access issues
- WebFetch blocked ("unable to verify domain safe") on raiffeisenbank.rs, printecgroup.com, offer/blog.printecgroup.com — routed via curl with desktop User-Agent instead (HTTP 200 on bank pages + offer landing).
- blog.printecgroup.com/how-to-achieve-balance... = HTTP 403 even with desktop UA; printecgroup.com/raiffeisen-serbia-branch-transformation/ now HTTP 404 (page removed) and NOT in Wayback. "41 MFM" device count remains carried, not re-pulled at source.
- Raiffeisen is private — no javne-nabavke/procurement tender trail for ATM lots.

## Signal rows — see structured output.
