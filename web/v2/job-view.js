import {S,esc,pretty,badge,note,button,date,toast} from './ui.js';
let analysisPollTimer=null,analysisPollGeneration=0;
const jobActive=j=>['queued','running'].includes(j.status)||j.worker_active;
const stageLabels={queued:'Queued for the local worker',preparing_context:'Checking the selected context',provider_request:'Waiting for a provider response',reading_response:'Reading the response',validating_response:'Validating a stage response',validating_proposal:'Validating the complete proposal',succeeded:'Ready for human review',failed:'Stopped before review',cancelled:'Cancelled',superseded:'Case changed; result discarded',interrupted:'Interrupted by server restart'};
export function analysisMonitor(jobs=S.analysisJobs??[]) {
  if(!jobs.length)return '';
  return `<section class="panel analysis-monitor"><header class="panel-head"><div><span class="kicker">ANALYSIS MONITOR</span><h2>Visible work. Explicit control.</h2></div><small>${jobs.filter(jobActive).length} active</small></header>${jobs.slice(0,8).map(j=>`<article class="analysis-job" data-job-id="${esc(j.id)}"><div class="analysis-stage"><span class="job-signal ${jobActive(j)?'working':''}"></span><div><h3>${esc(stageLabels[j.stage]??pretty(j.stage))}</h3><p>${esc(j.provider)} · ${esc(j.purpose)} · based on revision ${j.base_revision}</p></div>${badge(j.status)}</div><div class="analysis-metadata"><span>${j.calls_completed}/${j.calls_started} started provider calls returned</span><span>Requested ${date(j.created_at)}</span></div><p class="note">${esc(j.message)}</p>${j.worker_active&&['cancelled','superseded'].includes(j.status)?note('An in-flight call is draining. No further stage or proposal publication is allowed.'):''}${['queued','running'].includes(j.status)?`<div class="toolbar">${button('Cancel analysis','cancel-analysis',false,`data-id="${esc(j.id)}"`)}</div>`:''}</article>`).join('')}</section><div class="spacer"></div>`;
}
export function stopAnalysisPolling(){analysisPollGeneration++;clearTimeout(analysisPollTimer);analysisPollTimer=null;S.analysisJobs=[];}
export async function updateAnalysisMonitor(services,{repeat=true}={}) {
  const caseId=S.current?.case.id,epoch=S.epoch,generation=++analysisPollGeneration;
  clearTimeout(analysisPollTimer);
  if(!caseId)return;
  async function tick(){
    if(generation!==analysisPollGeneration||epoch!==S.epoch||caseId!==S.current?.case.id)return;
    try {
      const jobs=await services.api(`/cases/${caseId}/analysis-jobs`);
      if(generation!==analysisPollGeneration||epoch!==S.epoch||caseId!==S.current?.case.id)return;
      const old=S.analysisJobs??[];const significant=JSON.stringify(jobs.map(j=>[j.id,j.status,j.stage,j.worker_active]))!==JSON.stringify(old.map(j=>[j.id,j.status,j.stage,j.worker_active]));
      S.analysisJobs=jobs;
      if(significant) {
        const proposals=await services.api(`/cases/${caseId}/proposals`);
        if(generation!==analysisPollGeneration||epoch!==S.epoch||caseId!==S.current?.case.id)return;
        S.proposals=proposals;
        const edited=document.querySelector('form[data-form="review-proposal"][data-dirty="true"]');
        if(['review','models'].includes(S.tab)&&!document.querySelector('.dialog')&&!edited)services.render();
        else {const target=document.querySelector('#analysis-monitor');if(target)target.innerHTML=analysisMonitor();}
      } else {const target=document.querySelector('#analysis-monitor');if(target)target.innerHTML=analysisMonitor();}
      if(repeat&&jobs.some(jobActive))analysisPollTimer=setTimeout(tick,750);
    } catch(err) {if(epoch===S.epoch&&generation===analysisPollGeneration)toast('Could not refresh analysis status. Use Refresh before starting another request.',true);}
  }
  await tick();
}
