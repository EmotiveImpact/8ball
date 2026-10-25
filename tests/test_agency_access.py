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
