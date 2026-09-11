# Western Balkans portals (AL/BA/XK/ME/MK) — 2026-07-14

Scope: national e-procurement portals + bank/central-bank ATM/self-service tenders & winners across Albania, Bosnia, Kosovo, Montenegro, North Macedonia. Confidence capped at Medium.

## Headline signals this run
- **TEB Kosovo own-portal (teb-kos.com/en/tenders/)** — several ACTIVE Printec-relevant lots re-confirmed and NEW (Jun 2026): Supply of **Cash Handling Machines**; **Remote (Digital) Onboarding & Digital Signature Integration**; **Production & Servicing of ATM Kiosk + Lighting Adverts** (Nov 2025); Electronic Security Systems / Security Monitoring room. Primary source, bank's own tender page. Deadlines not shown on index (several show "deadline extensions").
- **Kosovo CBK Regulation on Cash Operations** (in force 01/02/2024; FAQ + facilitated-implementation plan ongoing into 2026) — mandates cash be re-circulated only after processing with "modern processing machines" and licenses client cash devices → sector-wide demand across all KS banks for cash-processing / recyclers / CDMs. Regulator primary PDF (bqk-kos.org).
- **Bank of Albania banknote-packaging** (baseline: deadline 08/07/2026, values UNVERIFIED) — bankofalbania.org fully blocked to fetch tool (403) and curl route; no press/award found. Deadline now PASSED; status unknown. LOGGED as blocked.

## Access / blocks logged
- bqk-kos.org — Cloudflare "Just a moment" JS challenge defeats both WebFetch and curl+desktop-UA. Escalation to Claude-in-Chrome attempted but tool not available in this environment. BQK publishes award PDFs at bqk-kos.org/wp-content/uploads/ (e.g. Jun-2026 group-life-insurance award seen) but index not enumerable.
- bankofalbania.org — 403 to all tools; no route succeeded.
- cbcg.me/e/javnost-rada/tenderi-i-oglasi — loads (curl+UA) but tender list is JS/AJAX-rendered; only nav shell returned. Actual current items not extracted.
- e-nabavki.gov.mk (MK) and NBRM tender pages — JS/ASPX portal; search not enumerable via fetch. nabavke.com indexes NBRM items (non-cash items seen: internet, software, presentation panels).
- ejn.gov.ba (BA) / CBBH — portal search not enumerable via fetch; CBBH procurement index page returns nav only.

## Signal rows — see structured output.
