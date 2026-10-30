"""Neutral incoming-event contract. Ingestion never grants command authority."""
from typing import Literal

from pydantic import AwareDatetime, ConfigDict, Field

from .primitives import Identifier, Strict, Text


class IncomingEvent(Strict):
    model_config = ConfigDict(extra='forbid', frozen=True, allow_inf_nan=False)
    schema_version: Literal['endstate.incoming.v1'] = 'endstate.incoming.v1'
    organisation_id: Identifier
    matter_id: Identifier
    source_id: Identifier
    source_version: Identifier
    event_id: Identifier
    kind: Literal['source_received', 'proposal_received']
    occurred_at: AwareDatetime | None = None
    base_revision: int | None = Field(default=None, strict=True, ge=0)
    text: Text
    review_status: Literal['pending'] = 'pending'


class EventReceipt(Strict):
    event: IncomingEvent
    sequence: int = Field(strict=True, ge=1)
    received_at: AwareDatetime
    content_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    command_authority: Literal[False] = False
