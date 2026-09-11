export const meta = {
  name: 'full-scout-round',
  description: 'DETERMINISTIC orchestrator for one complete source-discovery round: discovery -> ingest (incl. the CODE recovery rungs) -> browser recovery rung -> prepare labels -> labeling -> finalize, IN FIXED ORDER. The control flow is code (no agent decides what runs); only what discovery FINDS varies. Hand-offs are files on disk.',
  phases: [
    { title: 'Discover', detail: 'the discovery swarm writes candidate slices to disk' },
    { title: 'Ingest', detail: 'round_ingest.py: merge slices, validate, HEAD-verify, then the CODE recovery rungs (GET + WAF handshake)' },
    { title: 'Repair', detail: 'an agent walks the FULL recovery ladder (web search + real Chrome) over whatever the code rungs could not settle' },
    { title: 'PrepareLabels', detail: 'round_prepare_labels.py: fold the browser verdicts in, rebuild labeling batches on FINAL liveness' },
    { title: 'Label', detail: 'the labeling swarm writes role+decision slices to disk' },
    { title: 'Finalize', detail: 'round_finalize.py: merge labels, route, sync registry, write the check-by-hand list, report convergence' },
  ],
}

const REPO = 'C:/Users/User/Dropbox/E - PRINTEC GROUP/AI/MARKET RESEARCH/Strategic Intelligence - Banking and Payments'
const DISCOVERY_JS = `${REPO}/routines/source_discovery_scout/discovery_workflow.js`
const LABELING_JS = `${REPO}/routines/source_discovery_scout/labeling_workflow.js`
const PY = 'PYTHONIOENCODING=utf-8 python'

// INPUTS (args): { run_id, config_path, promotion_db, data_root, country, country_name, sector,
//                  workstreams[], topics[], languages[], min_cells, max_cells }
let a = args
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }
const cfg = (a && typeof a === 'object') ? a : {}
const runId = cfg.run_id || 'dr_gr_a2_live_004'
const dataRoot = cfg.data_root || `${REPO}/data`
const configPath = cfg.config_path || `${REPO}/configs/discovery_runs/gr_a2_tenders_procurement.yaml`
const promotionDb = cfg.promotion_db || `${REPO}/data/promotion.db`
const countryName = cfg.country_name || 'Greece'
const scopeLabel = `${countryName} - banking AND payments - ${(cfg.workstreams || ['A2']).join(',')} - ${(cfg.topics || ['tenders', 'procurement']).join(', ')}`
const ai = `${dataRoot}/run_logs/${runId}/agent_inputs`

const INGEST_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['ok', 'still_unreachable'],
  properties: { ok: { type: 'boolean' }, ingested: { type: 'number' }, failed_urls: { type: 'number' },
               still_unreachable: { type: 'number' } },
}
// browser_ok is REQUIRED: the agent must state whether Chrome actually worked. Without it, a Chrome-less
// agent can report all-zeros and the round looks clean while every false-dead survives.
const RECOVERY_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['browser_ok', 'verified', 'repaired', 'dead'],
  properties: { browser_ok: { type: 'boolean' }, verified: { type: 'number' }, repaired: { type: 'number' },
               dead: { type: 'number' }, unresolved: { type: 'number' }, note: { type: 'string' } },
}
const PREP_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['batch_files'],
  properties: { batch_files: { type: 'array', items: { type: 'string' } },
               browser_verdicts_folded: { type: 'number' }, still_unreachable: { type: 'number' } },
}
const FINALIZE_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['deliverable'],
  properties: { deliverable: { type: 'string' }, convergence: { type: 'object', additionalProperties: true }, note: { type: 'string' } },
}

// ── Discover ──────────────────────────────────────────────────────────────────
phase('Discover')
const discArgs = {
  country: cfg.country || 'GR', country_name: countryName, sector: cfg.sector || 'both',
  workstreams: cfg.workstreams || ['A2'], topics: cfg.topics || ['tenders', 'procurement'],
  languages: cfg.languages || ['el', 'en'], min_cells: cfg.min_cells || 20, max_cells: cfg.max_cells || 32,
  run_id: runId, data_root: dataRoot,
}
const disc = await workflow({ scriptPath: DISCOVERY_JS }, discArgs)
log(`discover: ${disc && disc.scouts_ok} scouts wrote slices (~${disc && disc.candidates} candidates)`)

