import {esc,field,select,textarea,warning,note,pretty,date} from './ui.js';

const action=(label,id)=>`<button type="button" class="button" data-pr-action="challenge-${id}">${label}</button>`;
const referenceOptions=refs=>[['','Select an inspected case reference'],...refs.map(r=>[r.id,`${r.kind}: ${r.title}`])];
const assumptions=[['','Select a declared assumption'],...[1,2,3,4].map(i=>[`a${i}`,`Perspective ${i} assumption`])];

export function challengeReview(values,brief){
 const draft=structuredClone(brief.draft);
 draft.dispositions=draft.contributions.flatMap(c=>values[`status_${c.id}`]?[{
  contribution_id:c.id,status:values[`status_${c.id}`],rationale:values[`rationale_${c.id}`]??''
 }]:[]);
 draft.operator_decision=values.outcome?{outcome:values.outcome,rationale:values.reason??'',
  contribution_ids:draft.contributions.filter(c=>values[`ack_${c.id}`]==='on').map(c=>c.id)}:null;
 return draft;
}

function dispositionView(brief,saved,values){
 const draft=brief.draft,decision=draft.operator_decision;
 const summary=`<h3>Operator disposition · not approval</h3>${decision?`<p><strong>${esc(pretty(decision.outcome))}</strong>: ${esc(decision.rationale)}</p><p>Explicitly considered: ${decision.contribution_ids.map(esc).join(', ')||'none'}</p>`:note('No operator decision supplied. Silence is not agreement.')}<p class="note">These labels concern review only. They do not verify a claim, choose a course or approve an action. Original objections remain in the brief.</p>`;
 if(saved)return summary+note('Saved dispositions are immutable. Recheck a saved brief to append a new review.');
 return summary+`<form data-pr-form="challenge-disposition">${draft.contributions.map(c=>{
  const d=draft.dispositions.find(x=>x.contribution_id===c.id);
  return `<fieldset class="pr-rubric"><legend>${esc(c.id)} · ${esc(pretty(c.kind))}</legend><blockquote>${esc(c.text)}</blockquote>${select('Operator review status',`status_${c.id}`,[['','No disposition supplied'],['open','Open'],['addressed_in_review','Addressed in review — not verified'],['retained_concern','Concern retained'],['deferred','Deferred']],values?.[`status_${c.id}`]??d?.status??'')}${textarea('Reason for this disposition',`rationale_${c.id}`,values?.[`rationale_${c.id}`]??d?.rationale??'','maxlength="1500"')}<label><input type="checkbox" name="ack_${esc(c.id)}" ${(values?values[`ack_${c.id}`]==='on':decision?.contribution_ids.includes(c.id))?'checked':''}> Explicitly considered in my next-review decision</label></fieldset>`;
 }).join('')}${select('Next-review decision','outcome',[['','Undecided'],['continue_review','Continue review with acknowledged objections'],['seek_information','Seek information'],['reconsider','Reconsider'],['defer','Defer']],values?.outcome??decision?.outcome??'')}${textarea('Why this next-review decision?','reason',values?.reason??decision?.rationale??'','maxlength="1500"')}<button type="submit" class="button">Preview operator disposition</button></form>`;
}

export function challengeDraft(values,revision,runId){
 const perspectives=[],contributions=[],branches=[];
 for(let i=1;i<=4;i++){
  const v=k=>values[`r${i}_${k}`]??'';
  if(!['label','objective','boundary','reference','assumption','objection','question','verification','counter','kind'].some(k=>v(k)))continue;
  perspectives.push({id:`r${i}`,label:v('label'),kind:v('kind'),objective:v('objective'),information_boundary:v('boundary'),permitted_references:[v('reference')]});
  for(const [kind,prefix] of [['assumption','a'],['objection','o'],['question','q']])if(v(kind))contributions.push({id:`${prefix}${i}`,role_id:`r${i}`,kind,text:v(kind),references:[v('reference')],counters:kind==='objection'&&v('counter')?[v('counter')]:[],verification_needed:v('verification'),origin:'operator_declared'});
 }
 for(let i=1;i<=3;i++){
  const v=k=>values[`b${i}_${k}`]??'';
  if(!['title','rationale','assumption','condition','truth','action','budget'].some(k=>v(k)))continue;
  const scenario={expected_revision:revision};
  if(v('condition')){if(!['true','false'].includes(v('truth')))throw new Error('Choose an explicit true or false assumption.');scenario.conditions={[v('condition')]:v('truth')==='true'};}
  else if(v('truth'))throw new Error('Select the condition for that hypothetical value.');
  if(v('action'))scenario.unavailable_actions=[v('action')];
  if(v('budget')!=='')scenario.budget=Number(v('budget'));
  branches.push({id:`b${i}`,title:v('title'),rationale:v('rationale'),assumption_ids:[v('assumption')],scenario});
 }
 return {run_id:runId,expected_revision:revision,perspectives,contributions,branches,predecessor_sha256:null};
}

