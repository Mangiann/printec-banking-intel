# Bank-owned procurement pages — findings (run 2026-07-14)

Scope: banks/central banks running their own RFP portals (PrivatBank, CEC, CNB, TEB, HNB, Poštanska štedionica) + adjacent bank-own awards revealing winners. Delta vs 2026-06-24 baseline, re-verified against primary sources where reachable.

## Status of carried-forward WATCH tenders
- **CNB CZ glass-steel cashier partitions** (E-ZAK contract_display_1284): CHANGED — deadline 25/06/2026 10:00 has passed; procedure now in **"Hodnocení" (Evaluation)** phase, NO winner/value yet. Small physical-security scope. Primary opened.
- **Greek OPSEA/ΟΠΣΕΑ EUR515.4m digital-ID** competitive dialogue: CHANGED — Phase A participation deadline moved from 25/06 to **27/07/2026** (one-month extension). Four consortia now named in press: OTE–Byte–Idemia; Unisystems–Veridos; Space Hellas–Nova–Zetes–**Thales**; AustriaCard–Toppan. Printec only a possible sub (Thales HSM / Namirial e-sign) — Thales is inside the Space Hellas consortium.
- **TEB Kosovo** own portal (teb-kos.com/en/tenders): still active, refreshed refs — Cash-Handling Machines 292-25 (deadline-extended), ATM Kiosk production/servicing 375-25, Remote/Digital Onboarding + e-signature (extended Jun-2026), Physical Security+CIT+ATM replenishment 636-24, Electronic Security Systems 590-24 (re-tender), NEW Security Monitoring-room supervision 281-26. TEB never publishes winners.
- **CEC Bank RO** (cec.ro/achizitii): portal now reachable via desktop UA (403 defeated). Only two anunțuri listed, both CLOSED: Info-SMS messaging IT (deadline 13/03/2026) and physical-security risk-analysis services (deadline 23/04/2026). No ATM/cash-equipment tender open. No winners published.
- **Bank of Albania** banknote-packaging: still BLOCKED — procurement pages 302/500 to all routes incl. desktop UA; deadline/values remain UNVERIFIED. Escalate to operator.
- **Poštanska štedionica RS** CIT+ATM-servicing (deadline 30/04/2026): award still not retrievable (posted.co.rs private bank; danas.rs ATM-renewal article 403s). No winner published.
- **PrivatBank UA 800 ATMs 2026**: still PRE-TENDER. tender.privatbank.ua = Angular SPA/302 API; uub mirror 403; Prozorro search SPA-only. No hardware notice retrievable. Printec incumbent.

## HNB Croatia 2026 procurement plan (PDF v2.8, updated ~29/04/2026) — primary opened
Plan lists multiple cash-equipment lines (CPV 42990000). Banknote sorting/packaging: V-53/2026 "sortiranje i pakiranje novčanica" and mid-size banknote sorter — open procedure (Otvoreni postupak). Coin processing: "Uređaji za obradu kovanica - blagajna". Large sorting system explicitly CPS/G+D (incumbent-locked). Values in the plan are column-misaligned in extraction; do not quote per-line figures without operator confirmation.

## Competitor award intel (for Agent 6)
- Payten (Asseco SEE) dominant in Croatia: maintains 3,100+ ATMs (Diebold Nixdorf & NCR brands); cash-recycling ATM delivery projects with Erste Bank Croatia and Raiffeisenbank Croatia. Locks HR bank-own ATM refresh away from Printec. Dates not pinned — Low confidence.

## Access blocked (logged)
- bankofalbania.org procurement: 302/500 (desktop UA) — escalate.
- posted.co.rs award pages / danas.rs: 403.
- tender.privatbank.ua API: 302; uub.com.ua: 403; prozorro.gov.ua search: SPA-only.
- cec.ro: 403 to WebFetch, DEFEATED via curl desktop UA (page retrieved).
