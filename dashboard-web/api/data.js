// GET /api/data            — latest dashboard snapshot from the (private) Vercel Blob store.
// GET /api/data?week=YYYY-MM-DD — a specific archived week.
// Read server-side with the read-write token (never a public blob URL). 404 when not found (502 on a
// genuine read error) — either way r.ok is false, so the frontend falls back to its bundled
// ./data.json snapshot (latest) or treats the week as unavailable.
import { get } from '@vercel/blob';

const LATEST_PATH = 'printec-dashboard-data.json';
const WEEK_RE = /^\d{4}-\d{2}-\d{2}$/;

function weekParam(req){
  if (req.query && req.query.week) return req.query.week;
  try { return new URL(req.url, 'http://x').searchParams.get('week'); } catch (e){ return null; }
}

export default async function handler(req, res){
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET'){
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'Method not allowed — use GET.' });
  }
  const week = weekParam(req);
  let path = LATEST_PATH;
  if (week){
    if (!WEEK_RE.test(week)) return res.status(400).json({ error: 'Invalid week (use YYYY-MM-DD).' });
    path = 'archive/' + week + '.json';   // WEEK_RE prevents path traversal
  }
  try {
    const r = await get(path, { access: 'private', useCache: false });
    if (!r || r.statusCode !== 200 || !r.stream){
      return res.status(404).json({ error: week ? 'No data for that week.' : 'No data published yet.' });
    }
    const body = await new Response(r.stream).text();
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    // archived weeks rarely change → cache a bit longer (a re-publish propagates within ~2 min); latest → short
    res.setHeader('Cache-Control', week
      ? 'public, max-age=60, s-maxage=120'
      : 'public, max-age=15, s-maxage=30, stale-while-revalidate=120');
    return res.status(200).send(body);
  } catch (e){
    console.error('data.js read error', e?.message || e);
    return res.status(502).json({ error: 'Upstream read failed.' });   // genuine outage, not "no data"
  }
}
