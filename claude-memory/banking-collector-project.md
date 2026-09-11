---
name: banking-collector-project
description: "Printec banking market-intelligence collector at ~/Downloads/BANKING — architecture, my promoted changes, and the registry scoped-use conclusion."
metadata: 
  node_type: memory
  type: project
  originSessionId: fac793f9-7e87-4dd9-b451-7b369c2d1f77
  modified: 2026-08-03T11:22:56.399Z
---

**Printec banking/payments market-intelligence collector** lives at `/Users/mangian/Downloads/BANKING/` (NOT the cwd `test marketing agent`, which only holds a trends memo). Operator: Kostas. Reference guide: `~/Downloads/EXTRACTION_PLAYBOOK.md` (authoritative; follow it where it conflicts with anything).

**Architecture (two layers):**
- LLM research: Agents 1–6 + 8 each call `weekly-intelligence/workflows/research-harness.workflow.js` with their slice of `weekly-intelligence/workflows/agent-units.json`; write `findings/NN-*/<date>.md`. Agent 7 (orchestrator, `agent-briefs/07-orchestrator.md`) triangulates → `master-signal-table.md`. A4-EU + A8 are scripted/checkpointed.
- Deterministic engine: `weekly-intelligence/scripts/run_weekly.py` = fetch_* → ingest → forecast → verify → build_dashboard → publish. Dashboard = `dashboard-web/` (local: `node _devserver.local.mjs` → :8766). `run_weekly.py --no-publish` builds locally without touching the live Vercel site.

**Changes I promoted (2026-07, backed up in `_pre-registry-backup-20260723-153255/`):**
- `scripts/verify.py` — registry self-heal (repairs dead cited URLs from the registry) + bot-wall detection (hard markers + thin-page reCAPTCHA guard + HTTP 202). On the real corpus ~160+ "reachable" sources were actually captcha walls.
- NEW `scripts/fetch_diavgeia.py` — Greek below-TED-threshold ΚΗΜΔΗΣ/Diavgeia tenders via OpenData `search.json?subject=` (the `q`/`query` params are DECORATION — proven). Terms/host in `references/diavgeia_config.json`. Wired into `run_weekly.py` + consumed by the Agent 2 brief.
- `references/source_access_registry.json` — 2,273-domain access map (5-country audit). SCOPED-USE conclusion from the Greece A/B: the registry helps the DETERMINISTIC layer (verify + fetch + specific-doc lookups) but gives NO gain on open-ended discovery agents — do NOT wire it into the A1/A5/A6 briefs.

**Source audits produced:** `<Country>_Banking_Payments_source_access_audit.xlsx` + `_report.md` for Greece, Albania, Bosnia, Bulgaria, Croatia (in the BANKING folder). Registry covers 5 of the 17 footprint countries.

**Harness failure mode (found 2026-07-30/31, Agent 1 run):** `research-harness.workflow.js` checkpoints **research** to `parts/<runDate>/<slug>.json` but holds **verification** only in memory. So an API session-limit kill destroys the verify stage while leaving paid-for research stranded on disk and invisible — the run then honestly reports those units `⚠ EMPTY`, which reads as "nothing happening in that market". In that run 446 researched signals across 34 units were stranded vs 164 that reached a document. **Fix not yet applied to the harness:** checkpoint verified output per unit as research already is.
- Workaround I added: NEW `weekly-intelligence/workflows/verify-checkpoints.workflow.js` — verify-ONLY pass that reads stranded checkpoints, skips re-research (far cheaper), and makes each agent write `parts/<runDate>/verified/<slug>.json` **before returning**. Recovered 22 units / 291 signals; 2 units survived *only* because of write-before-return.
- A 42-unit Agent-1 run does NOT fit one limit window (~200k tokens/unit; ~11.7M total, 4 limit hits). Run it in batches of ~12–18 and merge the rendered rows mechanically — never let an LLM re-write the table.
- **Confirmed again 2026-08-02/03 (Agent 3, 11 units):** same shape — 3 limit kills (2 session, then the WEEKLY limit), research always survived on disk, verification always died because it runs last. Third attempt after the weekly reset completed clean: 23/23 agents, 202 verified signals, `emptyAfterGapfill: []`. **A 11-unit regulation run needs ~2.2M subagent tokens and does NOT reliably fit one window.**
- Two recovery tools now live in the repo (built 2026-08-03, Agent-3 run):
  - `weekly-intelligence/scripts/render_from_checkpoints.py` — rebuilds a complete findings file from `parts/<runDate>/*.json` after ANY interrupted run. Prefers `<slug>.verified.json` over the raw checkpoint, tags each row's verification verdict, renders the regulation/signals table exactly as the harness does, and emits honest coverage + residual-gap sections. Use it to ship a floor deliverable immediately instead of waiting out a limit window.
  - `weekly-intelligence/workflows/agent3-launch-2026-08-02.workflow.js` — args-inlined launcher calling the harness via `workflow()`. **Pattern worth reusing for every agent:** it makes a retry after a limit kill a one-line `Workflow({scriptPath})` with no giant args payload to resend, and the harness's STEP-0 checkpoint resume then replays finished units cheaply.

**Open:** F5 (TED CPV scope) unresolved — don't broaden CPV. Agent 1 `2026-07-30.md` is at 34/42 banks — Montenegro, North Macedonia and all 6 regional-group units (Erste, KBC, RBI, OTP/Intesa/NLB/UniCredit, Addiko, ProCredit) still owed, so per-country fleet figures are un-cross-checked against group disclosure. See [[pos-paper-roll-order-project]] for the unrelated other project.
