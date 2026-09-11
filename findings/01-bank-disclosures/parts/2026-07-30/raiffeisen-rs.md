# Raiffeisen banka a.d. Beograd (Serbia) — run 2026-07-30

## Headline

The single biggest find this run is the bank's **own locator API** (an AEM `maps.viewport.json` endpoint behind
`raiffeisenbank.rs/sr/stanovnistvo/lokacije.html`), which publishes the complete, typed, per-device estate.
As at 30/07/2026 it returns **517 places at 317 locations: 415 self-service devices + 102 branches**, each
device carrying a `subType` and a service list. This replaces every carried estimate with a hard, primary,
re-pullable number.

| Device class (locator `subType`) | Count |
|---|---|
| Višenamenski uređaj (multifunctional) | 240 |
| Običan bankomat (cash-out only) | 125 |
| KUAN (deposit-only, merchant takings) | 50 |
| **Total devices** | **415** |

By function: 204 do RSD **and** EUR deposit+withdrawal (recycler class), 35 do RSD deposit+withdrawal,
125 are cash-out only, 51 are deposit-only. All 364 card-operated units accept contactless.

| Branch service tag | Branches |
|---|---|
| Bezgotovinska filijala (cashless branch) | 36 |
| Višenamenski uređaj inside branch | 97 |
| Blagajna do 13h (half-day till) | 53 |
| Blagajna ceo dan (full-day till) | 13 |
| Kuan uređaj za uplatu pazara | 34 |
| Livix uređaj za uplatu pazara | 14 |
| Cash HUB | 6 |
| Sefovi | 6 |
| **Total branches** | **102** (47 cities) |

## Baseline corrections

- **"41 multifunctional ATMs on x-core"** — superseded. There are **240** multifunctional devices. The Printec
  corporate case page `printecgroup.com/raiffeisen-serbia-branch-transformation/` is still **404**; a Printec
  case-study landing page IS live at `offer.printecgroup.com/raiffeisen-bank-case-study` but the document is
  gated and publishes no counts, dates or hardware vendor. **x-core incumbency scope remains unproven.**
- **"1m active-client target 2026"** — stale. 1m active clients was passed at the 2023 RBA banka (ex-Crédit
  Agricole) merger, alongside "139 locations / 300+ ATMs". Today: 102 branches (−27%), 415 devices (+38%).
- **"iRačun >250k"** — now **>300,000** cumulative openings over five years (bank statement, 20/07/2026).

## Vendor discovery (standing task)

Two cash-automation competitors are named inside the account by the bank's own locator:
- **KUAN** — cash deposit system by **Masterwork Automodules Tech Corp. (Taiwan)**; 50 standalone units + 34 in-branch.
- **Livix** — intelligent banknote deposit system / smart safe by **Vivex Group (Belgrade)**, NBS- and ECB-certified,
  20 notes/sec, 12,000-note capacity; 14 in-branch units.

## Audited 2025 figures (AR 2025, published on raiffeisenbank.rs)

2,084 employees and **102 branches** at 31/12/2025 (2024: 2,049 / 103); total assets RSD 774,123,699k;
profit after tax RSD 29,059,422k; deposit market share 11.5%; corporate credit share 10.2%;
payments 15.5% domestic volume share (#3) and 22.1% international (#2); FX 23% (#1); customers +5.4% y/y.
Digital: ~80% of product sales via digital channels; 78% of retail and 56% of SME acquisitions digital;
iPortal used by 56% of active corporate clients; Premium segment does **97% of its cash transactions on
multifunctional devices**. A full **AI operating model** was established in 2025, "paving the way for scale and
agentic AI in 2026".

## Files

- Checkpoint JSON: `raiffeisen-rs.json` (same directory)
- Working dir: `/private/tmp/.../scratchpad/rbrs/` (`vp.json` = locator dump, `rbrs_ar2025.txt` = AR text)
