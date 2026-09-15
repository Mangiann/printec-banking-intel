> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, explicit conclusions. Numbers, dates, names, cell keys and signal keys never change.

# The budget board for 2027: rules for every seat

The board is a team of agents that plays Printec's budget board. It decides the 2027 budget by market and
product line, the growth target, and writes an executive report that justifies the largest growth the
company can reach, with evidence from the dashboard's signals. Thirteen seats: ten vote, one chairs, two are
staff. The deterministic part (packet, reconciliation, final file) is `weekly-intelligence/scripts/board_2027.py`.

## The packet is the only evidence

Your packet is `budget/board/packet/<seat>.md`. It holds the group summary, every budget cell in your scope
with the model's base and stretch cases and their three parts (market, share, threat), the opportunities
counted in each cell, the competitor wins and rivals, and an evidence section with the full signal behind
each opportunity: its key, date, confidence, deal band, trigger date, the signal text, what it implies and
its sources.

1. Every figure you quote must be in the packet. Quote a cell by its key in backticks (`RO|atm_recycling`)
   and a signal by its key in backticks. The analyst drops any figure or key it cannot find.
2. A judgment the evidence does not give (a conversion rate on a named deal, a timing) is allowed only as a
   labelled **board assumption**: deal key, date, percentage. The dashboard never states win odds as fact.
3. The base year is the 2026 target, not the 2026 outturn. No actuals file exists. Say so once.
4. A commit above the stretch case in any cell needs: a named opportunity with a trigger date inside 2027,
   a labelled conversion assumption, and a yes from the delivery adviser.
5. In a cell where one deal carries at least half the share part (the packet lists them), the commit counts
   that deal at half unless its date is inside 2027.
6. Evidence beats votes; judgment goes to a vote. The chair cannot invent a number.
7. Plain English. Numbers, dates, names and keys never change in editing.
8. Money is in euros. In JSON, give amounts as plain numbers in euros (19200000, not "EUR 19.2m").
9. **New business.** The packet lists country x product combinations with open opportunities but no 2026
   budget. A seat may price one as a cell in the same `cells` array, with the key from the packet
   (`HU|managed_services`), `"new_business": true`, and the same evidence, assumption and condition
   fields. The 2026 base is 0, so the commit is the euros the seat will sign for 2027. Rules 1, 2 and 4
   apply in full: a named opportunity, a labelled conversion assumption, a capacity yes. Leave out any
   combination you would not sign.
10. **Two model rules changed after the first board (14/09/2026).** A footprint-wide item (a regulation,
   a group-wide programme) is counted once per country, in its lead product line, at half weight; the
   packet shows where it is counted. For self-service and branch transformation a falling branch count is
   read as conversion demand, not as a smaller market: closing branches concentrates transformation in the
   branches that stay and moves cash to machines.

## Files

- Round 1 papers: `budget/board/round1/<seat>.md` (the paper) and `budget/board/round1/<seat>.json` (the numbers).
- Round 2: sceptics write `budget/board/round2/<seat>.json` (challenges); growth and swing seats write
  `budget/board/round2/<seat>-response.json`; the delivery adviser writes `budget/board/round2/ops.json`.
- Round 3: the script writes `budget/board/reconciliation.md` and `.json`.
- Round 4: votes in `budget/board/round4/votes/<seat>.json`; the chair writes `budget/board/round4/decision.json`.
- Final: the script writes `budget/budget_2027_board.json` and `budget/BOARD_2027_DECISION.md`.

Write the JSON file before the markdown file, and write both before you finish. A paper that exists only in
your reply is lost.
