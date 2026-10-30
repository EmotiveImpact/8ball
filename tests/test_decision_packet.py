"""Verified, scoped, read-only local packets; no client sharing or agency bypass."""
from datetime import timedelta
import json
import sqlite3

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from endstate.decision_packet import Selection, DisclosureDenied, project
from eightball.api import make_app
from eightball.store import Store as LegacyStore, Conflict, digest
from eightball.v2.commands import Command
from eightball.v2.decision_packet import DecisionPackets, Request, local_operator_scope
from eightball.v2.rehearsal import Rehearsals
from tests.test_rehearsal import env, save, draft, NOW, TOKEN


@pytest.fixture
def packet_env(env, monkeypatch):
    monkeypatch.setattr('eightball.v2.decision_packet.utcnow',lambda:NOW)
    store,case,rehearsals = env
    first,_ = save(rehearsals,case)
    history = rehearsals.view(case.id)
    request = Request(expected_revision=case.revision,expected_sequence=1,
                      expected_head_sha256=history['head_hash'],brief_sha256=first['record']['brief']['brief_sha256'])
    return store,case,rehearsals,request


@pytest.mark.parametrize('mode',['operator_review','reference_index'])
def test_verified_packet_no_mutation_and_explicit_omissions(packet_env,mode):
    store,case,_,request = packet_env
    before = store.audit(case.id)
    request = Request(**{**request.model_dump(),'mode':mode,'references':['case:summary'] if mode == 'reference_index' else []})
    result = DecisionPackets(store,policy=local_operator_scope).read(case.id,request)
    assert result['packet_sha256'] == digest({k:v for k,v in result.items() if k != 'packet_sha256'})
    assert not result['complete_audit'] and not result['persisted'] and not result['execution_authorized'] and not result['facts_attested']
    assert result['omissions'] and not result['missing_predecessors']
    assert result['history_head_sha256'] == request.expected_head_sha256
    assert store.audit(case.id) == before
    if mode == 'reference_index':
        assert result['brief'] is None and result['predecessors'] is None
        assert len(result['references']) == 1
        text = json.dumps(result)
        for private in (case.summary,case.desired_outcome,'Fictional supplier','Supply may remain available.'):
            assert private not in text
        assert set(result['references'][0]) == {'reference','sha256'}
    else:
        result['brief']['draft']['contributions'][0]['text'] = 'Changed local copy'
        assert store.audit(case.id) == before


@pytest.mark.parametrize('mode',['operator_review','reference_index'])
def test_server_policy_deny_and_reference_revocation(packet_env,mode):
    store,case,_,request = packet_env
    if mode == 'reference_index':
        request = Request(**{**request.model_dump(),'mode':mode,'references':['case:summary']})
    for scope in (None,set(),{'case:desired_outcome'}):
        with pytest.raises(DisclosureDenied):DecisionPackets(store,policy=lambda db,c:scope).read(case.id,request)
    if mode == 'reference_index':
        result = DecisionPackets(store,policy=lambda db,c:{'case:summary'}).read(case.id,request)
        assert result['brief'] is None


@pytest.mark.parametrize('kind',['revision','sequence','head','missing_brief','missing_ref','expired','future','case_change','history_change'])
def test_stale_or_missing_inputs_fail_closed(packet_env,monkeypatch,kind):
    store,case,service,request = packet_env
    if kind == 'revision':request.expected_revision += 1
    elif kind == 'sequence':request.expected_sequence += 1
    elif kind == 'head':request.expected_head_sha256 = '0'*64
    elif kind == 'missing_brief':request.brief_sha256 = '0'*64
    elif kind == 'missing_ref':request = Request(**{**request.model_dump(),'mode':'reference_index','references':['source:missing']})
    elif kind in ('expired','future'):
        monkeypatch.setattr('eightball.v2.decision_packet.utcnow',lambda:NOW+timedelta(minutes=16) if kind=='expired' else NOW-timedelta(seconds=1))
    elif kind == 'case_change':
        store.change(case.id,Command(event_id='change',expected_revision=0,kind='metadata',payload={'summary':'New information'}))
        request.expected_revision = 1
    else:save(service,case,event_id='another')
    with pytest.raises((Conflict,ValueError)):DecisionPackets(store,policy=local_operator_scope).read(case.id,request)


def test_current_packet_retains_predecessor_pointers(packet_env):
    store,case,service,request = packet_env
    data = draft();data['predecessor_sha256'] = request.brief_sha256;data['run_id'] = 'recheck'
    second,_ = save(service,case,data,event_id='second')
    history = service.view(case.id)
    latest = Request(expected_revision=0,expected_sequence=2,expected_head_sha256=history['head_hash'],brief_sha256=second['record']['brief']['brief_sha256'])
    packet = DecisionPackets(store,policy=local_operator_scope).read(case.id,latest)
    assert packet['predecessors'] == [{'brief_sha256':request.brief_sha256,'sequence':1,'case_revision':0,'content_included':False}]


