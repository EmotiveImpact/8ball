/** Read-only case projection for the relationship explorer.
 * No inference, authority, store writes or external dependencies.
 * IDs are namespaced: an actor and an action may share a domain ID.
 */
export const GRAPH_KINDS = ['objective','actor','condition','action','evidence','claim','event','decision','question','constraint','resource'];
export const GRAPH_LABELS = {objective:'Outcomes',actor:'People',condition:'Conditions',action:'Actions',evidence:'Sources',claim:'Claims',event:'Events',decision:'Decisions',question:'Questions',constraint:'Restrictions',resource:'Resources'};
export const graphKey = (kind,id) => `${kind}:${id}`;
export function graphAtoms(expression) {
  if (!expression) return [];
  return expression.op === 'atom' ? [{id:expression.condition_id,value:expression.value}] : (expression.args??[]).flatMap(graphAtoms);
}
export function graphProject(caseData, planData) {
  const nodes=[], links=[], index=new Map(), missing=[], seenLinks=new Set();
  const addNode=(kind,obj,state,description='')=>{
    const key=graphKey(kind,obj.id);
    if(index.has(key)) throw new Error('Duplicate graph object: '+key);
    const label=obj.name??obj.title??obj.question??obj.statement??obj.id;
    const node={key,id:obj.id,kind,label:String(label),state:state??'recorded',description:String(description),object:obj};
    nodes.push(node);index.set(key,node);
  };
  for(const o of caseData.graph.objectives) addNode('objective',o,planData.objective_states?.[o.id]??'unknown',o.mandatory?'Mandatory outcome':'Optional outcome');
  for(const o of caseData.actors) addNode('actor',o,'reported',o.role||'Role not established');
  for(const o of caseData.graph.conditions) addNode('condition',o,planData.states[o.id]?.status??'unknown',o.confirmation);
  for(const o of caseData.graph.actions) addNode('action',o,planData.action_states[o.id]?.status??'unknown',o.purpose);
  for(const o of caseData.evidence) addNode('evidence',o,o.status,o.source);
  for(const o of caseData.claims) addNode('claim',o,o.status,'Recorded assertion, not an attested condition');
  for(const o of caseData.events) addNode('event',o,o.status,o.time_label);
  const reviewed=new Set(caseData.evidence.filter(e=>e.status==='reviewed').map(e=>e.id));
  for(const o of caseData.decisions) addNode('decision',o,o.selected?((o.evidence_ids??[]).some(id=>!reviewed.has(id))?'needs_review':'recorded'):'pending',o.owner);
  for(const o of caseData.questions) addNode('question',o,o.status==='answered'&&(o.evidence_ids??[]).some(id=>!reviewed.has(id))?'needs_review':o.status,o.why);
  for(const o of caseData.constraints) addNode('constraint',o,o.confirmed?'reviewed':'pending',o.kind);
  for(const o of caseData.resources) addNode('resource',o,'recorded','Capacity-one resource');
  const addLink=(from,to,label,kind='declared',extra={})=>{
    if(!index.has(from)||!index.has(to)){missing.push({from,to,label});return;}
    const sig=JSON.stringify([from,to,label,extra.reference??'']);if(seenLinks.has(sig))return;seenLinks.add(sig);
    links.push({key:`link-${links.length}`,from,to,label,kind,historical:false,...extra});
  };
  for(const r of caseData.relationships) addLink(graphKey('actor',r.from_actor),graphKey('actor',r.to_actor),r.kind.replaceAll('_',' '),'relationship',{reference:r.id});
  for(const o of caseData.graph.conditions) if(o.actor_id) addLink(graphKey('actor',o.actor_id),graphKey('condition',o.id),'associated actor');
  for(const o of caseData.graph.actions){
    const k=graphKey('action',o.id);
    for(const x of graphAtoms(o.requires)) addLink(graphKey('condition',x.id),k,x.value?'prerequisite: true':'prerequisite: false','prerequisite');
    for(const x of graphAtoms(o.guard)) addLink(graphKey('condition',x.id),k,x.value?'guard: true':'guard: false','guard');
    for(const x of o.effects) addLink(k,graphKey('condition',x.condition_id),x.value?'intends true':'intends false','intended');
    for(const id of o.actor_ids??[]) addLink(graphKey('actor',id),k,'involved in');
    for(const id of o.resources??[]) addLink(graphKey('resource',id),k,'required resource');
    if(o.decision_id) addLink(graphKey('decision',o.decision_id),k,'requires option: '+o.decision_option,'decision');
    for(const b of o.contingencies??[]){
      for(const x of graphAtoms(b.when)) addLink(graphKey('condition',x.id),k,'response trigger: '+b.label,'contingency');
      for(const id of b.next_action_ids??[]) addLink(k,graphKey('action',id),'conditional follow-up: '+b.label,'contingency');
    }
  }
  for(const o of caseData.graph.objectives){
    for(const x of graphAtoms(o.success)) addLink(graphKey('condition',x.id),graphKey('objective',o.id),x.value?'success criterion: true':'success criterion: false','objective');
    for(const x of graphAtoms(o.failure)) addLink(graphKey('condition',x.id),graphKey('objective',o.id),x.value?'failure criterion: true':'failure criterion: false','failure');
  }
  const superseded=new Set(caseData.observations.flatMap(o=>o.supersedes??[]));
  const sourceStatus=new Map(caseData.evidence.map(e=>[e.id,e.status]));
  for(const o of caseData.observations){
    const historical=superseded.has(o.id)||sourceStatus.get(o.evidence_id)!=='reviewed';
    addLink(graphKey('evidence',o.evidence_id),graphKey('condition',o.condition_id),o.value?'supports true':'supports false','observation',{
      reference:o.id,historical,reason:superseded.has(o.id)?'Superseded observation':historical?'Source is not currently reviewed':'Active operator attestation'});
  }
  for(const n of nodes){
    for(const p of n.object.provenance?.references??[]) addLink(graphKey('evidence',p.evidence_id),n.key,'source quotation','provenance',{reference:`${p.start}:${p.end}`,historical:sourceStatus.get(p.evidence_id)==='retracted',reason:'Source quotation, not an attestation'});
    for(const id of n.object.evidence_ids??[]) addLink(graphKey('evidence',id),n.key,'evidence considered','provenance',{historical:sourceStatus.get(id)==='retracted'});
    if(n.kind==='event') for(const id of n.object.actor_ids??[]) addLink(graphKey('actor',id),n.key,'reported involvement');
    if(n.kind==='claim'){
      if(n.object.speaker_id)addLink(graphKey('actor',n.object.speaker_id),n.key,'attributed speaker');
      if(n.object.condition_id)addLink(n.key,graphKey('condition',n.object.condition_id),'claim about condition','claim');
    }
    if(n.kind==='question') for(const id of n.object.condition_ids??[]) addLink(n.key,graphKey('condition',id),'question concerns');
    if(n.kind==='constraint'){
      for(const x of graphAtoms(n.object.predicate)) addLink(graphKey('condition',x.id),n.key,'required restriction predicate','guard');
      const ids=n.object.action_ids?.length?n.object.action_ids:caseData.graph.actions.map(a=>a.id);
      for(const id of ids) addLink(n.key,graphKey('action',id),n.object.hard?'hard restriction':'soft preference','guard');
    }
  }
  return {nodes,links,index,missing,caseId:caseData.id,revision:caseData.revision};
}
export function graphVisible(graph, {kinds=GRAPH_KINDS,query='',scope='all',selected=null,depth=1,history=false}={}){
  const allowed=new Set(kinds),q=query.trim().toLocaleLowerCase();
  let nodes=graph.nodes.filter(n=>allowed.has(n.kind));
  let keys=new Set(nodes.map(n=>n.key));
  let links=graph.links.filter(l=>keys.has(l.from)&&keys.has(l.to)&&(history||!l.historical));
  if(scope==='local'){
    const neighbourhood=new Set(keys.has(selected)?[selected]:[]),frontier=new Set(neighbourhood);
    for(let d=0;d<Math.min(3,Math.max(1,depth));d++){
      const next=new Set();for(const l of links){if(frontier.has(l.from)&&!neighbourhood.has(l.to))next.add(l.to);if(frontier.has(l.to)&&!neighbourhood.has(l.from))next.add(l.from);}
      for(const k of next)neighbourhood.add(k);frontier.clear();for(const k of next)frontier.add(k);
    }
    nodes=nodes.filter(n=>neighbourhood.has(n.key));
  }
  if(q)nodes=nodes.filter(n=>`${n.label} ${n.kind} ${n.description}`.toLocaleLowerCase().includes(q));
  keys=new Set(nodes.map(n=>n.key));links=links.filter(l=>keys.has(l.from)&&keys.has(l.to));
  return {nodes,links};
}
export function graphNeighbourKeys(graph,key){
  const neighbours=new Set();for(const l of graph.links){if(l.from===key)neighbours.add(l.to);if(l.to===key)neighbours.add(l.from);}return neighbours;
}
/** Bounded, deterministic layout. Coordinates carry no authority or causal meaning.
 * No perpetual animation: stable positions make pointer and keyboard use predictable.
 * Large sets use a non-quadratic grid fallback with an explicit UI notice.
 */
