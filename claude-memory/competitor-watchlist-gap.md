---
name: competitor-watchlist-gap
description: "Novidea/GRGBanking/TR-SYS were missing from the dashboard's competitors (18/09/2026) because only the vendor agent adds names to references/competitors.json; fixed with a cross-agent candidate scan (competitor_candidates.py) + a triage rule in the Agent 6 brief; ALSO the lesson that build_dashboard.py must NOT be rerun ad hoc (it overwrites dashboard-web/data.json and budget/ files from a stale ingest state)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0bb1fab0-f44e-4aec-8f89-37f3eb288af0
  modified: 2026-09-18T14:10:56.609Z
---

**The gap (found by the user 18/09/2026):** Novidea (local installer and maintainer of Eurobank's 450+ GRGBanking H68V recyclers in Greece, integrated by Transaction Systems / TR-SYS, refresh window 2027–2029) was named twice by the bank-disclosures agent (findings 24/06 and 24/07/2026, "NEW COMPETITOR") but never became a competitor on the dashboard. Reason: the Competition tab is driven by the curated watchlist `weekly-intelligence/references/competitors.json` (name + `detect` tokens, matched against signal texts in build_dashboard.py); only Agent 6 (vendors) adds names, via `scripts/add_competitor.py`, from its own long-tail sweeps and tender winners; it never reads the other agents' findings. Mellon was on the seeded list from day one, so it always lit up.

**Fix 1 (done 18/09):** added Novidea (local-peer, GR, atm_recycling + managed_services, threat Medium), GRGBanking (global OEM, GR, atm_recycling) and Transaction Systems (TR-SYS) (local-peer, GR, atm_recycling + self_service) with the TR-SYS case study as source; watchlist now 164. GRG and TR-SYS match the Eurobank phygital signal; Novidea has a card with its `latest` note only until a signal names it.

**Fix 2 (done 18/09):** `weekly-intelligence/scripts/competitor_candidates.py [--since DATE]` scans every findings/*.md for names next to cues (competitor, incumbent, integrator, installer, maintenance, supplier, awarded to, won by, winner, displace…) that no watchlist detect token matches; filters banks, country adjectives, ordinary words (anything also seen in lower case in the corpus); writes `intel-cache/competitor_candidates.json` + `COMPETITOR_CANDIDATES.md` ranked. Recall over precision: still some noise ("Agent-6", "SZRB"). The Agent 6 brief (`agent-briefs/06-vendors-competitors.md`, section "Triage the cross-agent candidate list every run") now requires running it and triaging each name before the hunt.

**LESSON, important:** to add competitors to the CURRENT published data, patch `intel-cache/dashboard-data.json` (append the vendor with `mention_keys`/`n_mentions` computed the way build_dashboard does, re-sort by threat then mentions, update `active_vendors` and each `matrix` row's `cells`), then COPY it to `dashboard-web/data.json` (that is the file build_artifact.py embeds as `window.__DASH_DATA__`). Do NOT rerun `build_dashboard.py` outside the weekly pipeline: on 18/09 it rebuilt from a stale ingest state (week 2026-08-31, n_new 180, futures 0, model base €149.7m) and overwrote `dashboard-web/data.json`, `weekly-intelligence/data/dashboard-data.json`, `budget/budget_actions.json` and `budget/budget_2027.json`; restored from git HEAD and the OneDrive backup of 16/09 (budget_2027 base 152.88 / stretch 159.76, actions generated 2026-09-07). Sanity checks before any publish: week 2026-09-07, 295 signals, n_new 153, 12 futures, "embedded docs: findings/08-futurist/2026-09-01.md" in the build output, file ≈ 7.9 MB.

Artifact v86 (personal) carries the three vendors; the Printec copy needs a republish. Related: [[banking-collector-project]], [[printec-dashboard-artifact]].
