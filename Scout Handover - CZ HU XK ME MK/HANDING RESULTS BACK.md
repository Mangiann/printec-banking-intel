# Handing the results back

When `python scripts/campaign.py --status` shows `"remaining": 0`, this machine's part is done: five
countries, six researches each, thirty rounds.

## What to send

Zip these two folders from the project and send them over (Dropbox, WeTransfer — anything that handles a
few hundred megabytes):

| Folder | What it holds |
|---|---|
| `data` | The five country registers, every round's raw findings, and the judging record. |
| `deliverables` | The five spreadsheets — the readable version of the same thing. |

Nothing in either folder belongs to anyone else. This machine only ever ran Czech Republic, Hungary,
Kosovo, Montenegro and North Macedonia, so there is nothing to filter out and nothing that can clash with
the main machine's files.

**Send whole files. Do not open, tidy, re-save or rename anything first.** The spreadsheets are generated
from the registers; an edited spreadsheet is silently out of step with the data behind it.

## If you noticed broken links

Some rounds produce a file called `<Country> - Sources to check by hand.xlsx`. Those are links the automatic
check could not settle — often a site that blocks robots but works fine in a normal browser. Fixing them by
hand is genuinely useful, but **optional**, and it needs the main machine to fold the corrections back in.
Mention it when you send the results rather than trying to apply them here.

---

## For the main machine — what to do with the package

*(This section is for Printec's Claude, not for the second machine.)*

The five countries were owned by the second machine while it was running them. When the results come home,
ownership comes home with them:

1. **Copy the files in.** Merge his `data/registries`, `data/source_candidates` and `data/run_logs` into the
   main project's, and his `deliverables/*.xlsx` into `deliverables/`. Every filename is country-specific,
   so nothing here overwrites existing work — but check that before copying, not after.
2. **Take ownership.** Add `CZ`, `HU`, `XK`, `ME`, `MK` to the `scopes` list in
   `data/campaign_assignment.json` on the main machine.
3. **Record what he completed.** Add his thirty `[scope, workstream]` pairs to the `done` list in
   `data/campaign_state.json`. His own copy of that file is the authoritative record of what actually
   finished — read it rather than assuming all thirty are there.
4. **Check the counts.** `python scripts/campaign.py --status` should then show `"done": 60` of
   `"total": 103` — the main machine now owns every scope in the plan again, with 43 sets left: the six
   remaining countries (36 sets) plus the seven region-wide sets. Then open one of his spreadsheets and confirm it
   holds real sources, in the local language. Do not take the driver's count as proof the work is good —
   it only knows what it was told.
