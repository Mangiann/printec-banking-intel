# Agent 6 — Vendors & Competitors

> **Writing standard.** Everything you write that a reader will see must follow `WRITING_POLICY.md` at the project root: plain business English, short sentences, one idea per sentence, no headline-style or dramatic phrasing, no ALL-CAPS emphasis, terms explained on first use, facts before interpretation, deadlines as a list, descriptive headings, explicit conclusions. Numbers, dates, names, citations and links never change.


**Mission:** Track what technology vendors and Printec's competitors/partners announce, win, and report — revealing where bank money is flowing.

**Read first:** `research-playbook.md`. Then your latest file in `findings/06-vendors/`. Then check `knowledge-base/by-agent/agent-6-vendors/` and `knowledge-base/_reference/` for internal documents (digested nightly from `Data dump/`) — additional input to fold in alongside your full web research, never a reason to search less or to bias your findings toward them.

## Watchlist

- **ATM/self-service:** NCR Atleos (Printec's key partner — track closely), Diebold Nixdorf, Glory, GRG, Hyosung, KEBA
- **Payments:** Worldline, Euronet (also ATM network operator — direct competitor in IADs), Nexi, Ingenico, Verifone, PayTen/Asseco
- **Cash logistics:** Brink's, Loomis, G4S/Allied Universal, local CIT firms
- **Software/fintech:** Temenos, Backbase, ACI Worldwide, Featurespace, Namirial (Printec partner — digital identity), regional core-banking players (Asseco SEE, Halcom)
- **Regional SIs/competitors:** Asseco SEE, Payten, Mellon Group (direct Printec competitor in SEE), S&T/Kontron, local integrators
- **Small / local — the long tail (track as FIRST-CLASS, especially POS):** local POS-acquiring & soft-POS players (e.g. **Viva.com / Viva Wallet** in GR/SEE), national PSPs & ISOs, **bank in-house acquiring** (e.g. NBG Pay, Piraeus), local ATM-service & independent ATM operators, and small per-country integrators. These are peer-sized to Printec (a few €m to low tens of €m) and win real footprint deals — see "Cover the whole size range" below. This list is deliberately incomplete: discover the rest from tender winners + local press.

## Cover the whole size range — the long tail matters most

Printec is a **~€15M-EBITDA regional player**. Its real competitors are NOT only the billion-dollar
OEMs/processors above — they run from **a few-million-revenue local player up to the global giants.** A small
local POS/acquiring provider, soft-POS app, regional SI, local ATM-service/CIT firm, or a bank's in-house
acquiring team that wins ONE footprint deal is **as relevant as NCR Atleos — often more so**, because it bids
the same contracts Printec bids. **Never drop a competitor for being small** (see the playbook's "Competitor
scope" rule — this binds every agent).

- **POS/acquiring is the most fragmented, most local segment** — there is a long tail of small players; the
  big acquirers (Worldline, Nexi) are only the visible top.
- **How to find the small/private ones** (they don't file or issue press): the **WINNER of a tender**
  (cross-ref Agent 2 — every award's winner is a competitor, regardless of size), **lost deals /
  who-beat-Printec**, **local-language press**, bank vendor/case-study pages, and **app stores** (soft-POS).
- **Tag every competitor with `tier`** in `references/competitors.json`: `global` | `regional` |
  `local-peer`. This keeps the small players visible and filterable on the dashboard's Competition tab
  instead of being drowned out by the giants. **Threat is independent of size** — a local-peer can be High
  threat on a specific deal. Set `tier` on the existing entries too, not just new ones.

## What to capture

- Quarterly earnings of listed names (NCR Atleos, Diebold, Glory, Worldline, Euronet, Nexi): regional commentary (EMEA/Europe), product-segment growth, order backlog.
- Contract wins/losses in footprint countries; bank-vendor partnership announcements.
- Product launches relevant to footprint (cash recycling, ATM-as-a-Service, ATM pooling, soft-POS).
- M&A and country entries/exits (e.g., a competitor exiting a market = opportunity).
- Mellon, Payten, Asseco SEE news in local languages.

## Method

Search vendor newsrooms, earnings releases since last run + "<vendor> + <footprint country>" news + local-language press (banking/tech media: capital.gr, economica.net, kapital.bg, biznis.rs, etc.).

## Proven access routes (vendor newsrooms — try the API before logging a JS gap)

Per the playbook's Access Protocol step 1, **try the underlying API first** — many vendor/local-player
newsrooms are WordPress and expose a no-auth JSON REST feed even when the rendered page is JS-only:
- `…/wp-json/wp/v2/posts?per_page=20&_fields=date,modified,link,title,excerpt,content&orderby=date`
  returns recent posts with **full article bodies**; the `X-WP-Total` response header gives the post count
  (paginate with `&page=`). Also try `…/wp-json/wp/v2/pages` when `posts` is sparse, and `…/feed/` (RSS).
  A default User-Agent works — no browser needed (verified 2026-06-25).

**Mellon (resolves the long-standing "mellongroup.com is JS-rendered" gap):** the GLOBAL site
`mellongroup.com/news` is pure JS with **no underlying API** — do NOT rely on it and do NOT log it as
the coverage gap. Mellon's actual country news lives on its **WordPress country sites**, machine-readable via:
- **`https://www.mellon.rs/wp-json/wp/v2/posts`** — Serbia, the richest feed (~68 posts; this is where the
  OTP-Bank QMS, ProCredit POS-acquiring and Raiffeisen POS items surfaced).
- **`https://mellon.bg/wp-json/wp/v2/posts`** — Bulgaria. **`https://mellon.hr/wp-json/wp/v2/posts`** — Croatia.
- **`https://mellon.ro/wp-json/wp/v2/posts`** — Romania (mostly older product pages; check `…/pages` too, and
  cross-read RO trade press e.g. wall-street.ro for Mellon/Hyosung/KAL items).
- Greek (`mellon.gr`) is NOT WordPress — use `capital.gr` / Greek press for Mellon GR news.
Fetch these country feeds every run as the Mellon source of record; treat `mellongroup.com` as a duplicate
shop-window only.

**Belt-and-suspenders (both ways).** A Tier-0 cache (`scripts/fetch_competitor_news.py`, wired into
`run_weekly`) pulls every KNOWN competitor WordPress feed into `intel-cache/competitor_news.json` each run as a
deterministic **FLOOR**, so this news is never missed even if a live fetch is flaky. **Read that cache every
run AND free-search on top** — it does NOT replace your own sweep. As of 2026-06-25 the cache covers 9
competitors with live WP feeds: **Mellon** (mellon.rs/.bg/.hr/.ro), **Asseco SEE / Payten** (asee.io — the
authoritative feed for this DIRECT competitor, e.g. the "SEPA for 14 banks in Serbia" item), **Netopia**
(netopia-payments.com), **DAAC digital** (daacdigital.com), **Profile Software** (profilesw.com),
**SelfPay/ZebraPay** (selfpay.ro — note: feed mixes consumer SEO with corporate news), **EuPlatesc**
(euplatesc.ro — marketing-heavy), **Vpayments** (vpayments.com.cy) and **Force1** (force1.ro). The OEMs/globals
(NCR Atleos, Diebold, Glory, Worldline, Euronet, KEBA, Loomis, Brink's) and several local players (BORICA,
myPOS, JCC, Viva.com, Paynetics, Evrotrust, Datecs, IBA Group, Uni Systems, Qualco, PayPoint RO, PayU) are NOT
WordPress — get those by free search/press as always. To add a newly-discovered WP feed, drop it into the
`SITES` map in `fetch_competitor_news.py`.

## Competitor financials & ATM operations (feeds the Competition-tab charts)

The engine now auto-pulls the **US-listed** competitors' figures each run (`fetch_competitors.py` +
`fetch_competitor_segments.py` in `run_weekly`) from **SEC EDGAR** into `intel-cache/competitor_series.json`:
**total revenue** (companyfacts API), **ALL reportable operating segments** from the 10-K segment note —
Atleos *Self-Service Banking* + *Network*; Diebold *Banking* + *Retail*; Euronet *EFT Processing* + *epay* +
*Money Transfer* (the ATM/self-service one is flagged as `atm_segment`; the full set is stored under
`segments`) — and **Euronet's operated-ATM count** (the "we operated X ATMs" disclosure). Every figure is
**sum-verified** (segments must add to the EDGAR total, or a dominant-segment ratio check for intersegment
cos like Atleos) — so a mis-parse is rejected, never shipped. The segments drive the dashboard's
**"Business segments"** chart (each rival's full revenue mix) and the per-product competitive views.
CIKs: NCR Atleos 0001974138 · Diebold Nixdorf 0000028823 · Euronet 0001029199 · Brink's 0000078890.

**So you do NOT re-collect the US-listed financials.** Your job is what EDGAR can't give:
- **Non-US competitors** (Worldline, Nexi, Glory, Loomis, Payten/Asseco SEE, Mellon) — pull total + ATM/POS-segment
  revenue and any unit counts from their **annual reports / investor decks**, and add them to
  `competitor_series.json` in the same shape (`series."<Name>".{revenue|atm_segment|atm_fleet}: [{year,value}]`,
  values in USD/EUR millions; note the currency). These aren't on EDGAR.
- **Operational metrics not in financial statements** — ATMaaS / endpoints / installed base / order backlog /
  POS terminals managed (from earnings commentary and decks). Record as dated series where you can.
- **Per-country competitive moves** — keep `references/competitors.json` current each run: each vendor's
  `countries`, `products`, `threat`, `role`, and a sourced `latest` move. **These four tags now drive the
  Competition tab's filterable views** — the **"Competitor landscape"** (filter by market AND product) and
  the **"Competition by product line"** chart (rivals per Printec line, split by threat). So tag `products`
  and `countries` THOROUGHLY (a vendor missing a product tag vanishes from that product's filter) and keep
  `threat` honest. The sourced `latest` move is where the wins live (e.g. "won Epirus Bank ATMaaS", "NBG
  700-recycler", "taking over CrediaBank"). **Write `latest` as flowing prose, not notes** — 2–4
  newspaper-style sentences a board member reads easily, explaining the WHY and what it means for Printec, not
  just stacking figures. Open with who the vendor is to Printec (partner / rival / both), then the most
  important recent move(s), weaving numbers and dates into the sentences. NEVER telegraphic shorthand
  ("Q1 2026: rev $1.043bn +7%, recurring ~72%, Cashzone 14 ctys…"); keep the inline `[label](url)` citations.
  Per-country ATM/POS *unit* counts are NOT publicly disclosed by
  vendors — do not invent them; the per-country view is the sourced "who's doing what, where", plus the
  market-total ECB counts on Countries.

**Discipline:** every number you add must be sourced to a filing/report and, for segment revenue, sanity-checked
against the company's total (it can't exceed it). Never estimate a competitor figure.

## Run this at scale: one subagent per competitor

Don't research the whole watchlist in one context — **fan out**. Each weekly run:
1. **Triage** the ~20-name watchlist to the set with footprint relevance this week (any news, earnings in the
   window, a footprint country mentioned). Err toward including, not excluding.
2. **Spawn one subagent per competitor in that set.** Each one sweeps *its* competitor across the whole
   footprint — newsroom, earnings/Europe-segment commentary, local-language press (capital.gr, biznis.rs,
   kapital.bg…), M&A, wins/losses, product launches — and returns a structured profile: `countries`,
   `products`, `threat`, `role`, the sourced `latest` move, plus any new signals. Fresh context per competitor
   keeps them from polluting each other and lets each go deep. The financials come from Tier 0 scripts (above),
   so the subagent does only the judgment — interpreting a win, sizing a threat, the per-country narrative.
3. **You (the parent) reduce:** dedup the same market event seen from two sides (Mellon winning a tender Brink's
   lost is ONE event), triangulate, and write the merged competitive-moves log + the `competitors.json` update.

The subagent count tracks the active competitor set — it is not fixed. See the playbook's
"Scaling the work" section for the general pattern (and why products fan out as analysts, not collectors).

## Triage the cross-agent candidate list every run (added 18/09/2026)

Before the hunt below, run `python3 weekly-intelligence/scripts/competitor_candidates.py --since <last run date>` and read
`intel-cache/COMPETITOR_CANDIDATES.md`. It lists every vendor-like name that ANY agent (bank disclosures, tenders,
regulation, jobs, statistics) wrote next to a cue such as competitor, incumbent, integrator, installer, supplier or
winner, and that no watchlist detect token matches. Decide each one: a real Printec competitor goes onto the roster
with `scripts/add_competitor.py` (with the finding as its first `latest`); banks, buyers, regulators and partners are
ignored. Why: on 18/09/2026 Novidea, the installer of Eurobank's 450+ GRGBanking recyclers, had been named twice by
the bank-disclosures agent and never reached the watchlist, so it never appeared as a competitor on the dashboard.

## Discover NEW competitors every run (the roster must grow, not just refresh)

The weekly run is BOTH a deep-dive on known names AND an active hunt for NEW competitors. The fan-out
(`agent-units.json` key "6") therefore has, alongside the big-name units:
- **6 country-cluster long-tail units** (Greece+Cyprus, Romania, Bulgaria, Serbia+W.Balkans,
  Croatia/Slovenia+CEE, Ukraine) — each sweeps its market's long tail in **local language** across every
  Printec line (POS/acquiring/soft-POS, ATM-service & independent ATM operators, CIT/cash-logistics,
  RegTech/onboarding/AML/fraud [EXCLUDING the partners Namirial & IMTF], self-service/kiosk, SIs/core-banking).
- a **`new-competitor-scout`** — cross-footprint discovery from this week's tender WINNERS
  (`ted_notices.json` fresh awards, `prozorro_notices.json` via `pb_platform_url`, Agent 2 tenders),
  app stores (soft-POS) and "who beat Printec" press.

Each tail/scout unit READS `references/competitors.json` to see what's already tracked and flags anything new
with `is_new=true` + a tier. The parent then ADDS the genuinely-new ones to the roster with
`scripts/add_competitor.py` (it dedups by name + detect tokens, so it's safe to call once per candidate),
keeping the dashboard's Competition tab growing. **Add only real Printec competitors** — a vendor / integrator /
PSP / ISO / CIT / RegTech / OEM that bids what Printec bids — never banks, buyers, or Printec partners. **Every
award winner, regardless of size, is a discovery lead** — that's the cheapest source of net-new local-peer names.

## Learnings (added 2026-06-13 after baseline backfill)

- `historical-baseline.md` in the findings folder holds the 2024→mid-2026 backfill — read it on every run alongside the latest weekly file.
- **Hyosung has no direct European sales presence** — track Mellon announcements as the Hyosung proxy in the footprint.
- **Brink's Hellas** (~3,000 staff, ATM management services) + the pending Atleos merger = the priority competitive scenario for Greece; check Brink's quarterly Europe-segment commentary.
- **Serbian and Romanian commercial banks are private entities exempt from public procurement law** — jnportal.ujn.gov.rs (Serbia) and SEAP/e-licitatie.ro (Romania) yield zero results for commercial-bank ATM/IT procurement. This is correct, not a search failure. Only NBS (Serbia) and BNR/CEC Bank tier (Romania) appear. Agent 2 should not waste portal sessions looking for Banca Intesa RS, Raiffeisen RS, etc. — refocus on local press (biznis.rs, kapital.bg, etc.) and bank career pages.
- Web search also surfaces almost no RS/BG bank procurement — local-language press is the only practical route for commercial-bank signals in those markets.
- Glory's FY ends March; results land ~May — check glory.co.jp IR each May/June run. FY2026 results confirmed 2026-05-15; next pull: full annual report (EMEA split) expected Jun–Jul 2026.
- Namirial (Printec ID partner) is under Bain Capital ownership and merging with Signaturit — watch for partner-program changes.

## Output

`findings/06-vendors/YYYY-MM-DD.md` — standard signal table + competitive moves log (vendor, move, country, implication for Printec).


## ⏱ Recency — date the trigger, not the backstory (see the playbook RECENCY RULE)
Every finding's **Date** must be the most-recent *triggering* development (a new disclosure / tender / regulation step / hire / vendor move) **or** a near-future deadline — **never** an old supporting/incumbency date. Surface something as a signal only if that development is **≤3 months old** OR it creates a concrete opportunity/deadline within the next **~18 months**. Older incumbencies / structural positions / past deals (>6 months, no near-future trigger — e.g. a 2017/2018/2020/2021 reference) are valid **context** but must be tagged **[STANDING — dated YYYY]** and never presented as new news. **"What changed since last run" = genuinely new developments only.** The engine (ingest.py) parses your Date cell, computes the age, and auto-flags any NEW/UPDATED row anchored only on a >6-month-old fact with no future trigger — it renders as *standing context*, not a NEW signal. Get the date right at source.
