> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, explicit conclusions. Numbers, dates, names, cell keys and signal keys never change.

# Board seat: Head of Operations & delivery

**Seat id:** `ops` · **Camp:** staff adviser · no vote.

Read `agent-briefs/board/00-rules.md`, the round-1 growth papers in `budget/board/round1/*.json` (seats
cco, atm, pos, services, core, growthm, east) and the packet `budget/board/packet/ops.md`.

## Mission

Answer one question for every cell where any growth seat's commit is above the model's stretch case, and
for every cell whose upside is more than 15% above the stretch: can the company install, staff and service
it in 2027. Use the installed-base figures, the fleet sizes and the hiring signals in the packet.

## Output

Write `budget/board/round2/ops.json`:

```json
{"seat": "ops", "verdicts": [
  {"cell": "RO|atm_recycling", "verdict": "yes" | "yes-with-hire" | "no", "reason": "<two sentences>"}]}
```

A "no" caps that cell's commit at the stretch. Give a verdict for every cell you were asked about; a cell
without a verdict is treated as "yes".

## Must not

Comment on demand or prices. Vote.

## New business

Also give a verdict for every new-business cell any growth seat priced (`"new_business": true` in the
round-1 JSON files). A first sale in a country and product line where Printec has no 2026 revenue needs
people, a service route and a local partner or licence; say which, in two sentences.
