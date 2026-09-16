/* ============================================================================
   Printec Banking Intelligence — renderer
   Consumes the DASH object produced by build_dashboard.py. Same data contract
   as the original dashboard; only the presentation changed.

   Data source resolution (in order):
     1. window.__DASH_DATA__   -> offline single-file build (data inlined)
     2. GET /api/data          -> live web app (Vercel Blob, written by the orchestrator)
     3. ./data.json            -> bundled fallback (last committed week)
   ============================================================================ */
(function(){
"use strict";

const $ = s => document.querySelector(s);
const el = (t,c,h) => { const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e; };
const esc = s => (s==null?"":String(s)).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const safeUrl = u => (u && /^https?:\/\//i.test(u)) ? u : "";   // only allow http(s) hrefs

/* ---- date helpers (manual parse → no timezone surprises) ---- */
const MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
const MON_ABBR=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const WEEK_RE=/^\d{4}-\d{2}-\d{2}$/;
function fmtWeek(wk){ if(!WEEK_RE.test(wk||'')) return wk||'—'; const [y,m,d]=wk.split('-').map(Number); return `${MON_ABBR[m-1]} ${d}, ${y}`; }
function monthKeyOf(wk){ return (wk||'').slice(0,7); }
function monthLabel(mk){ const [y,m]=(mk||'').split('-').map(Number); return (MONTHS[m-1]||'')+' '+(y||''); }
/* diff two snapshots by signal key → added / removed / confidence_changed (mirrors build_dashboard) */
function diffSnapshots(prev, cur){
  const pk=new Map((prev&&prev.signals||[]).map(s=>[s.key,s]));
  const ck=new Map((cur&&cur.signals||[]).map(s=>[s.key,s]));
  const added=[], removed=[], confidence_changed=[];
  ck.forEach((s,k)=>{ if(!pk.has(k)) added.push(s.bank_theme);
    else if(pk.get(k).confidence!==s.confidence) confidence_changed.push({bank_theme:s.bank_theme,from:pk.get(k).confidence,to:s.confidence}); });
  pk.forEach((s,k)=>{ if(!ck.has(k)) removed.push(s.bank_theme); });
  return {added, removed, confidence_changed, baseline: !prev};
}
/* ---- product accent colours (pastel) ---- */
const PCOL = {
  atm_recycling:'#8FB7E6', self_service:'#76C7BE', pos_acquiring:'#BFA7E6', payments_instant:'#F0CF49',
  digital_onboarding:'#A6C47C', fraud_monitoring:'#EE9BB0', compliance_resilience:'#F0B073',
  physical_security:'#A7B0C0', managed_services:'#7AD0D8', core_digital:'#C3A6E8'
};
// section-header tile colour — randomised per section, distinct, and stable within a page load
const SEC_COLORS=['sh-cyan','sh-yellow','sh-green','sh-blue','sh-lilac'];
const _secColorCache={};
function secHeadColor(key){
  if(_secColorCache[key]) return _secColorCache[key];
  const used=new Set(Object.values(_secColorCache));
  const pool=SEC_COLORS.filter(c=>!used.has(c)); const from=pool.length?pool:SEC_COLORS;
  return (_secColorCache[key]=from[Math.floor(Math.random()*from.length)]);
}
const ICON = {
  overview:'<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
  country:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.5 4 5.7 4 9s-1.4 6.5-4 9c-2.6-2.5-4-5.7-4-9s1.4-6.5 4-9z"/>',
  product:'<path d="M12 3 3 7.5 12 12l9-4.5L12 3z"/><path d="M3 12l9 4.5L21 12"/><path d="M3 16.5 12 21l9-4.5"/>',
  competition:'<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3z"/>',
  accounts:'<rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9h18M8 2.5v4M16 2.5v4"/><path d="m9 14 2 2 4-4"/>',
  patterns:'<path d="M3 17l5-6 4 3 5-7"/><path d="M3 21h18"/><circle cx="20" cy="6" r="1.4" fill="currentColor" stroke="none"/>',
  outlook:'<path d="M3 17l6-6 4 4 8-8"/><path d="M21 7v5h-5"/>',
  baselines:'<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M3 20h18"/>',
  underlying:'<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h10"/>',
  futures:'<circle cx="12" cy="13.5" r="7.5"/><path d="M12 13.5V9.5"/><path d="M9.5 2.6h5"/><path d="M18.8 7.2l1.4-1.4"/>',
  signals:'<path d="M3 12h3l2.5-7 4 14 3-9 2 2h3.5"/>',
  architecture:'<rect x="9" y="3" width="6" height="5" rx="1.4"/><rect x="3" y="16" width="6" height="5" rx="1.4"/><rect x="15" y="16" width="6" height="5" rx="1.4"/><path d="M12 8v3.5M6 16v-2.5h12v2.5"/>'
};
const TABS = [
  // PERSPECTIVES — the interpretive lenses: what this means and where it's heading
  {id:'outlook',    label:'By signals',        group:'near', icon:ICON.outlook,    title:'Near-term outlook — from the weekly signals',   sub:'Six research agents check public sources every week: bank results and reports, tender websites, regulators\u2019 deadlines, market statistics, job adverts and vendor news. Every finding has a date and a link to a page you can open yourself. A seventh agent, the orchestrator, reads the week\u2019s findings market by market and writes the outlooks below. Each card lists the signals it is based on, so you can trace any call back to its evidence. This is the fastest of the three views, and it changes every week.'},
  {id:'patterns',   label:'By patterns',       group:'near', icon:ICON.patterns,   title:'Near-term outlook — from the structural patterns',  sub:'Patterns are the market forces that last. They change over months, not weeks, so they come from the whole knowledge base, not from one week\u2019s news. The sources are the RBR ATM market reports, the Futurist agent\u2019s research, and the collected statistics, regulation and vendor findings. A pattern is kept only if it is backed by evidence from official public sources: the ECB, EU law, national central banks and named consulting reports. Patterns are refreshed about once a month. Read each week\u2019s signals against them: a signal that goes against a pattern is the interesting one.'},
  {id:'baselines',  label:'Charts', group:'near', icon:ICON.baselines, title:'Near-term outlook — charts', sub:'These are recorded numbers, not opinions. For EU markets they come from the ECB Data Portal: payment terminals, card cash withdrawals, branches and staff. For non-EU markets they come from each national central bank, plus a dated market workbook. Every series is yearly and shows the year it was last updated, so you can see when a market has gone quiet. Beside the recorded line, each chart shows two readings of next year: one from the signals and one from the patterns.'},
  {id:'futures',    label:'Future outlook',     group:'future', icon:ICON.futures,    title:'Structural outlook, 2 to 5 years',                sub:'Where cash, self-service, payments and ATMs are heading in the next 2 to 5 years, up to about 2028\u20132031. Written by the Futurist agent from internal trend reports and public research.'},
  {id:'underlying', label:'The underlying data', group:'future', icon:ICON.underlying, title:'The underlying data',             sub:'The numbers behind the 3\u20135 year view: revenue by segment, how competition is shifting, the risks to watch, and the dated turning points. Every figure names its source.'},
  // MARKET DATA — the specific findings broken down by segment
  {id:'overview',   label:'Overview',          group:'data'        , icon:ICON.overview,   title:'Footprint overview',          sub:'Where the opportunity is across the footprint: pipeline value by market and by product, and the strongest opportunities open right now.'},
  {id:'country',    label:'Countries',          group:'data', nested:true,         icon:ICON.country,    title:'Markets',                  sub:'Opportunity by market, the background numbers for each, and the themes that affect every country at once.'},
  {id:'product',    label:'Products',           group:'data', nested:true,         icon:ICON.product,    title:'Products and demand',           sub:'How strong demand is for each Printec solution, based on the evidence collected so far.'},
  {id:'competition',label:'Competition',        group:'data', nested:true,         icon:ICON.competition,title:'Competitors and partners',        sub:'Competitor and partner pressure across the footprint: where Printec is being shut out and where gaps are opening.'},
  {id:'accounts',   label:'Accounts & timing',  group:'data',         icon:ICON.accounts,   title:'Account targets and deadlines',             sub:'Named banks to approach, with the reason to act now, plus the regulatory deadlines that force banks to spend (the buying window).'},
  {id:'signals',    label:'All signals',        group:'data',         icon:ICON.signals,    title:'All signals',             sub:'Every signal in this week\u2019s table: opportunities, positions already held, deals a competitor won, and the market drivers behind them. Filter by market, product, lane or confidence.'},
  // BUDGET — the group budget beside the market, a stand-alone tab at the end (11/09/2026)
  {id:'budget',     label:'Budget 2027',        group:'budget',       icon:ICON.overview,   title:'Budget 2027',   sub:'The 2027 budget: the executive summary, then the moves market by market. Click an estimate to show it in the table; click a cell or open a line for the details.'},
];
const TAB_GROUPS = [
  {id:'near',   label:'Near-term perspectives'},
  {id:'future', label:'Future perspectives'},
  {id:'data',   label:'Market data'},
  {id:'budget', label:'Budget'}
];

let DASH=null, sigByKey={}, charts=[], current='overview', dataSource='bundled';
let manifest={weeks:[]}, view={mode:'latest', week:null, monthKey:null, monthInfo:null};
let opRank='recent';   // overview "Top opportunities" lens: 'recent' (freshest first) | 'value' (largest indicative € size)

/* ----------------------------------------------------------------- load */
// loadData(week): a specific archived week → /api/data?week=… (null if not found).
// loadData(null): the latest snapshot, with the same inline → live → bundled fallback chain.
async function loadData(week){
  if (window.__DASH_DATA__){ dataSource='inline'; return window.__DASH_DATA__; }   // offline: single snapshot
  if (week){
    try{
      const r = await fetch('/api/data?week='+encodeURIComponent(week), {cache:'no-store'});
      if (r.ok){ const j = await r.json(); if (j && j.signals) return j; }
    }catch(e){}
    return null;   // archived week unavailable
  }
  try{
    const r = await fetch('/api/data', {cache:'no-store'});
    if (r.ok){ const j = await r.json(); if (j && j.signals){ dataSource='live'; return j; } }
  }catch(e){ /* fall through to bundled */ }
  const r2 = await fetch('./data.json', {cache:'no-store'});
  if (!r2.ok) throw new Error('No data available');
  const j2 = await r2.json();
  if (!j2 || !Array.isArray(j2.signals)) throw new Error('Bundled snapshot is malformed');
  dataSource='bundled'; return j2;
}
// the index of archived weeks; synthesised from the current snapshot when offline or before any publish.
async function loadManifest(){
  const synth = () => { const d=DASH||window.__DASH_DATA__;
    return d ? {weeks:[{week:d.week, generated:d.generated, ...(d.kpis||{})}]} : {weeks:[]}; };
  if (window.__DASH_DATA__) return synth();
  try{
    const r = await fetch('/api/manifest', {cache:'no-store'});
    if (r.ok){ const m = await r.json(); if (m && Array.isArray(m.weeks) && m.weeks.length) return m; }
  }catch(e){}
  // a transient manifest error shouldn't collapse the picker — keep the last good index if we have one
  if (manifest && Array.isArray(manifest.weeks) && manifest.weeks.length>1) return manifest;
  return synth();
}

/* ----------------------------------------------------------------- helpers */
function prods(s){ return (s.products||[]).map(p =>
  `<span class="pp" style="border-color:${PCOL[p]||'#E7DDC9'}">${esc(DASH.prod_label[p]||p)}</span>`).join(""); }
/* ---- source / evidence helpers ---- */
const FINDING_TOPIC={'01-bank-disclosures':'Bank disclosures','02-tenders':'Tenders & procurement',
  '03-regulation':'Regulation','04-statistics':'Market statistics','05-jobs':'Jobs & leadership','06-vendors':'Competitors & partners'};
function findingLabel(p){
  const f=String(p||'').split('/')[1]||'';
  const num=f.slice(0,2);
  const agent=/^\d+$/.test(num)?('A'+String(parseInt(num,10))):'';
  let topic=FINDING_TOPIC[f];
  if(!topic){ let t=/^\d\d-/.test(f)?f.slice(3):f; t=t.replace(/-/g,' ').trim(); topic=t?t.charAt(0).toUpperCase()+t.slice(1):'Evidence file'; }
  return topic+(agent?(' ('+agent+')'):'');
}
// A bare URL is shown as its host plus a trimmed path. It contains no spaces, so nothing can wrap it —
// the whole label has to be capped, not just the path, or a long one pushes its column off the page.
function prettyUrl(u){
  try{
    const a=new URL(u);
    const host=a.hostname.replace(/^www\./,'');
    let p=(a.pathname||'').replace(/\/$/,'');
    const room=42-host.length;
    if(p.length>room) p = room>4 ? p.slice(0,room-1)+'…' : (p?'/…':'');
    return host+p;
  }catch(e){ return String(u||''); }
}
// Source DOCUMENTS + link-rot SNAPSHOTS are served by /api/evidence on the live web app. The offline
// single-file build (data inlined, no server) can only offer the external web links, so gate on that.
const EVIDENCE_LIVE = !window.__DASH_DATA__;
function docHref(fp){ return '/api/evidence?week='+encodeURIComponent((DASH&&DASH.week)||'')+'&path='+encodeURIComponent(fp); }
function snapHref(snap){ return '/api/evidence?snapshot='+encodeURIComponent(String(snap||'').replace(/\.txt$/,'')); }

// ============================================================================
// In-app evidence VIEWER. The /api/evidence endpoint serves everything as inert
// text/plain (snapshots are raw third-party HTML and must never execute on our
// origin). So instead of navigating the browser to that raw text, we fetch it
// and render it readably here: Markdown for the agent's .md findings, and a
// SAFE text extraction (via DOMParser — never executes scripts) for snapshots.
// All file content is HTML-escaped before rendering; only a whitelisted set of
// structural tags is emitted, so this is XSS-safe even on untrusted captures.
// ----------------------------------------------------------------------------
function inlineMd(s){
  const str=String(s==null?'':s);
  const re=/(`[^`]+`)|(\*\*[^*]+\*\*|__[^_]+__)|(\*[^*\s][^*]*\*|_[^_\s][^_]*_)|\[([^\]]+)\]\((https?:\/\/[^)\s]+|findings\/\d\d-[a-z0-9-]+\/[A-Za-z0-9._-]+\.md)\)|(https?:\/\/[^\s)]+)/g;
  let out='',last=0,m;
  while((m=re.exec(str))){
    out+=esc(str.slice(last,m.index));
    if(m[1]) out+=`<code>${esc(m[1].slice(1,-1))}</code>`;
    else if(m[2]) out+=`<strong>${esc(m[2].slice(2,-2))}</strong>`;
    else if(m[3]) out+=`<em>${esc(m[3].slice(1,-1))}</em>`;
    else if(m[4]!=null && m[5]){
      if(/^findings\//.test(m[5])) out+= EVIDENCE_LIVE
          ? `<a class="link srcfile" href="${esc(docHref(m[5]))}">${esc(m[4])}</a>` : esc(m[4]);
      else { const u=safeUrl(m[5]); out+= u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(m[4])}</a>`:esc(m[4]); }
    }
    else if(m[6]){ const u=safeUrl(m[6]); out+= u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(prettyUrl(m[6]))}</a>`:esc(m[6]); }
    last=re.lastIndex;
  }
  return out+esc(str.slice(last));
}
function mdToHtml(md){
  const lines=String(md==null?'':md).replace(/\r\n?/g,'\n').split('\n');
  const sep=l=>/^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$/.test(l);
  const cells=l=>l.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(c=>c.trim());
  let html='', i=0;
  while(i<lines.length){
    const l=lines[i];
    if(/^\s*$/.test(l)){ i++; continue; }
    if(/^\s*```/.test(l)){ i++; const buf=[]; while(i<lines.length && !/^\s*```/.test(lines[i])){ buf.push(lines[i]); i++; } i++; html+=`<pre class="md-code"><code>${esc(buf.join('\n'))}</code></pre>`; continue; }
    if(l.indexOf('|')>=0 && i+1<lines.length && sep(lines[i+1])){
      const head=cells(l); i+=2; const rows=[];
      while(i<lines.length && lines[i].indexOf('|')>=0 && !/^\s*$/.test(lines[i])){ rows.push(cells(lines[i])); i++; }
      html+='<div class="md-tablewrap"><table class="md-table"><thead><tr>'+head.map(c=>`<th>${inlineMd(c)}</th>`).join('')+
        '</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(c=>`<td>${inlineMd(c)}</td>`).join('')+'</tr>').join('')+'</tbody></table></div>'; continue;
    }
    const h=l.match(/^(#{1,6})\s+(.*)$/);
    if(h){ const n=h[1].length; html+=`<h${n} class="md-h">${inlineMd(h[2].replace(/\s+#+\s*$/,''))}</h${n}>`; i++; continue; }
    if(/^\s*([-*_])\s*(\1\s*){2,}$/.test(l)){ html+='<hr class="md-hr">'; i++; continue; }
    if(/^\s*>/.test(l)){ const buf=[]; while(i<lines.length && /^\s*>/.test(lines[i])){ buf.push(lines[i].replace(/^\s*>\s?/,'')); i++; } html+=`<blockquote class="md-bq">${inlineMd(buf.join(' '))}</blockquote>`; continue; }
    if(/^\s*([-*+]|\d+\.)\s+/.test(l)){
      const ordered=/^\s*\d+\.\s+/.test(l), tag=ordered?'ol':'ul', items=[];
      while(i<lines.length && /^\s*([-*+]|\d+\.)\s+/.test(lines[i])){ items.push(lines[i].replace(/^\s*([-*+]|\d+\.)\s+/,'')); i++; }
      html+=`<${tag} class="md-list">`+items.map(it=>`<li>${inlineMd(it)}</li>`).join('')+`</${tag}>`; continue;
    }
    const buf=[];
    while(i<lines.length && !/^\s*$/.test(lines[i]) && !/^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|>|```)/.test(lines[i]) && !(lines[i].indexOf('|')>=0 && i+1<lines.length && sep(lines[i+1]))){ buf.push(lines[i]); i++; }
    if(buf.length) html+=`<p class="md-p">${inlineMd(buf.join(' '))}</p>`; else i++;
  }
  return html;
}
// Safe HTML→text: parse in a detached document (scripts never run, no resources load), strip noise, keep block breaks.
function htmlToText(html){
  let doc; try{ doc=new DOMParser().parseFromString(String(html||''),'text/html'); }catch(e){ return String(html||''); }
  doc.querySelectorAll('script,style,noscript,svg,iframe,head,template,nav,header,footer,aside,form').forEach(n=>n.remove());
  // reader-mode: pick the LARGEST main-content container, NOT the first. News pages wrap every teaser/related
  // item in its own <article> (dozens per page), so querySelector('article') grabs a one-line snippet instead
  // of the story. Score article/main/[role=main] by text length and take the biggest; if that's only a small
  // slice of the page (the real content lives in a plain <div>), fall back to the whole body.
  const _tlen=el=>((el&&el.textContent)||'').replace(/\s+/g,' ').trim().length;
  const _body=doc.body||doc.documentElement;
  let root=_body, _best=0;
  doc.querySelectorAll('article, main, [role="main"]').forEach(el=>{ const l=_tlen(el); if(l>_best){ _best=l; root=el; } });
  if(_best && _best < Math.max(400, _tlen(_body)*0.2)) root=_body;
  const BLOCK=new Set(['P','DIV','SECTION','ARTICLE','MAIN','UL','OL','LI','TABLE','TR','TD','TH','H1','H2','H3','H4','H5','H6','BLOCKQUOTE','PRE','FIGURE','FIGCAPTION','HR']);
  const out=[];
  (function walk(node){
    for(const c of node.childNodes){
      if(c.nodeType===3) out.push(c.nodeValue);
      else if(c.nodeType===1){
        if(c.tagName==='BR'){ out.push('\n'); continue; }
        const b=BLOCK.has(c.tagName); if(b) out.push('\n'); walk(c); if(b) out.push('\n');
      }
    }
  })(root);
  return out.join('').replace(/[ \t ]+/g,' ').replace(/ *\n */g,'\n').replace(/\n{3,}/g,'\n\n').trim();
}
function snapshotToHtml(raw){
  const lines=String(raw==null?'':raw).replace(/^﻿/,'').replace(/\r\n?/g,'\n').split('\n'); const meta={}; let hi=0;
  for(; hi<lines.length; hi++){ const mm=lines[hi].match(/^\s*(URL|FETCHED|HTTP):\s*(.*)$/); if(mm){ meta[mm[1]]=mm[2].replace(/\s+$/,''); } else if(/^\s*$/.test(lines[hi])) continue; else break; }
  const body=lines.slice(hi).join('\n');
  const u=safeUrl(meta.URL||'');
  const looksHtml=/<\s*(!doctype|html|body|div|p|table|head|span|a|script)\b/i.test(body);
  const readable=looksHtml?htmlToText(body):body.trim();
  return `<div class="snap-meta">`+
    (meta.URL?`<div class="snap-url">Captured from ${u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(meta.URL)}</a>`:esc(meta.URL)}</div>`:'')+
    `<div class="snap-sub">${meta.FETCHED?'Retrieved '+esc(meta.FETCHED):''}${meta.HTTP?' · HTTP '+esc(meta.HTTP):''} · point-in-time archived copy (link-rot defense)</div></div>`+
    `<pre class="snap-body">${esc(readable)}</pre>`;
}
let _evv;
function evViewer(){
  if(_evv) return _evv;
  const ov=document.createElement('div'); ov.className='ev-overlay'; ov.setAttribute('hidden','');
  ov.innerHTML='<div class="ev-modal" role="dialog" aria-modal="true" aria-label="Source viewer">'+
    '<div class="ev-head"><div class="ev-title"></div><div class="ev-actions">'+
    '<a class="ev-raw link" target="_blank" rel="noopener noreferrer" title="Open the raw file in a new tab">raw ↗</a>'+
    '<button class="ev-close" type="button" aria-label="Close">✕</button></div></div><div class="ev-body"></div></div>';
  document.body.appendChild(ov);
  const hide=()=>ov.setAttribute('hidden','');
  ov.addEventListener('click',e=>{ if(e.target===ov) hide(); });
  ov.querySelector('.ev-close').addEventListener('click',hide);
  document.addEventListener('keydown',e=>{ if(e.key==='Escape' && !ov.hasAttribute('hidden')) hide(); });
  _evv={ov,title:ov.querySelector('.ev-title'),body:ov.querySelector('.ev-body'),raw:ov.querySelector('.ev-raw'),show:()=>ov.removeAttribute('hidden'),hide};
  return _evv;
}
function isPdfUrl(u){ return /\.pdf(?:[?#]|$)/i.test(String(u||'')); }
// PDF.js, lazy-loaded once. We render PDFs to <canvas> rather than an <iframe>, because the dashboard runs
// inside the Claude desktop app (Electron), whose renderer has no native PDF plugin — a <iframe src=*.pdf>
// just shows a gray box there. Canvas rendering works in Electron, headless and real browsers alike.
let _pdfjsP;
function loadPdfJs(){
  if(_pdfjsP) return _pdfjsP;
  _pdfjsP=new Promise((resolve,reject)=>{
    if(window.pdfjsLib){ resolve(window.pdfjsLib); return; }
    const s=document.createElement('script');
    s.src='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    s.onload=()=>{ try{ window.pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'; resolve(window.pdfjsLib); }catch(e){ reject(e); } };
    s.onerror=()=>reject(new Error('pdf.js failed to load'));
    document.head.appendChild(s);
  });
  return _pdfjsP;
}
async function renderPdfPage(pdf, num, canvas){
  try{
    const page=await pdf.getPage(num);
    const cw=Math.min((canvas.parentElement&&canvas.parentElement.clientWidth)||820, 900);
    const base=page.getViewport({scale:1});
    const scale=(cw/base.width)*(window.devicePixelRatio||1);
    const vp=page.getViewport({scale});
    canvas.width=vp.width; canvas.height=vp.height; canvas.style.height='auto';
    await page.render({canvasContext:canvas.getContext('2d'), viewport:vp}).promise;
  }catch(e){}
}
async function renderPdfDoc(container, url, startPage){
  let lib; try{ lib=await loadPdfJs(); }
  catch(e){ container.innerHTML='<div class="ev-msg">Couldn’t load the PDF viewer. <a class="link" href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">Open the PDF directly ↗</a></div>'; return; }
  try{
    const pdf=await lib.getDocument({url}).promise;   // uses HTTP range requests against /api/evidence
    container.innerHTML='';
    const pages=document.createElement('div'); pages.style.cssText='display:flex;flex-direction:column;align-items:center;gap:12px';
    container.appendChild(pages);
    const io=new IntersectionObserver(es=>{ es.forEach(en=>{ if(en.isIntersecting){ const c=en.target; io.unobserve(c); renderPdfPage(pdf,+c.dataset.page,c); } }); },{root:container, rootMargin:'1000px'});
    for(let p=1;p<=pdf.numPages;p++){ const cv=document.createElement('canvas'); cv.dataset.page=p; cv.width=820; cv.height=1060; cv.style.cssText='width:100%;max-width:900px;height:auto;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.15);border-radius:4px'; pages.appendChild(cv); io.observe(cv); }
    if(startPage>1){ const t=pages.querySelector('canvas[data-page="'+startPage+'"]'); if(t) setTimeout(()=>t.scrollIntoView({block:'start'}),200); }
  }catch(e){ container.innerHTML='<div class="ev-msg">Couldn’t render this PDF ('+esc(String((e&&e.message)||e))+'). <a class="link" href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">Open it directly ↗</a></div>'; }
}
async function openEvidence(href, label){
  const v=evViewer();
  // a source PDF (?pdf=<slug>&page=N) → render it with PDF.js at the cited page
  const pdfm=href.match(/[?&]pdf=([a-z0-9-]+)/i);
  if(pdfm){
    const pg=(href.match(/[?&]page=(\d+)/)||[])[1];
    const src='/api/evidence?pdf='+pdfm[1];
    let t=(label||'Source report').replace(/\s*↗\s*$/,'').trim();
    if(pg && !new RegExp('p\\.'+pg+'(?!\\d)').test(t)) t+=' — p.'+pg;
    v.title.textContent=t;
    v.raw.href=src+(pg?('#page='+pg):''); v.body.className='ev-body';
    v.body.innerHTML='<div class="ev-msg">Loading the report…</div>'; v.show();
    renderPdfDoc(v.body, src, pg?parseInt(pg):1);
    return;
  }
  const isSnap=/[?&]snapshot=/.test(href);
  v.title.textContent=isSnap?'Archived source snapshot':(label||'Source document');
  v.raw.href=href; v.body.className='ev-body'; v.body.innerHTML='<div class="ev-msg">Loading…</div>'; v.show();
  try{
    const r=await fetch(href,{headers:{'Accept':'text/plain'}});
    if(!r.ok){ v.body.innerHTML='<div class="ev-msg">'+(r.status===404?'This source hasn’t been published to the live store yet.':'Couldn’t load this source (HTTP '+esc(String(r.status))+').')+'</div>'; return; }
    const txt=await r.text();
    if(isSnap){
      const mu=txt.match(/^URL:\s*(\S+)/m);
      if(/%PDF-/.test(txt.slice(0,2000)) && mu){ v.body.innerHTML='<div class="ev-msg">This source is a PDF — the point-in-time text archive isn’t viewable. <a class="link" href="'+esc(mu[1])+'" target="_blank" rel="noopener noreferrer">Open the original PDF ↗</a></div>'; return; }  // a PDF snapshot is mangled text
      v.body.classList.add('ev-snap'); v.body.innerHTML=snapshotToHtml(txt);
    }
    else { v.body.classList.add('ev-md'); v.body.innerHTML=mdToHtml(txt); }
    v.body.scrollTop=0;
  }catch(e){ v.body.innerHTML='<div class="ev-msg">Couldn’t load this source (network error).</div>'; }
}
// intercept clicks on any /api/evidence link → open the readable viewer instead of the raw text tab
document.addEventListener('click',e=>{
  const a=e.target.closest && e.target.closest('a[href^="/api/evidence"]');
  if(!a || a.classList.contains('ev-raw')) return;   // let the in-modal "raw ↗" open the file natively
  e.preventDefault();
  openEvidence(a.getAttribute('href'), (a.textContent||'').replace(/^[↗\s]+/,'').trim());
});
// Turn citations embedded in any free-text field (stats figures, regulatory deadlines, milestone rows,
// outlook drivers) into clickable sources — the same idea as the signal Sources line, applied everywhere a
// number or claim carries a reference. Recognises markdown [label](url), bare http(s) URLs, and internal
// findings/… refs (→ the source document on the live app). All non-link text is HTML-escaped, so this is
// safe to run on raw source strings.
function linkify(text){
  const str=String(text==null?'':text);
  const re=/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|(https?:\/\/[^\s)]+)|(findings\/\d\d-[a-z0-9-]+\/[A-Za-z0-9._-]+\.md)/g;
  let out='',last=0,m;
  while((m=re.exec(str))){
    out+=esc(str.slice(last,m.index));
    if(m[1]&&m[2]){ const u=safeUrl(m[2]); out+=u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(m[1])}</a>`:esc(m[1]); }
    else if(m[3]){ const u=safeUrl(m[3]); out+=u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(prettyUrl(m[3]))}</a>`:esc(m[3]); }
    else if(m[4]){ const fp=m[4]; out+=EVIDENCE_LIVE
      ?`<a class="link srcfile" href="${esc(docHref(fp))}" target="_blank" rel="noopener noreferrer" title="Open the source document — ${esc(fp)}">${esc(findingLabel(fp))}</a>`
      :`<span class="srcfile" title="${esc(fp)}">${esc(findingLabel(fp))}</span>`; }
    last=re.lastIndex;
  }
  out+=esc(str.slice(last));
  return out;
}
// a clickable "Source: …" line from a structured {Source name, URL} pair (workbook rows / curated items)
function sourceLine(name, url){
  const u=safeUrl(url);
  const inner=u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(name||prettyUrl(url))}</a>`
               :(name?linkify(name):'');
  return inner?`<div class="small muted evsrc">Source: ${inner}</div>`:'';
}
// a plain-text "Source: …" caption for charts (multi-source / internal-pipeline strings, not a single clickable
// workbook link). Returns a DOM node so callers can append it as the footer of a chart card / chart-panel.
function chartSource(srcText){ return el("div","small muted evsrc","Source: "+srcText); }
// case-insensitive field lookup (workbook-ingested rows keep human key names like "Source"/"URL")
function field(o,names){ if(!o)return''; for(const k in o){ if(names.indexOf(k.toLowerCase().trim())>=0 && o[k]!=null && o[k]!=='') return o[k]; } return ''; }
// the headline source line: real web links are clickable; internal finding refs become labelled chips
// (what kind of evidence it is) rather than the old dead "A1" text — and link to the source document on
// the live app. The full clickable trail is below.
function srcLinks(s){ return (s.sources||[]).map(x =>{
  const u = safeUrl(x.url);
  if(u) return `<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(x.text)}</a>`;
  if(x.url && x.url.indexOf('findings/')===0){
    const lbl=findingLabel(x.url);
    return EVIDENCE_LIVE
      ? `<a class="link srcfile" href="${esc(docHref(x.url))}" target="_blank" rel="noopener noreferrer" title="Open the source document — ${esc(x.url)}">${esc(lbl)}</a>`
      : `<span class="srcfile" title="${esc(x.url)}">${esc(lbl)}</span>`;
  }
  return esc(x.text);
  }).join(" &middot; ") || '<span class="muted">—</span>'; }
// the evidence trail: every external source verify.py re-fetched for the finding files this signal cites,
// each clickable with a reachability marker (✓ live & snapshotted · ⚠ unreachable when last checked) and,
// on the live app, an "archived" link to the point-in-time snapshot + the agent's full source document.
// Shared: render the per-finding-file <details> groups for a list of cited finding paths. Reused by signal
// cards AND the Outlook tab so a reader can open the exact agent source documents (each URL ✓/⚠ + snapshot).
function evidenceGroups(cites){
  const idx=DASH.evidence_files||{};
  return (cites||[]).map(fp=>{
    const ev=idx[fp]; if(!ev||!(ev.sources&&ev.sources.length)) return '';
    const items=ev.sources.map(x=>{
      const ok=x.status==='ok';
      const u=safeUrl(x.url);
      const link=u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(prettyUrl(x.url))}</a>`:esc(prettyUrl(x.url));
      const arch=(EVIDENCE_LIVE && x.snapshot)?` <a class="link evarch" href="${esc(snapHref(x.snapshot))}" target="_blank" rel="noopener noreferrer" title="Point-in-time archived copy (link-rot defense)">archived</a>`:'';
      const mark=ok?`<span class="evmark ok" title="reachable &amp; snapshotted this run${x.snapshot?' ('+esc(x.snapshot)+')':''}">✓</span>`
                   :`<span class="evmark bad" title="unreachable when last checked${x.code?' — HTTP '+esc(x.code):''}">⚠</span>`;
      return `<li>${mark}${link}${arch}</li>`;
    }).join('');
    const docLi=EVIDENCE_LIVE?`<li class="evdoc"><a class="link" href="${esc(docHref(fp))}" target="_blank" rel="noopener noreferrer">↗ Open the full ${esc(ev.label||'')} document</a></li>`:'';
    return `<details class="evfile"><summary><span class="evf-lbl">${esc(ev.label||fp)}</span><span class="evf-n">${ev.reachable} of ${ev.total} reachable</span></summary><ul class="evlist">${docLi}${items}</ul></details>`;
  }).filter(Boolean).join('');
}
// CARD-SCOPED evidence trail: ONLY the sources this card actually cites (its Source cell + inline links in
// its own text), each clickable with a reachability marker (✓ live & snapshotted · ⚠ unreachable · · not
// re-checked) and an "archived" snapshot link. The agent's full working files are a demoted pointer, not an
// expanded dump — so a reader sees the handful of sources that back THIS card, not every link the agent filed.
// CARD-SCOPED sources, shared by signal cards and the Outlook/Future cards. Renders ONLY the sources a card
// actually cites, each with a reachability marker (✓ live & snapshotted · ⚠ unreachable · · not re-checked).
// HTML sources keep a readable archived snapshot; PDF sources open in a new tab (their text snapshot is unusable
// and Electron/iframe can't embed them). The agent's full files are a demoted "working notes" pointer, never an
// expanded per-file dump — so a reader sees the handful of sources that back THIS card, not every link filed.
function citedSourcesHtml(cited){
  if(!cited || !cited.length) return '';
  return '<ul class="evlist evcited">'+cited.map(x=>{
    const ok=x.status==='ok', u=safeUrl(x.url), pdf=isPdfUrl(x.url);
    const label=esc(x.label||prettyUrl(x.url||''));
    const link=u?`<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer"${pdf?' title="Open the source PDF"':''}>${label}</a>`:label;
    const arch=(!pdf && EVIDENCE_LIVE && x.snapshot)?` <a class="link evarch" href="${esc(snapHref(x.snapshot))}" target="_blank" rel="noopener noreferrer" title="Point-in-time archived copy (link-rot defense)">archived</a>`:'';
    const mark=ok?`<span class="evmark ok" title="reachable &amp; snapshotted this run">✓</span>`
              : x.status?`<span class="evmark bad" title="unreachable when last checked${x.code?' — HTTP '+esc(x.code):''}">⚠</span>`
              : `<span class="evmark" title="not re-checked this run">·</span>`;
    return `<li>${mark}${link}${arch}</li>`;
  }).join('')+'</ul>';
}
function workingNotesHtml(files){
  if(!files || !files.length) return '';
  const links=files.map(fp=> EVIDENCE_LIVE
      ? `<a class="link srcfile" href="${esc(docHref(fp))}" target="_blank" rel="noopener noreferrer" title="Open the agent's full working notes — ${esc(fp)}">${esc(findingLabel(fp))}</a>`
      : `<span class="srcfile" title="${esc(fp)}">${esc(findingLabel(fp))}</span>`).join(' &middot; ');
  return `<div class="muted evnote evworking">Working notes: ${links}</div>`;
}
function evidenceTrail(s){
  const p=s.provenance||{};
  const cited=p.cited||[], files=p.cites||[];
  if(!cited.length && !files.length) return '';
  return `<div class="k">Sources</div><div class="small evtrail">${citedSourcesHtml(cited)}${workingNotesHtml(files)}</div>`;
}
// The Outlook is reasoned judgment, but every fact in it comes from specific signals + agent findings. This
// renders that trail under each outlook: the signals it's built on, an optional headline link, and a
// collapsible evidence trail of every source behind the agent files it reasons from — so the reader can check.
function outlookEvidence(o){
  const ev=o&&o.evidence; if(!ev) return '';
  const sigs=ev.signals||[];
  const cited=ev.cited||[], files=ev.cites||[];
  const chips=sigs.length?`<div class="ol-builton"><span class="ol-evk" title="The signals this projection is based on. Click one to see the signal and its sources.">Built on</span> ${sigs.map(x=>`<span class="srcfile ol-sig" data-sigkey="${esc(x.key)}" role="button" tabindex="0" title="Show this signal &amp; its sources">${esc(x.bank_theme)}</span>`).join('')}<div class="ol-sigdetail" hidden></div></div>`:'';
  // CARD-SCOPED sources (same model as signal cards): only what this projection cites — its drivers'/rationale's
  // inline links + headline + source_reports — with reachability; cited finding files become "Working notes".
  const n=cited.length, r=cited.filter(x=>x.status==='ok').length;
  const srcBlock=(cited.length||files.length)
    ? `<div class="ol-srcline"><span class="ol-evk">Sources</span>${n?` <span class="evf-n">${r} of ${n} reachable</span>`:''}</div><div class="small evtrail">${citedSourcesHtml(cited)}${workingNotesHtml(files)}</div>`
    : '';
  const ung=ev.ungrounded||[];
  const ungNote=ung.length?`<details class="ol-ungrounded"><summary>⚠ ${ung.length} claim${ung.length>1?'s':''} not yet linked to a cited source</summary><ul>${ung.map(u=>`<li>${esc(u)}</li>`).join('')}</ul><div class="muted evnote">Flagged by the citation audit: these specific points are reasoned in but don't yet trace to one of the cited sources above. Treat with extra care until sourced.</div></details>`:'';
  const valnote=ev.validated?`<div class="ol-valnote" title="A separate check read this outlook against the documents it cites, independently of the analyst who wrote it.">✓ Independently validated${ung.length?` — every other claim traces to a cited source`:` — all claims trace to a cited source`}.</div>`:'';
  if(!sigs.length && !srcBlock) return '';
  return `<div class="ol-evidence">${chips}${srcBlock}${ungNote}${valnote}</div>`;
}
// A "Built on" chip names a master-table signal the projection reasons from. Clicking it reveals that signal
// inline — what it implies + its source links — so the reader can see what the chip refers to without leaving
// the card (signals live across several tabs and may be collapsed, so an inline reveal is the reliable trail).
function revealSignal(chip){
  const wrap=chip.closest('.ol-builton'); if(!wrap) return;
  const panel=wrap.querySelector('.ol-sigdetail'); if(!panel) return;
  const key=chip.dataset.sigkey;
  if(!panel.hidden && panel.dataset.k===key){ panel.hidden=true; chip.classList.remove('on'); return; }   // toggle off
  wrap.querySelectorAll('.ol-sig.on').forEach(o=>o.classList.remove('on'));
  chip.classList.add('on'); panel.dataset.k=key; panel.hidden=false;
  const sg=sigByKey[key];
  panel.innerHTML = sg
    ? `<div class="ol-sigd-h"><b>${esc(sg.bank_theme)}</b> <span class="flag">${esc(ctryNames(sg))}</span> <span class="pill ${esc(sg.confidence)}">${esc(sg.confidence||'—')}</span></div>`
      +`<div class="ol-sigd-b">${esc(sg.implies||sg.signal||'')}</div>`
      +`<div class="ol-sigd-s"><span class="ol-evk">Sources</span> ${srcLinks(sg)}</div>`
    : `<div class="muted">This signal isn't in the current week's set (it may have aged out since the projection was written). It's the master-table theme the projection was reasoned from.</div>`;
}
function ctryNames(s){
  if (s.footprint_wide && s.countries.length===0) return "Footprint-wide";
  let n = s.countries.map(c => DASH.code2name[c]||c);
  if (s.footprint_wide) n.push("+wide");
  return n.join(", ") || s.country_raw || "—";
}
function provBadge(p){
  if(!p || p.status==='unaudited') return '';
  const M={strong:['prov-ok','✓ sourced'], thin:['prov-thin','◐ sourcing'], broken:['prov-bad','⚠ sources dead'], filed:['prov-thin','◐ in notes']};
  const e=M[p.status]; if(!e) return '';
  if(p.status==='filed') return `<span class="tag ${e[0]}" title="The source links for this card are in the agent\u2019s working file. Open the evidence trail to see them.">${e[1]}</span>`;
  return `<span class="tag ${e[0]}" title="Evidence base: ${p.reachable} of ${p.sources} cited source(s) reachable &amp; snapshotted${p.checked?' · checked '+esc(p.checked):''}">${e[1]}</span>`;
}
function provLine(p){
  if(!p || p.status==='unaudited') return 'Evidence base not audited this run.';
  if(p.status==='filed') return `Specific source links for this card are in the agent working notes (see the evidence trail). <span class="muted">${p.files} working file(s)${p.checked?' · checked '+esc(p.checked):''}.</span>`;
  return `${p.reachable} of ${p.sources} cited source(s) reachable &amp; snapshotted${p.checked?' · checked '+esc(p.checked):''}. <span class="muted">Only the sources this card cites — the agent's full source set is in the working notes below.</span>`;
}
const chev = '<svg class="chev" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>';

