/* Isolated host mount. api(relativePath, body?) must use verified agency auth. */
const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const field=(name,label,type='text',value='')=>`<label>${escape(label)}<input name="${name}" type="${type}" value="${escape(value)}" required></label>`;
const content=view=>`<h3>${escape(view.title)}</h3><p class="collaboration-copy">${escape(view.summary)}</p><ul>${view.statements.map(item=>`<li><strong>${escape(item.evidence_state)}</strong>: ${escape(item.text)}</li>`).join('')}</ul>`;

export function mountCollaboration(root,{api,caseId,objectId,binding}){
 if(typeof api!=='function'||!caseId||!objectId||!binding)throw new Error('An authenticated host API and exact object binding are required.');
 const base=`/cases/${encodeURIComponent(caseId)}/collaboration`,objects=`${base}/objects/${encodeURIComponent(objectId)}`;
 let active=true,busy=false,uncertain=false,epoch=0,review=null,grants=[],message='Nothing is shared by creating a draft. Review is separate from permission to act.';
 const initialId=crypto.randomUUID();
 function render(){
  if(!active)return;
  root.innerHTML=`<section class="collaboration-panel"><h2>Specialists & client updates</h2><p role="status">${escape(message)}</p><p>Fictional local engineering. No secure portal, external send or action approval is implied.</p>
  <button type="button" data-collaboration="refresh" ${busy?'disabled':''}>Refresh grants / clear uncertain save</button>
  <fieldset ${busy||uncertain?'disabled':''}><legend>Revocable specialist or client access</legend><form data-collaboration-form="grant">
   ${field('id','Unique grant ID','text',initialId)}${field('issuer','Recipient identity issuer','url')}${field('subject','Recipient identity subject')}
   <label>Grant purpose<select name="purpose"><option value="expert">Expert: specific object</option><option value="expert_matter">Expert: whole matter</option><option value="client_projection">Client: exact projection only</option></select></label>
   <label>Projection ID (client grants only)<input name="projection_id"></label>
   ${field('valid_from','Valid from (ISO time with timezone)','text',new Date().toISOString())}${field('expires_at','Expires at (ISO time with timezone)')}
   <label>Why is this access needed?<textarea name="rationale" required minlength="10" maxlength="2000"></textarea></label><button>Create revocable grant</button></form>
   <ul>${grants.map(item=>`<li>${escape(item.request.id)} · ${escape(item.request.purpose)} · ${escape(item.request.recipient.subject)} · ${item.revoked?'Revoked':`Expires ${escape(item.request.expires_at)} <button type="button" data-collaboration="revoke" data-id="${escape(item.request.id)}">Revoke</button>`}</li>`).join('')}</ul></fieldset>
  <fieldset ${busy||uncertain?'disabled':''}><legend>Author a separate client projection</legend><p>Only this authored content can be reviewed for the client. No internal fields are copied. Case revision ${escape(binding.case_revision)} / object revision ${escape(binding.object_revision)}.</p>
   <form data-collaboration-form="draft">${field('id','Unique projection ID','text',initialId+'-projection')}${field('issuer','Client identity issuer','url')}${field('subject','Client identity subject')}${field('title','Client title')}
   <label>Client summary<textarea name="summary" required maxlength="6000"></textarea></label><button>Save unshared draft</button></form></fieldset>
  <fieldset ${busy||uncertain?'disabled':''}><legend>Inspect exact disclosure before review</legend><form data-collaboration-form="inspect">${field('projection_id','Projection ID')}<button>Inspect draft</button></form>
   ${review?`<article>${content(review.content)}<p>Recipient: ${escape(review.recipient.issuer)} / ${escape(review.recipient.subject)}. State: ${escape(review.state)}${review.stale?' · STALE':''}</p><p>Exact digest: <code>${escape(review.digest)}</code></p><p>Source revision, recipient and grant revocation are checked again on every client read. Review does not verify truth.</p>
    <form data-collaboration-form="review">${field('grant_id','Exact client grant ID')}<label>Review rationale<textarea name="rationale" required minlength="10" maxlength="2000"></textarea></label><label><input name="confirmed" type="checkbox" required> I reviewed this exact content for this recipient; I am not its author.</label><button ${review.state!=='draft'||review.stale?'disabled':''}>Record separate disclosure review</button></form>
    <button type="button" data-collaboration="withdraw" data-id="${escape(review.id)}" ${review.state==='withdrawn'?'disabled':''}>Withdraw projection locally</button></article>`:''}
  </fieldset></section>`;
 }
 async function action(operation,{mutation=false}={}){
  if(busy||!active)return;
  busy=true;const generation=++epoch;
  for(const button of root.querySelectorAll('button'))button.disabled=true;
  try{const result=await operation();if(!active||generation!==epoch)return;message=result||'Saved. No external send or action was approved.';}
  catch(error){if(!active||generation!==epoch)return;review=null;grants=[];uncertain=mutation;message=mutation?'The save outcome is unknown or rejected. Refresh before making another change; never blindly repeat a disclosure.':(error.message||'Access is unavailable.');}
  finally{if(active&&generation===epoch){busy=false;render();}}
 }
 async function submit(event){
  const form=event.target.closest('[data-collaboration-form]');if(!form||!root.contains(form))return;event.preventDefault();
  const values=Object.fromEntries(new FormData(form));const kind=form.dataset.collaborationForm;
  if(uncertain&&kind!=='inspect')return;
  await action(async()=>{
   switch(kind){
    case'grant':{
     const purpose=values.purpose==='expert_matter'?'expert':values.purpose;
     const request={...values,purpose,recipient:{issuer:values.issuer,subject:values.subject},object_id:values.purpose==='expert_matter'?null:objectId,projection_id:purpose==='client_projection'?values.projection_id:null};
     delete request.issuer;delete request.subject;
     const result=await api(base+'/grants',request);grants=[result,...grants.filter(item=>item.request.id!==result.request.id)];return `Grant ${result.request.id} recorded. Clients still require separate exact disclosure review.`;
    }
    case'draft':review=await api(objects+'/projections',{id:values.id,expected_binding:binding,recipient:{issuer:values.issuer,subject:values.subject},content:{title:values.title,summary:values.summary,statements:[]}});return `Draft ${review.id} saved without client access. A different authorised reviewer must inspect it.`;
    case'inspect':review=await api(objects+`/projections/${encodeURIComponent(values.projection_id)}/review`);return 'Inspect the exact client content and recipient. Stale drafts need a new ID and current host binding.';
    case'review':if(review&&values.confirmed){review=await api(objects+`/projections/${encodeURIComponent(review.id)}/review`,{expected_digest:review.digest,grant_id:values.grant_id,rationale:values.rationale});return 'Disclosure review recorded. Only the exact authorised client can pull this projection; nothing was sent.';}break;
   }
  },{mutation:kind!=='inspect'});
 }
 async function click(event){
  const button=event.target.closest('[data-collaboration]');if(!button||!root.contains(button))return;
  await action(async()=>{
   switch(button.dataset.collaboration){
    case'refresh':review=null;grants=[];grants=await api(base+'/grants');uncertain=false;return 'Current grants loaded. Refresh the host object before drafting against a newer revision.';
    case'revoke':await api(base+`/grants/${encodeURIComponent(button.dataset.id)}/revoke`,{});grants=grants.map(item=>item.request.id===button.dataset.id?{...item,revoked:true}:item);return 'Grant revoked. Prior responses cannot be recalled.';
    case'withdraw':await api(objects+`/projections/${encodeURIComponent(button.dataset.id)}/withdraw`,{});review=null;return 'Projection withdrawn locally. No external cancellation or recall is claimed.';
   }
  },{mutation:button.dataset.collaboration!=='refresh'});
 }
 root.addEventListener('submit',submit);root.addEventListener('click',click);render();
 return ()=>{active=false;epoch++;review=null;grants=[];root.removeEventListener('submit',submit);root.removeEventListener('click',click);root.replaceChildren();};
}

