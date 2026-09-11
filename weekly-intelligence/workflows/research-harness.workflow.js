// ============================================================================
// research-harness.workflow.js  —  SHARED collector harness for Agents 1-6
// ============================================================================
// Purpose: the reliable fan-out research pattern, used by every COLLECTOR agent
// (Bank Disclosures, Tenders, Regulation, Statistics non-EU, Jobs, Vendors).
//
// WHY THIS EXISTS (root-cause of the 24/06/2026 failure):
//   The old approach asked ONE synthesis LLM to hand-write the entire signal
//   table (~465 rows). It hit its output ceiling and SILENTLY dropped ~70% of
//   verified rows — whole markets (Bosnia, Montenegro, N.Macedonia) vanished
//   even though their research agents had succeeded. The data existed, was
//   verified, reached the reducer, and the reducer truncated it.
//
// THE FIX (three guarantees):
//   1. DETERMINISTIC RENDER — the table is built in JavaScript by mapping over
//      the verified signal objects. No LLM renders the table, so nothing can be
//      truncated or dropped. The LLM only writes the short prose narrative.
//   2. COMPLETENESS GATE — after research+verify, any unit that returned zero
//      signals (or whose agent died → null) is retried via gap-fill, up to
//      MAX_GAPFILL_ROUNDS. The run cannot "succeed" with a silently-empty unit.
//   3. PER-UNIT CHECKPOINT — each research agent also writes its part to disk
//      (parts/<runDate>/<slug>.md) for audit/recovery, mirroring the futurist
//      workflow's resilience pattern.
//
// CONTRACT — the calling agent (its SKILL.md) passes `args`:
//   {
//     agentNo:        1,
//     agentLabel:     "Bank Disclosures",
//     runDate:        "2026-06-24",            // YYYY-MM-DD (NEVER derive in JS)
//     findingsDir:    ".../findings/01-bank-disclosures",   // absolute path, forward slashes (portable on Windows + macOS)
//     unitNoun:       "bank",                  // for prompts/labels
//     units:          [{ slug, name, focus, langs }],   // the fan-out work-list
//     productContext: "Printec sells ...",     // 1-paragraph Printec offer map
//     rules:          "HARD RULES: ...",        // playbook rules block
//     prevSummary:    "BASELINE — already known: ...",  // delta context (optional)
//     tableKind:      "signals" | "tenders" | "regulation",  // controls columns/extras
//     researchModel:  "sonnet",                // optional; default inherit
//   }
//
// RETURNS: { markdown, stats:{ units, covered, signals, perUnit, emptyAfterGapfill } }
//   The calling agent writes `markdown` to findingsDir/<runDate>.md with the
//   Write tool (UTF-8), then sanity-checks stats.emptyAfterGapfill === [].
// ============================================================================

export const meta = {
  name: 'research-harness',
  description: 'Shared collector harness: fan-out per unit, adversarial verify, completeness gate, DETERMINISTIC table render (no LLM truncation), bounded narrative',
  phases: [
    { title: 'Research', detail: 'one deep agent per unit; researches, checkpoints to disk, returns structured signals' },
    { title: 'Verify',   detail: 'adversarial per-unit fact-check of every signal against primary sources' },
    { title: 'GapFill',  detail: 'retry any unit that returned zero signals or died (completeness gate)' },
    { title: 'Narrate',  detail: 'bounded LLM writes the prose narrative only; the table is rendered in JS' },
  ],
}

// `args` may arrive as a real object (when a parent workflow calls this via the
// workflow() hook) OR as a JSON STRING (when an agent passes it through the Workflow
// TOOL boundary, which serializes objects to a string — verified 24/06/2026). Tolerate
// both so the documented SKILL pattern (pass args directly) works without a launcher.
let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
if (!A || typeof A !== 'object') A = {}
const RUN_DATE = A.runDate || 'UNDATED'
const FINDINGS = A.findingsDir || ''
const PARTS = FINDINGS ? `${FINDINGS}/parts/${RUN_DATE}` : ''
const UNIT_NOUN = A.unitNoun || 'entity'
const UNITS = Array.isArray(A.units) ? A.units : []
const PRODUCT = A.productContext || 'Printec sells ATM/self-service, cash automation/recyclers, POS/acquiring, digital onboarding/eKYC, AML/compliance, transaction monitoring, HSM/security, and managed services.'
const RULES = A.rules || 'HARD RULES: never invent numbers/dates/values; cite every claim with source name + stable URL + date (DD/MM/YYYY); confidence caps at Medium (only the Orchestrator promotes to High); explain jargon in plain language; search English + local language; on a JS/403/PDF block try the API, then a cached snippet, then escalate to Claude-in-Chrome (load via ToolSearch), and never silently drop a source — log it.'
const PREV = A.prevSummary || ''
const TABLE_KIND = A.tableKind || 'signals'
const RESEARCH_MODEL = A.researchModel || undefined
const MAX_GAPFILL_ROUNDS = 2
// Statistics agent (4) only: each unit also returns a one-line-per-metric country_trend summary
// (so the harness renders the dashboard-read `## Country trends summary` table deterministically,
// instead of the SKILL hand-appending it) plus dated series_points (so non-EU markets chart). Other
// agents leave this flag unset -> no extra schema fields, prompt, render, or output. EU footprint rows
// are added downstream by ingest.py from the scripted ECB series; the harness handles only non-EU.
const EMIT_TRENDS = !!A.emitCountryTrends

