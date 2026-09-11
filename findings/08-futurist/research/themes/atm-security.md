# Physical & cyber ATM security — attack trends, IBNS/neutralisation, fraud

## Direction & summary (2027-2031)

The arc to 2031 is a **bifurcation**: the global ATM installed base slowly shrinks (toward ~2.9m machines by end-2028 per RBR/Datos), yet **value-at-risk per machine rises and attacker sophistication migrates up the stack** — so security spend per terminal grows even as terminal counts fall. Three vectors run on different clocks:

1. **Physical attacks (explosives / ram-rip-out) remain the dominant loss driver in Europe and are structurally persistent.** EAST data show physical-attack *incidents* climbing (3,728 in 2022 → 4,637 in 2023 → 5,953 in 2024) with explosive attacks generating the majority of losses (~61-71% of physical-attack losses). Cross-border, professionalised gangs (notably Netherlands/Utrecht-based crews hitting Germany, Switzerland, Austria, France with solid/aluminium-powder explosives) are the defining 2024-2026 pattern, and law-enforcement takedowns through 2025-2026 confirm an organised, mobile threat rather than opportunistic crime. Expect this to **persist and push hard into CEE/SEE** as Western-European deterrence (gas-suppression, IBNS mandates, dye-staining, faster police response) displaces attackers eastward.

2. **Logical / cyber attacks bifurcate by geography.** Jackpotting (Ploutus, black-box, XFS abuse) **surged in the US in 2025** (~700 incidents, ~USD 20m losses, ~1,900 cumulative since 2020) while **falling to near-zero in Europe** (EAST: 7 → 3 attacks 2023→2024, all black-box; confirmed malware attacks dropped from 3 to 0 H2-2024→H1-2025). The European decline reflects hardened endpoints (whitelisting, encryption, EDR); the US surge reflects soft targets (outdated software, weak remote access). Through 2027-2031 the cyber frontier shifts toward **network/host-based and remote logical attacks** rather than physical malware insertion — raising the premium on endpoint hardening and DORA-aligned operational resilience.

3. **Card fraud (skimming) keeps declining** structurally as EMV/contactless/cardless mature; offset by rising **terminal fraud** (card/cash trapping, transaction-reversal fraud, relay attacks) which doubled in 2024 — low-tech, high-volume, hard to eradicate.

**Pace & confidence:** High confidence on the physical-attack persistence and the US-vs-Europe cyber split (multiple independent law-enforcement + industry sources agree). Medium confidence on the eastward geographic displacement into Printec's footprint (directionally supported by gang mobility and the deterrence-displacement pattern, but no published CEE/SEE forecast series isolates this). Note: the strongest single dataset (EAST) is industry-association-sourced and covers ~19-20 jurisdictions, so absolute counts undercount the true European total.

## Key drivers

