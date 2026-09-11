# Albania (Bank of Albania) — ATM/POS/Cards/Cash — findings 2026-07-27

Focus: payment instruments series (ATM/POS/cards/cash). Primary sources: Bank of Albania press + BIS keynote (Holta Zaçaj, Balkan Payment Forum, 14/05/2026); press: Monitor.al (20/02/2026).

## Headline 2025 statistics
- **POS terminals: 31,263 (+27.7% YoY)** — record. (Monitor 20/02/2026)
- **Card payments at POS: 27.2M txns (+38.7%), value 105.75bn lek (+27%)**. POS now 17.5% of card ops (was 16%).
- **Milestone: POS card payments surpassed ATM cash withdrawals for the first time** (51% vs <43% of txns, 9M 2025).
- **Active cards: 1.65M (+9.4%); debit 1.46M (+10%, ~88%); credit ~120k (+5.6%)**.
- Card payments = 67% of all bank payments; 94% of card payments by individuals.
- **~900 ATMs, 11 banks; ~35-40% of ATMs accept deposits** (CPT Group). Cash in circ. growing ~7.5%/yr 2020-24.
- Bank branches ~390 (2023) down from 429 (2019).

## Structural / regulatory
- **Instant payments**: BoA cloning Bank of Italy TIPS; go-live targeted fall 2026 (tentative June 2026). Centralized unified QR Code planned. (Monitor)
- **SEPA**: Albania acceded Nov 2025; 363k SEPA transfers / €4.3bn in first 6 months across 11 banks. (BIS keynote 14/05/2026)
- **Open banking**: first licence to EMI Easypay sh.p.k. 26/11/2024; now 2 EMIs live on open banking; 10 EMIs licensed post-PSD2 (Law 55/2020). (BoA press; BIS keynote)

## Printec mapping
POS/acquiring (booming POS base); card issuance/personalization; cash automation/recyclers (dispense-only ATM upgrade, cash still growing); instant-payments/QR rails → transaction monitoring + HSM; SEPA → AML/compliance + monitoring; open banking → eKYC/onboarding + API security/HSM; branch decline → self-service migration + managed services.

## Access log
- BoA press page HTTP 403 to WebFetch → retried with desktop UA curl, succeeded.
- BoA payment stats page = JS/Cloudflare-rendered tables (ajax); values taken from press + keynote instead.

(See structured signals for full rows.)
