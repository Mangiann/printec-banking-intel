# Chief Financial Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own the revenue forecast, the budget, and the board's revenue bridge. I sign off on the spend that runs this
intelligence operation (eight research agents plus a verification pass), and I have to defend that spend against the
decisions it actually changed. From a market-intelligence tool I need three things: (1) a **sizing methodology I can
audit** — where every euro comes from; (2) **expected value**, not gross headline numbers, so I can weight a pipeline
the way I weight my own funnel; and (3) a **link to reality** — either Printec's own bookings/win-loss, or a proven
forecast track record — so the confidence labels are bankable rather than asserted. I will judge this tool by whether I
can build a single line of a budget or a board slide from it.

## Verdict (TL;DR)

This is a genuinely strong **outside-in market-radar** — well-sourced, honestly hedged, and disciplined about evidence.
But as a **financial instrument it is not yet usable**, and the one number most likely to reach a board slide — the
**€99.3m "pipeline"** — is the weakest thing in the product. I traced it to source: `pot_value` is a flat constant
keyed only to a size band (every XL deal = €7.5m, L = €3.0m, M = €0.6m), and €99.3m is the **gross sum** of those
constants across "opportunity" signals. It is **not** expected value, not win-probability-weighted, not anchored to
any specific tender figure, and — critically — the per-deal number contradicts the band definition shown to the reader
(XL is labelled "≥€5m" but hard-coded to exactly 7.5). With **0 of 174 forecasts resolved (MAPE null)** and **no link
to Printec's CRM, bookings, margin or win/loss**, I cannot build a budget, a revenue bridge, or an ROI case for the
operation from this today. Fixable — but today it is a research library, not a planning input.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 6 | Evidence discipline and sourcing are strong; the *quantitative* layer (pot_value, ev_score) is ordinal dressed as financial. |
| Completeness | 4 | No expected-value rollup, no TAM/SAM/SOM, no link to Printec's own pipeline/margin/win-loss — the half I need to plan is absent. |
| Clarity | 6 | The "not additive / click the bar" framing is honest, but €99.3m reads as a pipeline figure to anyone who skims, and the band-vs-point inconsistency is hidden. |
| Insightfulness | 6 | The competitive and structural reads are revealing; the financials restate band counts, they don't reveal value. |
| Short-term growth | 5 | Useful for *prioritising* which 8 accounts to chase; useless for *quantifying* what they're worth or forecasting bookings. |
| Long-term growth | 6 | The Futures money-pools + CAGRs give a credible strategic frame; unanchored to Printec's share, so not yet a planning model. |
| **Overall** | **5.3** | A trustworthy market radar wearing a finance costume it hasn't earned. |

## What is genuinely good

- **The sizing logic is honest *once you read the code*.** `ingest.py:452` assigns `pot_value` from band only and the
  comment explicitly says it is "NOT win-probability-adjusted." The team is not pretending this is expected value at the
  data layer. The dashboard copy (app.js line 650/670) also tells the reader bars are "**not additive**" and that a deal
  shows under several markets/products. That is more intellectual honesty than most internal "pipeline" decks I see.
- **Dual ranking exists.** There is both an objective €m view (`pot_value`) and a risk-adjusted `ev_score`
  (`SIZE_W × WIN_W × CONF_WEIGHT`, ingest.py:125–131). The *intent* — separate "how big" from "how likely" — is exactly
  right and is the seed of a real EV rollup.
- **Evidence trail and provenance.** 1,253 sources checked, point-in-time snapshots, ⚠ flags on unreachable links, and
  `cite_ungrounded` self-flagging in the Outlook tab. For an auditor's seat, a tool that volunteers what its sources do
  *not* support is rare and valuable.