// Recency chip — surfaces how fresh the TRIGGERING development is (computed deterministically by the
// engine's recency gate), so a card can never look "new" while resting on an old standing fact.
function ymShort(iso){ if(!iso) return ''; const m=/^(\d{4})-(\d{2})/.exec(iso); if(!m) return esc(iso);
  const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; return MON[+m[2]-1]+' '+m[1]; }
function recencyChip(s){
  if(s.held) return '';   // held/secured positions aren't opportunities — the HELD pill carries the meaning
  const r=s.recency;
  if(r==='fresh') return `<span class="tag rec-fresh" title="The development behind this is less than 3 months old${s.dev_date?' ('+esc(s.dev_date)+')':''}">● fresh</span>`;
  if(r==='recent') return `<span class="tag rec-recent" title="The development behind this is 3 to 6 months old${s.dev_date?' ('+esc(s.dev_date)+')':''}">recent</span>`;
  if(r==='standing' && s.has_future_trigger) return `<span class="tag rec-fwd" title="An older development, but a future deadline keeps it current">forward → ${ymShort(s.future_date)}</span>`;
  if(r==='standing') return `<span class="tag rec-standing" title="The development behind this is more than 6 months old. Background, not news">standing · ${ymShort(s.dev_date)||'dated'}</span>`;
  return s.has_future_trigger?`<span class="tag rec-fwd" title="Future deadline keeps it a current opportunity">forward → ${ymShort(s.future_date)}</span>`:'';
}
// Objective deal-size value — the band is anchored to real tender/capex figures where known; the €m
// midpoints below are an indicative SCALE for aggregation/sorting only, never win-probability-adjusted
// (whether Printec can capture a deal is the business's call, not the dashboard's).
const POT_EUR = {XL:7.5, L:3, M:0.6, S:0.1};
const SIZE_RANGE = {XL:'≥€5m', L:'€1–5m', M:'€0.2–1m', S:'<€0.2m'};
function potEur(b){ return POT_EUR[b] || 0; }
// the date used to rank "most recent": the triggering development if fresh/recent, else the future trigger
function sortDate(s){ return (s && (s.dev_date || s.future_date)) || ''; }
function isStanding(s){ return !!(s && (s.stale_new || (s.recency==='standing' && !s.has_future_trigger) || s.recency==='undated' && !s.has_future_trigger)); }
function isOpportunity(s){ if(s && typeof s.is_opportunity==='boolean') return s.is_opportunity;   // engine gate
  // Deal size is NOT part of the test (changed 2026-08): a net-new contest with no published value is still
  // a contest. Unsized ones carry €0 into the value charts and are labelled "value unscoped".
  return !!(s && (!s.lane || s.lane==='opportunity') && s.is_current && !s.stale_new && !s.held); }   // biddable, current, not held/owned/lost
function isUnscopedOpp(s){ if(s && typeof s.unscoped_opp==='boolean') return s.unscoped_opp;
  return !!(s && isOpportunity(s) && potEur(s.size_band)<=0); }
/* ---- INDIRECT (derived) opportunities ------------------------------------------------------
   A play that no single signal states, composed from 2+ signals across 2+ independent agents.
   Rendered so the inference is impossible to mistake for a sourced deal: a DERIVED badge, the
   composition rule spelled out, the components readable in one click, and the falsifier shown
   next to the claim rather than buried. */
const LANE_LABEL={opportunity:'Opportunity',installed_base:'Installed base',lost:'Lost / competitor-held',context:'Market context / threat'};
function derivedCard(d){
  const mk=(d.countries||[]).map(c=>DASH.code2name[c]||c).join(', ')||(d.footprint_wide?'Footprint-wide':'—');
  const comps=(d.component_keys||[]).map(k=>sigByKey[k]).filter(Boolean);
  const c=el("div","sig derived");
  const row=(k,v)=> v?`<div class="k">${k}</div><div>${inlineMd(v)}</div>`:'';
  c.innerHTML=
   `<div class="t">${esc(d.title)} <span class="pill derived" title="An indirect opportunity. No single signal states it; it comes from combining the ${comps.length} signals below. The facts are sourced; the combination is analysis.">DERIVED</span>${chev}</div>
    <div class="meta">
      <span class="pill ${d.confidence}">${esc(d.confidence)}</span>
      <span class="flag">${esc(mk)}</span>
      <span class="tag unscoped" title="Adds €0 to the value charts. A combined opportunity is never given a made-up deal size.">value unscoped</span>
      <span class="tag" title="How many independent agents stand behind the signals used here, counted from the signals themselves.">${(d.agents||[]).join('+')}</span>
      <span class="tag" title="How many signals this play is composed from.">${comps.length} signals</span>
      ${d.n_new_components?`<span class="pill new">${d.n_new_components} new</span>`:''}
      ${(d.stale_components||[]).length?`<span class="pill standing" title="Refers to ${d.stale_components.length} signal(s) that are no longer in the current table. Check again before acting.">${d.stale_components.length} stale citation${d.stale_components.length===1?'':'s'}</span>`:''}
    </div>
    <div class="prods">${prods({products:d.products||[]})}</div>
    <div class="body">
      ${row('Who buys', d.buyer)}
      ${row('What forces it (dated)', d.trigger)}
      ${row('The play', d.claim)}
      ${row('Why no single signal shows it', d.why_not_visible)}
      ${row('What would kill it', d.falsifier)}
      <div class="k">Composed from</div>
      <div><details class="derived-sigs"><summary>View the ${comps.length} signals behind this play<span class="prod-sigs-chev" aria-hidden="true"></span></summary><div class="ev-body"></div></details></div>
    </div>`;
  const host=c.querySelector('.ev-body');
  comps.forEach(g=>{ const w=el("div","comp");
    w.appendChild(el("div","comp-lane",LANE_LABEL[g.lane]||g.lane));
    w.appendChild(sigCard(g)); host.appendChild(w); });
  const toggle=()=>{ const o=c.classList.toggle("open"); c.setAttribute("aria-expanded",o?"true":"false"); };
  c.setAttribute("role","button"); c.setAttribute("tabindex","0"); c.setAttribute("aria-expanded","false");
  const NESTED='a, details, summary, button, select, input, textarea, label, .sig';
  c.addEventListener('click',e=>{ const n=e.target.closest(NESTED); if(n && c.contains(n) && n!==c) return; toggle(); });
  c.addEventListener('keydown',e=>{ if(e.target!==c) return; if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); } });
  return c;
}
function derivedSection(list,opts){
  opts=opts||{};
  const c=el("div","card lane derived-lane");
  c.innerHTML=`<div class="hd"><div><h2>${esc(opts.title||'Indirect opportunities — composed from several signals')}</h2><div class="desc">Opportunities that <b>no single signal states</b>. Each one is built by combining two or more signals from <b>different agents</b> — often signals the rankings leave out (a market driver with no buyer, a deal a competitor holds, a position Printec already owns). The facts behind each are sourced and clickable. <b>The combination itself is analysis, not a sourced deal</b>, so confidence is capped at Medium-High and none carries a euro value. Each one says what would prove it wrong.</div></div></div>`;
  list.forEach(d=>c.appendChild(derivedCard(d)));
  return c;
}

function sigCard(s){
  if(!s) return el("div");
  const c = el("div","sig"); c.dataset.key=s.key;
  c.setAttribute("role","button"); c.setAttribute("tabindex","0"); c.setAttribute("aria-expanded","false");
  const laneChip = s.lane==='installed_base'
      ? `<span class="pill held" title="Printec already holds this — ${s.contest_type==='owned_asset'?'an asset Printec owns or operates':'a renewal that is near-certain'}. Something to defend and grow, not an opportunity to win.">${s.contest_type==='owned_asset'?'OWNED':'RENEWAL'}</span>`
    : s.lane==='lost'
      ? `<span class="pill lost" title="A named competitor won this, or holds the most valuable part of it. Useful to know, not an opportunity to chase.">LOST</span>`
    : s.biddable===false
      // A row the stricter gate moved out of the rankings. It says so on the card, because a real
      // development quietly dropping out of a count reads as a bug, not as a judgement.
      ? `<span class="pill standing" title="${esc(s.not_biddable_why||'')} — kept as background, and still counted in every signal list.">CONTEXT</span>`
      : `${s.is_new_this_week?'<span class="pill new">NEW</span>':''}${s.stale_new?'<span class="pill standing" title="New to the table this week, but the development behind it is more than 6 months old and has no near-term deadline. Shown as background, not news.">STANDING</span>':''}`;
  c.innerHTML =
   `<div class="t">${esc(s.bank_theme)} ${laneChip}${chev}</div>
    <div class="meta">
      <span class="pill ${s.confidence}">${esc(s.confidence||'—')}</span>
      <span class="flag">${esc(ctryNames(s))}</span>
      ${s.held?`<span class="tag" title="Printec already owns or operates this. A position held, not an opportunity to size.">held position</span>`
        :(potEur(s.size_band)>0?`<span class="tag ev" title="Deal-size band, based on tender or capex figures where known (XL ≥€5m · L €1–5m · M €0.2–1m · S <€0.2m).">${esc(s.size_band)} · ${SIZE_RANGE[s.size_band]||''}</span>`
        :(isUnscopedOpp(s)?`<span class="tag unscoped" title="A real, open contest with no published value yet. It counts as an opportunity everywhere on this dashboard, but adds €0 to the value charts, because we never invent a figure. Finding its size is the next step.">value unscoped</span>`
        :`<span class="tag unscoped" title="Not a deal to bid for: a threat or a market driver. Tracked under Competition and Patterns.">macro / threat</span>`))}
      <span class="tag" title="How many independent agents confirm this signal">${(s.agents||[]).join('+')||'—'}</span>
      ${recencyChip(s)}
      ${provBadge(s.provenance)}
      <span class="muted">${esc(s.date)}</span>
    </div>
    <div class="prods">${prods(s)}</div>
    <div class="body">
      <div class="k">Signal</div><div>${inlineMd(s.signal)}</div>
      <div class="k">What it implies</div><div>${inlineMd(s.implies)}</div>
      <div class="k">6–12 mo likelihood</div><div>${inlineMd(s.likelihood)}</div>
      <div class="k">Recommended follow-up</div><div>${inlineMd(s.follow_up)}</div>
      ${evidenceTrail(s)}
    </div>`;
  const toggle=()=>{ const o=c.classList.toggle("open"); c.setAttribute("aria-expanded", o?"true":"false"); };
  // Only toggle the card from a NON-expandable, non-interactive region. The Evidence trail nests its own
  // <details> groups (plus links/controls); a click inside one of those must drive only that inner control,
  // never bubble up and collapse the parent card (which would also leave the inner <details> stuck open).
  const NESTED='a, details, summary, button, select, input, textarea, label';
  // only bail for an interactive/expandable element INSIDE this card — closest() also matches ANCESTORS
  // (e.g. the product card's "View N signals" <details> wrapper), which must not block the card's own toggle.
  c.addEventListener('click', e=>{ const n=e.target.closest(NESTED); if(n && c.contains(n)) return; toggle(); });
  c.addEventListener('keydown', e=>{ if(e.target!==c) return;   // let a focused nested control handle its own keys
    if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); } });
  return c;
}