// ---- structured-output schemas -------------------------------------------
const SIGNAL_PROPS = {
  entity:        { type: 'string', description: 'the specific bank/portal/competitor/regulator/country this row is about' },
  country:       { type: 'string' },
  signal:        { type: 'string', description: 'the factual signal, with any hard figures' },
  source_name:   { type: 'string' },
  source_url:    { type: 'string' },
  source_date:   { type: 'string', description: 'DD/MM/YYYY or Mon-YYYY' },
  source_tier:   { type: 'string', enum: ['primary', 'regulator', 'press', 'aggregator'] },
  implies:       { type: 'string', description: 'what it implies for a Printec product/opportunity' },
  likelihood:    { type: 'string', description: '6-12 month likelihood, short phrase' },
  confidence:    { type: 'string', enum: ['Medium', 'Low'] },
  opp_size:      { type: 'string', enum: ['XL', 'L', 'M', 'S', 'Unscoped'] },
  win:           { type: 'string', enum: ['High', 'Medium', 'Low', '—'] },
  followup:      { type: 'string' },
  deadline:      { type: 'string', description: 'tenders only: closing date DD/MM/YYYY, else empty' },
  is_new:        { type: 'boolean', description: 'true if NEW or materially CHANGED vs the previous findings file' },
}
const SIGNAL_REQUIRED = ['entity','country','signal','source_name','source_url','source_date','source_tier','implies','likelihood','confidence','opp_size','win','followup','deadline','is_new']

const RESEARCH_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    slug:    { type: 'string' },
    signals: { type: 'array', items: { type: 'object', additionalProperties: false, properties: SIGNAL_PROPS, required: SIGNAL_REQUIRED } },
    coverage_notes: { type: 'string', description: 'what was searched; genuine gaps and why' },
    access_issues:  { type: 'string' },
    operator_requests: { type: 'string', description: 'gated/paywalled PDFs an operator should fetch, or "none"' },
  },
  required: ['slug', 'signals', 'coverage_notes', 'access_issues', 'operator_requests'],
}

// Statistics-only schema extension (EMIT_TRENDS): a per-country trend summary + dated chartable points.
if (EMIT_TRENDS) {
  RESEARCH_SCHEMA.properties.country_trend = {
    type: 'object', additionalProperties: false,
    description: 'one short cell per column for this country\'s row in the Country-trends summary table',
    properties: {
      atms:             { type: 'string', description: 'latest ATM count + period + y/y trend, e.g. "626 (2024), +23% y/y"' },
      branches:         { type: 'string', description: 'latest bank-branch count + period + trend, or "—" if not found this run' },
      cash_trend:       { type: 'string', description: 'cash-usage / withdrawal direction in plain words' },
      instant_payments: { type: 'string', description: 'instant-payment scheme status (TIPS-clone, SEPA, IPS...) + any volume' },
      implication:      { type: 'string', description: 'the Printec product angle for this market' },
    },
    required: ['atms', 'branches', 'cash_trend', 'instant_payments', 'implication'],
  }
  RESEARCH_SCHEMA.properties.series_points = {
    type: 'array',
    description: 'EVERY dated multi-year structural point you found for this country (one object per metric per year), so the dashboard can chart and forecast the trend. Cite the source for each. Empty array if none.',
    items: {
      type: 'object', additionalProperties: false,
      properties: {
        metric:      { type: 'string', enum: ['atms', 'pos', 'branches', 'cash'] },
        year:        { type: 'integer' },
        value:       { type: 'number' },
        provisional: { type: 'boolean', description: 'true for interim/half-year/quarter or otherwise provisional reads' },
        unit:        { type: 'string', description: 'e.g. "terminals", "offices"' },
        source_name: { type: 'string' },
        source_url:  { type: 'string' },
      },
      required: ['metric', 'year', 'value', 'provisional', 'unit', 'source_name', 'source_url'],
    },
  }
  RESEARCH_SCHEMA.required = RESEARCH_SCHEMA.required.concat(['country_trend', 'series_points'])
}

