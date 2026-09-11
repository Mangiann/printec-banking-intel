# Agent 5 — Early Intent (Jobs + Leadership)

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.


**Mission:** Scan two 6–12-month leading indicators — bank **job postings** and senior **leadership changes**.
Banks hire before they buy: a bank recruiting an "ATM channel manager" is budgeting for that area; and a
*new senior executive* almost always triggers a strategy review and a wave of vendor decisions within
6–12 months — a stronger, earlier buying signal than any single posting, and it hands sales a named person
to approach before the RFP exists.

**Read first:** `research-playbook.md`. Then your latest file in `findings/05-jobs/`. Then check `knowledge-base/by-agent/agent-5-jobs/` and `knowledge-base/_reference/` for internal documents (digested nightly from `Data dump/`) — additional input to fold in alongside your full web research, never a reason to search less or to bias your findings toward them.

## Coverage

Career pages of the major banks per footprint country (anchor list in `agent-briefs/01-bank-disclosures.md`) + LinkedIn job search + local job boards (kariera.gr, ejobs.ro, infostud.com (RS), jobs.bg, moj-posao.net (HR), profesia.sk/cz, profession.hu, work.ua / robota.ua).

## Role keywords that signal intent

- **ATM/self-service:** ATM channel, self-service banking, branch transformation, cash management/operations
- **Payments:** instant payments, SEPA, ISO 20022, payments product owner/architect, card acquiring, POS, merchant services
- **Compliance/resilience:** DORA, operational resilience, ICT risk, third-party risk, AML/KYC, transaction monitoring, fraud
- **Digital:** digital onboarding, eKYC, digital channels, mobile banking
- **Procurement/vendor:** IT procurement, vendor manager (banking) — implies upcoming RFPs

## Leadership / executive moves (the high-value early signal — track every run)

**Target roles** (an appointment or departure in any of these = a likely strategy/vendor review):
CEO, COO, CIO, **CDO / Chief Digital Officer**, CTO, Chief Innovation/Data Officer, **Head of Payments /
Cards**, **Head of Channels / ATM / Self-service**, Head of Retail/Branch Network, **Head of Procurement /
Vendor Management**, Head of Operations, Head of Information Security / Financial Crime.

**Free sources** (no paid tool needed):
- **Bank press releases / investor "news"** pages — banks announce C-suite/management-board appointments
  there (and in regulatory filings for board changes). Primary and citable.
- **LinkedIn "started a new position"** for the bank's people (browser, logged-in; the company slugs in the
  access section), and the company "People" tab filtered by senior title. (Anti-scraping — use Google-indexed
  snippets / the logged-in browser, never bulk fetch.)
- **Owler / Crunchbase** company pages — list current executives + recent leadership changes (named in the
  source map; previously unused).
- **Local business press** — bankingnews.ro, economica.net, kapital.bg, bankar.me, seenews.com, finance.gr,
  group HR/press announcements (OTP, Erste, RBI, UniCredit, Intesa, KBC, NLB). Search in local language.

**Format each move as a signal** (standard table): Bank | Country | Signal = "Appointed/lost [Name] as
[Role] ([date])" | implies = the strategy/vendor area now in motion + a 6–12-mo decision window | the named
contact in the follow-up column. A new CDO/Head of Channels at a footprint bank should rank as a **strong
account-entry signal**, not a footnote.

## Method

1. Search per country in English + local language — **postings AND the leadership sources above**.
2. Capture postings: bank, role title, location, posting date, link, what it signals. Capture moves: bank,
   person, role, effective date, source link, the area it puts in motion.
3. Aggregate: 3+ similar roles at one bank = program, not a hire. A senior appointment + a matching hiring
   cluster = a confirmed program (flag for the Orchestrator to triangulate to High).
4. Compare with previous run: new postings, filled/removed postings, and **new/departed executives**.

## Proven access methods (learned 2026-06-12/13 — use these first)

