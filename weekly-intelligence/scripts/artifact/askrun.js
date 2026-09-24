// askrun.js — run the dashboard chat's prompt builder and tools from the command line, on the real data.
//   node askrun.js preamble "question"          -> prints the exact input the page would send
//   node askrun.js tool <name> '<json input>'    -> prints the tool's result (or "Error: ...")
//   node askrun.js tools                          -> prints the tool list
// Lives in the repo (the session scratchpad is wiped between days). Reads ASK_JS out of patch_artifact.py
// and the pieces of dashboard-web/app.js the chat relies on, then evaluates them on the real data files.
const fs=require('fs'), path=require('path');
const ROOT=path.resolve(__dirname,'..','..','..');
const app=fs.readFileSync(path.join(ROOT,'dashboard-web/app.js'),'utf8');
const patch=fs.readFileSync(path.join(__dirname,'patch_artifact.py'),'utf8');
const m=patch.match(/ASK_JS = r"""([\s\S]*?)"""\n/); if(!m) throw new Error('ASK_JS not found');
const askjs=m[1].replace('__ASK_BUILD__','cli');
// pieces of app.js the chat relies on
const grab=(re)=>{ const x=app.match(re); if(!x) throw new Error('missing '+re); return x[0]; };
const TABS_SRC=(()=>{ const i=app.indexOf('const TABS = ['); const j=app.indexOf('\n];', i); return app.slice(i, j+3); })();
const ICON_STUB='const ICON=new Proxy({}, {get:()=>""});';
const helpers=[ 'const POT_EUR = {XL:7.5, L:3, M:0.6, S:0.1};', 'function potEur(b){ return POT_EUR[b] || 0; }',
  grab(/function isOpportunity\(s\)\{[\s\S]*?\n(?=function isUnscopedOpp)/) ].join('\n');
const D=JSON.parse(fs.readFileSync(path.join(ROOT,'intel-cache/dashboard-data.json'),'utf8'));
D.budget=JSON.parse(fs.readFileSync(path.join(ROOT,'budget/budget_actions.json'),'utf8'));
D.budget_2027=JSON.parse(fs.readFileSync(path.join(ROOT,'budget/budget_2027.json'),'utf8'));
D.budget_2027_board=JSON.parse(fs.readFileSync(path.join(ROOT,'budget/budget_2027_board.json'),'utf8'));
try{ D.budget_2027_categories=JSON.parse(fs.readFileSync(path.join(ROOT,'budget/budget_2027_categories.json'),'utf8')); }catch(e){}
try{ D.budget_2027_stretch=JSON.parse(fs.readFileSync(path.join(ROOT,'budget/budget_2027_stretch.json'),'utf8')); }catch(e){}
const sigByKey={}; D.signals.forEach(s=>sigByKey[s.key]=s);
const stub={ window:{__DASH_BUDGET_UNLOCKED__:true}, document:{querySelector:()=>null, addEventListener(){}, body:{appendChild(){}}},
  el:(t,c,h)=>({className:c, innerHTML:h||'', appendChild(){}, querySelector:()=>null, querySelectorAll:()=>[], classList:{add(){},remove(){},toggle(){}}, addEventListener(){}, dataset:{}}),
  esc:s=>String(s==null?'':s), mdToHtml:s=>String(s), current:'budget', DASH:D, sigByKey };
const src=ICON_STUB+'\n'+TABS_SRC+'\n'+helpers+'\n'+askjs+'\n;return window.__askDebug;';
const fn=new Function('window','document','el','esc','mdToHtml','current','DASH','sigByKey', src);
const dbg=fn(stub.window, stub.document, stub.el, stub.esc, stub.mdToHtml, stub.current, stub.DASH, stub.sigByKey);
const [cmd,a,b]=process.argv.slice(2);
if(cmd==='preamble'){ process.stdout.write(dbg.buildInput(a||'')); }
else if(cmd==='tools'){ console.log(JSON.stringify(dbg.tools.map(t=>({name:t.name,description:t.description,inputSchema:t.inputSchema||null})),null,1)); }
else if(cmd==='tool'){ const t=dbg.tools.find(x=>x.name===a); if(!t){ console.log('Error: unknown tool '+a); process.exit(0); } let inp={}; try{ inp=b?JSON.parse(b):{}; }catch(e){ console.log('Error: input must be JSON'); process.exit(0); } try{ const r=t.execute(inp,{}); console.log(typeof r==='string'?r:JSON.stringify(r,null,1)); }catch(e){ console.log('Error: '+(e&&e.message||e)); } }
else console.log('usage: node askrun.js preamble "q" | tool <name> <json> | tools');