// Pull a single readable headline clause out of a dense vendor "latest" string for the overview newspaper
// summary: drop a leading date prefix (e.g. "Q1 2026:"), then cut at the first sentence/clause boundary that
// isn't inside a figure (so "$1.043bn" / "14 countries." don't split it). Long clauses are trimmed on a word
// boundary. The Competition tab still shows the full text — this is just the lead.
function firstMove(text){
  let t=String(text==null?'':text).trim();
  if(!t) return '';
  t=t.replace(/^(?:Q[1-4]\s*)?\d{4}[^:]{0,18}:\s*/,'');                 // strip a leading "Q1 2026:" / "2026 H1:" date label
  let cut=t.length, m, re=/[.;]\s+(?=[A-Z(])/g;
  while((m=re.exec(t))){ if(!/\d/.test(t[m.index-1])){ cut=m.index; break; } }   // first clause break not right after a digit
  let out=t.slice(0,cut).trim();
  if(out.length>190) out=out.slice(0,188).replace(/[\s,;:(]+\S*$/,'').trim()+'…';
  return out;
}

// Reveal panels under a clicked bar — the same drill-down on EVERY bar chart. A bar's items are listed
// below the chart so the reader can see exactly what's behind it (and, for €-value bars, audit the maths).
function revealHead(box, titleHtml){
  box.innerHTML='';
  const head=el("div","reveal-head", titleHtml+`<button class="reveal-x" type="button" aria-label="Close">✕</button>`);
  head.querySelector('.reveal-x').addEventListener('click',()=>{ box.innerHTML=''; });
  box.appendChild(head); box.scrollIntoView({behavior:'smooth',block:'nearest'});
}
// signals behind a bar. contrib=true → show each deal's €-band contribution + the bar's € sum (value bars);
// contrib=false → just list the linked signals (for count / activity bars where the sum isn't €).
function fillSignalReveal(box, label, signals, contrib){
  const list=(signals||[]).filter(Boolean).sort((a,b)=>potEur(b.size_band)-potEur(a.size_band));
  const sum=list.reduce((a,g)=>a+potEur(g.size_band),0);
  const nU=list.filter(isUnscopedOpp).length;
  // "€0.0m from 1 opportunity" reads as worthless; when nothing here carries a published figure, say so
  const head=contrib
    ? (sum>0
        ? `<b>${esc(label)}</b> — €${sum.toFixed(1)}m from ${list.length} opportunit${list.length===1?'y':'ies'} <span class="muted">(sum of the deal-size € below${nU?`; ${nU} of them not yet scoped, so this is a floor`:''})</span>`
        : `<b>${esc(label)}</b> — ${list.length} opportunit${list.length===1?'y':'ies'}, <b>value not yet scoped</b> <span class="muted">(no published deal figure yet — nothing invented)</span>`)
    : `<b>${esc(label)}</b> — ${list.length} signal${list.length===1?'':'s'}`;
  revealHead(box, head);
  if(!list.length){ box.appendChild(el("div","empty","No signals behind this bar.")); return; }
  list.forEach(g=>{ const w=el("div","reveal-item");
    if(contrib) w.appendChild(el("div","small reveal-contrib", potEur(g.size_band)>0
      ? `<b>€${potEur(g.size_band).toFixed(1)}m</b> · band ${esc(g.size_band)} · ${esc(ctryNames(g))}`
      : `<b>value unscoped</b> · no published figure · ${esc(ctryNames(g))}`));
    w.appendChild(sigCard(g)); box.appendChild(w); });
}
// deadlines/tenders behind a bar (Products → demand under deadline)
function fillDeadlineReveal(box, label, items){
  revealHead(box, `<b>${esc(label)}</b> — ${items.length} time-pressured item${items.length===1?'':'s'}`);
  const tl=el("div","tl");
  items.slice().sort((a,b)=>String(a.date).localeCompare(String(b.date))).forEach(d=>{
    const it=el("div","tl-item "+(d.bucket||''));
    const cd=d.days_until<0?`${-d.days_until}d ago`:`in ${d.days_until}d`;
    it.innerHTML=`<div class="tl-when"><div class="d">${esc(d.date)}</div><div class="c">${cd} · ${esc(d.type||'')}</div></div>`
      +`<div class="tl-body"><b>${esc(d.title)}</b><div class="small muted" style="margin-top:2px">${(d.geo_names||[]).map(esc).join(", ")}</div>`
      +`<div class="small" style="margin-top:5px">${linkify(d.forces||'')}</div>${sourceLine(d.source, field(d,['url','link']))}</div>`;
    tl.appendChild(it); });
  box.appendChild(tl);
}
// competitor cards behind a bar (Competition → by product line)
function fillVendorReveal(box, label, vendors){
  revealHead(box, `<b>${esc(label)}</b> — ${vendors.length} competitor${vendors.length===1?'':'s'}`);
  if(!vendors.length){ box.appendChild(el("div","empty","No competitors.")); return; }
  const grid=el("div","vendgrid"); vendors.forEach(v=>grid.appendChild(vendorCard(v))); box.appendChild(grid);
}
// one competitor card with its linked-signals expander (shared by the landscape list + the by-product reveal)
function vendorCard(v){
  const c=el('div','vend');
  c.innerHTML=`<div class="vh"><b>${esc(v.name)}</b><span class="pill threat-${v.threat}">${esc(v.threat)} threat</span><span class="tag">${esc(v.role)}</span>${v.tier?`<span class="tag tier-${v.tier}">${esc(v.tier)}</span>`:''}</div>
    <div class="desc" style="margin-bottom:7px">${(v.countries||[]).map(cc=>esc(DASH.code2name[cc]||cc)).join(', ')||'footprint-wide'} &middot; ${(v.products||[]).map(p=>esc(DASH.prod_label[p]||p)).join(', ')||'—'}${v.last_updated?` &middot; <span class="vend-asof" title="When this entry was last refreshed">as of ${esc(fmtWeek(v.last_updated))}</span>`:''}</div>
    <div class="small">${inlineMd(v.latest)}</div>`;
  const keys=(v.mention_keys||[]).filter(k=>sigByKey[k]);
  if(keys.length){
    const det=el('details','vend-sigs');
    det.innerHTML=`<summary>${keys.length} linked signal${keys.length>1?'s':''} — click to view</summary>`;
    const body=el('div','vend-sigbody'); det.appendChild(body);
    let built=false;
    det.addEventListener('toggle',()=>{ c.classList.toggle('expanded', det.open);
      if(det.open && !built){ built=true; keys.forEach(k=>body.appendChild(sigCard(sigByKey[k]))); } });
    c.appendChild(det);
  } else { c.appendChild(el('div','small muted vend-nosig',"Not named in any active signal — the move above is the latest; use the period picker for past weeks.")); }
  return c;
}

/* ----------------------------------------------------------------- OVERVIEW */
function renderOverview(s){
  ['ovPot','ovProd','ovEv','ovSize','ovWin'].forEach(id=>{ const c=window.Chart&&Chart.getChart(id); if(c){const i=charts.indexOf(c);if(i>=0)charts.splice(i,1);c.destroy();} });
  s.innerHTML="";
  const k=DASH.kpis;
  const isMonth = view.mode==='month';

  if(view.mode!=='latest'){
    const asof = isMonth ? `end of ${esc(view.monthInfo.label)} (week of ${esc(view.monthInfo.monthEndWeek)})` : `the week of ${esc(view.week)}`;
    s.appendChild(el("div","asof",`Point-in-time snapshot — every figure, deadline countdown and movement reflects ${asof}, not today.`));
  }

  // potential opportunity value by market — objective scale from the deal-size bands (current, biddable
  // signals only), summed per country. Shown as an interactive footprint MAP (choropleth) and the ranked BARS
  // side by side; clicking either drives the same fillSignalReveal drill-down. Map geometry: footprint-map.js.
  (function(){
    const sigs=(DASH.signals||[]).filter(isOpportunity);
    if(!sigs.length) return;
    const FW='__fw__';   // opportunities not tied to a single market get their own bar (nothing dropped)
    const potByC={}, itemsByC={};
    sigs.forEach(g=>{ const cs=(g.countries||[]); (cs.length?cs:[FW]).forEach(cc=>{ potByC[cc]=(potByC[cc]||0)+potEur(g.size_band); (itemsByC[cc]=itemsByC[cc]||[]).push(g); }); });
    const rows=Object.entries(potByC).filter(([,v])=>v>0).sort((a,b)=>b[1]-a[1]);
    // Markets whose live contests are ALL value-unscoped: they sum to €0, so they cannot appear on a €-bar
    // without inventing a number. They get their own clickable strip below the chart instead of vanishing.
    const unscopedOnly=Object.keys(itemsByC).filter(c=>c!==FW && !(potByC[c]>0)).sort((a,b)=>itemsByC[b].length-itemsByC[a].length);
    const nUnscoped=sigs.filter(isUnscopedOpp).length;
    const distinct=sigs.reduce((a,g)=>a+potEur(g.size_band),0);
    const MAP=window.FOOTPRINT_MAP;
    const NICE={UA:'Ukraine',MK:'North Macedonia',BA:'Bosnia & Herzegovina',ME:'Montenegro',XK:'Kosovo'};
    const cname=c=> c===FW?'Footprint-wide':(DASH.code2name[c]||NICE[c]||(MAP&&MAP.countries[c]&&MAP.countries[c].name)||c);
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Opportunity value by market</h2><div class="desc">Every <b>open opportunity that can be bid for</b>, sized by its deal band (XL ≥€5m · L €1–5m · M €0.2–1m · S &lt;€0.2m), shown on a map and as a ranked list. <b>Click a market</b> on the map or a bar to see the deals behind it. A deal can involve several markets and is counted under each, so the bars <b>do not add up</b> — the whole pipeline is <b>€${distinct.toFixed(1)}m across ${sigs.length} distinct opportunities</b>.${nUnscoped?` <b>${nUnscoped}</b> of those have <b>no published value yet</b>. They count as opportunities everywhere but add <b>€0</b> to these bars, so the total is a <b>minimum, not a maximum</b>.`:''}</div></div></div>`;
    s.appendChild(card);
    const reveal=el("div","reveal");
    let cur=null;
    const pick=(key)=>{ card.querySelectorAll('.fmap-c.sel').forEach(p=>p.classList.remove('sel'));
      if(key===cur){ cur=null; reveal.innerHTML=''; return; }
      cur=key; const pe=card.querySelector(`.fmap-c[data-code="${key}"]`); if(pe) pe.classList.add('sel');
      fillSignalReveal(reveal, cname(key), itemsByC[key]||[], true); };

    const split=el("div","market-split");
    // BARS — the ranked, precise read (a deal can touch several markets, so the bars <b>do not add up</b>)
    const barsWrap=el("div","mkt-bars");
    barsWrap.innerHTML=`<div class="chart-panel"><div class="chartbox"><canvas id="ovPot"></canvas></div></div>`;
    const drawBars=()=> mkBar("ovPot",rows.map(([c])=>cname(c)),rows.map(([,v])=>+v.toFixed(1)),rows.map(([c])=>c===FW?'#A7B0C0':'#23C0E2'),"Potential value (€m)",true,rows.map(([c])=>cname(c)),
        i=>{ pick(rows[i][0]); });

    // the unscoped-only strip: markets carrying live contests that no €-bar can show
    const unscopedStrip=()=>{ if(!unscopedOnly.length) return null;
      const w=el("div","unscoped-strip");
      w.innerHTML=`<span class="mlk">Open, value not yet scoped</span>`;
      unscopedOnly.forEach(c=>{ const b=el("button","map-fw"); b.type='button';
        b.innerHTML=`${esc(cname(c))} · ${itemsByC[c].length} contest${itemsByC[c].length===1?'':'s'}`;
        b.title='Live contests in this market with no published deal value — click to read them. They carry €0 into the bars above by design.';
        b.addEventListener('click',()=>pick(c)); w.appendChild(b); });
      return w; };

    if(!MAP){ card.appendChild(barsWrap); const u=unscopedStrip(); if(u) card.appendChild(u); card.appendChild(reveal); card.appendChild(chartSource("Printec research agents.")); drawBars(); return; }

    // MAP — the geographic companion (choropleth shaded by the band-sum; no on-map labels, the bars name every market)
    const vmax=Math.max(...rows.filter(([c])=>c!==FW).map(([,v])=>v), 0.0001);
    const hx=h=>{h=h.replace('#','');return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)];};
    const lerp=(a,b,t)=>{const A=hx(a),B=hx(b);return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*t).toString(16).padStart(2,'0')).join('');};
    const fillFor=v=> v>0 ? lerp('#D3EFF8','#0B6F87',Math.sqrt(v/vmax)) : '#E6DECE';
    const paths=Object.entries(MAP.countries).map(([code,c])=>{ const v=potByC[code]||0, n=(itemsByC[code]||[]).length;
      const lbl = v>0 ? ('€'+v.toFixed(1)+'m, '+n+' opportunities')
                : (n ? (n+' opportunit'+(n===1?'y':'ies')+', value not yet scoped') : 'no current opportunity');
      return `<path class="fmap-c${(v>0||n)?' has':''}" data-code="${code}" d="${c.d}" fill="${fillFor(v)}" aria-label="${esc(cname(code))}: ${lbl}"></path>`; }).join('');
    const mapBox=el("div","mkt-map");
    mapBox.innerHTML=`<div class="map-wrap"><svg class="fmap" viewBox="${MAP.viewBox}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Opportunity value by market across the Printec footprint"><path class="fmap-ctx" d="${MAP.context}"></path>${outsidePaths(MAP)}${paths}</svg><div class="map-tip" hidden></div></div>
      <div class="map-legend"><span class="mlk">Value</span><span>€0</span><span class="map-grad"></span><span>€${vmax.toFixed(0)}m</span><span class="mlk2"><span class="msw"></span> none</span></div>`;
    split.appendChild(mapBox); split.appendChild(barsWrap);
    card.appendChild(split);
    if((itemsByC[FW]||[]).length){ const fw=el("button","map-fw"); fw.type='button';
      fw.innerHTML=`◆ Footprint-wide — ${potByC[FW]>0?'€'+potByC[FW].toFixed(1)+'m · ':'value unscoped · '}${(itemsByC[FW]||[]).length} opportunities (not on the map)`;
      fw.addEventListener('click',()=>pick(FW)); card.appendChild(fw); }
    const _u=unscopedStrip(); if(_u) card.appendChild(_u);
    card.appendChild(reveal);
    card.appendChild(chartSource("Printec research agents."));
    drawBars();

    const tip=mapBox.querySelector('.map-tip'), wrap=mapBox.querySelector('.map-wrap');
    mapBox.querySelectorAll('.fmap-c').forEach(p=>{ const code=p.dataset.code, v=potByC[code]||0, n=(itemsByC[code]||[]).length;
      p.addEventListener('mousemove',e=>{ const r=wrap.getBoundingClientRect();
        tip.innerHTML=`<b>${esc(cname(code))}</b><br>${v>0?('€'+v.toFixed(1)+'m · '+n+' opportunit'+(n===1?'y':'ies')):(n?(n+' opportunit'+(n===1?'y':'ies')+' · value not yet scoped'):'no current opportunity')}`;
        tip.style.left=(e.clientX-r.left)+'px'; tip.style.top=(e.clientY-r.top)+'px'; tip.hidden=false; });
      p.addEventListener('mouseleave',()=>{ tip.hidden=true; });
      if(v>0||n) p.addEventListener('click',()=>pick(code)); });
  })();

  // potential opportunity value by PRODUCT — the headline cut of the Products tab (all markets, no filter):
  // same objective deal-size scale, summed per Printec solution (a signal counts for every solution it touches).
  (function(){
    const sigs=(DASH.signals||[]).filter(isOpportunity);
    const liveIds=DASH.products.filter(p=>p.n_signals>0).map(p=>p.id);
    const rows=liveIds.map(id=>{ const items=sigs.filter(g=>(g.products||[]).includes(id));
      return {id,label:DASH.prod_label[id]||id,items,v:items.reduce((a,g)=>a+potEur(g.size_band),0)}; })
      .filter(r=>r.v>0).sort((a,b)=>b.v-a.v);
    if(!rows.length) return;
    const distinct=sigs.reduce((a,g)=>a+potEur(g.size_band),0);
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Opportunity value by product</h2><div class="desc">Every <b>open opportunity that can be bid for</b>, sized by its deal band, for each Printec solution. <b>Click a bar</b> to see the deals behind it. Most deals fund several solutions and are counted under each, so the bars <b>do not add up</b> — the whole pipeline is <b>€${distinct.toFixed(1)}m across ${sigs.length} distinct opportunities</b>. Per-market detail is on the <b>Products</b> tab.</div></div></div>
      <div class="chart-panel"><div class="chartbox tall"><canvas id="ovProd"></canvas></div></div>`;
    s.appendChild(card);
    const reveal=el("div","reveal"); card.appendChild(reveal);
    let cur=-1;
    mkBar("ovProd",rows.map(r=>r.label),rows.map(r=>+r.v.toFixed(1)),rows.map(r=>PCOL[r.id]||'#23C0E2'),"Potential value (€m)",true,rows.map(r=>r.label),
      i=>{ if(i===cur){ cur=-1; reveal.innerHTML=''; return; } cur=i; fillSignalReveal(reveal, rows[i].label, rows[i].items, true); });
    card.appendChild(chartSource("Printec research agents."));
  })();

  // competition & partners — a plain-English read of this week's moves (newspaper, not a data table). Prefers
  // an authored brief (DASH.competition_brief, prose from the weekly Orchestrator) and otherwise synthesises a
  // short lead + the sharpest headline moves from the competitor watchlist. Full detail is on the Competition tab.
  (function(){
    const comps=DASH.competitors||[];
    if(!comps.length) return;
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Competitor and partner moves this week</h2><div class="desc">The most important competitor and partner moves this week. The full picture, financials and the market-by-market pressure matrix are on the <b>Competition</b> tab.</div></div></div>`;
    const brief=DASH.competition_brief;
    if(brief && String(brief).trim()){
      const body=el("div","news"); body.innerHTML=mdToHtml(String(brief));
      card.appendChild(body);
      card.appendChild(el("div","small muted evsrc",`Distilled by the weekly Orchestrator from the competitors &amp; partners findings — see the Competition tab for the full landscape.`));
    } else {
      const TH={High:3,Medium:2,Low:1};
      const cty=v=>(v.countries||[]).map(c=>DASH.code2name[c]||c).join(', ')||'footprint-wide';
      const partner=comps.find(v=>v.role==='both'||v.role==='partner');
      const rivals=comps.filter(v=>['competitor','both','oem'].includes(v.role))
        .sort((a,b)=>(TH[b.threat]||0)-(TH[a.threat]||0)||(b.n_mentions||0)-(a.n_mentions||0));
      const active=rivals.filter(v=>v.n_mentions>0);
      const top=(active.length?active:rivals).filter(v=>v!==partner).slice(0,4);
      const nHigh=rivals.filter(v=>v.threat==='High').length;
      let html=`<div class="bv-lead">Printec competes with <span class="lead-emph">${rivals.length} tracked rivals</span> across the footprint, <span class="lead-emph">${nHigh} of them high-threat</span>. This is what changed this week.</div>`;
      if(partner) html+=`<div class="note amber" style="margin-top:13px"><b>Partner watch — ${esc(partner.name)}:</b> ${linkify(firstMove(partner.latest))}</div>`;
      if(top.length){
        html+=`<div class="news-sub">The sharpest competitor moves</div>`;
        html+=`<ul class="bv-list">`+top.map(v=>`<li><b>${esc(v.name)}</b> <span class="muted small">(${esc(v.threat)} threat · ${esc(cty(v))})</span> — ${linkify(firstMove(v.latest))}</li>`).join('')+`</ul>`;
      }
      html+=`<div class="small muted evsrc">From the ${comps.length}-name competitor &amp; partner watchlist; one headline move per name. See the Competition tab for the full picture.</div>`;
      const wrap=el("div"); wrap.innerHTML=html; card.appendChild(wrap);
    }
    s.appendChild(card);
  })();

  const opsTitle = isMonth ? `Top opportunities — ${esc(view.monthInfo.label)}`
                 : view.mode==='week' ? `Top opportunities — week of ${esc(view.week)}`
                 : 'Top opportunities this week';
  const opps=(DASH.signals||[]).filter(isOpportunity);   // current + biddable only (standing/threats excluded)
  const byRecent=(a,b)=> (String(sortDate(b)).localeCompare(String(sortDate(a)))) || (potEur(b.size_band)-potEur(a.size_band));
  const byValue =(a,b)=> (potEur(b.size_band)-potEur(a.size_band)) || (String(sortDate(b)).localeCompare(String(sortDate(a))));
  const mode=(opRank==='value')?'value':'recent';
  // Overview shows the top 10 only (09/09/2026); All signals carries the full list with filters
  const TOP_N=10;
  const sorted=opps.slice().sort(mode==='value'?byValue:byRecent);
  const ranked=sorted.slice(0,TOP_N);
  const more=sorted.length-ranked.length;
  const opsDesc = (mode==='value'
    ? 'The 10 biggest <b>current, biddable</b> opportunities by deal size (€).'
    : 'The 10 <b>freshest</b> opportunities this week, newest development on top. Click any card for the evidence and the date it broke.')
    + (more>0 ? ` The other ${more} are on the <b>All signals</b> tab.` : '');
  const ops=el("div","card");
  ops.innerHTML=`<div class="hd"><div><h2>${opsTitle}</h2><div class="desc">${opsDesc}</div></div><div class="seg"><button class="${mode==='recent'?'on':''}" data-r="recent" title="Newest triggering development first">Most recent</button><button class="${mode==='value'?'on':''}" data-r="value" title="Largest indicative deal size first">Largest €</button></div></div>`;
  if(!ranked.length) ops.innerHTML+=`<div class="desc" style="padding:8px 2px">No fresh biddable opportunities this week — see standing positions and threats under Competition &amp; Patterns.</div>`;
  ranked.forEach(g=>ops.appendChild(sigCard(g)));
  if(more>0) ops.appendChild(el("div","small muted ops-more",
    `Showing the top ${ranked.length} of ${sorted.length}. See <b>All signals</b> for the rest, with filters by market, product and confidence.`));
  s.appendChild(ops);
  ops.querySelectorAll('.seg button').forEach(b=>b.addEventListener('click',()=>{ opRank=b.dataset.r; renderOverview(s); }));

  // Overview ends at the top opportunities (09/09/2026). Positions already held, deals competitors
  // won and the indirect opportunities are all still in the data and on their own tabs — All signals
  // carries every one of them, with a lane filter — so repeating them here only lengthened the page.
}

/* ---- structural data FUSION ----------------------------------------------------------------
   Merge the ECB/HBA series (DASH.series, keyed by country name) and the licensed RBR ATM reports
   (DASH.rbr_series, keyed by code) into ONE per-country, per-canonical-metric structure carrying
   recorded + projected points. RBR's ~200 inconsistent metric names are canonicalised, and each
   metric's historical/forecast variants are merged. Crucially we pick ONE source per (country,
   metric) — never splice ECB and RBR point-by-point (they measure differently) — so every line is
   internally consistent: RBR wins where it has the forecast + long history; ECB covers Greece and
   POS (RBR has no Greece, no POS). Cached; invalidated when the week changes (applyAndRender). */
let _fused=null;
function buildFused(){
  if(_fused) return _fused;
  const c2n=DASH.code2name||{}, n2c={}; Object.keys(c2n).forEach(c=>{ n2c[c2n[c]]=c; });
  const SYN=[
    [/^atm installed base\b(?!.*(location|manufacturer|long historical))/i,'atms','ATMs (installed base)'],
    [/^bank branches\b/i,'branches','Bank branches'],
    [/(number of (atm )?cash withdrawals|cash withdrawals[ ,\-]+annual number|annual number of cash withdrawals|cash withdrawals \(annual number)/i,'cash_num','Cash withdrawals (annual number)'],
    [/annual value of (atm )?cash withdrawals|cash withdrawals[ ,\-]+annual value|value of (atm )?cash withdrawals/i,'cash_val','Cash withdrawals (annual value)'],
    [/average (number of )?cash withdrawals per atm/i,'cash_per_atm','Cash withdrawals per ATM / month'],
    [/average value (of (a )?cash withdrawal|per (atm )?cash withdrawal|per cash withdrawal)/i,'cash_avg','Average value per withdrawal'],
    [/average value withdrawn per atm/i,'cash_val_per_atm','Average value withdrawn per ATM'],
    [/recycl/i,'recyclers','Cash recyclers (note-recycling ATMs)'],
    [/automated note[ \-]?deposit/i,'deposit','Deposit-automation ATMs'],
    [/stand-?alone (deposit )?terminals|standalone terminals/i,'sats','Stand-alone deposit terminals (SATs)'],
    [/atm shipments/i,'shipments','ATM shipments (forecast)'],
    [/per million people/i,'density','ATMs per million people'],
    [/per 100 bank branches/i,'per100br','ATMs per 100 bank branches'],
    [/\biad|independently deployed|of which iads/i,'iad','IAD-deployed ATMs'],
    [/by manufacturer|manufacturer installed base/i,'by_mfr','ATMs by manufacturer'],
    [/by location|off-site|through-the-wall|\blobby\b|\bhall\b|drive-through|branch-based/i,'by_loc','ATMs by location'],
    [/domestic (atm )?sharing|shared-network|connected atms/i,'sharing','Domestic ATM sharing'],
    [/withdrawal value as.*proportion of gdp/i,'cash_gdp','Cash withdrawals as % of GDP'],
    [/nfc cash withdrawal/i,'nfc','ATMs with NFC withdrawal'],
    [/as % of all atm transactions|as a share of atm transactions/i,'cash_share','Cash withdrawals as % of ATM transactions'],
    [/annual growth rate/i,'growth','ATM annual growth rate']
  ];
  const canon=name=>{ const isFc=/\bforecast\b/i.test(name)&&!/historical/i.test(name);
    for(let i=0;i<SYN.length;i++){ if(SYN[i][0].test(name)) return {key:SYN[i][1],display:SYN[i][2],isFc}; }
    let c=String(name).replace(/[,(\- ]*\b(forecast|historical)\b[ .)\-]*/ig,' ').replace(/,?\s*\d{4}(-\d{4})?/g,' ').replace(/\(total\)|\(year-end\)|\(number of atms\)|\(atms in service at year-end\)/ig,' ').replace(/[()]/g,' ').replace(/\s{2,}/g,' ').replace(/[\s,;:\-]+$/,'').trim();
    return {key:'g:'+c.toLowerCase(),display:c,isFc}; };
  const ECBM={atms:'ATMs (installed base)',pos:'POS terminals',branches:'Bank branches',cash:'Cash withdrawals (annual number)'};
  const ECBK={atms:'atms',pos:'pos',branches:'branches',cash:'cash_num'};
  const cand={};
  const put=(code,key,disp,src,year,val,fc)=>{ if(val==null||!isFinite(val))return; (cand[code]=cand[code]||{}); const m=(cand[code][key]=cand[code][key]||{}); const o=(m[src]=m[src]||{rec:{},proj:{},display:disp}); (fc?o.proj:o.rec)[year]=val; };
  const ser=DASH.series||{};
  Object.keys(ser).forEach(nm=>{ const code=n2c[nm]; if(!code) return; const o=ser[nm];
    Object.keys(ECBK).forEach(ek=>{ (o[ek]||[]).forEach(p=>put(code,ECBK[ek],ECBM[ek],'ECB',p.year,p.value,!!p.provisional)); }); });
  const rbr=DASH.rbr_series||{};
  Object.keys(rbr).forEach(code=>{ (rbr[code].series||[]).forEach(sx=>{ const cm=canon(sx.metric);
    (sx.points||[]).forEach(p=>put(code,cm.key,cm.display,'RBR',p.year,p.value, cm.isFc||!!p.provisional)); }); });
  const byCode={}, metrics={};
  Object.keys(cand).forEach(code=>{ byCode[code]={};
    Object.keys(cand[code]).forEach(key=>{ const srcs=cand[code][key];
      const opts=Object.keys(srcs).map(src=>({src,rec:srcs[src].rec,proj:srcs[src].proj,display:srcs[src].display}));
      opts.sort((a,b)=>((Object.keys(b.proj).length>0)-(Object.keys(a.proj).length>0))||((Object.keys(b.rec).length+Object.keys(b.proj).length)-(Object.keys(a.rec).length+Object.keys(a.proj).length)));
      const best=opts[0];
      const rec=Object.keys(best.rec).map(Number).sort((a,b)=>a-b).map(y=>({year:y,value:best.rec[y]}));
      const proj=Object.keys(best.proj).map(Number).filter(y=>!(y in best.rec)).sort((a,b)=>a-b).map(y=>({year:y,value:best.proj[y]}));
      byCode[code][key]={display:best.display,rec,proj,src:best.src};
      const mm=metrics[key]=metrics[key]||{key,display:best.display,codes:[],proj:0}; mm.codes.push(code); if(proj.length) mm.proj++;
    }); });
  const order=['atms','branches','pos'].concat(SYN.map(s=>s[1]).filter(k=>k!=='atms'&&k!=='branches'));   // pos is ECB-only (not in SYN); keep it among the core structural metrics
  const list=Object.keys(metrics).map(k=>metrics[k]).sort((a,b)=>{
    const ag=a.key.indexOf('g:')===0, bg=b.key.indexOf('g:')===0;
    if(ag!==bg) return ag?1:-1;
    if(!ag) return order.indexOf(a.key)-order.indexOf(b.key);
    return b.codes.length-a.codes.length; });
  _fused={byCode, metrics:list};
  return _fused;
}
// one fused metric, one line per selected market: recorded solid + projection dashed (◇), anchored to the last actual.
function drawFusedMetric(id, codes, metricKey, index){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  const F=index||buildFused(), pal=['#23C0E2','#E2715E','#7FB069','#E0B83A','#6FA8D6','#BFA7E6','#9C4A36','#553897','#27506F','#3D5A1C'];
  const empty=msg=>{ const p=ctx.closest('.chart-panel'); if(p) p.innerHTML='<div class="empty">'+msg+'</div>'; };
  if(!codes.length){ empty('Pick at least one market.'); return; }
  const series=codes.map(code=>({code,m:(F.byCode[code]||{})[metricKey]})).filter(x=>x.m && (x.m.rec.length||x.m.proj.length));
  if(!series.length){ empty('No data for this metric in the selected markets.'); return; }
  const yset=new Set(); series.forEach(x=>{ x.m.rec.forEach(p=>yset.add(p.year)); x.m.proj.forEach(p=>yset.add(p.year)); });
  const years=[...yset].sort((a,b)=>a-b);
  const ds=[];
  series.forEach((x,i)=>{ const col=pal[i%pal.length], nm=DASH.code2name[x.code]||x.code;
    const recBy={}; x.m.rec.forEach(p=>recBy[p.year]=p.value);
    const projBy={}; x.m.proj.forEach(p=>projBy[p.year]=p.value);
    const lastRec=x.m.rec.length?x.m.rec[x.m.rec.length-1]:null;
    if(x.m.rec.length) ds.push({label:nm,borderColor:col,backgroundColor:col+'22',borderWidth:2.2,tension:.25,fill:false,spanGaps:true,pointRadius:2.4,pointBackgroundColor:col,
      data:years.map(y=> y in recBy?recBy[y]:null)});
    if(x.m.proj.length) ds.push({label: x.m.rec.length? nm+' (proj)' : nm, borderColor:col,backgroundColor:'transparent',borderWidth:2,borderDash:[6,4],tension:.25,fill:false,spanGaps:true,
      pointStyle:'rectRot',pointRadius:years.map(y=> y in projBy?4.5:0),pointBackgroundColor:col,
      data:years.map(y=> (lastRec&&y===lastRec.year)?lastRec.value : (y in projBy?projBy[y]:null))});
  });
  const disp=series[0].m.display||metricKey;
  charts.push(new Chart(ctx,{type:'line',data:{labels:years,datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},
      plugins:{title:{display:true,text:disp+' — by market',color:'#16130D',font:{family:chartFont(),size:14,weight:'700'},padding:{bottom:2}},
        subtitle:{display:true,text:'solid = recorded · ◇ dashed = projection',color:'#928B7B',font:{family:chartFont(),size:10},padding:{bottom:10}},
        legend:{position:'bottom',labels:{color:'#5F594C',font:{family:chartFont(),weight:'600',size:11},usePointStyle:true,boxWidth:8,padding:9,filter:it=>!/ \(proj\)$/.test(it.text)}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},callbacks:{label:it=>` ${it.dataset.label}: ${fmtNum(it.raw)}`}}},
      scales:{x:{title:{display:true,text:'Year',color:'#5F594C',font:{family:chartFont(),size:11,weight:'600'}},ticks:{color:'#928B7B',font:{family:chartFont()}},grid:{color:'#EFE7D6'},border:{display:false}},
              y:{ticks:{color:'#928B7B',font:{family:chartFont()},callback:v=>fmtNum(v)},grid:{color:'#EFE7D6'},border:{display:false}}}}}));
}
// reusable section over the fused data. Market selection is either multi-market chips (select/clear all) or —
// when opts.singleMarket — a single-country dropdown (one market at a time), matching the Products ATM chart.
// The metric dropdown ("the other parameters") is identical in both modes.
function fusedChartSection(s, opts){
  const ALL=opts.index||buildFused();
  const metrics=opts.metricKeys?ALL.metrics.filter(m=>opts.metricKeys.indexOf(m.key)>=0):ALL.metrics;
  const F={byCode:ALL.byCode, metrics}; if(!F.metrics.length) return;
  const id=opts.id;
  let metricKey=F.metrics.some(m=>m.key===opts.defaultMetric)?opts.defaultMetric:F.metrics[0].key;
  const PREF=['GR','RO','BG','HU','CZ','SK','HR','SI','CY','RS','UA','AL','BA','MK','ME','XK'];
  const orderCodes=cs=>PREF.filter(c=>cs.includes(c)).concat(cs.filter(c=>!PREF.includes(c)).sort());
  const codesFor=()=>{ const m=F.metrics.find(x=>x.key===metricKey); return orderCodes((m?m.codes:[]).slice()); };
  const card=el("div","card");
  card.innerHTML=`<div class="hd"><div><h2>${esc(opts.title)}</h2><div class="desc">${opts.desc}</div></div></div>`;
  const ctrl=el("div","trendctrl");
  const mkCanvas=()=>{ const cw=el("div","chart-panel"); cw.innerHTML=`<div class="chartbox xtall"><canvas id="${id}"></canvas></div>`; return cw; };
  const killChart=()=>{ const ex=window.Chart&&Chart.getChart(id); if(ex){const i=charts.indexOf(ex);if(i>=0)charts.splice(i,1);ex.destroy();} };

  if(opts.singleMarket){
    // Metric + single-country "Market" dropdowns — one market at a time (Products ATM-chart UX)
    const flt=el("div","tablefilters");
    flt.innerHTML=`<label>Metric <select class="fus-m"></select></label><label>Market <select class="fus-c"></select></label>`;
    const msel=flt.querySelector('.fus-m'), csel=flt.querySelector('.fus-c');
    F.metrics.forEach(m=>{ const o=document.createElement('option'); o.value=m.key; o.textContent=m.display+(m.proj?' ◇':''); if(m.key===metricKey)o.selected=true; msel.appendChild(o); });
    let cur=codesFor()[0];
    const fillC=()=>{ const codes=codesFor(); if(codes.indexOf(cur)<0) cur=codes[0];
      csel.innerHTML=codes.map(c=>`<option value="${c}"${c===cur?' selected':''}>${esc(DASH.code2name[c]||c)}</option>`).join(''); };
    ctrl.appendChild(flt); card.appendChild(ctrl);
    const cw=mkCanvas(); card.appendChild(cw);
    // source caption — per-metric when srcByMetric is given (different metrics come from different sources), else static
    const srcCap = (opts.srcByMetric||opts.srcText) ? chartSource("") : null;
    if(srcCap) card.appendChild(srcCap);
    const setSrc=()=>{ if(!srcCap) return; const t = opts.srcByMetric ? (opts.srcByMetric[metricKey]||opts.srcByMetric._default||"") : opts.srcText; srcCap.textContent = "Source: "+t; };
    s.appendChild(card);
    const draw=()=>{ drawFusedMetric(id, cur?[cur]:[], metricKey, F); setSrc(); };
    const redraw=()=>{ killChart(); if(!document.getElementById(id)) cw.innerHTML=`<div class="chartbox xtall"><canvas id="${id}"></canvas></div>`; draw(); };
    msel.addEventListener('change',()=>{ metricKey=msel.value; fillC(); redraw(); });
    csel.addEventListener('change',()=>{ cur=csel.value; redraw(); });
    fillC(); draw();
    return;
  }

  // metric dropdown + multi-market chips (select/clear all)
  let codes=codesFor(); const sel=new Set(codes);
  const mwrap=el("div","tablefilters"); mwrap.innerHTML=`<label>Metric <select class="fus-m"></select></label>`;
  const msel=mwrap.querySelector('select');
  F.metrics.forEach(m=>{ const o=document.createElement('option'); o.value=m.key; o.textContent=m.display+(m.proj?' ◇':''); if(m.key===metricKey)o.selected=true; msel.appendChild(o); });
  const crow=el("div","cchips"); const allBtn=el("button","cchip alltoggle");
  ctrl.appendChild(mwrap); ctrl.appendChild(crow); card.appendChild(ctrl);
  const cw=mkCanvas(); card.appendChild(cw); s.appendChild(card);
  const draw=()=>drawFusedMetric(id, codes.filter(c=>sel.has(c)), metricKey, F);
  const redraw=()=>{ killChart(); if(!document.getElementById(id)) cw.innerHTML=`<div class="chartbox xtall"><canvas id="${id}"></canvas></div>`; draw(); };
  const syncAll=()=>{ allBtn.textContent=(sel.size===codes.length?'Clear all':'Select all'); };
  const chips=()=>{ crow.innerHTML=''; crow.appendChild(allBtn);
    codes=codesFor(); [...sel].forEach(c=>{ if(codes.indexOf(c)<0) sel.delete(c); }); if(!sel.size) codes.forEach(c=>sel.add(c));
    syncAll();
    codes.forEach(c=>{ const b=el("button","cchip"+(sel.has(c)?" on":"")); b.textContent=DASH.code2name[c]||c; b.dataset.c=c;
      b.addEventListener('click',()=>{ if(sel.has(c))sel.delete(c); else sel.add(c); b.classList.toggle('on'); syncAll(); redraw(); }); crow.appendChild(b); }); };
  allBtn.addEventListener('click',()=>{ if(sel.size===codes.length) sel.clear(); else codes.forEach(c=>sel.add(c)); crow.querySelectorAll('.cchip[data-c]').forEach(x=>x.classList.toggle('on',sel.has(x.dataset.c))); syncAll(); redraw(); });
  msel.addEventListener('change',()=>{ metricKey=msel.value; chips(); redraw(); });
  chips(); draw();
}

/* ---- RBR-derived ATM series: Total ATMs (incl. independent deployers) and the derived Bank-operated ATMs
   (= Total − IAD, the complement of RBR's "IAD-deployed ATMs"). RBR's decomposition is internally consistent
   (the splits sum to the total), so the bank line is exact for measured years; for the forecast we carry the
   last measured IAD share forward. ONE source (RBR) feeds both metrics in BOTH charts → the numbers agree. */
function rbrAtmSeries(){
  const get=(code,metric)=>{ for(const sx of (DASH.atm_market||[])) if(sx.country===code && sx.metric===metric) return sx; return null; };
  const out={};
  (DASH.atm_market||[]).forEach(sx=>{ if(sx.metric!=='ATM installed base') return; const code=sx.country;
    const totH=(sx.history||[]).map(p=>({year:p.year,value:p.value})), totF=(sx.forecast||[]).map(p=>({year:p.year,value:p.value}));
    const iadH=((get(code,'IAD-deployed ATMs')||{}).history)||[];
    const iadAt=y=>{ const f=iadH.find(p=>p.year===y); return f?f.value:null; };
    const bankRec=totH.map(p=>{ const i=iadAt(p.year); return i!=null?{year:p.year,value:Math.round(p.value-i)}:null; }).filter(Boolean);
    let share=null; const lastH=totH[totH.length-1]; if(lastH){ const i=iadAt(lastH.year); if(i!=null&&lastH.value) share=i/lastH.value; }
    const bankProj=(share!=null)?totF.map(p=>({year:p.year,value:Math.round(p.value*(1-share))})):[];
    out[code]={ total:{rec:totH,proj:totF}, bank:{rec:bankRec,proj:bankProj} };
  });
  return out;
}
/* ---- Country structural index (Countries chart): ATMs from RBR (Total + derived Bank — the SAME data the
   Products tab uses, so the two pages agree), POS/branches/cash from the ECB Data Portal, plus ECB's own ATM
   count kept as a labelled CROSS-CHECK (not blended). Same {byCode, metrics} shape fusedChartSection wants. */
function countryStructIndex(){
  const ser=DASH.series||{}, c2n=DASH.code2name||{}, n2c={}; Object.keys(c2n).forEach(c=>{ n2c[c2n[c]]=c; });
  const rbr=rbrAtmSeries(), byCode={}, met={};
  const add=(code,key,disp,rec,proj)=>{ if(!(rec&&rec.length)&&!(proj&&proj.length))return; (byCode[code]=byCode[code]||{})[key]={display:disp,rec:rec||[],proj:proj||[]}; const m=met[key]=met[key]||{key,display:disp,codes:[],proj:0}; m.codes.push(code); if(proj&&proj.length)m.proj++; };
  Object.keys(rbr).forEach(code=>{ add(code,'atms','Total ATMs (incl. independent deployers) · RBR',rbr[code].total.rec,rbr[code].total.proj);
    add(code,'bank','Bank-operated ATMs (excl. independent deployers) · RBR',rbr[code].bank.rec,rbr[code].bank.proj); });
  Object.keys(ser).forEach(nm=>{ const code=n2c[nm]; if(!code) return; const o=ser[nm];
    add(code,'atms_ecb','ATMs, bank-reported · ECB (cross-check)',(o.atms||[]).map(p=>({year:p.year,value:p.value})),[]);
    add(code,'pos','POS terminals · ECB',(o.pos||[]).map(p=>({year:p.year,value:p.value})),[]);
    add(code,'branches','Bank branches · ECB',(o.branches||[]).map(p=>({year:p.year,value:p.value})),[]);
    add(code,'cash','Card cash withdrawals (millions, per half-year) · ECB',(o.cash||[]).map(p=>({year:p.year,value:p.value})),[]); });
  return {byCode, metrics:['atms','bank','atms_ecb','pos','branches','cash'].map(k=>met[k]).filter(Boolean)};
}

/* ---- RBR ATM-market index from DASH.atm_market (deep-read extraction). Time-series metrics use the same
   {byCode, metrics} shape for the line chart; snapshot metrics are read via atmLatest() for the bar/stack cards. */
let _atm=null;
function atmIndex(){
  if(_atm) return _atm;
  const byCode={}, met={};
  (DASH.atm_market||[]).forEach(sx=>{ const code=sx.country, k=sx.metric;
    byCode[code]=byCode[code]||{};
    byCode[code][k]={display:k, unit:sx.unit, rec:(sx.history||[]).map(p=>({year:p.year,value:p.value})), proj:(sx.forecast||[]).map(p=>({year:p.year,value:p.value}))};
    const ts=(sx.history||[]).length>=2 || (sx.forecast||[]).length>0;
    const m=met[k]=met[k]||{key:k,display:k,codes:[],proj:0,ts:false,unit:sx.unit};
    m.codes.push(code); if((sx.forecast||[]).length) m.proj++; if(ts) m.ts=true; });
  // relabel raw "ATM installed base" as the Total, and inject the derived Bank-operated series (Total − IAD)
  if(met['ATM installed base']) met['ATM installed base'].display='Total ATMs (incl. independent deployers)';
  Object.keys(byCode).forEach(c=>{ if(byCode[c]['ATM installed base']) byCode[c]['ATM installed base'].display='Total ATMs (incl. independent deployers)'; });
  const rbr=rbrAtmSeries();
  Object.keys(rbr).forEach(code=>{ const b=rbr[code].bank; if(!(b.rec.length||b.proj.length)) return;
    (byCode[code]=byCode[code]||{})['Bank-operated ATMs']={display:'Bank-operated ATMs (excl. independent deployers)',unit:'ATMs',rec:b.rec,proj:b.proj};
    const m=met['Bank-operated ATMs']=met['Bank-operated ATMs']||{key:'Bank-operated ATMs',display:'Bank-operated ATMs (excl. independent deployers)',codes:[],proj:0,ts:true,unit:'ATMs'}; m.codes.push(code); if(b.proj.length)m.proj++; });
  _atm={byCode, metrics:Object.keys(met).map(k=>met[k])};
  return _atm;
}
// latest reported value per country for a metric (history end, else forecast end) — for the snapshot bar/stacks
function atmLatest(metric){ const idx=atmIndex(), out={};
  Object.keys(idx.byCode).forEach(code=>{ const m=idx.byCode[code][metric]; if(!m) return;
    const last=m.rec.length?m.rec[m.rec.length-1]:(m.proj.length?m.proj[m.proj.length-1]:null); if(last) out[code]=last.value; });
  return out; }
const ATM_ORDER=['GR','RO','BG','HU','CZ','SK','HR','SI','CY','RS','UA','AL','BA','MK','ME','XK'];
// cross-country snapshot bar (latest year) with a metric dropdown — for density / recycling / branch benchmarks
function atmSnapshotSection(s, opts){
  const metrics=opts.metrics.filter(m=>atmIndex().metrics.some(x=>x.key===m.key));
  if(!metrics.length) return;
  let key=metrics.some(m=>m.key===opts.defaultKey)?opts.defaultKey:metrics[0].key;
  const card=el("div","card");
  card.innerHTML=`<div class="hd"><div><h2>${esc(opts.title)}</h2><div class="desc">${opts.desc}</div></div></div>`;
  const flt=el("div","tablefilters"); flt.innerHTML=`<label>Measure <select class="snm"></select></label>`;
  const sel=flt.querySelector('select');
  metrics.forEach(m=>{ const o=document.createElement('option'); o.value=m.key; o.textContent=m.label; if(m.key===key)o.selected=true; sel.appendChild(o); });
  card.appendChild(flt);
  const cw=el("div","chart-panel"); cw.innerHTML=`<div class="chartbox tall"><canvas id="${opts.id}"></canvas></div>`; card.appendChild(cw);
  if(opts.srcText) card.appendChild(chartSource(opts.srcText));
  s.appendChild(card);
  const draw=()=>{
    const m=metrics.find(x=>x.key===key), vals=atmLatest(key);
    const rows=Object.keys(vals).map(c=>({c,v:vals[c],name:DASH.code2name[c]||c})).filter(r=>isFinite(r.v)).sort((a,b)=>b.v-a.v);
    const ex=window.Chart&&Chart.getChart(opts.id); if(ex){const i=charts.indexOf(ex);if(i>=0)charts.splice(i,1);ex.destroy();}
    if(!document.getElementById(opts.id)) cw.innerHTML=`<div class="chartbox tall"><canvas id="${opts.id}"></canvas></div>`;
    if(!rows.length){ cw.innerHTML='<div class="empty">No data for this measure.</div>'; return; }
    const box=cw.querySelector('.chartbox'); if(box) box.style.height=Math.max(220,rows.length*26)+'px';
    mkBar(opts.id, rows.map(r=>r.name), rows.map(r=>+(+r.v).toFixed(2)), rows.map(()=>'#23C0E2'), (m&&m.label)||key, true, rows.map(r=>r.name));
  };
  sel.addEventListener('change',()=>{ key=sel.value; draw(); });
  draw();
}
// stacked horizontal bar of latest-year component metrics per country — for channel mix & vendor mix
function atmStackSection(s, opts){
  const idx=atmIndex();
  const codes=ATM_ORDER.filter(c=> idx.byCode[c] && opts.segments.some(seg=>idx.byCode[c][seg.metric]));
  const rows=codes.map(c=>{ const vals=opts.segments.map(seg=>{ const m=idx.byCode[c][seg.metric]; const last=m&&(m.rec.length?m.rec[m.rec.length-1]:(m.proj.length?m.proj[m.proj.length-1]:null)); return last?last.value:0; });
    return {c,name:DASH.code2name[c]||c,vals,total:vals.reduce((a,b)=>a+b,0)}; }).filter(r=>r.total>0).sort((a,b)=>b.total-a.total);
  if(!rows.length) return;
  const card=el("div","card"); card.innerHTML=`<div class="hd"><div><h2>${esc(opts.title)}</h2><div class="desc">${opts.desc}</div></div></div>`;
  const cw=el("div","chart-panel"); cw.innerHTML=`<div class="chartbox tall"><canvas id="${opts.id}"></canvas></div>`; card.appendChild(cw);
  if(opts.srcText) card.appendChild(chartSource(opts.srcText));
  s.appendChild(card);
  const box=cw.querySelector('.chartbox'); if(box) box.style.height=Math.max(240,rows.length*30)+'px';
  const ds=opts.segments.map((seg,si)=>({label:seg.label,color:seg.color,data:rows.map(r=>r.vals[si])}));
  mkStackBar(opts.id, rows.map(r=>r.name), ds, {horizontal:true, title:opts.title, subtitle:'latest reported year (2022)', tip:it=>` ${it.dataset.label}: ${fmtNum(it.raw)}`});
}
/* ---- UNIFIED MULTI-SOURCE metric (phase 1: Total ATMs from ECB + RBR) -----------------------------
   The same metric is counted by several sources that disagree (different method + year). Rather than pick
   one or hide the conflict, we plot EVERY source as its own line (solid = measured, dashed = forecast) and,
   across the sources the reader keeps ticked, draw a live AVERAGE + a shaded RANGE band (lowest–highest of
   the measured values). The source toggles are shared (`_unifSel`) so the metric reads the same everywhere.
   Phase 1 = ECB (DASH.series) + RBR (DASH.atm_market); national-bank/press points come in phase 2. */
function multiSourceAtms(){
  const c2n=DASH.code2name||{}, n2c={}; Object.keys(c2n).forEach(c=>{ n2c[c2n[c]]=c; });
  const by={};
  const ser=DASH.series||{};                                  // ECB Payment Statistics — measured, official
  Object.keys(ser).forEach(nm=>{ const code=n2c[nm], pts=(ser[nm]||{}).atms||[]; if(!code||!pts.length) return;
    (by[code]=by[code]||[]).push({src:'ECB Payment Statistics', short:'ECB', tier:1, rec:pts.map(p=>({year:p.year,value:p.value})), proj:[]}); });
  (DASH.atm_market||[]).forEach(sx=>{ if(sx.metric!=='ATM installed base') return; const code=sx.country;  // RBR — measured history + forecast
    (by[code]=by[code]||[]).push({src:'RBR ATM Market 2028', short:'RBR', tier:2,
      rec:(sx.history||[]).map(p=>({year:p.year,value:p.value})), proj:(sx.forecast||[]).map(p=>({year:p.year,value:p.value}))}); });
  const extra=window.ATM_EXTRA_SOURCES||{};                   // World Bank / IMF FAS (+ later national-bank/press), from atm-sources.js
  Object.keys(extra).forEach(code=>{ (extra[code]||[]).forEach(s=>{ if(!(s.rec&&s.rec.length)&&!(s.proj&&s.proj.length)) return;
    (by[code]=by[code]||[]).push({src:s.src, short:s.short, tier:s.tier||1, url:s.url, rec:s.rec||[], proj:s.proj||[]}); }); });
  const order=['GR','RO','BG','HU','CZ','SK','HR','SI','CY','RS','UA','AL','BA','MK','ME','XK'];
  const codes=order.filter(c=>by[c]&&by[c].length).concat(Object.keys(by).filter(c=>!order.includes(c)));
  return {byCode:by, codes};
}
// source-line palette = the "Demand under deadline" product bars; ONE solid, full-colour line per source.
const UNIF_COL={ECB:'#8FB7E6', RBR:'#F0B073', WB:'#A6C47C', NAT:'#EE9BB0', BNR:'#76C7BE', Press:'#C3A6E8'};
const unifColOf=s=>UNIF_COL[s]||'#A7B0C0';
function drawUnifiedAtm(canvasId, sources){
  const ex=window.Chart&&Chart.getChart(canvasId); if(ex){const i=charts.indexOf(ex);if(i>=0)charts.splice(i,1);ex.destroy();}
  const ctx=document.getElementById(canvasId); if(!ctx||!window.Chart) return;
  const yset=new Set(); sources.forEach(s=>{ s.rec.forEach(p=>yset.add(p.year)); s.proj.forEach(p=>yset.add(p.year)); });
  const years=[...yset].sort((a,b)=>a-b);
  const recAt=(s,y)=>{ const f=s.rec.find(p=>p.year===y); return f?f.value:null; };
  const projAt=(s,y)=>{ const f=s.proj.find(p=>p.year===y); return f?f.value:null; };
  const ds=[];
  sources.forEach(s=>{ const col=unifColOf(s.short);   // one solid, full-colour line per source (measured), dashed continuation = forecast
    ds.push({label:s.src, data:years.map(y=>recAt(s,y)), borderColor:col, backgroundColor:col, borderWidth:2.4, pointRadius:2.2, pointHoverRadius:4, tension:.3, spanGaps:true});
    if(s.proj.length){ const lr=s.rec.length?s.rec[s.rec.length-1]:null;
      ds.push({label:s.src+' — forecast', data:years.map(y=>(lr&&y===lr.year)?lr.value:projAt(s,y)), borderColor:col, backgroundColor:col, borderWidth:2, borderDash:[5,4], pointRadius:1.8, tension:.3, spanGaps:true}); }
  });
  const chart=new Chart(ctx,{type:'line', data:{labels:years, datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},
      plugins:{
        subtitle:{display:true,text:'solid = measured · dashed = forecast to 2028',color:'#928B7B',font:{family:chartFont(),size:10},padding:{bottom:8}},
        legend:{position:'bottom',labels:{color:'#5F594C',font:{family:chartFont(),weight:'600',size:11},usePointStyle:true,boxWidth:8,padding:9,filter:it=>!/ — forecast$/.test(it.text)}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},callbacks:{label:it=>` ${it.dataset.label}: ${fmtNum(it.raw)}`}}},
      scales:{x:{ticks:{color:'#928B7B',font:{family:chartFont()}},grid:{color:'#EFE7D6'},border:{display:false}},
              y:{ticks:{color:'#928B7B',font:{family:chartFont()},callback:v=>fmtNum(v)},grid:{color:'#EFE7D6'},border:{display:false}}}}});
  charts.push(chart);
}
function unifiedAtmSection(s){
  const ms=multiSourceAtms(); if(!ms.codes.length) return;
  if(!(window.__unifAtmCode && ms.codes.includes(window.__unifAtmCode))) window.__unifAtmCode = ms.codes.includes('GR')?'GR':ms.codes[0];
  const card=el("div","card");
  card.innerHTML=`<div class="hd"><div><h2>ATM numbers and forecast to 2028</h2><div class="desc">Sources count ATMs differently — mainly over whether machines run by non-banks are included — and coverage varies by country. Each coloured line is one source (solid = measured, dashed = forecast to 2028). The sources are named in the legend below the chart.</div></div></div>`;
  const flt=el("div","tablefilters"); flt.innerHTML=`<label>Market <select class="unifc"></select></label>`;
  const csel=flt.querySelector('select');
  ms.codes.forEach(c=>{ const o=document.createElement('option'); o.value=c; o.textContent=DASH.code2name[c]||c; if(c===window.__unifAtmCode)o.selected=true; csel.appendChild(o); });
  card.appendChild(flt);
  const cw=el("div","chart-panel"); cw.innerHTML=`<div class="chartbox xtall"><canvas id="unifAtm"></canvas></div>`; card.appendChild(cw);
  // dynamic source caption — names the selected country and exactly which sources are plotted for it (updates on change)
  const srcCap=chartSource(""); card.appendChild(srcCap);
  const setSrc=()=>{ const list=ms.byCode[window.__unifAtmCode]||[];
    const names=[...new Set(list.map(x=>x.src))].join(', ');
    const cn=DASH.code2name[window.__unifAtmCode]||window.__unifAtmCode;
    srcCap.textContent=`Source — ${cn}: ${names||'no sources'}. Each line is one source plotted on its own (not blended); solid = measured, dashed = forecast to 2028.`; };
  s.appendChild(card);
  const redraw=()=>{ if(!document.getElementById('unifAtm')) cw.innerHTML=`<div class="chartbox xtall"><canvas id="unifAtm"></canvas></div>`; drawUnifiedAtm('unifAtm', ms.byCode[window.__unifAtmCode]||[]); setSrc(); };
  csel.addEventListener('change',()=>{ window.__unifAtmCode=csel.value; redraw(); });
  redraw();
}
// the dedicated ATM-market section (Products page) — fed by the deep-read RBR dataset (DASH.atm_market)
function renderAtmSection(s){
  unifiedAtmSection(s);   // multi-source, weighted ATMs chart (per country) leads the section
  if(!(DASH.atm_market||[]).length) return;
  atmSnapshotSection(s,{ id:'atmBench', defaultKey:'ATMs per million people',
    srcText:'RBR ATM Market 2028 (licensed) — 2022 figures.',
    title:'ATM market — cross-country benchmark (2022)',
    desc:'Where each market sits on the key ATM-market measures (latest reported year). Pick a measure to re-rank the footprint.',
    metrics:[
      {key:'ATMs per million people', label:'ATMs per million people'},
      {key:'ATMs per 100 bank branches', label:'ATMs per 100 bank branches'},
      {key:'ATMs per USD bn GDP', label:'ATMs per USD bn GDP'},
      {key:'Cash recyclers — % of base', label:'Cash recyclers (% of ATMs)'},
      {key:'Automated note-deposit — % of base', label:'Deposit-automation (% of ATMs)'},
      {key:'ATM installed base', label:'ATM installed base (2022)'},
      {key:'Bank branches', label:'Bank branches (2022)'} ]});
  atmStackSection(s,{ id:'atmLoc', title:'ATM channel mix by market (2022)',
    srcText:'RBR ATM Market 2028 (licensed) — 2022 channel breakdown.',
    desc:'Where each market’s ATMs sit — off-site vs branch-based (through-the-wall / lobby / hall). The off-site shift drives independent-deployer and managed-services demand.',
    segments:[
      {metric:'ATMs: off-site', label:'Off-site', color:'#23C0E2'},
      {metric:'ATMs: through-the-wall', label:'Through-the-wall', color:'#6FA8D6'},
      {metric:'ATMs: lobby', label:'Lobby', color:'#7FB069'},
      {metric:'ATMs: hall', label:'Hall', color:'#E0B83A'},
      {metric:'ATMs: branch-based', label:'Branch-based', color:'#BFA7E6'} ]});
  atmStackSection(s,{ id:'atmVendor', title:'ATM installed base by manufacturer (2022)',
    srcText:'RBR ATM Market 2028 (licensed) — 2022 vendor installed base.',
    desc:'Who supplies the installed fleet in each market — NCR/Atleos (Printec’s partner) vs Diebold Nixdorf and the rest.',
    segments:[
      {metric:'ATM installed base — NCR/Atleos', label:'NCR / Atleos', color:'#23C0E2'},
      {metric:'ATM installed base — Diebold Nixdorf', label:'Diebold Nixdorf', color:'#E2715E'},
      {metric:'ATM installed base — GRG', label:'GRG', color:'#7FB069'},
      {metric:'ATM installed base — KEBA', label:'KEBA', color:'#E0B83A'},
      {metric:'ATM installed base — Hyosung', label:'Hyosung', color:'#BFA7E6'},
      {metric:'ATM installed base — other vendors', label:'Other vendors', color:'#A7B0C0'} ]});
}

/* ----------------------------------------------------------------- COUNTRY */
// The market-detail table mixes two kinds of cell: the scripted ECB line ("7,421 ◇ 2025, +18.5% y/y (ECB)")
// and the statistics agent's hand-written paragraph for the non-EU markets. The table shows every cell
// in the short shape — the first clause, cut at a dash, semicolon or sentence end — and the expanded row
// carries the full text (asked 10/09/2026). Nothing is dropped, only moved.
const CELL_MAX=110, CELL_MIN=40;
function cellPlain(t){ return String(t||'').replace(/\[([^\]]+)\]\([^)]*\)/g,'$1').replace(/[*_`]+/g,'').trim(); }
function cellCut(t){
  const p=cellPlain(t); if(p.length<=CELL_MAX) return null;
  const marks=[]; const re=/( — | – | - |; |\. (?=[A-Z0-9]))/g; let m;
  while((m=re.exec(p))) marks.push(m.index);
  const inWin=marks.filter(i=>i>=CELL_MIN&&i<=CELL_MAX);
  let cut=inWin.length?inWin[0]:(marks.filter(i=>i<=CELL_MAX).pop()||-1);
  if(cut<CELL_MIN){ cut=p.lastIndexOf(' ',CELL_MAX); if(cut<CELL_MIN) cut=CELL_MAX; }
  // never end inside a bracket: step back to before the bracket that was left open
  let head=p.slice(0,cut);
  while((head.match(/\(/g)||[]).length>(head.match(/\)/g)||[]).length){ const k=head.lastIndexOf('('); if(k<CELL_MIN/2) break; head=head.slice(0,k); }
  return head.replace(/[\s,;:—–-]+$/,'');
}
function isTrimmed(t){ return cellCut(t)!==null; }
function shortCell(t){
  if(!t) return '—';
  const cut=cellCut(t);
  if(cut===null) return linkify(t);
  return '<span title="'+esc(cellPlain(t))+'">'+esc(cut)+'\u2026</span>';
}

/* ----------------------------------------------------------------- BUDGET 2026 (11/09/2026)
   The group budget (target revenue, revenue profit, margin) by market and product line, joined by
   budget_actions.py with the dashboard's own evidence. This tab only lays the join out: the numbers,
   the action each cell was given and the reasons the script recorded. Nothing is computed here. */
const BG_ACT={win:'Win',find:'Find',defend:'Defend','protect margin':'Protect margin','market risk':'Market risk',stretch:'Stretch',watch:'Watch'};
const bgCls=a=>'bg-'+String(a||'watch').replace(/\s+/g,'-');
const bgM=v=>'\u20ac'+(Number(v||0)/1e6).toFixed(1)+'m';
function bgPill(a){ return `<span class="bg-pill ${bgCls(a)}">${esc(BG_ACT[a]||a)}</span>`; }
function bgCellBody(x, sigByKey){
  const w=el("div","bg-body");
  const nums=`<div class="bg-nums">
      <div><span class="k">Target</span><b>${bgM(x.target)}</b></div>
      <div><span class="k">New (hardware + software)</span><b>${bgM(x.new)}</b></div>
      <div><span class="k">Recurring (services + outsourcing)</span><b>${bgM(x.recurring)}</b></div>
      <div><span class="k">Revenue profit</span><b>${bgM(x.rp)}</b></div>
      <div><span class="k">Margin</span><b>${x.margin_pct}%</b> <span class="muted small">line average ${x.line_margin_pct}%</span></div>
      ${x.outlook?`<div><span class="k">Market outlook ${esc(String(x.outlook.year))} (${esc(x.outlook.metric)})</span><b>${x.outlook.mean_pct>=0?'+':''}${x.outlook.mean_pct}% a year</b> <span class="muted small">${x.outlook.std_pct!=null?'\u00b1 '+x.outlook.std_pct+'% \u00b7 ':''}${x.outlook.n} reading${x.outlook.n>1?'s':''}</span></div>`:''}
    </div>`;
  const reasons=`<div class="bg-sec"><div class="k">Why this action</div><ul class="bg-reasons">${(x.reasons||[]).map(r=>`<li>${esc(r)}</li>`).join('')}</ul>${(x.flags||[]).length>1?`<div class="small muted">Other tests that fired: ${x.flags.filter(f=>f!==x.action).map(f=>bgPill(f)).join(' ')}</div>`:''}</div>`;
  const dated=(x.dated||[]).length?`<div class="bg-sec"><div class="k">Dated items before the end of ${esc(String((DASH.budget||{}).year||2026))}</div><ul class="bg-dated">${x.dated.map(d=>`<li><span class="bg-date">${esc(fmtWeek?fmtWeek(d.date):d.date)}</span> ${d.url?`<a class="link" href="${esc(d.url)}" target="_blank" rel="noopener">${esc(d.title||'')}</a>`:esc(d.title||'')} <span class="muted small">\u00b7 ${esc(d.type||'')}</span></li>`).join('')}</ul></div>`:'';
  const subs=Object.keys(x.subcategories||{}).length?`<div class="bg-sec"><div class="k">Budget lines in this cell</div><div class="bg-subs">${Object.entries(x.subcategories).map(([k,v])=>`<span class="tag">${esc(k)} ${bgM(v)}</span>`).join(' ')}</div></div>`:'';
  const rivals=(x.high_threat||[]).length?`<div class="bg-sec"><div class="k">High-threat rivals here (${x.n_high_threat} of ${x.n_rivals})</div><ul class="bg-rivals">${x.high_threat.map(v=>`<li><b>${esc(v.name)}</b>${v.role?` <span class="muted">\u00b7 ${esc(v.role)}</span>`:''}${v.latest?`<div class="small">${linkify(v.latest)}</div>`:''}</li>`).join('')}</ul></div>`:'';
  w.innerHTML=nums+reasons+dated+subs+rivals;
  const addSigs=(title,list)=>{ if(!list||!list.length) return; const sec=el("div","bg-sec"); sec.innerHTML=`<div class="k">${esc(title)} (${list.length})</div>`; list.forEach(o=>{ const sg=sigByKey[o.key]; if(sg) sec.appendChild(sigCard(sg)); }); w.appendChild(sec); };
  addSigs('Open opportunities', x.opportunities);
  addSigs('Positions Printec holds', x.held);
  addSigs('Won by a competitor', x.lost);
  return w;
}
// ---- the Admin unlock: password -> PBKDF2 key -> AES-GCM decrypt -> DASH.budget (14/09/2026) ----
async function budgetDecrypt(password){
  const E=window.__DASH_BUDGET_ENC__; if(!E||!window.crypto||!crypto.subtle) throw new Error('This browser cannot decrypt the budget block.');
  const b64=x=>Uint8Array.from(atob(x),c=>c.charCodeAt(0)), te=new TextEncoder();
  const base=await crypto.subtle.importKey('raw',te.encode(password),'PBKDF2',false,['deriveKey']);
  const key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:b64(E.salt),iterations:E.iter||200000,hash:'SHA-256'},base,{name:'AES-GCM',length:256},false,['decrypt']);
  const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:b64(E.iv)},key,b64(E.ct));
  return JSON.parse(new TextDecoder().decode(pt));
}
function budgetUnlockDialog(nav, adm){
  let box=nav.querySelector('.admin-box');
  if(box){ box.remove(); return; }
  box=el("div","admin-box");
  box.innerHTML=`<label class="small">Password<input type="password" autocomplete="current-password" aria-label="Admin password"></label><div class="admin-row"><button type="button" class="admin-go">Unlock</button><span class="admin-msg small muted"></span></div>`;
  adm.insertAdjacentElement('afterend',box);
  const inp=box.querySelector('input'), msg=box.querySelector('.admin-msg');
  const go=async()=>{ msg.textContent='Checking\u2026';
    try{ const P=await budgetDecrypt(inp.value); DASH.budget=P.budget; if(P.budget_2027) DASH.budget_2027=P.budget_2027; if(P.budget_2027_board) DASH.budget_2027_board=P.budget_2027_board;
         window.__DASH_BUDGET_UNLOCKED__=true; box.remove(); adm.remove(); buildShell(); show('budget'); }
    catch(e){ msg.textContent='Wrong password.'; inp.select(); } };
  box.querySelector('.admin-go').addEventListener('click',go);
  inp.addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); go(); } });
  inp.focus();
}
function renderBudget(s){
  s.innerHTML="";
  const B=DASH.budget;
  if(!B||!B.cells||!B.cells.length){ s.appendChild(el("div","card","<div class='empty'>No budget file in this build. Put <code>budget/budget_clean.xlsx</code> in the project folder and rebuild.</div>")); return; }
  const sigByKey={}; (DASH.signals||[]).forEach(x=>sigByKey[x.key]=x);
  const P=DASH.budget_2027||{}, Bd=DASH.budget_2027_board; const hasBoard=!!(Bd&&Bd.cells&&Bd.cells.length);
  const T=B.totals, U=B.uncovered||{};
  const pc=v=>(v>=0?'+':'')+Number(v).toFixed(1)+'%';
  const chips=(keys,label)=>{ const ks=(keys||[]).filter(k=>sigByKey[k]); if(!ks.length) return '';
    return `<div class="ol-builton"><span class="ol-evk" title="The signals this rests on. Click one to see the signal and its sources.">${esc(label||'Evidence')}</span> ${ks.map(k=>`<span class="srcfile ol-sig" data-sigkey="${esc(k)}" role="button" tabindex="0" title="Show this signal &amp; its sources">${esc(sigByKey[k].bank_theme)}</span>`).join('')}<div class="ol-sigdetail" hidden></div></div>`; };
  const viewName=id=>{ const x=(Bd&&Bd.seats||[]).find(y=>y.seat===id); return x?x.title:id; };
  const bdK={}, bdC={}, bdL={}; if(hasBoard){ Bd.cells.forEach(c=>bdK[c.code+'|'+c.line]=c); Bd.by_country.forEach(c=>bdC[c.code]=c); Bd.by_line.forEach(l=>bdL[l.line]=l); }
  const mdK={}; (P.cells||[]).forEach(c=>mdK[c.code+'|'+c.line]=c);
  const reachSet=new Set(hasBoard?(Bd.largest_reachable_cells||[]):[]);
  // the same glyph chips the Future outlook uses for its section headers
  const GL={flag:'<path d="M5 21V4h11l-1.5 4L16 12H5"/>',bolt:'<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
            grid:'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
            map:'<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
            target:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.6"/><circle cx="12" cy="12" r="1"/>',
            gem:'<path d="M12 3l2.3 5.7L20 11l-5.7 2.3L12 19l-2.3-5.7L4 11l5.7-2.3z"/>',
            shield:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
            check:'<path d="M20 6L9 17l-5-5"/>',
            doc:'<path d="M6 3h9l5 5v13H6z"/><path d="M14 3v6h6M9 13h7M9 17h7"/>'};
  const chip=(tone,glyph)=>`<span class="bl-chip bl-${tone}"><svg viewBox="0 0 24 24" aria-hidden="true">${glyph}</svg></span>`;
  const shead=(tone,glyph,title,desc)=>`<div class="bl-shead">${chip(tone,glyph)}<div><h2>${esc(title)}</h2>${desc?`<div class="desc">${esc(desc)}</div>`:''}</div></div>`;
  const TONES=['cyan','lilac','green','yellow'];
  // a bold-led markdown paragraph list -> Future-outlook sections: the lead becomes the header, the rest the prose
  const splitLead=md=>String(md||'').split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean).map(par=>{ const m=par.match(/^\*\*(.+?)\*\*\.?\s*([\s\S]*)$/); return m?{lead:m[1].replace(/\.$/,''),text:m[2]}:{lead:'',text:par}; });

  // ---- scenario shown in the moves grid; the estimate cards switch it ----
  const SCEN={y2026:{label:'2026 budget'},floor:{label:'Lowest acceptable'},budget:{label:'2027 budget'},upside:{label:'Maximum on the table'},today:{label:'Reviewed budget before the plan'}};
  const isPlan=hasBoard&&!!Bd.plan_based;
  let scen=hasBoard?'budget':'y2026';
  const cellVal=(k,sc)=>{ const c=B.cells.find(x=>x.code+'|'+x.line===k); const b=bdK[k]; if(!c) return null;
    if(sc==='y2026'||!b) return {v:c.target,g:null};
    const x=b.board;
    const v=sc==='floor'?x.floor:sc==='upside'?x.upside:sc==='today'?((x.today&&x.today.target!=null)?x.today.target:x.target):x.target; return {v,g:c.target?(v/c.target-1)*100:null}; };

  // 1. executive summary, in the Future outlook's form: cyan hero with the number, four estimate cards
  //    (clickable: they switch the moves grid), then the summary's paragraphs as full-width sections
  if(hasBoard){
    const Tb=Bd.totals, R=Bd.report||{};
    const paras=splitLead(R.executive_summary_md||'');
    const thesis=paras.length&&!paras[0].lead?paras.shift().text:'';
    const hero=el("div","bl-hero");
    hero.innerHTML=`<span class="bl-blob"></span><span class="bl-kicker">Budget 2027</span><h2 class="bl-htitle">Executive summary</h2>${thesis?`<div class="bl-thesis">${mdToHtml(thesis)}</div>`:''}
      <div class="bg-est">
        ${[['y2026','k-blue','2026 budget',bgM(Tb.rev_2026),'profit '+bgM(Tb.rp_2026)],
           ['floor','k-yellow','Lowest acceptable',bgM(Tb.floor),pc(Tb.floor_growth_pct)+' on 2026 · profit '+bgM(Tb.rp_floor)],
           ['budget','k-green','2027 budget',bgM(Tb.commit),pc(Tb.commit_growth_pct)+' · profit '+bgM(Tb.rp_commit)],
           isPlan?['upside','k-lilac','Maximum on the table',bgM(Tb.upside),pc(Tb.upside_growth_pct)+' · every deal won, every capability built']
                 :['reach','k-lilac','Most the evidence supports',bgM(Tb.reachable!=null?Tb.reachable:Tb.upside),pc(Tb.reachable_growth_pct!=null?Tb.reachable_growth_pct:Tb.upside_growth_pct)+' · if the dated deals are won']]
          .map(([id,tone,lab,big,sub])=>`<div class="bl-kpi ${tone} bg-estcard${scen===id?' on':''}" data-scen="${id}" role="button" tabindex="0" title="Show this estimate in the table below"><span class="blob"></span><div class="bl-kpi-h"><div class="bl-kpi-t">${esc(lab)}</div></div><div class="bg-estnum">${big}</div><div class="bl-kpi-d">${esc(sub)}</div><div class="bg-estshown">shown in the table</div></div>`).join('')}
      </div>
      ${isPlan&&Tb.supported_today?`<div class="bg-esthint bg-today"><span class="bg-estcard bg-todaylink" data-scen="today" role="button" tabindex="0" title="Show what the evidence supports today, cell by cell">What the evidence supports today, before the plan\u2019s actions: <b>${bgM(Tb.supported_today)} (${pc(Tb.supported_today_growth_pct)})</b>; the reviewed budget before the plan was ${bgM((Tb.today||{}).commit||0)} (${pc(((Tb.today||{}).commit_growth_pct)||0)}). Click to show that budget in the table.</span></div>`:''}
      <div class="bg-esthint">Click an estimate to show it in the table of moves below.</div>`;
    s.appendChild(hero);
    const card=el("div","card");
    card.innerHTML=paras.map((p,i)=>`<div class="bl-sec bg-secp">${shead(TONES[i%TONES.length],[GL.bolt,GL.grid,GL.map,GL.target,GL.gem,GL.shield,GL.check][i%7],p.lead||'',null)}<div class="bg-prose">${mdToHtml(p.text)}</div></div>`).join('');
    // the full explanation, folded, in the same form
    const d=el("details","bl-panel bg-full"); d.innerHTML=`<summary class="bl-panel-sum">The full explanation: how the number was built, the evidence, the challenges<span class="bl-panel-chev" aria-hidden="true"></span></summary>`;
    const body=el("div","bl-panel-body");
    let h='';
    if(Tb.parts){ const KC=['k-cyan','k-yellow','k-green','k-lilac']; const parts=[['Named deals in the signals',Tb.parts.named_deals_net,'net of the competitor threat'],['Market outlook',Tb.parts.market_outlook,Tb.parts.outlook_cells?`${Tb.parts.outlook_cells.patterns_and_signals} cells on patterns and signals readings, ${Tb.parts.outlook_cells.signals_only} on signals only, ${Tb.parts.outlook_cells.none} with no outlook`:''],['Recurring revenue',Tb.parts.recurring,'price and scope on services and outsourcing'],['New business',Tb.parts.new_business||0,'country and product combinations with no 2026 budget']];
      h+=`<div class="bl-sec">${shead('lilac',GL.bolt,'Where the growth of '+bgM(Tb.commit-Tb.rev_2026)+' comes from','Estimates that rest on named deals in the signals and estimates that rest on the market outlook are shown separately. The outlook is the mean of the dashboard’s readings; there is no statistical trend fit.')}<div class="bl-grid bg-grid4">${parts.map((q,i)=>`<div class="bl-kpi ${KC[i]}"><span class="blob"></span><div class="bl-kpi-h"><div class="bl-kpi-t">${esc(q[0])}</div></div><div class="bg-estnum">${bgM(q[1])}</div><div class="bl-kpi-d">${esc(q[2])}</div></div>`).join('')}</div></div>`; }
    if(Bd.largest_reachable_basis) h+=`<div class="bl-sec">${shead('green',GL.target,'How the most the evidence supports is built',null)}<div class="bg-prose">${mdToHtml(Bd.largest_reachable_basis)}</div></div>`;
    (R.sections||[]).forEach((x,i)=>{ h+=`<div class="bl-sec">${shead(TONES[(i+1)%TONES.length],[GL.doc,GL.grid,GL.map,GL.target,GL.shield,GL.bolt,GL.check,GL.gem][i%8],x.title,null)}<div class="bg-prose">${mdToHtml(x.text)}</div>${chips(x.evidence)}</div>`; });
    if((R.levers||[]).length) h+=`<div class="bl-sec">${shead('yellow',GL.gem,'The levers behind the most the evidence supports',R.levers.length+' budget lines, with the deals and dates they rest on.')}<div class="bl-stack">${R.levers.map(l=>`<div class="bl-tile"><span class="bl-pill bl-green">${esc(l.country||'')} · ${esc(l.line_label||l.cell)}</span><div class="bl-tile-t">2026 ${bgM(l.target_2026||0)} → budget ${bgM(l.commit||0)}${l.commit_growth_pct!=null?` (${pc(l.commit_growth_pct)})`:''} → reachable ${bgM(l.upside||0)}${l.upside_growth_pct!=null?` (${pc(l.upside_growth_pct)})`:''}</div><div class="bl-tile-d">${esc(l.why||'')}</div>${chips(l.evidence)}</div>`).join('')}</div></div>`;
    if((Bd.new_business||[]).length||(Bd.new_business_unpriced||[]).length){
      h+=`<div class="bl-sec">${shead('cyan',GL.flag,'New business',`${(Bd.new_business||[]).length} country and product combinations with no 2026 budget are in the number${(Bd.new_business_unpriced||[]).length?`; ${Bd.new_business_unpriced.length} more have opportunities but no number yet`:''}.`)}<div class="tablewrap"><table class="bgtable"><thead><tr><th>Country × product</th><th>2027 budget</th><th>Most the evidence supports</th><th>Set by</th><th>Why</th></tr></thead><tbody>${(Bd.new_business||[]).slice().sort((x,y)=>y.board.target-x.board.target).map(o=>`<tr><td><b>${esc(o.country)}</b><div class="small muted">${esc(o.line_label)}</div></td><td><b>${bgM(o.board.target)}</b>${o.board.dissent?`<div class="small muted">${esc(o.board.dissent.view||viewName(o.board.dissent.seat))} would set ${bgM(o.board.dissent.number)}</div>`:''}</td><td>${bgM(o.board.upside)}</td><td class="small">${esc(o.board.proposer_title)}${o.board.decided_by_chair?' · settled in the review':''}</td><td class="small">${esc(o.board.reason)}${chips(o.board.evidence)}</td></tr>`).join('')}</tbody></table></div>`;
      if((Bd.new_business_unpriced||[]).length){ const top=Bd.new_business_unpriced.slice().sort((x,y)=>y.n_opps-x.n_opps).slice(0,12); h+=`<div class="small muted bg-unpriced"><b>With opportunities but no number yet</b> (largest first): ${top.map(e=>`${esc(e.country)} × ${esc(e.line_label)} (${e.n_opps})`).join(' · ')}${Bd.new_business_unpriced.length>12?` and ${Bd.new_business_unpriced.length-12} more`:''}.</div>`; }
      h+=`</div>`;
    }
    if((R.conditions||[]).length) h+=`<div class="bl-sec">${shead('green',GL.check,'Conditions attached to the budget',null)}<div class="bl-stack">${R.conditions.map((x,i)=>`<div class="bl-tile"><div class="bl-tile-d"><b>${i+1}.</b> ${esc(x)}</div></div>`).join('')}</div></div>`;
    if((R.change_our_mind||[]).length) h+=`<div class="bl-sec">${shead('yellow',GL.bolt,'What would change the number',null)}<div class="bl-stack">${R.change_our_mind.map(x=>`<div class="bl-tile"><div class="bl-tile-d">${esc(x)}</div></div>`).join('')}</div></div>`;
    if((Bd.dissent_views||[]).length) h+=`<div class="bl-sec">${shead('lilac',GL.shield,'The views that would set a lower number',null)}<div class="bl-stack">${Bd.dissent_views.map(v=>`<div class="bl-tile"><span class="bl-pill bl-green">${esc(v.title)}</span><div class="bl-tile-t">${esc(v.reason||'')}</div><div class="bl-tile-d">${esc(v.text||'')}</div></div>`).join('')}</div></div>`;
    h+=`<div class="small muted evsrc">Built on the dashboard’s signals and market readings. Every figure traces to a budget line or a signal; conversion rates are labelled assumptions, never evidence. Model build of ${esc(Bd.built_from)}.</div>`;
    body.innerHTML=h; d.appendChild(body); card.appendChild(d); s.appendChild(card);
  }

  // 2. the moves, market by market: each cell is a budget line with the estimate chosen above, coloured by
  //    its move. Click a cell and the details appear underneath.
  const lines=(B.by_line||[]); const rows=(B.by_country||[]);
  const byKey={}; B.cells.forEach(c=>byKey[c.code+'|'+c.line]=c);
  const boardBlock=k=>{ const b=bdK[k]; const c=byKey[k]; const m=mdK[k]; if(!b&&!m) return '';
    if(!b) return `<div class="bg-sec"><div class="k">2027 (model)</div><div class="small">Base ${bgM(m.base.target)} (${pc(m.base.growth_pct)}) · stretch ${bgM(m.stretch.target)} (${pc(m.stretch.growth_pct)}).</div></div>`;
    const x=b.board; const capv=x.capacity?`${esc(x.capacity.verdict==='yes'?'delivery confirmed':x.capacity.verdict==='yes-with-hire'?'delivery confirmed with hires':x.capacity.verdict==='no'?'delivery not confirmed':x.capacity.verdict)}${x.capacity.reason?': '+esc(x.capacity.reason):''}`:'';
    const fmtD=d=>{ const mm=String(d||'').match(/^(\d{4})-(\d{2})-(\d{2})$/); if(!mm) return esc(d||''); const MO=['January','February','March','April','May','June','July','August','September','October','November','December']; return `${parseInt(mm[3])} ${MO[parseInt(mm[2])-1]} ${mm[1]}`; };
    const PA=x.plan_actions||[];
    return `<div class="bg-sec bg-boardsec"><div class="k">The 2027 number</div>
      <div class="bg-nums">
        <div><span class="k">2026 budget</span><b>${bgM(c.target)}</b></div>
        <div><span class="k">Lowest acceptable</span><b>${bgM(x.floor)}</b>${x.floor_growth_pct!=null?` <span class="muted small">${pc(x.floor_growth_pct)}</span>`:''}</div>
        <div><span class="k">2027 budget</span><b>${bgM(x.target)}</b>${x.growth_pct!=null?` <span class="muted small">${pc(x.growth_pct)}</span>`:''}</div>
        <div><span class="k">Maximum on the table</span><b>${bgM(x.upside)}</b></div>
        ${x.today?`<div><span class="k">What the evidence supports today</span><b>${bgM(x.today.floor)} / ${bgM(x.today.target)} / ${bgM(x.today.upside)}</b> <span class="muted small">floor / budget / highest, before the plan</span></div>`:''}
        ${m?`<div><span class="k">Model base / stretch</span><b>${bgM(m.base.target)} / ${bgM(m.stretch.target)}</b></div>`:''}
      </div>
      ${PA.length?`<div class="k" style="margin-top:6px">The plan for this line: ${PA.length} action${PA.length===1?'':'s'}, ${bgM(PA.reduce((s,a)=>s+(a.eur_budget||0),0))} to the budget${x.gap_closer_eur?`, plus ${bgM(x.gap_closer_eur)} on the floor from one of the three closing facts`:''}</div><ul class="bg-dated">${PA.map(a=>`<li>${esc(a.what)} <span class="muted small">\u00b7 ${esc(a.kind)} \u00b7 by ${fmtD(a.by)} \u00b7 ${esc(a.owner)} \u00b7 floor ${bgM(a.eur_floor||0)}, budget ${bgM(a.eur_budget||0)}${a.deal_title?' \u00b7 '+esc(a.deal_title):''}</span></li>`).join('')}</ul>`:''}
      <div class="small"><b>${esc(x.proposer_title)}${x.decided_by_chair?' · settled in the review':''}:</b> ${esc(x.reason)}${x.decided_by_chair&&x.chair_reason?` <b>Settled:</b> ${esc(x.chair_reason)}`:''}</div>
      ${x.parts?`<div class="small muted">Named deals net of threat ${bgM(x.parts.named_deals_net)} · market outlook ${bgM(x.parts.market_outlook)} · recurring ${bgM(x.parts.recurring)}.</div>`:''}
      ${(x.assumptions||[]).length?`<div class="small"><b>Assumptions:</b> ${x.assumptions.map(a=>esc(a.text||'')+(a.conversion_pct!=null?' ('+a.conversion_pct+'%'+(a.date?' by '+esc(a.date):'')+')':'')).join(' ')}</div>`:''}
      ${(x.conditions||[]).length?`<div class="small"><b>Conditions:</b> ${x.conditions.map(esc).join('; ')}</div>`:''}
      ${capv?`<div class="small"><b>Delivery check:</b> ${capv}</div>`:''}
      ${x.dissent?`<div class="small"><b>${esc(x.dissent.view||viewName(x.dissent.seat))} would set ${bgM(x.dissent.number)}:</b> ${esc(x.dissent.reason)}</div>`:''}
      ${chips(x.evidence,'Evidence')}
    </div>`; };
  const grid=el("div","card");
  grid.innerHTML=`<div class="hd"><div><h2>The moves, market by market</h2><div class="desc">Each cell is a budget line with the estimate chosen above (<b class="bg-scenlabel"></b>) and the move it calls for. <b>Click a cell</b> and the details appear underneath: the numbers, why this move, the dated items, the signals and how the 2027 number was set. Lines under €0.05m are left blank. The column <b>Retail and other, carried flat</b> holds the budget lines the market model does not analyse (retail equipment and rows with no product name); they keep their 2026 figure in every estimate and count in the totals.</div></div></div>
    <div class="bg-legend">${Object.entries(B.actions_legend||{}).map(([a,tx])=>`<div>${bgPill(a)}<span>${esc(tx)}</span></div>`).join('')}</div>`;
  const wrapT=el("div","tablewrap"); const t=el("table","bgtable"); wrapT.appendChild(t); grid.appendChild(wrapT);
  const detail=el("div","bg-detail"); detail.hidden=true; grid.appendChild(detail);
  const showCell=k=>{ const c=byKey[k]; if(!c) return; detail.hidden=false;
    detail.innerHTML=`<div class="bg-detail-h">${bgPill(c.action)}<b>${esc(c.country)} × ${esc(c.line_label)}</b><button type="button" class="bg-close" aria-label="Close">×</button></div>`;
    const bb=el("div"); bb.innerHTML=boardBlock(k); if(bb.firstElementChild) detail.appendChild(bb.firstElementChild);
    detail.appendChild(bgCellBody(c,sigByKey)); detail.querySelector('.bg-close').addEventListener('click',()=>{ detail.hidden=true; }); detail.scrollIntoView({behavior:'smooth',block:'nearest'}); };
  // totals: anchor on the file's own totals for the scenario (floor / commit) and add only the difference
  // the visible cells make, so retail, unnamed lines, tiny cells and new business are never double counted
  const anchorKey=sc=>sc==='floor'?'floor':sc==='upside'?'upside':'commit';
  const anchorCell=(b,sc)=>sc==='floor'?b.board.floor:sc==='upside'?b.board.upside:sc==='today'?((b.board.today&&b.board.today.target!=null)?b.board.today.target:b.board.target):b.board.target;
  const nbDelta=(sc,pred)=>{ if(!Bd) return 0; if(sc==='today') return Bd.new_business.filter(pred).reduce((a,o)=>a+(((o.board.today||{}).target||0)-o.board.target),0); return 0; };
  const drawGrid=()=>{
    grid.querySelector('.bg-scenlabel').textContent=SCEN[scen].label;
    const NC='Budget lines the market model does not analyse, carried into 2027 unchanged: retail lines (self-checkout, retail POS, store equipment, vending, telecom, printing) and rows with no product name (“Other”). Included in the country total, no move of their own.';
    t.innerHTML=`<thead><tr><th>Market</th>${lines.map(l=>`<th title="${esc(l.line_label)}">${esc(l.line_label)}</th>`).join('')}<th title="${esc(NC)}">Retail and other, carried flat <span class="bg-help" aria-hidden="true">?</span></th><th>Total</th></tr></thead>`;
    const tb=el("tbody"); const lineVal={}, lineAnchor={};
    rows.forEach(r=>{
      const tr=el("tr"); let rowVal=0, rowAnchor=0;
      const cellsHtml=lines.map(l=>{ const k=r.code+'|'+l.line; const c=byKey[k]; if(!c||c.target<5e4) return '<td class="bg-cell bg-none"></td>'; const n=cellVal(k,scen); const b=bdK[k];
          rowVal+=n.v; lineVal[l.line]=(lineVal[l.line]||0)+n.v; if(b){ const av=anchorCell(b,scen); rowAnchor+=av; lineAnchor[l.line]=(lineAnchor[l.line]||0)+av; }
          return `<td class="bg-cell ${bgCls(c.action)}" data-k="${esc(k)}" role="button" tabindex="0" title="${esc(r.country)} × ${esc(l.line_label)}: ${esc(BG_ACT[c.action])}. 2026 ${bgM(c.target)}${n.g!=null?` → ${bgM(n.v)} (${pc(n.g)})`:''}. ${c.n_opps} open opportunit${c.n_opps===1?'y':'ies'}.">${bgM(n.v)}<div class="bg-act">${esc(BG_ACT[c.action])}${n.g!=null?' · '+pc(n.g):''}</div></td>`; }).join('');
      const rc=bdC[r.code];
      const total=(scen==='y2026'||!rc)?r.target:(rc[scen==='today'?'commit':anchorKey(scen)]+(rowVal-rowAnchor)+nbDelta(scen,o=>o.code===r.code));
      tr.innerHTML=`<td><b>${esc(r.country)}</b><div class="small muted">2026 ${bgM(r.target)}</div></td>`+cellsHtml+`<td class="small muted" title="${esc(r.country)}: retail ${bgM(r.retail||0)}, other ${bgM(r.other||0)}. ${esc(NC)}">${bgM((r.retail||0)+(r.other||0))}<div class="bg-act">retail ${bgM(r.retail||0)} · other ${bgM(r.other||0)}</div></td><td><b>${bgM(total)}</b>${scen!=='y2026'&&r.target?`<div class="small muted">${pc((total/r.target-1)*100)}</div>`:''}</td>`;
      tb.appendChild(tr);
    });
    const grand=(scen==='y2026'||!hasBoard)?T.target:scen==='today'?((Bd.totals.today||{}).commit||Bd.totals.commit):Bd.totals[anchorKey(scen)];
    const tf=el("tr","bg-total"); tf.innerHTML=`<td><b>Group</b></td>${lines.map(l=>{ const lc=bdL[l.line]; const v=(scen==='y2026'||!lc)?l.target:(lc[scen==='today'?'commit':anchorKey(scen)]+((lineVal[l.line]||0)-(lineAnchor[l.line]||0))+nbDelta(scen,o=>o.line===l.line)); return `<td><b>${bgM(v)}</b><div class="small muted">${scen!=='y2026'&&l.target?pc((v/l.target-1)*100):(l.margin_pct+'%')}</div></td>`; }).join('')}<td class="small muted" title="${esc(NC)}">${bgM((U.retail||0)+(U.other||0))}<div class="bg-act">retail ${bgM(U.retail||0)} · other ${bgM(U.other||0)}</div></td><td><b>${bgM(grand)}</b>${scen!=='y2026'&&T.target?`<div class="small muted">${pc((grand/T.target-1)*100)}</div>`:''}</td>`;
    tb.appendChild(tf); t.appendChild(tb);
    t.querySelectorAll('.bg-cell[data-k]').forEach(td=>{ td.addEventListener('click',()=>showCell(td.dataset.k)); td.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); showCell(td.dataset.k); } }); });
  };
  s.appendChild(grid); drawGrid();
  // clicking an estimate card redraws the grid AND takes the reader down to it, so the change is seen
  // (asked 14/09/2026: without the scroll nobody understood what the click did)
  const setScen=id=>{ if(!SCEN[id]) return; scen=id; s.querySelectorAll('.bg-estcard').forEach(x=>x.classList.toggle('on',x.dataset.scen===id)); detail.hidden=true; drawGrid();
    grid.scrollIntoView({behavior:'smooth',block:'start'}); grid.classList.remove('bg-flash'); void grid.offsetWidth; grid.classList.add('bg-flash'); };
  s.querySelectorAll('.bg-estcard').forEach(x=>{ x.addEventListener('click',()=>setScen(x.dataset.scen)); x.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); setScen(x.dataset.scen); } }); });

  // (the ranked list of moves was removed on 14/09/2026: it repeated the grid above)
}

