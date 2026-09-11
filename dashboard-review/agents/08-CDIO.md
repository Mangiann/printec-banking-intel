# Chief Data & Information Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own this artefact *as a data product*. My job is not to like the charts — it is to be able to stand
in front of the board and say "you can act on this number" without later being embarrassed. That means
I need: traceable provenance, a transparent and reproducible scoring method, honest uncertainty,
controlled access to anything competitively sensitive, and a maintenance/lineage story that survives a
key person being on holiday or a feed dying silently. I read the engine (`ingest.py`, `build_dashboard.py`,
`verify.py`, `publish.py`), the API layer (`api/data.js`, `api/evidence.js`, `api/upload.js`,
`middleware.js`) and sampled the live `data.json`. The good news: this is engineered far better than the
briefing implies. The bad news: it is not yet board-certifiable, and one of the briefing's own claims is
wrong in a way that matters.

## Verdict (TL;DR)

This is the most genuinely *engineered* market-intelligence product I have reviewed at Printec — the
scoring is deterministic and traceable to source code, the trust pass snapshots every link, and the
outlooks self-flag their own ungrounded extrapolation. It is materially more trustworthy than a typical
"AI report." But it is **not yet board-certifiable**: the headline €99.3m "pipeline" is a band-multiplied
constant masquerading as a bottom-up euro estimate, the LLM-written competition brief asserts a *future*
event (the 30 June Brink's/Atleos vote) as already-passed fact, the forecasting track record is literally
unmeasured (0/174 resolved), and there is no data-quality SLA, no agent-failure alarm, and no single owner
of record. Fix the temporal-honesty defect and label the sizing, and I can certify it for decision-support;
not for committed financial reporting.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 7 | Deterministic, code-traceable scoring + real link-snapshotting; undermined by an LLM brief stating a future vote as past. |
| Completeness | 5 | Strong outside-in coverage, but no lineage/SLA/audit log, no agent-health monitor, no expected-value rollup. |
| Clarity | 6 | Evidence trail and `cite_ungrounded` are exemplary; 8 dense tabs and an unexplained €99.3m number hurt signal-to-noise. |
| Insightfulness | 7 | `cite_ungrounded` and the dual strength/EV ranking surface real epistemic structure most tools hide. |
| Short-term growth | 6 | Triangulated, dated, actionable signals (PrivatBank 800-unit) — but sizing I can't defend and no CRM closed loop. |
| Long-term growth | 5 | Futurist arc is coherent; structural cash/ATM bias + unproven forecasting limit it as a 2–5yr planning base. |
| **Overall** | **6** | A trustworthy *engine* wrapped around an over-confident *presentation*; certifiable for support, not for the board's bottom line. |

## What is genuinely good

- **The scoring is not a black box — it is code I can audit.** `ingest.py:score_signal` is a transparent
  weighting: `confidence_weight + min(agents,3)·0.4 + likelihood_bonus`. `score_ev` is
  `size × win × confidence` with published weight tables (`SIZE_W`, `WIN_W`). The PrivatBank signal's
  `strength: 4.8` and `ev_score: 36` are *reproducible from the row*. The build docstring's claim — "the
  dashboard never displays a number that isn't traceable to a source row" — is substantially true for
  strength/EV. That is rare and it is the single best thing here.
- **The trust pass is real, not decorative.** `verify.py` re-fetches every cited URL, records HTTP status,
  and writes a content-hashed point-in-time snapshot so a dead link still opens its capture. The
  provenance block on each signal (`reachable`, `status`, per-source `code`/`snapshot`) is populated from
  this. 1,059/1,253 reachable with the failures *counted and shown* is honest engineering.
- **`cite_ungrounded` is the most intellectually honest field I have seen in an LLM product.** 4 of 15
  Outlook cards carry it, and the content is substantive — e.g. outlook 0 flags that the "three war years"
  fleet-stability framing comes from the deterministic baseline, not the cited A4 statistics doc, which
  "gives only the point-in-time ~15.7k Q1-2026 figure." That is a model voluntarily marking its own
  weakest claim. It earns trust.
- **Access control is better than the briefing states.** The briefing says "the underlying evidence is
  public." The code refutes that: `api/data.js` and `api/evidence.js` read from a **private** Blob
  (`access: 'private'`), and `middleware.js` gates the entire site — data and evidence endpoints included.
  Upload auth uses `timingSafeEqual` against `UPLOAD_SECRET`. The competitive-intel exposure the briefing
  worried about is largely closed at the infrastructure layer.
- **Single-writer publish with archival integrity.** `api/upload.js` writes a dated `archive/<week>.json`
  *and* the latest pointer *and* a manifest, validates `signals[]` + `week`, and degrades gracefully if
  the manifest write fails. History is genuinely immutable per week.

## What is missing or weak

- **The €99.3m "pipeline total" is a band-to-constant lookup, not an estimate.** `ingest.py` sets
  `pot_value = {XL:7.5, L:3.0, M:0.6, S:0.1}[size_band]`. Every XL deal is booked at exactly €7.5m
  regardless of reality. The engine's *own* Outlook describes the PrivatBank lot as "EUR 10-20m" — yet it
  contributes €7.5m to the headline. So €99.3m is a deliberately conservative mechanical floor. That is a
  *defensible* choice, but the Overview tab presents it as a euro pipeline figure with no "indicative band
  proxy, not a forecast" label. I will be asked "is that real money?" and today the honest answer is "no,
  it's 11 XL deals × €7.5m." That gap between what the number *is* and what it *looks like* is my single
  biggest certification blocker.
- **A future event asserted as past, by the LLM, with no qualifier.** `competition_brief` (generated
  2026-06-25) reads: *"both shareholder votes passed on 30 June."* The vote was *scheduled* for 30 June;
  as of generation and as of today (29 June) it had not occurred. My web check confirms the deal terms
  ($6.6bn, $30 cash + 0.1574 Brink's shares, Q1-2027 close target) but also confirms the **30 June vote
  was prospective**. This is exactly the hallucination class this seat exists to catch: a generated
  narrative converting a calendar item into a completed fact. The deterministic layer would never do this;
  the LLM brief is ungoverned by the same discipline as the signals.
- **No forecasting track record — confidence is asserted, never tested.** `forecast_accuracy` =
  `{total:174, resolved:0, mape:null}`. 14 of 15 Outlooks are labelled "High" confidence. Until even a
  handful resolve, "High" is a vibe, not a calibrated probability. The dual-ranking discipline elsewhere
  makes this omission more glaring.
- **No data-quality SLA, lineage log, or agent-health monitor.** `run_weekly.py` runs every `fetch_*`
  step *best-effort* — "if a source is unreachable, the cached file is reused." That means a feed can die
  and the dashboard silently serves stale data with no flag. There is no per-agent freshness stamp on the
  face of the product ("Agent 6 last succeeded: …"), no alert when reachability drops below a threshold,
  no run-success ledger. If an agent silently fails, *no one finds out from this product.*
- **Verification disables TLS validation.** `verify.py` sets `ctx.verify_mode = CERT_NONE`. The comment
  ("reachability audit, not a transaction") is reasonable, but "reachable" then doesn't certify the source
  is authentic/un-tampered. For a provenance system that is the point, that is a quiet integrity gap.
- **Key-person / pipeline fragility.** The whole chain is a chain of `subprocess.run` calls with two
  env-var secrets and a manually-updated `master-signal-table.md` as the human input. There is no
  redundancy, no second operator, no documented runbook surfaced here. This is a one-person product.

## What I cannot decide from this today

- **Whether €99.3m is worth pursuing as a portfolio.** No expected-value rollup (Σ value × win-prob) is
  shown on the face — `ev_score` exists per signal but the headline is undiscounted band-sums. I can't
  rank by risk-adjusted return.
- **Whether we are winning or losing.** The dashboard is purely outside-in. It does not ingest Printec
  bookings, backlog, or win/loss, so I cannot reconcile "29 signals / €99.3m" against our actual pipeline.
  The 0–6 pressure matrix tells me *intensity*, not *our* position.
- **Whether the data is fresh enough to act this week.** With best-effort caching and no agent-success
  ledger, I cannot tell whether last night's run actually reached the tender portals or quietly reused a
  three-week-old cache.
- **Whether I can quote any euro figure to the board.** Until sizing is labelled and the temporal defect
  is fixed, no.

## Domain reality-check

- **Brink's/NCR Atleos: terms right, timing wrong.** Web sources (investor.ncratleos.com; Seeking Alpha
  "June 30 Vote and Performance Update"; TipRanks supplemental-disclosures coverage) confirm the ~$6.6bn
  deal, the $30.00 cash + 0.1574 share consideration (~$50.40 implied), the ~78/22 post-close split, the
  10–11 June stockholder suits, and a **30 June 2026 vote** with a **Q1 2027 close target**. The dashboard
  gets the substance right and the *tense* wrong — it reports the vote as passed. That is a self-inflicted
  credibility wound on its own headline competition story.
- **Provenance honesty checks out.** The 157 HTTP-errors / 37 unreachable are counted in `provenance` and
  reflected per-signal — the product does not hide its own link rot. Good.
- **`forecast_coverage` is honest about projectability.** It correctly flags 2-point series as
  `projectable:false` rather than extrapolating from two dots. That is the right instinct; it just needs to
  be paired with an actual back-test once horizons mature.

## My recommendations

**Now (this sprint):**
1. **Add a governance pass over LLM-generated prose** (`competition_brief`, outlook `rationale`). Effort:
   medium. Impact: high. A deterministic check — any future-dated event ("vote", deadline) referenced in
   past tense must be flagged or rewritten — would have caught the 30 June error. *Unlocks:* I can trust
   the narrative tabs, not just the signal rows.
2. **Relabel every euro figure.** Effort: low. Impact: high. Tag `pot_value`/the €99.3m total as
   "indicative size-band proxy (XL≈€7.5m … M≈€0.6m), not a forecast or pipeline value." *Unlocks:* I can
   put the number on a slide without misleading the board.
3. **Surface a per-agent freshness/success stamp on Overview.** Effort: low (the data exists in the run).
   Impact: high. *Unlocks:* I can tell at a glance whether to trust this week's data or treat it as stale.

**Next (next quarter):**
4. **Stand up a data-quality SLA + run ledger + alerting.** Effort: medium. Impact: high. Threshold alarms
   on reachability (<85%), zero-new-signals, agent-failure. *Unlocks:* silent-failure protection; the
   first half of an audit story.
5. **Ship an expected-value rollup** (Σ ev / Σ value×win-prob) as the Overview headline beside the raw
   band-sum. Effort: low (logic already in `score_ev`). Impact: medium. *Unlocks:* risk-adjusted
   prioritisation.
6. **Re-enable TLS verification in `verify.py`** (fall back to permissive only on cert failure, and *flag*
   it). Effort: low. Impact: medium. *Unlocks:* provenance that certifies authenticity, not just reachability.

**Later (this year):**
7. **Begin resolving forecasts and publish MAPE.** Effort: medium, ongoing. Impact: high long-term.
   *Unlocks:* calibrated confidence labels — the difference between "support tool" and "trusted forecaster."
8. **Integrate Printec's own bookings/win-loss** for an inside-out reconciliation. Effort: high. Impact:
   high. *Unlocks:* the one view I actually run the business from — market signal vs our reality.
9. **Document a runbook + name an accountable owner of record.** Effort: low. Impact: high for resilience.
   *Unlocks:* removing the single-person bus factor and completing the audit/lineage story.
