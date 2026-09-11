# CrediaBank (ex-Attica Bank) — Greece — run 27/08/2026

**Status: complete.** Primary-source run built on the H1-2026 results presentation (06/08/2026), the Company Information Memorandum dated 30/03/2026 (a ~1.4m-character disclosure document, by far the richest source on this bank), the 30/12/2025 Euronet announcement, two New Experience branch press releases, and a live pull of the bank's own branch/ATM locator on 27/08/2026.

## The headline for Printec

Two things move in opposite directions this run.

**Against us — Greece.** CrediaBank is contractually exiting ATM and acquiring ownership. The Euronet Collaboration Agreements include a *"Master Services Agreement for ATMs and Recyclers"* making Euronet Card Services the **exclusive** provider of ATM-related technical services to CrediaBank and its affiliates in Greece. All 141 ATMs (80 on-site, 61 off-site at 31/12/2025) transfer to Euronet Card Services. Long-stop date **30/09/2026**; card-services full integration expected from **October 2026**. The Greek ATM/acquiring buying centre for this bank moves to Euronet/epay.

**For us — branches, compliance, Malta.** The "New Experience" branch model is explicitly cash-automation-led (TCRs replacing the teller counter, VTS/virtual teller stations, card-based entry recognition). 24 branches are committed for rebranding by end-2026 (8 done, 6 by early Q4, 10 by year-end), and the CIM states the intent to remodel the **entire** 66-branch network over two years with TCRs as a standard feature. Separately, a **>EUR 60m 2026-2028 Digital Transformation Program** with an 80+ person tech team explicitly names regulatory, compliance, cybersecurity and risk systems, digital onboarding and core-banking modernisation. And the HSBC Malta closing has **slipped to Q2 2027** — an 18-month runway to position for the carve-out of a 12-branch, 63-ATM, ~923-FTE bank off HSBC's group platforms.

## What changed since the 30/07/2026 baseline

- HSBC Malta expected closing moved from "end-2026 / early-2027" to **Q2 2027** (bank's own slide, 06/08/2026; confirmed on the record by HSBC Malta's CEO 05/08/2026).
- Branch rebranding is now quantified and dated: 24 by end-2026, 8 already done.
- Euronet deal terms are now visible at contract level (exclusivity clauses, 30/09/2026 long-stop, Oct-2026 card integration) via the March-2026 CIM — not previously in scope.
- Two further M&A closings dated Q4 2026: Pantelakis Securities (70%) and Evropi Holdings (bancassurance, EUR 260m share swap, signed 21/05/2026).
- Locator pull 27/08/2026: 64 branch sites and 56 off-site ATM locations — the off-site ATM count is down from 61 at 31/12/2025.

## Signals

See `crediabank-gr.json` for the structured rows (11 signals).

## Access notes

- The H1-2026 results PDF returns as binary to the fetch tool; extracted locally with pdfminer. Same for the CIM (4.7MB) and the branch press releases.
- `crediabank.com/en/group/press-office/` and the Greek `/omilos/grafeio-typou/` listing are JS-rendered and expose no JSON API; the sitemap.xml omits the press office entirely. Individual press releases were reached via site-scoped search plus a browser-UA curl to harvest the `/media/<hash>/*.pdf` link. No source was dropped.
- `ir.euronetworldwide.com` timed out to WebFetch twice; retrieved successfully with a desktop-browser User-Agent via curl.
