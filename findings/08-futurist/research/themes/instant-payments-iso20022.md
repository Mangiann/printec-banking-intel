# Instant payments & ISO 20022 maturing; account-to-account; VoP

## Direction & summary (2027-2031)

The 2025-2026 window flips instant payments from an optional rail to the European default. The EU Instant Payments Regulation (IPR) has, since 9 October 2025, obliged all euro-area PSPs to both receive and send SEPA instant credit transfers (SCT Inst) at no premium over standard transfers, and to offer free Verification of Payee (VoP) before every euro credit transfer. Non-euro EU PSPs follow by 9 July 2027. In parallel, the SWIFT cross-border MT-to-ISO 20022 coexistence period closed on 22 November 2025, so by 2027 ISO 20022 is the de-facto messaging standard for both domestic instant and cross-border flows — carrying richer, structured data (structured addresses become mandatory from November 2026) that makes VoP, fraud screening, sanctions matching and reconciliation materially easier.

Over 2027-2031 the arc is one of maturation rather than introduction: instant settles as the baseline (Capgemini projects ~22% of global non-cash volume by 2028; McKinsey sees EU instant transactions rising ~10x to ~30bn by 2028 at ~50% CAGR), and the strategic battleground moves up the stack to account-to-account (A2A) payments at the point of sale and in e-commerce, where instant rails plus open banking and pan-European wallets (EPI's Wero) credibly threaten 15-25% of future card-volume growth. Cross-border interlinking (BIS/Nexus, TIPS-to-Nexus exploration) and the digital euro (pilot from H2 2027, potential first issuance 2029) extend the instant paradigm internationally and into central-bank money. Confidence: HIGH on the regulatory/standards trajectory in Europe (it is legislated and dated); MEDIUM on the pace at which A2A displaces card volume and on digital-euro issuance, which remains contingent on EU legislation expected in 2026. The objective read: demand shifts decisively from "can we do instant?" to "can we do instant safely, with structured data, at A2A scale, cross-border" — i.e. toward verification, fraud, ISO 20022 data handling and acceptance, not just clearing connectivity.

## Key drivers

- EU Instant Payments Regulation mandates: euro-area PSPs must receive SCT Inst from 9 Jan 2025 and send from 9 Oct 2025 at no extra cost; non-euro EU PSPs by 9 Jul 2027 — a hard, dated demand pull. [ECB Instant Payments Regulation](https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html); [EPC/ECB SCT Inst status update, June 2025 ERPB, p.2-3](https://www.ecb.europa.eu/paym/groups/erpb/shared/pdf/23th-ERPB-meeting/Status_update_on_SCT_Inst_scheme_and_QR-code_standardisation.pdf)
- Verification of Payee (VoP) became mandatory for euro-area PSPs on 9 Oct 2025 (free name+IBAN check before every credit transfer), with the EPC VoP Scheme Rulebook in force from 5 Oct 2025; non-euro EU PSPs by 9 Jul 2027 — creates a standing demand for verification/matching infrastructure. [PwC Legal — VoP under the IPR](https://legal.pwc.de/en/news/articles/verification-of-payee-requirements-vop-under-the-eus-instant-payments-regulation-ipr); [EPC — VoP scheme rulebook now in force](https://www.europeanpaymentscouncil.eu/document-library/press-releases/verification-payee-scheme-rulebook-now-force)
- ISO 20022 cross-border coexistence ended 22 Nov 2025 (end of MT/MX parallel run); structured-only/hybrid postal addresses mandatory from Nov 2026 — richer structured data becomes the norm, enabling better VoP, fraud and reconciliation. [Swift — ISO 20022 for financial institutions](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions); [NICE Actimize — Nov 2025 deadline](https://www.niceactimize.com/blog/aml-iso-20022-deadline)
- Bank readiness gap is the bottleneck and the opportunity: only 5% of banks were assessed "ready to lead" instant-payment acceleration, only 13% of European banks have a strong technology foundation, and only 25% could receive / 53% fully send instant payments at survey time. [Capgemini World Payments Report 2025 press release, p.1-2](https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf)
- A2A as a card challenger: A2A instant solutions bypass card networks and could offset 15-25% of future card-transaction-volume growth; EPI's Wero wallet is expected to accelerate European A2A adoption. [Capgemini WPR 2025 press release, p.1](https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf); [McKinsey 2025 Global Payments Report](https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report)
- Cross-border interlinking matures: BIS Project Nexus (Nexus Global Payments incorporated in Singapore, March 2025 by India, Malaysia, Philippines, Singapore, Thailand) standardises connection of domestic instant systems; the Eurosystem is exploring linking TIPS to Nexus — first wave reaches a 1.7bn-person market. [BIS — Project Nexus](https://www.bis.org/about/bisih/topics/fmis/nexus.htm); [MAS — Nexus blueprint completed](https://www.mas.gov.sg/news/media-releases/2024/project-nexus-completes-comprehensive-blueprint-for-connecting-domestic-ipses-globally)
- Digital euro extends instant into central-bank money: ECB closed its preparation phase Oct 2025, targets a 12-month pilot from H2 2027 and readiness for potential first issuance in 2029, contingent on EU legislation expected in 2026; ~EUR1.3bn development cost and ~EUR320m/yr operating cost from 2029. [ECB — Eurosystem moving to next phase of digital euro](https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr251030~8c5b5beef0.en.html); [ECB — preparation phase closing report](https://www.ecb.europa.eu/euro/digital_euro/progress/html/ecb.deprp202510.en.html)

## Numeric series (for charts)

| metric | year | value | source-url (+page) |
|---|---|---|---|
| SCT Inst share of total credit-transfer volume (SCT+SCT Inst), euro area | Q1 2024 | 17.34% | https://www.ecb.europa.eu/paym/groups/erpb/shared/pdf/23th-ERPB-meeting/Status_update_on_SCT_Inst_scheme_and_QR-code_standardisation.pdf (p.3) |
| SCT Inst share of total credit-transfer volume (SCT+SCT Inst), euro area | Q1 2025 | 24.74% | https://www.ecb.europa.eu/paym/groups/erpb/shared/pdf/23th-ERPB-meeting/Status_update_on_SCT_Inst_scheme_and_QR-code_standardisation.pdf (p.3) |
| Registered SCT Inst scheme participants (SEPA) | Jun 2025 | 2,765 (78% of SCT adherents; 91% in euro area) | https://www.ecb.europa.eu/paym/groups/erpb/shared/pdf/23th-ERPB-meeting/Status_update_on_SCT_Inst_scheme_and_QR-code_standardisation.pdf (p.2) |
| Global instant payments share of non-cash transaction volume | 2028 | 22% | https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf (p.1) |
| Global non-cash transaction volume | 2023 | 1,411 billion | https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf (p.1) |
| Global non-cash transaction volume | 2024 | 1,650 billion (forecast) | https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf (p.1) |
| Global non-cash transaction volume | 2028 | 2,838 billion (forecast) | https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf (p.1) |
| A2A potential offset of future card-volume growth | 2028 | 15-25% | https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf (p.1) |
| European banks with strong tech foundation for instant payments | 2024 | 13% | https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf (p.2) |
| EU instant-payment transactions (count) | ~2024 | ~3 billion | https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report |
| EU instant-payment transactions (count, forecast) | 2028 | ~30 billion (~50% CAGR) | https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report |
| Global real-time transactions (count, forecast) | 2028 | 575.1 billion (16.7% CAGR 2023-28) | https://www.aciworldwide.com/real-time-payments-report |
| Real-time payments share of all electronic payments globally | 2028 | 27.1% | https://www.aciworldwide.com/real-time-payments-report |
| Global instant-payments transaction value | 2024 | USD 22 trillion | https://www.juniperresearch.com/press/pressreleasesinstant-payment-transactions-to-surpass-58tn-globally/ |
| Global instant-payments transaction value (forecast) | 2028 | USD 58 trillion (+161% vs 2024) | https://www.juniperresearch.com/press/pressreleasesinstant-payment-transactions-to-surpass-58tn-globally/ |
| Global instant-payments transaction value (forecast) | 2029 | >USD 110 trillion (from ~USD 60tn in 2025) | https://www.juniperresearch.com/press/instant-payments-to-exceed-110-trillion-by-2029-globally-accelerated-by-european-regulation-fednow-impact/ |
| Global A2A transaction value (forecast) | 2030 | ~USD 195 trillion (+113% over 5 yrs) | https://www.openbankingexpo.com/news/juniper-research-global-a2a-transaction-value-to-hit-195tn-by-2030/ |
| Digital euro — potential first issuance | 2029 | target (pilot from H2 2027) | https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr251030~8c5b5beef0.en.html |

## Printec implication

This theme pulls demand hardest toward Printec's onboarding/compliance/security and payments-acceptance lines rather than toward cash hardware. Three concrete pulls:

1. Verification of Payee and fraud/identity tooling. VoP is now a standing legal obligation across the EU (euro area live; rest by Jul 2027) and Printec's 17 CEE/SEE countries include many non-euro markets approaching that 2027 cliff with low bank readiness. Printec's onboarding, identity, security and compliance/managed-services portfolio maps directly onto helping banks and PSPs deliver compliant VoP, real-time fraud screening and ISO 20022 structured-data handling — the maturing instant rails make these mandatory, recurring spend, not projects.

2. Payments / POS acceptance for A2A. If A2A offsets 15-25% of card-volume growth and Wero scales, merchants and acquirers in the footprint will need acceptance that handles instant A2A (request-to-pay, QR, wallet) alongside cards. This favours Printec's POS/payments and self-service acceptance lines and positions it to broker the card-to-A2A transition rather than be disintermediated by it.

3. Self-service and ATM relevance, reframed. Instant/A2A and the digital euro accelerate the decline of card-and-cash-only journeys, but also create new endpoints — cash-in/cash-out for digital euro, instant top-up, identity capture — that self-service and recycling hardware (with the NCR Atleos partnership) can host if upgraded for ISO 20022 / instant connectivity. The risk is to legacy cash volume; the hedge is repositioning the estate as multi-rail customer-interaction points.

Net: prioritise compliance/verification and A2A acceptance offerings now, since the regulatory deadlines (Oct 2025, Jul 2027) and the bank-readiness gap create an immediate, fundable demand window through 2027-2031.

Note: any VoP, instant-payments or ISO 20022 implementation guidance for clients touches PCI DSS, GDPR and DORA obligations and should be flagged for human/Compliance review before deployment.

## Sources

- ECB — Instant Payments Regulation overview · https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html
- ECB / EPC — Status update on SCT Inst scheme, June 2025 ERPB meeting (ERPB/2025/003) · https://www.ecb.europa.eu/paym/groups/erpb/shared/pdf/23th-ERPB-meeting/Status_update_on_SCT_Inst_scheme_and_QR-code_standardisation.pdf · p.2-3
- PwC Legal — Verification of Payee requirements (VoP) under the EU's IPR · https://legal.pwc.de/en/news/articles/verification-of-payee-requirements-vop-under-the-eus-instant-payments-regulation-ipr
- European Payments Council — VoP scheme rulebook now in force · https://www.europeanpaymentscouncil.eu/document-library/press-releases/verification-payee-scheme-rulebook-now-force
- Swift — ISO 20022 for financial institutions · https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions
- NICE Actimize — Preparing for the ISO 20022 November 2025 deadline · https://www.niceactimize.com/blog/aml-iso-20022-deadline
- Capgemini Research Institute — World Payments Report 2025 (press release) · https://www.capgemini.com/wp-content/uploads/2024/09/09_10_World-Payments-Report-2025-Press-Release-3.pdf · p.1-2
- Capgemini — World Payments Report 2025 (landing) · https://www.capgemini.com/insights/research-library/world-payments-report-2025/
- McKinsey — The 2025 McKinsey Global Payments Report: Competing systems, contested outcomes · https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report
- ACI Worldwide — Prime Time for Real-Time global payments report · https://www.aciworldwide.com/real-time-payments-report
- Juniper Research — Instant payment transactions to surpass $58tn globally by 2028 · https://www.juniperresearch.com/press/pressreleasesinstant-payment-transactions-to-surpass-58tn-globally/
- Juniper Research — Instant payments to exceed $110tn by 2029 globally · https://www.juniperresearch.com/press/instant-payments-to-exceed-110-trillion-by-2029-globally-accelerated-by-european-regulation-fednow-impact/
- Open Banking Expo / Juniper Research — Global A2A transaction value to hit $195tn by 2030 · https://www.openbankingexpo.com/news/juniper-research-global-a2a-transaction-value-to-hit-195tn-by-2030/
- BIS — Project Nexus: enabling instant cross-border payments · https://www.bis.org/about/bisih/topics/fmis/nexus.htm
- MAS — Project Nexus completes comprehensive blueprint for connecting domestic IPSes globally · https://www.mas.gov.sg/news/media-releases/2024/project-nexus-completes-comprehensive-blueprint-for-connecting-domestic-ipses-globally
- ECB — Eurosystem moving to next phase of digital euro project (30 Oct 2025) · https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr251030~8c5b5beef0.en.html
- ECB — Preparation phase of a digital euro, closing report (Oct 2025) · https://www.ecb.europa.eu/euro/digital_euro/progress/html/ecb.deprp202510.en.html

## SOURCE REQUESTS FOR OPERATOR

- McKinsey 2025 Global Payments Report — full PDF/report. URL: https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report . Holds: the underlying EU instant-payments 3bn→~30bn-by-2028 series, A2A/wallet share of global POS volume, and monetization/fee-model analysis (interchange compression). The web page gives headline figures only; the full chart pack would let us extract a clean year-by-year EU instant series for the dashboard.
- Capgemini World Payments Report 2025 — full report (gated download). URL: https://www.capgemini.com/insights/research-library/world-payments-report-2025/ . Holds: regional non-cash volume series and instant-payment readiness scoring by region/bank segment; useful to pull CEE/SEE-specific readiness if broken out.
- ACI Worldwide "Prime Time for Real-Time" 2024/2025 report — full PDF. URL: https://www.aciworldwide.com/real-time-payments-report . Holds: country-level real-time transaction volumes and CAGRs (including any CEE/SEE markets in Printec's footprint) and the 575.1bn-by-2028 / 27.1%-of-electronic-payments build-up.
- Juniper Research instant-payments & A2A market reports (2025-30). URL: https://www.juniperresearch.com/research/fintech-payments/emerging-payments/instant-payments-research-report/ . Holds: the full value series ($22tn 2024 → $58tn 2028 → >$110tn 2029) and the $91.5tn→$195tn A2A series with regional splits — paywalled beyond the press releases.
