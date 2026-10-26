import base64
from datetime import timedelta
import json
import sqlite3
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from tests.agency_fixture import make_fixture
from eightball.agency_host import _authority, ROUTE_OPERATIONS, OPERATIONS_PREFIX
from eightball.authorisation import Grant, Operation
from eightball.oidc.login import SESSION_COOKIE
from eightball.v2.request_limits import body_limit


@pytest.fixture
def env(tmp_path):
    return make_fixture(tmp_path)


def browser(env, who='author'):
    return TestClient(env.app, base_url='https://testserver',
        cookies={SESSION_COOKIE: env.cookies[who]}, headers={'Origin': 'https://testserver'})


def upload(env, client, content=b'Fictional source, not an observation.'):
    response = client.post(f'/api/v2/cases/{env.case.id}/vault', json={
        'content_base64': base64.b64encode(content).decode(), 'filename': 'fictional.txt',
        'media_type': 'text/plain', 'retain_until': (env.now+timedelta(days=8)).isoformat(),
        'command_id': uuid4().hex})
    assert response.status_code == 200, response.text
    return response.json()


def release(env, client, obj):
    response = client.post(f'/api/v2/cases/{env.case.id}/vault/{obj["object_id"]}/scan', json={
        'expected_revision': obj['vault_revision'], 'command_id': uuid4().hex})
    assert response.status_code == 200, response.text
    return response.json()


def test_all_mounted_agency_routes_have_exact_reviewed_mapping(env):
    assert env.host.events.inference_slot is env.app.state.analysis_jobs.slot
    for route in env.app.routes:
        path = getattr(route, 'path', '')
        if '/vault' in path or '/collaboration' in path or '/operations' in path or '/knowledge' in path or '/domain-packs' in path or '/agency-objects/' in path:
            for method in route.methods:
                assert (method, path) in env.host.access.route_operations, (method, path)
    assert ('GET', OPERATIONS_PREFIX) in env.host.access.route_operations


def test_missing_configuration_and_local_token_never_authorise_agency_data(env, tmp_path):
    from eightball.api import make_app
    from eightball.store import Store
    local = TestClient(make_app(Store(str(tmp_path/'local.db')), 'x'*40))
    assert local.get('/api/v2/agency-status').json()['configured'] is False
    assert local.get('/v2/agency.html').status_code == 200
    assert local.get('/api/v2/cases/fictional/vault', headers={'Authorization': 'Bearer '+'x'*40}).status_code == 404
    with browser(env) as client:
        assert client.get(f'/api/v2/cases/{env.case.id}/vault', headers={'Authorization': 'Bearer '+'fictional-local-operator-token-not-agency'*2}).status_code == 401
        assert client.get(f'/api/v2/cases/{env.case.id}/unmapped-route').status_code == 404
        response = client.get('/v2/agency.html')
        assert "script-src 'self'" in response.headers['Content-Security-Policy']
        assert "'unsafe-inline'" not in response.headers['Content-Security-Policy']


def test_real_vault_scan_binding_and_knowledge_routes_share_source_gates(env):
    with browser(env) as client:
        obj = upload(env, client)
        path = f'/api/v2/cases/{env.case.id}/agency-objects/{obj["object_id"]}'
        assert client.get(path).status_code in (403, 409)
        obj = release(env, client, obj)
        binding = client.get(path)
        assert binding.status_code == 200, binding.text
        assert binding.json()['sources'][0]['sha256'] == obj['sha256']
        assert client.get(f'/api/v2/cases/{env.case.id}/knowledge').json()['items'] == []
        draft = dict(kind='precedent', title='Fictional reference', summary='Only a source-local hypothesis',
            assumptions=['May be inapplicable'], authority_requirements=['Current mandate'],
            confirmation_criteria=['Independent observation'], limitations=['Not verified'],
            sources=[dict(source_id=obj['object_id'], sha256=obj['sha256'], start=0, end=16, quote='Fictional source')])
        result = client.post(f'/api/v2/cases/{env.case.id}/knowledge/reference', json=dict(expected_revision=0,
            expected_case_revision=env.case.revision, request_id=uuid4().hex, draft=draft))
        assert result.status_code == 200, result.text
        assert client.get(f'/api/v2/cases/{env.case.id}/knowledge?q=Fictional').json()['items'] == []
        current = client.get(f'/api/v2/cases/{env.case.id}/knowledge/reference').json()
        with browser(env, 'reviewer') as reviewer:
            result = reviewer.post(f'/api/v2/cases/{env.case.id}/knowledge/reference', json=dict(expected_revision=current['revision'],
                expected_case_revision=env.case.revision, request_id=uuid4().hex,
                review=dict(version=current['item']['version'], draft_sha256=current['item']['draft_sha256'],
                            verdict='use_as_reference', rationale='Exact source-local fictional reference review', specialist_scope='Fictional engineering')))
            assert result.status_code == 200, result.text
        assert client.get(f'/api/v2/cases/{env.case.id}/knowledge?q=Fictional').json()['items']
        env.policy['allow'] = False
        assert client.get(path).status_code == 403
        assert client.get(f'/api/v2/cases/{env.case.id}/knowledge/reference').status_code in (403, 404)


