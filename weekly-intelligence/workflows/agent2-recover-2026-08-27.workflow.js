// Agent 2 recovery pass, run 2026-08-27.
// Pass 1 (agent2-launch-2026-08-27) lost 25 of 47 agents to a session limit: 8 procurement
// portals died at the VERIFY stage AFTER their research checkpoints were written to disk
// (150 researched signals sitting in parts/2026-08-27_run1-orphaned-backup/). This pass runs
// the adversarial verify those 8 units never got, in BATCHES of <=11 signals per agent —
// the documented fix for the 32k output-token cap that kills verify on rich units.
// Each batch agent Reads its slice from the backup checkpoint, re-verifies against primary
// sources, and WRITES a JSON array to parts/2026-08-27/verify/<slug>-b<N>.json, which
// merge_harness_runs.py folds in with --extra (which wins over every journal).

export const meta = {
  name: 'agent2-tenders-recover',
  description: 'Batched adversarial verify for the 8 Agent-2 portals whose verify died on the session limit (150 researched signals recovered from checkpoint)',
  phases: [
    { title: 'BatchVerify', detail: 'one agent per <=11-signal batch; re-verifies against primary sources and writes a JSON array to disk' },
  ],
}

const PARTS = '/Users/mangian/Downloads/BANKING/findings/02-tenders/parts/2026-08-27'
const BACKUP = '/Users/mangian/Downloads/BANKING/findings/02-tenders/parts/2026-08-27_run1-orphaned-backup'
const OUT = `${PARTS}/verify`

// slug -> [ [startIndex, endIndexExclusive], ... ]   (signal counts from the checkpoints)
const BATCHES = [
  { slug: 'romania-seap-sicap',      n: 24, cuts: [[0, 8], [8, 16], [16, 24]] },
  { slug: 'slovenia-enarocanje',     n: 25, cuts: [[0, 9], [9, 17], [17, 25]] },
  { slug: 'serbia-ujn',              n: 22, cuts: [[0, 11], [11, 22]] },
  { slug: 'western-balkans-portals', n: 21, cuts: [[0, 11], [11, 21]] },
  { slug: 'slovakia-uvo',            n: 20, cuts: [[0, 10], [10, 20]] },
  { slug: 'bank-owned-pages',        n: 14, cuts: [[0, 7], [7, 14]] },
  { slug: 'hungary-ekr',             n: 13, cuts: [[0, 7], [7, 13]] },
  { slug: 'cyprus-eprocurement',     n: 11, cuts: [[0, 11]] },
]

const SIGNAL_PROPS = {
  entity:        { type: 'string' },
  country:       { type: 'string' },
  signal:        { type: 'string' },
  source_name:   { type: 'string' },
  source_url:    { type: 'string' },
  source_date:   { type: 'string' },
  source_tier:   { type: 'string', enum: ['primary', 'regulator', 'press', 'aggregator'] },
  implies:       { type: 'string' },
  likelihood:    { type: 'string' },
  confidence:    { type: 'string', enum: ['Medium', 'Low'] },
  opp_size:      { type: 'string', enum: ['XL', 'L', 'M', 'S', 'Unscoped'] },
  win:           { type: 'string', enum: ['High', 'Medium', 'Low', '—'] },
  followup:      { type: 'string' },
  deadline:      { type: 'string' },
  is_new:        { type: 'boolean' },
  verification:  { type: 'string', enum: ['confirmed', 'contradicted', 'unconfirmed'] },
  verifier_note: { type: 'string' },
  keep:          { type: 'boolean' },
}
const REQ = Object.keys(SIGNAL_PROPS)

const BATCH_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    slug:  { type: 'string' },
    batch: { type: 'number' },
    file:  { type: 'string', description: 'the absolute path of the JSON array you wrote' },
    verified_signals: { type: 'array', items: { type: 'object', additionalProperties: false, properties: SIGNAL_PROPS, required: REQ } },
    residual_gaps: { type: 'string' },
  },
  required: ['slug', 'batch', 'file', 'verified_signals', 'residual_gaps'],
}

const RULES = `HARD RULES (Printec research playbook, Agent 2 — Tenders & Procurement):
1. NEVER INVENT a value, deadline, CPV code, reference number or winner. A tender with no published value keeps opp_size "Unscoped" — a missing figure is a gap in DISCLOSURE, not evidence there is no deal. Quote figures with their currency and excl./incl. VAT exactly as the notice states.
2. CITE EVERY TENDER with buyer name (original language + English gloss), a stable canonical link (TED /xml or /pdf, Prozorro tender id, the national notice id) and the date DD/MM/YYYY. Prefer the PRIMARY notice over an aggregator.
3. CAPTURE THE WINNER OF EVERY AWARD, no matter how small. Printec is a ~EUR15M-EBITDA regional player, so a EUR 30k local POS/ATM-service winner is a first-class competitor. Keep the winner's name, legal entity/registration number where published, value and date IN THE SIGNAL TEXT — Agent 6 reads it from there. Never drop a winner for being small.
4. Today is 27/08/2026. A tender whose deadline has passed is NOT biddable — make sure the signal text says whether it is awarded, cancelled, in evaluation or status-unverified.
5. DEADLINES: the deadline field carries DD/MM/YYYY only for tenders that are still OPEN. Awards, cancellations and non-tender signals leave it empty.
6. CONFIDENCE CAPS AT MEDIUM (single-agent rule). Aggregator-only or press-only = Low.
7. RECENCY: source_date must be the most recent TRIGGERING development (new notice, extension, award, cancellation) or a concrete future deadline within ~18 months. Older-than-6-month items with no near-future trigger are CONTEXT — the signal text must carry [STANDING — dated YYYY] and is_new must be false.
8. PLAIN LANGUAGE: explain procurement/payments jargon on first use.
9. Opp. size bands: XL (>= ~EUR5m or footprint-wide), L (~EUR1-5m), M (~EUR0.2-1m), S (< ~EUR0.2m), Unscoped (macro/threat/too early).
10. ACCESS: on a 403/JS block, first retry the SAME primary URL with a desktop Chrome User-Agent (this alone defeats cec.ro, posted.co.rs, bankofalbania.org, centralbank.cy), then the site's own JSON/CSV API behind the SPA, then local PDF text extraction (pdftotext/pdfminer), then a cached snippet. NEVER solve a CAPTCHA and never work around a login wall.`

