"""Matter-scoped policy for the agency build, not an authentication adapter.

Inputs must come from verified identity and server-owned membership records.
The opt-in agency boundary consumes this policy; trusted-local mode is separate.
Never accept these records from request bodies or treat a permit as case/action approval.
"""
from datetime import datetime
from enum import Enum

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class Operation(str, Enum):
    READ = 'read'
    WRITE = 'write'
    EXPORT = 'export'
    SEARCH = 'search'
    INFER = 'infer'
    DOWNLOAD = 'download'


class Record(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, strict=True)


class Identity(Record):
    issuer: str = Field(min_length=1, max_length=2048)
    subject: str = Field(min_length=1, max_length=512)


class Resource(Record):
    organisation_id: str = Field(min_length=1, max_length=128)
    matter_id: str = Field(min_length=1, max_length=128)
    object_id: str | None = Field(default=None, min_length=1, max_length=128)


class Grant(Record):
    identity: Identity
    resource: Resource
    operations: frozenset[Operation]
    valid_from: AwareDatetime
    expires_at: AwareDatetime
    revoked: bool = False


def permits(identity: Identity, resource: Resource, operation: Operation,
            grants: tuple[Grant, ...], *, now: datetime) -> bool:
    """Deny by default; exact tenant/matter and issuer/subject matching.

    Object grants never grant a matter listing/search/export or a different
    object. Callers must check every object consumed by inference and exports.
    Revocation is read afresh by callers, not cached in a browser capability.
    Invalid or naive clocks deny instead of extending a grant indefinitely.
    """
    if (not isinstance(identity, Identity) or not isinstance(resource, Resource)
            or not isinstance(operation, Operation) or not isinstance(now, datetime)
            or now.tzinfo is None or now.utcoffset() is None):
        return False
    for grant in grants:
        if not isinstance(grant, Grant) or grant.revoked:
            continue
        scope = grant.resource
        if (grant.identity == identity
                and scope.organisation_id == resource.organisation_id
                and scope.matter_id == resource.matter_id
                and (scope.object_id is None or scope.object_id == resource.object_id)
                and operation in grant.operations
                and grant.valid_from <= now < grant.expires_at):
            return True
    return False
