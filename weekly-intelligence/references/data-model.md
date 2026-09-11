# Data model (intel-cache)

`ingest.py` writes these JSON files into the cache dir (`<research folder>/intel-cache/` by default).
Everything is derived from the master signal table and the history workbook — no fabricated values.

| File | Shape | Notes |
|---|---|---|
| `signals.json` | list of signal objects | One per active master-table row. Fields: `key`, `bank_theme`, `countries` (ISO2 list), `footprint_wide` (bool), `signal`, `implies`, `likelihood`, `confidence`, `follow_up`, `sources` [{text,url}], `agents` [A#], `date`, `products` (category ids), `primary_product`, `strength`, `size_band` (XL/L/M/S/Unscoped), `win_prob` (High/Medium/Low/""), `ev_score` (expected value), `status`, `week_first_seen`, `week_last_confirmed`, `is_new_this_week`. |
| `_ledger.json` | {signal key: first-seen week} | **Persistent week-over-week state. Do not delete.** Lets the dashboard say what is genuinely new vs. carried over. |
| `_prev_signals_min.json` | {key: {confidence, bank_theme}} | Snapshot of last run, for the Movements panel (adds/drops/confidence changes). |
| `timeseries.json` | list | Long-format rows from the workbook Metrics sheet (country, scope, metric, unit, period, value, source, url...). |
| `series.json` | {country: {atms|branches|pos|cash: [{year,value,provisional?}]}} | Clean annual sector series for the per-country trend charts (Countries tab "Structural trends" grid). Built from the workbook **plus** `structural_series.json` (ECB), so all 10 EU markets chart, not just Greece. Hand-curated workbook series win where present (Greece ATMs/branches = HBA, 2014→). |
| `structural_series.json` | {generated, source, meta, series:{ISO2:{atms|pos|branches|cash:[{year,value,provisional}]}}} | ECB Data Portal multi-year series for the 10 EU footprint countries, pulled by `fetch_ecb.py` (best-effort first step of `run_weekly`; ATMs/POS/cash reduced half-yearly→annual). `ingest.py` merges it into `series.json` + `timeseries.json`. Re-run `fetch_ecb.py` to refresh; cached between runs so a network hiccup never blanks the charts. |
| `competitor_series.json` | {generated, source, meta, series:{`<Competitor>`:{revenue\|atm_segment\|atm_fleet:[{year,value}], atm_segment_label, **segments:{`<segName>`:[{year,value}]}**, segments_verified}}} | Multi-year competitor financials for the **Competition-tab charts**. `fetch_competitors.py` pulls **total revenue**; `fetch_competitor_segments.py` pulls **ALL reportable operating segments** (Atleos SSB+Network, Diebold Banking+Retail, Euronet EFT+epay+Money Transfer → `segments`, with the ATM one also as `atm_segment`) + **Euronet operated-ATM count** — both best-effort first steps of `run_weekly`, **sum-verified** (segments must add to the EDGAR total, or a dominant-segment ratio check for intersegment cos; `segments_verified` records which). US-listed only (Atleos/Diebold/Euronet/Brink's); the Vendors agent appends non-US names (Worldline, Nexi, Glory, Loomis) by hand in the same shape from annual reports. `build_dashboard` passes it straight through into the DASH payload as `competitor_series`. Revenue/segment in USD millions → chart renders as $B (`segments` drives the **"Business segments"** stacked bar); `atm_fleet` in ATM units. |
| `events.json` | list | Workbook Milestones (dated bank/market events). |
| `patterns.json` | list | Workbook Patterns (structural mechanics to read signals against). |
| `country_stats.json` | list | Latest per-country ATM/branch/cash/instant snapshot, parsed from the newest `findings/04-statistics` file. |
| `summary.json` | object | Run metadata (week, counts, source files). |
| `forecast.json` | {generated_week, horizon, accuracy, forecasts[], coverage[]} | `forecast.py` **statistical baseline** (secondary on the dashboard). Each forecast: country, metric, history (each point has a `provisional` flag → ◇ on the chart), projection, slope, cagr_pct, fit_quality (R²), inflection, method. `coverage[]` lists every series + whether it's projectable (≥3 pts) — drives the data-coverage panel. Deterministic; never the headline forecast. |
| `forecast_narrative.json` | {week, outlooks[]} | The **reasoned, judgment-led outlooks** the dashboard leads with — written by the Orchestrator (seeded by the `reasoned-market-outlooks` workflow). Each outlook: country, scope, horizon, direction, projected (range/qualitative), confidence, drivers[], rationale. This is analyst judgment weighing regulation/competitors/macro/leading-indicators — explicitly adjusting the math baseline, not curve-fitting. |
| `futures_narrative.json` | {week, generated_by, board_view{}, futures[]} | The **3–5yr structural outlooks** authored by **Agent 8 (Futurist)** from deep PUBLIC research (all countries). `futures[]` — one per structural trend: oid, scope, country/region, horizon, direction, projected, confidence, drivers[], rationale, cite_files[], **`source_reports[{label,url,page}]`** (PUBLIC, clickable, page-anchored) and optional **`chart{title,type,labels,series}`** (a numeric series → a plot). `build_dashboard` evidence-grounds each and emits top-level **`futures`**. Also carries **`board_view`** — the OBJECTIVE summary: verdict · products rising/fading · money/revenue pools · competition · threats · timeline · scenarios · markets-stance (shown LAST, labelled an analyst read) · confidence · basis. **No agent-chosen "bets" or "decisions" — it's a reporting tool; the CEO decides.** Emitted as **`futures_board`**. The dashboard shows the trends first (collapsible), then the objective board data, stance last. Authored monthly by the Futurist, not the Orchestrator. |
| `predictions.json` | list | Hit/miss ledger. Each numeric projection is logged once (target_year, projected_value, made_on_week) and auto-RESOLVED when the workbook later carries the actual, recording abs_pct_error. Builds an honest forecast-accuracy (MAPE) track record. |
| `verification.json` | {summary, files{path:{total,reachable,checked_at,sources[]}}, urls{}} | `verify.py` (trust pass) re-fetches every cited external URL, records reachability, and snapshots reachable ones. `build_dashboard` joins this to each signal's evidence files → a per-signal `provenance` {sources, reachable, files, status (strong/thin/broken/unaudited), checked, **`cites`** (the `findings/…` files the signal draws on)} surfaced as a card badge, and emits a single top-level `evidence_files` map in the DASH payload (`{findings-path: {label, total, reachable, checked, sources:[{url,status,code,snapshot}]}}`). The dashboard joins `provenance.cites` → `evidence_files` to render the per-card **evidence trail**: every cited URL, clickable, with a ✓ reachable / ⚠ unreachable marker. Deterministic *reachability* only — figure-level confirmation is the orchestrator's Chrome re-check. |
| `snapshots/<sha1>.txt` | text files | Point-in-time captures of each reachable source (URL + retrieval date + page text). Link-rot defense: a claim can be traced even if the live page later changes/dies. |

## Two ranking lenses

**1. Strength (evidence weight, not money)** — `strength = confidence_weight + 0.4*min(agents,3) +
likelihood_adj`, where confidence_weight = High 3 / Medium-High 2.5 / Medium 2 / Low 1, and likelihood_adj
= +0.6 if the likelihood text contains "high", 0 if "medium", -0.2 otherwise. Ranks by *how well-evidenced*
a signal is.

**2. Expected value (decision weight)** — `ev_score = size_weight × win_weight × confidence_weight`, where
size_weight = XL 4 / L 3 / M 2 / S 1 / Unscoped 0, and win_weight = High 3 / Medium 2 / Low 1. Ranks by
*how valuable* an opportunity is, risk-adjusted. **Unscoped rows (threats, macro drivers) score 0 and drop
out of the value ranking**, so a diffuse signal can't outrank a concrete biddable deal. `size_band` and
`win_prob` are judged per signal by the agents/orchestrator (see the playbook rubric); the engine never
invents them. The dashboard exposes both lenses (a "By value / By evidence" toggle); the brief leads with
expected value. Country `ev_score` = sum of in-country signal EVs (`top_ops_ev`, `account_targets_ev` are
the EV-ranked key lists in the DASH payload). Neither score is a budget or market size.

## Re-classification
Country resolution and product tagging happen in `ingest.py` from `references/footprint.json` and
`references/product_map.json`. To change how a signal is bucketed, edit those reference files and re-run —
do not hand-edit `signals.json` (it is regenerated each run).
