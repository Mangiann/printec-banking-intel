# Postbank (Eurobank Bulgaria AD) — 27/08/2026

**Status:** complete · 10 signals · confidence capped at Medium

## Headline

Postbank is **expanding**, not shrinking, its physical network — and every new office is specified with a self-service zone. On 28/04/2026 the bank announced Postbank NEXT as a *network* of phygital offices plus "expansion of the office network". Meanwhile its own locator shows **275 of its 501 ATM sites still cannot take a deposit**. That is the quantified white space.

## Fleet counts, re-pulled 27/08/2026 (primary, machine-readable)

Source: `https://content.postbank.bg/Contacts/Network` — legacy host, server-rendered, no JS, desktop User-Agent required. Per-site flags in `data-types="|isATM|isATMWithDeposit|"`.

| Flag | Count |
|---|---|
| Total location records | 668 |
| ATM sites (`isATM`) | **501** |
| — of which deposit-capable (`isATMWithDeposit`) | **226** (45.1%) |
| — cash-out only | **275** |
| Branches (`isBranch`) | 167 |
| With self-service zone (`isSelfServiceZone`) | 154 |
| Self-service zone open 24/7 (`isSSZ24H`) | 137 |
| Specialised centres | 71 |
| Priority desks | 50 |

Baseline 30/07/2026 was 498 / 225 → **+3 ATM sites, +1 deposit-capable in four weeks.**

⚠️ The English mirror (`/en/Contacts/Network`) returns **fewer** records — 634 total, 467 ATM, 212 deposit — while branch counts match exactly. Always pull the **Bulgarian** URL.

## Signal rows

| # | Date | Signal | Printec fit | Size / Win | New |
|---|---|---|---|---|---|
| 1 | 27/08/2026 | 501 ATM sites, only 226 deposit-capable; 154 self-service zones (137 × 24/7) | ATM/self-service, cash recyclers, managed services | XL / Medium | ✅ |
| 2 | 28/04/2026 | Postbank NEXT declared a *network*; "expansion of the office network" announced; new front-office system + **new card platform** + 100+ AI solutions delivered | Self-service, HSM/security, transaction monitoring | XL / Medium | ✅ |
| 3 | 14/05/2026 | First Postbank Next office (XOPark): 5 zones incl. Express Banking Digital Zone + video-consultation zone | Self-service, cash automation, managed services | L / Medium | ✅ |
| 4 | 27/08/2026 | Two device SKUs confirmed: CASH (deposit-capable) and KIOSK (cashless); EUR cash-in, EEA transfers, municipal taxes, 250+ billers; open to other banks' cardholders | Cash automation, POS/acquiring adjacency | L / Medium | — |
| 5 | 16/07/2026 | End-to-end onboarding in Postbank App — account + digital debit card + channels in minutes, no branch, no paper | Digital onboarding/eKYC, AML | M / Medium | ✅ |
| 6 | 22/06/2026 | Selected to EU AI Act Advisory Forum; only CEE bank of 700+ applicants; first sitting 19/06/2026 | AML/monitoring under AI-Act governance | M / Low | ✅ |
| 7 | 27/03/2026 | AI Loan Administration scaling — **IBM watsonX + integrator IBS**; 90% pilot accuracy | Competitive intel | S / Low | ✅ |
| 8 | 20/11/2025 | EVA digital assistant (self-hosted `chatbot2.postbank.bg`), now an "Ask EVA" nav entry for retail *and* business; EVA AI Voice Bot slated for call centre from early 2026 | Context / remote assistance | S / Low | — |
| 9 | 07/08/2026 | Dual BGN/EUR display removed from 14/08/2026 across App, Web, ONE wallet | Euro programme closes; cash-cycle is next lever | S / Low | ✅ |
| 10 | 28/07/2026 | Moody's affirms A3 deposit / Baa2 issuer, stable; equity/RWA 22.1%, NP/assets 1.7% | Capex not constrained | Unscoped | ✅ |

## Access issues

- `www.postbank.bg` behind Imperva; new locations page returns chrome only. **Claude-in-Chrome escalation attempted and failed — extension not connected.** Worked around via the legacy `content.postbank.bg` host.
- `eurobankholdings.gr` is an SPA to plain fetch — the H1-2026 results announcement (30/07/2026) could not be retrieved.
- `eurobank.gr` IR index stale, nothing after 9M-2025; `/first-half-2026` 404s.
- `bnb.bg` payment-statistics paths all return the site's error page even with a desktop UA.
- WebSearch budget (200/200) exhausted mid-run; second half done by direct fetch and link-walking.

## Operator requests

1. Fetch Eurobank Holdings **H1-2026** release (30/07/2026) via browser or the ATHEX OAM.
2. Fetch **BNB** Q2-2026 ATM/POS terminal counts (path not discoverable from the site's own nav).
3. Reconnect Claude-in-Chrome.
4. **Add to source catalogue:** `https://content.postbank.bg/Contacts/Network` — tested OK, no JS, parse `data-types` attributes. Bulgarian URL only.
