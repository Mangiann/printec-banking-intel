> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, explicit conclusions. Numbers, dates, names, cell keys and signal keys never change.

# Round 4: the vote

Every voting seat reads `budget/board/reconciliation.md` (the board table after the challenges), then
writes `budget/board/round4/votes/<seat>.json`:

```json
{"seat": "<seat>", "vote": "for" | "against",
 "reason": "<three to five sentences: the commit total, why you vote as you do, the one condition you attach>",
 "minority_report": "<sceptics only: one or two paragraphs for the record; growth seats leave empty>"}
```

The vote is on the commit total in the reconciliation. A vote for means you would sign that budget with the
conditions listed. A vote against must name the number you would sign instead, and it must be a number
already on the table (the floor, the base, the stretch, or your own round-1 number).
