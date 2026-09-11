# Chief Technology / Innovation Officer — review of the Printec Banking Intelligence Dashboard

## Who I am & what I need this dashboard to do for me

I own the product & technology roadmap, the build/buy/partner calls, the R&D bets, and the partner
stack. I do not need another market-size deck. I need an instrument that tells me **what to build, with
whom, and by when** — and that maps Printec's actual portfolio (an integrator/managed-services book that
is today heavily ATM/cash and branch) onto where the technology and the regulated demand are going. The
two tabs that live in my seat are **Future outlook (2–5 yr)** — futures cards, the money/competition/
threats board, and the structured `bottom_line` (thesis, picture, gems, 2030 endstate) — and the
**per-product 6–12-month product-direction outlooks** (`product-outlooks.js`). I judge them on technical
soundness, on whether the "gems" are buildable openings or essays, and on whether the engine has correctly
diagnosed that our growth spine is software/platform/data, not hardware.

## Verdict (TL;DR)

This is the strongest part of the dashboard and, frankly, better strategy work than most of what I see
from paid analyst houses. The Future tab has a genuine thesis ("value migrates to operating the regulated
rails — identity, real-time data, fraud, resilience, governance — as managed services"), and the five
gems are real, legally-anchored, buyable wedges, not essays — each names the statute, the deadline, the
incumbent competitors, and *why Printec specifically* (the neutral-operator / integrator role) has a
right to play. It is also unusually honest: it flags that the gem markets are crowded, that >40% of
agentic projects will be cancelled, and that "timing, not existence, is the live risk." The hard gap for
me is that it stops one step short of a roadmap: there is no build/buy/partner verdict, no capability-gap
assessment against our current stack, no sequencing or investment envelope, and no named-partner
shortlist. It tells me where to point, brilliantly; it does not yet tell me what to commission Monday.

## Scorecard

| Dimension | Score /10 | One-line justification |
|---|---|---|
| Quality | 8 | Dense, citation-linked, externally verifiable (I checked EUDI Art. 5b/5f dates, agentic-AI consensus, A2A sizing — all hold); self-flags its own weak spots. |
| Completeness | 7 | Covers 11 futures domains + 12 product lines; but no capability-gap map, no build/buy/partner layer, A2A under-developed as a standalone play. |
| Clarity | 7 | The `bottom_line` (thesis → picture → gems → 2030 strip) is excellent IA; but 11 futures cards + 12 product outlooks of ~2.5k chars each is a heavy read for a roadmap decision. |
| Insightfulness | 9 | The gems are genuinely non-obvious (Art. 75 neutral AML-utility operator, PQC discovery/CBOM, long-tail relying party) and reframe Printec's integrator role as the edge. |
| Short-term growth | 6 | Product-direction outlooks name real H2-2026/2027 catalysts (IPR VoP, Bulgaria euro, Hungary Act XVIII), but no expected-value or "commission this now" layer. |
| Long-term growth | 8 | This is the tab's home turf — it correctly identifies the 2027-2030 perimeters and that services/data, not hardware, are the spine. |
| **Overall** | **7.5** | Best-in-class diagnosis of *where* the market goes; one step short of a *what-to-build* roadmap. |

## What is genuinely good

- **The thesis is correct and load-bearing.** `futures_board.bottom_line.thesis` states the durable money
  is "operating the shared, regulated rails... as managed services across many markets and a buyer base
  far wider than banks." That is exactly the right read for an integrator — it tells me our moat is the
  neutral-operator / orchestration role, not owning a horizontal product. It reframes our existing
  shared-ATM-network competence as transferable to AML utilities and identity-acceptance hubs.

- **The gems are buildable, not rhetorical.** Gem 3 (Art. 75 AML data-sharing utility, applicable
  10 Jul 2027) is the standout: it correctly diagnoses that TMNL failed on *centralisation*, not
  collaboration, names the analytics incumbents (Lucinity, Fenergo, Wodan, Consilient), and carves out
  the slot Printec can actually own — the *neutral operator* of the shared infrastructure, mirroring our
  ATM-pooling role. Gem 4 (PQC: build the CBOM / cryptographic bill-of-materials as the near-term billable
  wedge, then the crypto-agile HSM refresh) is a clean, sequenced, hardware-plus-services motion sold to a
  *new buyer* (CISO/security-architecture). These are commissionable.

- **It honestly differentiates hardware from spine.** Despite the well-known weekly ATM-signal bias, the
  Future tab's money board explicitly tags "AI in banking (software & services), >30% CAGR — the largest
  new pool" as up, and `money[10]` cash/self-service as a *managed-services annuity, not the growth spine*.
  The product-direction layer reinforces this: the software lines (`compliance_resilience`,
  `fraud_monitoring`, `payments_instant`) are tagged **strong growth** while `atm_recycling` is only
  **growth**. The `payments_instant` card even self-criticises the weekly score: *"The internal score
  looks conservative against this catalyst density."* That is the engine catching its own ATM bias — good.

- **It is externally accurate.** I spot-checked the EUDI claims (issuance 6 Dec 2026, mandatory
  acceptance/SCA 6 Dec 2027, Art. 5b(10) intermediary-is-a-relying-party, Art. 5f obligation breadth) and
  the agentic-AI framing against current sources — both match the consensus. The "honest hedge" that the
  80% wallet target may slip to ~2032, and the standing threat card "regulatory dates slip — timing, not
  existence, is the live risk," are exactly the caveats a roadmap owner needs.

## What is missing or weak

- **No build/buy/partner layer.** Every gem ends at "this is an opening." None says *build vs. OEM vs.
  partner*. For Gem 1 (long-tail relying-party acceptance) do we build a verifier, white-label Signicat's
  reusable-ID hub, or resell? For Gem 3 do we license a federated-learning/PET stack (Lucinity) and wrap
  it in our operations, or build? This is the single decision the tab exists to inform and it is absent.

- **No capability-gap map against Printec's current stack.** The dashboard maps demand to *product lines*
  but never to *our actual capabilities*. Gem 4's PQC discovery and Gem 3's AML-utility orchestration imply
  skills (cryptographic inventory tooling, PET/secure-enclave ops, model-risk instrumentation for Gem 2's
  AI-Act self-attestation) we likely do not have in-house. I cannot size the R&D/hiring bet without a
  "have / need-to-acquire" column on each gem.

- **A2A / account-to-account is under-sized as a standalone play.** The endstate strip notes "A2A
  offsetting 15-25% of card growth," but external consensus is more aggressive (ECB: ~60% of e-commerce
  and 20% of face-to-face on instant transfers by 2030; 30-40% of e-commerce A2A). A2A appears only as the
  rail under instant payments + VoP, not as a distinct distribution-disruption opportunity for our
  POS/acquiring book. For a CTO weighing where acquiring economics go, that is a material under-development.

