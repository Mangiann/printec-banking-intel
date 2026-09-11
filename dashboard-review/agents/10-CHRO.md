# Chief Human Resources / People Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own workforce planning, capability building and talent strategy. My job is to staff the growth this
dashboard implies — to translate "where the money goes" into "what skills, how many people, in which
countries, by when, built or bought." Two things I came to the tool for:

1. **Hiring as a demand signal.** The pipeline carries a jobs/hiring agent (Agent 5). Banks hire ~6–12
   months *ahead* of the buy. I want that early-intent visible, and I want it turned around: where our
   *clients* are building teams tells us where they're about to spend — and (separately) what *we* must
   be able to deliver against.
2. **The capability gap.** The Future tab's own thesis is that banking's centre of gravity moves to
   identity, AML/financial-crime, AI governance/model-risk, PQC/crypto-agility, cloud-core and real-time
   data by 2030 — capabilities a long way from ATM field services. I need the dashboard to expose *our*
   gap against that, so I can plan hire/reskill/locate ahead of the 2027 regulatory wall.

## Verdict (TL;DR)

The hiring intelligence is genuinely good as a *client demand* signal and is already being used the smart
way — Agent 5 reads where banks are staffing (Piraeus's ~900 hires, Alpha's ~38 IT-risk/cyber roles, OTP
Srbija's AI/DevOps/ICT-risk cluster) and corroborates the strongest deals (PrivatBank confirmed by A1+A2+A5).
But that intelligence is **buried inside signal prose and "(A5)" citations — there is no jobs/hiring view,
no leadership-mover board, no demand-lead-time framing.** And on my second, bigger question the tool is
**effectively silent**: a full-text scan of `data.json` returns **0** hits for skill, reskill, talent,
workforce, scarcity, staffing, attrition, wage or salary. The dashboard models demand as if labour to
deliver it is free and infinite. That is a real blind spot, because the exact capabilities its 2030 thesis
chases — AML/RegTech, AI-governance, PQC/HSM, identity — are the scarcest, slowest-to-build skills in the
market right now. This is the dashboard's least-served seat, and it matters.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 6 | Agent 5 source material is rigorous and triangulated, but talent is never treated as a variable. |
| Completeness | 3 | Client-hiring is present; Printec's own capability gap, scarcity and location strategy are absent. |
| Clarity | 5 | Hiring intel is real but hidden in prose; no dedicated surface, no "skills by deadline" view. |
| Insightfulness | 4 | Surfaces client buying-intent well; reveals nothing about the constraint on executing the strategy. |
| Short-term growth | 6 | Leadership-mover + careers signals are usable now for outreach timing and account entry. |
| Long-term growth | 3 | Names where the money goes but not who builds it — no workforce roadmap to the 2027/2030 wall. |
| **Overall** | **4.5** | A strong demand engine that ignores the talent supply side that determines whether we can deliver. |

## What is genuinely good

- **Agent 5 as a leading buying-intent indicator — and already used the right way.** The brief asks whether
  hiring could be turned around to read where clients are building teams. It already is. In the jobs findings
  (`findings/05-jobs/2026-06-24.md`) and the master signals, **Piraeus's "~900 new hires (~70% under 35)"**
  across a 2026–2030 AI/digital plan, **Alpha Bank's "~38 live roles" in Cyber Risk, IT Risk & Compliance,
  Software Architecture and Data Engineering**, **Alpha Bank Cyprus's CRM/Salesforce + Credit-Risk-Models
  hiring**, and **OTP Srbija's AI/DevOps/ICT-risk cluster** are read as forward signals of platform spend.
  That is exactly the inversion I wanted — client headcount as a demand antenna.
- **Triangulation gives the signals credibility.** PrivatBank and the Hungarian Act XVIII build are confirmed
  across disclosures (A1) + tenders (A2) + jobs (A5). When hiring corroborates a tender, I trust the timing
  enough to pre-position delivery capacity. That A5 cross-check is real evidence discipline.
- **Named leadership movers are an account-entry gift.** SLSP's new CEO Michaela Bauer (ex-KBC CIO), NLB's
  CTO Reinhard Holl, K&H's CIIO Loska Gergely, Intesa RO's new COTO Anca Petcu — each tagged with a "why-now"
  and an org to approach. For my counterparts on the sales side this is high-quality, time-sensitive material.

## What is missing or weak

- **No jobs/hiring surface at all.** I checked `app.js`: the only trace of Agent 5 is the evidence-viewer
  label `'05-jobs':'Jobs & leadership'` (line 117). There is no tab, chart, or "who's hiring what, where"
  board. The richest leading indicator in the pipeline is reduced to "(A5)" inside paragraphs. A time-poor
  reader will never extract the hiring story.
- **Zero capability-gap layer for Printec.** The Products tab (`data.json` products) scores *client demand
  intensity* — ATM/cash 85.8 down to card issuing 7.5 — but there is no parallel read of **our delivery
  capability** per line. I cannot see whether we can actually staff AML/RegTech (client demand 49.2 +
  fraud 38.1), digital identity (22.5) or HSM/PQC (16.5). Demand without a capability overlay is half a
  decision.
- **No "skills × country × deadline" view against the regulatory wall.** The deadline tracker (23 dated
  items — AMLR 10 Jul 2027, AMLA supervision, DORA-adjacent, EUDI wallet Dec 2026, PQC 2027–2030) is the
  natural spine for a workforce plan. Nothing converts a deadline into an FTE/skill requirement by geography.
  I cannot answer "how many AML engineers and identity specialists, in which countries, by when."
- **Talent never appears as a constraint on the growth story.** The €99.3m pipeline and the 2030 thesis are
  presented as if deliverable on demand. There is no scarcity flag, no time-to-hire, no wage-pressure, no
  build-vs-buy note. The futures `gems` (eIDAS-2 relying parties, AML Article-75 data utility, PQC/HSM
  migration) are commercial openings that each presume scarce, hard-to-hire talent — and that risk is unstated.
- **No location strategy input.** Our footprint spans 17 countries with very different labour costs and talent
  depth (Ukraine engineering, Romania/Bulgaria scale, Greece compliance). The dashboard never connects demand
  geography to where we should *site* capability. That's a core CHRO decision left unsupported.

## What I cannot decide from this today

- **Where to invest reskilling budget.** I can see ATM/cash is the demand mass *this week* and identity/AML/HSM
  is the long-term spine — but not how fast to move field-service and ATM engineers toward RegTech/identity/cloud
  roles, or what that retraining costs and takes.
- **The 2027 staffing plan.** I cannot size the AML/AI-governance/PQC team needed to capture the AMLR/AMLA/DORA
  wave, nor phase hiring against the dated deadlines, nor decide which countries to hub it in.
- **Build vs buy vs partner for scarce capability.** No view of where we acquihire, partner (e.g. with the AML
  utility / identity plays the gems describe), or train internally.
- **Whether the pipeline is even staffable.** If we won a meaningful share of €99.3m skewed toward instant
  payments, AML and identity, could we deliver it with today's workforce? The tool offers no answer.

## Domain reality-check

External evidence strongly supports treating talent as a binding constraint — which makes its absence here a
genuine flaw, not a nicety:

- AMLA is scaling to **>400 staff by end-2027** and **AMLR obligations bite 10 Jul 2027**; advisers are telling
  institutions to **resource and train AML talent now**, with **75% of compliance professionals expecting a very
  competitive market** for AML specialists ([Fourthline](https://www.fourthline.com/blog/how-to-prepare-for-amla-compliance-what-financial-institutions-must-do-before-2027),
  [Selby Jennings](https://www.selbyjennings.com/en-us/industry-insights/hiring-advice/the-compliance-market-in-europe)).
- The scarcest profile is exactly the **hybrid compliance-plus-technology** skill the dashboard's thesis chases;
  these roles take years to build and run **48–89 day** time-to-fill, with a structural shortfall of ~**350,000
  digital workers** and fintechs poaching compliance leads ([Wolters Kluwer](https://www.wolterskluwer.com/en/expert-insights/bankings-talent-crisis-is-now-a-strategic-risk),
  [MSH](https://www.talentmsh.com/insights/hiring-trends-statistics-financial-services-banking)).
- **DORA is already reshaping hiring** (cited by ~26% of organisations), and **60% of compliance teams plan new
  technology investment** for AMLR ([Financial Crime Academy](https://financialcrimeacademy.org/aml-recruitment-trends/)).

What the dashboard gets right: its *demand* and *regulatory-timeline* reads are accurate and consistent with this
external picture — the money really is moving where the thesis says. What it gets wrong by omission: it presents
that demand as frictionless, when the binding constraint across the whole industry is the supply of the very
people who deliver it. For a systems integrator whose product *is* its people, that omission understates
execution risk on the entire growth story.

## My recommendations

**Now** (low effort, high impact) — *unlocks: turn hiring intel into action; flag execution risk.*
- Add a **"Who's hiring what" panel** (Overview or Accounts) that lifts Agent 5's client-hiring and leadership
  movers out of prose: bank, country, role cluster (AI / AML / cyber / cards / channels), and the demand lead-time
  read. Pure re-surfacing of data already in `findings/05-jobs` — no new sourcing.
- Add a one-line **talent-constraint flag** to each Future `gem` and high-value outlook ("requires scarce
  AML/identity/PQC skills; market time-to-fill 2–3 mo"), citing the AMLR/AMLA timeline. Cheap honesty that
  reframes the growth story as resource-constrained.

**Next** (medium effort, high impact) — *unlocks: reskilling budget and the 2027 staffing plan.*
- Build a **capability overlay on the Products tab**: alongside client-demand intensity per line, a Printec
  delivery-capability/coverage score. The demand-minus-capability delta is the reskilling priority list.
- Add a **"skills × country × deadline" view** off the deadline tracker that converts each dated item (AMLR 2027,
  EUDI 2026, PQC 2027–30) into an indicative skill mix and geography, so I can phase hiring against the wall.

**Later** (higher effort, high impact) — *unlocks: location strategy and build/buy/partner decisions.*
- Add a **talent-supply lens by country** (cost, availability, attrition for AML/identity/cloud/cyber) so demand
  geography maps to where we should site or hub capability — feeding a deliberate location strategy across the
  17-country footprint.
- Ingest a minimal slice of **internal workforce data** (headcount + skills by line/country, open reqs, delivery
  backlog) so the outside-in market view finally meets the inside-out capacity view, and the €99.3m pipeline can
  be tested for staffability.
