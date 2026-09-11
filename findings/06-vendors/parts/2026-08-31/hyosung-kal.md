# Agent 6 — Hyosung + KAL (Kalignite) — run 31/08/2026

Hyosung has no direct European sales arm, so the beat is worked through MELLON (its footprint proxy and KAL's regional partner) plus KAL's own newsroom and Brink's (minority KAL shareholder since 23/06/2025).

## Headlines this run
1. **Mellon jumped into Slovenia and Hungary.** 2025 group accounts (reported 11/08/2026) show revenue EUR 258.82m, EBITDA EUR 14.13m, net profit EUR 6.83m, >9,600 staff — the first verifiable Mellon scale figures, correcting the old "unverifiable" baseline. New wholly-owned Mellon Systems and Services d.o.o. (Ljubljana) and Mellon Hungary LLC (Budapest).
2. **Mellon bought Camelot Sistemi d.o.o. (Zagreb)** for an initial EUR 75,165.60 — a micro queue-management/branch integrator, Fina confirms Mellon Technologies as sole member.
3. **Ukrgasbank Hyosung-servicing tender UA-2025-05-30-001290-a RESOLVED** — SalesServiceSolutions LLC, UAH 1,269,820, no e-system; amendment 27/04/2026 extends to 31/05/2027 and adds a PCI DSS responsibility matrix.
4. **Brink's Q2 2026 (05/08/2026)**: AMS/DRS +14% organic, 14th straight mid-teens quarter, AMS/DRS ~30-32% of revenue. Brink's owns a KAL stake.
5. **KAL newsroom: no new footprint bank.** Latest post 02/07/2026. Active pitch is Windows-11 migration via Kalignite Hypervisor — an explicit attack on ATM hardware refresh.

## Access notes
- SOLVED a long-carried block: mellongroup.com/news has no REST API but the page exposes `news_load_url` = https://mellongroup.com/news/load, which returns JSON when POSTed with the page's `csrf_token` and `page` — full 9-page archive now readable. Latest item 20/06/2026.
- mellon.hr and mellon.com.pl WP APIs now return valid but EMPTY JSON (no posts) — previously logged as WAF blocks.
