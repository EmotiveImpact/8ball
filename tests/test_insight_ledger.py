from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import json
import pytest
from fastapi.testclient import TestClient
from eightball.api import make_app
from eightball.store import Store as V1,Conflict
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.insights import Insights,Scan,ReviewInsight,Hypothesis,InsightQuestion,project
from eightball.v2.commands import Command
from eightball.models import uid,utcnow

@pytest.fixture
def setup(tmp_path):
 legacy=V1(str(tmp_path/'case.db'));s=Store(legacy.path);c=s.create(demo_case(),fixture=True)
 client=TestClient(make_app(legacy,'x'*32),headers={'Authorization':'Bearer '+'x'*32})
 return s,c,Insights(s),client

def ctx(c,v=None):return dict(event_id=uid(),expected_revision=c.revision,expected_insight_revision=v['insight_revision'] if v else 0)
def scan(c,i,v=None,**kw):return i.scan(c.id,Scan(**ctx(c,v),**kw))
def get(v,rule='shared_condition'):return next(x for x in v['items'] if x['insight']['rule']==rule)
def review(c,i,v,disposition='dismissed',row=None):
 x=(row or get(v))['insight'];return i.review(c.id,ReviewInsight(**ctx(c,v),insight_id=x['id'],fingerprint=x['fingerprint'],disposition=disposition,reason='Explicit operator rationale'))
def update(s,c,kind,payload):return s.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind=kind,payload=payload))[0]

def test_reads_are_non_mutating_and_old_export_unchanged(setup):
 s,c,i,cl=setup;before=s.audit(c.id)
 assert i.view(c.id)['items']==[]
 assert s.audit(c.id)==before and 'emergent_insights' not in before

def test_scan_and_review_preserve_entire_case_chain(setup):
 s,c,i,cl=setup;before=s.audit(c.id);v=scan(c,i);v=review(c,i,v)
 after=s.audit(c.id);assert after.pop('emergent_insights')['valid']
 assert after==before and s.get(c.id)==c and len(v['items'])>0

def test_dismissed_never_deleted_and_reopen_keeps_reason(setup):
 s,c,i,cl=setup;v=review(c,i,scan(c,i));row=get(v);assert row['review_status']=='dismissed'
 v=review(c,i,v,'unreviewed');row=get(v)
 assert row['review_status']=='unreviewed' and len(row['reviews'])==2

def test_unchanged_rescan_retains_review(setup):
 s,c,i,cl=setup;v=review(c,i,scan(c,i));x=get(v)['insight']['id'];v=scan(c,i,v)
 assert next(xr for xr in v['items'] if xr['insight']['id']==x)['review_status']=='dismissed'

def test_retraction_invalidates_scan_then_reopens_changed_finding(setup):
 s,c,i,cl=setup;v=scan(c,i);row=get(v,'single_source_cluster');v=review(c,i,v,row=row)
 c=update(s,c,'review_evidence',{'evidence_id':'e_preserve','status':'retracted'})
 stale=i.view(c.id);assert stale['scan_outdated'] and not any(r['can_review'] for r in stale['items'])
 with pytest.raises(Conflict):review(c,i,stale,row=row)
 v=scan(c,i,stale);history=next(x for x in v['items'] if x['insight']['id']==row['insight']['id'])
 assert not history['present'] and history['presence']=='not_reproduced' and history['reviews']

def test_changed_fingerprint_requires_fresh_review(setup):
 s,c,i,cl=setup;v=scan(c,i);row=get(v,'actor_concentration');v=review(c,i,v,row=row)
 actor=next(a for a in c.actors if any(r['kind']=='actor' and r['id']==a.id for r in row['insight']['references']))
 obj=actor.model_dump(mode='json');obj['stance']='Changed recorded position'
 c=update(s,c,'upsert_object',{'kind':'actor','object':obj});v=scan(c,i,i.view(c.id));new=next(r for r in v['items'] if r['insight']['id']==row['insight']['id'])
 assert new['review_status']=='unreviewed' and new['review_outdated']

