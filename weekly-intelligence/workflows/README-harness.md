# Research harness — reliability rebuild (2026-06-24)

## Why this exists
On 24/06/2026 an exhaustive Agent-1 run *looked* complete (workflow reported success, 465 verified signals) but had **silently dropped whole markets** (Bosnia, Montenegro, North Macedonia). Forensics showed the cause was **not** agent failure or page-access problems:

- 100 of 102 agents succeeded; **zero API errors**; the "ended before completion" reds in the UI were a mid-run snapshot (concurrency cap ~16).
- The data for the missing markets **was researched and verified** — it reached the final step.
- The **final synthesis LLM was asked to hand-write a ~465-row table in one response, hit its output ceiling, and truncated ~70% of the rows.** Small markets lost the cut. The synth's own "coverage gaps" section didn't notice.

So the failure mode to engineer out is **silent omission in the reduce step**, not agent reliability and not Chrome access.

## The fix — `research-harness.workflow.js`
A single shared harness that every collector agent (1–6) calls. Three guarantees:

1. **Deterministic render.** The signal table is built in **JavaScript** by mapping over the verified signal objects (`renderTable`). No LLM renders the table, so it can never be truncated or silently shortened. The LLM only writes the short "What changed" + "Top opportunities" prose.
2. **Completeness gate.** After research→verify, any unit that returned **zero** signals (or whose agent died → null) is retried via gap-fill, up to 2 rounds. If still empty, the file carries an explicit **⚠ COVERAGE WARNING** and `stats.emptyAfterGapfill` lists it. A run can no longer "succeed" with a silently-empty unit.
3. **Per-unit checkpoint.** Each research agent also writes its part to `findings/<dir>/parts/<runDate>/<slug>.md` for audit/recovery.

Pipeline: `Research` (one agent per unit, schema-constrained) → `Verify` (adversarial per-claim fact-check) → `GapFill` (completeness loop) → `Narrate` (bounded prose) → deterministic JS assembly → returns `{ markdown, stats }`.

The deterministic assembly renders, in order: the bounded narrative, the open-tender pipeline (tenders only), the **signal table**, **verification notes** (contradicted/unconfirmed), an **"Access issues & operator requests"** section (the research agents' per-unit `access_issues`/`operator_requests`, which `Verify` discards — captured separately so the operator's manual to-do list and the blocked-source log survive), and the honest **per-unit coverage table**.

## How an agent uses it
The collector SKILL.md files do:
1. Read playbook + brief + previous findings (summarise the baseline).
2. Read `agent-units.json` → the object under this agent's number = the fan-out work-list (`unitNoun`, `tableKind`, `findingsDir`, `units[]`).
3. Augment `units` with anything newly discovered this run (never drop a unit for being small).
4. Call `Workflow({ scriptPath: ".../research-harness.workflow.js", args: { ...config, runDate, prevSummary, units } })`.
   - **`args` may arrive as a JSON string.** The Workflow TOOL boundary serializes the `args` object to a string (verified 24/06/2026 — a passed object reaches the script as `typeof args === "string"`). The harness now **parses a stringified `args`** at the top, so this direct-args call works as written — **no launcher script is needed.** (A parent that calls the harness via the in-script `workflow(scriptPath, obj)` hook passes a real object; the harness handles both.)
5. Write the returned `result.markdown` to `findings/<dir>/<runDate>.md` (clean UTF-8; no entity-decoding needed because JS rendered it).
6. Sanity-check `stats.emptyAfterGapfill` — leave any coverage warning intact.

`productContext` and `rules` default inside the harness, so the SKILL doesn't have to pass them.

## Work-lists — `agent-units.json`
One source of truth for "what entities each agent fans out over." Edit there to add/remove a bank, portal, competitor, regulation workstream, market, or country. Keys `1`–`6`; `_shared` holds the Printec offer map.

## Scope
- **Agents 1, 2, 3, 4 (non-EU), 5, 6** → use the harness.
- **Agent 4 (EU counts)** stay **scripted** (`scripts/fetch_ecb.py`, Tier 0) — the harness only covers the non-EU markets the ECB portal can't.
- **Agent 8 (Futurist)** already uses `future-trends-research.workflow.js`, which is checkpoint-resilient and whose synthesis is built downstream by `run_weekly.py`/Python (deterministic) — it does **not** have the truncation problem, so it's left as-is.
- **Agent 7 (Orchestrator)** is a **reducer**, not a collector. Its determinism is already in `build_dashboard.py` (Python). Its SKILL adds a **completeness check**: confirm it ingested the latest findings file from every source agent before publishing.

## Tests
`research-harness.workflow.js` was validated end-to-end against stubbed agents (a temp Node harness): deterministic render with pipe/newline escaping, value-ordering, the gap-fill loop recovering an empty unit, and the coverage warning firing for a unit that stays empty.