// Countries on the map that are NOT Printec markets (MAP.outside — Austria since 02/09/2026, redrawn
// 10/09/2026): grey, not clickable, named on hover so the gap on the map reads as a choice, not a hole.
function outsidePaths(MAP){
  return Object.entries((MAP&&MAP.outside)||{}).map(([code,c])=>
    `<path class="fmap-out" data-code="${code}" d="${c.d}" aria-label="${esc(c.name)}: not a Printec market"><title>${esc(c.name)} — not a Printec market</title></path>`).join('');
}

function renderCountry(s){
  s.innerHTML="";
  const top=el("div","card");
  top.innerHTML=`<div class="hd"><div><h2>Markets ranked by opportunity value</h2><div class="desc">Market priority = <b>total deal value (€m)</b>: the deal bands of all biddable signals in each market, added up and anchored to tender or capex figures where known. Green bars have new signals this week. <b>Click a bar</b> to list that market's opportunities. The per-market figures below come from the statistics agent.</div></div></div>
    <div class="chart-panel"><div class="chartbox tall"><canvas id="cChart"></canvas></div></div>
    <div class="legend"><span><span class="sw" style="background:var(--cyan)"></span>potential value (€m)</span><span><span class="sw" style="background:var(--green)"></span>has new signals this week</span></div>`;
  s.appendChild(top);
  const cReveal=el("div","reveal"); top.appendChild(cReveal);
  top.appendChild(chartSource("Printec research agents."));

  const tw=el("div","card");
  tw.innerHTML=`<div class="hd"><div><h2>Market detail and background figures</h2><div class="desc">The ATM, branch and instant-payment columns are the latest figures from the statistics agent. Click a market to see its signals and what they mean.</div></div></div>`;
  // Filters, above the table. Sixteen markets with an expandable signal list underneath each is a lot
  // of scrolling to reach one country (raised on the strategy call, 36:58).
  const cflt=el("div","tablefilters");
  // A few markets carry their own code as their "region" (GR, UA) — show the market's name there
  // rather than a two-letter code the reader has to decode.
  const regions=[...new Set(DASH.countries.map(c=>c.region).filter(Boolean))].sort();
  const rgLabel=r=>DASH.code2name[r]||r;
  cflt.innerHTML=`<label>Region <select id="ctRegion"><option value="">All regions</option>${regions.map(r=>`<option value="${esc(r)}">${esc(rgLabel(r))}</option>`).join('')}</select></label>
    <label>Sort <select id="ctSort"><option value="value">Largest value</option><option value="signals">Most signals</option><option value="new">Most new this week</option><option value="name">Market name</option></select></label>
    <label class="toggle"><input type="checkbox" id="ctNew"> New signals only</label>
    <input type="search" id="ctQ" placeholder="find a market…" aria-label="Find a market">`;
  tw.appendChild(cflt);
  const ctCount=el("div","desc"); ctCount.style.padding="2px 2px 8px"; tw.appendChild(ctCount);
  const wrapT=el("div","tablewrap");
  const tbl=el("table");
  tbl.innerHTML=`<thead><tr><th>Market</th><th>Value €m</th><th>Signals</th><th>High</th><th>New</th><th>ATMs</th><th>Branches</th><th>Instant pay</th></tr></thead>`;
  const tb=el("tbody");
  const maxScore=Math.max(1,...DASH.countries.map(x=>x.score));
  const CT_SORT={value:(a,b)=>b.score-a.score, signals:(a,b)=>b.n_signals-a.n_signals,
                 new:(a,b)=>(b.n_new||0)-(a.n_new||0)||b.score-a.score,
                 name:(a,b)=>String(a.name).localeCompare(String(b.name))};
  function ctRows(){
    const rg=$("#ctRegion").value, q=$("#ctQ").value.trim().toLowerCase(), onlyNew=$("#ctNew").checked;
    return DASH.countries
      .filter(c=>!(c.n_signals===0 && !c.atms && !c.branches))
      .filter(c=>!rg||c.region===rg)
      .filter(c=>!onlyNew||(c.n_new||0)>0)
      .filter(c=>!q||String(c.name).toLowerCase().includes(q))
      .slice().sort(CT_SORT[$("#ctSort").value]||CT_SORT.value);
  }
  function ctDraw(){
  tb.innerHTML="";
  const _shown=ctRows();
  const _total=DASH.countries.filter(c=>!(c.n_signals===0 && !c.atms && !c.branches)).length;
  ctCount.innerHTML=`Showing <b>${_shown.length}</b> of ${_total} markets.`;
  if(!_shown.length){ const _tr=el("tr"); const _td=el("td"); _td.colSpan=8;
    _td.appendChild(el("div","empty","No market matches these filters.")); _tr.appendChild(_td); tb.appendChild(_tr); return; }
  _shown.forEach(c=>{
    const tr=el("tr","clickable");
    tr.innerHTML=`<td><b>${esc(c.name)}</b> <span class="flag">${esc(c.region)}${c.euro?' · €':''}</span></td>
      <td><b>€${c.score}m</b><div class="bar"><i style="width:${Math.min(100,c.score/maxScore*100)}%"></i></div></td>
      <td>${c.n_signals}</td>
      <td>${c.n_high?('<span class="pill High">'+c.n_high+'</span>'):'<span class="muted">—</span>'}</td>
      <td>${c.n_new?('<span class="pill new">'+c.n_new+'</span>'):'<span class="muted">—</span>'}</td>
      <td class="small">${shortCell(c.atms)}</td><td class="small">${shortCell(c.branches)}</td><td class="small">${shortCell(c.instant)}</td>`;
    const det=el("tr"); det.style.display="none";
    const td=el("td"); td.colSpan=8;
    const wrap=el("div"); wrap.style.padding="4px 2px 8px";
    if(c.implication) wrap.appendChild(el("div","note","<b>Implication:</b> "+linkify(c.implication)));
    // cells the table shows in short form get their full text here (asked 10/09/2026)
    const _full=[['ATMs',c.atms],['Branches',c.branches],['Instant payments',c.instant]].filter(x=>isTrimmed(x[1]));
    if(_full.length) wrap.appendChild(el("div","note","<b>Background figures in full.</b> "+_full.map(x=>'<b>'+x[0]+':</b> '+linkify(x[1])).join(' ')));
    // the market's own signals first, then the indirect plays that touch it (asked 10/09/2026)
    c.signal_keys.forEach(key=>wrap.appendChild(sigCard(sigByKey[key])));
    if(!c.signal_keys.length) wrap.appendChild(el("div","empty","No bank-specific signals yet. Only the background statistics."));
    const der=(DASH.derived||[]).filter(d=>(d.countries||[]).includes(c.code) || d.footprint_wide);
    if(der.length) wrap.appendChild(derivedSection(der,{title:'Indirect opportunities involving '+c.name}));
    td.appendChild(wrap); det.appendChild(td);
    tr.addEventListener('click',()=>{ det.style.display = det.style.display==="none" ? "" : "none"; });
    tb.appendChild(tr); tb.appendChild(det);
  });
  }
  tbl.appendChild(tb); wrapT.appendChild(tbl); tw.appendChild(wrapT); s.appendChild(tw);
  ["#ctRegion","#ctSort","#ctNew"].forEach(k=>$(k).onchange=ctDraw); $("#ctQ").oninput=ctDraw; ctDraw();

  if(DASH.wide_signals && DASH.wide_signals.length){
    // Collapsed by default: this block dumps every cross-cutting signal at full length and pushed the
    // structural charts below it off the page (strategy call, 38:28). The heading still states the count,
    // so nothing is hidden — it just no longer costs a screen of scrolling to get past.
    const fw=el("div","card");
    const _wide=DASH.wide_signals.map(k=>sigByKey[k]).filter(Boolean)
      .sort((a,b)=>(potEur(b.size_band)-potEur(a.size_band))||String(sortDate(b)).localeCompare(String(sortDate(a))));
    fw.innerHTML=`<div class="hd"><div><h2>Footprint-wide themes (${_wide.length})</h2><div class="desc">Signals that lift demand in <i>every</i> market at once: regulation, sector structure, partner and competitor moves. They are kept out of the country ranking above so single-market opportunities stay comparable, but they shape the background everywhere.</div></div></div>`;
    const det=el("details","fw-fold");
    det.innerHTML=`<summary>Show the ${_wide.length} footprint-wide signals</summary>`;
    const body=el("div"); det.appendChild(body);
    let _built=false;
    det.addEventListener('toggle',()=>{ if(det.open && !_built){ _built=true; _wide.forEach(sg=>body.appendChild(sigCard(sg))); }
      det.querySelector('summary').textContent = det.open ? 'Hide the footprint-wide signals' : `Show the ${_wide.length} footprint-wide signals`; });
    fw.appendChild(det);
    s.appendChild(fw);
  }

  // core structural counts — devices/branches deployed by market (ECB/HBA actuals), multi-market + metric
  // dropdown. The deep ATM-market detail (recyclers, density, vendors, forecast to 2028) lives on Products.
  fusedChartSection(s,{ id:'fusCountry', index:countryStructIndex(), defaultMetric:'atms', singleMarket:true,
    srcByMetric:{
      atms:'RBR ATM Market 2028 (licensed). Solid = recorded, dashed = RBR forecast to 2028.',
      bank:'RBR ATM Market 2028 (licensed) — Total minus RBR’s independent-deployer (IAD) count. Solid = recorded, dashed = forecast to 2028.',
      atms_ecb:'ECB Payment Statistics — ECB’s own bank-reported ATM count, shown as a cross-check to RBR.',
      pos:'ECB Data Portal (data.ecb.europa.eu); Greece via the Hellenic Bank Association.',
      branches:'ECB Data Portal (data.ecb.europa.eu); Greece via the Hellenic Bank Association.',
      cash:'ECB Data Portal — card cash-withdrawal transaction count (millions, per half-year); Greece via the Hellenic Bank Association.'
    },
    title:'Structural trends across the footprint',
    desc:'<b>Total ATMs</b> and <b>Bank-operated ATMs</b> (Total − independent deployers) are the licensed RBR figures — the same numbers shown on the <b>Products</b> tab. POS terminals and bank branches are from the <a class="link" href="https://data.ecb.europa.eu" target="_blank" rel="noopener noreferrer">ECB Data Portal</a> (Greece from HBA); <b>card cash withdrawals</b> are the ECB count of card cash-withdrawal transactions (in <b>millions</b>, reported per half-year — a transaction count, not a euro value). ECB’s own ATM count is kept as a labelled <b>cross-check</b> — it broadly agrees except where a country reports on a different basis (Austria runs well above, Cyprus below). Pick a metric and a market; solid = recorded, ◇ dashed = RBR forecast to 2028.' });

  // every market with a live contest — including those whose contests are all value-unscoped (score €0 but
  // n_opps>0), which must stay on the axis and clickable rather than disappearing for want of a figure.
  const ranked=DASH.countries.filter(c=>c.score>0 || (c.n_opps||0)>0);
  let cCur=-1;
  mkBar("cChart",ranked.map(c=>c.name),ranked.map(c=>c.score),
        ranked.map(c=>c.n_new>0?'#A6C47C':'#23C0E2'),"Potential value (€m)",true,ranked.map(c=>c.name),
        i=>{ if(i===cCur){ cCur=-1; cReveal.innerHTML=''; return; } cCur=i;
          fillSignalReveal(cReveal, ranked[i].name, (ranked[i].signal_keys||[]).map(k=>sigByKey[k]).filter(g=>g&&isOpportunity(g)), true); });
}