- **Cloud-core vendor dynamics are named but not actioned.** The competition board correctly flags
  Thought Machine / Mambu / Tuum / 10x winning greenfield, and `core_digital` is framed as a "decade-long
  coexistence programme." Right diagnosis — but no partner recommendation. As an integrator the obvious
  move is a SaaS-core *delivery partnership*; the tab does not surface which vendor to align with in CEE/SEE.

- **No sequencing or investment envelope.** Five gems + 11 futures + 12 product directions, all "go." With
  finite R&D budget I need a ranked 2-3 bet shortlist with rough cost/time-to-revenue. The tab gives me a
  menu, not a portfolio.

## What I cannot decide from this today

1. **Which 2-3 gems to fund.** All five are credible; I have no expected-value, no effort estimate, no
   capability-gap to rank them. PQC discovery (Gem 4) and the AML neutral-operator (Gem 3) *look* like the
   best fit-to-strength, but the tab does not assert that or cost it.
2. **Build vs. buy vs. partner on any of them.** No verdict, so no procurement or hiring can start.
3. **Which cloud-core vendor to partner with** for the coexistence-integration play in our footprint.
4. **Whether to make an R&D bet on A2A/Pay-by-Bank** as our acquiring book's hedge against card economics.
5. **What to stop doing.** The thesis says cash/ATM is the annuity to optimise, never the spine — but
   there is no guidance on R&D *reallocation* away from hardware toward the spine. A roadmap is also a
   list of things you defund.

