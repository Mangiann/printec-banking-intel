# NLB Komercijalna banka (Serbia) — run 30/07/2026

**Status: complete.** 15 signals, all new or materially changed vs the baseline.

## Headline

1. **NLB Group finalised Group-level tenders for ATMs AND Cash Deposit Machines (CDS) during 2025** — stated in the NLB Group Annual Report 2025, supplier not named. This relocates the buying decision for Serbia's fleet from Belgrade to Ljubljana and is the most actionable fact of the run.
2. **The fleet is 304 ATMs, not "300"** — pulled from the bank's own live locator API. 193 at branches, **111 off-branch (36.5%)**.
3. **102 of the 304 ATMs (34%) cannot accept cash at all.** Meanwhile NBS data shows Serbian ATM *deposit* transactions grew **+31.7% by count and +51.6% by value YoY in Q1 2026**, while withdrawals grew +0.9%. That is the recycler business case, written by the regulator.
4. **A 2030 board commitment to equip ALL Group ATMs with accessibility features**, with the EU digital accessibility directive already in force since June 2025.
5. **The ATM OEM is still not named.** A full-text search of the 17MB Group annual report for fifteen vendor names returned zero hits.

## Estate, from the bank's own locator (30/07/2026)

| Item | Count |
|---|---|
| ATMs | 304 (235 addresses, 133 towns) |
| — at branch addresses | 193 |
| — off-branch | 111 |
| ATMs accepting RSD+EUR cash deposit | 202 (66%) |
| ATMs dispensing EUR | 103 (34%) |
| ATMs accepting merchant takings | 130 (43%) |
| ATMs with QR bill payment | 302 |
| Branch locations listed | 129 (84 towns) — vs **139** reported by NLB Group |
| Branches with a 24/7 self-service zone | 52 (~40%) |
| Branches with a CDS merchant-deposit device | 85 |
| Branches with step-free disabled access | 51 |
| Branches still running a day/night safe (DNT) | 6 |
| Standalone CDS cash-deposit stations | 91 (86 off-branch) |
| Partner merchant locations (instalments) | 1,627 |
| Employees (31/12/2025, Pillar 3) | 2,153 |

## Market context (National Bank of Serbia, updated 01/06/2026)

- Serbia ATMs: **3,336** at end-Q1 2026 (3,265 end-2025; 3,219 end-Q1 2025) — **+3.6% YoY, still growing**.
- POS terminals: **187,957** (+10.3% YoY). Virtual POS: 5,948.
- ATM cash-in Q1 2026: 3,202,644 txns / RSD 151,638m (+31.7% / +51.6% YoY).
- ATM cash-out Q1 2026: 24,793,602 txns (+0.9% YoY).
- NLB KB's 304 ATMs ≈ 9.1% of the national fleet vs a 10.2% asset share.

## Financials

FY2025: assets EUR 6,062.4m, PAT EUR 153.8m, CIR 40.8%, RoE 18.0%, NPL 0.8%, market share 10.2%.
Q1 2026: assets EUR 6,468.6m, PAT EUR 33.0m, CIR 42.8%, gross loans +20% YoY (best in Group).
H1 2026 statutory statements already filed; **NLB Group H1 2026 earnings call 06/08/2026** — re-run this bank right after.

## Other signals

- **>90% of standard services off-branch by end-2026**, restated 19/03/2026 by EB member for operations and IT Bojana Kaličanin-Stojanović; two-thirds of budget allocation to modern technology.
- **SEPA euro payments live 05/05/2026** — same-day execution, immediate crediting → real-time screening / transaction-monitoring load.
- **391,309 active digital users** at 31/03/2026 (Group's 2nd largest); 2026 priorities include NLB Klik relaunch in Serbia, mobile-first biometric onboarding, self-service legal-entity onboarding.
- Video banking outsourced to a third party (**nlb.nexios.io**) on the public site.

## Printec mapping

- **XL**: recycler retrofit of the 102 dispense-only ATMs; call-offs against the 2025 Group ATM/CDS frameworks.
- **L**: managed services for the 111 off-branch ATMs; 24/7 self-service zones for the ~77 branches without one; accessibility retrofit of 304 ATMs by 2030; dual-currency dispense on 201 RSD-only units; smart safes for the 6 DNT branches.
- **M**: AML / transaction monitoring on the new SEPA rails; digital onboarding / eKYC; acquiring across 1,627 merchant sites.

## Open items / operator requests

1. Photograph an NLB KB ATM fascia and welcome screen in Belgrade to read the OEM badge — fastest route to naming the incumbent.
2. Ask NLB Group procurement (Ljubljana) who won the 2025 ATM and CDS tenders, and the framework term.
3. Check NBS supervisory outsourcing / critical-service-provider filings for ATM operation and maintenance.

## Access notes

- nlbkb.rs needs a desktop User-Agent. The working data route is the AEM Sling selector `.../branchsearch.facilities.json` under `/content/nlbbanks/...` (found by grepping the site clientlib JS); `.model.json` and `.branches.json` on the same component return 400, `/bin/nlb/branches.json` returns 404.
- nbs.rs served fine with a desktop User-Agent; statistics taken from the raw `.xlsx` workbooks.
- `pdftotext` is not installed locally — all PDFs extracted with pdfminer.six.
- Unresolved: 129 vs 139 branches; 181 (published PDFs) vs 202 (live locator) deposit-capable ATMs — the locator figure is used, the PDF figure is not reported as fact.