// ── Ingest (deterministic Python, run by a bash agent that just executes one command) ──
// round_ingest HEAD-verifies every URL and then runs the CODE recovery rungs (a real GET, then a WAF
// handshake with cookies) automatically — no browser, no agent. Whatever they cannot settle is written to
// remaining_failures.json for the browser rung below. still_unreachable tells us whether the browser is
// even needed this round.
phase('Ingest')
const ingest = await agent(
  `Run EXACTLY this ONE command from the repo root and WAIT for it to finish — it can take ~15-20 minutes ` +
  `because it HEAD-verifies every URL AND runs the code recovery rungs over the network (be patient; if the ` +
  `Bash timeout is too short, run it in the background and poll its output file until it prints its JSON ` +
  `summary). Do NOT change any files yourself.\n\n${PY} "${REPO}/scripts/round_ingest.py" --run-id ${runId} ` +
  `--config "${configPath}" --data-root "${dataRoot}" --promotion-db "${promotionDb}"\n\n` +
  `When it finishes, report from its JSON summary: ingested, failed_urls, and failed_after_code_recovery as ` +
  `still_unreachable. ok=true iff the command printed its summary.`,
  { schema: INGEST_SCHEMA, label: 'ingest', phase: 'Ingest', agentType: 'general-purpose' })
const stillUnreachable = (ingest && ingest.still_unreachable) || 0
log(`ingest: ${ingest && ingest.ingested} candidates, ${ingest && ingest.failed_urls} failed URLs, ${stillUnreachable} still unreachable after the code rungs`)

// ── Repair: the AGENT recovery rung — the FULL ladder (web search + real Chrome) ──────────────────────
// The code rungs already ran in Ingest. This rung investigates only what they could not settle
// (remaining_failures.json). It does EVERYTHING it can to reach a source — WebFetch, WebSearch, and a real
// Chrome — because "a failed fetch is a hypothesis, not a verdict". CRITICAL: if there ARE still-unreachable
// URLs but Chrome cannot be reached, the round STOPS and alarms rather than silently skipping (that silent
// skip is exactly what locked ~1,381 live sources out of the registry).
phase('Repair')
let recovery = { browser_ok: true, verified: 0, repaired: 0, dead: 0, unresolved: 0 }
if (stillUnreachable > 0) {
  recovery = await agent(
    `You are the AGENT recovery rung of a source-discovery round. Deterministic code rungs already recovered ` +
    `everything a plain web request could; you handle the hard residue. Do EVERYTHING you can to reach each ` +
    `source — you have WebFetch, WebSearch, AND a real Chrome (claude-in-chrome MCP).\n\n` +
    `LOAD CHROME FIRST and PROVE it works: ToolSearch select:mcp__claude-in-chrome__tabs_context_mcp,` +
    `mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp — ` +
    `then create your own tab and open ONE url and read it. If the MCP tools are unavailable or Chrome cannot ` +
    `open a page, set browser_ok=false and STOP immediately (do the WebFetch/WebSearch rungs if you like, but ` +
    `you MUST report browser_ok=false). NEVER invent results, NEVER report zeros as though the work were done ` +
    `— a silent no-op here locks live sources out of the registry, which is the exact bug this rung exists to ` +
    `prevent.\n\n` +
    `INPUT: read ${ai}/remaining_failures.json — {candidate_id, source_url, http_status}. Work through EVERY ` +
    `item, walking the ladder and STOPPING at the first rung that resolves it:\n` +
    `  1. WebFetch/open the url. Real relevant content renders (a 403/challenge that then settles is LIVE) -> "verified".\n` +
    `  2. 404 -> the page MOVED. Read the site root nav / sitemap.xml for the section; or use the site's search. Found -> "repaired" + corrected_url.\n` +
    `  3. Still lost -> WebSearch (site:domain topic, or the org name + topic). Found -> "repaired" + corrected_url.\n` +
    `  4. Entity doubt -> WebSearch the ORGANISATION: renamed/merged/acquired/wound-down? Successor with the equivalent page -> "repaired" + successor. Genuinely gone -> "dead" + grade_of_dead + successor.\n` +
    `  5. Bot-defended and you cannot confirm content, but the site is clearly live -> "unresolved" (NOT dead).\n\n` +
    `RULES: NEVER "verified" without SEEING real content. NEVER "dead" just because a fetch failed — "dead" needs ` +
    `evidence the org/resource is genuinely gone; when unsure use "unresolved". NEVER solve a CAPTCHA (-> "unresolved", ` +
    `note "captcha"). A wrong "dead" permanently locks out a live source.\n\n` +
    `WRITE a TOP-LEVEL JSON ARRAY to ${ai}/browser_recovery_results.json, one object per candidate_id: ` +
    `{"candidate_id","outcome":"verified|repaired|dead|unresolved","corrected_url"(only if repaired),` +
    `"grade_of_dead":"moved_unknown|rebranded|merged|wound_down|defunct"(only if dead),` +
    `"successor":{"name","url"}(if found),"ladder_step":1-5,"evidence":"one line of what you actually saw"}.\n\n` +
    `Then report browser_ok plus the verified/repaired/dead/unresolved counts.`,
    { schema: RECOVERY_SCHEMA, label: 'agent-recovery', phase: 'Repair', agentType: 'general-purpose' })
  log(`repair: browser_ok=${recovery && recovery.browser_ok} — ${recovery && recovery.verified} verified / ${recovery && recovery.repaired} repaired / ${recovery && recovery.unresolved} unresolved / ${recovery && recovery.dead} dead`)

  // HARD ALARM + HALT: there was browser work to do and Chrome did not respond. Do NOT continue past this
  // point on incomplete recovery — drop the ACTION-NEEDED file, print the banner, and stop the round. It is
  // fully resumable: re-running skips discovery/ingest and retries this rung once Chrome is up.
  if (recovery && recovery.browser_ok === false) {
    await agent(
      `Run EXACTLY this ONE command and report done=true when it prints its banner:\n\n${PY} ` +
      `"${REPO}/scripts/round_alarm.py" --run-id ${runId} --country "${countryName}" --reason chrome_unreachable ` +
      `--detail "${stillUnreachable} source URL(s) still need the browser and Chrome did not respond."`,
      { schema: { type: 'object', additionalProperties: true, required: ['done'], properties: { done: { type: 'boolean' } } },
        label: 'alarm', phase: 'Repair', agentType: 'general-purpose' })
    throw new Error(`ROUND HALTED: Chrome unreachable with ${stillUnreachable} URL(s) still to check. ` +
      `An ACTION NEEDED file was written to deliverables/. Enable Chrome and re-run this round to resume.`)
  }
} else {
  log('repair: skipped — the code rungs reached everything; no browser work needed')
}

