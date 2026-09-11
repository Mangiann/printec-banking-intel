// One-time (idempotent) upload of the licensed source-report PDFs to the private Vercel Blob store,
// so /api/evidence?pdf=<slug> can serve them and the dashboard can embed them at the cited page.
//
// HOW IT WORKS: this store uses OIDC (no static read-write token is retrievable locally, and OIDC is
// enabled only for the production environment). So instead of writing to Blob directly, this streams
// each PDF DIRECTLY to Blob storage via the deployed /api/upload-blob route, which mints a short-lived
// client-upload token in the production runtime (where OIDC works). The file goes local -> Blob, never
// through the serverless body (so the ~4.5 MB request-body limit doesn't apply) and the licensed PDFs
// never enter git or the deployment bundle. Blobs are written PRIVATE.
//
// Run from the dashboard-web/ folder with the shared upload secret in the environment:
//   PowerShell:  $env:PRINTEC_UPLOAD_SECRET = "..."; node scripts/upload-pdfs.js
//   bash:        PRINTEC_UPLOAD_SECRET="..." node scripts/upload-pdfs.js
// Optionally set PRINTEC_DASHBOARD_URL (defaults to the live app). The secret must match Vercel's
// UPLOAD_SECRET. Re-running overwrites in place (allowOverwrite). Adding a new report = add it to
// knowledge-base/scripts/dr_plan.py DOCS and to the list below, then rerun.
import { upload } from '@vercel/blob/client';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const BASE = (process.env.PRINTEC_DASHBOARD_URL || 'https://printec-market-research.vercel.app').replace(/\/+$/, '');
const SECRET = process.env.PRINTEC_UPLOAD_SECRET || process.env.UPLOAD_SECRET;

// slug -> source file. Slugs MUST match the ?pdf=<slug> links emitted in the dashboard data
// (source of truth: knowledge-base/scripts/dr_plan.py DOCS).
const PROC = path.resolve('..', 'knowledge-base', 'processed');
const DOCS = [
  { slug: 'rbr-cee-atm-2028', file: 'RBR Reports - Central and Eastern Europe ATM Market and Forecasts to 2028 (NCR Atleos)[34] (1).pdf' },
  { slug: 'rbr-we-atm-2028',  file: 'RBR Reports - Western Europe ATM Market and Forecasts to 2028 (NCR Atleos) (1).pdf' },
];

if (!SECRET){
  console.error('Set PRINTEC_UPLOAD_SECRET (must equal Vercel UPLOAD_SECRET). See the header of this file.');
  process.exit(1);
}

let failed = 0;
for (const d of DOCS){
  const src = path.join(PROC, d.file);
  const dest = `evidence/pdfs/${d.slug}.pdf`;
  try {
    await stat(src);
    const buf = await readFile(src);
    const res = await upload(dest, buf, {
      access: 'private',
      contentType: 'application/pdf',
      multipart: true,
      handleUploadUrl: `${BASE}/api/upload-blob`,
      clientPayload: SECRET,
    });
    console.log(`✓ ${dest}  (${(buf.length / 1048576).toFixed(2)} MB)  ${res.url}`);
  } catch (e){
    failed++;
    console.error(`✗ ${dest}  — ${e?.message || e}`);
  }
}
process.exit(failed ? 1 : 0);
