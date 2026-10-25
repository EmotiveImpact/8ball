from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import json

import pytest

from endstate.events import IncomingEvent
from eightball.agency_access import AccessRegistry
from eightball.authorisation import Grant, Identity, Operation, Resource
from eightball.event_inbox import EventInbox
from eightball.event_work import EventWork
from eightball.models import utcnow
from eightball.store import Conflict, canonical, digest
from eightball.v2.commands import Command
from eightball.v2.event_reviews import EventReviews
from eightball.v2.playbooks import demo_case
from eightball.v2.store import Store

SCOPE = dict(organisation_id='agency',matter_id='matter')


@pytest.fixture
def review(tmp_path):
    store=Store(str(tmp_path/'case.db'));case=store.create(demo_case(),fixture=True)
    reviews=EventReviews(store);registry=AccessRegistry(store.path)
    registry.bind_case(case.id,Resource(**SCOPE))
    identity=Identity(issuer='https://identity.fixture.example',subject='reviewer')
    registry.add_grant('write',Grant(identity=identity,resource=Resource(**SCOPE),
        operations=frozenset({Operation.WRITE}),valid_from=utcnow()-timedelta(minutes=1),
        expires_at=utcnow()+timedelta(hours=1)))
    EventInbox(store.path).append(IncomingEvent(**SCOPE,source_id='source',source_version='v1',
        event_id='incoming',kind='proposal_received',base_revision=0,text='Original fictional source'),**SCOPE)
    queue=EventWork(store.path);job=queue.enqueue(**SCOPE,sequence=1,base_revision=0,case_id=case.id)
    token=queue.claim(job,**SCOPE)
    queue.finish(job,token,'Original unreviewed processing text',**SCOPE,current_revision=0,permission_valid=True)
    graph=case.graph.model_dump(mode='json');graph['actions'][0]['cost']+=100
    command=Command(event_id='reviewed-amendment',expected_revision=0,kind='replace_graph',payload={'graph':graph})
    request=dict(work_id=job,case_id=case.id,reviewer=identity,command=command,
                 rationale='Reviewed the changed cost against the fictional source.')
    return store,case,reviews,registry,queue,request


def test_review_is_atomic_auditable_and_idempotent(review):
    store,case,reviews,_,queue,request=review
    before=store.audit(case.id)
    record=reviews.commit_graph(**request)
    assert store.get(case.id).revision==1
    assert store.get(case.id).observations==case.observations
    assert not store.get(case.id).approvals
    assert queue.inspect(request['work_id'],**SCOPE)['state']=='committed'
    assert reviews.commit_graph(**request)==record
    audit=store.audit(case.id)
    assert audit['valid'] and audit['replay_matches_snapshot']
    assert len(audit['events'])==len(before['events'])+1
    saved=audit['incoming_event_reviews']['records'][0]
    assert saved['source_receipt']['event']['text']=='Original fictional source'
    assert saved['original_result']=='Original unreviewed processing text'
    assert saved['request']['rationale']==request['rationale']
    assert saved['unassisted_model_acceptance'] is False and saved['changes']
    assert saved['actor'].startswith('identity:')


def test_revoked_permission_blocks_even_a_duplicate_acknowledgement(review):
    store,case,reviews,registry,_,request=review
    reviews.commit_graph(**request);before=store.audit(case.id)
    registry.revoke('write')
    with pytest.raises(PermissionError):reviews.commit_graph(**request)
    assert store.audit(case.id)==before


@pytest.mark.parametrize('mode',['revoked','expired','read_only','object_only'])
def test_current_matter_write_grant_is_required(review,mode):
    store,case,reviews,registry,_,request=review
    registry.revoke('write');before=store.audit(case.id)
    if mode!='revoked':
        registry.add_grant('replacement',Grant(identity=request['reviewer'],
            resource=Resource(**SCOPE,object_id='one-object' if mode=='object_only' else None),
            operations=frozenset({Operation.READ if mode=='read_only' else Operation.WRITE}),
            valid_from=utcnow()-timedelta(hours=2),
            expires_at=utcnow()+timedelta(hours=-1 if mode=='expired' else 1)))
    with pytest.raises(PermissionError):reviews.commit_graph(**request)
    assert store.audit(case.id)==before