/* ----------------------------------------------------------------- PRODUCT */
function renderProduct(s){
  s.innerHTML="";

  // product demand BY MARKET — per-country filter (a signal counts for each product it touches)
  (function(){
    const sigs=DASH.signals||[];
    const liveIds=DASH.products.filter(p=>p.n_signals>0).map(p=>p.id);
    const actCtry=[...new Set(sigs.flatMap(g=>g.countries||[]))].sort((a,b)=>(DASH.code2name[a]||a).localeCompare(DASH.code2name[b]||b));
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Product opportunity value by market</h2><div class="desc">Deal value (€m) of this week's <b>current, biddable</b> opportunities touching each Printec solution, summed from the deal-size bands (a signal counts for every solution it touches). Filter to one market to see what it is pulling. <b>Click a bar</b> to list the opportunities behind it.</div></div></div>`;
    const flt=el("div","tablefilters");
    flt.innerHTML=`<label>Market <select id="pdC"><option value="">All markets</option>${actCtry.map(c=>`<option value="${c}">${esc(DASH.code2name[c]||c)}</option>`).join('')}</select></label>`;
    card.appendChild(flt);
    const cw=el("div","chart-panel"); cw.innerHTML='<div class="chartbox tall"><canvas id="pdChart"></canvas></div>'; card.appendChild(cw);
    const pdReveal=el("div","reveal"); card.appendChild(pdReveal);
    card.appendChild(chartSource("Printec research agents."));
    s.appendChild(card);
    let pdCur=-1;
    const draw=()=>{
      const cc=$("#pdC").value;
      const rows=liveIds.map(id=>{ const items=sigs.filter(g=>(g.products||[]).includes(id)&&isOpportunity(g)&&(!cc||(g.countries||[]).includes(cc)));
        return {id,label:DASH.prod_label[id]||id,items,v:items.reduce((a,g)=>a+potEur(g.size_band),0)}; })
        .filter(r=>r.v>0).sort((a,b)=>b.v-a.v);
      if(!rows.length){ cw.innerHTML='<div class="empty">No product opportunities in this market.</div>'; pdReveal.innerHTML=''; return; }
      mkBar('pdChart',rows.map(r=>r.label),rows.map(r=>+r.v.toFixed(1)),rows.map(r=>PCOL[r.id]||'#23C0E2'),"Potential value (€m)",true,rows.map(r=>r.label),
        i=>{ if(i===pdCur){ pdCur=-1; pdReveal.innerHTML=''; return; } pdCur=i; fillSignalReveal(pdReveal, rows[i].label, rows[i].items, true); });
    };
    const redraw=()=>{ const ex=window.Chart&&Chart.getChart('pdChart'); if(ex){const i=charts.indexOf(ex);if(i>=0)charts.splice(i,1);ex.destroy();} pdCur=-1; pdReveal.innerHTML=''; if(!document.getElementById('pdChart')) cw.innerHTML='<div class="chartbox tall"><canvas id="pdChart"></canvas></div>'; draw(); };
    flt.querySelector('select').addEventListener('change',redraw);
    draw();
  })();

  // demand under deadline — tenders & mandates by product (from the deadlines array; categorical)
  (function(){
    const dl=DASH.deadlines||[]; const m={}, itemsBy={};
    dl.forEach(d=>(d.products||[]).forEach(p=>{ m[p]=(m[p]||0)+1; (itemsBy[p]=itemsBy[p]||[]).push(d); }));
    const rows=Object.entries(m).map(([id,n])=>({id,label:DASH.prod_label[id]||id,n})).sort((a,b)=>b.n-a.n);
    if(rows.length){
      const card=el("div","card");
      card.innerHTML=`<div class="hd"><div><h2>Tenders and deadlines by product line</h2><div class="desc">How many time-pressured items — named tenders and regulatory deadlines — hit each Printec line. This is where the clock is forcing banks to spend. <b>Click a bar</b> to list the deadlines behind it.</div></div></div>`;
      const cw=el("div","chart-panel"); cw.innerHTML='<div class="chartbox tall"><canvas id="tpChart"></canvas></div>'; card.appendChild(cw);
      const tpReveal=el("div","reveal"); card.appendChild(tpReveal);
      card.appendChild(chartSource("Printec research agents \u2014 named tenders and regulatory deadlines."));
      s.appendChild(card);
      let tpCur=-1;
      mkBar('tpChart',rows.map(r=>r.label),rows.map(r=>r.n),rows.map(r=>PCOL[r.id]||'#E0B83A'),"Deadlines / tenders",true,rows.map(r=>r.label),
        i=>{ if(i===tpCur){ tpCur=-1; tpReveal.innerHTML=''; return; } tpCur=i; fillDeadlineReveal(tpReveal, rows[i].label, itemsBy[rows[i].id]||[]); });
    }
  })();

  // dedicated ATM-market section — fed by the deep-read RBR dataset (DASH.atm_market), 17 markets incl. GR/CY
  renderAtmSection(s);

  const live=DASH.products.filter(p=>p.n_signals>0);
  live.forEach(p=>{
    const c=el("div","card");
    c.innerHTML=`<div class="hd tight"><div class="prodhead"><span class="swatch" style="background:${PCOL[p.id]||'#23C0E2'}"></span><h2>${esc(p.label)}</h2><span class="tag" title="Total value (€m) of open, biddable opportunities that involve this solution">€${p.score}m</span><span class="tag">${p.n_signals} signals · ${p.n_high} High</span></div></div>
      <div class="desc" style="margin-bottom:15px">${esc(p.printec)} &nbsp;&middot;&nbsp; Most opportunity value in: ${p.top_countries.map(cc=>esc(DASH.code2name[cc]||cc)).join(", ")||'—'}</div>`;
    // signals start COLLAPSED — the reader scans titles/subtitles first, then expands to dive into the sub-cards
    const sigs=p.signal_keys.map(k=>sigByKey[k]).filter(Boolean).sort((a,b)=>(potEur(b.size_band)-potEur(a.size_band))||String(sortDate(b)).localeCompare(String(sortDate(a))));
    if(sigs.length){
      const n=sigs.length, det=el("details","prod-sigs");
      det.innerHTML=`<summary class="prod-sigs-sum"><span class="prod-sigs-lbl"></span><span class="prod-sigs-chev" aria-hidden="true"></span></summary>`;
      const lbl=det.querySelector('.prod-sigs-lbl'), setLbl=()=>{ lbl.textContent=det.open?'Hide signals':`View ${n} signal${n>1?'s':''}`; };
      setLbl(); det.addEventListener('toggle',setLbl);
      const body=el("div","prod-sigs-body"); sigs.forEach(sg=>body.appendChild(sigCard(sg)));
      det.appendChild(body); c.appendChild(det);
    }
    s.appendChild(c);
  });
}

/* ----------------------------------------------------------------- COMPETITION */
function renderCompetition(s){
  s.innerHTML="";
  const note=el("div","card");
  note.innerHTML=`<div class="hd"><div><h2>Competitors and partners</h2><div class="desc">Who is winning bank money in the footprint, where Printec is being shut out, and where service gaps are opening. Threat = the pressure on Printec's channel right now.</div></div></div>`;
  const partner=DASH.competitors.find(v=>v.name.indexOf("Atleos")>=0);
  if(partner){ const pw=el("div","card sec-head sh-yellow pw-card");
    pw.innerHTML=`<span class="blob"></span><div class="pw-h">Partner-channel watch — ${esc(partner.name)}</div><div class="pw-text">${linkify(partner.latest)}</div>`;
    note.appendChild(pw); }
  s.appendChild(note);

  // The written read of this week's moves, and the date the watchlist was last refreshed. Asked for on
  // the strategy call (22:04): a reader landing here needs to know how current this page is before
  // trusting a threat ranking, and the summary was previously only on Overview.
  (function(){
    const brief=DASH.competition_brief;
    const dates=(DASH.competitors||[]).map(v=>v.last_updated).filter(Boolean).sort();
    const asOf=dates.length?dates[dates.length-1]:null;
    const nDated=(DASH.competitors||[]).filter(v=>v.last_updated).length;
    if(!brief && !asOf) return;
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Latest summary</h2><div class="desc">What moved in the competitive landscape this week, written by the weekly orchestrator from the competitor and partner findings.</div></div>`
      + (asOf?`<span class="asof-chip" title="The latest date any competitor on the watchlist was updated. ${nDated} of ${(DASH.competitors||[]).length} entries have a date; the rest are standing profiles that did not change.">as of ${esc(fmtWeek(asOf))}</span>`:'')
      + `</div>`;
    if(brief && String(brief).trim()){
      const body=el("div","news"); body.innerHTML=mdToHtml(String(brief)); card.appendChild(body);
    } else {
      card.appendChild(el("div","empty","No written summary this week — the landscape below is the standing watchlist."));
    }
    s.appendChild(card);
  })();

  // ("Competitor financials & ATM operations" SEC-EDGAR chart section removed per request.)

  // competition by product line — how contested each Printec line is, split by threat
  (function(){
    const comps=DASH.competitors||[]; const prodCount={};
    comps.forEach(v=>(v.products||[]).forEach(p=>{ const m=prodCount[p]=prodCount[p]||{High:0,Medium:0,Low:0}; m[v.threat]=(m[v.threat]||0)+1; }));
    const prows=Object.entries(prodCount).map(([id,m])=>({id,label:DASH.prod_label[id]||id,total:(m.High||0)+(m.Medium||0)+(m.Low||0),m})).sort((a,b)=>b.total-a.total);
    if(prows.length){
      const card=el("div","card");
      card.innerHTML=`<div class="hd"><div><h2>Competition by product line</h2><div class="desc">How many rivals compete for each Printec solution, split by threat level. <b>Click a bar</b> to list the competitors on that line.</div></div></div>`;
      const cw=el("div","chart-panel"); cw.innerHTML='<div class="chartbox tall"><canvas id="prodCompBar"></canvas></div>'; card.appendChild(cw);
      const pcReveal=el("div","reveal"); card.appendChild(pcReveal);
      card.appendChild(chartSource("Printec research agents — which competitors sell into which Printec product line."));
      s.appendChild(card);
      const ds=[['High','#0E7C99'],['Medium','#23C0E2'],['Low','#B7E7F2']].map(([t,c])=>({label:t+' threat',color:c,data:prows.map(r=>r.m[t]||0)}));
      const TH={High:3,Medium:2,Low:1};
      let pcCur=-1;
      mkStackBar('prodCompBar',prows.map(r=>r.label),ds,{horizontal:true,title:'Competition by product line',subtitle:'Number of rivals per Printec line, stacked by threat level.',tip:it=>` ${it.dataset.label}: ${it.raw}`,
        onBar:i=>{ if(i===pcCur){ pcCur=-1; pcReveal.innerHTML=''; return; } pcCur=i; const id=prows[i].id;
          fillVendorReveal(pcReveal, prows[i].label, comps.filter(v=>(v.products||[]).includes(id)).sort((a,b)=>(TH[b.threat]||0)-(TH[a.threat]||0)||(b.n_mentions||0)-(a.n_mentions||0))); }});
    }
  })();

  // competitor landscape — filter by market AND product (the page's main sliceable view; unifies the old
  // activity-by-market + who's-pressing-hardest + profiles cards into one filterable section)
  (function(){
    const comps=DASH.competitors||[]; if(!comps.length) return;
    const allCtry=[...new Set(comps.flatMap(v=>v.countries||[]))];
    const PREF=['GR','RO','BG','RS','HU','CZ','CY','HR','UA','SK','SI','AL','BA','XK','ME','MK'];
    const ctryOrder=PREF.filter(c=>allCtry.includes(c)).concat(allCtry.filter(c=>!PREF.includes(c)).sort());   // never drop a present market
    const allProd=[...new Set(comps.flatMap(v=>v.products||[]))].sort((a,b)=>(DASH.prod_label[a]||a).localeCompare(DASH.prod_label[b]||b));
    const mv=DASH.active_vendors||[], mrows=DASH.matrix||[];
    const matchMV=name=>mv.find(x=>x===name||x.split(' ')[0]===name.split(' ')[0]);
    const intensity=(v,cc)=>{ const m=matchMV(v.name); if(!m) return v.n_mentions||0; if(cc){ const row=mrows.find(r=>r.code===cc); return row?(row.cells[m]||0):0; } return mrows.reduce((a,r)=>a+(r.cells[m]||0),0); };
    window.__land=window.__land||{cc:'',pid:'',tier:''}; const st=window.__land;
    const TH={High:3,Medium:2,Low:1}, THC={High:'#E2715E',Medium:'#E0B83A',Low:'#7FB069'};
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Competitors by market and product line</h2><div class="desc">Pick a market and/or a Printec product line to see which rivals compete there. The chart ranks rivals by how many active signals name them. <b>Click a bar</b> to read those signals. The cards below list the full field: presence, threat, role and latest move.</div></div></div>`;
    const flt=el("div","tablefilters");
    flt.innerHTML=`<label>Market <select id="lndC"><option value="">All markets</option>${ctryOrder.map(c=>`<option value="${c}">${esc(DASH.code2name[c]||c)}</option>`).join('')}</select></label>
      <label>Product <select id="lndP"><option value="">All products</option>${allProd.map(p=>`<option value="${p}">${esc(DASH.prod_label[p]||p)}</option>`).join('')}</select></label>
      <label>Size <select id="lndT"><option value="">All sizes</option><option value="local-peer">Local / peer</option><option value="regional">Regional</option><option value="global">Global</option></select></label>`;
    card.appendChild(flt);
    const cw=el("div","chart-panel"); cw.innerHTML='<div class="chartbox tall"><canvas id="landBar"></canvas></div>'; card.appendChild(cw);
    const landReveal=el("div","reveal"); card.appendChild(landReveal);
    card.appendChild(chartSource("Printec research agents \u2014 how often each competitor is named in the active signals."));
    const list=el("div","vendgrid"); list.style.marginTop='22px'; card.appendChild(list); s.appendChild(card);
    let landCur=-1;
    const linkedSigs=v=>(v.mention_keys||[]).map(k=>sigByKey[k]).filter(g=>g&&(!st.cc||(g.countries||[]).includes(st.cc)));   // active signals naming the rival (within the market filter)
    const draw=()=>{
      st.cc=$("#lndC").value; st.pid=$("#lndP").value; st.tier=$("#lndT")?$("#lndT").value:'';
      landCur=-1; landReveal.innerHTML='';
      const here=comps.filter(v=>(!st.cc||(v.countries||[]).includes(st.cc))&&(!st.pid||(v.products||[]).includes(st.pid))&&(!st.tier||v.tier===st.tier));
      const active=here.map(v=>({v,sigs:linkedSigs(v)})).filter(x=>x.sigs.length).sort((a,b)=>(b.sigs.length-a.sigs.length)||(TH[b.v.threat]||0)-(TH[a.v.threat]||0));
      const ex=window.Chart&&Chart.getChart('landBar'); if(ex){const i=charts.indexOf(ex);if(i>=0)charts.splice(i,1);ex.destroy();}
      if(!document.getElementById('landBar')) cw.innerHTML='<div class="chartbox tall"><canvas id="landBar"></canvas></div>';
      if(active.length){
        const box=cw.querySelector('.chartbox'); if(box) box.style.height=Math.max(160,active.length*30)+'px';
        mkBar('landBar',active.map(x=>x.v.name),active.map(x=>x.sigs.length),active.map(()=>'#23C0E2'),'Linked active signals',true,active.map(x=>x.v.name),
          i=>{ if(i===landCur){ landCur=-1; landReveal.innerHTML=''; return; } landCur=i; fillSignalReveal(landReveal, active[i].v.name, active[i].sigs, false); });
      } else { cw.innerHTML='<div class="empty">No competitor in this filter is named in any active signal. The full list is in the cards below.</div>'; }
      list.innerHTML='';
      if(!here.length){ list.appendChild(el('div','empty','No competitor mapped to this filter yet.')); return; }
      here.forEach(v=>list.appendChild(vendorCard(v)));   // all matching competitors (no cap — the full field is the point of this page)
    };
    flt.querySelectorAll('select').forEach(se=>se.addEventListener('change',draw));
    draw();
  })();

  // competitive density by market & size tier — reflects the FULL competitor set (incl. the local long tail)
  (function(){
    const comps=DASH.competitors||[];
    const PREF=['GR','CY','RO','BG','RS','HR','SI','SK','CZ','HU','UA','AL','BA','XK','ME','MK'];
    const allC=[...new Set(comps.flatMap(v=>v.countries||[]))];                              // every market present in the data
    const order=PREF.filter(c=>allC.includes(c)).concat(allC.filter(c=>!PREF.includes(c)).sort());   // preferred order, then any extras — never drop a market
    const rows=order.map(cc=>{
      const here=comps.filter(v=>(v.countries||[]).includes(cc));
      if(!here.length) return null;
      const cnt=t=>here.filter(v=>v.tier===t).length;
      return {name:DASH.code2name[cc]||cc, lp:cnt('local-peer'), rg:cnt('regional'), gl:cnt('global'), total:here.length};
    }).filter(Boolean).sort((a,b)=>b.total-a.total);
    if(!rows.length) return;
    const max=Math.max.apply(null,rows.map(r=>r.total));
    const card=el("div","card");
    card.innerHTML=`<div class="hd"><div><h2>Number of competitors by market and size</h2><div class="desc">How many competitors Printec faces in each market, split by size, including the local long tail (from the ${comps.length}-name watchlist). Darker = more crowded. Use the filters above to see who they are.</div></div></div>`;
    const wrap=el("div","tablewrap"); const t=el("table","matrix");
    t.innerHTML=`<thead><tr><th>Market</th><th>Local / peer</th><th>Regional</th><th>Global</th><th>Total</th></tr></thead>`;
    const tb=el("tbody");
    const cell=v=>{ const a=v?(0.16+0.84*Math.min(v,max)/max):0; return v?`<span class="cell" style="background:rgba(35,192,226,${a.toFixed(2)})">${v}</span>`:'<span class="muted">·</span>'; };
    rows.forEach(r=>{ const tr=el("tr"); tr.innerHTML=`<td><b>${esc(r.name)}</b></td><td>${cell(r.lp)}</td><td>${cell(r.rg)}</td><td>${cell(r.gl)}</td><td><b>${r.total}</b></td>`; tb.appendChild(tr); });
    t.appendChild(tb); wrap.appendChild(t); card.appendChild(wrap); s.appendChild(card);
  })();

  const mw=el("div","card");
  mw.innerHTML=`<div class="hd"><div><h2>Named vendors by market</h2><div class="desc">The most active named vendors, by market (curated footprint plus signal mentions). Darker = stronger presence.</div></div></div>`;
  const wrapT=el("div","tablewrap");
  const t=el("table","matrix");
  t.innerHTML=`<thead><tr><th>Market</th>${DASH.active_vendors.map(v=>`<th>${esc(v.split(' ')[0])}</th>`).join("")}</tr></thead>`;
  const tb=el("tbody"); const maxv=4;
  DASH.matrix.forEach(r=>{
    const tr=el("tr"); let cells=`<td><b>${esc(r.name)}</b></td>`;
    DASH.active_vendors.forEach(v=>{ const val=r.cells[v]||0;
      const a=val?(0.18+0.82*Math.min(val,maxv)/maxv):0;
      cells+=`<td>${val?`<span class="cell" style="background:rgba(226,113,94,${a.toFixed(2)})">${val}</span>`:'<span class="muted">·</span>'}</td>`; });
    tr.innerHTML=cells; tb.appendChild(tr);
  });
  t.appendChild(tb); wrapT.appendChild(t); mw.appendChild(wrapT); s.appendChild(mw);
}

