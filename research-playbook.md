# Banking Market Research Playbook

**Owner:** Kostas Karakasiliotis | **Last updated:** 2026-06-13
**Objective:** Infer what banks in Printec's footprint are working on, where they spend money, and what they will likely need in the next 6–12 months — without direct bank interviews.

## Country footprint (verified printecgroup.com, 2026-06-12)

Albania, Bosnia & Herzegovina, Bulgaria, Croatia, Cyprus, Czech Republic, Greece, Hungary, Kosovo, Montenegro,
North Macedonia, Romania, Serbia, Slovakia, Slovenia, Ukraine (16).

> **Austria was removed from the footprint on 2026-09-02 (owner decision).** It is out of scope for every agent:
> do not collect Austrian signals, do not raise Austria-scoped opportunities, and do not rank Austria as a market.
> Austrian-headquartered groups (Erste, RBI) and Austrian-domiciled vendors remain in scope **only** where they
> act in one of the 16 markets — attribute such a signal to the market where the activity happens, never to Austria.

## Agent organization

| # | Agent | Method | Cadence | Findings folder |
|---|-------|--------|---------|-----------------|
| 1 | Bank Disclosures | Primary IR: annual reports, investor/strategy-day decks, verbatim earnings transcripts (aggregators last-resort) | Monthly (5th) | `findings/01-bank-disclosures/` |
| 2 | Tenders & Procurement | TED (API/bulk + saved-search alert), Diavgeia/ΚΗΜΔΗΣ, SEAP/SICAP, CAIS EOP, Serbian portal, bank-owned pages + local equivalents | Weekly (Mon) | `findings/02-tenders/` |
| 3 | Regulation & Deadlines | DORA, instant payments, PSD3/PSR, ISO 20022, digital euro, accessibility, AML/KYC | Twice monthly (1st, 15th) | `findings/03-regulation/` |
| 4 | Market Statistics | Central banks, ECB/EBA stats, banking associations | Monthly (10th) | `findings/04-statistics/` |
| 5 | Early Intent (Jobs + Leadership) | Bank job postings + senior leadership changes (new CDO/CIO/Head of Payments/Channels…) | Weekly (Tue) | `findings/05-jobs/` |
| 6 | Vendors & Competitors | NCR Atleos, Diebold Nixdorf, Glory, Worldline, Euronet, fintech partners | Weekly (Wed) | `findings/06-vendors/` |
| 7 | Orchestrator | Triangulates 1–6 + 8, updates master table, writes weekly brief | Weekly (Fri) | `master-signal-table.md`, `weekly-briefs/` |
| 8 | Futurist (3–5yr outlook) | Global structural-trend research + the internal trend/forecast reports in the knowledge base; reasons 3–5 years out | Monthly (1st) | `findings/08-futurist/`, authors `intel-cache/futures_narrative.json` |

## Scaling the work: script the numbers, fan out the research

As we add duties, route each by its nature — and **let the number of subagents scale with what is actually
found that week** (competitors in play, products in demand, portals with activity). It is NOT a fixed roster.
Three tiers:

