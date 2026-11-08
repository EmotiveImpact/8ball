"""Agency policy isolation, not OIDC/API/database enforcement evidence."""
from datetime import datetime, timedelta, timezone

import pytest

from eightball.authorisation import Grant, Identity, Operation, Resource, permits

NOW = datetime(2026, 10, 25, tzinfo=timezone.utc)
WHO = Identity(issuer='https://identity.fixture.example', subject='operator-1')
MATTER = Resource(organisation_id='agency-a', matter_id='matter-1')


def grant(**changes):
    values = dict(identity=WHO, resource=MATTER, operations=frozenset(Operation),
                  valid_from=NOW-timedelta(hours=1), expires_at=NOW+timedelta(hours=1))
    return Grant(**(values | changes))


@pytest.mark.parametrize('operation', list(Operation))
def test_every_operation_requires_same_identity_tenant_and_matter(operation):
    assert permits(WHO, MATTER, operation, (grant(),), now=NOW)
    assert not permits(WHO, MATTER, operation, (), now=NOW)
    for who in (Identity(issuer=WHO.issuer, subject='other'),
                Identity(issuer='https://other.fixture.example', subject=WHO.subject)):
        assert not permits(who, MATTER, operation, (grant(),), now=NOW)
    for target in (Resource(organisation_id='agency-b', matter_id='matter-1'),
                   Resource(organisation_id='agency-a', matter_id='matter-2')):
        assert not permits(WHO, target, operation, (grant(),), now=NOW)


@pytest.mark.parametrize('operation', list(Operation))
def test_revocation_expiry_and_future_grants_deny(operation):
    for g in (grant(revoked=True), grant(expires_at=NOW),
              grant(valid_from=NOW+timedelta(seconds=1))):
        assert not permits(WHO, MATTER, operation, (g,), now=NOW)
    assert not permits(WHO, MATTER, operation, (grant(),), now=NOW.replace(tzinfo=None))


def test_read_only_object_grant_cannot_expand_to_other_objects_or_operations():
    target = Resource(organisation_id='agency-a', matter_id='matter-1', object_id='evidence-1')
    g = grant(resource=target, operations=frozenset({Operation.READ}))
    assert permits(WHO, target, Operation.READ, (g,), now=NOW)
    assert not permits(WHO, MATTER, Operation.READ, (g,), now=NOW)
    other = Resource(organisation_id='agency-a', matter_id='matter-1', object_id='evidence-2')
    assert not permits(WHO, other, Operation.READ, (g,), now=NOW)
    for op in set(Operation)-{Operation.READ}:
        assert not permits(WHO, target, op, (g,), now=NOW)
    assert not permits(WHO, target, 'read', (g,), now=NOW)
