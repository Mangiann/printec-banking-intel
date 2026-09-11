// ============================================================================
// verify-checkpoints.workflow.js — RECOVERY harness for Agents 1-6
// ============================================================================
// WHY: research-harness.workflow.js checkpoints each unit's RESEARCH to
// parts/<runDate>/<slug>.json before the Verify phase runs. When a run dies on
// an API session limit, that research survives on disk but never gets
// adversarially verified, so the harness (correctly) reports the unit as EMPTY
// and the work is invisible. On 30-31/07/2026 that cost 22 units / ~330
// researched signals across three separate limit hits.
//
// WHAT: one agent per unit that READS the existing checkpoint and does ONLY the
// adversarial verification pass — no re-research, so it costs a fraction of a
// full harness run. Each agent WRITES its own verified output to
// parts/<runDate>/verified/<slug>.json BEFORE returning, so partial progress
// survives the next limit hit. Rendering is done downstream in Python.
//
// ARGS: { runDate, partsDir, slugs[], rules? }
// ============================================================================

export const meta = {
  name: 'verify-checkpoints',
  description: 'Adversarially verify research checkpoints left on disk by a harness run that died mid-flight',
  phases: [
    { title: 'Verify', detail: 'one agent per unit: read checkpoint, fact-check every claim against primary sources, write verified JSON to disk' },
  ],
}

let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const RUN_DATE = A.runDate || 'UNDATED'
const PARTS = A.partsDir || ''
const SLUGS = Array.isArray(A.slugs) ? A.slugs : []
const RULES = A.rules || 'HARD RULES: never invent numbers/dates/values; cite every claim with source name + stable URL + date (DD/MM/YYYY); confidence caps at Medium; explain jargon in plain language.'

const SIGNAL_PROPS = {
  entity:      { type: 'string' },
  country:     { type: 'string' },
  signal:      { type: 'string' },
  source_name: { type: 'string' },
  source_url:  { type: 'string' },
  source_date: { type: 'string' },
  source_tier: { type: 'string', enum: ['primary', 'regulator', 'press', 'aggregator'] },
  implies:     { type: 'string' },
  likelihood:  { type: 'string' },
  confidence:  { type: 'string', enum: ['Medium', 'Low'] },
  opp_size:    { type: 'string', enum: ['XL', 'L', 'M', 'S', 'Unscoped'] },
  win:         { type: 'string' },
  followup:    { type: 'string' },
  is_new:      { type: 'boolean' },
  verification:  { type: 'string', enum: ['confirmed', 'partially-confirmed', 'unconfirmed', 'contradicted'] },
  verifier_note: { type: 'string' },
  keep:          { type: 'boolean' },
}
const REQ = ['entity', 'country', 'signal', 'source_name', 'source_url', 'source_date', 'source_tier',
  'implies', 'likelihood', 'confidence', 'opp_size', 'win', 'followup', 'is_new',
  'verification', 'verifier_note', 'keep']

const SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    slug: { type: 'string' },
    verified_signals: { type: 'array', items: { type: 'object', additionalProperties: false, properties: SIGNAL_PROPS, required: REQ } },
    residual_gaps: { type: 'string' },
    wrote_file: { type: 'boolean', description: 'true once the verified JSON has been written to disk' },
  },
  required: ['slug', 'verified_signals', 'residual_gaps', 'wrote_file'],
}

function prompt(slug) {
  return `You are the adversarial VERIFIER for Printec banking market intelligence, run ${RUN_DATE}, unit "${slug}".

A previous research pass already collected signals for this unit but was killed by an API session limit before verification could run. Its output is on disk at:
  ${PARTS}/${slug}.json
(a JSON object with a "signals" array; also "coverage_notes", "access_issues", "operator_requests").

STEP 1 — Read that file (Read tool, or Bash cat if large).

STEP 2 — For EVERY signal, independently fact-check it against a PRIMARY source. Do not take the researcher's word for anything.
- Open the cited URL. If it 404s / is JS-blocked / is a PDF, try: the API, a desktop-User-Agent curl, a Google cache or site: snippet, then the bank's own IR page. Log what failed.
- Check the FIGURE: does the source actually state that number, for that date, on that basis? Fleet counts are the usual failure — sites vs machines, group vs country, ATMs vs ATMs+kiosks.
- Check the DATE: the Date must be the most-recent TRIGGERING development, never an old backstory or incumbency date. Anything >6 months old with no concrete future trigger (deadline, go-live, tender, deal close within ~18 months) must be re-tagged in the signal text as "[STANDING — dated YYYY]" and must NOT be presented as new. Set is_new accordingly.
- Set verification: "confirmed" (primary source states it), "partially-confirmed" (directionally right, detail off — CORRECT the figure in the signal text and say so in verifier_note), "unconfirmed" (could not reach an independent source — drop confidence to Low), "contradicted" (the source says something materially different — CORRECT it, and set keep=false ONLY if the claim is fabricated or the corrected version is worthless).
- verifier_note: state what you actually checked and what you found, including the corrected value + source when you changed something.

STEP 3 — Keep the Printec framing intact: implies / likelihood / opp_size (XL >=~EUR 5m or footprint-wide, L ~1-5m, M ~0.2-1m, S <~0.2m, Unscoped for a threat/macro driver) / win / followup. Confidence caps at Medium — NEVER High (only the Orchestrator promotes, after cross-agent confirmation). Correct any opp_size the evidence does not support.

STEP 4 — BEFORE you return, WRITE your result to disk so it survives a session-limit kill:
  mkdir -p "${PARTS}/verified" && write the JSON object {"slug":..., "verified_signals":[...], "residual_gaps":"..."} to "${PARTS}/verified/${slug}.json"
Use a Bash heredoc or the Write tool. Then set wrote_file=true. THIS STEP IS MANDATORY — a returned-but-unwritten result is lost if the run dies.

${RULES}

Return the same structure you wrote. Drop a signal ONLY if it is fabricated or contradicted-and-worthless; a corrected signal is more valuable than a deleted one.`
}

phase('Verify')
log(`Verifying ${SLUGS.length} checkpointed unit(s) from ${PARTS}`)

const results = await parallel(SLUGS.map(slug => () =>
  agent(prompt(slug), { label: `verify:${slug}`, phase: 'Verify', effort: 'high', schema: SCHEMA })
))

const ok = results.filter(Boolean)
const perUnit = {}
let total = 0
ok.forEach(r => {
  const kept = (r.verified_signals || []).filter(s => s.keep !== false)
  perUnit[r.slug] = kept.length
  total += kept.length
})
const missing = SLUGS.filter(s => !ok.some(r => r.slug === s))
log(`Verified ${ok.length}/${SLUGS.length} units; ${total} signals kept; no result for: ${missing.length ? missing.join(', ') : 'none'}`)

return { perUnit, total, verifiedUnits: ok.length, missing, partsDir: `${PARTS}/verified` }
