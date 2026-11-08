import json
import sqlite3
from datetime import timedelta

import pytest
from pydantic import ValidationError

from eightball.authorisation import Identity
from eightball.projections.service import ClientContent, ClientStatement, DraftRequest, ReviewRequest, Projections
from eightball.store import Conflict
from tests.test_collaboration import AUTHOR, REVIEWER, EXPERT, CLIENT, env, grant_request


def draft(env, **updates):
    with env.host.transaction() as db:
        binding = env.host.binding(db, 'case-a', 'object-a')
    request = DraftRequest.model_validate(dict(id='projection-a', expected_binding=binding, recipient=CLIENT,
                                         content=ClientContent(title='Fictional client update', summary='Only separately authored material.',
                                                               statements=(ClientStatement(text='Outcome not observed'),))) | updates)
    return env.projections.draft(actor=AUTHOR, case_id='case-a', object_id='object-a', request=request)


def client_grant(env, **updates):
    request = grant_request(env, **(dict(id='client-grant', purpose='client_projection', recipient=CLIENT,
                                        projection_id='projection-a') | updates))
    return env.host.create_grant(actor=AUTHOR, case_id='case-a', request=request)


def review(env, record, **updates):
    request = ReviewRequest(expected_digest=record['digest'], grant_id='client-grant', rationale='Reviewed fictional disclosure for this recipient.')
    return env.projections.review(**(dict(actor=REVIEWER, case_id='case-a', object_id='object-a',
                                          projection_id='projection-a', request=request) | updates))


def client_read(env, **updates):
    return env.projections.client_read(**(dict(actor=CLIENT, case_id='case-a', object_id='object-a', projection_id='projection-a') | updates))


def ready(env):
    record = draft(env)
    client_grant(env)
    review(env, record)
    return record


def test_draft_has_no_client_visibility_and_no_default_internal_view(env):
    record = draft(env)
    with pytest.raises(PermissionError):
        client_read(env)
    client_grant(env)
    with pytest.raises(PermissionError):
        client_read(env)
    with pytest.raises(PermissionError):
        env.projections.inspect(actor=CLIENT, case_id='case-a', object_id='object-a', projection_id='projection-a')
    review(env, record)
    result = client_read(env)
    assert set(result) == {'id', 'content', 'reviewed_at', 'action_permission', 'external_send'}
    assert result['content']['statements'][0]['evidence_state'] == 'unknown'
    assert result['action_permission'] is result['external_send'] is False
    encoded = json.dumps(result)
    for secret in ('opaque-source', 'vault_revision', 'internal_note', 'source_text', 'fictional.invalid', 'matter-a', 'sha256', 'grant_id'):
        assert secret not in encoded


def test_wrong_client_expert_tenant_matter_object_are_denied(env):
    ready(env)
    for args in ({'actor': EXPERT}, {'actor': AUTHOR}, {'case_id': 'case-b'}, {'case_id': 'case-c'},
                 {'object_id': 'object-b'}, {'actor': Identity(issuer='https://other.invalid', subject='client')}):
        with pytest.raises((PermissionError, KeyError)):
            client_read(env, **args)


@pytest.mark.parametrize('column', ['revision', 'object_revision', 'vault_revision'])
def test_stale_case_object_or_vault_revision_invalidates_review_and_read(env, column):
    record = ready(env)
    with sqlite3.connect(env.path) as db:
        db.execute(f"UPDATE fixture_cases SET {column}={column}+1 WHERE id='case-a'")
    assert env.projections.inspect(actor=REVIEWER, case_id='case-a', object_id='object-a', projection_id='projection-a')['stale']
    with pytest.raises(Conflict):
        client_read(env)
    with pytest.raises(Conflict):
        review(env, record)


def test_review_requires_separate_current_reviewer_and_exact_digest(env):
    record = draft(env)
    client_grant(env)
    with sqlite3.connect(env.path) as db:
        db.execute('UPDATE fixture_members SET capabilities=? WHERE identity=?',
                   (json.dumps(['projection.review']), AUTHOR.model_dump_json()))
    with pytest.raises(PermissionError):
        review(env, record, actor=AUTHOR)
    with pytest.raises(PermissionError):
        review(env, record, actor=CLIENT)
    with pytest.raises(Conflict):
        review(env, record, request=ReviewRequest(expected_digest='0'*64, grant_id='client-grant', rationale='Reviewed a different draft'))
    with pytest.raises(PermissionError):
        client_read(env)


def test_client_grant_revocation_prevents_review_read_and_replacement(env):
    record = ready(env)
    env.host.revoke_grant(actor=AUTHOR, case_id='case-a', grant_id='client-grant')
    with pytest.raises(PermissionError):
        client_read(env)
    with pytest.raises(PermissionError):
        review(env, record)
    client_grant(env, id='replacement-grant')
    with pytest.raises(PermissionError):
        client_read(env)


