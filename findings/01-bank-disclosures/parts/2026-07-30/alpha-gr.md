# Alpha Bank (Greece) — Printec signal scan, 2026-07-30

Slug: alpha-gr. Focus: retail transformation, contactless ATMs, VSS, Siron AML partner.
Method this run: went straight to the alpha.gr Greek press-office index (`/el/omilos/grafeio-typou`) with a desktop
User-Agent, harvested the raw `/-/media/AlphaGr/Files/Group/Press-Releases/2026/*.pdf` hrefs and extracted every
July-2026 release locally with pdfminer.six (venv at /tmp/pdfvenv). That surfaced eight primary releases the
previous runs never saw. Also pulled the Bank of Greece 2025 supervision/AML enforcement numbers, and re-verified
the ATM / APS / online-onboarding product pages and the branch count from alpha.gr directly.

## NEW this run (all primary unless flagged)

- **FinQuest 2026 open call launched TODAY, 30/07/2026; applications extended to 20/09/2026.** Four themes,
  two of which are Printec's home turf: **"Fraud Zero & Digital Trust"** (fraud protection, cybersecurity,
  **digital identity**) and **"Next Generation Customer Experience"** (explicitly names **digital onboarding**,
  conversational AI, hyper-personalisation). Winner: €15,000 + a **pilot in Alpha's real banking environment**;
  6 finalists into an Oct–Nov 2026 accelerator; finalists get direct access to Alpha business/tech decision
  makers and can be picked for pilots regardless of ranking. This is a named, dated, open door into Alpha's
  eKYC / fraud / AML buying centre with a hard deadline.
- **Visa Click to Pay live 14/07/2026 — Alpha is first in the Greek market.** Card data replaced by an
  encrypted token (tokenisation) for debit/credit/prepaid Visa; activation via web/mobile banking.
  Card-not-present tokenisation => HSM / key-management / issuing-security workload.
- **ElevenLabs AI voice agent in the call centre, 09/07/2026 — first bank in Greece at this scale**, with
  stated **gradual expansion to all digital touchpoints**. Natural-language intent routing replaces IVR menus.
  Adjacent to Printec's ATM voice-guidance install base and to self-service channel managed services.
- **EIF / InvestEU agreement 28/07/2026: >€40mn of guaranteed instruments**, incl. **unsecured microloans up to
  €50,000** and social-enterprise liquidity. Small-ticket, high-volume micro-SME lending => remote onboarding,
  eKYC and automated decisioning volume.
- **UniCredit–Alpha cross-border cooperation extended to Bulgaria, 08/07/2026** (senior meeting at UniCredit
  Bulbank HQ, Sofia; "single platform… operate as one coherent team"). Printec is present in Bulgaria.
- **H1 2026 results = TOMORROW, Friday 31/07/2026** (primary financial calendar, 14/05/2026). Imminent trigger.
- **Bank of Greece Annual Preventive Supervision & Resolution Report 2025, published 28/07/2026:** total fines
  **€2,273,325** (banks €1.908mn, servicers €233,400); **one credit institution fined €1,891,050 for 13 AML/CFT
  breaches**; 38 supervisory breaches overall; findings explicitly cite **shortcomings in transaction-monitoring
  systems** and CDD. Institution not named. Direct AML/transaction-monitoring (Siron) prospecting hook.
- **Hard footprint number: 245 branches in Greece** (alpha.gr Branch Network page) — sizes the APS/ATM estate.
- **Retail onboarding 2.0 confirmed primary**: first account opened phone-only, **gov.gr identity certification**,
  ID check by **video call**, instant debit card + digital-banking codes, IRIS payments.
- **Euromoney Awards for Excellence 2026, 20/07/2026**: Best Bank in Greece + Best Bank in Diversity & Inclusion;
  Euromoney calls Alpha "the standout performer in Greece"; marks completion of the 2023–2025 business plan
  (next plan / Investor Day pending).
- **Alpha Way Change Agents Program, 20/07/2026**: 600 employees in the change-agent community, 83 certified
  with Athens University of Economics & Business; MoU signed. Evidence of real transformation-execution capacity.
- **AstroBank (Cyprus) integration in flight**: Alpha Bank Cyprus runs a live "System Integration" FAQ hub for
  ex-AstroBank customers covering Login & Access, Cards, Alpha 360 & SecureCode — full operational integration
  (digital platforms, cards, applications, systems) targeted within 2026.
- **>€100mn/year invested in new technologies, "AI-first" organisation** — press-reported figure (Low), primary
  confirmation not located.

## Carried / re-verified from primary
- **Contactless ATMs**: alpha.gr ATM page confirms tap transactions with card *and digital wallet* (phone /
  smartwatch), cash deposits credited immediately, DCC on foreign-currency cards.
- **APS (Automated Payment Systems) in most branches**: bill payment with cash or contactless card, cash
  deposits to own/third-party accounts with card-based identity verification.
- **VSS completed Feb 2026** (€47mn cost, ~350 departures, ~€15mn annual benefit) — unchanged, no new round found.
- **Retail transformation 31/03/2026**: 5 directorates + 25 regions, branches to advisory/development centres,
  remote branch + customer service centre absorb daily transactions, contactless ATM introduced.
- **Printec = ATM incumbent at Alpha** (voice guidance; instant payments implementation) — Printec blog is
  Cloudflare-403 to both the fetch tool and a desktop-UA curl, so treated as standing background, not re-cited.

## Access log
- `blog.printecgroup.com/...instant-payments...` — 403 to WebFetch, then 403 (Cloudflare error 1034) to curl with
  a full desktop Chrome UA. Not cited this run.
- `bankofgreece.gr/enimerosi/grafeio-typoy/...` — HTTP 200 but the announcement list is JS-rendered; no PDF hrefs
  in the static HTML. Desktop-UA retry did not help. Fell back to Greek press reporting the named BoG report.
- `alpha.gr/en/group/press-office` — 404; the working index is the Greek `/el/omilos/grafeio-typou`.
- Alpha PDFs are image/vector-heavy: WebFetch returns unusable binary; all text extracted locally with pdfminer.six.

## Signal rows — see StructuredOutput.
