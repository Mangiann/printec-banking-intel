# Greece Data-Capture Test — Improvement Log

**Started:** 2026-06-30 | **Owner:** Kostas Karakasiliotis
**Vehicle:** Greece-only interactive run of the full collector flow (Agents 1–6 → Orchestrator → engine).

## Method (agreed)

1. Run the **full flow for Greece interactively**, one step at a time, with operator approval before each agent/script run.
2. **Change nothing during the test.** Every problem, gap, or idea is recorded here as a finding — no edits to scripts, briefs, or config mid-run.
3. **HARD RULE (operator, 2026-07-01): never alter ANY production file (scripts, references, intel-cache, dashboard data) during the test.** All test work happens in a **dedicated, isolated test folder** with **new files for Greece only** — copies, never the live ones. Production stays untouched until we decide to implement.
4. At the **end**, implement the agreed findings as one batch.
5. **Re-run the Greece flow on the improved version** and compare against the as-is baseline to measure the difference.

> **Status 2026-07-01:** test NOT yet started. A previous attempt to edit `fetch_ted.py` in production was **reverted** — the file is back to its original state. Next session: (a) settle the CPV/sourcing question (F5), (b) set up the isolated test folder, (c) then begin Step 1.

Status key: 🟢 Agreed · 🟡 Proposed (to decide) · 🔵 To verify during run · ✅ Implemented (end of test)

---

## Findings

### F1 — Add a banking-sector CENSUS unit to Agent 1 🟢 Agreed
**Problem:** The bank list in `agent-units.json` is hand-curated and only updated reactively (a human re-encodes a merger/rename after a subagent happens to surface it — e.g. units already carry `crediabank-gr "(ex-Attica)"`, `alpha-cyprus "(ex-AstroBank)"`, `eurobank-cyprus "(ex-Hellenic)"`, all typed in after the fact). Nothing systematically checks whether our picture of the sector is still accurate. A **new bank entering Greece**, a **rename**, or an **exit** can go unnoticed.
**Fix:** Add an Agent-1 unit "Greek banking-sector census" — one subagent that each run pulls the authoritative registers (**Bank of Greece register of credit institutions**, **Hellenic Bank Association members**, **ECB SSM supervised-entities list**) and **diffs them against the unit list**, flagging new licences, mergers, renames, exits. Mirrors the existing `horizon-scan` (A3) and `new-competitor-scout` (A6) discovery-unit pattern.
**Scope note:** start with Greece; generalise to the full footprint after the test proves it.

### F2 — Add a procurement-SOURCE-discovery unit to Agent 2 🟢 Agreed
**Problem:** Agent 2 only fans out over *known* portals. Niche or bank-owned RFP pages we haven't catalogued are found only by luck. (Partly mitigated for above-threshold tenders because ΚΗΜΔΗΣ/Diavgeia + TED are mandatory publication points by law; real exposure is below-threshold / bank-internal RFPs.)
**Fix:** Add an Agent-2 unit "Greek procurement-source discovery" — a subagent that sweeps for bank-owned RFP pages and niche/sub-threshold procurement sources not in the catalogue, and proposes additions to the portal list.

### F3 — KB / Data-dump processor should emit ENTITY & SOURCE-change signals 🟢 Agreed
**Problem:** Documents dropped in `Data dump/` frequently *announce* exactly the things the census (F1/F2) needs — a merger, a rebrand, a new entrant, a new vendor/portal. Today the `data-dump-processor` digests a doc into per-agent summaries but does **not** specifically extract "the banking/source universe changed" signals.
**Fix:** Extend the `data-dump-processor` SKILL so that, while digesting each new document, it also identifies and flags **new/renamed/merged/exited banks** and **new portals/sources/vendors** mentioned, and routes them as structured "entity & source updates" into the census mechanism (feed F1/F2 — e.g. a dedicated digest section or a note to Agents 1/2). Keep it cited (page/slide), never invented.

