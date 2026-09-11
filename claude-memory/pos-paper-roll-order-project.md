---
name: pos-paper-roll-order-project
description: "The POS paper-roll ordering chatbot project — location, stack, DB approach, and status"
metadata: 
  node_type: memory
  type: project
  originSessionId: b62eba77-999e-4283-94b4-46d98e04c976
---

Deterministic (no-GenAI) chatbot for a SINGLE bank's VIP merchants in BiH to request
thermal paper-roll delivery for EFT POS terminals, validating the terminal by TID +
serial number and creating a mock FSM request (future SAP FSM Service Call). Fully
rewritten from the earlier generic "order paper rolls" flow.

- **Location:** `/Users/mangian/POS paper roll order` (spaces — always quote the path). OUTSIDE the session's default working dir; treat it as the project root.
- **Stack:** Node 20, TypeScript strict, Fastify 5, Prisma 7, Zod, Vitest, ESLint/Prettier, Docker. Modular monolith.
- **DB approach (non-obvious):** no Docker/Postgres on this machine. Runtime uses a Prisma driver adapter by `DB_DRIVER`: `pglite` (in-process Postgres via `pglite-prisma-adapter`, default for local/demo/tests) or `pg` (Docker). PGlite DDL is generated from the schema via `prisma migrate diff --from-empty --to-schema ... --script` into `prisma/pglite-schema.sql` and applied at startup. Prisma 7 gotcha: datasource `url` lives in `prisma.config.ts`, not `schema.prisma`. Regenerate DDL + client after any schema change.
- **Architecture:** shared channel model (`src/channels/channel.types.ts`) + one conversation engine (`src/conversations/state-machine.ts`, 24-state `ConversationState` enum). Providers behind interfaces: `TerminalRegistryClient` (mock/excel/http, `src/terminals/`) and `FsmRequestClient` (mock/http, `src/fsm/`). Everything scoped by `BANK_ID`; merchant never picks a bank. Bosnian is the merchant language; en is dev-only.
- **Status (2026-07-19): COMPLETE bank-workflow rewrite, all green.** 85 Vitest tests pass, lint 0 errors, `tsc`/build clean. Simulator verified live (welcome→model→TID `12345678`→serial `100-200-300`→confirm→`FSM-DEMO-2026-*`; duplicate confirm = no 2nd request). WhatsApp Cloud API adapter BUILT but disabled (`WHATSAPP_ENABLED=false`); Viber skeleton BUILT but disabled. 14 docs + README written.
- **Demo TIDs (seeded, fake):** 12345678 (happy, V240m, serial 100-200-300, VIP), 22345678 (Castles S1F2, 5000000022), 33345678 (VIP-ineligible), 44345678 (has recent request), 55345678 (inactive merchant), 99999999 (not found). Serial rules: Verifone = 3-3-3 hyphenated PRESERVE_HYPHENS; Castles = 10 digits DIGITS_ONLY.
- **Still mocked / before production:** no live SAP/FSM or ticketing call ever; confirm real registry + FSM HTTP contracts; replace demo admin Basic auth; official terminal images/instructions + real call-centre number need bank/Printec approval. Terminal images are labelled DEMO placeholders (`src/simulator-ui/assets/terminals/*.svg`).
- Run: `npm run dev` → http://localhost:3000/simulator ; admin `/admin` (admin/demo-admin-password). Tests: `npm test`.

## Live WhatsApp demo — restart checklist (added 2026-07-29; DEMO 2026-07-30 11:30)
Real WhatsApp works end-to-end (created FSM-DEMO-2026-000125/127 via WHATSAPP_CHATBOT). To bring it live after idle:
1. Start app: `npx tsx src/app/server.ts` (reads .env; WHATSAPP_ENABLED=true).
2. Start tunnel: `cloudflared tunnel --url http://localhost:3000` → NEW https URL each time (quick tunnel is ephemeral). macOS negative-DNS-cache can make local curl 000 briefly; verify via `--resolve` or trust Meta.
3. Meta webhook: paste `<tunnel>/webhooks/whatsapp` as Callback URL + existing WHATSAPP_VERIFY_TOKEN → Verify and save. (messages field + WABA subscribed_apps persist.)
4. Token: temp token from WhatsApp→API Setup expires ~24h → paste into WHATSAPP_ACCESS_TOKEN, restart app. RECOMMEND permanent System-User token (never expires; whatsapp_business_messaging + whatsapp_business_management scopes).
5. Recipient: user's phone must be in test-number allowed recipients (Meta→API Setup→Manage phone number list; ~5 max). 131030 = recipient not allowed.
6. Clean demo: reset test orders/conversations (keep seeded terminals/merchants). 15-day recent-request guard makes reused TID 12345678 show "delivered?" prompt — use TID 22345678/serial 5000000022 for a clean fresh order.
7. Diagnostics that don't leak secrets: token check via `graph.facebook.com/<ver>/<PID>?fields=display_phone_number`; app logs "whatsapp inbound message" (no phone/content); outbound errors show Graph code (190=expired token, 131030=recipient, 100=bad image URI). Browser previews /wa /vi /simulator are the reliable demo surface (no token/tunnel).

## Networking gotchas discovered 2026-07-30 (demo day)
- Some venue/guest Wi-Fi BLOCKS cloudflared's default QUIC/UDP transport → tunnel stuck "control stream encountered a failure / Retrying / Tunnel not found". FIX: `cloudflared tunnel --url http://localhost:3000 --protocol http2` (TCP) — connects instantly where QUIC fails. Quick-tunnel URL still changes each restart → re-point Meta webhook Callback URL.
- Same network also blocked Node's outbound HTTPS to graph.facebook.com (undici "fetch failed"/timeout) while `curl` worked — not TLS (NODE_TLS_REJECT_UNAUTHORIZED=0 didn't help), not proxy. App can't send WhatsApp replies on such a network → inbound arrives but no reply. FIX: use a phone hotspot / different network. Start app with `NODE_OPTIONS=--dns-result-order=ipv4first` as a mitigation for IPv6 stalls.
- Diagnosis pattern: inbound works (Meta→Cloudflare→tunnel) but outbound fails (app→Meta via Node) → it's the local network blocking Node egress, not phones/recipients. Verify tunnel externally with `curl --resolve <host>:443:<edgeIP>` (bypasses macOS negative-DNS cache). Browser previews /wa /vi /simulator need ZERO internet — always the safe demo fallback.
