# Chief Commercial Officer / Chief Revenue Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own the number. My test is brutally simple: can a regional sales lead and a field rep open this on Monday
and walk into a bank with a *plan* — the right account, the right trigger, the incumbent to displace, the
named buyer to call, the next concrete step, and a battlecard against whoever is in the seat (Mellon, Euronet,
Payten/Asseco, NCR-Atleos/Brink's, Diebold, Hyosung)? Or is it a beautifully sourced analyst feed that tells
me what's happening but not what *I* should do about it? I also need to manage pipeline: coverage vs target,
expected value, where we are being locked out, and where a gap just opened that we should swarm.

## Verdict (TL;DR)

This is the best *market-trigger* layer I have seen for our footprint — the 26 account targets are real, dated,
incumbent-aware opportunities, and the `competition_brief` is genuinely decision-grade (I web-verified its three
headline claims and they are exact). But it is a battlecard *input*, not a battlecard *system*. It tells a rep
*which door* and *why now*; it does not tell them *who to call by name*, *how to beat the named competitor in
that specific deal*, or *what's already in our pipeline against it*. The euro sizing is a band placeholder, not
a forecast, and there is zero CRM/win-loss linkage. Net: a superb top-of-funnel radar that I would deploy
tomorrow, sitting roughly halfway to the sales-ready battlecard tool the briefing implies it is.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 7 | Trigger-level evidence is rigorous and triangulated; competitive facts verified accurate against primary sources. |
| Completeness | 5 | No named buyers, no battlecards, no pipeline-coverage view, no CRM/win-loss loop — the back half of the funnel is absent. |
| Clarity | 6 | "Accounts & timing" reads well per-card, but 26 targets with no swarm/locked-out triage and band-derived values blur priority. |
| Insightfulness | 7 | The EV re-rank, the Cashflex-owned-fleet framing, and the consolidation thesis surface non-obvious plays a rep wouldn't infer. |
| Short-term growth | 7 | Strong: dated triggers + follow-ups give a rep a quarter's worth of "why now" calls; held back by no owner/contact layer. |
| Long-term growth | 6 | The threat targets (Mellon/Euronet/Payten, Brink's-Atleos) frame structural positioning, but no scenario tied to our own capacity/share. |
| **Overall** | **6.5** | A best-in-class opportunity radar that stops short of a sales-execution system. |

## What is genuinely good

**The account targets are real opportunities, not market commentary** (Accounts & timing). I resolved all 26
`account_targets` against the signal table — every one matched. Take PrivatBank (`privatbank-atm-fleet-renewal-800-unit-2026-lot`):
it names the size (800-unit 2026 follow-on after 1,200 in 2025), our position (verified *sole supplier* of 1,140
NCR SelfServ recyclers, ~€19.6m signed 16/01/2025), the trigger (board member Musienko's public confirmation),
and a follow-up a rep can act on today — *"Register/monitor tender.privatbank.ua + Prozorro buyer 14360570 weekly
for the 800-unit notice; brief NCR Atleos incumbent-defence."* That is a usable play. Banca Transilvania is
similar quality: it cites the actual RON 1,017.4m 2026 capex (+20.6%), the named cash-processing-centre /
hardware-retail-cards / security capex lines, and the live "Enterprise Architect – Cards Domain" hiring as a
6–12-month vendor-selection leading indicator. That hiring-as-buying-signal triangulation (A1 disclosures + A5
jobs) is exactly the kind of edge a rep cannot get from a press feed.

**The `competition_brief` is decision-grade and accurate.** I pressure-tested it externally. The Brink's/Atleos
$6.6bn, the 30 June 2026 shareholder votes, and the Q1 2027 targeted close all match the primary filings; the
Euronet/CrediaBank claim ($22bn/yr, Q3 2026 close, ATM-network fold-in) matches Euronet's own release exactly.
The brief correctly frames the *commercial* implication — our key ATM partner is becoming an end-to-end
hardware+CIT+managed-services rival via Brink's Hellas — which is the single most important thing my Greek and
SEE teams need to internalise this quarter.

**The EV re-ranking earns its keep** (`account_targets_ev`). The raw list leads with PrivatBank/Hungary/CEC; the
EV-weighted list promotes Piraeus/Cashflex, Alpha Bank, and Bank of Cyprus — the high-win, Printec-adjacent Greek
plays. That is the difference between "biggest" and "best risk-adjusted," and it is the view I'd put in front of
a sales lead first.

**The pressure matrix is a usable lock-out map** (`matrix`, 16 markets × 12 competitors, 0–6). Greece reads
Mellon 6 / Euronet 5 / Hyosung 5 / NCR 4 / Brink's 4 — i.e. we are in a knife-fight at home. Cyprus is near-empty.
That instantly tells a rep where to *defend* vs where to *hunt* whitespace.

## What is missing or weak

**No named buyer anywhere.** Across all 29 signals there are exactly three decision-maker references ("Head of
Payment", "CTO", "COO") and not one *named* individual. A rep cannot "approach now" without a person. This is the
single biggest gap between "account target" and "account *plan*."

**There is no battlecard.** The 156-name watchlist and the `competitor` records carry `name/role/threat/latest/
products` but no `how_to_win`, no positioning, no "where they're weak," no reference-win proof points. So when the
matrix says "Mellon = 6 in Greece," the rep learns *that* they'll meet Mellon, not *how to beat* Mellon. The
briefing frames this as a "battlecard system" — it is not yet one. It's a threat register.

**The euro sizing is a band placeholder masquerading as a forecast.** Every `pot_value` across the 26 targets
collapses to four numbers — XL=€7.5m (×10), L=€3m (×10), M=€0.6m (×2), Unscoped=€0 (×4). The €99.3m "pipeline"
is `band × count`, not bottom-up deal sizing. I can't run capacity or set a quota off it, and putting a precise
"€7.5m" on a card a rep will quote to a partner is a credibility risk.

**No pipeline coverage and no CRM linkage.** I cannot see target vs actual pipeline, how many of these 26 we are
already *in*, or our win/loss history against Mellon/Euronet. `win_prob` is a 3-bucket label (4 High / 18 Medium /
2 Low / 5 blank) asserted from incumbency, not calibrated against any outcome data — and forecast_accuracy shows
0 of 174 resolved, MAPE null, so even the engine admits it's unproven.

## What I cannot decide from this today

- **Who do I assign each target to, and is anyone already on it?** No owner, no status, no closed loop.
- **What's my realistic pipeline this quarter?** Band-math €99.3m is not a number I can commit to the board.
- **How do I win the contested ones?** Greece is Mellon-6/Euronet-5; I have the trigger but no play to displace them.
- **Where exactly are we being locked out vs where did a gap just open?** The matrix shows intensity, but there's
  no "newly-opened gap" flag (e.g. CrediaBank's ATMs going to Euronet *closes* a door — is that flagged as a loss-risk?).
- **Which targets touch our actual delivery capacity?** Three XL ATM lots landing together (PrivatBank, CEC,
  Banca Transilvania) may exceed our recycler/field capacity — nothing here tells me.

## Domain reality-check

I verified the two load-bearing competitive claims against primary sources and both are exact: Brink's/NCR Atleos
at $6.6bn with 30 June 2026 votes and Q1 2027 close ([NCR Atleos IR](https://investor.ncratleos.com/news-events/press-releases/detail/174/brinks-to-acquire-ncr-atleos-for-6-6-billion-creating-leading-financial-technology-infrastructure-company)),
and Euronet/CrediaBank at >$22bn/yr, >240k merchants, Q3 2026 close ([Euronet IR](https://ir.euronetworldwide.com/news-releases/news-release-details/euronet-signs-strategic-partnership-agreement-acquire-merchant)).
Crucially, the Euronet release states Euronet will *fully manage CrediaBank's in-branch and off-site ATMs* — that
is a direct lock-out of an ATM-managed-services opportunity in our home market, and the dashboard treats Euronet
mainly as a "threat" target (Unscoped, €0) rather than flagging the specific defended-account loss. That's the
kind of commercial nuance a CRO needs surfaced as an alert, not buried in a brief. The dashboard's competitive
read is accurate; its translation of that read into "so which of *our* accounts is now at risk" is underdeveloped.

## My recommendations

**NOW (low effort, high impact)**
1. **Add a contact/owner layer to each account target** — even a free-text "buyer role + named individual if known
   + Printec owner + status (not-started/in-pursuit/bidding/won/lost)." Unlocks: assigning the 26 targets and
   running them as a pipeline instead of a reading list. *Effort: low. Impact: high.*
2. **Replace single-point `pot_value` with a range + an explicit "band estimate — not quoted" label.** Unlocks:
   I can use it for triage without a rep mis-quoting €7.5m to a customer. *Effort: low. Impact: medium.*
3. **Add a "gap just opened / door just closed" flag** driven off the competition_brief (e.g. CrediaBank-ATMs →
   Euronet = defended-account-at-risk). Unlocks: same-week defensive swarm. *Effort: low. Impact: high.*

**NEXT (medium effort, high impact)**
4. **Build a real battlecard per top competitor** (Mellon, Euronet, Payten/Asseco, NCR-Atleos/Brink's, Hyosung):
   where they win, where they're weak, our 3 proof-points, the counter-pitch. Tie it to the matrix cell. Unlocks:
   a rep can actually contest the Greece-6 accounts. *Effort: medium. Impact: high.*
5. **Pipeline-coverage view: 26 targets vs which we're in, with EV roll-up (value × calibrated win_prob).** Unlocks:
   a board-quotable quarterly number. *Effort: medium. Impact: high.*

**LATER (higher effort)**
6. **CRM/win-loss ingestion** to calibrate `win_prob` against real outcomes and close the loop (did we act, did we
   win). Unlocks: trustworthy forecasting and a learning system instead of asserted "High." *Effort: high. Impact: high.*
7. **Capacity overlay** — flag when concurrent XL lots exceed delivery capacity. *Effort: high. Impact: medium.*