def test_disappeared_reappeared_finding_not_silently_dismissed(setup):
 s,c,i,cl=setup;v=scan(c,i);row=get(v,'unknown_wait');aid=next(r['id'] for r in row['insight']['references'] if r['kind']=='action');v=review(c,i,v,row=row)
 original=next(a for a in c.graph.actions if a.id==aid).model_dump(mode='json')
 c=update(s,c,'upsert_object',{'kind':'action','object':{**original,'wait_minutes':30}});v=scan(c,i,i.view(c.id))
 assert not next(r for r in v['items'] if r['insight']['id']==row['insight']['id'])['present']
 c=update(s,c,'upsert_object',{'kind':'action','object':original});v=scan(c,i,i.view(c.id));new=next(r for r in v['items'] if r['insight']['id']==row['insight']['id'])
 assert new['review_status']=='unreviewed' and new['change']=='reappeared'

def test_policy_disabled_is_not_a_resolved_finding(setup):
 s,c,i,cl=setup
 # Exercise the projection without altering real case clocks.
 from eightball.v2.insights import verify_ledger,ledger_rows
 v=scan(c,i)
 with s.connection() as db:es=verify_ledger(ledger_rows(db,c.id),c.id)
 old=es[0]['body']['findings'][0];old['rule']='freshness_review'
 second=json.loads(json.dumps(es[0]));second['event_id']='second';second['body']['findings']=[];second['body']['rules_disabled']=['freshness_review']
 projected=project([es[0],second],c.revision,utcnow());row=next(r for r in projected['items'] if r['insight']['id']==old['id'])
 assert row['presence']=='not_evaluated' and row['review_status']=='unreviewed'

def test_scan_is_idempotent_and_different_content_conflicts(setup):
 s,c,i,cl=setup;r=Scan(**ctx(c));i.scan(c.id,r);i.scan(c.id,r)
 assert i.view(c.id)['insight_revision']==1
 with pytest.raises(Conflict):i.scan(c.id,r.model_copy(update={'policy':r.policy.model_copy(update={'freshness_hours':10})}))

def test_stale_insight_revision_cannot_overwrite_review(setup):
 s,c,i,cl=setup;v=scan(c,i);review(c,i,v)
 with pytest.raises(Conflict):review(c,i,v,'useful')

def test_case_revision_and_fingerprint_checked(setup):
 s,c,i,cl=setup;v=scan(c,i);x=get(v)['insight']
 req=ReviewInsight(**ctx(c,v),insight_id=x['id'],fingerprint='0'*64,disposition='useful',reason='Human reason')
 with pytest.raises(Conflict):i.review(c.id,req)
 c2=update(s,c,'metadata',{'budget':6000})
 with pytest.raises(Conflict):review(c,i,v)

def test_only_one_concurrent_review_wins(setup):
 s,c,i,cl=setup;v=scan(c,i)
 def run(_):
  try:review(c,i,v);return 200
  except Conflict:return 409
 with ThreadPoolExecutor(max_workers=2) as p:assert sorted(p.map(run,[0,1]))==[200,409]

def test_question_promotion_is_explicit_atomic_and_deduplicated(setup):
 s,c,i,cl=setup;v=scan(c,i);row=get(v);x=row['insight'];before=s.get(c.id)
 req=InsightQuestion(**ctx(c,v),insight_id=x['id'],fingerprint=x['fingerprint'],question='What evidence would settle this?',owner='Case lead',reason='Investigate a shared prerequisite')
 out=i.create_question(c.id,req);after=s.get(c.id)
 assert after.revision==1 and after.observations==before.observations and len(after.questions)==len(before.questions)+1
 assert after.questions[-1].id==out['question_id'] and s.audit(c.id)['emergent_insights']['valid']
 assert i.create_question(c.id,req)['question_id']==out['question_id']
 v=scan(after,i,i.view(c.id));req=req.model_copy(update=ctx(after,v))
 with pytest.raises(Conflict):i.create_question(c.id,req)

def test_failed_question_rolls_back_both_ledgers(setup,monkeypatch):
 s,c,i,cl=setup;v=scan(c,i);x=get(v)['insight'];before=s.audit(c.id)
 monkeypatch.setattr(i,'_append',lambda *a,**kw:(_ for _ in ()).throw(ValueError('fixture failure')))
 with pytest.raises(ValueError):i.create_question(c.id,InsightQuestion(**ctx(c,v),insight_id=x['id'],fingerprint=x['fingerprint'],question='Verify?',owner='Case lead',reason='Fixture reason'))
 assert s.audit(c.id)==before

def test_human_hypotheses_are_recorded_without_becoming_facts(setup):
 s,c,i,cl=setup;before=s.get(c.id);req=Hypothesis(**ctx(c),title='Maybe one decision unlocks two routes',meaning='A possibility not a fact',why='The chart links overlap',verify='Who has authority?',references=[{'kind':'actor','id':'coo'}]);v=i.add_hypothesis(c.id,req)
 assert v['items'][0]['insight']['kind']=='hypothesis' and v['items'][0]['manual'] and s.get(c.id)==before

