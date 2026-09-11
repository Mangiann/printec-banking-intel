# Greece agent refresh — RUNBOOK (operator-supervised)

Prepared 2026-07-24. **Runs one step at a time, with your approval before each** (per the test-notes method).
Scope: **Greece-core, 19 units** across 5 collector agents. A4-Greece is scripted (no agent step). Nothing
publishes until you explicitly approve Step 8.

## Pre-flight (all green as of prep)
harness ✓ · agent-units ✓ · references incl. `source_access_registry.json` + `diavgeia_config.json` ✓ ·
fetch_diavgeia/verify/run_weekly compile ✓ · Tier-0 caches fresh (0d) ✓ · baseline findings + master table ✓.

## What was backed up (rollback)
`_pre-registry-backup-20260723-153255/`: `master-signal-table.md.pre-greece-run`, `data.json.pre-greece-run`,
plus the earlier script/brief originals. Findings are ADDITIVE (a new `<dir>/2026-07-24.md`), so they don't
overwrite anything. To roll back the table/dashboard, restore those two files and re-run Step 7 build.

## Open decision that affects this run
- **F5 (TED/CPV scope) is UNRESOLVED.** Agent 2 (Step 2) should NOT broaden CPV. It now also reads the new
  `intel-cache/greek_tenders_diavgeia.json` cache (below-threshold Greek tenders) — triage it for relevance.

---

## Steps

Each collector step is one `Workflow` call with the prepared args, then a review. The harness runs
Research → Verify → GapFill → Narrate → deterministic JS table, and returns `{markdown, stats}`. Write
`result.markdown` to the agent's `findings/<dir>/2026-07-24.md`; **leave any `stats.emptyAfterGapfill`
coverage warning intact.**

- [ ] **Step 1 — Agent 1 Bank Disclosures (6 GR banks).**
  `Workflow({ scriptPath: "weekly-intelligence/workflows/research-harness.workflow.js", args: <greece-refresh-run/agent1.args.json> })`
  Review the returned table + coverage; write to `findings/01-bank-disclosures/2026-07-24.md`.

- [ ] **Step 2 — Agent 2 Tenders (3 units + Diavgeia cache).** Same call with `agent2.args.json`.
  Read `intel-cache/greek_tenders_diavgeia.json` FIRST (per the updated brief), triage for relevance.
  **Do not change CPV scope (F5).** Write to `findings/02-tenders-procurement/2026-07-24.md`.

- [ ] **Step 3 — Agent 3 Regulation (6 units).** `agent3.args.json` → `findings/03-regulation-deadlines/2026-07-24.md`.

- [ ] **Step 4 — Agent 5 Jobs (1 unit).** `agent5.args.json` → `findings/05-jobs-early-intent/2026-07-24.md`.

- [ ] **Step 5 — Agent 6 Vendors (3 units).** `agent6.args.json` → `findings/06-vendors-competitors/2026-07-24.md`.

- [ ] **(A4 Greece — no step.)** EU stats incl. Greece are scripted via `fetch_ecb.py` (runs in Step 7).
- [ ] **(A8 Futurist — optional.)** `future-trends-research.workflow.js` if you want the 3–5yr layer refreshed.

- [ ] **Step 6 — Agent 7 Orchestrator (reduce).** Follow `agent-briefs/07-orchestrator.md`:
  triangulate the 5 new findings files → update `master-signal-table.md` (dedup; assign Type + Opp-size;
  lead each Date with the most-recent development), write `intel-cache/competition_brief.json` and
  `intel-cache/forecast_narrative.json`, then run the independent validator
  `Workflow({ scriptPath: "weekly-intelligence/workflows/validate-outlooks.workflow.js" })`.

- [ ] **Step 7 — Build (local, NO publish).**
  `cd weekly-intelligence/scripts && python3 run_weekly.py --root .. --week 2026-07-24 --no-publish`
  This refreshes fetches (incl. Diavgeia), ingests the new table, runs the **registry-aware verify**
  (watch for the `… bot-blocked | … repaired via registry` line), builds `dashboard-web/data.json`.
  Then review locally: restart the dev server and open http://localhost:8766
  (`cd dashboard-web && node _devserver.local.mjs`).

- [ ] **Step 8 — Publish (ONLY on explicit approval).** Set `PRINTEC_DASHBOARD_URL` +
  `PRINTEC_UPLOAD_SECRET`, then re-run Step 7 WITHOUT `--no-publish`. Confirm the log says
  `publish: OK 200` and `publish-evidence: done`. This updates the live site Kostas sees — do not do this
  until the local review (Step 7) looks right.

## Notes
- Cyprus banks (bank-of-cyprus, eurobank-cyprus, alpha-cyprus) are EXCLUDED for a pure-Greece run — add them
  to `agent1.args.json` `units` if you want the GR/CY region together.
- Expect this to span session-usage windows; each agent step is independently resumable.