**Tier 0 — deterministic scripts own the NUMBERS.** Anything with a stable endpoint and machine-readable
output (ECB Data Portal, SEC EDGAR financials, TED bulk, Prozorro API) belongs in
`weekly-intelligence/scripts/` (`fetch_ecb.py`, `fetch_competitors.py`, `fetch_competitor_segments.py`),
wired into `run_weekly`. **Do not spawn an agent to re-pull a figure a script can fetch, sum-verify and cache.**
This is not about cost — it is about reliability: an agent reading a 10-K can misread a figure; a script that
sum-checks segments against the EDGAR total cannot ship a wrong number. Numbers are the ONLY thing that stays
narrow. (That is why the competitor financials did NOT make the Vendors agent busier — the numbers are
scripted; the agent does only the judgment the script can't.)

**Tier 1 — fan out qualitative RESEARCH, one subagent per entity.** Open-ended "what is X doing" research over
independent *entities* (competitors, banks, country portals) SHOULD fan out, one subagent per entity, scaled
to the live set — this is the default, not a reluctant exception:
- **Vendors agent → one subagent per active competitor.** Each sweeps that competitor across the whole
  footprint (newsroom, earnings commentary, local-language press, M&A, wins/losses, product launches) and
  returns a structured profile + signals. The count = competitors with footprint relevance this week (triage
  the ~20-name watchlist first, deep-dive the active ones — err toward more, not fewer).
- **Tenders agent → one per portal/language; Bank-Disclosures / Jobs → one per market** when the week is heavy.

  An entity passes the fan-out test when all three hold: (a) it's an independent unit that doesn't need the
  others' results to do its part; (b) it benefits from its own fresh context (no cross-pollution, no blown
  parent window); (c) its output merges mechanically. Competitors, banks and portals all pass cleanly.

**Tier 2 — fan out SYNTHESIS, one analyst per facet.** A *product* (or theme) is NOT an entity with its own
newsroom — it is a *lens* over signals the other agents already collected (cash-recycling demand shows up in a
bank's recycler tender, a branch-transformation note, cash-in-circulation stats — there is no "cash-recycling
source"). So do NOT put a *collector* on each product (that just re-walks the tenders/regulation/bank sources
with a filter). Instead, after collection, fan out one **analyst** subagent per product category to read the
assembled corpus + structural stats and write that product's **demand outlook** (trend, drivers, which markets,
which accounts, what to pitch) — the Outlook-tab logic, per product. Same scaling principle, one tier later,
because products *reduce over the corpus* rather than *collect from sources*.

**The parent always REDUCES.** Triangulation, dedup, confidence-promotion and ranking need the whole picture
and cannot be parallelised away — one market event seen from two competitors' sides is ONE event; the parent /
Orchestrator merges it. Subagents map; parents reduce.

**Net:** the subagent count is *dynamic*, keyed to the discovered work-list — active competitors, in-demand
products, live portals — the same elastic pattern the Orchestrator already uses for validation and writing.
Scout cheaply to enumerate the set, then fan out across it. Never invent figures inside any tier (Rule 1 below).

**Fan-out axis per agent — this is standing instruction, not optional. Each brief carries its own
"Searching at scale" section with the specifics:**

| Agent | Fan out one subagent per… | What each subagent exhausts | Numbers come from |
|---|---|---|---|
| 1 · Bank Disclosures | bank (or regional group) | that bank's IR site / strategy-day deck / verbatim transcript | the bank's own disclosures |
| 2 · Tenders | procurement portal / country (TED = one) | that portal's proven access route, in local language | the notice values themselves |
| 3 · Regulation | regulation workstream (DORA, instant payments…) | that rule's status across every jurisdiction + the local-language sweep | — (deadlines, not figures) |
| 4 · Statistics | country (non-EU markets first) | that market's central-bank series + leading indicators | EU counts are SCRIPTED (`fetch_ecb.py`) |
| 5 · Jobs + Leadership | market | that market's job boards + LinkedIn + leadership press | — (signals, not figures) |
| 6 · Vendors | competitor | that competitor across the whole footprint | financials are SCRIPTED (EDGAR) |
| 8 · Futurist | structural trend-driver / theme (cash→digital, instant payments, AI, regulation arc) | that driver's 3–5yr global + footprint trajectory | — (projections labelled; figures only from cited reports) |

A breadth-heavy agent **enumerates its live set, fans out one deep subagent per item, and reduces the results
itself.** The Orchestrator is the final reduce — its dedup load grows with the fan-out (the same event arrives
from several niches at once), and **only _cross-agent_ confirmation earns High confidence — two subagents of
the same agent are not independent sources.**

## Internal documents (the knowledge base)

