// POST /api/upload  — store this week's dashboard data in Vercel Blob.
// Auth: header  x-upload-secret: <UPLOAD_SECRET env var>
// Body: the DASH JSON produced by build_dashboard.py (dashboard-data.json).
//
// Writes three things (all private blobs, read back server-side via /api/data + /api/manifest):
//   1. archive/<week>.json   a dated snapshot kept for history (re-publishing the same week overwrites only that week)
//   2. printec-dashboard-data.json   the "latest" pointer (fast default path)
//   3. manifest.json         a small index of every archived week (for the dashboard's period picker)
//
// Required Vercel env vars:
//   UPLOAD_SECRET            a long random string you also give the orchestrator
//   BLOB_READ_WRITE_TOKEN    auto-injected once you connect a Blob store to the project
//
// No CORS headers: this is a server-to-server endpoint (the Python orchestrator), never a browser.
import { put, get } from '@vercel/blob';
import { timingSafeEqual } from 'node:crypto';

// Stream the raw body ourselves so the MAX_BYTES guard always applies (don't let the platform pre-parse it).
export const config = { api: { bodyParser: false } };

const LATEST_PATH = 'printec-dashboard-data.json';
const MANIFEST_PATH = 'manifest.json';
const MAX_BYTES = 8 * 1024 * 1024;
const WEEK_RE = /^\d{4}-\d{2}-\d{2}$/;
const PUT_OPTS = { access: 'private', addRandomSuffix: false, allowOverwrite: true,
                   contentType: 'application/json', cacheControlMaxAge: 60 };

function safeEqual(a, b){
  const ab = Buffer.from(String(a == null ? '' : a), 'utf8');
  const bb = Buffer.from(String(b == null ? '' : b), 'utf8');
  if (ab.length !== bb.length) return false;
  return timingSafeEqual(ab, bb);
}
async function readBody(req){
  if (req.body !== undefined && req.body !== null){
    return typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
  }
  const chunks = []; let total = 0;
  for await (const chunk of req){
    const buf = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += buf.length;
    if (total > MAX_BYTES){ const e = new Error('payload too large'); e.code = 413; throw e; }
    chunks.push(buf);
  }
  return Buffer.concat(chunks).toString('utf8');
}
async function readManifest(){
  try{
    const r = await get(MANIFEST_PATH, { access: 'private', useCache: false });
    if (!r || r.statusCode !== 200 || !r.stream) return { weeks: [] };
    const m = JSON.parse(await new Response(r.stream).text());
    return (m && Array.isArray(m.weeks)) ? m : { weeks: [] };
  } catch (e){ return { weeks: [] }; }
}

export default async function handler(req, res){
  if (req.method !== 'POST'){
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed — use POST.' });
  }
  if (!process.env.UPLOAD_SECRET){
    return res.status(500).json({ error: 'Server not configured: UPLOAD_SECRET is missing.' });
  }
  let header = req.headers['x-upload-secret'];
  if (Array.isArray(header)) header = header[0];
  if (!safeEqual(header, process.env.UPLOAD_SECRET)){
    return res.status(401).json({ error: 'Unauthorized.' });
  }

  let parsed;
  try { parsed = JSON.parse(await readBody(req)); }
  catch (e){
    if (e && e.code === 413) return res.status(413).json({ error: 'Payload too large.' });
    return res.status(400).json({ error: 'Body is not valid JSON.' });
  }
  if (!parsed || !Array.isArray(parsed.signals)){
    return res.status(422).json({ error: 'Payload does not look like dashboard data (missing signals[]).' });
  }
  const week = parsed.week;
  if (!week || !WEEK_RE.test(week)){
    return res.status(422).json({ error: 'Payload is missing a valid week (YYYY-MM-DD).' });
  }

  const json = JSON.stringify(parsed);
  try {
    // 1. permanent dated snapshot, 2. latest pointer
    await put('archive/' + week + '.json', json, PUT_OPTS);
    const blob = await put(LATEST_PATH, json, PUT_OPTS);

    // 3. update the week index — defensive: archive + latest already succeeded, so a manifest
    //    hiccup must NOT fail the publish. Single-writer design (one orchestrator), so the
    //    read-modify-write window is acceptable; the SDK offers no compare-and-swap on put().
    let weeksCount = null, manifestState = 'updated';
    try {
      const manifest = await readManifest();
      const k = parsed.kpis || {};
      const entry = { week, generated: parsed.generated || '',
        n_signals: k.n_signals ?? null, n_new: k.n_new ?? null, n_high: k.n_high ?? null,
        n_imminent: k.n_imminent ?? null, n_countries_active: k.n_countries_active ?? null };
      manifest.weeks = (manifest.weeks || []).filter(w => WEEK_RE.test(w.week) && w.week !== week);
      manifest.weeks.push(entry);
      manifest.weeks.sort((a, b) => (a.week < b.week ? 1 : a.week > b.week ? -1 : 0)); // newest first (ISO = lexical)
      manifest.updated = parsed.generated || '';
      await put(MANIFEST_PATH, JSON.stringify(manifest), PUT_OPTS);
      weeksCount = manifest.weeks.length;
    } catch (e){
      manifestState = 'stale';
      console.error('manifest update failed (data still published):', e?.message || e);
    }

    return res.status(200).json({ ok: true, url: blob.url, week, signals: parsed.signals.length,
                                  weeks: weeksCount, manifest: manifestState });
  } catch (e){
    return res.status(500).json({ error: 'Blob write failed: ' + (e?.message || String(e)) });
  }
}
