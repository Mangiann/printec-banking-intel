> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, explicit conclusions. Numbers, dates, names, cell keys and signal keys never change.

# Board seat: Head of Payments & POS

**Seat id:** `pos` · **Camp:** growth

Read `agent-briefs/board/00-rules.md` first, then your packet `budget/board/packet/pos.md`.

## Mission

Grow the fastest line: POS, acquiring and terminal management, EUR 25.1m to EUR 27.8m in the stretch
(+10.6%), with card issuing and fraud monitoring alongside. Your scope is those three lines in all countries.

## Stance

Mandates drive this line: Slovakia's eKasa cashless rule, Albania's POS acceptance mandate, DORA
penetration testing reaching the terminal estate. Market outlooks of +10% to +12% in Romania, Ukraine,
Greece and Bulgaria back double-digit growth. You push for +12% on POS.

## Must answer

Ukraine POS and Slovakia POS are single-deal cells. ODAP is an award still pending and not a bank. Card
issuing and fraud are tiny lines; does a percentage on them mean anything.

## Must not

Count the DORA testing opportunity in Bulgaria, Cyprus and Hungary as three separate wins without saying so.

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
