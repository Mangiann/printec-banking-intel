# Oschadbank + Raiffeisen Bank Ukraine — 27/08/2026

**Slug:** `oschadbank-ua` · **Status:** complete · **Signals:** 14 · **Confidence:** Medium (2 rows Low)

## Headline

The sharpest thing in this window is not a bank disclosure at all — it is a **dated regulatory forcing event**. The NBU puts a **brand-new UAH 2,000 banknote into circulation on 04/09/2026** and opened consultation on the cash-operations rules on 26/08/2026 (comments close the same day the note ships). Every one of Ukraine's ~15,800 ATMs, every recycler and every branch cash-processing machine needs validator firmware, denomination templates, cassette configuration and re-certification. That is non-discretionary spend with a calendar date on it, in a market where bank profits just fell 32%.

Second theme: **both banks are shrinking physical presence while volume grows.** Raiffeisen Ukraine is at 256 outlets (from 298 eighteen months ago) serving 3.12m customers (+8.2% YoY). The national ATM estate is flat at 15.8k while POS acceptance points grew 13.9% in six months. Nobody is buying more ATMs; everybody needs the ones they have to cost less.

Third theme: **compliance and resilience are board-level in Ukraine right now.** The Sense Bank affair — an NBU inspection into whether an automated financial-monitoring system was *switched off* to let UAH 150m of bail through — will be asked of every bank board including state-owned Oschadbank. Meanwhile Oschadbank had three digital-channel disruption events in eleven weeks.

## Signal rows

| # | Entity | Signal (short) | Date | Tier | Printec hook | Size / Win |
|---|---|---|---|---|---|---|
| 1 | NBU (market frame) | ATM fleet flat at **15.8k** (+0.2% YTD); POS **582.5k** (+4.3%); acceptance points **699.3k** (+13.9%); cashless 96% by count / 67% by value; ~UAH 1.27tn still withdrawn as cash in H1 | 18/08/2026 | regulator | Recycler retrofit, ATM-as-a-service, managed services; softPOS on the acceptance side | L / Medium |
| 2 | NBU (binds all) | **UAH 2,000 banknote enters circulation 04/09/2026**; cash-ops rules consultation closes 04/09/2026 | 26/08/2026 | regulator | Validator firmware + template updates, cassette/denomination reconfiguration, re-certification at fleet scale | L / Medium |
| 3 | Oschadbank **and** Raiffeisen UA | Named 2 of 4 **authorised banks** for exchanging withdrawn 1/2/5/10 UAH notes **to 28/02/2029** (others only to 26/02/2027) | 02/03/2026 | regulator | Teller-assist recyclers, automated note/coin handling for a multi-year manual duty | M / Medium |
| 4 | **Oschadbank** | Assets **UAH 518.87bn**, 2nd of 59 banks; loans +6.7% to 136.83bn; but H1 net profit **UAH 3.38bn, down 2.9×**, fell 2nd→4th. Sector profit −32% | 14/08/2026 | press | Opex not capex: ATM-as-a-service, managed cash cycle, hosted compliance | XL / Medium |
| 5 | **Oschadbank** | **Outage 25/08/2026** — internal cybersecurity systems triggered; mobile app + legal-entity services down. Plus "major system updates" 11/06/2026 and interruption warning 29/06/2026 | 25/08/2026 | press | SLA-backed managed services, remote estate monitoring, self-service as independent fallback path | L / Medium |
| 6 | **Oschadbank** | Micro-business lending **+37% to UAH 3.3bn**, 2,596 loans from 2,799 applications; portfolio >UAH 7.6bn; 313 agri microloans under portfolio guarantees worth UAH 459.8m | 26/08/2026 | press | Digital onboarding/eKYC at volume, AML/sanctions screening at origination, guarantee reporting | M / Medium |
| 7 | **Oschadbank** | UAH 4.8bn dividends to state budget; joined **open banking ecosystem 05/08/2026** (with OTP, Sense) | 15/07 & 05/08/2026 | aggregator | ASPSP API security, strong customer authentication, HSM — *needs primary confirmation* | M / **Low** |
| 8 | NBU — open banking | Regime live under board resolutions **81 and 82 of 25/07/2025**; TPP register holds only **6 providers (3 PISP, 3 AISP)** | 25/07/2025 | regulator | Qualified open-banking certificates, SCA, HSM/security, API monitoring — build-out barely started | M / Medium |
| 9 | NBU — AI supervision | Discussion Document on ethical/responsible AI open for response; **Nov-2025 survey: 208 institutions, 64% use AI/ML, 23% actively**; no AI law yet; EU AI Act (2024/1689) as reference; White Paper next | Nov-2025 / live 27/08/2026 | regulator | Explainable, auditable AML / monitoring / fraud / eKYC decisioning with human-in-the-loop and appeal trail | M / Medium |
| 10 | NBU / Sense Bank (read-across) | NBU inspecting **interference with an automated financial-monitoring system** during UAH 150m bail; parties admit "switching off the bank's automated systems"; finmon director suspended, board chair dismissed | 21/08/2026 | press | AML/transaction monitoring sold on **tamper-evidence and audit integrity**, not detection rates | L / Medium |
| 11 | **Raiffeisen UA** | **256 business outlets** at 30/06/2026 (295 a year earlier, 298 at end-2024) while **customers +8.2% to 3.124m** and staff −6.3% to 4,814; loans +29.3%; PAT €70.3m | 31/07/2026 | **primary** | Recyclers/assisted service inside the remaining 256; eKYC; managed services for a thinner estate | L / Medium |
| 12 | **Raiffeisen UA** | Fee income −€10.7m partly from "lower earnings from clearing, settlement and payment services"; admin costs down on **"lower software depreciation"**; tax +€17.2m on a **50% bank tax rate** | 31/07/2026 | **primary** | Prior platform cycle running off → re-tender window; pitch opex model | M / **Low** |
| 13 | **Raiffeisen UA** | **67% of new FOP (entrepreneur) accounts opened online**; corporate Open APIs live (balance + ISO statement, OAuth2/JWT, sandbox/UAT/prod) | 27/08/2026 | **primary** | Sell the verification/compliance layer under an already-scaled digital channel | M / Medium |
| 14 | **Raiffeisen UA** | **Relocated Bohodukhiv branch** opened after the previous one was destroyed by shelling; RBI notes intensified attacks on energy infrastructure in winter 2025/26 | 21/08/2026 | **primary** | Rapidly deployable low-footprint self-service with power/connectivity autonomy; redeployment SLAs | M / Medium |

