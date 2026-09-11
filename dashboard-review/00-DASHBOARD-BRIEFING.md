# Briefing — Printec Banking Intelligence Dashboard (for the C-level review panel)

**Purpose of this document:** give each reviewer an accurate, common base of fact about what the
dashboard *is*, what it *contains*, how it is *built*, and how it is *organised*, so the critique is
grounded in the artefact rather than in assumptions. Reviewers may also open the source files (paths
below) to verify any claim. Be critical and objective; do not assume the product is good because it
is detailed.

---

## 1. What it is

A **weekly banking-technology market-intelligence dashboard** for **Printec Group** covering its
**~17-country footprint** (Greece, Cyprus, Romania, Bulgaria, Hungary, Czechia, Slovakia, Slovenia,
Austria, Croatia, Serbia, Ukraine, plus Western Balkans: Albania, North Macedonia, Bosnia,
Montenegro, Kosovo).

- **What Printec is:** a systems integrator / managed-services provider in banking technology —
  ATMs & cash automation (NCR Atleos hardware, recyclers, APTRA OptiCash), self-service & branch
  transformation, POS/acquiring & terminal management, payments modernization, fraud/AML,
  compliance & operational resilience, payment security/HSM, card issuing, digital onboarding, core
  & digital channels, and managed services across all of these.
- **The tool:** a static web app (`index.html` + `app.js` ~170 KB + `styles.css`) that renders a
  ~1 MB `data.json` produced by a pipeline of 8 autonomous research "agents" (bank disclosures,
  tenders/procurement, regulation, market statistics, jobs/hiring, vendors/competitors, an
  orchestrator, and a futurist) plus a trust/verification pass. Published weekly to Vercel Blob; the
  page reads `/api/data`. Login-gated UI; the underlying evidence is public.
- **Current snapshot under review:** week **2026-06-25**, generated 2026-06-25.

## 2. Headline numbers (this week)

- **29 signals** (17 new this week, 28 high-confidence, 10 with imminent deadlines), 16/17 countries active.
- **Pipeline framing:** ~**€99.3m** total potential value across the biddable opportunities; size
  bands distribution — XL 11, L 10, M 3, Unscoped 5.
- **Provenance:** **1,253 sources checked** → 1,059 reachable, 157 HTTP errors, 37 unreachable
  (~15% with link issues). Each signal/outlook carries an evidence trail (✓/⚠), an archived
  point-in-time snapshot per reachable source, and links to the agent source documents.
- **156 competitors/partners** tracked; **382 ATM-market data rows**; **23 regulatory deadlines**;
  **87 forecast points** (note: forecast_accuracy = 174 total, **0 resolved, MAPE null** — i.e. the
  forecasting track record is not yet measurable).
- **26 account targets**, **8 top operational opportunities**, **31 patterns**, **13 milestone events**,
  **15 reasoned 6–12 month outlooks**, **11 multi-year (2–5yr) futures projections**.

## 3. The eight tabs (information architecture)

1. **Overview — "This week in the footprint."** KPIs, the signals that moved (NEW/UPDATED/STANDING/HELD),
   the highest-strength opportunities, "opportunity value by product" bar chart (non-additive; click a
   bar → deals behind it), and a newspaper-style "Competition & partners — this week" lead.
2. **Countries — "Where to focus."** Opportunity by market with a per-country structural backdrop
   (ATM installed base + y/y, bank branches + y/y, cash trend, instant-payments scheme status), an
   `implication` line, and the signals per country. Market-detail charts (ATM density per million,
   per 100 branches, per GDP; recycler %; deposit-automation %) with a weighted **multi-source ATM
   chart** (ECB / RBR / World Bank-IMF / national central-bank sources).
