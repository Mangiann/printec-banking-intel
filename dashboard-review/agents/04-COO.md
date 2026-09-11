# Chief Operating Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own delivery capacity and managed-services operations across ~17 markets. My job is to make sure that when the
commercial side wins, we can actually deliver — the right skills, in the right country, at the right time — without
over-committing engineers in one geography while another opportunity starves. I need this dashboard to do three
operational things: (1) give me enough **lead time** on real buying windows to staff and pre-position; (2) tell me
**which capabilities and which countries** demand is concentrating in, so I can capacity-plan and hire ahead of the
curve; and (3) close the loop — show me whether a surfaced opportunity was **acted on, bid, won or lost**, so I can
hold the delivery org accountable and learn. Crucially I need the NCR Atleos/Brink's event translated into an
operational contingency I can execute, because that is my single largest partner-dependency risk.

## Verdict (TL;DR)

This is an excellent market-sensing instrument and a weak operating instrument. The signal quality, follow-up
specificity and the Brink's/Atleos competitive read are genuinely strong — I trust the *what's happening*. But it is
outside-in only: there is no owner, no status, no due-date, no closed-loop tracking, and zero connection to my
delivery backlog, skills inventory or capacity by country. I cannot capacity-plan from it, I cannot tell whether we
acted on last week's "imminent" windows, and the one event that most threatens my operations — our key ATM partner
becoming a CIT-conglomerate competitor — is described vividly but not converted into a contingency I can run. It tells
me where to look; it does not help me decide what to staff.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 7 | Signal follow-ups are specific and corroborated; merger facts check out against the SEC 424B3. |
| Completeness | 4 | No owner/status/closed-loop layer, no capacity/skills/country-resourcing layer, no link to Printec's own backlog. |
| Clarity | 6 | "Recommended follow-up" is readable per-signal, but there is no single ops view of "what's due, who owns it, are we late." |
| Insightfulness | 6 | The consolidation-of-the-cash-value-chain read is genuinely revealing; the rest mostly tells me what BD already knows. |
| Short-term growth | 5 | Deadline tracker has live windows, but several "imminent" items give me <7 days — too late to mobilise delivery. |
| Long-term growth | 6 | The managed-services-annuity thesis is the right strategic frame; it just isn't operationalised into a capability roadmap. |
| **Overall** | **5.5** | A best-in-class market radar bolted to a non-existent operating cockpit. |

## What is genuinely good

- **Accounts & timing → follow_up field.** Every one of the 29 signals carries a substantive, concrete next action.
  The PrivatBank 800-unit lot reads: *"Register/monitor tender.privatbank.ua + Prozorro buyer 14360570 weekly for the
  800-unit notice; brief NCR Atleos incumbent-defence; confirm 2025 delivery completion."* That is operator-grade — it
  names the portal, the buyer ID and the cadence. This is the best part of the tool for me.
