// Deep-read the important, figure-dense KB reports with VISION — text extraction misses charts/graphs.
// COMPREHENSIVE: every country/market in the report + the regional/forecast/methodology charts (for the
// 3-5yr Futurist, the whole world is the leading indicator — we want ALL countries and ALL the data, not a
// footprint subset). Pattern: map each doc (read its TOC) → fan out one vision agent per section → parent
// reduces to enriched digests.
//
// Documents are hardcoded (args passing into workflows is unreliable). To deep-read another report later,
// edit DOCS and re-run. render_pages.py renders pages to PNG (temp); agents Read the PNGs.
// Returns [{slug,label,total_pages,sections:[{label,pages,markdown,adds_beyond_text}]}].

export const meta = {
  name: 'deep-read-document',
  description: 'Comprehensive vision deep-read of the RBR ATM reports — EVERY country + forecast charts, chart-level detail',
  phases: [{ title: 'Map', detail: 'read each report TOC, list every country + the forecast/regional sections' },
           { title: 'Vision read', detail: 'render + read each section, extract all chart/table data' }],
}

// ROOT is per-host: pass args.root (or an args string) to override on another machine; defaults to the
// repo's known location so a no-arg run still works. Forward slashes resolve on both Windows and macOS.
let _A = args || {}
if (typeof _A === 'string') { try { _A = JSON.parse(_A) } catch (e) { _A = { root: _A } } }
const ROOT = (_A && _A.root) || '/Users/mangian/Downloads/BANKING'
const RP = ROOT + '/knowledge-base/scripts/render_pages.py'
const PROC = ROOT + '/knowledge-base/processed/'
const PY = (_A && _A.py) || 'python3'   // Python 3 launcher: python3 on macOS/Linux; pass args.py="python" (or "py -3") on Windows

const DOCS = [
  { slug: 'rbr-cee-atm-2028',
    label: 'RBR Central & Eastern Europe ATM Market & Forecasts to 2028',
    path: PROC + 'RBR Reports - Central and Eastern Europe ATM Market and Forecasts to 2028 (NCR Atleos)[34] (1).pdf' },
  { slug: 'rbr-we-atm-2028',
    label: 'RBR Western Europe ATM Market & Forecasts to 2028',
    path: PROC + 'RBR Reports - Western Europe ATM Market and Forecasts to 2028 (NCR Atleos) (1).pdf' },
]

const RANGES_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    total_pages: { type: 'number' },
    ranges: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        label: { type: 'string', description: 'country name, or "Regional overview" / "Forecasts" / "Methodology"' },
        pages: { type: 'string', description: 'render_pages spec e.g. "118-129"' },
      },
      required: ['label', 'pages'] } },
  },
  required: ['total_pages', 'ranges'],
}
const SECTION_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    label: { type: 'string' }, pages: { type: 'string' },
    markdown: { type: 'string', description: 'extracted detail: figures/charts/tables as markdown, with p.N cites' },
    adds_beyond_text: { type: 'boolean', description: 'true if the CHARTS carried data not present as plain text' },
  },
  required: ['label', 'pages', 'markdown', 'adds_beyond_text'],
}

phase('Map')
const maps = await parallel(DOCS.map(d => () => agent(
  `You are mapping a large market report so it can be vision-read in full. We want EVERY country/market in
this report, plus the cross-country sections — NOTHING skipped (this feeds a 3-5yr global outlook, so all
markets are relevant as leading indicators, not just one region).
Document: "${d.path}"  (title: ${d.label}).

Steps:
1. Run: ${PY} "${RP}" "${d.path}" --count   (note the page count).
2. Render & READ the contents pages: ${PY} "${RP}" "${d.path}" --pages "1-12"  → it prints PNG paths; open each with the Read tool. The TOC lists every country/section with a page number (it may span several pages — read them all).
3. Build a target range for EVERY entry: one range per country/market section (ALL of them), PLUS the regional/global OVERVIEW, the FORECAST section, and METHODOLOGY/definitions. Each range ≈ that section's own pages (≈6-15). Do not omit any country. Use the next section's start page to bound each range.
Return {total_pages, ranges:[{label, pages}]} — real page numbers, every section covered.`,
  { label: `map:${d.slug}`, phase: 'Map', schema: RANGES_SCHEMA })))

const work = []
DOCS.forEach((d, i) => {
  const m = maps[i]
  const rs = (m && m.ranges) ? m.ranges.slice(0, 80) : []   // generous cap; reports have ~40-55 sections each
  rs.forEach(r => work.push({ d, r }))
  log(`${d.slug}: ${rs.length} sections mapped (${m && m.total_pages} pages)`)
})
if (!work.length) return DOCS.map(d => ({ slug: d.slug, label: d.label, sections: [] }))

phase('Vision read')
const done = await parallel(work.map(w => () => agent(
  `You are vision-reading one section of "${w.d.label}" — extract EVERY data point, especially what lives in
CHARTS/GRAPHS that plain-text extraction misses.
1. Render: ${PY} "${RP}" "${w.d.path}" --pages "${w.r.pages}"  → it prints PNG paths.
2. Open EACH PNG with the Read tool and study it — text, tables, and above all the bar/line/pie CHARTS (read
   their axis values, data labels, legends, trend direction).
3. Return markdown for this section ("${w.r.label}"): the key figures with their numbers and the page (cite
   "p.N"), each chart's takeaway, installed-base / shipment / cash-withdrawal / forecast values, and the
   3-5yr direction. NEVER invent a number — only what is on the page. Be precise and dense.
Set adds_beyond_text=true if the CHARTS held numbers/insight not already available as plain text on the page.`,
  { label: `vision:${w.d.slug}:${w.r.label.slice(0, 16)}`, phase: 'Vision read', schema: SECTION_SCHEMA })
  .then(s => s ? { ...s, slug: w.d.slug } : null)))

return DOCS.map((d, i) => ({
  slug: d.slug, label: d.label,
  total_pages: (maps[i] && maps[i].total_pages) || null,
  sections: done.filter(s => s && s.slug === d.slug),
}))
