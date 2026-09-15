---
name: banking-repo-github
description: "BANKING project is a Git repo pushed to the user's personal GitHub (temporary home until IT provides Azure DevOps); what is excluded and where the old dashboard-web history sits"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9a51b16c-1ba3-43e8-aabe-9882bfb8346d
  modified: 2026-09-11T08:49:41.130Z
---

`~/Downloads/BANKING` became a Git repository on 11/09/2026 (branch `main`, remote `origin` = https://github.com/Mangiann/printec-banking-intel, private, the user's personal account — IT approved it as a temporary home; the intended final home is an Azure DevOps repo plus an Azure Static Web App for the dashboard).

Excluded by `.gitignore`: `.env*`, `node_modules`, `intel-cache/snapshots/` (488 MB web captures), `_*-backup-*/` folders, the licensed RBR PDFs and their `rbr-*.md` extracts, `scratch_*.txt`. The repo also carries copies of the scheduled agent tasks (`scheduled-agents-backup/`) and of these memory notes (`claude-memory/`).

The old `dashboard-web` Vercel repo (40 commits, remote github.com/karakasi/Printec-market-research) had its `.git` moved to `~/Downloads/BANKING-dashboard-web-dotgit-backup`. The Vercel deployment itself is gone (404).

The files kept out of Git (secrets, licensed RBR reports and extracts, backup folders, snapshots zip, old dashboard-web Git history) are copied to the user's Printec OneDrive: `~/Library/CloudStorage/OneDrive-PrintecS.A/Printec-banking-backup/<date>/` (first copy 11/09/2026, 173 MB, with a README). Never use the KorrDot OneDrive for Printec material — the user refused it.

**How to apply:** when the user says "push", commit the day's changes in BANKING and push `main`. Commit as user.name `mangian`, email mangian27@gmail.com (repo-local config). See [[printec-dashboard-artifact]] and [[banking-collector-project]].
