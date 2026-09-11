# Source scouting — Czech Republic · Hungary · Kosovo · Montenegro · North Macedonia

This machine does **one job**: find the sources that publish banking-and-payments information in five
countries, and catalogue them in a spreadsheet. Nothing else.

It does **not** download documents, read them, extract facts, or build anything. Those stages of the wider
Printec system run on the main machine, and **their code is not in this folder** — so they cannot be started
here by accident.

## The job

Six researches per country, thirty rounds in total:

| Code | Research | What it looks for |
|---|---|---|
| A1 | Disclosures | annual reports, investor relations, earnings, press releases |
| A2 | Tenders & Procurement | procurement portals, tender and award notices, public contracts |
| A3 | Regulation & Deadlines | central banks, supervisors, consultations, rule deadlines |
| A4 | Market Statistics | payment and card statistics, cash/ATM/POS data, adoption |
| A5 | Early Intent & Jobs | job postings, leadership moves, org changes |
| A6 | Vendors & Competitors | competitor and vendor sites, case studies, partners, events |

Each round searches in the country's own language **and** English, checks every link is alive, judges each
find, and files the survivors.

## What comes out

Two spreadsheets per country, in `deliverables/`:

- **`<Country> - Banking & Payments Sources.xlsx`** — the catalogue. One row per source: what it is, who
  publishes it, what it covers, which research it belongs to, whether the link works, and whether we are
  allowed to use it. This is the deliverable.
- **`<Country> - Sources to check by hand.xlsx`** — the handful of links the automatic check could not
  settle. Optional; the main machine folds corrections back in.

Behind each spreadsheet sits that country's register (`data/registries/<ISO>.db`). The spreadsheet is
generated from it, so **both** go back to Printec at the end — an edited spreadsheet is silently out of step
with the register behind it.

## The scope fence — do not go outside it

`data/campaign_assignment.json` names the five countries this machine owns. The other eleven are being
scouted on the main Printec machine **right now**.

The driver enforces this: it will not hand out another country's round, and will refuse to mark one done.
**Do not widen that file** without the project owner's say-so. Two machines on one country means a wasted
four-hour round and two spreadsheets that overwrite each other. A refusal is the system working.

## How a round runs

One command asks what is next, and the answer contains everything else:

```bash
PYTHONIOENCODING=utf-8 python scripts/campaign.py --next
```

It returns one country + one research, fully resolved — the languages to search in, the register to write
to, the spreadsheet that grows, and the exact commands for each later stage. Then: discover (about 28 agents
search) → check every link → judge each find → file it → tick it off. **One round per sitting, about
50 minutes.** Full detail: `routines/source_discovery_scout/SCOUT_ROUTINE.md`.

`PYTHONIOENCODING=utf-8` goes on **every** Python command. It is terminal character-encoding only — it has
nothing to do with the search language. Search languages come from each country's own setting: Czech
Republic → cs + en; Hungary → hu + en; Kosovo → sq, sr + en; Montenegro → sr + en; North Macedonia → mk + en.

## The rules that bind this work

Read `docs/PROTOCOL.md` — it is binding, not guidance. In short:

1. **Never run a stage alone** — run the routine.
2. **A stage that cannot run STOPS the round** — report it, never skip it.
3. **The ledger is written LAST** — after the output is stored, never before.
4. **Prove every zero** — "nothing found" is a claim; show total-versus-matched.
5. **A bound may exist; a silent bound may not** — always report what was excluded.
6. **Code decides, agents propose** — an agent never certifies its own work.

Once, three stages were run and seven skipped — including both quality gates — and nothing errored. Every
command reported success throughout. That is why the routine is run whole, never stage by stage.

## Working with this user

- **Plain English. Always.** Short sentences, no jargon, no file paths or function names in explanations.
  Answer the question in the first sentence.
- **Propose before executing.**
- **Never oversell.** Check numbers against the spreadsheet yourself; do not repeat a sub-agent's summary as
  fact. Say plainly what did not work.
- **Token cost is a real constraint.** Say what something will cost before spending it.

## Standing constraints

- **Five countries only** — CZ, HU, XK, ME, MK.
- **Scouting only.** Finding sources, never fetching or reading what they publish.
- **This folder is not under version control.** A mistaken edit cannot be undone — copy a file before
  changing it, and delete nothing in `data/`.
- **Results go back whole.** See `../HANDING RESULTS BACK.md`.
