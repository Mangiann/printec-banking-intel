# Independent Board Adviser — challenge to the C-level review panel

*An 11th, deliberately adversarial voice. Its job was NOT to re-review the dashboard but to challenge the
panel of 10 — find what they collectively missed, where they contradict each other, where their praise or
criticism is overblown, and whose perspective is absent. Think activist non-exec + the company's owners.*

> **Editor's note (verified):** four of this adviser's load-bearing claims were independently re-checked
> against the actual code/data and **all four hold** — the June-25-generated `competition_brief` does state
> the 30 June votes "passed"; `verify.py:48-49` sets `check_hostname=False` + `CERT_NONE`; `prod_printec`
> carries a full 12-line capability map; and `single-vendor / customer concentration / fx risk / talent /
> reskill / attrition` all return **0 hits** in `data.json`.

---

## Collective blind spots — what no panelist raised but should have

1. **The usage question was never asked.** All 10 rated quality / insightfulness / completeness; not one
   asked the only question that ultimately matters — *does anyone open this tool, and has it ever changed a
   single Printec decision?* `data.json` KPIs are pure counts (`n_signals`, `n_new`); there is zero usage
   telemetry, no owner/outcome/acted field, no decisions-ledger. A 1 MB weekly artefact behind a login that
   no executive demonstrably reads would score **identically** on this panel. This is the most
   decision-changing gap in the whole exercise.

2. **No zero-based / kill option.** Every reviewer prescribed *more* — EV rollups, battlecards, scenario
   layers, capability overlays, talent panels, ABM export, enterprise-risk panels. Nobody asked whether the
   right move is *fewer, sharper, owned* outputs (kill 5 of 8 tabs; ship one weekly 5-line action memo to
   named owners; stop). The aggregate of the panel's "now" recs is a multi-quarter roadmap that would make a
   tool of unproven usage **heavier**. No one proposed sunsetting anything.

3. **Key-person / pipeline fragility was under-weighted.** Only the CDIO flagged the single-curator bus
   factor and silent-failure risk (`run_weekly.py` reuses cached files if a feed dies; no owner, no runbook;
   a manually-edited `master-signal-table.md`). For an 8-agent LLM pipeline that is the *foundation under
   every other reviewer's praise*, this is an existential operating risk treated as a footnote by 9 of 10
   seats.

4. **Selection bias was named but not indicted.** Several reviewers noted the cash-vs-future "tension." None
   drew the methodological conclusion: the tool measures best *exactly where Printec's legacy revenue already
   is* (tenders, ATM data rows, cash stats are the most instrumented → ATM/cash 85.8, 25/29 signals) and is
   near-blind *precisely where its own thesis says the future lies* (identity 22.5, HSM 16.5). The instrument
   systematically over-weights the harvest market and under-detects the build market — **so it will keep
   confirming the past.** That is a structural sourcing bias, not a UI "tension" to be "resolved" with a panel.

5. **Hallucination is systemic, and the panel's own "verification" is theatre.** The `competition_brief`
   asserts "both shareholder votes passed on 30 June" — generated 25 June, a future event stated as past.
   CDIO and COO caught it. But CEO, CFO, CCO, CSO and CMO each wrote that they "verified / web-checked" that
   exact Brink's/Atleos item as "exact/accurate" — and **all five missed the planted future-as-past error in
   the sentence they quoted.** If five C-levels "verify" a brief and none catches it, the evidence trail is
   breeding false confidence, not protecting against it.

6. **`prod_printec` exists — CHRO and CTO over-stated the gap.** `data.json` carries a rich per-line Printec
   capability map (e.g. "Payment HSMs Thales payShield 10K, remote key injection, PCI-PIN…"). The real defect
   is that capability is *described but never scored* or joined to demand intensity — so the
   demand-minus-capability delta can't be computed. Two reviewers framed it as "absent"; it is "present but
   unscored" — a far cheaper fix they missed by not reading the field.

7. **ROI / cost-to-run was raised by only the CFO.** An 8-agent LLM pipeline + a weekly re-fetch of 1,253
   sources has real recurring compute and human-curation cost. Nine of ten seats implicitly treat the tool as
   free and argue only about features. Without a cost-per-decision denominator, every "add this" rec is unpriced.

## Panel conflicts — where two roles materially disagree, and who is right

- **Feature maximalism vs what the CEO actually needs.** The CEO's own first weakness is cognitive load
  ("8 dense tabs, no what-changed/so-what/now-what view") and he asks for **one** apex screen. Yet CTO, CMO,
  CCO, CSO, CRCO and CHRO collectively prescribe a dozen *new* tabs/panels. The CEO wants compression; six of
  his reports want expansion. **The CEO's instinct is better-founded** — an unused tool gets less used, not
  more, by adding surface area.
