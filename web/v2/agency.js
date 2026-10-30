import {mountIdentity} from './identity-access.js';
import {mountVault} from './vault-panel.js';
import {mountCollaboration,mountClientProjection} from './collaboration-view.js';
import {mountKnowledge} from './intelligence-knowledge.js';

const $=id=>document.getElementById(id);
let epoch=0,context=null,caseId='',disposers=[];
let disposeKnowledge=()=>{};
const tell=text=>{$('context-status').textContent=text;};
function clear(){epoch++;for(const dispose of disposers)dispose();disposers=[];disposeKnowledge();context=null;caseId='';$('case-panels').hidden=true;for(const id of ['pack-results','event-results','operations-results','knowledge-exact-result','collaboration','client-projection','vault'])$(id).replaceChildren();}
async function request(path,body,{responseType='json'}={}){
 const current=epoch;
 const response=await fetch(path,{credentials:'same-origin',cache:'no-store',...(body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})});
 if(current!==epoch)throw new Error('Case context changed. Reload the current case.');
 if(response.status===401||response.status===403){clear();throw new Error('Access unavailable or revoked. Private views cleared. Sign in and reopen the case.');}
 if(!response.ok)throw new Error('Request denied or state changed. Refresh and review before retrying.');
 return responseType==='blob'?response.blob():response.json();
}
const api=(path,body)=>request('/api/v2'+path,body);
const base=()=>`/cases/${encodeURIComponent(caseId)}`;
const output=(id,value)=>{$(id).textContent=JSON.stringify(value,null,2);};
function form(id,action){$(id).addEventListener('submit',async event=>{event.preventDefault();const current=epoch;const button=event.submitter;if(button)button.disabled=true;try{await action(Object.fromEntries(new FormData(event.target)),event.submitter);if(current===epoch)tell('Request completed. Review state, evidence and permissions remain distinct.');}catch(error){tell(error.message);}finally{if(button)button.disabled=false;}});}
function click(id,action){$(id).addEventListener('click',async()=>{try{await action();}catch(error){tell(error.message);}});}
clear();
mountIdentity($('identity'));
$('identity').addEventListener('click',()=>{clear();tell('Identity interaction cleared private views. Reopen your exact case after sign-in.');});
click('clear-context',()=>{clear();tell('Case context cleared.');});
form('case-context',async values=>{
 clear();caseId=values.case_id;
 context=await api(base()+'/agency-context');
 $('case-panels').hidden=false;
 const vaultPanel=mountVault($('vault'),{caseId,request:(path,options={})=>request(path,options.body,{responseType:options.responseType})});
 disposers.push(()=>vaultPanel.dispose());
 mountLibrary();
});
function mountLibrary(){
 disposeKnowledge();
 const prefix=base()+'/knowledge';
 disposeKnowledge=mountKnowledge($('knowledge'),{
  search:(query)=>api(prefix+'?q='+encodeURIComponent(query)),
  read:(item,{history=false}={})=>api(prefix+'/'+encodeURIComponent(item)+'?history='+history),
  write:(item,body)=>api(prefix+'/'+encodeURIComponent(item),body)
 });
}
form('object-context',async values=>{
 const objectId=values.object_id;
 const binding=await api(base()+'/agency-objects/'+encodeURIComponent(objectId));
 disposers.push(mountCollaboration($('collaboration'),{api,caseId,objectId,binding}));
});
form('client-context',async values=>{clear();caseId=values.case_id;disposers.push(mountClientProjection($('client-projection'),{api,caseId,objectId:values.object_id,projectionId:values.projection_id}));});
form('knowledge-write',async values=>{await api(base()+'/knowledge/'+encodeURIComponent(values.item_id),JSON.parse(values.body));mountLibrary();});
form('knowledge-exact',async values=>output('knowledge-exact-result',await api(base()+'/knowledge/'+encodeURIComponent(values.item_id)+'?history=true')));
click('packs',async()=>output('pack-results',await api(base()+'/domain-packs')));
form('pack-preview',async values=>output('pack-results',await api(base()+'/domain-packs/'+encodeURIComponent(values.pack)+'/preview',JSON.parse(values.body))));
form('incoming',async values=>output('event-results',await api(base()+'/incoming-events',JSON.parse(values.body))));
form('processing-review',async values=>output('event-results',await api(base()+`/incoming-events/${Number(values.sequence)}/processing-review`,{expected_revision:context.case_revision,receipt_sha256:values.receipt_sha256,rationale:values.rationale})));
form('enqueue',async values=>output('event-results',await api(base()+'/event-attempts',{sequence:Number(values.sequence),review_id:values.review_id,expected_revision:context.case_revision,request_id:crypto.randomUUID()})));
form('work-status',async(values,button)=>{
 output('event-results',await api(base()+`/event-work/${encodeURIComponent(values.work_id)}/${button?.name==='cancel'?'cancel':'dispatch-status'}`,button?.name==='cancel'?{}:undefined));
 if(button?.name!=='cancel'){
  const link=document.createElement('a');link.href='/v2/event-review.html?'+new URLSearchParams({case:caseId,work:values.work_id,session:'1'});link.textContent='Open explicit source/result/graph review using current session';$('event-results').append(document.createElement('br'),link);
 }
});
form('revoke-processing',async values=>output('event-results',await api(base()+`/processing-reviews/${encodeURIComponent(values.review_id)}/revoke`,{})));
const operations=()=>`/organisations/${encodeURIComponent(context.scope.organisation_id)}/matters/${encodeURIComponent(context.scope.matter_id)}${base()}/operations`;
click('operations-refresh',async()=>output('operations-results',await api(operations())));
form('operations-open',async values=>{if(!values.target_id)delete values.target_id;output('operations-results',await api(operations(),{...values,request_id:crypto.randomUUID()}));});
form('operations-transition',async(values,button)=>output('operations-results',await api(operations()+`/${encodeURIComponent(values.record_id)}/${button?.name==='verify'?'verify-revocation':'transition'}`,{request_id:crypto.randomUUID(),expected_revision:Number(values.expected_revision),...(button?.name==='verify'?{}:{state:values.state})})));
document.addEventListener('visibilitychange',()=>{if(document.hidden){clear();tell('Private views cleared while this page was hidden. Reopen the exact case.');}});
window.addEventListener('pagehide',clear);
try{const status=await request('/api/v2/agency-status');$('configuration').textContent=status.configured?`Explicit engineering host. Keys: ${status.keys_configured?'configured':'missing'}. Scanner: ${status.scanner_configured?'configured':'missing'}. Source policy: ${status.source_policy_configured?'configured':'missing'}. Missing adapters deny. Production acceptance remains open.`:'Agency services are not configured. Local operator mode remains available; its token cannot unlock agency services.';}catch(error){tell(error.message);}
