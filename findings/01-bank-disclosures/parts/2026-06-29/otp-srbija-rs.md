# OTP banka Srbija — findings 2026-06-29

## Summary
OTP banka Srbija a.d. Novi Sad — 2nd-largest bank in Serbia (14.22% asset share, RSD ~995.98bn total assets, 2025); ~725k active clients, 154 branches/91 cities, ~275 owned ATMs, ~2,720 employees. #1 in retail+corporate loans (housing 22.1%, cash 19.5%). Formed by merging Société Générale Srbija + Vojvođanska banka + OTP Banka Serbia under OTP Group (Hungary). Strategy = digital transformation + market-position defence; cashless/cash-light branches pushing clients to ATMs (self-service migration); video onboarding (<15 min, digital card instant).

## Fleet (vendor mix CONFIRMED)
- ATM locator exposes hardware models: **DN450V (DN Series 450V), CINEO2550 / C2560 (Wincor/Diebold Nixdorf CINEO recyclers)** => fleet is substantially Diebold Nixdorf with recyclers already live. RECYCLING-tagged ATMs at many sites; RSD+EUR deposit, dinar deposit, EUR withdrawal, business cash deposit (≤50k RSD).
- Fleet figures vary: bank FAQ ">300 devices"/322 locator points; thebanks.eu 275 owned ATMs (2025); FB post (dated) 286. Shared withdrawals via Multicard/Vojvođanska + 165 MoneyGet ATMs.

## Processing / payments
- **Payten (Asseco SEE) + Chip Card** = card/ATM/POS processing incumbent; did the Vojvođanska+OTP migration (completed Jun 2021); first-in-Serbia SoftPOS with OTP. Processing lock, NOT a hardware/managed-services lock.
- UnionPay acceptance at OTP ATMs (SeeNews).
- Serbia not EU => no PSD2; NBS IPS instant payments live (incl. merchant-POS instant pay). No OTP Srbija open-banking API confirmed (OTP Croatia has api.otpbanka.hr).

## Printec angle
- Printec is an active Serbian-market vendor (NCR SelfServ 91 video-ATM showcase 2015) AND services OTP GROUP's Croatian fleet: **OTP banka Hrvatska + Splitska banka — 500+ ATMs, full HW/SW support on NCR APTRA Advance NDC** (group-level reference to leverage). DN-heavy Serbian fleet fits Printec multi-vendor managed services + OptiCash + recycler lifecycle.
- Recurring biddable tenders on OTP Srbija site: ATM illuminated masks (Mar 2025), counter cash registers (50 units, Aug 2024), thermal rolls, physical-technical security, branch adaptations.

## Sources
- https://www.otpbanka.rs/najcesca-pitanja-bankomati/
- https://www.otpbanka.rs/en/locations-of-branches/ (DN450V/CINEO2550/C2560 models)
- https://www.otpbanka.rs/o-nama/osnovni-podaci-2/ (tenders)
- https://www.otpbanka.rs/digitalna-transformacija-i-ocuvanje-trzisne-pozicije-glavni-prioriteti/
- https://thebanks.eu/banks/18540/market_share (assets/share/ATM count)
- https://www.payten.com/en/news-events/news/successful-integration-project-vojvodjanka-banka-d-novi-sad-and-otp-banka-serbia-supported-chip-card/
- https://www.payten.com/en/news-events/news/otp-banka-and-payten-implemented-revolutionary-contactless-payment-solution-first-time-serbia-softpos/
- https://blog.printecgroup.com/otp-and-splitska-banka-trust-printec-with-their-atm-fleet-suport (OTP Group Croatia 500+ ATM reference)
- https://www.ekapija.com/news/1133199/ (Printec NCR SelfServ 91 Serbia)
- https://nbs.rs/en/ciljevi-i-funkcije/platni-sistem/nbs-operator/ips-nbs/ (NBS IPS)
- https://seenews.com/news/otp-starts-accepting-cards-of-chinas-unionpay-at-atms-in-serbia-1173856
