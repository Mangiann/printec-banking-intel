# Bulgaria — CAIS EOP (app.eop.bg) — 2026-07-14

Focus: post-euro ATM/CDM, recycler, self-service, POS tenders. Euro adopted 01/01/2026.

## Method / access
- app.eop.bg is an Angular SPA (Negometrix); WebFetch + curl (browser UA) return only the "Loading" shell — no server-side content. Logged, then routed via **TED (EU Official Journal) API + notice XML**, which mirrors all Bulgarian above-threshold notices and carries winners/values. This is the primary-source channel that works.
- Structural check via TED CPV filters (30123600 cash dispensers = 0 all-time BGR; POS CPVs = 0 relevant).

## Key findings (all winners captured for Agent 6)
1. **Bulgarian Post euro cash-machine tender — AWARDED to ОБС ТРЕЙД ООД (OBS Trade OOD, Asenovgrad)**. TED 420954-2025 (award, 30/06/2025), contracts signed 10/06/2025. 4 lots to OBS Trade totalling ~2,613,750 BGN: banknote-counters type1 1,160,250 / type2 282,750; coin-counters type1 1,114,750 / type2 56,000. (Original lot 3 "banknote-counting machines" split off under ZOP art.21.) 2 tenderers/lot. Buyer profile app.eop.bg/today/439815. Competitor win — the euro cash-machine hardware wave is DONE.
2. **BNB cash-equipment supply+maintenance — AWARDED to ТЕЛЕСПРИНТ-90 ООД (Telesprint-90 OOD)**. TED 30800-2025 (16/01/2025), contracts 14/01/2025. Lot1 spare parts for G+D **BPS M7** banknote-processing system + Notapack-10 packaging line 71,200 BGN; Lot2 maintenance of **BPS C1-F** banknote counters 96,000 BGN; est. total 177,500 BGN. Reveals BNB runs Giesecke+Devrient BPS gear, serviced by local Telesprint-90. app.eop.bg/today/436403.
3. **Bulgarian Post euro video-surveillance — AWARDED to ЕНИГМА ГАРД ЕООД (Enigma Guard EOOD)**. TED 627866-2025 (award 25/09/2025), contract 17/09/2025, value **6,973,143.10 BGN** (est. 6,983,914.00), 3 tenderers. Scope: supply+install CCTV at post sites doing lev→euro currency conversion. app.eop.bg/today/448929. Recurring security-systems tech-support tenders exist (434380-2025 04/07/2025; 76725-2026 03/02/2026) = managed-service follow-on.
4. **STRUCTURAL: zero ATM/CDM/recycler/self-service/POS public tenders on EOP.** CPV 30123600 = 0 BGR all-time; no POS-terminal notices. BG commercial banks (DSK/OTP, UniCredit Bulbank, Postbank, UBB, Fibank, ProCredit) buy ATM/recycler/POS privately off-portal. Post-euro ATM demand → direct bank BD, not EOP.

Confidence capped at Medium per rules.
