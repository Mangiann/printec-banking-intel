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

# ---------- C. "Ask the data": a chat over the dashboard's own data, answered by the viewer's Claude ----------
# Appended to app.js at build time (artifact only). Uses the artifact runtime's `sample` capability: the page
# builds the question (instructions + a fact sheet + the last turns), offers a few page functions as tools,
# and the claude.ai viewer runs it on the viewer's own account. Hidden wherever the capability is absent.
ASK_JS = r"""
/* ---- Ask the data (artifact build) ------------------------------------------------------------ */
(function(){
  const clip=(s,n)=>{ s=String(s==null?'':s).replace(/\s+/g,' ').trim(); return s.length>n?s.slice(0,n-1)+'…':s; };
  const Mm=v=>(v==null||isNaN(v))?'-':('EUR '+(Number(v)/1e6).toFixed(2)+'m');
  const pct=v=>(v==null||isNaN(v))?'-':((v>=0?'+':'')+Number(v).toFixed(1)+'%');
  const unlocked=()=>!!(DASH && DASH.budget_2027_board);   // the base budget ships in plain text (24/09/2026)
  const cname=c=>(DASH.code2name||{})[c]||c;
  const codeOf=t=>{ t=String(t||'').trim(); if(!t) return ''; const up=t.toUpperCase(); if((DASH.code2name||{})[up]) return up; const hit=Object.entries(DASH.code2name||{}).find(([k,v])=>String(v).toLowerCase()===t.toLowerCase()||String(v).toLowerCase().startsWith(t.toLowerCase())); return hit?hit[0]:''; };
  const lineOf=t=>{ t=String(t||'').trim().toLowerCase(); if(!t) return ''; const L=DASH.prod_label||{}; if(L[t]) return t; const hit=Object.entries(L).find(([k,v])=>String(v).toLowerCase().includes(t)||k.includes(t.replace(/\s+/g,'_'))); return hit?hit[0]:''; };
  const sigBrief=s=>({key:s.key, title:s.bank_theme, countries:(s.countries||[]).map(cname), products:(s.products||[]).map(p=>(DASH.prod_label||{})[p]||p), band:s.size_band||'', confidence:s.confidence||'', date:clip(s.date,160), trigger_date:s.future_date||'', lane:s.lane||'', implies:clip(s.implies,320)});

  /* ---- how the dashboard is built: labels, columns, cards and rules, so questions about the page itself
          can be answered, not only questions about the figures ---- */
  function glossary(){
    const G=[];
    G.push('HOW THE DASHBOARD IS BUILT. Tabs: '+(typeof TABS!=='undefined'?TABS.map(t=>t.label+' = '+clip(t.sub,160)).join(' | '):''));
    G.push('Signals are the dashboard\u2019s units of evidence: one development at one bank, market or regulation, with a date, a confidence (High, Medium-High, Medium, Low), the agents that confirmed it, source links, "what it implies" and a follow-up. Each signal has a lane: opportunity (a net-new deal Printec can win), installed base (a renewal or asset Printec already holds; not an opportunity), lost (a named competitor won it), or context (a macro driver or threat). Deal-size bands: XL at least EUR 5m, L EUR 1m to 5m, M EUR 0.2m to 1m, S under EUR 0.2m, unscoped = a real contest with no published value (counted as an opportunity, EUR 0 in value charts). Recency chips: fresh (development under 3 months old), recent, forward (a dated deadline ahead), standing (older than 6 months, kept as background). Opportunity value per market = the deal bands of its biddable signals added up.');
    G.push('Outlooks (Charts tab and "market outlook" everywhere): the mean of the dashboard\u2019s readings for a metric next year (patterns readings and signals readings), with the spread shown as low and high. There is no statistical trend fit anywhere. Projections start from the last reported point.');
    const single=!!(DASH.budget_2027_board&&DASH.budget_2027_board.single_number);
    G.push('BUDGET 2027 TAB, top to bottom. (1) The Budget group in the sidebar has "Budget 2027" (the EUR 180.0m budget, visible to every viewer) and, only after the Admin unlock, a nested "Stretched budget" (the same budget taken to EUR 200.0m; that page shows the stretch card, then the category view and the moves table on the stretch). On the Budget 2027 page, "Executive summary": a cyan panel with the number and '+(single?'two clickable estimate cards: "2026 budget" (the 2026 group budget target, second submission; it is a target, not actual revenue, because no actuals file exists yet) and "2027 base budget" (the single number to be signed: it rests on the deals in the signals, the growth of the markets, the contracts already held and the new business the capability decisions open; there is no separate lowest acceptable number, and no new staff are planned because the existing teams deliver the plan)'+(DASH.budget_2027_stretch?', and a third card "Stretch to EUR 200m": the budget taken to EUR 200.0m from new business and the payments industry only, with no named deal of the plan changed; clicking it shows the stretch in the moves table and the category view':'')+'. '
      :'four clickable estimate cards: "2026 budget" (the 2026 group budget target, second submission; it is a target, not actual revenue, because no actuals file exists yet), "Lowest acceptable" (the floor: the lowest number every view accepts once the plan\u2019s dated actions, hires and capability decisions have happened; it includes three named facts that make it double digits), "2027 budget" (the number to be signed, the plan\u2019s actions included), and "Maximum on the table" (the highest estimate in every line plus the new business the capability decisions open). ')+(DASH.budget_2027_board&&DASH.budget_2027_board.only_target?'The 2027 budget is the one and only 2027 number on the page: there is no lower, middle, reviewed or model figure to quote, and if asked for one, say the page carries a single target. ':'Under the cards a line says what the evidence supports today before the plan\u2019s actions and the reviewed budget before the plan; ')+'Clicking a card shows that estimate in the moves table. Then the summary paragraphs, and a fold "The full explanation" with the sections, the levers, the new business, the conditions and the views that would set a lower number. (2) "The moves, market by market": a table with the 15 markets down and the product lines across; each cell is one budget line (market x product line) showing the chosen estimate in EUR and its growth on 2026, coloured by the move it calls for. Moves: win = new revenue is budgeted and open opportunities or dated items exist to go after; find = new revenue is budgeted but the tool holds no open opportunity yet; defend = recurring revenue sits where competitors have won or several high-threat rivals compete; protect margin = the margin is well above the line\u2019s group average and strong rivals are present; market risk = new revenue is budgeted in a market the projections show shrinking; stretch = the market grows and opportunities are open against a small new-revenue target; watch = nothing dated, nothing threatening. Clicking a cell opens the details underneath: the 2027 number (2026 budget, '+(single?'':'lowest acceptable, ')+'2027 budget'+(single?'':', maximum')+(DASH.budget_2027_board&&DASH.budget_2027_board.only_target?'':', what the evidence supports today, the model\u2019s base and stretch')+'), the plan\u2019s actions for that line with kind, date, owner and euros, the reasoning, the delivery check, any lower view, then why this move, the dated items, the budget lines inside the cell, the high-threat rivals and the signals as cards. The column "Retail and other, carried flat" (earlier called "Not covered") holds the budget lines the market model does not analyse: retail lines (self-checkout, retail POS, store equipment, smart vending, Vendipack, telecom, printing and scanning; EUR 7.7m group-wide) and rows with no product name ("Other", "Other cash handling", "Other security and compliance", "Other branch equipment"; EUR 5.6m group-wide). They keep their 2026 figure in every estimate, count in the country total and have no move of their own; the finance view wants them given an owner and a 2027 number. Lines under EUR 0.05m are left blank. "Total" is the market\u2019s whole 2027 figure for the chosen estimate.');
    G.push('(1a) "Where the growth comes from", right under the executive summary: four drivers take the 2026 budget to the 2027 budget and each euro is counted once. Named deals = purchases banks and post offices have already announced (dated orders and tenders, share taken from competitors, capability decisions, and the deals the market model already counts after what competitors are expected to win). Market outlook = growth of the markets Printec already sells in, read from the dashboard\u2019s market readings, no statistical forecast; shown as a rate of 2026 revenue. Recurring revenue = service and outsourcing contracts already held, shown as a rate of the 2026 recurring base and split into better pricing at renewal and efficiency; the growth of the contracts held as the estates grow is presented inside those two steps. New business has a fold "What the new business is" naming the product lines (managed services, payments modernisation, fraud monitoring, self-service, compliance, digital identity and more), without amounts or countries. New business = products Printec does not yet sell in a country where the signals show banks buying; part of it depends on capability decisions Printec has yet to take. Each tile shows the amount, its share of the growth, what it is, what proves it, what is inside and the signals behind it. The same four drivers appear as a numbered strip inside the top panel. Under the tiles a waterfall chart "Step by step: every lever and the revenue it brings" runs from the 2026 budget through every lever (dated orders and tenders, share taken from competitors, capability decisions, deals the market model already counts, growth of the markets, better pricing, efficiency, and the three parts of new business) to the 2027 budget, and a table "How each step is achieved" gives for each lever the revenue it brings, the rate behind it (the lever\u2019s revenue divided by its 2026 base), how it is done, who owns it and by when.');
    if(DASH.budget_2027_stretch) G.push('(1c) "The stretch to EUR 200.0m", a card after the drivers: the 2027 budget of EUR 180.0m plus five layers, each with what it is, what proves it, its items and the signals behind it: (1) new business priced the way the plan priced its own (the country and product combinations where the signals show banks buying but the plan set no number, priced by the same rule the base budget used: what the plan set for its 29 new-business combinations divided by the opportunity value behind them, 5.3% with a 2027-dated opportunity and 3.6% without); (2) regulations and industry changes that hit every bank at once (the digital euro terminal specifications, the identity wallet, the anti-money-laundering rules, the DORA testing scope) counted in every payments line they affect at full weight, where the base budget counts them once per country at half weight; (3) acquiring estates at the full terminal-market rate instead of half; (4) one year of the payments industry\u2019s growth from the Future outlook on the payments software lines (identity 15.4%, anti-money-laundering 18.0%, key management 15.3%, instant payments 15.0%); (5) the payments combinations converting at a higher rate, still under the rate of the plan\u2019s best third. Then a waterfall, the narrative, what the new business is by product line with countries, the capability decisions the plan already names, the Future outlook themes, what must be true and the risks. Profit on the stretch is estimated at the 2026 group margin on the added revenue. In the moves table and the category view the stretch shows per line as the budget plus the payments extras; the new combinations sit in the country and line totals.');
    G.push('(1b) "The budget by category", between the executive summary and the moves table: the same 2027 numbers in the four categories of the Printec budget file, hardware (HW), software (SW), services (SV, which includes installation and maintenance) and outsourcing (OUT), with their subcategories (ATM, EFT-POS, Anti-Money Laundering, Self-Service Kiosks and so on). Five tiles (one per category, and profit at held category margins; retail lines and budget rows with no product name are carried flat at their 2026 value inside their own category, so there is no separate retail item), a waterfall chart for the group from the 2026 budget to the chosen estimate category by category, a second waterfall showing the same growth by what produces it (the model\u2019s recurring growth, the model\u2019s named deals and outlook, dated orders and tenders, share wins, hires, capability decisions, price steps, closing facts, balance), then a market picker with that market\u2019s waterfall, its category table (2026, the estimate, change, profit, margin, opening to subcategories with the product lines they belong to) and a written explanation per category. The split rules: a dated order or share win is divided the way the country\u2019s 2026 revenue for that subcategory already divides across the four categories; the model\u2019s recurring growth goes to services and outsourcing in their 2026 ratio; '+(single?'revenue that existing staff deliver goes to services (outsourcing for managed services)':'hires go to services (outsourcing for managed services)')+'; capability decisions go to software; price steps go to services and outsourcing;'+(single?'':' the closing facts follow the full mix;')+' a combination with no 2026 revenue uses the group mix for its line and a first outsourcing contract is 100% outsourcing under ATM; retail lines and rows with no product name are carried flat inside their own category; profit holds each country\u2019s 2026 margin by category and subcategory, which is why this profit differs a little from the line view\u2019s profit. The estimate cards above switch this section too.');
    G.push('How the 2027 model grows a line: the 2026 target is carried forward on three visible parts: the market outlook for the line\u2019s metric (ATMs, POS terminals, bank branches), the share Printec can take from the open opportunities (weighted by band: XL 3 points, L 2, M 1, S or unscoped 0.5; one point = one percent of new revenue; a footprint-wide regulation counts once per country at half weight in its lead line), and a threat haircut for recorded competitor wins and high-threat rivals. New revenue (hardware and software) takes the full rate; recurring revenue (services and outsourcing) moves at half the market rate. Margins are held at 2026 levels per line. A falling branch count is read as conversion demand for self-service and branch transformation (closing branches concentrates transformation in the branches that stay). "Single point" marks a cell where one deal carries at least half of its share part. New business = market x product combinations with opportunities in the signals but no 2026 budget. Board assumptions (conversion rates on named deals) are labelled judgments, never evidence. Views: the commercial, line and market views propose numbers; the finance, risk and outside (a bank buyer\u2019s) views challenge them; delivery confirms capacity ("delivery confirmed", "confirmed with hires", "not confirmed").');
    return G.join('\n');
  }

  /* ---- the fact sheet: what every question carries ---- */
  function factSheet(){
    const L=[];
    L.push('Dashboard week: '+(DASH.week||'')+'. Currency EUR. Figures are as published on the dashboard.');
    if(DASH.kpis) L.push('Headline figures: '+clip(JSON.stringify(DASH.kpis),600));
    L.push('\nMarkets (name: opportunity value EUR m, signals, high-confidence, new this week; ATMs; branches):');
    (DASH.countries||[]).filter(c=>c.n_signals||c.atms||c.branches).forEach(c=>L.push('- '+c.name+': value '+c.score+'m, '+c.n_signals+' signals, '+(c.n_high||0)+' high, '+(c.n_new||0)+' new; ATMs '+clip(c.atms,40)+'; branches '+clip(c.branches,40)));
    L.push('\nProduct lines (label: signals, opportunity value):');
    (DASH.products||[]).forEach(p=>L.push('- '+(p.label||p.name||p.id)+': '+(p.n_signals||0)+' signals'+(p.score!=null?', value '+p.score+'m':'')));
    const opps=(DASH.signals||[]).filter(s=>{ try{ return isOpportunity(s); }catch(e){ return !!s.is_opportunity; } }).slice().sort((a,b)=>potEur(b.size_band)-potEur(a.size_band)).slice(0,14);
    L.push('\nLargest open opportunities (key | title | markets | band | trigger date):');
    opps.forEach(s=>L.push('- '+s.key+' | '+clip(s.bank_theme,90)+' | '+(s.countries||[]).map(cname).join(', ')+' | '+(s.size_band||'')+' | '+(s.future_date||'no date')));
    const dl=(DASH.deadlines||[]).slice().sort((a,b)=>String(a.date).localeCompare(String(b.date))).slice(0,12);
    if(dl.length){ L.push('\nNext deadlines:'); dl.forEach(d=>L.push('- '+d.date+' '+clip(d.title,100)+' ('+(d.geography||[]).map(cname).join(', ')+')')); }
    if(DASH.competition_brief) L.push('\nCompetition summary this week: '+clip(DASH.competition_brief,1400));
    if((DASH.futures||[]).length) L.push('\nStructural trends to 2030 (titles): '+DASH.futures.map(f=>clip(f.headline||f.title||f.scope||'',80)).join(' | '));
    if(unlocked()){
      const B=DASH.budget_2027_board, T=B.totals;
      const single=!!B.single_number;
      L.push('\nBUDGET 2027: 2026 budget '+Mm(T.rev_2026)+(single?'':'; lowest acceptable '+Mm(T.floor)+' ('+pct(T.floor_growth_pct)+')')+'; 2027 budget '+Mm(T.commit)+' ('+pct(T.commit_growth_pct)+')'+(single?' (the single number: the highest estimate with every named deal counted as won; no separate lowest acceptable number; no hires planned, existing staff share the delivery)':'; maximum '+Mm(T.upside)+' ('+pct(T.upside_growth_pct)+')')+(T.supported_today?'; what the evidence supports today '+Mm(T.supported_today)+' ('+pct(T.supported_today_growth_pct)+')':'')+'. Profit at held margins: budget '+Mm(T.rp_commit)+'.');
      L.push('By market (2026 -> 2027 budget, growth): '+(B.by_country||[]).map(c=>c.country+' '+Mm(c.rev_2026)+' -> '+Mm(c.commit)+' ('+pct(c.commit_growth_pct)+')').join('; '));
      L.push('By line: '+(B.by_line||[]).map(l=>l.line_label+' '+Mm(l.rev_2026)+' -> '+Mm(l.commit)+(l.commit_growth_pct!=null?' ('+pct(l.commit_growth_pct)+')':'')).join('; '));
      const CT=DASH.budget_2027_categories; if(CT&&CT.group){ const G=CT.group; const one=!G.floor||!G.upside; L.push('By category (2026 -> 2027 budget'+(one?'':'; floor; maximum')+'): '+(CT.categories||[]).map(k=>(CT.cat_label||{})[k]+' ('+k+') '+Mm(G.y2026[k])+' -> '+Mm(G.budget[k])+(one?'':'; '+Mm(G.floor[k])+'; '+Mm(G.upside[k]))).join('; ')+'; retail flat '+Mm(Object.values(G.flat||{}).reduce((a,b)=>a+b,0))+'. Profit at held category margins, budget: '+Mm(G.rp_total_budget)+'.'); }
      const STx=DASH.budget_2027_stretch; if(STx&&STx.layers) L.push('STRETCH TO EUR 200.0m (new business and the payments industry only; no named deal changed): '+Mm(STx.start)+' -> '+Mm(STx.total)+' ('+pct(STx.growth_pct)+' on 2026)'+(STx.unsupported>5e4?'; '+Mm(STx.unsupported)+' not yet backed by a signal':'')+'. Layers: '+STx.layers.map(l=>l.title+' '+Mm(l.eur)+' ('+l.n+' items)').join('; ')+'. New business it adds by line: '+(STx.new_business_lines||[]).map(r=>r.line+' '+Mm(r.eur)+' in '+r.countries.join(', ')).join('; ')+'. Rates: '+(STx.rates.dated*100).toFixed(1)+'% of opportunity value with a 2027-dated opportunity, '+(STx.rates.undated*100).toFixed(1)+'% without; payments combinations at '+((STx.rates.undated+STx.rates.payments_uplift)*100).toFixed(1)+'% against '+(STx.rates.best_third*100).toFixed(0)+'% for the plan\u2019s best third.'+(STx.texts&&STx.texts.headline?' '+STx.texts.headline:''));
      if(B.drivers&&B.drivers.items) L.push('Growth drivers ('+Mm(B.drivers.from)+' + '+Mm(B.drivers.growth)+' = '+Mm(B.drivers.to)+'): '+B.drivers.items.map(d=>d.title+' '+Mm(d.eur)+(d.rate_pct!=null?' = +'+d.rate_pct+'% of '+d.rate_of:'')+' ('+d.share_pct+'% of the growth; inside: '+(d.inside||[]).map(x=>x[0]+' '+Mm(x[1])).join(', ')+(d.lines?'; what it is: '+d.lines.map(r=>r.line+' '+Mm(r.eur)+' in '+r.countries.join(', ')).join('; '):'')+'). '+d.proof).join(' | '));
      if(B.drivers&&B.drivers.levers) L.push('Levers (revenue, rate on its 2026 base, how, who, by when): '+B.drivers.levers.map(l=>l.label+' +'+Mm(l.eur)+(l.rate!=null?' = '+l.rate+'% of '+l.rate_of:'')+'; '+l.how+' ['+(l.who||'')+'; '+(l.when||'')+']').join(' | '));
      if(B.report && B.report.executive_summary_md) L.push('Executive summary: '+clip(B.report.executive_summary_md.replace(/\*\*/g,''),2600));
    } else {
      L.push('\nNo budget data is in this build.');
    }
    const ctx=[]; ctx.push('The viewer is on the "'+(current||'')+'" tab.');
    const det=document.querySelector('.bg-detail:not([hidden]) .bg-detail-h b'); if(det) ctx.push('Open budget line: '+clip(det.textContent,80)+'.');
    const sg=document.querySelector('.sig.open .t'); if(sg) ctx.push('Open signal: '+clip(sg.textContent,90)+'.');
    L.push('\nContext: '+ctx.join(' '));
    return clip(L.join('\n'),24000).replace(/…$/,'');
  }

  /* ---- page functions Claude may call ---- */
  const tools=[
    {name:'search_signals', description:'Search the dashboard’s market signals by words, optionally filtered by market and product line. Returns up to 8 matches with key, title, markets, band, confidence, dates and a short implication. Use it before answering anything about a bank, a tender, a regulation or a market development.',
     inputSchema:{type:'object',properties:{query:{type:'string'},country:{type:'string',description:'market name or code, optional'},product:{type:'string',description:'product line name, optional'}},required:['query']},
     execute(inp){ const q=String(inp.query||'').toLowerCase().split(/[^a-z0-9À-ɏ]+/).filter(w=>w.length>2); const cc=codeOf(inp.country), ln=lineOf(inp.product);
       const all=(DASH.signals||[]); const hays=all.map(s=>(s.bank_theme+' '+s.implies+' '+s.signal).toLowerCase()); const wt={}; q.forEach(w=>{ const df=hays.filter(h=>h.includes(w)).length; wt[w]=df?1/(1+Math.log(df)):0; }); const scored=all.map((s,i)=>{ if(cc&&!(s.countries||[]).includes(cc)) return null; if(ln&&!(s.products||[]).includes(ln)) return null; const hay=hays[i]; let sc=0; q.forEach(w=>{ if(!wt[w]) return; if(hay.includes(w)) sc+=wt[w]; if(String(s.bank_theme||'').toLowerCase().includes(w)) sc+=2*wt[w]; }); return sc?{sc,s}:null; }).filter(Boolean).sort((a,b)=>b.sc-a.sc).slice(0,8);
       if(!scored.length) return {matches:[], note:'no signal matches these words'+(cc?' in '+cname(cc):'')};
       return {matches:scored.map(x=>sigBrief(x.s))}; }},
    {name:'get_signal', description:'Return one signal in full by its key: the development, what it implies for Printec, the recommended follow-up, likelihood, product lines and the source links. Use after search_signals when the detail matters.',
     inputSchema:{type:'object',properties:{key:{type:'string'}},required:['key']},
     execute(inp){ const s=sigByKey[String(inp.key||'')]; if(!s) throw new Error('no signal with key '+inp.key); return Object.assign(sigBrief(s),{signal:clip(s.signal,3200), implies:clip(s.implies,1600), follow_up:clip(s.follow_up,600), likelihood:clip(s.likelihood,300), sources:(s.sources||[]).map(x=>({text:x.text,url:x.url})).slice(0,8)}); }},
    {name:'get_market', description:'Return one market (country): its opportunity value, signal counts, ATM, branch and instant-payment figures, the implication written for it, the 2027 outlook readings, and its ten largest signals (keys and titles).',
     inputSchema:{type:'object',properties:{country:{type:'string',description:'market name or two-letter code'}},required:['country']},
     execute(inp){ const cc=codeOf(inp.country); if(!cc) throw new Error('unknown market '+inp.country); const c=(DASH.countries||[]).find(x=>x.name===cname(cc))||{}; const sigs=(DASH.signals||[]).filter(s=>(s.countries||[]).includes(cc)).sort((a,b)=>potEur(b.size_band)-potEur(a.size_band)).slice(0,10);
       const ol=(DASH.projection_consensus||[]).filter(r=>r.country===cname(cc)).map(r=>({metric:r.metric, year:r.year, mean_pct:r.mean_pct, low_pct:r.low_pct, high_pct:r.high_pct, readings:r.n}));
       return {market:cname(cc), value_eur_m:c.score, signals:c.n_signals, high_confidence:c.n_high, new_this_week:c.n_new, atms:clip(c.atms,300), branches:clip(c.branches,300), instant_payments:clip(c.instant,300), implication:clip(c.implication,900), outlook_2027:ol, top_signals:sigs.map(s=>({key:s.key,title:clip(s.bank_theme,110),band:s.size_band||'',trigger_date:s.future_date||''}))}; }},
    {name:'get_product_line', description:'Return one Printec product line: its signal count and value on the dashboard, the outlook written for it, and its ten largest signals (keys and titles).',
     inputSchema:{type:'object',properties:{product:{type:'string',description:'product line name, e.g. ATM, POS, managed services, compliance, self-service'}},required:['product']},
     execute(inp){ const ln=lineOf(inp.product); if(!ln) throw new Error('unknown product line '+inp.product); const p=(DASH.products||[]).find(x=>x.id===ln||x.key===ln||x.line===ln)||{}; const po=(DASH.product_outlooks||[]).find(x=>x.product===ln||x.id===ln)||{};
       const sigs=(DASH.signals||[]).filter(s=>(s.products||[]).includes(ln)).sort((a,b)=>potEur(b.size_band)-potEur(a.size_band)).slice(0,10);
       return {line:(DASH.prod_label||{})[ln]||ln, signals:p.n_signals, value_eur_m:p.score, outlook:clip(po.projection||po.summary||po.headline||'',900), top_signals:sigs.map(s=>({key:s.key,title:clip(s.bank_theme,110),markets:(s.countries||[]).map(cname),band:s.size_band||''}))}; }},
    {name:'get_competitor', description:'Return one competitor or partner from the watchlist: role, threat level, markets, product lines and its latest recorded moves.',
     inputSchema:{type:'object',properties:{name:{type:'string'}},required:['name']},
     execute(inp){ const q=String(inp.name||'').toLowerCase(); const v=(DASH.competitors||[]).find(x=>String(x.name||'').toLowerCase().includes(q)); if(!v) throw new Error('no competitor matching '+inp.name); return {name:v.name, role:v.role, threat:v.threat, markets:(v.countries||[]).map(cname), products:(v.products||[]).map(p=>(DASH.prod_label||{})[p]||p), latest:clip(v.latest,2400), last_updated:v.last_updated||''}; }},
    {name:'list_deadlines', description:'List dated items (regulatory deadlines, tender dates, milestones), optionally for one market, sorted by date. Returns up to 20.',
     inputSchema:{type:'object',properties:{country:{type:'string',description:'optional market'}},required:[]},
     execute(inp){ const cc=codeOf(inp.country); const d=(DASH.deadlines||[]).filter(x=>!cc||(x.geography||[]).includes(cc)).slice().sort((a,b)=>String(a.date).localeCompare(String(b.date))).slice(0,20); return {deadlines:d.map(x=>({date:x.date,title:clip(x.title,140),type:x.type||'',markets:(x.geography||[]).map(cname),products:(x.products||[]).map(p=>(DASH.prod_label||{})[p]||p)}))}; }},
    {name:'get_budget_line', description:'Only when the 2027 budget view is unlocked: return the budget lines for a market, a product line, or one market-and-line cell: the 2026 budget, the lowest acceptable, the 2027 budget and the maximum, the reasoning, the actions with dates and owners, and the signals behind them. Throws if the budget is locked.',
     inputSchema:{type:'object',properties:{country:{type:'string',description:'optional market'},product:{type:'string',description:'optional product line'}},required:[]},
     execute(inp){ if(!unlocked()) throw new Error('the 2027 budget view is locked; ask the viewer to unlock it with the Admin link'); const B=DASH.budget_2027_board; const cc=codeOf(inp.country), ln=lineOf(inp.product);
       let cells=(B.cells||[]).concat(B.new_business||[]).filter(o=>(!cc||o.code===cc)&&(!ln||o.line===ln)); if(!cells.length) throw new Error('no budget line for that market and product'); cells=cells.sort((a,b)=>b.board.target-a.board.target).slice(0,6);
       const sg=!!B.single_number; return {lines:cells.map(o=>({market:o.country, line:o.line_label, budget_2026:Mm(o.target_2026), ...(sg?{}:{lowest_acceptable:Mm(o.board.floor)}), budget_2027:Mm(o.board.target), growth:pct(o.board.growth_pct), ...(sg?{}:{maximum:Mm(o.board.upside)}), ...(B.only_target?{}:{supported_today:o.board.today?Mm(o.board.today.target):''}), plan_adds_to_budget:o.board.plan_budget_delta!=null?Mm(o.board.plan_budget_delta):'', ...((DASH.budget_2027_stretch&&(DASH.budget_2027_stretch.cells||[]).find(x=>x.code===o.code&&x.line===o.line)&&(DASH.budget_2027_stretch.cells||[]).find(x=>x.code===o.code&&x.line===o.line).extra>0)?{stretch_2027:Mm((DASH.budget_2027_stretch.cells||[]).find(x=>x.code===o.code&&x.line===o.line).stretch)}:{}), ...(sg?{}:{plan_adds_to_floor:o.board.plan_floor_delta!=null?Mm(o.board.plan_floor_delta):'', floor_includes_closing_fact:o.board.gap_closer_eur?Mm(o.board.gap_closer_eur)+' (one of the three named facts that make the floor double digits)':''}), move:((DASH.budget||{}).cells||[]).filter(c=>c.code===o.code&&c.line===o.line).map(c=>c.action)[0]||'', reason:clip(o.board.reason,900), actions:(o.board.plan_actions||[]).slice(0,8).map(a=>({what:clip(a.what,180),kind:a.kind,by:a.by,owner:a.owner,budget_eur:a.eur_budget})), signals:(o.board.evidence||[]).slice(0,8)}))}; }},
    {name:'list_moves', description:'List the budget lines that carry a given move in the moves table (win, find, defend, protect margin, market risk, stretch, watch), optionally for one market: market, product line, the move, the 2026 budget, the 2027 budget and the reason the move fired. Use it for questions like \u201cwhich lines are protect margin\u201d or \u201cwhat are the moves in Greece\u201d.',
     inputSchema:{type:'object',properties:{move:{type:'string',description:'one of win, find, defend, protect margin, market risk, stretch, watch; optional'},country:{type:'string',description:'optional market'}},required:[]},
     execute(inp){ const cells=((DASH.budget||{}).cells||[]); if(!cells.length) throw new Error('the moves table is not available in this session'); const mv=String(inp.move||'').toLowerCase().trim(); const cc=codeOf(inp.country);
       const B=DASH.budget_2027_board; const bk={}; if(B){ (B.cells||[]).forEach(o=>bk[o.code+'|'+o.line]=o); }
       const rows=cells.filter(c=>c.target>=5e4&&(!mv||c.action===mv)&&(!cc||c.code===cc)).sort((a,b)=>b.target-a.target).slice(0,25);
       if(!rows.length) return {lines:[], note:'no budget line carries that move'+(cc?' in '+cname(cc):'')};
       return {count:rows.length, lines:rows.map(c=>{ const b=bk[c.code+'|'+c.line]; return {market:c.country, line:c.line_label, move:c.action, budget_2026:Mm(c.target), budget_2027:b?Mm(b.board.target):'', margin_pct:c.margin_pct, why:clip((c.reasons||[]).join(' '),260)}; })}; }},
    {name:'get_budget_categories', description:'The 2027 budget in the categories of the Printec budget file (hardware, software, services, outsourcing) for the group or one market: 2026, lowest acceptable, budget, maximum and profit per category, the subcategories with their numbers, what produces each category\u2019s growth, and the written explanation. Only after the Admin unlock.',
     inputSchema:{type:'object',properties:{country:{type:'string',description:'market name; omit for the group'}},required:[]},
     execute(inp){ const CT=DASH.budget_2027_categories; if(!unlocked()||!CT||!CT.group) throw new Error('the budget view is locked in this session'); const cats=CT.categories||[]; const CL=CT.cat_label||{};
       const row=(o,rp)=>Object.fromEntries(cats.map(k=>[CL[k]+' ('+k+')',{budget_2026:Mm(o.y2026[k]),...(o.floor?{lowest_acceptable:Mm(o.floor[k])}:{}),budget_2027:Mm(o.budget[k]),...(o.upside?{maximum:Mm(o.upside[k])}:{}),profit_budget:Mm((o.rp_budget||{})[k])}]));
       if(!inp.country){ const G=CT.group; const bs=(CT.by_source||{}).budget||{}; return {scope:'group',categories:row(G),retail_flat:Mm(Object.values(G.flat||{}).reduce((a,b)=>a+b,0)),total_2026:Mm(G.total_y2026),total_budget_2027:Mm(G.total_budget),profit_budget_at_category_margins:Mm(G.rp_total_budget),growth_by_source_budget:Object.fromEntries(Object.entries(bs).map(([k,v])=>[k,Mm(Object.values(v).reduce((a,b)=>a+b,0))])),rules:CT.rules}; }
       const cc=codeOf(inp.country); if(!cc) throw new Error('unknown market '+inp.country); const C=(CT.countries||[]).find(x=>x.code===cc); if(!C) throw new Error('no category data for '+cname(cc));
       return {market:C.country,categories:row(C),retail_flat:Mm(Object.values(C.flat||{}).reduce((a,b)=>a+b,0)),total_2026:Mm(C.total_y2026),total_budget_2027:Mm(C.total_budget),profit_budget:Mm(C.rp_total_budget),subcategories:(C.subs||[]).filter(x=>!x.flat).map(x=>({category:x.cat,subcategory:x.sub,budget_2026:Mm(x.y2026),budget_2027:Mm(x.budget),product_lines:x.lines})),explanation:C.text}; }},
    {name:'get_stretch', description:'The stretch to EUR 200.0m: the 2027 budget taken to EUR 200.0m from new business and the payments industry only, no named deal changed. Returns the total, the five layers with their amounts and explanations, the largest items of each layer, what the new business is by product line and country (optionally for one market), the capability decisions, the Future outlook themes, what must be true and the risks. Only after the Admin unlock.',
     inputSchema:{type:'object',properties:{country:{type:'string',description:'market name; omit for the group'}},required:[]},
     execute(inp){ const S=DASH.budget_2027_stretch; if(!unlocked()||!S||!S.layers) throw new Error('the stretch view is locked or not built'); const cc=codeOf(inp.country);
       const items=l=>(l.items||[]).filter(x=>!cc||x.code===cc).slice(0,8).map(x=>({market:x.country,line:x.line_label,eur:Mm(x.eur!=null?x.eur:x.stretch),rate:x.rate_total!=null?(x.rate_total*100).toFixed(1)+'%':x.rate!=null?(x.rate*100).toFixed(1)+'%':undefined,largest_signal:x.largest||undefined,why:x.why||x.note||undefined}));
       const out={total:Mm(S.total),budget:Mm(S.start),added:Mm(S.total-S.start),growth_on_2026:pct(S.growth_pct),not_backed_by_a_signal:S.unsupported>5e4?Mm(S.unsupported):'none',layers:S.layers.map(l=>({title:l.title,eur:Mm(l.eur),items:l.n,what:l.what,proof:l.proof,largest:items(l)})),
         new_business_by_line:(S.new_business_lines||[]).map(r=>({line:r.line,eur:Mm(r.eur),countries:r.countries})),rates:{with_2027_dated_opportunity:(S.rates.dated*100).toFixed(1)+'%',without:(S.rates.undated*100).toFixed(1)+'%',payments_combinations:((S.rates.undated+S.rates.payments_uplift)*100).toFixed(1)+'%',plans_best_third:(S.rates.best_third*100).toFixed(0)+'%'},
         capability_decisions:(S.capabilities||[]).map(c=>c.area+' ('+c.decision+', by '+c.by+', '+c.owner+')'),future_outlook:(S.futures||[]).map(f=>f.scope),profit_on_the_stretch:Mm(S.rp_stretch),conditions:(S.texts||{}).conditions||[],risks:(S.texts||{}).risks||[]};
       if(cc){ out.market=cname(cc); out.new_combinations=(S.new_cells||[]).filter(x=>x.code===cc).map(x=>({line:x.line_label,eur:Mm(x.stretch),rate:(x.rate*100).toFixed(1)+'%',largest_signal:x.largest,reason:x.reason})); out.by_country=(S.by_country||[]).filter(c=>c.code===cc).map(c=>({budget:Mm(c.budget),stretch:Mm(c.stretch)}))[0]; }
       return out; }},
    {name:'get_outlook', description:'Return the 2027 outlook readings for a market: for each metric (ATMs, POS terminals, bank branches, cash) the mean growth, the range and the number of readings, as shown on the Charts tab. There is no statistical trend fit; readings come from patterns and signals.',
     inputSchema:{type:'object',properties:{country:{type:'string'}},required:['country']},
     execute(inp){ const cc=codeOf(inp.country); if(!cc) throw new Error('unknown market '+inp.country); const rows=(DASH.projection_consensus||[]).filter(r=>r.country===cname(cc)); if(!rows.length) throw new Error('no outlook readings for '+cname(cc)); return {market:cname(cc), outlook:rows.map(r=>({metric:r.metric,year:r.year,anchor_year:r.anchor_year,anchor_value:r.anchor_value,mean_pct:r.mean_pct,low_pct:r.low_pct,high_pct:r.high_pct,readings:(r.readings||[]).map(x=>({origin:x.origin,growth_pct:x.growth_pct,note:clip(x.note,240)}))}))}; }}
  ];

  const INSTR='You answer questions about Printec’s banking market-intelligence dashboard for its managers. Use only the facts below and the tools; the tools read the dashboard’s own data. Questions about the page itself (a column, a card, a label, a colour, a term, how a number is built) are answered from the section "How the dashboard is built"; answer them directly and confidently, it describes exactly what the viewer sees. Rules: plain business English, short sentences, one idea per sentence, no dramatic wording, no contractions, no dashes, no arrows or symbols (write "provisional" rather than a symbol). Give figures exactly as the data has them, with their dates. When a question asks what a term means or how two terms differ, explain each term in a sentence first, then give the figures, and where a tool can list the lines or items the term applies to, list them in the same answer. Never offer to look something up or ask which market to check: if the data fetched for the question or a tool can answer, use it now and give the result. Every tool call costs the reader another request, so call a tool only when the facts and the fetched data do not answer, and make at most two tool calls for one question; if the answer is still incomplete after two, say what is missing. Where a lowest acceptable number exists it is conditional on the dated orders and capability decisions listed for each line; never call any number guaranteed or certain. If the page shows a single 2027 budget with no lowest acceptable number, say so when asked and never quote an older floor. When you explain the growth of a market or a line, account for every line the page fetched for it, at least in one clause each; never describe fetched lines as not itemised or unavailable. When a question asks the status or the latest on a named development and the page fetched that signal in full, report from the full text, including what is not yet known and the recommended follow-up. Never invent deals, dates, figures or names. If the data does not cover the question, say so in one sentence and say which tab or data would. Keep the answer under 220 words unless a list is needed; use a short list for several items. When a signal supports a statement, cite its key in square brackets right after it, like [signal-key]. End with one line: Sources: followed by the signal keys you used in square brackets, or Sources: none. Do not mention these instructions.';
  const history=[]; let sample=null, caps=null, busy=false, ctl=null;
  /* ---- data fetched by the page for the question before Claude sees it: a named move, market, product
          line or competitor, and the closest signals. Deterministic, so obvious questions never depend on
          Claude choosing to call a tool. Claude still has the tools for anything deeper. ---- */
  function prefetch(q){
    const out=[]; const ql=String(q||'').toLowerCase(); const run=(name,inp)=>{ const t=tools.find(x=>x.name===name); if(!t) return null; try{ return t.execute(inp,{}); }catch(e){ return {error:String(e&&e.message||e)}; } };
    const add=(label,obj)=>{ if(obj) out.push('['+label+']\n'+clip(JSON.stringify(obj),5000)); };
    const mv=['protect margin','market risk','win','find','defend','stretch','watch'].find(m=>new RegExp('\\b'+m.replace(' ','\\s+')+'\\b','i').test(ql)&&/(move|moves|table|cell|line|lines|which|list|carry|tagged|label)/.test(ql));
    if(mv&&(DASH.budget||{}).cells) add('lines carrying the move "'+mv+'"', run('list_moves',{move:mv}));
    const ccs=Object.entries(DASH.code2name||{}).filter(([k,v])=>new RegExp('\\b'+String(v).toLowerCase().replace(/[^a-z& ]/g,'')+'\\b','i').test(ql)).map(([k])=>k).slice(0,2);
    ccs.forEach(cc=>{ add('market '+cname(cc), run('get_market',{country:cc})); if(unlocked()) add('budget lines, '+cname(cc), run('get_budget_line',{country:cc})); });
    const comp=(DASH.competitors||[]).find(v=>{ const n=String(v.name||'').toLowerCase().replace(/['\u2019]s?$/,''); return n.length>3&&ql.includes(n.split(' ')[0].replace(/[^a-z]/g,''))&&ql.includes(n.split(' ')[0].replace(/[^a-z]/g,'')); });
    if(comp) add('competitor '+comp.name, run('get_competitor',{name:comp.name}));
    const lineWords={atm:'ATM',pos:'POS','managed service':'managed services',outsourc:'managed services','self-service':'self-service','self service':'self-service',kiosk:'self-service',compliance:'compliance',fraud:'fraud','digital identity':'digital identity',onboarding:'digital identity','card issuing':'card issuing'};
    if(/hardware|software|\bservices\b|outsourcing|categor|waterfall|\bhw\b|\bsw\b|\bsv\b|\bout\b/.test(ql)&&unlocked()&&DASH.budget_2027_categories) add('budget by category'+(ccs.length?', '+cname(ccs[0]):' (group)'), run('get_budget_categories',ccs.length?{country:ccs[0]}:{}));
    if(/stretch|200 ?m|200 million|two hundred/.test(ql)&&unlocked()&&DASH.budget_2027_stretch) add('the stretch to EUR 200.0m'+(ccs.length?', '+cname(ccs[0]):''), run('get_stretch',ccs.length?{country:ccs[0]}:{}));
    const lw=Object.keys(lineWords).find(w=>ql.includes(w)); if(lw&&!ccs.length) add('product line', run('get_product_line',{product:lineWords[lw]}));
    if(/deadline|deadlines|dated|due|when/.test(ql)) add('dated items'+(ccs.length?' in '+cname(ccs[0]):''), run('list_deadlines',ccs.length?{country:ccs[0]}:{}));
    const sr=run('search_signals',{query:q}); if(sr&&sr.matches&&sr.matches.length){ add('closest signals to the question (candidates; open with get_signal if needed)', {matches:sr.matches.slice(0,5)});
      const stop=/^(about|after|before|which|where|what|when|their|there|these|those|with|from|does|have|will|would|should|could|status|latest|update|tender|bank|banks|market|budget|signal|signals|dashboard|printec)$/;
      const words=ql.replace(/[^a-z0-9\s]/g,' ').split(/\s+/).filter(w=>w.length>=5&&!stop.test(w));
      const top=sr.matches.slice(0,5).find(m=>{ const tl=String(m.title||'').toLowerCase(); return words.some(w=>tl.includes(w)); });
      if(top) add('the closest signal in full (the question names it)', run('get_signal',{key:top.key})); }
    return out.join('\n\n');
  }
  function buildInput(q){
    let hist='';
    history.slice(-3).forEach(t=>{ hist+='\nQ: '+clip(t.q,500)+'\nA: '+clip(t.a,1400)+'\n'; });
    const pre=prefetch(q);
    return INSTR+'\n\n=== HOW THE DASHBOARD IS BUILT (labels, columns, cards, rules) ===\n'+glossary()+'\n\n=== DASHBOARD FACTS ===\n'+factSheet()+(pre?'\n\n=== DATA THE PAGE FETCHED FOR THIS QUESTION (use it; call a tool only for what is missing) ===\n'+pre:'')+(hist?'\n\n=== EARLIER IN THIS CONVERSATION ===\n'+hist:'')+'\n\n=== QUESTION ===\n'+q;
  }
  function renderAnswer(text){
    let body=String(text||''); const keys=[]; body=body.replace(/\[([a-z0-9][a-z0-9-]{5,})\]/g,(m,k)=>{ if(sigByKey[k]&&!keys.includes(k)) keys.push(k); return sigByKey[k]?'':m; });
    body=body.replace(/\n?\s*Sources?:\s*(none|.*)$/i,'').trim();
    const chips=keys.length?`<div class="ol-builton"><span class="ol-evk">Sources</span> ${keys.map(k=>`<span class="srcfile ol-sig" data-sigkey="${esc(k)}" role="button" tabindex="0" title="Show this signal &amp; its sources">${esc(sigByKey[k].bank_theme)}</span>`).join('')}<div class="ol-sigdetail" hidden></div></div>`:'';
    return mdToHtml(body)+chips;
  }
  const SUGG={overview:['What changed this week?','Which markets have the most open opportunities?','What are the next deadlines?'],
    budget:['Where does the growth of the base budget come from?','Which deals carry the Romanian budget?','How does hardware grow in 2027?'],
    budget_stretch:['What is the stretched budget made of?','Which new business does the stretch add in Slovakia?','What must be true for the stretched budget?'],
    country:['What is the outlook for ATMs in Bulgaria?','Which Ukrainian tenders are open?','Where is Printec strongest?'],
    product:['Which product line has the most opportunities?','What drives POS growth?','What is happening in managed services?'],
    competition:['What did Brink’s and NCR Atleos do this quarter?','Who threatens the Greek ATM business?','Which rivals are high threat in Romania?'],
    signals:['Which signals are new this week?','List the XL opportunities with a 2027 date.','What is the single largest deal on the table?'],
    futures:['What does the market look like by 2030?','Which trends hurt the cash business?','Where are the hidden opportunities?']};
  function mount(){
    const fab=el("button","ask-fab"); fab.type='button'; fab.innerHTML='<span class="ask-fab-dot"></span>Ask the data'; fab.title='Ask a question about what this dashboard shows';
    const dr=el("div","ask-drawer"); dr.setAttribute('role','dialog'); dr.setAttribute('aria-label','Ask the data');
    dr.innerHTML=`<div class="ask-head"><div><div class="ask-kicker">Ask the data</div><div class="ask-sub">Answers come from this dashboard’s signals, figures and budget, with the sources linked. Your own Claude account answers them. <span class="ask-build">${BUILD}</span></div></div><button type="button" class="ask-close" aria-label="Close">×</button></div>
      <div class="ask-body"><div class="ask-sugg"></div><div class="ask-msgs"></div></div>
      <form class="ask-form"><textarea class="ask-in" rows="2" placeholder="Ask about a market, a bank, a deal, a competitor, a number…" aria-label="Your question"></textarea><div class="ask-row"><span class="ask-status small muted"></span><button type="submit" class="ask-go">Ask</button></div></form>`;
    document.body.appendChild(fab); document.body.appendChild(dr);
    const msgs=dr.querySelector('.ask-msgs'), sugg=dr.querySelector('.ask-sugg'), form=dr.querySelector('.ask-form'), inp=dr.querySelector('.ask-in'), go=dr.querySelector('.ask-go'), status=dr.querySelector('.ask-status');
    const open=()=>{ dr.classList.add('show'); fab.classList.add('open'); drawSugg(); setTimeout(()=>inp.focus(),200); };
    const close=()=>{ dr.classList.remove('show'); fab.classList.remove('open'); };
    fab.addEventListener('click',()=>dr.classList.contains('show')?close():open()); dr.querySelector('.ask-close').addEventListener('click',close);
    function drawSugg(){ const list=SUGG[current]||SUGG.overview; sugg.innerHTML=(history.length?'':'<div class="ask-evk">Try</div>')+list.map(q=>`<button type="button" class="ask-chip">${esc(q)}</button>`).join(''); sugg.querySelectorAll('.ask-chip').forEach(b=>b.addEventListener('click',()=>{ inp.value=b.textContent; form.requestSubmit(); })); }
    function add(cls,html){ const d=el("div","ask-msg "+cls); d.innerHTML=html; msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight; return d; }
    async function run(q){
      if(busy||!q) return; busy=true; go.textContent='Stop'; status.textContent='Thinking…'; sugg.innerHTML='';
      add('ask-q',esc(q)); const a=add('ask-a','<span class="muted">Thinking…</span>'); ctl=new AbortController();
      const opts={signal:ctl.signal, modelTier:'default', onText:({text})=>{ a.textContent=text; msgs.scrollTop=msgs.scrollHeight; }};
      if(caps&&caps.tools) opts.tools=tools.slice(0,caps.tools.maxCount||tools.length); else opts.cache=false;
      try{ const r=await sample(buildInput(q),opts); a.innerHTML=renderAnswer(r.text); history.push({q,a:r.text}); status.textContent=r.truncated?'The answer was cut short by the length limit.':''; const bs=dr.querySelector('.ask-build'); if(bs&&r.modelTierApplied) bs.textContent=BUILD+' \u00b7 answered by the '+r.modelTierApplied+' model tier'; }
      catch(e){ const code=e&&e.code; if(code==='cancelled'){ a.innerHTML=(e.text?renderAnswer(e.text):'')+'<div class="small muted">Stopped.</div>'; if(e.text) history.push({q,a:e.text}); status.textContent=''; }
        else if(code==='not_granted'){ a.innerHTML='<div class="small muted">Asking is not allowed in this view.</div>'; status.textContent=''; fab.hidden=true; }
        else if(code==='rate_limited'){ a.innerHTML='<div class="small muted">Too many questions at once. Wait a moment and ask again.</div>'; status.textContent=''; }
        else if(code==='tools_unavailable'&&caps){ caps={maxPromptBytes:caps.maxPromptBytes}; a.remove(); busy=false; go.textContent='Ask'; return run(q); }
        else { a.innerHTML='<div class="small muted">The question could not be answered ('+esc(code||'error')+'). '+esc((e&&e.message)||'')+'</div>'; status.textContent=''; } }
      busy=false; ctl=null; go.textContent='Ask'; inp.value=''; drawSugg();
    }
    form.addEventListener('submit',e=>{ e.preventDefault(); if(busy){ if(ctl) ctl.abort(); return; } run(inp.value.trim()); });
    inp.addEventListener('keydown',e=>{ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); form.requestSubmit(); } });
    document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&dr.classList.contains('show')) close(); });
  }
  window.__askDebug={factSheet, glossary, prefetch, tools, buildInput, renderAnswer};
  // when the chat cannot mount, say why in one small line at the bottom right (build stamp included, so a
  // viewer can tell whether the share pin already points at a build that has the chat)
  const BUILD='build __ASK_BUILD__';
  function note(msg){ const d=el("div","ask-note"); d.textContent='Ask the data: '+msg+' \u00b7 '+BUILD; document.body.appendChild(d); }
  if(!window.claude || typeof window.claude.use!=='function'){ note('not available outside the claude.ai viewer'); return; }
  window.claude.use('sample').then(async s=>{
    if(!s){ let st='unavailable'; try{ const pm=await window.claude.use('permissions'); if(pm) st=await pm.state('sample'); }catch(e){} note('the viewer did not serve the chat capability (state: '+st+')'); return; }
    sample=s; s.limits().then(c=>{ caps=c; }).catch(()=>{}); mount();
  }).catch(e=>note('could not start ('+((e&&e.message)||e)+')'));
})();
"""

