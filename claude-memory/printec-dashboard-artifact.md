---
name: printec-dashboard-artifact
description: The Printec Intelligence Dashboard is published as two Claude Artifacts (a personal one and the Printec/Enterprise one); the URLs, how to rebuild it, the share-pin gotcha, and why it cannot be verified in a browser from here.
metadata:
  type: project
---

The BANKING dashboard is shared with colleagues as a Claude Artifact at
**https://claude.ai/code/artifact/f8587bba-8f0d-4417-9a35-57ac4fa67ec3** (since 16/09/2026 the platform lists it under the short link https://claude.ai/artifact/Xfg3R2ND4oGgLG8fkMdTwY; same artifact, version 66 carries the "Ask the data" chat and declares `capabilities: {sample: {}}` — keep declaring it on every republish, a non-empty capabilities object is a full-set declaration)
(a second artifact, "Printec Weekly Intelligence", holds the weekly brief).

**The Printec (Enterprise) copy — use this one for colleagues.** Published 17/09/2026 from the Printec
account as a separate artifact: **https://claude.ai/artifact/8a7CuDd3HCX6WQWAfbXLqA** (title "Printec
Intelligence Dashboard", favicon 📊, `capabilities: {sample: {}}`, runtime contract 0.2.52). Version 1 is
the `build 17/09/2026 15:09` file — the €180.0m single-budget decision plus the budget-by-category
waterfalls. **Version 2** (17/09/2026) = the next republish of the same built file from this project. **Version 3** (17/09/2026) = republish of the 7.4 MB built file (budget-by-category build). **Version 4** (17/09/2026) = the `build 17/09/2026 17:04` file (7.5 MB). **Version 5** (18/09/2026) = the `build 18/09/2026 17:51` file (7.5 MB). The personal link above is now the *test* copy (memory rule: test on personal, publish from
Enterprise); do NOT republish over the personal URL when colleagues are meant to see the change, and do not
pass the personal URL as `url` when updating the Printec one — they are two artifacts with two histories.
The share link the user received from the Printec publish carries a share key: https://claude.ai/artifact/8a7CuDd3HCX6WQWAfbXLqA?sk=Qk1b7q_AsA3Hta9UytOZPQ (17/09/2026) — that is the link colleagues get; the base URL without `sk` is the one to pass as `url` when republishing. Updating the Printec copy needs a session signed into the Printec account (the personal session lists only the personal artifacts as "mine").

Publishing it from a fresh session means copying the built file into the scratchpad first: the Artifact tool
only accepts sources under the working directory or the scratchpad, and this project's working directory is
not the BANKING repo.

**Share-pin gotcha — but check the sharing mode first.** On 17/09/2026, reading the Printec/Enterprise artifact reported it as *"owned by you, shared with your organization (viewers see updates immediately)"*, and version 2 was published there. So for the org-shared Printec copy no pin move appears to be needed. The pin gotcha still applies to a share link carrying an `?sk=` share key and to what an anonymous/signed-out viewer sees: that serves the *pinned* version, so if colleagues are using the `sk=` link, the owner must open the artifact → Share and move the pinned version to the latest. After republishing, say which of the two applies rather than asserting the pin move unconditionally.

**Verifying it in a browser is mostly blocked — plan for that.** Two independent walls:
1. This project's sessions often descend from a scheduled task, and dev servers cannot be started from an unattended session, so `preview_start {name}` fails and there is no way to serve the built file. `file://` is refused too.
2. Opening the artifact URL DOES work, but the page runs in a **cross-origin iframe** (`<id>.frame.claudeusercontent.com`), so `read_page`/`find` stop at the iframe boundary and synthesized clicks do not reach the inner document. Navigating to the frame URL directly redirects back, and repeated attempts make the frame 403 for an anonymous session. Signed out, the URL serves the **pinned** version, not the latest — useful for seeing exactly what colleagues see.

So: verify by running the real built code in node against the real payload (extract the `<script>` blocks from the built HTML, stub `Chart`/`document`/`window`, call the actual functions and print the datasets), then ask the user to eyeball anything structural. That workflow caught real bugs; screenshots were never available.

**Rebuild recipe:** the build scripts live IN THE REPO at `weekly-intelligence/scripts/artifact/` —
`build_artifact.py` (assembles the single file), `patch_artifact.py` (build-time patches to app.js) and a
vendored `chart.umd.min.js`. Run `python3 build_artifact.py` then `patch_artifact.py`; it writes `printec-dashboard.html` (~7.4 MB as of 17/09/2026, well under the 16 MB cap). **Do not keep these in the scratchpad** — an earlier copy lived in session temp and was wiped, and had to be recovered by diffing the published artifact's embedded app.js against the repo's.

`patch_artifact.py` applies its patches at BUILD TIME only (dashboard-web/app.js is never modified, so Vercel
is unaffected): (A) the offline evidence viewer, serving findings docs from `window.__DASH_DOCS__` because
`/api/evidence` does not exist in a single file; (B) the Statistical-baselines explainers. Every anchor is
asserted to match exactly once, so an upstream app.js change fails the build loudly — it did, correctly, when a column header was renamed.

Related: [[banking-collector-project]].

**Publishing to Printec without switching accounts (set up 18/09/2026):** the company pays for both accounts; the user keeps the desktop app on the personal Max account for the work ("better results") and publishes to the Printec artifact from the terminal with a SECOND stored login: Claude Code CLI installed with npm into the user's nvm node (v2.1.197, no sudo), login kept in `CLAUDE_CONFIG_DIR=~/.claude-printec` (one-time `/login` with the Printec account, done by the user). Script: `weekly-intelligence/scripts/artifact/publish_printec.sh` (headless `claude -p --dangerously-skip-permissions --allowedTools Artifact,Read`, cwd ~/Downloads/BANKING so the built file is under the working directory, prompt passes the Printec URL as `url` and keeps `capabilities {sample:{}}`). First run is a test: if the Artifact tool is unavailable in print mode or the flag names differ, adjust the script. Note the shell has a `claude` function wrapper (claude-auto-retry) — the script uses `command claude`.
