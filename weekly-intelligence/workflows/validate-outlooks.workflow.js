/* ============================================================================
   validate-outlooks — independent traceability audit of the weekly Outlook.

   The semantic sibling of verify.py: verify.py checks "is the cited source
   reachable"; this checks "do the outlook's claims actually trace to the
   sources it cites." It is INDEPENDENT of the orchestrator that authored the
   outlooks — one fact-checker agent per market reads each outlook against the
   actual finding documents it cites and flags any concrete claim it can't find
   support for. The result is written to intel-cache/outlook_validation.json,
   which build_dashboard.py merges (authoritative over the orchestrator's own
   self-reported flags) and the dashboard renders as the per-outlook
   "⚠ N claim(s) not yet linked to a cited source" caveat + a
   "✓ independently validated" marker.

   Run it AFTER the orchestrator writes forecast_narrative.json and BEFORE
   run_weekly.py builds the dashboard:
     Workflow({ scriptPath: ".../weekly-intelligence/workflows/validate-outlooks.workflow.js" })

   Paths are project-rooted (this is the Printec research folder's weekly flow).
   ============================================================================ */
export const meta = {
  name: 'validate-outlooks',
  description: 'Independent traceability audit of the weekly 6-12mth Outlook AND the 2-5yr Future-outlook: do their claims trace to the cited sources?',
  phases: [
    { title: 'Validate', detail: 'independent fact-checkers: per-market outlooks + per-line product outlooks vs the docs they cite' },
    { title: 'Validate futures', detail: 'one fact-checker per 2-5yr projection vs its cited findings + the local knowledge base' },
    { title: 'Write',    detail: 'persist verdicts to outlook_validation.json + futures_validation.json' },
  ],
}

// ROOT is per-host: pass args.root (or an args string) to override on another machine; defaults to the
// repo's known location so a no-arg run still works. Forward slashes resolve on both Windows and macOS.
let _A = args || {}
if (typeof _A === 'string') { try { _A = JSON.parse(_A) } catch (e) { _A = { root: _A } } }
const ROOT = (_A && _A.root) || "/Users/mangian/Downloads/BANKING"
const NAR  = ROOT + "/intel-cache/forecast_narrative.json"
const OUT  = ROOT + "/intel-cache/outlook_validation.json"
const FNAR = ROOT + "/intel-cache/futures_narrative.json"      // the Futurist's 2-5yr projections (Agent 8)
const FOUT = ROOT + "/intel-cache/futures_validation.json"     // futures audit, merged by build_dashboard.py
const MARKETS = ["Greece","Hungary","Ukraine","Romania","Serbia","Bulgaria","Footprint-wide"]

const SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { results: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    properties: {
      oid: { type: 'integer' },
      verdict: { type: 'string', enum: ['grounded','thin','unsupported'] },
      ungrounded: { type: 'array', items: { type: 'string' } },
    },
    required: ['oid','verdict','ungrounded'],
  }}},
  required: ['results'],
}

const valPrompt = (m) => `You are an INDEPENDENT fact-checker. You did NOT write these market outlooks — your only job is to check whether their factual claims trace to the sources they cite, so a reader can verify them. Be a strict but fair skeptic.

1. Read the narrative file (Read tool): ${NAR}
   It has an "outlooks" array; each item = {oid, country, scope, drivers[], rationale, cite_signals[], cite_files[]}.
2. For EVERY outlook whose country == "${m}":
   a. Read each finding document listed in that outlook's cite_files. They are relative paths like
      "findings/04-statistics/2026-06-12.md"; the absolute path is "${ROOT}" + "/" + that path. Read each
      one with the Read tool (skip any that don't exist). These cited docs are the evidence base you check against.
   b. Walk the outlook's drivers and rationale. For each SPECIFIC, FALSIFIABLE factual claim — a number or
      percentage, a named programme/event, a date or deadline, a money figure, a named bank/vendor/competitor —
      decide whether the cited finding documents actually support it.
   c. Do NOT flag judgment, interpretation, or forward projections (those are the analyst's reasoned call, not
      facts to source). Flag ONLY concrete factual assertions for which you cannot find support in the cited docs.
3. Return one result per "${m}" outlook:
   - oid (integer, from the narrative)
   - verdict: "grounded" (every load-bearing fact traces), "thin" (a secondary fact or two doesn't trace), or
     "unsupported" (a core claim doesn't trace).
   - ungrounded: the list of specific claims (quote each briefly) you could NOT locate in the cited documents.
     Empty list if everything traces. When you genuinely cannot find support, flag it — under-claiming the gaps
     is the failure to avoid.`

