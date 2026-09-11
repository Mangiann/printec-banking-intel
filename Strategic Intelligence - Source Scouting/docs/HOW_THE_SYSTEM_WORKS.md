# How the Source-Scouting System Works — a plain guide

*For a non-developer who wants to understand the whole machine: what runs, in what order, which file does
what, why there are four kinds of files, and why a "simple" scouting system needs this many pieces.*

---

## 1. The one idea behind everything

The system builds and maintains a **master list of sources** — the places where banking **and payments**
tender/procurement intelligence lives in a country (portals, registries, vendor pressrooms, tender
aggregators, job boards as weak signals, …). It is the **first layer** of a longer chain
(`sources → acquisition → parsing → evidence → claims → signals → opportunities → dashboards`). This project
only does the **sources** layer.

One principle explains almost every design choice:

> **Imaginative in discovery, strict in storage.**
> A creative AI *finds* sources (it's good at imagining where information hides). Strict, boring, testable
> code *checks, counts, de-duplicates, verifies, and stores* them (computers are good at not making mistakes).
> **The AI never decides what is true, reachable, safe, or already-known — code does.**

If you remember only that sentence, the rest of the system makes sense: it is split the way it is to keep the
imaginative part and the strict part apart.

---

## 2. The four kinds of files (why "so many languages")

| Kind | Extension | What it is | Why this language |
|---|---|---|---|
| **Python** | `.py` | The **strict brain**. Validates, counts, de-dups, verifies URLs, applies safety rules, stores to the database, writes the Excel. Deterministic: same input → same output, every time. | Python is best for data work and is what all 282 automated tests are written against. This is the layer we *trust*. |
| **JavaScript** | `.js` | The **AI orchestration**: one **orchestrator** that runs a whole round in fixed order, plus two **swarm engines** it calls (many scouts search; many labelers judge). | The tool that runs AI swarms (the Workflow tool) speaks JavaScript. The orchestrator's control flow is deterministic code; the swarm engines are thin conductors that spawn agents and let them write their answers to disk. |
| **JSON** | `.json` | Two jobs: (a) **contracts** — the *rules* for what a valid record looks like (the `schemas/`), and (b) **data** — the actual records and the AI's raw outputs (scout findings, role verdicts, decisions). | JSON Schema is the industry-standard way to say "a valid record must have these fields, of these types." It lets code *reject* anything malformed. |
| **YAML** | `.yaml` | The **run settings** — which country, sector, topics, languages. One short file per kind of run. | Easy for a human to read and edit; it's just the knobs. |
| **Markdown** | `.md` | Two jobs: (a) **human docs** (this file, the dev log), and (b) **the AI's instruction playbook** — the exact briefing the scout AI is given. | Plain text a human and an AI both read. |

**This is not accidental complexity.** Each language is doing the one thing it's best at. The AI part *must*
be JS (that's the tool). The strict part *should* be Python (data + tests). The contracts *should* be JSON
Schema (a standard). Forcing them into one language would make each part worse, not simpler.

---

## 3. What runs when — one scouting round, stage by stage

A full round is **7 stages**. Some are the AI (imaginative), some are Python (strict). Each stage hands a
**file** to the next — that's how the AI's work gets checked before it's trusted.

**What runs them in order?** A single **deterministic orchestrator**, `full_round_workflow.js` — a Workflow
whose control flow is CODE. It calls every stage below in a **fixed order**; no agent decides what runs or can
skip a step (only what discovery *finds* varies). The two AI swarms write their output to disk as "slices",
and two one-command Python steps (`round_ingest.py`, `round_finalize.py`) do the strict work between them, so
every hand-off is a file, not a judgement call. (You can also run or resume any single stage by hand — see
`SCOUT_ROUTINE.md`.)

```
        AI (imaginative)                         PYTHON (strict)                        HUMAN (optional)
  ┌─────────────────────────┐          ┌──────────────────────────────┐          ┌────────────────────┐
1 │ DISCOVERY               │  writes  │                              │          │                    │
  │ discovery_workflow.js   │ ───────► │ 2 INGEST                     │          │                    │
  │ (plan → bilingual       │ scout_   │ run_pipeline.py + runner.py  │          │                    │
  │  scouts → merge)        │ output   │ + normalize.py               │          │                    │
  └─────────────────────────┘ .json    │ (validate, verify URLs,      │          │                    │
                                        │  de-dup, snap vocab, count)  │          │                    │
  ┌─────────────────────────┐          └──────────────┬───────────────┘          │                    │
3 │ BROWSER LINK-REPAIR     │  writes                 │ candidates.jsonl          │                    │
  │ a recovery agent in     │ recovery_               ▼                           │                    │
  │ real Chrome walks the   │ results   ┌──────────────────────────────┐          │                    │
  │ "is it really dead?"     │ .json ──►│ (recovery.py folds results in)│          │                    │
  │ ladder                  │          └──────────────────────────────┘          │                    │
  └─────────────────────────┘                                                     │                    │
  ┌─────────────────────────┐          ┌──────────────────────────────┐          │                    │
4 │ LABELING                │  writes  │ 5 GROUP → ROLE → ROUTE        │          │                    │
  │ labeling_workflow.js    │ ───────► │ consolidate.py, prelabel.py,  │          │                    │
  │ (role + decision per     │ role_    │ route.py                     │          │                    │
  │  source, in batches)    │ verdicts │ (group by entity, sort into  │          │                    │
  │                         │ .json    │  keep/evidence/pointer/…)    │          │                    │
  └─────────────────────────┘          └──────────────┬───────────────┘          │                    │
                                        6 DELIVERABLE  │                          │                    │
                                        master_export.py writes                   │ opens the ONE      │
                                        deliverables/<one Excel> ────────────────►│ Excel, edits       │
                                        7 SYNC → registry (promotion.db)          │ decisions (or not) │
                                        sync_registry.py + promotion/*            └────────────────────┘
```

**Stage by stage:**

| # | Stage | Who | Reads | Writes | What it does |
|---|---|---|---|---|---|
| 1 | **Discovery** | AI (JS swarm) | the config | `agent_inputs/scout_slices/*.json` | A planner splits the country into ~20–32 "coverage cells"; one deep **bilingual** (Greek+English) scout per cell searches the web and **writes its found sources to a slice file**. |
| 2 | **Ingest** | Python (`round_ingest.py`) | the slices | `data/source_candidates/<run>.jsonl` | Merges the slices, then `normalize.py` expands them to full records + snaps sloppy words to the allowed vocabulary + safety clamps, and `runner.py` validates against schema, HEAD-checks every URL, de-dups, counts (the AI's numbers are ignored). Also writes `failed_urls.json` + the labeling batches. |
| 3 | **Browser link-repair** | AI (Chrome) | the failed URLs | `agent_inputs/recovery_results.json` | A crude HEAD check over-reports "dead" ~5×. An agent drives a **real Chrome** through a recovery ladder (is it just bot-blocked? did it move? did the company rebrand?) and reports verified/repaired/dead. `recovery.py` folds the result back in — fail-closed (never marks "alive" without proof). |
| 4 | **Labeling** | AI (JS engine) | the candidates | `role_verdicts.json`, `decision_suggestions.json` | For each source, two *recommendations*: a **role** (durable source / one-off evidence / directory / weak) and a **decision** (approve / needs-access / reject / defer). Recommendations only — code and humans still decide. |
| 5 | **Group → Role → Route** | Python | candidates + the AI labels | machine artifacts under `data/.../artifacts/` | `consolidate.py` groups many pages of one website into one entity; `route.py` sorts everything into the durable monitoring list vs the evidence/pointer/marginal ledgers — losing nothing. |
| 6 | **Deliverable** | Python | the registry | `deliverables/<one Excel>` | `master_export.py` writes the single human file: **all** sources, each tagged with the run that added it. |
| 7 | **Sync to registry** | Python | the review sheet | `data/promotion.db` | `sync_registry.py` + the `promotion/` layer promote the approved sources into the master database, **safety-gated** (a source only goes "active" if it's public + legally allowed + verified). The human's Excel edits win if they made any; otherwise the AI's suggestion is used. |

**Convergence report** (an extra Python step) then measures: how many sources this run found that we'd never
seen before — the number that tells us whether more runs are still worth it.

---

## 4. Every file, by job (the "why so many" answered concretely)

Files are grouped so that **each file has one job**. That is what lets us test each piece, reason about it,
and fix one thing without breaking another. Here is the whole map.

### 4a. The contracts — `schemas/` (7 JSON files)
The *rulebooks*. Each says "a valid record of this type must look exactly like this." Code validates every
record against them, so nothing malformed is ever stored.
`source_candidate` (a found source), `access_review_task` (a blocked source needing a human), `negative_finding`
(a dead end worth remembering), `coverage_gap` (a hole in coverage), `source_registry` (an accepted master-list
source), `discovery_run_manifest` (the audit record of one run), `promotion_event` (one step in the promote history).

### 4b. The scout routine — `routines/source_discovery_scout/`
| File | Language | Job |
|---|---|---|
| `full_round_workflow.js` | JS (**the orchestrator**) | Runs a WHOLE round deterministically: discover → ingest → repair → label → finalize, in fixed order. The conductor whose control flow is code. |
| `discovery_workflow.js` | JS (AI swarm) | The discovery swarm (plan → bilingual scouts); each scout **writes its findings to a slice file**. |
| `labeling_workflow.js` | JS (AI swarm) | The labeling swarm (role + decision per source); each batch **writes its labels to a slice file**. |
| `runner.py` | Python (strict) | The guardrail around the scout: validate, verify URLs, de-dup, count, write the run's audit manifest. The AI cannot bypass it. |
| `normalize.py` | Python (strict) | Turns the AI's *compact* findings into full records; snaps sloppy words ("open" → "public") to the allowed vocabulary; forces safety clamps. |
| `recovery.py` | Python (strict) | Applies the browser-repair results, fail-closed. |
| `routine_prompt.md` | Markdown | The **exact briefing** the scout AI is given (its method + hard rules). |
| `SCOUT_ROUTINE.md` | Markdown | How to run a round: the one-command orchestrator + the per-stage manual fallback. |

### 4c. The promotion layer — `promotion/` (the strict "librarian")
Turns an **approved** candidate into an official master-list source, with a full audit trail. This is the most
safety-critical code, so it is split into small, single-purpose pieces that are individually tested:
`db.py` (the only file that talks to the database), `promote.py` (add a new source), `merge.py` (fold a
duplicate into an existing one), `update.py` (add info to an existing one), `lifecycle.py` (reject/retire/
deactivate), `apply.py` (turn a run's review decisions into promote/reject/hold actions), `gates.py` (the
9 safety checks every promotion must pass), `safety.py` + `restrictiveness.py` (decide "can we collect this?"
— always erring to the safer answer), `mapper.py` (shape a candidate into a source record), `enrich.py`
(safely merge extra info), `validation.py` (run the schema checks), `integrity.py` (a read-only auditor),
`util.py` (small helpers).

*Why split so finely?* Because a mistake here could mark a forbidden source "safe to collect." Small isolated
pieces + one test each = that class of mistake gets caught by a test, not by you.

### 4d. The review layer — `review/`
| File | Job |
|---|---|
| `crossrun.py` | Novelty check: is each source new, or seen in an earlier run / already in the master list? |
| `consolidate.py` | Group many URLs of one organisation into one entity. |
| `route.py` | Sort candidates into the durable list vs evidence / pointer / marginal ledgers. |
| `prelabel.py` | The guardrail around the AI's role/decision labels (clamp anything invalid). |
| `_safe.py` | Tiny helpers so every reader of on-disk data is "total" — it can never crash on a bad record. |
| `excel.py` | The per-run review sheet (export for a human, read their edits back). |
| `master_export.py` | The single master-list Excel deliverable. |

### 4e. The orchestration — `scripts/`
The **command-line entry points** that chain the pieces. The two the orchestrator calls, one command each:
`round_ingest.py` (merge discovery slices → strict ingest → build labeling batches) and `round_finalize.py`
(merge label slices → route → sync registry → convergence report). Under them: `run_pipeline.py` (the strict
ingest→deliverable pipeline), `sync_registry.py` (promote a run + refresh the deliverable), and
`round_status.py` (says where a half-finished round stands, so a stopped session never loses its place). The
rest are small single-operation tools (`promote_candidate.py`, `ingest_scout_output.py`, …) for one-off actions.

### 4f. Settings & docs
`configs/discovery_runs/*.yaml` (the run knobs), `docs/` (this guide, the dev log, the design notes),
`tests/` (282 automated checks), `data/` (all machine state), `deliverables/` (the one human Excel).

---

## 5. Why so many files — the honest answer

You could write this in one giant file. Here's why we don't:

1. **One job per file = one place to look.** When something is wrong with URL-checking, it's in `runner.py`,
   full stop. A 5,000-line mega-file would mean hunting.
2. **Safety needs a wall.** The rules that decide "is this safe/legal to collect" live in their own files
   (`safety.py`, `gates.py`, `restrictiveness.py`) that the creative AI code cannot reach or override. Mixing
   them into everything would let a bug in one place weaken a safety rule elsewhere.
3. **Testing.** 273 automated tests each target one small piece. Small files are testable; big ones aren't.
   Those tests are exactly what catch bugs *before you see them*.
4. **The AI/strict split is the whole point.** Keeping the imaginative AI (a few JS + markdown files) apart
   from the strict storage (the Python files) is not overhead — it's the safety design. If the AI and the
   storage were one blob, the AI could quietly corrupt the master list.
5. **Change one thing safely.** Small files mean a fix to the Excel layout can't break the promotion database.

The cost of many small files is that a *flow* touches several of them — which is exactly what this guide is
for. The benefit is that the system is testable, safe, and fixable one piece at a time.

---

## 6. Follow one source through the machine (a worked trail)

> The scout finds **"AADE — Registry of POS Providers"**.

1. **Discovery** (`discovery_workflow.js`, AI): a scout **writes it to a slice file** — a name, a URL, a guess
   at why it matters. *Not trusted yet.*
2. **Ingest** (`round_ingest.py` → `normalize.py` → `runner.py`, Python): merges the slices, expands it to a
   full record, snaps its access word to `public`, HEAD-checks the URL, de-dups it, writes it to
   `data/source_candidates/<run>.jsonl`.
3. **Link-repair** (Chrome agent → `recovery.py`): the URL loaded fine → marked genuinely verified.
4. **Labeling** (`labeling_workflow.js`, AI): role = `keep` (a durable source), decision = `approve`.
5. **Route** (`route.py`, Python): placed in the durable monitoring list.
6. **Sync** (`sync_registry.py` → `promotion/`, Python): passes the 9 safety gates (public + allowed +
   verified) → promoted into `promotion.db` as an **active** source.
7. **Deliverable** (`master_export.py`, Python): appears as one row in
   `deliverables/Greece - Banking & Payments Sources (…).xlsx`, tagged with the run that found it.

At no point did the AI decide it was real, reachable, or safe. It only *suggested*; code *confirmed*.

---

## 7. Where everything lives (folder map)

```
schemas/        the 7 rulebooks (JSON Schema)
routines/source_discovery_scout/   the scout: orchestrator + 2 swarm engines (.js) + strict runner/normalize/recovery (.py) + playbooks (.md)
promotion/      the strict "librarian" — approved candidate → audited master-list source (Python + SQLite)
review/         novelty, grouping, roles, routing, the Excel round-trip, the master export (Python)
scripts/        the command-line entry points that chain it all
configs/        the run settings (YAML)
data/           ALL machine state — candidates, audit logs, promotion.db, per-run artifacts. Humans don't look here.
deliverables/   the ONE human Excel (the whole master list). This is what a reviewer opens.
docs/           this guide + the dev log + design notes
tests/          273 automated checks
```

**Rule of thumb:** if a human should see it, it's in `deliverables/`. Everything else under `data/` is the
machine's own bookkeeping.
