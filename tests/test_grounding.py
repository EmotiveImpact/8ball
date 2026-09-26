from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import json
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from eightball.api import make_app
from eightball.store import Store as Legacy, Conflict
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Actor, Evidence, uid, utcnow
from eightball.v2.commands import Command
from eightball.v2.grounding import *
from endstate.time_review import TimeInterpretation

@pytest.fixture
def setup(tmp_path):
    legacy=Legacy(str(tmp_path/'test.db'));store=Store(legacy.path)
    case=demo_case()
    case.actors.extend([Actor(id='alex1',name='Alex Morgan',role='Legal adviser'),Actor(id='alex2',name='Alex Morgan',role='Customer finance')])
    case.evidence.append(Evidence(id='names',title='Fictional source',source='Case lead',
        text='😀\r\nAlex Morgan in finance asked for the report by noon tomorrow, London time.',status='reviewed'))
    case=store.create(case,fixture=True)
    client=TestClient(make_app(legacy,'x'*32),headers={'Authorization':'Bearer '+'x'*32})
    return store,case,GroundingDesk(store),client


def context(case,desk):return dict(expected_revision=case.revision,expected_review_revision=desk.view(case.id)['review_revision'])
def mention(case,text='Alex Morgan'):
    src=next(e for e in case.evidence if e.id=='names');start=src.text.index(text)
    return SourceMention(evidence_id=src.id,start=start,end=start+len(text),quote=text,content_sha256=text_hash(src.text))
def create(case,desk,kind='identity',text='Alex Morgan'):
    return desk.create(case.id,NewReview(**context(case,desk),event_id=uid(),kind=kind,mention=mention(case,text),note='Who or what date does this source refer to?'))
def record(case,desk):return desk.view(case.id)['records'][0]
def identity(case,desk,**kw):
    return desk.identity(case.id,IdentityDecision(**context(case,desk),event_id=uid(),review_id=record(case,desk)['id'],
            **{'disposition':'linked','actor_id':'alex2','reason':'Source specifies finance, reviewed with the case lead',**kw}))
def time():return TimeInterpretation(calendar_date='2026-09-25',wall_time='12:00',time_zone='Europe/London',zone_reason='Explicit London wording')
def preview_request(case,desk,**kw):
    return DeadlinePreview(**context(case,desk),review_id=record(case,desk)['id'],interpretation=kw.pop('interpretation',time()),
        target=kw.pop('target',DeadlineTarget(kind='condition',id='report')),reason='Source identifies the incident report deadline',**kw)
def apply_time(case,desk,req=None):
    req=req or preview_request(case,desk);p=desk.preview(case.id,req)
    return desk.apply_deadline(case.id,ApplyDeadline(**req.model_dump(),event_id=uid(),preview_digest=p['preview_digest']))
def change(s,c,kind,payload):return s.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind=kind,payload=payload))[0]


def test_opening_review_desk_does_not_change_legacy_export(setup):
    s,c,d,cl=setup;before=s.audit(c.id)
    assert d.view(c.id)['records']==[] and 'source_interpretations' not in before
    assert s.audit(c.id)==before


def test_create_retains_exact_unicode_quote_and_no_case_change(setup):
    s,c,d,cl=setup;before=s.audit(c.id);create(c,d)
    r=record(c,d);assert r['mention']['start']==3 and r['mention']['quote']=='Alex Morgan'
    after=s.audit(c.id);assert after.pop('source_interpretations')['valid'] and after==before
    assert s.get(c.id)==c


def test_same_name_returns_two_candidates_not_one_merged_person(setup):
    s,c,d,cl=setup;create(c,d);r=record(c,d)
    assert {o['id'] for o in r['candidates']}=={'alex1','alex2'}
    assert all(o['not_identity_proof'] for o in r['candidates'])
    identity(c,d);r=record(c,d)
    assert r['actor_id']=='alex2' and r['status']=='linked'
    assert s.get(c.id).actors==c.actors and s.get(c.id).observations==c.observations


