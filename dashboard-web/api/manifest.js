// GET /api/manifest  — the index of archived weeks (for the dashboard's period picker).
// Returns { updated, weeks: [{week, generated, n_signals, n_new, n_high, n_imminent, n_countries_active}, ...] }
// newest first. Returns {"weeks":[]} (HTTP 200) when nothing is published yet or on error, so the
// frontend always gets a valid shape and falls back to a single-week (latest-only) selector.
import { get } from '@vercel/blob';

const MANIFEST_PATH = 'manifest.json';
const EMPTY = '{"weeks":[]}';

export default async function handler(req, res){
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET'){
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'Method not allowed — use GET.' });
  }
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  try {
    const r = await get(MANIFEST_PATH, { access: 'private', useCache: false });
    if (!r || r.statusCode !== 200 || !r.stream){ return res.status(200).send(EMPTY); }
    const body = await new Response(r.stream).text();
    res.setHeader('Cache-Control', 'public, max-age=30, s-maxage=60, stale-while-revalidate=120');
    return res.status(200).send(body);
  } catch (e){
    console.error('manifest.js error', e?.message || e);
    return res.status(503).json({ error: 'Manifest read failed.' });   // genuine error ≠ "nothing published yet" (200 EMPTY)
  }
}
