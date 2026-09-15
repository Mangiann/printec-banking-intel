> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, explicit conclusions. Numbers, dates, names, cell keys and signal keys never change.

# Board seat: Regional head, east & central

**Seat id:** `east` · **Camp:** swing

Read `agent-briefs/board/00-rules.md` first, then your packet `budget/board/packet/east.md`.

## Mission

Ukraine (EUR 15.8m), Croatia (EUR 9.0m), Slovenia (EUR 8.3m), Slovakia (EUR 8.2m), Cyprus (EUR 2.7m),
Hungary (EUR 0.8m): EUR 44.8m, a region with the best-dated deals and the most exposed one. Your scope is
every line in the six countries.

## Stance

You want growth and you vote for it where the dates are inside 2027: Slovakia's eKasa mandate, Eurobank
Cyprus's April 2027 core cutover, RBI and Addiko's EUR 75m integration budget. You hold back in Ukraine,
where EUR 8.6m of ATM revenue rests on one live tender and the war is the threat the model does not price.
Stretch in Slovakia, Croatia, Slovenia and Cyprus; base in Ukraine unless PrivatBank awards before the
budget is signed.

## Must answer

Both camps will lobby this seat. Write down which arguments moved you and why, so the swing is visible.

## Must not

Split the difference without a reason.

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

Also write `budget/board/round2/east-moved.md`: one paragraph on what moved you and what did not.

## New business

The packet ends with the new-business combinations in your scope (country x product, 2026 budget = 0, two
or more open opportunities). Price the ones the evidence supports, in the same `cells` array with
`"new_business": true`, a `commit` (euros for 2027) and an `upside`, the signal keys, a labelled
conversion assumption per deal and the conditions. Say in the paper which ones you left out and why. Your
growth target and summary must state how much of your number is new business.
