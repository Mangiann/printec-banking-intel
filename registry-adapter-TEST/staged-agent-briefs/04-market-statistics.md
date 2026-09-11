# Agent 4 — Market Statistics

> **⟦STAGED TEST v2 — Validated starting sources (load first)⟧**
> Before free-searching, read your access slice **`references/source_registry_A4.json`** — domains already
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


**Mission:** Track structural data on cash, branches, ATMs, and payments per footprint country — the demand backdrop for Printec's products.

**Read first:** `research-playbook.md`. Then your latest file in `findings/04-statistics/`. Then check `knowledge-base/by-agent/agent-4-statistics/` and `knowledge-base/_reference/` for internal documents (digested nightly from `Data dump/`) — additional input to fold in alongside your full web research, never a reason to search less or to bias your findings toward them.

## Sources

- ECB Data Portal — payment statistics (cards, instant credit transfers, POS counts, ATM counts), published ~annually with mid-year updates.
- EBA reports and risk dashboards.
- National central banks: Bank of Greece, BNR (RO), BNB (BG), NBS (RS), CNB (HR), Banka Slovenije, ČNB (CZ), NBS (SK), MNB (HU), NBU (UA), Central Bank of Cyprus, and the smaller-market central banks.
- National banking associations (e.g., Hellenic Bank Association — publishes Greek branch/ATM counts).
- Eurostat (cash usage proxies), SPACE survey (ECB cash study).

## Automated structural back-series (already pulled for you — don't re-report it)

The engine now runs **`fetch_ecb.py`** at the start of every weekly run (`run_weekly.py`), pulling the
multi-year ECB Data Portal series for all 10 EU footprint countries — **ATMs, POS terminals, bank branches,
cash withdrawals** — into `intel-cache/structural_series.json`, which `ingest.py` merges into the dashboard's
per-country trend charts + forecast. So you do **not** need to hand-transcribe ECB ATM/POS/branch/cash history
into the workbook anymore. Focus your effort on what the ECB feed can't give:
- **Non-EU markets** (Serbia, Ukraine, Albania, BiH, Kosovo, Montenegro, N. Macedonia) — ECB has no data; build
  their multi-year series from the central banks (NBS, NBU, etc.) and put them in the workbook as `Sector`-scoped
  annual rows so they chart too.