const VERIFY_PROPS = Object.assign({}, SIGNAL_PROPS, {
  verification: { type: 'string', enum: ['confirmed', 'partially-confirmed', 'unconfirmed', 'contradicted'] },
  verifier_note: { type: 'string', description: 'what the independent re-check found; corrected value + source if a figure was wrong' },
  keep: { type: 'boolean', description: 'false only if fabricated/contradicted and should be dropped' },
})
const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    slug: { type: 'string' },
    verified_signals: { type: 'array', items: { type: 'object', additionalProperties: false, properties: VERIFY_PROPS, required: SIGNAL_REQUIRED.concat(['verification','verifier_note','keep']) } },
    residual_gaps: { type: 'string' },
  },
  required: ['slug', 'verified_signals', 'residual_gaps'],
}
// EMIT_TRENDS: the adversarial pass also re-verifies the country_trend cells + chartable series_points
// (same shapes as research), so the dashboard's Country-trends figures carry the same guarantee as signals.
if (EMIT_TRENDS) {
  VERIFY_SCHEMA.properties.country_trend = RESEARCH_SCHEMA.properties.country_trend
  VERIFY_SCHEMA.properties.series_points = RESEARCH_SCHEMA.properties.series_points
  VERIFY_SCHEMA.required = VERIFY_SCHEMA.required.concat(['country_trend', 'series_points'])
}

