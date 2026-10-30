from datetime import datetime
from typing import Literal, Protocol
import sqlite3

from pydantic import BaseModel, ConfigDict, Field

from eightball.authorisation import Identity


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, strict=True)


class Scope(Strict):
    organisation_id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,128}$')
    matter_id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,128}$')
    case_id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,128}$')


class OpenRecord(Strict):
    request_id: str = Field(pattern=r'^[A-Za-z0-9_-]{8,100}$')
    kind: Literal['incident', 'pilot_finding', 'revocation']
    severity: Literal['critical', 'high', 'medium', 'low']
    category: Literal['confidentiality', 'availability', 'integrity', 'safety',
                      'usefulness', 'correction', 'access']
    evidence_sha256: str | None = Field(default=None, pattern=r'^[a-f0-9]{64}$')
    target_id: str | None = Field(default=None, pattern=r'^[A-Za-z0-9_-]{1,128}$')


class Transition(Strict):
    request_id: str = Field(pattern=r'^[A-Za-z0-9_-]{8,100}$')
    expected_revision: int = Field(ge=0)
    state: Literal['investigating', 'contained', 'resolved', 'closed', 'cancelled']
    evidence_sha256: str | None = Field(default=None, pattern=r'^[a-f0-9]{64}$')


class VerifyRevocation(Strict):
    request_id: str = Field(pattern=r'^[A-Za-z0-9_-]{8,100}$')
    expected_revision: int = Field(ge=0)


SURFACES = ('api', 'database', 'object_links', 'search', 'model_cache', 'workers')
ProbeResult = Literal['denied', 'access_still_allowed', 'unavailable']


class Authority(Protocol):
    def __call__(self, db: sqlite3.Connection, identity: Identity, scope: Scope,
                 operation: str, now: datetime) -> bool: ...


class RevocationProbe(Protocol):
    def __call__(self, db: sqlite3.Connection, scope: Scope, target_id: str,
                 surface: str) -> ProbeResult: ...
