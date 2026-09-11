#!/usr/bin/env python3
"""Build-time patches applied to dashboard-web/app.js when packaging the Artifact.

dashboard-web/app.js on disk is NEVER modified, so the live Vercel app is unaffected.
Every anchor is asserted to match exactly once — if app.js changes upstream the build
fails loudly instead of silently producing something broken.

A. Offline evidence viewer  — serve the findings documents from window.__DASH_DOCS__
   instead of the /api/evidence endpoint, which does not exist in a single-file build.
B. Baseline explainers      — the "Charts" tab table gets
   provenance, a partial-year warning, a stale-base marker and the market's related
   signals, so a bare trend number can be judged rather than just read.
"""

HELPERS = r"""
/* ---- baseline explainers (artifact build) -------------------------------- */
const BL_PROD={'ATM installed base':['atm_recycling','managed_services'],
 'ATMs':['atm_recycling','managed_services'],
 'Cash withdrawals':['atm_recycling','managed_services'],
 'Cash in circulation (value)':['atm_recycling','managed_services'],
 'Banknotes exported (value)':['atm_recycling','managed_services'],
 'Counter cash deposits and withdrawals (value)':['atm_recycling','managed_services'],
 'Cash withdrawn from accounts (value)':['atm_recycling','managed_services'],
 'Cash withdrawals (local measure)':['atm_recycling','managed_services'],
 'Cash withdrawals — annual value (USD)':['atm_recycling','managed_services'],
 'Bank branches':['self_service','managed_services'],
 'Bank employees':['self_service','managed_services'],
 'POS terminals':['pos_acquiring']};
let _blN2C=null;
function blCode(name){ if(!_blN2C){ _blN2C={}; for(const k in DASH.code2name) _blN2C[DASH.code2name[k]]=k; } return _blN2C[name]; }
function blRunYear(){ return parseInt(String(DASH.week||'').slice(0,4))||new Date().getFullYear(); }
function blProvisional(f){ const h=(f.history||[]); return !!(h.length && h[h.length-1].provisional); }
// The three projection lines, told straight: what each one is drawn from, and — for the ones this
// row does not get — why not. A missing line must read as a stated limit, not as a rendering bug.
function blLines(f){
  const mine=(DASH.projection_lines||[]).filter(l=>l.country===f.country&&l.metric===f.metric);
  const gaps=(DASH.projection_gaps||[]).filter(g=>g.country===f.country&&g.metric===f.metric);
  const out=[];   // the statistical fit is no longer shown on the chart or in this panel (08/09/2026)
  for(const o of ['signals','patterns']){
    const l=mine.find(x=>x.origin===o), g=gaps.find(x=>x.origin===o);
    const col=o==='signals'?'#e5764e':'#6b4c9a';
    const name=o==='signals'?'By signals':'By patterns';
    if(o==='signals' && !l){
      // No analyst line, but the rule-based point for next year still says something. It lives
      // HERE, in the one row about signals, so the panel never says "none" beside a star.
      const pt=mine.find(x=>x.origin==='signals_point');
      const pg=gaps.find(x=>x.origin==='signals_point');
      if(pt){
        const leanTxt=pt.lean>0.15?'leaning up':pt.lean<-0.15?'leaning down':'balanced';
        out.push({origin:o, col:col, name:name,
          body:'<b>The signals put '+pt.year+' at about '+fmtNum(pt.value)+' ('+leanTxt+').</b> '
              +esc(pt.explain||'')
              +' <i>How this is made: each signal for this market and product is read for whether it says '
              +esc(f.metric.toLowerCase())+' are growing or shrinking. The net lean, weighted by signal strength, '
              +'moves the last reported value by the series\u2019 own typical yearly change for each year to '
              +esc(String(pt.year))+'. It is a rule, shown in full \u2014 not a measured figure.</i>'});
      } else {
        out.push({origin:o, col:col, name:name, missing:true,
                  body:esc((g&&g.reason)||(pg&&pg.reason)||'not produced for this row')});
      }
      continue;
    }
    if(l){
      let body='';
      if(o==='signals'){
        const pt=mine.find(x=>x.origin==='signals_point');
        body='<b>'+esc(l.direction||'reasoned projection')+'.</b> '+esc(l.mechanism||'')
            +' <i>'+esc(l.judgement||'')+'</i>'
            +(l.rebased&&l.rebased.note?' '+esc(l.rebased.note):'')
            +(pt?' <b>For '+pt.year+' this puts the figure at about '+fmtNum(pt.value)+'.</b>':'')
            +(l.confidence?' · confidence '+esc(l.confidence):'')
            +(l.cite_signals&&l.cite_signals.length?' · based on '+l.cite_signals.length+' cited signal'+(l.cite_signals.length>1?'s':''):'');
      } else {
        // one sentence for THIS country and metric (written by the engine), then the pattern it rests on
        const endYr=(l.projection&&l.projection.length)?l.projection[l.projection.length-1].year:'';
        const fv=v=>Math.abs(v)<100?(Math.round(v*10)/10).toLocaleString('en-US',{minimumFractionDigits:1,maximumFractionDigits:1}):fmtNum(v);
        const endVal=(l.band&&l.band.high&&l.band.low)
          ? 'between about '+fv(l.band.low[l.band.low.length-1].value)+' and '+fv(l.band.high[l.band.high.length-1].value)
          : ((l.projection&&l.projection.length)?'at about '+fv(l.projection[l.projection.length-1].value):'');
        body=(endYr&&endVal?'<b>The patterns put '+endYr+' '+endVal+'.</b> ':'')
            +esc(l.explain||l.basis||'')
            +(l.pattern_no?' <a class="link bl-patlink" href="#pattern-'+l.pattern_no+'" data-pattern="'+l.pattern_no+'" data-pat="'+esc(String(l.claim||'').slice(0,60))+'">See Pattern #'+l.pattern_no+' in By patterns \u2192</a>':'');
      }
      out.push({origin:o, col:col, name:name, body:body});
    } else {
      out.push({origin:o, col:col, name:name, missing:true,
                body:g?esc(g.reason):'not produced for this row'});
    }
  }
  return out;
}
function blLinesHtml(f){
  // the signals list sits directly under the By signals row, indented to the row's text column
  return '<div class="bl-block"><div class="bl-k">The projections on this chart</div>'
    + blLines(f).map(l=>'<div class="bl-line'+(l.missing?' bl-line-off':'')+'">'
        + '<span class="bl-swatch" style="background:'+l.col+'"></span>'
        + '<span class="bl-lname">'+l.name+(l.missing?' — none':'')+'</span>'
        + '<span class="bl-lbody">'+l.body+'</span></div>'
        + (l.origin==='signals'?'<div class="bl-subline">'+blWhyHtml(f)+'</div>':'')).join('')
    + '</div>';
}
function blSignals(f){
  const code=blCode(f.country), prods=BL_PROD[f.metric]||[];
  if(!code||!prods.length) return [];
  return (DASH.signals||[]).filter(s=>(s.countries||[]).includes(code) &&
      (prods.indexOf(s.primary_product)>=0 || prods.some(p=>(s.products||[]).indexOf(p)>=0)))
    .sort((a,b)=>{ const pa=prods.indexOf(a.primary_product)>=0?1:0, pb=prods.indexOf(b.primary_product)>=0?1:0;
                   return (pb-pa) || String(b.dev_date||'').localeCompare(String(a.dev_date||'')); });
}
function blHowHtml(f){
  const h=f.history||[], pts=h.length, yrs=pts?(h[0].year+'–'+h[pts-1].year):'—';
  const warn=blProvisional(f)
    ? '<div class="bl-warn"><b>⚠ '+esc(String(h[pts-1].year))+' is a provisional figure.</b> Every line starts from it, so treat the '
      +'projections with care and read the direction from the completed years.</div>'
    : '';
  // The method / r² / fit / projection-window / horizon lines were removed on request (08/09/2026):
  // the three-projections panel below is the explanation now. Only the provisional-year warning stays.
  return warn;
}
function blWhyHtml(f){
  // EVERY signal tagged to this market and product line, not a sample. A reader judging a projection
  // needs to know the whole evidence base exists; showing "the 3 closest of 36" invited the opposite
  // reading. Each chip is truncated for width and carries its full title on hover, so the list stays
  // scannable at 36 entries without hiding any of them.
  const all=blSignals(f);
  if(!all.length) return '<div class="bl-block"><div class="bl-k">Context for judging this projection</div>'
    +'<div class="muted small">No signal this week is tagged to this market and product, so there is nothing to weigh '
    +'this projection against yet.</div></div>';
  // Folded by default and grouped by month inside. Up to 36 chips in one block was too much to look
  // at (asked 08/09/2026). Nothing is dropped: the summary line states the count, and opening it
  // shows every signal, newest month first. Chips and the reveal box stay inside ONE .ol-builton so
  // clicking a chip still opens the signal in place.
  const chip=s=>'<span class="srcfile ol-sig" data-sigkey="'+esc(s.key)+'" role="button" tabindex="0" '
      +'title="'+esc(s.bank_theme)+(s.dev_date?' — '+esc(s.dev_date):'')+'">'
      +(s.dev_date?'<span class="ol-sigdate">'+esc(String(s.dev_date).slice(8))+'</span>':'')
      +'<span class="ol-signame">'+esc(s.bank_theme)+'</span></span>';
  const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const monthOf=s=>{ const d=String(s.dev_date||''); return /^\d{4}-\d{2}/.test(d)?d.slice(0,7):''; };
  const label=m=>m?MON[parseInt(m.slice(5),10)-1]+' '+m.slice(0,4):'Undated';
  const groups={}; all.forEach(s=>{ const m=monthOf(s); (groups[m]=groups[m]||[]).push(s); });
  const months=Object.keys(groups).sort((a,b)=>b.localeCompare(a));
  const body=months.map(m=>'<div class="bl-sigmonth"><span>'+esc(label(m))+'</span><span class="bl-sigmonth-n">'+groups[m].length+'</span></div>'
      +'<div class="bl-sigwrap">'+groups[m].map(chip).join('')+'</div>').join('');
  const newest=all.map(s=>String(s.dev_date||'')).filter(Boolean).sort().pop();
  const head='Show all '+all.length+' signal'+(all.length>1?'s':'')+' for this market and product line'
      +(newest?' <span class="muted">· newest '+esc(label(newest.slice(0,7)))+'</span>':'');
  return '<div class="bl-block"><div class="bl-k">Signals to weigh against this projection</div>'
    +'<details class="bl-sigfold"><summary>'+head+'</summary>'
    +'<div class="ol-builton">'+body+'<div class="ol-sigdetail" hidden></div></div></details></div>';
}
"""

