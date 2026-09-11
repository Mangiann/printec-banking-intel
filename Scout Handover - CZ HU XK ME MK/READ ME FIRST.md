# Read me first

Thanks for taking this on. Here is the whole thing in one page.

## What you are running

Printec is building a market-intelligence system for **banking and payments** across 16 countries. The first
step is finding the **sources** — the websites, portals, registers and statistics pages that publish anything
useful in each country. Five countries are already done. You are taking five more:

**Czech Republic · Hungary · Kosovo · Montenegro · North Macedonia**

You are not reading or analysing anything, and neither is the software. It searches — in each country's own
language and in English — works out which sites are worth tracking, checks the links work, and writes them
into a spreadsheet. It never downloads the reports, tenders or statistics those sites publish. That happens
later, at Printec, on a different machine. The code for it isn't even in this package.

## What it will cost you

- **A computer that can be left on**, with the Claude app open. It works in the background.
- **Two to four days**, unattended. Thirty rounds, about 50 minutes each, one at a time.
- **About 15 minutes of your attention at the start**, and a glance once a day.

It cannot break anything or lose work. If a round fails or the machine is switched off mid-way, it simply
picks that round up again next time.

## How to set it up

Open the Claude app, point it at this folder, and give it this instruction:

> Read "SETUP - give this to Claude.md" in this folder and follow it step by step.

It will check your Python, copy the project somewhere permanent, prove the setup works, and schedule the
automation. It will ask you where to put things. **If it reports that a check failed, don't wave it through
— send the message to Printec.** A setup that half-works produces a catalogue that quietly misses half a
country, and nothing will look wrong.

## The one rule

**Only those five countries.** The other eleven are running on Printec's own machine at the same time. If
both machines ran the same country, that country would be searched twice — four hours wasted — and the two
spreadsheets would overwrite each other.

The software enforces this: it will refuse to start, or to record, any country outside your five. **If it
refuses something, that is it working correctly.** Don't edit the settings to get around it, and don't let
Claude do so either. If you think the split should change, ask Printec first.

## What you will get

In the `deliverables` folder, filling up as it goes:

- **`<Country> - Banking & Payments Sources.xlsx`** — the catalogue, one per country. Each row is a source:
  what it is, who publishes it, what it covers, which of the six researches it belongs to, whether the link
  works, and whether we are allowed to use it. **This is the deliverable.**
- **`<Country> - Sources to check by hand.xlsx`** — a short list of links the automatic check could not
  settle, usually sites that block robots but work fine in a normal browser. Nothing you need to act on.

## How you'll know it's finished

Ask Claude "how is the scouting going?" any time, or run this in the project folder:

```bash
python scripts/campaign.py --status
```

When it shows `"remaining": 0`, you're done. Then open **`HANDING RESULTS BACK.md`** — it says exactly which
two folders to zip up and send back.

## What's in this package

| | |
|---|---|
| `READ ME FIRST.md` | This page. |
| `SETUP - give this to Claude.md` | The setup instructions. Give this to Claude, not to yourself. |
| `scheduled-task-prompt.md` | The text the automation follows on each run. Claude copies it during setup. |
| `HANDING RESULTS BACK.md` | What to send back when you're finished. |
| `project/` | The software. Claude copies this somewhere permanent in step 1. |