- **The headline competitive intel checks out.** I verified the Brink's/NCR Atleos item: $6.6bn, ~$30 cash + 0.1574
  Brink's shares (~$50.40/share implied), close targeted Q1 2027 — all confirmed against the SEC filing and Brink's IR.
  That is the single most strategically material fact for an ATM-led integrator, and the dashboard got it right and
  framed its "so-what" (Printec's key hardware partner becoming a CIT conglomerate) correctly.
- **Forecast honesty.** `forecast_accuracy: {total:174, resolved:0, mape:null}` is shown rather than buried. The tool
  admits its forecasts are unproven. I respect that far more than a fabricated accuracy number.

## What is missing or weak

- **€99.3m is a gross band-count, not a pipeline.** It is `Σ pot_value` over `is_opportunity` signals
  (build_dashboard.py:382), where each value is a band constant. So 11 XL signals contribute €82.5m of the €99.3m
  *regardless of which banks they are*. PrivatBank's 800-unit fleet and "Regulatory compliance wave — DORA/AML"
  both carry exactly €7.5m. That is not a number I can put in front of a board as "addressable pipeline."
- **No expected value rollup.** I have `pot_value` (€) and `win_prob` (High/Med/Low) on every signal but the dashboard
  **never multiplies them**. An EV pipeline = Σ(pot_value × P(win)) is one line of code and would convert €99.3m gross
  into a defensible risk-adjusted figure. `ev_score` is *not* this — it is a dimensionless 0–36 ordinal product, not euros.
- **The band-to-euro point estimate contradicts its own definition.** Reader sees "XL ≥€5m" (app.js:650); engine codes
  XL = exactly €7.5m. An open-ended band collapsed to a single midpoint with no documented basis means the €99.3m has a
  fabricated precision. Where did 7.5 come from? It is not anchored to any tender value in the data.
- **No TAM / SAM / SOM.** The Futures tab has 10 market pools with CAGRs (good), but there is no line from "AML/RegTech
  pool grows at X%" to "Printec's serviceable share in our 17 countries is €Y." I cannot size the prize.
- **No link to Printec's actuals.** Zero ingestion of bookings, revenue, margin, delivery backlog, or win/loss history.
  I cannot calibrate `win_prob` against our real hit rate, I cannot build a revenue bridge, and I cannot tell whether
  these 8 "top ops" are already in our funnel or genuinely net-new.
- **ROI of the operation is unmeasured.** Eight agents + verification run weekly. There is no closed loop — no field
  tracking whether a flagged opportunity was pursued and won. I cannot compute the cost-per-decision-changed, which is
  the only metric that justifies the run cost to me.

## What I cannot decide from this today

1. **My number for the board.** I cannot state a risk-adjusted addressable pipeline. €99.3m is not it (gross, band-flat);
   there is no EV figure to replace it.
2. **Budget allocation by product line.** "Opportunity value by product" is band-count, non-additive, and double-counts
   across deals — I cannot allocate sales/pre-sales headcount or capex against it.
3. **Whether to trust any "High confidence" outlook.** With MAPE null and 0/174 resolved, "High" is an assertion. I
   cannot weight a forecast I cannot back-test.
4. **Whether the intelligence op pays for itself.** No decision-changed ledger, no link to won revenue → no ROI.
5. **The Brink's/Atleos *financial* exposure to Printec.** The qualitative read is right, but I cannot see our euro
   revenue-at-risk from a partner becoming a competitor — because our own partner-channel revenue isn't in the tool.

## Domain reality-check

- **Brink's/NCR Atleos:** verified accurate ($6.6bn, Q1 2027 target close, ~$50.40/share implied, ~78/22 post-close
  ownership) against the [SEC 8-K exhibit](https://www.sec.gov/Archives/edgar/data/78890/000110465926020500/tm267399d1_ex99-1.htm)
  and [Brink's IR](https://investors.brinks.com/news-releases/news-release-details/brinks-acquire-ncr-atleos-66-billion-creating-leading-financial).
  The dashboard's framing is sound; my only finance note is that it stops at the narrative and never quantifies Printec's
  partner-revenue exposure.
- **Sizing convention:** the band cut-offs (XL ≥€5m, L €1–5m, M €0.2–1m) are a reasonable convention, but collapsing an
  open-ended top band to a single €7.5m point with no documented basis is exactly the kind of unsupported precision an
  auditor flags. Standard practice would be a documented midpoint *with a range* (e.g. XL = €5–15m, model at €7.5m) and
  a sensitivity band on the rollup.
- **Expected value is industry-standard funnel math.** Any CRM (Salesforce, Dynamics) reports weighted pipeline =
  value × stage-probability. The tool already holds both inputs and simply doesn't do the multiply — a conspicuous gap
  for a tool that leads with a euro headline.

## My recommendations

**Now (low effort, high impact)**
- **Ship an EV rollup.** Add `ev_value = pot_value × P(win)` (map High/Med/Low → 0.6/0.35/0.15, documented) and surface
  **two numbers**: gross €99.3m and risk-adjusted €~XXm. *Unlocks:* a board-defensible pipeline figure. ~1 day.
- **Fix the band/point contradiction.** Either show ranges (XL €5–15m) or rename the headline to "indicative band-weighted
  scale, not a pipeline forecast." *Unlocks:* removes the single biggest credibility risk on the Overview tab. Hours.
- **Add a methodology footnote** on Overview stating pot_value is a band constant, non-additive, gross. *Unlocks:* lets a
  skim-reader not misread €99.3m as committed pipeline. Hours.

**Next (medium effort, high impact)**
- **Anchor XL/L to real tender capex where known.** PrivatBank 800-unit and CEC full-stack have public/derivable budget
  ranges; use them instead of a flat 7.5. *Unlocks:* per-deal numbers I can actually defend. ~1 week.
- **Begin resolving forecasts.** Even 10–20 resolved points with a first MAPE turns "High confidence" from assertion to
  evidence. *Unlocks:* bankable confidence labels. Ongoing, low marginal cost.

**Later (higher effort, strategic)**
- **Link to Printec's CRM/bookings (one-way, read-only).** Tag each top-op as in-funnel / net-new, and back-test
  `win_prob` against our real hit rate. *Unlocks:* a true revenue bridge and calibrated probabilities.
- **Add a decisions-changed ledger** (signal → pursued? → won? → €). *Unlocks:* the ROI case that justifies the agent
  run-cost to me — without it I cannot defend the spend at budget time.
- **Add a SAM line on each Futures money-pool** (pool × Printec serviceable share in-footprint). *Unlocks:* sizing the
  long-term prize, not just naming the CAGR.
