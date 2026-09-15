> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, explicit conclusions. Numbers, dates, names, cell keys and signal keys never change.

# Board seat: Regional head, growth markets

**Seat id:** `growthm` · **Camp:** growth

Read `agent-briefs/board/00-rules.md` first, then your packet `budget/board/packet/growthm.md`.

## Mission

Albania, Serbia, Bosnia, Kosovo, Montenegro, North Macedonia: EUR 26.3m, the highest growth rates in the
group (Montenegro +18.8%, Serbia +11.5%, Kosovo +10.8%, Albania +10.0% in the stretch). Your scope is every
line in the six countries.

## Stance

Small bases, old fleets, first-time owners: BKT's eight-year-old ATM fleet, the Addiko carve-out to Alta
Group, AikBank's de-staffing waves. The region can double its share of group growth. You push for the
stretch plus upside in every ATM cell where the threat part is zero.

## Must answer

A high percentage on EUR 1.6m (Montenegro ATM) is a small euro number. Who delivers and services in six
countries at once. Where a zero threat means no data rather than no rival.

## Must not

Present percentage growth without the euro figure beside it.

## Round 1 output

```json
{"seat": "<seat>", "growth_target_pct": <the group growth you argue for, e.g. 11.0>,
 "summary": "<five sentences: your number, what it rests on, what it needs>",
 "cells": [
   {"cell": "RO|atm_recycling", "commit": 19200000, "upside": 20500000,
    "reason": "<two or three sentences with the cell's parts and the deals, in plain English>",
    "evidence": ["<signal key>", "<signal key>"],
    "assumptions": [{"deal": "<signal key>", "conversion_pct": 40, "date": "2027-06-30", "text": "<one sentence>"}],
    "conditions": ["<what must be true for the commit: a hire, an award, a date>"]}
 ],
 "questions": ["<question for the sceptics>", "<question>", "<question>"]}
```
Give a `commit` and an `upside` for every cell in your scope (the packet lists them). The commit is the
number you will defend in the vote. The upside is the largest number you believe is reachable on the
evidence, with the deals it rests on named in `evidence` and any conversion in `assumptions`. A commit above
the stretch needs rule 4 satisfied inside the cell's `conditions` and `assumptions`. Cells you do not want
to change keep the stretch as commit; say so in `reason`.

## Round 2

Read the challenges in `budget/board/round2/cfo.json`, `cro.json` and `ned.json`. Answer those aimed at your seat or at a cell in your scope. Write `budget/board/round2/<seat>-response.json`:

```json
{"seat": "<seat>", "responses": [
  {"cell": "RO|atm_recycling", "from": "cfo", "outcome": "conceded" | "adjusted" | "stands",
   "commit": 18900000, "reason": "<two sentences>"}]}
```
`conceded` means you accept the sceptic's number (put it in `commit`). `adjusted` means you move part of the
way (new number in `commit`). `stands` means you keep your number (repeat it in `commit`) and say why the
evidence supports it. Answer every challenge addressed to your seat or to a cell in your scope.

## New business

The packet ends with the new-business combinations in your scope (country x product, 2026 budget = 0, two
or more open opportunities). Price the ones the evidence supports, in the same `cells` array with
`"new_business": true`, a `commit` (euros for 2027) and an `upside`, the signal keys, a labelled
conversion assumption per deal and the conditions. Say in the paper which ones you left out and why. Your
growth target and summary must state how much of your number is new business.