def test_cross_tenant_case_object_and_operations_identifiers_deny_without_content(env):
    with browser(env) as client:
        obj = release(env, client, upload(env, client))
        for path in [f'/api/v2/cases/{env.other.id}/vault',
                     f'/api/v2/cases/{env.other.id}/agency-objects/{obj["object_id"]}',
                     f'/api/v2/cases/{env.other.id}/knowledge',
                     f'/api/v2/organisations/fictional-other/matters/fictional-other/cases/{env.case.id}/operations']:
            response = client.get(path)
            assert response.status_code == 403, response.text
            assert 'Fictional source' not in response.text


def test_long_scan_after_session_logout_cannot_release_original(env):
    with browser(env) as client:
        obj = upload(env, client)
        env.scanner.after = lambda: env.sessions.logout(env.cookies['author'])
        response = client.post(f'/api/v2/cases/{env.case.id}/vault/{obj["object_id"]}/scan',
            json={'expected_revision': obj['vault_revision'], 'command_id': uuid4().hex})
        assert response.status_code in (401, 403)
        with sqlite3.connect(env.path) as db:
            assert db.execute('SELECT status FROM vault_state WHERE object_id=?', (obj['object_id'],)).fetchone()[0] != 'released'


def test_cookie_mutations_require_exact_origin_and_no_implicit_provider_work(env):
    with TestClient(env.app, base_url='https://testserver', cookies={SESSION_COOKIE: env.cookies['author']}) as client:
        path = f'/api/v2/cases/{env.case.id}/incoming-events'
        assert client.post(path, json={}).status_code == 403
        assert client.post(path, json={}, headers={'Origin': 'https://foreign.invalid'}).status_code == 403
        assert client.post(path, json={}, headers={'Origin': 'https://testserver'}).status_code == 422
        assert env.host.events.processor is None


def test_advertised_max_upload_and_exact_actual_body_limits(env):
    with browser(env) as client:
        obj = upload(env, client, b'x'*262144)
        assert obj['size_bytes'] == 262144
        path = f'/api/v2/cases/{env.case.id}/vault'
        assert body_limit(path) == 400000
        assert body_limit(path+'/arbitrary') == 300000
        assert client.post(path, content=b' '*400001, headers={'Content-Type': 'application/json'}).status_code == 413
        assert client.post(path, content=b' '*350000, headers={'Content-Type': 'application/json', 'Content-Length': '1'}).status_code == 413
        assert client.post(path, content=b'{}', headers={'Content-Type': 'application/json', 'Content-Length': '20'}).status_code == 413


def test_absent_keys_scanner_source_policy_and_capability_fail_closed(env):
    with browser(env) as client:
        obj = upload(env, client)
        env.host.vault.scanner = None
        assert client.post(f'/api/v2/cases/{env.case.id}/vault/{obj["object_id"]}/scan', json={
            'expected_revision': obj['vault_revision'], 'command_id': uuid4().hex}).status_code == 503
        env.host.vault.scanner = env.scanner
        obj = release(env, client, obj)
        env.host.source_consent = None
        assert client.get(f'/api/v2/cases/{env.case.id}/agency-objects/{obj["object_id"]}').status_code == 403
        env.host.keys = None
        assert client.get(f'/api/v2/cases/{env.case.id}/vault').status_code == 503
        with sqlite3.connect(env.path) as db:
            db.execute("UPDATE agency_capabilities SET revoked=1 WHERE capability='internal.read'")
        assert client.get(f'/api/v2/cases/{env.case.id}').status_code == 403


