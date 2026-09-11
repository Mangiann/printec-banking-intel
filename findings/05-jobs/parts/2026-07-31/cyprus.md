# Cyprus — Agent 5 (Early Intent: jobs + leadership) — run 2026-07-31

## Headline
- **Eurobank Limited (ex-Hellenic + ex-Eurobank Cyprus) is the hiring engine of the market**: ~18 live vacancies, of which a 10-role Digital Channels / Digital Banking Engineering cluster posted 15/06–22/07/2026 → PROGRAM, not individual hires.
- **JCC Payment Systems** (the national card processor, ~30 yrs, owned by the Cypriot banks) has 6 live IT/infrastructure roles incl. *Support Engineer – Digital Channels* and *Manager Applications* → PROGRAM.
- **Bank of Cyprus + JCC selected by the ECB for the digital-euro pilot** (ECB PR 14/07/2026; pilot H2-2027, 12 months).
- **Central Bank of Cyprus appointed a new CIO** (Nikolas Anastasiou, ex-Logicom Solutions, 05/06/2026) — follows its Dec-2025 vacancy for Director of the IT Directorate.
- **Alpha Bank Cyprus** put Salesforce Financial Services Cloud live 30/04/2026 across branches + call centre, and reshuffled its ExCo (new CFO June 2026).
- **Zero-vacancy findings**: Bank of Cyprus public careers portal, Alpha Bank Cyprus (no portal at all — CV by e-mail), Ancoria Bank and cdbbank all showed no live public postings on 31/07/2026.

## Structural anchors (Association of Cyprus Banks 2026 data, published 02/07/2026)
| Bank | Branches | ATMs | Employees |
|---|---|---|---|
| Eurobank Limited | 59 | 156 | 2,450 |
| Bank of Cyprus | 56 | 132 | 2,447 |
| Alpha Bank Cyprus | 25 | 26 | 746 |
| NBG (Cyprus) | 2 | 4 | 143 |
| Société Générale Bank Cyprus | 3 | 3 | 113 |
| Ancoria / cdbbank / HFC | 3 / 2 / 5 | 0 / 0 / 0 | 138 / 133 / 83 |
| **Sector** | **155** | **321** | **6,253** |

## Access
- `eurobank.cy` (all pages incl. `/en/group/open-vacancies`) → **Cloudflare 403** to both curl (desktop UA) and WebFetch. Worked around via `cypruswork.com` aggregation + Google-indexed vacancy-code pages (`/open-vacancies/cco2026`, `/doe2026`, `/dsai2026`).
- `carierista.com` → **Cloudflare 403** to both routes.
- `ergodotisi.com` → search results are login-gated.
- Bank of Cyprus SuccessFactors/e-recruitment → gated (public page shows "no vacancies").
- LinkedIn indexes ~12 Bank of Cyprus jobs in Cyprus but blocks bulk fetch.
