# Agent 10 — Product-line critic

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.

**Runs after the weekly Orchestrator (Agent 7) has written the master table and BEFORE the dashboard is
rebuilt.** It is a judging step, not a research step. It decides which Printec product line or lines each
signal is really about. It never changes the signal itself.

## Why it exists

`ingest.py` tags a signal with every product category whose keywords appear anywhere in its text. A long
row that mentions ATMs, POS, onboarding and DORA in passing therefore lands in six or seven categories,
most of them not what the row is about. That spreads a signal across product pages, product counts and the
signal-based projections where it does not belong (raised 09/09/2026).

The critic reads the whole row and keeps only the lines it creates demand for, or directly changes the
market of: one lead line, at most three in total. Its verdicts live in
`weekly-intelligence/references/product_review.json`. `ingest.py` applies them on every run, so the
critic only needs to judge signals it has not seen, or whose text changed since its last verdict.

## What it judges

Every signal in `intel-cache/signals.json` without a current verdict. `product_critic.py batches` picks
them out; it compares a hash of the signal text with the hash stored beside each verdict.

## The rules

1. Read the whole row: the theme, the signal, what it implies and the recommended follow-up.
2. Keep only the categories the signal creates demand for, or directly changes the market of. A word in
   passing is not a category. A bank's ATM count mentioned in a report about card growth does not make it
   an ATM signal.
3. Return 1 to 3 category ids from `product_map.json`, lead first. Most signals have one or two.
4. The keyword tags are a hint, not an answer. Drop what is not relevant. Add a category the keywords
   missed only when the row clearly calls for it.
5. A market or regulatory backdrop with no Printec line still gets its closest category.
6. Give a `why` of one short sentence in plain English.

## How to run it

```
python3 weekly-intelligence/scripts/product_critic.py batches --root <BANKING> --work <workdir>
```
This writes `<workdir>/TAXONOMY.md` (the categories and rules), `<workdir>/items/batchNN.json` (the
signals to judge, 24 per batch) and `manifest.json`. Add `--all` to re-judge every signal.

For each batch: read `TAXONOMY.md` and the batch file, judge every item, and write
`<workdir>/out/batchNN.json` as a JSON array of `{"key", "products", "why"}` with the same keys, in the
same order. Batches are independent — fan them out in parallel (one agent per batch).

Then:
```
python3 weekly-intelligence/scripts/product_critic.py merge --root <BANKING> --work <workdir> --week <Monday>
```
This validates every verdict (known ids, 1 to 3 of them) and writes the accepted ones into
`product_review.json`. Malformed verdicts go to `<workdir>/failed.json`; redo those once and merge again.

Finally rebuild in the usual order: `ingest.py` (it prints how many signals took a verdict), `forecast.py`,
`project_lines.py`, `build_dashboard.py`, `plain_lint.py`, `artifact/build_artifact.py`, then republish.
Agent 9 (the plain-English editor) runs after this step, because it also rebuilds.

## What it must never do

- Edit the master table, a findings file, or any agent brief.
- Write a verdict by hand into `product_review.json` without running the merge check.
- Use a category id that is not in `product_map.json`.
