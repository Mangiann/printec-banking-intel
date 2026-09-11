# Hungary — EKR (ekr.gov.hu / kozbeszerzes.hu) — run 01/08/2026

**Status: complete.** 11 signals, all new or materially changed vs the 24/07/2026 published file.

## Headline

**The Act XVIII of 2025 ATM rollout will never appear in EKR.** An exhaustive sweep of the EKR
public notice register (undocumented public API + full CSV exports, 20+ Hungarian keyword
variants) returns zero ATM or banknote-handling procurement. MBH, Erste, K&H, Takarékbank and
Gránit do not exist as contracting authorities in EKR at all; OTP appears only as a subsidised
buyer of construction works. Every EKR hit for the string "ATM" is HungaroControl and means
Air Traffic Management — exactly as the brief warned. Hungary's ~600 remaining mandated ATMs are
a **direct commercial sale**, not a tender watch.

## What is actually happening on the mandate

- Phase 2 (settlements 500–1,000 people) is **still live under the new Tisza-led government** —
  ~600 ATMs due by **31/12/2026**, banks have slowed hoping for relief and got none
  (Telex, 15/06/2026). Cost cited: **HUF 8–10m per machine** install + first year, against
  **0–2 withdrawals a day**.
- Non-compliance fines escalate from **HUF 5m after 3 months to HUF 150m after 24 months**.
- MNB decree 19/2025 (VI. 26.) allocates settlements bank by bank — OTP 383, MBH 147, K&H 102,
  Erste 93, Raiffeisen 64, CIB 52, UniCredit 46, Gránit 13, MagNet 13 (~913 settlements).
  Swap/assumption contracts for Phase-2 sites were due **28/02/2026**, ERA notification
  **16/03/2026**, and any operation-assumption contract must run **at least 5 years**.
- Fleet: **5,688 ATMs at 31/03/2026** vs 5,211 a year earlier (+477, +9.15%); Budapest −8.
- Decommissioning was **relaxed** from 07/06/2025 (Korm. rendelet 129/2025 (VI. 5.)) — machines
  can now be relocated, which drives refurbishment/re-siting services work.
- **Constitutional Court: still no ruling.** OTP + Erste + Raiffeisen filed 10/11/2025 via the
  Budapest Stock Exchange against Act XVIII/2025, NGM 16/2025, MNB 19/2025, MNB 20/2025 and the
  amendment of MNB 1/2023. Nine months on, nothing published; the mandate stands.

## Bid-able now

| Buyer | Item | Deadline | Ref |
|---|---|---|---|
| **MNB** | Network HSMs — Entrust nShield 5c mid + 36m vendor support, CPV 48730000 | **24/08/2026** | TED 511411-2026 / EKR001466692026 |
| MNB | NSS + HSM support & consultancy services | closed 14/07/2026, award pending | KÉ 10711/2026 / EKR001193282026 |
| ORFK | EES border kit: 16 self-service biometric kiosks + 8 ABC e-gates + 75 outdoor face-capture units | closed 28/07/2026 (3 extensions) | TED 497245-2026 / EKR002342252025 |

## Competitor win to log

**BKK Budapest — POS/mPOS/softPOS + acquiring + Qvik, HUF 1,318,733,639 (~EUR 3.3m), awarded
22/06/2026** to a consortium **led by SimplePay Zrt. (32835155244) with OTP Bank Nyrt.
(10537914444)**. TED 424870-2026. Hungarian public POS estates are won by bank+PSP consortia —
Printec would need a Hungarian acquiring partner.

## Access route that works (record it)

EKR is an Angular SPA. Pull `https://ekr.gov.hu/main.<hash>.bundle.js` (note: **not** under
`/portal/`), extract `/api/publikus/kozbeszerzesi-hirdetmenyek`. Query params `eljarasTargya`
and `ajanlatkeroNeve` work as case-insensitive substring filters; **page size is hard-capped at
10** and date params are ignored, so use the unpaginated CSV export at
`/api/publikus/kozbeszerzesi-hirdetmenyek/exportalas/csv?<same params>`.

Blocked this run: njt.hu (connection reset, even with desktop UA — use net.jogtar.hu/getpdf
instead); alkotmanybirosag.hu case search (JS-only); public.mkab.hu PDFs (unparseable);
net.jogtar.hu getpdf for amending decree A2500020.MNB (121-byte non-PDF).
