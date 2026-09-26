// Pure draft editing. Never sends commands, attests evidence or stores case data.
export const studioClone = value => JSON.parse(JSON.stringify(value));
export const studioEqual = (a,b) => JSON.stringify(a) === JSON.stringify(b);
export function createStudioDraft(caseData) {
  return {caseId:caseData.id,baseRevision:caseData.revision,baseCase:studioClone(caseData),
    graph:studioClone(caseData.graph),original:studioClone(caseData.graph),selection:null,
    undo:[],redo:[],preview:null,serial:0,pending:false,search:''};
}
export const studioDirty = draft => !studioEqual(draft.graph,draft.original);
export function studioSelected(draft) {
  return draft.selection ? draft.graph[draft.selection.collection]?.find(o=>o.id===draft.selection.id) : null;
}
export function studioMutate(draft,change) {
  const before=studioClone(draft.graph),copy=studioClone(draft.graph);
  change(copy);
  if(studioEqual(before,copy))return false;
  draft.undo.push(before);if(draft.undo.length>30)draft.undo.shift();
  draft.redo=[];draft.graph=copy;draft.preview=null;draft.serial++;return true;
}
export function studioHistory(draft,direction) {
  const from=direction==='undo'?draft.undo:draft.redo,to=direction==='undo'?draft.redo:draft.undo;
  if(!from.length)return false;
  to.push(studioClone(draft.graph));draft.graph=from.pop();draft.preview=null;draft.serial++;
  if(!studioSelected(draft))draft.selection=null;return true;
}
export function studioPath(root,path) {
  const parts=path.split('.');
  if(parts.some(p=>!p||['__proto__','constructor','prototype'].includes(p)||!/^\w+$/.test(p)))throw new Error('Invalid draft field');
  let parent=root;for(const p of parts.slice(0,-1)){if(parent==null||typeof parent!=='object'||!Object.hasOwn(parent,p))throw new Error('Draft field no longer exists');parent=parent[p];}
  return {parent,key:parts.at(-1)};
}
export function studioSet(root,path,value) {const {parent,key}=studioPath(root,path);parent[key]=value;}
export function studioAt(root,path) {const {parent,key}=studioPath(root,path);return parent[key];}
export function studioAtom(cid='') {return {op:'atom',condition_id:cid,value:true,args:[]};}
export function studioGroup(op='all') {return {op,condition_id:null,value:true,args:[]};}
export function studioRules(expr) {return !expr?[]:expr.op==='atom'?[expr.condition_id]:expr.args.flatMap(studioRules);}
export function studioReferences(draft,kind,id) {
  const refs=[];
  if(kind==='conditions') {
    for(const a of draft.graph.actions) {
      if([...studioRules(a.requires),...studioRules(a.guard),...a.effects.map(e=>e.condition_id),...a.contingencies.flatMap(c=>studioRules(c.when))].includes(id))refs.push(a.title);
    }
    for(const o of draft.graph.objectives)if([...studioRules(o.success),...studioRules(o.failure)].includes(id))refs.push(o.title);
    for(const x of [...draft.baseCase.questions,...draft.baseCase.claims,...draft.baseCase.constraints]) {
      if(x.condition_id===id||x.condition_ids?.includes(id)||studioRules(x.predicate).includes(id))refs.push(x.title??x.question??'Referenced source claim');
    }
    if(draft.baseCase.observations.some(o=>o.condition_id===id))refs.push('Historical observations');
  } else if(kind==='actions') {
    if(draft.baseCase.completed.includes(id))refs.push('Completed action history');
    for(const a of draft.graph.actions)if(a.contingencies.some(b=>b.next_action_ids.includes(id)))refs.push(a.title+' contingency');
    for(const c of draft.baseCase.constraints)if(c.action_ids.includes(id))refs.push(c.title);
  }
  return [...new Set(refs)];
}
export function studioRemove(draft,kind,id) {
  const refs=studioReferences(draft,kind,id);
  if(refs.length)throw new Error('Still referenced by: '+refs.join(', ')+'. Edit those links explicitly first.');
  studioMutate(draft,g=>{g[kind]=g[kind].filter(x=>x.id!==id);});draft.selection=null;
}
export function studioCreate(draft,kind,id) {
  if(!['conditions','actions','objectives'].includes(kind))throw new Error('Unsupported draft object');
  if(draft.graph[kind].some(o=>o.id===id))throw new Error('Repeated object ID');
  const provenance={origin:'operator',references:[],run_id:null,note:'Human-authored Plan Studio draft'};
  let value;
  if(kind==='conditions')value={id,title:'New condition',confirmation:'',kind:'prerequisite',due_at:null,criticality:'ordinary',actor_id:null,provenance};
  if(kind==='actions')value={id,title:'New action',owner:draft.baseCase.owner,purpose:'',requires:studioGroup(),guard:studioGroup(),effects:[],
    minutes:30,cost:0,risk:'medium',approval_required:true,contingent:false,wait_minutes:null,earliest_start:null,expires_at:null,
    reversibility:'difficult',side_effects:[],actor_ids:[],resources:[],decision_id:null,decision_option:null,enabled:true,contingencies:[],provenance};
  if(kind==='objectives')value={id,title:'New objective',mandatory:true,priority:1,success:studioGroup(),failure:null,provenance};
  studioMutate(draft,g=>g[kind].push(value));draft.selection={collection:kind,id};return value;
}
export function studioEdit(draft,fn) {
  const sel=draft.selection;if(!sel)throw new Error('Select a record first');
  if(sel.collection==='actions'&&draft.baseCase.completed.includes(sel.id))throw new Error('Completed actions cannot be rewritten');
  return studioMutate(draft,g=>fn(g[sel.collection].find(x=>x.id===sel.id)));
}
export function studioChangeField(draft,path,value) {
  const sel=draft.selection;
  if(sel?.collection==='conditions'&&['title','confirmation','kind'].includes(path)&&draft.baseCase.observations.some(o=>o.condition_id===sel.id))throw new Error('Observed condition meanings cannot be rewritten');
  studioEdit(draft,obj=>studioSet(obj,path,value));
}