function editor(session,refs){
 const c=session.case,values=session.challengeValues??{},v=k=>values[k]??'';
 return `<form data-pr-form="challenge"><p class="note">Optional: up to four fictional/archetype perspectives, twelve statements and three explicit branches. Empty sections stay absent. No model fills them in.</p>${[1,2,3,4].map(i=>`<details class="pr-rubric" ${i===1?'open':''}><summary>Perspective ${i}${v(`r${i}_label`)?' · '+esc(v(`r${i}_label`)):''}</summary><div class="form-grid">${field('Declared label',`r${i}_label`,v(`r${i}_label`),'text','maxlength="180"')}${select('Perspective type',`r${i}_kind`,[['','Choose explicitly'],['fictional','Fictional'],['archetype','Archetype']],v(`r${i}_kind`))}</div>${textarea('Declared objective',`r${i}_objective`,v(`r${i}_objective`),'maxlength="1500"')}${textarea('Information boundary / what is not known',`r${i}_boundary`,v(`r${i}_boundary`),'maxlength="1500"')}${select('Inspected reference available to this perspective',`r${i}_reference`,referenceOptions(refs),v(`r${i}_reference`))}${textarea('Assumption (optional)',`r${i}_assumption`,v(`r${i}_assumption`),'maxlength="1500"')}${textarea('Objection (optional, retained without a majority vote)',`r${i}_objection`,v(`r${i}_objection`),'maxlength="1500"')}${select('Objection counters (optional)',`r${i}_counter`,[['','No specific counter-link'],...assumptions.slice(1)],v(`r${i}_counter`))}${textarea('Question (optional; not added to the case)',`r${i}_question`,v(`r${i}_question`),'maxlength="1500"')}${textarea('Evidence needed to verify/reconsider these statements',`r${i}_verification`,v(`r${i}_verification`),'maxlength="1500"')}</details>`).join('')}
 <h3>Explicit hypothetical branches</h3>${[1,2,3].map(i=>`<details class="pr-rubric" ${i===1?'open':''}><summary>Branch ${i}</summary>${field('Branch title',`b${i}_title`,v(`b${i}_title`),'text','maxlength="180"')}${textarea('Why compare this branch?',`b${i}_rationale`,v(`b${i}_rationale`),'maxlength="1500"')}${select('Linked assumption',`b${i}_assumption`,assumptions,v(`b${i}_assumption`))}<div class="form-grid">${select('Hypothetical condition (optional)',`b${i}_condition`,[['','No condition overlay'],...c.graph.conditions.map(x=>[x.id,x.title])],v(`b${i}_condition`))}${select('Explicit hypothetical value',`b${i}_truth`,[['','No value'],['true','True, hypothetically'],['false','False, hypothetically']],v(`b${i}_truth`))}${select('Unavailable action (optional)',`b${i}_action`,[['','No action removed'],...c.graph.actions.filter(x=>x.enabled&&!c.completed.includes(x.id)).map(x=>[x.id,x.title])],v(`b${i}_action`))}${field('Alternative budget (GBP), optional',`b${i}_budget`,v(`b${i}_budget`),'number','min="0" max="100000000"')}</div></details>`).join('')}
 <button type="submit" class="button primary">Compare declared assumptions</button><p class="note">Prepare is read-only. A separate save records only this derived brief. Use Sources and Human review to inspect references; a label is not verification.</p></form>`;
}

