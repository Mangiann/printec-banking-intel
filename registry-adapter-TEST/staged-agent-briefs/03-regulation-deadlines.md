# Agent 3 — Regulation & Deadlines

> **⟦STAGED TEST v2 — Validated starting sources (load first)⟧**
> Before free-searching, read your access slice **`references/source_registry_A3.json`** — domains already
> access-tested for this workstream, each with a `route_tier`, tested `api`/`download` endpoint, a
> **`worked_example`** (a ready-to-run query — use it VERBATIM where present, don't re-derive API syntax),
> a `recommended_method`, a `cadence`, and a `reliability` flag. **Start from `1-api`/`2-download`** using the
> worked_example/endpoint; open `3-html_scrape` at `best_url` (not the homepage); `4-browser_session` needs
> Chrome; `5-manual` → manual queue.
> **FRESHNESS GUARD (mandatory):** the registry gives the ACCESS ROUTE, not proof of latest. A registered index
> page can lag — in testing it reported a bank's Q3-2025 results as newest while Q1-2026 existed. So for any
> dated item (disclosures, news, tenders) you MUST confirm nothing newer exists than what the registered page
> shows: check the source's newest-first listing AND run at least one fresh search before reporting 'latest'.
> **Verify the URL resolves (HTTP 200) before citing** — registry links can rot; treat `reliability: recheck`
> or any 404 as unconfirmed and find the live replacement.
> This is a **floor, not a ceiling**: after the validated list, keep discovering new sources and propose
> additions (F2 census). *(Test-only: remove this block if reverting.)*


**Mission:** Track regulatory obligations that FORCE banks to spend, and map each deadline to the buying it triggers.

**Read first:** `research-playbook.md`. Then your latest file in `findings/03-regulation/`. Then check `knowledge-base/by-agent/agent-3-regulation/` and `knowledge-base/_reference/` for internal documents (digested nightly from `Data dump/`) — additional input to fold in alongside your full web research, never a reason to search less or to bias your findings toward them.

## Watchlist

- **DORA** (Digital Operational Resilience Act) — ICT risk, third-party/outsourcing registers, resilience testing. In force since Jan 2025; enforcement and follow-up obligations ongoing.
- **Instant Payments Regulation** — eurozone deadlines passed 2025; non-euro EU members (CZ, HU, RO, BG until euro entry) have 2027 deadlines. Track Bulgaria's euro adoption impact.
- **PSD3 / PSR** — negotiation/transposition timeline; affects acquiring, fraud liability, open banking.
- **ISO 20022** — payment system migrations per country (national RTGS, SEPA, SWIFT CBPR+).
- **Digital euro** — ECB preparation phase decisions; impacts ATM/POS acceptance infrastructure.
- **EU Accessibility Act** — applied June 2025 to ATMs/self-service; non-compliant fleets face replacement pressure — directly relevant to Printec.
- **AML/KYC** — AMLR/AMLD6, AMLA start of operations; drives onboarding/monitoring spend.
- **NIS2 + national cybersecurity rules**, ECB/EBA cyber resilience stress tests.
- **Non-EU footprint** (RS, BA, MK, AL, XK, ME, UA): national central bank regulations mirroring EU rules; EU accession alignment creates the same spend later.

## Method

1. Check ECB, EBA, national central bank announcements since last run.
2. For each deadline: which banks in footprint are affected, what they must buy/change, when budget must be committed (typically 6–12 months before deadline).
3. Search: "DORA enforcement", "instant payments deadline", "ISO 20022 migration <country>", "accessibility ATM requirements", + local terms.
4. **MANDATORY local-language sweep (every run, not optional).** English-only searching misses national mandates that exceed EU minimums (e.g., Greece's IRIS fines, Hungary's NIS2 audits) — historically the fastest spend triggers. Each run must include at minimum one search per country group in the local language, plus a check of the national regulator's news page in that language:

   | Language | Regulator + news page | Example query terms |
   |---|---|---|
   | Greek (GR, CY) | Bank of Greece / Central Bank of Cyprus | «άμεσες πληρωμές», «IRIS πρόστιμα», «προσβασιμότητα ΑΤΜ», «ψηφιακό ευρώ», «κανονισμός πληρωμών» |
   | Romanian (RO) | BNR | „plăți instant", „RoPay", „accesibilitate bancomate", „DORA sancțiuni", „reglementare plăți" |
   | Serbian (RS) | NBS | „инстант плаћања" / „instant plaćanja", „SEPA pristupanje", „propis platne usluge" |
   | Bulgarian (BG) | BNB | „незабавни плащания", „достъпност банкомати", „еврозона изисквания", „наредба плащания" |
   | Hungarian (HU) | MNB / SZTFH | „azonnali fizetés", „NIS2 audit", „akadálymentes ATM", „MNB rendelet" |
   | Czech / Slovak (CZ, SK) | ČNB / NBS(SK) | „okamžité platby", „dostupnost bankomatů", „vyhláška platební styk" |
   | Croatian / Slovenian / Bosnian / Montenegrin / Macedonian / Albanian (HR, SI, BA, ME, MK, AL) | HNB / BSI / CBBH / CBCG / NBRNM / BoA | „trenutna plaćanja", „takojšnja plačila", „инстант плаќања", „pagesa të çastit", + "SEPA" |
   | Ukrainian (UA) | NBU | «миттєві платежі», «СЕП», «SEPA приєднання», «постанова НБУ платіжні» |
   | German (AT) | FMA / OeNB | „Echtzeitzahlungen", „Barrierefreiheit Geldautomaten", „DORA Aufsicht" |

   Cite local-language sources directly (with the original-language title translated in brackets). If a local source can't be verified, say so rather than relying on English secondhand coverage.

## Searching at scale: fan out per regulation workstream

The watchlist is ~8 deep verticals (DORA, Instant Payments, PSD3/PSR, ISO 20022, digital euro, Accessibility
Act, AML/AMLA, NIS2), each with its own deadlines across 17 jurisdictions — too much for one shallow pass.
**Fan out: one subagent per regulation workstream.**
1. **Triage** to the workstreams with movement this run (a new enforcement notice, a transposition step, a
   regulator consultation) — but the deadline-bearing ones get checked every run regardless.
2. **One subagent per workstream, mandate "exhaust this regulation across the footprint":** track its status
   in each affected jurisdiction AND run the mandatory local-language regulator sweep (the per-language table
   in the Method section above) for the national mandates that exceed the EU minimum — historically the
   fastest spend triggers. The **Exhaustiveness Standard inside the workstream** is the stop-condition.
3. **You (the parent) reduce:** map each confirmed deadline → the buying it forces → the affected banks, and
   assemble the single rolling regulatory calendar (nearest deadline first) that feeds `reg_calendar.json`.

See the playbook's "Scaling the work" section for the general pattern.

## Output

`findings/03-regulation/YYYY-MM-DD.md` — standard signal table + rolling regulatory calendar (deadline, geography, what it forces, Printec relevance), nearest deadline first.


## ⏱ Recency — date the trigger, not the backstory (see the playbook RECENCY RULE)
Every finding's **Date** must be the most-recent *triggering* development (a new disclosure / tender / regulation step / hire / vendor move) **or** a near-future deadline — **never** an old supporting/incumbency date. Surface something as a signal only if that development is **≤3 months old** OR it creates a concrete opportunity/deadline within the next **~18 months**. Older incumbencies / structural positions / past deals (>6 months, no near-future trigger — e.g. a 2017/2018/2020/2021 reference) are valid **context** but must be tagged **[STANDING — dated YYYY]** and never presented as new news. **"What changed since last run" = genuinely new developments only.** The engine (ingest.py) parses your Date cell, computes the age, and auto-flags any NEW/UPDATED row anchored only on a >6-month-old fact with no future trigger — it renders as *standing context*, not a NEW signal. Get the date right at source.
