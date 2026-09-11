# Printec Banking Intelligence Dashboard — C-Level Review: Final Report

**Date:** 2026-06-29 · **Snapshot reviewed:** week of 2026-06-25
**Method:** 10 simulated Printec C-level executives reviewed the dashboard independently and critically, each
grounding their critique in the live files, **web-verifying** facts in their domain, and writing a full report
(`agents/01…10`). An 11th independent "board adviser" then challenged the panel for blind spots, conflicts and
overclaims (`agents/11`). I then computed the consensus, **independently re-verified the four most consequential
claims against the actual code/data**, and wrote the verdict below. No file in the dashboard or project was changed.

---

## 1. The bottom line

> **The best outside-in market radar Printec owns — rigorous, well-sourced, and unusually honest about its own
> limits — but unproven in actual use, structurally biased toward the legacy cash/ATM market, resting on a
> fragile single-person pipeline, and one synthesis layer short of decision-grade.
> Prove usage and fix the trust defects before adding surface area.**

**Panel overall: 6.2 / 10.** This is a genuinely strong intelligence *library*, not yet an executive *cockpit*.
It tells leadership what is happening and even where 2030 is going; it cannot yet let them **size a bet, net it to
what Printec can deliver, or prove it changed a decision.** The good news: the two highest-impact fixes are cheap
(two multiplies and two labels). The hard news: the deepest issues are not features — they are *usage, sourcing
bias, and trust*, and more tabs make them worse.

## 2. Scorecard (panel average across all 10 seats)

| Dimension | Score /10 | Read |
|---|---|---|
| **Quality** (rigour, evidence, accuracy) | **7.2** | Highest-rated. Real evidence discipline, traceable scoring, web-verifiable facts. Dragged down by an uncaught hallucination and disabled TLS validation in the trust layer. |
| **Insightfulness** (how revealing) | **7.1** | The 2030 thesis and the 5 "gems" are sharper than most paid analyst output. |
| **Long-term growth utility** | **6.3** | Correct, load-bearing strategic thesis — but stops at diagnosis, no bets made. |
| **Clarity** (clearness, IA) | **6.2** | Excellent tab-level "so-what" copy; but 8 dense tabs with no apex compression view. |
| **Short-term growth utility** | **6.0** | Operator-grade triggers a rep could use — but no named buyer, battlecard or CRM loop. |
| **Completeness** (vs what's needed to decide) | **5.1** | **Lowest, tellingly.** No expected-value sizing, no inside-out Printec data, no own-risk/talent lens. |
| **Overall** | **6.2** | A strong radar that ends one layer short of a decision instrument. |

The *shape* of the scorecard is the headline: **high on quality/insight, lowest on completeness.** The tool knows
a lot and reasons well; it just doesn't close the loop into a decision.

## 3. Per-seat verdicts

| # | Seat | Score | One-line verdict |
|---|---|:--:|---|
| 1 | **CEO** | 6.3 | "Decision-*informing*, not yet decision-*grade*: an analyst's library, not a CEO's cockpit — can't size a bet or resolve cash-vs-future into an allocation." |
| 2 | **CFO** | 5.3 | "A strong market radar but not a financial instrument: the €99.3m is a gross band-count, forecasts are 0/174 resolved, no link to our P&L." |
| 3 | **CTO / Innovation** | **7.5** | "Stronger than most paid analyst output — a correct thesis and 5 buildable, legally-anchored gems — but it stops at diagnosis: no build/buy/partner verdict." |
| 4 | **COO** | 5.5 | "Excellent market-sensing, weak operating instrument: no owner/status/outcome loop, no capacity link, the partner-risk event never becomes a contingency." |
| 5 | **CCO (Sales)** | 6.5 | "The best 'why-now' trigger radar I've seen for our footprint — but a battlecard *input*, not a battlecard *system*: no named buyers, no how-to-win." |
| 6 | **CSO (Strategy)** | 7.0 | "Has the raw material for strategy and reasons the Atleos threat — but delivers one deterministic narrative, never a ranked where-to-play or the actual call." |
| 7 | **CMO** | 7.0 | "The strongest marketing raw material we own, trapped in a login-gated tool with no externalization path and no stated positioning." |
| 8 | **CDIO (Data)** | 6.0 | "The most genuinely engineered product at Printec — but not board-certifiable until the temporal hallucination, the sizing labels, and the SLA/owner gaps are fixed." |
| 9 | **CRCO (Risk)** | 6.5 | "Regulatory layer is genuinely trustworthy (web-verified) — but it barely touches Printec's *own* risk, and 14/15 'High' labels outrun a 0/174 track record." |
| 10 | **CHRO (People)** | **4.5** | "Models demand as if labour to deliver it were free: zero hits for skill/talent/workforce — silent exactly where the 2027 skills are scarcest." |

The spread (4.5 → 7.5) is itself a finding: the dashboard serves **strategy/innovation/marketing** seats well and
**finance/operations/people** seats poorly — because it is outside-in market intelligence with no inside-out layer.

## 4. What is genuinely good (consensus — cited by 3+ seats)

1. **A decision-grade, externally-verifiable competition read.** The Brink's / NCR Atleos ~$6.6bn item (and
   Euronet/CrediaBank) lands the "partner-becomes-competitor" so-what cleanly; the headline figures check out
   against SEC filings. *(Caveat in §6 — the same brief carries an uncaught hallucination.)*
