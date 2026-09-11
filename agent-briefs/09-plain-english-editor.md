# Agent 9 — Plain-English editor

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.


**Runs after the weekly Orchestrator (Agent 7) has written its outputs and BEFORE the dashboard is
rebuilt and published.** It is an editing step, not a research step. It changes wording only. It never
adds, removes or changes a fact.

The other agents' briefs are untouched. They write as they always have; this agent rewrites what
readers will see into plain English (decision of 09/09/2026).

Order in the week: Agent 7 (Orchestrator), then Agent 10 (the product-line critic, `10-product-critic.md`),
then this agent. Agent 10 rebuilds but does not publish; this agent publishes.

## What it edits

Every reader-facing text the dashboard shows:

| File | Fields |
|---|---|
| `master-signal-table.md` | the Signal, What it implies and Recommended follow-up cells of the rows dated this week |
| `intel-cache/forecast_narrative.json` | outlooks and product outlooks: summary, projected, rationale, drivers |
| `intel-cache/futures_narrative.json` | futures cards (projected, rationale, drivers); board items (money, competition, threats, timeline); bottom line |
| `intel-cache/patterns_kb.json` | pattern, evidence, implication |
| `weekly-intelligence/references/competitors.json` | latest |
| `intel-cache/derived_opportunities.json` | claim, why_not_visible_in_one_signal, falsifier, trigger |
| `intel-cache/competition_brief.json` | brief |
| `intel-cache/signal_projections.json` | mechanism, judgement, contrast, anchors |

## The rules (the same rules every rewrite must pass)

1. Keep every number, percentage, money amount, date, year, count, name and URL exactly as written.
2. Keep every markdown link; the link text may be simplified, the URL may not change.
3. Short sentences, one idea each, everyday words, active voice. Explain jargon in a few words the first
   time it appears. Do not remove the technical term.
4. Same facts, same order, same structure. Similar or shorter length. British spelling.
5. Table cells: no `|`, no line breaks. Patterns: every rate phrase (`~3-4%/yr`, `Hungary +18.6%`,
   `GROWING — …; STABLE — …; DECLINING — …`) stays word for word — the engine reads them.

The model to follow — tone and level — is the Croatia text in `STYLE.md`, which `plain_batches.py`
writes into the work folder on every run.

## How to run it

```
python3 weekly-intelligence/scripts/plain_batches.py --root <BANKING> --work <workdir> --since <Monday of this week>
```
This writes `<workdir>/items/batchNN.json` (originals), `manifest.json` and `STYLE.md`. `--since` limits
the master-table rows to this week's; every other file is small and is always included in full.

For each batch: read `STYLE.md` and the batch file, rewrite every field of every item, and write
`<workdir>/out/batchNN.json` as a JSON array of `{"id", "fields"}` with the same ids. Batches are
independent — fan them out in parallel (one agent per batch).

Then:
```
python3 weekly-intelligence/scripts/plain_merge.py --root <BANKING> --work <workdir>
```
This checks every field with `plain_check.py` and writes back **only** the fields that kept every number,
date, money amount and link. Anything that lost a figure is left as it was and listed in
`<workdir>/failed.json`. Redo those (same rules) and merge again; after two passes, leave what still fails
in its original wording and say so in the run note.

Finally rebuild and publish exactly as the Orchestrator does: `build_dashboard.py`, then
`python3 weekly-intelligence/scripts/plain_lint.py --data intel-cache` (the writing check — fix what it
lists if it is more than a handful, then rebuild), then `weekly-intelligence/scripts/artifact/build_artifact.py`,
then republish the artifact. Put the lint summary in the run note.

## What it must never do

- Change a figure, a date, a name or a link. The checker will refuse the field; do not work around it.
- Touch any file not listed above, or any agent brief.
- Publish without running the checker.
