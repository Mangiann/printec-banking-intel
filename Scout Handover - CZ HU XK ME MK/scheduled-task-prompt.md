# The scheduled-task prompt (copy this text verbatim)

This is the instruction the automation follows every time it wakes up. It is written for a fresh session
with no memory of anything, so it repeats everything it needs.

Create the task with `taskId: scout-campaign-step`, `cronExpression: 13,43 * * * *` (twice an hour), and the
description:

> Every ~30 min: run one source-scouting round for the next pending set assigned to this machine (CZ, HU,
> XK, ME, MK), then stop. Skips while busy; resumes partial rounds.

---

## Prompt text

Run ONE step of the banking-&-payments source-scouting campaign, then STOP (exactly one set per firing). Work in the project directory that contains `scripts/campaign.py`. Put `PYTHONIOENCODING=utf-8` on EVERY python/bash command so non-English text prints without crashing (Czech, Hungarian, Albanian, Macedonian and Serbian Cyrillic) — this is ONLY terminal character-encoding and has NOTHING to do with the search language. Search languages come from the descriptor's `languages` field, set per country (Czech Republic → cs,en; Hungary → hu,en; Kosovo → sq,sr,en; Montenegro → sr,en; North Macedonia → mk,en).

STEP 1 — GET THE NEXT SET
Run: `PYTHONIOENCODING=utf-8 python scripts/campaign.py --next`
- If it prints a line containing `"error"` and exits non-zero: this machine's assignment file is missing, empty or wrong. Do NOT try to work around it and do NOT run any country. Report the message to the user and STOP.
- If it prints `{"done_all": true, ...}`: every country assigned to this machine is finished. Report that and STOP — do nothing else. The other countries in `research_plan.yaml` belong to the main Printec machine and must NOT be run here.
- Otherwise it prints a JSON descriptor with keys: scope, workstream, workstream_label, run_id, discovery_args, ingest_cmd, label_batch_dir, labeling_scope, finalize_cmd, complete_cmd, deliverable. Use these values EXACTLY as given. (If it has `"resumed": true`, this set was interrupted before — the same run_id resumes.)

STEP 2 — RUN ONE SCOUT ROUND
Let SLICES = `<data_root>/run_logs/<run_id>/agent_inputs/scout_slices` (data_root and run_id are in discovery_args).
(a) DISCOVERY: if SLICES already contains one or more `.json` files, SKIP this and go to (b). Otherwise launch and WAIT for completion:
    Workflow({ scriptPath: "routines/source_discovery_scout/discovery_workflow.js", args: <the descriptor's discovery_args object, verbatim> })
    (It writes ~28 scout slice files to SLICES. It runs ~40 min in the background — wait for the completion notification before continuing.)
(b) INGEST: if `data/source_candidates/<run_id>.jsonl` already exists, skip; otherwise run the descriptor's `ingest_cmd` exactly (a python command; ~10 min — it checks every URL). Wait for exit 0. It writes the candidates and the label batches.
(c) LABELING: if the folder `<data_root>/run_logs/<run_id>/agent_inputs/label_slices` already has `.json` files, skip; otherwise list the `.json` files in the descriptor's `label_batch_dir` (ABSOLUTE paths), then launch and WAIT:
    Workflow({ scriptPath: "routines/source_discovery_scout/labeling_workflow.js", args: { batch_files: [<those absolute paths>], scope: "<descriptor's labeling_scope>", run_id: "<run_id>", data_root: "<data_root from discovery_args>" } })
(d) FINALIZE: run the descriptor's `finalize_cmd` exactly. It merges labels, routes, syncs into that country's register (`data/registries/<SCOPE>.db`), and prints a convergence object.
Do NOT run any browser / claude-in-chrome recovery — it is unavailable in a scheduled run and is batched separately later.

STEP 3 — MARK DONE
ONLY if finalize succeeded (printed a convergence object, exit 0), run the descriptor's `complete_cmd`. If ANY stage failed, do NOT run complete_cmd (so the next firing resumes this same set) — report which stage failed and STOP. If `complete_cmd` itself is refused with an `"error"` about assignment, report it and STOP; never edit `data/campaign_assignment.json` to get around a refusal.

STEP 4 — REPORT + STOP
Report: the set (scope + workstream_label), the run_id, the convergence numbers from finalize, and the remaining count from `PYTHONIOENCODING=utf-8 python scripts/campaign.py --status`. Then STOP. Do not start another set — exactly one set per firing.
