"""Typed result compatibility, not model-quality or public-service acceptance."""
from copy import deepcopy
import json
from datetime import timedelta
import pytest
from pydantic import ValidationError
from endstate.api import PlanRequest, PlanResponse, calculate
from endstate.results import validate_plan, PLAN_ADAPTER
from eightball.v2.playbooks import demo_case, get_playbook
from eightball.v2.planner import to_snapshot
from eightball.models import utcnow


def response():
    c=demo_case();return calculate(PlanRequest(snapshot=to_snapshot(c),as_of=utcnow()))


def test_result_schema_fully_describes_nested_routes_and_briefing():
    schema=PlanResponse.model_json_schema()
    for name in ['RouteResult','PlanResult','ActionState','BriefingResult','QuestionResult','ScheduleEntry']:
        assert name in schema['$defs']
        assert schema['$defs'][name]['additionalProperties'] is False
    assert schema['$defs']['RouteResult']['properties']['minutes']['anyOf']


def test_json_roundtrip_and_mapping_api_stay_exact():
    r=response();raw=r.model_dump(mode='json')
    again=PlanResponse.model_validate_json(r.model_dump_json())
    assert again.model_dump(mode='json')==raw
    assert isinstance(r.plan,dict) and isinstance(r.plan['routes'][0],dict)
    assert validate_plan(r.plan)==r.plan
    assert r.plan is not again.plan


@pytest.mark.parametrize('mutator',[
    lambda p:p.update(outcome_evidenced='yes'),
    lambda p:p.update(computed_at='2026-09-24T00:00:00'),
    lambda p:p.update(revision=True),
    lambda p:p['routes'][0].update(success_probability=.99),
    lambda p:p['routes'][0].update(minutes=float('nan')),
    lambda p:p['routes'][0].update(total_cost=-1),
    lambda p:p['routes'][0].update(risk=8),
    lambda p:p['routes'][0].update(provisional='true'),
    lambda p:p['routes'][0]['schedule'][0].update(wait_known='yes'),
    lambda p:p['routes'][0]['schedule'][0].update(active_end_minute=-4),
    lambda p:p['routes'][0]['evidence_coverage'].update(supported=True),
    lambda p:p['routes'][0]['dependencies'].append(['a']),
])
def test_invalid_nested_output_rejected(mutator):
    data=deepcopy(response().plan);mutator(data)
    with pytest.raises((ValueError,ValidationError)):validate_plan(data)


@pytest.mark.parametrize('mutator',[
    lambda p:p['routes'].append(deepcopy(p['routes'][0])),
    lambda p:p['objective_failures'].append('not-an-objective'),
    lambda p:p['action_states']['preserve'].update(id='other'),
    lambda p:p['routes'][0]['used_conditions'].append('missing'),
    lambda p:p['routes'][0]['actions'].append('phantom'),
    lambda p:p['routes'][0]['schedule'].reverse(),
    lambda p:p['routes'][0]['schedule'][0].update(end_minute=0),
    lambda p:p['routes'][0].update(total_cost=1),
    lambda p:p['routes'][0]['evidence_coverage'].update(supported=999999),
    lambda p:p['routes'][0]['objectives'].clear(),
    lambda p:p['routes'][0]['dependencies'].append(['missing','missing']),
    lambda p:p['routes'][0]['ready'].append('missing'),
])
def test_cross_field_inconsistency_rejected(mutator):
    data=deepcopy(response().plan);mutator(data)
    with pytest.raises(ValueError):validate_plan(data)


@pytest.mark.parametrize('mutator',[
    lambda d:d.update(revision=d['revision']+1),
    lambda d:d['briefing']['routes'].clear(),
    lambda d:d['briefing']['now'].append({'id':'missing','title':'Bad','status':'ready'}),
    lambda d:d['briefing']['questions'][0]['route_ids'].append('missing'),
])
def test_response_cannot_mix_snapshots(mutator):
    data=response().model_dump(mode='json');mutator(data)
    with pytest.raises(ValueError):PlanResponse.model_validate(data)


def test_caller_mutation_does_not_change_input_or_other_response():
    c=demo_case();s=to_snapshot(c);before=s.model_dump(mode='json')
    a=calculate(PlanRequest(snapshot=s,as_of=utcnow()))
    b=calculate(PlanRequest(snapshot=s,as_of=utcnow()))
    a.plan['states'].clear();a.briefing['routes'].clear()
    assert s.model_dump(mode='json')==before and b.plan['states'] and b.briefing['routes']


def test_no_assurance_number_exists_in_result_schema():
    text=json.dumps(PlanResponse.model_json_schema())
    assert 'success_probability' not in text and 'likelihood' not in text
