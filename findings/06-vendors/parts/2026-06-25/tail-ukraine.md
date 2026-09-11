# Ukraine — Long-tail & NEW competitor discovery (Agent 6, 2026-06-25)

Checkpoint. Slug: tail-ukraine. Languages: EN + UK.

## Method
- Read references/competitors.json (156 vendors; UA-tracked: UPC, UkrCard/UKRKART, ProCard, amofintech, monobank, PayForce, BS/2, ISSP, CIT Security, EasyPay, IBA tapXphone, Topwise/Landi, Diebold).
- Folded intel-cache/prozorro_notices.json (PrivatBank 82 awarded, Oschadbank 15). TED has no UA scope. competitor_news.json no UA items.
- Fresh 2026 Prozorro awards now COMPLETE (baseline had them unresolved):
  - UA-2026-06-11-013572-a Mobile Android POS w/ HAL API, $2.18M (PB-2026-01-30-3067542)
  - UA-2026-06-15-012172-a ATM large-node modules (cash cassette/clamps/lock), UAH 7.21M (PB-2026-01-29-3067524)
  - PrivatBank Oct/Nov 2025: 39,000 stationary Android POS UAH 151.7M; 37,810 portable Android POS $2.80M.
  - Oschadbank UA-2025-07-15-007950-a ATM cassettes UAH 10.68M.

## Key findings
- DISCOVERY (is_new): Checkbox — UA ПРРО/fiscal vendor offering tap-to-phone (SoftPOS) acquiring integration; threatens Printec POS/TMS at the micro-merchant tail. tier=local-peer.
- DISCOVERY (is_new): Raiffeisen Bank Aval "POS terminal in 23 min" express acquiring, Android terminals, Mastercard-backed, 23/03/2026 — bank-led acquiring onboarding, erodes Printec terminal+onboarding pull-through at this acquirer.
- monobank SoftPOS ("plata by mono" / terminal-in-phone): +40% users since Jan-2025 (vendor-stated); own-brand physical POS launched Oct-2024 targeting UA top-5, ~15,000 own devices/yr — bank-as-vendor verticalization vs Printec Verifone/Castles supply.
- Regulatory TAM driver: from 01/01/2026 POS mandate extends to merchants in towns <5,000 pop (Finance.ua); from 26/06/2026 NBU phone-confirmation rule on terminal card top-ups (RBC-Ukraine).
- UA fintech SIs surfaced (Scroll.media 29/05/2026): Sigma Software (KYC/AML agents), Kindgeek (onboarding/white-label core), DeepInspire (loan origination), N-iX (core-banking modernization) — SI/onboarding rivals to Printec software & Namirial/Siron-adjacent lines.
- Prozorro fresh awards (status complete, winners UNRESOLVED — operator/Chrome on tender.privatbank.ua): UA-2026-06-11-013572-a Mobile Android POS HAL API $2.18M (PB-2026-01-30); UA-2026-06-15-012172-a ATM large-node modules UAH 7.21M (PB-2026-01-29). Also Oschadbank UA-2025-07-15-007950-a ATM cassettes UAH 10.68M.

## Access issues
- tender.privatbank.ua / prozorro.gov.ua/tender JS-only; no public friendly-ID->UUID resolver; no Chrome connected this run -> winners unresolved (operator step).
- zakupivli.pro and Forbes.ua = HTTP 403 to fetch.
