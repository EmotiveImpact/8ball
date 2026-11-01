"""Real host transactions with controlled HTTP, not live inference or human review."""
from copy import deepcopy
import json

import httpx
import pytest

from eightball.event_workers.operating import OperatingPlanningProcessor
from eightball.store import digest
from eightball.v2.compatible import CompatibleSession
from eightball.v2.coordinated_results import project_coordinated
from eightball.v2.operating_results import project_operating
from tests.test_compatible_integration import envelope
from tests.test_compatible_provider import configure
from tests.test_event_dispatch import dispatch, process, status
from tests.test_coordinated_planning import presentation, replace_result
from tests.test_operating_planning import outputs, specification


@pytest.fixture
def operating(dispatch, monkeypatch, request):
    d = dispatch
    configure(monkeypatch)
    calls, after, transform, ticks = [], [None], [None], [0]
    values = outputs()
    for value in values[1:4]:
        value['concerns'][0]['source_quote'] = d['receipt'].event.text
    def serve(req):
        payload = json.loads(req.content)
        value = deepcopy(values[len(calls)])
        calls.append(payload)
        if transform[0]:
            value = transform[0](value, len(calls))
        result = envelope(value, model=payload['model'])
        if after[0]:
            after[0](len(calls))
        return httpx.Response(200, json=result)
    client = httpx.Client(transport=httpx.MockTransport(serve))
    request.addfinalizer(client.close)
    processor = OperatingPlanningProcessor(specification(), allow_external=True,
        planning_session_factory=lambda **kw: CompatibleSession(client=client, **kw), timer=lambda: ticks[0])
    d['service'].cancel(case_id=d['case'].id, identity=d['operator'], work_id=d['work_id'])
    d['service'].processor = processor
    source_review = d['service'].review_source(case_id=d['case'].id, identity=d['operator'],
        sequence=d['receipt'].sequence, expected_revision=d['case'].revision,
        receipt_sha256=digest(d['receipt'].model_dump(mode='json')),
        rationale='Explicit fictional full operating-plan method with bounded unpriced role review calls.')
    d['work_id'] = d['service'].enqueue(**(d['enqueue'] | {'request_id': 'full-plan', 'review_id': source_review['id']}))
    return d, processor, calls, after, transform, ticks


def test_existing_host_full_plan_result_replays_offline_and_is_read_only(operating):
    d, processor, calls, _, _, _ = operating
    before = d['store'].audit(d['case'].id)
    process(d)
    r = json.loads(status(d)['work']['result'])
    assert r['stop_reason'] == 'completed' and len(calls) == 5
    assert r['specialist_receipts'] == []
    assert processor.max_generation_calls == 5
    for sorted_keys in (False, True):
        raw = replace_result(d, r, sort_keys=sorted_keys)
        view = presentation(d)
        p = view['operating_planning']
        assert p['available'] and p['initial']['plan'] == r['initial']['plan']
        assert p['comparison']['changed_fields'] == ['steps']
        assert p['revision']['dispositions'] == r['revision']['dispositions']
        assert p['planning_cost_status'] == 'unknown_not_provider_reported'
        assert len(p['planning_calls']) == 5
        assert project_coordinated(raw, d['receipt'], d['case'].id, d['case'].revision) is None
    assert d['store'].audit(d['case'].id) == before and len(calls) == 5


@pytest.mark.parametrize('mutation', [
    lambda r: r.update(execution_authorized=True),
    lambda r: r.update(receipt_sha256='f'*64),
    lambda r: r.update(base_revision=10),
    lambda r: r['spec']['brief'].update(outcome='An altered goal'),
    lambda r: r['initial']['plan']['steps'][0].update(title='Altered original'),
    lambda r: r['comparison'].update(improvement_established=True),
    lambda r: r['challenges'][0]['review']['concerns'][0].update(why_it_matters='Altered review'),
    lambda r: r['revision']['dispositions'].pop(),
    lambda r: r['final_synthesis'].update(objections_resolved=True),
    lambda r: r['attempts'][0].update(input_sha256='0'*64),
    lambda r: r['attempts'][0].update(validated=False),
    lambda r: r['attempts'].append(deepcopy(r['attempts'][-1])),
    lambda r: r['planning_receipt']['calls'][0].update(raw_content='{}'),
    lambda r: r['planning_receipt']['calls'][0].pop('request_sha256'),
    lambda r: r['planning_receipt'].update(requested_model='unapproved-substitute'),
])
def test_corrupt_report_keeps_raw_output_without_interpreting_it(operating, mutation):
    d, _, _, _, _, _ = operating
    process(d)
    r = json.loads(status(d)['work']['result'])
    mutation(r)
    raw = replace_result(d, r)
    view = presentation(d)
    assert view['operating_planning'] == {'available': False}
    assert view['original_result'] == raw


@pytest.mark.parametrize('stage', range(1, 6))
def test_failed_model_outputs_remain_visible_and_are_not_retried(operating, stage):
    d, _, calls, _, transform, _ = operating
    transform[0] = lambda value, index: value | {'unexpected': 'rejected'} if index == stage else value
    process(d)
    report = json.loads(status(d)['work']['result'])
    assert report['stop_reason'] != 'completed' and len(calls) == stage
    p = presentation(d)['operating_planning']
    assert p['available'] and p['final_synthesis'] is None
    assert p['attempts'][-1]['output']['unexpected'] == 'rejected'


def test_access_revoked_during_role_review_cannot_publish(operating):
    d, _, calls, after, _, _ = operating
    after[0] = lambda count: d['registry'].revoke('worker') if count == 2 else None
    process(d)
    assert len(calls) == 2
    assert status(d)['work']['result'] is None


def test_time_budget_no_further_calls_or_completed_synthesis(operating):
    d, _, calls, after, _, ticks = operating
    after[0] = lambda count: ticks.__setitem__(0, 121) if count == 2 else None
    process(d)
    report = json.loads(status(d)['work']['result'])
    assert len(calls) == 2 and report['stop_reason'] == 'time_budget'
    assert report['final_synthesis'] is None
    assert presentation(d)['operating_planning']['available']


def test_external_permission_is_required_and_legacy_config_is_distinct(operating):
    d, processor, *_ = operating
    with pytest.raises(PermissionError):
        OperatingPlanningProcessor(specification(), allow_external=False)
    with pytest.raises(PermissionError):
        processor(d['receipt'], d['case'])
    assert isinstance(processor.configuration_sha256, str)