def test_distinct_then_revised_link_keeps_both_judgements(setup):
    s,c,d,cl=setup;create(c,d);identity(c,d,disposition='distinct',actor_id='alex1');identity(c,d)
    r=record(c,d);assert r['status']=='linked' and len(r['history'])==3
    e=s.audit(c.id)['source_interpretations']['events']
    assert e[1]['review']['status']=='distinct' and e[1]['review']['actor_id']=='alex1'


def test_dismiss_reopen_never_deletes_or_reverts_application(setup):
    s,c,d,cl=setup;create(c,d);rid=record(c,d)['id']
    for disp in ['dismissed','open']:
        d.dispose(c.id,Disposition(**context(c,d),event_id=uid(),review_id=rid,disposition=disp,reason='Owner-requested reconsideration'))
    assert record(c,d)['status']=='open' and len(record(c,d)['history'])==3
    assert s.get(c.id)==c


def test_actor_revision_requires_review_of_existing_link(setup):
    s,c,d,cl=setup;create(c,d);identity(c,d)
    obj=next(a for a in c.actors if a.id=='alex2').model_dump(mode='json');obj['role']='Authority changed, unverified'
    c=change(s,c,'upsert_object',{'kind':'actor','object':obj})
    assert 'actor_record_changed' in record(c,d)['warnings']
    identity(c,d);assert not record(c,d)['warnings']


def test_source_retraction_flags_link_but_does_not_remove_history(setup):
    s,c,d,cl=setup;create(c,d);identity(c,d)
    c=change(s,c,'review_evidence',{'evidence_id':'names','status':'retracted'})
    assert 'source_unavailable_or_retracted' in record(c,d)['warnings']
    with pytest.raises(ValueError):identity(c,d)
    assert len(record(c,d)['history'])==2