def test_projection_client_never_gets_internal_case_or_source_access(env):
    with browser(env) as author, browser(env, 'reviewer') as reviewer:
        obj = release(env, author, upload(env, author))
        oid = obj['object_id']
        resource = env.scope.model_copy(update={'object_id': oid})
        env.registry.add_grant('client-object', Grant(identity=env.identities['client'], resource=resource,
            operations=frozenset({Operation.READ}), valid_from=env.now-timedelta(minutes=1), expires_at=env.now+timedelta(hours=1)))
        env.host.grant_capability('client-projection', identity=env.identities['client'], resource=resource,
            capability='projection.client', valid_from=env.now-timedelta(minutes=1), expires_at=env.now+timedelta(hours=1))
        binding = author.get(f'/api/v2/cases/{env.case.id}/agency-objects/{oid}').json()
        prefix = f'/api/v2/cases/{env.case.id}/collaboration'
        projection = prefix+f'/objects/{oid}/projections/projection'
        draft = author.post(prefix+f'/objects/{oid}/projections', json=dict(id='projection', expected_binding=binding,
            recipient=env.identities['client'].model_dump(), content=dict(title='Curated update', summary='No internal source text.', statements=[])))
        assert draft.status_code == 200, draft.text
        grant = author.post(prefix+'/grants', json=dict(id='client-disclosure', recipient=env.identities['client'].model_dump(),
            purpose='client_projection', object_id=oid, projection_id='projection', valid_from=(env.now-timedelta(minutes=1)).isoformat(),
            expires_at=(env.now+timedelta(hours=1)).isoformat(), rationale='Fictional exact client disclosure'))
        assert grant.status_code == 200, grant.text
        inspected = reviewer.get(projection+'/review')
        assert inspected.status_code == 200, inspected.text
        review = reviewer.post(projection+'/review', json=dict(expected_digest=inspected.json()['digest'], grant_id='client-disclosure', rationale='Reviewed only this exact fictional update'))
        assert review.status_code == 200, review.text
        with browser(env, 'client') as client:
            result = client.get(projection)
            assert result.status_code == 200, result.text
            assert 'sources' not in result.json() and 'binding' not in result.json()
            for path in [f'/api/v2/cases/{env.case.id}', f'/api/v2/cases/{env.case.id}/vault/{oid}', f'/api/v2/cases/{env.case.id}/knowledge']:
                assert client.get(path).status_code == 403
            author.post(prefix+'/grants/client-disclosure/revoke', json={})
            assert client.get(projection).status_code == 403


def queued_event(env, client):
    from endstate.events import IncomingEvent
    from eightball.agency_access import CurrentAuthority
    from eightball.store import digest
    obj = release(env, client, upload(env, client))
    actor = env.identities['author']
    authority = CurrentAuthority(env.registry, lambda: env.sessions.identity(env.cookies['author']))
    with env.host.as_current(authority):
        receipt = env.host.events.ingest(case_id=env.case.id, identity=actor, event=IncomingEvent(
            organisation_id=env.scope.organisation_id, matter_id=env.scope.matter_id, source_id=obj['object_id'],
            source_version='1', event_id=uuid4().hex, kind='source_received', base_revision=env.case.revision,
            text='Fictional source, not an observation.'))
        review = env.host.events.review_source(case_id=env.case.id, identity=actor, sequence=receipt.sequence,
            expected_revision=env.case.revision, receipt_sha256=digest(receipt.model_dump(mode='json')),
            rationale='Fictional explicit processing consent, not factual or action approval')
        work_id = env.host.events.enqueue(case_id=env.case.id, identity=actor, sequence=receipt.sequence,
            expected_revision=env.case.revision, review_id=review['id'], request_id=uuid4().hex)
    return authority, work_id, review


@pytest.mark.parametrize('invalidate', ['cancel', 'logout', 'review-revoke', 'source-policy'])
def test_worker_rechecks_host_policy_after_claim_and_never_repeats_call(env, invalidate):
    from eightball.event_inbox import EventConflict
    with browser(env) as client:
        authority, work, review = queued_event(env, client)
        calls = []
        def processor(*args):
            calls.append('one controlled fixture call, not model inference')
            if invalidate == 'cancel':
                env.host.events.cancel(case_id=env.case.id, identity=env.identities['author'], work_id=work)
            elif invalidate == 'review-revoke':
                env.host.events.revoke_source_review(case_id=env.case.id, identity=env.identities['author'], review_id=review['id'])
            elif invalidate == 'source-policy':
                env.policy['allow'] = False
            else:
                env.sessions.logout(env.cookies['author'])
            return 'Unreviewed fixture output must not publish.'
        env.host.events.processor = processor
        try:
            with env.host.as_current(authority):
                result = env.host.events.process(case_id=env.case.id, work_id=work, worker=env.identities['author'])
                assert result['state'] != 'awaiting_review'
        except PermissionError:
            assert invalidate == 'logout'
        with pytest.raises((PermissionError, EventConflict)):
            with env.host.as_current(authority):
                env.host.events.process(case_id=env.case.id, work_id=work, worker=env.identities['author'])
        assert len(calls) == 1
        assert env.store.get(env.case.id).revision == env.case.revision
