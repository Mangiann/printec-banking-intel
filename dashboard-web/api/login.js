// POST /api/login  { "password": "..." }  → sets the shared-auth cookie when the password matches.
// The password + token live server-side only (never shipped to the browser). Override via env if desired.
const PASSWORD = process.env.DASH_PASSWORD || 'printec2026';
const TOKEN    = process.env.DASH_TOKEN    || 'ptx1_4f9a2c7e83b14d05a6f1e2c9';
const MAX_AGE  = 60 * 60 * 24 * 30;   // 30 days

async function readBody(req){
  if (req.body != null) return req.body;
  const chunks = []; for await (const c of req) chunks.push(c);
  return Buffer.concat(chunks).toString('utf8');
}

export default async function handler(req, res){
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST'){ res.setHeader('Allow', 'POST'); return res.status(405).json({ error: 'POST only' }); }
  let pw = '';
  try { const b = await readBody(req); const o = (typeof b === 'string') ? JSON.parse(b || '{}') : b; pw = (o && o.password) || ''; }
  catch (e){ pw = ''; }
  if (String(pw) !== PASSWORD) return res.status(401).json({ ok: false });
  res.setHeader('Set-Cookie', `dash_auth=${TOKEN}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${MAX_AGE}`);
  return res.status(200).json({ ok: true });
}