/* ----------------------------------------------------------------- ACCOUNTS + REGULATORY */
function renderAccounts(s){
  s.innerHTML="";
  const rc=el("div","card");
  rc.innerHTML=`<div class="hd"><div><h2>Regulatory deadlines</h2><div class="desc">Deadlines that force banks to spend. Banks usually commit budget 6–12 months before a date, so the countdown is the buying window. Red = within 60 days, amber = within 6 months.</div></div></div>`;
  const tl=el("div","tl");
  DASH.deadlines.forEach(d=>{
    const it=el("div","tl-item "+d.bucket);
    const cd = d.days_until<0 ? `${-d.days_until}d ago` : `in ${d.days_until}d`;
    it.innerHTML=`<div class="tl-when"><div class="d">${esc(d.date)}</div><div class="c">${cd} · ${esc(d.type)}</div></div>
      <div class="tl-body"><b>${esc(d.title)}</b>
        <div class="small muted" style="margin-top:2px">${d.geo_names.map(esc).join(", ")}</div>
        <div class="small" style="margin-top:5px">${linkify(d.forces)}</div>
        <div style="margin-top:6px">${(d.products||[]).map(p=>'<span class="pp" style="border-color:'+(PCOL[p]||'#E7DDC9')+'">'+esc(DASH.prod_label[p]||p)+'</span>').join('')}</div>
        ${sourceLine(d.source, field(d,['url','link']))}</div>`;
    tl.appendChild(it);
  });
  rc.appendChild(tl); s.appendChild(rc);

  const ac=el("div","card");
  ac.innerHTML=`<div class="hd"><div><h2>Account targets</h2><div class="desc">Bank-specific signals, each with the reason to act now and a recommended action. Rank by most recent development, largest deal size, or most independent confirmations. Filter by market, product or confidence, or switch to new-only.</div></div></div>`;
  const ctrl=el("div","controls");
  const csel=el("select"); csel.innerHTML=`<option value="">All markets</option>`+DASH.countries.filter(c=>c.n_signals).map(c=>`<option value="${c.code}">${esc(c.name)}</option>`).join("");
  const psel=el("select"); psel.innerHTML=`<option value="">All products</option>`+DASH.products.filter(p=>p.n_signals).map(p=>`<option value="${p.id}">${esc(p.label)}</option>`).join("");
  const fsel=el("select"); fsel.innerHTML=`<option value="">Any confidence</option><option>High</option><option>Medium-High</option><option>Medium</option>`;
  const newt=el("label","toggle"); const cb=el("input"); cb.type="checkbox"; newt.appendChild(cb); newt.appendChild(document.createTextNode("New this week only"));
  const ssel=el("select"); ssel.innerHTML=`<option value="recent">Sort: most recent</option><option value="value">Sort: largest deal size</option><option value="agents">Sort: most corroborated</option>`;
  const q=el("input"); q.type="search"; q.placeholder="search bank / theme…"; q.setAttribute("aria-label","Search bank or theme");
  ctrl.append(csel,psel,fsel,ssel,newt,q); ac.appendChild(ctrl);
  const list=el("div"); ac.appendChild(list); s.appendChild(ac);
  function draw(){
    list.innerHTML="";
    let rows=DASH.account_targets.map(k=>sigByKey[k]).filter(Boolean);
    if(csel.value) rows=rows.filter(r=>r.countries.includes(csel.value));
    if(psel.value) rows=rows.filter(r=>r.products.includes(psel.value));
    if(fsel.value) rows=rows.filter(r=>r.confidence===fsel.value);
    if(cb.checked) rows=rows.filter(r=>r.is_new_this_week);
    if(q.value.trim()){ const x=q.value.toLowerCase(); rows=rows.filter(r=>(r.bank_theme+r.signal+r.implies).toLowerCase().includes(x)); }
    const cmp={
      recent:(a,b)=> String(sortDate(b)).localeCompare(String(sortDate(a))) || (potEur(b.size_band)-potEur(a.size_band)),
      value:(a,b)=> (potEur(b.size_band)-potEur(a.size_band)) || String(sortDate(b)).localeCompare(String(sortDate(a))),
      agents:(a,b)=> ((b.agents||[]).length-(a.agents||[]).length) || (potEur(b.size_band)-potEur(a.size_band)) };
    rows.sort(cmp[ssel.value]||cmp.recent);
    if(!rows.length){ list.appendChild(el("div","empty","No matching signals.")); return; }
    rows.forEach(r=>list.appendChild(sigCard(r)));
  }
  [csel,psel,fsel,ssel].forEach(e=>e.onchange=draw); cb.onchange=draw; q.oninput=draw; draw();
}

// break a dense evidence paragraph into scannable bullets — split on sentence/clause boundaries that aren't
// inside a figure (so "EUR1.59tn" / "-1.8%" don't split). Falls back to a single line if it doesn't segment.
// Which of a pattern's sources backs a given point of evidence. The sources are listed per pattern, not
// per point, so this matches on the distinctive words of each source's own title — "RBR", "SPACE",
// "Data Portal", a year. A word that appears in EVERY source of that pattern tells us nothing, so it
// scores nothing. Below the threshold no source is shown: a wrong attribution is worse than none, and
// the full list still appears under "Based on".
const _CITE_STOP=new Set(['the','and','for','with','from','into','across','over','end','eu','atm','atms','cash','market','markets','report','reports','series','data','study','index','edition','table','tables','figure','figures','page','pages']);
function citeTokens(t){
  return new Set(String(t||'').toLowerCase().match(/[a-z][a-z0-9&\-]{2,}|\b(?:19|20)\d{2}\b/g)?.filter(w=>!_CITE_STOP.has(w))||[]);
}
function sourcesFor(point, cits){
  if(!cits||cits.length<2) return [];
  const toks=cits.map(c=>citeTokens(c&&c.text));
  const df={}; toks.forEach(set=>set.forEach(w=>{ df[w]=(df[w]||0)+1; }));
  const hay=' '+String(point||'').toLowerCase()+' ';
  const scored=cits.map((c,i)=>{
    let score=0;
    toks[i].forEach(w=>{
      if(df[w]===cits.length) return;                       // in every source: not distinctive
      if(!new RegExp('(?:^|[^a-z0-9])'+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?:[^a-z0-9]|$)').test(hay)) return;
      score += (w.length>=4?2:1) / df[w];                    // rarer across the sources counts for more
    });
    return {c, score};
  }).filter(x=>x.score>=2).sort((a,b)=>b.score-a.score);
  return scored.slice(0,2).map(x=>x.c);
}
// One bullet per point of evidence, as before. The rewritten evidence is written in paragraphs, and a
// paragraph is a group of points that share a source — so the bullets stay fine-grained (one sentence
// each) and the source line sits once under the group, rather than repeating under every bullet.
function evPoints(t){
  const re=/[.;]\s+(?=[A-Z(])/g; let parts=[], last=0, m;
  while((m=re.exec(t))){ if(/\d/.test(t[m.index-1])) continue; parts.push(t.slice(last,m.index)); last=m.index+m[0].length; }
  parts.push(t.slice(last));
  return parts.map(x=>x.replace(/^[;.\s]+/,'').replace(/\s+$/,'').trim()).filter(x=>x.length>2);
}
function evidenceBlock(text, cits){
  let t=String(text==null?'':text).trim(); if(!t) return '';
  const groups=t.split(/\n\s*\n/).map(x=>x.trim()).filter(x=>x.length>2).map(g=>({text:g, points:evPoints(g)}));
  const total=groups.reduce((a,g)=>a+g.points.length,0);
  if(total<2) return `<div class="k">Evidence</div><div class="ol-why">${linkify(t)}</div>`;
  // each group is wrapped so a rule down its left edge shows at a glance which bullets share a source
  const body=groups.map(g=>{
    const f=sourcesFor(g.text,cits);                       // matched on the whole group, not one sentence
    return `<div class="ev-group${f.length?' ev-group-src':''}">`
         + `<ul class="ev-list">${g.points.map(it=>`<li>${linkify(it)}</li>`).join('')}</ul>`
         + (f.length?`<div class="ev-src">Source: ${citeLinks(f)}</div>`:'')
         + `</div>`;
  }).join('');
  return `<div class="ol-drivers"><div class="k">Evidence</div>${body}</div>`;
}
// render official pattern citations ([{text,url}]) as web links: public http(s) open in a new tab; the
// /api/evidence endpoint (Blob-served, e.g. the licensed RBR PDF) opens the in-app viewer; bare text stays text.
function citeLinks(cits){
  return (cits||[]).map(c=>{ const u=(c&&c.url)||'', t=(c&&c.text)||'';
    if(/^https?:\/\//i.test(u)) return `<a class="link" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(t||prettyUrl(u))}</a>`;
    if(u.indexOf('/api/evidence')===0) return `<a class="link" href="${esc(u)}">${esc(t||'source')}</a>`;
    return t?esc(t):''; }).filter(Boolean).join(' &middot; ');
}

/* ----------------------------------------------------------------- ALL SIGNALS
   The unfiltered record. Every other tab is a CUT of the signal set (opportunities, accounts,
   per-country, per-product); this is the set itself, including the macro/threat rows that carry the
   market trend but are deliberately kept out of every ranking. Read-the-market view, not a pipeline. */
function renderSignals(s){
  s.innerHTML="";
  const all=(DASH.signals||[]).slice();
  const card=el("div","card");
  const nBy=l=>all.filter(g=>(g.lane||'opportunity')===l).length;
  card.innerHTML=`<div class="hd"><div><h2>All signals this week</h2><div class="desc">All <b>${all.length}</b> signals in the table — <b>${nBy('opportunity')}</b> open opportunities, <b>${nBy('installed_base')}</b> already held, <b>${nBy('lost')}</b> competitor-won, <b>${nBy('context')}</b> market context. The other tabs each show a cut of this list; nothing is left out here. Click any card for the evidence, the date it broke and the recommended follow-up.</div></div></div>`;
  const ctrl=el("div","controls");
  const csel=el("select"); csel.innerHTML=`<option value="">All markets</option>`+DASH.countries.filter(c=>c.n_signals).map(c=>`<option value="${c.code}">${esc(c.name)}</option>`).join("")+`<option value="__fw__">Footprint-wide</option>`;
  const psel=el("select"); psel.innerHTML=`<option value="">All products</option>`+DASH.products.filter(p=>p.n_signals).map(p=>`<option value="${p.id}">${esc(p.label)}</option>`).join("");
  const lsel=el("select"); lsel.innerHTML=`<option value="">Every lane</option>`+Object.keys(LANE_LABEL).map(l=>`<option value="${l}">${LANE_LABEL[l]}</option>`).join("");
  const fsel=el("select"); fsel.innerHTML=`<option value="">Any confidence</option><option>High</option><option>Medium-High</option><option>Medium</option><option>Low</option>`;
  const ssel=el("select"); ssel.innerHTML=`<option value="recent">Sort: most recent</option><option value="value">Sort: largest deal size</option><option value="agents">Sort: most corroborated</option><option value="market">Sort: by market</option>`;
  const newt=el("label","toggle"); const cb=el("input"); cb.type="checkbox"; newt.appendChild(cb); newt.appendChild(document.createTextNode("New this week only"));
  const q=el("input"); q.type="search"; q.placeholder="search bank / theme / evidence…"; q.setAttribute("aria-label","Search signals");
  ctrl.append(csel,psel,lsel,fsel,ssel,newt,q); card.appendChild(ctrl);
  const count=el("div","desc"); count.style.padding="2px 2px 6px"; card.appendChild(count);
  const list=el("div"); card.appendChild(list); s.appendChild(card);
  function draw(){
    list.innerHTML="";
    let rows=all;
    if(csel.value==='__fw__') rows=rows.filter(r=>!(r.countries||[]).length||r.footprint_wide);
    else if(csel.value) rows=rows.filter(r=>(r.countries||[]).includes(csel.value));
    if(psel.value) rows=rows.filter(r=>(r.products||[]).includes(psel.value));
    if(lsel.value) rows=rows.filter(r=>(r.lane||'opportunity')===lsel.value);
    if(fsel.value) rows=rows.filter(r=>r.confidence===fsel.value);
    if(cb.checked) rows=rows.filter(r=>r.is_new_this_week);
    if(q.value.trim()){ const x=q.value.toLowerCase();
      rows=rows.filter(r=>(r.bank_theme+r.signal+r.implies+r.follow_up+(r.source||'')).toLowerCase().includes(x)); }
    const cmp={
      recent:(a,b)=> String(sortDate(b)).localeCompare(String(sortDate(a))) || (potEur(b.size_band)-potEur(a.size_band)),
      value:(a,b)=> (potEur(b.size_band)-potEur(a.size_band)) || String(sortDate(b)).localeCompare(String(sortDate(a))),
      agents:(a,b)=> ((b.agents||[]).length-(a.agents||[]).length) || String(sortDate(b)).localeCompare(String(sortDate(a))),
      market:(a,b)=> String(ctryNames(a)).localeCompare(String(ctryNames(b))) || String(sortDate(b)).localeCompare(String(sortDate(a)))};
    rows=rows.slice().sort(cmp[ssel.value]||cmp.recent);
    count.innerHTML=`Showing <b>${rows.length}</b> of ${all.length} signals.`;
    if(!rows.length){ list.appendChild(el("div","empty","No signals match these filters.")); return; }
    rows.forEach(r=>list.appendChild(sigCard(r)));
  }
  [csel,psel,lsel,fsel,ssel].forEach(e=>e.onchange=draw); cb.onchange=draw; q.oninput=draw; draw();

  if((DASH.derived||[]).length) s.appendChild(derivedSection(DASH.derived));
}

/* ----------------------------------------------------------------- PATTERNS / HISTORY */
function renderPatterns(s){
  s.innerHTML="";
  // No single wrapping "Structural patterns" card (per request, 08/09/2026) — the page title/subtitle
  // already frame the tab. Each theme gets its OWN container instead, so the categories read as
  // separate blocks rather than one long scroll inside a single card.
  const GROUP_ORDER=['Cash & ATM economics','Branches & channel shift','Operating model & vendor landscape','Payments & regulation','Digital & identity','Macro & country divergence','Procurement & demand cadence'];
  const byGroup={}; DASH.patterns.forEach(p=>{ const g=p['Group']||'Other'; (byGroup[g]=byGroup[g]||[]).push(p); });
  const groups=GROUP_ORDER.filter(g=>byGroup[g]).concat(Object.keys(byGroup).filter(g=>GROUP_ORDER.indexOf(g)<0));
  let n=0;
  groups.forEach(g=>{
    const gc=el("div","card");
    gc.innerHTML=`<div class="hd tight"><div><h2>${esc(g)}</h2></div><span class="pat-group-n">${byGroup[g].length}</span></div>`;
    byGroup[g].forEach(p=>{
      n++;
      const vals=Object.values(p);
      const pat=vals[1]||'', ev=vals[2]||'', means=vals[3]||'', conf=vals[4]||'', src=p['Source']||p['Sources']||'', cits=p['Citations']||[];
      // Direction + rate as the PATTERN states them. Both come from the patterns file; neither is
      // inferred here. A rate is shown only when the pattern's own headline claims one — reading a
      // percentage out of the evidence would promote a supporting statistic to a headline claim.
      const PATDIR={up:['▲','pat-up','grows'],down:['▼','pat-down','shrinks'],
                    flat:['▬','pat-flat','holds'],mixed:['◆','pat-mixed','cuts both ways']};
      const _d=PATDIR[String(p['Direction']||'').toLowerCase()];
      const _rate=String(p['Rate']||'').trim()
        || ((String(pat).match(/~?\s*[+-]?\d+(?:\.\d+)?\s*(?:[-–]\s*\d+(?:\.\d+)?\s*)?%\s*\/\s*(?:yr|year)/i)||[''])[0].trim());
      const _chip=(_d||_rate)
        ? `<span class="pat-trend ${_d?_d[1]:'pat-flat'}" title="${_d?`This mechanic ${_d[2]} the market`:'The rate this pattern claims'}${_rate?` — the pattern states ${esc(_rate)}`:''}">${_d?_d[0]:''}${_rate?`<span class="pat-rate">${esc(_rate)}</span>`:''}</span>`
        : '';
      const based=cits.length?citeLinks(cits):(src?linkify(src):'');
      const det=el("details","reason-card pat-card");
      det.id='pattern-'+n;                       // jump target for "See Pattern #n" links elsewhere
      det.dataset.pat=String(pat).slice(0,60).toLowerCase();
      det.innerHTML=`<summary class="rc-sum"><div class="rc-head"><b class="ol-scope"><span class="pat-num">Pattern #${n}</span> ${esc(pat)}</b>${_chip}<span class="rc-chev" aria-hidden="true"></span></div>${means?`<div class="ol-h">What does this mean for Printec?</div><div class="ol-proj">${linkify(means)}</div>`:''}</summary>`;
      const body=el("div","fc-body");
      body.innerHTML=`${evidenceBlock(ev,cits)}${conf?`<div class="fc-conf"><span class="small muted">Confidence in this pattern:</span> <span class="pill ${esc(conf)}">${esc(conf)}</span></div>`:''}${based?`<div class="ol-evidence"><div class="ol-srcline"><span class="ol-evk">Based on</span> ${based}</div></div>`:''}`;
      det.appendChild(body);
      gc.appendChild(det);
    });
    s.appendChild(gc);
  });
}

/* ----------------------------------------------------------------- OUTLOOK (forecasts) */
function fmtNum(n){ return (typeof n==='number') ? n.toLocaleString('en-US',{maximumFractionDigits:0}) : esc(n); }
// which structural metric(s) a reasoned outlook is actually ABOUT — judged from its scope/title + the
// projection headline ONLY (not the rationale, which often references other calls e.g. "subordinate to the
// ATM-mandate lines"). So we attach a chart only when it matches the insight; a payments/compliance call
// that has no chartable structural series gets none rather than an unrelated ATMs/branches plot.
function outlookMetrics(o){
  const t=((o.scope||'')+' '+(o.projected||'')).toLowerCase();
  const out=new Set();
  if(/\batms?\b|self[- ]?service|cash recycl|recycler|cash automation|cash machine|\bbranch|branch network|network rationali/.test(t)){ out.add('atm'); out.add('branch'); }
  if(/\bpos\b|point[- ]of[- ]sale|acquir|merchant|card payment|payment terminal|soft[- ]?pos|terminal estate/.test(t)) out.add('pos');
  if(/cash withdrawal|cash usage|cash in circulation|cash-in-circulation|cash resilien|cash demand/.test(t)) out.add('cash');
  return [...out];
}
function renderOutlook(s){
  s.innerHTML="";
  const fc=DASH.forecast||[], outlook=DASH.outlook||[], cov=DASH.forecast_coverage||[];
  const cid = c => 'fc_'+String(c).replace(/[^a-z0-9]/gi,'');
  let olN=0;

  // The page title and subtitle already frame this tab. The section header, the intro line on the first
  // product card and the baseline-accuracy pill were all removed on request (08-09/09/2026): the cards
  // open straight onto the product lines.

  // === product lines: where each one is heading across the footprint ===
  const prodOl=(DASH.product_outlooks&&DASH.product_outlooks.length)?DASH.product_outlooks:(window.PRODUCT_OUTLOOKS||[]);
  if(prodOl.length){
    prodOl.forEach(o=>{
      const card=el("div","card");
      const tag=o.m!=null?`<span class="tag" title="Current opportunity value across the footprint">€${o.m}m</span>`:'';
      card.innerHTML=`<div class="hd tight"><div class="prodhead"><span class="swatch" style="background:${PCOL[o.id]||'#23C0E2'}"></span><h2>${esc(o.label)}</h2>${tag}</div></div>`;
      card.appendChild(reasonCard(o,{product:true}));
      s.appendChild(card);
    });
  }

  // === reasoned outlooks by market — opportunities (winnable net-new) lead; owned/lost routed below ===
  if(outlook.length){
    // render one "<Country> — outlook" card (keeps the lazy structural-chart wiring)
    const olName=c=>(c==='EU'?'Footprint-wide':(DASH.code2name[c]||c));
    const olScore=c=>{ const r=(DASH.countries||[]).find(x=>x.code===c); return r?r.score:-1; };
    const renderCountryCard=(country,items,host)=>{
      // each market opens collapsed (asked 10/09/2026): the header shows the name, the deal value and
      // how many calls sit inside; click it to reveal them
      const card=el("details","card ol-market-fold");
      const _sc=olScore(country);
      card.innerHTML=`<summary class="hd tight ol-market-sum"><div><h2>${esc(olName(country))} — outlook</h2></div>`
        +`<span class="ol-market-meta">${_sc>=0?`<span class="tag" title="Total deal value in this market, from the Countries tab">€${_sc}m</span>`:''}`
        +`<span class="tag quiet">${items.length} call${items.length===1?'':'s'}</span></span></summary>`;
      items.forEach(o=>{
        let chartHtml='', oid=null, cfs=null, overlays=[];
        const mk=outlookMetrics(o);
        if(mk.length){
          cfs=fc.filter(f=>f.country===country && mk.some(k=>new RegExp(k,'i').test(f.metric))).slice(0,2);
          if(cfs.length){
            oid='ol_'+(country+'_'+(olN++)).replace(/[^a-z0-9]/gi,'');
            overlays=(DASH.outlook_overlays||[]).filter(ov=>ov.country===country && cfs.some(f=>f.metric===ov.metric));
            chartHtml=`<div class="desc" style="margin-top:9px">Structural backdrop for this call — solid = recorded · ◇ = provisional · bold = the analyst's reasoned projection:</div><div class="chart-panel" style="margin-top:6px"><div class="chartbox"><canvas id="${oid}"></canvas></div></div><div class="small muted evsrc">Source: dated market workbook + ECB series; analyst projection overlaid.</div>`;
          }
        }
        card.appendChild(reasonCard(o,{chartHtml, onExpand:(oid&&cfs)?()=>drawBaselineChart(oid,cfs,overlays):null}));
      });
      (host||s).appendChild(card);
    };
    // Group by market. Order by deal size or by recency — the call asked for size, because "newest
    // first" buries a large market that simply had a quiet week (strategy call, 23:23).
    const odate=o=>String(o.dev_date||'');
    const groupAndRender=(list,host,mode)=>{
      const byC={}; list.forEach(o=>{ (byC[o.country]=byC[o.country]||[]).push(o); });
      Object.values(byC).forEach(arr=>arr.sort((a,b)=>odate(b).localeCompare(odate(a))));
      const keys=Object.keys(byC).sort(mode==='size'
        ? (a,b)=>(olScore(b)-olScore(a)) || odate(byC[b][0]).localeCompare(odate(byC[a][0]))
        : (a,b)=>odate(byC[b][0]).localeCompare(odate(byC[a][0])));
      keys.forEach(c=>renderCountryCard(c,byC[c],host));
      return keys.length;
    };
    const oppOl=outlook.filter(o=>(o.lane||'opportunity')==='opportunity');
    const ctxOl=outlook.filter(o=>(o.lane||'opportunity')!=='opportunity');
    const lead2=el("div","card sec-head "+secHeadColor('ol-market'));
    lead2.innerHTML=`<span class="blob"></span><div class="hd"><div><h2>Near-term opportunities by market</h2><div class="desc">The most concrete <b>winnable, new</b> opportunities in each market — named tenders and bank programmes Printec does not already hold. Positions already held and deals competitors won are shown separately below.</div></div></div>`;
    s.appendChild(lead2);
    const olFlt=el("div","tablefilters");
    const olMkts=[...new Set(outlook.map(o=>o.country))].sort((a,b)=>olName(a).localeCompare(olName(b)));
    olFlt.innerHTML=`<label>Market <select id="olC"><option value="">All markets</option>${olMkts.map(c=>`<option value="${esc(c)}">${esc(olName(c))}</option>`).join('')}</select></label>
      <label>Order <select id="olS"><option value="size">Largest market first</option><option value="date">Newest development first</option></select></label>`;
    s.appendChild(olFlt);
    const olCount=el("div","desc"); olCount.style.padding="0 2px 10px"; s.appendChild(olCount);
    const hostOpp=el("div"); s.appendChild(hostOpp);
    const lead3=el("div","card sec-head "+secHeadColor('ol-market'));
    lead3.innerHTML=`<span class="blob"></span><div class="hd"><div><h2>Positions held and deals lost</h2><div class="desc">Positions Printec <b>already holds</b> (to defend and grow) and deals a <b>named competitor</b> won or holds the valuable part of. Kept for context, <b>not</b> as near-term opportunities to win.</div></div></div>`;
    const hostCtx=el("div");
    s.appendChild(lead3); s.appendChild(hostCtx);
    function olDraw(){
      const cF=$("#olC").value, mode=$("#olS").value;
      const opp=cF?oppOl.filter(o=>o.country===cF):oppOl;
      const ctx=cF?ctxOl.filter(o=>o.country===cF):ctxOl;
      hostOpp.innerHTML=""; hostCtx.innerHTML="";
      olCount.innerHTML=`Showing <b>${opp.length}</b> of ${oppOl.length} opportunities`+(cF?` in ${esc(olName(cF))}`:` across ${new Set(oppOl.map(o=>o.country)).size} markets`)+`.`;
      if(opp.length) groupAndRender(opp,hostOpp,mode);
      else hostOpp.appendChild(el("div","card","<div class='empty'>No clean net-new contest"+(cF?" in "+esc(olName(cF)):" surfaced this week")+".</div>"));
      lead3.style.display = ctx.length ? "" : "none";
      if(ctx.length) groupAndRender(ctx,hostCtx,mode);
    }
    $("#olC").onchange=olDraw; $("#olS").onchange=olDraw; olDraw();
  } else {
    s.appendChild(el("div","card","<div class='empty'>No outlooks yet. The weekly orchestrator writes them from the signals and the baselines.</div>"));
  }

  // (Removed the "Data coverage" card — a verbose per-metric coverage dump, low reader value.)

}


/* ----------------------------------------------------------------- CHARTS (own tab; was "Statistical baselines")
   Moved out of the Outlook tab on the strategy call of 04/09/2026: the outlooks there are a 6-12 month
   read, while these are annual series on their own clock, and stacking them under one heading made the
   tab long and the horizon ambiguous. The tab opens EMPTY on purpose — pick a market on the map and a
   metric, and only then does a chart appear. The full table stays below, sorted by trend, because
   scanning every market by trend is the one genuinely useful cross-market view. */
// The pooled reading for next year (project_lines.py consensus): the mean and spread of every
// projection drawn on the chart, each stated as the change per year from the last completed year.
// Asked on 09/09/2026 — the map and the table used the fitted trend alone, which is one source.
function blRunYearSafe(){ return parseInt(String(DASH.week||'').slice(0,4))||new Date().getFullYear(); }
function blCons(f){ return (DASH.projection_consensus||[]).find(c=>c.country===f.country&&c.metric===f.metric)||null; }
function pctTxt(v){ return (v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'%'; }
function consShort(c){ return c ? pctTxt(c.mean_pct)+(c.std_pct!=null?' \u00b1 '+c.std_pct.toFixed(1)+'%':'')+' \u00b7 '+c.n+' reading'+(c.n>1?'s':'') : 'no projection'; }
function consTitle(c){ return c ? c.readings.map(r=>r.name+' '+pctTxt(r.growth_pct)).join(' \u00b7 ') : ''; }
function consHtml(c,f){
  if(!c) return '';
  const rows=c.readings.map(r=>`<div class="bl-cons-row"><span class="bl-cons-name">${esc(r.name)}</span><span class="bl-cons-val">${esc(String(c.year))}: ${fmtNum(r.value)}</span><span class="bl-cons-g ${r.growth_pct>=0?'up':'down'}">${pctTxt(r.growth_pct)} a year</span></div>`).join('');
  const spread=c.std_pct!=null?` The readings sit <b>\u00b1 ${c.std_pct.toFixed(1)} points</b> apart (one standard deviation), from ${pctTxt(c.low_pct)} to ${pctTxt(c.high_pct)}.`:' Only one projection reaches this year, so there is no spread to report.';
  return `<div class="bl-cons"><div class="bl-k">Outlook for ${esc(String(c.year))}: all projections pooled</div>
    <div class="bl-cons-head"><span class="bl-cons-big ${c.mean_pct>=0?'up':'down'}">${pctTxt(c.mean_pct)}</span><span class="bl-cons-unit">a year, on average</span>${c.std_pct!=null?`<span class="bl-cons-sd">\u00b1 ${c.std_pct.toFixed(1)}%</span>`:''}<span class="bl-cons-n">${c.n} reading${c.n>1?'s':''}</span></div>
    <div class="small bl-cons-txt">Each projection starts from the last reported point (${esc(String(c.anchor_year))}: ${fmtNum(c.anchor_value)}${c.anchor_n>1?`, the mean of ${c.anchor_n} readings for that year`:''}) and is measured to its ${esc(String(c.year))} value, as a change per year. The mean is the figure shown on the map and in the table.${spread}</div>
    <div class="bl-cons-rows">${rows}</div></div>`;
}

function renderBaselines(s){
  s.innerHTML="";
  const fc=DASH.forecast||[];
  if(!fc.length){ s.appendChild(el("div","card","<div class='empty'>No baseline series in this build.</div>")); return; }

  // the picker offers only metrics recorded for two or more markets (asked 10/09/2026): a metric with
  // one market makes no map. Single-market series stay in the table below, where a row can be charted.
  const _cnt={}; fc.forEach(f=>{ (_cnt[f.metric]=_cnt[f.metric]||new Set()).add(f.country); });
  const metrics=[...new Set(fc.map(f=>f.metric))].filter(m=>_cnt[m].size>=2).sort();
  const byKey=(c,m)=>fc.find(f=>f.country===c&&f.metric===m);
  // Opens on a real series rather than an empty frame: Greece / ATMs is the longest, densest row in
  // the build (11 recorded years), so the three lines and the 2027 star all have something to show.
  let selM=metrics.includes('ATMs')?'ATMs':metrics[0];
  let selC=byKey('Greece',selM)?'Greece':(fc.find(f=>f.metric===selM)||{}).country||null;

  // ---- picker: metric dropdown, then map on the left and the chart beside it ---------------------
  const pick=el("div","card");
  // metric picker and market picker side by side (market added 10/09/2026); the map click still works
  pick.innerHTML=`<div class="hd tight"><div><h2>Pick a metric and a market</h2></div></div>
    <div class="bl-pickers">
      <label class="bl-mselect"><span class="bl-plabel">Metric</span><select id="blMetric" aria-label="Metric">${metrics.map(m=>`<option${m===selM?' selected':''}>${esc(m)}</option>`).join('')}</select></label>
      <label class="bl-mselect"><span class="bl-plabel">Market</span><select id="blCountry" aria-label="Market"></select></label>
    </div>`;
  // map first, chart underneath it (09/09/2026) — a full-width chart has room for the years and the
  // legend, which a half-width column did not
  const split=el("div","bl-stack");
  const mapHost=el("div","bl-maphost"); const chartHost=el("div","bl-chartcol");
  split.appendChild(mapHost); split.appendChild(chartHost);
  pick.appendChild(split);
  s.appendChild(pick);

  // ---- the reading of the selected series, INSIDE the same container, under the map and chart -------
  const chartCard=el("div","bl-reading"); pick.appendChild(chartCard);

  // diverging scale: blue = growing, red = shrinking, warm neutral = no series for this metric.
  const HX=h=>{h=h.replace('#','');return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)];};
  const LERP=(a,b,t)=>{const A=HX(a),B=HX(b);return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*t).toString(16).padStart(2,'0')).join('');};
  const NODATA='#E6DECE', MID='#F0EFEC';
  function shade(cagr,span){ if(cagr==null) return NODATA;
    const t=Math.min(1,Math.sqrt(Math.abs(cagr)/(span||1)));
    return cagr>=0 ? LERP(MID,'#2e9e4f',t) : LERP(MID,'#e34948',t); }

  function paintMap(){
    const MAP=window.FOOTPRINT_MAP;
    const rows=fc.filter(f=>f.metric===selM);
    const cagrByCode={}, consByCode={};
    rows.forEach(f=>{ const code=Object.keys(DASH.code2name).find(k=>DASH.code2name[k]===f.country);
      const c=blCons(f); if(code&&c){ cagrByCode[code]=c.mean_pct; consByCode[code]=c; } });
    const _yr=(rows.map(blCons).find(Boolean)||{}).year||(blRunYearSafe()+1);
    const span=Math.max(1,...Object.values(cagrByCode).map(v=>Math.abs(v||0)));
    if(!MAP){
      mapHost.innerHTML='';
      const wrap=el("div","bl-nomap");
      Object.keys(cagrByCode).sort((a,b)=>(cagrByCode[b]||0)-(cagrByCode[a]||0)).forEach(code=>{
        const b=el("button","map-fw"); b.type='button';
        b.textContent=`${DASH.code2name[code]} ${consShort(consByCode[code])}`;
        b.addEventListener('click',()=>{ selC=DASH.code2name[code]; draw(); }); wrap.appendChild(b); });
      mapHost.appendChild(wrap); return;
    }
    const paths=Object.entries(MAP.countries).map(([code,c])=>{
      const has=code in cagrByCode, v=cagrByCode[code];
      const lbl=has?`${selM}, ${_yr} outlook: ${consShort(consByCode[code])} a year`:`no ${selM} series`;
      return `<path class="fmap-c${has?' has':''}" data-code="${code}" d="${c.d}" fill="${shade(has?v:null,span)}" aria-label="${esc(DASH.code2name[code]||code)}: ${esc(lbl)}"></path>`;
    }).join('');
    // legend first: it is the map column's "caption row", the same height as the chart's caption,
    // so the map and the chart start on the same line and share the same height
    mapHost.innerHTML=`<div class="map-legend"><span class="mlk" title="The mean of every projection for ${_yr}, stated as a change per year">${esc(selM)}: ${_yr} outlook, mean of all projections</span><span>shrinking</span><span class="bl-grad"></span><span>growing</span><span class="mlk2"><span class="msw"></span> no series</span></div>
      <div class="map-wrap"><svg class="fmap" viewBox="${MAP.viewBox}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${esc(selM)}: ${_yr} outlook per year across the footprint, mean of all projections"><path class="fmap-ctx" d="${MAP.context}"></path>${outsidePaths(MAP)}${paths}</svg><div class="map-tip" hidden></div></div>`;
    const tip=mapHost.querySelector('.map-tip'), wrap=mapHost.querySelector('.map-wrap');
    mapHost.querySelectorAll('.fmap-c').forEach(p=>{ const code=p.dataset.code, has=code in cagrByCode, v=cagrByCode[code];
      p.addEventListener('mousemove',e=>{ const r=wrap.getBoundingClientRect();
        tip.innerHTML=`<b>${esc(DASH.code2name[code]||code)}</b><br>${has?`${esc(selM)}, ${_yr}: ${esc(consShort(consByCode[code]))} a year<br><span class="muted">${esc(consTitle(consByCode[code]))}</span>`:`no ${esc(selM)} series`}`;
        tip.style.left=(e.clientX-r.left)+'px'; tip.style.top=(e.clientY-r.top)+'px'; tip.hidden=false; });
      p.addEventListener('mouseleave',()=>{ tip.hidden=true; });
      if(has) p.addEventListener('click',()=>{ selC=DASH.code2name[code]; draw(); }); });
    if(selC){ const sc=Object.keys(DASH.code2name).find(k=>DASH.code2name[k]===selC);
      const pe=mapHost.querySelector(`.fmap-c[data-code="${sc}"]`); if(pe) pe.classList.add('sel'); }
  }

  // the market list follows the metric: only markets with a recorded series for it
  function fillCountries(){
    const sel=$("#blCountry"); if(!sel) return;
    const cs=[...new Set(fc.filter(f=>f.metric===selM).map(f=>f.country))].sort();
    sel.innerHTML=`<option value="">Choose a market</option>`+cs.map(c=>`<option${c===selC?' selected':''}>${esc(c)}</option>`).join('');
  }
  function draw(){
    fillCountries();
    paintMap();
    // every redraw replaces the canvas, so retire any Chart still bound to a detached one
    charts=charts.filter(c=>{ if(c&&c.canvas&&!document.body.contains(c.canvas)){ try{c.destroy();}catch(e){} return false; } return true; });
    const f=selC?byKey(selC,selM):null;
    if(!f){
      chartHost.innerHTML=`<div class="bl-empty"><div class="bl-empty-h">${selC?`No ${esc(selM)} series for ${esc(selC)}`:'Nothing charted yet'}</div>`
        +`<div class="bl-empty-b">${selC?`${esc(selC)} has no recorded ${esc(selM)} series, so there is nothing to fit. Pick another metric, or another market.`:`Click a market on the map to chart its <b>${esc(selM)}</b>.`}</div></div>`;
      chartCard.innerHTML=`<div class="bl-empty"><div class="bl-empty-b">Pick a market with a recorded ${esc(selM)} series to see how the number was made, the three projections and the signals behind them.</div></div>`;
      return;
    }
    const cid='blmain_'+(f.country+'_'+f.metric).replace(/[^a-z0-9]/gi,'');
    // the full wording of the unit sits under the title when it says more than the axis can — e.g. that
    // Albania's "million lek" is cash in circulation, not withdrawals
    const _un=(f.unit_note&&f.unit&&String(f.unit_note).trim()!==String(f.unit).trim())?`<span class="muted small">${esc(f.unit_note)}</span>`:'';
    chartHost.innerHTML=`<div class="bl-charthead"><b>${esc(f.country)} — ${esc(f.metric)}</b>${_un}</div>`
      +`<div class="chart-panel"><div class="chartbox tall"><canvas id="${cid}"></canvas></div></div>`;
    chartCard.innerHTML=consHtml(blCons(f),f);   // the pooled next-year reading first; the caption above the chart names the row
    // the three-projections panel now carries the signals list itself (under the By signals row)
    if(typeof blLinesHtml==='function'){ const x=el("div"); x.innerHTML=blLinesHtml(f); chartCard.appendChild(x); }
    drawBaselineChart(cid,[f],(DASH.outlook_overlays||[]).filter(o=>o.country===f.country&&o.metric===f.metric));
  }

  $("#blCountry").addEventListener('change',e=>{ selC=e.target.value||null; draw(); });
  $("#blMetric").addEventListener('change',e=>{
    selM=e.target.value;
    if(!byKey(selC,selM)){ const alt=fc.find(f=>f.metric===selM); selC=alt?alt.country:selC; }
    draw();
  });
  draw();

  // === the full table of series — filter, sort, click a row to chart it ===
  if(fc.length){
    const tw=el("div","card");
    // These are ANNUAL series, so their horizon is stated in full calendar years — it does not follow
    // the 6-12 month window of the analyst outlooks above. Each series ends where its data lets it:
    // one year out by default, two where the data is recent and the fit holds (see horizon_reason).
    const _cy=((DASH.projection_consensus||[])[0]||{}).year||(blRunYearSafe()+1);
    tw.innerHTML=`<div class="hd"><div><h2>All series (${fc.length})</h2><div class="desc">Every recorded series, with its outlook for ${_cy}. The outlook is the mean of all the projections we hold for that series (patterns and signals), each stated as a change per year from the last reported point, with the spread between them (\u00b1 one standard deviation). Filter or sort, and <b>click any row to chart it</b>. ◇ = provisional.</div></div></div>`;
    const cs=[...new Set(fc.map(f=>f.country))].sort(), ms=[...new Set(fc.map(f=>f.metric))].sort();
    const flt=el("div","tablefilters");
    flt.innerHTML=`<label>Market <select id="blC"><option value="">All markets</option>${cs.map(c=>`<option>${esc(c)}</option>`).join('')}</select></label>
      <label>Metric <select id="blM"><option value="">All metrics</option>${ms.map(m=>`<option>${esc(m)}</option>`).join('')}</select></label>`;
    tw.appendChild(flt);
    const wrapT=el("div","tablewrap"); const t=el("table"); t.className="bltable";
    const COLS=[['country','Market'],['metric','Metric'],['latest','Latest reported'],['trend',_cy+' outlook /yr'],['pat','By patterns '+_cy],['sig','By signals '+_cy]];
    // the two readings a row holds for the outlook year, straight from the projection lines
    const blRow=f=>{ const mine=(DASH.projection_lines||[]).filter(l=>l.country===f.country&&l.metric===f.metric);
      const pat=mine.find(l=>l.origin==='patterns'), sig=mine.find(l=>l.origin==='signals'), sp=mine.find(l=>l.origin==='signals_point');
      const patV=pat?((pat.projection||[]).find(p=>p.year===_cy)||{}).value:null;
      const sigV=sig?((sig.projection||[]).find(p=>p.year===_cy)||{}).value:null;
      return {pat:patV!=null?patV:null, sig:sigV!=null?sigV:null, rule:(sigV==null&&sp&&sp.year===_cy)?sp.value:null}; };
    t.innerHTML=`<thead><tr>${COLS.map(c=>`<th class="thsort" data-k="${c[0]}">${c[1]}</th>`).join('')}</tr></thead>`;
    const tb=el("tbody"); t.appendChild(tb); wrapT.appendChild(t); tw.appendChild(wrapT); s.appendChild(tw);
    let sk='trend', sd=-1;
    const KV={country:f=>(f.country||'').toLowerCase(),metric:f=>(f.metric||'').toLowerCase(),latest:f=>(f.anchor||{}).value||0,
      trend:f=>{ const c=blCons(f); return c?c.mean_pct:-1e9; },pat:f=>{ const r=blRow(f); return r.pat==null?-1e9:r.pat; },
      sig:f=>{ const r=blRow(f); return r.sig!=null?r.sig:(r.rule!=null?r.rule:-1e9); }};
    function render(){
      const cF=$("#blC").value, mF=$("#blM").value;
      const list=fc.filter(f=>(!cF||f.country===cF)&&(!mF||f.metric===mF))
        .sort((a,b)=>{ const va=KV[sk](a),vb=KV[sk](b); return (va>vb?1:va<vb?-1:0)*sd; });
      tb.innerHTML='';
      list.forEach(f=>{
        const h=f.history[f.history.length-1], a=f.anchor||{year:h.year,value:h.value,n:1}, _c=blCons(f), _r=blRow(f), up=(_c?_c.mean_pct:0)>=0;
        const tr=el("tr","clickable");
        tr.innerHTML=`<td><b>${esc(f.country)}</b></td><td>${esc(f.metric)}</td>
          <td class="small">${esc(a.year)}: ${fmtNum(a.value)}${a.n>1?` <span class="muted">mean of ${a.n}</span>`:''}</td>
          <td class="small" title="${esc(consTitle(_c))}">${_c?`<span style="color:${up?'var(--green-ink)':'var(--danger)'};font-weight:700">${up?'▲':'▼'} ${Math.abs(_c.mean_pct).toFixed(1)}%</span>${_c.std_pct!=null?` <span class="muted">\u00b1 ${_c.std_pct.toFixed(1)}%</span>`:''} <span class="muted">\u00b7 ${_c.n} reading${_c.n>1?'s':''}</span>`:'<span class="muted">no projection</span>'}</td>
          <td class="small">${_r.pat!=null?fmtNum(_r.pat):'<span class="muted">\u2014</span>'}</td>
          <td class="small">${_r.sig!=null?fmtNum(_r.sig):_r.rule!=null?'~'+fmtNum(_r.rule):'<span class="muted">\u2014</span>'}</td>`;
        const det=el("tr"); det.style.display="none"; const td=el("td"); td.colSpan=6;
        const cid2='bl_'+(f.country+'_'+f.metric).replace(/[^a-z0-9]/gi,'');
        td.innerHTML=`<div class="chart-panel"><div class="chartbox"><canvas id="${cid2}"></canvas></div></div><div class="small muted evsrc">Source: dated market workbook + ECB series; trend-fit by the statistics agent.</div>`;
        det.appendChild(td);
        tr.addEventListener('click',()=>{
          const closed=det.style.display==="none"; det.style.display=closed?"":"none";
          if(closed && !det.dataset.drawn){ det.dataset.drawn="1";
            drawBaselineChart(cid2,[f],(DASH.outlook_overlays||[]).filter(o=>o.country===f.country&&o.metric===f.metric)); }
        });
        tb.appendChild(tr); tb.appendChild(det);
      });
    }
    t.querySelectorAll('.thsort').forEach(th=>th.addEventListener('click',()=>{
      const k=th.dataset.k; if(sk===k) sd*=-1; else { sk=k; sd=(k==='country'||k==='metric')?1:-1; }
      t.querySelectorAll('.thsort').forEach(x=>x.classList.remove('asc','desc')); th.classList.add(sd>0?'asc':'desc'); render(); }));
    flt.querySelectorAll('select').forEach(sel=>sel.addEventListener('change',render));
    render();
  }

}

