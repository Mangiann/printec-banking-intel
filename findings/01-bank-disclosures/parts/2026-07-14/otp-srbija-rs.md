# OTP banka Srbija — findings 2026-07-14 (re-verify + new discovery)

## Summary
OTP banka Srbija a.d. Novi Sad — 2nd-largest bank in Serbia, part of OTP Group (Hungary). Confirmed footprint: **274 ATMs** (largest network in Serbia, 91 cities), ~153 branches, ~2,734 employees. Fleet is DN-heavy (Diebold Nixdorf DN450V, CINEO2550/C2560 recyclers) with RECYCLING-tagged units live; **Cash-In self-service deposit machines at 85 branch locations**. Payten (Asseco SEE) / Chip Card is the incumbent card/ATM/POS processor. 2025 after-tax profit +19% (HUF 79.3bn contribution). Digital-first, self-service migration strategy.

## NEW / CHANGED vs 2026-06-24 baseline
- **Active 2026 branch-adaptation tender programme** (primary, otpbanka.rs tenders page, dateModified 08/07/2026): a continuous stream of "Adaptacija ekspoziture" tenders in 2026 — Stara Pazova (08/07), Kuršumlija (05/06), Niš (05/06, 12/05), Vršac (18/05), Požega (12/05), Odžaci (07/04), Vrbas (24/03), Bačka Palanka (24/03), Beograd/Save Maškovića (12/03), Paraćin (12/03). 10+ branches refitted Mar–Jul 2026 => branch-transformation wave; Printec entry for in-branch self-service / TCR / recycler / kiosk placement during refits.
- **PSD2/open-banking deadline 01/01/2026 now PASSED / in force**: NBS RTS published + compliance deadline extended to 01/01/2026 (from 06/05/2025). As of Jul-2026 banks in technical implementation; open-banking (AIS/PIS, SCA, secure TPP APIs) is a live legal obligation for OTP Srbija => HSM/SCA/fraud & transaction-monitoring/AML angle. Payten/Chip Card likely API-layer provider (competitive to Printec on monitoring).
- **Payten/Chip Card "Digital First" card issuance implemented for OTP Bank Serbia** (Q4): instant card details/PIN/wallet provisioning via mobile app before physical card. Deepens processor incumbency (processing lock, not HW/managed-services lock).
- **Chip Card / Payten deploying "unattended POS terminals for automated services" in Serbia** — self-service/unattended payment automation; competitive context for Printec self-service.
- **Chip Card powered first Discover transaction in Serbia**; **Chip Card awarded e-money issuing licence by NBS** — Payten ecosystem expansion around OTP.
- **OTP Group Q1-2026**: after-tax profit HUF 324bn (~EUR 845m), +9% YoY (group, not Serbia-specific) — capex capacity intact.

## Fleet / vendor (carried, re-verified)
- DN-heavy: DN450V, CINEO2550/C2560 recyclers; RSD+EUR deposit, EUR withdrawal live. Multi-vendor managed-services + OptiCash + recycler-lifecycle fit.
- Printec services OTP GROUP's Croatian fleet (OTP HR + Splitska, 500+ NCR ATMs) — group-level reference to leverage into Serbia.

## Printec angle
- 274 DN recycler fleet + post-merger harmonisation => OptiCash + multi-vendor managed services + monitoring.
- 2026 branch refits => in-branch TCR/kiosk/self-service placement window.
- Open-banking in force => HSM / SCA / INETCO transaction monitoring / Siron AML white-space (no named Printec AML vendor).

## Sources
- https://www.otpbanka.rs/o-nama/osnovni-podaci-2/ (2026 branch-adaptation tenders; dateModified 08/07/2026)
- https://www.otpbanka.rs/en/cash-processing/ (Cash-In at 85 branches)
- https://www.companywall.rs/firma/otp-banka-srbija/MMhYcOr0 (274 ATMs, 153 branches, 2,734 employees)
- https://seenews.com/news/otp-banka-srbijas-after-tax-profit-rises-19-percent-in-2025-1291013
- https://www.payten.com/en/news-events/news/digital-first-functionality-for-otp-bank-in-serbia/
- https://www.payten.com/en/news-events/news/unattended-pos-terminals-for-automated-services-in-serbia/
- https://www.payten.com/en/news-events/news/chip-card-powers-first-discover-transaction-in-serbia/
- https://ffnews.com/newsarticle/fintech/the-national-bank-of-serbia-publishes-regulatory-technical-standards-and-extends-psd2-compliance-deadline-to-january-1st-2026/
- https://zuniclaw.com/en/open-banking-serbia/
- https://bif.rs/2026/05/otp-grupa-zabelezila-snazan-rast-u-prvom-kvartalu-2026-godine/

## Access log
- payten.com — WebFetch fails (TLS "unable to verify first certificate") and browser-UA curl hangs; content from search snippets + partial curl. Operator re-fetch needed for exact article dates.
- otpbanka.rs — WebFetch "Socket is closed"; browser-UA curl succeeded (tenders table extracted).
- ceelegalmatters.com/banking-2026 — HTTP 403 on WebFetch; open-banking status corroborated via zuniclaw + ffnews.
- openbankingtracker.com/country/serbia — WebFetch timeout; status from search snippet + zuniclaw.
