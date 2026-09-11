# Mellon Group — findings 2026-07-15 (re-run / deepen pass #3)

Target: Mellon Group / Mellon Technologies — DIRECT competitor, tier: regional. Piraeus/Athens HQ; Hyosung TNS + KAL ATM stack reseller; Ingenico EFTPOS authorized partner.

## Method / coverage
- Swept all four WordPress country feeds `/wp-json/wp/v2/posts?per_page=20`:
  - mellon.rs: latest = 18/02/2026 (QMS OTP) — no post since 25/06. (Newly-noticed older post: Raiffeisen Serbia Ingenico POS, 20/08/2025 — was NOT in prior file.)
  - mellon.bg: **ONE NEW post 29/06/2026** — Postbank 35-yr tennis gala sponsorship.
  - mellon.hr: wp-json empty/static — no posts.
  - mellon.ro: only 2018 static service pages — no post since 25/06.
- mellongroup.com JS-only; article slugs render via WebFetch. Checked Bulgaria-Hyosung (03/06/2024, standing), Romania Hyosung/KAL (06/10/2025, baseline), NBG landmark (16/01/2024, standing), "urgent notice" (27/07/2023, standing fraud alert).
- English + Greek + local searches (Serbian/Bulgarian/Romanian). No NEW named-bank Hyosung/KAL/POS win surfaced since 25/06.

## NEW / CHANGED vs prior file (25/06)
1. **Mellon Bulgaria × Postbank — 35-yr anniversary tennis gala sponsor (29/06/2026), NEW.** Mellon.bg post: Mellon Bulgaria is Postbank's "long-standing technology partner"; GM Borislav Arsov cites partnership "built on trust, technological excellence." No contract/hardware named — event PR. Confirms Mellon's entrenchment at Postbank Bulgaria (Eurobank BG, a top-4 BG bank). Threat to Printec BG ATM/POS/cash-automation ambitions. is_new=true. Confidence Low (sponsorship PR, no deal).

## STANDING / newly-noticed context (is_new=false)
2. **Raiffeisen Serbia — Mellon Ingenico POS terminals (mellon.rs, dated 20/08/2025).** Not in prior file. Raiffeisen Serbia is a Printec x-core (multivendor ATM software) reference customer — Mellon holds the POS acquiring/terminal side there. Competitive-overlap threat at a shared account. [STANDING — dated 2025]
3. **Scale proxies now conflict/updated:** search snippets state "14 countries / 9,000 people" and "11 countries / ~€240m revenue last year" (wall-street.ro) vs prior "8,300 emp / €184m staff-leasing" (bankingnews 2024). Rough proxies only, no filing. Confidence Low.
4. NBG ~700 Hyosung Series 8 + KAL (K3A/KTC) — carry, 16/01/2024 [STANDING].
5. Mellon Romania Hyosung TNS + KAL portfolio launch 06/10/2025 (wall-street.ro advertorial; no named bank) [STANDING — baseline].
6. Mellon Bulgaria Hyosung Series 8 showcase Sofia 03/06/2024 ("building on Poland + Greece integrations"; euro-adoption rationale) [STANDING].

## Access notes
- mellon.hr & mellon.ro wp-json = static/empty (no newsroom). mellon.bg & mellon.rs feeds OK, no auth.
- mellongroup.com/news index still JS-only; individual article slugs render via WebFetch.
- No fresh TED/Prozorro Mellon/Hyosung award resolved this pass; UA Hyosung-servicing tender winner still unresolved (needs operator/Chrome).
