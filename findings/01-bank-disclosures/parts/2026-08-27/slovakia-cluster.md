# Slovakia cluster — Slovenská sporiteľňa, VÚB, Tatra banka
Run date 27/08/2026 · slug `slovakia-cluster` · status **complete**

## Headline

The Slovak story this window is **two clocks running at once**:

1. **A cash-automation clock at the banks.** SLSP is shrinking branches four times faster than ATMs (140 → 128 branches vs 752 → 733 ATMs in six months to 30/06/2026), while only about a third of its fleet takes deposits. VÚB, by contrast, held its network flat at 163 outlets and has only 150 deposit ATMs. Neither bank's deposit ATMs accept **coins** — a total white space.
2. **A fiscal/POS clock at the tax administration.** Act **384/2025 Coll.** on Revenue Recording took effect 01/01/2026 and, since **01/05/2026**, obliges every eKasa merchant to accept a cashless payment on any sale over **EUR 1**, backed by fines up to **EUR 40,000**. A replacement national platform, **SAFE**, is coming but explicitly *not* in 2026.

The single best piece of news: **PRINTEC SLOVAKIA already holds a valid FR SR eKasa certification** (decision 322095/2025, 20/06/2025 — "Printec eKasa Service v1.2" on SwissBit F6), confirmed on the register valid at 19/08/2026. Diebold Nixdorf s.r.o. is on the same list. Printec can sell into the acceptance mandate today; most rivals cannot.

## Signals

| # | Entity | Signal | Date | Size / Win |
|---|--------|--------|------|-----------|
| 1 | SLSP | ATMs 752 → 733; branches 140 → 128 in H1-2026 | 30/07/2026 | XL / Med |
| 2 | SLSP | 746 ATMs incl. 250 deposit ATMs (infographic) — conflicts with 733 in the KPI table | 30/07/2026 | XL / Med |
| 3 | SLSP | Deposit ATMs take notes only; coins explicitly excluded | 27/08/2026 | M / Med |
| 4 | VÚB | 150 deposit ATMs; 50-note vs 200-note models; coins excluded | 27/08/2026 | L / Med |
| 5 | VÚB | 163 business outlets at 30/06/2026, unchanged since 31/12/2025 | 30/06/2026 | M / Med |
| 6 | FR SR / merchants | Act 384/2025 s.15 — cashless acceptance mandatory above EUR 1 from 01/05/2026 | 01/01/2026 | XL / Med |
| 7 | FR SR / merchants | s.15(3) lets a **third party** supply the QR payment-confirmation means; fines EUR 3,000–40,000 | 01/01/2026 | L / Med |
| 8 | FR SR | New **SAFE** revenue-recording system; go-live "not expected in 2026" | 27/08/2026 | XL / Med |
| 9 | Printec vs Diebold Nixdorf | Both on the FR SR certified eKasa list valid at 19/08/2026 | 19/08/2026 | L / **High** |
| 10 | FR SR | Built-in lifecycle: 2-yr credentials, 2–6-yr CHDU fill, 5-yr certification | 27/08/2026 | M / Med |
| 11 | NBS | National anti-online-fraud coordination platform launched with the Ministry of Interior | 01/12/2025 | M / Med |

## Access issues

- **tatrabanka.sk is fully behind a Cloudflare interstitial** (HTTP 403 "Just a moment…") on every path tried, including `/robots.txt` and `/sitemap.xml`, with a desktop UA, cookie jar and full header set. Claude-in-Chrome was unavailable (extension not connected). **Tatra banka is therefore unresearched this run** — see operator requests.
- VÚB's ATM locator endpoints return only a city list; no machine-readable ATM feed obtained.
- nbs.sk payment-card page carries no current ATM/POS series (latest figure is 31/12/2021).
- slov-lex.sk main portal is JS-gated; resolved via its static mirror.
- The session's WebSearch budget (200/200) was exhausted before this subagent started — all work was direct-fetch plus local PDF extraction.
