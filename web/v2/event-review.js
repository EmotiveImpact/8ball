import {S,esc,warning,note,modal,closeModal,toast} from './ui.js';
import {studioPage,studioClick,studioChange} from './studio-view.js';
import {createStudioDraft,studioDirty} from './studio-model.js';

const params=new URLSearchParams(location.search),caseId=params.get('case'),workId=params.get('work');
const sessionMode=params.get('session')==='1';
const validLink=[caseId,workId].every(v=>typeof v==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(v));
const base=`/api/v2/cases/${encodeURIComponent(caseId)}`,work=`${base}/event-work/${encodeURIComponent(workId)}`;
let token='',epoch=0,view=null,loading=false,rationale='',uncertain=false,notice=null,message='';
const button=(label,action)=>`<button type="button" class="button" data-event-action="${action}">${label}</button>`;
const editable=()=>view?.reviewable&&view?.can_review&&!uncertain;
function specialistComparison(){
 const r=view?.specialist_review;
 if(!r)return '';
 if(!r.available)return warning('Specialist comparison could not be validated against the retained answers and source. No comparison is interpreted; inspect the original output below.');
 const names={'jev-latest':'Jev','clef-flash':'Clef Flash','gpt-6-luna-decisions':'GPT-6 Luna Decisions'},name=m=>names[m]??m;
 const stops={completed:'The processing attempt finished.',time_budget:'The processing time budget stopped further requests.',setup_or_provider_failed:'Setup or a provider request failed; no automatic retry was made.',unknown_reported_cost:'Reported cost is unknown; further requests were stopped.',reported_cost_budget:'The reported-cost threshold stopped further requests.'};
 const questions=r.questions.map(q=>{
  const spec=r.spec.questions.find(s=>s.id===q.id),coverage=q.disagreement?'Different answers — unresolved.':!r.answered_models?'No validated answers.':q.missing_models.length?'Some answers are missing; do not infer agreement.':r.requested_models===1?'One model only — not independent confirmation.':'Returned choices match — not independent confirmation.';
  return `<section class="specialist-question"><h3>Question: ${esc(q.id)}</h3><p>${esc(spec.instructions)}</p><p class="note">${esc(coverage)}</p><ul class="specialist-answers">${r.spec.models.map(model=>{
   const attempt=r.attempts.find(a=>a.model===model),choice=q.choices[model];
   return `<li><h4>${esc(name(model))}</h4>${choice!==undefined?`<p>Choice: <strong>${esc(choice)}</strong></p><p>${esc(spec.criteria[choice])}</p>`:`<p><strong>No validated answer</strong></p><p>${attempt?.status==='failed'?'The attempt failed.':'Not started.'}</p>`}</li>`;
  }).join('')}</ul></section>`;
 }).join('');
 return `<section class="panel specialist-comparison" aria-labelledby="specialist-title"><h2 id="specialist-title">Specialist comparison</h2><p class="note">Advisory only. These are model choices, not votes, evidence, approval or predictions. No answer is applied to the case.</p><p>${r.answered_models} of ${r.requested_models} selected models answered. ${esc(stops[r.stop_reason])}</p><p class="note">${r.base_revision===view.current_revision?'Retained for':'Historical comparison for'} case revision ${r.base_revision}; current revision ${view.current_revision}.</p>${questions}<details><summary>Request, cost and provenance details</summary><p>Known provider-reported cost: USD ${esc(r.known_reported_cost_usd)}. Actual provider billing is not verified; this is not a billing cap.</p>${r.unknown_cost_attempts.length?`<p>Unknown reported cost: ${esc(r.unknown_cost_attempts.map(name).join(', '))}. Unknown does not mean free.</p>`:''}${r.not_started_models.length?`<p>No request recorded for: ${esc(r.not_started_models.map(name).join(', '))}.</p>`:''}<p>Confidence and choice distributions in the original output are not calibrated outcome probabilities. These integrity hashes are not independent provider attestations.</p><dl class="specialist-provenance"><dt>Reviewed input SHA256</dt><dd>${esc(r.input_sha256)}</dd><dt>Configuration SHA256</dt><dd>${esc(r.spec_sha256)}</dd></dl>${r.attempts.map(a=>`<h3>${esc(name(a.model))} request</h3><p>${a.request_started?'Request recorded.':'No request recorded.'} Provider-reported served model: ${esc(a.served_model??'Unavailable')}. ${a.status==='answered'? `${esc(a.usage.input_tokens)} input tokens; ${esc(a.usage.output_tokens)} output tokens.`:'Token usage unavailable.'}</p><dl class="specialist-provenance"><dt>Request SHA256</dt><dd>${esc(a.request_sha256??'Unavailable')}</dd><dt>Response SHA256</dt><dd>${esc(a.response_sha256??'Unavailable')}</dd></dl>`).join('')}</details></section>`;
}
function render(){
 const title=S.current?.case.title??'Review incoming change';
 let content;
 if(!validLink)content=warning('This review link is incomplete. Open the case review link supplied by your workspace.');
 else if(!token)content=`<section class="panel review-login"><h2>Open your review</h2>${sessionMode?`<p class="body-copy">Sign in through the <a href="/v2/agency.html">agency desk</a>, then explicitly open this exact review using your current session.</p>${button('Open current session review','session-open')}`:`<p class="body-copy">Use the account access token supplied for this review. Account sign-in is not connected in this development build.</p><form id="review-login"><label class="field"><span>Account access token</span><input name="token" type="password" required autocomplete="off" spellcheck="false"></label><button class="button primary" type="submit">Open review</button></form>`}${message?warning(message):''}</section>`;
 else if(loading)content='<p role="status">Loading the original source and current case…</p>';
 else if(!view)content=warning(message||'This review could not be opened.')+button('Try again','refresh');
 else content=`<p class="note">${esc(S.current.case.desired_outcome)}</p><div class="review-status" role="status">${esc(message|| (view.state==='committed'?'Review committed. The original source and processing output remain preserved.':!view.reviewable?'This result cannot be committed: its case revision or processing state has changed.':!view.can_review?'Read-only access. You can inspect the original material; write permission is required to amend the case.':'Pending review · Nothing has changed in the case.'))}</div>
 ${view.source_receipt?specialistComparison():''}
 ${view.source_receipt?`<div class="review-originals"><section class="panel"><h2>Original source</h2><p class="note">Source ${esc(view.source_receipt.event.source_id)} · Version ${esc(view.source_receipt.event.source_version)}</p><div class="review-text" tabindex="0" aria-label="Original source">${esc(view.source_receipt.event.text)}</div></section><section class="panel"><h2>Original processing output</h2><p class="note">Unreviewed suggestion. Reading it does not establish facts or approve actions.</p><div class="review-text" tabindex="0" aria-label="Original processing output">${esc(view.original_result??'No processing output has been retained.')}</div></section></div>`:warning('Source processing review is no longer current. Original material and output are withheld; refresh current authority before continuing.')}
 ${view.state!=='committed'?`<p class="body-copy">The editor starts from the current case graph. Make only the amendments you have checked against the source and suggestion. Preview the effects before committing.</p><fieldset class="review-editor" ${editable()?'':'disabled'}><legend class="sr-only">Reviewed graph amendment</legend><label class="field review-reason"><span>Why is this amendment justified?</span><textarea id="review-rationale" minlength="10" maxlength="2000" rows="3">${esc(rationale)}</textarea></label>${studioPage({showLiveReview:false})}</fieldset>`:''}
 <section class="panel review-notices"><h2>Change notices</h2>${button('Check change notices','notice-pull')}${notice?`<p>Case revision ${notice.revision} has a recorded reviewed amendment.</p>${button('Acknowledge receipt','notice-ack')}<p class="note">Acknowledges delivery only. No case action is approved.</p>`:''}</section>`;
 document.querySelector('#app').innerHTML=`<main id="main"><header class="review-header"><div><span class="kicker">8BALL / INCOMING CHANGE</span><h1 tabindex="-1">${esc(title)}</h1></div><div class="toolbar">${token?button('Refresh review','refresh')+button('Lock review','lock'):''}</div></header>${content}</main>`;
}
function lock(reason=''){epoch++;token='';view=null;S.current=null;S.studio=null;rationale='';notice=null;loading=false;uncertain=false;message=reason;closeModal();render();}
async function api(path,body){
 const generation=epoch;
 const response=await fetch(path,{credentials:'same-origin',method:body===undefined?'GET':'POST',headers:{...(sessionMode?{}:{Authorization:'Bearer '+token}),...(body===undefined?{}:{'Content-Type':'application/json'})},...(body===undefined?{}:{body:JSON.stringify(body)})});
 if(generation!==epoch)throw new Error('Review session changed.');
 if(response.status===401||response.status===403){lock('Access is no longer available. Reopen with a currently authorised account.');throw new Error('Access is not permitted.');}
 const result=await response.json();
 if(generation!==epoch)throw new Error('Review session changed.');
 if(!response.ok){const error=new Error(typeof result.detail==='string'?result.detail:'The request was rejected.');error.status=response.status;throw error;}
 return result;
}
async function load(){
 const generation=++epoch;loading=true;message='';render();
 try{
  const [current,result]=await Promise.all([api(base),api(work)]);
  if(generation!==epoch)return;
  if(current.case.revision!==result.current_revision)throw new Error('The case changed while loading. Refresh to inspect a consistent revision.');
  S.current=current;S.studio=createStudioDraft(current.case);view=result;rationale='';uncertain=false;notice=null;
 }catch(error){if(generation===epoch){view=null;S.current=null;S.studio=null;message=error.message;}}
 finally{if(generation===epoch){loading=false;render();document.querySelector('h1')?.focus();}}
}
const services={render,api:async(path,body)=>{
 if(path!==`/cases/${caseId}/graph/preview`)throw new Error('Unsupported review operation.');
 try{return await api(work+'/preview',body);}catch(error){if(view&&error.status===409){view.reviewable=false;message='This review is stale. Refresh before making another amendment.';}throw error;}
},commit:async(kind,payload,context)=>{
 if(!editable()||kind!=='replace_graph'||context.caseId!==caseId)throw new Error('This review cannot commit a case amendment.');
 if(rationale.trim().length<10)throw new Error('Explain why this amendment is justified (at least 10 characters).');
 const generation=epoch;
 try{
  const record=await api(work+'/review',{command:{event_id:crypto.randomUUID(),expected_revision:context.revision,kind,payload},rationale});
  if(generation!==epoch)return;
  closeModal();view.state='committed';view.reviewable=false;message=`Reviewed amendment committed at case revision ${record.committed_revision}. No facts or action approvals were created.`;
  render();document.querySelector('h1')?.focus();
 }catch(error){
  if(generation===epoch&&token){uncertain=true;message=error.status===409?'The case or processing state changed. Refresh before trying again.':error.status===422?'The amendment was rejected. Refresh before starting a new draft.':'The save outcome is unknown. Refresh this review before trying again.';closeModal();render();}
  throw error;
 }
}};
document.addEventListener('submit',async event=>{
 if(event.target.id!=='review-login')return;event.preventDefault();token=new FormData(event.target).get('token').trim();event.target.reset();await load();
});
document.addEventListener('input',event=>{if(event.target.id==='review-rationale')rationale=event.target.value;});
document.addEventListener('change',event=>{
 if(!event.target.matches('[data-studio-field],[data-studio-list],[data-studio-search]'))return;
 try{if(!editable())throw new Error('This review is read-only.');studioChange(event.target,services);}catch(error){toast(error.message,true);}
});
document.addEventListener('click',async event=>{
 const el=event.target.closest('button');if(!el)return;
 try{
  if(el.dataset.action==='close'){closeModal();return;}
  if(el.dataset.studio){
   if(!editable())throw new Error('This review is read-only.');
   if(['commit','commit-confirm'].includes(el.dataset.studio)&&rationale.trim().length<10){document.querySelector('#review-rationale')?.focus();throw new Error('Explain why this amendment is justified before committing.');}
   await studioClick(el,services);return;
  }
  switch(el.dataset.eventAction){
   case'session-open':token='session';await load();break;
   case'lock':lock();break;
   case'refresh':if(S.studio&&studioDirty(S.studio)&&view?.state!=='committed'){modal('Refresh this review?',note('Refreshing discards your uncommitted edits and loads the current case.')+button('Discard edits and refresh','refresh-confirm'));}else await load();break;
   case'refresh-confirm':closeModal();await load();break;
   case'notice-pull':notice=await api(base+'/change-notices/pull',{});render();if(!notice)toast('No unacknowledged change notice for this case.');break;
   case'notice-ack':if(notice){await api(base+`/change-notices/${notice.id}/acknowledge`,{});notice=null;render();toast('Delivery acknowledged. No action was approved.');}break;
  }
 }catch(error){toast(error.message,true);}
});
document.addEventListener('keydown',event=>{
 if(event.key==='Escape'){closeModal();return;}
 const dialog=document.querySelector('.dialog');if(event.key!=='Tab'||!dialog)return;
 const nodes=[...dialog.querySelectorAll('button:not([disabled]),input,textarea,a')].filter(el=>el.getClientRects().length),first=nodes[0],last=nodes.at(-1);
 if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
 else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
});
window.addEventListener('beforeunload',event=>{if(S.studio&&studioDirty(S.studio)&&view?.state!=='committed'){event.preventDefault();event.returnValue='';}});
document.addEventListener('visibilitychange',()=>{if(sessionMode&&document.hidden)lock('Private review cleared while hidden. Reopen with your current session.');});
render();
