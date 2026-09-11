# Serbia — Agent 5 (Early Intent: jobs + leadership) — run 2026-07-31

**Status: complete.** 13 signals. Fresh full run (no prior checkpoint for this runDate).

## Headline

**RBI won the Addiko takeover.** Acceptance period closed 29/07/2026 17:00 CEST; RBI announced 10,831,435 shares = **56.16%**, clearing its lowered 55% threshold. NLB's higher EUR 37.00 bid lost to RBI's EUR 26.50. This **reverses the baseline** (NLB ahead, RBI at 50.42% on 09/06/2026). RBI now controls **both Raiffeisen banka Beograd and Addiko Bank Beograd** → two ATM fleets, two POS/acquiring estates, two card portfolios to consolidate. Raiffeisen Serbia is already a Printec **x-core** reference customer. This is the largest Serbian opportunity in the run (XL / win High) — **flagged to Orchestrator**.

Second-order confirmation: Raiffeisen banka's own live hiring matches. A **"Menadžer prihvatne mreže"** (Acquiring Network Manager — owns POS estate pricing *and* proposes ATM placement/relocation, rok 01/08/2026) plus a **6-role financial-crime/control cluster** (AML ×2, fraud risk, regulatory compliance, internal control, internal audit — all closing 07–14/08/2026) out of only 11 live ads. Senior mandate + matching hiring cluster = **confirmed programme**.

## Signal rows

| # | Entity | Signal | Date | Size / Win | New |
|---|---|---|---|---|---|
| 1 | RBI / Addiko (RS) | RBI wins Addiko, 56.16% final acceptance; Raiffeisen RS + Addiko RS to consolidate | 29/07/2026 | XL / High | ✅ |
| 2 | NBS + 18 banks | SEPA Credit Transfer **operational 05/05/2026**; register entry 10/04/2026; SCT Inst is the announced next phase | 05/05/2026 | XL / Medium | ✅ |
| 3 | Raiffeisen banka | "Menadžer prihvatne mreže" — POS + e-comm + ATM acquiring, ATM siting | 31/07/2026 (rok 01/08) | L / Medium | ✅ |
| 4 | Raiffeisen banka | **PROGRAM**: 5–6 concurrent AML / fraud-risk / compliance / control roles | 31/07/2026 (rok 14/08) | L / Medium | ✅ |
| 5 | AikBank + OTP RS + UniCredit RS | Serbia's **first live Mastercard Agent Pay** agentic transactions (agent tokens, consent, identity verification) | 18/06/2026 | L / Medium | ✅ |
| 6 | NBS | Draft amendment to Law on Interbank Fees — caps extended to **foreign-issued cards** (0.20/0.30% domestic; 1.15/1.50% foreign online) | 16/06/2026 | M / Medium | ✅ |
| 7 | Erste Bank a.d. Novi Sad | 9 live ads incl. infosec-risk specialist + senior system + senior network engineer | 31/07/2026 (rok 06/08) | M / Low | ✅ |
| 8 | Banca Intesa | Product Owner, Card Products — issuing, card-system parametrisation, regulation | 31/07/2026 (rok 08/08) | M / Low | ✅ |
| 9 | OTP banka Srbija | **Zorana Aleksić to Executive Board** (retail, digital-plus-advice mandate); + Enterprise Architect & Head of Infrastructure Platforms | 03/07/2026 | L / Medium | ✅ |
| 10 | NLB Komercijalna | **ZERO** live postings; baseline's digital-services ad lapsed 02/07/2026, not re-posted. UniCredit RS also zero | 31/07/2026 | S / — | ✅ |
| 11 | AikBank | [STANDING – 2025] Eurobank Direktna merger complete 31/03/2025 → **150 branches / 550 ATMs**, EUR 6.4bn assets | 31/03/2025 | L / Medium | — |
| 12 | Banca Intesa | [STANDING – 2025] Paperless in **48 branches** w/ qualified e-signature; 75% faster processing; committed to network-wide extension | 27/06/2025 | L / Medium | — |
| 13 | NBS statistics | [STANDING – 2025] End-2024: **3,218 ATMs** (+4.5%), **160k+ POS** (+17.7%), 12.2m cards, 681.7m purchases | 13/03/2025 | Unscoped / — | — |

## Read-across for Printec

- **Addiko integration** is the wedge: x-core multivendor ATM software, NCR fleet rationalisation, POS/TMS consolidation, card re-issue + HSM re-keying, AML convergence, and heavy field/managed services to touch every device.
- **SEPA SCT Inst phase** = ISO 20022 + 24/7 rails + in-line screening at up to 18 banks → INETCO + IMTF Siron.
- **Interchange caps** squeeze acquiring margin → softPOS + TMS + digital merchant onboarding become the cost answer.
- **Agentic payments already live** at three banks → tokenisation, Thales HSM/PCI-PIN, and a fraud-monitoring gap on a brand-new transaction class.
- ATM fleet is flat (+4.5%) while POS grew +17.7% → Serbia is a **recycler/upgrade + POS-volume** market, not a dispenser-growth market.

## Boards actually checked (zero postings is a finding)

poslovi.infostud.com employer feeds — Raiffeisen banka (11), OTP banka Srbija (8, only 4 genuine), Banca Intesa (2), AikBank (2), Erste Bank a.d. Novi Sad (9, via `company_id=249`), **NLB Komercijalna (0)**, **UniCredit Bank Srbija (0)** — plus Infostud banking category 58, erstebank.rs careers, nlbkb.rs careers.

Privacy rule observed throughout: role title, bank, URL, date only. Executive names appear only from published corporate announcements.

## Access issues (summary)

`nlbkb.rs/.../karijera` 404 · `erstegroup-careers.com` DNS ENOTFOUND · `beta.rs` 403 · `seenews.com` 403 · `rbinternational.com` takeover-law index JS-only (used the EQS release) · `nlb.csod.com` JWT-gated. **Trap:** Infostud's `/oglasi-za-posao-firma/{slug}` URL silently falls through to a generic 236-result list instead of erroring — only `company_id=NNN` is reliable, and a slug miss must never be read as zero.

## Top operator requests

1. EPC SCT / SCT Inst participant register — name the 18 Serbian adherents, identify non-SCT-Inst banks.
2. NBS interchange draft text + consultation notice (press dates 11/06 vs 16/06/2026 conflict).
3. Official Austrian Takeover Act **result** publication + Serbian clearance filings for Addiko.
4. Browser checks: Erste Group ATS, NLB Cornerstone, and own career pages for Banka Poštanska štedionica, Halkbank RS, ProCredit RS, Mobi Banka.