- **Cross-border, professionalised explosive-attack gangs are the structural physical threat** — coordinated EU takedowns through 2025-2026 (18+ arrests of a Netherlands-based crew; further arrests in Austria, Germany, Switzerland) show organised groups using solid/aluminium-powder explosives across multiple countries, not isolated crime ([Europol — four arrests, solid explosives Germany/Austria](https://www.europol.europa.eu/media-press/newsroom/news/four-suspected-atm-attackers-arrested-in-coordinated-takedown), [Eurojust — nine arrests, ATM bombings across Europe](https://www.eurojust.europa.eu/news/nine-arrests-connected-atm-bombings-across-europe)).
- **Germany is the bellwether and shows defence is failing at scale** — ~461 attacks in 2023 (2nd-highest since 2005); banks spent >€300m on security yet ~60% of attacks still succeeded as of 2024, evidencing that hardening alone is insufficient and pushing demand toward neutralisation ([CNN — criminals looting millions, Germany prime target](https://www.cnn.com/2024/10/27/europe/criminals-atm-robberies-europe-intl)).
- **Explosive attacks dominate losses even when incident counts dip** — EAST 2024: 71% of ATM physical-attack losses were from explosive attacks; ~"two ATMs blown up every day" across tracked jurisdictions ([EAST — terminal fraud attacks double](https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/) via [ATM Marketplace](https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/)).
- **Collateral cost per explosive attack dwarfs the cash stolen** — vendor estimate: ATM destruction $200k-$350k plus up to ~$1m surrounding-property damage; hook-and-chain rip-outs ~€110k-€180k per incident in under two minutes ([Diebold Nixdorf — protecting the self-service channel](https://www.dieboldnixdorf.com/en-us/banking/insights/blog/protecting-your-self-service-channel-from-physical-attacks/)).
- **Jackpotting / logical attacks surging in the US, collapsing in Europe** — FBI/IC3: ~700 incidents and ~USD 20m losses in 2025, ~1,900 since 2020, Ploutus the dominant family exploiting XFS ([FBI via SecurityWeek](https://www.securityweek.com/fbi-20-million-losses-caused-by-700-atm-jackpotting-attacks-in-2025/), [The Record](https://therecord.media/fbi-atm-jackpotting-2025-report), [FBI IC3 FLASH 20260219-001](https://www.ic3.gov/CSA/2026/260219.pdf)); Europe near-zero malware attacks ([Finextra — ATM malware/logical attacks fall in Europe](https://www.finextra.com/pressarticle/80191/atm-malware-and-logical-attacks-fall-in-europe)).
- **XFS abuse is the durable cyber attack surface** — the CEN/XFS API that mediates ATM software-to-hardware lets attackers bypass bank authorisation and dispense cash directly; defence is migrating to ATM-specific EDR, behavioural XFS-manipulation detection, air-gapped management networks and certificate-based comms ([SISA — Ploutus surge 2026](https://sisa.ai/resource/blog/atm-jackpotting-ploutus-malware-surge-in-2026), [Illumant — financial-sector threats 2026](https://www.illumant.com/blog/2026/03/10/financial-sector-threats-atm-malware-beyond-why-banking-security-must-evolve-in-2026/)).
- **Terminal fraud (non-physical, non-malware) doubled in 2024** — card trapping +66%, cash trapping +105%, transaction-reversal fraud +367%, relay attacks +505% — low-tech, high-volume, persistent ([ATM Marketplace / EAST 2024](https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/)).
- **IBNS / cash-degradation neutralisation is the regulatory and operational answer to physical attacks** — already mandatory for CIT in Sweden, Belgium and increasingly for ATMs in France; ECB has had a euro-banknote neutralisation framework since 2003; a 2025 multinational study (18 labs, 13 countries) flags the need for harmonised forensic standards — i.e. the technology scales further this decade ([Wikipedia — IBNS](https://en.wikipedia.org/wiki/Intelligent_banknote_neutralisation_system), [ScienceDirect 2025 — harmonising IBNS staining-ink tracing](https://www.sciencedirect.com/science/article/abs/pii/S0379073825004013), [Mactwin — irreversible cash degradation](https://mactwincashsecurity.com/our-vision-on-cash-security/irreversible-cash-degradation/)).
- **Declining global ATM base concentrates value and raises per-terminal stakes** — RBR/Datos forecasts global ATM numbers falling to ~2.9m by end-2028 (from ~3.0m), with developed-market decline offset by MEA growth; fewer, higher-value machines justify more security per unit ([Datos/RBR Global ATM Intelligence Service](https://datos-insights.com/what-we-offer/rbr-data-services/banking-automation/global-atm-intelligence-service/), [ATM Marketplace — slow decline through 2024](https://www.atmmarketplace.com/news/number-of-atms-worldwide-set-for-a-slow-decline-through-2024/)).
- **Cash stays relevant in Europe, sustaining the attack surface** — ECB SPACE 2024: cash still used in ~50% of euro-area POS transactions and remains the most-used method; 62% of consumers consider cash access vital (up from 60% in 2022) — meaning ATMs (and their attractiveness to attackers) do not disappear within the horizon ([ECB SPACE 2024](https://www.ecb.europa.eu/stats/ecb_surveys/space/html/ecb.space2024~19d46f0f17.en.html)).
- **Skimming structurally fades; biometrics/cardless rise** — EMV/contactless erodes skimming (still ~77% of *card-fraud* cases but a shrinking absolute base); biometric verification forecast to become standard on cardless ATMs by ~2029, shifting fraud away from the card and toward host/credential channels ([coinlaw — ATM statistics 2025](https://coinlaw.io/atm-statistics/)).

## Numeric series (for charts)

| metric | year | value | source (+page) |
|---|---|---|---|
| ATM-related physical attacks (incidents, EAST jurisdictions) | 2019 | 4,571 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| ATM-related physical attacks (incidents) | 2022 | 3,728 | https://www.atmmarketplace.com/news/east-records-drop-in-atm-card-fraud-increase-in-explosive-attacks/ |
| ATM-related physical attacks (incidents) | 2023 | 4,637 | https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ |
| ATM-related physical attacks (incidents) | 2024 | 5,953 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| ATM explosive attacks (incidents) | 2019 | 977 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| ATM explosive attacks (incidents) | 2022 | 727 | https://www.atmmarketplace.com/news/east-records-drop-in-atm-card-fraud-increase-in-explosive-attacks/ |
| ATM explosive attacks (incidents) | 2023 | 714 | https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ |
| ATM explosive attacks (incidents) | 2024 | 602 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| ATM physical-attack losses (EUR m) | 2023 | 9 | https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ |
| ATM physical-attack losses (EUR m) | 2024 | 12 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| Explosive-attack losses (EUR m) | 2023 | 5.36 | https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ |
| Explosive-attack losses (EUR m) | 2024 | 8.56 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| Total ATM-fraud losses, all types (EUR m) | 2022 | 200 | https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ |
| Total ATM-fraud losses, all types (EUR m) | 2023 | 173 | https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ |
| Total ATM-fraud losses, all types (EUR m) | 2024 | 71 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| ATM malware/logical attacks (incidents, EAST) | 2023 | 7 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| ATM malware/logical attacks (incidents, EAST) | 2024 | 3 | https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ |
| Card-trapping attacks (incidents, EAST) | 2023 | 1,630 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Card-trapping attacks (incidents, EAST) | 2024 | 2,704 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Cash-trapping attacks (incidents, EAST) | 2023 | 4,795 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Cash-trapping attacks (incidents, EAST) | 2024 | 9,811 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Transaction-reversal-fraud attacks (incidents, EAST) | 2023 | 338 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Transaction-reversal-fraud attacks (incidents, EAST) | 2024 | 1,577 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Relay attacks (incidents, EAST) | 2023 | 63 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| Relay attacks (incidents, EAST) | 2024 | 381 | https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ |
| US ATM jackpotting incidents | 2025 | 700 | https://www.securityweek.com/fbi-20-million-losses-caused-by-700-atm-jackpotting-attacks-in-2025/ |
| US ATM jackpotting losses (USD m) | 2025 | 20 | https://www.securityweek.com/fbi-20-million-losses-caused-by-700-atm-jackpotting-attacks-in-2025/ |
| US ATM jackpotting incidents (cumulative since 2020) | 2025 | ~1,900 | https://www.securityweek.com/fbi-20-million-losses-caused-by-700-atm-jackpotting-attacks-in-2025/ |
| Germany ATM explosive robberies | 2023 | 461 | https://www.cnn.com/2024/10/27/europe/criminals-atm-robberies-europe-intl |
| Global ATM installed base (m, forecast) | 2028 | ~2.9 | https://www.atmmarketplace.com/news/number-of-atms-worldwide-set-for-a-slow-decline-through-2024/ |
| Euro-area POS transactions paid in cash (%) | 2024 | ~50 | https://www.ecb.europa.eu/stats/ecb_surveys/space/html/ecb.space2024~19d46f0f17.en.html |
| Euro-area consumers rating cash access as vital (%) | 2022 | 60 | https://www.ecb.europa.eu/stats/ecb_surveys/space/html/ecb.space2024~19d46f0f17.en.html |
| Euro-area consumers rating cash access as vital (%) | 2024 | 62 | https://www.ecb.europa.eu/stats/ecb_surveys/space/html/ecb.space2024~19d46f0f17.en.html |

*Note: EAST counts cover ~19-20 reporting jurisdictions and are association-collected, so they undercount the full European total; treat as a consistent index/trend rather than an absolute census. 2024 "total losses €71m down 59%" reflects a large drop in card-fraud-related losses, not a fall in physical/explosive losses, which rose.*

## Printec implication

This theme pulls demand toward Printec's **physical ATM security and cash-protection stack** plus its **managed-services + compliance** layer — the most defensible, recurring-revenue parts of the portfolio in a shrinking-fleet world:

- **Cash neutralisation / IBNS and anti-explosive hardening** become the lead growth product. Germany's "€300m spent, 60% still succeed" reality proves passive armour is insufficient; the market is moving to **degrade the reward** (ink/dye staining, glue/cash-degradation, gas-suppression detection). As Western Europe hardens and gangs displace eastward into Printec's CEE/SEE footprint, demand for neutralisation retrofits on the installed NCR Atleos base should rise materially through 2027-2031. This is the single clearest pull.
- **ATM endpoint security & DORA-aligned managed services.** Europe's near-zero malware count is *earned* through hardening (whitelisting, encryption, EDR, secured remote access). Printec can productise "keep it at zero" — ATM-specific EDR, XFS-integrity monitoring, patch/lifecycle management — as a recurring managed-security service, directly mapped to DORA operational-resilience obligations its banking clients face.
- **Anti-terminal-fraud sensing** (anti-card-trap, anti-cash-trap, TRF/relay detection) — the 2024 doubling makes detection kits and software updates a steady attach-sale on the self-service fleet.
- **Strategic framing for the C-suite:** fewer ATMs but higher value-at-risk per unit = rising security spend per terminal. Printec's recurring **security + monitoring + compliance** revenue is structurally more resilient than hardware refresh as the fleet contracts. Flag: any production/security/payment-related deployment here requires human review and testing before go-live, and any deployment touching cardholder data must remain PCI DSS-aligned.

## Sources

- EAST — European Terminal Fraud attacks double (2024 report) · https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ · web page
- EAST — ATM Physical Attacks rise in Europe (2023 report) · https://www.association-secure-transactions.eu/atm-physical-attacks-rise-in-europe/ · web page
- EAST — ATM explosive attack criminals arrested in coordinated police action · https://www.association-secure-transactions.eu/atm-explosive-attack-criminals-arrested-in-coordinated-police-action/ · web page
- ATM Marketplace — Terminal fraud attacks increasing in Europe (carries EAST 2024 figures) · https://www.atmmarketplace.com/news/terminal-fraud-attacks-increasing-in-europe/ · web page
- ATM Marketplace — EAST records drop in card fraud, increase in explosive attacks (2022 figures) · https://www.atmmarketplace.com/news/east-records-drop-in-atm-card-fraud-increase-in-explosive-attacks/ · web page
- ATM Marketplace — Number of ATMs worldwide set for slow decline through 2024 (RBR forecast) · https://www.atmmarketplace.com/news/number-of-atms-worldwide-set-for-a-slow-decline-through-2024/ · web page
- Datos Insights / RBR — Global ATM Intelligence Service (end-2024 status, 2030 forecast) · https://datos-insights.com/what-we-offer/rbr-data-services/banking-automation/global-atm-intelligence-service/ · web page
- Europol — Four suspected ATM attackers arrested, solid explosives Germany/Austria · https://www.europol.europa.eu/media-press/newsroom/news/four-suspected-atm-attackers-arrested-in-coordinated-takedown · web page
- Eurojust — Nine arrests connected to ATM bombings across Europe · https://www.eurojust.europa.eu/news/nine-arrests-connected-atm-bombings-across-europe · web page
- CNN — Criminals looting millions from ATMs in Europe; Germany prime target · https://www.cnn.com/2024/10/27/europe/criminals-atm-robberies-europe-intl · web page
- Diebold Nixdorf — Protecting your self-service channel from physical attacks · https://www.dieboldnixdorf.com/en-us/banking/insights/blog/protecting-your-self-service-channel-from-physical-attacks/ · web page
- FBI / IC3 — FLASH 20260219-001, increase in malware-enabled ATM jackpotting · https://www.ic3.gov/CSA/2026/260219.pdf · PDF (binary, not text-extractable via fetch)
- SecurityWeek — FBI: $20M losses from 700 ATM jackpotting attacks in 2025 · https://www.securityweek.com/fbi-20-million-losses-caused-by-700-atm-jackpotting-attacks-in-2025/ · web page
- The Record (Recorded Future) — FBI ATM jackpotting 2025 report · https://therecord.media/fbi-atm-jackpotting-2025-report · web page
- Finextra — ATM malware and logical attacks fall in Europe · https://www.finextra.com/pressarticle/80191/atm-malware-and-logical-attacks-fall-in-europe · web page
- SISA — ATM jackpotting: Ploutus malware surge in 2026 · https://sisa.ai/resource/blog/atm-jackpotting-ploutus-malware-surge-in-2026 · web page
- Illumant — Financial-sector threats: ATM malware & beyond, why banking security must evolve in 2026 · https://www.illumant.com/blog/2026/03/10/financial-sector-threats-atm-malware-beyond-why-banking-security-must-evolve-in-2026/ · web page
- Wikipedia — Intelligent banknote neutralisation system (regulatory/mandate history) · https://en.wikipedia.org/wiki/Intelligent_banknote_neutralisation_system · web page
- ScienceDirect — Towards harmonised practices in tracing staining inks from activated IBNS (2025 multinational survey) · https://www.sciencedirect.com/science/article/abs/pii/S0379073825004013 · journal abstract
- Mactwin Cash Security — Irreversible cash degradation · https://mactwincashsecurity.com/our-vision-on-cash-security/irreversible-cash-degradation/ · web page
- ECB — SPACE 2024 (payment attitudes of euro-area consumers) · https://www.ecb.europa.eu/stats/ecb_surveys/space/html/ecb.space2024~19d46f0f17.en.html · web page
- coinlaw — ATM statistics 2025 (skimming share, biometric/cardless outlook) · https://coinlaw.io/atm-statistics/ · web page

## SOURCE REQUESTS FOR OPERATOR

- **EAST European Payment Terminal Crime Report (full 2024 + 2023 editions)** — https://www.association-secure-transactions.eu/european-terminal-fraud-attacks-double/ — the EAST site returns HTTP 403 to automated fetches; figures above were triangulated via ATM Marketplace and the EAST press summaries. The full member report holds the country-level breakdowns (incl. CEE/SEE jurisdictions) and the complete loss-by-attack-type tables needed to isolate Printec's footprint. Worth retrieving directly (member access or via Printec's EAST contact).
- **RBR / Datos Insights Global ATM Intelligence Service & "Global ATM Market and Forecasts"** — https://datos-insights.com/what-we-offer/rbr-data-services/banking-automation/global-atm-intelligence-service/ — paid subscription. Holds the authoritative installed-base series by country to 2030 and the per-region growth/decline split (key for sizing the shrinking-fleet-but-rising-security-spend thesis in Printec's 17 markets).
- **FBI/IC3 FLASH 20260219-001 (PDF)** — https://www.ic3.gov/CSA/2026/260219.pdf — the PDF downloaded but was not text-extractable via automated fetch (binary saved locally). Open manually to confirm the exact 2025 incident/loss figures and the full year-by-year and defensive-recommendation detail.
- **Grand View Research — Global ATM Market (to 2030, ~3.6% CAGR, ~USD 31.64bn by 2030)** — https://www.grandviewresearch.com/press-release/global-atm-market — returned 403; the press release headline figure (USD 31.64bn by 2030, 3.6% CAGR) is citable from the search snippet but the segment/region detail behind the paywall would strengthen the market-sizing.
