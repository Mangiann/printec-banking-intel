# DORA (Digital Operational Resilience) — Findings 2026-07-14

**Workstream:** DORA / digital operational resilience. **Confidence capped at Medium (single agent).**
**Baseline:** 2026-06-24 Agent-3 run. Report ONLY what is NEW or CHANGED since, or sources the baseline never saw.

## Plain-language note
- **DORA** (Reg. EU 2022/2554, in force 17 Jan 2025): EU rulebook forcing banks/PSPs to manage ICT risk, report major ICT incidents, keep a register of ICT outsourcing, and test resilience.
- **Register of Information (RoI)** — Art. 28/29: structured register of every ICT third-party contract, submitted annually to the national regulator (EBA xBRL-CSV format, 15 templates / ~105 data points).
- **TLPT** — Art. 26-27: red-team attack simulations on the largest banks under TIBER-EU, at least every 3 years.
- **CTPP** — Art. 31: ICT providers (cloud, core-banking, payments) designated by the ESAs as systemically critical and placed under direct EU oversight (JETs / Lead Overseer).
- **CSA** (Common Supervisory Action): coordinated cross-EU supervisory exercise run by NCAs to a shared ESMA/EBA methodology.

## NEW / CHANGED since 2026-06-24

1. **ESMA CSA on CASPs' digital operational resilience for custody — NEW (08/07/2026, primary ESMA).** First coordinated MiCA/DORA-aligned resilience review of crypto custody: NCAs assess governance, key & storage management, transaction controls, incident detection/response, smart-contract risk, third-party dependencies on a risk-based CASP sample. Runs H2-2026 → H1-2027; consolidated report to ESMA H2-2027. Weak footprint fit (crypto custodians, not core Printec bank customers) but touches Thales HSM/key-storage, INETCO monitoring, incident response.
2. **RoI 2026 cycle closed; validation materially tightened — development baseline part file never captured.** Second annual RoI cycle (reference date 31/12/2025): national submission deadlines Feb–Mar 2026, correction window 31/03→30/04/2026, NCAs consolidate to ESAs. ESAs applied validation stricter than the 2024 dry-run (where only 6.5% passed all checks); widespread rejections — LEI gaps, subcontractor-linkage errors, template formatting. Next cycle reference date 31/12/2026 → submissions early 2027. Printec is a *registered ICT third-party* to footprint banks (x-core, NCR/Atleos ATM sw, cash automation, Siron AML), so its contracts must appear in every client's register and carry DORA clauses.
3. **DORA subcontracting RTS — Delegated Reg (EU) 2025/532, OJ 02/07/2025, now applies. [STANDING dated 02/07/2025], not in baseline part.** Sets what a financial entity must assess before subcontracting ICT services that support critical/important functions (audit rights, exit, chain-monitoring, concentration). Printec's managed/field-services, telemetry and multivendor-ATM contracts at footprint banks must be DORA-conformant — a differentiator and a re-papering opportunity.
4. **CTPP oversight now operational (2026) — enrichment of baseline.** ESAs Guide on Oversight activities (JC 2025/29, 15/07/2025) confirms JETs + Joint Oversight Venture; five activities (designation, annual risk assessment, in-depth examination, recommendations, follow-up). First comprehensive examinations + binding recommendations expected during 2026; CTPPs pay annual oversight fees and face periodic penalty payments up to 1% of average daily worldwide turnover per day of breach (Art. 35(6)). Printec is not a CTPP but rides several of the 19 (AWS/Microsoft/Oracle) — indirect assurance.
5. **Footprint transposition gap — Bulgaria & Slovenia still under DORA Directive (2022/2556) infringement. [STANDING dated 27/03/2025], not in baseline part.** Commission letter of formal notice 27/03/2025 to 13 MS incl. BG, SI (also GR, RO). Romania since closed via OUG 14/2026 (03/2026); Greece via Law 5193/2025. Residual national-transposition uncertainty for BG/SI banks and their vendors. Recommend Compliance/DPO confirm current national status.

## TLPT note (no material change)
SSM TIBER-EU Implementation Guide (Nov-2025) confirms 9–14-month test cycle; first-cycle deadline 17/01/2028; entities targeting completion should start red-team procurement by Q1-2027; qualified-provider capacity constrained. Most footprint entities are LSIs/subsidiaries (in scope via parent groups Erste/RBI/UniCredit/OTP/NBG). Printec offers no red-teaming, but its ATM/self-service estate sits inside the test perimeter — device telemetry/monitoring supports evidence.

## Signal rows — see structured output.
