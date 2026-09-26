"""Build a self-contained, read-only visual preview with fictional case data.
No API token, live backend or model request is included. This reuses the actual
case graph modules; it is not an alternative production implementation.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from eightball.v2.playbooks import demo_case
from eightball.v2.planner import plan,briefing


def build(output:Path):
    now=datetime(2026,9,23,12,0,tzinfo=timezone.utc)
    case=demo_case(now);result=plan(case,now)
    payload={'case':case.model_dump(mode='json'),'plan':result,'briefing':briefing(case,result)}
    parts=[]
    for filename in ['ui.js','graph-model.js','graph-view.js']:
        text=(ROOT/'web/v2'/filename).read_text()
        text=re.sub(r'^import .*?;\s*$','',text,flags=re.M)
        text=re.sub(r'\bexport\s+','',text)
        parts.append(text)
    state=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    code='\n'.join(parts)+'\nS.current='+state+''';
S.tab='map';
document.getElementById('app').innerHTML=`<main class="preview-main"><div class="preview-brand"><div class="brand"><div class="ball"><span>8</span></div>8BALL</div><span class="engine-signature">POWERED BY ENDSTATE</span><span class="preview-tag">READ-ONLY DESIGN PREVIEW</span></div><div class="preview-heading"><div><span class="kicker">V0.2 / CASE EXPLORER</span><h1>See the whole situation.</h1><p>Explore the design with fictional Northstar data. No backend, model, account or live case is connected.</p></div></div>${graphWorkspace()}<p class="preview-foot">Working interface preview, not a production release. This file contains a fictional snapshot. Layout changes are memory-only and cannot alter evidence.</p></main>`;
mountGraphWorkspace();
document.addEventListener('click',e=>{
  if(e.target.closest('[data-action="close"]')){closeModal();return;}
  const el=e.target.closest('[data-object]');if(!el)return;
  const graph=graphProject(S.current.case,S.current.plan),node=graph.index.get(el.dataset.object+':'+el.dataset.id);
  if(node)modal(node.label,`<p class="note">Read-only fictional record. No editing or attestation in this preview.</p><pre class="code">${esc(JSON.stringify(node.object,null,2))}</pre>`);
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});
'''
    css=(ROOT/'web/v2/style.css').read_text()+'''
.preview-main{max-width:1530px;padding:30px 35px;margin:auto}.preview-brand{display:flex;gap:22px;align-items:center;margin-bottom:42px}.preview-brand .engine-signature{font-size:9px}.preview-tag{margin-left:auto;border:1px solid #3c4453;border-radius:4px;padding:7px 9px;color:#aeb9cc;font-size:8px;letter-spacing:1px}.preview-heading{margin-bottom:25px}.preview-heading h1{margin:9px 0 12px;font-size:38px}.preview-heading p{font-size:12px;color:#939faf}.preview-foot{font-size:10px;line-height:1.7;color:#909aad;margin-top:20px}.preview-main .gx-stage{height:620px}.preview-main .gx-inspector{max-height:660px}@media(max-width:700px){.preview-main{padding:22px 12px}.preview-brand{gap:12px;margin-bottom:30px;flex-wrap:wrap}.preview-tag{margin-left:0}.preview-main .gx-stage{height:420px}.preview-main .gx-inspector{max-height:none}.preview-heading h1{font-size:29px}}
'''
    html='''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>8BALL · Relationship explorer · Read-only preview</title><style>'''+css+'''</style></head><body><div id="app"></div><div id="modal"></div><div id="toast" role="status" aria-live="polite"></div><script type="module">'''+code+'''</script></body></html>'''
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(html,encoding='utf-8')
    print(f'Created read-only preview: {output}')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'artifacts/graph/8BALL-Interactive-Design-Preview.html')
    build(parser.parse_args().output)