def test_reviewer_or_client_membership_revocation_blocks_access(env):
    ready(env)
    with sqlite3.connect(env.path) as db:
        db.execute('DELETE FROM fixture_members WHERE identity=?', (REVIEWER.model_dump_json(),))
    with pytest.raises(PermissionError):
        client_read(env)


def test_withdrawal_is_terminal_idempotent_preserves_review_history(env):
    record = ready(env)
    result = env.projections.withdraw(actor=AUTHOR, case_id='case-a', object_id='object-a', projection_id='projection-a')
    assert result == env.projections.withdraw(actor=AUTHOR, case_id='case-a', object_id='object-a', projection_id='projection-a')
    assert result['external_cancellation'] is False
    with pytest.raises(PermissionError):
        client_read(env)
    with pytest.raises(Conflict):
        review(env, record)
    with pytest.raises(Conflict):
        draft(env)
    row = env.projections.inspect(actor=AUTHOR, case_id='case-a', object_id='object-a', projection_id='projection-a')
    assert row['state'] == 'withdrawn' and row['review']['reviewer']['subject'] == REVIEWER.subject


def test_restart_idempotency_preserves_exact_review_and_no_duplicate_audit(env):
    record = draft(env)
    assert draft(env) == record
    client_grant(env)
    reviewed = review(env, record)
    env.projections = Projections(env.host)
    assert review(env, record) == reviewed
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT COUNT(*) FROM collaboration_audit').fetchone()[0] == 3
    assert client_read(env)['content']['title'] == 'Fictional client update'
    with pytest.raises(Conflict):
        draft(env, content=ClientContent(title='Changed', summary='New material'))
    with pytest.raises(Conflict):
        review(env, record, request=ReviewRequest(expected_digest=record['digest'], grant_id='client-grant', rationale='A different review rationale'))


def test_client_grants_are_exact_projection_recipient_and_expiry(env):
    draft(env)
    with pytest.raises(ValidationError):
        grant_request(env, purpose='client_projection', object_id=None)
    with pytest.raises(Conflict):
        client_grant(env, recipient=EXPERT)
    with pytest.raises(Conflict):
        client_grant(env, object_id='object-b')
    client_grant(env)
    record = env.projections.inspect(actor=AUTHOR, case_id='case-a', object_id='object-a', projection_id='projection-a')
    review(env, record)
    env.clock[0] += timedelta(hours=1)
    with pytest.raises(PermissionError):
        client_read(env)


def test_audit_failure_rolls_back_review_withdrawal_and_read(env):
    record = draft(env)
    client_grant(env)
    def fail():
        with sqlite3.connect(env.path) as db:
            db.execute("CREATE TRIGGER fail_audit BEFORE INSERT ON collaboration_audit BEGIN SELECT RAISE(ABORT,'test failure'); END")
    fail()
    with pytest.raises(sqlite3.IntegrityError):
        review(env, record)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT state,review FROM collaboration_projections').fetchone() == ('draft', None)
        db.execute('DROP TRIGGER fail_audit')
    review(env, record)
    fail()
    with pytest.raises(sqlite3.IntegrityError):
        client_read(env)
    with pytest.raises(sqlite3.IntegrityError):
        env.projections.withdraw(actor=AUTHOR, case_id='case-a', object_id='object-a', projection_id='projection-a')
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT state FROM collaboration_projections').fetchone()[0] == 'reviewed'


def test_corrupt_review_or_draft_never_publishes(env):
    ready(env)
    with sqlite3.connect(env.path) as db:
        db.execute("UPDATE collaboration_projections SET review='{}'")
    with pytest.raises(Conflict):
        client_read(env)


def test_source_retraction_does_not_allow_review_or_client_read(env):
    record = ready(env)
    with sqlite3.connect(env.path) as db:
        db.execute("UPDATE fixture_cases SET ready=0 WHERE id='case-a'")
    with pytest.raises(PermissionError):
        client_read(env)
    with pytest.raises(PermissionError):
        review(env, record)


def test_client_disclosure_does_not_give_client_internal_source_authority(env):
    record = draft(env)
    client_grant(env)
    review(env, record)
    identities = []
    original = env.host.sources.require_current
    def current(db, binding, *, identity):
        identities.append(identity)
        if identity == CLIENT:
            raise PermissionError('Clients have no internal vault read')
        return original(db, binding, identity=identity)
    env.host.sources.require_current = current
    assert client_read(env)['external_send'] is False
    assert identities == [REVIEWER, REVIEWER]


def test_cancellation_rolls_back_review_and_its_audit(env):
    record = draft(env)
    client_grant(env)
    original = env.host.audit
    def interrupt(db, **kwargs):
        original(db, **kwargs)
        raise KeyboardInterrupt('Fictional cancellation')
    env.host.audit = interrupt
    with pytest.raises(KeyboardInterrupt):
        review(env, record=record)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT state FROM collaboration_projections').fetchone()[0] == 'draft'
        assert all(json.loads(row[0])['kind'] != 'projection_reviewed' for row in db.execute('SELECT record FROM collaboration_audit'))