- **Is the sizing honest or fabricated?** The CFO calls XL = exactly €7.5m "fabricated precision" that
  contradicts the "XL ≥ €5m" definition shown; the CDIO independently confirms the band-to-constant lookup;
  yet the CEO leans on the €99.3m as "a credible TAM-direction skeleton." These cannot both stand. **The
  CFO/CDIO reading wins**; the €99.3m is a band-count artefact, not a pipeline.
- **Access control.** The briefing and most reviewers assumed "the evidence is public." The CDIO read the code
  (`api/data.js`, `middleware.js`, `timingSafeEqual` on the upload secret) and showed the Blob is **private**
  and the whole site incl. evidence endpoints is gated. The CMO then built part of a "no externalization path"
  critique on the public-evidence premise. **The CDIO's code-level reading wins**; the public-evidence worry
  is wrong, and the CMO's externalization framing is partly mis-grounded (though the *positioning* gap stands).
- **Which layer is "strongest" is contested.** CTO and CSO crown the Futures/2030 thesis; CCO and COO crown
  the Accounts-&-timing trigger layer as the only thing they'd "deploy tomorrow." Given that near-term revenue
  funds the company and the Futures layer is entirely un-backtested (0/174 resolved), **the CCO/COO near-term
  bias is the more defensible anchor of value today.**
- **Confidence labels.** CRCO and CDIO say "High" on 14/15 outlooks is an over-claim against MAPE-null; the
  CMO calls the same projected ranges a "credibility moat" worth publishing. **The risk seat overrides the
  marketing seat** — publishing asserted-but-unbacktested "High" confidence externally is the riskier path.

## Overclaims to temper

- **"Best market-intelligence asset in the company" (CEO) / "better than most paid analyst output" (CTO) /
  "best situational-awareness product I've seen" (CSO)** — three superlatives, **zero comparators named.** No
  benchmark against existing analyst subscriptions, CRM intelligence, or the sales team's own field knowledge.
  The tool may be repackaging the same Grand View / SEC sources the analysts already use.
- **"I verified the Brink's/Atleos deal as accurate" (CEO, CFO, CCO, CSO)** — the same brief contains the
  false past-tense vote. Verifying the dollar figure while missing the temporal hallucination beside it is
  *partial verification dressed as full.* The honest claim is "I spot-checked the headline number."
- **CMO "almost no competitor has anything like it… no rival is publicly discussing" the gems** — the gems are
  derived from *public* regulation (AMLR Art.75, EUDI, AI Act, PQC) and public market reports, exactly what
  RegTech vendors and Big-4 publish constantly. The differentiation is **synthesis-for-our-footprint, not
  proprietary insight.**
- **CDIO "most genuinely engineered product…"** while the same review documents a headline hallucination,
  **TLS validation disabled** (`CERT_NONE`), no SLA, no alarm, no owner. A trust product whose own provenance
  layer disables cert validation is not "well-engineered" on that axis.
- **CCO "account_targets_ev re-ranking adds genuine value"** — `ev_score` is a 0-36 dimensionless ordinal and
  `win_prob` is an asserted 3-bucket label with 0/174 resolved. Re-ranking by an uncalibrated ordinal is a
  re-sorted guess, not a "risk-adjusted view," until any win_prob is back-tested.

## Missing voices — who a real Printec board would have added

1. **The owner / PE / shareholder.** Is the cash spent building and running this pipeline earning a return,
   and would that money do more deployed directly against the sales pipeline? No payback, no opportunity-cost
   framing, no "kill it and buy an analyst subscription" counterfactual.
2. **The actual user — a frontline sales rep / KAM / bid manager.** Every seat is C-level. Nobody asked the
   person who would supposedly act on "who to approach now" whether they'd open an 8-tab login-gated web app
   mid-deal — or whether they already know the PrivatBank lot from their own desk.
3. **The customer — a bank CIO/CISO/Head of Payments.** No bank-side voice tested whether the "why-now"
   triggers match how banks actually budget and procure; selection bias toward public tenders may miss the
   real, relationship-driven decision moments.
4. **A data-science / forecasting skeptic.** 174 forecasts, 0 resolved is not "unproven track record" — it is
   *no forecasting product yet*; the Outlook and Futures apparatus is currently **unfalsifiable.**
5. **An infosec / SRE voice on the pipeline itself.** `CERT_NONE`, silent cache-reuse on feed failure, and a
   single curator are red flags for a tool whose entire pitch is trustworthy provenance.
6. **A "do we even need this" cost-discipline challenger.** Would a quarterly human-written 2-pager deliver
   ~80% of the decision value at ~5% of the build/run cost and key-person risk? The null hypothesis the panel
   never entertained.
