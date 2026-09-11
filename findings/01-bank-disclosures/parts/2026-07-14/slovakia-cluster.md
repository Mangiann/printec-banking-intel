# Slovakia cluster — bank disclosures (2026-07-14, merged 7th pass)

Target: Slovenská sporiteľňa (Erste), VÚB (Intesa Sanpaolo), Tatra banka (RBI). Also ČSOB, UniCredit, Fio, Slovenská pošta.
Focus: deposit-ATM expansion, ATM 2.0 coin deposit, eKasa POS mandate, OptiCash/APTRA.
Printec SK incumbency: main provider of NCR/Atleos ATMs, payment terminals, self-checkout, eKasa ECR, Android POS platform, ATM software (APTRA/OptiCash). Slovak commercial banks are PRIVATE — no UVO tenders; procure directly.
Access: WebFetch blocked at network layer for .sk domains (slsp.sk, techbyte.sk "unable to verify domain safe"; tatrabanka.sk PDF socket-hangup). Used WebSearch index snippets of PRIMARY pages (slsp.sk, tatrabanka.sk, vub.sk, fio.sk) + press. Logged.

## NEW / CHANGED vs 2026-06-29 baseline

1. **VÚB launches new financial-agents network (Intesa Sanpaolo Fideuram model) — announced 06/07/2026.** SK + Hungary first ISP-group countries; target ~1,200 agents + 2,500 relationship managers, ~1m clients; later HR/RS/SI/RO/AL/BA/MD/UA/CZ/EG. (sita.sk 06/07/2026; teraz.sk.) NEW.
   → Printec: digital onboarding/eKYC, AML/compliance, managed services.

2. **SLSP new-ATM-system software developer = Asseco** (touchit.sk 26/06/2026) — SOFTWARE COMPETITOR signal vs Printec APTRA/OptiCash at SLSP. SLSP fleet ~752 total, ~290 deposit/recycling (2025). Contactless (card-less) DEPOSIT via phone/smartwatch live at all deposit ATMs since March 2026. (touchit.sk; slsp.sk "Bezkontaktné vklady a výbery"; kryptomagazin.sk.) NEW (Asseco + card-less deposit).
   → Printec: defend software incumbency; NFC reader upgrades, recyclers, managed services.

3. **VÚB core/channel migration deepened.** "VÚB Banking" unified app (one platform across 7 ISP countries) migration of most retail clients completed ~11/12/2025; >80% migrated. ISP group core = Thought Machine (UK) under Isytech cloud. VÚB ~142 deposit-capable ATMs of ~500+; stated intent to "significantly expand" deposit ATMs. (vub.sk; touchit.sk.) CHANGED — Thought Machine named, cutover pinned.
   → Printec: channel/self-service integration to new core, x-core, deposit-ATM supply.

4. **Fio banka — own Slovak ATM network, ALL recycling (deposit+withdraw), contactless.** 14 units now; target ≥50 within 3 years, then regional expansion. Greenfield recycler fleet; supplier undisclosed. (fio.sk; sme.sk index; finreport.sk.) NEW competitor/opportunity.
   → Printec: cash recyclers, managed services, field service.

5. **Tatra banka Bankomat 2.0 recycling rollout (annual report 2025).** 303 ATMs / 259 deposit ATMs; goal to REPLACE ALL withdrawal ATMs with deposit/recycling units; coin-deposit ATMs 40+ (all 1c–€2, free, 300 coins/day cap); end-2026 adds Bankomat 2.0 in Piešťany, Prievidza, Levice, Trenčín, Žilina, Komárno. (tatrabanka.sk AR2025/blog; techbyte.sk.) CHANGED/deepened.
   → Printec: coin recyclers (Glory/DN iCASH), recyclers, OptiCash cash-cycle optimisation, field services.

6. **eKasa cashless-acceptance mandate LIVE + enforced.** Act 384/2025 Coll.: from 01/05/2026 (moved from 01/03) every eKasa merchant must offer ≥1 cashless option for purchases >€1. Finančná správa inspections ACTIVE from May 2026. Fines: cashless breach €500–15,000; first eKasa breach €1,500–20,000, repeat €3,000–40,000. Law hardware-agnostic (QR/Pay-by-square satisfies → dampens dedicated-terminal pull). Subsidy "Slovensko platí kartou" = up to 9 months fee-free terminal for merchants without card acceptance in prior 12 months. Act 384/2025 also removed most eKasa exemptions from 01/01/2026 → new service/from-the-yard merchants need ECR. (techbyte.sk 05/2026; grantthornton.sk; podnikajte.sk; financnasprava.sk.) CHANGED — now live & enforced.
   → Printec: POS terminals (Verifone/Castles), SoftPOS/Tap-to-Pay, eKasa ECR, acquiring/TMS.

7. **UniCredit Bank SK — 56 deposit machines** retained at all former branch sites. (kd.sk; sita.sk.) Context.

8. **Slovenská pošta self-service cash kiosks — UNCHANGED.** Still 5-branch pilot since 15/08/2025; deposit/withdraw + ePoukaz + Pay-by-square; NO scale-up tender. STILL PRE-TENDER. (posta.sk; sita.sk.)

## Data-quality notes
- Tatra deposit-ATM counts vary by definition (259 "vkladomaty" vs 40+ coin / 300+ deposit-capable). SLSP fleet ~752 (2025, down from 761). UniCredit 56 deposit machines. Fio 14 recyclers.
- Confidence capped Medium per rules. Signal rows: see structured output.