## What I could not get — real gaps, not quiet ground

- **EBRD guarantee — entirely unresearched.** `ebrd.com` is a JS SPA; search and project finder return an empty template to every fetch route, `api.ebrd.com` does not resolve. With no WebSearch available there was no way in. **Must be re-run.**
- **Power Banking — unresearched as a named programme.** No primary or press source surfaced through the entry points reachable without search. Only indirect resilience evidence (rows 5 and 14).
- **Core migration — no direct evidence** for either bank. Closest are RBI's "lower software depreciation" and Oschadbank's 11/06/2026 "major system updates" — both inferential.
- **Neither bank's own ATM count.** RBI does not publish ATMs by country; Oschadbank's site and locator are blocked. The 15,800 figure is the **national NBU total**, not a bank-level number — do not attribute it to either bank.

## Access log

- **`www.oschadbank.ua` — hard block, no first-party content retrieved.** Every URL returns HTTP 200 with a 212-byte Imperva/Incapsula stub. Tried: WebFetch (redirect loop), curl + desktop UA, curl + full desktop header set (Accept-Language uk-UA, sec-ch-ua, Sec-Fetch-*, compressed) with cookie jar and a second same-session request, apex host, `/sitemap.xml`, `/robots.txt`, `/atm-branches`. **Claude-in-Chrome escalation attempted and failed — extension not connected.**
- **`bank.gov.ua` — 403 to WebFetch, defeated by curl + desktop UA** (as the run instructions predicted). All NBU content came via that route. Its `/ua/search` returns 400, no working RSS, and news pagination is JS — so the NBU backlog beyond the front page could not be enumerated.
- **`raiffeisen.ua` — partial.** News list renders; **article bodies are client-rendered** (only title + meta description in server HTML; the only embedded JSON is schema.org org markup). `/uk/news`, `/en/about-bank/press-center`, `/en/atm-branches`, `/api/branches` all 404.
- **`forbes.ua/finance`** 404.
- **Session constraint:** WebSearch budget was already exhausted (200/200) before the first query for this bank. Everything above was obtained by direct fetching and local PDF/XLSM parsing.

## Operator requests

1. **Oschadbank site behind Imperva** — open `/news`, `/ua/news`, the investor/reporting section and the locator at `/ua/map` in a real browser. Capture ATM and branch counts, the H1-2026 interim report, any Power Banking or core-migration disclosure, and the 11/06/2026 "major system updates" release. *Biggest single gap.*
2. **EBRD Project Finder** — run "Oschadbank" and "Raiffeisen Bank Aval / Raiffeisen Bank Ukraine"; export PSDs for any 2025–26 guarantee, risk-sharing or portfolio-guarantee facility with amounts and board dates.
3. **NBU AI Discussion Document** — retrieve the PDF, publication date and response deadline from the supervision page.
4. **NBU draft resolution package** for the UAH 2,000 banknote cash-operations rules (draft, comparison table, impact analysis PDFs) — the handling/packaging specs matter for recycler and validator configuration.
5. **Power Banking** — locate the current NBU or Ukrainian Banking Association source: participant banks, number of Power Banking points, power-autonomy requirements.
6. **Raiffeisen article bodies** — capture full text of the 27/08/2026 FOP-online, 21/08/2026 Bohodukhiv and 11/08/2026 AI Focus 2026 items, plus the AI Focus 2026 study PDF.
