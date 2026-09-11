# Hungary banking cluster — findings 2026-06-29

Focus: Act XVIII / MNB ATM mandate, OTP eMACH.ai core (NOT MBH), MBH integration, AML fines.

## Headline corrections vs baseline
- **eMACH.ai is OTP's platform, NOT MBH's.** OTP chose Intellect Digital Core (IDC), built on eMACH.ai, contract signed 08/12/2023 (parallel rollout OTP HU + DSK Bulgaria). MBH chose Thought Machine (2022). The focus brief conflated these.
- Mandate instrument is **MNB decree 19/2025. (VI. 26.)** (published Official Gazette 26/06/2025) + NGM decree 16/2025. (V. 29.). Timeline: ATM in every >1,000-pop municipality by 31/12/2025; every >500-pop by 31/12/2026. Banks could swap/transfer obligations via ≥5-yr contracts by 31/07/2025.

## ATM mandate — per-bank assignment (MNB 19/2025)
By municipalities assigned (Bank360): OTP 357, MBH 213, K&H 109, Erste 100, Raiffeisen 59, CIB 54, UniCredit 44, Gránit 13, MagNet 13 = 962 municipalities.
By net-new ATM units / cost (Bankmonitor): OTP 428 (1,712m HUF), MBH 195 (780m), K&H 117 (468m), Erste 104 (416m), Raiffeisen 65, CIB 52, UniCredit 52, Gránit 13, MagNet 13 = 1,039 ATMs (~4.156bn HUF @ 4m HUF/unit).

## ATM fleet sizes early 2026 (Origo)
OTP ~2,000; MBH 1,200; K&H 639; Erste 491; UniCredit 195; CIB 156.
New units deployed prior year: MBH led with 316 new, OTP 128, K&H 92. New-share: MBH >25%, K&H 14.4%, Erste/UniCredit 7-9%.
Deposit-capable (recycler/CDM): OTP 536, K&H 448, Erste 260, MBH 252, UniCredit 94, CIB 70.

## AML fines — MNB, 07/01/2025 (PRIMARY mnb.hu)
- OTP fined 28.125m HUF; MBH fined 15m HUF. K&H fined 20.5m HUF (separate action).
- OTP: incomplete retrospective screening (enhanced-DD customers), e-money screening gaps, no review of screening-system mods vs AML trend reports, weak source-of-funds verification on cash deposits >10m HUF, weak beneficial-ownership controls, incomplete training docs.
- MBH: missing internal rules for trust-asset-mgmt alert processing, inconsistent alert handling, **insufficient staffing to process screening alerts within regulatory timeframes**, no source-of-funds documentation procedure.
- K&H: failure to report numerous suspicious transactions, inadequate CDD, beneficial-owner verification gaps, improperly operated screening system.

## MBH integration
- MKB + Takarékbank merged 30/04/2023, "MBH Bank" from 01/05/2023. IT migration to single group platform completing 2026. Major unification bank-holiday 31/12/2025–04/01/2026 (customer systems unified). Core = Thought Machine cloud.

## OTP eMACH.ai
- IDC/eMACH.ai contract 08/12/2023 (coop agreement May 2023); parallel OTP HU + DSK Bulgaria. No confirmed 2026 go-live milestone surfaced this run.

## Printec mapping
- Mandate 1,039 net-new ATMs by 31/12/2026 = ATM hardware + cash-recycler + x-core/managed-services + joint-network consortium play. MBH (316 new + recycler gap, 252 deposit vs 1,200 fleet) and OTP (428 mandated) are biggest.
- AML fines across OTP/MBH/K&H, esp. MBH staffing/transaction-monitoring gap = AML/transaction-monitoring (Siron) + managed-services pitch.
- MBH 2026 IT consolidation + OTP core migration = channel/ATM-driver integration windows.
