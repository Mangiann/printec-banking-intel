// Edge middleware — a single shared-password gate for the whole dashboard + its data/evidence APIs.
// The publish endpoints (/api/upload*) carry their own UPLOAD_SECRET, so they are NEVER gated here
// (otherwise the weekly run could not POST). The login page + login/logout APIs are also open.
// Auth is a cookie holding a server-only TOKEN, set by /api/login when the password matches.
import { next } from '@vercel/edge';

export const config = { matcher: '/(.*)' };

const TOKEN = process.env.DASH_TOKEN || 'ptx1_4f9a2c7e83b14d05a6f1e2c9';

function isOpen(p){
  return p === '/login' || p === '/login.html'
      || p.startsWith('/api/login') || p.startsWith('/api/logout')
      || p.startsWith('/api/upload');           // /api/upload + /api/upload-evidence (own secret)
}

export default function middleware(req){
  const url = new URL(req.url);
  const p = url.pathname;
  if (isOpen(p)) return next();
  const cookie = req.headers.get('cookie') || '';
  if (cookie.split(/; */).some(c => c === 'dash_auth=' + TOKEN)) return next();
  // not signed in
  const accept = req.headers.get('accept') || '';
  if (req.method === 'GET' && accept.includes('text/html')){
    const to = new URL('/login', req.url);
    to.searchParams.set('next', p + url.search);
    return Response.redirect(to, 302);
  }
  return new Response('Unauthorized — sign in at /login', { status: 401 });
}
