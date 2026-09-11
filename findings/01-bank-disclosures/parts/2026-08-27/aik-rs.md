# AikBank / AikGroup — 27/08/2026

**Slug:** `aik-rs` · **Status:** complete · **Signals:** 12

## Headline

Three things moved since the 30/07/2026 baseline.

**1. A competitor is already inside the estate.** AikBank's own August branch-renovation notices tell customers to use **"MoneyGet isplatni bankomati"** when the in-branch ATM is down. MoneyGet Serbia is operated by **Payten d.o.o.**, the payments arm of **Asseco South Eastern Europe** — a direct Printec competitor — and its Serbian locator lists **200 ATM locations**. MoneyGet also runs in **Croatia, Montenegro and Albania**, i.e. three of AikGroup's four markets. This is the single most commercially important discovery this run and does not appear in the baseline at all. It also explains the FY2025 Note-30 collapse in ATM-site right-of-use assets (RSD 47.3m → 13.3m): AikBank did not just cull off-premise ATMs, it substituted an Asseco-operated network.

**2. The group fleet is now reconciled from three independent operator sources.** Serbia **570** ATMs (AikBank feed), Montenegro **49** (Hipotekarna AJAX locator, newly opened), Slovenia **64** standalone ATM sites (Gorenjska `branch-sitemap.xml`) → **~683 ATMs across three markets**, Croatia still pending. The Montenegro count also settles the baseline's unresolved 47-vs-56 discrepancy in AikBank's own marketing.

**3. Deposit-automation demand is measurably rising while AikBank's estate stays 80% cash-out-only.** NBS data updated **19/08/2026** puts Serbia at **3,412 ATMs / 195,121 POS at 30/06/2026** (from 3,336 / 187,957 at Q1) and shows **ATM cash-in transactions up 6.4% q/q by count and 14.7% by value**. AikBank meanwhile converted just **+2 multifunction ATMs and +4 ATS** in four weeks — a ~6 device/month drip against a 457-machine backlog.

Croatia (Podravska banka) is **still not closed** — verified at the Zagreb Stock Exchange, where nothing has been filed since the voting-rights notice of 11/06/2026.

## Signals

| # | Entity | Signal | Date | New |
|---|--------|--------|------|-----|
| 1 | AikBank | Locator re-pull: 570 ATMs (457 dispense-only, 113 multifunction), 63 ATS, 113 branches | 27/08/2026 | yes |
| 2 | AikBank / MoneyGet | Renovation notices refer customers to MoneyGet IAD ATMs | 26/08/2026 | yes |
| 3 | Payten / Asseco SEE | MoneyGet = Payten d.o.o. (Asseco SEE); 200 ATM sites in Serbia; also HR/ME/AL | 27/08/2026 | yes |
| 4 | AikBank | Four new branch-renovation notices in August, works dated to 07/10/2026 | 26/08/2026 | yes |
| 5 | AikBank | EBRD EUR 30m factoring line, first in RSD; new digital factoring platform | 04/08/2026 | yes |
| 6 | M&V / Banking Group | FY2025 consolidated accounts; perimeter is domestic-only, not AikGroup | 20/05/2026 | yes |
| 7 | NBS | Serbia 3,412 ATMs / 195,121 POS / 6,278 virtual POS at 30/06/2026 | 19/08/2026 | yes |
| 8 | NBS | ATM cash-in Q2-2026: 3.41m txns / RSD 173.9bn; +14.7% q/q by value | 19/08/2026 | yes |
| 9 | Podravska banka | Still unclosed; nothing filed at ZSE since 11/06/2026; Q2 report 28/07/2026 | 27/08/2026 | yes |
| 10 | Hipotekarna banka | Locator API opened: 49 ATM + 24 branch records; settles 47-vs-56 | 27/08/2026 | yes |
| 11 | Gorenjska banka | 64 standalone ATM sites + 18 branches from branch sitemap | 27/08/2026 | yes |
| 12 | NBS (regulation) | Video-ID decision 43/2026: 6-month conduct and 12-month technical deadlines | 07/05/2026 | yes |

## Access notes

WebSearch budget was exhausted (200/200) before any AikBank query ran — **all** of this is direct primary-source fetching. Two JS/403 escalations succeeded and are worth reusing:

- **Hipotekarna banka** locator is JS-rendered; the underlying endpoint is `POST /wp-admin/admin-ajax.php` with `action=hb_business_locations_list`, found by reading `wp-content/plugins/hbforms1.11.2/business-locations/locations.js`. Returns clean JSON. **Closes a standing operator request for Montenegro.**
- **aikbank.rs PDFs are served gzip-encoded** and must be gunzipped before pdfminer will parse them (they sniff as `gzip compressed data`, not PDF).
- ZSE EHO issuer search works unauthenticated at `/obavijesti-izdavatelja/search` with `tx_issuerpublicationmanager_publicnewslisting[query]` + `[filter]=ticker`.
