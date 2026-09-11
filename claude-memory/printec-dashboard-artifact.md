---
name: printec-dashboard-artifact
description: The Printec Intelligence Dashboard is published as a Claude Artifact at a fixed URL; how to rebuild it, the share-pin gotcha, and why it cannot be verified in a browser from here.
metadata:
  type: project
---

The BANKING dashboard is shared with colleagues as a Claude Artifact at
**https://claude.ai/code/artifact/f8587bba-8f0d-4417-9a35-57ac4fa67ec3**
(a second artifact, "Printec Weekly Intelligence", holds the weekly brief).

**Share-pin gotcha (the important part):** the artifact's share link is *pinned to a specific version*. Republishing does NOT update what colleagues see — the owner must open the artifact → Share and move the pinned version to the latest, otherwise viewers keep seeing the old dashboard. Always tell the user this after republishing.

**Verifying it in a browser is mostly blocked — plan for that.** Two independent walls:
1. This project's sessions often descend from a scheduled task, and dev servers cannot be started from an unattended session, so `preview_start {name}` fails and there is no way to serve the built file. `file://` is refused too.
2. Opening the artifact URL DOES work, but the page runs in a **cross-origin iframe** (`<id>.frame.claudeusercontent.com`), so `read_page`/`find` stop at the iframe boundary and synthesized clicks do not reach the inner document. Navigating to the frame URL directly redirects back, and repeated attempts make the frame 403 for an anonymous session. Signed out, the URL serves the **pinned** version, not the latest — useful for seeing exactly what colleagues see.

So: verify by running the real built code in node against the real payload (extract the `<script>` blocks from the built HTML, stub `Chart`/`document`/`window`, call the actual functions and print the datasets), then ask the user to eyeball anything structural. That workflow caught real bugs; screenshots were never available.

**Rebuild recipe:** the build scripts live IN THE REPO at `weekly-intelligence/scripts/artifact/` —
`build_artifact.py` (assembles the single file), `patch_artifact.py` (build-time patches to app.js) and a
vendored `chart.umd.min.js`. Run `python3 build_artifact.py` then `patch_artifact.py`; it writes `printec-dashboard.html` (~5.2 MB, well under the 16 MB cap). **Do not keep these in the scratchpad** — an earlier copy lived in session temp and was wiped, and had to be recovered by diffing the published artifact's embedded app.js against the repo's.

`patch_artifact.py` applies its patches at BUILD TIME only (dashboard-web/app.js is never modified, so Vercel
is unaffected): (A) the offline evidence viewer, serving findings docs from `window.__DASH_DOCS__` because
`/api/evidence` does not exist in a single file; (B) the Statistical-baselines explainers. Every anchor is
asserted to match exactly once, so an upstream app.js change fails the build loudly — it did, correctly, when a column header was renamed.

Related: [[banking-collector-project]].