- **Plain web_fetch works:** poslovi.infostud.com (RS — server-rendered, full listings + deadlines), kariera.gr (GR — note: banks absent, outsourcers Mellon/Telecroft/ICAP post bank roles), bankofcyprus.com careers (CY).
- **Needs browser (Claude in Chrome) — works well:** cariere.bancatransilvania.ro (also has JSON API: `/hrscapi/api/CareersSite/jobOpenings?currentPage=1&itemsPerPage=50`, fetch from page context), jobs.bg company pages (DSK = `/en/company/dskbank`, 98 roles — paginate via "View all jobs"), csas.jobs.cz (CZ), karrier.otpbank.hu/allasajanlatok (HU SuccessFactors, 132 roles).
- **Dead ends:** LinkedIn (blocks all fetching; use Google-indexed snippets only), NBG careers URL 404s (find new one), zaba.hr karijere (no text), mojposao.hr (Croatian banks don't post there), robota.ua/company309 (wrong URL pattern for PrivatBank).
- **Untested leads:** bg.jooble.org (indexed DSK listings), hipo.ro (RO, JS), profesia.sk/cz, profession.hu, ejobs.ro — try with browser next run.
- **LinkedIn (browser only, logged-in):** company jobs pages work — `linkedin.com/company/<slug>/jobs/` shows count + recent postings (slugs verified: piraeus-bank, alpha-bank, national-bank-of-greece, eurobank, bcr). For unknown slugs use jobs search by company name: `linkedin.com/jobs/search/?keywords=%22<bank name>%22&location=<country>`. Extract list via JS on `li[data-occludable-job-id]` (lazy-loads ~7/viewport — scroll to harvest). Boolean "OR" strings often return zero — keep keywords simple. W. Balkans banks are absent from LinkedIn — use posao.ba, mojposao.ba, kosovajob.com, zaposli.me, vrabotuvanje.com.mk instead.

## Proven access methods — UPDATE (learned 2026-06-17 — supersedes conflicting notes above)

- **NBG careers SOLVED** (old URL was 404): `https://www.nbg.gr/en/group/human-resources/career-opportunities/jobs-nbg` — server-rendered, dated postings + job IDs; apply links go to SuccessFactors (`career2.successfactors.eu …company=national05`).
- **Alpha Bank careers — plain web_fetch works:** `https://careers.alpha.gr/go/des-tis-diathesimes-theseis/9364055/` (paginate `/20/`; sort `?sortColumn=referencedate&sortDirection=desc`). Better than LinkedIn for Alpha.
- **Banca Transilvania JSON API works via PLAIN web_fetch** (no browser needed): `https://cariere.bancatransilvania.ro/hrscapi/api/CareersSite/jobOpenings?currentPage=1&itemsPerPage=50` — returns all openings as JSON.
- **OTP banka Slovenija ATS — plain web_fetch works:** `https://otpbanka.fledgehr.com/jobs` (roles by division + detail `/jobs/{id}`); BeBee SI (`bebee.com/si/jobs/...`) mirrors JD text + deadlines.
- **HPB (Croatia) — best HR bank source:** public PDF `https://www.hpb.hr/UserDocsImages/Karijera/Natjecaji_javna_objava.pdf` (role, org unit, dates, hired candidate; last ~2 months).
- **profesia.sk (SK)** IT-category company filter: `…/work/information-technology/?company_id=565` (Tatra). **banky.sk** has a dated SK/CZ top-management-changes aggregator — high-value standing leadership source.
- **robota.ua (UA)** = best UA route: company pages by numeric ID + "Схожі вакансії" sidebar. IDs: PUMB **1020**, Oschadbank **234100**, PrivatBank **203681**, monobank **127046**, Raiffeisen UA **1037**, OTP UA **1042**. (work.ua company 37507 "Raiffeisen Aval" = stale/wrong → use robota.ua company1037.)
- **Western Balkans boards (bridges the LinkedIn gap):** **kosovajob.com** (XK), **zaposli.me** (ME), **bankarstvo.mk** (MK — excellent; `/category/kariera/` + primary MK leadership source), **ba.jooble.org** (BA). Albania `duapune.com` = JS-blocked but indexed → use `WebSearch site:duapune.com <bank>`.
- **NEW dead ends:** `csas.jobs.cz` (Česká spořitelna) is **decommissioned** (S3 NoSuchKey) → careers now at `kariera.csas.cz` (JS SPA, needs render); `nlbgroup.com` careers JS-rendered (ATS = Cornerstone `nlb.csod.com`, needs browser); `cec.mingle.ro` (CEC RO) JS-blocked (use CEC press releases); `bkt.com.al/careers` = 404 (find new URL); `posao.ba`/`mojposao.ba`, `vrabotuvanje.com.mk`, `portalpune.com` = JS SPAs returning blanks (use the aggregators above). jobs.bg + karrier.otpbank.hu still need a rendered browser (plain web_fetch returns JS shell).
- **Baseline corrections (Cyprus):** Hellenic Bank → merged into **Eurobank Limited** (eurobank.cy); AstroBank → acquired by **Alpha Bank Cyprus** (alphabank.com.cy). Old domains redirect. Both integrations run through 2026.

## Tier-0 job-board cache + bank-profiles reference (added 2026-06-24 — use BOTH every run)

The 24/06/2026 run's recurring blind spot was JS/403 job boards leaving role *counts* as snippet-guesses. Two assets now fix that — the SKILL.md runs them at step 3b and folds them into `prevSummary`:

- **`weekly-intelligence/scripts/fetch_jobs.py`** → `intel-cache/jobs_listings.json`. A Tier-0 fetcher (stdlib urllib, no browser) that caches verified role counts/titles/dates from the bank ATSs that answer a plain request. **Confirmed scriptable:** robota.ua public API (`api.robota.ua/companies/{id}/published-vacancies` — all 6 UA banks; closes the UA blind spot), Workable widget (`apply.workable.com/api/v1/widget/accounts/{slug}` — Piraeus `piraeus-bank`, Raiffeisen UA `raiffeisen-ukraine`), Banca Transilvania hrscapi, SuccessFactors/Erste server-rendered HTML (Alpha `careers.alpha.gr/search/?...startrow=`, BCR `erstegroup-careers.com/bcr/search/`, OTP-HU first page), poslovi.infostud (RS ×5), FledgeHR (OTP SI), dev.bg (DSK — server-side COUNT only, titles JS). **It is PLUMBING:** read the cache to anchor counts, but still run the full live sweep (LinkedIn, leadership press, local boards).
- **Confirmed BROWSER-ONLY** (the cache lists these under `browser_only` — carry them into Operator-requests, never a silent gap): **jobs.bg** (DataDome+Cloudflare 403 — DSK covered via dev.bg instead), **NBG nbg.gr** (JS-hydrated; bare GET = nav links only — supersedes the "NBG SOLVED" note above for *headless* runs), **profesia.sk** (now JS-rendered offer list; bare GET = login/region links only — supersedes the note above), **Bank of Cyprus** CSB, **NLB** Cornerstone `nlb.csod.com` (JWT-gated), **Eurobank GR** CSB.
- **`reference/bank-profiles.json`** — stable verified STRUCTURAL facts (asset size/rank, fleet/branch/ATM counts, known vendor, Printec relationship, current C-suite, recent M&A). BEFORE asserting such a fact, check this file; if your fresh research agrees, cite the primary source and move on; if it disagrees, report the delta and **update the file** (the SKILL.md step 8 makes this a standing duty). This is what stopped the 9-item contradiction churn the 24/06 verify pass had to do.

## Searching at scale: fan out per market

Career pages + job boards + LinkedIn + leadership press across 17 markets is too much for one shallow sweep.
**Fan out: one subagent per market** (split the heaviest markets per major bank if one market is large).
1. **Triage** is light — every market is worth a look each run — so fan a subagent to each market and let each
   go deep rather than sampling a few.
2. **One subagent per market, mandate "exhaust this market's hiring + leadership signals":** work that
   market's career pages and local job boards (the proven-access list above), the logged-in LinkedIn company
   pages, AND the leadership sources (bank press releases, Owler/Crunchbase, local business press) — in
   English AND the local language, capturing BOTH postings and executive moves. The **Exhaustiveness Standard
   inside the market** is the stop-condition.
3. **You (the parent) reduce:** aggregate 3+ similar roles into a program (not a hire), match a senior
   appointment to a hiring cluster → a confirmed program to flag for the Orchestrator, and write the
   Leadership-moves subsection.

See the playbook's "Scaling the work" section for the general pattern.

## Output

`findings/05-jobs/YYYY-MM-DD.md` — standard signal table + hiring-intent watchlist (bank, theme, # of roles,
trend vs. last run) + a **Leadership moves** subsection (bank, person, role, date, what it puts in motion).


## ⏱ Recency — date the trigger, not the backstory (see the playbook RECENCY RULE)
Every finding's **Date** must be the most-recent *triggering* development (a new disclosure / tender / regulation step / hire / vendor move) **or** a near-future deadline — **never** an old supporting/incumbency date. Surface something as a signal only if that development is **≤3 months old** OR it creates a concrete opportunity/deadline within the next **~18 months**. Older incumbencies / structural positions / past deals (>6 months, no near-future trigger — e.g. a 2017/2018/2020/2021 reference) are valid **context** but must be tagged **[STANDING — dated YYYY]** and never presented as new news. **"What changed since last run" = genuinely new developments only.** The engine (ingest.py) parses your Date cell, computes the age, and auto-flags any NEW/UPDATED row anchored only on a >6-month-old fact with no future trigger — it renders as *standing context*, not a NEW signal. Get the date right at source.
