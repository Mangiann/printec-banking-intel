# Alpha Bank (Greece) — Printec signal scan, 2026-08-27

Slug: `alpha-gr`. Focus: H1-2026 results, retail transformation, contactless ATMs, VSS, Siron AML partner.

## Method this run (deliberately different entry points from 30/07)
The 30/07 run stopped one day BEFORE Alpha's H1-2026 results (31/07/2026), so the whole August reporting
cluster was virgin ground. This run went at it four ways:
1. `alpha.gr/el/omilos/Grafeio-Typou/Press-Releases` with a desktop User-Agent — harvested every PDF href and
   pulled the nine releases/corporate announcements dated 30/07–25/08/2026.
2. The **H1-2026 English Semi Annual Financial Report** (4.4 MB) — this is the document the previous runs never
   opened, and it contains a dedicated **"ATM Network & Automated Payment Systems"** section.
3. The **Q2-2026 investor deck**, found by guessing the folder convention
   `/Files/Group/Apotelesmata/2026-Q2/20260731-presentation.pdf` after the IR presentations page proved JS-only.
4. **NEW SOURCE — the Hellenic Bank Association per-bank statistics** (`hba.gr/En/Statistics/List?type=...`),
   which publishes a **bank-by-bank ATM fleet PDF** and a **bank-by-bank branch/personnel PDF**. No previous run
   has ever used these. They give Alpha's fleet count from a third-party primary source and let the
   country-level figure be reconciled against the bank's own disclosure — the reconciliation the baseline
   flagged as never having been done.

All PDF text extracted locally with pypdf (venv at `/tmp/pdfvenv2`); Alpha's PDFs are vector-heavy and
unusable through the fetch tool.

## Headline: the self-service estate is now quantified from two independent primary sources

| Measure | Value | Date | Source |
|---|---|---|---|
| Alpha ATMs in Greece | **1,199** (575 on-site / **624 off-site**) | 31/12/2025 | HBA per-bank ATM PDF |
| Alpha branches in Greece | **249** (HBA definition) / **261** incl. corporate & private banking centres | 31/12/2025 / Q2-2026 | HBA PDF / Q2-2026 deck |
| Alpha personnel in Greece | **5,665** (HBA) / **5,754** (deck, Q2-2026) | 31/12/2025 / 30/06/2026 | HBA PDF / Q2-2026 deck |
| Greek market total ATMs (HBA members) | 5,625 | 31/12/2025 | HBA per-bank ATM PDF |

**52% of Alpha's fleet is OFF-SITE** (624 of 1,199) — more off-site than on-site. Roughly 4.8 ATMs per branch.
Off-site devices are the ones that carry cash-in-transit cost, remote monitoring load and availability risk:
this is the managed-services argument, in Alpha's own numbers.

## NEW this run (all primary)

- **Contactless (NFC) ATM rollout COMPLETED fleet-wide in January 2026; adoption already 30% of all ATM
  transactions.** Availability **97.5%**, +0.5pp YoY. **137 ATM network optimisation studies** completed in
  H1-2026, yielding **ten new off-site ATMs**. ATM transaction volumes stable. Self-service devices called
  "the primary transaction channel within the Bank's branch network". *(Supersedes the baseline's vaguer
  "contactless ATM introduced".)*
- **98% of branches have at least one APS.** Digital channels — which Alpha explicitly defines as
  **"Web, Mobile, ATM, APS"** — carried **98% of total monetary transaction volume**; only 2% at the counter.
- **Cyprus VSS, €17.5m provision in Q2-2026** — the CFO states on the call it is "primarily the envisaged
  restructuring charge for the acquisition of AstroBank". H1-2026 provisions of €64m cover new voluntary
  separation schemes in Greece **and** Cyprus (the Greek leg is the €47m / c.350 FTE Q1 round already known).
  *Corrects the baseline's "VSS completed Feb 2026, no new round found".*
- **Investor Day set for NOVEMBER 2026** — the successor to the 2023–2026 Strategic Plan, i.e. the meeting at
  which the next capex envelope is fixed. FY-2026 EPS guidance raised to €0.41 (+13%).
- **International Customer Onboarding launched in H1-2026** — fully remote account opening for residents of
  Germany, UK, USA, Cyprus and Israel, "with plans for gradual expansion to additional countries".
- **AMLA direct-supervision clock**: selection of up to 40 entities in **2027**, supervision from **2028**;
  Bank of Greece ran a group-level data collection on **15/06/2026** to identify Greek candidates. Alpha fed
  into AMLA's consultations (CDD, ongoing monitoring, business-wide risk assessment) via the HBA.
- **Aegean Bonus Visa FX conversion fee cut from 2% to 0%, 25/08/2026** — relevant because Alpha's ATMs run DCC.
- Alpha Trust squeeze-out completed **24/08/2026** (100% ownership); buyback running since 14/08/2026;
  ExCo reshuffle 30/07/2026 (new Chief of Wholesale Banking from 15/09/2026).

## Re-verified from primary (unchanged)
- ATM capability set on `alpha.gr/en/retail/support-center/atm` (checked 27/08/2026): contactless by card **and**
  digital wallet, immediate-credit cash deposits, DCC, card activation/PIN change, prepaid load, other banks' cards.
- Retail transformation: 25 geographical Regions established March 2026; Chief Retail Distribution Officer
  reporting to the CEO since July 2025; branches moving to advisory.

## Genuine gap
- **Siron / AML vendor NOT confirmed.** No Alpha disclosure, and no public source, names Siron, FICO/Tonbeller
  or any AML transaction-monitoring vendor at Alpha. The H1-2026 report discusses the AML regulatory agenda in
  detail but names no supplier. Treat "Siron AML partner" as an unverified premise, not a fact.

## Access log
- `alpha.gr/en/Group/investor-relations/presentations` — HTTP 200 but deck list is JS-rendered, zero PDF hrefs
  in static HTML. Worked around by guessing the `/Apotelesmata/2026-Q2/20260731-presentation.pdf` convention (200).
- `alpha.gr/en/group/investor-relations/group-results-and-reporting/financial-results-presentations` — 404.
- `alpha.gr/en/Group/the-company/branch-network` and `/en/retail/support-center/branch-and-atm-network` — the
  first is a nav shell with a JS map, the second 404s. Branch count taken from the HBA PDF and the deck instead.
- `alphabank.com.cy/en/astrobank` + `/faqs-migration` — reachable, but carry **no dated** migration milestones.
- `hba.gr` PDF paths contain Greek characters and must be percent-encoded before the GET.

## Signal rows — see StructuredOutput / the JSON checkpoint.
