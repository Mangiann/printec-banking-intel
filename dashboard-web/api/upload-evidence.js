// Bulk evidence channel for the publisher (publish.py). Auth: header x-upload-secret == UPLOAD_SECRET.
//
// POST /api/upload-evidence
//   Body JSON: { week: "YYYY-MM-DD", files: [ {kind, ...} ] } sent in <=~3MB batches (snapshots total
//   ~36MB, well over the serverless body limit, so the publisher chunks them).
//     kind "finding"  {path:"findings/NN-topic/<name>.md", content}  -> evidence/<week>/findings/<path>
//     kind "snapshot" {id:"<sha1>", content}                          -> evidence/snapshots/<id>.txt
//   Snapshots are content-addressed (same source -> same path) so re-publishing just overwrites; the
//   publisher skips ones already stored (see the index GET) to avoid re-sending 36MB every week.
//
// GET /api/upload-evidence?index=snapshots  -> { snapshots: ["<sha1>", ...] } so the publisher can
//   send only the deltas.
//
// Server-to-server only (no CORS). Required env: UPLOAD_SECRET, BLOB_READ_WRITE_TOKEN.
import { put, list } from '@vercel/blob';
import { timingSafeEqual } from 'node:crypto';

export const config = { api: { bodyParser: false } };

const MAX_BYTES = 8 * 1024 * 1024;
const WEEK_RE = /^\d{4}-\d{2}-\d{2}$/;
const SNAP_RE = /^[0-9a-f]{8,64}$/i;
const FIND_RE = /^findings\/\d\d-[a-z0-9-]+\/[A-Za-z0-9._-]+\.md$/;
const PUT_OPTS = { access: 'private', addRandomSuffix: false, allowOverwrite: true,
                   contentType: 'text/plain; charset=utf-8', cacheControlMaxAge: 600 };
const SNAP_PREFIX = 'evidence/snapshots/';

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
async function listSnapshotIds(){
  const ids = []; let cursor;
  do {
    const r = await list({ prefix: SNAP_PREFIX, cursor, limit: 1000 });
    for (const b of (r.blobs || [])){
      const m = /([0-9a-f]{8,64})\.txt$/i.exec(b.pathname || '');
      if (m) ids.push(m[1]);
    }
    cursor = r.cursor;
  } while (cursor);
  return ids;
}

export default async function handler(req, res){
  if (!process.env.UPLOAD_SECRET){
    return res.status(500).json({ error: 'Server not configured: UPLOAD_SECRET is missing.' });
  }
  let header = req.headers['x-upload-secret'];
  if (Array.isArray(header)) header = header[0];
  if (!safeEqual(header, process.env.UPLOAD_SECRET)){
    return res.status(401).json({ error: 'Unauthorized.' });
  }

  if (req.method === 'GET'){
    if ((req.query && req.query.index) || /[?&]index=/.test(req.url || '')){
      try { return res.status(200).json({ snapshots: await listSnapshotIds() }); }
      catch (e){ return res.status(200).json({ snapshots: [], warning: 'index unavailable' }); }
    }
    return res.status(400).json({ error: 'Use ?index=snapshots.' });
  }
  if (req.method !== 'POST'){
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'Method not allowed.' });
  }

  let parsed;
  try { parsed = JSON.parse(await readBody(req)); }
  catch (e){
    if (e && e.code === 413) return res.status(413).json({ error: 'Batch too large.' });
    return res.status(400).json({ error: 'Body is not valid JSON.' });
  }
  const week = parsed && parsed.week;
  const files = parsed && parsed.files;
  if (week != null && !WEEK_RE.test(week)) return res.status(422).json({ error: 'Invalid week.' });
  if (!Array.isArray(files)) return res.status(422).json({ error: 'Missing files[].' });

  // NOTE: each validator MUST return a (possibly rejected) promise — never throw synchronously here.
  // A synchronous throw inside files.map() escapes Promise.allSettled and 500s the WHOLE batch instead
  // of failing just the one file. Wrap each item so a bad file becomes a rejected promise, not a crash.
  const results = await Promise.allSettled(files.map(f => {
    try {
      if (!f || typeof f.content !== 'string') throw new Error('bad file');
      if (f.kind === 'snapshot'){
        if (!SNAP_RE.test(f.id || '')) throw new Error('bad snapshot id: ' + f.id);
        return put(SNAP_PREFIX + f.id + '.txt', f.content, PUT_OPTS);
      }
      if (f.kind === 'finding'){
        if (!week) throw new Error('finding needs a week');
        if ((f.path || '').includes('..') || !FIND_RE.test(f.path || '')) throw new Error('bad path: ' + f.path);
        return put('evidence/' + week + '/' + f.path, f.content, PUT_OPTS);
      }
      throw new Error('unknown kind: ' + (f && f.kind));
    } catch (e){
      return Promise.reject(e);
    }
  }));

  const written = results.filter(r => r.status === 'fulfilled').length;
  const errors = results.filter(r => r.status === 'rejected').map(r => String(r.reason && r.reason.message || r.reason)).slice(0, 10);
  return res.status(errors.length ? 207 : 200).json({ ok: !errors.length, written, failed: errors.length, errors });
}
