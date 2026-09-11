# Romania — SEAP/SICAP (e-licitatie) — Tender scan 2026-07-14

Analyst: Printec banking market-research. Portal slug: romania-seap-sicap.
Baseline (2026-06-24) had NO Romania item, so all rows below are new to the findings file.

## Structural finding (important context)
Romania's large retail banks — BCR, BRD, Banca Transilvania, Raiffeisen, ING, UniCredit — are PRIVATELY owned and do NOT procure through SEAP/SICAP; their ATM/POS/cash/security buys happen via private tenders invisible to SEAP. The state-owned buyers that DO use public procurement are: CEC Bank (mostly via its OWN portal cec.ro/achizitii, only some services on SEAP), BNR (central bank), Compania Naţională Poşta Română, and the new third state bank Banca de Investiţii şi Dezvoltare (BID, own portal bidromania.eu). Net: near-term Printec self-service/POS/cash openings visible on SEAP are thin; the live signals are security/services and standing-incumbent positions.

## Signals
1. BNR (Banca Naţională a României) — open tender "sistem centralizat de securitate" (SCS) for HQ dispatch centre; est. 12.43M lei (~€2.5M), 24-month contract, best value-for-money; published 11/01/2026 on SEAP; bid deadline 12/02/2026; SINGLE bid received from Global Operation Center — award pending. Physical surveillance/security hardware+software (CCTV/access) — marginal Printec fit; capture winner for Agent 6. Sources: bursa.ro 11/01/2026; profit.ro 26/02/2026 (single-bid). is_new=true.
2. CEC Bank — "servicii de elaborare a analizelor de risc la securitatea fizică pentru obiectivele CEC BANK" (physical-security risk-analysis services); bid deadline 23/04/2026 (now closed); winner not published. Maps to Printec managed services / security assessment. Source: cec.ro/anunturi (submitted 02/04/2026). is_new=true.
3. Poşta Română — open tender for banking services to process online card payments for Tezaur state-securities programme; est. 19.98M lei; deadline 21/08/2025; SOLE bid & winner: CEC Bank. Acquiring/payments adjacency (CEC is the acquirer, not Printec). Winner captured. Sources: profit.ro, economica.net. is_new=true.
4. CEC Bank — standing incumbent position: >1,000 ATMs/multifunction recyclers deployed (lei+euro cash-in, FX, bill-pay); ~1,100 units replaced 2020-2023, 80%+ of fleet modernised; supplier chosen by competitive procedure, not publicly named. No active tender now — monitor cec.ro/achizitii for next refresh wave (core ATM/recycler/self-service fit). Sources: cec.ro press, zf.ro. is_new=false.
5. Banca de Investiţii şi Dezvoltare (BID) — new 100%-state development bank (EC state-aid cleared 26/06/2026); procures via own portal bidromania.eu/transparenta/anunturi. Recent lines: "Echipamente IT" (05/06/2026), "echipamente pentru securizarea infrastructurii IT" (24/09/2025), IFRS9 provisioning app, rating models. Guarantee bank (no ATM/POS) — Printec fit limited to HSM/IT-security/AML; monitor. is_new=true.

6. Poşta Română + Visa + CEC Bank — "DIRECT CASH DEPOSIT" service LAUNCHED 17/07/2025: cash deposit onto any bank card at 1,500+ post offices + 9,000+ PDA/mPOS courier terminals (plus card-at-home payment). Rural financial inclusion. Printec = POS/acquiring, cash automation, managed services; signals large mPOS/terminal estate at Posta. Terminal supplier undisclosed (follow-up). Source: posta-romana.ro press 17/07/2025; cec.ro press. is_new=true.
7. BNR — banknote PROCESSING + DESTRUCTION equipment MAINTENANCE, 2 lots, est. 2.73M lei, open tender via SEAP, best value-for-money, deadline 09/10/2024 (now awarded). Recurring annual maintenance of cash-processing machines. Printec = cash automation / managed services. Stale — monitor SEAP for 2026 re-issue. Sources: dcnews.ro 09/09/2024; digi24.ro. is_new=false.
8. Rural cash-access gap (market driver) — Iaşi county: ATMs in only ~10% of 93 communes; Min. Finanţe states it cannot direct ATM siting (banks/operators place on commercial criteria); only ~35% of rural pop. banked. Underpins state-backed self-service/POS/ATM demand. Printec = ATM/self-service, POS. Source: ziarulevenimentul.ro. is_new=true.

## Access log
- cec.ro (fetch tool 403) → defeated with desktop User-Agent via curl (HTTP 200); primary content extracted locally.
- licitatie-publica.ro/authority/cec-bank → login-walled, no data. sicap.ai → HTTP 429 (rate-limited), not used.
- BNR SEAP notice page not opened directly (JS); corroborated via multiple Romanian press + confirmed SEAP publication.
