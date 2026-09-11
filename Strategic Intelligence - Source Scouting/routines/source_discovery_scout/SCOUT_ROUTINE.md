# Scout Routine — run ONE full source-discovery round

## ✅ THE ONE-COMMAND WAY (deterministic orchestrator — prefer this)

Run the whole round with a **single Workflow call**. The orchestrator's control flow is CODE — it runs all
six phases (discover → ingest → repair → prepare-labels → label → finalize) in fixed order; **no agent decides
what runs or can skip a stage**. Only what discovery *finds* varies.

**URL recovery is a mandatory, layered ladder — never a silent no-op.** A HEAD check calls ~5× more URLs
"dead" than really are (403 = bot-defended-but-live, 405 = HEAD-refused, 429 = we were impolite, timeout =
slow). So every failed URL is walked down a ladder: **(1) a plain GET and (2) a WAF-handshake retry run
automatically as CODE inside `ingest`** (no browser, no agent); **(3) an agent then does everything else —
web search + a real Chrome** — over only what code could not settle. **If there are still-unreachable URLs and
Chrome cannot be reached, the round HALTS and drops an `ACTION NEEDED` file into `deliverables/`** rather than
silently shipping false-deads (that silent skip once locked ~1,381 live sources out of the registry). Whatever
survives the whole ladder goes onto a **`<Country> - Sources to check by hand.xlsx`** for a human, who fixes
the links and hands it back to `scripts/apply_manual_url_checks.py`.

```
Workflow({ scriptPath: "routines/source_discovery_scout/full_round_workflow.js",
           args: { run_id: "dr_gr_a2_live_004",
                   config_path: "configs/discovery_runs/gr_a2_tenders_procurement.yaml",
                   promotion_db: "data/promotion.db",
                   country: "GR", country_name: "Greece", sector: "both",
                   workstreams: ["A2"], topics: ["tenders","procurement"], languages: ["el","en"] } })
```

Prereqs: a connected **Chrome** (claude-in-chrome) for the repair phase. If a phase snags, everything is
checkpointed — `python scripts/round_status.py --run-id <id>` shows where to resume. Under the hood it calls
the two AI swarms (`discovery_workflow.js`, `labeling_workflow.js`, which write their output to disk as
slices) and the two deterministic Python commands (`round_ingest.py`, `round_finalize.py`).

The numbered steps below are the SAME pipeline, decomposed — use them only to run/resume a single phase by hand.

---

**Purpose (manual mode).** The steps below let an agent run (or resume) a round stage-by-stage from the INPUTS.
The orchestrator above runs them for you in fixed order; this section is the fallback / per-stage reference.

---

## INPUTS (the only thing that changes)

| input | example | notes |
|---|---|---|
| `run_id` | `dr_gr_a2_live_003` | unique per round; convention `dr_<country>_<ws>_live_<NNN>` |
| `config` | `configs/discovery_runs/gr_a2_tenders_procurement.yaml` | defines country / sector / workstream / topics / languages |
| `promotion_db` | `data/promotion.db` | the registry (used for novelty + the final promote) |

That's it. Everything below is derived from these three.

### TOKEN SAFETY / RESUME (never lose a session's work to the 5-hour window)
Every stage writes a durable artifact, and heavy discovery runs in the **background** (it survives session
interrupts — proven on round 1). So a usage-window hit never loses work. To see exactly where a round stands
and what to run next, in ANY session:
```
python scripts/round_status.py --run-id <run_id>
```
It prints each stage DONE/PENDING and the resume command for the first pending stage. The deterministic
stages are **idempotent** — re-running resumes, it never re-charges finished work. The discovery engine is
also **budget-aware**: pass a `+Nk` token target and it scales the scout fan-out to fit instead of dying
mid-run. So: if you hit the wall, just re-open this routine, run `round_status.py`, and continue.

### PREREQUISITES (environment, not per-run inputs)
- Run from the project root. Python 3 with `jsonschema` + `openpyxl` importable.
- **Greek/Unicode:** every Python call must set `PYTHONIOENCODING=utf-8` (Windows console is cp1252).
- **The `repair` phase needs a live Chrome** with the `claude-in-chrome` extension connected — but only when
  the CODE recovery rungs (which run first, inside `ingest`) leave something still unreachable. You no longer
  have to remember this: if Chrome is needed and not connected, the round **stops itself and writes an
  `ACTION NEEDED - ... .txt` into `deliverables/`** telling you to connect Chrome and re-run (it resumes,
  skipping discovery/ingest). It will **never** quietly proceed without the browser rung — that is the exact
  failure this design removed.

---

## STEP 0 — read the config, set variables
Read the `config` YAML. Extract `country`, `country_name`, `sector` (`both` = banking AND payments),
`workstreams`, `topics`, `languages`. Build the args object for the discovery engine (JSON) — include
`run_id` + `data_root` so the scouts know where to write their slices:
```json
{ "country":"GR", "country_name":"Greece", "sector":"both",
  "workstreams":["A2"], "topics":["tenders","procurement"], "languages":["el","en"],
  "run_id":"<run_id>", "data_root":"<abs path to data/>" }
```

