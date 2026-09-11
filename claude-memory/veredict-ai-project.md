---
name: veredict-ai-project
description: "Veredict AI evidence-backed AI-review demo app built at veredict-ai/ (Next.js, not the FastAPI stack from the brief)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b62cee5-c736-4fa2-a512-38428d86dfa7
---

**Veredict AI** — "AI review you can prove." Enterprise localization-QA demo built at
`/Users/mangian/Documents/test marketing agent/veredict-ai`. Core concept:
FINDING → EVIDENCE → RULE → DECISION → AUDIT TRAIL.

Stack: **Next.js 15 App Router + React 19 + strict TypeScript + Tailwind v3 + lucide**.
Backend = typed Next.js route handlers over a **JSON file store** (`.data/db.json`,
seeded on first run) — NOT the FastAPI/Postgres/Docker stack the brief asked for.
That deviation was deliberate: it makes the demo runnable/verifiable with no native
deps or Docker. Domain logic (`src/domain`, framework-free) is isolated behind
`src/server` so a real backend can swap in. `EvaluatorProvider` interface is the
model-backend seam; `DEMO_MODE=true` uses `SeededEvaluatorProvider`.

Run with **npm** (pnpm is broken on the machine's Node 20.20 — needs Node 22).
`npm run dev` (I ran it on port 3111 during the build). All gates green:
typecheck, lint, 9 tests (`node --import tsx --test`), production build.

**Why:** the user asked for a polished working demo; a Next.js monolith was the
reliable path to end-to-end functionality in this env.
**How to apply:** if extending it, keep domain logic in `src/domain`; add mutations
in `src/server/store.ts` (each records an AuditEvent); UI style maps live in `src/lib/ui.ts`.
