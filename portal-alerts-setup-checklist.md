# One-time setup: saved-search alerts on procurement portals

**Why:** the key portals are JavaScript-only, so the automated weekly agent can't search them directly. A saved search with e-mail alerts on each portal closes that gap permanently — new matching tenders arrive in your inbox, and (if you later connect e-mail to Cowork) the weekly agent can read them automatically. ~15–20 minutes total, free.

**Search terms to use everywhere** (adapt to portal language):
ATM / bancomat / bankomat / банкомат · cash recycler · self-service · POS / ПОС терминали / terminale POS · cash-in-transit / chrematapostoles · ATM maintenance.
Where CPV filtering exists, use: **30123200** (ATMs/cash dispensers), 30123000, 30144400, 48000000 (software), 72000000 (IT services).

## Checklist

1. **TED (EU-wide — covers all EU footprint countries)** — ted.europa.eu
   Create a free EU Login account → Advanced Search → filter CPV 30123200 + your countries → "Save search" → enable e-mail notification. One saved search per CPV group is cleanest. (TED also offers daily bulk-data downloads **and a free Search API** — `api.ted.europa.eu/v3` — the weekly agent queries directly without login; see `agent-briefs/02-tenders-procurement.md`. The saved-search alert is the belt-and-braces so nothing is missed between runs.)
2. **Romania — SEAP/SICAP** — e-licitatie.ro
   Free supplier account → "Proceduri de atribuire" search → save filters (keywords: bancomat, POS, self-service; buyers: CEC Bank*, Poșta Română) → activate notifications. *CEC also tenders off-platform at cec.ro/achizitii — no alerts there; the weekly agent already monitors it.
3. **Bulgaria — CAIS EOP** — app.eop.bg
   Free registration → Регистър на поръчките → save search (банкомат, ПОС, самообслужване) → e-mail notifications.
4. **Serbia — Portal javnih nabavki** — jnportal.ujn.gov.rs
   Free account → search "bankomat" → subscribe to notifications; also save buyer-based searches for Banka Poštanska štedionica and JP Pošta Srbije.
5. **Ukraine — Prozorro** — prozorro.gov.ua
   Use a free aggregator account (e.g., zakupivli.pro or smarttender.biz) for keyword alerts on "банкомат", and buyer alerts for Oschadbank (EDRPOU 00032129) and PrivatBank (14360570). Also register at tender.privatbank.ua (PrivatBank's own commercial-tender portal).
6. **Croatia — EOJN** — eojn.hr: save search "bankomat"; buyer: Hrvatska pošta, HPB.
7. **Greece — ΚΗΜΔΗΣ/ESIDIS** (eprocurement.gov.gr): saved search ΑΤΜ / τερματικά POS / χρηματαποστολές. Diavgeia needs no account — the agent reads it via API (e.g., diavgeia.gov.gr/f/elta).
8. **Optional (lower volume):** Cyprus eprocurement.gov.cy · Czechia nen.nipez.cz · Slovakia uvo.gov.sk · Hungary ekr.gov.hu · Slovenia enarocanje.si · Bosnia ejn.gov.ba · N. Macedonia e-nabavki.gov.mk · Albania app.gov.al · Kosovo e-prokurimi.rks-gov.net · Montenegro cejn.gov.me — same pattern: free account → saved search → e-mail alert.

## Leadership-change alerts (free — feeds Agent 5's exec-move tracking)

A new senior executive at a footprint bank is one of the strongest 6–12-month buying signals. Set free
e-mail alerts so these surface automatically:
- **Google Alerts** (free) per major bank, e.g.:
  `"<Bank name>" (appointed OR "Chief Digital Officer" OR CDO OR "Head of Payments" OR "Head of Channels" OR "management board")` — repeat for each anchor bank in `agent-briefs/01-bank-disclosures.md`.
- **Follow** each bank's **LinkedIn** company page (their senior people show "started a new position").
- Bookmark each bank's **Owler** profile (lists current executives + recent leadership changes).
New C-suite / management-board moves then arrive in your inbox; the weekly agent reads them like any other source.

## Page-change watches (free tier — for portals/pages with no native alert)

For the bank-owned procurement pages that publish *outside* the national portals (and have no e-mail alert),
set a free **Visualping** (or similar) page-change watch — a change triggers an e-mail:
- `cec.ro/achizitii` (CEC Bank), `posted.co.rs/o-nama/nabavke.html` (Poštanska štedionica),
  `tender.privatbank.ua` (PrivatBank), `bankofalbania.org` tender notices.
~5 min each on the free tier (a handful of watches).

## What the weekly agent does meanwhile (no setup needed)

Buyer-website monitoring (cec.ro/achizitii, elta.gr, oschadbank.ua, bankofgreece.gr, posta-romana.ro, OeNB/USP, bankofalbania.org tender notices — server-rendered, fetchable directly), Diavgeia and Prozorro open APIs, TED bulk data, and web-search triangulation in local languages — as in `findings/02-tenders/`.

## Note on Claude in Chrome (2026-06-12)

Browser-control from this Cowork session is currently blocked by a permission bug (every navigation auto-denied with no visible prompt despite correct extension settings and completed onboarding). Reported status: pending. If a later app/extension update fixes it, the queued "Chrome sweep" task can fill the award-history gaps (winners, values) in `historical-baseline.md` directly from the portals.