function prompt(slug, batchNo, start, end, total) {
  const outFile = `${OUT}/${slug}-b${batchNo}.json`
  return `You are an ADVERSARIAL fact-checker for Printec's banking tender research, run date 27/08/2026.

A research agent for the procurement portal "${slug}" finished its work and wrote a checkpoint to disk, then died before its claims could be verified. Your job is to run the verification it never got — on ONE BATCH of its signals.

STEP 1 — READ THE CHECKPOINT. Use the Read tool on:
${BACKUP}/${slug}.json
It is an object with a "signals" array of ${total} objects (plus coverage_notes / access_issues / operator_requests, which you should read for context but must NOT return).

STEP 2 — TAKE YOUR SLICE ONLY. Verify signals at zero-based index ${start} up to but NOT including ${end} (that is ${end - start} signals, batch ${batchNo}). Ignore every other signal in the file — another agent has them. Do not renumber, merge or split them.

STEP 3 — VERIFY EACH ONE INDEPENDENTLY, defaulting to SKEPTICISM. For every signal in your slice:
- Re-fetch the PRIMARY source (the TED notice at https://ted.europa.eu/en/notice/<id>/xml or /pdf, the national portal notice, the Prozorro CDB record, the buyer's own tender page) and confirm the buyer, the reference number, the value + currency + VAT basis, the deadline, the status and any named winner.
- A tender the researcher recorded as OPEN: re-check TODAY (27/08/2026) whether it is still open, has been extended (new deadline), has closed and is in evaluation, has been AWARDED (then get the winner, value and award date — this is the single most valuable thing you can add) or has been CANCELLED. Update the signal text and the deadline field to the CURRENT truth.
- Wrong number/date/vendor -> verification="contradicted", put the CORRECTED value and the source that proves it in verifier_note, and FIX the signal text. Set keep=false ONLY if the item is fabricated or does not exist.
- Aggregator-only claim -> confidence="Low" and say so in verifier_note.
- No independent confirmation -> verification="unconfirmed", confidence="Low", keep=true (do not drop it unless it is clearly false).
- verification="confirmed" requires a primary/regulator source you ACTUALLY re-fetched this run. Confidence still caps at Medium.
Preserve every useful field; tighten "implies" to the concrete Printec product angle; keep opp_size/win sane; keep is_new honest against the 01/08/2026 baseline.

STEP 4 — WRITE YOUR RESULT TO DISK BEFORE YOU RETURN IT. Use the Write tool to write a JSON ARRAY (not an object — a bare array of your verified signal objects, same field names as the input plus verification / verifier_note / keep) to exactly:
${outFile}
Write it as soon as you have verified 3-4 signals and RE-WRITE it as you finish more, so a kill does not lose the batch. This file is what the merge script reads — if you skip it, your work is lost even if you return it.

STEP 5 — return the structured object with slug="${slug}", batch=${batchNo}, file="${outFile}", your verified_signals array, and residual_gaps (what you could not confirm and the route that failed).

${RULES}`
}

phase('BatchVerify')
const jobs = []
for (const b of BATCHES) {
  b.cuts.forEach((c, i) => {
    jobs.push({ slug: b.slug, batchNo: i + 1, start: c[0], end: c[1], total: b.n })
  })
}
log(`Recovery verify — ${BATCHES.length} portals, ${jobs.length} batches, ${BATCHES.reduce((a, b) => a + b.n, 0)} researched signals to re-verify`)

const results = await parallel(jobs.map(j => () =>
  agent(prompt(j.slug, j.batchNo, j.start, j.end, j.total), {
    label: `bverify:${j.slug}-b${j.batchNo}`,
    phase: 'BatchVerify',
    effort: 'high',
    schema: BATCH_SCHEMA,
  })
))

const ok = results.filter(Boolean)
const bySlug = {}
for (const r of ok) {
  bySlug[r.slug] = (bySlug[r.slug] || 0) + (r.verified_signals || []).length
}
log(`Recovered: ${ok.length}/${jobs.length} batches, ${ok.reduce((a, r) => a + (r.verified_signals || []).length, 0)} verified signals`)

return {
  batches: jobs.length,
  succeeded: ok.length,
  failed: jobs.filter((j, i) => !results[i]).map(j => `${j.slug}-b${j.batchNo}`),
  perUnit: bySlug,
  files: ok.map(r => r.file),
}
