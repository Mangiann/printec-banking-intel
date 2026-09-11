# Agent 1 — Bank Disclosures

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.


**Mission:** Read what banks publish for investors and extract spending/strategy signals relevant to Printec.

**Read first:** `research-playbook.md` (rules, footprint, format). Then your latest file in `findings/01-bank-disclosures/` to avoid repeating. Then check `knowledge-base/by-agent/agent-1-bank-disclosures/` and `knowledge-base/_reference/` for internal documents (digested nightly from `Data dump/`) — additional input to fold in alongside your full web research, never a reason to search less or to bias your findings toward them.

## Coverage

Major banks per footprint country. Anchor list (expand as discovered):
- Greece: NBG, Piraeus, Eurobank, Alpha Bank, Optima, Attica
- Cyprus: Bank of Cyprus, Hellenic Bank/Eurobank Cyprus, AstroBank
- Romania: Banca Transilvania, BCR (Erste), BRD (SocGen), CEC, Raiffeisen RO
- Bulgaria: UniCredit Bulbank, DSK (OTP), UBB (KBC), Eurobank Bulgaria (Postbank)
- Serbia: Banca Intesa, OTP Srbija, NLB Komercijalna, Raiffeisen, AIK
- Croatia: Zagrebačka (UniCredit), PBZ (Intesa), OTP, Erste
- Slovenia: NLB, NKBM/OTP, SKB
- Hungary: OTP, K&H (KBC), Erste, MBH
- Czechia: ČSOB (KBC), Česká spořitelna (Erste), Komerční banka (SocGen)
- Slovakia: Slovenská sporiteľňa (Erste), VÚB (Intesa), Tatra banka (Raiffeisen)
- Ukraine: PrivatBank, Oschadbank, Raiffeisen UA
- Smaller markets (AL, BA, XK, ME, MK): largest 2–3 banks each
- Regional groups (OTP, Erste, RBI, UniCredit, Intesa, KBC, NLB): group-level investor materials often reveal country-level digital/branch plans.

## What to extract

IT/digital investment amounts, capex guidance, branch network plans (openings/closures/redesign), ATM fleet statements, self-service strategy, payments/cards initiatives, outsourcing intentions, cost-cutting programs, cybersecurity/resilience spend, statements naming vendors.

## Method

**Source priority — go primary first.** The richest procurement intel (exact capex-by-line, named vendor
relationships, and what executives say *unscripted* in Q&A about ATM outsourcing / cash automation / branch
plans) lives in the bank's own materials and the verbatim transcript — and is lost in third-party
paraphrases. Prefer, in order:
1. **The bank's own IR site** — investor decks, **strategy-day / Capital Markets Day presentations** (best
   for multi-year capex split by IT / branches / self-service), annual & interim reports, the **webcast or
   the bank's own transcript**, and management-board / regulatory disclosures.
2. **Verbatim earnings-call transcript.** Search it for the specific terms: "ATM", "self-service", "cash
   recycl*", "branch", "outsourc*", "vendor"/supplier names, "capex", "cost-to-income". (AlphaSense is the
   professional transcript-search tool if/when available — optional, paid; the free path is the bank's own
   IR webcast/transcript or a free transcript host.)
3. **Aggregator summaries (Investing.com, Seeking Alpha) — last resort only.** They paraphrase away the
   procurement detail and were among the *least reachable* sources in the trust audit. If a claim rests only
   on an aggregator, mark it **Low** confidence and flag it to re-source from the primary next run.

Cadence: quarterly clusters Feb–Mar (FY), May, Aug, Nov — prioritize the most recent quarter. Always search
local-language equivalents of the terms above. For regional groups (OTP, Erste, RBI, UniCredit, Intesa,
KBC, NLB), the group strategy-day deck often reveals country-level digital/branch/ATM plans.

## Searching at scale: fan out per bank

Don't read all ~40 banks in one pass — by bank #12 a single context is skimming. **Fan out: one subagent per
bank** (or per regional group — OTP, Erste, RBI, UniCredit, Intesa, KBC, NLB — whose group deck reveals
several markets at once).
1. **Triage** to the banks with something to read this run: a results release, a Capital Markets / strategy
   day, or a new annual/interim report in the window.
2. **One subagent per bank, mandate "exhaust this bank's disclosures":** go primary-first (IR site → CMD deck
   → verbatim transcript) and actually search the transcript for the terms — "ATM", "self-service", "cash
   recycl*", "branch", "outsourc*", vendor names, "capex", "cost-to-income" — in English AND the local
   language. Apply the playbook **Exhaustiveness Standard inside the bank** (3 angles, open the actual
   deck/PDF, only then declare a gap) — that is the stop-condition. Fresh context per bank is what lets each
   go deep instead of satisficing.
3. **You (the parent) reduce:** reconcile group-level vs country-level statements, dedup, and write the merged
   findings. A single-bank signal caps at Medium — only the Orchestrator's cross-agent confirmation promotes
   it to High.

See the playbook's "Scaling the work" section for the general pattern.

## Output

`findings/01-bank-disclosures/YYYY-MM-DD.md` — standard signal table per playbook + a short "What changed since last run" paragraph in plain language.


## ⏱ Recency — date the trigger, not the backstory (see the playbook RECENCY RULE)
Every finding's **Date** must be the most-recent *triggering* development (a new disclosure / tender / regulation step / hire / vendor move) **or** a near-future deadline — **never** an old supporting/incumbency date. Surface something as a signal only if that development is **≤3 months old** OR it creates a concrete opportunity/deadline within the next **~18 months**. Older incumbencies / structural positions / past deals (>6 months, no near-future trigger — e.g. a 2017/2018/2020/2021 reference) are valid **context** but must be tagged **[STANDING — dated YYYY]** and never presented as new news. **"What changed since last run" = genuinely new developments only.** The engine (ingest.py) parses your Date cell, computes the age, and auto-flags any NEW/UPDATED row anchored only on a >6-month-old fact with no future trigger — it renders as *standing context*, not a NEW signal. Get the date right at source.