## STEP 1 — DISCOVERY (agent: multi-agent swarm)
Run the saved engine, passing the args from step 0:
```
Workflow({ scriptPath: "routines/source_discovery_scout/discovery_workflow.js", args: <args object> })
```
It plans the landscape into coverage cells and runs one deep bilingual scout per cell. **Each scout WRITES its
findings to a slice file** in `data/run_logs/<run_id>/agent_inputs/scout_slices/` (the engine returns only a
small ack: how many scouts wrote, ~candidate count). Nothing to save by hand — the payload is already on disk.

## STEP 2 — INGEST + HEAD-verify (deterministic, ONE command)
```
PYTHONIOENCODING=utf-8 python scripts/round_ingest.py \
  --run-id <run_id> --config <config> --promotion-db <promotion_db>
```
`round_ingest.py` merges the slices → `scout_output.json`, runs normalize + runner (validate, HEAD-verify
every URL, de-dup, count), writes `data/source_candidates/<run_id>.jsonl`, and then writes `failed_urls.json`
(input to step 3) + the `label_batches/` (input to step 4). A malformed slice is skipped, never fatal.

## STEP 3 — BROWSER LINK-REPAIR (agent: real Chrome — DO NOT SKIP)
The HEAD check over-reports "dead" ~5× (WAFs, JS challenges, moves). Recover the real ones.
Read `data/source_candidates/<run_id>.jsonl`; collect every candidate whose `url_verification.status` is
`failed` (its `candidate_id` + `source_url`). Spawn ONE recovery agent (it needs the Chrome MCP):
```
Agent({ subagent_type: "general-purpose", description: "browser URL recovery",
  prompt: "<the recovery-agent prompt below, with the failed list pasted in>" })
```
**Recovery-agent prompt (fixed):**
> You have a real Chrome via the `claude-in-chrome` MCP (load its tools with ToolSearch
> `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp`).
> Read `data/run_logs/<run_id>/agent_inputs/failed_urls.json`. For EACH url walk the recovery ladder
> (playbook §"Source liveness & recovery"): (1) open it, wait for it to settle, read the page — a
> 403/timeout/challenge that then renders is **live** → `outcome:"verified"`; (2) if 404, read the site root
> nav/sitemap for the moved path → `"repaired"` + corrected_url; (3) if a section was retired, use the site's
> search → `"repaired"`; (4) if the whole entity is in doubt, research the organisation by name for a
> rename/merger/successor → `"repaired"` to the live successor URL, else `"dead"` + grade + successor.
> **WRITE a TOP-LEVEL JSON ARRAY** (not wrapped in any key) to
> `data/run_logs/<run_id>/agent_inputs/recovery_results.json`, one object per candidate_id:
> `{"candidate_id","outcome":"verified|repaired|dead","corrected_url":"<if repaired>",
> "grade_of_dead":"moved_unknown|rebranded|merged|wound_down|defunct","successor":{"name","url"},
> "ladder_step":1-5,"evidence":"one line"}`. NEVER solve a CAPTCHA — mark that url `dead`, evidence
> "captcha → human". NEVER mark verified without actually rendering the page. (Field names must be exactly
> `outcome` and a top-level array — that is what `recovery.py` reads.)

## STEP 4 — LLM LABELING (agent: multi-agent swarm)
Run the saved labeling engine on the batch files `round_ingest.py` wrote:
```
Workflow({ scriptPath: "routines/source_discovery_scout/labeling_workflow.js",
           args: { batch_files: [<abs paths of data/run_logs/<run_id>/agent_inputs/label_batches/*.json>],
                   scope: "<country> - banking AND payments - <ws> - <topics>",
                   run_id: "<run_id>", data_root: "<abs path to data/>" } })
```
Each batch agent judges its candidates — a **role** (keep / fold_into_parent / evidence_not_source /
pointer_once / marginal) and a **decision** (approve / needs_access / reject / defer) — and **writes its labels
to a slice file** in `agent_inputs/label_slices/`. Recommendations only; code + humans still decide.

## STEP 5 — FINALIZE (deterministic, ONE command)
```
PYTHONIOENCODING=utf-8 python scripts/round_finalize.py \
  --run-id <run_id> --config <config> --promotion-db <promotion_db>
```
`round_finalize.py` merges the label slices → `role_verdicts.json` + `decision_suggestions.json` (clamped by
`prelabel.normalize_roles`/`normalize_suggestions`), runs the full pipeline (folds in the browser recovery +
roles + suggestions → machine artifacts + the ONE master-list deliverable in `deliverables/`), **syncs** the
run into the registry (safety-gated: a source goes **active** only if public + legally allowed + verified,
else **paused**), and prints the **convergence report** `{ total, new, seen_prior_run, in_registry }` vs every
prior run + the registry (`new` = genuinely novel URLs — the convergence signal). Human review of the Excel is
OPTIONAL; the LLM defaults populate the registry with or without it.

---

## What the next agent needs to know: NOTHING but the INPUTS.
Give it `run_id`, `config`, `promotion_db`, confirm Chrome is connected. Prefer the one-command orchestrator at
the top; the numbered steps are the per-stage manual fallback.
