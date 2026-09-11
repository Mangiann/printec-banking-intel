# Kosovo (CBK) — Statistics findings — 2026-07-15

Primary sources this run (all via browser-UA curl + pdfminer; bqk-kos.org & bankassoc-kos.com return 403 to WebFetch):
- CBK Annual Report 2024 (BQK_RV_2024.pdf, published Jul-2025) — https://bqk-kos.org/wp-content/uploads/2025/07/BQK_RV_2024.pdf — multi-year ATM/POS series + 2024 txn volumes/values.
- CBK "Use of Bank Cards in Kosovo" Sep-2025 ed. (data 31 Dec 2024) — https://bqk-kos.org/repository/docs/SistemiIPagesave/Use%20of%20bank%20cards%20in%20Kosovo.pdf
- CBK Monthly Financial System info, NOVEMBER 2025 (BQK_SF_Nentor-2025.pdf) — https://bqk-kos.org/wp-content/uploads/2025/12/BQK_SF_Nentor-2025.pdf — bank units/branches 235, 10 banks, 4,203 staff.
- Kosovo Banking Association, "Kosovo banking sector moves towards instant payments," 19/05/2026 — https://bankassoc-kos.com/kosovo-banking-sector-moves-towards-instant-payments/
- CEE Legal Matters, "Kosovo: New Banking Law Comes into Force…" (2026) — https://ceelegalmatters.com/briefings/32395-kosovo-new-banking-law-comes-into-force-with-further-reforms-ahead
- Law on Banks 08/L-304, Gazeta Zyrtare Nr.2, 27/01/2026 — https://bqk-kos.org/wp-content/uploads/2026/01/LIGJI_NR._08_L-304_PER_BANKAT.pdf
- CBK regulation on non-bank PSP access to payment systems, Dec-2025 — https://bqk-kos.org/wp-content/uploads/2025/12/Rregullore-per-qasjen-e-ofruesve-te-sherbimeve-te-pagesave-jo-banka-ne-sistemet-e-pagesave.pdf
- World Bank feature 25/03/2026 (instant payments "later this year" incl. Kosovo).

## NEW / CHANGED vs 2026-06-24 baseline
- LEGAL SETBACK (material): Constitutional Court ANNULLED the Assembly's Dec-2024 decisions on procedural grounds. Law on Payment Services 08/L-328 (+AML) were REPEALED; only the Law on Banks survived / was re-enacted (08/L-304 in force via Gazeta Zyrtare 27/01/2026). PSD2/EMD2/PAD/IFR transposition + 20-reg package + SEPA now gated on RE-ADOPTION of the Payment Services law. Baseline treated the laws as merely "gated on review" — they were actually struck down.
- Bank units/branches = 235 (Nov-2025); 10 banks (7 foreign), 4,203 employees. FRESH branch count.
- TIPS clone still on: finalized "mid-2026" (AR2024) / instant payments "later this year 2026" (WB Mar-2026, KBA May-2026). LoI with Bank of Italy + regional CBs.
- CBK joined EACHA (European Automated Clearing Houses assoc.) 2024 — clearing modernization.
- ARC (Civil Registration Agency) + KBA partnership 12/05/2026 for account-data update without physical presence → remote onboarding/eKYC angle.
- CBK QR-code standardization guideline approved (retail + bill payments).
- Dec-2025 regulation opens payment-system access to non-bank PSPs (IBAN extended to EMIs/PIs).

## Hard infra — latest confirmed hard counts still END-2024 (AR2025 delivered to Assembly 30/06/2026 but PDF not yet on site; next "Use of Bank Cards" ~Sep-2026)
- ATMs 635 (2024); withdrawal 634, credit-transfer 53, DEPOSIT-CAPABLE 377 (59.4%). Multi-year: 513/516/534/583/635 (2020-24).
- POS 20,913 (2024); 18 w/ cash-withdrawal, 20,895 EFTPOS; 98% contactless. Multi-year: 13,421/13,836/14,769/17,187/20,913 (AR2024 shows 2024=20,859).
- Cards: debit ~1.5m (+5.61%), credit ~195k (+8.17%) end-2024; 1,281,368 contactless cards; 55% Visa / 43% MC / ~2% local.
- 2024 txns: ATM withdrawals 22,168,758 (+3.1% count), value €4,566,821,728 (+5%); POS payments 46,516,019 (+39.4% count), value €1,344,220,625 (+31.8%); e-banking 11,365,089 txns, €24,969,678,755. Card accounts 2.53m.
- Merchant whitespace: only 6,234 of 90,365 active business accounts (6.7%) have POS.

## Printec mapping
- 377 deposit ATMs (59.4%) & growing → NCR intelligent-deposit/recyclers + x-core + APTRA OptiCash + telemetry.
- 6.7% merchant POS penetration + POS txns +39.4% → Verifone/Castles + TMS (largest single opportunity).
- TIPS clone + ISO 20022 + non-bank PSP access → INETCO real-time monitoring, Thales HSM/PCI.
- Payment-Services-law re-adoption → PSD2 SCA/open banking → eKYC (Namirial), Siron/FICO AML; ARC/remote-onboarding partnership reinforces eKYC.
- 235 branches / branch offload → self-service kiosks + deposit ATMs.
