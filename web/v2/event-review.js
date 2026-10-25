import {S,esc,warning,note,modal,closeModal,toast} from './ui.js';
import {studioPage,studioClick,studioChange} from './studio-view.js';
import {createStudioDraft,studioDirty} from './studio-model.js';

const params=new URLSearchParams(location.search),caseId=params.get('case'),workId=params.get('work');
const validLink=[caseId,workId].every(v=>typeof v==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(v));
const base=`/api/v2/cases/${encodeURIComponent(caseId)}`,work=`${base}/event-work/${encodeURIComponent(workId)}`;
let token='',epoch=0,view=null,loading=false,rationale='',uncertain=false,notice=null,message='';
const button=(label,action)=>`<button type="button" class="button" data-event-action="${action}">${label}</button>`;
const editable=()=>view?.reviewable&&view?.can_review&&!uncertain;
function render(){
 const title=S.current?.case.title??'Review incoming change';
 let content;
 if(!validLink)content=warning('This review link is incomplete. Open the case review link supplied by your workspace.');
 else if(!token)content=`<section class="panel review-login"><h2>Open your review</h2><p class="body-copy">Use the account access token supplied for this review. Account sign-in is not connected in this development build.</p><form id="review-login"><label class="field"><span>Account access token</span><input name="token" type="password" required autocomplete="off" spellcheck="false"></label><button class="button primary" type="submit">Open review</button></form>${message?warning(message):''}</section>`;
 else if(loading)content='<p role="status">Loading the original source and current case…</p>';
 else if(!view)content=warning(message||'This review could not be opened.')+button('Try again','refresh');
 else content=`<p class="note">${esc(S.current.case.desired_outcome)}</p><div class="review-status" role="status">${esc(message|| (view.state==='committed'?'Review committed. The original source and processing output remain preserved.':!view.reviewable?'This result cannot be committed: its case revision or processing state has changed.':!view.can_review?'Read-only access. You can inspect the original material; write permission is required to amend the case.':'Pending review · Nothing has changed in the case.'))}</div>
 <div class="review-originals"><section class="panel"><h2>Original source</h2><p class="note">Source ${esc(view.source_receipt.event.source_id)} · Version ${esc(view.source_receipt.event.source_version)}</p><div class="review-text" tabindex="0" aria-label="Original source">${esc(view.source_receipt.event.text)}</div></section><section class="panel"><h2>Original processing output</h2><p class="note">Unreviewed suggestion. Reading it does not establish facts or approve actions.</p><div class="review-text" tabindex="0" aria-label="Original processing output">${esc(view.original_result??'No processing output has been retained.')}</div></section></div>
 ${view.state!=='committed'?`<p class="body-copy">The editor starts from the current case graph. Make only the amendments you have checked against the source and suggestion. Preview the effects before committing.</p><fieldset class="review-editor" ${editable()?'':'disabled'}><legend class="sr-only">Reviewed graph amendment</legend><label class="field review-reason"><span>Why is this amendment justified?</span><textarea id="review-rationale" minlength="10" maxlength="2000" rows="3">${esc(rationale)}</textarea></label>${studioPage({showLiveReview:false})}</fieldset>`:''}
 <section class="panel review-notices"><h2>Change notices</h2>${button('Check change notices','notice-pull')}${notice?`<p>Case revision ${notice.revision} has a recorded reviewed amendment.</p>${button('Acknowledge receipt','notice-ack')}<p class="note">Acknowledges delivery only. No case action is approved.</p>`:''}</section>`;
 document.querySelector('#app').innerHTML=`<main id="main"><header class="review-header"><div><span class="kicker">8BALL / INCOMING CHANGE</span><h1 tabindex="-1">${esc(title)}</h1></div><div class="toolbar">${token?button('Refresh review','refresh')+button('Lock review','lock'):''}</div></header>${content}</main>`;
}
function lock(reason=''){epoch++;token='';view=null;S.current=null;S.studio=null;rationale='';notice=null;loading=false;uncertain=false;message=reason;closeModal();render();}
async function api(path,body){
 const generation=epoch;
 const response=await fetch(path,{method:body===undefined?'GET':'POST',headers:{Authorization:'Bearer '+token,...(body===undefined?{}:{'Content-Type':'application/json'})},...(body===undefined?{}:{body:JSON.stringify(body)})});
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
render();
