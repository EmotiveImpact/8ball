import {S,esc,icon,badge,button,heading,note,warning,gbp,duration,pretty,localDate,toast,modal,closeModal} from './ui.js';
import {createStudioDraft,studioDirty,studioSelected,studioHistory,studioClone,studioEdit,studioSet,studioAt,studioPath,studioAtom,studioGroup,studioRemove,studioCreate,studioChangeField} from './studio-model.js';

const stButton=(label,action,attrs='',primary=false)=>`<button type="button" class="button ${primary?'primary':''}" data-studio="${action}" ${attrs}>${label}</button>`;
const stOptions=(items,current)=>items.map(([id,label])=>`<option value="${esc(id)}" ${String(id)===String(current)?'selected':''}>${esc(label)}</option>`).join('');
function stField(label,path,value,{type='text',disabled=false,nullable=false,max=180,min=null,multiline=false}={}) {
  const attrs=`data-studio-field="${esc(path)}" data-type="${type}" ${nullable?'data-nullable':''} ${disabled?'disabled':''}`;
  let content;
  if(type==='checkbox')return `<label class="check"><input type="checkbox" ${attrs} ${value?'checked':''}><span>${esc(label)}</span></label>`;
  if(type==='datetime-local')value=value?localDate(value):'';
  content=multiline?`<textarea ${attrs} maxlength="${max}" rows="3">${esc(value??'')}</textarea>`:`<input type="${type}" ${attrs} value="${esc(value??'')}" ${type==='number'?`step="1" ${min===null?'':`min="${min}"`}`:`maxlength="${max}"`}>`;
  return `<label class="field"><span>${esc(label)}</span>${content}</label>`;
}
const stSelect=(label,path,items,value,{nullable=false,disabled=false}={})=>`<label class="field"><span>${esc(label)}</span><select data-studio-field="${esc(path)}" ${nullable?'data-nullable':''} ${disabled?'disabled':''}>${stOptions(items,value??'')}</select></label>`;
const stChoices=(label,path,items,values)=>`<fieldset class="st-options"><legend>${esc(label)}</legend>${items.length?items.map(([id,t])=>`<label class="check"><input type="checkbox" data-studio-list="${esc(path)}" value="${esc(id)}" ${values.includes(id)?'checked':''}><span>${esc(t)}</span></label>`).join(''):note('None recorded in this case.')}</fieldset>`;
const stConditions=()=>S.studio.graph.conditions.map(c=>[c.id,c.title]);
const stActions=()=>S.studio.graph.actions.map(a=>[a.id,a.title]);
function stExpression(e,path,label='Requirements',depth=0) {
  if(!e)return `<div class="st-expr-empty">${note('No '+label.toLowerCase()+' set.')} ${stButton('Add condition','set-expression',`data-path="${esc(path)}"`)}</div>`;
  if(depth>8)return warning('Expression depth exceeds the supported editor limit. Inspect advanced JSON.');
  if(e.op==='atom')return `<div class="st-rule"><div class="st-rule-fields">${stSelect('Condition',path+'.condition_id',[['','Choose a condition'],...stConditions()],e.condition_id)}${stSelect('Must be explicitly',path+'.value',[['true','True'],['false','False']],String(e.value))}</div><div class="st-rule-controls">${stButton('Group','wrap',`data-path="${esc(path)}" aria-label="Wrap ${esc(label)} in a group"`)}${stButton('Remove','remove-expression',`data-path="${esc(path)}" aria-label="Remove ${esc(label)} rule"`)}</div></div>`;
  return `<fieldset class="st-expression"><legend>${esc(label)}</legend><div class="st-group-head"><label><span class="sr-only">Combination</span><select data-studio-field="${esc(path)}.op">${stOptions([['all','ALL of these (AND)'],['any','ANY of these (OR)']],e.op)}</select></label><small>${e.op==='all'?'Every requirement must hold.':'One supported alternative is enough.'}</small></div>${e.args.length?e.args.map((x,i)=>stExpression(x,path+'.args.'+i,'Requirement '+(i+1),depth+1)).join(''):note(e.op==='all'?'No requirements in this group. This is unconditional.':'Empty OR group is invalid. Add an alternative.')}<div class="st-rule-toolbar">${depth<7&&e.args.length<8?stButton('＋ Condition','add-rule',`data-path="${esc(path)}"`)+stButton('＋ Nested group','add-group',`data-path="${esc(path)}"`):note('Group limit reached.')}${path.includes('.args.')?stButton('Remove group','remove-expression',`data-path="${esc(path)}"`):''}</div></fieldset>`;
}
function stConditionEditor(c) {
  const locked=S.studio.baseCase.observations.some(o=>o.condition_id===c.id);
  return `${locked?warning('This condition has historical observations. Its meaning is locked; create a new condition for a different assertion.','neutral'):''}
    ${stField('Condition title','title',c.title,{disabled:locked})}${stField('What evidence would establish this?','confirmation',c.confirmation,{disabled:locked,multiline:true})}
    <div class="form-grid">${stSelect('Type','kind',['fact','prerequisite','target','external_state','verification'].map(x=>[x,pretty(x)]),c.kind,{disabled:locked})}${stSelect('Importance','criticality',['ordinary','important','critical'].map(x=>[x,pretty(x)]),c.criticality)}${stField('Condition deadline','due_at',c.due_at,{type:'datetime-local',nullable:true})}${stSelect('Linked actor','actor_id',[['','Not assigned'],...S.studio.baseCase.actors.map(a=>[a.id,a.name])],c.actor_id,{nullable:true})}</div>${note('Editing a condition never changes its evidence state. Observations are recorded separately.')}`;
}
function stActionEditor(a) {
  const base=S.studio.baseCase,locked=base.completed.includes(a.id);
  const d=base.decisions.find(d=>d.id===a.decision_id);
  return `${locked?warning('Completed action: preserved as history. Create another action rather than rewriting this one.','neutral'):''}<fieldset class="st-unframed" ${locked?'disabled':''}>
    ${stField('Action title','title',a.title)}${stField('Purpose','purpose',a.purpose,{multiline:true})}
    <div class="form-grid">${stField('Responsible owner','owner',a.owner)}${stSelect('Reversibility','reversibility',['reversible','difficult','irreversible'].map(x=>[x,pretty(x)]),a.reversibility)}${stField('Active duration (minutes)','minutes',a.minutes,{type:'number',min:1})}${stField('Estimated cost (GBP)','cost',a.cost,{type:'number',min:0})}${stField('Waiting time (minutes), blank when unknown','wait_minutes',a.wait_minutes,{type:'number',min:0,nullable:true})}${stSelect('Operator-rated risk','risk',['low','medium','high'].map(x=>[x,pretty(x)]),a.risk)}</div>
    <div class="st-flags">${stField('Enabled for planning','enabled',a.enabled,{type:'checkbox'})}${stField('Human approval required','approval_required',a.approval_required,{type:'checkbox'})}${stField('Another party controls the result','contingent',a.contingent,{type:'checkbox'})}</div>
    <details open class="st-section"><summary>Prerequisites <span>What must be true first</span></summary>${stExpression(a.requires,'requires','Prerequisites')}</details>
    <details class="st-section"><summary>Restrictions / guard <span>Explicit evidence required to act</span></summary>${note('False means explicitly contradicted, not unknown. Guards never turn assumptions into facts.')}${stExpression(a.guard,'guard','Guard')}</details>
    <details open class="st-section"><summary>Intended results <span>Still require proof after the action</span></summary>${a.effects.map((e,i)=>`<div class="st-rule"><div class="st-rule-fields">${stSelect('Intended condition',`effects.${i}.condition_id`,[['','Choose condition'],...stConditions()],e.condition_id)}${stSelect('Intended value',`effects.${i}.value`,[['true','True'],['false','False']],String(e.value))}</div>${stButton('Remove','remove-item',`data-path="effects" data-index="${i}"`)}</div>`).join('')}${a.effects.length<8?stButton('＋ Result condition','add-effect'):''}${!a.effects.length?note('At least one intended effect is required.'):''}</details>
    <details class="st-section"><summary>Timing, resources & decisions <span>Limits and authorisation</span></summary><div class="form-grid">${stField('Earliest start','earliest_start',a.earliest_start,{type:'datetime-local',nullable:true})}${stField('Action expires at','expires_at',a.expires_at,{type:'datetime-local',nullable:true})}${stSelect('Decision gate','decision_id',[['','No decision gate'],...base.decisions.map(d=>[d.id,d.question])],a.decision_id,{nullable:true})}${stSelect('Required option','decision_option',[['','Select option'],...(d?.options??[]).map(o=>[o.id,o.title])],a.decision_option,{nullable:true})}</div>${stChoices('Resources (one action at a time)','resources',base.resources.map(r=>[r.id,r.name]),a.resources)}${stChoices('Actors involved','actor_ids',base.actors.map(a=>[a.id,a.name]),a.actor_ids)}</details>
    <details class="st-section"><summary>Contingencies <span>Acceptance, refusal or no response</span></summary>${a.contingencies.map((b,i)=>`<section class="st-contingency"><div class="meta"><span class="kicker">BRANCH ${i+1}</span>${stButton('Remove branch','remove-item',`data-path="contingencies" data-index="${i}"`)}</div>${stField('Branch label',`contingencies.${i}.label`,b.label)}${stField('Human response / follow-up',`contingencies.${i}.response`,b.response,{multiline:true})}${stExpression(b.when,`contingencies.${i}.when`,'Trigger')}${stField('Review time',`contingencies.${i}.due_at`,b.due_at,{type:'datetime-local',nullable:true})}${stChoices('Possible follow-up actions',`contingencies.${i}.next_action_ids`,stActions(),b.next_action_ids)}</section>`).join('')}${a.contingencies.length<8?stButton('＋ Add contingency','add-contingency'):''}${note('Triggers are observed conditions, not automatic emails or actions.')}</details>
    <details class="st-section"><summary>Possible side effects</summary>${stField('One possible side effect per line','side_effects',a.side_effects.join('\n'),{type:'lines',multiline:true,max:2200})}${note('These are disclosed possibilities, not automatically applied real-world effects.')}</details></fieldset>`;
}
function stObjectiveEditor(o) {
  return `${stField('Objective title','title',o.title)}<div class="st-flags">${stField('Mandatory for resolution','mandatory',o.mandatory,{type:'checkbox'})}</div>${stField('Priority (1 highest, 5 lowest)','priority',o.priority,{type:'number',min:1})}${stExpression(o.success,'success','Success conditions')}<div class="spacer"></div><h3>Failure criteria</h3>${stExpression(o.failure,'failure','Failure criteria')}${o.failure?stButton('Remove failure criterion','clear-failure'):''}${warning('Empty success groups are rejected. Changing this target does not make it achieved.','neutral')}`;
}
function stPreviewPanel() {
  const d=S.studio,p=d.preview;
  if(!p)return `<div class="st-preview-empty">${icon('routes')}<h3>See the effect before you commit.</h3><p>Preview calculates routes from this draft. Your live case, evidence and decisions remain untouched.</p></div>`;
  return `<div class="st-preview-metrics"><div><b>${p.edits.length}</b><small>Object changes</small></div><div><b>${p.live_routes} → ${p.plan.routes.length}</b><small>Candidate routes</small></div></div>${p.warnings.map(w=>warning(w,'neutral')).join('')}
    <h3>Changes to review</h3>${p.edits.map(e=>`<div class="st-diff"><span>${badge('reported',e.change)}</span><div><strong>${esc(e.title)}</strong><small>${esc(e.fields.join(', '))}</small></div></div>`).join('')||note('No graph changes.')}
    <h3>Draft route results</h3>${p.plan.routes.map(r=>`<div class="st-draft-route"><strong>${esc(r.title)}</strong>${badge(r.status)}<p>${r.provisional?'≥ ':''}${duration(r.minutes)} · ${gbp(r.total_cost)}</p><small>${r.evidence_gaps.length} evidence gaps · ${r.external_dependencies.length} external dependencies</small>${r.hard_breaches.length?note(r.hard_breaches.join('; ')):''}</div>`).join('')||note('No plan can be computed without mandatory objectives.')}`;
}
export function studioPage() {
  const c=S.current.case;
  if(!S.studio||S.studio.caseId!==c.id)S.studio=createStudioDraft(c);
  const d=S.studio,o=studioSelected(d),dirty=studioDirty(d),stale=d.baseRevision!==c.revision;
  return heading('PLAN STUDIO / HUMAN AUTHORING','Engineer the route.','Build explicit conditions, dependencies and contingencies. Preview first. Commit deliberately.',
    `<button type="button" class="button" data-pr-action="open">Review live plan</button>`+stButton('Undo','undo',d.undo.length?'':'disabled')+stButton('Redo','redo',d.redo.length?'':'disabled')+
    stButton('Discard draft','discard',dirty?'':'disabled')+stButton(d.pending?'Calculating…':'Preview changes','preview',d.pending||stale?'disabled':'',true))+
    `<div class="st-statusbar"><span>${badge('reported','DRAFT · NOT LIVE')} Based on case revision ${d.baseRevision}</span><span>${dirty?'Unsaved changes':'No changes'}${stale?' · Case has changed; reload the draft':''}</span></div>`+
    (stale?warning('The live case changed while this draft was open. It cannot overwrite the newer revision. Export or inspect your changes, then discard and restart.'): '')+
    `<div class="studio-layout"><aside class="st-library"><header><span class="kicker">PLAN OBJECTS</span><label class="field"><span class="sr-only">Find an object</span><input type="search" data-studio-search value="${esc(d.search)}" placeholder="Find an object…"></label></header>${['conditions','actions','objectives'].map(kind=>`<section><div class="st-library-title"><h3>${pretty(kind)} <small>${d.graph[kind].length}</small></h3>${stButton('＋','create',`data-kind="${kind}" aria-label="Add ${kind.slice(0,-1)}"`)}</div><div class="st-object-list">${d.graph[kind].filter(x=>x.title.toLowerCase().includes(d.search.toLowerCase())).map(x=>`<button type="button" data-studio="select" data-kind="${kind}" data-id="${esc(x.id)}" class="st-object ${d.selection?.id===x.id&&d.selection?.collection===kind?'selected':''}"><span>${esc(x.title)}</span>${kind==='conditions'?badge(S.current.plan.states[x.id]?.status??'unknown'):kind==='actions'&&d.baseCase.completed.includes(x.id)?icon('lock'):icon('arrow')}</button>`).join('')||note('No matching records.')}</div></section>`).join('')}</aside>
    <section class="st-editor">${o?`<header><span class="kicker">${esc(d.selection.collection.slice(0,-1))} / ${esc(o.id.slice(0,18))}</span><h2>${esc(o.title)}</h2></header><div class="st-editor-body">${d.selection.collection==='conditions'?stConditionEditor(o):d.selection.collection==='actions'?stActionEditor(o):stObjectiveEditor(o)}<div class="st-editor-footer">${stButton('Remove record','remove')}<details><summary>Inspect structured record</summary><pre class="code">${esc(JSON.stringify(o,null,2))}</pre></details></div></div>`:`<div class="st-welcome"><span class="kicker">YOUR OUTCOME</span><h2>${esc(c.desired_outcome)}</h2><p>Select a condition, action or objective. Changes stay in this draft until you preview and commit them.</p><div class="st-guide"><span>01</span><p>Define what must become true.</p><span>02</span><p>Connect the prerequisites and available actions.</p><span>03</span><p>Check alternatives and explicit proof of success.</p></div></div>`}</section>
    <aside class="st-impact"><header><span class="kicker">CHANGE PREVIEW</span><h2>What this changes</h2></header><div class="st-impact-body">${stPreviewPanel()}</div><footer>${stButton('Review & commit','commit',d.preview&&dirty&&!stale&&!d.pending?'':'disabled',true)}${note('No messages sent. No evidence state changed.')}</footer></aside></div>`;
}
export async function studioClick(el,services) {
  const d=S.studio;if(!d)return;
  const action=el.dataset.studio,path=el.dataset.path;
  if(d.pending&&!['select'].includes(action))throw new Error('Wait for the current preview or save to finish.');
  if(action==='select'){d.selection={collection:el.dataset.kind,id:el.dataset.id};services.render();return;}
  if(action==='create')studioCreate(d,el.dataset.kind,el.dataset.kind.slice(0,1)+'_'+crypto.randomUUID().replaceAll('-',''));
  if(action==='undo'||action==='redo')studioHistory(d,action);
  if(action==='remove')studioRemove(d,d.selection.collection,d.selection.id);
  if(action==='discard') {
    modal('Discard this local draft?',note('This removes only your uncommitted Plan Studio edits. The live case stays unchanged.')+`<div class="form-actions">${stButton('Discard edits','discard-confirm')}</div>`);return;
  }
  if(action==='discard-confirm'){S.studio=createStudioDraft(S.current.case);closeModal();services.render();return;}
  if(['add-rule','add-group'].includes(action))studioEdit(d,o=>{const e=studioAt(o,path);if(e.args.length>=8)throw new Error('Eight children per group maximum.');e.args.push(action==='add-rule'?studioAtom():studioGroup());});
  if(action==='wrap')studioEdit(d,o=>studioSet(o,path,{...studioGroup(),args:[studioClone(studioAt(o,path))]}));
  if(action==='set-expression')studioEdit(d,o=>studioSet(o,path,studioAtom()));
  if(action==='clear-failure')studioEdit(d,o=>o.failure=null);
  if(action==='remove-expression')studioEdit(d,o=>{
    if(path.includes('.args.')){const parts=path.split('.'),i=Number(parts.pop());studioAt(o,parts.join('.')).splice(i,1);}
    else studioSet(o,path,path==='failure'?null:studioGroup());
  });
  if(action==='add-effect')studioEdit(d,o=>{if(o.effects.length>=8)throw new Error('Eight effects maximum.');o.effects.push({condition_id:'',value:true});});
  if(action==='add-contingency')studioEdit(d,o=>{if(o.contingencies.length>=8)throw new Error('Eight branches maximum.');o.contingencies.push({label:'New branch',response:'',when:studioAtom(),next_action_ids:[],due_at:null});});
  if(action==='remove-item')studioEdit(d,o=>studioAt(o,path).splice(Number(el.dataset.index),1));
  if(action==='preview') {
    const serial=d.serial;d.pending=true;services.render();
    try {const result=await services.api(`/cases/${d.caseId}/graph/preview`,{expected_revision:d.baseRevision,graph:studioClone(d.graph)});if(S.studio===d&&d.serial===serial)d.preview=result;}
    finally {d.pending=false;services.render();}
    return;
  }
  if(action==='commit') {
    if(!d.preview||!studioDirty(d))throw new Error('Preview this exact draft before committing.');
    modal('Commit this plan amendment?',warning(`${d.preview.edits.length} graph object(s) change. Existing approvals are invalidated. Evidence observations are not changed.`,'neutral')+`<div class="form-actions">${stButton('Commit reviewed amendment','commit-confirm','',true)}</div>`);return;
  }
  if(action==='commit-confirm') {
    if(!d.preview||d.baseRevision!==S.current.case.revision)throw new Error('Preview is stale. Reload and review again.');
    d.pending=true;
    try {await services.commit('replace_graph',{graph:studioClone(d.graph)},{caseId:d.caseId,revision:d.baseRevision});S.studio=createStudioDraft(S.current.case);services.render();}
    finally {d.pending=false;}
    return;
  }
  services.render();
}
export function studioChange(el,services) {
  const d=S.studio;if(!d)return;
  if(d.pending)throw new Error('Cannot change the draft while saving or previewing.');
  if(el.hasAttribute('data-studio-search')){d.search=el.value;services.render();return;}
  if(el.dataset.studioList){studioEdit(d,o=>{const values=studioAt(o,el.dataset.studioList);studioSet(o,el.dataset.studioList,el.checked?[...new Set([...values,el.value])]:values.filter(v=>v!==el.value));});}
  else {
    const path=el.dataset.studioField;let value=el.value;
    if(el.type==='checkbox')value=el.checked;
    else if(path.endsWith('.value'))value=value==='true';
    else if(el.dataset.type==='number'){value=el.value===''&&el.hasAttribute('data-nullable')?null:Number(el.value);if(value!==null&&(!Number.isInteger(value)||value<0))throw new Error('Enter a non-negative whole number.');}
    else if(el.dataset.type==='datetime-local')value=value?new Date(value).toISOString():null;
    else if(el.dataset.type==='lines')value=value.split('\n').map(s=>s.trim()).filter(Boolean);
    else if(el.hasAttribute('data-nullable')&&value==='')value=null;
    if(path==='decision_id')studioEdit(d,o=>{o.decision_id=value;o.decision_option=null;});
    else studioChangeField(d,path,value);
  }
  const selected=studioSelected(d);
  const structural=el.hasAttribute('data-studio-search')||el.dataset.studioField==='decision_id'||el.dataset.studioField?.endsWith('.op');
  if(structural){
    const selector=el.dataset.studioField?`[data-studio-field="${CSS.escape(el.dataset.studioField)}"]`:'[data-studio-search]';
    services.render();document.querySelector(selector)?.focus();
  } else {
    // Do not replace a form on blur: that would swallow the user's next click.
    const title=document.querySelector('.st-editor>header h2');if(title&&selected)title.textContent=selected.title;
    if(d.selection){const label=document.querySelector(`[data-studio="select"][data-kind="${d.selection.collection}"][data-id="${CSS.escape(d.selection.id)}"] span`);if(label&&selected)label.textContent=selected.title;}
    const status=document.querySelector('.st-statusbar>span:last-child');if(status)status.textContent=studioDirty(d)?'Unsaved changes':'No changes';
    const preview=document.querySelector('.st-impact-body');if(preview)preview.innerHTML=stPreviewPanel();
    const commit=document.querySelector('[data-studio="commit"]');if(commit)commit.disabled=true;
    const undo=document.querySelector('[data-studio="undo"]');if(undo)undo.disabled=!d.undo.length;
    const redo=document.querySelector('[data-studio="redo"]');if(redo)redo.disabled=!d.redo.length;
    const discard=document.querySelector('[data-studio="discard"]');if(discard)discard.disabled=!studioDirty(d);
  }
}
