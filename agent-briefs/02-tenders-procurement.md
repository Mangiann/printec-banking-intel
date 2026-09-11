# Agent 2 — Tenders & Procurement

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.


**Mission:** Find public tenders and procurement notices showing banks (and state institutions) buying technology Printec sells.

> **SCOPE (2026-09-02): Austria is OUT of the footprint.** Do not work `ausschreibungen.usp.gv.at`, do not
> open Austrian buyers (OeNB, GSA, Münze Österreich), and do not raise Austria-scoped opportunities. Austrian
> *suppliers* still matter when they bid in the 16 markets — attribute the signal to the market where the
> contract is. Entries about Austria below this line are the historical run log, kept as record, not a work-list.

**Read first:** `research-playbook.md`. Then your latest file in `findings/02-tenders/`. Then check `knowledge-base/by-agent/agent-2-tenders/` and `knowledge-base/_reference/` for internal documents (digested nightly from `Data dump/`) — additional input to fold in alongside your full web research, never a reason to search less or to bias your findings toward them.

## Sources

- **TED** (ted.europa.eu) — EU-wide, covers all EU footprint countries. CPV codes: 30123000 (office/business machines incl. ATMs), 30144400 (automatic fare/payment), 48000000 (software), 72000000 (IT services), 3512x (surveillance/security), 66000000 (financial services).
- **Greece:** Diavgeia (diavgeia.gov.gr), ΚΗΜΔΗΣ/ESIDIS (eprocurement.gov.gr) — search Greek terms.
- **Romania:** SEAP/SICAP (e-licitatie.ro).
- **Serbia:** Portal javnih nabavki (jnportal.ujn.gov.rs).
- **Bulgaria:** CAIS EOP (app.eop.bg).
- **Others:** Croatia EOJN, Slovenia enarocanje.si, Czechia nen.nipez.cz, Slovakia uvo.gov.sk, Hungary ekr.gov.hu, Ukraine Prozorro (prozorro.gov.ua), Bosnia ejn.gov.ba, N. Macedonia e-nabavki.gov.mk, Albania app.gov.al, Kosovo e-prokurimi.rks-gov.net, Montenegro cejn.gov.me, Cyprus eprocurement.gov.cy.
- State-owned banks and post offices (CEC Romania, Oschadbank, Hrvatska pošta, ELTA) tender publicly — high-value targets.
- **Scripted Tier-0 caches (read these FIRST — they close the TED + Ukraine + Greece blind spots deterministically):** `intel-cache/ted_notices.json` (EU-wide TED notices: id, buyer, country, CPV, deadline, value, winner, EN PDF link — from `scripts/fetch_ted.py`, TED Search API v3 POST), `intel-cache/prozorro_notices.json` (PrivatBank/Oschadbank ATM-cash tenders + other UA buyers, with status & tender links — from `scripts/fetch_prozorro.py`, Prozorro search API POST), and **`intel-cache/greek_tenders_diavgeia.json`** (Greek **below-TED-threshold** ΚΗΜΔΗΣ/Diavgeia decisions for ATM / cash-automation / POS / self-service — `ada`, `subject`, buyer `org`, `date`, `doc_url` — from `scripts/fetch_diavgeia.py`, Diavgeia OpenData `search.json?subject=` [the PROVEN filter param; `q`/`query` are decoration], **no auth, no Chrome** — this **closes the Greek Diavgeia/ΚΗΜΔΗΣ "needs-Chrome" gap noted in the run-log below**; terms live in `references/diavgeia_config.json`). All three are refreshed by `run_weekly` and by your SKILL step 4. Fold them into the TED, Ukraine and **Greece** units and verify each (the TED `…/notice/<id>/pdf` route reads in full; the Prozorro `link` shows the awarded supplier; the Diavgeia `doc_url` opens the decision PDF). The Diavgeia cache is a broad sweep — **triage for relevance** (drop municipal bank-fee-accounting rows; keep genuine ATM/POS/self-service procurements) and lead each kept row's date with its most-recent development. Winners feed Agent 6.

## Search terms

EN: ATM, cash recycler, self-service kiosk, POS terminal, card acquiring, cash-in-transit, ATM maintenance, branch security, transaction monitoring, digital onboarding.
Local: ΑΤΜ/ΑΤΜ συντήρηση, αυτόματα μηχανήματα ανάληψης, τερματικά POS (EL); bancomat, terminale POS (RO); банкомат, ПОС терминали (BG/SR); bankomat (HR/SI/CZ/SK); банкомат, платіжний термінал (UK).

## What to capture