## Domain reality-check

- **EUDI / eIDAS-2 (Gems 1):** Verified. Acceptance/SCA obligation 6 Dec 2027, Art. 5b(10) intermediary
  construct, and the Art. 5f breadth beyond the named sectors all match current sources
  ([identyum](https://identyum.com/eudi-wallet-eidas-2-obliged-entities-2027/),
  [Lissi](https://www.lissi.id/blog/the-eudi-wallet-intermediary-a-guide-to-the-eidas-2-0-ecosystems-most-critical-role)).
  The long-tail-obligated-buyer insight is real and, in my experience, genuinely under-served.
- **Agentic AI (futures[3]):** "Copilot to governed operator," value in the assurance layer, >40%
  cancellation — all align with the 2026 consensus (57% of bank execs expect embedded agents in
  risk/compliance/fraud within three years; Gartner's >40% cancellation call —
  [CIO Dive](https://www.ciodive.com/news/banks-agentic-ai-scale-2026/809532/),
  [Accelirate](https://www.accelirate.com/agentic-ai-statistics-2026/)). Correctly sized.
- **A2A (endstate strip):** The dashboard is *conservative* vs. the ECB's 2030 e-commerce/face-to-face
  numbers ([Open Banking Expo](https://www.openbankingexpo.com/news/new-research-finds-european-consumers-mostly-favour-a2a-payments-over-cards/)).
  Defensible, but the opportunity is under-built for our acquiring line.
- **ATM/managed-services shift:** The `atm_recycling` outlook's "chase the value shift (recycling +
  managed services 4.66% CAGR), not raw units" is the right strategic instruction and matches my read of
  the post-Brink's/Atleos market.

Net: where the tab makes factual claims, they hold up. The weakness is not accuracy — it is that the
analysis stops at diagnosis.

## My recommendations

**Now (low effort, high impact — unlocks funding decisions):**
- Add a **build/buy/partner verdict + capability-gap row to each gem** (have / need-to-acquire / named
  candidate partner). Decision unlocked: which 2-3 gems to commission and whether by hiring, OEM, or
  partnership. This is the missing last inch and is mostly synthesis of content already present.
- Add a **ranked bet shortlist** (top 3 gems by fit-to-strength × deadline proximity × revenue-type) with
  a rough time-to-first-revenue. Decision unlocked: R&D portfolio allocation for the next two quarters.

**Next (medium effort, high impact):**
- **Name the cloud-core partner** for the CEE/SEE coexistence play (which of Thought Machine / Mambu /
  Tuum / 10x to align with) and the EUDI-hub / AML-PET vendor candidates per gem. Decision: partner
  pipeline. *Effort: medium (needs vendor-fit research). Impact: high — moves partnerships from "watch" to
  "negotiate."*
- **Promote A2A/Pay-by-Bank to a standalone product-direction outlook** under POS/acquiring, sized against
  the ECB 2030 numbers. Decision: whether to hedge our acquiring book. *Effort: medium. Impact: medium-high.*

**Later (medium effort, strategic):**
- Add an **R&D reallocation view** — what to defund in hardware to fund the spine — so the "annuity, not
  spine" thesis becomes a budget instruction, not a slogan. *Effort: medium. Impact: high long-term.*
- Tie the gems to a **time-to-revenue / TRL track** so I can watch a bet mature from discovery (CBOM, Gem
  4) to scaled managed service. Decision: stage-gate our innovation portfolio.
