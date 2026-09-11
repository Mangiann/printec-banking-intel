export const meta = {
  name: 'source-discovery-scout',
  description: 'One full R2 source-discovery scout round for a country x workstream: plan the source landscape into coverage cells, run one deep bilingual scout per cell, merge into a single compact scout_output.',
  phases: [
    { title: 'Plan', detail: 'size the source landscape into non-overlapping coverage cells' },
    { title: 'Scout', detail: 'one deep bilingual source-analyst per cell' },
  ],
}

// ─────────────────────────────────────────────────────────────────────────────
// INPUTS  (args) — the ONLY thing that changes between runs / countries.
// Pass the discovery-run config as a JSON object, e.g.:
//   { country:'GR', country_name:'Greece', sector:'banking', workstreams:['A2'],
//     topics:['tenders','procurement'], languages:['el','en'] }
// ─────────────────────────────────────────────────────────────────────────────
// args may arrive as a parsed object OR (depending on the harness) a JSON string — accept both, so the
// inputs are never silently ignored (which would fall back to the GR defaults for ANY country).
let _args = args
if (typeof _args === 'string') { try { _args = JSON.parse(_args) } catch (e) { _args = {} } }
const cfg = (_args && typeof _args === 'object') ? _args : {}
const country = cfg.country || 'GR'
const countryName = cfg.country_name || 'Greece'
const sector = cfg.sector || 'both'   // banking AND payments by default — never silently narrow to one
const workstreams = Array.isArray(cfg.workstreams) && cfg.workstreams.length ? cfg.workstreams : ['A2']
const topics = Array.isArray(cfg.topics) && cfg.topics.length ? cfg.topics : ['tenders', 'procurement']
const languages = Array.isArray(cfg.languages) && cfg.languages.length ? cfg.languages : ['el', 'en']
const minCells = Number(cfg.min_cells) || 20
const maxCells = Number(cfg.max_cells) || 32
const playbook = cfg.playbook_path ||
  'C:/Users/User/Dropbox/E - PRINTEC GROUP/AI/MARKET RESEARCH/Strategic Intelligence - Banking and Payments/routines/source_discovery_scout/routine_prompt.md'

const localLangs = languages.filter(l => String(l).toLowerCase() !== 'en')
const scope = `${countryName} (${country}) · sector=${sector} · workstream(s)=${workstreams.join(',')} · topics=${topics.join(', ')} · languages=${languages.join(', ')}`

// Each scout WRITES its own slice file to disk here (the orchestrator's deterministic ingest merges them).
// run_id + data_root come from the orchestrator; defaults let a standalone run still work.
const runId = cfg.run_id || 'dr_scout_adhoc'
const dataRoot = cfg.data_root ||
  'C:/Users/User/Dropbox/E - PRINTEC GROUP/AI/MARKET RESEARCH/Strategic Intelligence - Banking and Payments/data'
const sliceDir = `${dataRoot}/run_logs/${runId}/agent_inputs/scout_slices`

// ─────────────────────────────────────────────────────────────────────────────
// SCHEMAS  (force structured output; normalize.py re-snaps every enum, so we keep
// the schemas permissive to avoid retry-churn while still shaping the records).
// ─────────────────────────────────────────────────────────────────────────────
const PLAN_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['cells'],
  properties: {
    cells: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['cell_id', 'focus', 'rationale', 'languages', 'example_queries'],
        properties: {
          cell_id: { type: 'string' },
          focus: { type: 'string', description: 'the actor-type / channel-type / angle this scout owns' },
          rationale: { type: 'string', description: 'first-principles reason this cell holds real sources' },
          languages: { type: 'array', items: { type: 'string' } },
          example_queries: { type: 'array', items: { type: 'string' }, description: 'bilingual seed queries' },
        },
      },
    },
  },
}