3. **Products — "What banks are buying."** Demand intensity scored across **12 Printec solution lines**
   (this week: ATM/cash 85.8, self-service 60.3, POS/acquiring 52.5, compliance/resilience 49.2,
   fraud 38.1, managed services 38.1, core/digital 32.1, payments-instant 27.6, digital identity 22.5,
   payment-security/HSM 16.5, physical security 7.5, card issuing 7.5). Plus a per-product-line
   **6–12 month product-direction outlook** (`product-outlooks.js`) and opportunity value by product.
4. **Competition — "Who is winning the money."** A plain-English `competition_brief` (this week led by
   the **Brink's acquisition of NCR Atleos, ~$6.6bn**, both shareholder votes passed 30 June, close
   targeted Q1 2027 — i.e. Printec's key ATM partner becomes part of a CIT conglomerate that can sell
   hardware+logistics+managed-services end-to-end; plus Mellon/KAL/Brink's alliance, Euronet
   consolidation). A competitor watchlist, a per-market **pressure matrix** (competitor × country
   intensity 0–6), ATM market-share series, and competitor financial series.
5. **Accounts & timing — "Who to approach now."** Bank-specific account targets with a why-now, plus
   the **regulatory deadline tracker** (23 dated items: Brink's/Atleos vote, MiCA/TFR, Bulgaria euro
   changeover, Slovakia eKasa, EPC VoP rulebook, AMLA RTS, NLB/Addiko, Western-Balkans TIPS-clone,
   SWIFT CBPR+, EUDI wallet, Hungary Act XVIII, Albania POS mandate, Instant Payments receive/send
   obligations, AMLR, AMLA supervision, digital euro, European Accessibility Act 2030, etc.). Each
   deadline has the "forces" (why it drives bank spend), affected geographies, and products.
6. **Patterns — "How it connects to history."** 31 persistent market-mechanics patterns (e.g. "cash is
   plateauing not dying"; "three-tier ATM gradient along the EU-maturity axis"; the footprint runs
   ~one cycle behind Western Europe) each with evidence, "what it means for Printec," confidence, and
   sources; plus a milestone timeline of 13 dated events.
7. **Outlook 6–12 mth — "Where the market is heading."** 15 analyst-reasoned outlook cards
   (country/scope), each with: direction (strong growth / growth / stable / …), a **projected value**
   (explicitly a precedent-based range, not a confirmed number), confidence, drivers (each citation-linked),
   a full **rationale paragraph**, a "Built on" list of the master-table signals it reasons from, an
   **evidence trail** of agent source documents, and a **validation verdict** (e.g. "grounded / validated")
   plus an explicit **`cite_ungrounded`** field flagging any claim the cited sources do *not* fully support.
8. **Future outlook — "The next chapter" (2–5 yr).** The 2028–2031 structural arc from the Futurist
   agent. A "futures board" split into **money** (10 market pools with CAGRs + sources — AI in banking,
   fraud/financial-crime, digital identity, AML/RegTech, instant payments & ISO 20022 data products,
   core-banking & cloud modernization, payment security/HSM, tokenization/stablecoins, embedded
   finance, cash/recyclers/ATMaaS), **competition**, **threats**, **timeline**, and a structured
   **bottom_line** (thesis + 3-paragraph "picture" + drivers + 5 "gems"/non-obvious openings +
   a 2030 end-state strip of now→then per domain). Thesis in one line: *"Banking's centre of gravity
   moves to identity, real-time data and governed AI by 2030; cash/ATM is a defensible managed-services
   annuity — the legacy base to optimise, never the growth spine."*

## 4. Data model & methodology (how to judge rigour)

- **Signals** carry: status, bank_theme, country, footprint_wide flag, the signal text (with **(A1/A2/…)
  agent citations** and external source links), sources[], implies (the "so-what"), likelihood,
  confidence, follow_up (the next action), size_band (XL/L/M/Unscoped), win_prob, products[],
  primary_product, dates (dev_date, age_days, recency), strength score, ev_score, pot_value (€m),
  held/is_opportunity flags, and a **provenance** block (cited sources with HTTP status + snapshot,
  files, reachable count, status strong/…, checked date).
