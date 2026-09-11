// ALL-PAGES vision deep-read of the RBR reports — every page read, no gaps.
// RESILIENT: each agent renders its 10-page window, reads the pages, and WRITES its extraction to a
// checkpoint file immediately (knowledge-base/_deepread/<slug>/pSSSS-EEEE.md). So a stall never loses
// work — re-run this workflow and it only processes the windows whose checkpoint is still missing
// (dr_plan.py computes that each run). Bounded per run (MAX_PER_RUN) to keep batches small and survivable.
// Drive it: run repeatedly until `python dr_plan.py` shows 0 missing, then assemble with dr_assemble.py.

export const meta = {
  name: 'deep-read-allpages',
  description: 'All-pages vision deep-read of the RBR reports — chunked, checkpointed to disk, resumable',
  phases: [{ title: 'Plan', detail: 'find the page-windows still missing a checkpoint' },
           { title: 'Vision read', detail: 'render + read each window, write its extraction to disk' }],
}

// ROOT is per-host: pass args.root (or an args string) to override on another machine; defaults to the
// repo's known location so a no-arg run still works. Forward slashes resolve on both Windows and macOS.
let _A = args || {}
if (typeof _A === 'string') { try { _A = JSON.parse(_A) } catch (e) { _A = { root: _A } } }
const ROOT = (_A && _A.root) || '/Users/mangian/Downloads/BANKING'
const RP = ROOT + '/knowledge-base/scripts/render_pages.py'
const PLAN = ROOT + '/knowledge-base/scripts/dr_plan.py'
const PY = (_A && _A.py) || 'python3'   // Python 3 launcher: python3 on macOS/Linux; pass args.py="python" (or "py -3") on Windows
const MAX_PER_RUN = 40

const PLAN_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    total_missing: { type: 'number' },
    missing: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: { slug: { type: 'string' }, path: { type: 'string' }, pages: { type: 'string' }, out: { type: 'string' } },
      required: ['slug', 'path', 'pages', 'out'] } },
  },
  required: ['total_missing', 'missing'],
}
const VR_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { out: { type: 'string' }, pages: { type: 'string' }, pages_read: { type: 'number' }, ok: { type: 'boolean' } },
  required: ['out', 'pages', 'pages_read', 'ok'],
}

phase('Plan')
const plan = await agent(
  `Run exactly this command and return its JSON output verbatim (parsed):\n\n  ${PY} "${PLAN}" --print-missing --limit ${MAX_PER_RUN}\n\nIt prints {"missing":[{slug,path,pages,out}], "total_missing":N, ...}. Return {total_missing, missing}.`,
  { label: 'plan', phase: 'Plan', schema: PLAN_SCHEMA, effort: 'low' })
const work = (plan && plan.missing) || []
log(`${plan && plan.total_missing} page-windows still missing; processing ${work.length} this run`)
if (!work.length) return { done: true, remaining: 0 }

phase('Vision read')
const done = await parallel(work.map(w => () => agent(
  `Vision-read pages ${w.pages} of an ATM market report and WRITE the extraction to a checkpoint file. Read EVERY page in the window — no skipping.
1. Render the pages:  ${PY} "${RP}" "${w.path}" --pages "${w.pages}"   → it prints PNG image paths.
2. Open EACH PNG with the Read tool and study it: body text, tables, and above all the bar/line/pie CHARTS — read their axis values, data labels, legends and trend direction.
3. WRITE a markdown file to EXACTLY this path with the Write tool: ${w.out}
   Format: a "# Pages ${w.pages}" heading, then for each page a short "### p.N" block with the key data on that page — figures with their numbers, chart takeaways with values, table contents, installed-base / shipment / cash-withdrawal / forecast values, and the country/section it covers. For a filler page (cover, blank, pure contents) write "### p.N — no substantive data". NEVER invent a number; only what is actually on the page. Be precise and dense.
Then return {out:"${w.out}", pages:"${w.pages}", pages_read:<how many pages you read>, ok:true}.`,
  { label: `vr:${w.slug}:${w.pages}`, phase: 'Vision read', schema: VR_SCHEMA })
)).then(rs => rs.filter(Boolean))

const wrote = done.filter(r => r && r.ok).length
return { processed: work.length, wrote, remaining_before_run: plan.total_missing }