// The 3–5yr Outlook tab — the Futurist agent's long-horizon view. Leads with a board-level summary (for the
// president), then the detail in COLLAPSIBLE per-theme sections (bold summary first, expand for the calls).
// Each call keeps its citations (Based-on reports + outlookEvidence trail) and shows a chart only if it carries
// one. Reuses linkify/outlookEvidence/mkLine/mkBar. No generic count-charts.
const DIRF={'strong growth':['▲','dir-up','Strong growth'],'growth':['▲','dir-up','Growth'],'flat':['▬','dir-flat','Flat'],'decline':['▼','dir-down','Decline'],'steep decline':['▼','dir-down','Steep decline'],'mixed':['◆','dir-mixed','Mixed']};

function drawFutureChart(id,c){
  if(!c||!c.series||!c.series.length||!c.labels||!c.labels.length) return;
  if(c.type==='bar'){ mkBar(id,c.labels,((c.series[0]||{}).data)||[],'#23C0E2',(c.series[0]&&c.series[0].label)||'',!!c.horizontal); }
  else { const sets=c.series.map((x,i)=>({label:x.label,data:x.data,color:['#23C0E2','#E2715E','#7FB069','#E0B83A'][i]||'#23C0E2'})); mkLine(id,c.title||'',c.labels,sets); }
}
// Shared collapsible "reasoned projection" card — used by BOTH the Outlook (6–12 mth) and Future-outlook
// (2–5 yr) tabs so they look and behave identically. Collapsed = the high-level view: direction badge +
// scope, the gray horizon line under it, and the bold lead (projected). Expanding reveals the rationale
// ("The deterministic…"), drivers, confidence and the evidence block (outlookEvidence: Based-on report links,
// Built-on signals, evidence trail, validation note). opts: {showMarket} prepend a "▸ country" context line
// (futures, which aren't grouped by country); {chartHtml} a chart panel appended to the body; {onExpand}
// fired once on first expand to lazily draw that chart so it sizes correctly (a canvas in a collapsed
// <details> has 0×0).
// light prose formatting for the in-body product outlook: "(a)..(b).." → bullets, break before the synthesis line
function prettyProj(html){ return String(html||'').replace(/\s*\(([a-h])\)\s+/g,'<br>• ').replace(/\s+(Where to point it:|Net:|Bottom line:)/g,'<br><br><b>$1</b> '); }
function reasonCard(o, opts){
  opts=opts||{};
  const d=DIRF[(o.direction||'').toLowerCase()]||['●','dir-flat',esc(o.direction||'')];
  const conf=o.confidence?`<div class="fc-conf"><span class="small muted">Confidence in this projection:</span> <span class="pill ${esc(o.confidence)}" title="How strongly the cited research supports this projection (High, Medium-High, Medium or Low)">${esc(o.confidence)}</span></div>`:'';
  const market=(opts.showMarket && o.country)?`<div class="small muted ol-market">▸ ${esc(o.country)}</div>`:'';
  const det=el("details","reason-card");
  if(opts.product) det.classList.add('rc-product');
  // product cards: collapsed = headline + a short high-level SUMMARY (read before expanding); the body holds all detail
  const projSummary = opts.product
    ? `<div class="ol-proj ol-summary">${linkify(o.summary||o.scope||'')}</div>`
    : `<div class="ol-proj">${linkify(o.projected||'')}</div>`;
  det.innerHTML=`<summary class="rc-sum"><div class="rc-head"><span class="dirbadge ${d[1]}" title="Projected direction over the horizon">${d[0]} ${esc(d[2])}</span><b class="ol-scope">${esc(o.scope)}</b><span class="rc-chev" aria-hidden="true"></span></div>${market}${o.horizon?`<div class="ol-h" title="Time horizon this projection covers">${esc(o.horizon)}</div>`:''}${projSummary}</summary>`;
  const body=el("div","fc-body");
  const outlookSec = opts.product ? `<div class="ol-sec"><div class="k">Outlook</div><div class="ol-proj-body">${prettyProj(linkify(o.projected||''))}</div></div>` : '';
  const whySec = opts.product ? (o.rationale?`<div class="ol-sec"><div class="k">Why now</div><div class="ol-why">${linkify(o.rationale)}</div></div>`:'') : `<div class="ol-why">${linkify(o.rationale||'')}</div>`;
  body.innerHTML=`${outlookSec}${whySec}
    ${(o.drivers&&o.drivers.length)?`<div class="ol-drivers"><div class="k">Key drivers</div><ul>${o.drivers.map(dr=>`<li>${linkify(dr)}</li>`).join('')}</ul></div>`:''}
    ${conf}
    ${outlookEvidence(o)}
    ${opts.chartHtml||''}`;
  det.appendChild(body);
  if(opts.onExpand) det.addEventListener('toggle',()=>{ if(det.open && !det.dataset.cd){ det.dataset.cd='1'; opts.onExpand(det); } });
  return det;
}

// One collapsible subsection (same style as the trend sections): bold summary on top, single-column body,
// its own source line. Used for the objective data blocks under the trends.
function subDetails(title, count, bodyHtml, open){
  const det=el("details","fut-theme");
  if(open) det.open=true;
  det.innerHTML=`<summary><span class="ft-name">${esc(title)}</span>${count?`<span class="ft-meta">${esc(String(count))}</span>`:''}</summary>`;
  const body=el("div","ft-body"); body.innerHTML=bodyHtml; det.appendChild(body);
  return det;
}


/* ----------------------------------------------------------------- UNDERLYING DATA (own tab)
   Promoted out of the Future-outlook tab: this is the quantified evidence under the 3-5yr call —
   revenue pools, the competitive shift, the risks and the dated inflection points. It used to sit
   last on that page and collapsed, which hid the market-size figures the team most wanted to reach.
   Here the sections open by default; the tab is the page. */
function renderUnderlying(s){
  s.innerHTML="";
  const b=DASH.futures_board||{};
  const src=()=>`<div class="small muted evsrc">Public sources cited inline — consulting houses, EU &amp; central-bank publications and vendor disclosures.</div>`;
  const TR={rising:'▲ rising',fading:'▼ fading',steady:'▬ steady',mixed:'◆ mixed'};
  const ARR={up:'▲',down:'▼',flat:'▬',mixed:'◆'};
  const DM={'strong growth':'▲','growth':'▲','flat':'▬','decline':'▼','steep decline':'▼','mixed':'◆'};
  const STANCE={invest:['Invest','st-invest'],defend:['Defend','st-defend'],hold:['Hold','st-hold'],exit:['Exit','st-exit'],watch:['Watch','st-watch']};
  const dataCard=el("div","card"); let any=false;
  dataCard.innerHTML=`<div class="hd"><div><h2>The underlying data</h2><div class="desc">The numbers and sources behind the 3–5 year view: revenue by segment, competition, risks and dated turning points. Every section is open; each names its source.</div></div></div>`;
  // ("Demand by product" sub-section removed per Kostas — it restated the heavy drivers + 2030 strip; this layer is the quantified evidence, not a re-telling.)
  if((b.money||[]).length){ any=true; dataCard.appendChild(subDetails('Revenue pools by segment', b.money.length,
    `<table class="bv-tbl"><tbody>`+b.money.map(m=>`<tr><td><b>${esc(m.segment)}</b></td><td class="small">${esc(ARR[(m.direction||'').toLowerCase()]||'')} ${esc(m.magnitude||'')}</td><td class="small muted">${linkify(m.note)}</td></tr>`).join('')+`</tbody></table>`+src(), true)); }
  if((b.competition||[]).length){ any=true; dataCard.appendChild(subDetails('Competitive shift', b.competition.length,
    `<ul class="bv-list">`+b.competition.map(c=>`<li><b>${esc(c.shift)}</b> — <span class="small muted">${linkify(c.note)}</span></li>`).join('')+`</ul>`+src(), true)); }
  if((b.threats||[]).length){ any=true; dataCard.appendChild(subDetails('Risks to watch', b.threats.length,
    `<ul class="bv-list">`+b.threats.map(t=>`<li><b>${esc(t.threat)}</b> — <span class="small muted">${linkify(t.note)}</span></li>`).join('')+`</ul>`+src(), true)); }
  if((b.timeline||[]).length){ any=true; dataCard.appendChild(subDetails('Timeline of inflection points', b.timeline.length,
    `<ul class="bv-list bv-time">`+b.timeline.map(t=>`<li><span class="bv-when">${esc(t.when)}</span><span class="bv-ev">${linkify(t.event)}</span></li>`).join('')+`</ul>`+src(), true)); }
  if(any) s.appendChild(dataCard);
  else s.appendChild(el("div","card","<div class='empty'>No data for this section yet. The monthly Futurist writes it with the 3\u20135 year outlook.</div>"));
}

