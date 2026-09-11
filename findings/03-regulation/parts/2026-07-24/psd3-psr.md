# PSD3 / PSR — Regulation workstream findings (run 2026-07-24)

Scope: EU timeline, fraud-liability, open banking changes. Primary-source first. Confidence capped Medium.
Search languages: English + English.

## Headline status (as of this run)
- Legislative status UNCHANGED vs 14/07/2026 run: EP Legislative Train (primary, last updated 20/06/2026) still says "close to adoption" — EP PLENARY has NOT formally adopted; Council formal adoption, signature and OJ publication all still pending. No OJ publication located as of 24/07/2026. No confirmed plenary sitting date found on OEIL/agenda.
- Procedure ref: 2023/0210(COD) (PSR), companion PSD3 directive. Rapporteur Morten Løkkegaard (Renew, DK). Provisional political agreement 27/11/2025; ECON approved negotiated text 05/05/2026; COREPER endorsed 22-23/04/2026 (Council ST-8221/8222-2026).

## Application timeline (source variance — logged, not resolved)
- General PSR application: majority of firm reads say ~21 months after OJ publication (Freshfields, openbankingtracker) → ~2028. Some reads say 18 months (Worldline re PSD3 transposition; AO Shearman re general PSR). PSD3 national transposition = 18 months after entry into force. Practical readiness H2-2027 → Q2/Q3 2028.
- Verification of Payee (VoP): ~27 months after entry into force per openbankingtracker (late 2028-2029). NOTE VoP already LIVE for euro credit transfers under the separate Instant Payments Regulation since 09/10/2025 — PSR generalises rather than introduces it.

## NEW / ENRICHED this run vs 14/07
- Impersonation ("spoofing") fraud liability sits in PSR Article 59; PSP must fully refund consumer within 10 business days of consumer notification OR police report; burden of proof on PSP to show consumer fraud/gross negligence.
- Extended liability chain: Electronic Communications Service Providers (ECSPs/telcos) face SECONDARY liability where they fail to remove fraudulent/illegal content after PSP notice; online platforms/hosting services likewise liable where fraud arose via their platform and they failed to act. Duty of telco-PSP cooperation on fraud prevention.
- Open banking specifics: PSD2 permanent fallback-interface obligation REMOVED (replaced by supervisory contingency); dedicated API must meet harmonised performance KPIs (uptime/latency/error rates, via EBA RTS); mandatory consumer permission dashboards (view/revoke TPP access); SCA simplification for AIS (~180-day re-auth window). Largely outside Printec core (note-only / eKYC-adjacent).

## Footprint exposure
Directly binds EU members in 17-country footprint: AT, BG, CY, CZ, GR, HR, HU, RO, SI, SK. Non-EU footprint (AL, BA, ME, MK, RS, XK, UA) not bound but candidate-country alignment likely follows. Budget window = NOW (H2-2026 / 2027) for fraud-monitoring + SCA stack ahead of ~2028 application.

## Printec mapping
Strongest hook = fraud-liability shift (Art 59): PSP full-refund exposure for spoofing/APP scams + VoP mismatch → real-time transaction monitoring (INETCO), fraud analytics (FICO), AML/KYC (IMTF Siron). SCA hardening → Namirial eKYC, Thales HSM/PCI. Open-banking API/dashboard = note-only (API infra, not Printec core).

## Key sources
- EP Legislative Train (primary): europarl.europa.eu/legislative-train (status 20/06/2026)
- Council ST-8221-2026 / ST-8222-2026 compromise texts (data.consilium.europa.eu)
- Freshfields, Worldline, openbankingtracker, AO Shearman, PwC alert (press/analysis, Low-Medium)