CSS = """
/* baseline explainers (artifact build) */
.bl-chev{display:inline-block;width:6px;height:6px;margin-right:8px;border-right:2px solid var(--ink-3);
  border-bottom:2px solid var(--ink-3);transform:rotate(-45deg);transition:transform .18s;vertical-align:middle}
tr.clickable.bl-open .bl-chev{transform:rotate(45deg)}
.bl-prov{color:#b06a00;font-weight:800;cursor:help}
.bl-nsig{display:inline-block;margin-left:8px;font-size:10.5px;font-weight:700;color:var(--cyan-ink);
  background:var(--cyan-soft);border:1px solid #bfe4f0;border-radius:var(--pill);padding:1px 8px;white-space:nowrap}
.bl-warn{background:var(--yellow-soft);border:1px solid #ecdc92;color:var(--yellow-ink);border-radius:var(--r-sm);
  padding:10px 13px;margin:12px 0 0;font-size:12.3px;line-height:1.55}
.bl-block{margin-top:13px}
.bl-k{font-size:10px;text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--ink-3);margin-bottom:5px}
.bl-note{margin-top:5px;line-height:1.5}
.bl-block .ol-builton{line-height:2}
.bl-back-badge{display:inline-block;margin-left:6px;font-size:10.5px;font-weight:700;color:#6e685b;background:#ece9e1;
  border:1px solid #ddd7c8;border-radius:var(--pill);padding:1px 9px;white-space:nowrap;cursor:help}
.bl-back{color:var(--yellow-ink);margin-top:4px}
.bl-line{display:grid;grid-template-columns:auto 96px minmax(0,1fr);gap:4px 10px;align-items:baseline;
  padding:7px 0;border-bottom:1px dashed var(--line-2)}
.bl-line:last-of-type{border-bottom:0}
.bl-swatch{width:16px;height:8px;border-radius:2px;align-self:start;margin-top:5px}  /* on the FIRST line of text, whatever the row's height — so every row's dash lines up with the statistical one */
.bl-lname{font-size:11.8px;font-weight:800;color:var(--ink)}
.bl-lbody{font-size:11.8px;line-height:1.55;color:var(--ink-2)}
.bl-lbody b{color:var(--ink);font-weight:700}
.bl-lbody i{font-style:normal;color:var(--ink-3)}
.bl-sigfold{border:1px solid var(--line);border-radius:var(--r-sm);background:var(--card);margin-top:4px}
.bl-sigfold>summary{list-style:none;cursor:pointer;padding:9px 13px;font-size:12px;font-weight:800;color:var(--ink);
  display:flex;align-items:center;gap:9px}
.bl-sigfold>summary::-webkit-details-marker{display:none}
.bl-sigfold>summary::before{content:"";width:6px;height:6px;border-right:1.7px solid var(--ink-3);
  border-bottom:1.7px solid var(--ink-3);transform:rotate(-45deg);transition:transform .18s;flex:0 0 auto}
.bl-sigfold[open]>summary::before{transform:rotate(45deg)}
.bl-sigfold>summary:hover{background:var(--card-2)}
.bl-sigfold[open]>summary{border-bottom:1px solid var(--line-2)}
.bl-sigfold .ol-builton{padding:8px 13px 12px;line-height:1.4}
.bl-sigmonth{display:flex;align-items:center;gap:8px;margin:9px 0 6px;font-size:10.5px;font-weight:800;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.bl-sigmonth:first-child{margin-top:2px}
.bl-sigmonth::after{content:"";flex:1;height:1px;background:var(--line-2)}
.bl-sigmonth-n{font-weight:700;background:var(--card-2);border:1px solid var(--line);border-radius:var(--pill);padding:0 7px}
.bl-sigwrap{display:flex;flex-wrap:wrap;gap:5px;align-items:flex-start;line-height:1.4}
.bl-sigwrap .srcfile{display:inline-flex;align-items:baseline;gap:6px;max-width:290px;margin:0}
.bl-sigwrap .ol-sigdate{flex:0 0 auto;font-size:9.5px;font-weight:700;color:var(--ink-3);
  font-variant-numeric:tabular-nums}
.bl-sigwrap .ol-signame{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bl-sigwrap .ol-sigdetail{flex:1 1 100%}
.bl-subline{padding:2px 0 8px 132px;border-bottom:1px dashed var(--line-2)}
.bl-subline .bl-block{margin-top:2px}
.bl-subline .bl-k{font-size:9.5px}
.bl-patlink{font-weight:700;white-space:nowrap}
@media(max-width:640px){.bl-subline{padding-left:0}}
.bl-line-off{opacity:.62}
.bl-line-off .bl-swatch{background:none!important;border:1.5px dashed var(--ink-3)}
@media(max-width:640px){.bl-line{grid-template-columns:auto minmax(0,1fr)}.bl-line .bl-lbody{grid-column:1/-1}}
"""

