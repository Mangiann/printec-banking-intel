# Croatia — EOJN (eojn.hr) — tenders run 2026-07-14

Method: EOJN portal is JS-only/401 to fetch + API. Primary route this run = **TED (Tenders Electronic Daily) API** (api.ted.europa.eu/v3/notices/search), which mirrors every above-threshold EOJN notice with full award/winner XML — bypasses the EOJN SPA block. Searched HNB, HP-Hrvatska pošta, Fina buyers + Croatia-wide CPV 30123xxx (cash/coin machines) 2025–2026, EN+HR. Winners parsed from eForms XML.

## NEW / CHANGED signals

1. **HP-Hrvatska pošta €2.5M payment-institution app tender CANCELLED (no winner).** Award notice 21436-2026 (13/01/2026): TenderResultCode `clos-nw`, reason `chan-need` (change of needs); 2 tenders received; est €2,547,010. Baseline had it "winner not announced" → now confirmed abandoned, may re-tender.
2. **Fina coin-counter tender ("Brojači kovanica", CPV 30123620), est €400,000 — CANCELLED / no winner.** CN 273370-2026 (22/04/2026, deadline 22/05/2026); award 435583-2026 (25/06/2026) result `clos-nw`. Genuine Fina cash-automation demand that failed to award → re-tender likely. Direct Printec coin-counting/cash-automation opening.
3. **HNB V-13/2026 Level-3 banknote-authenticity sensors AWARDED to Giesecke+Devrient Currency Technology GmbH, €717,625.20.** VEAT 47656-2026 (22/01) → award 194942-2026 (20/03/2026). Actual value ~2.7× the 264k plan line. Confirms G+D lock on HNB CPS sorter. Agent-6 competitor intel.
4. **HNB V-31/2026 cut-banknote extraction system maintenance AWARDED to EUROKOD PISAČIĆ d.o.o., €152,937.79.** VEAT 173353-2026 (12/03) → award 234073-2026 (07/04/2026). NEW local competitor: Eurokod resells ARCA cash recyclers (CM18), CDS-9 note/coin deposit, Paypod, Lincsafe smart safes, RCS-800 coin recycler — a direct Printec cash-automation rival in Croatia.
5. **HNB CPS banknote processing/destruction maintenance — modification AWARDED to CPS Service and Support Limited, €210,100.05** (282014-2026, 24/04/2026); related open tender "Održavanje ... CPS 7000i" 236172-2026 (07/04, deadline 06/05/2026, now closed). CPS-class kit sole-serviced by CPS Ltd — Printec channel effectively locked out.

## RE-STATUS (unchanged)
- **HNB V-34/2026** banknote-processing system supply+maint (est €1.8M, open, Q4 2026): NOT yet published on TED/EOJN as of 14/07/2026 — still pending, watch Q4.
- HNB smaller cash lines (V-53 €240k, M-24 €60k, V-11 coin-teller €147k): no notice yet.
- Commercial banks (Zagrebačka, PBZ, RBA, OTP, Addiko, Erste): no ATM/POS/self-service EOJN notices — structural (private, procure off-portal). Erste OptiCash footprint = account play.