// ---- prompt builders ------------------------------------------------------
function researchPrompt(u) {
  return `You are a banking market-research analyst for Printec Group (regional CEE/SEE transaction-technology vendor, 17-country footprint). Exhaustively research ONE ${UNIT_NOUN} and return ONLY structured findings.

STEP 0 — RESUME CHECK (do this FIRST, before any searching). A previous run of THIS SAME runDate may have been interrupted (usage limit, crash). Use the Read tool on:
${PARTS}/${u.slug}.json
- If that file EXISTS and holds a valid object with a non-empty \`signals\` array, the work for this ${UNIT_NOUN} was ALREADY DONE this run. Do NOT re-research. Return those signals as your structured output (unchanged), plus its coverage_notes/access_issues/operator_requests, and STOP. Say "resumed from checkpoint" in coverage_notes.
- If the file holds \`"status":"partial"\`, it is an INTERRUPTED run: keep the signals it already contains, and continue researching ONLY the gaps its \`remaining\` note lists — do not redo the finished ones.
- If it does not exist or is unreadable/empty, proceed with the full research below (this is a normal fresh run).

TARGET ${UNIT_NOUN.toUpperCase()}: ${u.name || u.slug}
WHAT TO COVER / FOCUS: ${u.focus || ''}
SEARCH LANGUAGES: English + ${u.langs || 'the local language(s) of the market'}.

${RULES}

PRINTEC OFFER (map every signal to one of these): ${PRODUCT}

${PREV ? 'BASELINE CONTEXT — what the LAST run already knew. Use it to (a) re-verify/deepen each item against PRIMARY sources and (b) avoid re-deriving old ground. It is NOT a checklist and NOT a closed list of what exists — it is deliberately incomplete. Your FIRST duty is to DISCOVER what is new or has changed since then: new developments, deadlines, enforcement/consultation actions, jurisdictions, players, and SOURCES the baseline never saw. Do not let it anchor or narrow your search; report the COMPLETE current picture.\n' + PREV + '\n' : ''}
METHOD: go primary-source first (the entity's own site/IR/report/transcript, then regulator/exchange, then press; aggregators last and marked Low). Try >=3 DISTINCT angles, and deliberately VARY your search terms, languages, source types and entry points each run (regulators, official journals, central banks, court/enforcement and consultation registers, local-language press, plus source environments you have not used before) so FRESH sources surface every run rather than re-walking the same pages. Open the actual deck/PDF/portal page. Connect every signal to a concrete Printec product. Use the opp_size/win bands from the rules. Mark is_new=true for anything NEW or materially CHANGED vs the previous findings file.
SOURCE CATALOGUE (additional candidates, NOT a substitute): a curated list of pre-identified, access-TESTED sources for your beat exists at \`/Users/mangian/Downloads/BANKING/weekly-intelligence/references/source_catalogue_A${A.agentNo}.json\` (read it with the Read tool; it is grouped \`by_country\`, critical+high priority only, and covers ONLY Greece, Albania, Bosnia & Herzegovina, Bulgaria and Croatia). If your target's market is in there, SKIM your country's slice and open the entries that are genuinely relevant to THIS ${UNIT_NOUN} — prefer ones with \`tested_ok: true\` and follow the \`how\` hint for API/download routes. It is a FLOOR, not a ceiling and not a checklist: keep doing the full open-web search above, let it NOT narrow or anchor you, prefer a fresher source your own search finds, and CITE ONLY what you actually opened. If your market is absent from the file, ignore this and research as normal.
ACCESS — when a central-bank/regulator page returns 403/JS to the fetch tool, do NOT fall straight to press: first retry the SAME primary URL with a desktop browser User-Agent (this defeats most 403s on national CB sites — proven on bqk-kos.org, and worth trying on bank.gov.ua, nbrm.mk, bankofalbania.org, nbs.rs), and for PDFs extract the text locally (pdfminer/pdftotext) rather than relying on the fetch tool. Only after that route fails do you drop to a cached snippet/press, and you log the blocked URL + the route you used.
${EMIT_TRENDS ? `STRUCTURAL TREND OUTPUT (required this run): also return\n- country_trend: a one-line cell per column (atms, branches, cash_trend, instant_payments, implication) summarising THIS country's current structural picture for the Country-trends table. Put the latest figure + period in atms/branches; use "—" for a metric you genuinely could not find this run.\n- series_points: EVERY dated multi-year point you found for atms/pos/branches/cash (one object per metric per year, with source_name + source_url), so the dashboard can chart and forecast the trend. Mark interim/half-year/quarter reads provisional=true. Do NOT invent or interpolate points — only dated values you actually found.\n` : ''}
RESILIENCE — SAVE AS YOU GO, never only at the end (a run can be killed mid-research by a usage limit; anything unsaved is lost).
Write TWO checkpoint files with the Write tool, and RE-WRITE them as you progress:
1. ${PARTS}/${u.slug}.json — the MACHINE-READABLE checkpoint used to resume. Same shape as your final answer:
   {"slug":"${u.slug}","status":"partial"|"complete","remaining":"<what is still unresearched, or empty>","signals":[...],"coverage_notes":"...","access_issues":"...","operator_requests":"..."}
   • Write it the FIRST time you have 2-3 confirmed signals — do NOT wait until you are finished.
   • UPDATE it every few signals thereafter (status:"partial", and keep \`remaining\` honest about what is left).
   • Set status:"complete" only on your final write, when research for this ${UNIT_NOUN} is genuinely done.
2. ${PARTS}/${u.slug}.md — a short human-readable markdown summary + your signal rows (written/updated alongside the JSON).
THEN return the structured object with slug="${u.slug}"${EMIT_TRENDS ? ', your signals[], country_trend and series_points[]' : ' and your signals[]'}.`
}

function verifyPrompt(slug, research) {
  return `You are an ADVERSARIAL fact-checker for Printec's banking research. A researcher returned the signals below for "${slug}". Independently RE-VERIFY each signal against PRIMARY sources, defaulting to skepticism.

For every signal: re-search the entity's own IR/report/transcript or the regulator/exchange to CONFIRM the figure, date, vendor and claim.
- Aggregator-only claims -> downgrade confidence to Low and flag.
- Wrong number/date/vendor -> verification="contradicted", put the CORRECTED value + source in verifier_note; fix the signal text, or set keep=false if fabricated.
- No independent confirmation -> "unconfirmed" + recommend Low (do not drop unless clearly false).
- "confirmed" requires a primary/regulator source you actually re-checked. Confidence still caps at Medium.
Preserve all useful fields; tighten "implies" to the Printec angle; keep opp_size/win sane.

${RULES}

SIGNALS TO VERIFY (slug="${slug}"):
${JSON.stringify(research.signals || [], null, 2)}
${EMIT_TRENDS ? `
ALSO RE-VERIFY the structural-trend summary for this country and return it too:
- country_trend: confirm each cell's figure/period against a primary source; correct any value your signal re-check contradicts; keep "—" where the metric is genuinely unavailable.
- series_points: keep ONLY dated points you can confirm are cited (drop or fix any you cannot verify, default to dropping the unconfirmable); never add or interpolate points.

COUNTRY_TREND TO VERIFY:
${JSON.stringify(research.country_trend || {}, null, 2)}
SERIES_POINTS TO VERIFY:
${JSON.stringify(research.series_points || [], null, 2)}
` : ''}
Return the cleaned, verified set with slug="${slug}"${EMIT_TRENDS ? ', including the verified country_trend and series_points' : ''}.`
}

// ---- deterministic markdown rendering (THE FIX: JS builds the table) ------
function cell(s) {
  if (s === undefined || s === null) return ''
  return String(s).replace(/\r?\n+/g, ' ').replace(/\|/g, '\\|').trim()
}
const SIZE_RANK = { XL: 0, L: 1, M: 2, S: 3, Unscoped: 4 }
const WIN_RANK = { High: 0, Medium: 1, Low: 2, '—': 3 }
function valueRank(s) {
  return (SIZE_RANK[s.opp_size] === undefined ? 9 : SIZE_RANK[s.opp_size]) * 10
       + (WIN_RANK[s.win] === undefined ? 9 : WIN_RANK[s.win])
}
function sourceLink(s) {
  const name = cell(s.source_name) || 'source'
  const url = cell(s.source_url)
  return url ? `[${name}](${url})` : name
}
function renderTable(signals) {
  if (TABLE_KIND === 'regulation') {
    const head = '| Workstream | Country/Scope | Status & deadline | Source (link) | Date | What it implies | 6-12 mo likelihood | Confidence | Opp. size | Win | Recommended follow-up |\n|---|---|---|---|---|---|---|---|---|---|---|'
    const rows = signals.map(s => `| ${cell(s.entity)} | ${cell(s.country)} | ${cell(s.signal)} | ${sourceLink(s)} | ${cell(s.source_date)} | ${cell(s.implies)} | ${cell(s.likelihood)} | ${cell(s.confidence)} | ${cell(s.opp_size)} | ${cell(s.win)} | ${cell(s.followup)} |`)
    return head + '\n' + rows.join('\n')
  }
  const head = `| ${TABLE_KIND === 'tenders' ? 'Buyer' : 'Bank/Entity'} | Country | Signal | Source (link) | Date | What it implies | 6-12 mo likelihood | Confidence | Opp. size | Win | Recommended follow-up |\n|---|---|---|---|---|---|---|---|---|---|---|`
  const rows = signals.map(s => `| ${cell(s.entity)} | ${cell(s.country)} | ${cell(s.signal)}${s.verification && s.verification !== 'confirmed' ? ` [${s.verification}]` : ''} | ${sourceLink(s)} | ${cell(s.source_date)} | ${cell(s.implies)} | ${cell(s.likelihood)} | ${cell(s.confidence)} | ${cell(s.opp_size)} | ${cell(s.win)} | ${cell(s.followup)} |`)
  return head + '\n' + rows.join('\n')
}
function renderTenderPipeline(signals) {
  const open = signals.filter(s => cell(s.deadline)).slice()
  if (!open.length) return ''
  // sort by deadline DD/MM/YYYY ascending (string parse, no Date())
  const key = s => { const m = cell(s.deadline).match(/(\d{2})\/(\d{2})\/(\d{4})/); return m ? m[3] + m[2] + m[1] : '99999999' }
  open.sort((a, b) => key(a) < key(b) ? -1 : key(a) > key(b) ? 1 : 0)
  const head = '\n## Open-tender pipeline (by deadline; closing soonest first)\n\n| Deadline | Buyer | Country | Tender | Value/scope | Source |\n|---|---|---|---|---|---|'
  const rows = open.map(s => `| ${cell(s.deadline)} | ${cell(s.entity)} | ${cell(s.country)} | ${cell(s.signal)} | ${cell(s.opp_size)} | ${sourceLink(s)} |`)
  return head + '\n' + rows.join('\n') + '\n'
}
// access_issues / operator_requests are collected per unit by the research agents
// (RESEARCH_SCHEMA) but dropped by verify; render them here so the operator's manual
// to-do list and the blocked-source log survive into the findings file.
function meaningful(x) {
  const t = cell(x)
  return !!t && !/^(none|n\/a|na|-|null|nan|no issues?|no access issues?|no operator requests?)\.?$/i.test(t)
}
function renderAccessOps() {
  const items = []
  UNITS.forEach(u => {
    const r = researchBySlug[u.slug]
    if (!r) return
    items.push({
      unit: u.name || u.slug,
      ai: meaningful(r.access_issues) ? cell(r.access_issues) : '',
      opr: meaningful(r.operator_requests) ? cell(r.operator_requests) : '',
    })
  })
  const aiItems = items.filter(i => i.ai)
  const opItems = items.filter(i => i.opr)
  if (!aiItems.length && !opItems.length) return ''
  let s = `\n## Access issues & operator requests (per ${UNIT_NOUN})\n`
  if (aiItems.length) {
    s += `\n| ${UNIT_NOUN} | Access issue / what failed & the fallback used |\n|---|---|\n`
    s += aiItems.map(i => `| ${cell(i.unit)} | ${i.ai} |`).join('\n') + '\n'
  }
  if (opItems.length) {
    s += `\n**Operator requests — gated / paywalled / blocked sources to fetch or verify manually:**\n`
    s += opItems.map(i => `- **${cell(i.unit)}:** ${i.opr}`).join('\n') + '\n'
  }
  return s
}

// country_trend render (EMIT_TRENDS only): the deterministic `## Country trends summary` table the
// dashboard's ingest.py reads. One row per unit, built in JS (no LLM render -> cannot be truncated).
// EU footprint rows are appended downstream by ingest from the scripted ECB series; this is non-EU only.
function unitCountryName(u) {
  return cell((u.name || u.slug).replace(/\s*\([^)]*\)\s*$/, ''))   // "Serbia (NBS)" -> "Serbia"
}
function renderCountryTrends() {
  if (!EMIT_TRENDS) return ''
  const rows = []
  UNITS.forEach(u => {
    const r = researchBySlug[u.slug]
    const ct = trendBySlug[u.slug] || (r && r.country_trend)   // verified first, raw research as fallback
    if (!ct) return
    rows.push(`| ${unitCountryName(u)} | ${cell(ct.atms)} | ${cell(ct.branches)} | ${cell(ct.cash_trend)} | ${cell(ct.instant_payments)} | ${cell(ct.implication)} |`)
  })
  if (!rows.length) return ''
  return `\n## Country trends summary\n\n_Researched ${UNIT_NOUN} structural trends, one row per ${UNIT_NOUN}, adversarially verified (machine-read into the dashboard's per-country card). EU footprint rows are added automatically by ingest from the scripted ECB series._\n\n| Country | ATMs | Branches | Cash trend | Instant payments | Implication for Printec |\n|---|---|---|---|---|---|\n` + rows.join('\n') + '\n'
}
// flat list of every verified dated point, for the SKILL to write structural_series_noneu.json (charts).
function collectSeriesPoints() {
  if (!EMIT_TRENDS) return []
  const pts = []
  UNITS.forEach(u => {
    const r = researchBySlug[u.slug]
    const sp = (Array.isArray(seriesBySlug[u.slug]) ? seriesBySlug[u.slug]   // verified first, raw research as fallback
              : (r && Array.isArray(r.series_points) ? r.series_points : []))
    sp.forEach(p => pts.push({ unit: u.slug, country: unitCountryName(u), metric: p.metric, year: p.year,
                               value: p.value, provisional: !!p.provisional, unit_label: p.unit || '',
                               source_name: p.source_name || '', source_url: p.source_url || '' }))
  })
  return pts
}
// Build the READY-TO-WRITE structural_series_noneu.json object, keyed by ISO code (units carry `code`),
// so the SKILL writes stats.noneuSeriesFile verbatim — no name->code mapping or reshaping in the SKILL
// (that hand-transform was the remaining next-run risk). ingest.merge_structural folds it into the charts.
function buildNoneuSeriesFile() {
  if (!EMIT_TRENDS) return null
  const series = {}
  UNITS.forEach(u => {
    if (!u.code) { log(`WARN: unit "${u.slug}" has no ISO "code" in agent-units.json -> its series_points cannot be charted`); return }
    const r = researchBySlug[u.slug]
    const sp = (Array.isArray(seriesBySlug[u.slug]) ? seriesBySlug[u.slug]
              : (r && Array.isArray(r.series_points) ? r.series_points : []))
    sp.forEach(p => {
      if (!p || !p.metric || typeof p.year !== 'number' || typeof p.value !== 'number') return
      const m = (series[u.code] = series[u.code] || {})
      const arr = (m[p.metric] = m[p.metric] || [])
      const point = { year: p.year, value: p.value, provisional: !!p.provisional, unit: p.unit || '', source: p.source_name || '', url: p.source_url || '' }
      const existing = arr.find(x => x.year === p.year)
      if (existing) Object.assign(existing, point); else arr.push(point)
    })
  })
  Object.keys(series).forEach(cc => Object.keys(series[cc]).forEach(mk => series[cc][mk].sort((a, b) => a.year - b.year)))
  if (!Object.keys(series).length) return null
  return { generated: RUN_DATE, source: 'National central banks (Agent 4, researched & adversarially verified)', series }
}

