/* Standalone architecture explorer (architecture.html) — a full-page pan/zoom canvas.
   Overview = colored-card ORGANOGRAM (who's who). Detailed = a DECISION FLOW-CHART (when each
   agent/script/tool fires and the decisions between them). Click any node → drawer with the verbatim
   prompt, rules, scripts, I/O. Agent nodes carry a robot icon; scripts a gear; files a doc. Data: window.ARCH. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const esc = s => String(s == null ? "" : s).replace(/[&<>]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[m]));
  const C = { cyan: ["#D3EFF8", "#0B6F87"], blue: ["#CFE1F3", "#27506F"], lilac: ["#E0D4F4", "#553897"], green: ["#D2E2B4", "#3D5A1C"], yellow: ["#F8E9A0", "#7A5C00"], peach: ["#F4D9CE", "#9C4A36"], teal: ["#CFE7E0", "#1C5A4A"], sand: ["#EFE7D6", "#6E685B"] };
  const SOLID = { cyan: "#23C0E2", blue: "#A4C6E7", lilac: "#BFA7E6", green: "#A6C47C", yellow: "#F0CF49", peach: "#E2715E", teal: "#3DAA8C" };
  const KIND_COLOR = { collector: "#0B6F87", orchestrator: "#0B6F87", futurist: "#1C5A4A", workflow: "#27506F", script: "#553897", fetcher: "#7A5C00", agent: "#0B6F87", reference: "#6E685B", datastore: "#0B6F87", dashboard: "#0B6F87", external: "#5F594C", scheduler: "#553897" };
  const GLYPH = {
    bank: '<path d="M3 21h18M5 21V10l7-4.5 7 4.5v11M9 21v-6h6v6"/>', tender: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    reg: '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>', stats: '<path d="M5 20V12M10 20V6M15 20v-9M20 20V9"/><path d="M3 20h18"/>',
    jobs: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>', vendors: '<path d="M4 9V5h16v4M4 9l1.5 11h13L20 9M4 9h16M10 14h4"/>',
    future: '<path d="M12 3l2.2 5.6L20 11l-5.8 2.4L12 19l-2.2-5.6L4 11l5.8-2.4z"/>', hub: '<circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="4" r="1.6"/><circle cx="12" cy="20" r="1.6"/><circle cx="4.5" cy="8" r="1.6"/><circle cx="19.5" cy="8" r="1.6"/><path d="M12 7.2v1.6M12 15.2v3M9.3 10.5 6 8.8M14.7 10.5 18 8.8"/>',
    net: '<circle cx="6" cy="6" r="2.3"/><circle cx="6" cy="18" r="2.3"/><circle cx="18" cy="12" r="2.3"/><path d="M8 7l8 4M8 17l8-4"/>', book: '<path d="M5 4h13v16H7a2 2 0 0 1-2-2z"/><path d="M9 4v16"/>',
    gear: '<circle cx="12" cy="12" r="3.4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>',
    shield: '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>', screen: '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 20h8M12 17v3"/>',
    doc: '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>', rules: '<path d="M5 3h11l3 3v15H5z"/><path d="M8 8h7M8 12h7M8 16h4"/>', file: '<path d="M7 3h8l4 4v14H7z"/><path d="M14 3v5h5"/>',
    bot: '<rect x="4" y="8" width="16" height="11" rx="4"/><path d="M12 4.5v3.5"/><circle cx="12" cy="3.4" r="1.5" fill="currentColor"/><circle cx="9" cy="13.5" r="1.5" fill="currentColor"/><circle cx="15" cy="13.5" r="1.5" fill="currentColor"/>',
    play: '<path d="M7 5l11 7-11 7z"/>',
  };
  const chip = (g, col) => `<span class="ichip" style="background:${col[0]};color:${col[1]}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">${GLYPH[g] || GLYPH.bot}</svg></span>`;

  const COLLECTORS = [
    { lab: "A1", id: "agent-1", name: "Bank Disclosures", cad: "Monthly", role: "Reads bank reports & decks; extracts spend / strategy signals", fan: "× 42 banks", c: "cyan", icon: "bank" },
    { lab: "A2", id: "agent-2", name: "Tenders & Procurement", cad: "Weekly", role: "Sweeps EU + national tender portals for live lots & winners", fan: "× 13 portals", c: "blue", icon: "tender" },
    { lab: "A3", id: "agent-3", name: "Regulation & Deadlines", cad: "1st & 15th", role: "Tracks the EU / CEE regulatory calendar + a horizon scan", fan: "× 11 workstreams", c: "lilac", icon: "reg" },
    { lab: "A4", id: "agent-4", name: "Market Statistics", cad: "Monthly", role: "Non-EU ATM / POS / cash series from central banks", fan: "× 7 markets", c: "green", icon: "stats" },
    { lab: "A5", id: "agent-5", name: "Early Intent · Jobs", cad: "Weekly", role: "Bank hiring + leadership moves read as buying signals", fan: "× 9 markets", c: "yellow", icon: "jobs" },
    { lab: "A6", id: "agent-6", name: "Vendors & Competitors", cad: "Weekly", role: "Competitor & partner moves; long-tail discovery", fan: "× 17 competitors", c: "peach", icon: "vendors" },
  ];
  const ESCR = [
    { id: "fetch-ecb", nm: "7 Tier-0 fetchers", d: "ECB · TED · Prozorro · jobs · vendor news · financials" },
    { id: "eng-ingest", nm: "ingest.py", d: "parse master table + workbook → score" }, { id: "eng-forecast", nm: "forecast.py", d: "project the trend lines" },
    { id: "eng-verify", nm: "verify.py", d: "re-fetch & snapshot every source" }, { id: "eng-build", nm: "build_dashboard.py", d: "assemble payload · merge verdicts" }, { id: "eng-publish", nm: "publish.py", d: "push to the live site" },
  ];

  const W = 1300;
  let level = 1, scale = 1, panX = 0, panY = 0;
  let stage, world, svg;
  const cardByKey = {}, posByKey = {};
  const nodes = () => (window.ARCH && window.ARCH.nodes) || [];
  const edges = () => (window.ARCH && window.ARCH.edges) || [];
  const nodeById = id => nodes().find(n => n.id === id);

  /* ---------- markdown + drawer (shared) ---------- */
  function mdToHtml(md) {
    if (!md) return ""; const lines = String(md).split(/\r?\n/); let html = "", inList = false;
    const inline = t => esc(t).replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>').replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/`([^`]+)`/g, "<code>$1</code>");
    for (let raw of lines) { const t = raw.trim();
      if (/^[-*]\s+/.test(t)) { if (!inList) { html += "<ul>"; inList = true; } html += "<li>" + inline(t.replace(/^[-*]\s+/, "")) + "</li>"; continue; }
      if (inList) { html += "</ul>"; inList = false; } if (!t) continue;
      const h = t.match(/^(#{2,4})\s+(.*)$/); html += h ? "<h4>" + inline(h[2]) + "</h4>" : "<p>" + inline(t) + "</p>"; }
    if (inList) html += "</ul>"; return html;
  }
  const promptHtml = p => esc(p).replace(/(\$\{[^}]+\}|\b[A-Z][A-Z_]{3,}\b)/g, '<span class="ph">$1</span>');
  function kbStructureHtml() {
    return '<div class="md" style="margin-bottom:11px"><p>Every midnight the <b>data-dump processor</b> turns any new file dropped in <code>Data dump/</code> into pre-digested, per-agent knowledge-base entries — reading the <b>charts &amp; figures</b>, not just the text. Each file is de-duplicated by <b>sha256</b>, so nothing is digested twice.</p></div>' +
      '<div class="kbflow">' +
      '<span class="kbstep file"><b>📁 Data dump</b><small>files dropped in</small></span><span class="kbarrow">→</span>' +
      '<span class="kbstep script"><b>extract.py</b><small>document → text</small></span><span class="kbarrow">→</span>' +
      '<span class="kbstep script"><b>render_pages.py</b><small>SEE the charts</small></span><span class="kbarrow">→</span>' +
      '<span class="kbstep agent"><b>digest + route</b><small>LLM · per agent</small></span><span class="kbarrow">→</span>' +
      '<span class="kbstep script"><b>commit_digests.py</b><small>+ update manifest</small></span>' +
      '</div>' +
      '<div class="kbtree"><div class="kbroot">📁 knowledge-base/</div>' +
      '<div class="kbrow"><span class="kbf">_reference/</span><span class="kbd">internal Printec decks &amp; capabilities — read by <b>every agent + the Orchestrator</b></span></div>' +
      '<div class="kbrow"><span class="kbf">by-agent/</span><span class="kbd">per-agent digests — <b>agent-1 … agent-8</b> (7 folders); each agent reads only its own</span></div>' +
      '<div class="kbrow"><span class="kbf">_deepread/</span><span class="kbd">all-pages vision deep-read — per-10-page checkpoints → <code>&lt;slug&gt;-deep.md</code></span></div>' +
      '<div class="kbrow"><span class="kbf">processed/</span><span class="kbd">the original source files, moved here after ingest</span></div>' +
      '<div class="kbrow"><span class="kbf">_staging/</span><span class="kbd">temporary working text (deleted at the end of each run)</span></div>' +
      '<div class="kbrow"><span class="kbf">_manifest.json</span><span class="kbd">the index — sha256 dedup · routing · tags</span></div>' +
      '</div>' +
      '<div class="md" style="margin-top:10px"><p>A document can serve <b>several</b> targets (e.g. a market-forecast report → <code>agent-4-statistics</code> + <code>agent-8-futurist</code>); internal Printec material always routes to <code>_reference/</code>.</p></div>';
  }
  let DR, SC;
  function ensureDrawer() {
    if (DR) return;
    SC = document.createElement("div"); SC.className = "arch-scrim";
    DR = document.createElement("aside"); DR.className = "arch-drawer"; DR.setAttribute("aria-hidden", "true");
    DR.innerHTML = '<div class="a-dhead"><button class="a-dclose" aria-label="Close">✕</button><div class="a-dkind"></div><h2 class="a-dtitle"></h2><p class="a-drole"></p><div class="a-dchips"></div></div><div class="a-dbody"></div>';
    document.body.appendChild(SC); document.body.appendChild(DR);
    SC.addEventListener("click", closeDrawer); DR.querySelector(".a-dclose").addEventListener("click", closeDrawer);
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeDrawer(); });
  }
  const q = s => DR.querySelector(s);
  function showDrawer() { ensureDrawer(); DR.classList.add("show"); SC.classList.add("show"); DR.setAttribute("aria-hidden", "false"); q(".a-dbody").scrollTop = 0; }
  function closeDrawer() { if (!DR) return; DR.classList.remove("show"); SC.classList.remove("show"); DR.setAttribute("aria-hidden", "true"); deselect(); }
  const sec = (t, b) => '<div class="dsec"><h3>' + esc(t) + "</h3>" + b + "</div>";
  function openInline(title, kind, role, detailMd) {
    ensureDrawer(); q(".a-dkind").textContent = kind || ""; q(".a-dkind").style.color = "var(--cyan-ink)";
    q(".a-dtitle").textContent = title || ""; q(".a-drole").textContent = role || ""; q(".a-dchips").innerHTML = "";
    q(".a-dbody").innerHTML = sec("What it is", '<div class="md">' + mdToHtml(detailMd || "") + "</div>"); showDrawer();
  }
  function openAbout() { openInline("How the machine works", "The system", "A weekly walkthrough, start to finish.", (window.ARCH && window.ARCH.narrative_md) || "The walkthrough is being generated."); }
  function openDrawer(id) {
    const n = nodeById(id); if (!n) return; ensureDrawer();
    q(".a-dkind").textContent = (n.kind || "") + (n.group ? " · " + n.group : ""); q(".a-dkind").style.color = KIND_COLOR[n.kind] || "var(--ink-2)";
    q(".a-dtitle").textContent = n.label || id; q(".a-drole").textContent = n.role || n.summary || "";
    const chips = []; if (n.cadence) chips.push('<span class="chip cad">' + esc(n.cadence) + "</span>");
    if (n.fanout && n.fanout.spawns) chips.push('<span class="chip">fans out: ' + esc(n.fanout.count || "sub-agents") + "</span>");
    q(".a-dchips").innerHTML = chips.join("");
    let html = "";
    if (n.detail_md) html += sec("How it works", '<div class="md">' + mdToHtml(n.detail_md) + "</div>");
    if (n.fanout && n.fanout.spawns) { const f = n.fanout; let fb = "";
      [["count", "How many"], ["per", "One per"], ["rounds", "Rounds"], ["verify", "Verification"]].forEach(([k, lbl]) => { if (f[k]) fb += '<div class="kv"><span class="k">' + lbl + '</span><span>' + esc(f[k]) + "</span></div>"; });
      if (f.how) fb += '<div class="md" style="margin-top:8px">' + mdToHtml(f.how) + "</div>"; if (fb) html += sec("Sub-agent fan-out", fb); }
    if (n.prompt_verbatim && n.prompt_verbatim.trim()) html += sec("Prompt / instructions (verbatim)", '<div class="prompt-wrap"><button class="copybtn" data-copy="' + id + '">Copy</button><div class="prompt-box">' + promptHtml(n.prompt_verbatim) + "</div></div>");
    if (Array.isArray(n.key_rules) && n.key_rules.length) html += sec("Hard rules", '<div class="md"><ul>' + n.key_rules.map(r => "<li>" + mdToHtml(r).replace(/^<p>|<\/p>$/g, "") + "</li>").join("") + "</ul></div>");
    if (Array.isArray(n.scripts_used) && n.scripts_used.length) html += sec("Scripts & tools used", n.scripts_used.map(x => '<div class="kv"><span class="k">' + esc(x.name) + '</span><span>' + esc(x.when) + "</span></div>").join(""));
    const io = []; if (Array.isArray(n.inputs) && n.inputs.length) io.push("<div><b>Reads:</b><br>" + n.inputs.map(x => '<span class="tag">' + esc(x) + "</span>").join("") + "</div>");
    if (Array.isArray(n.outputs) && n.outputs.length) io.push('<div style="margin-top:8px"><b>Writes:</b><br>' + n.outputs.map(x => '<span class="tag">' + esc(x) + "</span>").join("") + "</div>");
    if (io.length) html += sec("Inputs & outputs", io.join(""));
    const outs = edges().filter(e => e.from === id), ins = edges().filter(e => e.to === id);
    if (outs.length || ins.length) { let cn = "";
      outs.forEach(e => { const t = nodeById(e.to); cn += '<div class="io">→ <span class="a" data-go="' + e.to + '">' + esc(t ? t.label : e.to) + '</span> <span style="color:var(--ink-2)">' + esc(e.label || "") + "</span></div>"; });
      ins.forEach(e => { const t = nodeById(e.from); cn += '<div class="io">← <span class="a" data-go="' + e.from + '">' + esc(t ? t.label : e.from) + '</span> <span style="color:var(--ink-2)">' + esc(e.label || "") + "</span></div>"; });
      html += sec("Connections", cn); }
    if (id === "data-dump") html = sec("How the knowledge base is organized", kbStructureHtml()) + html;
    q(".a-dbody").innerHTML = html || '<div class="md"><p>Details are being generated.</p></div>';
    q(".a-dbody").querySelectorAll("[data-copy]").forEach(b => b.onclick = () => { const t = (nodeById(b.dataset.copy) || {}).prompt_verbatim || ""; navigator.clipboard && navigator.clipboard.writeText(t); b.textContent = "Copied ✓"; setTimeout(() => b.textContent = "Copy", 1400); });
    q(".a-dbody").querySelectorAll("[data-go]").forEach(a => a.onclick = () => { if (nodeById(a.dataset.go)) openDrawer(a.dataset.go); });
    showDrawer();
  }
  function openNodeOr(id, fallback) { if (id && nodeById(id)) openDrawer(id); else fallback(); }

  /* ---------- shared canvas helpers ---------- */
  function deselect() { [...world.querySelectorAll(".obx,.fnode")].forEach(c => c.classList.remove("sel")); }
  function selectKey(k) { deselect(); const c = cardByKey[k]; if (c) c.classList.add("sel"); }
  function clearWorld() { [...world.querySelectorAll(".obx,.fnode,.tbadge,.elabel,.stage-band")].forEach(e => e.remove()); svg.innerHTML = '<defs><marker id="arw" markerWidth="9" markerHeight="9" refX="6.5" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#b9ad92"/></marker></defs>'; Object.keys(cardByKey).forEach(k => delete cardByKey[k]); Object.keys(posByKey).forEach(k => delete posByKey[k]); }
  function seg(x1, y1, x2, y2, flow) { const p = document.createElementNS(NS, "path"); p.setAttribute("d", `M${x1},${y1} L${x2},${y2}`); p.setAttribute("class", "oconn" + (flow ? " flow" : "")); svg.appendChild(p); }
  function bus(parents, fromY, children, toY) { const m = Math.round((fromY + toY) / 2); parents.forEach(px => seg(px, fromY, px, m)); const xs = parents.concat(children); seg(Math.min(...xs), m, Math.max(...xs), m); children.forEach(cx => seg(cx, m, cx, toY)); }
  function elbow(x1, y1, x2, y2) { const mx = Math.round((x1 + x2) / 2); seg(x1, y1, mx, y1); seg(mx, y1, mx, y2); seg(mx, y2, x2, y2); }
  function tbadge(num, cy, label) { const d = document.createElement("div"); d.className = "tbadge"; d.style.cssText = `left:6px;top:${cy - 16}px`; d.innerHTML = `<span class="tn">${num}</span><span class="tl">${esc(label || "")}</span>`; world.appendChild(d); }

  /* ---------- OVERVIEW: organogram ---------- */
  function obox(o) {
    const el = document.createElement("div"); el.className = "obx " + (o.cls || ""); el.style.cssText = `left:${o.x}px;top:${o.y}px;width:${o.w}px;height:${o.h}px`;
    el.dataset.key = o.key; el.innerHTML = o.html; el._box = o;
    el.addEventListener("click", e => { e.stopPropagation(); selectKey(o.key); o.node && nodeById(o.node) ? openDrawer(o.node) : openInline(o.title || "Detail", o.kind || "", o.role || "", o.detail || ""); });
    world.appendChild(el); cardByKey[o.key] = el; posByKey[o.key] = { x: o.x, y: o.y, w: o.w, h: o.h };
  }
  function collectorCard(a, x, y, w, h) {
    const c = C[a.c], nm = a.name;
    obox({ key: "ag-" + a.id, node: a.id, x, y, w, h, cls: "ccard",
      html: `<span class="stack" style="background:${c[0]};border-color:${SOLID[a.c]}"></span><span class="stack s2" style="background:${c[0]};border-color:${SOLID[a.c]}"></span>` +
        `<div class="cface" style="background:${c[0]};color:${c[1]}"><span class="blob" style="background:${SOLID[a.c]}"></span>` +
        `<div class="chead">${chip("bot", ["#fff", c[1]])}<span class="ccode">${a.lab}</span><span class="ccad">${esc(a.cad)}</span></div>` +
        `<div class="ctitle">${esc(nm)}</div><div class="crole">${esc(a.role)}</div><div class="cfan">⇲ fans out <b>${esc(a.fan)}</b></div></div>` });
  }
  function buildOrg() {
    const cx = W / 2;
    const Y = { mission: 18, coll: 150, harn: 350, orch: 482, branch: 648, out: 900 };
    const CH = 158, ORH = 96, AGENT = ["#D3EFF8", "#0B6F87"];
    const mw = 600, mh = 44; obox({ key: "mission", x: cx - mw / 2, y: Y.mission, w: mw, h: mh, cls: "mission", title: "Mission", kind: "The goal", role: "Why the whole system exists.", detail: "The entire pipeline exists to **infer what banks across Printec's 17-country footprint will need to buy in the next 6–12 months** — early enough to act — and to back every call with primary-source evidence.", html: `<span class="mdot"></span><b>MISSION</b><span class="mtx">infer what banks will need in the next 6–12 months</span>` });
    const n = COLLECTORS.length, gap = 18, side = 92, aw = Math.round((W - side * 2 - (n - 1) * gap) / n), ax0 = (W - (n * aw + (n - 1) * gap)) / 2, aC = [];
    COLLECTORS.forEach((a, i) => { const x = ax0 + i * (aw + gap); collectorCard(a, x, Y.coll, aw, CH); aC.push(Math.round(x + aw / 2)); });
    tbadge("①", Y.coll + CH / 2, "Collect");
    const hw = 660; obox({ key: "harness", node: "research-harness", x: cx - hw / 2, y: Y.harn, w: hw, h: 84, cls: "harness", html: `${chip("bot", AGENT)}<div class="htxt"><div class="htop"><b>Shared research harness</b><span class="hpill">1 sub-agent / unit</span><span class="hpill">adversarial verify</span><span class="hpill">gap-fill ×2</span><span class="hpill">deterministic render</span></div><span class="hsub">the reliable fan-out every collector calls — no verified row can be silently dropped</span></div>` });
    tbadge("②", Y.harn + 42, "Fan-out");
    const ow = 560, oxb = cx - ow / 2; obox({ key: "orch", node: "agent-7", x: oxb, y: Y.orch, w: ow, h: ORH, cls: "orch", html: `${chip("bot", AGENT)}<div class="otxt"><div class="otop"><b>Orchestrator</b><span class="ocode">A7</span><span class="ocad">Weekly</span></div><span class="osub">triangulates findings · promotes to High only on 2+ agent agreement · writes outlooks · runs the engine · spawns the validator</span></div>` });
    tbadge("③", Y.orch + ORH / 2, "Triangulate");
    const kbw = 230, kbx = side, fuw = 250, fux = W - side - fuw;
    obox({ key: "kb", node: "data-dump", x: kbx, y: Y.orch - 10, w: kbw, h: 116, cls: "feeder kbcard", html: `<span class="blob" style="background:${SOLID.yellow}"></span>${chip("book", ["#fff", "#7A5C00"])}<div class="ftx"><div class="ftop"><b>Knowledge base</b><span class="fcad" style="color:#7A5C00">store</span></div><span class="fsub">decks, reports &amp; PDFs → per-agent digests</span></div>` });
    obox({ key: "fut", node: "agent-8", x: fux, y: Y.orch - 10, w: fuw, h: 116, cls: "feeder futcard", html: `<span class="blob" style="background:${SOLID.teal}"></span>${chip("bot", ["#fff", "#1C5A4A"])}<div class="ftx"><div class="ftop"><b>Futurist</b><span class="ocode" style="color:#1C5A4A;background:#fff">A8</span><span class="fcad" style="color:#1C5A4A">Monthly</span></div><span class="fsub">the 2–5-yr arc; feeds the Orchestrator + Future tab</span></div>` });
    const bh = 172, elx = side, elw = Math.round(W / 2 - side - 16), vrx = cx + 16, vrw = Math.round(W / 2 - side - 16), eCx = elx + elw / 2, vCx = vrx + vrw / 2;
    obox({ key: "compute", node: "eng-runweekly", x: elx, y: Y.branch, w: elw, h: bh, cls: "obox compute", html: `<div class="ohd">${chip("gear", ["#E0D4F4", "#553897"])}<div><div class="otitle">COMPUTE — deterministic engine</div><div class="osubt">Python · run_weekly.py · scripts own the numbers · no LLM</div></div><span class="bnum" style="color:#553897">④</span></div><div class="bsum" style="margin-bottom:10px">Six scripts run in sequence each week — sum-verified, no model in the loop:</div><div class="spills"><span class="spill">fetch</span><span class="spill">ingest</span><span class="spill">forecast</span><span class="spill">verify</span><span class="spill">build</span><span class="spill">publish</span></div>` });
    obox({ key: "audit", node: "wf-validate", x: vrx, y: Y.branch, w: vrw, h: bh, cls: "obox audit", html: `<div class="ohd">${chip("bot", AGENT)}<div><div class="otitle">AUDIT — validator workflow</div><div class="osubt">spawned by the Orchestrator · independent fact-check</div></div><span class="bnum" style="color:#0B6F87">⑤</span></div><div class="bsum">Re-reads every outlook <b>and</b> every 2–5-yr future against its cited sources, then writes <b>✓ / ⚠</b> verdicts.<br>Claim-checkers <b>× N</b> &nbsp;+&nbsp; a Writer.</div>` });
    const ow2 = 300, ogap = 30, o1x = cx - ow2 - ogap / 2, o2x = cx + ogap / 2, oy = Y.out, ohh = 60;
    obox({ key: "live", node: "dashboard", x: o1x, y: oy, w: ow2, h: ohh, cls: "output", html: `${chip("screen", ["#D2E2B4", "#3D5A1C"])}<div><b>Live dashboard</b><span>8 interactive views</span></div>` });
    obox({ key: "brief", x: o2x, y: oy, w: ow2, h: ohh, cls: "output", title: "Board brief", kind: "Output", role: "The weekly written summary.", detail: "The **board brief** the Orchestrator writes each week: BLUF + the Top-3 opportunities, movements vs last week, watch items and gaps.", html: `${chip("doc", ["#EFE7D6", "#6E685B"])}<div><b>Board brief</b><span>BLUF + Top-3 opportunities</span></div>` });
    tbadge("⑥", oy + ohh / 2, "Deliver");
    bus([cx], Y.mission + mh, aC, Y.coll); bus(aC, Y.coll + CH, [cx], Y.harn); seg(cx, Y.harn + 84, cx, Y.orch);
    elbow(kbx + kbw, Y.orch + ORH / 2, oxb, Y.orch + ORH / 2); elbow(fux, Y.orch + ORH / 2, oxb + ow, Y.orch + ORH / 2);
    bus([cx], Y.orch + ORH, [eCx, vCx], Y.branch); bus([eCx, vCx], Y.branch + bh, [o1x + ow2 / 2, o2x + ow2 / 2], oy);
  }

  /* ---------- DETAILED: decision flow-chart ---------- */
  const FCOL = { agent: C.cyan, script: C.lilac, file: C.sand, output: C.green, proc: C.sand, start: C.sand, dec: C.yellow };
  const FICON = { agent: "bot", script: "gear", file: "doc", output: "screen", proc: "rules", start: "play" };
  function fnode(o) {
    const el = document.createElement("div"); el.className = "fnode fn-" + o.t + (o.side ? " fn-side" : ""); el.style.cssText = `left:${o.x}px;top:${o.y}px;width:${o.w}px;height:${o.h}px`;
    el.dataset.key = o.id;
    const ic = (o.t === "dec" || o.t === "start") ? "" : chip(o.icon || FICON[o.t] || "bot", FCOL[o.t] || C.cyan);
    el.innerHTML = (o.badge ? `<span class="fbadge">${esc(o.badge)}</span>` : "") + ic + `<div class="ftext"><b>${esc(o.b)}</b>${o.s ? `<span>${esc(o.s)}</span>` : ""}</div>`;
    el.addEventListener("click", e => { e.stopPropagation(); selectKey(o.id); openNodeOr(o.node, () => openInline(o.b, o.t === "dec" ? "Decision" : (o.t === "file" ? "Data / file" : "Step"), o.s || "", o.det || "")); });
    world.appendChild(el); cardByKey[o.id] = el; posByKey[o.id] = { x: o.x, y: o.y, w: o.w, h: o.h };
  }
  function rc(k) { const p = posByKey[k]; return { x: p.x, y: p.y, w: p.w, h: p.h, cx: p.x + p.w / 2, cy: p.y + p.h / 2, r: p.x + p.w, b: p.y + p.h }; }
  function flabel(x, y, txt) { if (!txt) return; const d = document.createElement("div"); d.className = "elabel"; d.style.cssText = `left:${x}px;top:${y}px`; d.textContent = txt; world.appendChild(d); }
  function fp(d) { const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); p.setAttribute("class", "oconn flow"); p.setAttribute("marker-end", "url(#arw)"); svg.appendChild(p); }
  function connect(aK, bK, type, label) {
    const a = rc(aK), b = rc(bK);
    if (type === "down") { const x1 = a.cx, y1 = a.b, x2 = b.cx, y2 = b.y; if (Math.abs(x1 - x2) < 4) fp(`M${x1},${y1} L${x2},${y2}`); else { const my = Math.round((y1 + y2) / 2); fp(`M${x1},${y1} L${x1},${my} L${x2},${my} L${x2},${y2}`); } flabel((x1 + x2) / 2 - 7, (y1 + y2) / 2 - 8, label); }
    else if (type === "toleft") { const x1 = a.x, y1 = a.cy, x2 = b.r, y2 = b.cy, mx = Math.round((x1 + x2) / 2); fp(`M${x1},${y1} L${mx},${y1} L${mx},${y2} L${x2},${y2}`); flabel(mx - 7, Math.min(y1, y2) - 14, label); }
    else if (type === "toright") { const x1 = a.r, y1 = a.cy, x2 = b.x, y2 = b.cy, mx = Math.round((x1 + x2) / 2); fp(`M${x1},${y1} L${mx},${y1} L${mx},${y2} L${x2},${y2}`); flabel(mx - 7, Math.min(y1, y2) - 14, label); }
    else if (type === "loop") { const x1 = a.cx, y1 = a.y, x2 = b.x, y2 = b.cy; fp(`M${x1},${y1} L${x1},${y2} L${x2},${y2}`); flabel(x1 - 16, (y1 + y2) / 2, label); }
  }
  function buildFlow() {
    const SX = 700, NW = 270, L = SX - NW / 2, DEC = 156, DL = SX - DEC / 2;
    const N = [
      { id: "f-sched", t: "start", x: L + 15, y: 30, w: 240, h: 40, b: "Weekly schedule fires", det: "Nine **local** Claude Code scheduled tasks run on their own cadence (collectors weekly/monthly, the Orchestrator weekly after them, the Futurist monthly, the knowledge-base daily). The app must be open." },
      { id: "f-collect", t: "agent", x: L, y: 110, w: NW, h: 60, b: "Collector agent  (×6)", s: "reads playbook · brief · previous findings · its work-list", det: "Each of the 6 collectors first reads the shared **research playbook**, its detailed **brief**, the **previous findings** (to report only what's new/changed) and its slice of **agent-units.json** (its fan-out work-list)." },
      { id: "f-harness", t: "script", icon: "net", x: L, y: 205, w: NW, h: 54, b: "calls research-harness", s: "the shared fan-out workflow", node: "research-harness" },
      { id: "f-research", t: "agent", x: L, y: 305, w: NW, h: 60, b: "Research sub-agent  (× N units)", s: "1 per unit · primary-source first · EN + local language", node: "research-harness" },
      { id: "f-verify", t: "agent", x: L, y: 405, w: NW, h: 60, b: "Adversarial verify", s: "re-checks every signal vs a primary source", node: "research-harness" },
      { id: "f-dec1", t: "dec", x: DL, y: 510, w: DEC, h: 120, b: "signals found?", det: "The completeness gate. A unit that returns nothing is retried — it can never be silently empty." },
      { id: "f-gap", t: "agent", side: 1, x: 250, y: 528, w: 230, h: 60, b: "Gap-fill retry", s: "≤ 2 rounds · try harder (local lang, regulator, PDF)", node: "research-harness" },
      { id: "f-render", t: "script", icon: "gear", x: L, y: 678, w: NW, h: 54, b: "render table in JS", s: "deterministic — the LLM never renders it", node: "research-harness" },
      { id: "f-write", t: "file", x: L, y: 766, w: NW, h: 50, b: "findings / NN / <date>.md", s: "the agent's dated findings file", det: "Each collector writes its verified signal table + short narrative to its dated findings file." },
      { id: "f-orch", t: "agent", x: L, y: 880, w: NW, h: 64, b: "Orchestrator reads all findings", s: "weekly · after the collectors · + the master signal table", node: "agent-7" },
      { id: "f-kb", t: "file", icon: "book", side: 1, x: 1010, y: 872, w: 250, h: 64, b: "Knowledge base · daily", s: "data store, filled nightly by the data-dump agent", node: "data-dump" },
      { id: "f-fut", t: "agent", icon: "future", side: 1, x: 140, y: 872, w: 250, h: 64, b: "Futurist · A8 · monthly", s: "future-trends + structural-patterns workflows", node: "agent-8" },
      { id: "f-dec2", t: "dec", x: DL, y: 985, w: DEC, h: 116, b: "a collector missing / empty?", det: "The completeness gate at the orchestration level — a missing agent or an empty unit is recorded as a gap, never hidden." },
      { id: "f-gapnote", t: "file", side: 1, x: 1010, y: 1010, w: 230, h: 50, b: "record coverage gap", s: "surfaced in the brief & dashboard" },
      { id: "f-tri", t: "agent", x: L, y: 1130, w: NW, h: 56, b: "triangulate signals", s: "group findings about the same bank / theme", node: "agent-7" },
      { id: "f-dec3", t: "dec", x: DL, y: 1235, w: DEC, h: 116, b: "2+ agents agree?", det: "Confidence is earned by agreement: only a signal confirmed by 2+ independent agents may be promoted to High." },
      { id: "f-high", t: "proc", side: 1, x: 1010, y: 1265, w: 220, h: 46, b: "mark High confidence" },
      { id: "f-med", t: "proc", side: 1, x: 180, y: 1265, w: 220, h: 46, b: "cap at Medium" },
      { id: "f-outlooks", t: "file", x: L, y: 1395, w: NW, h: 54, b: "outlooks → forecast_narrative.json", s: "direction · range · drivers · cite_ungrounded", node: "agent-7" },
      { id: "f-spawn", t: "script", icon: "net", x: L, y: 1490, w: NW, h: 50, b: "spawn validator workflow", node: "wf-validate" },
      { id: "f-val", t: "agent", x: L, y: 1580, w: NW, h: 62, b: "Claim-checker  (× N) + Writer", s: "re-reads each cited doc · independent fact-check", node: "wf-validate" },
      { id: "f-valout", t: "file", x: L, y: 1685, w: NW, h: 50, b: "outlook / futures _validation.json", s: "✓ / ⚠ verdicts, merged at build", node: "wf-validate" },
      { id: "f-run", t: "script", icon: "gear", x: L, y: 1790, w: NW, h: 54, b: "run  python run_weekly.py", s: "the deterministic engine — chains the steps below", node: "eng-runweekly" },
      { id: "f-fetch", t: "script", x: L, y: 1884, w: NW, h: 50, b: "7 Tier-0 fetchers", s: "ECB · TED · Prozorro · jobs · vendor news", node: "fetch-ecb" },
      { id: "f-ingest", t: "script", x: L, y: 1962, w: NW, h: 46, b: "ingest.py", s: "score & size every signal", node: "eng-ingest" },
      { id: "f-forecast", t: "script", x: L, y: 2032, w: NW, h: 46, b: "forecast.py", s: "project the trend lines", node: "eng-forecast" },
      { id: "f-vereng", t: "script", x: L, y: 2102, w: NW, h: 46, b: "verify.py", s: "re-fetch & snapshot every source", node: "eng-verify" },
      { id: "f-build", t: "script", x: L, y: 2172, w: NW, h: 46, b: "build_dashboard.py", s: "assemble payload · merge ✓/⚠ verdicts", node: "eng-build" },
      { id: "f-dec4", t: "dec", x: DL, y: 2252, w: DEC, h: 116, b: "publish env set?", det: "publish.py runs only when PRINTEC_DASHBOARD_URL + PRINTEC_UPLOAD_SECRET are set; otherwise the build still succeeds locally and the push is skipped." },
      { id: "f-pub", t: "script", x: L, y: 2410, w: NW, h: 52, b: "publish.py → Vercel Blob", s: "no redeploy — /api/data flips to live", node: "eng-publish" },
      { id: "f-skip", t: "proc", side: 1, x: 1010, y: 2282, w: 220, h: 46, b: "skip · local only" },
      { id: "f-dash", t: "output", x: 470, y: 2520, w: 250, h: 56, b: "Live dashboard", s: "8 interactive views", node: "dashboard" },
      { id: "f-brief", t: "file", x: 760, y: 2520, w: 250, h: 56, b: "board brief", s: "BLUF + Top-3 (written by the Orchestrator)" },
    ];
    N.forEach(fnode);
    // stage bands
    [["COLLECT  ·  per agent, weekly / monthly", 110], ["FAN-OUT  ·  the shared harness, per unit", 305], ["TRIANGULATE  ·  Orchestrator, weekly", 880], ["AUDIT  ·  independent validator", 1580], ["COMPUTE  ·  deterministic Python engine", 1790], ["PUBLISH", 2520]].forEach(([t, y]) => { const d = document.createElement("div"); d.className = "stage-band"; d.style.cssText = `left:16px;top:${y - 22}px`; d.textContent = t; world.appendChild(d); });
    connect("f-sched", "f-collect", "down"); connect("f-collect", "f-harness", "down"); connect("f-harness", "f-research", "down"); connect("f-research", "f-verify", "down");
    connect("f-verify", "f-dec1", "down"); connect("f-dec1", "f-gap", "toleft", "no"); connect("f-gap", "f-verify", "loop", "retry"); connect("f-dec1", "f-render", "down", "yes");
    connect("f-render", "f-write", "down"); connect("f-write", "f-orch", "down");
    connect("f-kb", "f-orch", "toleft", "context"); connect("f-fut", "f-orch", "toright", "futures");
    connect("f-orch", "f-dec2", "down"); connect("f-dec2", "f-gapnote", "toright", "yes"); connect("f-dec2", "f-tri", "down", "no");
    connect("f-tri", "f-dec3", "down"); connect("f-dec3", "f-high", "toright", "yes"); connect("f-dec3", "f-med", "toleft", "no"); connect("f-high", "f-outlooks", "down"); connect("f-med", "f-outlooks", "down");
    connect("f-outlooks", "f-spawn", "down"); connect("f-spawn", "f-val", "down"); connect("f-val", "f-valout", "down"); connect("f-valout", "f-run", "down");
    connect("f-run", "f-fetch", "down"); connect("f-fetch", "f-ingest", "down"); connect("f-ingest", "f-forecast", "down"); connect("f-forecast", "f-vereng", "down"); connect("f-vereng", "f-build", "down");
    connect("f-build", "f-dec4", "down"); connect("f-dec4", "f-pub", "down", "yes"); connect("f-dec4", "f-skip", "toright", "no");
    connect("f-pub", "f-dash", "down"); connect("f-pub", "f-brief", "down");
  }

  /* ---------- render + pan/zoom ---------- */
  function render() { clearWorld(); deselect(); if (level === 1) buildOrg(); else buildFlow(); fit(); }
  function bounds() { let a = 1e9, b = 1e9, c = -1e9, d = -1e9; Object.values(posByKey).forEach(p => { a = Math.min(a, p.x); b = Math.min(b, p.y); c = Math.max(c, p.x + p.w); d = Math.max(d, p.y + p.h); }); if (a === 1e9) return { x: 0, y: 0, w: W, h: 700 }; return { x: a, y: b, w: c - a, h: d - b }; }
  function apply() { world.style.transform = `translate(${panX}px,${panY}px) scale(${scale})`; }
  function fit() { const bd = bounds(), pad = 60, cw = bd.w + pad * 2, ch = bd.h + pad * 2, sw = stage.clientWidth, sh = stage.clientHeight; scale = Math.min(sw / cw, sh / ch, 1.1); scale = Math.max(scale, 0.12); panX = (sw - cw * scale) / 2 - (bd.x - pad) * scale; panY = (sh - ch * scale) / 2 - (bd.y - pad) * scale; apply(); }
  function zoomAt(px, py, f) { const ns = Math.min(2.4, Math.max(0.1, scale * f)), wx = (px - panX) / scale, wy = (py - panY) / scale; scale = ns; panX = px - wx * scale; panY = py - wy * scale; apply(); }

  function init() {
    stage = document.getElementById("stage"); world = document.getElementById("world"); svg = document.getElementById("edges");
    const ld = document.getElementById("loader"); if (ld) ld.remove();
    document.getElementById("legend").hidden = false; document.getElementById("hint").hidden = false;
    document.getElementById("legendItems").innerHTML =
      '<div class="lg"><span class="lgi" style="background:#D3EFF8;color:#0B6F87">' + `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">${GLYPH.bot}</svg>` + '</span> AI agent · LLM</div>' +
      '<div class="lg"><span class="lgi" style="background:#E0D4F4;color:#553897">' + `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">${GLYPH.gear}</svg>` + '</span> Python script · deterministic</div>' +
      '<div class="lg"><span class="lgi" style="background:#FBF6EC;color:#6E685B">' + `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">${GLYPH.doc}</svg>` + '</span> File / data</div>' +
      '<div class="lg"><span class="lgd"></span> Decision <span style="opacity:.6;margin-left:4px">(Detailed)</span></div>';
    stage.addEventListener("wheel", e => { e.preventDefault(); const r = stage.getBoundingClientRect(); zoomAt(e.clientX - r.left, e.clientY - r.top, e.deltaY < 0 ? 1.12 : 0.89); }, { passive: false });
    let drag = false, sx = 0, sy = 0, spx = 0, spy = 0, moved = false;
    stage.addEventListener("mousedown", e => { if (e.target.closest(".obx,.fnode")) return; drag = true; moved = false; sx = e.clientX; sy = e.clientY; spx = panX; spy = panY; stage.classList.add("grabbing"); });
    window.addEventListener("mousemove", e => { if (!drag) return; panX = spx + (e.clientX - sx); panY = spy + (e.clientY - sy); if (Math.abs(e.clientX - sx) + Math.abs(e.clientY - sy) > 4) moved = true; apply(); });
    window.addEventListener("mouseup", () => { drag = false; stage.classList.remove("grabbing"); });
    document.getElementById("zin").onclick = () => zoomAt(stage.clientWidth / 2, stage.clientHeight / 2, 1.18);
    document.getElementById("zout").onclick = () => zoomAt(stage.clientWidth / 2, stage.clientHeight / 2, 0.85);
    document.getElementById("fit").onclick = fit;
    document.getElementById("walkBtn").onclick = openAbout;
    document.getElementById("lvl").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; level = +b.dataset.lvl; [...b.parentNode.children].forEach(x => x.classList.toggle("active", x === b)); render(); });
    render();
    window.addEventListener("resize", fit);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