function briefView(brief,saved,reviewValues){
 const base=brief.baseline.inspection.baseline;
 return `<section data-challenge-result><h3>Assumption challenge · revision ${brief.case_revision}</h3>${note(brief.notice)}<p>${esc(brief.coverage.state)} · ${brief.coverage.declared_perspectives} declared perspectives / ${brief.coverage.contributing_perspectives} with contributions · ${brief.coverage.unresolved_objections.length} unresolved objections · ${brief.coverage.unanswered_questions.length} unanswered questions</p>${note(brief.coverage.notice)}<div class="pr-trials"><section class="pr-trial"><span class="kicker">LIVE BASELINE</span><h3>${base.constraint_compatible} compatible / ${base.candidate_routes} returned routes</h3>${base.search_truncated?warning('Search bound reached; returned routes only.'):''}</section>${brief.branches.map(b=>`<section class="pr-trial"><span class="kicker">HYPOTHETICAL · NOT APPLIED</span><h3>${esc(brief.draft.branches.find(x=>x.id===b.id).title)}</h3><p>${b.result.constraint_compatible} compatible / ${b.result.candidate_routes} returned routes · change ${b.compatible_change}</p>${b.result.search_truncated?warning('Search bound reached; returned routes only.'):''}<details><summary>Declared overlay and route differences</summary><pre class="code">${esc(JSON.stringify({assumptions:brief.draft.branches.find(x=>x.id===b.id),result:b.result,manifest:b.manifest,manifest_sha256:b.manifest_sha256},null,2))}</pre></details></section>`).join('')}</div>${brief.draft.perspectives.map(p=>`<section class="pr-rubric"><h3>${esc(p.label)} · ${esc(p.kind)}</h3><p>${esc(p.objective)}</p><p>Information boundary: ${esc(p.information_boundary)}</p><small>Declared references: ${p.permitted_references.map(esc).join(' · ')}</small>${brief.draft.contributions.filter(c=>c.role_id===p.id).map(c=>`<article><h4>${esc(pretty(c.kind))} · ${esc(c.id)}</h4><p>${esc(c.text)}</p>${c.counters.length?`<p>Counter-position to ${c.counters.map(esc).join(', ')}</p>`:''}<p>Evidence needed: ${esc(c.verification_needed)}</p></article>`).join('')||note('No contribution supplied. Not agreement or refusal.')}</section>`).join('')}${dispositionView(brief,saved,reviewValues)}${brief.reconsideration?`<section><h3>Explicit reconsideration</h3><p>${esc(brief.reconsideration.notice)}</p><p>Changed references: ${brief.reconsideration.changed_references.map(esc).join(', ')||'None'}</p><p>Baseline calculation changed: ${brief.reconsideration.baseline_changed?'yes':'no'}. Time and case changes can both affect it.</p></section>`:''}<p>${saved?note('Derived brief saved. No case facts, course selection or permissions changed.'):action('Save this derived brief','save')}${action('New declaration','new')}</p><p class="note">Save and use the current-history packet controls to export after server verification. Questions remain suggestions. Open the existing Questions or Insights workflow separately; nothing here creates or answers one.</p></section>`;
}

export function challengeView(session,refs){
 const rows=session.challengeHistory?.records??[];
 return warning('Assumption challenge: operator-declared hypotheses, not a working model swarm or real-person response prediction. Local operator mode only.','neutral')+(session.challengeResult?briefView(session.challengeResult.brief,session.challengeSaved,session.challengeReviewValues):editor(session,refs))+`<h3>Saved derived briefs</h3>${action('Refresh challenge history','history')}<p class="note">Maximum 100 saved briefs per case; 128 KiB per brief. History is immutable and included in local case export. Human reviews remain separate.</p>${rows.slice().reverse().map(r=>historyEntry(r,refs)).join('')||note('No saved briefs.')}`;
}

function historyEntry(row,refs){
 const stale=row.case_changed||row.time_expired;
 return `<section class="pr-history"><h4>Brief ${row.sequence} · revision ${row.brief.case_revision}</h4>
 <p>${date(row.recorded_at)} · ${row.case_changed?'Historical: case changed':row.time_expired?'Calculation window elapsed':'Matches current case snapshot'}</p>
 <p>${row.brief.coverage.unresolved_objections.length} objections retained. ${row.brief.coverage.unanswered_questions.length} unanswered questions.</p>
 <button type="button" class="button" data-pr-action="challenge-recheck" data-brief-hash="${esc(row.brief.brief_sha256)}">Recheck these declarations against live case</button>
 ${stale?note('Recheck and save a current brief before generating a decision packet. Historical content remains in the local case audit.'):`<form data-pr-form="challenge-packet" data-brief-hash="${esc(row.brief.brief_sha256)}">
 <h5>Decision packet · current server checks required</h5>
 ${select('Packet content','mode',[['operator_review','Internal operator review'],['reference_index','Restricted reference index — no narrative']])}
 ${select('Reference for restricted index only','reference',referenceOptions(refs))}
 <p class="note">Internal review includes the saved brief and lineage pointers, not original documents or a complete audit. A restricted index contains only the selected reference ID/hash and packet metadata; all narrative is omitted. Neither grants permission to share. Downloaded copies cannot be remotely revoked.</p>
 <button type="submit" class="button">Generate decision packet</button></form>`}</section>`;
}