export function mountClientProjection(root,{api,caseId,objectId,projectionId}){
 if(typeof api!=='function'||![caseId,objectId,projectionId].every(value=>typeof value==='string'&&value))throw new Error('Exact authenticated projection context required.');
 let active=true,generation=0;
 const path=`/cases/${encodeURIComponent(caseId)}/collaboration/objects/${encodeURIComponent(objectId)}/projections/${encodeURIComponent(projectionId)}`;
 async function refresh(){
  const epoch=++generation;root.textContent='Checking current client access…';
  try{const view=await api(path);if(!active||epoch!==generation)return;root.innerHTML=`<section class="collaboration-panel"><h2>Reviewed client update</h2>${content(view.content)}<p>Reviewed ${escape(view.reviewed_at)}. This is a curated projection, not the internal case or permission to act.</p><button type="button">Refresh current access</button></section>`;}
  catch{if(active&&epoch===generation)root.innerHTML='<p role="alert">This reviewed update is unavailable. It may be unreviewed, stale, withdrawn or no longer authorised.</p><button type="button">Check access again</button>';}
 }
 const click=event=>{if(event.target.closest('button'))void refresh();};root.addEventListener('click',click);void refresh();
 return ()=>{active=false;generation++;root.removeEventListener('click',click);root.replaceChildren();};
}
