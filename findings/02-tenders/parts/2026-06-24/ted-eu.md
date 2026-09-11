# TED (EU-wide) — tenders findings (2026-06-24, run 5)

Slug: ted-eu. Portal: Tenders Electronic Daily (ted.europa.eu) — the EU Official Journal supplement for above-threshold public procurement.
Scope: ATM, cash automation, self-service, POS, security, IT-outsourcing across EU footprint.

## Access route map (what works / fails THIS run)
- TED v3 search API: POST-only (GET=405). UI/RSS render JS-empty. Not reachable without operator POST.
- Notice DETAIL pages (ted.europa.eu/en/notice/-/detail/NNNNNN-2026): JS-rendered -> WebFetch returns empty navigation chrome only.
- Notice PDF route (ted.europa.eu/en/notice/NNNNNN-2026/pdf): GET works. WebFetch's extractor CANNOT decompress the PDF streams (returns only metadata + footer emails). BUT the Read tool DOES fully decompress and extract the notice text (confirmed on 99272-2026). So pipeline = find ID -> fetch /pdf to save binary -> Read the saved PDF.
- Claude-in-Chrome: NO browser connected this run (list_connected_browsers = []). Escalation unavailable.
- Finding footprint banking notice IDs is the bottleneck: Google-indexed TED PDFs match the ECB/TED footer BOILERPLATE on every notice, so keyword queries (ATM, cash recycling, Geldausgabeautomaten, currency sorter) surface German/NL/RO municipal construction & utility notices, not banking-equipment subjects. Free-text via Google cannot isolate subject matter.

## Net result this run
No NEW footprint ATM/cash/POS/security banking notice could be reliably enumerated on TED with available tools. Notice IDs read (99272 EE grounds-maint; 235576 BE; 328580/266950/335552 NL; 357390/211740/148660/247411/252716/290743 DE; 82266 RO Distrigaz gas) were all non-banking false positives.

The baseline DELTA items mostly live on NATIONAL portals owned by other agents (Prozorro UA, EOJN HR, E-ZAK CZ, posted.co.rs RS, teb-kos.com XK, bankofalbania.org AL) — they are NOT TED-native, so TED is the wrong portal to re-status them.

## TED-native confirmation (carry-forward award, re-verified via primary source)
- AT — OeNB rural-ATM operation FRAMEWORK with PSA Payment Services Austria GmbH. Primary sources (oenb.at; profil.at "Nationalbank-omaten" 5.5M EUR/5yr; up to ~120 rural ATMs prioritising municipalities with no ATM/branch) confirm STILL CURRENT. Prior pass cited 372,457.40 EUR single-lot figure; the programme-level framework is ~5.5M EUR over 5 years. Printec angle: approach PSA as channel partner for NCR hardware + field service.

## OPERATOR UNBLOCK (biggest lever)
Run a TED expert/POST search (CPV 30123400 cash machines / 30123430 ATMs / 50000000-class maintenance / 30236000; or buyer = central banks) restricted to footprint NUTS codes (BG/RO/HR/CZ/SK/SI/HU/GR/AT/CY), then hand the notice IDs back — the /pdf+Read pipeline will then fully extract each.
