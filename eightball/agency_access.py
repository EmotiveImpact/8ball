"""Opt-in agency access boundary. No network discovery or public provisioning.

The operator provisions keys, case ownership and grants outside the HTTP API.
This development boundary does not replace production PostgreSQL row policies,
OIDC browser login/MFA, worker revocation or a security-reviewed deployment.
"""
from datetime import datetime, timezone
import sqlite3

import jwt
from fastapi import HTTPException, Request

from .authorisation import Grant, Identity, Operation, Resource, permits


class AccessRegistry:
    def __init__(self, path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS agency_case_scope (
                case_id TEXT PRIMARY KEY, organisation_id TEXT NOT NULL,
                matter_id TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS agency_grants (
                id TEXT PRIMARY KEY, body TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
            ''')

    def bind_case(self, case_id: str, scope: Resource):
        if scope.object_id is not None:
            raise ValueError('Case ownership must be a matter scope')
        with sqlite3.connect(self.path) as db:
            # Ownership cannot be silently overwritten or migrated.
            db.execute('INSERT INTO agency_case_scope VALUES (?,?,?)',
                       (case_id, scope.organisation_id, scope.matter_id))

    def add_grant(self, grant_id: str, grant: Grant):
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO agency_grants VALUES (?,?,?)',
                       (grant_id, grant.model_dump_json(), int(grant.revoked)))

    def revoke(self, grant_id: str):
        with sqlite3.connect(self.path) as db:
            db.execute('UPDATE agency_grants SET revoked=1 WHERE id=?', (grant_id,))

    def allowed(self, identity: Identity, case_id: str, operation: Operation) -> bool:
        with sqlite3.connect(self.path) as db:
            db.execute('BEGIN')
            scope = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?',
                               (case_id,)).fetchone()
            if scope is None:
                return False
            grants = tuple(Grant.model_validate_json(row[0]) for row in
                           db.execute('SELECT body FROM agency_grants WHERE revoked=0'))
            return permits(identity, Resource(organisation_id=scope[0], matter_id=scope[1]),
                           operation, grants, now=datetime.now(timezone.utc))


class AgencyAccess:
    def __init__(self, registry: AccessRegistry, *, issuer: str, audience: str, public_key: str):
        if not issuer.startswith('https://') or not audience:
            raise ValueError('Explicit HTTPS issuer and audience required')
        self.registry, self.issuer, self.audience = registry, issuer, audience
        self.public_key = public_key

    def identity(self, bearer: str) -> Identity:
        try:
            if not bearer.startswith('Bearer ') or len(bearer) > 16384:
                raise ValueError('Invalid bearer')
            claims = jwt.decode(bearer[7:], self.public_key, algorithms=['RS256'],
                                issuer=self.issuer, audience=self.audience,
                                options={'require': ['iss', 'sub', 'aud', 'exp', 'iat']})
            return Identity(issuer=claims['iss'], subject=claims['sub'])
        except (jwt.PyJWTError, ValueError, TypeError):
            raise HTTPException(401, 'A valid agency identity token is required') from None

    def __call__(self, request: Request):
        identity = self.identity(request.headers.get('authorization', ''))
        # Only explicitly mapped operations are exposed. Reviewed-event writes
        # recheck permissions/revision inside their own case transaction.
        case_id = request.path_params.get('case_id')
        operations = {
            ('GET', '/api/v2/cases/{case_id}'): Operation.READ,
            ('GET', '/api/v2/cases/{case_id}/history'): Operation.READ,
            ('GET', '/api/v2/cases/{case_id}/export'): Operation.EXPORT,
            ('GET', '/api/v2/cases/{case_id}/event-work/{work_id}'): Operation.READ,
            ('POST', '/api/v2/cases/{case_id}/event-work/{work_id}/review'): Operation.WRITE,
            ('POST', '/api/v2/cases/{case_id}/change-notices/pull'): Operation.READ,
            ('POST', '/api/v2/cases/{case_id}/change-notices/{notice_id}/acknowledge'): Operation.READ,
        }
        route = request.scope.get('route')
        operation = operations.get((request.method, getattr(route, 'path', '')))
        if (not case_id or operation is None
                or not self.registry.allowed(identity, case_id, operation)):
            raise HTTPException(403, 'Access is not permitted')
        request.state.agency_identity = identity