- **Deadline tracker (Accounts & timing).** 23 dated items, correctly bucketed imminent/soon/later with `days_until`,
  each with a "forces" rationale tying the date to bank spend and the affected geographies/products. The Bulgaria
  lev→euro window (free exchange ends 30 June → "banks rationalise the temporary cash capacity… fleet optimization,
  recycler recalibration, decommissioning") is exactly the kind of post-event managed-services pull my org should be
  pre-staffing for.
- **Competition brief on Brink's/NCR Atleos.** The prose is accurate and sharp — I independently verified the core
  facts against the SEC 424B3 (vote 30 June 2026, $30 cash + 0.1574 BCO/share, ~22%/78% ownership split). It correctly
  identifies that Brink's Hellas already runs CIT + full ATM managed services in Greece *today* — i.e. the competitive
  threat is live in my home market before the deal even closes.
- **Triangulation.** The strongest opportunities are confirmed across multiple agents (disclosures + tenders + jobs),
  which gives me confidence the demand is real before I commit delivery thinking to it.

## What is missing or weak

- **No owner / status / closed-loop layer.** I checked the signal schema directly: the only accountability-adjacent
  field is `status`, and its values are `NEW / UPDATED / SECURED` — these describe the *signal's* lifecycle, not
  *Printec's* action. There is no assignee, no "bid/no-bid" decision, no bid-due date, no win/loss outcome. Last week's
  10 "imminent" follow-ups have no record of whether anyone did them. Signals → action → outcome is structurally
  broken, and that is the single biggest gap for my seat.
- **No capacity / skills / country-resourcing layer.** I can see *demand* by country (GR 7 signals, RO 5, RS/MK 4 each,
  BA/ME 3) and by product line, but nothing about my *supply*: which skills each opportunity needs, the delivery effort,
  or my current load by geography. Only 5 of 29 follow-ups even mention resourcing, and none translate into "you will
  need N recycler-certified engineers in Romania in Q3." I cannot capacity-plan from this — which is the literal thing
  this dashboard was supposed to help me do.
- **"Imminent" is often too late for delivery.** Of 10 imminent deadlines, 7 fall within 14 days and 5 within 7 days of
  the snapshot. A POS-subsidy window closing in 5 days, or Croatia Post's POS-maintenance tender closing 6 July, gives
  my delivery org no usable mobilisation runway. The bucketing is honest but exposes that the weekly cadence surfaces
  some windows after the point where ops can pre-position.
- **Brink's/Atleos has no executable contingency.** The deadline item says *"Scenario planning required"* — but the
  dashboard stops there. For an event that could turn my key hardware partner into a competitor-conglomerate, I need a
  contingency I can run: alternate-hardware qualification timeline (Hyosung/Diebold), spare-parts and SLA exposure on
  the existing Atleos base, which managed-services contracts are most exposed, and a trigger date. None of that is here.
- **Stale-as-of-generation risk.** The data is generated 2026-06-25 but asserts "both shareholder votes passed 30 June"
  — a future event stated as fact. The open shareholder litigation (suits filed 10–11 June) that creates genuine
  deal-completion uncertainty is not surfaced as a risk factor. For contingency planning, that uncertainty matters.

## What I cannot decide from this today

- **Where to add or move delivery headcount over the next two quarters.** No skills-by-opportunity, no effort sizing,
  no current-load view.
- **Whether we are over- or under-committed in any of the 17 markets.** Demand is shown; my capacity is invisible, so
  the balance I most need to manage is unanswerable.
- **Whether last week's opportunities converted.** No closed loop means I cannot run an ops review of "we flagged 10
  imminent windows — how many did we bid, how many did we win, where did delivery slip."
- **What to physically do about Atleos.** No alternate-vendor qualification plan, no exposure map, no trigger date.
- **Which "imminent" windows are still catchable.** Without a bid-due field and an owner, I cannot triage the 5-day
  windows from the 36-day ones operationally.

## Domain reality-check

The competitive intelligence holds up. I verified the Brink's/NCR Atleos terms against the SEC Form 424B3
(EDGAR CIK 0000078890): special meetings 30 June 2026, $30.00 cash + 0.1574 BCO share per NATL share, ~22%/78%
post-merger ownership — all consistent with the dashboard. The framing that this combines CIT + ATM managed services +
Atleos hardware into one end-to-end rival is the correct operational read, and Brink's Hellas's existing CIT-plus-ATM
footprint in Greece is real. Two things the dashboard under-weights: (1) the merger faced **shareholder litigation**
(suits 10–11 June 2026 alleging disclosure deficiencies) and a UK competition review — both are deal-completion
contingencies my partner-risk planning should hold, and the dashboard treats close as near-certain; (2) it states the
30 June vote as already-passed in a 25 June snapshot, which is a tense/freshness error.

Sources: [SEC Form 424B3, Brink's/NCR Atleos](https://www.sec.gov/Archives/edgar/data/0000078890/000114036126022935/ny20069704x6_424b3.htm);
[NCR Atleos & Brink's reaffirm merger amid shareholder suits — TipRanks](https://www.tipranks.com/news/company-announcements/ncr-atleos-brinks-reaffirm-merger-amid-shareholder-suits).

## My recommendations

**Now**
- *Add an owner + status + bid-due field to every Accounts & timing signal* (effort: low; impact: high). Even a simple
  Owner / Bid-due / Decision (bid·no-bid·watch) / Outcome (won·lost·pending) closes the loop. Unlocks: weekly ops
  accountability review and a measurable conversion rate on flagged opportunities.
- *Turn the Brink's/Atleos item into a one-page ops contingency* (effort: low; impact: high) — exposure map of
  Atleos-dependent managed-services contracts, alternate-hardware qualification lead time, spare-parts/SLA risk, and a
  named trigger date. Unlocks: a partner-risk decision I can actually execute instead of "scenario planning required."

**Next**
- *Add a delivery-effort / skills tag per opportunity* (effort: medium; impact: high) — even coarse (recycler-cert
  engineers, integration days, country). Unlocks: capacity planning and ahead-of-curve hiring by geography.
- *Flag windows by mobilisation-feasibility, not just days_until* (effort: low; impact: medium) — mark deadlines where
  the runway is too short for delivery to pre-position vs. those still catchable. Unlocks: honest ops triage.

**Later**
- *Ingest Printec's own backlog/capacity/utilisation by country* (effort: high; impact: high) to render a true
  demand-vs-supply view. Unlocks: the over/under-commitment decision across 17 markets that I cannot make today.
- *Operationalise the managed-services-annuity thesis into a capability roadmap* (effort: medium; impact: medium) —
  which managed-services skills to build over 2–5 years to defend the cash/ATM annuity while pivoting toward
  identity/real-time-data delivery. Unlocks: long-term workforce strategy aligned to the futures board.