// Per-line audit for the PRODUCT-direction outlooks (keyed by oid, like the futures audit below) — these
// answer "where is each Printec line heading" and are NOT grouped by market, so check them one oid at a time.
const PITEM = {
  type: 'object', additionalProperties: false,
  properties: {
    oid: { type: 'integer' },
    verdict: { type: 'string', enum: ['grounded','thin','unsupported'] },
    ungrounded: { type: 'array', items: { type: 'string' } },
  },
  required: ['oid','verdict','ungrounded'],
}
const prodValPrompt = (oid) => `You are an INDEPENDENT fact-checker. You did NOT write these product-line outlooks — check whether the PRODUCT-direction outlook oid=${oid} traces to the sources it cites. Be a strict but fair skeptic.

TRACEABILITY, not live reachability. Your evidence base is LOCAL: (a) the finding docs the outlook lists in cite_files; (b) verify.py's SNAPSHOTS of every cited URL — intel-cache/snapshots/<sha1>.txt (the fetched text, pinned this run), so a claim backed by an inline [label](url) counts as grounded if that source's snapshot supports it; (c) the KNOWLEDGE BASE of paid/internal reports (knowledge-base/by-agent/, _reference/, _deepread/ — Grep for a figure). NEVER flag a claim merely because its URL is paywalled or offline — check the snapshot / KB first.

1. Read ${NAR} (Read tool); find the item whose oid == ${oid} in its "product_outlooks" array. Each = {oid, id, label, scope, summary, projected, rationale, drivers[], cite_files[]}.
2. Read each finding doc in its cite_files (relative paths under "${ROOT}"; skip any missing). Consult snapshots / the knowledge base for inline-cited or paid figures per the policy above.
3. Walk drivers, projected and summary. For each SPECIFIC, FALSIFIABLE factual claim — a number/percentage, a named programme/regulation/deadline, a money figure, a named bank/vendor — decide whether the cited evidence supports it. Do NOT flag judgment, interpretation, or the forward projection itself.
4. Return: oid (integer), verdict ("grounded" = every load-bearing fact traces, "thin" = a secondary fact or two doesn't, "unsupported" = a core claim doesn't), and ungrounded (the specific claims you could NOT locate, quoted briefly; [] if all trace).`

const byMarket = await pipeline(
  MARKETS,
  (m) => agent(valPrompt(m), { label: `validate:${m}`, phase: 'Validate', schema: SCHEMA })
           .then(r => ({ market: m, results: (r && r.results) || [] }))
)

// product-direction outlooks: enumerate their oids, then audit each one — merged into the same validated set
const penum = await agent(`Read ${NAR} with the Read tool and return {oids:[...]} — the integer oid of every item in its "product_outlooks" array (return {oids:[]} if there is no such array or it is empty).`,
  { label: 'enumerate:product-outlooks', phase: 'Validate',
    schema: { type: 'object', additionalProperties: false, properties: { oids: { type: 'array', items: { type: 'integer' } } }, required: ['oids'] } })
const prodResults = (await pipeline(
  (penum && penum.oids) || [],
  (oid) => agent(prodValPrompt(oid), { label: `product:oid-${oid}`, phase: 'Validate', schema: PITEM })
)).filter(Boolean)

const validated = []
for (const r of byMarket.filter(Boolean)) for (const o of (r.results || [])) validated.push(o)
for (const o of prodResults) validated.push(o)
validated.sort((a,b) => a.oid - b.oid)
const flagged = validated.filter(v => v.ungrounded && v.ungrounded.length).length
log(`validated ${validated.length} outlooks (incl. ${prodResults.length} product lines) — ${flagged} carry >=1 ungrounded claim`)

// Persist independently of the orchestrator's authored narrative (mirrors verify.py -> verification.json).
const writePrompt = `Read ${NAR} (Read tool) and note its top-level "week" value. Then use the Write tool to
create a file at EXACTLY this path:
${OUT}
Its content must be this JSON object, with <WEEK> replaced by the week you read, pretty-printed with 2-space
indent. Copy every oid, verdict and ungrounded string VERBATIM — do not edit, summarise or reorder them:

{
  "week": "<WEEK>",
  "generated_by": "validate-outlooks workflow (independent traceability audit)",
  "validated": ${JSON.stringify(validated)}
}

After writing, confirm the absolute path written and the count of validated entries.`
await agent(writePrompt, { label: 'write:outlook_validation.json', phase: 'Write' })

/* ----------------------------------------------------------------------------
   2-5yr Future-outlook audit (same traceability check, applied to the Futurist's
   projections in futures_narrative.json). Mirrors the outlook audit above; the
   only twist is the PAID-SOURCE policy — many futures cite subscription reports
   (RBR, Datos Insights, McKinsey) whose live URLs are paywalled. Result is
   written to futures_validation.json, which build_dashboard.py merges exactly
   like outlook_validation.json (per-future "✓ independently validated" + the
   "⚠ N claim(s) not yet linked to a cited source" caveat).
   ---------------------------------------------------------------------------- */