Beyond the open web, Printec drops internal documents — paid market reports (e.g. RBR ATM forecasts), the
company products deck, competitor/partner sheets — into the `Data dump/` folder. A nightly job digests each
new file into pre-summarised metadata under `knowledge-base/` and moves the original into
`knowledge-base/processed/`. It is **additional evidence to fold into your normal research — NOT a substitute
for it, and NOT something to be biased toward.** As you research, also draw on your knowledge base:

- `knowledge-base/by-agent/agent-<N>-…/` — documents routed to YOUR beat, each a `.md` with tags, a summary,
  key points and a link to the original. Skim these first; open the full original (in `processed/`) when a
  digest shows it is relevant.
- `knowledge-base/_reference/` — shared internal material every agent + the Orchestrator should know, above
  all the **Printec products/solutions deck** (use it to map a market signal to the exact Printec product,
  and to know what Printec can actually sell into a trend).

These internal documents are **extra input, not the spine of your work**: cite them where they genuinely help
(report + page), but **keep searching the web as fully as ever, and let NO single document bias a conclusion** —
always triangulate across independent sources. This is a **reporting tool**: surface the cited evidence and let
the reader decide; do not bend findings toward whatever one report happens to say.

**Reading the real pages — charts, graphs, figures (ALL agents).** The digests, and even the raw text
extraction, CANNOT see data that lives only inside a CHART, GRAPH or image. So when you rely on one of these
documents for a figure — or want to cross-check a number from another source against it — open the actual
pages and look at them:

```
python knowledge-base/scripts/render_pages.py "<original in knowledge-base/processed/>" --pages "45-52"
```

It renders those pages to images (it handles large, encrypted PDFs and PowerPoint decks) and prints the image
paths; open each with the **Read tool**, which shows the page exactly as printed — bar/line/pie charts
included. Use `--figures` to list the pages that carry exhibits, or `--count` for the page count. Always cite
the page you read (`p.N`). This is the way to extract or confirm anything the digest can't show. The nightly
processor already does this when a document arrives; the heavy, page-by-page version for the most important
reports is the `deep-read-document` workflow (`weekly-intelligence/workflows/deep-read-document.workflow.js`),
which writes an enriched `<slug>-deep.md` digest covering **every country/market** in the report (for the
3-5yr outlook the whole world is a leading indicator — not just the footprint).

## Source catalogue (`SOURCES/` folder) — additional candidates, NOT a substitute

For **all 16 footprint countries** there is a catalogue of pre-identified sources at
`SOURCES/<Country> - Banking & Payments Sources.xlsx` (sheet `All sources`, plus `Pending - needs access`;
columns: `workstream`, `added_in_run`, `added_on`, `status`, `priority`, `source_name`, `source_type`, `url`,
`access`, `legal`, `sector`, `topics`, `why_track_it`). Two batches, same format, different provenance:

- **Hand-built (2026-07):** Greece, Albania, Bosnia & Herzegovina, Bulgaria, Croatia. URLs captured once,
  never re-verified — see the CORRECTED-URL bullet below.
- **Scouted (2026-08):** Cyprus, Czech Republic, Hungary, Kosovo, Montenegro, North Macedonia, Romania,
  Serbia, Slovakia, Slovenia, Ukraine. Every URL was fetched at capture time and searched in the local
  language as well as English, so these need no separate corrected-URL workbook. They are smaller per
  country than the hand-built ones — shorter, but tested.

Where a workbook exists for your market, treat it exactly like the internal knowledge base above:
**additional candidate sources to fold into your normal research — NOT a substitute for it, and NOT something
to be biased toward.** Keep searching the open web as fully as ever; the catalogue is a floor, never a
ceiling.

- **Filter to your own beat.** The `workstream` column carries `A1`–`A6` — take the rows matching YOUR agent
  number; they were curated for that beat. (`A1` disclosures · `A2` tenders · `A3` regulation · `A4`
  statistics · `A5` jobs/early-intent · `A6` vendors/competitors.)
