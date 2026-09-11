# Banca Transilvania (Romania) — run 2026-07-30

Fresh run (no prior checkpoint for this runDate). Focus: annual capex (IT/digital), self-banking machines, OTP RO merger, POS.

## Access note
`www.bancatransilvania.ro` serves a bot-block HTML page (HTTP 403) to both the fetch tool and curl with a desktop User-Agent. The **identical** files are returned HTTP 200 from the language subdomains `it.` / `en.` / `hu.bancatransilvania.ro` (same `/files/app/media/...` paths). PDFs were downloaded there and text-extracted locally with pdfminer. The 20 MB 2025 annual report was also mirrored on bvb.ro.

## Headline numbers found

| Metric | 31/12/2024 | 31/12/2025 | 31/03/2026 |
|---|---|---|---|
| Units in network | 513 | 531 | 522 (ASF table) |
| ATMs | 1,937 | 2,031 | 2,025 |
| of which multifunctional (MFM) | 651 | 696 | 696 |
| BT Express terminals | n/d | 577 | 632 |
| Installed POS | 148,000 | 178,414 | >188,000 |
| Cards | 7,172,201 | 8,145,668 | 8.2m |
| Unique digital users | 4,435,953 | 4,928,070 | 5.0m |

Baseline said ~1,800 ATMs / 550+ MFM / 470+ BT Express / 177,000 POS — all superseded.

### 2026 investment budget (RON m, incl. VAT; AGM 28/04/2026; planning rate 5.17 RON/EUR)
Buildings 105.94 · IT & cards 663.17 (IT hardware 34.23, IT software 407.82, retail & cards 221.11 = HW 51.92 + SW 169.19) · **Machines 21.39** · Security 9.79 · **Cash-processing centre 7.88** · Digital initiatives 177.22 · Other 32.00 · **Total 1,017.40** (+20.6% vs 2025 budget).

### Other
- ROBOR cartel: Competition Council fined BT **RON 875.74m** in its own name plus **RON 85.03m for OTP Bank România's conduct** (inherited via the merger) — total RON 960.77m, ~94% of the whole 2026 capex budget. BT is appealing to the Bucharest Court of Appeal. Sector total RON 3.73bn / 10 banks.
- BT **Investor Day 01/10/2026**; H1-2026 results 21/08/2026, call 24/08/2026.
- 02/07/2026: first AI-agent-initiated card payment in Europe with Visa (Visa Intelligent Commerce / Agentic Ready pilot), at Brick Depot LEGO Certified Store.
- Victoriabank (Moldova): 67 units, 269 ATMs, 10,574 POS, 635,089 cards, 6,061 merchants at 31/12/2025.
- Romania market (BNR, 31/12/2025): 11,136 ATMs, 729,408 POS, 685,731 EFTPOS, 28.63m active cards → BT ≈18% of ATMs, ≈24% of POS.

See the JSON part file for the structured signal rows.
