# Scheduled agents — backup & migration (Enterprise → Team)

**Nothing here depends on the account.** Each agent's instructions live in three places in this repo:
`scheduled-agents-backup/<id>/SKILL.md` (the scheduled-task prompt, frozen from the live tasks 2026-06-24),
`agent-briefs/*.md` (the detailed brief each task tells the agent to follow), and `research-playbook.md`.
Only the *schedule registration* and stored tool-approvals live in the account/scheduler — those are
documented below so they can be recreated exactly.

## ⚠️ CRITICAL: these must be LOCAL scheduled tasks, NOT cloud "routines"

Claude Code has **two** scheduling systems:

| | LOCAL scheduled task (Desktop → Routines → **Local**) | CLOUD routine (`/schedule`, claude.ai/code/routines) |
|---|---|---|
| Runs on | your machine (app must be open) | Anthropic cloud infra |
| Local file access (`C:\…\Dropbox\…`) | **YES** | **NO** — fresh git clone each run |
| Local Python engine (`run_weekly.py` etc.) | **YES** | NO |
| Plan availability | all plans incl. **Team** | all plans incl. Team |

This whole system reads/writes local files (`findings/`, `intel-cache/`, `knowledge-base/`,
`dashboard-web/`) and runs a local Python engine. It will ONLY work as **LOCAL** tasks. A cloud
routine cannot see the Dropbox folder or run the engine — do not recreate these as cloud routines.

Local tasks ARE available on Team. The likely reason they "disappeared" on the Team login is that the
scheduler view is login-scoped — the task files may still be on disk at
`C:\Users\User\.claude\scheduled-tasks\<id>\SKILL.md` under this OS user. Check there first; if present,
they may just need re-enabling. The repo backup below is the safety net regardless.

## How to recreate each task on Team

For every row below: Desktop app → **Routines → New routine → Local** (or ask Claude in a session to
"set up a local scheduled task in folder C:\…\BANKING"), then:
1. **Prompt** = the full body of `scheduled-agents-backup/<id>/SKILL.md` (verbatim).
2. **Working folder** = `C:\Users\User\Dropbox\E - PRINTEC GROUP\AI\MARKET RESEARCH\BANKING`.
3. **Schedule** = the cron below (local time).
4. After creating, do ONE manual **"Run now"** and approve the tools it requests (web search/fetch; for
   agent-7 also Python + Workflow; for data-dump also Python). Approvals are stored on the task so later
   unattended runs don't stall on a permission prompt (this is what blocked the 2026-06-24 morning run).

## The 9 tasks — schedules

`<id>` = both the scheduler task id and the backup sub-folder name.

| id | Intended production cadence | cron (production) | Current live cron (2026-06-24, temporary Wed test) |
|---|---|---|---|
| agent-1-bank-disclosures | Monthly, 1st ~08:00 | `0 8 1 * *` | `0 5 * * 3` |
| agent-2-tenders-procurement | Weekly, Fri ~09:09 | `9 9 * * 5` | `0 7 * * 3` |
| agent-3-regulation-deadlines | 1st & 15th ~09:00 | `0 9 1,15 * *` | `0 9 1,15 * *` (unchanged) |
| agent-4-market-statistics | Monthly, 1st ~08:30 | `30 8 1 * *` | `0 9 * * 3` |
| agent-5-jobs-early-intent | Weekly, Fri ~09:31 | `31 9 * * 5` | `0 10 * * 3` |
| agent-6-vendors-competitors | Weekly, Fri ~10:04 | `4 10 * * 5` | `0 11 * * 3` |
| agent-7-orchestrator | Weekly, Fri ~12:03 (AFTER collectors) | `3 12 * * 5` | `0 16 * * 3` |
| agent-8-futurist | Monthly, 1st ~08:15 | `15 8 1 * *` | `15 8 1 * *` (unchanged) |
| data-dump-processor | Daily ~00:07 | `7 0 * * *` | `0 1 * * *` |

NOTE: agents 1,2,4,5,6,7 were temporarily shifted to **Wednesday** on 2026-06-24 to test a same-day run;
the "production cadence" column is the original Friday/monthly design. Recreate with the production cron
unless you still want the Wednesday test cadence.

## Ordering dependency (don't break it)

The collectors (1–6) must run before the orchestrator (7) each week; the orchestrator triangulates their
findings, then writes outlooks → spawns the validator → runs the engine → publishes. The Futurist (8) is
monthly and feeds the orchestrator's reading + the dashboard's Future-outlook tab. Keep agent-7 scheduled
*after* the collectors on the same day.

## Live-publish env vars (set in the runner's environment, not just a shell)

`PRINTEC_DASHBOARD_URL` = `https://printec-market-research.vercel.app`
`PRINTEC_UPLOAD_SECRET` = (the Vercel project's `UPLOAD_SECRET`)
Without both, the build succeeds locally but the live Vercel dashboard isn't updated.
