# North Macedonia banking cluster — findings 2026-06-29

Banks: Komercijalna, Stopanska (NBG), NLB, Halkbank, Sparkasse, UNIBank, ProCredit, Silk Road.
Focus: Stopanska/NBG transformation, cash-in ATMs, 24/7 zones, SEPA/instant payments, OneID.

## Headline / what's NEW vs baseline (2026-06-24)
- **SEPA went LIVE 07/10/2025** — 9 of 12 NM banks live on SEPA credit transfer day one (NLB, Stopanska, Komercijalna, Sparkasse, Halkbank, ProCredit, TTK, UNI Banka, Centralna Kooperativna); remaining 3 due by end-Q1 2026. Fees cut ~6-8x. (NBRM / MIA). NEW.
- **NLB Banka Skopje 2025 results (30/01/2026):** completed **38 strategic transformation initiatives** — Apple Pay, "Digital first / Mobile first", SEPA integration, **phase-one branch redesign into advisory/consultation centres** (de-tellering). **2026 agenda explicitly: digital onboarding for businesses, SME lending platform, INSTANT PAYMENTS, AI.** NEW — strong managed-services/self-service/onboarding/AML pull.
- **Stopanska–OneID partnership (Jan 2026)** for remote data update/eKYC; **Apple Pay launched 20/01/2026**; **new modernized "Grand Central" HQ branch opened 26/05/2026** (Skopje centre). NEW.
- **OneID national e-ID scheme** (operated by KIBS Trust / Nextsense, registered Dec 2021) now spans **8 banks** (Komercijalna, Stopanska, NLB, Sparkasse, Halkbank, ProCredit, Silk Road, + Triglav insurer, Mint Credit). eKYC/remote-signature backbone — digital onboarding angle. NEW depth.
- **Printec = verified incumbent at Komercijalna** (POS/acquiring): Komercijalna's ENTIRE POS terminal network made contactless via Printec — "first bank in country" fully contactless; Printec named "trusted partner". Printec has a Skopje legal entity (Printec Technology DOOEL). Confirms in-country delivery base. CARRIED→VERIFIED.

## Komercijalna Banka (primary: 31.12.2025 presentation PDF)
- **189 active ATMs** (largest network in country), **55 branches** (Dec 2025).
- 1 fully digital 24/7 branch + 9 big city branches w/ 24/7 digital zones + 13 regional w/ 24/7 zones.
- Digital kiosks for cashless payments; mBanka/mBankaKo apps; KomPay m-wallet (MasterCard, 2018); OneID e-ID (2022, "Top Innovator UX" award); largest issuer, VISA card-acceptance growth award 4 yrs.
- Largest bank: assets €3,130.8m, 21.66% share. Printec POS incumbent.

## Stopanska Banka (NBG, ~93.4%)
- 60 cash-in ATMs deployed (denar deposits, 24/7) — dated **Nov 2023** (baseline-era, NOT new), vendor not named.
- NBG synergy/know-how transfer in digital transformation; Oracle Mantas AML, Azure/M365 stack.
- NEW 2026: OneID data-update, Apple Pay, Grand Central branch, MIPS domestic fee cuts -70% (Aug 2025).

## NLB Banka Skopje
- NLB **Cash In ATMs** (24/7) live — deposit-capable fleet (recycler-class), vendor not named.
- 2025 transformation + 2026 instant-payments/onboarding/AI roadmap. Assets 156.9bn MKD (+19.6%).

## Others
- ProCredit Bank: runs "Зона 24/7" self-service zones model; digital-first.
- Sparkasse: OneID participant (azuriranje), expanding ATM network (FB).
- Halkbank: OneID participant; Halk Mobi POS (softPOS); OneID announcement page TLS-cert error.

## Access issues
- NBRM (nbrm.mk) sector ATM/POS totals: HTTP 403 even with desktop browser UA — sector counts NOT verified this run. Needs Claude-in-Chrome.
- KB PDF binary to WebFetch → extracted locally with pdftotext (worked).
- blog.printecgroup.com & printecgroup.com/offices: 403 (Printec-KB contactless detail via search index).
- halkbank.com.mk OneID page: TLS ERR_TLS_CERT_ALTNAME_INVALID.
