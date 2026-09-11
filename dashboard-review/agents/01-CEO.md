# Chief Executive Officer — review of the Printec Banking Intelligence Dashboard

*Reviewer: Markos Stavridis, Group CEO (capital allocation across 17 markets & 12 product lines; the growth narrative to the board and owners)*

## Who I am & what I need this dashboard to do for me

I sit on roughly €X of annual capex and bid-resourcing decisions spread across 17 markets and 12 product lines. My job is not to know everything that moved in the market this week — it is to decide **where to push, what to defend, and what to harvest or exit**, and to defend that allocation to the board and owners with a coherent story. My test is narrow and brutal: *can I size a bet from this?* I need three things the dashboard largely does not yet give me as a single object — (1) a top-of-funnel "what changed this week, so what, now what" that survives a 90-second read; (2) an expected-value view that discounts raw pipeline by win-probability and ties to our actual capacity and margin; and (3) an explicit reconciliation of the tension between where this week's signal concentrates (cash/ATM) and where the long-term money is said to be (identity, real-time data, governed AI).

## Verdict (TL;DR)

This is the best outside-in market-intelligence asset I have seen inside this company — genuinely rigorous, well-sourced (I independently verified the Brink's/NCR Atleos $6.6bn deal and the AI-in-banking 31.8% CAGR; both are accurate), and honest about its own limits. But it is an **analyst's library, not a CEO's cockpit.** It tells me what is happening in extraordinary detail and even tells me where the puck is going in 2030 — yet it will not, today, let me *size a bet*: the pipeline total is an undiscounted raw sum, `win_prob` is a text label not a number, and there is no expected-value rollup, no link to our own bookings/capacity/margin, and no single synthesis view above the eight tabs that resolves the cash-vs-future tension into an allocation. It informs my narrative superbly and my capital decisions only partially.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 8 | Source discipline is real — triangulation across agents, archived snapshots, `cite_ungrounded` self-flagging; headline facts verified true. |
| Completeness | 5 | Strong on outside-in market signal; absent on the inside-out half I allocate against — our pipeline, capacity, margin, win/loss. |
| Clarity | 5 | Each tab is clear; the *whole* is not — 8 dense tabs, no apex synthesis, cognitive load is high for a time-poor reader. |
| Insightfulness | 8 | The futures `bottom_line` thesis and the "operate the regulated rails as managed services" reframe are genuinely decision-changing. |
| Short-term growth | 6 | Names the live deals (PrivatBank 800-unit, Piraeus CashFlex) but cannot rank them by expected value or against our capacity. |
| Long-term growth | 7 | The 2-5yr money-pool map with CAGRs is a credible strategy input; it just isn't yet wired to a Printec capability/where-to-build gap. |
| **Overall** | **6.3** | Decision-*informing*, not yet decision-*grade*, for capital allocation. |

## What is genuinely good

- **Futures `bottom_line.thesis` (Future outlook tab).** The one-line thesis — *"the durable money is not in any single mandate but in operating the shared, regulated rails… as managed services across many markets and a buyer base far wider than banks"* — is the single most useful sentence in the product. It reframes our identity from "ATM integrator" to "operator of regulated rails," which is exactly the narrative I need to take to owners. The supporting `drivers` (the 2027 regulatory wall with the honest hedge that "dates slip," EUDI possibly drifting to ~2032) show judgment, not hype.
- **The money-pool map (`futures_board.money`, 11 pools with CAGRs and sources).** AI in banking ~31.8%, fraud/financial-crime ~15.5% ("fastest near-term ROI"), identity ~15-17%, instant payments ~10x volume to 2028 — each with a live source link. This is a credible TAM-direction skeleton for long-range allocation. I verified the AI figure against Grand View Research; it is accurate (note: the field-wide range is $64-144bn across firms — the dashboard cites the high end without flagging the dispersion).
- **The `competition_brief` (Competition tab).** Plain-English, lands the *so-what*: Brink's absorbing our key ATM partner Atleos creates an end-to-end CIT+hardware+managed-services rival, and Brink's Hellas already runs CIT plus ATM managed services in Greece. That is a defend-the-base alarm I can act on. Independently verified — the $6.6bn, ~78/22 ownership split, +$2.6bn debt, Q1 2027 close are all correct.
- **Evidence discipline.** `cite_ungrounded` on the outlook cards (e.g. the PrivatBank card honestly flags that the "three war years" framing is baseline trend, not in the cited A4 doc) is rare intellectual honesty for an internal tool. Triangulation (PrivatBank 800-unit confirmed by A1+A2+A5) is exactly how I want a claim de-risked before it reaches me.

## What is missing or weak

- **No bet-sizing layer.** The pipeline "total" is a raw sum of `pot_value` (24 signals summing to ~€114m in the data; ~€99.3m biddable per the briefing) **undiscounted by win probability.** Worse, `win_prob` is stored as a text label ("High"), so an expected-value (value × p(win)) rollup is literally not computable from this data. I cannot rank the PrivatBank 800-unit lot against the Piraeus CashFlex 850-ATM fleet on a risk-adjusted basis — which is the actual decision. This is the single biggest gap.
- **No inside-out data.** The dashboard is entirely market-facing. It does not know our bookings, delivery backlog, engineer capacity, product-line margin, or win/loss history. I cannot allocate capital purely on market attractiveness — I allocate where attractiveness *meets our right-to-win and free capacity*. Today I'd have to mentally overlay that, every week.
- **No apex synthesis view.** There is no "this week in one screen" above the tabs. `movements` (19 added, 14 removed, **0 confidence_changed**) is plumbing, not narrative. The Overview tab is a good lead but still a tab among eight. A time-poor CEO needs a half-page: *what changed, what it means, the one or two allocation implications.*
- **The cash-vs-future tension is stated but never resolved into an allocation.** Products tab: ATM/cash scores 85.8 (25 of 29 signals touch it); the lines the Futurist itself calls the growth spine score lowest (identity 22.5, instant 27.6, HSM 16.5, card issuing 7.5). The dashboard presents both truths and leaves *me* to reconcile them. It should explicitly say: harvest the cash annuity for cash-flow, fund the build in identity/fraud/rails — with a number against each.
- **Forecasting track record is unproven** (`forecast_accuracy`: 174 total, **0 resolved, MAPE null**). Every "High" confidence is asserted, not back-tested. Fine for now, but I cannot yet trust the projected-value ranges as planning inputs.

## What I cannot decide from this today

1. **Where to put the next euro of bid-resourcing.** No risk-adjusted (EV) ranking of opportunities, no overlay of our capacity — so I cannot prioritize PrivatBank vs Piraeus vs Alpha branch transformation on the dimension that matters.
2. **How much to invest in building the future-spine capabilities** (identity, real-time fraud orchestration, AML/RegTech, HSM/PQC). The money-pools tell me the market is large and growing; nothing tells me Printec's current right-to-win, the build cost, or the capability gap to close.
3. **What to defend vs harvest in cash/ATM** in light of the Brink's-Atleos consolidation. The threat is named; the *response posture per market* (where Brink's Hellas already competes vs where we still hold the rail) is not laid out as a defend/harvest map.
4. **The board narrative's hard numbers.** I can tell the story (rails-as-managed-services); I cannot yet attach a 3-year revenue/margin shape to it from this tool.