def test_stale_case_does_not_consume_result(review):
    store,case,reviews,_,queue,request=review
    store.change(case.id,Command(event_id='changed',expected_revision=0,kind='metadata',payload={'budget':1234}))
    before=store.audit(case.id)
    with pytest.raises(Conflict):reviews.commit_graph(**request)
    assert store.audit(case.id)==before
    assert queue.inspect(request['work_id'],**SCOPE)['state']=='awaiting_review'


def test_cross_matter_and_non_graph_commands_are_denied(review):
    store,case,reviews,registry,_,request=review
    other=store.create(demo_case(),fixture=True)
    registry.bind_case(other.id,Resource(organisation_id='other',matter_id='other'))
    with pytest.raises(PermissionError):reviews.commit_graph(**(request|{'case_id':other.id}))
    command=Command(event_id='forbidden',expected_revision=0,kind='metadata',payload={'budget':1})
    with pytest.raises(ValueError):reviews.commit_graph(**(request|{'command':command}))
    assert store.get(case.id).revision==0 and store.get(other.id).revision==0


def test_failure_after_case_write_rolls_back_case_and_consumption(review,monkeypatch):
    store,case,reviews,_,queue,request=review;before=store.audit(case.id)
    original=store._persist
    def fail(*args,**kwargs):
        original(*args,**kwargs)
        raise RuntimeError('Injected local failure')
    monkeypatch.setattr(store,'_persist',fail)
    with pytest.raises(RuntimeError):reviews.commit_graph(**request)
    assert store.audit(case.id)==before
    assert queue.inspect(request['work_id'],**SCOPE)['state']=='awaiting_review'


def test_changed_retry_and_corrupt_review_are_visible(review):
    store,case,reviews,_,_,request=review
    reviews.commit_graph(**request)
    with pytest.raises(Conflict):reviews.commit_graph(**(request|{'rationale':'Different review rationale'}))
    with store.connection() as db:
        db.execute("UPDATE event_consumptions SET record='{}'");db.commit()
    assert not store.audit(case.id)['valid']


def test_unconsumed_cases_keep_original_export_shape(review):
    store,case,_,_,_,_=review
    assert 'incoming_event_reviews' not in store.audit(case.id)


def test_concurrent_identical_consumption_commits_once(review):
    store,case,reviews,_,_,request=review
    with ThreadPoolExecutor(max_workers=2) as pool:
        records=list(pool.map(lambda _:reviews.commit_graph(**request),range(2)))
    assert records[0]==records[1] and store.get(case.id).revision==1


def test_rehashed_result_tampering_cannot_break_case_chain_binding(review):
    store,case,reviews,_,_,request=review
    record=reviews.commit_graph(**request)
    record['original_result']='Substituted processing result'
    with store.connection() as db:
        db.execute('UPDATE event_consumptions SET record=?,digest=?',(canonical(record),digest(record)))
        db.commit()
    audit=store.audit(case.id)
    assert not audit['valid'] and not audit['incoming_event_reviews']['valid']


def test_permission_expiring_during_calculation_rolls_back(review,monkeypatch):
    store,case,reviews,_,queue,request=review;before=store.audit(case.id)
    now=utcnow();ticks=iter([now,now+timedelta(hours=2)])
    monkeypatch.setattr('eightball.v2.event_reviews.utcnow',lambda:next(ticks))
    with pytest.raises(PermissionError):reviews.commit_graph(**request)
    assert store.audit(case.id)==before
    assert queue.inspect(request['work_id'],**SCOPE)['state']=='awaiting_review'


def notice_reader(review):
    store,case,_,registry,_,request=review
    registry.add_grant('notice-read',Grant(identity=request['reviewer'],resource=Resource(**SCOPE),
        operations=frozenset({Operation.READ}),valid_from=utcnow()-timedelta(minutes=1),
        expires_at=utcnow()+timedelta(hours=1)))
    return dict(case_id=case.id,reader=request['reviewer'])