ASK_CSS = """
/* ---- Ask the data (artifact build) ---- */
.ask-fab{position:fixed;right:22px;bottom:22px;z-index:230;display:inline-flex;align-items:center;gap:9px;background:var(--side);color:#fff;border:0;border-radius:var(--pill);height:44px;padding:0 18px;font:inherit;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 10px 30px rgba(20,16,8,.28)}
.ask-fab:hover{transform:translateY(-1px)}
.ask-fab-dot{width:9px;height:9px;border-radius:50%;background:var(--cyan);box-shadow:0 0 0 3px rgba(35,192,226,.25)}
.ask-fab.open{background:var(--cyan);color:#06303b}
.ask-note{position:fixed;right:16px;bottom:12px;z-index:230;font-size:10.5px;color:var(--ink-3);background:var(--card);border:1px solid var(--line);border-radius:var(--pill);padding:4px 10px;max-width:70vw}
.ask-drawer{position:fixed;top:0;right:0;height:100vh;width:min(540px,94vw);background:var(--card);border-left:1px solid var(--line);box-shadow:-14px 0 40px rgba(20,19,16,.16);transform:translateX(102%);transition:transform .26s cubic-bezier(.4,0,.2,1);z-index:225;display:flex;flex-direction:column}
.ask-drawer.show{transform:none}
.ask-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:18px 20px 14px;border-bottom:1px solid var(--line)}
.ask-kicker{font-size:16px;font-weight:800;letter-spacing:-.3px}
.ask-sub{font-size:11.5px;color:var(--ink-2);margin-top:4px;line-height:1.45;max-width:420px}
.ask-build{color:var(--ink-3);white-space:nowrap}
.ask-close{width:32px;height:32px;border-radius:9px;border:1px solid var(--line);background:var(--card);font-size:16px;cursor:pointer;color:var(--ink-2);flex:0 0 auto}
.ask-close:hover{border-color:var(--danger);color:var(--danger)}
.ask-body{flex:1;overflow-y:auto;padding:14px 20px;display:flex;flex-direction:column;gap:10px}
.ask-evk{font-size:9.8px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3);margin-bottom:6px}
.ask-sugg{display:flex;flex-wrap:wrap;gap:6px}
.ask-chip{font:inherit;font-size:12px;font-weight:600;color:var(--ink-2);background:var(--card-2);border:1px solid var(--line);border-radius:var(--pill);padding:6px 12px;cursor:pointer;text-align:left}
.ask-chip:hover{border-color:var(--cyan);color:var(--ink)}
.ask-msgs{display:flex;flex-direction:column;gap:10px}
.ask-msg{border-radius:var(--r-md);padding:11px 14px;font-size:13px;line-height:1.55;max-width:100%}
.ask-q{align-self:flex-end;background:var(--cyan-soft);color:var(--cyan-ink);font-weight:600;max-width:88%}
.ask-a{background:var(--card-2);border:1px solid var(--line);white-space:normal}
.ask-a .md-p{margin:0 0 8px;font-size:13px;line-height:1.6;color:var(--ink)}
.ask-a .md-p:last-child{margin-bottom:0}
.ask-a ul,.ask-a ol{margin:4px 0 8px;padding-left:20px}
.ask-a .ol-builton{margin-top:8px;border-top:1px dashed var(--line);padding-top:8px}
.ask-form{border-top:1px solid var(--line);padding:12px 20px 16px;display:flex;flex-direction:column;gap:8px;background:var(--card)}
.ask-in{width:100%;resize:vertical;min-height:52px;border:1px solid var(--line);border-radius:var(--r-sm);padding:10px 12px;font:inherit;font-size:13px;background:var(--card-2);color:var(--ink)}
.ask-in:focus{outline:none;border-color:var(--cyan);box-shadow:0 0 0 3px var(--cyan-soft)}
.ask-row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.ask-go{font:inherit;font-size:12.5px;font-weight:700;background:var(--side);color:#fff;border:0;border-radius:var(--pill);height:36px;padding:0 18px;cursor:pointer}
.ask-go:hover{background:#23201a}
@media(max-width:640px){.ask-fab{right:12px;bottom:12px}}
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
