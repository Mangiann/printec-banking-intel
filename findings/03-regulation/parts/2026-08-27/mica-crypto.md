# Agent 3 - Regulation & Deadlines - MiCA / crypto-asset rules
Run date 27/08/2026 | slug `mica-crypto` | status COMPLETE | 15 signals

## Headline
The single hardest fact of this workstream is that the **MiCA transitional period ended EU-wide on 1 July 2026**. ESMA's Public Statement ESMA75-113276571-1710 of 23/06/2026 turned that date into an operational wind-down mandate with full AML/CFT obligations preserved *through* the exit. Across the ten EU footprint markets the licensing outcome is a near-total cull: **Czechia 251 applications -> 11 licences; Slovenia 35 domestic providers -> 3; Bulgaria 8 applications -> 2 licences (4 refused); Croatia 5; Slovakia 6; Greece 2; Hungary 1; Austria a handful**. EU-wide only **312** entities hold a CASP permission (NBS-SK, 29/07/2026).

Two consequences drive Printec demand:
1. **The volume route for banks is MiCA Art.60 notification, not Art.63 licensing.** HANFA, CySEC and CNB all run a separate Art.60 register. An Art.60(7) notification requires a programme of operations, internal control mechanisms, asset segregation, custody, AML and ICT evidence - a direct map onto IMTF Siron / FICO (AML-KYC), INETCO (transaction monitoring), Namirial (eKYC onboarding) and Thales HSM/PCI (custody key protection).
2. **Client-book migration.** Unauthorised CASPs must move clients to authorised ones, and the receiving CASP must run full CDD onboarding on every transferred client. That is a bulk eKYC + AML event happening now.

## Open deadline
- **30/09/2026 23:59 CEST** - European Commission targeted consultation on the MiCA review closes (published 20/05/2026 under MiCA Arts.140 & 142; extended from 31/08/2026 on 29/06/2026). Live topics include third-country multi-issuance / fungibility of stablecoins (ESRB Recommendation ESRB/2025/9).

## Market-by-market
| Market | Status | Note |
|---|---|---|
| CZ | 11 licences / 251 applications | Highest application volume in the EU; CNB failing applicants on governance/AML/ICT |
| SK | 6 licences | MiCA applicable in SK since 30/12/2025, ahead of the EU date |
| HR | 5 (4 registered) | Art.60 notification route open to banks via HANFA/HNB |
| SI | 3 domestic of 35 | ATVP; site Cloudflare-blocked |
| BG | 2 (Alaric Securities, Belayer); 4 of 8 refused | BNB supervises EMT issuers, not FSC |
| GR | 2, first ever on 22/07/2026 | One is a **custodian** - HSM relevance |
| HU | 1 (Tiwala/CoinCash, 20/07/2026) | MiCA mandatory in HU since 01/07/2025 |
| CY | Art.63 + Art.60 registers | National-regime filing gate was 27/02/2026 |
| AT | RBI is a Qivalis founding shareholder | FMA licensing live |
| **RO** | **NO competent authority designated** | EC infringement; Parliament back 01/09/2026 |
| RS | Law on Digital Assets 153/2020; banks still barred from crypto | MiCA gap analysis done, no amendment timetable |
| UA | Draft law 10225-d, MiCA-based, awaiting 2nd reading | Would let banks work with virtual assets |
| MK / ME | Licensing regimes signalled for 2026, MiCA-aligned | Not yet adopted |
| BA / XK | No 2026 development surfaced | Genuine gap |

## Bank-issued token
**Qivalis** (Amsterdam JV) has applied to De Nederlandsche Bank for an **electronic money institution licence** to issue a euro EMT. **Raiffeisen Bank International (AT) is a named founding shareholder**; the consortium has grown to 37 banks in 15 countries. Launch targeted H2 2026, conditional on the licence. Fireblocks supplies tokenisation/wallet/custody. Note MiCA's EMT reserve rule - at least 30% of reserves in deposits with separate credit institutions - makes footprint banks candidate reserve-deposit takers.

## Access issues
- `cysec.gov.cy/en-GB/entities/crypto-asset-services-providers-casps/` -> HTTP 410 Gone
- `atvp.si` -> HTTP 403 to the fetch tool AND to a desktop-User-Agent curl (Cloudflare JS interstitial)
- `delo.si` article -> 302 to napaka.delo.si
- `theblock.co` -> self-signed certificate error