def test_deadline_preview_is_isolated_and_explicitly_utc(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');before=s.audit(c.id)
    p=d.preview(c.id,preview_request(c,d))
    assert p['resolution']['selected']['utc']=='2026-09-25T11:00:00+00:00'
    assert p['can_apply'] and p['target_title']=='Incident report approved'
    assert s.audit(c.id)==before


def test_apply_changes_only_selected_schedule_and_invalidates_approvals(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');out=apply_time(c,d);after=s.get(c.id)
    assert after.revision==c.revision+1 and after.observations==c.observations and after.actors==c.actors
    assert after.deadline==c.deadline and after.approvals==[]
    assert next(x for x in after.graph.conditions if x.id=='report').due_at.isoformat()=='2026-09-25T11:00:00+00:00'
    a=s.audit(c.id);assert a['valid'] and a['source_interpretations']['valid']
    assert a['events'][-1]['kind']=='apply_deadline_review'
    assert a['events'][-1]['payload']['interpretation']['mention']['quote']=='noon tomorrow'
    assert out['reviews']['records'][0]['status']=='applied'


@pytest.mark.parametrize('kind,target_id', [('case',None),('decision','escalation'),('question','q_authority')])
def test_each_supported_deadline_target(setup,kind,target_id):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow')
    req=preview_request(c,d,target=DeadlineTarget(kind=kind,id=target_id or c.id));apply_time(c,d,req)
    assert s.get(c.id).revision==1 and s.audit(c.id)['valid']


def test_retraction_does_not_silently_remove_a_deadline(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');apply_time(c,d)
    c=s.get(c.id);before=c.graph
    c=change(s,c,'review_evidence',{'evidence_id':'names','status':'retracted'})
    assert c.graph==before
    assert record(c,d)['needs_attention'] and not record(c,d)['can_interpret']


def test_later_manual_deadline_edit_marked_as_overridden(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');apply_time(c,d)
    c=s.get(c.id);g=c.graph.model_dump(mode='json');next(x for x in g['conditions'] if x['id']=='report')['due_at']='2026-10-01T12:00:00Z'
    change(s,c,'replace_graph',{'graph':g})
    assert 'deadline_has_subsequently_changed' in record(s.get(c.id),d)['warnings']


def test_ambiguous_time_cannot_be_applied_without_fold(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow')
    req=preview_request(c,d,interpretation=time().model_copy(update={'calendar_date':'2026-10-25','wall_time':'01:30'}))
    p=d.preview(c.id,req);assert not p['can_apply'] and p['resolution']['status']=='ambiguous'
    with pytest.raises(ValueError):d.apply_deadline(c.id,ApplyDeadline(**req.model_dump(),event_id=uid(),preview_digest=p['preview_digest']))
    req=req.model_copy(update={'interpretation':req.interpretation.model_copy(update={'fold':1})});apply_time(c,d,req)
    assert s.get(c.id).revision==1


def test_preview_digest_detects_changed_intent_even_at_same_revision(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');req=preview_request(c,d);p=d.preview(c.id,req)
    with pytest.raises(Conflict):d.apply_deadline(c.id,ApplyDeadline(**{**req.model_dump(),'reason':'Changed after preview'},event_id=uid(),preview_digest=p['preview_digest']))
    assert s.get(c.id)==c


def test_source_review_required_for_interpretation_not_capture(setup):
    s,c,d,cl=setup;c=change(s,c,'add_evidence',{'title':'New','source':'Sender','text':'Tomorrow.'})
    e=c.evidence[-1]
    d.create(c.id,NewReview(**context(c,d),event_id=uid(),kind='deadline',mention=SourceMention(evidence_id=e.id,start=0,end=9,quote=e.text,content_sha256=text_hash(e.text)),note='Resolve exact day'))
    with pytest.raises(ValueError,match='Review the evidence'):d.preview(c.id,preview_request(c,d))
    assert 'source_needs_review' in record(c,d)['warnings']


@pytest.mark.parametrize('mutation',[{'content_sha256':'0'*64},{'quote':'Alex Morgen'}, {'evidence_id':'another-case'}])
def test_forged_quote_hash_or_cross_case_source_rejected(setup,mutation):
    s,c,d,cl=setup;bad=SourceMention.model_validate({**mention(c).model_dump(),**mutation})
    with pytest.raises(ValueError):d.create(c.id,NewReview(**context(c,d),event_id=uid(),kind='identity',mention=bad,note='Check exact name'))
    assert not d.view(c.id)['records']


def test_same_mention_cannot_be_duplicated(setup):
    s,c,d,cl=setup;create(c,d)
    with pytest.raises(Conflict):create(c,d)


def test_event_retries_are_idempotent_after_revision_change(setup):
    s,c,d,cl=setup;r=NewReview(**context(c,d),event_id=uid(),kind='identity',mention=mention(c),note='Check person')
    d.create(c.id,r);d.create(c.id,r)
    assert d.view(c.id)['review_revision']==1
    with pytest.raises(Conflict):d.create(c.id,r.model_copy(update={'note':'Different request'}))


def test_deadline_retry_does_not_repeat_case_amendment(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');req=preview_request(c,d);p=d.preview(c.id,req)
    a=ApplyDeadline(**req.model_dump(),event_id=uid(),preview_digest=p['preview_digest'])
    d.apply_deadline(c.id,a);assert d.apply_deadline(c.id,a)['duplicate']
    assert s.get(c.id).revision==1


def test_stale_case_and_review_revision_fail(setup):
    s,c,d,cl=setup;create(c,d);old=context(c,d);identity(c,d)
    with pytest.raises(Conflict):d.dispose(c.id,Disposition(**old,event_id=uid(),review_id=record(c,d)['id'],disposition='open',reason='Stale view'))
    change(s,c,'metadata',{'budget':6000})
    with pytest.raises(Conflict):identity(c,d)


def test_concurrent_operator_writes_have_one_winner(setup):
    s,c,d,cl=setup;create(c,d);ctx=context(c,d);rid=record(c,d)['id']
    def run(i):
        try:
            d.identity(c.id,IdentityDecision(**ctx,event_id=uid(),review_id=rid,disposition='linked',actor_id=f'alex{i}',reason='Explicit reviewer judgement'))
            return 200
        except Conflict:return 409
    with ThreadPoolExecutor(max_workers=2) as pool:assert sorted(pool.map(run,[1,2]))==[200,409]


def test_case_and_review_transaction_roll_back_together(setup,monkeypatch):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');before=s.audit(c.id)
    def fail(*args,**kw):raise RuntimeError('Injected persistence failure')
    monkeypatch.setattr(d,'_append',fail)
    with pytest.raises(RuntimeError):apply_time(c,d)
    assert s.audit(c.id)==before


def test_journal_tampering_detected_and_no_further_writes(setup):
    s,c,d,cl=setup;create(c,d)
    with s.connection() as db:db.execute('UPDATE v2_grounding_events SET hash=? WHERE case_id=?',('tampered',c.id));db.commit()
    assert not s.audit(c.id)['valid']
    with pytest.raises(ValueError):d.view(c.id)


def test_applied_deadline_cannot_lose_its_review_history_unnoticed(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');apply_time(c,d)
    with s.connection() as db:db.execute('DELETE FROM v2_grounding_events WHERE case_id=?',(c.id,));db.commit()
    assert not s.audit(c.id)['valid']


def test_generic_command_cannot_bypass_review_service(setup):
    s,c,d,cl=setup
    r=cl.post(f'/api/v2/cases/{c.id}/commands',json={'event_id':uid(),'expected_revision':0,'kind':'apply_deadline_review','payload':{}})
    assert r.status_code==422 and s.get(c.id)==c


def test_api_read_create_preview_apply_and_isolation(setup):
    s,c,d,cl=setup;base=f'/api/v2/cases/{c.id}/grounding'
    assert cl.get(base).status_code==200
    req=NewReview(**context(c,d),event_id=uid(),kind='deadline',mention=mention(c,'noon tomorrow'),note='Establish report deadline')
    assert cl.post(base+'/create',json=req.model_dump(mode='json')).status_code==200
    pr=preview_request(c,d);result=cl.post(base+'/deadline-preview',json=pr.model_dump(mode='json'));assert result.status_code==200,result.text
    ar=ApplyDeadline(**pr.model_dump(),event_id=uid(),preview_digest=result.json()['preview_digest'])
    assert cl.post(base+'/deadline-apply',json=ar.model_dump(mode='json')).status_code==200
    assert cl.get('/api/v2/cases/missing/grounding').status_code==404
    assert cl.get(base,headers={'Authorization':'Bearer invalid'}).status_code==401


def test_reload_preserves_interpretations(setup):
    s,c,d,cl=setup;create(c,d);identity(c,d)
    assert GroundingDesk(Store(s.path)).view(c.id)==d.view(c.id)


def test_history_includes_every_original_reviewer_reason(setup):
    s,c,d,cl=setup;create(c,d);identity(c,d,disposition='distinct',actor_id='alex1',reason='Legal name is a different person');identity(c,d,reason='Finance identity explicitly checked')
    history=record(c,d)['history']
    assert history[1]['reason']=='Legal name is a different person'
    assert history[2]['reason']=='Finance identity explicitly checked'
    assert history[1]['disposition']=='distinct' and history[1]['actor_name']=='Alex Morgan'


def test_unknown_target_or_cross_case_identity_is_rejected(setup):
    s,c,d,cl=setup;create(c,d)
    with pytest.raises(ValueError):identity(c,d,actor_id='outside_this_case')
    create(c,d,'deadline','noon tomorrow')
    with pytest.raises(ValueError):d.preview(c.id,preview_request(c,d,target=DeadlineTarget(kind='case',id='another_case')))


def test_source_status_is_rechecked_after_preview(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');req=preview_request(c,d);p=d.preview(c.id,req)
    new=change(s,c,'review_evidence',{'evidence_id':'names','status':'retracted'})
    with pytest.raises(Conflict):d.apply_deadline(c.id,ApplyDeadline(**req.model_dump(),event_id=uid(),preview_digest=p['preview_digest']))
    assert new.graph==c.graph


def test_existing_signed_decision_is_not_erased_by_deadline_amendment(setup):
    s,c,d,cl=setup;c=change(s,c,'decide',{'decision_id':'escalation','option_id':'hold','rationale':'Wait for report','evidence_ids':['names']})
    before=c.decisions[0].model_dump();create(c,d,'deadline','noon tomorrow');apply_time(c,d,preview_request(c,d,target=DeadlineTarget(kind='decision',id='escalation')))
    after=s.get(c.id).decisions[0].model_dump()
    assert {k:v for k,v in before.items() if k!='needed_by'}=={k:v for k,v in after.items() if k!='needed_by'}


def test_tampered_preview_cannot_replace_the_requested_target(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');req=preview_request(c,d);p=d.preview(c.id,req)
    with pytest.raises(Conflict):d.apply_deadline(c.id,ApplyDeadline(**{**req.model_dump(),'target':{'kind':'case','id':c.id}},event_id=uid(),preview_digest=p['preview_digest']))
    assert s.get(c.id)==c


def test_blank_reason_and_privileged_extra_fields_rejected():
    with pytest.raises(ValidationError):IdentityDecision(event_id='e',expected_revision=0,expected_review_revision=0,review_id='r',disposition='unresolved',reason='   ')
    with pytest.raises(ValidationError):IdentityDecision(event_id='e',expected_revision=0,expected_review_revision=0,review_id='r',disposition='linked',actor_id='a',reason='Reason provided',verified=True)


def test_applied_deadline_has_same_quote_despite_repeated_historical_reviews(setup):
    s,c,d,cl=setup;create(c,d,'deadline','noon tomorrow');apply_time(c,d);c=s.get(c.id);first=record(c,d)
    req=preview_request(c,d,interpretation=time().model_copy(update={'calendar_date':'2026-09-26'}));apply_time(c,d,req)
    rows=s.audit(c.id)['source_interpretations']['events']
    applied=[r for r in rows if r['operation']=='deadline_applied']
    assert len(applied)==2 and applied[0]['review']['application']['utc']!=applied[1]['review']['application']['utc']
    assert applied[0]['review']['mention']==applied[1]['review']['mention']==first['mention']
    assert s.audit(c.id)['valid']


def test_live_approval_is_really_invalidated_not_just_an_empty_list(setup):
    s,c,d,cl=setup
    c=change(s,c,'add_evidence',{'title':'Language approval','source':'Fictional legal reviewer','text':'External wording is reviewed and approved.'})
    e=c.evidence[-1].id
    c=change(s,c,'review_evidence',{'evidence_id':e,'status':'reviewed'})
    c=change(s,c,'observe',{'condition_id':'language','evidence_id':e,'value':True,'rationale':'Written fictional approval'})
    c=change(s,c,'approve',{'action_id':'listen'})
    assert len(c.approvals)==1
    create(c,d,'deadline','noon tomorrow');req=preview_request(c,d)
    assert d.preview(c.id,req)['approvals_to_invalidate']==1
    apply_time(c,d,req)
    assert not s.get(c.id).approvals


def test_original_source_retraction_invalidates_linked_excerpt_review(setup):
    from eightball.v2.source_desk import SourceDesk
    from eightball.v2.source_contracts import ImportSource,CapturePassages,Passage,RetractSource
    s,c,d,cl=setup;source=SourceDesk(s)
    text='Alex Morgan in finance confirmed the contact details.'
    c,_,doc=source.import_source(c.id,ImportSource(event_id=uid(),expected_revision=c.revision,title='Original email',source='Fictional author',text=text))
    result=source.capture(c.id,CapturePassages(event_id=uid(),expected_revision=c.revision,passages=[Passage(document_id=doc['id'],start=0,end=len(text),content_sha256=text_hash(text))]))
    c=s.get(c.id);e=c.evidence[-1]
    c=change(s,c,'review_evidence',{'evidence_id':e.id,'status':'reviewed'})
    d.create(c.id,NewReview(**context(c,d),event_id=uid(),kind='identity',note='Resolve exact name',mention=SourceMention(evidence_id=e.id,start=0,end=11,quote='Alex Morgan',content_sha256=text_hash(text))))
    identity(c,d)
    source.retract(c.id,doc['id'],RetractSource(event_id=uid(),expected_revision=c.revision,reason='Fictional source withdrawn'))
    assert record(s.get(c.id),d)['needs_attention']
    assert s.audit(c.id)['valid'] and s.audit(c.id)['source_integrity']['valid']