- **Longer ATM history** (ECB's half-yearly ATM/POS series only start ~2022) — pull deeper national series where
  available (e.g. Greece's HBA goes to 2014), as `Sector` rows.
- **Leading indicators** (Google Trends, app-store, eKYC) and the latest provisional figures, as before.

## Proven data routes (validated 2026-06-12 — use these first)

**HARD RULE: search in the local language FIRST for every non-EU market. English-only searches falsely reported gaps for UA, AL, MK, XK that local-language searches filled immediately.**

**HARD RULE (access): a 403/JS block to WebFetch is NOT a dead end — retry the SAME primary URL with a desktop-browser User-Agent BEFORE falling to press.** Many national central-bank sites (NBU `bank.gov.ua`, NBRNM `nbrm.mk`, Bank of Albania `bankofalbania.org`, NBS `nbs.rs`, CBK `bqk-kos.org`) return 403 to the bare fetch tool but serve the page to a normal browser UA: `curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36" "<url>"`, then extract any PDF text locally with `pdfminer.six`/`pdftotext`. This route reached the CBK PDFs in the 2026-06-24 run; using it first keeps figures at **primary/regulator tier** instead of being capped at Low because only a press snippet was reachable. Only after the UA-retry fails do you drop to a cached snippet/press — and log the blocked URL + the route you used.

ECB Data Portal API (direct CSV, no UI needed — substitute country codes/years):
- Branches (annual): `https://data-api.ecb.europa.eu/service/data/SSI/A.<CC>.122C.N40.1.A1.Z0Z.Z?format=csvdata&startPeriod=<YYYY>`
- ATMs (half-yearly): `https://data-api.ecb.europa.eu/service/data/PTN/H.<CC>.W0.2221._T.PN?format=csvdata&startPeriod=<YYYY>` (POS = terminal type `2222`)
- Cash withdrawals (half-yearly): `https://data-api.ecb.europa.eu/service/data/PAY/H.<CC>.W0.CW1.1._Z.N.PN?format=csvdata&startPeriod=<YYYY>`
- Multiple countries: `GR+CY+AT+HR+SI+SK+BG+RO+HU+CZ` in the country position. Watch for OBS_STATUS "P" (provisional) and series breaks (BG POS 2023-S1; CY POS 2025-S1).

National 2026-frequency sources (faster than ECB's annual cycle):
- Serbia: NBS monthly IPS PDFs ([ips.nbs.rs](https://ips.nbs.rs/en)); quarterly payment-services releases; branch counts only inside NBS quarterly Banking Sector Report PDFs.
- Ukraine: NBU quarterly card-market releases — SEARCH IN UKRAINIAN ([bank.gov.ua](https://bank.gov.ua/ua/news/all)); branch counts via RBC-Ukraine citing NBU.
- Greece: DIAS statistics ([dias.com.gr](https://www.dias.com.gr/en/statistics2024/)) for IRIS; HBA for branches/ATMs.
- Hungary: MNB quarterly payment stats ([statisztika.mnb.hu](https://statisztika.mnb.hu/en)); ATM-program coverage in Hungarian business press.
- Romania: BNR interactive database; bankingnews.ro and cursdeguvernare.ro reliably relay BNR card/ATM/POS data.
- Bulgaria: BNB monthly currency-circulation stats (euro-changeover tracking through 2026).
- Croatia: HNB annual "Payment Cards and Card Transactions" PDF (official ATM counts incl. contactless/security splits — ECB PTN series for HR is noisy, don't use alone).
- Czechia: ČNB half-yearly payment statistics commentary; CERTIS stats page.
- Albania: Bank of Albania payment stats, heavily covered by monitor.al — search in Albanian.
- North Macedonia: NBRNM quarterly tables ([nbrm.mk](https://www.nbrm.mk/platiezhna_statistika.nspx), 90-day lag) — search in Macedonian.
- Kosovo: CBK monthly payment-systems reports + annual card-usage report ([bqk-kos.org](https://bqk-kos.org)).
- BiH: CBBH dashboard is login-gated — use CBBH Quarterly Bulletin PDFs + FBA/ABRS agency reports.
- Montenegro: CBCG annual payment-system report PDF (monthly releases lack terminal counts).
- Vendor proxies for current-year signals: NCR Atleos, Euronet, Diebold, Glory, Worldline quarterly earnings (Q1 reports ~late Apr/early May).

## Leading indicators (forward-looking — they move BEFORE the ECB structural counts)

The sources above are mostly *lagging* (they tell you what already happened to ATM/branch counts). Add a
short **leading-indicator sweep** each run — these arrive months earlier and feed the dashboard's Outlook
(forecast) layer. Record them as dated time-series where you can, so the trend can be projected:

- **Google Trends** (trends.google.com): footprint-country interest in terms like instant payments
  («άμεσες πληρωμές», „plăți instant", «миттєві платежі»), mobile/online banking, SoftPOS, "ATM near me".
  A rising query trend is an early demand signal. Note the relative index + the direction.
- **App-store adoption**: top-charts rank and recent rating-count growth of the leading banks' mobile apps
  (App Store / Google Play, per country) — a proxy for digital-channel momentum and where self-service is
  displacing the branch fastest.
- **Web traffic** (Similarweb free tier): visits trend to banks' digital-product / onboarding pages — a
  proxy for digital-onboarding demand.
- **Mobile-banking & eKYC adoption** where published (e.g. gov.gr eKYC users, central-bank digital-payment
  dashboards) — already partly in the workbook; keep the series growing.

Flag each as **leading** in the notes so it is read as a momentum signal, not a structural count. Where a
metric has ≥3 dated points, the engine will project it automatically.

## What to track (per country, time series)

ATM count and trend; bank branch count and trend; cash withdrawals (volume/value); card payments at POS;
instant payment adoption; POS terminal counts; cash-in-circulation; **plus the leading indicators above**.

## Recency & provisional data (chase the latest; flag the uncertain)

- **Chase the freshest annual count.** Structural ATM/branch totals publish with a lag, so a series can sit
  a year behind. Re-pull each country's authoritative annual figure the moment it lands — for Greece, the
  **HBA "Greek Banking System Overview"** and **Bank of Greece** (likely H2 2026 for the 2025 numbers);
  don't wait for the slower ECB annual cycle. Note the expected publication month so the next run re-checks.
- **Mark provisional figures as provisional.** When you record an interim / half-year / OBS_STATUS "P"
  value, set its Confidence to **Low** (or put "provisional" in the notes). The forecast engine then flags
  it distinctly (a ◇ marker) on the Outlook chart and keeps it out of the firm trend line — so an early
  read is visible without polluting the projection.

## Interpretation guide (always connect to need)

- Branches falling + ATMs steady → self-service/offsite ATM demand, managed services.
- ATMs falling fast → fleet consolidation → replacement/pooling/outsourcing opportunity.
- Cash usage resilient + bank cost pressure → cash recycling demand.
- Instant payments growth → fraud monitoring + payments infrastructure demand.
- POS terminal growth → acquiring/terminal estate opportunities.

## Searching at scale: fan out per country

The EU structural counts are already SCRIPTED for you (`fetch_ecb.py` — see above), so don't spend agents
re-pulling ECB ATM/POS/branch/cash. Where fan-out pays is everything the ECB feed can't give. **Fan out: one
subagent per country**, weighted to the markets that still need hand-collection.
1. **Triage:** the **non-EU markets** (RS, UA, AL, BA, XK, ME, MK) always need a subagent — ECB has nothing
   for them; an EU market needs one only to chase a freshly-published national figure or a leading indicator.
2. **One subagent per country, mandate "exhaust this market's structural data":** use that country's proven
   data route (the per-country list above — NBS IPS PDFs, NBU Ukrainian-language releases, CBK monthly
   reports, HNB card PDF…), **search in the local language FIRST** (the hard rule — English-only falsely
   reported gaps for UA/AL/MK/XK), build the multi-year series as `Sector` rows, and run the leading-indicator
   sweep (Google Trends, app-store, eKYC). Local-language **Exhaustiveness Standard inside the market** is the
   stop-condition.
3. **You (the parent) reduce:** assemble the per-country trends table, mark provisional figures Low (so they
   ◇-flag and stay out of the firm trend line), and keep the workbook series growing.

See the playbook's "Scaling the work" section for the general pattern.

## Output

`findings/04-statistics/YYYY-MM-DD.md` — standard signal table for NEW/UPDATED data only + a country trends summary table (Country | ATMs | Branches | Cash trend | Instant payments | Implication).


## ⏱ Recency — date the trigger, not the backstory (see the playbook RECENCY RULE)
Every finding's **Date** must be the most-recent *triggering* development (a new disclosure / tender / regulation step / hire / vendor move) **or** a near-future deadline — **never** an old supporting/incumbency date. Surface something as a signal only if that development is **≤3 months old** OR it creates a concrete opportunity/deadline within the next **~18 months**. Older incumbencies / structural positions / past deals (>6 months, no near-future trigger — e.g. a 2017/2018/2020/2021 reference) are valid **context** but must be tagged **[STANDING — dated YYYY]** and never presented as new news. **"What changed since last run" = genuinely new developments only.** The engine (ingest.py) parses your Date cell, computes the age, and auto-flags any NEW/UPDATED row anchored only on a >6-month-old fact with no future trigger — it renders as *standing context*, not a NEW signal. Get the date right at source.
