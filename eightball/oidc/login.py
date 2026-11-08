"""Pinned public-client OIDC authorization-code flow (Core 1.0, RFC 7636).

Provider registration, MFA policy and trusted signing-key rotation are operator
responsibilities. No claim or cookie grants a matter or approves a domain action.
"""
from dataclasses import dataclass, field
import base64
import hashlib
import hmac
import json
import secrets
import sqlite3
import time
from urllib.parse import urlencode, urlsplit

import httpx
import jwt

from eightball.authorisation import Identity


class LoginDenied(Exception):
    pass


SESSION_COOKIE = '__Host-eightball-session'
ATTEMPT_COOKIE = '__Host-eightball-login'


def digest(value: str) -> str:
    return hashlib.sha256(value.encode('ascii')).hexdigest()


def opaque(value) -> bool:
    return (isinstance(value, str) and 40 <= len(value) <= 128
            and all(c.isascii() and (c.isalnum() or c in '-_') for c in value))


def https_url(value):
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment):
        raise ValueError('Pinned HTTPS endpoints without userinfo, query or fragment required')
    return parsed


@dataclass(frozen=True)
class OIDCConfig:
    issuer: str
    client_id: str
    authorization_endpoint: str
    token_endpoint: str
    redirect_uri: str
    signing_keys: dict[str, str] = field(repr=False)
    required_acr: str | None = None
    session_seconds: int = 1800

    def __post_init__(self):
        for value in (self.issuer, self.authorization_endpoint, self.token_endpoint, self.redirect_uri):
            https_url(value)
        if (not self.client_id or not self.signing_keys or not 60 <= self.session_seconds <= 28800
                or any(not kid or not key for kid, key in self.signing_keys.items())):
            raise ValueError('Explicit client, pinned keys and bounded session lifetime required')
        # Take a private copy; callers cannot rotate trust by mutating their dict.
        from types import MappingProxyType
        object.__setattr__(self, 'signing_keys', MappingProxyType(dict(self.signing_keys)))

    @property
    def origin(self):
        parsed = urlsplit(self.redirect_uri)
        return f'{parsed.scheme}://{parsed.netloc}'


class TokenEndpoint:
    """One bounded public-client PKCE exchange; no retry, redirect or refresh."""

    def __init__(self, config: OIDCConfig, *, transport=None):
        self.config, self.transport = config, transport

    def __call__(self, *, code: str, verifier: str) -> str:
        try:
            with httpx.Client(transport=self.transport, timeout=10, follow_redirects=False,
                              trust_env=False) as client:
                with client.stream('POST', self.config.token_endpoint, data={
                    'grant_type': 'authorization_code', 'client_id': self.config.client_id,
                    'redirect_uri': self.config.redirect_uri, 'code': code,
                    'code_verifier': verifier,
                }, headers={'Accept': 'application/json'}) as response:
                    if response.status_code != 200:
                        raise LoginDenied('Identity provider exchange failed')
                    body = bytearray()
                    for chunk in response.iter_bytes():
                        body.extend(chunk)
                        if len(body) > 65536:
                            raise LoginDenied('Identity provider response exceeds limit')
            result = json.loads(body)
            token = result.get('id_token') if isinstance(result, dict) else None
            if not isinstance(token, str) or not 1 <= len(token) <= 16384:
                raise LoginDenied('Identity provider returned no valid ID token')
            return token
        except (httpx.HTTPError, ValueError):
            raise LoginDenied('Identity provider exchange failed') from None