const PAYWALL = `PAID-SOURCE / PAYWALL POLICY — read carefully. Your job is TRACEABILITY (does the claim trace to the evidence THIS PROJECT holds), NOT live reachability (that is verify.py's separate, deterministic job). Your evidence base is LOCAL and already captured:
 - the cited finding documents you are told to read;
 - verify.py's SNAPSHOTS of every cited source — intel-cache/snapshots/<sha1>.txt (the fetched text, pinned this run);
 - the KNOWLEDGE BASE of paid/internal reports: knowledge-base/by-agent/, knowledge-base/_reference/, and the page-by-page deep-reads under knowledge-base/_deepread/ (e.g. the RBR CEE/WE ATM-to-2028 reports). Use Grep to find a specific figure; do NOT read whole deep-read files.
RULE: NEVER flag a claim ungrounded merely because its original source URL is paywalled, 403s, or is offline — the source is snapshotted and/or its content is local. Check the local copies above first. Flag a claim ungrounded ONLY if it traces to NO cited source in the findings, snapshots, or knowledge base.`

const FSCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    oid: { type: 'integer' },
    verdict: { type: 'string', enum: ['grounded','thin','unsupported'] },
    ungrounded: { type: 'array', items: { type: 'string' } },
  },
  required: ['oid','verdict','ungrounded'],
}

const futValPrompt = (oid) => `You are an INDEPENDENT fact-checker. You did NOT write these projections — your only job is to check whether the 2-5yr Future-outlook projection oid=${oid} (authored by the Futurist, Agent 8) traces to the sources it cites. Be a strict but fair skeptic.
${PAYWALL}

1. Read the futures narrative (Read tool): ${FNAR}
   It has a "futures" array; find the item whose oid == ${oid}. Each item = {oid, scope, projected, rationale, drivers[], cite_files[]}.
2. Read each finding document in that future's cite_files. They are relative paths like "findings/08-futurist/research/themes/cash-recycling-deposit.md"; the absolute path is "${ROOT}" + "/" + that path. Read each (skip any that don't exist). These cited docs are your evidence base. For any figure attributed to a paid report (RBR / Datos Insights / McKinsey / Gartner / Juniper / ...), ALSO consult the knowledge base per the PAID-SOURCE policy above (Grep the deep-reads / by-agent digests for the figure).
3. Walk the future's drivers and projected headline. For each SPECIFIC, FALSIFIABLE factual claim — a number or percentage, a named programme/event, a date or deadline, a money figure, a named bank/vendor/competitor — decide whether the cited findings + knowledge base support it.
4. Do NOT flag judgment, interpretation, or the forward projection itself (those are the analyst's reasoned, labelled call — not facts to source). Flag ONLY concrete factual assertions for which you cannot find support.
5. Return one result for oid ${oid}:
   - oid (integer)
   - verdict: "grounded" (every load-bearing fact traces), "thin" (a secondary fact or two doesn't), or "unsupported" (a core claim doesn't trace).
   - ungrounded: the specific claims (quote each briefly) you could NOT locate in the findings, snapshots, or knowledge base. Empty list if everything traces. Under-claiming the gaps is the failure to avoid.`

// enumerate the futures' oids (the script can't read files; an agent does)
const fenum = await agent(`Read ${FNAR} with the Read tool and return {oids:[...]} — the integer oid of every item in its "futures" array.`,
  { label: 'enumerate:futures', phase: 'Validate futures',
    schema: { type: 'object', additionalProperties: false, properties: { oids: { type: 'array', items: { type: 'integer' } } }, required: ['oids'] } })
const foids = (fenum && fenum.oids) || []

const futResults = (await pipeline(
  foids,
  (oid) => agent(futValPrompt(oid), { label: `future:oid-${oid}`, phase: 'Validate futures', schema: FSCHEMA })
)).filter(Boolean).sort((a, b) => a.oid - b.oid)
const fflagged = futResults.filter(v => v.ungrounded && v.ungrounded.length).length
log(`validated ${futResults.length} futures — ${fflagged} carry >=1 ungrounded claim`)

// presence in futures_validation.json => "independently validated" (same contract as outlooks); verdict +
// ungrounded carry the detail. build_dashboard.py reads futures[].{validated,verdict,ungrounded}.
const futOut = futResults.map(r => ({ oid: r.oid, validated: true, verdict: r.verdict, ungrounded: r.ungrounded }))
const fwritePrompt = `Read ${FNAR} (Read tool) and note its top-level "week" value. Then use the Write tool to create a file at EXACTLY this path:
${FOUT}
Its content must be this JSON object, with <WEEK> replaced by the week you read, pretty-printed with 2-space indent. Copy every oid, verdict and ungrounded string VERBATIM — do not edit, summarise or reorder them:

{
  "week": "<WEEK>",
  "generated_by": "validate-outlooks workflow (independent traceability audit — futures)",
  "futures": ${JSON.stringify(futOut)}
}

After writing, confirm the absolute path written and the count of futures entries.`
await agent(fwritePrompt, { label: 'write:futures_validation.json', phase: 'Write' })

return { validated, flagged, futures: futResults, fflagged }