def test_cross_case_source_reference_denied(setup):
 s,c,i,cl=setup;req=Hypothesis(**ctx(c),title='Hypothesis',meaning='Test',why='Test',verify='Verify?',references=[{'kind':'evidence','id':'other-case-evidence'}])
 with pytest.raises(ValueError):i.add_hypothesis(c.id,req)
 assert i.view(c.id)['insight_revision']==0

def test_manual_hypothesis_history_not_removed_by_scan(setup):
 s,c,i,cl=setup;req=Hypothesis(**ctx(c),title='Do not lose this possibility',meaning='Needs review',why='Operator noticed it',verify='How could we disprove it?',references=[{'kind':'condition','id':'root'}]);v=i.add_hypothesis(c.id,req);iid=v['items'][0]['insight']['id'];v=scan(c,i,v)
 assert any(x['manual'] and x['insight']['id']==iid for x in v['items'])

def test_review_does_not_accept_confirmed_as_a_truth_state(setup):
 s,c,i,cl=setup;v=scan(c,i);x=get(v)['insight']
 r=cl.post(f'/api/v2/cases/{c.id}/insights/review',json={**ctx(c,v),'insight_id':x['id'],'fingerprint':x['fingerprint'],'disposition':'confirmed','reason':'Pretend it is true'})
 assert r.status_code==422 and s.get(c.id).observations==c.observations

def test_tampered_insight_chain_detected_and_not_hidden_by_case_export(setup):
 s,c,i,cl=setup;scan(c,i)
 with s.connection() as db:db.execute('UPDATE v2_insight_events SET hash=? WHERE case_id=?',('tampered',c.id));db.commit()
 assert not s.audit(c.id)['valid'] and not s.audit(c.id)['emergent_insights']['valid']
 with pytest.raises(ValueError):i.view(c.id)

def test_source_free_case_export_compatibility_and_model_trace_unchanged(setup):
 s,c,i,cl=setup;a=s.audit(c.id);v=scan(c,i);b=s.audit(c.id)
 assert b['events']==a['events'] and b['model_runs']==a['model_runs'] and b['head_hash']==a['head_hash']

def test_target_edited_without_criteria_is_only_alignment_question(setup):
 s,c,i,cl=setup;c=update(s,c,'metadata',{'desired_outcome':'A different target for the client'});v=scan(c,i)
 row=get(v,'target_alignment');assert row['insight']['kind']=='inferred' and 'may still' in row['insight']['verify']
 assert s.get(c.id).desired_outcome==c.desired_outcome

def test_snapshot_restart_retains_reviews(setup):
 s,c,i,cl=setup;v=review(c,i,scan(c,i));assert Insights(Store(s.path)).view(c.id)['items']==v['items']

@pytest.mark.parametrize('path',['/insight-rules','/build-discoveries','/cases/absent/insights'])
def test_new_reads_require_auth(setup,path):
 s,c,i,cl=setup;r=cl.get('/api/v2'+path,headers={'Authorization':'Bearer wrong'});assert r.status_code==401

@pytest.mark.parametrize('path',['scan','review','hypotheses','question'])
def test_new_writes_require_auth(setup,path):
 s,c,i,cl=setup;r=cl.post(f'/api/v2/cases/{c.id}/insights/'+path,json={},headers={'Authorization':'Bearer wrong'});assert r.status_code==401

def test_naive_or_unknown_request_fields_are_rejected(setup):
 s,c,i,cl=setup;base=f'/api/v2/cases/{c.id}/insights/scan'
 assert cl.post(base,json={**ctx(c),'force':True}).status_code==422
 assert cl.post(base,json={**ctx(c),'policy':{'freshness_hours':True}}).status_code==422
 assert cl.post(base,json=ctx(c),headers={'Origin':'https://other.example'}).status_code==403

def test_reviewer_reason_must_not_be_blank(setup):
 s,c,i,cl=setup;v=scan(c,i);x=get(v)['insight']
 req=ReviewInsight(**ctx(c,v),insight_id=x['id'],fingerprint=x['fingerprint'],disposition='dismissed',reason='   ')
 with pytest.raises(ValueError):i.review(c.id,req)

