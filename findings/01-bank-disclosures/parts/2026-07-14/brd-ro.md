# BRD – Groupe Société Générale (Romania) — findings 2026-07-14 (refresh)

Analyst: Printec banking market-research. Slug: brd-ro. Confidence capped at Medium.

## Summary
BRD is deep into a multi-year "pragmatic" branch-contraction + self-service-substitution cycle —
a textbook Printec cash-automation/recycler/managed-services setup. Latest primary data (Q1 2026
report, published 29/04/2026):
- **Branches: 334 at 31/03/2026 (-24 YoY)**, continuing the slide from 347 (31/12/2025, -41 YoY),
  388 (2024) and 423 (2023). ~21% contraction over 3 years.
- **24/7 self-service cash zones: 266 locations at 31/03/2026** — DOWN from 272 at end-2025 (the
  count had ramped 194→225→272 over 2023-25, so the -6 QoQ dip is a change worth watching; likely
  follows branch closures where the self-service pocket also closed).
- **Terminal fleet (carried from FY2025 disclosure, not re-verified primary this run): ~1,600+
  terminals** = ATM + MBA multifunctional deposit machines + KIOSK/ROBO automatic cash machines;
  ~1,400 ATMs. MBA = multifunctional/deposit-class hardware already in estate → recycler-upgrade pull.
- **Digital YouBRD: 1.92m users (+12% YoY), ~10.7m Q1 app transactions (+24% YoY), value RON17.4bn (+35%)**.
- **Cybersecurity SOC outsourced to Safetech Innovations** (Printec competitor on managed-security):
  Darktrace / Cynet / Ironscales / Axonius; original term Mar-2020→Sep-2023 with 3-yr auto-renewal →
  renewal window ~Sep-2026 now imminent.
- Digital front-end already served by FintechOS (onboarding/loan origination, delivered <8 months)
  and Backbase (omni-channel) — competitive context that compresses Printec's eKYC/onboarding room.

## Signals
1. Branch contraction — 334 @31/03/2026, -24 YoY (from 347 end-2025). Self-service/recycler backfill. L / Medium. NEW.
2. 24/7 self-service cash zones — 266 @31/03/2026, DOWN from 272 end-2025 (-6 QoQ). TCR/recycler + OptiCash + managed services. L / Medium. CHANGED.
3. Terminal fleet ~1,600 (ATM + MBA multifunctional deposit + ROBO), ~1,400 ATMs — recycler upgrade / lifecycle. L / Low (carried, not re-verified primary).
4. YouBRD digital — 1.92m users +12%, ~10.7m tx Q1 +24%, RON17.4bn +35% — teller-cash substitution + eKYC/onboarding relevance. M / Medium. NEW.
5. Safetech SOC incumbent — Darktrace/Cynet/Ironscales/Axonius; auto-renew 3yr from Sep-2023 → ~Sep-2026 renewal window imminent. Printec AML/txn-monitoring/HSM adjacency (Safetech = competitor). M / Low.
6. Safetech competitive strength — 7 of top-10 RO banks are clients; targets +25% turnover/profit 2026 (prelim results 24/02/2026). Competitor entrenchment context. S / Low. NEW.
7. FintechOS onboarding/loan-origination live (<8 months) — competitive context vs Printec eKYC. M / Low.
8. Backbase omni-channel platform partnership — competitive context vs Printec digital. S / Low.

## Sources
- BRD Q1 2026 EN report — https://www.bvb.ro/infocont/infocont26/BRD_20260429183423_BRD-Q1-2026-Report.pdf (29/04/2026)
- BRD Q1 2026 RO report — https://www.bvb.ro/infocont/infocont26/BRD_20260429183408_BRD-Raport-Trim-1-2026-RO.pdf (29/04/2026)
- BRD group results page — https://www.brd.ro/rezultatele-grupului-brd-t1-2026 (29/04/2026)
- bancherul (press corroboration) — https://www.bancherul.ro/brd-continua-sa-inchida-sucursale/
- Safetech SOC case study (BRD) — https://www.safetechinnovations.com/soc-services-for-one-of-europes-largest-banks
- Safetech 2025 preliminary results — https://safetech.ro/wp-content/uploads/2026/02/EN-Safetech-2025-Preliminary-Results_240226.pdf (24/02/2026)
- FintechOS case study — https://fintechos.com/case-study/brd-socgen-digital-transformation-8m/
- Backbase press — https://www.backbase.com/press/brd-groupe-societe-generale-partners-with-backbase-to-build-its-omni-channel-platform

## Access log
- BVB Q1 2026 PDF returned binary to WebFetch; local pdfminer/pypdf extraction too slow (timed out on 2.3MB file). Key figures (334 branches, 266 self-service, 1.92m YouBRD, tx/value) confirmed via BVB report + BRD results page search snippets quoting the report directly. Terminal-fleet (~1,600 / MBA / ROBO) carried from FY2025 disclosure, NOT re-verified against primary this run → confidence Low; flagged for operator PDF extraction.
- safetechinnovations.com blocked by fetch safety check; details from indexed case-study snippet.
- FintechOS & Backbase PDFs/pages: PDF binary + domain safety block; details from case-study landing snippets.