// ============================================================================
// RUN
// ============================================================================
if (!UNITS.length) {
  return { markdown: `# Agent ${A.agentNo || '?'} — ${A.agentLabel || ''} — ${RUN_DATE}\n\n_No units passed to the harness; nothing to research._\n`, stats: { units: 0, covered: 0, signals: 0, perUnit: {}, emptyAfterGapfill: [] } }
}

log(`Harness start: Agent ${A.agentNo} (${A.agentLabel}) — ${UNITS.length} ${UNIT_NOUN}(s), runDate ${RUN_DATE}`)

// --- Phase 1+2: research -> verify, per unit (pipeline, no barrier) ---------
// Stash each research agent's raw output (access_issues / operator_requests /
// coverage_notes) keyed by slug — the verify stage discards these fields, so capture
// them here for the deterministic "Access issues & operator requests" render below.
const researchBySlug = {}
phase('Research')
const piped = await pipeline(
  UNITS,
  (u) => agent(researchPrompt(u), { label: `research:${u.slug}`, phase: 'Research', model: RESEARCH_MODEL, effort: 'medium', schema: RESEARCH_SCHEMA })
          .then(r => { if (r) researchBySlug[u.slug] = r; return r }),
  (research, u) => {
    if (!research || !Array.isArray(research.signals) || research.signals.length === 0) {
      return { slug: u.slug, verified_signals: [], residual_gaps: research ? (research.coverage_notes || 'no signals') : 'research agent returned null' }
    }
    return agent(verifyPrompt(u.slug, research), { label: `verify:${u.slug}`, phase: 'Verify', effort: 'high', schema: VERIFY_SCHEMA })
  }
)

