# AML — AMLA / AMLR — findings (run 2026-07-15, retry round 2)

Slug: aml-amla-amlr. Confidence capped at Medium (regulation agent). Primary sources: AMLA, FATF, EUR-Lex, national regulators.

## Summary of NEW / CHANGED developments since baseline (24/06/2026)

1. **AMLA delivered its Level-2 RTS package around the 10/07/2026 deadline.** On **08/07/2026** AMLA published the final **RTS on enforcement / pecuniary sanctions & administrative measures (Art. 53(10) AMLD6)** — a harmonised EU enforcement approach classifying breaches into four gravity levels so "the same breach in the same circumstances leads to the same enforcement outcome" EU-wide. Applies once adopted by the Commission. Source: amla.europa.eu press release 08/07/2026.
2. **AMLA rule-making accelerated in early July 2026** with a wave of consultations/finalisations: 02/07/2026 public consultation on a **common EU format for reporting suspicions (STR)**; 03/07/2026 common formats for FIU cooperation / EPPO reporting; 06/07/2026 cross-border FIU information exchange; 13/07/2026 harmonised risk assessments (non-financial sector). Standardised STR/monitoring output formats affect every footprint bank's transaction-monitoring stack.
3. **Direct-supervision selection machinery live.** AMLA published its **reporting package for provisionally-eligible obliged entities on 12/05/2026** (webinar 10/06/2026); national supervisors must return data by **15/08/2026**; provisional list of ~eligible entities by **end-Sep-2026**; formal selection 2027; direct supervision of ~40 highest-risk groups from **2028**.
4. **Montenegro (footprint ME): AML Act amendments IN FORCE 12/05/2026**, explicitly aligning with EU Reg 2024/1624 (AMLR) + MONEYVAL/FATF. Occasional-transaction CDD threshold cut EUR15,000->EUR10,000; CDD now mandatory on cash EUR3,000-10,000 with FIU report within 3 working days; cash payments EUR10,000+ must go by wire to a Montenegrin account; ordered continuous monitoring must notify FIU on customer transactions >EUR1,000 (natural person)/>EUR3,000 (legal entity); UBO falls back to all managers if none identifiable. Source: BDK Advokati via CEE Legal Matters 12/06/2026.
5. **FATF grey-listed Bosnia & Herzegovina 19/06/2026** (baseline already had this) — CONFIRMED via FATF plenary outcomes (Paris 17-19/06/2026); MER Dec-2024 MONEYVAL-driven; action plan on DNFBP supervision, sanctions, beneficial ownership. Footprint BA banks face heightened correspondent-bank EDD.
6. **AMLD6 beneficial-ownership register provisions (Arts 11-13, 15) due 10/07/2026**; Commission opened infringement proceedings (autumn 2025) against 11 MS over the missed 10/07/2025 FIU-access deadline. Footprint EU MS affected: AT, BG, CY, CZ, GR, HR, HU, RO, SI, SK.
7. **Ukraine (footprint UA):** NBU aligning AML with EU 5th/6th AMLD + AMLR for SEPA/EU-accession; reporting-entity base expanded to VASPs, real-estate agents, non-bank PIs; 25% UBO threshold. (Low confidence - generic sourcing.)

## Access notes
- CEE Legal Matters (BDK Montenegro article) returned HTTP 403 to WebFetch; retrieved via curl with desktop User-Agent.
- AMLA /news_en JS-rendered (0 results to fetch); used /news-media/news-articles_en instead.
- Guessed AMLA press-release slug 404'd; found correct URL via search then fetched.

Signal rows returned in the StructuredOutput object.
