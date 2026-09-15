---
name: budget-2026-tab
description: "The Printec group 2026 budget (target revenue, revenue profit, margin by country × product) is joined to the dashboard as a \"Budget 2026\" tab via budget_actions.py; file lives in budget/ (git-ignored); columns confirmed by the user"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9a51b16c-1ba3-43e8-aabe-9882bfb8346d
  modified: 2026-09-11T11:24:31.923Z
---

Started 11/09/2026. The budget file `~/Downloads/BANKING/budget/budget_clean.xlsx` (sheet "BGT 2026 - 2nd Submission", 15 Printec entities, no Czech) has per country → HW/SW/SV/OUT → product subcategory: `Revenue (TR_REV_Total)` = target revenue, `RP_Total` = revenue profit, `RM%` = margin. The user confirmed those meanings on 11/09/2026 (the file has NO actuals-to-date; "pace" waits for an actuals file). Group total €148.7m revenue, €80.4m profit (54%).

Mapping in `weekly-intelligence/references/budget_map.json`: subcategories → the 12 product lines; retail lines (SCO, ECR-POS, store equipment, vending, Vendipack, telecom, printing = €7.7m) and "Other" (€8.0m) are "not covered" (10.6%); 89–91% maps.

`weekly-intelligence/scripts/budget_actions.py` (`compute(root, D)`) is called from inside `build_dashboard.py` on the finished payload and embeds `DASH.budget`; it also writes `intel-cache/budget_actions.json`. Actions per cell: win / find / defend / protect margin / market risk / stretch / watch, chosen by explicit tests, primary = the fired test with most money behind it. Pipeline is never shown as a € ratio against the target (deal bands are multi-year and double-counted across lines).

The tab (`renderBudget` in app.js, nav id `budget`, label "Budget 2026") shows tiles, a markets × lines grid coloured by action, and the ranked action list with drill-down (sigCard for each opportunity). Access (decided 14/09/2026): ONE app, one file, one link. The user rejected a two-file/two-link build ("I don't want to maintain 2 apps") — never propose separate builds again. build_dashboard.py writes budget/budget_actions.json + budget/budget_2027.json (git-ignored) and keeps the budget OUT of dashboard-data.json/data.json; build_artifact.py encrypts them (PBKDF2-SHA256 200k + AES-256-GCM) with the password in budget/budget.password (auto-generated if missing, chmod 600) into `window.__DASH_BUDGET_ENC__`. An "Admin" link at the foot of the sidebar asks for the password, decrypts in the browser (WebCrypto) and adds the Budget tab; locked again on reload.

2027 proposal (11/09/2026): `budget_2027.py` (`compute(root, D)`, called inside build_dashboard after the 2026 join; embeds `DASH.budget_2027`; `main()` also writes `budget/budget_2027_proposal.xlsx` and `budget/BUDGET_2027_PROPOSAL.md`). Growth per cell = market outlook (+std in stretch) + share from open opportunities (band points, capped) − threat haircut; recurring at half market rate; margins held; retail/other flat; base year = 2026 target. Result: base €152.3m (+2.5%), stretch €160.0m (+7.6%). I decided to propose the STRETCH as the 2027 budget with the base as the floor (user asked me to decide). Shown as a fourth section on the Budget tab with a scenario picker.

**Next:** Agent 11 "Budget analyst" brief for the weekly narrative (not yet written); actuals file for pace when available; ask finance what sits in "Other" (€7.6m).