- **Prefer the CORRECTED URL — the HAND-BUILT catalogue is stale.** (Greece, Albania, Bosnia, Bulgaria,
  Croatia only; the scouted eleven do not need this.) Those URLs were captured once and never re-verified:
  measured across the five hand-built workbooks, **73% now differ from their working version** and some are
  dead. A tested version of the same catalogue exists as
  `<Country>_Banking_Payments_source_access_audit.xlsx` → sheet `Source_Audit`, columns **`Final/corrected
  URL`**, **`Access status`** and **`Recommended collection method`** (plus `API_and_Dynamic_Sources` for
  tested API/download endpoints). **Use that URL in preference to the raw one in `SOURCES/`.** If a link is
  dead in both, self-heal it as you would any source (Rule 9) and cite the URL that actually worked.
- **Read the `status` column — it is a collection-clearance flag, not a quality score.** `active` (6,917 rows)
  means the source cleared every safety gate: publicly accessible, legally allowed, reviewed, and its URL
  verified. `paused` (9,332 rows) means at least one gate is not yet satisfied. **Work `active` rows first.**
  For a `paused` row, the `access` and `legal` cells tell you WHY, and they split into two very different cases:
    - **Not yet assessed** — `legal: unclear` or `access: unknown`. Nobody has looked; it is not a finding of
      restriction. This is the bulk of them, and most of the scouted eleven (73% of those rows are
      paused — ~88% in the five smallest markets — so treating `paused` as "skip" would discard most of
      them). Treat these as **leads**:
      open one if it is relevant to your beat, satisfy yourself it is genuinely public, and cite it only if
      you actually read it.
    - **Assessed and restricted** — `legal: requires_review`/`restricted`, or `access` of
      `requires_paid_subscription`, `blocked`, `requires_credentials`, `requires_legal_review`,
      `requires_free_account`. **Do not open these and do not work around the restriction.** They are
      concentrated in the hand-built five (555 `requires_review` + 84 access-restricted rows); the scouted
      eleven have 188 + 11. If such a source matters, flag it for a human rather than fetching it.

  Never treat `paused` as "cleared", and never treat it as "skip" — check the two cells and act accordingly.
- **Sort by `priority`** (critical → high → medium → low) and work the top of your slice first; do not try to
  walk the whole list — it is candidate material, not a checklist to exhaust.
- **Cite what you actually opened**, never a catalogue row you did not read. A source appearing in the
  catalogue is not evidence of anything by itself.
- **Every footprint market now has a workbook.** (The former exception, Austria, left the footprint on
  2026-09-02 and is out of scope entirely — see the Country footprint section.)

## Rules (all agents)

> ### ⏱ RECENCY RULE (read first — this is the #1 quality bar)
> A finding is only a **signal** if it is driven by a development that is genuinely **current**. From the
> first regular cycle onward (the seed run was the one-time exception that loaded history):
> - **Date the TRIGGER, not the backstory.** The `Date` column must carry the date of the *most recent
>   material development* that makes this a signal now (the new disclosure / tender notice / regulation
>   step / hire / vendor move / leadership change), **never** the date of an old supporting fact. If the
>   row rests on several dates, lead with the newest development; put older anchors in the text as context.
> - **"Fresh" = ≤ 3 months old.** Only surface something as a current signal if its triggering development
>   is within the last ~3 months **OR** it creates a concrete opportunity/deadline within the next ~18
>   months (a future tender, go-live, regulatory deadline, deal close). A future deadline keeps an
>   older-origin item current — capture that future date in the `Date` cell.
> - **Standing facts are CONTEXT, not news.** Incumbencies, structural positions, and past deals/press
>   (anything older than ~6 months with no near-future trigger — e.g. a 2017/2018/2020/2021 reference)
>   are valuable supporting context but **must be tagged `[STANDING — dated YYYY]`** in the Signal text and
>   **must never be presented as a new finding.** Do not put a stale standing fact in "What changed since
>   last run."
> - **"What changed since last run" = only genuinely new developments** since your previous dated file.
> - The engine enforces this deterministically: `ingest.py` parses your `Date` cell, computes the age, and
>   **flags any row badged NEW/UPDATED whose only anchor is >6 months old with no future trigger** — it is
>   shown on the dashboard as *standing context*, not as a NEW signal, and it dents the agent's quality
>   score. So get the date right at source.

