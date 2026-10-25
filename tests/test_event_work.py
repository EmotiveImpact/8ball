from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest
from endstate.events import IncomingEvent
from eightball.event_inbox import EventInbox, EventConflict
from eightball.event_work import EventWork

SCOPE = dict(organisation_id='a', matter_id='m')


@pytest.fixture
def work(tmp_path):
    path = tmp_path/'inbox.db'
    EventInbox(path).append(IncomingEvent(**SCOPE, source_id='s',source_version='v1',
        event_id='e',kind='source_received',text='Fictional source'), **SCOPE)
    clock = [datetime(2026,10,25,tzinfo=timezone.utc)]
    queue = EventWork(path,clock=lambda:clock[0])
    return queue, queue.enqueue(**SCOPE,sequence=1,base_revision=3), clock


def test_restart_keeps_attempt_and_requires_review(work):
    queue, job, clock = work
    token = queue.claim(job,**SCOPE)
    restored = EventWork(queue.path,clock=lambda:clock[0])
    assert restored.finish(job,token,'Candidate only',**SCOPE,current_revision=3,permission_valid=True) == 'awaiting_review'
    assert restored.inspect(job,**SCOPE)['result'] == 'Candidate only'
    with pytest.raises(EventConflict): restored.claim(job,**SCOPE)


@pytest.mark.parametrize('revision,permission,state',[(4,True,'stale'),(3,False,'permission_denied')])
def test_changed_inputs_retain_output_without_publishing(work,revision,permission,state):
    queue,job,_=work;token=queue.claim(job,**SCOPE)
    assert queue.finish(job,token,'Retained failure',**SCOPE,current_revision=revision,permission_valid=permission)==state
    assert queue.inspect(job,**SCOPE)['result']=='Retained failure'


def test_cancel_blocks_late_result_and_cannot_be_reclaimed(work):
    queue,job,_=work;token=queue.claim(job,**SCOPE)
    queue.cancel(job,**SCOPE);queue.cancel(job,**SCOPE)
    with pytest.raises(EventConflict):queue.finish(job,token,'Late',**SCOPE,current_revision=3,permission_valid=True)
    with pytest.raises(EventConflict):queue.claim(job,**SCOPE)


def test_expiry_interrupts_without_automatic_retry(work):
    queue,job,clock=work;token=queue.claim(job,**SCOPE,lease_seconds=1)
    clock[0]+=timedelta(seconds=1)
    assert queue.inspect(job,**SCOPE)['state']=='interrupted'
    with pytest.raises(EventConflict):queue.finish(job,token,'Late',**SCOPE,current_revision=3,permission_valid=True)
    new=queue.enqueue(**SCOPE,sequence=1,base_revision=3)
    assert new!=job and queue.inspect(job,**SCOPE)['state']=='interrupted'


def test_concurrent_claim_has_one_winner(work):
    queue,job,_=work
    def claim(_):
        try:return queue.claim(job,**SCOPE)
        except EventConflict:return None
    with ThreadPoolExecutor(max_workers=4) as pool:tokens=list(pool.map(claim,range(8)))
    assert sum(t is not None for t in tokens)==1


def test_wrong_scope_and_token_cannot_publish(work):
    queue,job,_=work;queue.claim(job,**SCOPE)
    with pytest.raises(KeyError):queue.inspect(job,organisation_id='other',matter_id='m')
    with pytest.raises(EventConflict):queue.finish(job,'wrong','Text',**SCOPE,current_revision=3,permission_valid=True)
    assert queue.inspect(job,**SCOPE)['state']=='running'
