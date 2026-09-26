import {S,esc,pretty,badge,note,warning,field,select,textarea,modal,closeModal,toast,date,gbp,duration,saveFile} from './ui.js';

let io=null, ticket=0, pending=null, openSequence=0;
const courseId=()=>crypto.randomUUID?.()??Array.from(crypto.getRandomValues(new Uint8Array(16)),b=>b.toString(16).padStart(2,'0')).join('');
export function clearCourse(){ticket++;openSequence++;pending=null;S.courseView=null;}
const same=(id,epoch)=>S.current?.case.id===id&&S.epoch===epoch;
const cb=(label,action,attrs='')=>`<button type="button" class="button" data-course-action="${action}" ${attrs}>${label}</button>`;
const current=()=>S.courseView?.courses?.find(c=>c.id===S.courseView.current_id);
const title=state=>({review_required:'Review required',no_trigger_detected:'No declared trigger detected',outcome_evidenced:'Outcome evidenced',not_assessable:'Cannot fully assess'}[state]??pretty(state));
export async function loadCourse(api){
  const id=S.current?.case.id,epoch=S.epoch,t=++ticket;
  if(!id)return;
  try{const data=await api(`/cases/${id}/courses`);if(t===ticket&&same(id,epoch))S.courseView=data;}
  catch(error){if(t===ticket&&same(id,epoch))S.courseView={case_id:id,error:error.message};}
}
export function courseBanner(){
  const v=S.courseView;
  if(!v||v.case_id!==S.current?.case.id)return '';
  if(v.error)return warning('Chosen course could not be verified: '+v.error);
  if(v.case_revision!==S.current.case.revision)return warning('The chosen-course assessment is older than this case. Refresh before relying on it.');
  const c=current();
  if(!c)return `<section class="course-empty"><div><span class="kicker">CHOSEN COURSE</span><p>Keep the team’s choice separate from the list of possibilities.</p></div><div class="toolbar"><button type="button" class="text-button" data-tab="routes">Explore routes ↗</button>${v.courses.length?cb('Choice history','history'):''}</div></section>`;
  const a=c.assessment.result,important=a.reasons.filter(r=>r.requires_review);
  return `<section class="course-banner" data-course-current="${esc(c.id)}"><div class="course-mark">↗</div><div class="course-main"><div class="course-meta"><span class="kicker">CHOSEN COURSE / REV ${c.selected_revision}</span>${badge(c.lifecycle==='paused'?'pending':a.state==='no_trigger_detected'?'reported':'pending',c.lifecycle==='paused'?'Course paused':title(a.state))}</div><h2>${esc(c.title)}</h2><p>${esc(important[0]?.detail??'Your recorded choice is preserved. Recalculation has not switched to a different route.')}</p><small>${a.remaining_action_ids.length} recorded actions not completed · ${a.completed_action_ids.length} completed · Checked ${date(a.as_of)} · On request</small></div><div class="toolbar">${cb('Inspect course','inspect')}${cb('History','history')}</div></section>`;
}
export function chooseCourseButton(r){return r.actions.length&&!r.hard_breaches.length?cb('Choose course','choose',`data-route="${esc(r.id)}"`):'';}
export function courseTimeline(){const v=S.courseView;if(!v||v.case_id!==S.current?.case.id)return [];return(v.records??[]).map(r=>({id:r.event_id,time:r.recorded_at,title:'Course '+pretty(r.operation).toLowerCase(),description:r.rationale,type:'Human course choice · not action approval'}));}
function watchesForm(){return `<div class="form-grid">${select('Reconsider when this condition…','watch_condition',[['','No explicit condition watch'],...S.current.case.graph.conditions.map(c=>[c.id,c.title])])}${select('…has this evidenced state','watch_state',[['true','Supported true'],['false','Supported false'],['disputed','Disputed'],['unknown','Unknown']])}</div>${field('Review time (optional, explicit UTC offset required)','review_at','','text','placeholder="2026-09-26T14:00:00+01:00"')}${note('A review time is checked when this view refreshes. It does not create a background notification.')}`;}
async function choose(routeId){
  openSequence++;
  const c=S.current.case;
  pending={caseId:c.id,revision:c.revision,epoch:S.epoch,routeId};
  modal('Choose a course',warning('This records the direction you intend to pursue. It neither approves actions nor establishes facts.','neutral')+`<form data-course-form="preview">${watchesForm()}<div class="form-actions"><button class="button primary" type="submit">Preview this choice</button></div></form>`);
}
function drawSelection(data){
  const p=data.preview,a=p.anchor,r=a.route;
  const conditions=a.baseline.graph.conditions;
  modal('Review the chosen course',`<div class="course-target"><span class="kicker">EXACT REQUESTED OUTCOME</span><h3>${esc(p.requested_outcome)}</h3></div><h2>${esc(r.title)}</h2><div class="course-stats"><div><strong>${duration(r.minutes)}</strong><small>Conditional estimate</small></div><div><strong>${gbp(r.total_cost)}</strong><small>Total estimated cost</small></div><div><strong>${r.external_dependencies.length}</strong><small>External dependencies</small></div></div>${warning('No guarantee of success. Unknown waits are lower bounds. Selecting this course does not change existing action permissions.','neutral')}${data.current_id?warning('This explicitly replaces the current choice. Its rationale and history will remain available.'):''}<form data-course-form="select">${textarea('Why are we choosing this course?','rationale','','required minlength="10" maxlength="2000"')}${textarea('Assumptions to keep visible (one per line, optional)','assumptions','','maxlength="5000"')}<div class="course-watches">${a.watches.map(w=>`<p>${esc(conditions.find(c=>c.id===w.condition_id)?.title??w.condition_id)} → ${esc(w.state)}</p>`).join('')}${note('Review time: '+(a.review_at??'Not set'))}</div><label class="check"><input type="checkbox" name="acknowledge" required><span>I have reviewed the conditions and estimates. This choice is not an action approval, factual attestation or prediction.</span></label><div class="form-actions"><button class="button primary" type="submit">Record chosen course</button></div></form>`,true);
}
async function inspect(){
  const id=S.current.case.id,epoch=S.epoch,seq=++openSequence;await loadCourse(io.api);
  if(!same(id,epoch)||seq!==openSequence)return;
  if(S.courseView?.error)throw new Error(S.courseView.error);
  const c=current();if(!c)throw new Error('There is no current course. Choose a route first.');
  pending={caseId:id,epoch,revision:S.current.case.revision,course:c,sequence:S.courseView.sequence};
  const a=c.assessment.result;
  const names=new Map(S.current.case.graph.actions.map(x=>[x.id,x.title]));
  modal('Chosen course',`<div class="course-meta"><span class="kicker">HUMAN CHOICE / REV ${c.selected_revision}</span>${badge('reported',pretty(c.lifecycle))}${badge(a.state==='no_trigger_detected'?'reported':'pending',title(a.state))}</div><h2>${esc(c.title)}</h2><div class="course-target"><span class="kicker">OUTCOME AT SELECTION</span><p>${esc(c.requested_outcome)}</p>${c.requested_outcome!==S.current.case.desired_outcome?`<div class="spacer"></div><span class="kicker">CURRENT REQUESTED OUTCOME</span><p>${esc(S.current.case.desired_outcome)}</p>`:''}</div><h3>Why this course</h3><blockquote>${esc(c.rationale)}</blockquote>${c.assumptions.length?`<h3>Operator-declared assumptions, not facts</h3>${c.assumptions.map(x=>`<p class="note">${esc(x)}</p>`).join('')}`:''}<div class="spacer"></div><h3>What needs reconsideration</h3>${a.reasons.map(r=>`<div class="course-reason"><strong>${esc(pretty(r.code))}</strong><p>${esc(r.detail)}</p><small>${esc(r.references.join(' · '))}</small></div>`).join('')||note('No declared trigger was detected. This is not assurance that no unmodelled change matters.')}<div class="spacer"></div><h3>Recorded work still not completed</h3><div class="course-actions">${a.remaining_action_ids.map(i=>`<span>${esc(names.get(i)??i)}</span>`).join('')||note('No recorded actions remain. Outcomes still require their separate evidence.')}</div>${note('Recalculation uses the original selected action set and prerequisite branches. A shorter remaining route is not a new course selection.')}<div class="spacer"></div><h3>Other current options, not selected</h3>${a.alternatives.map(r=>`<div class="row"><div><h3>${esc(r.title)}</h3><p>${esc(pretty(r.status))}</p></div>${!r.hard_breaches.length?chooseCourseButton(r):''}</div>`).join('')||note('No other options were returned within the current catalogue and bounds.')}<div class="spacer"></div>${warning('Pausing or retiring this record does not cancel external work or revoke separate action approvals. Reviewing never clears these diagnostics.','neutral')}<div class="toolbar">${cb('Record review','transition','data-operation="review"')}${cb(c.lifecycle==='paused'?'Resume record':'Pause record','transition',`data-operation="${c.lifecycle==='paused'?'resume':'pause'}"`)}${cb('Retire record','transition','data-operation="retire"')}${cb('Export course history','export')}</div>${c.latest_review?note('Last recorded review: '+date(c.latest_review.recorded_at)+'. This is a historical judgement, not approval of the latest case.'):''}`,true);
}
function transition(op){
 const p=pending;if(!p?.course)throw new Error('Refresh the chosen course first.');
 p.operation=op;
 modal(pretty(op)+' course record',warning('The original choice and all judgements remain in history. This does not attest facts, send messages or authorise any action.','neutral')+`<h3>${esc(p.course.title)}</h3><form data-course-form="event">${textarea('Reason for this judgement','rationale','','required minlength="10" maxlength="2000"')}<div class="form-actions"><button class="button primary" type="submit">Record ${esc(op)}</button></div></form>`);
}
async function history(){
 const id=S.current.case.id,epoch=S.epoch,seq=++openSequence;await loadCourse(io.api);if(!same(id,epoch)||seq!==openSequence)return;
 const v=S.courseView;if(v.error)throw new Error(v.error);
 modal('Course history',note('Choices and lifecycle judgements are separate from the factual case and action-approval ledger. Previous and retired records stay visible.')+(v.courses??[]).map(c=>`<section class="course-history"><div class="course-meta">${badge('reported',pretty(c.lifecycle))}<small>Selected ${date(c.selected_at)} · Revision ${c.selected_revision}</small></div><h3>${esc(c.title)}</h3><p>${esc(c.rationale)}</p></section>`).join('')+`<details><summary>Inspect the recorded sequence</summary>${(v.records??[]).map(r=>`<div class="row"><div><h3>${esc(pretty(r.operation))}</h3><p>${esc(r.rationale)}</p><small>Case revision ${r.case_revision} · ${date(r.recorded_at)}</small></div></div>`).join('')}</details><div class="form-actions">${cb('Export course history','export')}</div>`,true);
}
export function bindCourse(services){
 io=services;
 document.addEventListener('click',async e=>{
  if(e.target.closest('[data-action=close],[data-tab],[data-case]')){pending=null;openSequence++;}
  const el=e.target.closest('[data-course-action]');if(!el)return;
  try{switch(el.dataset.courseAction){
   case'choose':await choose(el.dataset.route);break;
   case'inspect':await inspect();break;
   case'transition':transition(el.dataset.operation);break;
   case'history':await history();break;
   case'export':{const id=S.current.case.id,epoch=S.epoch;const data=await io.api(`/cases/${id}/export`);if(!same(id,epoch))return;if(!data.valid)throw new Error('The case audit did not verify.');saveFile('8BALL-chosen-course-history.json',data.chosen_courses??{records:[]});break;}
  }}catch(error){toast(error.message,true);}
 });
 document.addEventListener('submit',async e=>{
  const f=e.target;if(!f.dataset.courseForm)return;e.preventDefault();
  const p=pending,button=f.querySelector('[type=submit]');if(button.disabled)return;
  button.disabled=true;
  try{
   if(!p||!same(p.caseId,p.epoch)||p.revision!==S.current.case.revision)throw new Error('The case changed. Reopen the course review.');
   const fd=new FormData(f),v=Object.fromEntries(fd),base=`/cases/${p.caseId}/courses`;
   if(f.dataset.courseForm==='preview'){
    const watches=v.watch_condition?[{condition_id:v.watch_condition,state:v.watch_state}]:[];
    if(v.review_at&&!/T.*(?:Z|[+-]\d{2}:\d{2})$/.test(v.review_at))throw new Error('Use an explicit ISO date/time with a UTC offset, for example 2026-09-26T14:00:00+01:00.');
    const data=await io.api(base+'/preview',{expected_revision:p.revision,route_id:p.routeId,watches,review_at:v.review_at||null});
    if(!same(p.caseId,p.epoch)||pending!==p||!f.isConnected)return;p.preview=data;drawSelection(data);return;
   }
   if(f.dataset.courseForm==='select'){
    const data=p.preview;if(!data)throw new Error('Preview this choice first.');
    await io.api(base+'/select',{event_id:courseId(),expected_revision:p.revision,expected_sequence:data.sequence,
      route_id:p.routeId,as_of:data.preview.as_of,preview_sha256:data.preview.preview_sha256,
      watches:data.preview.anchor.watches,review_at:data.preview.anchor.review_at,rationale:v.rationale,
      assumptions:v.assumptions.split('\n').map(x=>x.trim()).filter(Boolean),
      replaces_course_id:data.current_id,acknowledge_limits:fd.has('acknowledge')});
   }else if(f.dataset.courseForm==='event'){
    const a=p.course.assessment;
    await io.api(base+'/events',{event_id:courseId(),expected_revision:p.revision,expected_sequence:p.sequence,
      course_id:p.course.id,operation:p.operation,rationale:v.rationale,assessment_as_of:a.as_of,assessment_sha256:a.assessment_sha256});
   }
   if(!same(p.caseId,p.epoch)||pending!==p)return;
   await loadCourse(io.api);if(!same(p.caseId,p.epoch))return;
   closeModal();pending=null;io.render();toast('Course judgement recorded. Facts and action approvals are unchanged.');
  }catch(error){toast(error.message,true);}finally{if(button.isConnected)button.disabled=false;}
 });
}
