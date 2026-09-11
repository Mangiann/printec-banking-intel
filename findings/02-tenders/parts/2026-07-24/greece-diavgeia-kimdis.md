# Greece — Diavgeia / KIMDIS / ESIDIS — Tenders & Awards (7th run, 2026-07-24)

Scope: Greek bank & public ATM / self-service / POS / cash-automation tenders & awards.
Method this run: read pre-fetched cache `intel-cache/greek_tenders_diavgeia.json` (276 ΚΗΜΔΗΣ/Diavgeia
OpenData decisions, subject= free-text sweep, 12-mo window, generated 2026-07-23), triaged for GENUINE
ATM/cash-automation/POS/self-service procurements, dropped municipal bank-fee accounting
("λογιστική τακτοποίηση") noise, and opened kept rows' doc_url PDFs (extracted locally with pdftotext).
Languages: Greek + English.

## Triage of the 276 cached decisions — mostly NOISE for Printec
- **τερματικά POS (84)**: overwhelmingly commodity single-terminal municipal buys / monthly rentals /
  maintenance from acquirers (Piraeus, NEXI) to collect fees (ports, water utilities, cinemas, consulates).
  Not vendor-procurable hardware. DROP.
- **ταμειακές μηχανές (123)**: fiscal cash-register / IRIS tax-mechanism upgrades under Greek AADE
  e-invoicing mandate — retail fiscal devices, not bank cash handling. DROP.
- **ATM (18)**: mostly irrigation-pipe "10/25 atm" pressure ratings + air-traffic-management "ATM" +
  municipal public-space **lease auctions** to site bank/Euronet ATMs (Alpha Bank Zografou, Bank of Epirus
  Preveza, Euronet Sithonia). No hardware procurement. DROP.
- **αυτοεξυπηρέτησης (13)**: car-wash self-service + military-canteen self-service. DROP.
- **συστήματος πληρωμών (19)**: controlled-parking payment mgmt + state Unified Payment System (ΕΣΥΠ)
  telco-bill settlement. DROP.

## GENUINE cash-automation signals (Printec cash-automation / recyclers + managed services) — all is_new
1. **Ταμείο Παρακαταθηκών & Δανείων (TPD / Consignment Deposits & Loans Fund — state credit institution)**
   — commitment decision €1,612.00 for **2 banknote-counting machines** for its **Thessaloniki branch**.
   ADA Ψ331469ΗΗ7-ΓΦΣ, 16/07/2026 (approval 9ΥΨΗ469ΗΗ7-ΦΛΤ, 10/07/2026). Small ticket but genuine
   state-bank branch cash-automation account.
2. **ΕΛΤΑ / Hellenic Post S.A.** — recurring **maintenance of banknote-counting machines** across the postal
   financial network. Confirmed PDF (ADA 9ΠΦΕΟΡΡ2-0ΒΟ, 17/07/2026): repair of **Glory CashDNA TN10** units
   at Kassandreia/Lykovrysi/Mytilene, invoice €1,113.15 incl VAT. Installed base also includes **SCANCOIN**
   (Patra) and **NC6500** (Heraklion). Incumbent supplier = **BOOS S.A.** (Συστήματα Οργανώσεως Τραπεζών
   Γραφείων Α.Ε.) under supply contract Φ.Π. 6276/2016. Competitive intel: BOOS is the entrenched Greek
   bank cash-automation vendor; ELTA's ageing counter fleet = replacement pipeline (ties to the ELTA
   interbank-ATM/counter plan tracked in prior runs).
3. **Μουσείο Ακρόπολης / Acropolis Museum** — direct award of **1 Ratiotec Rapidcount X 600F** 2-pocket
   mixed counting/sorting (fitness + counterfeit detection) counter, €1,500 machine (+€132 calculators),
   total €1,632 +24% VAT. ADA 95ΧΝ469ΗΤ0-ΧΝΧ, 15/07/2026. Minor cultural buyer; competitor = Ratiotec.

## Competitor landscape confirmed in Greek cash-counting (Printec displacement targets)
Glory (CashDNA), Scancoin, De La Rue/Kisan (NC6500), Ratiotec — supplied/serviced via BOOS S.A. and similar.

See structured output for signal rows.
