# North Macedonia banking cluster — findings 2026-07-14

Banks: Komercijalna, Stopanska (NBG), NLB, Halkbank, Sparkasse, UNIBank, ProCredit, Silk Road.
Focus: Stopanska/NBG transformation, cash-in ATMs, 24/7 zones, SEPA/instant payments, OneID.

## What's NEW / CHANGED vs previous file (2026-06-29)
- **KIBS licensed 17/09/2025 as operator of the domestic denar instant credit-transfer system** (NBRM, Law on Payment Services & Payment Systems). Project in FINAL phase: two linked platforms — central instant-clearing engine + end-user initiation/acceptance channels. NBRM separately building a **new instant-payment system as a "TIPS clone"** under the ECB Western Balkans initiative (Vice-Governor Velichkovski, makfax). Denar, real-time (~10s), 24/7/365; domestic only for now (FX law blocks cross-border). NEW/deepened. → transaction monitoring, real-time AML/fraud, HSM, managed services, POS/acceptance.
- **Stopanska "Grand" central branch (opened 26/05/2026)** — confirmed layout: advisory/consultation model (open consult positions, meeting offices, tellers, internal ATM training area) + **dedicated 24/7 ATM zone with THREE cash-in bankomats** + STB Broker. Concrete new cash-in deployment count. NEW detail (branch open was known; the 3 cash-in machines is new granularity). → cash-in ATMs/recyclers, branch transformation self-service, managed services.
- **SCA mandate from 01/03/2026**: NBRM requires strong customer authentication for online card payments; **NLB Pay became the sole app to confirm NLB online payments** (skopje1.mk). NEW. → HSM/security, transaction monitoring.
- **Halkbank NM new digital functionalities**: fully online application + approval of debit cards, credit cards and overdrafts (no branch visit), on top of Online Deposit/Online Credit — positions as digital-products leader. NEW. → digital onboarding/eKYC.
- **Printec + Namirial event "The Next-Gen Ecosystem for Digital Identity" (13/05/2026)** — regional digital-identity/eKYC ecosystem push; reinforces Printec eKYC positioning relevant to OneID banks. NEW (regional, not NM-exclusive).

## Re-verified against primary sources
- **Komercijalna (KB presentation 31.12.2025, PDF):** 189 active ATMs (largest network), 55 branches (44 city incl. 27 Skopje, 11 regional); 1 fully digital 24/7 city branch + 9 big-city 24/7 digital zones; 7 regional + 6 regional-city branches with 24/7 zones. OneID (2022), Apple Pay/Visa Direct etc. Assets EUR 3,130.8m. Printec POS/acquiring incumbent (carried). CONFIRMED.
- **SEPA live since 07/10/2025** (carried; first banks registered by EPC). Instant domestic layer is the live workstream now (KIBS).
- **Stopanska ATM directory** lists per-site CashIn yes/no flags (deposit-capable fleet exists); no total/vendor published.

## Access issues / logged
- nbrm.mk: reachable via search; specific sector ATM/POS totals pages still not pulled this run (KIBS press + bank primaries used instead).
- pdftotext unavailable locally → extracted KB PDF via pdfminer.six (worked).
- Halkbank digital-functionalities article: no firm publication date visible in fetch (Low confidence, retrieval Jul-2026).

## Signal rows: see structured output (slug=north-macedonia).
