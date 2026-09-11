# Czechia — NEN (nen.nipez.cz) — ATM/self-service/POS tenders
Run date: 14/07/2026 | Analyst: Printec banking market-research agent | slug: czechia-nen

## Method / coverage
- NEN (nen.nipez.cz) is JS-rendered and not usefully full-text indexed by web search; only one banking-adjacent notice surfaced via search-engine index. Primary discovery therefore ran through the EU TED API (api.ted.europa.eu/v3), filtered to buyer-country=CZE and cash-equipment CPV codes (30123600 money-dispensing/coin machines, 30123500 counting, 30123000, 42961000 payment terminals, 30142000 cash registers), cross-referenced back to Czech buyer profiles.
- Reality check: Czech commercial banks (ČSOB, KB, Česká spořitelna, Moneta, Air/Raiffeisen) are private and do NOT publish on NEN. The only public-sector cash/self-service demand runs through (a) Czech Post (Česká pošta) — which uses the Tender Arena profile, not NEN — and (b) miscellaneous state/municipal buyers on NEN (Prague Castle ticketing/self-service kiosks). CNB uses its own E-ZAK (ezak.cnb.cz), out of NEN scope.
- No genuine bank-ATM / cash-recycler tender exists on NEN this run.

## Signals
1. Správa Pražského hradu (Prague Castle Administration) — NEN N006/25/V00042174 — "Dodávka pokladního systému" = comprehensive cash-register + self-service ticketing kiosk system (cash terminals, self-service kiosks, ticket printers, turnstiles, access control). Open procedure, est. 60,000,000 CZK excl. VAT (~EUR 2.4m). Deadline 05/02/2026 (passed); correction/contract notice re-published on TED 22/12/2025 (854456-2025) and 22/01/2026 (46110-2026); NEN status still "not terminated" (under evaluation, no award notice yet). Printec fit: self-service kiosk / POS / cash-handling — but heritage ticketing, not banking; needs local SI. is_new=true. Win Low, size M.

2. Česká pošta, s.p. — coin-wrapping machines framework ("Dodávky ruličkovaček mincí"), max value 13,000,000 CZK. AWARDED to **Albacon Systems, a.s.** (Czech cash-tech). Award notices TED 69695-2026 (contract concluded 31/12/2025) and 305254-2026 (concluded 31/03/2026). Criterion: lowest price. Portal: Tender Arena (profile "Cp"), not NEN. Competitor capture. is_new=true. size S.

3. Česká pošta, s.p. — coin-sorting machines ("Dodávky třídiček mincí"), value 1,950,000 CZK. AWARDED to **Bankovní technika spol. s r.o.** Award notice TED 468595-2025 (concluded 04/07/2025). Portal: Tender Arena. Competitor capture. is_new=true. size S.

## Baseline re-status
- CNB glass-steel cashier partitions (E-ZAK) — outside NEN; not re-checked here (different portal).
- No other baseline item maps to NEN.

## Winners captured for Agent 6
- Albacon Systems, a.s. — Czech Post coin-wrapping machines (incumbent).
- Bankovní technika spol. s r.o. — Czech Post coin-sorting machines (incumbent).
