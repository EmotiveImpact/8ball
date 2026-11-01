from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
import sqlite3

import pytest
from pydantic import ValidationError

from endstate.events import IncomingEvent
from eightball.event_inbox import EventInbox, EventConflict


def event(**kwargs):
    return IncomingEvent(**(dict(organisation_id='a', matter_id='m', source_id='s',
        source_version='v1', event_id='e', kind='source_received', text='Fictional source') | kwargs))


def append(inbox, value):
    return inbox.append(value, organisation_id='a', matter_id='m')


def test_duplicate_survives_restart_without_new_receipt_or_authority(tmp_path):
    path=tmp_path/'inbox.db'; inbox=EventInbox(path)
    first=append(inbox,event())
    again=append(EventInbox(path),event())
    assert first == again and first.sequence == 1
    assert first.event.occurred_at is None and first.command_authority is False
    assert first.event.review_status == 'pending'
    assert len(inbox.read(organisation_id='a',matter_id='m')) == 1


def test_conflicting_retry_rolls_back_and_preserves_original(tmp_path):
    inbox=EventInbox(tmp_path/'inbox.db'); first=append(inbox,event())
    for changes in ({'text':'Changed'}, {'source_version':'v2'}, {'base_revision':9}):
        with pytest.raises(EventConflict): append(inbox,event(**changes))
    assert inbox.read(organisation_id='a',matter_id='m') == [first]
    assert append(inbox,event(event_id='next')).sequence == 2


def test_concurrent_duplicate_is_single_durable_event(tmp_path):
    inbox=EventInbox(tmp_path/'inbox.db')
    with ThreadPoolExecutor(max_workers=8) as pool:
        receipts=list(pool.map(lambda _:append(inbox,event()), range(16)))
    assert all(r == receipts[0] for r in receipts)


def test_delayed_events_keep_occurrence_time_and_arrival_order(tmp_path):
    inbox=EventInbox(tmp_path/'inbox.db'); now=datetime.now(timezone.utc)
    append(inbox,event(occurred_at=now))
    append(inbox,event(event_id='late',occurred_at=now-timedelta(days=2)))
    page=inbox.read(organisation_id='a',matter_id='m',after=1,limit=1)
    assert page[0].sequence == 2 and page[0].event.event_id == 'late'
    assert page[0].event.occurred_at == now-timedelta(days=2)


def test_scope_is_checked_and_queries_never_cross_it(tmp_path):
    inbox=EventInbox(tmp_path/'inbox.db'); append(inbox,event())
    with pytest.raises(EventConflict): append(inbox,event(organisation_id='b'))
    assert inbox.read(organisation_id='b',matter_id='m') == []
    assert inbox.read(organisation_id='a',matter_id='other') == []


@pytest.mark.parametrize('changes',[{'review_status':'accepted'}, {'command_authority':True},
    {'kind':'approve'}, {'occurred_at':datetime(2026,1,1)}, {'base_revision':True}])
def test_incoming_text_cannot_supply_review_or_command_authority(changes):
    with pytest.raises(ValidationError): event(**changes)


def test_corrupt_record_fails_visibly(tmp_path):
    inbox=EventInbox(tmp_path/'inbox.db'); append(inbox,event())
    with sqlite3.connect(inbox.path) as db:
        db.execute("UPDATE incoming_events SET body='{}'")
    with pytest.raises(EventConflict): inbox.read(organisation_id='a',matter_id='m')
    with pytest.raises(EventConflict): append(inbox,event())