1. **Never invent** numbers, budgets, market sizes, or timelines. If data is unavailable, say so and suggest the next-best proxy.
2. **Every claim cited**: source name, URL, date.
3. **Connect every signal** to a possible banking need, vendor opportunity, budget direction, or likely 6–12 month action. No generic market summaries.
4. **Standard finding format** (one table per findings file):
   `Bank | Country | Signal | Source (link) | Date | What it implies | 6–12 mo likelihood | Confidence (H/M/L) | Type | Opp. size | Recommended follow-up`
   (See the sizing & contest-type rubric below. There is NO Win column — never estimate the odds of winning.)
5. **Confidence scoring**: High = 2+ independent quality sources, recent. Medium = 1 quality source or 2 weak ones. Low = single weak/old signal. Single-agent findings cap at Medium; only the Orchestrator may assign High after cross-agent confirmation.
6. **File naming**: `findings/<agent-folder>/YYYY-MM-DD.md` (run date). Read your previous file first — report what is NEW or CHANGED, don't repeat old findings.
7. **Plain language**: follow `WRITING_POLICY.md` (project root) for everything a reader sees — plain business English, short sentences, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, jargon explained on first use, deadlines as a list, descriptive headings, explicit conclusions; add new terms to `glossary.md`.
8. **Search languages**: English + local language of each country (Greek, Romanian, Serbian, Bulgarian, etc.).
9. **Citable, stable URLs**: every source URL you record is re-fetched and snapshotted each week by the
   trust pass (`verify.py`) — prefer canonical/primary URLs over session-bound or search-result links so a
   claim can always be re-checked. If a key figure lives only on a JS-heavy or login-gated page, capture
   the figure in the finding text AND note the access route, so the orchestrator can re-confirm it.

## Competitor scope — from a few million to the giants (ALL agents, read this)

