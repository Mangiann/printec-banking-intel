# Chief Risk & Compliance Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own two things: (1) the accuracy and completeness of how we read the EU/CEE regulatory stack that drives our
clients' spend and our own obligations, and (2) Printec's enterprise risk register — supplier concentration,
geopolitical/Ukraine exposure, FX, customer concentration, counterparty risk, and the *analytical* risk of betting
decisions on a model's confidence labels. I need this tool to (a) give me a regulatory calendar I can trust without
re-checking every date, (b) frame regulation as both opportunity *and* obligation/liability, and (c) tell me where
*Printec itself* is exposed — not only where the market is moving.

## Verdict (TL;DR)

The regulatory layer is genuinely strong: I web-verified the load-bearing dates (Instant Payments non-euro
receive 09-Jan-2027 / send 09-Jul-2027, AI Act high-risk deferral to Dec-2027/Aug-2028, digital euro "issuance 2029
contingent on 2026 legislation") and the dashboard gets them right, including the hard CEE-specific nuances most tools
botch. The futures **threats** panel is the most risk-literate content in the product — "DORA accountability cannot
be outsourced," CTPP designation exposure, GDPR-vs-AML-utility failure, "dates slip — timing not existence is the
risk." But the dashboard has a structural blind spot that is squarely my problem: it is almost entirely *outside-in
market opportunity* and barely addresses **Printec's own enterprise risk**. "Single-vendor" and "customer
concentration" and "FX risk" return literally zero hits in the data; the Atleos→Brink's event is framed as a
competitive/market story, not as *our* key-supplier dependency. And 14 of 15 outlooks are labelled "High" confidence
against a forecast track record of **0 of 174 resolved, MAPE null** — the self-flagging mitigates this, but the
headline label still over-claims.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 7 | Dates I spot-checked are accurate and well-sourced; forecast objects carry method/r², but "High" confidence labels outrun an unproven track record. |
| Completeness | 6 | Strong regulatory coverage, but DORA and PSD3/PSR are absent as *dated* items, and Printec's own risk register (supplier/customer/FX/Ukraine) is essentially missing. |
| Clarity | 7 | The deadline tracker with `forces`, geos, products and a countdown is genuinely decision-grade; no single "obligation vs opportunity" lens though. |
| Insightfulness | 7 | Futures `threats` surface non-obvious liability truths (CTPP, GDPR-vs-AML, date-slip); the rest mostly restates known mandates. |
| Short-term growth | 6 | The buying-window framing of deadlines is useful, but I cannot price *our* exposure to the Atleos→Brink's transition that hits in this same 0–12 mth window. |
| Long-term growth | 7 | "Sell managed readiness, not date-timed projects" and the 2030 governance-layer thesis are the right strategic risk posture. |
| **Overall** | **6.5** | Trustworthy regulatory radar and a sharp market-risk panel, undermined by a missing own-enterprise-risk layer and over-confident forecast labels. |

## What is genuinely good

- **Accounts & timing → regulatory deadline tracker (23 dated items).** This is the strongest thing here for my seat.
  Each item carries `forces` (why it drives bank spend), `geography`/`geo_names`, `products`, an EUR-Lex/ECB/regulator
  `url`, and a `days_until` countdown bucketed now/next/later. I verified the IPR rows against the regulation: the
  RECEIVE obligation 09-Jan-2027 and SEND 09-Jul-2027 for non-euro CEE (CZ/HU/RO) are *correct*, and the "from EUR
  accounts" qualifier on the send row is a precise nuance — IPR covers euro-denominated transfers, so a non-euro PSP's
  obligation attaches to its euro accounts. Most market trackers get this wrong; this one didn't.
- **Non-euro CEE handled properly.** Bulgaria's separate IPR-compliance row (01-Jan-2027, tied to euro entry), the
  Western-Balkans TIPS-clone go-live, Slovakia eKasa, Hungary Act XVIII — these are footprint-specific obligations a
  generic EU calendar would omit. The digital-euro item correctly scopes to euro/euro-entrant geos and labels itself
  "Low-confidence, long-fuse."
- **Date-realism discipline.** The digital-euro row says "potential first issuance (target, contingent on 2026
  legislation)" and the AI Act is correctly deferred (Dec-2027 / Aug-2028). The futures threat "Regulatory dates slip
  — timing, not existence, is the live risk" is exactly the caveat a risk officer wants stated out loud, and it's
  warranted: I confirmed the AI Act omnibus deferral and the EUDI 80%-target slip toward ~2032.
- **Futures → threats panel.** "DORA / PCI / AMLR accountability cannot be outsourced" with the 18-Nov-2025 CTPP
  designation cited, and "GDPR / data-localisation can sink AML data-sharing utilities" (TMNL wind-down). This is the
  only place the tool consistently frames regulation as *liability*, not just spend — and it does it well.
- **Self-flagging of ungrounded extrapolation.** Every outlook carries `cite_ungrounded` — e.g. the PrivatBank card
  openly states its "three war years" framing is from the deterministic baseline, not the cited statistics doc. That
  is real evidence discipline and it materially raises my trust.

## What is missing or weak

- **DORA and PSD3/PSR are not dated items in the tracker.** DORA appears 103× in text and PSD3/PSR 42×/34×, but
  neither has a row in the 23-item deadline tracker. DORA's TLPT cycle and ongoing CTPP oversight are live; PSD3/PSR is
  in trilogue with adoption expected in 2026 and a ~18-month application runway. For a resilience/payments-regulation
  radar these two are headline mandates — their absence from the *dated* calendar is a coverage hole.
