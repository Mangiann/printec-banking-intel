# Setup instructions — for Claude

You are setting up a **source-scouting automation** on this machine. Work through the steps in order.
Every step has a check. **If a check does not produce the stated result, stop and tell the user — do not
work around it.** A setup that half-works here produces a spreadsheet that silently misses half a country.

---

## What this is

Printec runs a market-intelligence system for banking and payments across 16 countries. Step one of that
system finds the **sources** — the websites, portals and registers that publish useful information. That
step has already been completed for five countries on the main machine. This machine takes five more:

**Czech Republic · Hungary · Kosovo · Montenegro · North Macedonia**

Six researches per country (disclosures · tenders · regulation · statistics · jobs · vendors) = **30 rounds**,
about **50 minutes each**. The automation does one round at a time and picks up where it left off, so it
can be interrupted freely.

**Scouting only.** This machine finds and catalogues sources. It does **not** download what those sources
publish, read it, or extract anything from it — those later stages run on Printec's own machine, and their
code is deliberately **not in this package**. If something seems to be missing, it is missing on purpose.

**What comes out:** two spreadsheets per country in `deliverables/` — `<Country> - Banking & Payments
Sources.xlsx` (the catalogue, one row per source, tagged by research) and `<Country> - Sources to check by
hand.xlsx` (the few links the automatic check could not settle). Each is generated from that country's
register in `data/registries/`, so the register goes back to Printec too.

## The one rule that matters

**This machine may only run those five countries.** The other eleven are running on the main Printec machine
right now. If both machines ran the same country, that country would be scouted twice — four hours wasted —
and the two spreadsheets would overwrite each other.

The code enforces this. `data/campaign_assignment.json` names the five countries, and the driver refuses to
hand out or tick off anything else. **Never edit that file to get past a refusal.** A refusal is the system
working. If the user wants a different split, they must agree it with the project owner first.

---

## Step 1 — Put the project somewhere permanent

Copy the `project` folder out of this handover package to a permanent location — the user's Documents
folder is fine. Do **not** run it from inside a Downloads folder or a zip.

Ask the user where they want it. Then rename it something meaningful, e.g.
`Strategic Intelligence - Source Scouting`.

**Check:** the folder contains `scripts/campaign.py`, `research_plan.yaml` and a `data` folder.
From here on, run every command **from that folder**.

## Step 2 — Python

The system needs **Python 3.11 or newer** and exactly two extra packages.

```bash
python --version
```

If Python is missing or older than 3.11, stop and ask the user to install it from python.org (tick "Add
Python to PATH" during install). Then, from the project folder:

```bash
python -m pip install -r requirements.txt
```

**Check:**

```bash
python -c "import jsonschema, openpyxl; print('ok', jsonschema.__version__, openpyxl.__version__)"
```

It must print `ok` and two version numbers. Two packages is correct and complete — scouting catalogues
sources, it never downloads a document, so it needs neither a browser engine nor a PDF reader.

## Step 3 — Prove the code works

Run both tests from the project folder:

```bash
python tests/test_campaign_assignment.py
```

```bash
python tests/test_scout_config.py
```

**Check:** both must end with `OK`. The first proves the country fence holds; the second proves the
country/language settings resolve.

## Step 4 — Prove this machine knows which countries it owns

```bash
python scripts/campaign.py --status
```

**Check:** it must print `"owner": "Second machine"`, scopes `CZ, HU, ME, MK, XK`, and
`"done": 0, "total": 30, "remaining": 30`.

If it prints an `error` instead, `data/campaign_assignment.json` is missing from the copy — go back to
step 1 rather than creating the file yourself.

## Step 5 — Prove the fence actually refuses

This is a positive control. Ask the driver to tick off a country this machine does **not** own:

```bash
python scripts/campaign.py --complete GR A1
```

**Check:** it must **fail** — printing a message containing `is not assigned to this machine` and exiting
with a non-zero code. If it succeeds, the fence is not working: stop, and tell the user the setup is not
safe to run.

## Step 6 — Set up the automation

Create a scheduled task using the scheduled-tasks tool:

- **taskId:** `scout-campaign-step`
- **cronExpression:** `13,43 * * * *`
- **description:** *Every ~30 min: run one source-scouting round for the next pending set assigned to this machine (CZ, HU, XK, ME, MK), then stop. Skips while busy; resumes partial rounds.*
- **prompt:** the full text under "Prompt text" in `scheduled-task-prompt.md`, copied **verbatim**. Do not
  summarise it or improve it — it runs in a fresh session with no memory, so every word it needs is in it.

**Check:** list the scheduled tasks and confirm `scout-campaign-step` is there and **enabled**.

Then tell the user this, in plain words: *scheduled tasks only run while the Claude app is open. If the app
is closed when one is due, it runs the next time you open it.* Leaving the machine on with the app open
overnight is how the 30 rounds get through fastest.

## Step 7 — Run the first round yourself, and watch it

Do not leave the first round to the schedule. Run one now so any problem surfaces while you are watching.

```bash
python scripts/campaign.py --next
```

This prints a JSON descriptor and claims the set. Follow the "Prompt text" in `scheduled-task-prompt.md`
from STEP 2 onwards, using the values it gave you exactly.

**Check, when it finishes:** a spreadsheet has appeared in `deliverables/` named after the country, and
`python scripts/campaign.py --status` shows `"done": 1, "remaining": 29`.

Report to the user: which country and research ran, how many sources it found, and how many were new.

---

## What to tell the user when setup is done

- **What will happen:** one round about every hour, roughly 50 minutes each, 30 rounds in total. Realistically
  two to four days with the machine on and the app open.
- **What they will see:** one spreadsheet per country in `deliverables/`, growing as each research completes.
  Five files in the end.
- **What to do if something breaks:** nothing. A failed round is not marked done, so the next firing retries
  it from where it stopped. Nothing is lost.
- **How to check progress at any time:** `python scripts/campaign.py --status`.
- **When it is finished:** `--status` shows `"remaining": 0`, and the automation reports
  `done_all`. Then follow `HANDING RESULTS BACK.md`.

## Things you must not do

- **Do not edit `data/campaign_assignment.json`.** Five countries, no more.
- **Do not run a single stage by hand** to "save time". Run the routine. `docs/PROTOCOL.md` explains why at
  length: skipping stages is how this project once let 16,345 unverified facts through with every command
  reporting success.
- **Do not delete anything in `data/`.** This folder is not under version control; a deletion is permanent.
- **Do not add the missing stages.** This machine scouts for sources and stops there. The code that
  downloads documents, reads them and builds the knowledge graph is deliberately **not in this package** —
  that is not an oversight to helpfully fix. If a document looks worth fetching, note it and tell Printec.
