import {S,esc,pretty,badge,button,icon,date,expr} from './ui.js';
import {GRAPH_KINDS,GRAPH_LABELS,graphProject,graphVisible,graphLayout,graphNeighbourKeys} from './graph-model.js';

// View preferences are case-local and memory-only. They never enter the case ledger.
const graphViews=new Map();
let graphDispose=()=>{};
export function clearGraphViews(){graphDispose();graphViews.clear();}
function graphPreferences(caseData){
  if(!graphViews.has(caseData.id))graphViews.set(caseData.id,{mode:'network',kinds:[...GRAPH_KINDS],query:'',scope:'all',depth:1,history:false,selected:null,pinned:{},camera:null,revision:caseData.revision});
  const v=graphViews.get(caseData.id);
  if(v.revision!==caseData.revision){v.camera=null;v.revision=caseData.revision;}
  return v;
}
export function graphWorkspace(){return `<section class="constellation" aria-label="Situation relationship explorer">
  <div class="gx-top"><div class="gx-mode" role="group" aria-label="Map layout"><button type="button" data-gx-mode="network">${icon('map')}Connections</button><button type="button" data-gx-mode="outcome">${icon('routes')}Outcome flow</button><button type="button" data-gx-mode="list">${icon('evidence')}Records</button></div><span class="gx-revision">CASE SNAPSHOT <b>REV ${S.current.case.revision}</b></span></div>
  <div class="gx-filters"><label class="gx-search">${icon('search')}<span class="sr-only">Search graph records</span><input type="search" data-gx-search placeholder="Find a person, condition or source…" maxlength="300" autocomplete="off"></label><label class="gx-scope"><span class="sr-only">Graph scope</span><select data-gx-scope><option value="all">Whole case</option><option value="local">Selected neighbourhood</option></select></label><label class="gx-depth"><span>Depth</span><select data-gx-depth aria-label="Neighbourhood depth"><option value="1">1 link</option><option value="2">2 links</option><option value="3">3 links</option></select></label><label class="gx-history"><input type="checkbox" data-gx-history>Historical links</label></div>
  <div class="gx-types" role="group" aria-label="Visible record types"></div>
  <div class="gx-body"><div class="gx-workarea"><div class="gx-stage" role="region" aria-label="Interactive case graph"><div class="gx-canvas"></div><div class="gx-overlay"><span class="gx-layout-label">RELATIONSHIP VIEW</span><span>Recorded connections, not inferred causation.</span></div><div class="gx-viewport-controls" role="group" aria-label="Graph navigation"><button type="button" data-gx-zoom="in" aria-label="Zoom in">+</button><button type="button" data-gx-zoom="out" aria-label="Zoom out">−</button><span class="gx-zoom-label"></span><button type="button" data-gx-fit>Fit</button><button type="button" data-gx-reset>Reset layout</button></div></div><div class="gx-foot"><span class="gx-count" role="status" aria-live="polite"></span><span>Drag to pan · drag a node to pin · + / − to zoom</span></div></div><aside class="gx-inspector" aria-label="Selected record inspector"></aside></div>
  <div class="gx-integrity">${icon('lock')}VIEW ONLY <span>Layout and filters do not change evidence, prerequisites, approvals or the audit trail.</span></div>
</section>`;}
function gxLabelLines(value,max=25){
  const words=value.split(/\s+/),lines=[''];for(const w of words){if((lines.at(-1)+' '+w).trim().length>max&&lines.at(-1))lines.push(w);else lines[lines.length-1]+=(lines.at(-1)?' ':'')+w;}
  if(lines.length>2)return [lines[0],lines[1].slice(0,max-1)+'…'];return lines;
}
function gxSvgMarkup(graph,layout,prefs){
  const {positions:p,width,height}=layout;
  const keyOrder=graph.nodes.map(n=>n.key),edgeId=new Map(keyOrder.map((k,i)=>[k,i]));
  const links=graph.links.map(l=>{const a=p[l.from],b=p[l.to],dx=b.x-a.x,dy=b.y-a.y,len=Math.max(1,Math.hypot(dx,dy));const bx=b.x-dx/len*14,by=b.y-dy/len*14;
    return `<line x1="${a.x}" y1="${a.y}" x2="${bx}" y2="${by}" class="gx-link ${l.historical?'historical':''} ${esc(l.kind)}" data-gx-edge="${esc(l.key)}" data-from="${edgeId.get(l.from)}" data-to="${edgeId.get(l.to)}" ${prefs.mode==='outcome'?'marker-end="url(#gx-arrow)"':''}><title>${esc(l.label)}${l.historical?' (historical, not active support)':''}</title></line>`;}).join('');
  const nodes=graph.nodes.map((n,i)=>{const pos=p[n.key],pin=Boolean(prefs.pinned[n.key]);return `<g class="gx-node ${esc(n.kind)} ${esc(n.state)} ${pin?'pinned':''}" transform="translate(${pos.x} ${pos.y})" tabindex="0" role="button" aria-pressed="${prefs.selected===n.key}" aria-label="${esc(pretty(n.kind)+': '+n.label+'. '+pretty(n.state))}" data-gx-key="${esc(n.key)}" data-gx-number="${i}"><title>${esc(n.label)}</title><circle class="gx-hit" r="26"/><circle class="gx-node-halo" r="20"/>${n.kind==='objective'?'<path class="gx-node-core" d="M0 -14 14 0 0 14 -14 0Z"/>':n.kind==='action'?'<rect class="gx-node-core" x="-8" y="-8" width="16" height="16" rx="4"/>':'<circle class="gx-node-core" r="'+(n.kind==='actor'?9:6)+'"/>'}<circle class="gx-pin-marker" cx="15" cy="-15" r="3"/>${gxLabelLines(n.label).map((line,j)=>`<text class="gx-node-label" x="0" y="${31+j*17}" text-anchor="middle">${esc(line)}</text>`).join('')}</g>`;}).join('');
  return `<svg class="gx-svg ${prefs.mode==='outcome'?'outcome-flow':''}" viewBox="0 0 ${width} ${height}" data-base-width="${width}" data-base-height="${height}" role="group" aria-label="${prefs.mode==='outcome'?'Directed outcome flow':'Connected case records'}" tabindex="0"><defs><marker id="gx-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 1 7 4 0 7" fill="none" stroke="currentColor"/></marker></defs><g class="gx-edges">${links}</g><g class="gx-nodes">${nodes}</g></svg>`;
}
function gxRecordDetails(node,caseData,planData){
  const o=node.object,rows=[];const row=(k,v)=>{if(v!==null&&v!==undefined&&String(v)!=='')rows.push(`<div class="gx-detail"><small>${esc(k)}</small><p>${esc(String(v))}</p></div>`);};
  if(node.kind==='actor'){row('Reported role',o.role||'Not established');row('Authority',o.authority||'Not established');row('Reported position',o.stance||'Not established');}
  if(node.kind==='condition'){row('What would establish this?',o.confirmation);row('Deadline',date(o.due_at));row('Observation IDs',planData.states[node.id]?.observations?.join(', ')||'No active supporting observation');}
  if(node.kind==='action'){row('Owner',o.owner);row('Purpose',o.purpose);row('Prerequisites (exact logic)',expr(o.requires));row('Guard (exact logic)',expr(o.guard));row('Readiness',planData.action_states[node.id]?.reasons?.join('. ')||pretty(planData.action_states[node.id]?.status??'unknown'));row('Effects','Intended only. Completing this action does not attest these results.');}
  if(node.kind==='objective'){row('Success criteria (exact logic)',expr(o.success));row('Failure criteria',o.failure?expr(o.failure):'None declared');row('Priority',o.mandatory?'Mandatory':'Optional');}
  if(node.kind==='evidence'){row('Provenance',o.source);row('Source text',o.text);row('Added',date(o.added_at));}
  if(node.kind==='claim')row('Assertion',o.statement);
  if(node.kind==='event'){row('Reported description',o.description);row('Event time',o.occurred_at?date(o.occurred_at):o.time_label);}
  if(node.kind==='decision'){row('Decision owner',o.owner);row('Selected option',o.options.find(x=>x.id===o.selected)?.title||'Not decided');row('Rationale',o.rationale);}
  if(node.kind==='question'){row('Why it matters',o.why);row('Owner',o.owner);row('Recorded answer',o.answer||'Unanswered');}
  if(node.kind==='constraint'){row('Restriction',o.hard?'Hard':'Soft preference');row('Exact predicate',o.predicate?expr(o.predicate):'Operator-declared restriction, not machine-verified compliance');}
  if(node.kind==='resource'){row('Capacity','One concurrent action');row('Available from',date(o.available_from));row('Available until',date(o.available_until));}
  if(node.state==='needs_review')row('Review required','An evidence source for this recorded answer or decision is no longer reviewed. Its history is retained, not treated as current support.');
  return rows.join('');
}
function gxInspector(graph,visible,prefs,caseData,planData){
  const n=graph.index.get(prefs.selected);
  if(!n){const established=caseData.graph.conditions.filter(c=>planData.states[c.id]?.status==='true').length;
    return `<div class="gx-inspector-top"><span class="kicker">CASE INTELLIGENCE</span>${icon('room')}</div><div class="gx-inspector-content"><div class="gx-intro-mark">8</div><h2>A clearer picture.<br>A better next move.</h2><p class="gx-description">Follow a person, a claim or a condition through the case. Select a record to inspect what it is connected to.</p><div class="gx-target-note"><span class="kicker">DESIRED OUTCOME</span><p>${esc(caseData.desired_outcome)}</p></div><div class="gx-summary"><div><strong>${caseData.actors.length}</strong><small>People & organisations</small></div><div><strong>${established}/${caseData.graph.conditions.length}</strong><small>Conditions supported true</small></div></div><div class="gx-tip"><b>Explore without changing the case.</b><span>Focus on a neighbourhood, inspect the original source, then return to the structured plan.</span></div></div>`;
  }
  const links=graph.links.filter(l=>(l.from===n.key||l.to===n.key)&&(prefs.history||!l.historical)),inView=visible.nodes.some(v=>v.key===n.key);
  const linkList=links.map(l=>{const other=graph.index.get(l.from===n.key?l.to:l.from);return `<button class="gx-connected-record" type="button" data-gx-select="${esc(other.key)}"><span>${esc(other.label)}</span><small>${l.from===n.key?'→':'←'} ${esc(l.label)}${l.historical?' · historical':''}</small></button>`;}).join('');
  const sources=(n.object.provenance?.references??[]).map(s=>`<blockquote class="gx-quote">${esc(s.quote)}<button type="button" data-gx-select="${esc('evidence:'+s.evidence_id)}">Source · characters ${s.start} to ${s.end} ↗</button></blockquote>`).join('');
  return `<div class="gx-inspector-top"><span class="kicker">${esc(n.kind.toUpperCase())} / RECORD</span><button type="button" class="icon-button" data-gx-clear aria-label="Clear graph selection">${icon('close')}</button></div><div class="gx-inspector-content"><h2 tabindex="-1">${esc(n.label)}</h2><div class="gx-statusline">${badge(n.state)}<small>${links.length} link${links.length===1?'':'s'}</small></div>${!inView?'<p class="gx-hidden-note">This record is hidden by your current filters.</p>':''}<div class="gx-inspector-actions"><button type="button" data-gx-focus>${icon('search')}Focus neighbourhood</button><button type="button" data-gx-pin ${prefs.mode!=='network'||!inView?'disabled':''}>${prefs.pinned[n.key]?'Unpin position':'Pin position'}</button></div>${['condition','action','evidence','actor'].includes(n.kind)?`<button type="button" class="gx-open-record" data-object="${esc(n.kind)}" data-id="${esc(n.id)}">Open full record ${icon('arrow')}</button>`:''}${gxRecordDetails(n,caseData,planData)}${sources}<h3 class="gx-links-title">Recorded connections</h3>${linkList||'<p class="note">No visible relationship records.</p>'}<p class="gx-disclaimer">${n.object.provenance?'Origin: '+esc(pretty(n.object.provenance.origin))+'. ':''}Proximity on the canvas is not evidence of influence, authority or cause.</p></div>`;
}
export function mountGraphWorkspace(){
  graphDispose();graphDispose=()=>{};const root=document.querySelector('.constellation');if(!root||!S.current)return;
  const caseData=S.current.case,planData=S.current.plan,graph=graphProject(caseData,planData),prefs=graphPreferences(caseData);
  if(prefs.selected&&!graph.index.has(prefs.selected))prefs.selected=null;
  for(const key of Object.keys(prefs.pinned))if(!graph.index.has(key))delete prefs.pinned[key];
  const abort=new AbortController(),on=(el,type,handler,opts={})=>el.addEventListener(type,handler,{...opts,signal:abort.signal});
  let shown,layout,hovered=null,pointer=null,dragMoved=false;
  const camera=()=>{
    if(prefs.camera)return prefs.camera;
    if((prefs.mode==='outcome'||layout.fallback)&&layout.width>1400){const point=layout.positions[prefs.selected],w=1400,h=Math.max(740,layout.height);return {x:Math.max(0,Math.min(layout.width-w,(point?.x??w/2)-w/2)),y:0,w,h};}
    return {x:0,y:0,w:layout.width,h:layout.height};
  };
  function setCamera(v){prefs.camera=v;root.querySelector('.gx-svg')?.setAttribute('viewBox',`${v.x} ${v.y} ${v.w} ${v.h}`);root.querySelector('.gx-zoom-label').textContent=Math.round(layout.width/v.w*100)+'%';}
  function zoom(factor){if(!layout)return;const v=camera(),newW=Math.min(layout.width*3,Math.max(layout.width/4,v.w*factor)),r=newW/v.w;setCamera({x:v.x+(v.w-newW)/2,y:v.y+(v.h-v.h*r)/2,w:newW,h:v.h*r});}
  function selectRecord(key,{focus=false}={}){
    if(!graph.index.has(key))return;prefs.selected=key;if(prefs.mode==='outcome')prefs.camera=null;if(focus){prefs.scope='local';prefs.query='';prefs.kinds=[...GRAPH_KINDS];}
    repaint();
  }
  function emphasise(){
    const focus=hovered??prefs.selected,neighbours=graphNeighbourKeys(shown,focus);
    for(const el of root.querySelectorAll('.gx-node')){const key=el.dataset.gxKey;el.classList.toggle('selected',key===prefs.selected);el.classList.toggle('near',key===focus||neighbours.has(key));el.classList.toggle('dim',Boolean(focus)&&key!==focus&&!neighbours.has(key));el.setAttribute('aria-pressed',String(key===prefs.selected));}
    for(const el of root.querySelectorAll('.gx-link')){const l=shown.links.find(x=>x.key===el.dataset.gxEdge);el.classList.toggle('highlighted',Boolean(focus)&&(l.from===focus||l.to===focus));el.classList.toggle('dim',Boolean(focus)&&l.from!==focus&&l.to!==focus);}
  }
  function repaint({keepSearchFocus=false}={}){
    const oldFocus=document.activeElement;
    const focusKey=oldFocus?.dataset?.gxKey,focusSelect=oldFocus?.dataset?.gxSelect,oldPosition=oldFocus?.selectionStart;
    shown=graphVisible(graph,prefs);
    // Flow deliberately excludes descriptive links from placement; exact expressions remain in the inspector.
    if(prefs.mode==='outcome')shown={nodes:shown.nodes.filter(n=>['condition','action','objective'].includes(n.kind)),links:shown.links.filter(l=>['prerequisite','intended','objective','failure','guard'].includes(l.kind))};
    const keys=new Set(shown.nodes.map(n=>n.key));shown.links=shown.links.filter(l=>keys.has(l.from)&&keys.has(l.to));
    const positions=prefs.scope==='local'&&prefs.selected&&!prefs.pinned[prefs.selected]?{...prefs.pinned,[prefs.selected]:{x:600,y:370}}:prefs.pinned;
    layout=graphLayout(shown,prefs.mode,positions);
    root.querySelectorAll('[data-gx-mode]').forEach(el=>{const active=el.dataset.gxMode===prefs.mode;el.classList.toggle('active',active);el.setAttribute('aria-pressed',String(active));});
    const search=root.querySelector('[data-gx-search]');if(search.value!==prefs.query)search.value=prefs.query;
    root.querySelector('[data-gx-scope]').value=prefs.scope;root.querySelector('[data-gx-depth]').value=String(prefs.depth);root.querySelector('[data-gx-depth]').disabled=prefs.scope!=='local';root.querySelector('[data-gx-history]').checked=prefs.history;
    root.querySelector('.gx-types').innerHTML=GRAPH_KINDS.filter(k=>graph.nodes.some(n=>n.kind===k)).map(kind=>`<button type="button" class="gx-type-chip ${prefs.kinds.includes(kind)?'on':''}" data-gx-kind="${kind}" aria-pressed="${prefs.kinds.includes(kind)}"><i class="gx-kind-dot ${kind}"></i>${GRAPH_LABELS[kind]}<span>${graph.nodes.filter(n=>n.kind===kind).length}</span></button>`).join('')+'<button type="button" class="gx-clear-filters" data-gx-all>Reset filters</button>';
    const canvas=root.querySelector('.gx-canvas');
    canvas.innerHTML=!shown.nodes.length?`<div class="gx-no-results"><h3>${graph.nodes.length?'No records match this view.':'The case picture starts here.'}</h3><p>${graph.nodes.length?'Reset the filters or select a different neighbourhood.':'Add evidence, people and an outcome structure. No connections are invented from an empty case.'}</p><button type="button" data-gx-all>Reset filters</button></div>`:prefs.mode==='list'?`<div class="gx-record-list"><div class="gx-list-header"><span>Record</span><span>Type</span><span>Recorded state</span></div>${shown.nodes.map(n=>`<button type="button" data-gx-select="${esc(n.key)}" class="${prefs.selected===n.key?'selected':''}"><span>${esc(n.label)}</span><small>${esc(pretty(n.kind))}</small><small>${esc(pretty(n.state))}</small></button>`).join('')}</div>`:gxSvgMarkup(shown,layout,prefs);
    root.querySelector('.gx-overlay').hidden=prefs.mode==='list'||!shown.nodes.length;
    root.querySelector('.gx-viewport-controls').hidden=prefs.mode==='list'||!shown.nodes.length;
    root.querySelector('.gx-layout-label').textContent=prefs.mode==='outcome'?'DIRECTED DEPENDENCIES':'RELATIONSHIP VIEW';
    root.querySelector('.gx-overlay>span:last-child').textContent=prefs.mode==='outcome'?'Select a record for exact AND / OR logic. Pan to explore.':'Recorded connections, not inferred causation.';
    root.querySelector('.gx-count').textContent=`${shown.nodes.length} of ${graph.nodes.length} records · ${shown.links.length} links${layout.fallback?' · large-case grid layout':''}${graph.missing.length?' · '+graph.missing.length+' unresolved references not displayed':''}`;
    root.querySelector('.gx-inspector').innerHTML=gxInspector(graph,shown,prefs,caseData,planData);
    if(prefs.mode!=='list')setCamera(camera());emphasise();
    if(keepSearchFocus){search.focus();try{search.setSelectionRange(oldPosition,oldPosition);}catch{}}
    else if(focusKey)root.querySelector(`[data-gx-key="${CSS.escape(focusKey)}"]`)?.focus({preventScroll:true});
    else if(focusSelect)root.querySelector(`[data-gx-select="${CSS.escape(focusSelect)}"]`)?.focus({preventScroll:true});
  }
  on(root,'click',e=>{
    const el=e.target.closest('[data-gx-key],[data-gx-select],[data-gx-mode],[data-gx-kind],[data-gx-fit],[data-gx-reset],[data-gx-zoom],[data-gx-clear],[data-gx-focus],[data-gx-pin],[data-gx-all]');if(!el)return;
    if(dragMoved){dragMoved=false;return;}
    if(el.dataset.gxKey){selectRecord(el.dataset.gxKey);return;}
    if(el.dataset.gxSelect){selectRecord(el.dataset.gxSelect);return;}
    if(el.dataset.gxMode){prefs.mode=el.dataset.gxMode;prefs.camera=null;repaint();return;}
    if(el.dataset.gxKind){prefs.kinds=prefs.kinds.includes(el.dataset.gxKind)?prefs.kinds.filter(k=>k!==el.dataset.gxKind):[...prefs.kinds,el.dataset.gxKind];prefs.camera=null;repaint();root.querySelector(`[data-gx-kind="${el.dataset.gxKind}"]`)?.focus();return;}
    if(el.hasAttribute('data-gx-clear')){prefs.selected=null;prefs.scope='all';repaint();return;}
    if(el.hasAttribute('data-gx-focus')){selectRecord(prefs.selected,{focus:true});return;}
    if(el.hasAttribute('data-gx-pin')){if(prefs.pinned[prefs.selected])delete prefs.pinned[prefs.selected];else prefs.pinned[prefs.selected]={...layout.positions[prefs.selected]};repaint();root.querySelector('[data-gx-pin]')?.focus();return;}
    if(el.hasAttribute('data-gx-all')){prefs.kinds=[...GRAPH_KINDS];prefs.query='';prefs.scope='all';prefs.history=false;prefs.camera=null;repaint();return;}
    if(el.hasAttribute('data-gx-fit')){setCamera({x:0,y:0,w:layout.width,h:layout.height});return;}
    if(el.hasAttribute('data-gx-reset')){prefs.pinned={};prefs.camera=null;repaint();return;}
    if(el.dataset.gxZoom)zoom(el.dataset.gxZoom==='in'?.8:1.25);
  });
  on(root,'input',e=>{if(e.target.matches('[data-gx-search]')){prefs.query=e.target.value;prefs.camera=null;repaint({keepSearchFocus:true});}});
  on(root,'change',e=>{if(e.target.matches('[data-gx-scope]')){prefs.scope=e.target.value;if(prefs.scope==='local'&&!prefs.selected)prefs.selected=graph.nodes.find(n=>n.kind==='objective')?.key??graph.nodes[0]?.key??null;}else if(e.target.matches('[data-gx-depth]'))prefs.depth=Number(e.target.value);else if(e.target.matches('[data-gx-history]'))prefs.history=e.target.checked;else return;prefs.camera=null;repaint();});
  on(root,'pointerover',e=>{const n=e.target.closest('[data-gx-key]');if(n){hovered=n.dataset.gxKey;emphasise();}});
  on(root,'pointerout',e=>{if(e.target.closest('[data-gx-key]')){hovered=null;emphasise();}});
  const clientPoint=(svg,x,y)=>{const matrix=svg.getScreenCTM();if(!matrix)return null;return new DOMPoint(x,y).matrixTransform(matrix.inverse());};
  on(root,'pointerdown',e=>{
    const svg=e.target.closest('.gx-svg');if(!svg||e.button!==0)return;const n=e.target.closest('[data-gx-key]');const p=clientPoint(svg,e.clientX,e.clientY);if(!p)return;
    pointer={id:e.pointerId,svg,hitKey:n?.dataset.gxKey,key:prefs.mode==='network'?n?.dataset.gxKey:null,start:p,clientX:e.clientX,clientY:e.clientY,camera:{...camera()}};dragMoved=false;svg.setPointerCapture(e.pointerId);
  });
  on(root,'pointermove',e=>{
    if(!pointer||pointer.id!==e.pointerId)return;const dx=e.clientX-pointer.clientX,dy=e.clientY-pointer.clientY;if(Math.hypot(dx,dy)<5&&!dragMoved)return;dragMoved=true;
    if(pointer.key){const p=clientPoint(pointer.svg,e.clientX,e.clientY);if(!p)return;const pos={x:Math.max(30,Math.min(layout.width-30,p.x)),y:Math.max(30,Math.min(layout.height-35,p.y))};prefs.pinned[pointer.key]=pos;layout.positions[pointer.key]=pos;
      pointer.svg.querySelector(`[data-gx-key="${CSS.escape(pointer.key)}"]`)?.setAttribute('transform',`translate(${pos.x} ${pos.y})`);
      for(const l of shown.links){const el=pointer.svg.querySelector(`[data-gx-edge="${l.key}"]`);if(l.from===pointer.key){el?.setAttribute('x1',String(pos.x));el?.setAttribute('y1',String(pos.y));}if(l.to===pointer.key){el?.setAttribute('x2',String(pos.x));el?.setAttribute('y2',String(pos.y));}}
    }else{const rect=pointer.svg.getBoundingClientRect(),scale=Math.min(rect.width/pointer.camera.w,rect.height/pointer.camera.h);setCamera({...pointer.camera,x:pointer.camera.x-dx/scale,y:pointer.camera.y-dy/scale});}
  });
  const stopPointer=e=>{if(!pointer||pointer.id!==e.pointerId)return;const moved=dragMoved,key=pointer.key,hitKey=pointer.hitKey;try{pointer.svg.releasePointerCapture(e.pointerId);}catch{}pointer=null;if(moved&&key){prefs.selected=key;repaint();}if(!moved&&hitKey){selectRecord(hitKey);}setTimeout(()=>{dragMoved=false;},0);};
  on(root,'pointerup',stopPointer);on(root,'pointercancel',stopPointer);
  // Wheel zoom is modified so scrolling the page never gets trapped in the canvas.
  on(root,'wheel',e=>{if(e.target.closest('.gx-svg')&&(e.ctrlKey||e.metaKey)){e.preventDefault();zoom(e.deltaY>0?1.1:.9);}},{passive:false});
  on(root,'keydown',e=>{
    const node=e.target.closest('[data-gx-key]'),svg=e.target.closest('.gx-svg');if(!svg)return;
    if(node&&['Enter',' '].includes(e.key)){e.preventDefault();selectRecord(node.dataset.gxKey);return;}
    if(e.key==='Escape'){prefs.selected=null;prefs.scope='all';repaint();return;}
    if(['+','=','-','_'].includes(e.key)){e.preventDefault();zoom(['+','='].includes(e.key)?.8:1.25);return;}
    if(e.key==='Home'){e.preventDefault();prefs.camera=null;setCamera(camera());return;}
    if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();const v=camera(),step=v.w*(e.shiftKey?.12:.04);setCamera({...v,x:v.x+(e.key==='ArrowLeft'?-step:e.key==='ArrowRight'?step:0),y:v.y+(e.key==='ArrowUp'?-step:e.key==='ArrowDown'?step:0)});}
  });
  repaint();graphDispose=()=>abort.abort();
}
