"""Offline fictional host setup shared by unit and native HTTP journeys.

Sessions are seeded directly, not evidence of real identity-provider acceptance.
Scanner verdicts are controlled fixtures, not malware-quality evidence.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import secrets
import sqlite3
from types import SimpleNamespace

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from eightball.agency_access import AccessRegistry, AgencyAccess
from eightball.agency_host import AgencyHost, CAPABILITIES
from eightball.api import make_app
from eightball.authorisation import Grant, Identity, Operation, Resource
from eightball.oidc.login import LoginService, OIDCConfig, digest
from eightball.store import Store as Legacy
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.vault.contracts import ScanResult
from eightball.vault.crypto import LocalKeyWrapper


class FixtureScanner:
    def __init__(self):
        self.after = lambda: None

    def scan(self, content, *, sha256, media_type):
        self.after()
        return ScanResult('clean', 'fixture-not-malware-proof', '1', 'fictional', sha256)


def make_fixture(directory, *, origin='https://testserver'):
    path = str(Path(directory) / 'fictional.sqlite3')
    legacy = Legacy(path)
    store = Store(path)
    case = store.create(demo_case(), fixture=True)
    other = store.create(demo_case(), fixture=True)
    registry = AccessRegistry(path)
    scope = Resource(organisation_id='fictional-agency', matter_id='fictional-matter')
    registry.bind_case(case.id, scope)
    registry.bind_case(other.id, Resource(organisation_id='fictional-other', matter_id='fictional-other'))
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    config = OIDCConfig(issuer='https://fictional-identity.invalid', client_id='fictional-8ball',
        authorization_endpoint='https://fictional-identity.invalid/authorize', token_endpoint='https://fictional-identity.invalid/token',
        redirect_uri=origin+'/api/v2/identity/callback', signing_keys={'fixture': public})
    sessions = LoginService(path, config, None)
    access = AgencyAccess(registry, issuer=config.issuer, audience=config.client_id, public_key=public, sessions=sessions)
    scanner = FixtureScanner()
    policy = {'allow': True}
    host = AgencyHost(access, keys=LocalKeyWrapper({'fixture': AESGCM.generate_key(bit_length=256)}, active_key_id='fixture'),
        scanner=scanner, source_consent=lambda *args: policy['allow'] is True)
    now = datetime.now(timezone.utc)
    identities, cookies = {}, {}
    for who in ('author', 'reviewer', 'client'):
        identity = identities[who] = Identity(issuer=config.issuer, subject=who)
        cookies[who] = secrets.token_urlsafe(32)
        with sqlite3.connect(path) as db:
            db.execute('INSERT INTO agency_browser_session VALUES (?,?,?,?,0)',
                (digest(cookies[who]), identity.issuer, identity.subject, sessions.clock()+1200))
        if who != 'client':
            registry.add_grant(who, Grant(identity=identity, resource=scope, operations=frozenset(Operation),
                valid_from=now-timedelta(minutes=1), expires_at=now+timedelta(hours=1)))
            for capability in CAPABILITIES:
                host.grant_capability(who+'-'+capability, identity=identity, resource=scope, capability=capability,
                    valid_from=now-timedelta(minutes=1), expires_at=now+timedelta(hours=1))
    app = make_app(legacy, 'fictional-local-operator-token-not-agency'*2, agency_host=host)
    return SimpleNamespace(app=app, host=host, store=store, path=path, case=case, other=other,
        registry=registry, scope=scope, sessions=sessions, cookies=cookies, identities=identities,
        scanner=scanner, policy=policy, now=now, key=key)