Buyer, country, subject, value (if stated), deadline, link, status (open/awarded/cancelled), winner if awarded. **The WINNER of any award is a competitor — capture it no matter how small or unknown the firm is, and pass it to Agent 6.** A small local company that just won a POS / ATM-service / integration deal Printec could have bid is a first-class competitor even with no press or filings (see the playbook's "Competitor scope" rule — Printec is ~€15M EBITDA, so a few-€m local winner is real competition). Awards to the known big competitors are signals too (Agent 6 overlap).

## Searching at scale: fan out per portal / country

One context can't work 17 national portals + TED deeply. **Fan out: one subagent per procurement portal /
country** (TED itself is a single subagent covering all EU members in one expert query).
1. **Triage** is light here — the portals are known. Always run TED (the API, all EU footprint in one query)
   plus the bank-owned pages (posted.co.rs, cec.ro), and fan a subagent to each national portal with its own
   access route.
2. **One subagent per portal, mandate "exhaust this portal":** use the documented access route from this
   brief's Method log (the JS/DataTable tricks, the Prozorro API, the correct local search terms) and search
   in the local language. Apply the **Exhaustiveness Standard inside the portal** — the documented route, then
   the API, then a `site:` cache — before reporting zero. (Many commercial-bank portals legitimately return
   zero because those banks are private — that IS the finding, not a failure.) That's the stop-condition.
3. **You (the parent) reduce:** dedup the same notice appearing in both TED and a national portal, sort the
   merged pipeline by deadline (flag anything closing within 30 days), and pass awards-won-by-competitors to
   Agent 6.

See the playbook's "Scaling the work" section for the general pattern.

## Output

`findings/02-tenders/YYYY-MM-DD.md` — standard signal table + open-tender pipeline list sorted by deadline. Flag anything closing within 30 days at the top.

## Method log (proven access routes — update each run)

*2026-06-13 (2nd run — Chrome sweep):*
- **PrivatBank own portal** (`tender.privatbank.ua/commercial/tender`) — JS-rendered DataTable, 3,998 tenders; filter with `?keyword=банкомат` URL param works. Direct tender URLs (`/tender/PB-YYYY-MM-DD-XXXXXXX`) are stable. Tender detail pages: click-through doesn't navigate; extract `<a href>` links via JS and navigate directly. **Critical finding:** Diebold Nixdorf recycling ATM maintenance cancelled twice (no supplier in UA market) and recycling ATM prequalification for next fleet cycle now active. Contact: Станіслав Гора (stanislav.gora@privatbank.ua), Svitlana Hlotova (svitlana.hlotova@privatbank.ua).
- **Prozorro aggregator** (`tender.uub.com.ua/company-EDRPOU/`) — company profile pages are static and paginated; useful for breadth. Oschadbank: EDRPOU 00032129. PrivatBank: EDRPOU 14360570. For detailed search, use `prozorro.gov.ua` directly or the API endpoint `https://prozorro.gov.ua/api/search/tenders` (POST; `edrpou` in POST body does NOT filter — only `query` works).
- **CAIS EOP Bulgaria** (`app.eop.bg`) — JS search form. Correct flow: open page → click "Търсене" to expand form → type keyword in search field → click "Добави" to add tag → click "Приложи" to apply. URL params don't work. Confirmed 0 open ATM/cash tenders for Bulgaria.
- **EOJN Croatia** (`eojn.hr/procurements-all`) — DevExtreme DataTable; use nativeSetter trick for input: `Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set.call(input, value)` + fire `input` event (bubbles:true) + `keyup` event. **Found:** HP Croatia Post POS maintenance (⚠️ 06.07.2026 deadline) and HNB CPS 7000i banknote processing. "Bankomat" keyword returns 0 (commercial banks are private).
- **EKR Hungary** (`ekr.gov.hu`) — "ATM" = Air Traffic Management (HungaroControl). Use "bankjegykiadó" or "pénzkiadó". Both return 0 for ATMs (Hungarian commercial banks are private, not covered by EKR).
- **Diavgeia Greece** (`diavgeia.gov.gr/f/elta`) — ELTA page loads in Angular; search not possible via Chrome page read. Recent acts are HR/personnel. The luminAPI endpoint (`luminapi.gov.gr`) returns HTML error (cross-origin). No new ELTA ATM procurement act found; plan still pre-tender.
- **Bank of Albania** (`bankofalbania.org/Rreth_Bankes/Njoftime_per_tendera/`) — static page; banknote packaging tender deadline confirmed **08.07.2026** (⚠️ 25 days from run date).
- **Bank-owned procurement pages first** — static HTML, complete, dated: `posted.co.rs/o-nama/nabavke.html` (Poštanska štedionica — NOT under Serbia's procurement law, publishes only there) and `cec.ro/achizitii` (CEC Bank runs own procedures outside SICAP). Check both every run.
- **TED — use the API, not the JS UI** (this closes the biggest tender blind spot; TED covers all EU footprint countries in one place):
  - **Search API** (no login): `POST https://api.ted.europa.eu/v3/notices/search` with an expert query combining CPV + country, e.g. `classification-cpv IN (30123000 30123200 30144400 48000000 72000000) AND place-of-performance-country IN (GRC ROU BGR HRV SVN CZE SVK HUN CYP)` and a recent `publication-date` window → structured JSON (buyer, title, value, deadline, links). Confirm the exact field/operator names from the TED Developer Portal on first use, then reuse.
  - **Daily bulk packages** (XML, no login) for a complete sweep when the API query is awkward.
  - **Detail:** notice PDFs at `ted.europa.eu/en/notice/<id>/pdf` render as text; the HTML meta-description carries country+title for cheap triage.
  - **Standing alert:** also enable the TED saved-search e-mail notification (one-time, free) so new matches arrive between runs — see `portal-alerts-setup-checklist.md` step 1.
- **Live watch items (next run):** Poštanska štedionica CIT+ATM-servicing award (still "у току"); PrivatBank recycling ATM prequalification completion → 2nd stage (hardware purchase) expected H2 2026; PrivatBank Diebold Nixdorf maintenance negotiated re-tender expected imminently; Bank of Albania deadline 08.07.2026; HP Croatia Post deadline 06.07.2026 (both ⚠️).

*2026-06-24 (3rd run — web search + WebFetch):*
- **PrivatBank 800 ATM purchase 2026 confirmed** — board member Dmytro Musienko (22 May 2026) confirmed 800 recycler/multifunctional ATMs to be purchased this year. This is the expected 2nd stage of PB-2026-03-17-3068329. Monitor tender.privatbank.ua for the hardware purchase tender notice. Contact: stanislav.gora@privatbank.ua.
- **Bank of Albania page** (`bankofalbania.org`) — returned HTTP 403 this run. **Operator action required: manually check before 08.07.2026 deadline.** Previous runs: static HTML, accessible.
- **CEC Romania** (`cec.ro/achizitii`) — returned HTTP 403 this run. Likely rate-limiting or temporary block. Re-try; use Google cache as fallback.
- **tender.uub.com.ua** (Prozorro aggregator, company pages) — returned HTTP 403 this run. Previously accessible. Use Chrome browser next run.
- **TED API** (`POST https://api.ted.europa.eu/v3/notices/search`) — returns HTTP 405 (POST not allowed via WebFetch). TED search UI is JS-rendered (results not loaded). **Must use Chrome browser or operator-run TED Expert Search / daily CSV bulk to cover EU tenders.** This remains the biggest blind spot.
- **Bulgaria euro conversion** (01.01.2026) — ATM fleets of all Big 5 banks reconfigured. CAIS EOP confirmed 0 open tenders (commercial banks private). Post-conversion ATM service and recycler hardware opportunity via direct bank outreach only.
- **Eurobank Greece** — NCR Atleos NDC Enterprise platform deployed across 950+ ATM fleet. Printec (NCR Global Partner 2026) should confirm involvement in servicing this estate.
- **Hungary ATM Act** (Act XVIII of 2025) — Phase 1 (settlements >2,000 pop); Phase 2 (>1,000 pop); long-term every settlement. Specific deadline decree from MNB Governor + Minister for National Economy still pending. trademagazin.hu has the Phase 1 settlement map.
- **Live watch items (next run):** ⚠️ Bank of Albania deadline 08.07.2026 (OPERATOR CHECK REQUIRED); ⚠️ HP Croatia Post deadline 06.07.2026 (OPERATOR CHECK REQUIRED); Poštanska štedionica CIT+ATM award still pending; PrivatBank 800 ATM hardware tender (watch tender.privatbank.ua and prozorro.gov.ua for EDRPOU 14360570); HNB Croatia CPS 7000i evaluation result; MNB Hungary mandate decree publication; CEC Romania next ATM batch tender.

*2026-06-24 (4th run — multi-agent fan-out, one sub-researcher per portal/country + TED; Chrome NOT connected):*
- **TED — the /pdf route is the key.** The v3 search API is POST-only (confirmed 405 again) and the UI/detail pages are JS-empty, BUT `ted.europa.eu/<lang>/notice/<id>/pdf` IS GET-fetchable and the **Read tool extracts full notice text** (buyer, CPV, value, deadline, winners) — verified on 4 notices. The only missing piece is **ID discovery**: `site:ted.europa.eu` WebSearch matches incidental boilerplate (every result was a false positive), the RSS feed ignores keyword params, and data.europa.eu returns datasets not notices. **Standing operator action:** run the TED POST expert-search once (CPV 30123000,30144400,48000000,72000000,50310000,50312000,35120000,66000000 AND country GRC,ROU,BGR,HRV,SVN,CZE,SVK,HUN,CYP,AUT AND publication-date ≥ run-date−30) and feed the notice IDs back — then the /pdf pipeline triages each. This is the single biggest unblock.
- **HNB Croatia — read the procurement-plan PDF, not EOJN.** `hnb.hr/documents/20182/121306/h-plan-nabave-hnb-2026.pdf` lists every planned tender with ref/value/procedure/quarter (extract with pdftotext; WebFetch can't parse the compressed stream but the saved binary reads fine). This run it revealed the whole cash-handling cluster: V-31 (€155k), V-32 CPS 7000i (€175k), V-33 (€226.1k), **V-34 new banknote-processing system €1.8M (Q4 2026)**, P-88 coin devices (€22k). NB: earlier "V-11 = coin devices €147k" was WRONG (V-11 is research-sector software licences; coin devices are P-88/2026 €22k) — always map the ref code to the line, don't trust a subject-to-ref guess.
- **HP Croatia POS (26.2.83):** confirmed still OPEN, deadline 06.07.2026 (published 12.06.2026, Velika Gorica) via the EOJN aggregator **nabavke.com** (hrvatska.posta.hr itself is 403). The ~€80k value is NOT this tender's — it belongs to a separate HP data-centre-maintenance tender (ref 26.2.90). Treat the POS value as unknown.
- **Kosovo (TEB SH.A.)** publishes IFB PDFs on its own site `teb-kos.com/en/tenders/` — rich in-scope cluster (digital onboarding+e-sign open to 29.06.2026 ID 270/26; cash-handling machines ID 259/26; ATM kiosk; electronic security; CIT+replenishment). TEB does NOT publish winners — email procurement@teb-kos.com. The PDFs are binary to WebFetch; download + pdftotext.
- **Austria (OeNB):** rural-ATM framework now AWARDED to **PSA Payment Services Austria** (€372,457.40, 60-mo, single bid) — read via direct deep-link on `ausschreibungen.usp.gv.at` (the list/search there is JS-empty; deep-links to known notices work).
- **Slovakia:** Slovenská pošta self-service cash-kiosk pilot (5 branches) — pre-tender, vendor undisclosed; engage now. **Czechia:** ČNB E-ZAK (`ezak.cnb.cz`) is GET-readable — found physical-security items (cashier screens, ballistic panels) + a G+D BPS M7 sorter. **Cyprus:** Veridos won the national biometric-ID system; CBC SIEM tender closed (€370k, no award). **Montenegro:** CBCG Eurosystem-alignment roadmap (tenders late 2026/2027). **Bosnia:** posta.ba returns a TLS-chain error.
- **Hungary ATM Act:** decrees PUBLISHED (NGM 16/2025; MNB 19/2025) — thresholds are >1,000 pop by 31.12.2025 and >500 pop by 31.12.2026 (NOT the >2,000/>1,000 in the old briefing). OTP filed a Constitutional Court challenge (Nov 2025) — allocation is contested; flag to Compliance before treating as final.
- **Still blocked (need Chrome):** PrivatBank portal (Angular SPA, template vars only), all Prozorro mirrors (403), Bank of Albania (whole domain 403), CEC Romania (403, 3rd run), EOJN Croatia (JS), Greek ESIDIS/KIMDIS/Diavgeia (JS), Serbia UJN (ASP.NET postback). Re-enabling Claude-in-Chrome for the scheduled run unblocks all of these in one pass.
- **Live watch items (next run):** ⚠️ Bank of Albania 08.07.2026 (OPERATOR); ⚠️ HP Croatia 06.07.2026 (OPERATOR); ⚠️ TEB Kosovo onboarding 29.06.2026; PrivatBank 800-ATM hardware notice (defend incumbency — Printec won the prior 1,140-unit / 838.64M UAH NCR contract Jan 2025); HNB V-34 €1.8M (Q4 2026) + V-31/32/33 award status; Poštanska CIT+ATM award; CEC post-rollout maintenance/managed-services; Slovenská pošta kiosk rollout decision; OeNB second municipality round (via PSA); Montenegro CBCG post-roadmap tenders.

*2026-06-24 (5th run — multi-agent harness, one sub-researcher per portal/country + TED; 13 portals, 27 agents, 75 verified signals, 0 empty after gap-fill; Chrome NOT connected):*
- **Harness infra (re-use this every run):** the shared `research-harness.workflow.js` needs `export const meta` as the **FIRST statement** (hoisted this run — it was below the `const` block and the Workflow runtime rejected it). The large `args` object must be handed to the harness via the JS launcher **`agent2-launch.workflow.js`** using the `workflow()` hook — passing `args` directly through the Workflow tool boundary stringifies it and the harness sees 0 units ("No units passed"). The task output is an envelope: read **`.result.markdown`** (nested under `result`, not top-level) from the `<task-id>.output` file and write it with UTF-8 (no BOM).
- **GR — NEW, highest-value (strategic, not a tender):** Printec (via **Printec Cash Network S.A.**) owns **80.10% of Cashflex/KEA**, now operating **~850 off-site Piraeus ATMs** (announced 22/05/2025, live H2-2025; KEA net assets ~€11m). A captive XL fleet to defend/upsell (NCR ATMs, x-core, telemetry, recyclers, OptiCash, managed services) and the natural vehicle to bid the ELTA all-bank-ATM network. Source: Piraeus Financial Holdings press release 22/05/2025.
- **GR — NEW public tender:** **OPSEA / national digital-ID system, €515.4m** (Υπερταμείο/Hyperfund for the Ministry of Citizen Protection), competitive dialogue, submission **extended to ~25/07/2026**; 4 consortia (OTE+Byte+Idemia; Unisystems+Veridos; Space Hellas+Nova+Zetes+Thales; Austria Card+Toppan). Large but low Printec win-probability (state citizen-ID, eIDAS2/EUDI hub) — digital-ID adjacency only.
- **HU — Act XVIII Phase 2 quantified:** ~**631 new ATMs** in 500–1,000-pop settlements by 31/12/2026 (Phase 2). No public tender — pursue the 9 assigned banks directly.
- **SK — NEW:** cashless-acceptance mandate **Act 384/2025 postponed to 01/05/2026** → drives POS/SoftPOS rollout.
- **Verification contradictions (do NOT treat as Printec openings):** Banca Intesa Beograd Diebold/Payten ATM-replacement = a **competitor win**, not an opening; the OeNB rural-ATM/PSA framework is a competitor capture, not an opening; the BORICA euro-cutover item was contradicted.
- **Access:** every JS/403 portal from the 4th run remained blocked (Chrome not connected) — the per-portal sub-researchers still reached findings via primary sites, regulator PDFs, local-language press and aggregators (13/13 covered, 0 empty). Re-enabling Claude-in-Chrome + running the TED POST expert-search would close the remaining blind spots.


*2026-08-01 (6th run — 15 portals; 2 harness passes + a batched verify; Chrome NOT connected):*
- **Coverage: 15/15 portals, 267 verified signals, 0 empty.** Added two units to the work-list that had shown
  activity but had no unit of their own: **austria-usp** (`ausschreibungen.usp.gv.at`) and
  **cyprus-eprocurement** (`eprocurement.gov.cy`). Both returned in-scope signals immediately — keep them.
- **HARNESS FAILURE MODE + THE FIX (read this before the next run).** Pass 1 lost 27 of 54 agents to
  `Connection closed mid-response` plus a session limit, and reported 7 units as EMPTY. They were **not**
  empty: each research agent had already written `parts/<runDate>/<slug>.json` and then died *while
  returning*, so verify/gap-fill saw nothing. **151 researched signals were sitting on disk.** Recovery that
  worked, and should be the standard response to this: (1) `cp -R parts/<runDate> parts/<runDate>_orphaned-backup`
  BEFORE anything re-runs, or the next pass overwrites the evidence; (2) re-invoke the harness scoped to ONLY
  the failed units, with each unit's `focus` naming its own backup checkpoint path and a
  **recover-verify-extend** mandate (read the checkpoint, re-verify each claim against the primary source,
  bring statuses current, then go beyond) — this is far cheaper than re-researching and it still gets the
  adversarial pass; (3) merge the passes with **`weekly-intelligence/scripts/merge_harness_runs.py`**, written
  this run for exactly this (it ports the harness's renderers — verified byte-identical against the real run —
  and adds the dedup + deadline banding below). Do NOT use `resumeFromRunId` for this: the failed agents are
  not cached, so they re-research from scratch anyway. Its `--journal` flag is repeatable and LATER runs win
  per unit, so pass the recovery pass last; `--extra slug=a.json,b.json` folds in batch-verified units.
- **Work-list updated (`agent-units.json` key "2"): now 15 units.** `austria-usp` and `cyprus-eprocurement`
  are permanent (both returned in-scope signals immediately), and three unit names were corrected to match
  what they actually cover. NB the SKILL's note about `findingsDir` being a Windows path is now **stale** —
  it already reads `/Users/mangian/Downloads/BANKING/findings/02-tenders`, so no override is needed.
- **32k OUTPUT-TOKEN CAP kills the verify step on rich units.** `gapverify:slovenia-enarocanje` failed twice
  with `response exceeded the 32000 output token maximum` — 29 verbose signals cannot be re-emitted in one
  response. Fix: verify in **batches of ~10 signals** (3 parallel subagents), each writing a JSON array to a
  file. Slovenia went from 0 to 28 verified this way. Any unit returning >20 signals needs this.
- **The parent MUST dedup, and only on STRONG identity.** 24 rows were the same notice found by both TED and a
  national portal. Safe keys: the **TED notice id** (`ted.europa.eu/*/notice/<id>`) and the **Prozorro UA id**
  (`UA-YYYY-MM-DD-NNNNNN-a`). **Do NOT dedup on a shared URL** — a portal search page, an XML/CSV API endpoint
  or a procurement-plan PDF is a *route*, not a tender: an early attempt keyed on URL silently deleted 24 real
  notices (several distinct ČNB, OeNB, NBRM and HNB-plan lines collapsed into one). Keep the richer row and
  append the dropped row's URL as a cross-reference.
- **Pipeline banding.** A flat ascending deadline sort buries the urgent rows under already-closed ones (15 of
  45 dated rows were in the past). Render three bands: ⚠ closing within 30 days → later → deadline passed /
  awaiting award (the last is worth keeping, because the award and its winner are the next event).
- **PrivatBank recycling ATMs are on the BANK'S OWN portal, not Prozorro** — `PB-2026-03-17-3068329`
  ("Ресайклінговий банкомат (1 етап)"), in pre-qualification since 08/04/2026 after a first attempt
  (`PB-2026-01-15-3067363`) was cancelled to rewrite the technical requirements. Budget deliberately "не вказано".
  Contact Hora Stanislav (stanislav.gora@privatbank.ua). Printec incumbency re-verified from primary:
  UA-2025-01-17-010779-a, UAH 838,639,173.73 incl. VAT; plus 39,000 Castles Saturn POS, UAH 151,734,960 (25/10/2025).
- **WINNERS resolved for Agent 6** (the run's main hand-off): Ukrgasbank's 81-ATM buy →
  **TOV "ATM sistems" (EDRPOU 44372551)**, UAH 49,720,800 incl. VAT, 16/04/2026 (the first attempt,
  UA-2025-11-20-012352-a, failed); Ukrposhta parcel terminals → **JV MODERN-EXPO**; PrivatBank SST components
  → **TOV "TK MAYTEK"**; PrivatBank POS → **Newland** (two tranches); ELTA's 300 banknote counters →
  **BOOS S.A.**; Banka Slovenije sorter maintenance incumbent → **Giesecke+Devrient** (EUR 963,000, single bid).
  And a Printec WIN outside the usual beat: **PRINTEC S.I. d.o.o.** holds Pošta Slovenije's parcel-locker
  supply + 5-year maintenance.
- **Access notes:** `enarocanje.si/pregled-objav/*` returns 404 to non-browser clients (JS SPA, no open notice
  API) — use the TED primary instead, but its **evidenčna-naročila / pogodba CSV endpoints ARE openly
  fetchable** and are the way into Slovenian below-threshold awards. TED `/xml` (eForms) is as fetchable as
  `/pdf` and is easier to field-check. Albania has **no public tender-notice search** (`app.gov.al` is the
  policy site; `bid.app.gov.al` is login-gated) — Bank of Albania's own tender pages are the route.
- **Live watch items (next run):** PrivatBank stage-1 pre-qualification → stage 2 hardware lot; Banka Slovenije sorter maintenance (17/08/2026); HP Croatia
  technical protection (17/08/2026); HNB V-15 (01/09/2026) and V-34 EUR 1.8m; Cyprus Insolvency Dept
  EUR 5.65m (15/09/2026); HAC Croatia card acceptance — unresolved 5 months past deadline, estimate tripled;
  Hrvatska pošta ref 26.2.83 still not findable in TED; Poštanska štedionica CIT+ATM award still pending.

*2026-08-27 (7th run — 15 portals; 1 harness pass + a BATCHED-VERIFY recovery pass; Chrome extension NOT connected, built-in Browser pane used):*
- **Coverage: 15/15 portals, 263 verified signals after dedup (281 researched), 0 empty.** 42 open tenders in the pipeline, 33 claims corrected by the adversarial pass, only 3 left unconfirmed.
- **THE HARNESS FAILURE REPEATED — AND THE RECOVERY IS NOW A ONE-SCRIPT DRILL.** Pass 1 lost **25 of 47 agents to a session limit**: all 15 research agents finished and checkpointed, but 8 portals died at VERIFY and both gap-fill rounds and the `narrate` step died too, so the harness published a COVERAGE WARNING naming 8 units as empty. They were not empty — **150 researched signals were on disk**. The drill that worked, in order: (1) `cp -R parts/<runDate> parts/<runDate>_run1-orphaned-backup` before anything re-runs; (2) confirm the research results are also in the run's `journal.jsonl` (they were — all 15); (3) run **`agent2-recover-<date>.workflow.js`**, a small purpose-built workflow that does ONLY the missing verify, in **batches of ≤11 signals per agent**, each agent Reading its own index slice from the backup checkpoint and Writing a JSON array to `parts/<runDate>/verify/<slug>-b<N>.json`; (4) merge with `merge_harness_runs.py --journal <pass1> --extra <slug>=<batch files>`. **17 batch agents, 17 succeeded, 0 failed, 150/150 signals recovered.** Batching is what makes this reliable — the 32k output cap is why the in-harness verify dies on any unit above ~20 signals, and 5 of the 8 lost units were in that band. Do NOT use `resumeFromRunId`: failed agents are not cached and re-research from scratch.
- **When `narrate` dies, the parent writes the prose.** `merge_harness_runs.py --narrative` takes a hand-written markdown file; the table is still machine-rendered, so nothing is at risk. Budget for this — the narrate agent is the last thing to run and therefore the most likely casualty of a limit.
- **Tier-0 caches were refreshed first and materially changed the run** (do this before launching): `fetch_ted.py --days 45` returned **219 in-scope notices, 92 with a named winner**; `fetch_prozorro.py` returned PrivatBank 82 / Oschadbank 19 / 263 other UA buyers; `fetch_diavgeia.py --months 3` landed 135 Greek below-threshold decisions.
- **NEW PROVEN ACCESS ROUTES (all found this run):**
  - **TED: if `/en/notice/<id>/xml` returns an empty body, retry the SAME notice on the buyer's language path** (`/hu/notice/<id>/xml` recovered the full 37.5 KB MNB HSM notice). This is a general technique, not a one-off.
  - **Prozorro friendly-IDs: `clarity-project.info/tender/<friendlyID>`** returns full server-rendered HTML with the UUID **and the winner** (the CDB only accepts the 32-hex UUID; dates are unix timestamps in `<span class="date" data-timestamp>`). This is how every UA award below was named.
  - **Slovenia: read the SPA bundle to recover the API contract** — `enarocanje.si/assets/index-*.js` plus its lazy chunks (`Objava-*.js`, `Pogodba-*.js`, `Evidencna-*.js`) name the exact endpoints; only exact names work, guessed paths 404. A desktop UA alone does NOT defeat the 404.
  - **Hungary EKR: fetch assets and API from the ROOT host** (`ekr.gov.hu/main.<hash>.bundle.js`, `ekr.gov.hu/api/...`) — `/portal/*` is an SPA catch-all returning index.html for every path including the JS bundles. The JSON search endpoint **silently ignores `page`** (104 sequential requests returned 1,040 rows with only 10 distinct ids) — use the CSV export.
  - **Czechia ČNB E-ZAK: the working GET route is `ezak.cnb.cz/contract_index.html?page=N`** (`/verejne-zakazky` and `/zakazky` 404/301). E-ZAK **never publishes the winning supplier or the contract value**, even on 'Zadáno' — recover both from the parallel TED notice.
  - **Romania SICAP: unfiltered `GetCNoticeList`/`GetCANoticeList` cap at 3,000 rows sorted ASCENDING from 2013**, so an unfiltered pull returns only 2019-2020 and looks like "nothing found". Use weekly `startPublicationDate`/`endPublicationDate` windows (17 per endpoint). With Referer + Origin + desktop UA there was no 403 at all this run.
  - **Serbia UJN: endpoint names cannot be guessed** — 401 without a cookie, 403 with a cookie but no UserToken, 400 on plausible-but-wrong route names and 405 on POST all look like dead ends. Route discovery needs a real network log; the **built-in Browser pane** (`mcp__Claude_Browser__preview_start` + `read_network_requests` + `javascript_tool`) works when the Chrome extension is not connected.
- **BLOCKED / DOWN this run (do not re-walk blindly):** Greek **KIMDIS/ESIDIS returned HTTP 503** (WebLogic "No backend server available" — a server outage, not a block) and **contracts.gr's per-CPV and per-organisation pages are GONE**; the Diavgeia openData API is the adequate substitute because every KIMDIS notice also carries a Diavgeia ADA. Slovak **eforms.uvo.gov.sk is now a Keycloak LOGIN WALL** and `opendata.uvo.gov.sk` does not resolve. Bulgaria's app.eop.bg is unchanged (Angular shell behind an F5 WAF, no backend JSON) — TED carries the CAIS EOP procedure ids, so notices still match back. Croatia EOJN `/api/postupci` still 401s. **pdftotext is not installed on this machine** — extract PDF text with pdfminer.six in Python instead.
- **THE RUN'S BIGGEST SUBSTANTIVE RESULT — a loss.** Banka Slovenije **awarded the banknote-sorter maintenance to Giesecke+Devrient Currency Technology GmbH on 21/08/2026 at EUR 1,890,000 excl. VAT**, single bid, six years to 31/08/2032 — **+96% on the EUR 963,000 predecessor**, after a first attempt was **cancelled 03/07/2026 when the same sole bidder quoted exactly the same price**. Re-tendering changed nothing. Use this as the argument at every other central bank on the same OEM lock.
- **PrivatBank: two distinct things, do not conflate them.** (a) The recycler programme `PB-2026-03-17-3068329` has sat at `active.stage2.waiting` for FIVE months — stage 1 qualification done, stage-2 commercial round never issued, no shortlist published, and no 2026 recycler award anywhere on Prozorro. Printec incumbency re-verified: UA-2025-01-17-010779-a, UAH 838,639,173.73 incl. VAT for **800× NCR SelfServ 2062 + 340× SelfServ 2064 = 1,140 recyclers** (note: the linked portal tender PB-2024-05-20-3055047 publishes no supplier name of its own). (b) A SEPARATE live contest — `PB-2026-08-20-3072069` 2-pocket banknote sorters, **EUR 1,538,156.59 incl. VAT, closed 28/08/2026** — where the portal **published the stage-1 qualified shortlist**: Glory Global Solutions (International) Ltd, TOV «Банківські технології» (33417694), TOV «ДІІП 2000» (40754185), TOV «Інноваційні банківські системи» (36184511). **Printec was not on it.** The portal never publishes winners but DOES publish shortlists — harvest them every run.
- **Two structural zeros confirmed as findings, not gaps:** Hungary's Act XVIII ATM mandate generates **zero procurement footprint** (bank-by-bank MNB decree allocation — pursue the nine assigned banks directly), and Serbia's portal carries almost no ATM tenders because the commercial banks are private.
- **Live watch items (next run):** PrivatBank stage-2 recycler round (the whole 800-machine programme hangs on it) and the outcome of the 28/08 sorter auction; ELTA EUR 6m Retail & Delivery Transformation consultation closes 10/09/2026 (specs still movable); Operátor ICT Prague CZK 250m payment gateway 31/08/2026; BNB EUR 115.48m coin blanks — closed 03/08/2026, no award; Cyprus Department of Insolvency EUR 5.652m on its SIXTH publication, 15/09/2026; NBS Serbia money-counting machines ЈН 397/2026 (11/09/2026); Bank of Albania three open tenders (09/09, 11/09, 17/09/2026); CBCG Montenegro vault equipment (07/10/2026, press-sourced only); Poštanska štedionica CIT+ATM award STILL pending; Hrvatska pošta technical protection closed 17/08/2026 awaiting award.

## ⏱ Recency — date the trigger, not the backstory (see the playbook RECENCY RULE)
Every finding's **Date** must be the most-recent *triggering* development (a new disclosure / tender / regulation step / hire / vendor move) **or** a near-future deadline — **never** an old supporting/incumbency date. Surface something as a signal only if that development is **≤3 months old** OR it creates a concrete opportunity/deadline within the next **~18 months**. Older incumbencies / structural positions / past deals (>6 months, no near-future trigger — e.g. a 2017/2018/2020/2021 reference) are valid **context** but must be tagged **[STANDING — dated YYYY]** and never presented as new news. **"What changed since last run" = genuinely new developments only.** The engine (ingest.py) parses your Date cell, computes the age, and auto-flags any NEW/UPDATED row anchored only on a >6-month-old fact with no future trigger — it renders as *standing context*, not a NEW signal. Get the date right at source.
