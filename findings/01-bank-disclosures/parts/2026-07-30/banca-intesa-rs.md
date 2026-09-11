# Banca Intesa Beograd — 2026-07-30 run

## Headline
The **2025 narrative annual report IS now published** — but not where the baseline looked for it. It is embedded inside the audited separate financial statements PDF (`Banca Intesa ad Pojedinacni FI 2025.pdf`, 5.29 MB), which the standalone `Godisnji_izvestaj_2025` path does not serve (404). Extracted locally with pdfminer. This closes the baseline's "2025 narrative annual report still unpublished" gap and supersedes the 2024-vintage 407 ATM / 110 cash-in / 118 kiosk numbers.

## Fleet, from the horse's mouth (31/12/2025)
- **434 self-service devices**, of which **375 dispense RSD**
- **123 multifunctional cash-in/cash-out devices** (RSD deposit+withdrawal, EUR from FX accounts)
- **135 specialised merchant daily-takings (pazar) deposit devices in 123 of 134 branches**
- 2025 activity: **+14 new ATMs, 26 in-branch ATMs replaced**
- **134 branches** (flat), **66 clusters**, network FTE **1,336** (−26), **24% cashless-format branches**, 6 full refurbishments + 20 partial
- 2,943 staff (vs 3,044 in 2024)

## Recycler business case is already proven here
- RSD deposits at devices = **86%** of equivalent teller deposits; EUR = **73%**
- 1.5m RSD deposits (+13.8%) ≈ **RSD 56bn** (+21.4%); 386k EUR deposits (+18.6%) ≈ **EUR 360m** (+21.4%)
- 2.3m merchant takings deposits ≈ **RSD 315bn**; 86% migrated off the teller
- ~21m ATM withdrawals incl. 442,000 in EUR; contactless withdrawal 1m txns / 101k users

## Baseline correction — the Payten story was two separate events
- **04/03/2020** Payten release: 200 ATMs replaced with **Diebold Nixdorf Cineo**, some with recycling. NOT part of the 2023 deal.
- **13/12/2023** Payten release: buy-out of **122 external-location ATMs**, **36-month** outsourcing contract, all installed machines replaced with latest-generation **DN CashOut and Recycling** devices within 12 months, plus pre-install works, network comms, **Vynamic Security**, site-lease negotiation; bank moves to no-capex fixed fee and transfers VISA/MC/PCI DSS compliance risk.
- **36 months from Dec-2023 ⇒ expiry around Dec-2026.** That is the single most actionable Printec window at this bank.
- FY2025 Note 20(a) confirms **POS terminals, ATM and ATS printer devices are leased** (right-of-use, portfolio approach) — device-as-a-service is now the bank's structural commercial model.

## Software / compliance
- Strategy commits to **"digitalisation of processes in financial-crime prevention and compliance"**; AML sits inside the Risk Appetite Framework and new AML/legal/IT early-warning limits were added in 2025. 23,130 AML training hours, 2,611 staff. Fraud: 168 suspicions analysed, 153 proven (4 internal / 149 external).
- **Isytech International IBD solution** = ISP group-standard digital-channel + single branch workstation stack ⇒ that layer is largely closed to Printec.
- Explicit intent to **"centralise or outsource shared activities"** + next-generation procurement cost programme ⇒ positive for managed services.
- Paperless Branch / Remote Offer runs on **ConsentID**, the Serbian eGovernment Office's cloud qualified e-signature ⇒ eKYC/e-signature white space is effectively closed.
- PD/LGD/EAD models rebuilt on **Google Cloud BigQuery + Vertex AI**.

## Market / regulatory context (Serbia)
- NBS Q1-2026: **187,957 POS** (+10.3%, +17,523 units), **ATM count +3.6% YoY**, 13,343,642 cards (+8.0%), 195.2m card POS txns (+18.7%). Serbia's ATM estate is still **growing**, unlike Western Europe.
- NBS draft amendments to the Interbank Fee Law (Jun-2026) would cap interchange on **foreign-issued** cards at 0.2% debit / 0.3% credit for the first time.
- NBS primary regs page flags as NOVO: AML Guidelines Decision (Gazette **41/2025**) and the remote **electronic identity verification** Decision (Gazette **43/2026**).

## Still open
- OEM of the 123 multifunctional units and the 135 takings devices is **not disclosed** (DN Cineo is the strong inference from Payten 2020/2023, unconfirmed for 2025 deployments).
- Whether the 434 includes the 122 Payten-owned external units.
- Exact expiry/renewal mechanics of the Payten 36-month contract — not disclosed by either party.