// collect verified signals per unit (+ the adversarially-verified country_trend / series_points)
const bySlug = {}
const trendBySlug = {}    // EMIT_TRENDS: verified country_trend per slug (falls back to raw research below)
const seriesBySlug = {}   // EMIT_TRENDS: verified series_points per slug
UNITS.forEach(u => { bySlug[u.slug] = [] })
function captureVerified(v) {
  if (!v || !v.slug) return
  if (Array.isArray(v.verified_signals)) bySlug[v.slug] = v.verified_signals.filter(s => s.keep !== false)
  if (v.country_trend) trendBySlug[v.slug] = v.country_trend
  if (Array.isArray(v.series_points)) seriesBySlug[v.slug] = v.series_points
}
piped.filter(Boolean).forEach(captureVerified)

// --- Phase 3: completeness gate — gap-fill any empty unit -------------------
phase('GapFill')
let round = 0
let empty = UNITS.filter(u => (bySlug[u.slug] || []).length === 0)
while (empty.length && round < MAX_GAPFILL_ROUNDS) {
  round++
  log(`Completeness gate round ${round}: ${empty.length} ${UNIT_NOUN}(s) still empty -> retrying: ${empty.map(u => u.slug).join(', ')}`)
  const refilled = await pipeline(
    empty,
    (u) => agent(`RETRY (round ${round}) — the first research pass returned NOTHING for this ${UNIT_NOUN}. Try harder: different keywords, the local language, the regulator/central-bank site, the entity's annual report PDF, and a Google site: search; escalate to Claude-in-Chrome (load via ToolSearch) for JS/403 pages. Return at least the verifiable signals you can find; if the ${UNIT_NOUN} genuinely has no public disclosure, return one row documenting that with the sources you checked.\n\n` + researchPrompt(u),
              { label: `gapfill:${u.slug}`, phase: 'GapFill', model: RESEARCH_MODEL, effort: 'high', schema: RESEARCH_SCHEMA })
          .then(r => { if (r) researchBySlug[u.slug] = r; return r }),
    (research, u) => {
      if (!research || !Array.isArray(research.signals) || research.signals.length === 0) return { slug: u.slug, verified_signals: [], residual_gaps: 'still empty' }
      return agent(verifyPrompt(u.slug, research), { label: `gapverify:${u.slug}`, phase: 'GapFill', effort: 'high', schema: VERIFY_SCHEMA })
    }
  )
  refilled.filter(Boolean).forEach(v => {
    if (!v || !v.slug) return
    if (Array.isArray(v.verified_signals) && v.verified_signals.length) {
      bySlug[v.slug] = v.verified_signals.filter(s => s.keep !== false)
    }
    if (v.country_trend) trendBySlug[v.slug] = v.country_trend
    if (Array.isArray(v.series_points) && v.series_points.length) seriesBySlug[v.slug] = v.series_points
  })
  empty = UNITS.filter(u => (bySlug[u.slug] || []).length === 0)
}
const emptyAfterGapfill = empty.map(u => u.slug)

