---
name: printec-market-research
description: Run one full source-discovery scout round for a country + sector from a plain-English request, e.g. "/printec-market-research Banking and payments in Greece". Parses the request, builds the run config, launches the deterministic orchestrator, and produces a distinct master Excel per country/sector set. Use when the user invokes /printec-market-research with a country/sector description, or asks to scout/find sources for a market.
---

# Printec Market Research — source-discovery scout

Invoked as `/printec-market-research <plain-English request>` (e.g. *"Tenders in Greece"*, *"Senior hires at
Bulgarian banks"*, *"Payment regulation in Serbia"*). Run ONE source-discovery scout round for **exactly what
the request says**. The research is one of a **fixed set of 7 workstreams** (below); the country is anything.
Data is stored **per country** — one registry + one Excel per country, with each source tagged by workstream.

## Step 1 — parse the request into (country, workstream)
- **country** — whatever country they name. **ANY country is allowed; none is off-limits.** From your own
  knowledge give its ISO-2 code and primary local language(s) — e.g. Greece → `GR`/`el`; France → `FR`/`fr`;
  Austria → `AT`/`de`; Serbia → `RS`/`sr`. Global/cross-country → `ZZ`/`en`.
- **workstream** — map their words to exactly ONE of the fixed researches (the code, from `research_plan.yaml`):

  | If they ask about… | workstream |
  |---|---|
  | disclosures, annual reports, investor/earnings, press releases | **A1** |
  | tenders, procurement, public contracts, bids, award notices | **A2** |
  | regulation, supervisors, central-bank rules, consultations, deadlines | **A3** |
  | market statistics, card/payment/cash/ATM/POS data, adoption | **A4** |
  | jobs, hiring, leadership/management moves, org changes | **A5** |
  | vendors, competitors, case studies, partners, product/conference moves | **A6** |
  | future trends, forecasts, analyst/consulting/academic outlook | **A8** |

  The workstream's search topics are fixed by its definition — you don't supply them. If the request clearly
  fits none of the 7, ask the user which research they mean.

**Geographic scope.** For **A1–A5** the scope is the country. For **A8 (trends)** — and the two supra-national
slices — the scope is a geographic LENS, not a country (pass the scope code as `--iso` with `--languages en`):

| The request is about… | scope (`--iso`) + workstream |
|---|---|
| worldwide trends | `GLOBAL` + A8 |
| European / EU trends | `EU` + A8 |
| our region / CEE / the Balkans trends | `CEE` + A8 |
| US trends | `US` + A8 |
| Asia / APAC trends | `APAC` + A8 |
| EU-wide regulation & deadlines | `EU` + A3 |
| global vendors / competitors | `GLOBAL` + A6 |

If a trends request names no scope, ask which lens (or default to `GLOBAL`). For A1–A6 country research, if the
request names no country, ask which. Sector is always banking **and** payments (`both`) — you don't ask.

## Step 1b — is this country ours to run?

Read `data/campaign_assignment.json` and check the parsed country is in its `scopes` list. That file names
the scopes THIS machine owns; the others are being scouted on a second machine right now. This skill builds
a run config directly, so — unlike the scheduled campaign — **nothing here blocks an unowned country.**

If the country is not listed, say so plainly and ask before going further: *"<Country> is assigned to the
other machine. Running it here would repeat a ~40-minute round and both copies would write the same
spreadsheet. Run it anyway?"* Proceed only on an explicit yes. Never edit the assignment file to make the
question go away.

## Step 2 — build the run config (deterministic)
```
PYTHONIOENCODING=utf-8 python scripts/scout_config.py --iso <ISO2> --country-name "<Country>" --languages "<local codes, comma-sep>" --workstream <A1|A2|A3|A4|A5|A6|A8>
```
It prints a JSON with `country, country_name, workstream, workstream_label, topics, languages, run_id,
config_path, promotion_db, data_root, deliverable_name`. The `promotion_db` is the **per-country** registry
(`data/registries/<ISO>.db`) and `deliverable_name` is the **per-country** Excel — so every workstream for a
country accumulates into the same country registry/Excel, tagged by workstream. Any country is accepted.

Tell the user, in one line, what you parsed: the country + workstream (e.g. "Greece · A5 Jobs"), the `run_id`,
and the Excel that will grow (`deliverable_name`) — so they can catch a misread. This is a heavy (~40 min) run.

## Step 3 — check Chrome
The browser link-repair phase needs a connected Chrome (claude-in-chrome). Call
`mcp__claude-in-chrome__list_connected_browsers` (load it via ToolSearch if needed). If none is connected, tell
the user to connect the extension; you may still proceed — that one phase will be flagged to finish later.

## Step 4 — launch the deterministic orchestrator
Pass the JSON from step 2 as the Workflow args (it already contains every field the orchestrator needs):
```
Workflow({ scriptPath: "routines/source_discovery_scout/full_round_workflow.js", args: <the step-2 JSON> })
```
The orchestrator runs all five phases in FIXED order — discover → ingest → browser-repair → label → finalize.
Its control flow is code; no stage can be skipped. It runs in the background; you'll be notified when it finishes.

## Step 5 — report
When it completes, report to the user: the **deliverable Excel** (`deliverables/<deliverable_name>`), the
**convergence numbers** (`new / seen_prior_run / in_registry`), and how many sources are now in that set's
master list. If a phase snagged, run `python scripts/round_status.py --run-id <run_id> --promotion-db <promotion_db>`
and tell the user the resume command.

## Notes
- **Any country; the research is one of the fixed 7.** No country whitelist. The 7 workstreams (A1–A6, A8)
  are the canonical researches from `research_plan.yaml` — wording maps to a code, never free text.
- **Storage is per country.** One registry `data/registries/<ISO>.db` and one Excel
  `deliverables/<Country> - Banking & Payments Sources.xlsx` per country; every workstream for that country
  accumulates there, **tagged by workstream** (a column). The globe reads one DB per country.
- **`research_plan.yaml`** is the full work queue (country × workstream). Work a few sets per 5-hour window;
  each run persists independently so a window cutoff never loses more than the one in-flight run.
- **Run again to grow a set.** Re-invoking the SAME (country, workstream) appends a new run (auto-incremented run_id) to that
  set's master Excel — it does not overwrite.
- **The pipeline is deterministic**; only what discovery *finds* varies. Full mechanics: `docs/HOW_THE_SYSTEM_WORKS.md`.