def test_outbox_survives_restart_and_duplicate_review_without_duplicate_notice(review):
    from eightball.v2.event_outbox import EventOutbox
    store,case,reviews,_,_,request=review; reader=notice_reader(review)
    reviews.commit_graph(**request);reviews.commit_graph(**request)
    outbox=EventOutbox(store);notice=outbox.pull(**reader)
    assert notice['revision']==1 and notice['command_authority'] is False
    assert 'original_result' not in notice and 'source_receipt' not in notice
    restarted=EventOutbox(Store(store.path))
    assert restarted.pull(**reader)==notice
    before=store.audit(case.id)
    restarted.acknowledge(**reader,notice_id=notice['id'])
    restarted.acknowledge(**reader,notice_id=notice['id'])
    assert restarted.pull(**reader) is None
    assert store.audit(case.id)==before


def test_outbox_write_failure_rolls_back_review_case_and_consumption(review,monkeypatch):
    from eightball.v2.event_outbox import EventOutbox
    store,case,reviews,_,queue,request=review;before=store.audit(case.id)
    original=EventOutbox.append
    def fail(db,record):
        original(db,record)
        raise RuntimeError('Failure after outbox insert')
    monkeypatch.setattr(EventOutbox,'append',fail)
    with pytest.raises(RuntimeError):reviews.commit_graph(**request)
    assert store.audit(case.id)==before
    assert queue.inspect(request['work_id'],**SCOPE)['state']=='awaiting_review'
    with store.connection() as db: assert db.execute('SELECT count(*) FROM event_outbox').fetchone()[0]==0


def test_outbox_rechecks_revocation_on_pull_and_ack(review):
    from eightball.v2.event_outbox import EventOutbox
    store,_,reviews,registry,_,request=review;reader=notice_reader(review)
    reviews.commit_graph(**request);outbox=EventOutbox(store);notice=outbox.pull(**reader)
    registry.revoke('notice-read')
    with pytest.raises(PermissionError):outbox.pull(**reader)
    with pytest.raises(PermissionError):outbox.acknowledge(**reader,notice_id=notice['id'])
    with store.connection() as db:
        assert db.execute('SELECT acknowledged_at FROM event_notice_delivery').fetchone()[0] is None


def test_outbox_different_reader_has_separate_delivery_and_cannot_ack_unread(review):
    from eightball.v2.event_outbox import EventOutbox
    store,case,reviews,registry,_,request=review;reader=notice_reader(review)
    other=Identity(issuer=request['reviewer'].issuer,subject='second-reader')
    registry.add_grant('second-read',Grant(identity=other,resource=Resource(**SCOPE),
        operations=frozenset({Operation.READ}),valid_from=utcnow()-timedelta(minutes=1),
        expires_at=utcnow()+timedelta(hours=1)))
    reviews.commit_graph(**request);outbox=EventOutbox(store);notice=outbox.pull(**reader)
    with pytest.raises(Conflict):outbox.acknowledge(case_id=case.id,reader=other,notice_id=notice['id'])
    outbox.acknowledge(**reader,notice_id=notice['id'])
    assert outbox.pull(case_id=case.id,reader=other)==notice
    assert outbox.pull(**reader) is None


def test_outbox_rehashed_metadata_tampering_is_rejected(review):
    from eightball.v2.event_outbox import EventOutbox
    store,_,reviews,_,_,request=review;reader=notice_reader(review)
    reviews.commit_graph(**request)
    with store.connection() as db:
        body=json.loads(db.execute('SELECT body FROM event_outbox').fetchone()[0]);body['revision']=99
        db.execute('UPDATE event_outbox SET body=?,digest=?',(canonical(body),digest(body)));db.commit()
    with pytest.raises(Conflict):EventOutbox(store).pull(**reader)


def test_outbox_wrong_case_and_write_only_reader_are_denied(review):
    from eightball.v2.event_outbox import EventOutbox
    store,case,reviews,registry,_,request=review
    reviews.commit_graph(**request);outbox=EventOutbox(store)
    with pytest.raises(PermissionError):outbox.pull(case_id=case.id,reader=request['reviewer'])
    reader=notice_reader(review);notice=outbox.pull(**reader)
    other=store.create(demo_case(),fixture=True)
    registry.bind_case(other.id,Resource(organisation_id='other',matter_id='other'))
    with pytest.raises(PermissionError):outbox.acknowledge(case_id=other.id,reader=request['reviewer'],notice_id=notice['id'])


