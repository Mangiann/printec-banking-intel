// GET /api/evidence?path=findings/<NN-topic>/<name>.md&week=YYYY-MM-DD
//   -> the agent's source DOCUMENT for that week  (evidence/<week>/findings/...)   [served inert text/plain]
// GET /api/evidence?snapshot=<sha1>
//   -> the point-in-time SNAPSHOT of a cited source (evidence/snapshots/<sha1>.txt), content-addressed
//      and week-independent (the link-rot defense capture).                         [served inert text/plain]
// GET /api/evidence?pdf=<slug>            (optionally with a #page=N fragment, applied client-side)
//   -> a licensed/internal SOURCE REPORT (evidence/pdfs/<slug>.pdf), served as application/pdf so the
//      dashboard can embed it at the cited page. These are our own first-party files (not third-party HTML),
//      so they are served WITHOUT the nosniff/text-plain inerting the snapshots get. The whole site —
//      including this endpoint — sits behind the shared-password edge middleware, so the reports are only
//      reachable by a signed-in user.
//
// Read server-side from the (private) Blob store, like /api/data.
// 400 invalid input · 404 not found · 502 read error.
import { get } from '@vercel/blob';

const WEEK_RE = /^\d{4}-\d{2}-\d{2}$/;
const SNAP_RE = /^[0-9a-f]{8,64}$/i;                              // sha1-style snapshot id (no extension)
const FIND_RE = /^findings\/\d\d-[a-z0-9-]+\/[A-Za-z0-9._-]+\.md$/; // findings/NN-topic/<name>.md
const PDF_RE  = /^[a-z0-9][a-z0-9-]{0,63}$/i;                     // pdf slug (e.g. rbr-cee-atm-2028)

function q(req, name){
  if (req.query && req.query[name] != null) return req.query[name];
  try { return new URL(req.url, 'http://x').searchParams.get(name); } catch (e){ return null; }
}

export default async function handler(req, res){
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET' && req.method !== 'HEAD'){
    res.setHeader('Allow', 'GET, HEAD');
    return res.status(405).json({ error: 'Method not allowed — use GET.' });
  }

  const pdf  = q(req, 'pdf');
  const snap = q(req, 'snapshot');
  let blobPath, filename;
  let mime = 'text/plain; charset=utf-8', inert = true, cache = 'public, max-age=300, s-maxage=600, stale-while-revalidate=120';
  if (pdf){
    if (!PDF_RE.test(pdf)) return res.status(400).json({ error: 'Invalid pdf id.' });
    blobPath = 'evidence/pdfs/' + pdf + '.pdf';
    filename = pdf + '.pdf';
    mime = 'application/pdf';
    inert = false;                                  // our own report — serve for inline viewing, no nosniff
    cache = 'private, max-age=86400';               // licensed: browser-cache only, never a shared CDN copy
  } else if (snap){
    if (!SNAP_RE.test(snap)) return res.status(400).json({ error: 'Invalid snapshot id.' });
    blobPath = 'evidence/snapshots/' + snap + '.txt';
    filename = snap + '.txt';
  } else {
    const path = q(req, 'path') || '';
    const week = q(req, 'week') || '';
    if (path.includes('..') || !FIND_RE.test(path)) return res.status(400).json({ error: 'Invalid path.' });
    if (week && !WEEK_RE.test(week)) return res.status(400).json({ error: 'Invalid week.' });
    blobPath = 'evidence/' + (week ? week + '/' : '') + path;     // WEEK_RE/FIND_RE prevent traversal
    filename = path.split('/').pop();
  }

  try {
    const r = await get(blobPath, { access: 'private', useCache: false });
    if (!r || r.statusCode !== 200 || !r.stream){
      return res.status(404).json({ error: 'Evidence not found (publish it first).' });
    }
    res.setHeader('Content-Type', mime);
    if (inert) res.setHeader('X-Content-Type-Options', 'nosniff');  // snapshots are third-party HTML — never sniff
    res.setHeader('Content-Disposition', 'inline; filename="' + filename.replace(/[^A-Za-z0-9._-]/g, '_') + '"');
    res.setHeader('Cache-Control', cache);
    if (req.method === 'HEAD') return res.status(200).end();        // existence/type probe (used by the viewer)
    if (inert){
      const body = await new Response(r.stream).text();
      return res.status(200).send(body);
    }
    const buf = Buffer.from(await new Response(r.stream).arrayBuffer());  // binary — must NOT go through .text()
    res.setHeader('Content-Length', String(buf.length));
    return res.status(200).send(buf);
  } catch (e){
    console.error('evidence.js read error', e?.message || e);
    return res.status(502).json({ error: 'Upstream read failed.' });
  }
}
