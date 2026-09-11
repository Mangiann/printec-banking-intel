// Public, deep, multi-level future-trends research for the Futurist (Agent 8). Builds a structured analyst
// report at three altitudes — global themes -> Printec products -> regions/countries — from PUBLIC sources
// (consulting houses, regulators, multilaterals, vendor guidance), triangulated and cited. No single report
// drives a section. RESILIENT: each unit's agent WRITES its checkpoint .md to disk, so a stall never loses
// work; re-run and it skips units whose checkpoint already exists (a planner agent lists what's done).
// Drive: re-run until all units have checkpoints, then synthesize futures_narrative.json from them.

export const meta = {
  name: 'future-trends-research',
  description: 'Deep PUBLIC 3-5yr research (consulting/regulators), fanned out global themes -> products -> regions, cited + series, checkpointed',
  phases: [{ title: 'Plan', detail: 'list units already researched' },
           { title: 'Research', detail: 'one deep public-research agent per missing unit' }],
}

// ROOT is per-host: pass args.root (or an args string) to override on another machine; defaults to the
// repo's known location so a no-arg run still works. Forward slashes resolve on both Windows and macOS.
let _A = args || {}
if (typeof _A === 'string') { try { _A = JSON.parse(_A) } catch (e) { _A = { root: _A } } }
const ROOT = (_A && _A.root) || '/Users/mangian/Downloads/BANKING'
const RDIR = ROOT + '/findings/08-futurist/research'

const UNITS = [
  // global structural themes
  ['themes', 'cash-to-digital', 'Cash-to-digital shift & cash resilience — cash-in-circulation, withdrawal volumes/values, cash-access policy, by region 2027-2031'],
  ['themes', 'branch-transformation', 'Bank branch network contraction & transformation (closures, formats, assisted self-service migration)'],
  ['themes', 'self-service-assisted', 'Self-service & assisted-service growth (kiosks, video teller, in-branch automation)'],
  ['themes', 'cash-recycling-deposit', 'Cash recycling & deposit automation — recycler share of fleet, adoption curve'],
  ['themes', 'atm-pooling-aaas', 'ATM pooling / ATM-as-a-Service / IAD estate transfers / managed ATM operations'],
  ['themes', 'instant-payments-iso20022', 'Instant payments & ISO 20022 maturing; account-to-account; VoP'],
  ['themes', 'softpos-acquiring', 'SoftPOS / Tap-to-Phone & acquiring fragmentation; merchant payment acceptance'],
  ['themes', 'digital-onboarding-eid', 'Digital onboarding, eID / digital identity wallets (EUDI), eKYC'],
  ['themes', 'ai-in-banking', 'AI in banking — fraud, service, ops, predictive maintenance, gen-AI'],
  ['themes', 'resilience-compliance', 'Operational resilience & compliance spend (DORA, AMLA/AML, accessibility)'],
  ['themes', 'digital-euro-cbdc', 'Digital euro & CBDCs — programme timeline, acceptance/wallet readiness, impact on cash/ATMs'],
  ['themes', 'atm-security', 'Physical & cyber ATM security — attack trends, IBNS/neutralisation, fraud'],
  // Printec product lines (demand outlook)
  ['products', 'atm-recyclers', '3-5yr demand outlook: ATMs & cash recyclers / intelligent deposit'],
  ['products', 'self-service-kiosks', '3-5yr demand outlook: self-service kiosks / assisted-service / bank kiosks'],
  ['products', 'pos-softpos', '3-5yr demand outlook: POS terminals, SoftPOS, terminal management'],
  ['products', 'onboarding-eid', '3-5yr demand outlook: digital onboarding / eID / e-signature'],
  ['products', 'aml-compliance', '3-5yr demand outlook: AML/KYC, transaction monitoring, compliance suite'],
  ['products', 'security-hsm', '3-5yr demand outlook: payment security, HSMs, key management, physical security'],
  ['products', 'managed-services', '3-5yr demand outlook: managed services / ATM-as-a-Service / outsourcing'],
  ['products', 'monitoring-analytics', '3-5yr demand outlook: monitoring, telemetry, transaction analytics'],
  // regions / countries (ALL relevant; mature markets as leading indicators; footprint highlighted)
  ['regions', 'global-overview', 'Global ATM/payments/self-service 3-5yr overview — the worldwide arc & what leads it'],
  ['regions', 'western-europe', 'Western Europe 3-5yr (leading indicator for CEE/SEE): ATM decline, pooling, recycling, IADs'],
  ['regions', 'north-america-nordics', 'North America + Nordics 3-5yr (most-digital leading indicators)'],
  ['regions', 'greece-cyprus', 'Greece & Cyprus 3-5yr (Printec home markets, euro-area)'],
  ['regions', 'cee-eu', 'CEE EU footprint 3-5yr (Czechia, Slovakia, Hungary, Romania, Bulgaria, Croatia, Slovenia, Austria)'],
  ['regions', 'see-non-eu', 'SEE non-EU footprint 3-5yr (Serbia, Albania, Bosnia, Kosovo, Montenegro, N. Macedonia)'],
  ['regions', 'ukraine', 'Ukraine 3-5yr (war-conditional; reconstruction/digitisation scenarios)'],
].map(([bucket, slug, focus]) => ({ bucket, slug, focus }))