def test_outbox_expiry_during_pull_does_not_record_delivery(review,monkeypatch):
    from eightball.v2.event_outbox import EventOutbox
    store,_,reviews,_,_,request=review;reader=notice_reader(review)
    reviews.commit_graph(**request)
    now=utcnow();ticks=iter([now,now,now+timedelta(hours=2)])
    monkeypatch.setattr('eightball.v2.event_outbox.utcnow',lambda:next(ticks))
    with pytest.raises(PermissionError):EventOutbox(store).pull(**reader)
    with store.connection() as db: assert db.execute('SELECT count(*) FROM event_notice_delivery').fetchone()[0]==0


def test_outbox_orders_two_changes_and_concurrent_pulls_repeat_same_notice(review):
    from eightball.v2.event_outbox import EventOutbox
    store,case,reviews,_,queue,request=review;reader=notice_reader(review)
    reviews.commit_graph(**request)
    EventInbox(store.path).append(IncomingEvent(**SCOPE,source_id='source',source_version='v2',
        event_id='incoming-2',kind='proposal_received',base_revision=1,text='Second fictional source'),**SCOPE)
    job=queue.enqueue(**SCOPE,sequence=2,base_revision=1,case_id=case.id);token=queue.claim(job,**SCOPE)
    queue.finish(job,token,'Second proposed result',**SCOPE,current_revision=1,permission_valid=True)
    graph=store.get(case.id).graph.model_dump(mode='json');graph['actions'][0]['cost']+=1
    command=Command(event_id='second-review',expected_revision=1,kind='replace_graph',payload={'graph':graph})
    reviews.commit_graph(**(request|dict(work_id=job,command=command)))
    outbox=EventOutbox(store)
    with ThreadPoolExecutor(max_workers=2) as pool:
        notices=list(pool.map(lambda _:outbox.pull(**reader),range(2)))
    assert notices[0]==notices[1] and notices[0]['revision']==1
    outbox.acknowledge(**reader,notice_id=notices[0]['id'])
    second=outbox.pull(**reader)
    assert second['revision']==2 and second['id']>notices[0]['id']
    outbox.acknowledge(**reader,notice_id=second['id'])
    assert outbox.pull(**reader) is None


def test_processing_result_cannot_move_to_another_case_in_same_matter(review):
    store,case,reviews,registry,queue,request=review
    other=store.create(demo_case(),fixture=True);registry.bind_case(other.id,Resource(**SCOPE))
    with pytest.raises(PermissionError):reviews.commit_graph(**(request|{'case_id':other.id}))
    notice_reader(review)
    with pytest.raises(KeyError):reviews.view(case_id=other.id,work_id=request['work_id'],reader=request['reviewer'])
    assert store.get(other.id).revision==0 and store.get(case.id).revision==0
    assert queue.inspect(request['work_id'],**SCOPE)['state']=='awaiting_review'


def test_historical_unbound_attempt_migration_preserves_output_but_cannot_commit(review):
    store,case,reviews,_,queue,request=review
    with store.connection() as db:
        db.execute('ALTER TABLE event_work DROP COLUMN case_id');db.commit()
    migrated=EventWork(store.path)
    work=migrated.inspect(request['work_id'],**SCOPE)
    assert work['case_id'] is None and work['result']=='Original unreviewed processing text'
    before=store.audit(case.id)
    with pytest.raises(Conflict,match='no case binding'):reviews.commit_graph(**request)
    assert store.audit(case.id)==before
    assert migrated.inspect(request['work_id'],**SCOPE)['state']=='awaiting_review'


def test_historical_committed_review_keeps_idempotent_acknowledgement(review):
    store,case,reviews,_,_,request=review
    record=reviews.commit_graph(**request)
    with store.connection() as db:
        db.execute('UPDATE event_work SET case_id=NULL');db.commit()
    assert reviews.commit_graph(**request)==record
    assert store.audit(case.id)['valid'] and store.get(case.id).revision==1


def test_case_bound_enqueue_rejects_other_scope_and_unknown_case(review):
    from eightball.event_inbox import EventConflict
    store,_,_,registry,queue,_=review
    other=store.create(demo_case(),fixture=True)
    registry.bind_case(other.id,Resource(organisation_id='other',matter_id='other'))
    for case_id in (other.id,'missing-case'):
        with pytest.raises(EventConflict):queue.enqueue(**SCOPE,sequence=1,base_revision=0,case_id=case_id)