// --- flatten + order by Printec value (biddable first), then by unit --------
const allSignals = []
UNITS.forEach(u => (bySlug[u.slug] || []).forEach(s => allSignals.push(s)))
allSignals.sort((a, b) => valueRank(a) - valueRank(b))

const perUnit = {}
UNITS.forEach(u => { perUnit[u.slug] = (bySlug[u.slug] || []).length })
const covered = UNITS.filter(u => (bySlug[u.slug] || []).length > 0).length
log(`Coverage: ${covered}/${UNITS.length} ${UNIT_NOUN}(s) returned signals; ${allSignals.length} verified signals total; empty after gap-fill: ${emptyAfterGapfill.length ? emptyAfterGapfill.join(', ') : 'none'}`)

// --- Phase 4: bounded narrative (LLM writes PROSE ONLY — cannot drop rows) --
phase('Narrate')
const narrativeInput = allSignals.map(s => ({ entity: s.entity, country: s.country, signal: (s.signal || '').slice(0, 200), opp_size: s.opp_size, win: s.win, confidence: s.confidence, is_new: s.is_new, verification: s.verification }))
const narrative = await agent(
  `You are the lead analyst for Printec's Agent ${A.agentNo} (${A.agentLabel}), run ${RUN_DATE}. Below are the ${allSignals.length} VERIFIED signals already collected and fact-checked this run (the full signal TABLE is rendered separately and automatically — do NOT reproduce it). Write ONLY two short prose sections in Markdown:

## What changed since last run
3-7 sentences, plain language, leading with the 3-4 highest-value NEW/changed items for Printec. Note any baseline figure that verification corrected or could not confirm.

## Top opportunities (ranked)
A numbered list, max 8, each one line: the entity + the Printec product to pitch + (opp_size, win). Pick the highest expected-value items (size x win x confidence) from the data below.

Output ONLY those two sections. Do not invent anything not present below.

SIGNALS (compact):
${JSON.stringify(narrativeInput, null, 2)}`,
  { label: 'narrate', phase: 'Narrate', effort: 'medium' }
)