export function graphLayout(graph,mode='network',pinned={}){
  const order=[...graph.nodes].sort((a,b)=>a.key.localeCompare(b.key)),w=1200,h=740,positions={};
  if(order.length>120){
    const cols=Math.max(4,Math.ceil(Math.sqrt(order.length*1.6))),rows=Math.ceil(order.length/cols);
    const outWidth=Math.max(w,cols*205+140),outHeight=Math.max(h,rows*100+100);
    order.forEach((n,i)=>positions[n.key]={x:100+(i%cols)*205,y:60+Math.floor(i/cols)*100});
    for(const n of order){const p=pinned[n.key];if(p&&Number.isFinite(p.x)&&Number.isFinite(p.y))positions[n.key]={x:Math.max(30,Math.min(outWidth-30,p.x)),y:Math.max(30,Math.min(outHeight-35,p.y))};}
    return {positions,width:outWidth,height:outHeight,fallback:true};
  }
  // The directed view preserves cycles as same-level clusters instead of recursing indefinitely.
  if(mode==='outcome'){
    const index=new Map(order.map((n,i)=>[n.key,i])),adj=order.map(()=>[]);
    const semantic=graph.links.filter(l=>['prerequisite','intended','objective','guard','failure'].includes(l.kind));
    for(const l of semantic)adj[index.get(l.from)].push(index.get(l.to));
    let serial=0;const stack=[],onStack=new Set(),number=new Map(),low=new Map(),components=[];
    function visit(v){number.set(v,serial);low.set(v,serial++);stack.push(v);onStack.add(v);
      for(const n of adj[v]){if(!number.has(n)){visit(n);low.set(v,Math.min(low.get(v),low.get(n)));}else if(onStack.has(n))low.set(v,Math.min(low.get(v),number.get(n)));}
      if(low.get(v)===number.get(v)){const group=[];let n;do{n=stack.pop();onStack.delete(n);group.push(n);}while(n!==v);components.push(group);}}
    order.forEach((_,i)=>{if(!number.has(i))visit(i);});
    const component=new Map();components.forEach((c,i)=>c.forEach(n=>component.set(n,i)));
    const levels=new Map();function level(i){if(levels.has(i))return levels.get(i);let v=0;for(const l of semantic){const a=component.get(index.get(l.from)),b=component.get(index.get(l.to));if(b===i&&a!==i)v=Math.max(v,level(a)+1);}levels.set(i,v);return v;}
    components.forEach((_,i)=>level(i));const columns=new Map();
    order.forEach((n,i)=>{const x=level(component.get(i));if(!columns.has(x))columns.set(x,[]);columns.get(x).push(n);});
    const max=Math.max(1,...columns.keys()),outWidth=Math.max(w,max*235+240),maxRows=Math.max(1,...[...columns.values()].map(c=>c.length)),outHeight=Math.max(h,maxRows*105+110);
    for(const [column,values] of columns)values.forEach((n,row)=>positions[n.key]={x:90+column*(outWidth-180)/max,y:(outHeight-(values.length-1)*105)/2+row*105});
    return {positions,width:outWidth,height:outHeight,fallback:false};
  }
  // Deterministic phyllotaxis seed followed by a fixed number of spring/repulsion steps.
  order.forEach((n,i)=>{const angle=i*2.399963229728653,r=Math.sqrt((i+1)/Math.max(1,order.length));positions[n.key]={x:w/2+Math.cos(angle)*r*460,y:h/2+Math.sin(angle)*r*265};});
  const validPin=k=>pinned[k]&&Number.isFinite(pinned[k].x)&&Number.isFinite(pinned[k].y);
  for(let tick=0;tick<190;tick++){
    const forces=new Map(order.map(n=>[n.key,{x:0,y:0}]));
    for(let i=0;i<order.length;i++)for(let j=i+1;j<order.length;j++){
      const a=positions[order[i].key],b=positions[order[j].key],dx=a.x-b.x,dy=a.y-b.y,dist=Math.max(1,Math.hypot(dx,dy));
      const f=Math.min(9,8500/(dist*dist))+(dist<135?(135-dist)*.07:0),fx=dx/dist*f,fy=dy/dist*f;
      forces.get(order[i].key).x+=fx;forces.get(order[i].key).y+=fy;forces.get(order[j].key).x-=fx;forces.get(order[j].key).y-=fy;
    }
    for(const l of graph.links){const a=positions[l.from],b=positions[l.to];if(!a||!b)continue;const dx=b.x-a.x,dy=b.y-a.y,dist=Math.max(1,Math.hypot(dx,dy)),f=(dist-220)*.008;forces.get(l.from).x+=dx/dist*f;forces.get(l.from).y+=dy/dist*f;forces.get(l.to).x-=dx/dist*f;forces.get(l.to).y-=dy/dist*f;}
    for(const n of order){const p=positions[n.key];if(validPin(n.key)){p.x=Math.max(70,Math.min(w-70,pinned[n.key].x));p.y=Math.max(50,Math.min(h-65,pinned[n.key].y));continue;}const f=forces.get(n.key);p.x=Math.max(70,Math.min(w-70,p.x+f.x+(w/2-p.x)*.0008));p.y=Math.max(50,Math.min(h-65,p.y+f.y+(h/2-p.y)*.001));}
  }
  // Resolve label rectangles as well as node circles. This is visual layout only.
  for(let pass=0;pass<180;pass++){
    let overlaps=0;
    for(let i=0;i<order.length;i++)for(let j=i+1;j<order.length;j++){
      const na=order[i],nb=order[j],a=positions[na.key],b=positions[nb.key];
      const aw=Math.min(190,Math.max(85,Math.min(25,na.label.length)*7.2+16)),bw=Math.min(190,Math.max(85,Math.min(25,nb.label.length)*7.2+16));
      const dx=b.x-a.x,dy=b.y-a.y,ox=(aw+bw)/2+12-Math.abs(dx),oy=99-Math.abs(dy);
      if(ox<=0||oy<=0)continue;overlaps++;
      const pa=validPin(na.key),pb=validPin(nb.key);if(pa&&pb)continue;
      const factor=pa||pb?1:.5,axis=ox/190<oy/99?'x':'y',push=(axis==='x'?ox:oy)*.55*factor;
      const direction=(axis==='x'?dx:dy)>=0?1:-1;
      if(!pa)a[axis]-=push*direction;if(!pb)b[axis]+=push*direction;
    }
    for(const n of order){const p=positions[n.key];p.x=Math.max(105,Math.min(w-105,p.x));p.y=Math.max(80,Math.min(h-90,p.y));}
    if(!overlaps)break;
  }
  return {positions,width:w,height:h,fallback:false};
}
