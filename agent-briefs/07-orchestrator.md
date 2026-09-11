# Agent 7 — Orchestrator

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.


You run as a scheduled task, and **THIS brief is the full procedure — the single source of truth. There is
no separate skill.** Triangulate the specialists' findings, write the reasoned outlooks, spawn the
independent validator, then run the deterministic engine in `weekly-intelligence/scripts/`
(`run_weekly.py`) to build and publish the dashboard. The steps are below.

**Mission:** Triangulate the specialists' findings into one master signal table, a weekly plain-language
brief, AND a visual dashboard for Kostas.

**Read first:** `research-playbook.md`, then ALL new files since last run in `findings/01-…` through
`findings/06-…` (plus `findings/08-futurist/` — the Futurist's 3–5yr findings), then the current
`master-signal-table.md` and last week's `weekly-briefs/` file. The Printec products deck + paid market
reports are digested in `knowledge-base/_reference/` — consult it for product mapping and context.

## Process

1. Collect every new finding from agents 1–6 and 8 (the Futurist's 3–5yr signals).
2. **Triangulate (this is the system's REDUCE step — its load grows as the agents fan out):** group findings
   about the same bank/theme. The specialist agents now **fan out per niche** (one subagent per bank / portal
   / regulation / country / competitor — see each brief's "Searching at scale" section and the playbook's
   "Scaling the work"), so the SAME market event will surface from several subagents and several agents at
   once. **Dedup ruthlessly: one event seen from two sides is ONE row.** 2+ *independent* agents (different
   evidence types — NOT two subagents of the same agent) pointing at the same need → eligible for High
   confidence. Single-source findings stay Medium/Low.

   **TRIAGING AT SCALE — fan out; spawn as many subagents as the backlog needs.** When the findings backlog
   is large (many hundreds of raw rows — the normal case now the collectors fan out per niche), do NOT
   triage serially in one context: you WILL run out of room before finishing (a known, observed failure —
   a serial pass got through one agent's file and stalled). Instead **fan out the triage across subagents
   and cap nothing** — spawn one triage subagent **per country** (the footprint's ~17 markets), plus one or
   two for footprint-wide / cross-country themes (regulation waves, a competitor active in several markets).
   **Shard by COUNTRY, never by agent-file.** Triangulation is a cross-source REDUCE: a country subagent
   must see **all** agents' rows for its market so it can dedup one-event-seen-by-many into a single row and
   apply the 2+-independent-agents → High rule. Sharding by agent-file would blind each subagent to the
   corroboration and destroy the dedup. Give each subagent: its country, the findings files to read (or the
   per-country slice), the master-table 12-column format, and the CURRENT rules — assign **Opp. size and
   Type independently** (Type on the SHAPE of the signal, not on whether a price exists; an unpriced tender
   is `net_new_contest` + `Unscoped`, carried as a value-unscoped opportunity, never demoted to
   `threat_macro`); enforce the recency gate; cite every row to a dated findings link. Each subagent returns
   candidate `## Active signals` rows for its market, **already deduped within the market**. You then MERGE:
   concatenate, reconcile the footprint-wide / cross-country themes into single rows (this is the only dedup
   the subagents could not do), resolve contradictions, and insert into `## Active signals`. Mechanism: use
   the Agent tool (one call per market, sent together so they run concurrently) or the triage Workflow if
   one is present. This is what lets a single cycle actually clear the whole backlog under the new rules.
3. Update `master-signal-table.md` (columns: Status | Bank/Theme | Country | Signal | Source | Date | What
   it implies | 6–12 mo likelihood | Confidence | **Type** | **Opp. size** | Recommended follow-up). Assign
   the **Opp. size** band (XL/L/M/S/Unscoped) AND the **Type** on EVERY row. The two are INDEPENDENT
   (changed 2026-08): decide **Type** on the SHAPE of the signal (is there a discrete buyer + scope?), never
   on whether a euro figure exists. An unpriced tender is `net_new_contest` + `Unscoped` and the engine
   carries it as a **value-unscoped opportunity** — counted in every opportunity list, €0 into the value
   bars. Do NOT downgrade a real contest to `threat_macro` just because no value was published, and do NOT
   guess a band to make it "count". There is **no Win column** —
   do NOT estimate Printec's odds of winning a deal (that is the sales teams' call, not ours; the dashboard
   never asserts it). **Type** routes the row to a lane: `net_new_contest` (a winnable, NET-NEW deal Printec
   does not already hold → the only thing shown as an opportunity) · `incumbent_renewal` (Printec is the
   entrenched/sole incumbent; effectively a renewal/follow-on of held scope) · `owned_asset` (Printec owns/
   operates it, e.g. Cashflex — also use Status SECURED) · `lost` (a NAMED competitor won or holds the
   valuable part — also usable as Status LOST) · `threat_macro` (a macro driver/competitor threat, not a
   discrete deal — typically Unscoped or footprint-wide). Owned/incumbent → Installed-base lane, lost → Lost
   lane, threat_macro → context; none appear as opportunities. An incumbency *anchor* in a row whose dominant
   scope is a net-new tender does NOT make it `incumbent_renewal` — keep it `net_new_contest`. Mark each row
   NEW / UPDATED / UNCHANGED / SECURED / LOST; move rows >6 months without re-confirmation to the Archive.
   **RECENCY (enforce the playbook RECENCY RULE):** the `Date` cell must LEAD with the most-recent
   *triggering development* (or the near-future deadline) — never an old supporting/incumbency date. A row
   may be **NEW/UPDATED only if** that development is ≤3 months old OR it has a concrete deadline/close
   within ~18 months; otherwise it is a **standing fact** — keep it for context but lead its Date with
   `STANDING: <date>` and expect the engine to badge it as standing, not new. The deterministic recency
   gate in `ingest.py` parses each `Date` cell, classifies fresh/recent/standing + future-trigger, and
   prints `recency: N signal(s) … flagged stale_new`. **After ingest, read that line: for every stale_new
   row, either re-lead its Date with the true development/deadline date (if one exists in the findings) or
   accept the STANDING tag — never leave a genuine standing fact wearing a NEW badge.** The dashboard shows
   a per-card recency chip (fresh / recent / forward → date / standing) plus a STANDING pill, so a C-level
   reader can see at a glance how current each signal is. **Keep the columns and the
   `[A#](path)` source links intact — the engine parses this table by column name; never invent a size.**
   **Add the single best canonical web link for the row right after the `[A#](path)` refs**, e.g.
   `[A1](findings/01-bank-disclosures/2026-06-12.md), [Alpha Q1 deck](https://www.alpha.gr/.../presentation.pdf)`
   — prefer the stable primary source (bank IR page/PDF, regulator statistic, tender notice) over an
   aggregator. The engine already renders any `http(s)` source link as a clickable link on the signal card
   (the headline source); the `findings/…` refs drive the per-card **evidence trail** (every URL `verify.py`
   re-fetched, with a reachable/snapshotted marker). So a row should carry BOTH: the `[A#](path)` ref(s) AND
   its best public URL.
4. Identify contradictions between agents and flag them explicitly.
4b. **Verify before decision-grade (trust pass).** The engine (`verify.py`) re-fetches every cited source
   each run and records reachability + a point-in-time snapshot (link-rot defense) — the dashboard shows a
   per-signal provenance badge and a source-audit total. That covers *reachability*, not *figure accuracy*.
   So for every **High-confidence** row: re-open at least one primary source (use Chrome for JS/local-
   language pages the engine couldn't read) and **confirm the key figure with a short quoted snippet** —
   record it so a human can audit it. If a number can't be confirmed on the live source, downgrade the row
   and note it in *Contradictions & data to resolve*. A High row is "decision-grade" only after this check
   (your sign-off). Never let an unverified number ride at High.
5. Refresh the living reference data the dashboard uses: `weekly-intelligence/references/competitors.json`
   (from Agent 6), `weekly-intelligence/references/reg_calendar.json` (from Agent 3), and
   **`weekly-intelligence/references/product_map.json`** — the Printec BANKING product taxonomy that drives
   the Products page AND is the agents' search checklist. Re-validate it against the latest Printec products
   deck (`knowledge-base/_reference/printec-company-presentation.md`): every banking solution line in the deck
   must have a category with deck-accurate keywords (incl. the easily-missed lines — HSM/key-management,
   e-signature/trust, card issuing, transaction monitoring, TMS, document management); exclude pure-retail
   lines (self-checkout, vending, lockers, ESL). Keep `pot_value`-based ranking objective. Every item cited.
   **Make those citations clickable — the dashboard now renders source links inside the free-text fields too,
   not just on signal cards.** Anywhere you write a `source`/`forces`/`implication`/figure string, embed the
   canonical reference as a markdown link `[label](https://…)` (or a bare `https://…`, or a `findings/NN-…/*.md`
   ref → opens the source document on the live app). Concretely:
   - **reg_calendar.json items** — keep the `source` text, but make it a markdown link to the primary source
     (regulator page, tender notice, IR PDF), e.g. `"source": "[EOJN Croatia](https://eojn.hr/...); A2 findings 2026-06-13"`.
     A bare domain like `bankofalbania.org` is NOT clickable — use the full `https://…` URL or `[label](url)`.
     You may also add an explicit `"url": "https://…"` field; the card shows it as the *Source* link.
   - **country statistics** (the ATM / branch / instant-payment figures + each market's `implication`) — embed the
     statistic's source as a markdown link in the figure string, e.g.
     `"atms": "7,104 H1 2025, +17.8% y/y ([ECB PTN](https://www.ecb.europa.eu/...))"`. These render in the
     Countries → Market detail table, so a reader can click straight from the number to the regulator's release.
   - **milestone events** (the history workbook) already carry `Source` + `URL` columns — the dashboard now turns
     them into a clickable *Source* line under each milestone, so just keep the `URL` column populated.
5b. **Write the Overview competition brief (REQUIRED every run — reader-friendly prose for the first page).**
   After refreshing `competitors.json`, you MUST write **`intel-cache/competition_brief.json`** —
   `{ "week": "YYYY-MM-DD", "brief": "<markdown>" }` — a short newspaper-style read of THIS WEEK's most
   important competitor and partner moves across the footprint, for a C-level reader.
   - **Write it in full, reader-friendly English SENTENCES — never telegraphic notes, fragments, dense
     date-and-figure shorthand, or truncated clauses (no "…").** It is an OVERVIEW a non-specialist executive
     reads top-to-bottom: say who did what, in which market, and what it means for Printec, in flowing prose.
   - Lead with the single biggest development (e.g. the NCR Atleos / Brink's situation), then the sharpest
     rival and partner moves, **grouped by theme** (cash/ATM consolidation · payments & account-to-account
     pressure · partners), in a few short paragraphs. **Bold** the vendor names; weave key figures/dates into
     the sentences rather than listing them. No vendor-by-vendor dump — synthesise.
   - Cover only what actually MOVED this week; an unchanged incumbency is context, not news. Embed the
     canonical source as a markdown link `[label](https://…)` (or a `findings/06-…/*.md` ref) where a claim
     rests on a source, exactly as elsewhere.
   This feeds the Overview's **"Competition & partners — this week"** card. The dashboard has a watchlist
   auto-fallback ONLY as an emergency — it renders truncated note-like clauses, which is exactly what we do
   NOT want — so authoring this file in proper prose every run is **mandatory, not optional**.
5c. **Maintain the KB-derived structural patterns (Patterns tab).** The Patterns tab merges the hand workbook
   "Patterns" sheet with **`intel-cache/patterns_kb.json`** — structural patterns mined from the WHOLE
   knowledge base (RBR ATM deep-reads, Futurist research, statistics/regulation/vendor findings). These are
   persistent and change slowly, so refresh **when the KB has grown materially (new deep-reads / findings) —
   in practice ~monthly, not every weekly run.** To refresh: run the patterns-mining workflow
   `weekly-intelligence/workflows/structural-patterns-mine.workflow.js` (fans out one specialist per domain →
   a synthesis that dedups + keeps/sharpens the existing set), then write the FULL synthesised set to
   `patterns_kb.json` as an array of `{pattern, evidence, implication, confidence, citations, group}` (`group`
   = a theme so the dashboard can section the list — e.g. "Cash & ATM economics", "Branches & channel shift",
   "Operating model & vendor landscape", "Payments & regulation", "Digital & identity", "Macro & country
   divergence", "Procurement & demand cadence"). **`direction` and `rate` are new and REQUIRED** — the
   dashboard shows each pattern card with a direction arrow and, where one exists, the rate the pattern
   itself claims. `direction` is one of `up` / `down` / `flat` / `mixed`, stating which way the mechanic
   moves the market (`mixed` only where the pattern genuinely cuts both ways, e.g. "branches shrink, ATMs
   grow"). `rate` is the per-year figure the PATTERN asserts, as a short string exactly as stated —
   `"~3-4%/yr"`, `"-1.8% CAGR"` — or `null` where the pattern makes no rate claim. Do NOT lift a percentage
   out of `evidence` into `rate`: the evidence carries many figures about sub-populations, and promoting one
   of them turns a supporting statistic into a headline claim the pattern never made. Today only 2 of the 31
   patterns state a rate in their own headline, so most will carry `null` — that is the correct answer, and
   the dashboard simply omits the chip. **`citations`
   is an array of `{text, url}` pointing to OFFICIAL, web-accessible primary sources** — ECB (SPACE study,
   Data Portal), EUR-Lex / EC pages for EU law, national central banks, named consulting reports — with their
   real public `https` URLs; for the licensed RBR reports use the Blob-served evidence viewer
   (`/api/evidence?pdf=rbr-cee-atm-2028` for CEE, `…rbr-we-atm-2028` for GR/CY/AT). **Never cite an internal
   `.md` path** (those aren't on the web). The build uses patterns_kb.json as the Patterns source (replacing
   the workbook sheet, which stays a fallback) and renumbers; the dashboard renders citations as a clickable
   "Based on:" line. A structural pattern
   is a PERSISTENT market mechanic (NOT a one-off signal, NOT a 3-5yr point
   forecast), evidence-backed, with a clear Printec implication — never duplicate the hand workbook patterns.
5d. **Maintain the INDIRECT opportunities** in `intel-cache/derived_opportunities.json` — the plays that no
   single signal states, composed from the intersection of 2+ signals from 2+ DIFFERENT agents. They are
   usually built from rows the rankings deliberately exclude: a `threat_macro` driver has no buyer, a `lost`
   row is competitor-held, an `installed_base` row is already ours — the opportunity lives in the overlap
   (e.g. a compliance obligation that attaches to the DEVICE survives losing the hardware deal; a pilot
   programme landing on a confirmed incumbent; two unrelated deadlines hitting the same estate in one
   quarter). Each cycle: re-check every existing entry against the new table (does its falsifier now fire?
   do its components still exist?), retire what has been overtaken, and add what this week's rows make
   visible. Every entry needs `buyer`, a dated `trigger`, `claim`, `why_not_visible_in_one_signal`,
   `falsifier` and `cite_signals` (component keys). **Do NOT hand-write the agent list or claim High
   confidence** — `build_dashboard.py` counts the agents from the resolved components and caps confidence at
   Medium-High, dropping any entry that fails the 2-signal / 2-agent rule with a printed reason. Read that
   output: a `derived: DROPPED …` line means the play did not survive its own evidence test. These are
   labelled DERIVED in the UI and never carry a euro value — they are analysis, not sourced deals.

6. **Build the dashboard + cache, then publish:** from `weekly-intelligence/scripts/` run
   `python run_weekly.py --root "<this folder>" --week YYYY-MM-DD`
   (needs `openpyxl`: `pip install openpyxl --break-system-packages`). This writes
   `intel-cache/*.json` (keeps `_ledger.json` for week-over-week), `intel-cache/dashboard-data.json`
   (the publishable payload), refreshes the web app's
   bundled snapshot `dashboard-web/data.json`, and — when `PRINTEC_DASHBOARD_URL` and
   `PRINTEC_UPLOAD_SECRET` are set in the environment — **publishes the data to the live Vercel
   dashboard** (POST to `<url>/api/upload`), so Kostas sees the new week with no redeploy. If those env
   vars are unset, publishing is skipped with a note and the run still succeeds. The live app is the
   `dashboard-web/` project (see `dashboard-web/README.md`).
   **REQUIRED for the live site to update — set both env vars in whatever environment runs this step**
   (the scheduled/cron runner, not just an interactive shell): `PRINTEC_DASHBOARD_URL` =
   `https://printec-market-research.vercel.app` and `PRINTEC_UPLOAD_SECRET` = the value of `UPLOAD_SECRET`
   in the Vercel project. On Windows set them persistently (`setx`) or in the runner's profile, since each
   run gets a fresh shell. The **same two vars also publish the evidence trail** — the agent source
   documents + link-rot snapshots that back every card (`publish.py` does this automatically right after
   the data POST; `--no-evidence` skips it). If the vars are missing, BOTH the data and the evidence
   silently don't reach the live site — the run still "succeeds", so confirm the publish line in the log
   says `publish: OK 200` and `publish-evidence: done`, not `publish: skipped`.
7. **Connect new → historic, then write the reasoned Outlook (this is JUDGMENT, not a math fit):** read
   the top movers against the workbook Patterns and multi-year series. Read `intel-cache/forecast.json` —
   the engine's deterministic linear baseline + the running accuracy/MAPE — but treat it ONLY as a
   reference to *argue with*. Then write **`intel-cache/forecast_narrative.json`**: a reasoned forward
   outlook per important market, weighing regulation/deadlines, competitor moves, bank programmes, macro &
   politics, and the leading indicators — and saying where you AGREE or DISAGREE with the naïve trend and
   why. The dashboard's **Outlook tab leads with these**; the math baseline is shown small underneath.
   (The **3–5 year** horizon is owned separately by **Agent 8, the Futurist**, which authors
   `intel-cache/futures_narrative.json` for the dashboard's **3–5yr Outlook** tab. Your `forecast_narrative.json`
   stays the near/mid-term view; read the Futurist's findings and weigh them where a long arc bears on a
   6–18-month call, but you do not author the 3–5yr futures yourself.)
   Format — an `{week, product_outlooks:[…], outlooks:[…]}` object. The Outlook tab now LEADS with a
   **product-direction layer** and shows the per-market calls beneath it, so write BOTH sets:
   - **`product_outlooks` — the headline. ONE outlook per Printec product line** (use the `product_map.json`
     ids + labels), answering *"where is THIS product heading across the footprint over the next 6–12 months,
     and where should Printec point it?"* On each, set `id` (the product_map id), `label` (the line name) and
     `m` (its opportunity value in €m, from the product's score); the dashboard orders by `m` and colours by `id`.
     **Cover EVERY material line — do NOT let the set skew to ATMs:** compliance, fraud, payments, digital
     identity, managed services, HSM, core/digital each get their own forward call. For a line with no real
     near-term catalyst, say so honestly ("flat — rides on the instant-payments build-out") rather than
     omitting it. (Audit finding that drove this: the old per-market outlooks were ~87% ATM-anchored while ATM
     is ~20% of opportunity value — the product layer is what makes the tab answer the question for ALL products.)
   - **`outlooks` — the per-market deal pipeline.** For EVERY active market, write its **winnable NET-NEW**
     opportunities (`Type` net_new_contest), **newest development first**, N≥2 where the market has two or more,
     else 1. An owned asset, an incumbent renewal, or an already-lost scope is **never the lead** — it renders in
     a separate **"Installed base & lost — context"** section, so do NOT make one the headline `scope`. Order by
     recency, NOT by certainty or deal size, and never assert or imply the odds of winning. Each outlook MUST set
     **`cite_signals`** to the master-table signal key(s) it is about — the dashboard inherits the outlook's lane
     (opportunity / installed_base / lost) and recency FROM those signals, so a miscite mis-routes the card.
     These render as **"Biggest near-term opportunities by market."**
   Each outlook in either set:
   `{ id (product_outlooks only — the product_map id) | country (outlooks only), scope, summary, horizon,
   direction (strong growth|growth|flat|decline|steep decline|mixed), projected, confidence (High|Medium-High|
   Medium|Low), drivers:[…], rationale }`.
   - **`oid` (required, both arrays):** give every outlook a unique integer `oid` — **unique ACROSS both
     `outlooks` and `product_outlooks`** (never reuse a number between the two; e.g. country outlooks 0..N,
     product outlooks 100..). The independent validator and the dashboard key each call's "✓ independently
     validated" verdict on its `oid`, so a collision would cross-wire two calls' verdicts.
   - **`scope` = a tight one-line HEADLINE** (≤ ~12 words). NO meta-commentary ("a footprint-level
     product-direction view…", "not a single-country deal") — the Copy rule below forbids it.
   - **`summary` = a 4–5 line HIGH-LEVEL read, in flowing prose.** This is the card's COLLAPSED subtitle, so a
     C-level reader gets the whole gist — direction + the main catalysts + where Printec should point the line —
     WITHOUT expanding. Don't repeat it verbatim in `projected`.
   - **`projected` = the full call (the EXPANDED detail), in flowing prose.** Open with the direction, give the
     catalysts, then a short **"Where to point it:"** (the specific markets / programmes / segments to chase) and a
     one-line **"Net:"** recommendation. `rationale` = the "why now". NEVER invent a precise figure not in evidence.
   **Write like a newspaper, not like notes** — flowing sentences a board member reads easily; never telegraphic
   shorthand ("Q1: rev $1.0bn +7%, recurring ~72%, …"). **Cite inside `drivers`, `rationale`, `projected` and
   `summary`** with a FULL markdown link `[label](https://…)` (or a `findings/NN-…/*.md` ref) — **never a bare
   `[label]` with no URL** (it renders as dead text). One link per claim that needs backing, not every clause.
   **Give each outlook its evidence trail — add three structured fields so a reader can trace the reasoned call to
   its sources** (the dashboard renders a per-outlook "Built on … / Evidence trail / honesty caveat" exactly like a
   signal card). THIS IS A REQUIRED PART OF WRITING EACH OUTLOOK, not an optional extra:
   - `cite_signals`: the EXACT master-table signal keys this outlook synthesizes (e.g. `["privatbank-atm-fleet-renewal"]`
     for the PrivatBank call, `["hungary-mandated-atm-rollout-…","otp-group-rising-it-spend-…"]` for the HU managed-
     services call). Use only real keys; an outlook is literally a synthesis OF specific signals, so list them.
   - `cite_files`: the EXACT `findings/NN-…/*.md` paths behind it — the agent docs you reason from plus the chosen
     signals' own cites. Optional `primary_url` = the single best canonical link for the headline fact.
   - `cite_ungrounded`: **the honesty check.** Before you finalise each outlook, re-read its own drivers/rationale
     and list any specific factual claim (a number, a named programme/event, a competitor name) that does NOT trace
     to one of the `cite_signals`/`cite_files` above — e.g. a vendor's financial health, a rollout date, a rival not
     in the signal set. `[]` if everything traces. The dashboard shows these as a small "⚠ N claim(s) not yet linked
     to a cited source" caveat on the card, so a reader knows exactly what is reasoned-in vs. sourced. Do this as the
     same discipline as the step-4b figure re-check: be your own skeptic. (An empty list because you skipped the check
     is worse than an honest non-empty one — under-claiming traceability is the failure mode to avoid.)
   The engine fills `cite_signals`/`cite_files` from your inline `(A#)` tags + the country's signals if you omit them,
   so the trail never disappears — but you must still write all three explicitly: the fallback can't know which
   claims are ungrounded, only you can. (Keep using the `(Agent N)`/`(A#)` tags in the prose too; the engine maps
   each to that agent's source document so the inline reference resolves to a clickable doc.)
   Make falsifiable calls so they can be graded; the predictions ledger (`predictions.json`) auto-grades the
   numeric baselines, and your qualitative calls compound accuracy over time. Projections/estimates are
   never sourced facts — label them as such.
   For a metric that has a statistical baseline chart (e.g. Greece ATMs/branches), you may also add an
   `overlays` array to the narrative so the chart shows your view, not just the math:
   `{country, metric, provisional:[{year,value}] (uncertain recent actuals → ◇ on the chart),
   projection:[{year,value}] (your reasoned forward value), note}`. Only add points you can ground.
7b. **Spawn the independent validator (a separate traceability audit — not you).** Once `forecast_narrative.json` is written, and BEFORE `run_weekly.py` (step 6) rebuilds the dashboard, run `Workflow({ scriptPath: "weekly-intelligence/workflows/validate-outlooks.workflow.js" })`. It re-reads each 6–12-month outlook AND each of Agent 8's 2–5-year futures against the documents they cite — independent of you, the author — and writes `intel-cache/outlook_validation.json` + `intel-cache/futures_validation.json`. `build_dashboard.py` merges both (authoritative over your own `cite_ungrounded` self-report) into the per-call "✓ independently validated" marker + "⚠ N claim(s) not yet linked to a cited source" caveat. The validator applies a paid-source/paywall policy (a claim backed by a snapshotted or knowledge-base copy of a paywalled report counts as grounded). The build warns if either file is missing/stale, so the audit is never silently skipped — run the validator (after step 7) before the step-6 build.
8. Write `weekly-briefs/YYYY-MM-DD.md` as a **board-grade note that leads with decisions, not data**:
   - **Bottom line up front (BLUF):** 2–3 sentences a CEO/CFO/CRO can read in 30 seconds — the single most
     important thing this week and the decision it forces (e.g. the Atleos/Brink's partner-vs-competitor
     question). Lead with the conclusion, not the evidence.
   - **Top 3 moves of the week:** the three freshest **winnable net-new** plays (`Type` net_new_contest,
     newest development first). For EACH: *Bank/target · Owner (who should act) · By-when · The one decision
     needed · Rough deal-size band (XL/L/M…)*. Rank by recency (then deal size) — NOT by any win/expected-value
     score, and NOT by how many agents saw them. Owned/incumbent/lost positions are not "moves to win."
   - **Then, in plain language:** the fuller opportunity list (bank, need, why-now, suggested Printec play);
     **Movements** vs. last week (the dashboard lists adds/drops/confidence changes); **Watch items** (weak
     single-agent signals needing one more confirmation — give a numeric trigger that would promote them);
     **Gaps** + next-best proxies. Explain any jargon on first use.
9. Update `glossary.md` with any new terms.
10. Do not tag product lines by hand. After this run, Agent 10 (`10-product-critic.md`) judges which Printec
    line each new or changed signal is really about and writes `weekly-intelligence/references/product_review.json`;
    `ingest.py` applies those verdicts over the keyword matcher on every build.

## Rules

- Never let a one-source claim carry High confidence.
- Every row in the master table must trace to a dated, linked source in an agent's findings file.
- Brief is for a reader NOT fluent in banking jargon — explain terms on first use.
- Never invent numbers/budgets/deadlines; the engine only classifies and does arithmetic on existing values.
- If an agent failed to run or produced nothing new, note it in the brief.
- **Copy rule (everything written for the dashboard — subtitles, outlook prose, the competition brief,
  source/figure strings):** say what a number or section IS — its meaning, unit and source. Never add
  meta-commentary about the writing ("a plain-English read of…", "labelled as forecasts") and never frame it
  as "what it is NOT" ("no time axis", "X/Y/Z are excluded"). Keep band definitions, legend keys and source
  links. **Win-probability is NOT estimated or recorded ANYWHERE — not in the table, not internally, not in
  prose** (judging the odds of winning is the sales teams' call, not market intelligence's; playbook OBJECTIVITY
  RULE). Opportunities are ordered by newest development first; deal size and confidence are context only.
- **Prose, not notes (all dashboard narrative — outlook `summary`/`projected`, the competition brief,
  competitor `latest`, pattern implications):** write flowing, newspaper-readable sentences a board member can
  skim — NOT telegraphic shorthand or scrap-paper notes ("Q1: rev $1.0bn +7%, recurring ~72%, Cashzone 14
  ctys…"). Weave figures and dates into the sentences as clauses. Where a card has a collapsed subtitle + an
  expandable body, the subtitle is a 4–5 line high-level SUMMARY (the reader gets the gist without expanding)
  and the full analysis lives in the expanded detail — never dump the whole analysis into the collapsed view.
- **Headlines are tight:** a card's `scope`/title is a one-line headline (≤ ~12 words), no trailing
  meta-clauses; the substance goes in the summary and body.