- **Triangulation:** the strongest signals are confirmed by **multiple independent agents** (e.g.
  PrivatBank 800-unit lot is confirmed by disclosures A1 + tenders A2 + jobs A5).
- **Outlooks** are explicitly analyst judgment but each is bound to its source signals + agent
  findings, validated, and self-flags ungrounded extrapolation (`cite_ungrounded`). Projected euro
  values are framed as **precedent-based ranges, not confirmed numbers**.
- **Evidence/snapshots:** every external link is re-fetched in a trust pass; reachable ones get an
  archived snapshot so a dead link still opens its capture; ⚠ marks unreachable.
- **History:** every weekly publish archives a dated snapshot; a period picker offers Latest / any past
  week / a monthly rollup with a start→end delta ("what moved this month").

## 5. Known characteristics worth probing (do not treat as exhaustive)

These are observations, not verdicts — reviewers should test, confirm, or refute them, and add their own:
- **ATM/cash centricity.** ATM & cash automation scores 85.8 with 25 of 29 signals touching it, while
  the lines the *Futurist tab itself* calls the growth spine (digital identity 22.5, payments-instant
  27.6, HSM/payment-security 16.5, card issuing 7.5) score lowest. There is an apparent tension between
  where this week's *signals* concentrate (cash/ATM, the legacy base) and where the *long-term thesis*
  says the money goes (identity, real-time data, governed AI). Is the weekly engine structurally biased
  toward the mature, well-instrumented part of the market?
- **Forecasting track record is unproven** (0 of 174 forecasts resolved; MAPE null). Confidence labels
  ("High") are asserted, not yet back-tested.
- **Sizing methodology.** Values are bands + a `pot_value` €m and a €99.3m pipeline total; the
  derivation of those euro figures (and of the 0–6 pressure-matrix scores, the strength/ev_score) is
  not surfaced to the reader. No explicit TAM/SAM/SOM, no expected-value (value × win-prob) rollup, no
  link to Printec's *actual* pipeline/CRM, revenue, margin, or win/loss history.
- **Link rot / freshness:** ~15% of sources had HTTP errors or were unreachable this week; several items
  are flagged UNVERIFIED.
- **Cognitive load:** 8 dense tabs, ~29 signals, 156 competitors, 31 patterns, 23 deadlines, 15 + 11
  outlooks. Is it decision-grade for a time-poor executive, or an analyst's reference library? Is there
  a single "what changed and what should we do" view above the detail?
- **No owner / accountability layer:** follow-ups exist per signal, but there is no assignment, status,
  or closed-loop tracking of whether Printec acted and won.
- **Single-company internal data is absent:** the dashboard is outside-in (market signals). It does not
  ingest Printec's own bookings, capacity, delivery backlog, customer health, or churn.

## 6. Source files (open these to verify)

- `dashboard-web/index.html`, `dashboard-web/styles.css` — shell & design system.
- `dashboard-web/app.js` — all rendering logic (tab definitions ~lines 62–69; charts; evidence viewer).
- `dashboard-web/data.json` — the full data (1 MB; sample specific keys with `node -e` rather than reading whole).
- `dashboard-web/product-outlooks.js`, `dashboard-web/atm-sources.js` — the product-direction and multi-source-ATM layers.
- `master-signal-table.md` — the underlying weekly signal table.
- `findings/01..08/*.md` — the agent source documents (bank disclosures, tenders, regulation, statistics, jobs, vendors, futurist).
- `weekly-intelligence/` — the engine (build_dashboard.py, publish.py, verify.py) and briefs.
- Live (login-gated): `https://printec-market-research.vercel.app`.

**Your job:** judge it from your C-level seat — quality, completeness, clarity, how revealing/insightful it
is, and how helpful it is as a driver of Printec's **short-term** and **long-term** growth. Be specific,
be critical, cite the tab/field, and separate "genuinely good" from "looks impressive but doesn't help me decide."
