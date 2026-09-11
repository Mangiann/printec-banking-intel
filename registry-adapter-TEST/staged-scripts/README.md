# Staged deterministic-layer changes (TEST — not wired to production)

These are the changes the Greece baseline justified: put the registry **only in the deterministic layer**
(verify + fetch), NOT in the discovery-agent briefs. All copies/new files — production
`weekly-intelligence/scripts/` is untouched. Promotion is a human decision.

## Files

### `verify.py` — registry-aware trust pass (copy of production + one change)
- **Diff from prod:** on a dead cited URL (http_error/unreachable), look the domain up in
  `source_access_registry.json` and retry the corrected `final_url`/`best_resource_url`; record
  `repaired_url` + `repair_status`, and a `repaired_via_registry` count in the summary. New optional
  `--registry <path>` arg (defaults to `references/source_access_registry.json`; skips repair if absent).
  Everything else is byte-identical to production.
- **Why:** the pilot cited a Worldline URL that 404'd; the registry already holds corrected URLs.
  Self-healing citations = fewer dead evidence links on the dashboard.
- **How to test:** `python verify.py --root <BANKING> --data <test-cache> --registry ../staged-references/source_access_registry.json`
  then check `verification.json` for `repaired_via_registry` > 0 and per-source `repaired_url`.

### `fetch_diavgeia.py` — NEW Tier-0 Greek sub-threshold tender sweep
- **What:** Diavgeia OpenData `search.json?subject=<term>` (the PILOT-PROVEN param — `q`/`query` are
  ignored). No auth. Writes `intel-cache/greek_tenders_diavgeia.json`. Best-effort (never raises; keeps
  cache on empty), so it slots into `run_weekly.py`'s fetch chain beside `fetch_ted.py`.
- **Why:** fills the below-TED-threshold ΚΗΜΔΗΣ/Diavgeia gap (F2) that the A2 agent kept thrashing on.
- **TESTED (2026-07-23):** 18-month sweep returned **187 decisions**, incl. the Deposits & Loans Fund
  banknote-counting notice (ada Ψ331469ΗΗ7-ΓΦΣ) the pilot found and municipal POS-terminal procurements.
- **KNOWN CAVEAT (access ≠ relevance):** broad terms (`τραπεζ…`, `POS`) also match municipal
  "λογιστική τακτοποίηση προμήθειας τραπέζης" (bank-fee accounting) — noise, not tenders. Add a downstream
  relevance filter (drop `λογιστική τακτοποίηση`; keep `ΠΡΟΜΗΘΕΙΑ … POS/ATM/τερματικ…`) or tighten TERMS
  before trusting the raw list. It's a floor to filter, not a finished feed.
- **To wire in:** add `subprocess.run([py, ".../fetch_diavgeia.py", "--data", data, "--week", week])`
  to `run_weekly.py` next to the `fetch_ted.py` line, and have `ingest.py` read the JSON as A2 candidates.

### `../staged-references/source_access_registry.json`
The registry, copied into `references/` so `verify.py` and the fetchers can read it. **Not** loaded by any
discovery-agent brief (baseline showed no gain there).

## NOT changed (deliberately)
- **Discovery-agent briefs (A1/A5/A6):** left alone — the baseline showed the registry front-end adds
  cost without gain on open-ended work. (The earlier `staged-agent-briefs/` block should NOT be promoted
  for those agents.)
- **`fetch_ted.py`:** the pilot showed a `title~` free-text pass finds notices that CPV-only misses — but
  **F5 (CPV scope) is unresolved**, so no change is staged here; discuss F5 first, then stage a title pass.

## v3 — brought up to EXTRACTION_PLAYBOOK standard (2026-07-23)

After comparing against `~/Downloads/EXTRACTION_PLAYBOOK.md`, both scripts were fixed (now live in production + synced here):
- **fetch_diavgeia.py**: terms/host/country moved to `references/diavgeia_config.json` (§6.6, no country-in-code); positive control before sweep (§6.2); pagination + per-term drop announcement, no silent cap (§6.4); LANDED counts not attempts (§6.3); ~1 req/s + retry-once (§2). Tested: 276 landed, 0 dropped, control 357k.
- **verify.py**: bot-wall marker detection (`__cf_chl`/`hcaptcha`/`recaptcha`/… + HTTP 202) so a captcha page is `blocked`, not stored as healthy `ok` (§2). Tested: clean 200→ok, challenge body→blocked, 202→blocked.
- **Proven the `subject=` filter** per §1 (gibberish→total 0, unfiltered→3.1M).

## v4 — §6.5 consumer wired (2026-07-23)

Correction: the tender caches are NOT read by `ingest.py` — TED/Prozorro are consumed by the **Agent 2 brief**
(`agent-briefs/02-tenders-procurement.md`, the "Scripted Tier-0 caches — read these FIRST" paragraph). So the
right §6.5 wiring is there, not in `ingest.py`. Done:
- **Refresh side:** `run_weekly.py` runs `fetch_diavgeia.py` (already wired).
- **Consume side:** the Agent 2 brief now lists `intel-cache/greek_tenders_diavgeia.json` alongside TED/Prozorro,
  tells the agent to triage it for relevance (drop municipal bank-fee-accounting; keep real ATM/POS/self-service),
  and notes it **closes the previously-documented "Greek Diavgeia needs-Chrome" blind spot** (the OpenData
  `subject=` path works server-side, no Chrome). Brief backed up to `_pre-registry-backup-*/`.

The capability now has a caller on both sides (§6.5 satisfied for this architecture — LLM agent reads the cache,
exactly like TED/Prozorro; the engine never fabricates signals from raw tenders).