function renderFutures(s){
  s.innerHTML="";
  const futures=DASH.futures||[];
  const b=DASH.futures_board||{};
  const RBR='RBR Central &amp; Eastern Europe and Western Europe — ATM Market &amp; Forecasts to 2028';
  const src=()=>`<div class="small muted evsrc">Public sources cited inline — consulting houses, EU &amp; central-bank publications and vendor disclosures.</div>`;

  // The distilled, market-wide bottom line: where the WHOLE banking market lands by 2030 — a consultant's
  // synthesis (heavy drivers everyone feels + the non-obvious hidden gems that open new accounts). Intelly
  // design language: ONE soft cyan feature card for the thesis (with a white inner panel for the picture, so it
  // never reads as a solid colour slab), then clean white cards whose headers carry a pastel icon-chip for
  // colour; inner items are soft tiles with NO left-border strips. Degrades to the legacy `verdict`.
  const bl=b.bottom_line;
  // small stroked glyphs for the section icon-chips (match .iconbtn stroke style)
  const GL={bolt:'<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
            gem:'<path d="M12 3l2.3 5.7L20 11l-5.7 2.3L12 19l-2.3-5.7L4 11l5.7-2.3z"/>',
            target:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.6"/><circle cx="12" cy="12" r="1"/>'};
  const chip=(tone,glyph)=>`<span class="bl-chip bl-${tone}"><svg viewBox="0 0 24 24" aria-hidden="true">${glyph}</svg></span>`;
  const shead=(tone,glyph,title,desc)=>`<div class="bl-shead">${chip(tone,glyph)}<div><h2>${esc(title)}</h2><div class="desc">${esc(desc)}</div></div></div>`;
  if(bl && (bl.thesis||bl.picture)){
    // 1) hero — soft cyan feature card: kicker + thesis on the tint, the 2030 picture in a white inner panel
    const hero=el("div","bl-hero");
    let h=`<span class="bl-blob"></span>`;
    if(bl.headline) h+=`<span class="bl-kicker">${esc(bl.headline)}</span>`;
    h+=`<h2 class="bl-htitle">The bottom line</h2>`;
    if(bl.thesis) h+=`<div class="bl-thesis">${linkify(bl.thesis)}</div>`;
    const pics=Array.isArray(bl.picture)?bl.picture:(bl.picture?[bl.picture]:[]);
    if(pics.length || bl.source_note){
      h+=`<details class="bl-panel"><summary class="bl-panel-sum">The 2030 picture<span class="bl-panel-chev" aria-hidden="true"></span></summary><div class="bl-panel-body">`
        +pics.map(p=>`<p>${linkify(p)}</p>`).join('')
        +`<div class="small muted evsrc">${bl.source_note?linkify(bl.source_note):('Distilled from the Futurist’s cited public research — '+RBR+', ECB and EU regulators.')}</div></div></details>`;
    }
    hero.innerHTML=h; s.appendChild(hero);
    // 2) heavy drivers — section header on the cream, then 4 pastel KPI-style cards (blob, content directly on
    // the tint, no inner white container) like the Overview top cards; colour-cycled, number-badged
    const drivers=bl.drivers||bl.forces||[];
    if(drivers.length){
      const KCOL=['k-yellow','k-green','k-blue','k-lilac'];
      const sec=el("div","bl-sec");
      sec.innerHTML=shead('lilac',GL.bolt,'The heavy drivers','The big forces every bank already feels by 2030 — the obvious-but-massive shifts.')
        +`<div class="bl-grid">`+drivers.map((f,i)=>`<div class="bl-kpi ${KCOL[i%KCOL.length]}"><span class="blob"></span><div class="bl-kpi-h"><span class="bl-num">${i+1}</span><div class="bl-kpi-t">${esc(f.title)}</div></div><div class="bl-kpi-d">${linkify(f.detail)}</div></div>`).join('')+`</div>`;
      s.appendChild(sec);
    }
    // 3) hidden gems — white card, green chip; single-column tiles, tag as a pastel pill kicker, no left strip
    if((bl.gems||[]).length){
      const c=el("div","card");
      c.innerHTML=shead('green',GL.gem,'Hidden gems','Under-the-radar shifts that open new accounts, new buyers and new product lines — the non-obvious opportunities, not today’s headlines.')
        +`<div class="bl-stack">`+bl.gems.map(g=>`<div class="bl-tile bl-gem">`+(g.tag?`<span class="bl-pill bl-green">${esc(g.tag)}</span>`:'')+`<div class="bl-tile-t">${esc(g.title)}</div><div class="bl-tile-d">${linkify(g.detail)}</div></div>`).join('')+`</div>`;
      s.appendChild(c);
    }
    // 4) where we land by 2030 — white card, yellow chip; clean before→after rows, hairline separators
    if((bl.endstate_2030||[]).length){
      const c=el("div","card");
      c.innerHTML=shead('yellow',GL.target,'Where we land by 2030','The market, before and after — across the product range, not just cash.')
        +`<div class="bl-end">`+bl.endstate_2030.map(r=>`<div class="bl-row"><div class="bl-metric">${esc(r.metric)}</div>`
          +`<div class="bl-shift"><span class="bl-now">${esc(r.now||'')}</span><span class="bl-arrow">→</span><span class="bl-then">${esc(r.then||'')}</span></div>`
          +(r.note?`<div class="bl-note">${linkify(r.note)}</div>`:'')+`</div>`).join('')+`</div>`;
      s.appendChild(c);
    }
  } else if(b.verdict){
    const txt=String(b.verdict).trim();
    const m=txt.match(/^(.*?[.!?])\s+([\s\S]+)$/);   // split off the opening thesis sentence
    const lead=m?m[1]:txt, rest=m?m[2]:'';
    const card=el("div","card sec-head "+secHeadColor('fut-bottom'));
    card.innerHTML=`<span class="blob"></span><div class="hd"><div><h2>The bottom line</h2></div></div>`
      +`<div class="bv-lead"><span class="lead-emph">${linkify(lead)}</span>${rest?' '+linkify(rest):''}</div>`
      +`<div class="small muted evsrc">Distilled from the Futurist's cited public research — ${RBR}, Datos Insights, ECB and EU regulators.</div>`;
    s.appendChild(card);
  }

  // 1) TRENDS first — a flat list of collapsible trend cards (each is one structural trend, with its own
  // chart + sources; charts draw lazily when a card is expanded so they size correctly)
  if(futures.length){
    const wrap=el("div","card");
    wrap.innerHTML=`<div class="hd"><div><h2>Structural trends, 2 to 5 years</h2><div class="desc">The forces reshaping the market by about 2027–2031, from public research by consulting houses, regulators and international bodies. Each card shows the expected direction (▲ growth, ▼ decline, ◆ mixed), a headline and the bottom-line projection. Click to expand the reasoning, drivers, chart, sources and the analyst's confidence.</div></div></div>`;
    futures.forEach((o,i)=>{
      let chartHtml='', cid=null;
      if(o.chart && o.chart.series && o.chart.series.length && o.chart.labels && o.chart.labels.length){
        cid='fxc_'+i;
        chartHtml=`<div class="chart-panel" style="margin-top:9px"><div class="minicap">${esc(o.chart.title||'')}</div><div class="chartbox short"><canvas id="${cid}"></canvas></div><div class="small muted evsrc">Source: Printec Futurist agent — reasoned projection; cited research appears in the axis labels and the evidence trail.</div></div>`;
      }
      wrap.appendChild(reasonCard(o,{showMarket:true, chartHtml, onExpand: cid?()=>drawFutureChart(cid,o.chart):null}));
    });
    s.appendChild(wrap);
  }

  // The numbers behind the call moved to their own tab (strategy call, 33:59): they were the last card on
  // an already long page AND collapsed by default, so the market-size figures nobody could find — "έχει
  // διαμαντάκια" — were two clicks and a full scroll away. Left here as a signpost, not a duplicate.
  const bHas=['money','competition','threats','timeline'].filter(k=>(b[k]||[]).length);
  if(bHas.length){
    const ptr=el("div","card");
    ptr.innerHTML=`<div class="hd"><div><h2>The numbers behind this outlook</h2><div class="desc">Revenue by segment, the competitive shift, the risks and the dated turning points — with sources — are on the <b>Underlying data</b> tab.</div></div></div>`;
    s.appendChild(ptr);
  }
  const any=bHas.length>0;

  // ("The analyst's view" — scenarios + per-market stance — was removed per Kostas: not wanted on this page.)

  if(!futures.length && !any){ s.appendChild(el("div","card","<div class='empty'>No 3\u20135 year outlook yet. The monthly Futurist writes it from the internal trend reports and public research.</div>")); }
}

/* ----------------------------------------------------------------- charts */
function chartFont(){ return '"Plus Jakarta Sans", system-ui, sans-serif'; }
function mkBar(id,labels,data,colors,title,horizontal,fullnames,onBar){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  charts.push(new Chart(ctx,{type:'bar',
    data:{labels,datasets:[{label:title,data,backgroundColor:colors,borderRadius:6,maxBarThickness:18}]},
    options:{indexAxis:horizontal?'y':'x',responsive:true,maintainAspectRatio:false,
      onClick:onBar?((e,els)=>{ if(els&&els.length) onBar(els[0].index); }):undefined,
      onHover:onBar?((e,els)=>{ const t=e&&e.native&&e.native.target; if(t) t.style.cursor=(els&&els.length)?'pointer':'default'; }):undefined,
      plugins:{legend:{display:false},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},
          callbacks:{title:it=>fullnames?fullnames[it[0].dataIndex]:it[0].label}}},
      scales:{x:{ticks:{color:'#928B7B',font:{family:chartFont()},autoSkip:false,maxRotation:0},grid:{color:'#EFE7D6'},border:{display:false}},
              y:{ticks:{color:'#5F594C',font:{family:chartFont(),weight:'600'},autoSkip:false},grid:{color:'#EFE7D6'},border:{display:false}}}}}));
}
function mkLine(id,title,labels,sets){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  charts.push(new Chart(ctx,{type:'line',
    data:{labels,datasets:sets.map(x=>({label:x.label,data:x.data,borderColor:x.color,backgroundColor:x.color+'22',
      tension:.35,fill:false,pointRadius:2.5,pointBackgroundColor:x.color,borderWidth:2.5}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{title:{display:true,text:title,color:'#16130D',font:{family:chartFont(),size:13,weight:'700'},padding:{bottom:10}},
        legend:{labels:{color:'#5F594C',font:{family:chartFont(),weight:'600'},usePointStyle:true,boxWidth:8}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()}}},
      scales:{x:{ticks:{color:'#928B7B',font:{family:chartFont()}},grid:{color:'#EFE7D6'},border:{display:false}},
              y:{ticks:{color:'#928B7B',font:{family:chartFont()}},grid:{color:'#EFE7D6'},border:{display:false}}}}}));
}
function mkDonut(id,labels,data,colors,title){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  const total=data.reduce((a,b)=>a+(+b||0),0)||1;
  charts.push(new Chart(ctx,{type:'doughnut',
    data:{labels,datasets:[{data,backgroundColor:colors,borderColor:'#FBF7EE',borderWidth:2,hoverOffset:6}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'56%',
      plugins:{title:{display:!!title,text:title,color:'#16130D',font:{family:chartFont(),size:13,weight:'700'},padding:{bottom:6}},
        legend:{position:'bottom',labels:{color:'#5F594C',font:{family:chartFont(),weight:'600',size:11},usePointStyle:true,boxWidth:8,padding:8}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},
          callbacks:{label:it=>` ${it.label}: ${it.raw} (${Math.round(it.raw/total*100)}%)`}}}}}));
}
function mkStackBar(id,labels,datasets,opts){
  opts=opts||{};
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  const valAxis=opts.horizontal?'x':'y';
  const sc={ x:{stacked:true,ticks:{color:'#928B7B',font:{family:chartFont()},autoSkip:false,maxRotation:0},grid:{color:'#EFE7D6'},border:{display:false}},
             y:{stacked:true,ticks:{color:'#5F594C',font:{family:chartFont(),weight:'600'},autoSkip:false},grid:{color:'#EFE7D6'},border:{display:false}} };
  if(opts.valFmt) sc[valAxis].ticks=Object.assign({},sc[valAxis].ticks,{callback:opts.valFmt});
  charts.push(new Chart(ctx,{type:'bar',
    data:{labels,datasets:datasets.map(d=>({label:d.label,data:d.data,backgroundColor:d.color,borderRadius:4,maxBarThickness:20}))},
    options:{indexAxis:opts.horizontal?'y':'x',responsive:true,maintainAspectRatio:false,
      onClick:opts.onBar?((e,els)=>{ if(els&&els.length) opts.onBar(els[0].index); }):undefined,
      onHover:opts.onBar?((e,els)=>{ const t=e&&e.native&&e.native.target; if(t) t.style.cursor=(els&&els.length)?'pointer':'default'; }):undefined,
      plugins:{title:{display:!!opts.title,text:opts.title||'',color:'#16130D',font:{family:chartFont(),size:14,weight:'700'},padding:{bottom:opts.subtitle?2:10}},
        subtitle:{display:!!opts.subtitle,text:opts.subtitle||'',color:'#928B7B',font:{family:chartFont(),size:9.5},padding:{bottom:10}},
        legend:{position:'bottom',labels:{color:'#5F594C',font:{family:chartFont(),weight:'600',size:11},usePointStyle:true,boxWidth:8,padding:8}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},callbacks:{label:opts.tip||(it=>` ${it.dataset.label}: ${it.raw}`)}}},
      scales:sc}}));
}
// competitor business segments: stacked bar, latest year, one stack per reported operating segment.
function drawCompetitorSegments(id, entities, ser){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  const empty=m=>{ const p=ctx.closest('.chart-panel'); if(p) p.innerHTML='<div class="empty">'+m+'</div>'; };
  const withSeg=entities.filter(n=>ser[n]&&ser[n].segments&&Object.keys(ser[n].segments).length);
  if(!withSeg.length){ empty('No segment breakdown for the selected competitors — only the US-listed filers (Atleos, Diebold, Euronet) disclose business segments. Pick one of those.'); return; }
  const SEGCOL=['#23C0E2','#E2715E','#7FB069','#E0B83A','#BFA7E6','#6FA8D6','#9C4A36','#553897'];
  const segNames=[]; withSeg.forEach(n=>Object.keys(ser[n].segments).forEach(sg=>{ if(!segNames.includes(sg)) segNames.push(sg); }));
  const cats=withSeg.map(n=>{ const yrs=Object.values(ser[n].segments).flatMap(a=>a.map(p=>p.year)); return {n,y:Math.max.apply(null,yrs)}; });
  const datasets=segNames.map((sg,i)=>({label:sg,color:SEGCOL[i%SEGCOL.length],
    data:cats.map(c=>{ const a=ser[c.n].segments[sg]||[]; const pt=a.find(p=>p.year===c.y)||(a.length?a[a.length-1]:null); return pt?pt.value:0; })}));
  mkStackBar(id, cats.map(c=>`${c.n} (${c.y})`), datasets, {horizontal:true,
    title:'Revenue by business segment (latest year)',
    subtitle:"Each rival's reported operating segments (10-K, USD billions). Atleos shows its 2 reportable of 3 segments.",
    valFmt:v=>'$'+(v/1000).toFixed(1)+'B', tip:it=>` ${it.dataset.label}: $${(it.raw/1000).toFixed(2)}B`});
}
// competitor financials/operations: ONE metric, one line per company. Real SEC EDGAR data.
// metric ∈ revenue | atm_segment (the ATM/self-service business) | atm_fleet (ATMs operated) | growth (YoY % of revenue)
function drawCompetitorChart(id, metric, entities, ser){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  const pal=['#23C0E2','#E2715E','#7FB069','#E0B83A','#BFA7E6','#6FA8D6'];
  const empty=m=>{ const p=ctx.closest('.chart-panel'); if(p) p.innerHTML='<div class="empty">'+m+'</div>'; };
  const growth=metric==='growth', base=growth?'revenue':metric, fleet=metric==='atm_fleet';
  const years=[...new Set(entities.flatMap(n=>((ser[n]&&ser[n][base])||[]).map(p=>p.year)))].sort((a,b)=>a-b);
  if(!entities.length){ empty('Pick at least one competitor.'); return; }
  if(!years.length){ empty('No data for this metric in the current selection.'); return; }
  const sets=entities.map((n,i)=>{
    const by=Object.fromEntries(((ser[n]&&ser[n][base])||[]).map(p=>[p.year,p.value])); const col=pal[i%pal.length];
    const data=years.map(y=> growth ? ((y in by && (y-1) in by && by[y-1]) ? Math.round((by[y]/by[y-1]-1)*1000)/10 : null) : (y in by ? by[y] : null));
    return {label:n,borderColor:col,backgroundColor:col+'22',borderWidth:2.2,tension:.25,fill:false,spanGaps:true,pointRadius:2.6,pointBackgroundColor:col,data};
  }).filter(d=>d.data.some(v=>v!=null));
  if(!sets.length){ empty('No data for this metric in the current selection.'); return; }
  const T={revenue:['Competitor revenue (annual)','Total revenue (USD billions)'],
           atm_segment:['ATM / self-service segment revenue','Segment revenue (USD billions)'],
           atm_fleet:['ATMs operated (year-end)','Number of ATMs'],
           growth:['Revenue growth (% YoY)','YoY revenue growth (%)']}[metric];
  const sub={revenue:'Source: SEC EDGAR annual filings',
             atm_segment:'The ATM/self-service business — Atleos: Self-Service Banking · Diebold: Banking · Euronet: EFT Processing (10-K, sum-verified)',
             atm_fleet:'Euronet — the disclosed ATM operator (10-K). Atleos and Diebold manufacture rather than operate ATMs.',
             growth:'Source: SEC EDGAR annual filings'}[metric];
  const tip = growth ? (it=>` ${it.dataset.label}: ${it.raw>0?'+':''}${it.raw}%`)
            : fleet  ? (it=>` ${it.dataset.label}: ${fmtNum(it.raw)} ATMs`)
            :          (it=>` ${it.dataset.label}: $${(it.raw/1000).toFixed(2)}B`);
  const yfmt = growth ? (v=>v+'%') : fleet ? (v=>fmtNum(v)) : (v=>'$'+(v/1000).toFixed(1)+'B');
  charts.push(new Chart(ctx,{type:'line',data:{labels:years,datasets:sets},
    options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},
      plugins:{title:{display:true,text:T[0],color:'#16130D',font:{family:chartFont(),size:14,weight:'700'},padding:{bottom:2}},
        subtitle:{display:true,text:sub,color:'#928B7B',font:{family:chartFont(),size:9.5},padding:{bottom:10}},
        legend:{position:'bottom',labels:{color:'#5F594C',font:{family:chartFont(),weight:'600',size:11},usePointStyle:true,boxWidth:8,padding:9}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},callbacks:{label:tip}}},
      scales:{x:{title:{display:true,text:'Year',color:'#5F594C',font:{family:chartFont(),size:11,weight:'600'}},ticks:{color:'#928B7B',font:{family:chartFont()}},grid:{color:'#EFE7D6'},border:{display:false}},
              y:{title:{display:true,text:T[1],color:'#5F594C',font:{family:chartFont(),size:11,weight:'600'}},ticks:{color:'#928B7B',font:{family:chartFont()},callback:yfmt},grid:{color:'#EFE7D6'},border:{display:false}}}}}));
}
// THREE lines, never fused (strategy call 04/09/2026): the statistical fit, the analyst reading of
// the signals, and the rate the structural patterns state. Fusing them would destroy the one thing
// they are for — letting the eye see whether independent readings agree. The three-line treatment
// applies only when a single metric is charted; the country outlook cards chart two metrics at once
// and keep their per-metric colouring, which would otherwise collide with the per-origin colours.
const PROJ_COL={act:'#16130D', stat:'#2a86b8', sig:'#e5764e', pat:'#6b4c9a'};   // blue / coral / purple — the palette the team asked for (08/09/2026)
function projLines(f){
  return (DASH.projection_lines||[]).filter(l=>l.country===f.country && l.metric===f.metric);
}
function drawBaselineChart(id, cfs, overlays){
  const ctx=document.getElementById(id); if(!ctx||!window.Chart) return;
  overlays=overlays||[];
  const COL={atm:'#6FA8D6', branch:'#E2715E'};
  const solo=cfs.length===1;
  const three=solo?projLines(cfs[0]):[];
  const sigL=three.find(l=>l.origin==='signals'), patL=three.find(l=>l.origin==='patterns');
  const sigP=three.find(l=>l.origin==='signals_point');   // the one-year signal-based point (a star)
  const yset=new Set();
  cfs.forEach(f=>{ f.history.forEach(p=>yset.add(p.year)); if(f.anchor) yset.add(f.anchor.year); });
  overlays.forEach(o=>{ (o.provisional||[]).forEach(p=>yset.add(p.year)); (o.projection||[]).forEach(p=>yset.add(p.year)); });
  three.forEach(l=>(l.projection||[]).forEach(p=>yset.add(p.year)));
  if(solo) (cfs[0].alt_series||[]).forEach(a=>{ (a.points||[]).forEach(p=>yset.add(p.year)); (a.projection||[]).forEach(p=>yset.add(p.year)); });
  if(sigP) yset.add(sigP.year);
  const years=[...yset].sort((a,b)=>a-b);
  const sets=[];
  cfs.forEach(f=>{
    const col=solo?PROJ_COL.act:(/atm/i.test(f.metric)?COL.atm:COL.branch);
    const ov=overlays.find(o=>o.metric===f.metric)||{};
    const firm=Object.fromEntries(f.history.map(p=>[p.year,p.value]));
    const prov=Object.fromEntries((ov.provisional||[]).map(p=>[p.year,p.value]));
    const hprov=new Set(f.history.filter(h=>h.provisional).map(h=>h.year));
    const isProvYear=y=> hprov.has(y) || (y in prov);
    // any line segment that ENDS on a provisional year is drawn dashed — on every dataset of the chart
    // provisional readings are drawn exactly like final ones (08/09/2026): solid line, same marker.
    // The flag is kept on the data and in the tooltip note, but not in the drawing.
    const provDash=(own)=>({borderDash:()=>own});
    const anaP=Object.fromEntries((ov.projection||[]).map(p=>[p.year,p.value]));
    const actualYears=years.filter(y=> (y in firm)||(y in prov));
    const lastAct=actualYears[actualYears.length-1];
    const lastActVal=(lastAct in prov)?prov[lastAct]:firm[lastAct];
    // every projection line starts at the row's anchor: the last reported point, measured or
    // provisional, from any source — the mean when a year holds several readings (09/09/2026)
    const anc=(solo&&f.anchor)?f.anchor:null;
    const startY=anc?anc.year:lastAct, startV=anc?anc.value:lastActVal;
    // 1. recorded history + provisional (one solid line; provisional points = ◇ amber). On a single-metric
    //    chart the black line says what the numbers are and who published them: "Recorded · terminals ·
    //    ECB Data Portal" — in the legend, in the tooltip, and (short form) at the end of the line.
    const _recU=solo?String(f.unit||'').trim():'', _recS=solo?String(f.source||'').trim():'';
    const _recLabel=solo?(_recS||'Recorded'):f.metric;   // legend = the source; the unit is on the axis and in the tooltip
    sets.push({label:_recLabel, projKey:solo?'act':undefined, endLabel:'Recorded',
      unitLabel:_recU&&!/^count$/i.test(_recU)?_recU:'',
      data:years.map(y=> (y in firm)?firm[y] : (y in prov)?prov[y] : null),
      borderColor:col, backgroundColor:col+'18', borderWidth:2.2, tension:.2, fill:false, spanGaps:true,
      pointStyle:'circle',
      pointRadius:years.map(y=> ((y in firm)||(y in prov))?2.6 : 0),
      pointBackgroundColor:col, pointBorderColor:col, pointBorderWidth:1});
    // 2. (no trend fit is drawn or computed for the dashboard — asked 09/09/2026)
    // 3. analyst reasoned projection (bold, triangle marker)
    if(ov.projection && ov.projection.length){
      sets.push({label:f.metric+' (analyst)',
        data:years.map(y=> y===startY?startV : (y in anaP)?anaP[y]:null),
        borderColor:col, borderWidth:2.8, tension:.2, fill:false, spanGaps:true,
        pointStyle:'triangle', pointRadius:years.map(y=> (y in anaP)?7:0),
        pointBackgroundColor:col, pointBorderColor:'#fff', pointBorderWidth:1.6});
    }
    // 4. the patterns line. A pattern that states a RANGE is drawn as a band, because that is what
    //    it claims — collapsing it to a single line would invent a precision the source lacks.
    if(patL){
      const pmid=Object.fromEntries((patL.projection||[]).map(p=>[p.year,p.value]));
      if(patL.band){
        const hi=Object.fromEntries(patL.band.high.map(p=>[p.year,p.value]));
        const lo=Object.fromEntries(patL.band.low.map(p=>[p.year,p.value]));
        sets.push({label:'By patterns', projKey:'pat', endLabel:'By patterns',
          data:years.map(y=> y===startY?startV : (y in hi)?hi[y]:null),
          borderColor:PROJ_COL.pat, borderWidth:2, borderDash:[6,4], tension:.2, spanGaps:true, pointRadius:0, segment:provDash([6,4]),
          fill:'+1', backgroundColor:'rgba(107,76,154,.14)'});
        sets.push({label:'', projKey:'pat', hideLegend:true,
          data:years.map(y=> y===startY?startV : (y in lo)?lo[y]:null),
          borderColor:PROJ_COL.pat, borderWidth:2, borderDash:[6,4], tension:.2, spanGaps:true, pointRadius:0, fill:false, segment:provDash([6,4])});
      } else {
        sets.push({label:'By patterns', projKey:'pat', endLabel:'By patterns',
          data:years.map(y=> y===startY?startV : (y in pmid)?pmid[y]:null),
          borderColor:PROJ_COL.pat, borderWidth:2, borderDash:[6,4], tension:.2, fill:false, spanGaps:true, segment:provDash([6,4]),
          pointStyle:'rect', pointRadius:years.map(y=> (y in pmid)?5:0),
          pointBackgroundColor:PROJ_COL.pat, pointBorderColor:PROJ_COL.pat, pointBorderWidth:0});
      }
    }
    // 4b. other organisations' readings of the same thing — points, joined by a faint dotted thread,
    //     each named by its source in the legend. Never fitted, never blended: they are there so the
    //     reader can see where two publishers agree and where they do not.
    const ALT_COL=['#8f8b80','#1a7a6e','#b08a2c','#3c6fb0','#a4547a'];   // warm grey, teal, ochre, blue, plum — apart from the three lines
    (solo?(f.alt_series||[]):[]).forEach((a,ai)=>{
      const pts=Object.fromEntries((a.points||[]).map(p=>[p.year,p.value]));
      const apv=new Set((a.points||[]).filter(p=>p.provisional).map(p=>p.year));
      // a source that IS the recorded line keeps the recorded line's colour; another source gets its own
      const c=a.own?col:ALT_COL[ai%ALT_COL.length];
      if((a.points||[]).length){
        sets.push({label:a.source, projKey:'alt', endLabel:a.source, unitLabel:a.unit||'',
          data:years.map(y=> (y in pts)?pts[y]:null),
          borderColor:c, borderWidth:1.4, tension:.2, fill:false, spanGaps:true,
          pointStyle:'crossRot', pointRadius:years.map(y=> (y in pts)?5:0), pointHoverRadius:7,
          pointBorderColor:c, pointBackgroundColor:c, pointBorderWidth:1.6});
      }
      // the source's OWN projection (RBR forecasts to 2028): dashed, from the end of its history
      if((a.projection||[]).length){
        const pj=Object.fromEntries(a.projection.map(p=>[p.year,p.value]));
        const hy=Object.keys(pts).map(Number); const ay=hy.length?Math.max(...hy):lastAct; const av=hy.length?pts[ay]:lastActVal;
        sets.push({label:a.source+' · projection', projKey:'altp', endLabel:a.source+' projection', unitLabel:a.unit||'', hideLegend:true,
          data:years.map(y=> y===ay?av : (y in pj)?pj[y]:null),
          borderColor:c, borderWidth:1.6, borderDash:[6,4], tension:.2, fill:false, spanGaps:true,
          pointStyle:'crossRot', pointRadius:years.map(y=> (y in pj)?4:0), pointHoverRadius:6,
          pointBorderColor:c, pointBackgroundColor:c, pointBorderWidth:1.4});
      }
    });
    // 5. "By signals" is ONE circle at the target year — no line, no stalk (09/09/2026). It is pushed
    //    last so it draws on top; and if another marker sits on the same spot (a patterns square or
    //    RBR's projection at the same value), it grows and gets a white ring so it stays visible.
    if(sigP){
      const yi=years.indexOf(sigP.year);
      const clash=yi>=0 && sets.some(d=>{ const v=d.data[yi]; return v!=null && Math.abs(v-sigP.value)<=Math.max(1,Math.abs(sigP.value)*0.01); });
      sets.push({label:'By signals', projKey:'sig', endLabel:'By signals', showLine:false,
        data:years.map(y=> y===sigP.year?sigP.value : null),
        borderColor:PROJ_COL.sig, fill:false,
        pointStyle:'circle', pointRadius:clash?9:7, pointHoverRadius:clash?11:9,
        pointBackgroundColor:PROJ_COL.sig, pointBorderColor:clash?'#fff':PROJ_COL.sig, pointBorderWidth:clash?2.5:0});
    }
  });
  const blCountry=(cfs[0]&&cfs[0].country)||'', blMetrics=[...new Set(cfs.map(c=>c.metric))];
  const blTitle=(blCountry?blCountry+' — ':'')+blMetrics.join(' & ');
  // the axis names the UNIT, not the metric (the title already names the metric): "terminals",
  // "million withdrawals per year", "RSD million withdrawn from payment accounts" — whatever the source says
  const _u=solo?String(cfs[0].unit||'').trim():'';
  const blY=solo?(!_u||/^count$/i.test(_u)?blMetrics[0]+' (count)':_u):(blMetrics.length===1?blMetrics[0]:'Count');
  const blSub=solo
    ? ('solid = measured'
       + ' · dashed = projected'
       + ((sigL||sigP)?' · star = where the signals put '+((sigP&&sigP.year)||((parseInt(String(DASH.week||'').slice(0,4))||new Date().getFullYear())+1)):'')
       + (patL&&patL.band?' · shaded = the range the patterns state':'')
       + (((cfs[0].alt_series)||[]).length?' · × = other organisations\u2019 readings':''))
    : 'solid = recorded · ◇ = provisional · bold = analyst projection';
  charts.push(new Chart(ctx,{type:'line',data:{labels:years,datasets:sets},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{title:{display:true,text:blTitle,color:'#16130D',font:{family:chartFont(),size:13,weight:'700'},padding:{bottom:2}},
        subtitle:{display:true,text:blSub,color:'#928B7B',font:{family:chartFont(),size:9.5},padding:{bottom:9}},
        legend:{labels:{color:'#5F594C',font:{family:chartFont(),weight:'600'},usePointStyle:true,boxWidth:8,
          filter:(it,data)=>!/\(model\)/.test(it.text) && it.text!=='' && !(data.datasets[it.datasetIndex]||{}).hideLegend}},
        tooltip:{backgroundColor:'#141310',padding:10,cornerRadius:10,titleFont:{family:chartFont()},bodyFont:{family:chartFont()},
          filter:it=>it.dataset.label!=='',   /* the band's lower edge is one reading, not two */
          callbacks:{label:it=>` ${it.dataset.endLabel||it.dataset.label}: ${fmtNum(it.raw)}${it.dataset.unitLabel?' '+it.dataset.unitLabel:''}${(it.dataset.projKey==='act'&&isProvYear(years[it.dataIndex]))?' (provisional)':''}`}}},
      scales:{x:{title:{display:true,text:'Year',color:'#5F594C',font:{family:chartFont(),size:11,weight:'600'}},ticks:{color:'#928B7B',font:{family:chartFont()}},grid:{color:'#EFE7D6'},border:{display:false}},
              y:{title:{display:true,text:blY,color:'#5F594C',font:{family:chartFont(),size:11,weight:'600'}},ticks:{color:'#928B7B',font:{family:chartFont()},callback:v=>fmtNum(v)},grid:{color:'#EFE7D6'},border:{display:false}}}}}));
}

/* ----------------------------------------------------------------- nav + shell */
const RENDER={budget:renderBudget,overview:renderOverview,country:renderCountry,product:renderProduct,competition:renderCompetition,accounts:renderAccounts,signals:renderSignals,outlook:renderOutlook,baselines:renderBaselines,underlying:renderUnderlying,futures:renderFutures,patterns:renderPatterns};
function navCount(id){
  const k=DASH.kpis;
  return {budget:((DASH.budget_2027||{}).cells||[]).length,overview:k.n_signals,country:k.n_countries_active,product:DASH.products.filter(p=>p.n_signals>0).length,
          competition:DASH.competitors.length,accounts:DASH.account_targets.length,signals:k.n_signals,
          outlook:(DASH.outlook||[]).length,baselines:(DASH.forecast||[]).length,
          futures:(DASH.futures||[]).length,patterns:DASH.patterns.length,
          underlying:['money','competition','threats','timeline'].reduce((a,k)=>a+((DASH.futures_board||{})[k]||[]).length,0)}[id] ?? '';
}
function show(id){
  current=id;
  document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id===id));
  document.querySelectorAll("#nav .nav-item").forEach(b=>b.classList.toggle("active",b.dataset.id===id));
  const meta=TABS.find(t=>t.id===id);
  let title=meta.title, sub=meta.sub;
  if(id==='overview'){
    if(view.mode==='month'){ title=view.monthInfo.label; sub='Everything found across the footprint as of the latest run in '+view.monthInfo.label+'.'; }
    else if(view.mode==='week'){ title='Week of '+view.week; sub='The footprint as it stood in this archived week — signals, movements and opportunities at the time.'; }
  }
  $("#topTitle").textContent=title; $("#topSub").textContent=sub;
  charts.forEach(c=>c.destroy()); charts=[];
  RENDER[id]($("#"+id));
  window.scrollTo({top:0,behavior:'smooth'});
}

/* ----------------------------------------------------------------- period / history */
function viewLabel(){
  if(view.mode==='month') return view.monthInfo.label+' · month view';
  if(view.mode==='week')  return 'Week of '+view.week+' · archived';
  return 'Week of '+((DASH&&DASH.week)||view.week||'');
}
function periodBtnLabel(){
  if(view.mode==='month') return view.monthInfo.label;
  if(view.mode==='week')  return 'Week of '+view.week;
  return 'Latest';
}
function applyAndRender(d){
  DASH=d; sigByKey={}; _fused=null; _atm=null; DASH.signals.forEach(s=>sigByKey[s.key]=s);
  buildShell(); updateBanner(); show(current);
}
async function goLatest(){
  const d=await loadData(null);
  if(!d||!d.signals) return;
  view={mode:'latest', week:d.week, monthKey:null, monthInfo:null};
  applyAndRender(d);
}
async function goWeek(week){
  const d=await loadData(week);
  if(!d||!d.signals){ flashUnavailable('That week’s data isn’t available yet (it may not have been published).'); return; }
  view={mode:'week', week:week, monthKey:null, monthInfo:null};
  applyAndRender(d);
}
async function goMonth(mk){
  const wks=(manifest.weeks||[]).map(w=>w.week).filter(w=>monthKeyOf(w)===mk).sort();
  if(!wks.length) return;
  const endWeek=wks[wks.length-1];
  const end=await loadData(endWeek);
  if(!end||!end.signals){ flashUnavailable('That month’s data isn’t available yet.'); return; }
  // The monthly rollup just shows what was found as of the month's latest run (the month-end snapshot). We
  // deliberately do NOT compute a "dropped"/movement delta — a signal absent this month usually just means the
  // agents didn't re-surface it that run, not that the opportunity ended.
  view={mode:'month', week:endWeek, monthKey:mk, monthInfo:{label:monthLabel(mk), monthEndWeek:endWeek}};
  applyAndRender(end);
}
function closePeriod(){ document.querySelectorAll('.period-panel.open').forEach(p=>{ p.classList.remove('open'); const b=p.previousElementSibling; if(b)b.setAttribute('aria-expanded','false'); }); }
// full-screen loading overlay — shown while a period switch fetches new data (week/month loads hit the network)
function setLoading(on){
  let o=document.getElementById('loadOverlay');
  if(on){
    if(!o){ o=document.createElement('div'); o.id='loadOverlay'; o.innerHTML='<div class="spinner" role="status" aria-label="Loading"></div>'; document.body.appendChild(o); }
    o.classList.add('show');
  } else if(o){ o.classList.remove('show'); }
}
function periodItem(label, meta, sel, cls, onClick){
  const it=el('div','period-item'+(cls?' '+cls:'')+(sel?' sel':''));
  it.setAttribute('role','menuitem'); it.tabIndex=0;
  it.innerHTML=`<span class="pl">${esc(label)}</span>`+(meta?`<span class="mo">${esc(meta)}</span>`:'');
  const go=async()=>{ closePeriod(); setLoading(true); try{ await onClick(); } finally{ setLoading(false); } };
  it.addEventListener('click',go);
  it.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); go(); } });
  return it;
}
function buildPeriodPanel(panel){
  panel.innerHTML="";
  const weeks=(manifest.weeks||[]).slice().sort((a,b)=> a.week<b.week?1:a.week>b.week?-1:0);
  const latestWeek=(weeks[0]||{}).week || (DASH&&DASH.week) || '';
  panel.appendChild(el('div','period-grp','Jump to'));
  panel.appendChild(periodItem('Latest', latestWeek?('Week of '+fmtWeek(latestWeek)):'', view.mode==='latest', 'latest', goLatest));
  const seen=new Set(), months=[];
  weeks.forEach(w=>{ const mk=monthKeyOf(w.week); if(!seen.has(mk)){ seen.add(mk); months.push(mk); } });
  months.forEach(mk=>{
    panel.appendChild(periodItem(monthLabel(mk), 'monthly rollup', view.mode==='month'&&view.monthKey===mk, 'month', ()=>goMonth(mk)));
    weeks.filter(w=>monthKeyOf(w.week)===mk).forEach(w=>{
      const meta=(w.n_signals!=null)?(w.n_signals+' signals'):'';
      panel.appendChild(periodItem(fmtWeek(w.week), meta, view.mode==='week'&&view.week===w.week, 'week', ()=>goWeek(w.week)));
    });
  });
}
function makePeriodControl(){
  const wrap=el('div','period');
  const btn=el('button','period-btn'+(view.mode==='latest'?'':' hist'));
  btn.setAttribute('aria-haspopup','menu'); btn.setAttribute('aria-expanded','false'); btn.setAttribute('aria-label','Choose period');
  btn.innerHTML=`<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="16" rx="3"></rect><path d="M3 9h18M8 2.5v4M16 2.5v4"></path></svg><span class="lbl">${esc(periodBtnLabel())}</span><svg class="chev" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"></polyline></svg>`;
  const panel=el('div','period-panel'); panel.setAttribute('role','menu');
  btn.addEventListener('click',e=>{ e.stopPropagation(); const willOpen=!panel.classList.contains('open'); closePeriod(); if(willOpen){ buildPeriodPanel(panel); panel.classList.add('open'); btn.setAttribute('aria-expanded','true'); } });
  panel.addEventListener('click',e=>e.stopPropagation());
  wrap.appendChild(btn); wrap.appendChild(panel);
  return wrap;
}

function buildShell(){
  charts.forEach(c=>{ try{ c.destroy(); }catch(e){} }); charts=[];   // tear down before the canvases they bind to are removed
  // sidebar nav
  const nav=$("#nav"); nav.innerHTML="";
  // the Budget tab and its group exist only when the build carries budget data (14/09/2026)
  const _hasBudget=!!(DASH&&DASH.budget&&DASH.budget.cells&&DASH.budget.cells.length);
  TAB_GROUPS.filter(g=>g.id!=='budget'||_hasBudget).forEach(g=>{
    nav.appendChild(el("div","side-label",g.label));
    TABS.filter(t=>t.group===g.id&&(t.id!=='budget'||_hasBudget)).forEach(t=>{
      const b=el("button","nav-item"+(t.nested?" nav-nested":"")); b.dataset.id=t.id;
      b.setAttribute("aria-label",t.label);
      b.innerHTML=`<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">${t.icon}</svg></span><span class="lab">${t.label}</span>`;
      b.addEventListener('click',()=>show(t.id));
      nav.appendChild(b);
    });
  });
  // log out — styled like a nav item, sitting just below the tabs (intelly pattern)
  const out=el("a","nav-item logout-link"); out.href="/api/logout"; out.title="Sign out"; out.setAttribute("aria-label","Log out");
  out.innerHTML=`<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg></span><span class="lab">Log out</span>`;
  nav.appendChild(out);
  // Admin: a small link at the foot of the sidebar. With a budget block in the build, it asks for
  // the password, decrypts the budget in the browser and adds the Budget tab. Locked again on reload.
  if(window.__DASH_BUDGET_ENC__ && !(DASH&&DASH.budget)){
    const adm=el("button","nav-item admin-link"); adm.type='button'; adm.title='Admin: unlock the budget view';
    adm.innerHTML=`<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span><span class="lbl">Admin</span>`;
    adm.addEventListener('click',()=>budgetUnlockDialog(nav,adm));
    nav.appendChild(adm);
  }

  // main: topbar + views + footer
  const root=$("#root"); root.innerHTML="";
  const top=el("div","topbar");
  top.innerHTML=`<div class="greet">
      <span class="wkpill${view.mode==='latest'?'':' hist'}" id="wkPill"></span>
      <h1 id="topTitle"></h1><p id="topSub"></p></div>
    <div class="topbar-actions" id="topActions">
      <a class="archbtn" id="archBtn" href="architecture.html" title="How this dashboard is built: the agents, prompts and data flow behind it"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="6" height="6" rx="1.4"></rect><rect x="15" y="4" width="6" height="6" rx="1.4"></rect><rect x="9" y="14" width="6" height="6" rx="1.4"></rect><path d="M6 10v2.5a1.5 1.5 0 0 0 1.5 1.5H9M18 10v2.5a1.5 1.5 0 0 1-1.5 1.5H15"></path></svg><span>Architecture</span></a>
      <button class="iconbtn" id="infoBtn" title="Method &amp; provenance" aria-label="Method and provenance"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 16v-4M12 8h.01"></path></svg></button>
    </div>`;
  root.appendChild(top);
  // period selector (prepended into the action bar) + the context pill
  $("#topActions").insertBefore(makePeriodControl(), $("#topActions").firstChild);
  $("#wkPill").innerHTML=`<span class="wkdot" style="width:6px;height:6px;border-radius:50%;background:var(--cyan-ink);display:inline-block"></span>${esc(viewLabel())}`;
  const views=el("div","views");
  TABS.forEach(t=>{ const sec=el("section","view"); sec.id=t.id; views.appendChild(sec); });
  root.appendChild(views);
  const foot=el("footer","appfoot"); foot.id="foot"; foot.hidden=true; foot.innerHTML=footerHTML(); root.appendChild(foot);  // hidden by default; revealed via the (i) Method & provenance button

  $("#infoBtn").addEventListener('click',()=>{ const f=document.querySelector('#foot'); if(!f) return; f.hidden=!f.hidden; if(!f.hidden) f.scrollIntoView({behavior:'smooth',block:'start'}); });
}

function footerHTML(){
  return `<b>Provenance &amp; method.</b> Built by the Printec weekly-intelligence skill (upgraded Orchestrator) from the research folder: <code>master-signal-table.md</code> (${DASH.signals.length} signals), the history workbook (${DASH.summary.n_timeseries_points||0} time-series points, ${DASH.patterns.length} patterns, ${DASH.events.length} milestones) and the latest statistics findings (${DASH.summary.n_country_stats||0} markets). Confidence: <span class="pill High">High</span> = 2+ independent agents agree; single-agent signals cap at <span class="pill Medium">Medium</span>. "Strength" is a confidence × agent-count × likelihood weighting used to rank signals. No figure here is invented; every number traces to a dated source in the master table or workbook.${(DASH.provenance&&DASH.provenance.total)?` <b>Source audit:</b> ${DASH.provenance.reachable} of ${DASH.provenance.total} cited external sources were re-fetched, reachable &amp; snapshotted this run (link-rot defense); figure-level confirmation of each number is the orchestrator’s weekly source re-check.`:''}`;
}

/* ----------------------------------------------------------------- boot */
function bindChrome(){
  const sb=$("#sidebar"), tog=$("#sideToggle");
  if(tog) tog.addEventListener('click',()=>{ const c=sb.classList.toggle('collapsed'); tog.setAttribute('aria-expanded', c?'false':'true'); });
  document.addEventListener('click',closePeriod);   // close the period menu on any outside click
  // "Built on" signal chips (delegated, once): click / Enter / Space reveals the signal + its sources inline
  document.addEventListener('click',e=>{ const c=e.target.closest&&e.target.closest('.ol-sig'); if(c) revealSignal(c); });
  // "See Pattern #n" — switch to the patterns tab, open that card, scroll to it. Matched by number first,
  // then by the start of the headline, so a renumbering upstream still lands on the right card.
  document.addEventListener('click',e=>{ const a=e.target.closest&&e.target.closest('.bl-patlink'); if(!a) return;
    e.preventDefault(); show('patterns');
    const n=a.dataset.pattern, key=(a.dataset.pat||'').toLowerCase();
    let card=n?document.getElementById('pattern-'+n):null;
    if(card && key && !(card.dataset.pat||'').startsWith(key.slice(0,40))) card=null;
    if(!card && key) card=[...document.querySelectorAll('.pat-card')].find(d=>(d.dataset.pat||'').startsWith(key.slice(0,40)))||null;
    if(!card) return;
    card.open=true; setTimeout(()=>card.scrollIntoView({behavior:'smooth',block:'start'}),60);
    card.classList.add('pat-flash'); setTimeout(()=>card.classList.remove('pat-flash'),1800); });
  document.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ const c=e.target.closest&&e.target.closest('.ol-sig'); if(c){ e.preventDefault(); revealSignal(c); } } });
}
function flashUnavailable(msg){
  const b=$("#banner"); if(!b) return;
  b.className="banner show"; b.textContent=msg;
  setTimeout(()=>{ if(b.textContent===msg) updateBanner(); }, 4500);
}
function updateBanner(){
  const b=$("#banner"); if(!b) return;
  if(view.mode!=='latest'){ b.className="banner"; b.textContent=""; return; }   // historical views are explicit
  if(dataSource==='bundled' && !window.__DASH_DATA__){
    b.className="banner show";
    b.textContent="Showing the bundled snapshot — the live feed had no data yet. It will switch to live automatically once the orchestrator publishes this week's run.";
  } else { b.className="banner"; b.textContent=""; }
}
async function boot(){
  bindChrome();
  try{
    DASH=await loadData(null);
    if(window.Chart){ Chart.defaults.font.family=chartFont(); Chart.defaults.color='#5F594C'; }
    DASH.signals.forEach(s=>sigByKey[s.key]=s);
    view={mode:'latest', week:DASH.week, monthKey:null, monthInfo:null};
    manifest=await loadManifest();
    buildShell();
    updateBanner();
    show('overview');
  }catch(e){
    $("#root").innerHTML=`<div class="loader"><div>Could not load dashboard data.</div><div class="small muted">${esc(e.message||e)}</div></div>`;
  }
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot); else boot();
})();