@pytest.mark.parametrize('mutation',['missing','cycle','digest','case_history'])
def test_corrupt_or_missing_lineage_not_silently_exported(packet_env,mutation):
    store,case,service,request = packet_env
    data = draft();data['predecessor_sha256'] = request.brief_sha256;data['run_id'] = 'recheck'
    second,_ = save(service,case,data,event_id='second')
    history = service.view(case.id)
    latest = Request(expected_revision=0,expected_sequence=2,expected_head_sha256=history['head_hash'],brief_sha256=second['record']['brief']['brief_sha256'])
    with store.connection() as db:
        if mutation == 'missing':db.execute('DELETE FROM v2_rehearsals WHERE case_id=? AND sequence=1',(case.id,))
        elif mutation == 'case_history':db.execute('DELETE FROM v2_events WHERE case_id=?',(case.id,))
        else:
            row = db.execute('SELECT record FROM v2_rehearsals WHERE case_id=? AND sequence=2',(case.id,)).fetchone()
            value = json.loads(row['record'])
            if mutation == 'cycle':value['brief']['draft']['predecessor_sha256'] = latest.brief_sha256
            else:value['brief']['brief_sha256'] = '0'*64
            db.execute('UPDATE v2_rehearsals SET record=?,hash=? WHERE case_id=? AND sequence=2',(json.dumps(value),digest(value),case.id))
        db.commit()
    with pytest.raises(ValueError,match='history'):DecisionPackets(store,policy=local_operator_scope).read(case.id,latest)


def test_permission_change_detected_even_when_policy_mutates_same_set(packet_env):
    store,case,_,request = packet_env
    allowed = local_operator_scope(None,case)
    calls = []
    def policy(db,c):
        calls.append(1)
        if len(calls) == 2:allowed.clear()
        return allowed
    with pytest.raises(DisclosureDenied,match='changed'):DecisionPackets(store,policy=policy).read(case.id,request)
    assert len(calls) == 2


def test_policy_transaction_serializes_revocation(packet_env):
    store,case,_,request = packet_env
    calls = []
    def policy(db,c):
        assert db.in_transaction
        with sqlite3.connect(store.path,timeout=0) as another:
            with pytest.raises(sqlite3.OperationalError,match='locked'):another.execute('BEGIN IMMEDIATE')
        calls.append(1)
        return local_operator_scope(db,c)
    DecisionPackets(store,policy=policy).read(case.id,request)
    assert len(calls) == 2


def test_api_auth_and_forbidden_client_scope(packet_env,monkeypatch):
    store,case,_,request = packet_env
    with TestClient(make_app(LegacyStore(store.path),TOKEN)) as client:
        path = f'/api/v2/cases/{case.id}/plan-reviews/rehearsals/packet'
        payload = request.model_dump(mode='json')
        assert client.post(path,json=payload).status_code == 401
        client.headers['Authorization'] = 'Bearer '+TOKEN
        assert client.post(path,json=payload).status_code == 200
        assert client.post(path,json={**payload,'allowed_references':['case:summary']}).status_code == 422
        assert client.post(path,json={**payload,'expected_sequence':99}).status_code == 409
    monkeypatch.setattr('eightball.v2.decision_packet.local_operator_scope',lambda db,c:None)
    with TestClient(make_app(LegacyStore(store.path),TOKEN)) as client:
        client.headers['Authorization'] = 'Bearer '+TOKEN
        assert client.post(path,json=payload).status_code == 403


def test_packets_and_local_history_unavailable_to_agency(tmp_path):
    from tests.agency_fixture import make_fixture
    from eightball.oidc.login import SESSION_COOKIE
    f = make_fixture(tmp_path)
    paths = {r.path for r in f.app.routes}
    assert '/api/v2/cases/{case_id}/plan-reviews/rehearsals/packet' not in paths
    assert '/api/v2/cases/{case_id}/plan-reviews/rehearsals/check' not in paths
    with TestClient(f.app,base_url='https://testserver') as client:
        client.cookies.set(SESSION_COOKIE,f.cookies['author'])
        path = f'/api/v2/cases/{f.case.id}/export'
        response = client.get(path)
        assert response.status_code == 200,response.text
        save(Rehearsals(f.store),f.case)
        assert client.get(path).status_code == 403


@pytest.mark.parametrize('value',[
    {'mode':'reference_index'}, {'mode':'operator_review','references':['case:summary']},
    {'mode':'reference_index','references':['case:summary','case:summary']},
    {'mode':'public'}, {'mode':'reference_index','references':['source:../bad']}])
def test_invalid_selection(value):
    with pytest.raises(ValidationError):Selection(**value)


def test_projection_revalidates_mutable_models():
    selection = Selection(mode='reference_index',references=['case:summary'])
    selection.references.append('case:summary')
    with pytest.raises(ValidationError):project({'reference_hashes':{'case:summary':'0'*64}},selection,{'case:summary'})
