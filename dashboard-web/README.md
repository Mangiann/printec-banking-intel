# Printec Banking Intelligence — live dashboard

A static dashboard (the redesigned "ivory" UI) that always shows the latest weekly run.
The orchestrator publishes each week's data to Vercel Blob through this app's own API;
the page reads it back from `/api/data`. No redeploy is needed to update the data.

```
dashboard-web/
├─ index.html        the dashboard shell
├─ styles.css        the design system
├─ app.js            renders the DASH data into the UI
├─ data.json         bundled fallback snapshot (last committed week) — shown until the live feed has data
├─ api/
│  ├─ data.js            GET  → latest data, or ?week=YYYY-MM-DD for an archived week (404 when missing)
│  ├─ manifest.js        GET  → index of archived weeks (powers the period picker)
│  ├─ upload.js          POST → store this week's data in Blob: archive/<week>.json + latest + manifest.json
│  ├─ evidence.js        GET  → a source document (?path=findings/…&week=…) or snapshot (?snapshot=<sha1>), inert text/plain
│  └─ upload-evidence.js POST → store source documents + link-rot snapshots; GET ?index=snapshots → dedup index
├─ package.json      one dependency: @vercel/blob
└─ vercel.json       static + functions config
```

## One-time setup (Vercel + GitHub)

1. **Push this folder to a GitHub repo** (e.g. `printec-banking-dashboard`).
   From inside `dashboard-web/`:
   ```bash
   git init && git add . && git commit -m "Printec banking dashboard"
   git branch -M main
   git remote add origin https://github.com/<you>/printec-banking-dashboard.git
   git push -u origin main
   ```

2. **Import the repo into Vercel** → *Add New… → Project → Import*. Framework preset: **Other**.
   Leave Build Command empty and Output Directory default — it's a static site plus serverless
   functions, so Vercel needs no build step (it just installs `@vercel/blob` for the functions).

3. **Add a Blob store**: Vercel project → *Storage → Create → Blob → Connect to project*.
   This auto-injects the `BLOB_READ_WRITE_TOKEN` env var the functions need.

4. **Add the upload secret**: Vercel project → *Settings → Environment Variables* →
   add `UPLOAD_SECRET` = a long random string (e.g. `openssl rand -hex 24`). Apply to Production
   (and Preview if you want). Redeploy once so the functions pick it up.

5. Open the deployment URL. It shows the **bundled snapshot** (`data.json`) until the first
   weekly publish, then flips to **live** automatically. Note your URL — e.g.
   `https://printec-banking-dashboard.vercel.app`.

## Weekly: how the data gets there

The orchestrator's weekly run does this for you (see `weekly-intelligence/scripts/publish.py`, run by
`run_weekly.py`). It POSTs the freshly-built `dashboard-data.json` to your site:

```
POST https://<your-app>.vercel.app/api/upload
Header  x-upload-secret: <UPLOAD_SECRET>
Body    <the dashboard-data.json contents>
```

Give the orchestrator two env vars so it can publish:

| Env var                  | Value                                             |
|--------------------------|---------------------------------------------------|
| `PRINTEC_DASHBOARD_URL`  | `https://<your-app>.vercel.app`                   |
| `PRINTEC_UPLOAD_SECRET`  | the same value you set as `UPLOAD_SECRET` in Vercel |

Manual test of the live endpoint (PowerShell):
```powershell
$body = Get-Content -Raw ..\intel-cache\dashboard-data.json
Invoke-RestMethod -Method Post -Uri "https://<your-app>.vercel.app/api/upload" `
  -Headers @{ "x-upload-secret" = "<UPLOAD_SECRET>"; "content-type" = "application/json" } `
  -Body $body
```
A `200 { ok: true, url, week, signals }` response means it's live. Reload the dashboard.

## History (week / month time-travel)

Every publish keeps a permanent dated snapshot (`archive/<week>.json`) and updates `manifest.json`, so
the dashboard's **period picker** (top-right) can show any past week or a **monthly rollup** — no extra
step for you; each weekly run archives automatically. The picker offers:

- **Latest** — the current week (default).
- **A past week** — loads that week's exact archived snapshot ("as-of" caption shown).
- **A month** — month-end state + a start→end delta ("X new this month", the full month movement) — the
  ready-made "what moved this month" view for the monthly strategy review.

History only accrues from publishes made by *this* version of `/api/upload`. A week published by an
older handler won't appear until it's re-published once (POST its `dashboard-data.json` to `/api/upload`).

## Source documents & snapshots (the evidence trail)

Each signal card has an **Evidence trail**: every external source the trust pass (`verify.py`) re-fetched,
clickable, with a ✓ reachable / ⚠ unreachable marker — plus a link to the agent's full **source document**
and, for each reachable source, an **archived** point-in-time **snapshot** (so a dead link still opens its
capture). These are served by `/api/evidence` from Blob.

`publish.py` uploads the evidence automatically after the data push (same `UPLOAD_SECRET`; no new env var):

- **Documents** — the ~12 agent finding `.md` files (~250 KB) → `evidence/<week>/findings/…`.
- **Snapshots** — the link-rot captures (~36 MB) → `evidence/snapshots/<sha1>.txt`, content-addressed.
  They're sent in size-bounded batches and **de-duplicated** against what the store already holds
  (`GET /api/upload-evidence?index=snapshots`), so the ~36 MB is a one-time cost; later weeks send only
  new captures. Pass `--no-evidence` to skip, or `--evidence-dry-run` to preview what would be sent.

**Source links everywhere, not just on cards.** Beyond the per-signal evidence trail, the dashboard renders
clickable citations embedded in the other free-text fields too: the **milestone timeline** (Patterns) shows a
*Source* link per event (from the workbook's `URL` column), and the **regulatory deadlines** (Accounts), the
**market statistics** (Countries → Market detail) and the **outlook drivers** (Outlook) turn any markdown
`[label](https://…)`, bare `https://…` URL, or internal `findings/…md` ref written into those strings into a
link. The orchestrator brief tells Agent 7 to embed those citations; until a field carries one it just shows as
plain text (no link), so this degrades gracefully.

**Outlook evidence trail.** Each reasoned outlook (the Outlook tab) is analyst judgment, but every fact in it
comes from specific signals + agent findings — so each outlook card shows a **Built on …** list of the master-
table signals it synthesizes plus a collapsible **Evidence trail** of the agent source documents behind it (same
✓/⚠ + snapshot + open-document UI as the signal cards). The engine (`build_dashboard.py`) attaches these from the
outlook's `cite_signals`/`cite_files` (written by the orchestrator) or, as a fallback, by parsing the inline
`(A#)` agent tags + the country's signals, so every outlook gets a trail.

**Public exposure:** the dashboard URL is public/no-auth, so published evidence is publicly reachable too.
Snapshots are captures of already-public pages + bank IR PDFs, so this is normally fine — but it is a
conscious choice. `/api/evidence` always serves `text/plain` with `X-Content-Type-Options: nosniff`, so a
captured third-party page is shown as inert source, never rendered/executed on this origin.

## Notes

- **Updating the look** — edit `styles.css` / `app.js` / `index.html`, push, Vercel redeploys.
- **`data.json`** is only a fallback for the very first load / if Blob is empty. The weekly run also
  refreshes it locally so a future `git push` keeps the committed snapshot current (optional — the
  live feed does not depend on it).
- If `npm install` ever fails on `@vercel/blob`, bump it: `npm i @vercel/blob@latest`, commit, push.