### F4 — Fix the Greek keyword tags in `fetch_ted.py` 🟡 Proposed (reverted from production)
**Problem:** The Greek relevance keywords are wrong/over-generic: `τραπεζομηχάν` (not a real Greek word for ATM) and `αυτόματ` (matches "automatic anything"). Low coverage impact (keywords only set a `relevant=true` triage flag, not part of the TED query) but they mis-prioritise.
**Proposed fix:** proper lowercase Greek stems (`τραπεζ`, `ατμ`, `αυτόματη ταμειολογιστική`, `ανάληψη μετρητ`, `ταμειακ`, `τερματικ`, `κάρτ`, `πληρωμ`, `συναλλαγ`, `αυτοεξυπηρέτησ`, `μετρητ`, `λογισμικ`, `πληροφοριακ`, `ασφάλει`, `συντήρησ`, `χρηματοκιβ`). **To apply in the test folder, NOT production.**

### F5 — TED sourcing scope / CPV strategy — REOPEN, needs design 🔴 To discuss
**Problem:** the script uses only 6 narrow CPV roots, so software-only tenders (AML, onboarding, monitoring, core) are invisible. I broadened CPV (added 48000000/72000000/66000000 + cards/hardware/telecoms) — **operator rejected this: "the new CPV are crap, we need to talk about those further."** The broad roots were also reverted.
**Why it's bigger than a CPV list:** ties into the vision below — detailed tender/disclosure data is only wanted for the **footprint**; the **rest of the world is for TRENDS**, not tender-level capture. So the CPV question is really *"what exactly do we deterministically pull for the footprint, and how do we model breadth-for-trends vs depth-for-footprint?"* **Decide together next session before any edit.** All experimentation in the test folder only.

### F6 — Chrome control unavailable in this (enterprise) session 🔵 To verify
**Problem:** Operator reports the enterprise Claude session lacks the browser control that the personal account had. JS-only Greek portals (ESIDIS / ΚΗΜΔΗΣ / Diavgeia) were historically read via Chrome; without it they are **degraded** (fall back to API → primary-source PDF → Google cache → bank/regulator sites → local press), not impossible.
**To do:** at Step 3 (Agent 2), actually test whether Chrome control responds in this session before choosing the route; document the fallback actually used and the resulting coverage. If permanently unavailable, record it as a standing environment constraint and judge whether the deterministic fallbacks are sufficient for Greek tenders.

---

## Vision & direction (operator note, 2026-07-01 — verbatim, to develop tomorrow)

> "We are not looking the dashboard from the right angle. We are analysts, so we need to be able to show the image of the market from the large scale, like wtf is going on with banking, what are the trends, short term and long term. Then identify based on the system we designed (but properly executed) the current data and what others are doing. Then be able to focus on groups like world - americas - europe - SEE - Balkans - Printec footprint - Asia - India - China - etc. Of course we only get the detailed data like tenders, disclosures and stuff only from the footprint, and for all the broaded we just see the trends and what they are doing in general so that we might find something to copy or see the future for our footprint. Then we can tell a different kind of story in the dashboard, we could really make a 3D globe and be able to zoom more and more to trends and eventually oportunities. We need to find a way to make a network of the information and all data and create logical hypotheses and suggestions for the reader and so much more.
>
> This all, provided we first solve the problem of how to really be thorough and complete in our searches no matter how much time it takes for the agents to run, and I'm pretty sure we have not identified all the sources of information about trends. I mean, I haven't seen youtube transcriptions of videos talking about trends, and that is one thing I know. What about blogs, other stuff, I'm sure we can do a better job."

**Key threads to work through (derived from the note — for discussion, NOT yet actioned):**
1. **Reframe the product as an analyst's market lens** — lead with "what's going on in banking, the short- and long-term trends," not a deal list.
2. **Two data tiers by geography:** *depth* (tenders, disclosures, deal-level) only for the **footprint**; *breadth/trends-only* for the rest of the world (world · Americas · Europe · SEE · Balkans · footprint · Asia · India · China …) — watched to spot what to copy / future signals for the footprint.
3. **A different dashboard story** — possibly a **3D globe**, zoom from world → region → trends → opportunities; an **information network/graph** linking data into **logical hypotheses + suggestions** for the reader.
4. **Prerequisite (must solve FIRST):** make the searches genuinely **thorough & complete**, regardless of agent runtime. We have NOT catalogued all trend sources — explicitly missing: **YouTube video transcripts**, **blogs**, and likely more. Source-discovery for *trends* is a known gap (separate from the footprint-entity census in F1/F2).

## Run log (what we actually executed)

_(nothing executed yet — test not started)_
