from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from fastapi.testclient import TestClient
import jwt
import pytest

from eightball.agency_access import AccessRegistry, AgencyAccess
from eightball.authorisation import Grant, Identity, Operation, Resource
from eightball.api import make_app
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case


@pytest.fixture
def fixture(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_bytes(serialization.Encoding.PEM,
                                          serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    issuer = 'https://identity.fixture.example'
    now = datetime.now(timezone.utc)
    claims = dict(iss=issuer, sub='operator', aud='8ball', iat=now, exp=now+timedelta(minutes=5))
    legacy = LegacyStore(str(tmp_path/'cases.db'))
    store = Store(legacy.path)
    own = store.create(demo_case(), fixture=True)
    other = store.create(demo_case(), fixture=True)
    registry = AccessRegistry(tmp_path/'access.db')
    scope = Resource(organisation_id='agency-a', matter_id='matter-a')
    registry.bind_case(own.id, scope)
    registry.bind_case(other.id, Resource(organisation_id='agency-b', matter_id='matter-b'))
    registry.add_grant('read', Grant(identity=Identity(issuer=issuer, subject='operator'),
        resource=scope, operations=frozenset({Operation.READ}), valid_from=now-timedelta(minutes=1),
        expires_at=now+timedelta(hours=1)))
    guard = AgencyAccess(registry, issuer=issuer, audience='8ball', public_key=public)
    client = TestClient(make_app(legacy, 'unused-local-token-with-32-characters', agency_access=guard))
    client.headers['Authorization'] = 'Bearer '+jwt.encode(claims,key,algorithm='RS256')
    return client, registry, own, other, key, claims


def test_api_scope_and_persistent_revocation(fixture):
    client, registry, own, other, _, _ = fixture
    assert client.get('/api/v2/cases/'+own.id).status_code == 200
    assert client.get('/api/v2/cases/'+other.id).status_code == 403
    assert client.get('/api/v2/cases/'+own.id+'/export').status_code == 403
    assert client.get('/api/v2/cases').status_code == 403
    assert client.get('/api/cases').status_code == 403
    AccessRegistry(registry.path).revoke('read')
    assert client.get('/api/v2/cases/'+own.id).status_code == 403


@pytest.mark.parametrize('suffix', ['commands','search','analyse','analysis-jobs','simulate'])
def test_unsupported_mutation_and_model_paths_deny(fixture, suffix):
    client, _, own, _, _, _ = fixture
    assert client.post('/api/v2/cases/'+own.id+'/'+suffix,json={}).status_code == 403


@pytest.mark.parametrize('change', [{'iss':'https://other.example'}, {'aud':'other'},
                                  {'exp':0}, {'sub':''}])
def test_bad_identity_claims_fail_before_data_access(fixture,change):
    client, _, own, _, key, claims = fixture
    client.headers['Authorization']='Bearer '+jwt.encode(claims|change,key,algorithm='RS256')
    assert client.get('/api/v2/cases/'+own.id).status_code == 401


def test_wrong_signing_key_and_algorithm_are_rejected(fixture):
    client, _, own, _, _, claims = fixture
    wrong = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    for token in (jwt.encode(claims,wrong,algorithm='RS256'),
                  jwt.encode(claims,'fixture-symmetric-key',algorithm='HS256')):
        client.headers['Authorization']='Bearer '+token
        assert client.get('/api/v2/cases/'+own.id).status_code == 401


@pytest.fixture
def events(fixture,tmp_path):
    from endstate.events import IncomingEvent
    from eightball.event_inbox import EventInbox
    from eightball.event_work import EventWork
    original,_,own,other,key,claims=fixture
    legacy=LegacyStore(str(tmp_path/'cases.db'));store=Store(legacy.path)
    registry=AccessRegistry(store.path);scope=Resource(organisation_id='agency-a',matter_id='matter-a')
    registry.bind_case(own.id,scope);registry.bind_case(other.id,Resource(organisation_id='agency-b',matter_id='matter-b'))
    identity=Identity(issuer=claims['iss'],subject=claims['sub']);now=datetime.now(timezone.utc)
    for name,op in [('read',Operation.READ),('write',Operation.WRITE)]:
        registry.add_grant(name,Grant(identity=identity,resource=scope,operations=frozenset({op}),
            valid_from=now-timedelta(minutes=1),expires_at=now+timedelta(hours=1)))
    public=key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    guard=AgencyAccess(registry,issuer=claims['iss'],audience='8ball',public_key=public)
    client=TestClient(make_app(legacy,'unused-local-token-with-32-characters',agency_access=guard))
    client.headers['Authorization']=original.headers['Authorization']
    args=dict(organisation_id='agency-a',matter_id='matter-a')
    EventInbox(store.path).append(IncomingEvent(**args,source_id='source',source_version='1',event_id='source-event',
        kind='proposal_received',base_revision=0,text='Fictional source for reviewed change'),**args)
    queue=EventWork(store.path);work=queue.enqueue(**args,sequence=1,base_revision=0,case_id=own.id)
    token=queue.claim(work,**args);queue.finish(work,token,'Original proposed change',**args,current_revision=0,permission_valid=True)
    graph=own.graph.model_dump(mode='json');graph['actions'][0]['cost']+=10
    body=dict(command=dict(event_id='review-api',expected_revision=0,kind='replace_graph',payload={'graph':graph}),
              rationale='Reviewed this cost against fictional source.')
    return client,registry,store,own,other,work,body


def test_verified_event_review_and_local_notice_api(events):
    client,_,store,own,_,work,body=events
    path=f'/api/v2/cases/{own.id}/event-work/{work}'
    view=client.get(path)
    assert view.status_code==200 and view.json()['reviewable']
    assert view.json()['original_result']=='Original proposed change'
    assert 'token_hash' not in view.text
    response=client.post(path+'/review',json=body)
    assert response.status_code==200 and response.json()['committed_revision']==1
    assert response.json()['request']['reviewer']=={'issuer':'https://identity.fixture.example','subject':'operator'}
    assert client.post(path+'/review',json=body).json()==response.json()
    assert not client.get(path).json()['reviewable']
    notices=f'/api/v2/cases/{own.id}/change-notices'
    notice=client.post(notices+'/pull',json={})
    assert notice.status_code==200 and notice.json()['revision']==1
    ack=client.post(notices+f"/{notice.json()['id']}/acknowledge",json={})
    assert ack.status_code==200 and ack.json()=={'delivery_acknowledged':True,'action_approved':False}
    assert client.post(notices+'/pull',json={}).json() is None
    assert store.audit(own.id)['valid']


@pytest.mark.parametrize('grant',['read','write'])
def test_review_api_requires_read_and_write_even_on_duplicate(events,grant):
    client,registry,store,own,_,work,body=events
    path=f'/api/v2/cases/{own.id}/event-work/{work}/review'
    assert client.post(path,json=body).status_code==200
    registry.revoke(grant)
    assert client.post(path,json=body).status_code==403
    assert store.get(own.id).revision==1


def test_event_api_cross_matter_unknown_and_injected_identity(events):
    client,_,store,own,other,work,body=events
    assert client.get(f'/api/v2/cases/{other.id}/event-work/{work}').status_code==403
    assert client.get(f'/api/v2/cases/{own.id}/event-work/missing').status_code==404
    path=f'/api/v2/cases/{own.id}/event-work/{work}/review'
    assert client.post(path,json=body|{'reviewer':{'subject':'admin'}}).status_code==422
    assert store.get(own.id).revision==0
    assert client.post(f'/api/v2/cases/{own.id}/commands',json=body['command']).status_code==403


@pytest.mark.parametrize("revoked_grant", ["read", "write"])
def test_event_review_rechecks_revocation_after_route_guard(events,monkeypatch,revoked_grant):
    client,registry,store,own,_,work,body=events
    original=registry.allowed
    def revoke_after_guard(*args,**kwargs):
        allowed=original(*args,**kwargs);registry.revoke(revoked_grant);return allowed
    monkeypatch.setattr(registry,'allowed',revoke_after_guard)
    response=client.post(f'/api/v2/cases/{own.id}/event-work/{work}/review',json=body)
    assert response.status_code==403 and store.get(own.id).revision==0


def test_event_api_stale_results_cannot_commit(events):
    from eightball.v2.commands import Command
    client,_,store,own,_,work,body=events
    store.change(own.id,Command(event_id='new',expected_revision=0,kind='metadata',payload={'budget':123}))
    path=f'/api/v2/cases/{own.id}/event-work/{work}'
    assert not client.get(path).json()['reviewable']
    assert client.post(path+'/review',json=body).status_code==409
    assert store.get(own.id).revision==1


def test_event_routes_are_absent_for_unshared_registry(fixture):
    client,_,own,_,_,_=fixture
    assert client.get(f'/api/v2/cases/{own.id}/event-work/any').status_code==404


def test_cancelled_attempt_and_revoked_notice_acknowledgement(events):
    from eightball.event_work import EventWork
    client,registry,store,own,_,work,body=events
    EventWork(store.path).cancel(work,organisation_id='agency-a',matter_id='matter-a')
    path=f'/api/v2/cases/{own.id}/event-work/{work}'
    assert client.get(path).json()['state']=='cancelled'
    assert client.post(path+'/review',json=body).status_code==409
    registry.revoke('read')
    assert client.post(f'/api/v2/cases/{own.id}/change-notices/1/acknowledge',json={}).status_code==403
    assert store.get(own.id).revision==0


def test_event_api_not_enabled_by_local_operator_token(tmp_path):
    client=TestClient(make_app(LegacyStore(str(tmp_path/'local.db')),'operator-token-with-at-least-32-characters'))
    client.headers['Authorization']='Bearer operator-token-with-at-least-32-characters'
    assert client.get('/api/v2/cases/example/event-work/example').status_code==404
