# Greece baseline A/B — run instructions (STAGED TEST)

Goal: measure what the source-access registry buys us, without touching production. Run the Greece
collector flow **twice** and compare: once as-is (control), once with the staged registry (treatment).

Everything needed is in this folder. **No production file is modified.**

## What's staged here

- `staged-references/` — a full copy of `weekly-intelligence/references/` **plus** the registry files
  (`source_registry.json` + `source_registry_A1…A6.json`).
- `staged-agent-briefs/` — copies of `agent-briefs/01…06` with one added block: *"Validated starting
  sources (load first)"*. Everything else in each brief is byte-for-byte the original.
- `source_access_registry.*` (parent folder) — the underlying registry the slices come from.

## Run it (interactive, one step at a time — per the test HARD RULE)

**Control (as-is):** run the Greece flow the normal way — Agents 1–6 from the production
`agent-briefs/`, reading production `references/`. Capture: wall-clock per agent, # sources touched,
# findings, # dead/blocked sources hit, coverage gaps noted.

**Treatment (with registry):** run the same Greece flow but point the agents at this folder:
- briefs → `registry-adapter-TEST/staged-agent-briefs/`
- references → `registry-adapter-TEST/staged-references/` (so `references/source_registry_A#.json` resolves)

Keep everything else identical (same week, same units in `agent-units.json`, same operator approvals).
Do **not** run `run_weekly.py`/`publish.py` for the A/B — that publishes to the live dashboard; the
comparison is about the *research/agent* layer, not the dashboard.

## What to measure (fill in)

| Metric | Control (as-is) | Treatment (registry) |
|---|---|---|
| Wall-clock, Agent 1–6 total | | |
| Distinct sources reached | | |
| Findings produced | | |
| Runs that hit a dead/blocked URL | | |
| Sources that needed re-discovery | | |
| New sources found on top of the slice | | |

**Success = treatment reaches the same-or-more findings with less time spent re-discovering access, and
the agents still propose new sources on top of the validated list** (floor, not ceiling).

## Scope & caveats (before you read too much into it)

- Registry covers **5 of 17 footprint countries** (GR, AL, BA, BG, HR). This baseline is **Greece only**,
  which is fully covered — a fair test. Do not generalise the delta to countries with no registry slice yet.
- `reliability` is mostly `unverified` (91 verified live). The Greece slice has the most verified entries,
  so Greece is the right first test.
- Registry confirms **access, not relevance** — expect the agents to still judge on-topic-ness.
- **F5 (TED/CPV tender scope) is unresolved** — the A2 run should not change tender scope during this test.

## If the baseline shows a win

Promote in one reviewed batch (the notes' "implement agreed findings as one batch"):
1. Copy `source_registry*.json` into the real `weekly-intelligence/references/`.
2. Apply the six brief snippets to the real `agent-briefs/` (the block is marked and self-removing).
3. Then widen coverage: commission source workbooks for the missing footprint countries, and widen
   live verification to raise the `verified` share.

## To revert
Delete this `registry-adapter-TEST/` folder. Production was never touched, so there is nothing else to undo.
