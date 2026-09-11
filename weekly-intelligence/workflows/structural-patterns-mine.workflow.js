export const meta = {
  name: 'structural-patterns-mine',
  description: 'Mine the full KB for evidence-backed structural patterns, dedup vs the existing 8, produce an enriched set',
  phases: [
    { title: 'Mine', detail: 'one specialist per domain mines the KB for persistent structural patterns' },
    { title: 'Synthesize', detail: 'dedup vs the existing 8 + merge into one ordered, evidence-backed pattern set' },
  ],
}

const KB = `Knowledge base & findings (you have Read + Grep):
- knowledge-base/by-agent/agent-4-statistics/  — RBR ATM deep-reads (rbr-cee-atm-2028-deep.md, rbr-we-atm-2028-deep.md) + statistics digests
- knowledge-base/by-agent/agent-8-futurist/    — futurist research (cash-to-digital, instant payments, etc.) + RBR
- findings/03-regulation/ , findings/04-statistics/ , findings/06-vendors/ , findings/08-futurist/  — dated agent findings
- master-signal-table.md  — the current weekly signals (context only — patterns sit ABOVE individual signals)
Footprint: Greece, Cyprus, Romania, Bulgaria, Hungary, Czechia, Slovakia, Croatia, Slovenia, Austria, Serbia, Ukraine, Albania, Bosnia, North Macedonia, Montenegro, Kosovo.`

const WHAT = `A STRUCTURAL PATTERN is a PERSISTENT market mechanic — how the market structurally behaves over years — NOT a one-off weekly signal (a specific deal/tender) and NOT a 3-5yr point forecast. Good patterns are evidence-backed, cross-market where possible, and carry a clear "what it means for Printec". Examples of the right altitude: "branches shrink while ATMs hold", "cash is plateauing not dying", "deposit-automation/recycling is displacing legacy cash ATMs". Find NON-OBVIOUS ones too.`

const DOMAINS = [
  { key:'cash_atm', title:'Cash & ATM structure', focus:'Cash usage trajectory (decline vs resilience), ATM installed-base trends, deposit-automation & recycling adoption, off-site vs branch ATM shift, SAT/legacy displacement, ATM density saturation vs headroom.' },
  { key:'branch_channel', title:'Branches & channel transformation', focus:'Branch contraction pace, branch-to-advice/phygital transformation, self-service migration, the branch / ATM / digital rebalancing.' },
  { key:'payments_reg', title:'Payments & regulation structure', focus:'Instant payments / SEPA / TIPS rollout, PSD3/PSR, DORA & operational resilience, digital euro, ISO 20022, euro adoption (e.g. Bulgaria), accessibility (EAA) — regulatory cadence that structurally forces bank spend.' },
  { key:'competition', title:'Competition & vendor structure', focus:'Market consolidation (M&A such as NLB/Addiko and NCR Atleos/Brinks), IAD / ATM-as-a-Service / managed-services outsourcing shift, vendor concentration & lock-in, the partner-vs-competitor dynamic.' },
  { key:'digital', title:'Digital banking & self-service', focus:'Mobile/internet banking scaling, eKYC/onboarding, AI assistants, the shift of transactions to digital and what stays physical.' },
  { key:'macro_divergence', title:'Macro & country divergence', focus:'SEE growth vs Western-Europe maturity, per-country structural divergence (e.g. Serbia physical-network stability, Ukraine war effects, post-euro Bulgaria, tourism-driven cash cycles), density/GDP headroom differences.' },
  { key:'procurement', title:'Procurement & demand cadence', focus:'State-bank open ATM/POS procurement cycles, tender-driven demand spikes, hiring/leadership moves as leading indicators of programmes, replacement-cycle cadence.' },
]

