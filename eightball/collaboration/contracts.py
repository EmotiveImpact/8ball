"""Explicit host-owned transaction adapters for fictional local engineering."""
from datetime import datetime
import sqlite3
from typing import Literal, Protocol

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

from ..authorisation import Identity, Resource


class Record(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)


class SourceVersion(Record):
    object_id: str = Field(min_length=1, max_length=128)
    version: int = Field(ge=1, strict=True)
    vault_revision: int = Field(ge=1, strict=True)
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


class Binding(Record):
    case_id: str = Field(min_length=1, max_length=128)
    resource: Resource
    case_revision: int = Field(ge=0, strict=True)
    object_revision: int = Field(ge=0, strict=True)
    sources: tuple[SourceVersion, ...] = Field(default=(), max_length=50)


class GrantRequest(Record):
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,100}$')
    recipient: Identity
    purpose: Literal['expert', 'client_projection']
    object_id: str | None = Field(default=None, min_length=1, max_length=128)
    projection_id: str | None = Field(default=None, pattern=r'^[A-Za-z0-9_-]{1,100}$')
    valid_from: AwareDatetime
    expires_at: AwareDatetime
    rationale: str = Field(min_length=10, max_length=2000)

    @model_validator(mode='after')
    def scope(self):
        if self.valid_from >= self.expires_at:
            raise ValueError('Grant expiry must follow its start')
        if self.purpose == 'client_projection' and (not self.object_id or not self.projection_id):
            raise ValueError('A client grant requires an exact object and projection')
        if self.purpose == 'expert' and self.projection_id is not None:
            raise ValueError('Expert grants cannot name a client projection')
        if len(self.rationale.strip()) < 10:
            raise ValueError('A meaningful rationale is required')
        return self


class CurrentPolicy(Protocol):
    def require(self, db: sqlite3.Connection, identity: Identity, binding: Binding,
                capability: str) -> None:
        """Raise PermissionError unless current identity/roles/grants permit it.

        Must use the passed transaction and exact tenant/matter/object. Capabilities
        are NOT aliases for generic READ/WRITE; clients cannot be internal readers.
        """


class CaseObjects(Protocol):
    def binding(self, db: sqlite3.Connection, case_id: str, object_id: str | None) -> Binding:
        """Read exact scope, case/object revisions and source versions, without I/O."""

    def expert_view(self, db: sqlite3.Connection, binding: Binding) -> dict:
        """Read only the bound object, never a whole case for an object grant."""


class SourceLifecycle(Protocol):
    def require_current(self, db: sqlite3.Connection, binding: Binding, *, identity: Identity) -> None:
        """Deny removed, quarantined, changed or unavailable referenced sources.

        Check lifecycle in this transaction; no network, original bytes or implicit
        source read grants for clients. Empty source sets are valid manual drafts.
        """


class VaultSources:
    """Consume the vault's transaction gate, never a standalone metadata preview."""
    def __init__(self, vault):
        if not callable(getattr(vault, 'require_source', None)):
            raise ValueError('A transaction-local vault source gate is required')
        self.vault = vault

    def require_current(self, db, binding, *, identity):
        if not db.in_transaction:
            raise PermissionError('Source checks require the collaboration transaction')
        for source in binding.sources:
            handle = self.vault.require_source(
                db, identity=identity, case_id=binding.case_id, object_id=source.object_id,
                expected_revision=source.vault_revision, expected_sha256=source.sha256,
            )
            if type(handle.get('schema_version')) is not int or handle['schema_version'] != 1:
                raise PermissionError('Unsupported vault source gate schema')
            current = SourceVersion.model_validate({key: handle[key] for key in SourceVersion.model_fields})
            if (current != source or handle['case_id'] != binding.case_id
                    or handle['organisation_id'] != binding.resource.organisation_id
                    or handle['matter_id'] != binding.resource.matter_id):
                raise PermissionError('Vault source gate returned a different scope/version')