def apply(app: str) -> str:
    box = [app]
    def one(old, new, what):
        n = box[0].count(old)
        if n != 1:
            raise SystemExit("patch_artifact: %s expected 1 occurrence, found %d — app.js changed upstream." % (what, n))
        box[0] = box[0].replace(old, new)

    # ---------- A. offline evidence viewer ----------
    one("function docHref(fp){",
        "function DOCEMB(fp){ return !!(window.__DASH_DOCS__ && window.__DASH_DOCS__[fp]); }\n"
        "function docHref(fp){",
        "A1 DOCEMB helper")
    one("""  v.raw.href=href; v.body.className='ev-body'; v.body.innerHTML='<div class="ev-msg">Loading…</div>'; v.show();
  try{""",
        """  v.raw.href=href; v.body.className='ev-body'; v.body.innerHTML='<div class="ev-msg">Loading…</div>'; v.show();
  {   // single-file build: serve the document from the embedded map, there is no /api/evidence here
    const _p=(href.match(/[?&]path=([^&]*)/)||[])[1];
    const _emb=_p&&window.__DASH_DOCS__?window.__DASH_DOCS__[decodeURIComponent(_p)]:null;
    if(_emb){ v.body.classList.add('ev-md'); v.body.innerHTML=mdToHtml(_emb); v.body.scrollTop=0; return; }
  }
  try{""",
        "A2 embedded-document branch")
    one("""    return EVIDENCE_LIVE""", """    return (EVIDENCE_LIVE || DOCEMB(x.url))""", "A3 cited-source link")
    one("""    const docLi=EVIDENCE_LIVE?""", """    const docLi=(EVIDENCE_LIVE||DOCEMB(fp))?""", "A4 document link")
    one("""  const links=files.map(fp=> EVIDENCE_LIVE""", """  const links=files.map(fp=> (EVIDENCE_LIVE || DOCEMB(fp))""", "A5 working-notes links")

    # ---------- B. baseline explainers ----------
    one("function drawBaselineChart(id, cfs, overlays){", HELPERS + "function drawBaselineChart(id, cfs, overlays){",
        "B1 helpers")
    one("Filter or sort, and <b>click any row to chart it</b>. ◇ = provisional.",
        "Filter or sort, and <b>open any row</b> for its chart and the readings behind it. "
        "◇ = provisional. ⚠ marks a series whose latest year is a part-year figure.",
        "B2 section description")
    one("""        tr.innerHTML=`<td><b>${esc(f.country)}</b></td><td>${esc(f.metric)}</td>
          <td class="small">${esc(a.year)}: ${fmtNum(a.value)}${a.n>1?` <span class="muted">mean of ${a.n}</span>`:''}</td>""",
        """        const _prov=!!a.provisional, _nsig=blSignals(f).length;
        tr.innerHTML=`<td><span class="bl-chev"></span><b>${esc(f.country)}</b></td><td>${esc(f.metric)}</td>
          <td class="small">${esc(a.year)}: ${fmtNum(a.value)}${a.n>1?` <span class="muted">mean of ${a.n}</span>`:''}${_prov?' <span class="bl-prov" title="The latest reported point is provisional (part-year or not yet final), so every line starts from a figure that may still change">&#9888;</span>':''}</td>""",
        "B4 row cells")
    one("""          <td class="small">${_r.sig!=null?fmtNum(_r.sig):_r.rule!=null?'~'+fmtNum(_r.rule):'<span class="muted">\\u2014</span>'}</td>`;""",
        """          <td class="small">${_r.sig!=null?fmtNum(_r.sig):_r.rule!=null?'~'+fmtNum(_r.rule):'<span class="muted">\\u2014</span>'}${_nsig?` <span class="bl-nsig" title="Signals recorded in this market for this product line">${_nsig} signal${_nsig>1?'s':''}</span>`:''}</td>`;""",
        "B6 signals cell chip")
    one("""        td.innerHTML=`<div class="chart-panel"><div class="chartbox"><canvas id="${cid2}"></canvas></div></div><div class="small muted evsrc">Source: dated market workbook + ECB series; trend-fit by the statistics agent.</div>`;""",
        """        td.innerHTML=`<div class="chart-panel"><div class="chartbox"><canvas id="${cid2}"></canvas></div></div>`
          + blHowHtml(f) + blLinesHtml(f);""",
        "B7 detail panel")
    one("""          const closed=det.style.display==="none"; det.style.display=closed?"":"none";""",
        """          const closed=det.style.display==="none"; det.style.display=closed?"":"none";
          tr.classList.toggle('bl-open', closed);""",
        "B8 chevron state")
    return box[0]
