# THE PROTOCOL

**This document is binding. It is not advice, a summary, or a description of how things usually go.
No agent and no human may deviate from it. If a step cannot be run, the work STOPS and the reason is
reported — it is never quietly skipped.**

Written 2026-07-29, after a deviation that cost roughly 20 million tokens and put 16,345 unverified,
unfiltered facts into the graph. That deviation is described at the end, because a rule without its
scar is a rule people talk themselves out of.

---

## Why this exists

The pipeline has stages. Each stage exists because something goes wrong without it. Running a stage
by hand, in isolation, "just to see", is how a stage gets skipped — and a skipped stage does not
announce itself. The graph fills with plausible-looking material and nothing errors.

**The pipeline is the unit of work. Not the stage.**

---

## The two pipelines, and what each stage is FOR

### Pipeline A — COLLECTION (`routines/content_collector/full_collection_round.js`)

Run per country, per workstream.

| # | Stage | What it does | Without it |
|---|---|---|---|
| 1 | **Pages** | Fetch each source page, detect whether it changed | Re-publication looks like news |
| 2 | **Judge** | An agent decides which links are worth following, **rejecting off-sector items by subject** | We download the whole internet |
| 3 | **Children** | Fetch exactly what the judge chose | Nothing is collected |
| 4 | **Read scans** | OCR the PDFs that are pictures of paper | Scanned documents are silently empty |
| 5 | **Backfill** | Recover documents today's capabilities would have taken, from pages already on disk | Every improvement applies only to future documents |
| 6 | **Audit** | Measure coverage and quality; write the workbook | Nobody can tell whether it worked |

### Pipeline B — KNOWLEDGE (`routines/knowledge_intelligence/full_knowledge_round.js`)

Run per country, after collection.

| # | Stage | What it does | Without it |
|---|---|---|---|
| 1 | **Enumerate** | List documents not yet read, batched by text volume | Work repeats or is missed |
| 2 | **Extract** | A swarm proposes facts, each with a verbatim excerpt | No facts |
| 3 | **Verify** | **A DIFFERENT agent checks each proposed fact against its excerpt and keeps only the supported ones** | A webinar invitation becomes an appointment; an awards page becomes a service contract |
| 4 | **Ingest** | Code grounds every excerpt, writes edges, then the ledger | Ungrounded claims enter the graph |
| 5 | **Harvest** | Transcribe typed-API payloads | Structured sources are ignored |
| 6 | **Resolve** | Merge entities that are the same company | One firm becomes five nodes; every count is wrong |
| 7 | **Privacy** | Classify personal data | GDPR exposure |
| 8 | **Relevance** | **Judge each document's SUBJECT against `data/knowledge/sector.json`; off-sector is marked, never deleted** | Off-sector documents pollute every layer above |
| 9 | **Audit** | Structural + grounding **GATE**. Non-zero exit blocks the deliverable | We publish material nobody checked |
| 10 | **Interpret** | Signals, needs, views, dashboards | No output |

---

## THE RULES

### R1 — Never run a stage alone
Run the **routine**. If you need one stage for a diagnostic, say out loud that the result is **not
production data** and do not let it reach the graph.

### R2 — A stage that cannot run STOPS the pipeline
It is never skipped, never deferred silently, never "we'll do it after". Report the blockage and halt.

### R3 — Relevance is judged BEFORE extraction, not after
Extracting from an off-sector document and marking it later wastes the most expensive step in the
system. **Move the sector judgement to collection time, on the document's own text.** A document that
fails it is marked and never queued for extraction.
*(Status: the judge filters LINKS by subject at collection today; the DOCUMENT-level check still runs
late in Pipeline B. This is the highest-priority change to make.)*

### R4 — Verification is not optional
The extractor is optimistic by design: it proposes. A **second, independent** agent must ask whether
the excerpt actually supports the fact, and may only keep or drop. Without it, "Save the date:
results presentation with the CFO" becomes an appointment — that is a real example from this graph.

### R5 — The ledger is written LAST
A document is marked read only after its facts are stored, and only if they actually reached the
grounding check. An interrupted run must leave unfinished work looking unfinished.

### R6 — Prove every zero
"Nothing found" is a claim. Show total-versus-matched before believing it. A step that reports success
while ingesting nothing has failed, and must exit non-zero.

### R7 — A bound may exist; a silent bound may not
Any limit, cap, slice or truncation must report exactly what it excluded. Twelve of these were found
in one day, one of them hiding 81% of the corpus.

### R8 — Code decides, agents propose
Wherever a check can be mechanical, code does it. An agent is never the only rung of a safety check,
and never certifies its own work.

---

## What to do when you want "just a quick test"

Legitimate, and it has one rule: **give it a run id that starts with `probe_`**, keep it out of the
main database, and delete it afterwards. Anything written under a `probe_` run is not evidence.

---

## The deviation this document exists to prevent

On 2026-07-28/29 the knowledge pipeline's ten stages were run as: **Enumerate → Extract → Ingest.**
Seven stages were skipped, including both quality gates.

The consequence, measured:

- **16,345 facts** entered the graph **unverified** (stage 3 skipped). Sampling shows roughly half are
  misreadings — conference speaker lists read as appointments, awards pages as service contracts,
  email signatures as leadership changes.
- **3,051 of 3,560 documents** were never checked for sector relevance (stage 8 skipped). Of the 509
  that had been checked in an earlier proper run, **20% were off-sector.**
- Duplicate companies were never merged (stage 6 skipped), so every organisation count is inflated.
- The audit gate never ran (stage 9 skipped), so nothing was blocked.

Nothing errored. Every number reported success. **The pipeline was correct; it simply was not run.**

The cost was roughly 20 million tokens of reading whose output now needs re-checking — not because
the reading was wrong, but because the checking never happened.

---

*Changes to this protocol require the project owner's explicit agreement, and the reason must be
recorded in `docs/DEV_LOG.md`.*