2. **A correct, load-bearing 2030 thesis.** "Value migrates to operating the regulated rails — identity, fraud,
   real-time data, resilience, governance — as managed services across many markets; cash/ATM is the annuity to
   optimise, never the growth spine." Five legally-anchored, buyer-and-date-specific **gems** (AMLR Art.75 neutral
   utility, EUDI long-tail acceptance, AI-Act self-attestation, PQC/HSM discovery, PSD3/MiCA re-auth cohort).
3. **Genuine evidence discipline.** `cite_ungrounded` self-flags extrapolation; agent triangulation (A1+A2+A5);
   `verify.py` writes point-in-time snapshots of every cited URL.
4. **An operator-grade trigger layer.** 26–29 dated, incumbent-aware account targets with specific follow-ups
   (PrivatBank 800-unit lot, Prozorro buyer ID, weekly cadence) and a **regulatorily-accurate** deadline tracker
   (IPR, AMLR, EUDI, AI-Act dates web-verified as correct, including the non-euro-CEE nuances).
5. **Honest, traceable internals.** `forecast_accuracy {174/0/null}` is *shown, not buried*; scoring reproduces
   from source code; the dual-ranking `ev_score` already separates "how big" from "how likely."

## 5. What is weak or missing (consensus — cited by 3+ seats)

1. **No expected-value / bet-sizing layer.** `pot_value` is a flat band constant (XL = exactly €7.5m each) and
   `win_prob` is a text label, so a value × p-win ranking is *not computable*. The €99.3m headline is a
   non-additive band-count, not a pipeline — and it contradicts the "XL ≥ €5m" definition shown to readers.
   **Both inputs to fix this already exist in the data.**
2. **No inside-out link to Printec's own economics.** Zero ingestion of bookings, backlog, margin, win/loss or
   capacity, so opportunity can never be netted to right-to-win or deliverable SOM. *(7 of 10 seats.)*
3. **Forecasts are unproven and confidence is over-claimed.** 14–15 of 15 outlook cards assert "High" while 0 of
   174 forecasts are resolved (MAPE null) — assertions, not back-tested planning inputs.
4. **It stops at diagnosis, never reaches a verdict.** No build/buy/partner call on the gems; no scenario branches
   with triggers/probabilities on the pivotal Atleos question; no ranked where-to-play / harvest-vs-build / exit
   allocation; no battlecards; no named buyers.
5. **No apex compression and no closed loop.** 8 dense tabs, no "what changed / so what / now what" view; no
   owner/status/outcome tracking — so the cash-vs-future tension is *presented* but never *resolved* into action.

## 6. The five sharpest, decision-changing insights (independently verified where marked ✅)

These came mostly from the independent critic and the most rigorous seats. They matter more than the feature list.

1. **The usage question was never asked — and there's no way to answer it.** Zero usage telemetry, no
   decisions-ledger. *No one can show the tool has ever changed a single Printec decision.* A polished weekly
   artefact behind a login that no exec demonstrably reads would score the same. **This is the most important
   finding in the review.**
2. **Selection bias is structural, not a "tension."** ✅ The instrument measures best exactly where Printec's
   legacy revenue already is (ATM/cash 85.8, 25/29 signals — tenders/cash stats are the most instrumented) and is
   near-blind where its own thesis says the future lies (identity 22.5, HSM 16.5). **It will keep confirming the
   past.** No UI panel fixes a sourcing bias.
3. **The evidence trail is breeding false confidence.** ✅ The `competition_brief`, **generated 25 June**, states
   the 30 June votes "**passed**" — a future event written as past. Five C-levels wrote they "verified" that exact
   item as accurate; **all five missed it.** A trust layer that produces over-trust is worse than none. *(Also ✅:
   `verify.py` disables TLS validation — `CERT_NONE` — so a green ✓ certifies reachability, not authenticity.)*