- **Printec's own enterprise risk is absent.** `single-vendor`, `customer concentration`, `fx risk` = 0 hits;
  `concentration` appears twice (both about the *market*, not us); `counterparty` once (a SWIFT data-quality note).
  The Atleos→Brink's deal — *our key ATM hardware supplier being absorbed into a CIT rival that already runs ATM
  managed services in Greece via Brink's Hellas* — is covered 209× (Atleos) / 133× (Brink's) but **only as a
  competitive market story**. Nowhere does the tool frame it as *Printec's single-supplier dependency and a
  near-term sourcing/continuity risk*. That is the single biggest risk item in our remit this quarter and the
  dashboard treats it as someone else's news.
- **Confidence labels over-claim.** 14/15 outlooks = "High" confidence while `forecast_accuracy` = {total 174,
  resolved 0, mape null}. The forecast objects do carry `fit_quality`, `r2` (0.977 on the Romania POS sample),
  `method` and `inflection` — so the *quantitative* projections are honest. But an LLM-generated card asserting "High"
  with zero resolved back-tests is optimism/anchoring bias wearing a lab coat. The label should be capped or renamed
  (e.g. "model fit: high / track record: unproven") until MAPE exists.
- **No obligation-vs-opportunity toggle.** Every deadline's `forces` is written as a *spend driver* ("must remediate",
  "must be compliant") — which doubles as the bank's *liability*, but the framing leans sell-side. I cannot filter
  "which of these create a compliance liability for *us* as a processor/managed-services provider" (e.g. our own DORA
  CTPP-adjacency, our AMLR data-handling, our EAA accessibility obligations on devices we operate).
- **No quantification of own-risk exposure.** There is a €99.3m pipeline number but no FX exposure by currency
  (RON/HUF/CZK/RSD/UAH), no revenue-concentration-by-client figure, no Ukraine operational-exposure line.

## What I cannot decide from this today

1. **The Atleos→Brink's mitigation decision.** Should we accelerate a second-source ATM hardware relationship
   (Hyosung/Diebold), renegotiate Atleos terms before close (~Q1 2027), or hedge via KAL/multivendor software? The
   dashboard tells me the deal is happening and what it means *competitively* — it gives me nothing on *our* contract
   exposure, spares/parts continuity, or pricing risk. I'd have to build that off-platform.
2. **How much regulatory-driven revenue is genuinely de-risked vs date-slip-exposed.** The threats panel rightly warns
   dates slip, but no outlook discounts its `projected` value for that risk. I can't see expected value = value ×
   win-prob × date-confidence anywhere.
3. **Our own compliance obligations.** As an operator of ATMs/POS/managed rails across the footprint, EAA-2030, DORA
   CTPP-adjacency and AMLR data-handling are *our* obligations, not just our clients'. The tool never separates
   "Printec sells this" from "Printec must comply with this."

## Domain reality-check

- **IPR dates (verified correct):** non-euro receive 09-Jan-2027, send 09-Jul-2027 — matches Osborne Clarke / Britepayments / Worldline. The dashboard's CZ/HU/RO scoping and "from EUR accounts" nuance are accurate. (It omits the non-bank-PSP 09-Apr-2027 date — minor, our clients are banks.)
- **AI Act (verified):** high-risk obligations deferred to 02-Dec-2027 (Annex III) / 02-Aug-2028 (Annex I) under the Digital Omnibus — the dashboard's threat note is right.
- **Digital euro (verified):** ECB target issuance 2029 contingent on 2026 legislation, pilot from mid-2027 — the deadline's "contingent / low-confidence / long-fuse" framing matches the ECB closing report.
- **Gap confirmed:** DORA and PSD3/PSR are live, material, and not in the dated tracker.

Sources: [Osborne Clarke — IPR obligations/timelines](https://www.osborneclarke.com/insights/what-are-key-obligations-and-timelines-eu-instant-payments-regulation); [Worldline — IPR for non-eurozone](https://worldline.com/en/home/main-navigation/resources/blogs/2025/instant-payments-regulation-a-key-development-for-non-eurozone-eu-countries); [Gibson Dunn — AI Act omnibus deferral](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/); [ECB — digital euro next phase](https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr251030~8c5b5beef0.en.html); [Morgan Lewis — DORA CTPP designations](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2025/11/dora-eu-regulators-announce-list-of-critical-ict-third-party-providers).

## My recommendations

**Now (low effort, high impact):**
- **Add a Printec enterprise-risk panel.** Five rows: supplier concentration (Atleos→Brink's), Ukraine operational
  exposure, FX by currency, top-client revenue concentration, counterparty. *Unlocks:* the board-level risk
  conversation the tool currently can't support. Effort low (one data block + one tab section); impact high.
- **Reframe the Atleos→Brink's item as a dual entry** — keep the competitive read, add a "supplier-dependency / sourcing
  continuity" risk read with a mitigation prompt. *Unlocks:* the second-source decision. Effort low; impact high.

**Next (medium effort, high impact):**
- **Split confidence into "model fit" vs "track record."** Stop printing bare "High" while MAPE is null; show both.
  *Unlocks:* trustworthy use of outlook `projected` values in commercial planning. Effort medium; impact high.
- **Add DORA and PSD3/PSR as dated tracker items** with their real milestones and a date-confidence flag.
  *Unlocks:* a complete resilience/payments calendar. Effort medium; impact medium-high.

**Later (medium effort, medium impact):**
- **Add an obligation-vs-opportunity toggle** to the deadline tracker, separating client spend-drivers from Printec's
  *own* compliance obligations (EAA, DORA CTPP-adjacency, AMLR data-handling). *Unlocks:* our own-compliance roadmap.
- **Add a date-slip discount to outlook projected values** (value × win-prob × date-confidence) so the €99.3m pipeline
  reads as risk-adjusted expected value. *Unlocks:* defensible forecasting to the board.
