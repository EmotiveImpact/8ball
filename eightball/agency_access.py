"""Opt-in agency access boundary. No network discovery or public provisioning.

The operator provisions keys, case ownership and grants outside the HTTP API.
This development boundary does not replace production PostgreSQL row policies,
configured live OIDC/MFA, complete worker enforcement or a security-reviewed deployment.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

import jwt
from fastapi import HTTPException, Request

from .authorisation import Grant, Identity, Operation, Resource, permits
from .oidc.login import LoginDenied, SESSION_COOKIE


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
        try:
            self.require(identity, case_id, (operation,))
            return True
        except (PermissionError, sqlite3.Error):
            return False

    def require(self, identity: Identity, case_id: str, operations: tuple[Operation, ...], *,
                object_ids: tuple[str, ...] = (), db: sqlite3.Connection | None = None) -> Resource:
        """Check current grants, never object existence or domain action permission.

        An injected transaction must own both case rows and registry tables.
        Callers retain responsibility for object ownership and expected revision.
        """
        if db is None:
            with sqlite3.connect(self.path) as connection:
                connection.execute('BEGIN IMMEDIATE')
                return self.require(identity, case_id, operations, object_ids=object_ids, db=connection)
        files = db.execute('PRAGMA database_list').fetchall()
        if (not db.in_transaction or not any(name == 'main' and filename
                and Path(filename).resolve() == Path(self.path).resolve()
                for _, name, filename in files)):
            raise PermissionError('Authority requires the registry transaction')
        # Acquire the writer reservation even for caller-owned transactions.
        # A stale WAL reader must fail, never authorise from its old snapshot.
        try:
            db.execute('UPDATE agency_grants SET revoked=revoked WHERE 0')
        except sqlite3.Error:
            raise PermissionError('Current authority transaction is unavailable') from None
        if (not isinstance(identity, Identity) or not isinstance(case_id, str) or not case_id
                or not isinstance(operations, tuple) or not operations
                or any(not isinstance(op, Operation) for op in operations)
                or not isinstance(object_ids, tuple)
                or any(not isinstance(obj, str) or not 1 <= len(obj) <= 128 for obj in object_ids)):
            raise PermissionError('Invalid authority scope')
        row = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?',
                         (case_id,)).fetchone()
        if row is None:
            raise PermissionError('Access is not permitted')
        try:
            scope = Resource(organisation_id=row[0], matter_id=row[1])
            grants = tuple(Grant.model_validate_json(row[0]) for row in
                           db.execute('SELECT body FROM agency_grants WHERE revoked=0'))
            resources = tuple(scope.model_copy(update={'object_id': obj}) for obj in object_ids) or (scope,)
            now = datetime.now(timezone.utc)
            if not all(permits(identity, resource, op, grants, now=now)
                       for resource in resources for op in operations):
                raise PermissionError('Access is not permitted')
        except (ValueError, TypeError):
            raise PermissionError('Invalid authority records') from None
        return scope

    @contextmanager
    def transaction(self, identity: Identity, case_id: str, operations: tuple[Operation, ...], *,
                    object_ids: tuple[str, ...] = ()):
        with sqlite3.connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            scope = self.require(identity, case_id, operations, object_ids=object_ids, db=db)
            yield db, scope
            self.require(identity, case_id, operations, object_ids=object_ids, db=db)


class CurrentAuthority:
    """Server-injected reauthentication callback, not a serialisable capability."""

    def __init__(self, registry: AccessRegistry, current_identity):
        self.registry = registry
        self.current_identity = current_identity

    def require(self, case_id, operations, *, object_ids=(), db=None):
        identity = self.current_identity()
        scope = self.registry.require(identity, case_id, operations, object_ids=object_ids, db=db)
        if self.current_identity() != identity:
            raise PermissionError('Current identity changed during authorisation')
        return scope

    @contextmanager
    def transaction(self, case_id, operations, *, object_ids=()):
        with sqlite3.connect(self.registry.path) as db:
            db.execute('BEGIN IMMEDIATE')
            identity = self.current_identity()
            scope = self.require(case_id, operations, object_ids=object_ids, db=db)
            if self.current_identity() != identity:
                raise PermissionError('Current identity changed during authorisation')
            yield db, scope
            self.require(case_id, operations, object_ids=object_ids, db=db)
            if self.current_identity() != identity:
                raise PermissionError('Current identity changed during authorisation')


class AgencyAccess:
    def __init__(self, registry: AccessRegistry, *, issuer: str, audience: str, public_key: str,
                 sessions=None):
        if not issuer.startswith('https://') or not audience:
            raise ValueError('Explicit HTTPS issuer and audience required')
        self.registry, self.issuer, self.audience = registry, issuer, audience
        self.public_key = public_key
        self.sessions = sessions

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

    def authority(self, request: Request) -> CurrentAuthority:
        bearer = request.headers.get('authorization')
        if bearer is not None:
            current = lambda: self.identity(bearer)
        elif self.sessions is not None:
            session = request.cookies.get(SESSION_COOKIE, '')

            def current():
                try:
                    return self.sessions.identity(session)
                except LoginDenied:
                    raise HTTPException(401, 'A current agency session is required') from None

            if (request.method not in ('GET', 'HEAD', 'OPTIONS')
                    and request.headers.get('origin') != self.sessions.config.origin):
                raise HTTPException(403, 'Same-origin session request required')
        else:
            raise HTTPException(401, 'A valid agency identity token is required')
        current()
        return CurrentAuthority(self.registry, current)

    def __call__(self, request: Request):
        authority = self.authority(request)
        # Only explicitly mapped operations are exposed. Reviewed-event writes
        # recheck permissions/revision inside their own case transaction.
        case_id = request.path_params.get('case_id')
        operations = {
            ('GET', '/api/v2/cases/{case_id}'): Operation.READ,
            ('GET', '/api/v2/cases/{case_id}/history'): Operation.READ,
            ('GET', '/api/v2/cases/{case_id}/export'): Operation.EXPORT,
            ('GET', '/api/v2/cases/{case_id}/event-work/{work_id}'): Operation.READ,
            ('POST', '/api/v2/cases/{case_id}/event-work/{work_id}/review'): Operation.WRITE,
            ('POST', '/api/v2/cases/{case_id}/event-work/{work_id}/preview'): Operation.READ,
            ('POST', '/api/v2/cases/{case_id}/change-notices/pull'): Operation.READ,
            ('POST', '/api/v2/cases/{case_id}/change-notices/{notice_id}/acknowledge'): Operation.READ,
        }
        route = request.scope.get('route')
        operation = operations.get((request.method, getattr(route, 'path', '')))
        if not case_id or operation is None:
            raise HTTPException(403, 'Access is not permitted')
        if not self.registry.allowed(authority.current_identity(), case_id, operation):
            raise HTTPException(403, 'Access is not permitted') from None
        request.state.agency_identity = authority.current_identity()
        request.state.agency_authority = authority