const CANDIDATE_ITEM = {
  type: 'object', additionalProperties: false,
  required: ['source_name', 'source_url', 'source_class', 'primary_language', 'why_relevant',
             'credibility_score', 'usefulness_score', 'confidence_score', 'priority'],
  properties: {
    source_name: { type: 'string' },
    source_url: { type: 'string' },
    domain: { type: 'string' },
    source_class: { type: 'string', enum: ['direct', 'indirect', 'pointer'] },
    source_subtype: { type: 'string' },
    primary_language: { type: 'string' },
    topics: { type: 'array', items: { type: 'string' } },
    access_status: { type: 'string' },
    legal_status: { type: 'string' },
    collection_allowed: { type: 'boolean' },
    suggested_collection_method: { type: 'string' },
    credibility_score: { type: 'number' },
    usefulness_score: { type: 'number' },
    confidence_score: { type: 'number' },
    priority: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
    why_relevant: { type: 'string' },
    known_limitations: { type: 'string' },
    example_urls: { type: 'array', items: { type: 'string' } },
    discovered_via_method: { type: 'string' },
    queries_used: { type: 'array', items: { type: 'string' } },
    local_language_terms_used: { type: 'array', items: { type: 'string' } },
    blocked: { type: 'boolean' },
    blocker_type: { type: 'string' },
    observed_blocker: { type: 'string' },
  },
}
const NEGATIVE_ITEM = {
  type: 'object', additionalProperties: false,
  required: ['finding_type', 'description', 'result_summary'],
  properties: {
    finding_type: { type: 'string' }, description: { type: 'string' },
    why_it_matters: { type: 'string' }, severity: { type: 'string' }, language: { type: 'string' },
    source_class: { type: 'string' }, topics: { type: 'array', items: { type: 'string' } },
    queries_used: { type: 'array', items: { type: 'string' } }, method: { type: 'string' },
    result_summary: { type: 'string' },
  },
}
const GAP_ITEM = {
  type: 'object', additionalProperties: false,
  required: ['gap_type', 'description', 'recommended_action'],
  properties: {
    gap_type: { type: 'string' }, coverage_dimension: { type: 'string' }, description: { type: 'string' },
    why_it_matters: { type: 'string' }, severity: { type: 'string' }, source_class: { type: 'string' },
    topics: { type: 'array', items: { type: 'string' } }, recommended_action: { type: 'string' },
    language: { type: 'string' },
  },
}
// The scout WRITES its findings to a slice file and returns only this small acknowledgement (the payload is
// on disk, so it never has to travel back through workflow memory / the orchestrator).
const ACK_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['slice_written', 'candidates'],
  properties: {
    slice_written: { type: 'boolean' },
    candidates: { type: 'number' },
    slice_path: { type: 'string' },
  },
}

// ─────────────────────────────────────────────────────────────────────────────
// PROMPTS
// ─────────────────────────────────────────────────────────────────────────────
const plannerPrompt = `You are the lead source-analyst planning ONE market-research source-discovery run.

SCOPE: ${scope}

Your job is NOT to find sources yet — it is to CARVE THE SOURCE LANDSCAPE into ${minCells}-${maxCells} non-overlapping COVERAGE CELLS, so that one scout per cell, working in parallel with no shared state, together cover the whole landscape with minimal overlap.

Reason from FIRST PRINCIPLES about where banking/payments ${topics.join('/')} intelligence for ${countryName} lives — do NOT use a fixed checklist. For each cell ask: who CREATES this information, who is legally REQUIRED to publish it, who BENEFITS from announcing it, who SELLS INTO / BUYS / REGULATES / AUDITS / AGGREGATES / ARCHIVES / TRANSLATES / COMMENTS on it, and who reveals weak signals INDIRECTLY (jobs, events, partnerships, awards, complaints, contracts, local media). Include POINTER cells (registers, association member lists, procurement indexes, vendor customer pages) that reveal where more sources live.

**READ THE SECTOR DEFINITION AT "${dataRoot}/knowledge/sector.json" BEFORE PLANNING ANYTHING.** It is the only statement of what this system researches and it changes; never plan from memory. Honour its "do_not_narrow" clause — a landscape you do not plan is a landscape nobody ever searches.

Give PAYMENTS equal weight to banking, never as an afterthought. Beyond that, let the file define the territory. Three routes must each get cells: (a) the public sector — portals, registries, TED; (b) the private-bank ecosystem — in ${countryName} the systemic banks are private, so their procurement bypasses public portals and the supplier / partner / tender-aggregator ecosystem is the indirect route; (c) the payments ecosystem as a first-class landscape of its own, not an annex to banking. Split by ACTOR TYPE / CHANNEL TYPE / LANGUAGE so cells do not collide.

Languages in play: ${languages.join(', ')} (local language(s) ${localLangs.join(', ') || 'n/a'} are MANDATORY, not optional). Give each cell bilingual example_queries.

Return ${minCells}-${maxCells} cells in the schema. Each cell: a distinct focus, a first-principles rationale, its languages, and 3-6 bilingual seed queries.`