const PREAMBLE = `You are a futurist banking-technology analyst building PRINTEC's 3-5 YEAR (2027-2031) outlook from PUBLIC, citable research.
Printec is a ~EUR15M-EBITDA transaction-technology company (ATMs/cash-recycling, self-service, POS/payments, onboarding, security, compliance, managed services) across 17 CEE/SEE countries; key partner NCR Atleos. For the long view you cover ALL relevant markets/global — mature markets lead the footprint.

METHOD (be deep & persistent — this is the whole point):
- Triangulate across MANY independent PUBLIC sources: consulting/advisory "future of" reports (McKinsey, BCG, Deloitte, Capgemini World Payments/Retail Banking Report, Accenture, Oliver Wyman, EY, KPMG, PwC, Gartner, Forrester, Juniper), regulators/multilaterals (ECB inc. digital-euro & SPACE, EBA, BIS, IMF, World Bank Findex, EU Commission), and vendor multi-year guidance (NCR Atleos, Diebold, Glory, Euronet, Worldline) treated as interested parties. NO single report may drive your conclusion.
- Use WebSearch + WebFetch (load them via ToolSearch if not already available). Try >=3 angles/queries. If a page is JS-heavy or shows only a paywalled preview, use Claude-in-Chrome (navigate + get_page_text). If a key report is fully gated/login-only, DO NOT drop it — list it under "## SOURCE REQUESTS FOR OPERATOR" with the URL and what it should contain.
- NEVER invent a number. Every figure and forecast must carry a cited PUBLIC source: label + URL + page (page if the source is a PDF/report).
- Extract NUMERIC SERIES wherever a source gives one (e.g. ATM installed base or cash-withdrawal value by year, adoption %), as a small table metric|year|value|source — these become dashboard charts.`

const RET = {
  type: 'object', additionalProperties: false,
  properties: {
    slug: { type: 'string' }, bucket: { type: 'string' },
    headline: { type: 'string', description: 'one-line direction/finding' },
    n_sources: { type: 'number' }, has_series: { type: 'boolean' },
  },
  required: ['slug', 'bucket', 'headline', 'n_sources', 'has_series'],
}

phase('Plan')
const planned = await agent(
  `List which research checkpoints already exist so we skip them. List every .md file under "${RDIR}" (recursively) — use your Glob/file-listing tool, or a shell command appropriate to the OS (find on macOS/Linux, dir /s /b on Windows).\nReturn {slugs:[...]} = the filenames without their .md extension (e.g. "cash-to-digital").`,
  { label: 'plan', phase: 'Plan', effort: 'low',
    schema: { type: 'object', additionalProperties: false, properties: { slugs: { type: 'array', items: { type: 'string' } } }, required: ['slugs'] } })
const have = new Set((planned && planned.slugs) || [])
const todo = UNITS.filter(u => !have.has(u.slug))
log(`${UNITS.length} units total; ${have.size} already done; researching ${todo.length}`)
if (!todo.length) return { done: true, total: UNITS.length }

phase('Research')
const res = await parallel(todo.map(u => () => agent(
  `${PREAMBLE}

YOUR UNIT (${u.bucket}): ${u.focus}

Research it deeply, then WRITE your checkpoint with the Write tool to EXACTLY this path:
${RDIR}/${u.bucket}/${u.slug}.md

Structure the file:
# ${u.focus}
## Direction & summary (2027-2031)   — the arc, pace, and confidence; objective.
## Key drivers                       — bullets, EACH ending with a [label](url) cite (+ p.N if a PDF).
## Numeric series (for charts)       — markdown table: metric | year | value | source-url(+page). Only real, cited numbers; omit if none found (set has_series=false).
## Printec implication               — what it pulls demand toward (which Printec product).
## Sources                           — every source used: label · URL · page.
## SOURCE REQUESTS FOR OPERATOR      — any gated/paywalled report worth accessing (URL + what it holds), or "none".

Then return {slug:"${u.slug}", bucket:"${u.bucket}", headline, n_sources, has_series}.`,
  { label: `res:${u.slug}`, phase: 'Research', schema: RET })
)).then(r => r.filter(Boolean))

return { processed: todo.length, done_now: res.length, results: res }
