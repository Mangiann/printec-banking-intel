# MiCA / crypto-asset rules — findings 2026-06-24

Slug: mica-crypto. Single-agent; confidence capped at Medium.

## Plain-language frame
MiCA (Markets in Crypto-Assets Regulation, EU 2023/1114) is the EU's single rulebook for crypto. A **CASP** (Crypto-Asset Service Provider) is any firm offering crypto custody, exchange, trading, transfer, etc. — it now needs one EU licence (passportable). An **EMT** (e-money token) is a stablecoin pegged 1:1 to a single fiat currency (e.g. euro); an **ART** (asset-referenced token) is backed by a basket. Banks ("credit institutions") get a lighter **notification** route (not full licensing) to offer crypto services.

## Key signals
1. **Qivalis** euro-stablecoin JV (Amsterdam, inc. Dec 2025): 37 banks / 15 countries by May 2026; founding members include **Raiffeisen Bank International (RBI)** — a Printec footprint bank — plus ING, KBC, UniCredit, CaixaBank, Danske, DekaBank, SEB, Banca Sella, BNP Paribas. Pursuing **DNB (Dutch central bank) EMI licence**; not yet granted as of May 2026. **H2 2026 launch** target. EMT 1:1 euro-backed, >=40% bank deposits + euro sovereigns; 24/7 redemption. Infra: **Fireblocks** (tokenisation/custody/treasury/compliance).
2. **RBI own CASP process** — initiated MiCAR CASP licensing via a subsidiary to offer **ART tokens for clients in 2026**; CEE subsidiaries building crypto custody with third-party custodians; Raiffeisen Landesbank NÖ-Wien partners Bitpanda in Austria. (RBI blog 22/01/2026.)
3. **Banca Sella** — first Italian bank authorised under MiCA (notification cleared 27/05/2026); custody/transfer/receipt for corporates in 2026; infra on **Fireblocks** pilot; **AML/KYC via Chainalysis** (blockchain analytics). Direct template for footprint banks.
4. **1 July 2026 hard deadline** — MiCA transitional/grandfathering ends across EU/EEA; RO, CY, BG had 18 months (to 01/07/2026); GR reportedly 12 months (ended ~30/12/2025 per secondary — conflicts with ESMA list, LOW). Unlicensed CASPs must cease serving EU clients.
5. **Travel Rule / TFR** — zero-threshold: every CASP-to-CASP transfer carries originator/beneficiary data; unhosted-wallet verification >EUR1,000; must be operational by 01/07/2026. AMLA begins supervising largest cross-border crypto firms 2026.

## Printec hook
Bank crypto/stablecoin entry = AML/KYC (IMTF Siron, FICO), on-chain + fiat transaction monitoring (INETCO), digital onboarding/eKYC (Namirial), Thales HSM/PCI for key custody. RBI is footprint (x-core ATM sw at Raiffeisen Serbia) — direct account angle.

Access: all via WebSearch/WebFetch; no Chrome escalation. Operator PDF: ESMA grandfathering list PDF + end-of-transitional-periods statement worth an operator pull to pin GR date.
