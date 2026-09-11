// Client-upload bridge for the licensed source PDFs (evidence/pdfs/<slug>.pdf).
//
// WHY THIS EXISTS: the Blob store authenticates by OIDC (no static read-write token is retrievable
// locally), and OIDC is enabled only for the PRODUCTION environment — so the PDFs cannot be written
// from a dev machine directly. This route runs in the production runtime (where OIDC works), mints a
// short-lived client-upload token, and lets a local script stream the file straight to Blob storage,
// bypassing the ~4.5 MB serverless request-body limit (the WE report is 7.7 MB).
//
// It is OPEN per middleware (path starts with /api/upload, so NOT cookie-gated) — authorization is the
// shared UPLOAD_SECRET, sent by the client as clientPayload and checked here in constant time. Scope is
// locked down hard: application/pdf only, and only the evidence/pdfs/<slug>.pdf pathname shape.
import { handleUpload } from '@vercel/blob/client';
import { timingSafeEqual } from 'node:crypto';

export const config = { api: { bodyParser: false } };

const PATH_RE = /^evidence\/pdfs\/[a-z0-9][a-z0-9-]{0,63}\.pdf$/i;

async function readBody(req){
  if (req.body != null) return typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
  const chunks = []; for await (const c of req) chunks.push(Buffer.isBuffer(c) ? c : Buffer.from(c));
  return Buffer.concat(chunks).toString('utf8');
}
function safeEqual(a, b){
  const ab = Buffer.from(String(a == null ? '' : a), 'utf8');
  const bb = Buffer.from(String(b == null ? '' : b), 'utf8');
  return ab.length === bb.length && timingSafeEqual(ab, bb);
}

export default async function handler(req, res){
  if (req.method !== 'POST'){ res.setHeader('Allow', 'POST'); return res.status(405).json({ error: 'POST only' }); }
  if (!process.env.UPLOAD_SECRET) return res.status(500).json({ error: 'Server not configured: UPLOAD_SECRET missing.' });

  let body;
  try { body = JSON.parse(await readBody(req)); }
  catch (e){ return res.status(400).json({ error: 'Body is not valid JSON.' }); }

  try {
    const result = await handleUpload({
      request: req,
      body,
      onBeforeGenerateToken: async (pathname, clientPayload) => {
        if (!safeEqual(clientPayload, process.env.UPLOAD_SECRET)) throw new Error('Unauthorized.');
        if (!PATH_RE.test(pathname || '')) throw new Error('Disallowed pathname.');
        return {
          allowedContentTypes: ['application/pdf'],
          addRandomSuffix: false,
          allowOverwrite: true,
          maximumSizeInBytes: 25 * 1024 * 1024,
          cacheControlMaxAge: 31536000,
        };
      },
    });
    return res.status(200).json(result);
  } catch (e){
    return res.status(400).json({ error: e?.message || 'upload handler error' });
  }
}
