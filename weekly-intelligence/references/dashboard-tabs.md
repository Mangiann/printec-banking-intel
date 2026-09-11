# Dashboard tabs (what each view answers)

1. **Overview** — KPIs (active signals, new this week, high-confidence, deadlines <=60 days, active
   markets), then the headline cut of each section: **"Potential opportunity value by market"** and
   **"Potential opportunity value by product"** (bars of indicative €m, summed from the deal-size bands of
   this week's current, biddable opportunities), a plain-English **"Competition & partners — this week"**
   summary (the most important competitor/partner moves — the Orchestrator's `competition_brief`, or an
   auto-synthesised fallback from the watchlist), and **"Top opportunities"** (toggle: most recent / largest
   €). Standing facts and already-held (SECURED → HELD) positions are kept out of the value charts and Top
   opportunities, shown only as tagged context. Click any signal card to expand evidence + recommended action.
   An opportunity with **no published deal value** is NOT hidden: it is counted everywhere, badged **"value
   unscoped"**, contributes €0 to the value bars (nothing is ever invented), and markets whose contests are
   all unscoped get their own clickable chip strip under the chart — so the euro headline is stated as a
   **floor, not a ceiling**. The tab closes with **"Indirect opportunities — composed from several signals"**
   (`DASH.derived`, fed by `intel-cache/derived_opportunities.json`): plays no single signal states, built
   from the intersection of 2+ signals across 2+ independent agents — typically rows the rankings exclude
   (macro drivers, lost scopes, installed-base positions). Each is badged **DERIVED** and shows who buys /
   what forces it (dated) / the play / why no single signal shows it / **what would kill it**, and opens its
   component signal cards in one click. `build_dashboard.py` enforces the 2-signal / 2-agent rule and caps
   their confidence at Medium-High; they never carry a euro value. They repeat inside each market's
   drill-down on Countries and at the foot of **All signals**.
2. **Countries** — total addressable deal value (€m) per market (bar, green = has new signals; click a bar
   for that market's opportunities), then a **core structural-trends chart**: **ECB/HBA actuals only** —
   device & branch counts (ATMs, POS terminals, bank branches, cash withdrawals) — with a metric dropdown
   and multi-market select. (The deep ATM-market detail lives on Products.) Then a sortable market table with
   the latest ATM/branch/instant-payment figures, and a "Footprint-wide themes" panel.
3. **Products** — **"Product opportunity value by market"** (indicative €m per Printec solution, per-market
   filter, click-to-reveal), a **"Demand under deadline"** bar, then the **dedicated ATM-market section** (fed
   by `DASH.atm_market`, the deep-read RBR dataset for all 17 footprint markets incl. Greece/Cyprus): (a)
   **installed base, usage & forecast to 2028** — multi-market line, metric dropdown (installed base, cash
   withdrawals number/value, per-ATM usage, shipments), recorded solid + ◇ dashed RBR forecast; (b)
   **cross-country benchmark (2022)** — ranked bar with a measure dropdown (ATMs per million / per 100
   branches / per GDP, recycler %, deposit-automation %, base, branches); (c) **channel mix** — stacked bar
   (off-site vs through-the-wall/lobby/hall/branch-based); (d) **installed base by manufacturer** — stacked
   bar (NCR/Atleos vs Diebold Nixdorf, GRG, KEBA, Hyosung, other). Then per-solution opportunity cards.
4. **Competition** — competitor financials & ATM operations (SEC EDGAR; metric toggle incl. **Business
   segments**, a stacked bar of each rival's full revenue mix by reported operating segment, + company
   toggles), a **"Competition by product line"** bar (rivals per Printec line, stacked by threat), a
   **"Competitor landscape"** section filterable by **market AND product** (a bar of rivals ranked by **how
   many of this week's signals name them** — click a bar to read exactly those signals — plus the full-field
   profile cards with threat/role/latest move, each with an **expander to read the linked signal cards**),
   the NCR Atleos/Brink's partner-channel watch, and a country x competitor pressure matrix.
5. **Accounts & deadlines** — a regulatory/event timeline with countdowns (the buying window), plus a
   filterable account-target list (by market, product, confidence, new-only) with why-now + recommended action.
5b. **All signals** — the unfiltered record: **every** signal in the week's table, not just the biddable ones.
   Every other tab is a *cut* of this set (opportunities, accounts, per-country, per-product); this is the set
   itself, including the macro/threat rows that carry the market trend but are deliberately kept out of every
   ranking. Filter by market (incl. footprint-wide), product, **lane** (opportunity · installed base · lost ·
   market context), confidence and new-only; sort by recency, deal size, corroboration or market; free-text
   search across the signal, implication, follow-up and source. Use it to read the market rather than the
   pipeline. The **indirect opportunities** (below) are repeated at the foot of this tab.
6. **Outlook (6–12 mth)** — "Where the market is heading." LEADS with a **product-direction layer**: one
   reasoned 6–12 month call per Printec product line (`product_outlooks`) — collapsed shows a 4–5 line
   plain-prose **summary**; expand for the full **Outlook / Why-now / Key drivers / Sources**. Ordered by
   opportunity value and covering EVERY line (not ATM-skewed). Below it, the **per-market deal pipeline**
   ("Biggest near-term opportunities by market", `outlooks`). Underneath, small, the deterministic linear
   baselines (`forecast.py`: history-vs-projection chart, per-metric table, MAPE accuracy badge) as the
   reference the reasoned calls argue against. Authored by the Orchestrator (`forecast_narrative.json`);
   everything labelled "projection", never a sourced fact.
7. **Patterns & history** — the structural patterns and the 2024->2026 milestone timeline that this week's
   signals attach to (how new data connects to history).
8. **Future outlook** — Agent 8 (the Futurist)'s 2–5yr view from deep PUBLIC research (consulting houses,
   regulators, multilaterals), **all countries**, written as a consultant and **de-biased away from ATMs/cash**
   (cash is the legacy base, never the lead). Top to bottom: **(a) The bottom line** — the executive synthesis
   (`board_view.bottom_line`): a cyan hero with a headline pill + an `h2` title + the thesis as a muted subtitle +
   a 3-paragraph "2030 picture"; then **The heavy drivers** (4 pastel KPI-style cards, 2×2), **Hidden gems**
   (single-column cards, each with a "new buyer / new line" tag — the non-obvious opportunities), and **Where we
   land by 2030** (a before→after strip across domains). **(b) Structural trends** (`futures[]`) — ~10–12
   collapsible deep-dive cards covering the full domain set (identity, payments+data, fincrime/fraud AI, governed
   AI, resilience, PQC/HSM, tokenization, embedded/open finance, core/cloud, SoftPOS), cash as ONE legacy card
   LAST; each has direction, projection, drivers, clickable source citations and a chart where the sources give a
   numeric series. **(c) The underlying data** — the lean cited EVIDENCE layer (`board_view.money` revenue pools ·
   `competition` the new arena · `threats` risks · `timeline` the regulatory calendar), terse one-figure-plus-
   citation lines, NOT a re-telling of the top. (The old "demand by product" sub-section and the "analyst's view"
   scenarios/market-stance were **removed**.) Source citations are **clickable — they open the report at the cited
   page**; never internal `.md` paths. An objective reporting tool: no agent-chosen "top bets". The 2027–2031
   structural arc — projections, never sourced facts. Fed by `intel-cache/futures_narrative.json`
   (`board_view.bottom_line` + the evidence arrays + `futures`).

A **period picker** (top-right) lets you view the latest week (default), time-travel to any past week
(its exact archived snapshot), or open a **monthly rollup** — the month-end state plus a start→end delta
("X new this month", the full month movement), built for the monthly strategy review. History accrues
automatically from each weekly publish.

The dashboard is a **live web app** on Vercel (`dashboard-web/`), rendering the `dashboard-data.json`
payload and auto-updated each weekly run (viewable anywhere, no redeploy). It pulls Chart.js from a
CDN, so charts need an internet connection to render.