## Domain reality-check

I pressure-tested the two load-bearing claims. **Brink's/NCR Atleos:** verified accurate — $6.6bn cash-and-stock, announced 26 Feb 2026, ~78/22 post-close ownership, +~$2.6bn assumed debt, Q1 2027 target close, UK competition review the open item ([SEC filing](https://www.sec.gov/Archives/edgar/data/78890/000110465926020500/tm267399d1_ex99-1.htm), [Brink's IR](https://investors.brinks.com/news-releases/news-release-details/brinks-acquire-ncr-atleos-66-billion-creating-leading-financial)). The strategic read — that this converts our hardware partner into an end-to-end rival — is the correct executive interpretation, not a restatement. **AI-in-banking pool:** the cited ~$26bn(2024)→$144bn(2030) at 31.8% CAGR matches [Grand View Research](https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-banking-market-report). My one caution: across firms the 2030 figure ranges $64-144bn and CAGR 18-35% ([Allied/openPR](https://www.openpr.com/news/4397872/ai-in-banking-market-set-to-reach-64-03-billion-by-2030-growing), [Knowledge Sourcing](https://www.knowledge-sourcing.com/report/artificial-intelligence-ai-in-banking-market)); the dashboard cites the most bullish source without flagging dispersion, which slightly inflates the apparent prize. Directionally, the thesis is sound and matches my own read of the CEE market: cash plateaus rather than dies, and the compliance-driven 2027 wall (instant payments, VoP, EUDI, AMLR) is real and is the genuine spend driver. The dashboard gets the *shape* of the next five years right.

## My recommendations

**NOW (low effort, high impact).**
- **Build a one-screen "CEO brief" above the tabs:** what changed (top 3 moves), so what (the allocation implication), now what (the 1-2 actions). Reuse existing fields; no new data. *Effort: low. Impact: high. Unlocks: the 90-second weekly read that makes this decision-grade instead of reference.*
- **Convert `win_prob` to a number and publish an expected-value column** (pot_value × p(win)) and an EV-ranked top-ops list. *Effort: low. Impact: high. Unlocks: risk-adjusted bid prioritization — the core capital decision.*

**NEXT (medium effort, high impact).**
- **Add an explicit defend/harvest/build allocation panel** that resolves the cash-vs-future tension: cash/ATM = harvest-for-cashflow with a € number; identity/fraud/rails = fund-the-build with a target share. *Effort: medium. Impact: high. Unlocks: the capital-allocation thesis I present to owners.*
- **Overlay Printec right-to-win and capacity** on each opportunity and each future money-pool (even a coarse 1-3 score). *Effort: medium. Impact: high. Unlocks: allocating where market attractiveness meets our ability to win and deliver.*

**LATER (higher effort, structural).**
- **Ingest our own bookings/backlog/margin/win-loss** so attractiveness can be tested against P&L reality, and **start resolving forecasts** so confidence labels earn trust (close the MAPE-null gap). *Effort: high. Impact: high. Unlocks: a true integrated strategy cockpit and a credible track record — the difference between an intelligence tool and a steering instrument.*
