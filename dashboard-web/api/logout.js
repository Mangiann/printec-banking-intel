// GET /api/logout  → clears the auth cookie and bounces back to the login page.
export default function handler(req, res){
  res.setHeader('Set-Cookie', 'dash_auth=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0');
  res.setHeader('Cache-Control', 'no-store');
  res.statusCode = 302;
  res.setHeader('Location', '/login');
  return res.end();
}
