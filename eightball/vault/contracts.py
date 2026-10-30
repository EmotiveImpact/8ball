"""Lane-local authority, encryption and scanner adapters."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol
import sqlite3

from eightball.authorisation import Identity, Resource


class VaultPermission(str, Enum):
    UPLOAD = 'upload'
    READ = 'read'
    DOWNLOAD = 'download'
    SCAN = 'scan'
    HOLD = 'hold'
    RETENTION = 'retention'
    DELETE = 'delete'
    AUDIT = 'audit'


class Authority(Protocol):
    def require(self, db: sqlite3.Connection, *, identity: Identity, case_id: str,
                object_id: str | None, permission: VaultPermission,
                now: datetime) -> Resource:
        """Read current grants on this transaction; return server-owned scope or deny."""


class KeyWrapper(Protocol):
    def wrap(self, key: bytes, *, context: bytes) -> dict: ...
    def unwrap(self, envelope: dict, *, context: bytes) -> bytes: ...


@dataclass(frozen=True)
class ScanResult:
    verdict: str
    engine: str
    version: str
    definitions: str
    content_sha256: str


class Scanner(Protocol):
    def scan(self, content: bytes, *, sha256: str, media_type: str) -> ScanResult:
        """Explicit bounded scan of supplied bytes; no source instructions or retries."""


class Conflict(ValueError):
    pass


class Unavailable(RuntimeError):
    pass


class IntegrityError(RuntimeError):
    pass
