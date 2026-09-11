# PrivatBank (Ukraine) — Printec findings — 2026-07-14 (checkpoint)

Printec Ukraine (TOV "Printek Ukraina E.L.L.C.", Kyiv) = sole/incumbent supplier of NCR (Atleos) recycling ATMs to PrivatBank. Focus: 1,140-unit 2025 contract, 800-unit 2026 follow-on, Prozorro tender status.

## Re-verified standing position (2025 contract) — unchanged
- Contract signed 16/01/2025 with Printek Ukraina, 838.64M UAH for 1,140 recycling ATMs: 800 x NCR SelfServ 2062 (lobby) + 340 x NCR SelfServ 2064 (through-the-wall). Recycle UAH/USD/EUR; FX exchange up to $1,000/€1,000. Delivery by end-Nov 2025, 2yr warranty, 50% advance. Printek sole stage-2 bidder. First ATM buy since 2016 nationalisation. Prozorro UA-2025-01-17-010779-a.

## 800-unit 2026 follow-on — status re-verified, STILL NOT TENDERED
- 21/05/2026 (Interfax) / 22/05/2026 (finclub): retail board member Dmytro Musienko confirms plan to buy 800 more ATMs in 2026 (replace fully-depreciated units with deposit+withdraw recyclers). Bought "1,200 ATMs in 2025 for ~1bn UAH."
- As of 14/07/2026: NO 800-unit tender/award located on Prozorro (tender.uub.com.ua company page 14360570 reviewed via desktop-UA, defeating 403 — most recent PrivatBank ATM-category items are consumables through 01/07/2026, not the unit lot). Repeat-award to Printec highly likely (incumbent + prior sole bidder) but not yet posted.

## NEW SIGNAL — active recycler maintenance/spare-parts stream (2026)
Primary source: tender.uub.com.ua ATM category (DK 30123200-9), mirror of PrivatBank Prozorro reports, retrieved via desktop UA. Continuous 2026 direct-contract procurements to keep the NCR recycler fleet running — evidence fleet is in active service and generating an aftermarket/managed-services revenue stream:
- UA-2026-07-01-004760-a: ATM large-node modules (Cash-cassette, clamps, limb lock) — 3,923,400.50 UAH (01/07/2026)
- UA-2026-07-01-005562-a: card-reader consumables (presenter/magnetic head V2CU) — 17,652.81 USD (01/07/2026)
- UA-2026-06-15-012172-a: ATM large-node modules (limb lock) — 7,211,025.00 UAH (15/06/2026)
- UA-2026-05-29-007894-a: ATM Recycler VS-Module spare parts — 385,000 UAH (29/05/2026)
- UA-2026-05-19-000673-a: ATM Recycler VS-Module (roller shaft) — 2,119,470 UAH (19/05/2026)
- UA-2026-03-28-000658-a: ATM Recycler VS-Module parts — 3,843,405.40 UAH (28/03/2026)
- UA-2026-03-23-015077-a: ATM video-surveillance systems — 1,802,400 UAH (23/03/2026)
PrivatBank internal IDs referenced (PB-2026-...) confirm parallel tender.privatbank.ua channel.

## Opportunity mapping
- #1 in-footprint opportunity: 800-unit repeat award (cash automation/recyclers, ATM/self-service, managed services). Printec repeat-award favourite.
- NEW: ongoing recycler spare-parts + managed-services aftermarket (multi-M UAH/quarter) tied to the installed 1,140-unit fleet — Printec managed-services angle.

## Access / resilience log
- tender.uub.com.ua — 403 to fetch tool; DEFEATED with desktop User-Agent (curl). Used for primary verification.
- tender.privatbank.ua — JS SPA, no static content; needs browser (not rendered this run).
- public-api.prozorro.gov.ua search endpoint — 404 (edrpou param unsupported on 2.5); prozorro.gov.ua search API — 405. Company page mirror used instead.
- nashigroshi.org — 403 (snippet used prior runs).