// ── PrepareLabels: fold the browser verdicts in, rebuild labeling batches on FINAL liveness ────────────
phase('PrepareLabels')
const prep = await agent(
  `Run EXACTLY this ONE command from the repo root, WAIT for it, then report batch_files (from its JSON ` +
  `summary), browser_verdicts_folded and still_unreachable. Do NOT change any files yourself.\n\n${PY} ` +
  `"${REPO}/scripts/round_prepare_labels.py" --run-id ${runId} --config "${configPath}" ` +
  `--data-root "${dataRoot}" --promotion-db "${promotionDb}"`,
  { schema: PREP_SCHEMA, label: 'prepare-labels', phase: 'PrepareLabels', agentType: 'general-purpose' })
const batchFiles = (prep && Array.isArray(prep.batch_files)) ? prep.batch_files : []
log(`prepare labels: folded ${prep && prep.browser_verdicts_folded} browser verdicts, ${prep && prep.still_unreachable} still unreachable, ${batchFiles.length} label batches`)

// ── Label (swarm writes slices) ──────────────────────────────────────────────────
phase('Label')
const lab = await workflow({ scriptPath: LABELING_JS },
  { batch_files: batchFiles, scope: scopeLabel, run_id: runId, data_root: dataRoot })
log(`label: ${lab && lab.labeled} labels across ${lab && lab.batches} batches`)

// ── Finalize (deterministic Python) ──────────────────────────────────────────────
phase('Finalize')
const fin = await agent(
  `Run EXACTLY this ONE command from the repo root and WAIT for it to finish, then report its JSON summary ` +
  `(the convergence object and the deliverable path). Do NOT change any files yourself.\n\n` +
  `${PY} "${REPO}/scripts/round_finalize.py" --run-id ${runId} --config "${configPath}" ` +
  `--data-root "${dataRoot}" --promotion-db "${promotionDb}"`,
  { schema: FINALIZE_SCHEMA, label: 'finalize', phase: 'Finalize', agentType: 'general-purpose' })

log(`finalize: deliverable -> ${fin && fin.deliverable}`)
return { run_id: runId, discover: disc, ingest, recovery, label: lab, finalize: fin }
