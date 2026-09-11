# Source-Access Registry Adapter — STAGED TEST (not wired to production)

**Status:** staging only. Nothing here is read by the live collector. This folder is copies/new files, per the test HARD RULE — no production file (`agent-units.json`, `agent-briefs/*`, `weekly-intelligence/scripts/*`) was touched.

**Generated:** 2026-07-22 · **Owner to review:** Kostas

## What this is

A validated **source-ACCESS layer** for the collector, built from the 5 audited source workbooks (Greece, Albania, Bosnia & Herzegovina, Bulgaria, Croatia). It answers, per source, *how to reach it and how to collect it* — the one thing `agent-units.json` (which only says *what entities* to research) never had.

- `source_registry.json` — all **2,273 domains → 7,077 sources**, domain-keyed, with route/endpoint/cadence/reliability.
- `source_registry_A1.json … A6.json` — the same, **pre-sliced per workstream/agent**, so each agent loads only its slice.

Route tiers (by source volume): **1-api 29% · 2-download 21% · 3-html_scrape 32% · 4-browser_session 13% · 5-manual 5%.** Half of all sources are on tested API/download routes.

## How to wire it (proposed — apply in a test copy, then decide)

1. Copy `source_registry.json` + the `A#` slices into a **test copy** of `weekly-intelligence/references/`.
2. Add the snippet below to each agent brief (`agent-briefs/01…06`), swapping `A1`/`1` for that agent's workstream/number. This is the only brief change; it is additive (agents still free-search on top).
3. Run the **controlled Greece interactive baseline** and compare coverage/run-time against the current as-is run.

### Brief snippet to add (per agent — example shows Agent 1 / A1)

> **Validated starting sources (load first).** Before free-searching, read your slice
> `weekly-intelligence/references/source_registry_A1.json`. It lists the domains we have already
> access-tested for your workstream, each with a `route_tier`, a tested `api`/`download` endpoint, a
> `recommended_method`, a `cadence`, and a `reliability` flag. **Start from the `1-api` and `2-download`
> entries** (cheapest, already reproducible) using the given endpoint; use `3-html_scrape` entries at the
> `best_url`, not the homepage. `4-browser_session` entries need Chrome (JS/anti-bot); `5-manual` entries
> go to the manual queue. Treat a `reliability: recheck` entry as unconfirmed — re-test before relying on it.
> This is a **floor, not a ceiling**: after working the validated list, keep discovering new sources and
> propose additions (feeds the F2 source-discovery census).

## Limitations (read before promoting)

- **Coverage: 5 of 17 footprint countries** (GR, AL, BA, BG, HR). The other 12 — including the ECB-covered
  CY, AT, SI, SK, RO, HU, CZ that `fetch_ecb.py` already pulls statistics for — have **no source workbooks**,
  so they are absent here. Expanding the registry to them requires building those countries' source lists
  first (a discovery run); it cannot be fabricated.
- **Reliability is mostly unverified.** 91 domains were live-checked (verified), 1 flagged `recheck`; the
  other ~2,172 carry the audit's finding but were not independently re-hit. A broader verification sweep
  should precede a full production run.
- **Access ≠ relevance.** The registry confirms how to reach a source, not that its content is on-topic;
  a relevance pass is still needed (some live endpoints are generic feeds).
- **F5 unresolved.** Do not use this to change the TED/CPV tender scope — that decision is still open.
- **Do not auto-edit production.** Promotion from this test folder to `references/` is a human decision.

## Baseline result & SCOPED-USE conclusion (post-baseline, 2026-07-23)

The 16-unit Greece baseline (real `agent-units.json` units, control vs treatment-v2) **overturned the pilot's blanket-win story.** On open-ended unit intelligence the registry gave NO efficiency gain: same findings (58 vs 58), MORE tool-calls (215 vs 195), MORE searches (110 vs 98), and a LOWER primary-source rate (55% vs 64%); only marginal wins (16/16 vs 15/16 covered, 5 fewer dead-ends).

**Why: the registry's value is task-shaped.**
- **Deterministic lookups** (a specific figure / document / tender via a known source) → big win (pilot: −76% searches; worked-examples −79% fetches). PROVEN.
- **Open-ended discovery** (A1 disclosures, A6 vendors — "what moved this quarter") → little/no gain, because the signals live in dispersed press/trade media the registry does not enumerate; the freshness guard even ADDED searches.

**So DO NOT wire the registry as a mandatory front-end to the discovery agents.** Use it only where proven:

| Wire the registry IN (deterministic) | Leave free-search (discovery) |
|---|---|
| A4 statistics (extends the scripted `fetch_ecb.py`) | A1 bank disclosures |
| A2 tender **API queries** (TED/Diavgeia worked-examples) | A6 vendors/competitors |
| `verify.py` trust pass — resolve/repair a cited URL | A5 early-intent |
| any "fetch THIS specific doc/figure" step | |

## Scoped promotion path

1. Promote `source_access_registry.json` into `references/` as a **reference for the deterministic scripts + verify.py**, NOT as an agent-brief front-end.
2. Apply the registry ONLY to the deterministic layer (see the file-change list below / in the session notes). Keep the discovery-agent briefs unchanged.
3. Widen live verification (raise `verified` share) and stand up the rotating URL health-check (link-rot is real — a registry URL 404'd).
4. Separately, commission source workbooks for the missing footprint countries (coverage still 5/17).

## v2 changes (post-pilot, 2026-07-23)

Driven by the 12-task Greece A/B pilot (registry cut discovery searches −76% and tool-calls −22%, but exposed two failure modes):

1. **Worked-example queries added** to 13 API-tier domains (ECB SDMX series-keys, TED POST body, Diavgeia `subject=` param [q/query are ignored — pilot lesson], KIMDIS, Workable, EUCLID, HNB, ATHEX, BoG DCAT). Agents use `worked_example` verbatim, which erases the API query-tuning fetch blow-ups seen on the tender/stats tasks.
2. **Freshness guard added to every brief snippet.** The registry is the access ROUTE, not proof of latest — in the pilot an agent reported a bank's Q3-2025 results as newest while Q1-2026 existed. Snippet now mandates a newest-first + fresh-search confirmation for any dated item, and an HTTP-200 check before citing (a registry URL 404'd in the pilot).

Still open: widen live verification (raise `verified` share), add source workbooks for the 12 missing footprint countries, and stand up the rotating health-check for URL rot.
