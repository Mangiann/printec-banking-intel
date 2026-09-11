# Eurobank Holdings (+ Postbank BG, Eurobank Cyprus) — 2026-07-30 (run 5, rebuilt)

Focus: phygital branches, Cash 360 recyclers, AI Factory, FY plan. Languages: EN + EL + BG.

The JSON checkpoint from the earlier attempt in this same run was missing (only the .md
survived), so this pass rebuilt the structured rows from primary sources and pushed into
NEW ground the earlier notes never reached: postbank.bg's own working news feed
(`/en/about-us/news/`), the Eurobank **1Q2026** deck, the Eurobank Limited (CY) **integration
FAQ** on `eurobank.com.cy`, the Cyprus Mail **2024 automated-service-points** story, and the
Bulgarian **CSoft** investment.

## Headline NEW items

1. **Postbank NEXT** — first next-generation phygital branch opened at XOPark, **14/05/2026**.
   Five named zones: Digital Express (self-service), Digital, Interactive, Assisted, and a
   dedicated **Video Consultation** zone. Journey starts at a greeter, passes through
   self-service, reaches a banker only if needed.
2. **Postbank full rebrand, 28/04/2026** (35th anniversary) — explicitly covers the **physical
   branches**, digital channels, apps and all materials, and announces a *network* of Postbank
   NEXT spaces with self-service zones and video consultation. Rollout staged over "the
   following months"; scope/capex deliberately unquantified.
3. **Eurobank Group's Luxembourg Innovation Investment Fund S.à r.l. bought into CSoft**
   (Bulgarian **core-banking** and digital-solutions vendor), **20/05/2026**, size undisclosed.
   A group shareholding in a regional banking-software vendor = captive-vendor headwind on the
   software side of the c.€730m envelope.
4. **Postbank launched fully in-app onboarding with NFC national-ID scanning**, **16/07/2026** —
   remote identification, automated checks, e-signing, active account + digital card in minutes.
   The eKYC slot in BG is now filled; it is a reference to sell into Cyprus, not a BG opening.
5. **Cyprus synergies raised to €140m** (baseline carried €120m), fully phased 2027, **€85m still
   to be captured**, capture 40%/70%/100% across 2025/26/27 — FY2025 deck.
6. **Cyprus core is NOT yet merged** — the bank's own FAQ refers to the coming "phase when
   systems are consolidated and transitioned to the new central banking system". Cross-estate ATM
   withdrawals capped at **€500/txn**; wallets and Mple Rewards still not extended.
7. **Cash 360 layer is now 13 coin + 5 note machines** (was 11+5 in 2022) and the coin-deposit
   routing threshold was cut from **>€200 to >€100**. Plus **unmanned "automated service points"**
   (ATMs + Cash 360 only, 24/7) launched **22/10/2024** in Nicosia, Limassol ×2, Larnaca, Paphos.
8. **Postbank is the only CEE bank on the European Commission's EU AI Act Advisory Forum**
   (22/06/2026), picked from >700 applicants into a ~170-member body alongside OpenAI, Google,
   Microsoft, Anthropic, IBM.
9. **1Q2026 primary network data**: 556 branches / 12,405 staff (4Q25: 562 / 12,408); 143
   wheelchair-accessible ATMs after +3 in the quarter; 184 branches = 69% wheelchair-accessible,
   implying a **c.267-branch** perimeter. **Contradiction logged**: FY25 deck says 144 at 31/12/25.
10. **Bulgaria 185 retail branches + 11 centres** at 4Q25 per the deck — supersedes the
    baseline's 182 + 11.
11. **2Q2026 results still unpublished at 17:34 EEST on 30/07/2026** (call at 18:00). Re-scrape.

## Access / blocks (logged)
- `eurobank.cy/*` → **403 Cloudflare** to curl with a desktop UA, HTML *and* the media PDF.
  Claude-in-Chrome renders the HTML; the **charges PDF opens in Chrome's PDF viewer and cannot
  be text-extracted** → operator item.
- Workaround: **`www.eurobank.com.cy`** (ex-Eurobank Cyprus domain) serves 200 to plain curl —
  the integration FAQ there is the best primary on the CY merger state.
- `eurobankholdings.gr/en/...` 301s to `eurobank.gr/el/omilos`.
- `eurobank.com.cy/sitemap.xml` returns homepage HTML, not XML.
- Eurobank press-office index exposes only ~9 items, no pagination → the 29/06/2026 Banking
  Forward release is unreachable; used Greek press.
- **postbank.bg news IS reachable** at `/en/about-us/news/` (the `/bg-BG/Za-nas/News` path is
  client-rendered and `/en/Za-nas/News/2026/05/...` deep links 404).
- Scratchpad race: another concurrent agent overwrote a shared `fy25.pdf` filename; all Eurobank
  PDFs were re-downloaded into a private subdirectory and re-verified.

## Printec mapping (headline)
- **Bulgaria is the live opportunity this run**: a rebrand touching every branch + a published
  next-gen branch template with a self-service zone and video consultation + 185 retail branches
  + an ATM estate just re-certified for euro. Recyclers/TCRs, kiosks, VTM and managed services.
- **Cyprus is the sharpest cash-automation gap**: 18 bulk-cash machines for the country's largest
  bank, a threshold cut that pushes *more* cash onto them, unmanned sites that depend on them
  entirely, and a core cutover ahead of the 2027 synergy deadline.
- **Greece is largely foreclosed on software** (EY/Microsoft/Accenture/Fairfax, now CSoft) —
  attack the regulated plumbing: eKYC, AML/transaction monitoring, HSM around agentic AI.

## Signal rows — see the JSON checkpoint / structured output.
