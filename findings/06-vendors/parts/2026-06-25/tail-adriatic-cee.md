# Agent 6 — Long-tail & NEW competitors: Croatia/Slovenia + CEE (HR/SI/HU/CZ/SK/AT)
Run date: 2026-06-25 · slug: tail-adriatic-cee

## Method / scope
Read weekly-intelligence/references/competitors.json (~156 tracked names) to dedup. Folded in
intel-cache: ted_notices.json (fresh awards only), prozorro_notices.json (UA-only, 0 in-scope),
competitor_news.json (mostly RO/MD + already-tracked). Then ran local-language discovery searches
(HR/SI/HU/SK/CZ/DE) for soft-POS, independent ATM operators, CIT, RegTech, kiosk, SI/core-banking.
Confidence capped at Medium per rules. No invented figures.

## Headline NEW / CHANGED signals
1. **Slovakia mandatory cashless-acceptance law from 01/05/2026** (delayed from 01/03). Every merchant
   with eKasa must enable a cashless option >EUR1 (card, mobile or QR); fines up to EUR40,000.
   Subsidised-terminal program: apply by **30/06/2026** for 12 months fee-free. Mass demand driver
   for SoftPOS/POS/TMS/QR across SK — accelerates ALL the SK soft-POS issuers (SKPAY, VÚB, ČSOB,
   UniCredit, Slovenská sporiteľňa, Tatra, Payten/Sonet). Threatens Printec Verifone/Castles + TMS
   unless Printec is on the subsidised-terminal supply side.
2. **Croatia national ATM-network initiative (MoF + HNB):** free basic-account package from 01/01/2026;
   two free cross-bank ATM cash withdrawals/month from 01/01/2027. Reshapes ATM economics — pressures
   bank-owned fleets and independent operators (Euronet, Auro Domus). Touches Printec NCR ATM /
   x-core multivendor / ATMaaS positioning in HR.
3. **DISCOVERY — Auro Domus d.o.o. (HR), is_new=true, tier=local-peer:** largest Croatian INDEPENDENT
   ATM network, >600 ATMs (vendor-stated), Zagreb + Adriatic coast, DCC/currency-conversion focus.
   Not in roster. Direct adjacency to Printec NCR ATM + x-core + field/managed services.
4. **DISCOVERY — Hungary soft-POS long tail:** Global Payments Europe (GPE) softPOS, CMO.hu,
   Magyar Telekom Soft POS, K&H POS — plus **qvik** MNB-mandated instant-payment QR scheme (QR/NFC/
   deep-link, bypasses card interchange; Scan&Go app bundles SoftPOS). qvik is a structural POS-
   displacement threat to Printec Verifone/Castles terminal economics in HU.
5. **FINA (HR) coin-counting tender 435583-2026 — NO WINNER / re-tender opportunity.** TED award notice
   (OJ S 120/2026, 25/06/2026): all tenders withdrawn/inadmissible, competition closed. Separate FINA
   "blagajnička oprema" maintenance tender (367642-2026) closes **01/07/2026**. Both map to Printec
   cash-automation/Glory/recycler + field-service lines — open, winnable.
6. **Ondato** (Baltic-HQ eKYC/AML, EU-wide) surfaced as regional RegTech long-tail — not in roster,
   competes with Printec's PARTNER stack (Namirial eKYC / IMTF Siron). Low-confidence as it did not
   surface tied to a specific HR/SI/HU/CZ/SK/AT bank win this week; flagged for roster, not scored high.

## Known-stale / partner exclusions respected
Namirial & IMTF/Siron treated as PARTNERS. Payten/Asseco SEE = competitor (already tracked; their SK
Sonet soft-POS benefits from the SK mandate). Euronet, Aircash, Viva, NBG Pay, SelfPay already tracked.

## Access issues
- ted.europa.eu HTML detail page returned empty to fetch tool (JS); resolved FINA 435583-2026 by
  downloading the TED PDF and extracting text locally via pdfminer → confirmed "No winner was chosen".
- CIT/cash-logistics CZ/SK discovery returned only generic market-report noise; no fresh in-scope new
  entrant found this week (genuine gap — see coverage notes).

## Signal rows — see structured output.