4. **Key-person / pipeline fragility is existential, not a footnote.** Single curator, no runbook, no owner of
   record, a manually-edited `master-signal-table.md`, and `run_weekly.py` silently reuses cached files when a
   feed dies. The foundation under every other strength can die quietly.
5. **The Atleos consolidation is BOTH a competitive threat AND Printec's single largest supplier-dependency
   risk.** ✅ `single-vendor`, `customer concentration`, `fx risk` all return **0 hits** in data.json; the biggest
   near-term sourcing risk is filed only as competitive news, with no second-source / term-renegotiation trigger
   before the ~Q1-2027 close.

*Bonus correction (✅):* the Printec capability map **exists** (`prod_printec`, 12 detailed lines incl. payShield
10K HSMs) — CHRO/CTO called it "absent." The cheap fix is to **score it and join it to demand**, not build it.

## 7. Where the panel disagreed — and which view wins

- **Compression vs expansion.** The CEO (the actual user) wants *one* apex screen; six reports prescribe a dozen
  new panels. → **Compression wins.** An unproven-usage tool gets less used by adding surface area.
- **Is €99.3m credible?** CEO leans on it; CFO/CDIO prove it's a band-count artefact. → **CFO/CDIO win.**
- **Is the evidence public?** Most assumed yes; CDIO's code reading shows it's private/gated. → **CDIO wins**
  (so the CMO's externalization critique is partly mis-grounded, though the *positioning* gap is real).
- **Strongest layer — Futures or Triggers?** → For *value realised today*, **the near-term trigger layer wins**;
  the Futures layer is unfalsifiable until forecasts resolve.
- **Publish "High"-confidence ranges externally (CMO) or suppress them (CRCO/CDIO)?** → **Risk seat wins** —
  don't externalize asserted-but-unbacktested confidence.

## 8. Prioritized roadmap (consolidated, de-duplicated, ranked)

### NOW — cheap, high-impact, mostly trust & compression (do before adding anything)
| Action | Effort | Impact | Owner |
|---|:--:|:--:|---|
| **Answer the usage question first:** add open/read telemetry + a one-line decisions-ledger (signal → acted? → won? → €). If after one quarter nothing traces to the tool, treat that as the governing fact. | low | high | CDIO |
| **Temporal-honesty governance pass** over all LLM prose (flag any future-dated event written in past tense — catches the "30 June passed" error) **+ relabel every € figure** as "indicative size-band proxy (XL ≈ €7.5m), not a pipeline forecast." | low | high | CDIO |
| **One apex "CEO brief" screen** (top-3 what-changed · so-what allocation · 1-2 now-what actions) — and *resist new tabs.* Pair with an **EV column** (`pot_value × P(win)`, map High/Med/Low → 0.6/0.35/0.15) beside the gross band-sum. | low | high | CEO |
| **Dual-frame the Brink's/Atleos item:** keep the competitive read; add a supplier-dependency/sourcing-continuity risk read with a named trigger date + a Hyosung/Diebold second-source qualification lead-time + a one-page ops contingency. | low | high | CRCO / COO |
| **Add owner/status/named-buyer layer** to the 26–29 account targets (+ a "door just opened/closed" flag off competition_brief) so the trigger list runs as a closed-loop pipeline. | low | high | CCO |
| **De-risk the pipeline:** name an owner of record, write a runbook, replace silent cache-reuse with an agent-health/freshness stamp + run ledger, and re-enable TLS validation in `verify.py`. | med | high | CDIO |

### NEXT — turn diagnosis into verdicts
| Action | Effort | Impact | Owner |
|---|:--:|:--:|---|
| **Score the existing `prod_printec` capability map and join it to demand intensity** → the demand-minus-capability delta is simultaneously the reskilling list (CHRO) and the R&D-allocation input (CTO). Add a build/buy/partner verdict + have/need-to-acquire row to each gem. | med | high | CTO |
| **Render a ranked where-to-play table** (17 markets: ATM tier × competitive pressure × Printec position → double-down / harvest / **exit**) + **scenario branches** on Atleos (neutral / direct-disintermediation / CMA-block) with triggers, rough probabilities, pre-committed moves. | high | high | CSO |
| **Begin resolving forecasts** → first MAPE; split confidence into model-fit vs track-record; stop printing bare "High" while MAPE is null; **do not publish** unbacktested confidence externally. | med | high | CRCO / CDIO |
| **Competitor battlecards** (Mellon, Euronet, Payten/Asseco, NCR-Atleos/Brink's, Hyosung) tied to the pressure-matrix cells. | med | med | CCO |
| **Decide positioning + controlled externalization:** claim "the neutral operator of the regulated rails across CEE/SEE"; build export-as-briefing with a public/confidential flag per field — gated behind the trust fixes; temper the "no rival has this" claim. | med | med | CMO |
| **Run the kill/zero-based counterfactual at budget time:** price the weekly run (compute + curator time), compute cost-per-decision from the new ledger, benchmark vs a quarterly human 2-pager and vs existing analyst/CRM subscriptions. | low | high | CFO |

### LATER — the inside-out leap (the structural upgrade)
| Action | Effort | Impact | Owner |
|---|:--:|:--:|---|
| **Ingest a read-only slice of Printec's own bookings/backlog/margin/win-loss + a minimal workforce/skills-by-country layer** → back-test win_prob, compute true SOM, capacity-plan delivery, and convert the regulatory clock into a skills × country × deadline hiring plan. *This is the deepest consensus gap (7 seats) and the move from intelligence library to steering instrument.* | high | high | COO |

## 9. My executive verdict (for the CEO and owners)

Printec has built something rare: a weekly, well-sourced, self-aware market-intelligence engine that most
mid-cap competitors cannot match, and whose 2030 thesis — *win by operating the regulated rails as managed
services* — is, in my judgement, **correct and the right organising idea for the company's long-term strategy.**
That alone makes it worth keeping.

But be clear-eyed about three things the polish can hide:

1. **It is currently a sensing instrument, not a steering one.** It has no expected-value, no link to your own
   numbers, and an unproven forecast record. Treat its euro figures as *direction*, never as *plan*, until the
   EV multiply and the inside-out link land.

2. **Its sourcing is biased toward your past.** Because cash/ATM is the most instrumented market, the tool will
   keep surfacing the harvest business and under-detecting the build business its own thesis says is the future.
   Don't let weekly signal-volume drive capital allocation — the absence of identity/HSM signals is a measurement
   artefact, not a market verdict.

3. **The single most valuable next step is not a feature — it's proof of use.** Before funding the (substantial)
   roadmap the panel wants, instrument whether anyone opens it and whether it has ever changed a decision or won a
   deal. If it has, the inside-out investment is obvious. If it hasn't after a quarter, the right answer may be a
   sharper, smaller tool — one apex action-memo to named owners — not a bigger one. And fix the trust defects
   (the future-as-past hallucination, the disabled TLS check, the single-curator fragility) regardless, because
   they quietly corrode the one thing the whole product sells: credibility.

**Net:** a genuine asset, scored ~6/10 today, with a clear and mostly *cheap* path to ~8 — provided the next moves
are *prove usage → fix trust → compress to action → connect inside-out*, in that order, rather than *add more tabs*.

## 10. Honest note on this exercise

This review was produced by 10 simulated executive personas plus an adversarial critic — not by Printec's real
leadership, real users, or real customers. The critic correctly flagged that the **actual user (a sales rep/bid
manager), the customer (a bank CIO), and the owner/PE seat were absent**, and that no real usage data exists to
test the tool's value in practice. Where claims were checkable I verified them against the live code and data
(§6); where they rest on judgement, they are flagged as such. The strongest single recommendation — *measure
usage and decisions before scaling* — is precisely the gap this simulation could not close on its own.

---

### Appendix — review documents
- **Briefing the panel critiqued against:** [00-DASHBOARD-BRIEFING.md](dashboard-review/00-DASHBOARD-BRIEFING.md)
- **Individual C-level reports:**
  [CEO](dashboard-review/agents/01-CEO.md) ·
  [CFO](dashboard-review/agents/02-CFO.md) ·
  [CTO](dashboard-review/agents/03-CTO.md) ·
  [COO](dashboard-review/agents/04-COO.md) ·
  [CCO](dashboard-review/agents/05-CCO.md) ·
  [CSO](dashboard-review/agents/06-CSO.md) ·
  [CMO](dashboard-review/agents/07-CMO.md) ·
  [CDIO](dashboard-review/agents/08-CDIO.md) ·
  [CRCO](dashboard-review/agents/09-CRCO.md) ·
  [CHRO](dashboard-review/agents/10-CHRO.md)
- **Independent board-adviser challenge:** [11-CRITIC-board-adviser.md](dashboard-review/agents/11-CRITIC-board-adviser.md)