// --- DETERMINISTIC assembly (JS) — nothing can be truncated -----------------
const contradicted = allSignals.filter(s => s.verification === 'contradicted')
const unconfirmed = allSignals.filter(s => s.verification === 'unconfirmed')
const header = `# Agent ${A.agentNo} — ${A.agentLabel} — Findings ${RUN_DATE}

(Method: shared research harness — one agent per ${UNIT_NOUN}, adversarial per-claim verification, completeness gate, DETERMINISTIC table render. ${UNITS.length} ${UNIT_NOUN}(s) targeted, ${covered} returned signals, ${allSignals.length} verified signals. Confidence capped at Medium per single-agent playbook. Table rows ordered by Printec value (size x win), biddable first.)
${emptyAfterGapfill.length ? `\n> **COVERAGE WARNING:** these ${UNIT_NOUN}(s) returned NO signals even after ${MAX_GAPFILL_ROUNDS} gap-fill rounds — treat as genuine gaps, not "nothing happening": **${emptyAfterGapfill.join(', ')}**.\n` : ''}`

const verifNote = (contradicted.length || unconfirmed.length)
  ? `\n## Verification notes\n- **Corrected/contradicted by the adversarial pass (${contradicted.length}):** ${contradicted.length ? contradicted.map(s => `${s.entity} — ${cell(s.verifier_note)}`).slice(0, 40).join('; ') : 'none'}\n- **Unconfirmed (single/weak source, kept at Low) (${unconfirmed.length}):** ${unconfirmed.length ? unconfirmed.map(s => s.entity).slice(0, 60).join(', ') : 'none'}\n`
  : ''

const coverageTable = `\n## Coverage (per ${UNIT_NOUN}, honest)\n\n| ${UNIT_NOUN} | signals |\n|---|---|\n` +
  UNITS.map(u => `| ${cell(u.name || u.slug)} | ${perUnit[u.slug]}${perUnit[u.slug] === 0 ? ' ⚠ EMPTY' : ''} |`).join('\n') + '\n'

const markdown = [
  header,
  narrative || '',
  renderCountryTrends(),
  TABLE_KIND === 'tenders' ? renderTenderPipeline(allSignals) : '',
  '\n## Signal table\n',
  renderTable(allSignals),
  verifNote,
  renderAccessOps(),
  coverageTable,
].join('\n')

const seriesPoints = collectSeriesPoints()
const noneuSeriesFile = buildNoneuSeriesFile()
log(`Country-trend output: ${EMIT_TRENDS ? `${UNITS.filter(u => researchBySlug[u.slug] && researchBySlug[u.slug].country_trend).length} trend rows, ${seriesPoints.length} chartable series points across ${noneuSeriesFile ? Object.keys(noneuSeriesFile.series).length : 0} ${UNIT_NOUN}(s)` : 'disabled'}`)

return {
  markdown,
  stats: { units: UNITS.length, covered, signals: allSignals.length, perUnit, emptyAfterGapfill, seriesPoints, noneuSeriesFile },
}
