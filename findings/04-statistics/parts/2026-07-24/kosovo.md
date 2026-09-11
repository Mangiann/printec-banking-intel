# Kosovo (CBK/BQK) — Statistics findings — run 2026-07-27

Focus: ATM count + deposit-capable share, POS growth, card stats. Languages: EN + Albanian.

## Access notes
- bqk-kos.org HTML pages are behind a Cloudflare "Just a moment" JS challenge (desktop-UA curl did NOT defeat it this run; time-series/statistics HTML pages unreadable via curl). Direct PDF/repository & wp-content URLs bypass the challenge and returned HTTP 200 — extracted locally with pdfminer.
- bankassoc-kos.com & balkaninsight.com return 403 to WebFetch; desktop-UA curl succeeded.

## Sources this run
- CBK "Use of Bank Cards in Kosovo" Sept 2025 ed. (data 31 Dec 2024) — https://bqk-kos.org/repository/docs/SistemiIPagesave/Use%20of%20bank%20cards%20in%20Kosovo.pdf
- CBK Financial System Monthly Info, Nov 2025 (banking macro only, no payments) — https://bqk-kos.org/wp-content/uploads/2025/12/BQK_SF_Nentor-2025.pdf
- KBA "Towards the modernization of the payment system!" — KIPS Upgrade & TIPS workshop, Brezovica (27/07/2026) — https://bankassoc-kos.com/towards-the-modernization-of-the-payment-system/
- KBA "Kosovo banking sector moves towards instant payments" — CBK/KBA workshop 19/05/2026 — https://bankassoc-kos.com/kosovo-banking-sector-moves-towards-instant-payments/
- KBA "Peja paves the way…" TAP to Phone / SoftPOS event with Visa — https://bankassoc-kos.com/peja-paves-the-way-towards-faster-and-safer-digital-payments/
- KBA "Gjakova is moving towards the future of digital payments" — https://bankassoc-kos.com/gjakova-is-moving-towards-the-future-of-digital-payments/
- Balkan Insight (BIRN), 18/11/2025 — Kosovo SEPA delay; €55m/yr savings — https://balkaninsight.com/2025/11/18/kosovo-paying-high-price-for-delay-in-joining-single-euro-payment-area/bi/
- ECB MIP news 17/01/2025 — Western Balkans instant payment settlement (TIPS Clone) rollout — https://www.ecb.europa.eu/press/intro/news/html/ecb.mipnews250117_2.en.html
- CBK Dec 2025 regulation, non-bank PSP access to payment systems — https://bqk-kos.org/wp-content/uploads/2025/12/Rregullore-per-qasjen-e-ofruesve-te-sherbimeve-te-pagesave-jo-banka-ne-sistemet-e-pagesave.pdf

## Hard infra (still end-2024 — next annual card report ~Sept 2026)
- ATMs 635 total: withdrawal 634, credit-transfer 53, cash-deposit 377 -> deposit-capable share 59.4%. POS 20,913 (18 with cash-withdrawal, 20,895 EFTPOS); 98% of POS contactless. Cards ~1.7m, 77% contactless. Source: CBK card report Sept 2025 (data 31/12/2024). CONFIRMS baseline, not new.

## NEW / CHANGED this run
- KIPS UPGRADE + TIPS workshop (KBA Payments Committee + CBK, Brezovica, 27/07/2026): harmonization of technical standards, national/government payment rules, NEW FILE FORMATS; CLONE TIPS + ISO 20022 transaction-limit definition; e-banking adaptation; standardization of instant payments across banks. -> Live implementation phase of the real-time rail. Printec: ISO 20022 migration, HSM, transaction monitoring, managed services, e-banking integration.
- Instant-payments workshop 19/05/2026: CBK Payments Dept Director Lumni Rrustolli on TIPS Clone technical architecture for 24/7 execution; external expert Daniel Jonas on strategy; Deputy Governor Dardan Fusha. -> vendor selection / integration window imminent.
- TIPS Clone regional instant-payments go-live expected AFTER H1 2026 (Albania, BiH, Montenegro, N.Macedonia, Kosovo). -> now in build/rollout, not just LoI (baseline).
- SEPA STILL BLOCKED: final application not submitted; three laws (08/L-304 Banks, 08/L-328 Payment Services, 08/L-333 AML amendment) awaiting Constitutional Court; Feb-2025 election political impasse, likely re-election. GET estimate €55m/yr savings (€26m remittances + €29m trade). 4 neighbours joined SEPA Oct 2025. -> PSD2/open-banking + AML stack deferred but pipeline intact.
- TAP-to-Phone / SoftPOS roadshow (Peja, Gjakova) with Visa targeting SMEs -> smartphone card acceptance to attack the merchant-POS whitespace (only ~6.7% of business accounts had POS at end-2024). Printec: SoftPOS/acquiring, TMS.
- Dec 2025 CBK regulation: non-bank PSP access to payment systems (IBAN/PSP access) -> new acquirers/PISPs entering; open-banking rails.
