export const meta = {
  name: 'source-labeling',
  description: 'LLM labeling pass over a run\'s candidates: a source ROLE verdict + a review DECISION suggestion per candidate, in parallel batches. Recommendations only — the human/safety layer still decides.',
  phases: [{ title: 'Label', detail: 'batch agents assign role + decision per candidate' }],
}

// INPUTS (args): { batch_files: ["<abs path to a JSON array of compact labeling rows>", ...],
//                  scope: "<one-line scope>" }
// Each batch file is read BY ITS AGENT (workflow scripts have no filesystem access), so args stays tiny.
let _args = args
if (typeof _args === 'string') { try { _args = JSON.parse(_args) } catch (e) { _args = {} } }
const cfg = (_args && typeof _args === 'object') ? _args : {}
const batchFiles = Array.isArray(cfg.batch_files) ? cfg.batch_files.filter(p => typeof p === 'string') : []
const scope = typeof cfg.scope === 'string' && cfg.scope ? cfg.scope : 'the run scope'
const runId = cfg.run_id || 'dr_label_adhoc'
const dataRoot = cfg.data_root ||
  'C:/Users/User/Dropbox/E - PRINTEC GROUP/AI/MARKET RESEARCH/Strategic Intelligence - Banking and Payments/data'
const labelDir = cfg.label_dir || `${dataRoot}/run_logs/${runId}/agent_inputs/label_slices`

// each batch agent WRITES its labels to a slice file and returns only this ack (payload stays on disk; the
// orchestrator's round_finalize.py merges + clamps the slices).
const ACK_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['written', 'count'],
  properties: { written: { type: 'boolean' }, count: { type: 'number' }, slice_path: { type: 'string' } },
}

const guidance = `You are a market-research SOURCE ANALYST doing review triage for: ${scope}.
For EACH candidate give TWO judgments — a ROLE and a DECISION — plus a one-line rationale and a priority.

ROLE — what kind of thing is this, for long-term monitoring?
  • keep               = a durable STANDALONE source worth monitoring on its own (a portal, a registry, an RSS/news hub, an API, a tender search).
  • fold_into_parent   = a sub-page/section of a larger site already covered by monitoring the parent (it has siblings_on_domain > 0 and adds nothing standalone).
  • evidence_not_source= a ONE-OFF artifact (a single article, PDF, case study, press release) — useful as evidence, not a place that keeps producing signals.
  • pointer_once       = a directory / member-list / index you MINE ONCE for leads, then archive (not monitored continuously).
  • marginal           = weak, low-credibility, off-scope, or redundant — probably drop.

DECISION — should a reviewer approve it into the monitored registry?
  • approve       = reachable, public, legally clear, clearly in-scope and valuable -> track it.
  • needs_access  = valuable but blocked (login / paywall / registration / credentials) -> a human must clear access first.
  • reject        = out of scope, forbidden to collect, or junk.
  • defer         = unclear value or reachability -> look again later.

Scope: **read the sector definition at "${dataRoot}/knowledge/sector.json" and judge against THAT.** It is the only statement of what is in scope and it changes; never judge from memory. Payments actors carry equal weight to banking, and the file's "do_not_narrow" clause outranks any instinct about what a technology company sells. A url_verification of "failed" is a soft signal only (a separate browser pass re-checks liveness) — never reject solely for that; prefer defer/needs_access.

Return a label for EVERY candidate_id in your batch — do not skip any.`

phase('Label')
log(`labeling ${batchFiles.length} batch files -> ${labelDir}`)

const results = await parallel(batchFiles.map((path, bi) => () =>
  agent(
    `${guidance}\n\nYOUR BATCH is the JSON array of candidates in this file — Read it FIRST:\n${path}\n\n` +
    `Then, using the Write tool, WRITE a file at ${labelDir}/labels_${bi}.json (create the folder if needed) ` +
    `whose content is a JSON ARRAY with ONE object per candidate_id in the batch:\n` +
    `{"candidate_id","role":"keep|fold_into_parent|evidence_not_source|pointer_once|marginal",` +
    `"decision":"approve|reject|needs_access|defer","priority":"low|medium|high|critical","rationale":"one line"}\n` +
    `Label EVERY candidate_id in the batch — skip none. After the file is written, reply written=true + count.`,
    { schema: ACK_SCHEMA, label: `label:batch${bi + 1}`, phase: 'Label', agentType: 'general-purpose' }
  )
))
const wrote = results.filter(r => r && r.written).length
const labeled = results.reduce((n, r) => n + (r && typeof r.count === 'number' ? r.count : 0), 0)
log(`${wrote}/${batchFiles.length} batches wrote label slices (~${labeled} labels) -> ${labelDir}`)

// The labels live on disk (one slice per batch). The orchestrator's round_finalize.py merges + clamps them.
return { label_dir: labelDir, batches: batchFiles.length, labeled }
