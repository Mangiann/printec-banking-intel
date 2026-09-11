# Kosovo (CBK) — Statistics findings — 2026-06-24

Primary sources this run (fetched via browser-UA curl + pdfminer; bqk-kos.org returns 403 to WebFetch):
- CBK National Payments Council (NPC) summary minutes, meeting 17 Jun 2025 — https://bqk-kos.org/wp-content/uploads/2025/06/ENG_Minutat-e-takimit-te-KKP_Final_17062025.pdf?lang=en
- CBK "Use of Bank Cards in Kosovo" Sep 2025 ed. (data 31 Dec 2024) — https://bqk-kos.org/repository/docs/SistemiIPagesave/Use%20of%20bank%20cards%20in%20Kosovo.pdf
- CBK press release 14 Feb 2025 (financial inclusion, end-2024) — https://bqk-kos.org/news/rritet-perfshirja-financiare-integriteti-i-sistemit-financiar-zgjerohet-rrjeti-i-institucioneve-financiare-dhe-sherbimet-digjitale/?lang=en
- German Economic Team, Kosovo SEPA accession brief — https://www.german-economic-team.com/en/newsletter/kosovos-sepa-accession-process-progress-and-expected-benefits/
- TEB Kosova (81 deposit ATMs) — https://teb-kos.com/en/digital-banking-channels/

## NEW / CHANGED vs baseline (baseline = end-2024 hard counts only)
- SEPA: pre-application completed Dec 2024; EU assessment POSTPONED due to constitutional review of the 3 new laws; CBK expects positive outcome 2026. SEPA est. EUR 55m/yr benefit (remittances 3.05%->0.67%; trade 0.43%->0.04%).
- INSTANT PAYMENTS ("TIPS Clone"): Letter of Intent signed with Bank of Italy (TIPS operator) + 3 regional central banks for a joint fast-payments solution. Major new ISO 20022 / real-time rail program.
- Law on Payment Services transposes PSD2/EMD2/PAD/IFR + package of 20 regulations -> open banking, PISP/AISP, strong customer authentication.
- POS transactions +43% y/y (NPC Jun 2025) — continuing trend after +36.78% (2024 card-card report).
- MERCHANT POS GAP: only 6,234 of 90,365 active business accounts (6.7%) have POS terminals; 1.21m citizens 16+, 88% banked. Huge POS acceptance whitespace.
- Apple Pay & PayPal enablement in progress (Google Pay already live); QR-code standardization guideline approved; IBAN extended to non-bank PSPs.
- Bank-level: TEB Kosova network at 81 deposit-capable ATMs.

## Hard infra (latest hard counts still end-2024)
- ATMs 635 (+8.4% y/y); deposit-capable 377 (59.4%); credit-transfer 53. POS 20,913 (+21.4% y/y), 98% contactless. Cards ~1.7m (+4.4%); contactless 77%. 48.14 cashless txns/capita 2024 (target was 25 by 2026). E-money accounts 79,706 (+74.6%). 2.6m customer accounts.

## Printec mapping
- TIPS Clone + ISO 20022 + open banking -> INETCO real-time monitoring, Thales HSM/PCI, terminal/onboarding stack.
- 377 deposit ATMs & growing -> NCR intelligent-deposit/recycler + x-core multivendor + telemetry.
- 6.7% merchant POS penetration + 43% txn growth -> Verifone/Castles + TMS (largest opportunity).
- eKYC/Namirial + Siron/FICO AML aligned to new AML-law amendments & PSD2 SCA.
