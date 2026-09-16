> **Writing standard.** Everything you write must follow `WRITING_POLICY.md`: plain business English, short sentences, one idea per sentence, no dramatic phrasing. Numbers, dates, names, cell keys and signal keys never change.

# The third sitting: the Chairman's mandate

The Chairman has read the 2027 budget and asks for two things: the **lowest acceptable number (the floor) must be double digits**, at least +10% on the 2026 budget of EUR 148.66m, which is **EUR 163.53m**, and the **budget itself must be as high as the evidence allows**. He names four areas, without limiting the board to them: (1) new markets and products, for example fraud monitoring, payments, managed services and outsourcing; (2) more market share in existing products; (3) the big markets, Ukraine in particular; (4) efficiency. A restructuring of professional services and customer services will happen; delivery may ask for what it needs.

## Where the second sitting left the numbers

| | 2027 | Growth |
|---|---|---|
| 2026 budget | EUR 148.66m | |
| Floor (lowest number every view accepts) | EUR 151.22m | +1.7% |
| Budget | EUR 156.22m | +5.1% |
| Most the dated evidence supports | EUR 165.09m | +11.1% |
| Highest estimate on the table | EUR 175.22m | +17.9% |

The floor is low for three reasons the sceptics gave and the board accepted: the 2026 figures are targets, not results; the largest deals carry no 2027 date; delivery capacity is conditional on hires. **A floor rises only when those objections are removed cell by cell.** The mandate therefore asks every seat a different question from the first two sittings: not "what number do you propose" but **"what has to happen, by when, and who does it, for this cell's floor and budget to rise, and to what number"**.

## What each seat writes (round 1)

Read `agent-briefs/board/00-rules.md`, your seat brief, your packet `budget/board/packet/<seat>.md` (the evidence; signal keys must come from it), the current numbers per cell in `budget/budget_2027_board.internal.json` (fields `board.floor`, `board.target`, `board.upside`, `board.reason`, `board.capacity`, `board.dissent`, `board.evidence`) and `budget/board/reconciliation.md`.

**Growth, line and market seats** write `budget/board/mandate/round1/<seat>.json`:

```json
{"seat": "<seat>",
 "summary": "<five sentences: what your scope can add to the floor and to the budget, by when, and the two or three actions that matter most>",
 "cells": [
   {"cell": "RO|atm_recycling", "floor_now": 18145918, "floor_if": 19200000, "budget_if": 20500000,
    "actions": [
      {"what": "<one sentence: the concrete action>", "kind": "date | share | capability | hire | pricing | efficiency",
       "deal": "<signal key or empty>", "by": "2027-03-31", "owner": "<sales RO | delivery | group | partner | finance>",
       "eur_floor": 1054082, "eur_budget": 1300000}
    ],
    "evidence": ["<signal key>"]}
 ],
 "new_business": [ {"cell": "HU|managed_services", "floor_now": 0, "floor_if": 400000, "budget_if": 800000, "actions": [], "evidence": []} ],
 "focus": {"new_markets": "<two sentences>", "market_share": "<two sentences>", "big_markets": "<two sentences>", "efficiency": "<two sentences>"}}
```

Rules for the numbers: `floor_now` is the cell's current `board.floor`. `floor_if` is the floor the cell would carry once the listed actions with `kind` date, hire or capability have happened (a dated order or RFP removes the timing objection; a hire removes the capacity objection; a capability removes the "no team" objection). `budget_if` is the budget the cell would then carry, never above what the evidence supports (the current `board.upside` unless you show a new dated fact). `eur_floor` and `eur_budget` on an action are the euros that action moves, and the actions of a cell must add up to `floor_if - floor_now` and `budget_if - board.target`. Every deal named must be a signal key in your packet. Dates are inside 2027 or the last quarter of 2026. Pricing and efficiency actions may be stated on recurring revenue (one point of price on a cell's recurring revenue = one percent of its `recurring_2026`). Do not invent deals, dates or capacities.

**Sceptic seats (cfo, cro, ned)** write the same file with, per cell they hold down, `{"cell": ..., "objection": "<one sentence>", "satisfied_by": "<the fact that would remove it: an order, an RFP date, a 2026 actual, a hire, a partner>", "by": "<date>", "floor_if_satisfied": <euros>}` in `cells`, plus `summary` and `focus`. The finance view also states what the double-digit floor needs on profit and on the EUR 13.33m of retail and unnamed revenue.

**The delivery seat (ops)** writes `budget/board/mandate/round1/ops.json`: `{"seat": "ops", "delivery_ask": [{"country": "HR", "lines": ["atm_recycling"], "people": "<what, how many>", "skills": "<what>", "by": "2027-03-31", "cost_eur": 180000, "for": "budget | maximum", "eur_at_stake": 720000}], "restructuring": "<one paragraph: what a professional-services and customer-services restructuring should give delivery to carry the maximum case>", "summary": "..."}` for the budget case (EUR 165.09m) and the maximum case (EUR 175.22m).

## What the chair writes (round 2)

The chair reads every round-1 file and writes `budget/board/mandate/decision.json`: the ladder (floor today, double-digit floor with its date and conditions, the budget, the maximum), the action list per cell with euros, dates and owners, the capability decisions, the delivery ask, the answer to the four focus areas, and a one-page executive brief for the Chairman in neutral third-person voice (no board, seats, votes, agents or first person; views only). The engine step `board_2027.py mandate` validates cell keys and signal keys, sums the euros and writes `budget/budget_2027_mandate.json` for the dashboard.