const scoutPrompt = (cell, i) => `You are a professional market-research SOURCE ANALYST for banking & payments. You discover, classify, and document long-term intelligence SOURCES — where relevant information lives and how reliable/accessible it is. You do NOT collect or parse content and you do NOT produce market conclusions.

RUN SCOPE: ${scope}
YOUR COVERAGE CELL (#${i + 1}): ${cell && cell.focus ? cell.focus : 'general source landscape'}
CELL RATIONALE: ${cell && cell.rationale ? cell.rationale : ''}
SEED QUERIES (extend them, do not stop here): ${cell && Array.isArray(cell.example_queries) ? cell.example_queries.join(' | ') : ''}

METHOD (full playbook on disk — Read it if you can: ${playbook}):
1. Build a local-language glossary + actor map for your cell (official names, acronyms, aliases, transliterations, English-in-local terms; flag noisy terms).
2. Infer source categories from first principles (who creates / must publish / benefits / sells / regulates / audits / aggregates / archives / reveals-indirectly). Do NOT work from a fixed checklist.
3. SEARCH IN BOTH ${languages.join(' AND ')} — local-language search is MANDATORY (English-only is forbidden). Note which queries were which.
4. Find POINTER sources and SNOWBALL them into more actors, terms, portals.
5. Classify each source direct / indirect / pointer; assess why it is worth tracking, credibility, access/legal status, and a suggested collection method.

TOOLS: use web search + fetch heavily. If WebSearch / WebFetch are not already available to you, FIRST call ToolSearch with query "select:WebSearch,WebFetch" to load them, then use them. Follow real links; snowball; look past the first page of results.

HARD RULES:
- NEVER fabricate a source, URL, or fact. If you did not actually find it, it is a negative_finding, not an invention.
- NEVER claim a URL is verified/reachable — a separate deterministic pass verifies liveness. Just provide the URL and your confidence.
- A failed fetch is a HYPOTHESIS, not a verdict — a 403/timeout usually means bot-defended-but-live; a 404 usually means moved. Do not record a source as dead on one bad fetch; note it as unverified.
- Local-language coverage is mandatory; if you had no local terms for something, say so in a negative_finding.

OUTPUT — WRITE your findings to ONE JSON file, then acknowledge. Using the Write tool, create (folder too if
needed) the file:  ${sliceDir}/slice_${i}.json  whose content is EXACTLY this JSON (valid JSON, no prose):
{
  "candidates": [ {"source_name","source_url","source_class":"direct|indirect|pointer","primary_language",
    "why_relevant","credibility_score":0..1,"usefulness_score":0..1,"confidence_score":0..1,
    "priority":"low|medium|high|critical","domain","source_subtype","topics":[],"access_status","legal_status",
    "collection_allowed":true,"suggested_collection_method","example_urls":[],"discovered_via_method",
    "queries_used":[],"local_language_terms_used":[],"blocked":false,"blocker_type","observed_blocker"} ],
  "negative_findings": [ {"finding_type","description","result_summary","why_it_matters","severity","language",
    "source_class","topics":[]} ],
  "coverage_gaps": [ {"gap_type","description","recommended_action","coverage_dimension","severity",
    "source_class","topics":[],"language"} ],
  "brief": "2-4 sentence source-landscape note for your cell"
}
Aim for THOROUGH coverage of YOUR cell (typically 10-25 candidates), not a token few. After the file is
written, reply with slice_written=true, the candidate count, and slice_path. If a source is blocked, set its
blocked=true + blocker_type + observed_blocker. Never fabricate; a dead end is a negative_finding.`

// ─────────────────────────────────────────────────────────────────────────────
// RUN
// ─────────────────────────────────────────────────────────────────────────────
phase('Plan')
const plan = await agent(plannerPrompt, { schema: PLAN_SCHEMA, label: 'plan:landscape',
                                         model: 'claude-opus-5', effort: 'low' })
let cells = plan && Array.isArray(plan.cells) ? plan.cells.filter(c => c && typeof c === 'object') : []
if (cells.length === 0) cells = [{ cell_id: 'c1', focus: 'general source landscape', rationale: '', example_queries: [] }]
// TOKEN SAFETY: if the caller set a token target (a "+Nk" directive), scale the fan-out to it so the round
// degrades gracefully instead of dying mid-way. Each deep bilingual scout ≈ ~80k output tokens. With no
// target, budget.total is null and we use the configured maxCells.
const budgetCap = (budget && budget.total) ? Math.max(4, Math.floor(budget.total / 80000)) : maxCells
const cellCap = Math.min(maxCells, budgetCap)
if (cells.length > cellCap) { log(`capping ${cells.length} planned cells -> ${cellCap} (token budget)`); cells = cells.slice(0, cellCap) }
log(`planned ${cells.length} coverage cells for ${scope}`)

phase('Scout')
const results = await parallel(cells.map((cell, i) => () =>
  agent(scoutPrompt(cell, i), { schema: ACK_SCHEMA, label: `scout:${cell.cell_id || i + 1}`, phase: 'Scout',
                                agentType: 'general-purpose',
                                model: 'claude-opus-5', effort: 'low' })
))
const scoutsOk = results.filter(r => r && r.slice_written).length
const totalCandidates = results.reduce((n, r) => n + (r && typeof r.candidates === 'number' ? r.candidates : 0), 0)
log(`${scoutsOk}/${cells.length} scouts wrote slices (~${totalCandidates} candidates) -> ${sliceDir}`)

// The payload lives on disk (one slice file per scout). The orchestrator's `round_ingest.py` merges + ingests.
return { slice_dir: sliceDir, cells: cells.length, scouts_ok: scoutsOk, candidates: totalCandidates }