const PATTERN = { type:'object', additionalProperties:false, required:['pattern','evidence','implication','confidence','sources'],
  properties:{
    pattern:{type:'string', description:'the structural mechanic, one crisp line'},
    evidence:{type:'string', description:'concrete data/trend backing it — figures, multi-year direction, which markets'},
    implication:{type:'string', description:'what it means for Printec (the business angle)'},
    confidence:{type:'string', description:'High | Medium | Low'},
    sources:{type:'string', description:'KB files / reports / figures it rests on'} } }
const MINE_SCHEMA = { type:'object', additionalProperties:false, required:['domain','patterns','notes'],
  properties:{ domain:{type:'string'}, patterns:{type:'array', items:PATTERN}, notes:{type:'string'} } }

phase('Mine')
const mined = (await parallel(DOMAINS.map(d => () => agent(
  `You mine the knowledge base for STRUCTURAL PATTERNS in ONE domain, to enrich a C-level dashboard's "Structural patterns" section.

${WHAT}

${KB}

YOUR DOMAIN: "${d.title}". Focus: ${d.focus}

Grep/read the relevant KB + findings, then return 3-6 evidence-backed structural patterns for your domain. Each must be a persistent mechanic (not a single deal), backed by concrete evidence (figures / multi-year direction / which markets), with a clear Printec implication, a confidence (High/Medium/Low), and its sources. Prefer patterns that span several footprint markets; flag single-market ones as such. Return ONLY the structured object.`,
  { schema: MINE_SCHEMA, label:'mine:'+d.key, phase:'Mine' }
)))).filter(Boolean)

phase('Synthesize')
const EXISTING = [
  'Branches shrink, ATMs grow (Greece)','Cash is plateauing, not dying','Cost lines are rising for IT, not falling',
  'Branch transformation wave (2024-2026), not branch elimination','State-owned banks run open ATM procurement cycles',
  'One-off events create dated demand spikes','Digital platforms hit scale -> branch role shifts to advice','Serbia diverges: physical network stable']
const SYNTH = { type:'object', additionalProperties:false, required:['patterns','notes'],
  properties:{
    patterns:{type:'array', items:{ type:'object', additionalProperties:false, required:['pattern','evidence','implication','confidence','status','sources'],
      properties:{ pattern:{type:'string'}, evidence:{type:'string'}, implication:{type:'string'}, confidence:{type:'string'}, status:{type:'string', description:'existing (one of the original 8, kept/sharpened) | new'}, sources:{type:'string', description:'the KB files / reports / figures this pattern rests on — carry through from the mined candidates (e.g. "RBR CEE ATM report; findings/08-futurist/research/themes/cash-to-digital.md; ECB statistics"); 2-4 concise refs'} } }},
    notes:{type:'string', description:'how many added, overlaps merged, and any low-confidence ones to treat cautiously'} } }

const synth = await agent(
  `You merge mined structural patterns into ONE clean, ordered set for a C-level dashboard "Structural patterns" table (columns: Pattern | Evidence | What it means for Printec | Confidence).

The dashboard ALREADY shows these 8 (keep them, sharpen wording/evidence if the KB supports it; mark status "existing"):
${JSON.stringify(EXISTING)}

Mined candidates by domain (JSON):
${JSON.stringify(mined)}

Produce the final set: the 8 existing (kept) PLUS the genuinely new, non-duplicate patterns from the mining — aim for a strong ~18-26 total. Dedup ruthlessly (merge overlaps into the best single statement). Every pattern needs real evidence (figures/direction/markets) and a Printec implication; drop anything that is actually a one-off signal or a pure 3-5yr forecast. Order logically (cash/ATM -> branches/channel -> payments/regulation -> competition/vendors -> digital -> macro/divergence -> procurement). Set status "existing" or "new". For every pattern, fill the sources field by carrying through the KB files/reports/figures the mined candidate(s) cited (2-4 concise refs, e.g. RBR CEE/WE ATM reports; findings/08-futurist/research/themes/cash-to-digital.md; ECB statistics); merge the sources when you merge patterns. Return ONLY the structured object.`,
  { schema: SYNTH, label:'synthesize', phase:'Synthesize' }
)

return { mined, synth }