def test_simulation_does_not_scan_or_write_insight_history(setup):
 s,c,i,cl=setup;scan(c,i);before=s.audit(c.id)
 r=cl.post(f'/api/v2/cases/{c.id}/simulate',json={'expected_revision':0,'conditions':{'refused':True}})
 assert r.status_code==200 and s.audit(c.id)==before

def test_stale_time_review_requires_new_scan(setup,monkeypatch):
 import eightball.v2.insights as mod
 s,c,i,cl=setup;v=scan(c,i);now=utcnow();monkeypatch.setattr(mod,'utcnow',lambda:now+timedelta(minutes=16))
 with pytest.raises(Conflict):review(c,i,v)

def test_manual_revisit_preserves_old_context_and_reopens_review(setup):
 from eightball.v2.insights import RevisitHypothesis
 s,c,i,cl=setup
 v=i.add_hypothesis(c.id,Hypothesis(**ctx(c),title='Possible bottleneck',meaning='Something to check',why='Operator hypothesis',verify='Who has authority?',references=[{'kind':'actor','id':'coo'}]));row=v['items'][0];v=review(c,i,v,row=row)
 c=update(s,c,'metadata',{'budget':6500})
 view=i.view(c.id);assert not view['items'][0]['can_review']
 req=RevisitHypothesis(**ctx(c,view),insight_id=row['insight']['id'],fingerprint=row['insight']['fingerprint'],reason='Reread the current records after the budget change')
 v=i.revisit_hypothesis(c.id,req);row=v['items'][0]
 assert row['review_status']=='unreviewed' and row['can_review'] and len(row['reviews'])==2
 assert row['reviews'][0]['disposition']=='dismissed' and s.get(c.id)==c
 assert i.revisit_hypothesis(c.id,req)['insight_revision']==v['insight_revision']

def test_revisit_cannot_change_a_derived_finding_to_a_hypothesis(setup):
 from eightball.v2.insights import RevisitHypothesis
 s,c,i,cl=setup;v=i.add_hypothesis(c.id,Hypothesis(**ctx(c),title='Review it',meaning='Maybe',why='Link',verify='Check?',references=[{'kind':'actor','id':'coo'}]))
 # A derived finding is not a manual hypothesis; do not turn it into one via revisit.
 v=scan(c,i,v);row=get(v)
 with pytest.raises(ValueError):i.revisit_hypothesis(c.id,RevisitHypothesis(**ctx(c,v),insight_id=row['insight']['id'],fingerprint=row['insight']['fingerprint'],reason='Cannot forge origin'))


@pytest.mark.parametrize('field',['title','meaning','why','verify'])
def test_manual_hypothesis_rejects_blank_fields(setup,field):
 from pydantic import ValidationError
 s,c,i,cl=setup
 data=dict(**ctx(c),title='Record',meaning='Maybe',why='Reason',verify='Check?',references=[{'kind':'actor','id':'coo'}])
 data[field]='   '
 with pytest.raises(ValidationError):Hypothesis.model_validate(data)


def test_revisit_cannot_reanchor_removed_condition_silently(setup):
 from eightball.v2.insights import RevisitHypothesis
 s,c,i,cl=setup
 # A non-observed condition can be removed explicitly through the graph editor.
 graph=c.graph.model_dump(mode='json');graph['conditions'].append({'id':'temporary','title':'Temporary condition','confirmation':'Direct evidence'})
 c=update(s,c,'replace_graph',{'graph':graph})
 v=i.add_hypothesis(c.id,Hypothesis(**ctx(c),title='Possible issue',meaning='Maybe',why='Operator idea',verify='Can we check?',references=[{'kind':'condition','id':'temporary'}]))
 row=v['items'][0]
 graph=c.graph.model_dump(mode='json');graph['conditions']=[x for x in graph['conditions'] if x['id']!='temporary']
 c=update(s,c,'replace_graph',{'graph':graph});before=s.audit(c.id);v=i.view(c.id)
 with pytest.raises(Conflict):i.revisit_hypothesis(c.id,RevisitHypothesis(**ctx(c,v),insight_id=row['insight']['id'],fingerprint=row['insight']['fingerprint'],reason='Do not invent replacement'))
 assert s.audit(c.id)==before


def test_rule_catalogue_includes_core_and_case_metadata_detectors(setup):
 s,c,i,cl=setup
 r=cl.get('/api/v2/insight-rules');assert r.status_code==200
 rules=r.json()['rules'];assert len(rules)==13 and len({x['id'] for x in rules})==13
 assert any(x['id']=='target_alignment' for x in rules)