Printec is a **~€15M-EBITDA regional player**, not a global vendor. So its real competitive set is **NOT
just the billion-dollar names** (NCR Atleos, Diebold, Worldline, Euronet, Brink's) — it spans the **full size
range, from a few-million-revenue local player up to the global OEMs.** A small local POS/acquiring provider,
soft-POS app, regional system integrator, local ATM-service or CIT firm, or a bank's in-house acquiring team
that wins a single footprint deal is **as competitively relevant as a giant — often more so**, because it bids
the very contracts Printec bids, on price / locality / agility.

**Rules for every agent:**
- **Never drop a competitor for being small.** "Too small to matter" is the wrong filter — a €20M (or €2M)
  local player can take the exact POS or ATM-service contract Printec wanted. Threat is independent of size.
- **POS / acquiring is the most fragmented, most local segment** — expect a long tail of small players
  (soft-POS, local PSPs, ISOs, bank-owned acquiring). Don't just list the big acquirers.
- **How to find the small/private ones** (they don't file or issue press): the **WINNER of a tender**
  (Agent 2 — capture every award's winner regardless of size and pass it to Agent 6); **lost deals /
  "who beat Printec"**; **local-language press**; bank vendor/case-study pages; and **app stores** (soft-POS).
- When you surface one, Agent 6 tags it in `competitors.json` with a **`tier`** — `global` | `regional` |
  `local-peer` — so the small ones stay visible and filterable, not drowned out by the giants.

## Sizing & contest-type rubric (the two ranking columns)

> **OBJECTIVITY RULE (decided 2026-06-25 — applies to the whole dashboard EXCEPT the Outlook tabs).**
> The dashboard first page and every ranked list are now **objective only**: signals are sorted by
> **recency** (newest development first — the default), **deal size (€, from the Opp.-size band)**, and
> **independent-agent corroboration**. **Win-probability and any expected-value (size × win × confidence)
> score are NOT shown or used for ranking anywhere** — whether Printec can capture a deal is the
> business's call, not the dashboard's. Standing facts are excluded from "Top opportunities" (they appear
> only as tagged context). Every signal carries a **Type** that routes it to ONE lane, and only the
> **opportunity** lane is shown as a near-term opportunity:
> - **`net_new_contest`** — a winnable, NET-NEW deal Printec does **not** already hold (a tender, funded
>   programme or mandate). The ONLY lane shown under "Top opportunities" / "Biggest near-term opportunities
>   by market". An incumbency *anchor* (Printec already serves the bank on something adjacent) does NOT
>   disqualify a genuinely net-new contest — keep it net_new_contest. **Nor does a missing deal value:**
>   an unpriced tender is `net_new_contest` + `Unscoped`, carried as a value-unscoped opportunity.
> - **`owned_asset`** — Printec already owns/operates the exact scope (e.g. the Cashflex fleet); also mark
>   Status `SECURED`. → **Installed base — own & defend** lane.
> - **`incumbent_renewal`** — Printec is the entrenched/sole incumbent and the deal is effectively a
>   renewal/follow-on of held scope (near-certain, not a contest to win). → **Installed base** lane.
> - **`lost`** — a NAMED competitor won or holds the most valuable part; also usable as Status `LOST`. →
>   **Lost / competitive-intel** lane.
> - **`threat_macro`** — a macro driver or competitor threat, not a discrete deal (usually `Unscoped` or
>   footprint-wide). → context.
> The engine drops owned_asset / incumbent_renewal / lost / threat_macro from ALL opportunity value,
> per-market totals, rankings and "Top opportunities"; each keeps its own labelled lane. Keep assigning
> **Opp. size** (objective scale, anchored to real figures). **Win-probability is NEVER estimated or
> recorded — there is no Win column** (the odds of winning are the sales teams' call, not ours). The
> **one exception is the Outlook (6–12mo) and Future-outlook (3–5yr) tabs**, which are explicitly the
> analyst's reasoned *opinion on the objective facts* — direction/confidence/rationale stay there.

These columns drive the master table. The Opp. size band feeds the dashboard's **objective potential-value
(€m)** ranking and per-market totals; the **Type** routes the lanes. **Never invent a number.** Assign a
*band*, not a euro figure, and only from what the evidence supports.

- **Opp. size** — the rough scale of the Printec-addressable opportunity, as a band:
  `XL` (≥ ~€5m, or a footprint-wide programme), `L` (~€1–5m, large single-bank deal),
  `M` (~€0.2–1m), `S` (< ~€0.2m), or **`Unscoped`** when the signal is a *threat, a macro driver,
  or too early to size* (e.g. "branch consolidation continues", a competitor move). Bands are indicative
  for ranking only — they are not quotes. If a real figure exists in the evidence (a tender value, a
  capex line), use it to pick the band and cite it.
  **SIZE NEVER DECIDES THE LANE (changed 2026-08).** `Unscoped` no longer removes a signal from the
  opportunity lane. Most tenders in this footprint never publish a value, so a missing figure is a gap in
  *disclosure*, not evidence that there is no deal. Decide `Type` on the SHAPE of the signal — is there a
  discrete buyer and a discrete scope? — and set `Opp. size` independently on what the figures support.
  A tender with no published value is `net_new_contest` + `Unscoped`: the engine carries it as a
  **value-unscoped opportunity**, counted in every opportunity list and count, contributing **€0** to the
  value bars. Never guess a band to make a deal "count"; the €-total is published as a floor, not a total.
- **Type** — which lane the signal belongs to: `net_new_contest` (winnable, net-new — the only lane shown
  as an opportunity) · `incumbent_renewal` (Printec entrenched/sole incumbent; renewal of held scope) ·
  `owned_asset` (Printec owns/operates it; also Status SECURED) · `lost` (a named competitor won/holds the
  valuable part; also Status LOST) · `threat_macro` (a driver/threat, not a deal; usually Unscoped). Do NOT
  record any win-probability — that is the sales teams' judgement, not market intelligence's.

`Unscoped` rows still appear (they rank on evidence strength) but contribute €0 to the value ranking, so a
diffuse macro signal never outranks a concrete biddable deal on money. An `Unscoped` row in the
**opportunity** lane is a real contest awaiting a figure — it is listed, badged "value unscoped", and
sizing it is a research task for the next cycle; an `Unscoped` row in `threat_macro` is not a deal at all.

## Access protocol: JS-blocked pages and PDFs

When you hit a page that requires JavaScript to render content, or a PDF that your tools cannot download directly, follow this sequence before giving up:

1. **Try the API first.** Many sites with JS frontends have plain JSON/CSV APIs underneath (e.g., Prozorro, ECB Data Portal, Banca Transilvania careers). Check the agent brief's "proven access routes" section — the API route may already be documented.
2. **Try a Google cache or search snippet.** A `site:` search on Google often returns indexed text from JS-heavy pages. Dated snippets in search results count as a signal if the full page is inaccessible.
3. **Try Claude in Chrome (browser tools).** If the page works when a human opens it in a browser, use `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`. This renders JavaScript and can read most pages. Check whether Claude in Chrome is connected before assuming it is not.
4. **For PDFs specifically:** if Chrome can render the PDF but downloading fails, use `mcp__Claude_in_Chrome__get_page_text` on the PDF URL — it reads PDF text without downloading. If the PDF is behind a login or CAPTCHA that you cannot bypass, **stop and ask the human operator**: write a clearly labelled `## PDF REQUESTS FOR OPERATOR` section at the bottom of your findings file listing each URL and what you expect it to contain. Do not skip the source — flag it.
5. **Log what you tried.** In the findings file, note in a `## Access issues` subsection: the URL, what method you tried, what failed, and what fallback you used or why you gave up. This prevents the next run from wasting time on the same dead ends.

Do NOT simply list a source as "inaccessible" without attempting at least steps 1–3.

### Standing decision on Claude-in-Chrome (resolved 2026-06-24)

Headless/scheduled runs **do not depend on Claude-in-Chrome.** The 24/06/2026 Tenders run
reached full coverage (13/13 portals, 0 empty after gap-fill) with Chrome **not** connected,
and the two hardest blind spots are now closed **deterministically** by Tier-0 scripts:
`scripts/fetch_ted.py` (TED Search API v3, POST — the EU-wide feed) and
`scripts/fetch_prozorro.py` (Prozorro search API, POST — PrivatBank/Oschadbank + UA buyers),
both wired into `run_weekly` and cached in `intel-cache/`. So:

- **Standard route for headless runs:** API → primary PDF (incl. the TED `…/notice/<id>/pdf`
  route and regulator procurement-plan PDFs) → Google cache/snippet → **Tier-0 script cache**.
- **Chrome is an OPTIONAL sourcing-quality lever**, not a reliability requirement. It only adds
  value for the residual JS/403 *national* portals (EOJN Croatia, Greek ESIDIS/Diavgeia, Serbia
  UJN, CEC Romania, Bank of Albania). If an operator runs interactively with the extension
  connected, agents MAY escalate to it for those specific portals.
- **Do NOT** carry "re-enable Chrome" as a blocking action, and do NOT log Chrome's absence as
  the reason for a coverage gap — a gap is only genuine after the standard route above is
  exhausted. Note the specific portal + failed access route instead.

## Exhaustiveness standard

Do not stop when you hit the first gap. A gap in search results is a prompt to try harder, not a finding. Before reporting something as unavailable:

1. **Try at least 3 distinct search angles**: different keywords, different languages, different source types (news, regulator, vendor, job board, procurement portal).
2. **Go one level deeper on promising leads**: if a search result mentions a bank initiative without details, fetch the source page; if a page mentions a document, try to find and read that document.
3. **Use proxies when primary sources fail**: vendor earnings mentioning a country, local press citing a regulator, job postings implying a program, a tender award revealing a winner — any of these can substitute for a primary announcement.
4. **Report depth, not just breadth**: it is better to find 5 solid signals with full source chains than 20 shallow mentions. Quality over quantity.
5. **Only declare a genuine gap** after exhausting the above. State specifically what you searched, what you found, and what the best available proxy is. Never write "no data available" without a suggested alternative.

## Priority signal themes — SEARCH THE FULL BANKING PRODUCT RANGE (standing instruction)

**Every agent must actively hunt demand signals for EVERY Printec banking product line below — not just the obvious ATM/POS ones.** Earlier runs over-indexed on ATMs/POS/branch and under-collected the rest, so we missed real opportunities. The canonical, machine-checked list is `weekly-intelligence/references/product_map.json` (the dashboard's product categories); the digested deck is `knowledge-base/_reference/printec-company-presentation.md`. Run searches (English + local language) for each of these, per market:

1. **ATM & cash automation / recycling** — ATM fleets, recyclers, intelligent-deposit, teller cash recyclers (TCR), smart safes, coin, OptiCash/APTRA cash management.
2. **Self-service, kiosks & branch transformation** — kiosks, bank kiosks, APS/SmartPay terminals, x-core, x-visio/QMS queue management, videobanking, phygital branches.
3. **POS, acquiring & terminal management** — EFT-POS terminals/PinPads, softPOS/tap-to-phone, x-pos, TMS (terminal management), POSight, payment facilitation/switching.
4. **Payments modernization (instant / ISO 20022)** — instant payments/SCT Inst, ISO 20022, VoP, payment hubs, RTGS, digital euro.
5. **Digital identity, onboarding & e-signature** — eKYC/video-ID/biometrics, **e-signature / eIDAS / qualified trust services**, EUDI-wallet acceptance.
6. **Fraud & transaction monitoring** — real-time transaction monitoring/analytics (INETCO), fraud/AML screening, FICO.
7. **Compliance & operational resilience** — DORA, AML (AMLR/AMLA), accessibility (EAA), PSD3/PSR, reconciliation/data-integrity, chargeback/dispute, **document management**.
8. **Physical ATM security** — IBNS/banknote-neutralisation, anti-skimming, vault locks, surge protection.
9. **Payment security & key management (HSM)** — payment HSMs (Thales payShield), **remote key injection (ERKM/SLKI), PCI-PIN / Payments Room**.
10. **Card issuing & management** — card issuing/management/personalisation, issuer-processor & card-platform programmes, scheme migrations.
11. **Managed services / outsourcing** — ATM-as-a-Service, device telemetry/remote monitoring, field/maintenance services, BPO.
12. **Core / digital channels (adjacent)** — core-banking & digital-channel programmes that precede channel/self-service spend.

A market's signal sweep is only complete when you have *looked* for each of the 12 (report "none found" explicitly where a category has no signal that week — don't silently skip it).

## Printec context (why these signals matter)

Printec sells the full banking stack above — vendor hardware (NCR Atleos, Verifone, Castles, Glory, Sesami, Consillion, Thales) wrapped with Printec in-house software (x-core, x-pos, x-visio, POSight, telemetry, TMS) and partner platforms (Namirial eKYC/e-signature, IMTF Siron AML, FICO, INETCO, FIS) plus managed/field services (500+ engineers, 100+ service points). Key partner: NCR Atleos (Global Partner of the Year – Europe 2026). Signals that imply demand for ANY of the 12 product lines = highest priority — including the previously-under-collected ones (HSM/key-management, e-signature/trust, card issuing, transaction monitoring, TMS, document management).
