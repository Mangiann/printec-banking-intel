# Ukraine — Prozorro (prozorro.gov.ua + tender.privatbank.ua)

Run 2026-06-24. Focus: PrivatBank 800-ATM 2026 lot, Oschadbank, ATM/SST/IT lots + winners.

## Access situation this run
- Prozorro public-facing search API and UI = 404/JS-empty to WebFetch. Aggregators zakupivli.pro / tender.uub.com.ua / opendatabot / clarity-project tender lists = 403 or JS-rendered (only summary stats render server-side). gov.e-tender.ua and smarttender deep-links = 404/homepage-only.
- OpenProcurement open-data API (api.openprocurement.org/api/2.5/tenders) IS reachable but is an unindexed firehose (no buyer/text filter) — not usable for targeted lookup without notice IDs.
- Claude-in-Chrome NOT available this run (list_connected_browsers returned empty — no paired browser).
- Net effect: winners of specific Prozorro award IDs remain non-retrievable; relied on Ukrainian press (finclub, interfax, open4business, dev.ua) for primary corroboration.

## Key confirmed facts
- PrivatBank 800-ATM 2026 plan: STILL PRE-TENDER. Confirmed by Musienko (board member, retail) at 22/05/2026 press conference via finclub + open4business + interfax. Multifunction deposit/dispense units to replace fully-depreciated old ATMs. No budget, no vendor, NO Prozorro/tender.privatbank.ua hardware-purchase notice found as of 24/06/2026. Fleet: 7,401 ATMs + 9,867 SSTs + 1,053 branches (Q1 2026). 2025: bought 1,200 ATMs for ~1bn UAH.
- Printec INCUMBENCY (re-verified, finclub): contract signed 16/01/2025, 838.64M UAH, 1,140 NCR SelfServ (800x SelfServ 2062 @ EUR16,644; 340x SelfServ 2064 @ EUR17,569), UAH/USD/EUR recycler, 2yr warranty, delivery deadline 30/11/2025, 50% advance. Printec was SOLE 2nd-stage bidder. TOV "Printec Ukraina El.El.Si." (dir. Yuriy Eysmont).
- Oschadbank cash-bags tender UA-2026-05-12-011684-a: cash-packaging bags + safe-packet carriers + cassette trunk-bags, deadline 26/05/2026 -> now IN EVALUATION. Winner not retrievable (403). Oschadbank fleet ~2,790 ATMs (2023 figure), Way4 core.

## Signal rows — see structured output
