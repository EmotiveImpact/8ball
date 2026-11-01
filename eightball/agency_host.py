"""Explicit engineering host. Shared transactions; no automatic provisioning.

Missing keys, scanner, processing policy or capabilities deny. Import enables
nothing. This is not production multi-tenant infrastructure.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from fastapi import APIRouter, Depends, Request

from .authorisation import Identity, Operation as O, Resource
from .collaboration.contracts import Binding, SourceVersion, VaultSources
from .collaboration.service import Collaboration
from .projections.service import Projections
from .event_workers.service import EventWorkerService
from .intelligence.knowledge import KnowledgeService, SourceSnapshot, SCHEMA
from .operations.journal import Operations, initialize
from .store import digest
from .v2.store import Store
from .vault.authority import RegistryAuthority
from .vault.contracts import Unavailable, VaultPermission
from .vault.service import Vault


_authority = ContextVar('agency_host_authority', default=None)
CAPABILITIES = {
    'internal.read': O.READ,
    'collaboration.manage': O.WRITE, 'collaboration.expert': O.READ,
    'projection.draft': O.WRITE, 'projection.inspect': O.READ,
    'projection.review': O.WRITE, 'projection.withdraw': O.WRITE, 'projection.client': O.READ,
    'knowledge.draft': O.WRITE, 'knowledge.review': O.WRITE, 'knowledge.retire': O.WRITE,
    'knowledge.read': O.READ, 'knowledge.search': O.SEARCH,
    'operations.read': O.READ, 'operations.open': O.WRITE, 'operations.transition': O.WRITE,
    'operations.verify_revocation': O.WRITE,
    **{'vault.' + p.value: O.WRITE for p in VaultPermission},
}

ROUTE_OPERATIONS = {
    ('GET', '/agency-context'): O.READ,
    ('GET', '/agency-objects/{object_id}'): O.READ,
    ('GET', '/vault'): O.READ, ('POST', '/vault'): O.WRITE,
    ('GET', '/vault/audit'): O.READ, ('GET', '/vault/{object_id}'): O.READ,
    ('POST', '/vault/{object_id}/download'): O.DOWNLOAD,
    ('POST', '/vault/{object_id}/scan'): O.WRITE,
    ('POST', '/vault/{object_id}/cancel-scan'): O.WRITE,
    ('POST', '/vault/{object_id}/hold'): O.WRITE,
    ('POST', '/vault/{object_id}/retention'): O.WRITE,
    ('POST', '/vault/{object_id}/delete-local'): O.WRITE,
    ('GET', '/collaboration/grants'): O.READ, ('POST', '/collaboration/grants'): O.WRITE,
    ('POST', '/collaboration/grants/{grant_id}/revoke'): O.WRITE,
    ('GET', '/collaboration/objects/{object_id}/expert/{grant_id}'): O.READ,
    ('POST', '/collaboration/objects/{object_id}/projections'): O.WRITE,
    ('GET', '/collaboration/objects/{object_id}/projections/{projection_id}/review'): O.READ,
    ('POST', '/collaboration/objects/{object_id}/projections/{projection_id}/review'): O.WRITE,
    ('POST', '/collaboration/objects/{object_id}/projections/{projection_id}/withdraw'): O.WRITE,
    ('GET', '/collaboration/objects/{object_id}/projections/{projection_id}'): O.READ,
    ('POST', '/incoming-events'): O.WRITE,
    ('POST', '/incoming-events/{sequence}/processing-review'): O.WRITE,
    ('POST', '/processing-reviews/{review_id}/revoke'): O.WRITE,
    ('POST', '/event-attempts'): O.INFER, ('POST', '/event-work/{work_id}/cancel'): O.WRITE,
    ('GET', '/event-work/{work_id}/dispatch-status'): O.READ,
    ('GET', '/event-work/{work_id}'): O.READ, ('POST', '/event-work/{work_id}/review'): O.WRITE,
    ('POST', '/event-work/{work_id}/preview'): O.READ, ('POST', '/change-notices/pull'): O.READ,
    ('POST', '/change-notices/{notice_id}/acknowledge'): O.READ,
    ('GET', '/knowledge'): O.SEARCH, ('GET', '/knowledge/{item_id}'): O.READ,
    ('POST', '/knowledge/{item_id}'): O.WRITE,
    ('GET', '/domain-packs'): O.READ, ('POST', '/domain-packs/{pack_id}/preview'): O.READ,
}
OPERATIONS_PREFIX = '/api/v2/organisations/{organisation_id}/matters/{matter_id}/cases/{case_id}/operations'


class AgencyHost:
    def __init__(self, access, *, keys=None, scanner=None, processor=None, source_consent=None,
                 deletion_guard=None, revocation_probe=None):
        self.access, self.path = access, access.registry.path
        self.access.host_boundary = self.boundary
        self.access.route_operations.update({(method, '/api/v2/cases/{case_id}' + path): op
                                             for (method, path), op in ROUTE_OPERATIONS.items()})
        self.access.route_operations.update({
            ('GET', OPERATIONS_PREFIX): O.READ, ('POST', OPERATIONS_PREFIX): O.WRITE,
            ('POST', OPERATIONS_PREFIX + '/{record_id}/transition'): O.WRITE,
            ('POST', OPERATIONS_PREFIX + '/{record_id}/verify-revocation'): O.WRITE,
        })
        self.store = Store(self.path)
        self.keys, self.scanner, self.processor = keys, scanner, processor
        self.source_consent = source_consent
        with sqlite3.connect(self.path) as db:
            db.execute('''CREATE TABLE IF NOT EXISTS agency_capabilities (
                id TEXT PRIMARY KEY, actor TEXT NOT NULL, organisation_id TEXT NOT NULL,
                matter_id TEXT NOT NULL, object_id TEXT, capability TEXT NOT NULL,
                valid_from TEXT NOT NULL, expires_at TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0)''')
            for statement in SCHEMA:
                db.execute(statement.replace('CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ', 1))
        self.vault_registry = RegistryAuthority(control=self.vault_control)
        self.vault = Vault(self.path, authority=self, keys=keys, scanner=scanner, deletion_guard=deletion_guard)
        self.collaboration = Collaboration(self.path, policy=self, cases=self, sources=VaultSources(self.vault))
        self.collaboration.initialize()
        self.projections = Projections(self.collaboration)
        initialize(self.path)
        self.operations = Operations(self.path, authority=self.operations_authority, probe=revocation_probe)
        self.events = EventWorkerService(self.store, authority=self.event_authority,
                                        source_policy=self.source_policy, processor=processor)
        self.knowledge = KnowledgeService(self.transaction, authorise=self.knowledge_authority,
                                         resolve_source=self.resolve_source, case_revision=self.case_revision)

    @contextmanager
    def transaction(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def current(self):
        bound = _authority.get()
        if bound is None or bound[0].registry is not self.access.registry:
            raise PermissionError('Current host authority required')
        identity = self.resolve(bound[0])
        if identity != bound[1]:
            raise PermissionError('Request principal changed')
        return identity

    @staticmethod
    def resolve(authority):
        from fastapi import HTTPException
        from .oidc.login import LoginDenied
        try:
            return authority.current_identity()
        except LoginDenied:
            raise PermissionError('Current principal unavailable') from None
        except HTTPException as error:
            if error.status_code not in (401, 403):
                raise
            raise PermissionError('Current principal unavailable') from None

    @contextmanager
    def as_current(self, authority):
        """Explicit server-owned worker invocation with a live identity resolver."""
        if authority.registry is not self.access.registry:
            raise PermissionError('Worker must use this host registry')
        token = _authority.set((authority, self.resolve(authority)))
        try:
            yield
            self.current()
        finally:
            _authority.reset(token)

    def boundary(self, request, authority, operation):
        identity = authority.current_identity()
        case_id = request.path_params['case_id']
        object_id = request.path_params.get('object_id')
        template = request.scope['route'].path
        client = template.endswith('/projections/{projection_id}') and request.method == 'GET'
        expert = template.endswith('/expert/{grant_id}') and request.method == 'GET'
        with self.transaction() as db:
            scope = self.scope(db, case_id).model_copy(update={'object_id': object_id})
            self.capability(db, identity, scope,
                            'projection.client' if client else 'collaboration.expert' if expert else 'internal.read')
            self.access.registry.require(identity, case_id, (operation,),
                                         object_ids=(object_id,) if object_id else (), db=db)
            if authority.current_identity() != identity:
                raise PermissionError('Current principal changed')

    def actor(self, identity, *, delegated=False):
        current = self.current()
        if not isinstance(identity, Identity) or (not delegated and identity != current):
            raise PermissionError('Request principal changed')

    def grant_capability(self, grant_id, *, identity, resource, capability, valid_from, expires_at):
        """Host-only bounded provisioning, never HTTP or a replacement for grants."""
        if capability not in CAPABILITIES or valid_from.tzinfo is None or expires_at <= valid_from:
            raise ValueError('Explicit bounded capability required')
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO agency_capabilities VALUES (?,?,?,?,?,?,?,?,0)',
                       (grant_id, digest(identity.model_dump(mode='json')), resource.organisation_id,
                        resource.matter_id, resource.object_id, capability,
                        valid_from.isoformat(), expires_at.isoformat()))

    def capability(self, db, identity, resource, capability):
        if capability not in CAPABILITIES:
            raise PermissionError('Unknown capability')
        rows = db.execute('''SELECT object_id,valid_from,expires_at FROM agency_capabilities
            WHERE actor=? AND organisation_id=? AND matter_id=? AND capability=? AND revoked=0''',
            (digest(identity.model_dump(mode='json')), resource.organisation_id, resource.matter_id, capability))
        now = datetime.now(timezone.utc)
        for obj, start, end in rows:
            if (obj is None or obj == resource.object_id) and datetime.fromisoformat(start) <= now < datetime.fromisoformat(end):
                return
        raise PermissionError('Current capability required')

    def scope(self, db, case_id):
        row = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?', (case_id,)).fetchone()
        if row is None:
            raise PermissionError('Access is not permitted')
        self.store._get(db, case_id)
        return Resource(organisation_id=row[0], matter_id=row[1])

    def require(self, db, identity=None, binding=None, capability=None, **vault):
        if vault:
            return self.vault_authority(db, identity=identity, **vault)
        # A client pull rechecks the stored reviewer's present disclosure/source
        # authority, but never replaces or forgets the current request principal.
        self.actor(identity, delegated=identity != self.current() and capability == 'projection.review')
        if self.scope(db, binding.case_id) != binding.resource.model_copy(update={'object_id': None}):
            raise PermissionError('Scope changed')
        self.capability(db, identity, binding.resource, capability)
        self.access.registry.require(identity, binding.case_id, (CAPABILITIES[capability],),
            object_ids=(binding.resource.object_id,) if binding.resource.object_id else (), db=db)

    def vault_control(self, db, identity, resource, permission, now):
        self.capability(db, identity, resource, 'vault.' + permission.value)
        return True

    def vault_authority(self, db, *, identity, case_id, object_id, permission, now):
        self.actor(identity, delegated=identity != self.current() and permission == VaultPermission.READ)
        if self.keys is None:
            raise Unavailable('Vault keys are not configured')
        self.scope(db, case_id)
        scope = self.vault_registry.require(db, identity=identity, case_id=case_id,
                                           object_id=object_id, permission=permission, now=now)
        self.capability(db, identity, scope, 'vault.' + permission.value)
        self.access.registry.require(identity, case_id, (O.READ,),
                                    object_ids=(object_id,) if object_id else (), db=db)
        if permission in (VaultPermission.READ, VaultPermission.DOWNLOAD) and object_id:
            self.consent(db, identity, case_id, object_id, 'read')
        return scope

    def consent(self, db, identity, case_id, object_id, purpose):
        if self.source_consent is None or self.source_consent(db, identity, case_id, object_id, purpose) is not True:
            raise PermissionError('Current source policy required')

    def binding(self, db, case_id, object_id=None):
        scope, case = self.scope(db, case_id), self.store._get(db, case_id)
        sources, revision = (), case.revision
        if object_id:
            # Deliberately support vault objects, not guessed whole-case records.
            row = db.execute('''SELECT o.descriptor,s.revision FROM vault_originals o
                JOIN vault_state s ON s.object_id=o.id WHERE o.id=? AND o.case_id=?''',
                (object_id, case_id)).fetchone()
            if row is None:
                raise PermissionError('Object unavailable')
            descriptor = json.loads(row[0])
            if (descriptor['organisation_id'], descriptor['matter_id']) != (scope.organisation_id, scope.matter_id):
                raise PermissionError('Object scope differs')
            sources = (SourceVersion(object_id=object_id, version=descriptor['version'],
                                     vault_revision=row[1], sha256=descriptor['sha256']),)
            revision = row[1]
        return Binding(case_id=case_id, resource=scope.model_copy(update={'object_id': object_id}),
                       case_revision=case.revision, object_revision=revision, sources=sources)

    def expert_view(self, db, binding):
        source = binding.sources[0]
        return {'object_id': source.object_id, 'sha256': source.sha256, 'version': source.version,
                'vault_revision': source.vault_revision, 'content_not_returned': True}

    def event_authority(self, db, identity, resource, operations, now):
        self.actor(identity)
        rows = db.execute('SELECT case_id FROM agency_case_scope WHERE organisation_id=? AND matter_id=?',
                          (resource.organisation_id, resource.matter_id)).fetchall()
        if not rows:
            return False
        self.access.registry.require(identity, rows[0][0], operations, db=db)
        return True

    def source_policy(self, db, identity, case_id, receipt, now):
        self.actor(identity)
        binding = self.binding(db, case_id, receipt.event.source_id)
        source = binding.sources[0]
        if (receipt.event.source_version != str(source.version)
                or sha256(receipt.event.text.encode('utf-8')).hexdigest() != source.sha256):
            return False
        self.consent(db, identity, case_id, source.object_id, 'process')
        VaultSources(self.vault).require_current(db, binding, identity=identity)
        return True

    def operations_authority(self, db, identity, scope, operation, now):
        self.actor(identity)
        binding = self.binding(db, scope.case_id)
        if (scope.organisation_id, scope.matter_id) != (binding.resource.organisation_id, binding.resource.matter_id):
            return False
        self.require(db, identity, binding, operation)
        return True

    def context(self, request, case_id):
        identity = self.current()
        with self.transaction() as db:
            scope = self.scope(db, case_id)
        return dict(organisation_id=scope.organisation_id, matter_id=scope.matter_id,
                    case_id=case_id, actor_id='actor_' + digest(identity.model_dump(mode='json')))

    def knowledge_authority(self, db, context, operation, item_id):
        identity = self.current()
        scope = self.scope(db, context.case_id)
        if (context.actor_id != 'actor_' + digest(identity.model_dump(mode='json'))
                or (context.organisation_id, context.matter_id) != (scope.organisation_id, scope.matter_id)):
            return False
        self.require(db, identity, self.binding(db, context.case_id), operation)
        return True

    def case_revision(self, db, context):
        return self.store._get(db, context.case_id).revision

    def resolve_source(self, db, context, source_id):
        identity = self.current()
        binding = self.binding(db, context.case_id, source_id)
        self.consent(db, identity, context.case_id, source_id, 'process')
        self.access.registry.require(identity, context.case_id, (O.READ, O.INFER), object_ids=(source_id,), db=db)
        VaultSources(self.vault).require_current(db, binding, identity=identity)
        row = self.vault._row(db, binding.resource, context.case_id, source_id)
        return SourceSnapshot(text=self.vault._bytes(db, row).decode('utf-8'), active=True)

    def status(self):
        return dict(configured=True, keys_configured=self.keys is not None,
                    scanner_configured=self.scanner is not None, processor_configured=self.processor is not None,
                    source_policy_configured=self.source_consent is not None, production_accepted=False)

    def routes(self, authorised):
        async def bind(request: Request):
            token = _authority.set((request.state.agency_authority, request.state.agency_identity))
            try:
                yield
            finally:
                _authority.reset(token)
        router = APIRouter(prefix='/api/v2', dependencies=[Depends(authorised), Depends(bind)])
        from .v2.vault_api import register_vault_routes
        from .v2.collaboration_api import register_collaboration_routes
        from .v2.event_api import register_event_routes, register_event_worker_routes
        from .intelligence.api import register_intelligence_routes
        from .operations.api import register_operations_routes
        register_vault_routes(router, self.vault)
        register_collaboration_routes(router, self.collaboration, self.projections)
        register_event_routes(router, self.store, source_policy=self.source_policy, current_identity=self.current)
        register_event_worker_routes(router, self.events)
        register_intelligence_routes(router, self.knowledge, context_for_request=self.context)
        register_operations_routes(router, self.operations)

        @router.get('/cases/{case_id}/domain-packs')
        def packs(case_id: str):
            from endstate.domain_packs.loader import load_pack_json, pack_reference
            with self.transaction() as db:
                self.access.registry.require(self.current(), case_id, (O.READ,), db=db)
                directory = Path(__file__).resolve().parent.parent / 'tests/fixtures/domain_packs'
                return [{'pack': pack_reference(load_pack_json(path.read_bytes())).model_dump(mode='json'),
                         'fixture': path.stem, 'review_only': True}
                        for path in sorted(directory.glob('*.json')) if not path.stem.startswith('invalid')]

        @router.post('/cases/{case_id}/domain-packs/{pack_id}/preview')
        def preview_pack(case_id: str, pack_id: str, body: dict):
            from endstate.domain_packs.loader import load_pack_json
            from endstate.domain_packs.consumer import PackConsumer, ConsumerRequest, Principal, BoundSnapshot
            from .v2.planner import to_snapshot
            if pack_id not in {'fixer', 'neutral', 'sales', 'support'}:
                raise PermissionError('Pack is not configured')
            pack = load_pack_json((Path(__file__).resolve().parent.parent /
                                   'tests/fixtures/domain_packs' / (pack_id + '.json')).read_bytes())
            request = ConsumerRequest.model_validate(body)
            with self.transaction() as db:
                identity = self.current()
                scope = self.scope(db, case_id)
                def check(principal, requested, operation):
                    self.actor(identity)
                    if (requested.tenant_id, requested.matter_id, requested.snapshot_id) != (scope.organisation_id, scope.matter_id, case_id):
                        return False
                    self.access.registry.require(identity, case_id, (O.READ,), db=db)
                    return True
                consumer = PackConsumer(pack, authorise=check,
                    read_snapshot=lambda requested: BoundSnapshot(scope=requested, snapshot=to_snapshot(self.store._get(db, case_id))))
                return consumer.calculate(Principal(subject='actor_' + digest(identity.model_dump(mode='json'))), request).model_dump(mode='json')

        @router.get('/cases/{case_id}/agency-context')
        def context(case_id: str):
            with self.transaction() as db:
                self.access.registry.require(self.current(), case_id, (O.READ,), db=db)
                return {'scope': self.scope(db, case_id).model_dump(),
                        'case_revision': self.store._get(db, case_id).revision}

        @router.get('/cases/{case_id}/agency-objects/{object_id}')
        def object_binding(case_id: str, object_id: str):
            from fastapi import HTTPException
            from .vault.contracts import Conflict
            with self.transaction() as db:
                binding = self.binding(db, case_id, object_id)
                self.require(db, self.current(), binding, 'projection.inspect')
                try:
                    VaultSources(self.vault).require_current(db, binding, identity=self.current())
                except Conflict:
                    raise HTTPException(409, 'Source lifecycle changed; refresh and review') from None
                return binding.model_dump(mode='json')
        return router


def load_host(config_path, database):
    """Strict host-only config; no executable adapters or remote fetch from JSON."""
    from .agency_access import AccessRegistry, AgencyAccess
    from .vault.crypto import LocalKeyWrapper
    config = json.loads(Path(config_path).read_text())
    if set(config) - {'issuer', 'audience', 'public_key_file', 'vault_key_file', 'oidc'}:
        raise ValueError('Unknown agency configuration fields')
    sessions = None
    if config.get('oidc'):
        from .oidc.login import OIDCConfig, LoginService, TokenEndpoint
        settings = dict(config['oidc'])
        settings['signing_keys'] = {kid: Path(path).read_text() for kid, path in settings.pop('signing_key_files').items()}
        settings['issuer'] = config['issuer']
        oidc = OIDCConfig(**settings)
        if oidc.client_id != config['audience']:
            raise ValueError('OIDC and API audience must match')
        sessions = LoginService(database, oidc, TokenEndpoint(oidc))
    access = AgencyAccess(AccessRegistry(database), issuer=config['issuer'], audience=config['audience'],
                          public_key=Path(config['public_key_file']).read_text(), sessions=sessions)
    keys = None
    if config.get('vault_key_file'):
        path = Path(config['vault_key_file'])
        if path.stat().st_mode & 0o077:
            raise ValueError('Vault key file must be private to the operating account')
        keys = LocalKeyWrapper({'local': path.read_bytes()}, active_key_id='local')
    return AgencyHost(access, keys=keys)
