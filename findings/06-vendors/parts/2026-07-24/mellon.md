# Mellon Group — findings 2026-07-24 (re-run / deepen pass #3)

Target: Mellon Group / Mellon Technologies — DIRECT competitor. Athens HQ; Hyosung TNS + KAL ATM stack reseller (Greece); Ingenico EFTPOS authorized partner; contact-centre/BPO + ATM/POS managed & field services across CEE/SEE + Poland + Ukraine. Read intel-cache/competitor_news.json first (3 cached posts). Re-queried all country wp-json feeds with a desktop UA.

## NEW / CHANGED vs prior file (2026-06-25)

1. **Mellon Serbia — POS acquiring win at Raiffeisen Bank a.d. Belgrade (Ingenico terminals). NEW.** Third Serbian POS-acquiring engagement, not in prior file (prior had only ProCredit POS 12/02 + OTP QMS 18/02). mellon.rs post dated 20/08/2025. Count/value not disclosed. Direct competitor to Printec POS/acquiring in Serbia; shows Mellon consolidating the Ingenico-EFTPOS acquiring channel across multiple Serbian banks (Raiffeisen, ProCredit). Source: mellon.rs. Confidence Medium.

2. **Mellon Bulgaria — Postbank (Eurobank Bulgaria) relationship signal. NEW.** Mellon Bulgaria was "official partner" of Postbank's 35th-anniversary Tennis Gala, Sofia 29/06/2026. Sponsorship, not a contract, but confirms an active Mellon–Postbank BG account (managed services / POS / self-service). Relationship-stability angle for Printec in Bulgaria. Source: mellon.bg. Confidence Medium (relationship inferred), value Low.

3. **Mellon Ukraine ATM stack = Diebold (Opteva), NOT Hyosung. Intel (competitive landscape).** mellon.com.ua/en shows Mellon UA reselling/servicing Diebold Opteva ATMs + recyclers, claims "one of the largest service teams in CESEE." Different stack than Greece's Hyosung/KAL. Relevant to Printec/NCR territory in Ukraine — Mellon competes there on Diebold field services, not Hyosung. Undated (capability page). Source: mellon.com.ua. Confidence Low.

## RE-VERIFIED (carry; not newly changed)
- NBG ~700 Hyosung Series 8 recyclers/dispensers + KAL (K3A app / KTC management) — landmark deal, orig 16/01/2024. mellongroup.com.
- Mellon Serbia QMS at OTP Banka Srbija (60+ branches) 18/02/2026; ProCredit POS acquiring 12/02/2026 — mellon.rs / cache.
- ATM Innovation & Strategy Forum Athens 01/04/2026 (KAL + Brink's); RBI Vienna 20/04/2026; Ingenico Kick-Off 03/03/2026 — homepage.
- EFTPOS base "350,000+ Ingenico deployed / 500,000+ supported, 9 countries"; managed ATM/POS outsourcing offer.

## KNOWN-STALE (not re-reported as new)
- Viddget interactive video-chat partnership = Nov-2018 (search surfaced it as if new; it is old).
- LG Self-Ordering Kiosk partnership = retail/hospitality self-service, undated on Mellon site; LG Gen-2 kiosk line is Aug-2025. Not banking.
- Mellon–Cleveron parcel-locker partnership = Apr-2021.
- Greek NBG staff-leasing labor controversy = 2024 (captured prior pass).
- Group scale proxies (~8,300 staff / €184m staff-leasing rev per bankingnews.gr 18/12/2024) — conflicting press figures, Low.

## Access / coverage notes
- All country wp-json re-queried with desktop UA: mellon.rs OK (no post newer than 18/02/2026; surfaced Raiffeisen POS 20/08/2025 which predates prior file but was never captured). mellon.bg OK (Postbank gala 29/06/2026 newest). mellon.hr + mellon.com.pl wp-json return non-JSON (WAF/redirect) — not resolved this pass. mellon.ro static (2018).
- mellongroup.com/news index JS-only; WebFetch returns shell only. Article slugs render individually. No Chrome MCP driven this pass.
- Did NOT re-run TED / Prozorro this pass (covered prior pass; UA-2025-05-30-001290-a Ukrgasbank Hyosung-servicing winner still UNRESOLVED). Gap.