class LoginService:
    def __init__(self, path, config: OIDCConfig, exchange, *, clock=time.time):
        self.path, self.config, self.exchange, self.clock = str(path), config, exchange, clock
        with sqlite3.connect(self.path) as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS agency_login_attempt (
                state_hash TEXT PRIMARY KEY, browser_hash TEXT NOT NULL,
                nonce TEXT NOT NULL, verifier TEXT NOT NULL, expires REAL NOT NULL,
                used INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS agency_browser_session (
                token_hash TEXT PRIMARY KEY, issuer TEXT NOT NULL, subject TEXT NOT NULL,
                expires REAL NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
            ''')

    def begin(self) -> tuple[str, str]:
        state, browser, nonce, verifier = (secrets.token_urlsafe(32) for _ in range(4))
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('ascii')).digest()).rstrip(b'=').decode()
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO agency_login_attempt VALUES (?,?,?,?,?,0)',
                       (digest(state), digest(browser), nonce, verifier, self.clock()+300))
        query = urlencode(dict(response_type='code', scope='openid', client_id=self.config.client_id,
            redirect_uri=self.config.redirect_uri, state=state, nonce=nonce,
            code_challenge=challenge, code_challenge_method='S256'))
        return self.config.authorization_endpoint+'?'+query, browser

    def cancel(self, browser: str):
        if opaque(browser):
            with sqlite3.connect(self.path) as db:
                db.execute('UPDATE agency_login_attempt SET used=2,verifier="",nonce="" '
                           'WHERE browser_hash=? AND used IN (0,1)',
                           (digest(browser),))

    def complete(self, *, state: str, browser: str, code: str, issuer: str) -> str:
        if (not opaque(state) or not opaque(browser) or not isinstance(code, str)
                or not 1 <= len(code) <= 4096 or issuer != self.config.issuer):
            raise LoginDenied('Invalid login response')
        with sqlite3.connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT browser_hash,nonce,verifier,expires,used FROM agency_login_attempt '
                             'WHERE state_hash=?', (digest(state),)).fetchone()
            if (row is None or row[4] or self.clock() >= row[3]
                    or not hmac.compare_digest(row[0], digest(browser))):
                raise LoginDenied('Login attempt is missing, expired or already used')
            # Consume before any external work: failure/restart requires a new login.
            db.execute('UPDATE agency_login_attempt SET used=1,verifier="",nonce="" WHERE state_hash=?',
                       (digest(state),))
        try:
            token = self.exchange(code=code, verifier=row[2])
        except Exception:
            raise LoginDenied('Identity provider exchange failed; start a new login') from None
        identity, expires = self.verify(token, nonce=row[1])
        session = secrets.token_urlsafe(32)
        with sqlite3.connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            attempt = db.execute('SELECT used,expires FROM agency_login_attempt WHERE state_hash=?',
                                 (digest(state),)).fetchone()
            if attempt is None or attempt[0] != 1 or self.clock() >= attempt[1]:
                raise LoginDenied('Login attempt cancelled or expired during exchange')
            db.execute('INSERT INTO agency_browser_session VALUES (?,?,?,?,0)',
                (digest(session), identity.issuer, identity.subject,
                 min(expires, self.clock()+self.config.session_seconds)))
            db.execute('UPDATE agency_login_attempt SET used=3 WHERE state_hash=?', (digest(state),))
        return session

    def verify(self, token: str, *, nonce: str) -> tuple[Identity, float]:
        try:
            if not isinstance(token, str) or not 1 <= len(token) <= 16384:
                raise ValueError('Invalid ID token')
            header = jwt.get_unverified_header(token)
            if header.get('alg') != 'RS256' or header.get('crit'):
                raise ValueError('Unsupported ID token header')
            key = self.config.signing_keys[header['kid']]
            claims = jwt.decode(token, key, algorithms=['RS256'], issuer=self.config.issuer,
                audience=self.config.client_id,
                options={'require': ['iss', 'sub', 'aud', 'exp', 'iat', 'nonce']})
            if (not isinstance(claims['nonce'], str) or not hmac.compare_digest(claims['nonce'], nonce)
                    or type(claims['iat']) is not int or type(claims['exp']) is not int
                    or claims['iat'] > self.clock() or claims['exp'] <= self.clock()
                    or claims['iat'] >= claims['exp']):
                raise ValueError('Invalid token claims')
            aud = claims['aud']
            if ((isinstance(aud, list) and len(aud) > 1 and claims.get('azp') != self.config.client_id)
                    or ('azp' in claims and claims['azp'] != self.config.client_id)):
                raise ValueError('Invalid authorised party')
            if self.config.required_acr is not None and claims.get('acr') != self.config.required_acr:
                raise ValueError('Required authentication context absent')
            return Identity(issuer=claims['iss'], subject=claims['sub']), claims['exp']
        except (jwt.PyJWTError, ValueError, KeyError, TypeError):
            raise LoginDenied('A valid provider ID token is required') from None

    def identity(self, session: str) -> Identity:
        if not opaque(session):
            raise LoginDenied('A current browser session is required')
        with sqlite3.connect(self.path) as db:
            row = db.execute('SELECT issuer,subject,expires,revoked FROM agency_browser_session '
                             'WHERE token_hash=?', (digest(session),)).fetchone()
        if row is None or row[3] or self.clock() >= row[2]:
            raise LoginDenied('A current browser session is required')
        return Identity(issuer=row[0], subject=row[1])

    def logout(self, session: str):
        if opaque(session):
            with sqlite3.connect(self.path) as db:
                db.execute('UPDATE agency_browser_session SET revoked=1 WHERE token_hash=?', (digest(session),))

    def revoke_identity(self, identity: Identity):
        with sqlite3.connect(self.path) as db:
            db.execute('UPDATE agency_browser_session SET revoked=1 WHERE issuer=? AND subject=?',
                       (identity.issuer, identity.subject))
