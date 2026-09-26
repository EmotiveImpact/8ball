"""Case-local, immutable text originals and source-exact passage requests.

This is a bounded developer source store, not a production evidence vault. Old
Case/Evidence snapshots and the model input limit remain unchanged. Offsets are
Unicode code points, zero-based, end-exclusive, against the unchanged stored text.
"""
from __future__ import annotations

from hashlib import sha256
import re
import unicodedata
from typing import Annotated, Literal
from pydantic import Field, field_validator, model_validator
from ..models import Strict, Identifier, Title

MAX_SOURCE_CHARS = 200_000
MAX_SOURCE_BYTES = 800_000
MAX_CASE_SOURCE_BYTES = 8_000_000
MAX_DOCUMENTS = 50
MAX_PASSAGES = 12
MAX_BATCH_CHARS = 12_000  # Never enlarge the existing model-context allowance.
CHUNK_SIZE = 4_000
SOURCE_BODY_LIMIT = 1_300_000  # Includes escaped JSON text, not a model input limit.
LongText = Annotated[str, Field(strict=True, min_length=1, max_length=MAX_SOURCE_CHARS)]


def text_hash(text: str) -> str:
    return sha256(text.encode('utf-8', errors='strict')).hexdigest()


def comparison_hash(text: str) -> str:
    """Candidate discovery only. Never use this representation as evidence."""
    return text_hash(' '.join(unicodedata.normalize('NFC', text).split()))


def source_warnings(text: str) -> list[str]:
    warnings = []
    if text.startswith('\ufeff'):
        warnings.append('Leading UTF-8 byte-order mark retained in the original text.')
    if any(c in text for c in ('\u202a','\u202b','\u202c','\u202d','\u202e','\u2066','\u2067','\u2068','\u2069')):
        warnings.append('Bidirectional control characters present. Inspect the original carefully.')
    if '\u200b' in text or '\u2060' in text:
        warnings.append('Invisible word-separation characters present and retained.')
    return warnings


class SourceInput(Strict):
    title: Title
    source: Title
    text: LongText
    filename: str | None = Field(default=None, max_length=180)
    previous_document_id: Identifier | None = None

    @field_validator('text')
    @classmethod
    def safe_text(cls, value):
        if not value.strip():
            raise ValueError('Source text cannot be blank')
        if '\x00' in value:
            raise ValueError('NUL bytes are not supported in text sources')
        try:
            size = len(value.encode('utf-8', errors='strict'))
        except UnicodeEncodeError:
            raise ValueError('Source must be valid Unicode text without lone surrogate characters') from None
        if size > MAX_SOURCE_BYTES:
            raise ValueError('Source exceeds the 800,000-byte UTF-8 limit')
        return value

    @field_validator('title', 'source', 'filename')
    @classmethod
    def meaningful_metadata(cls, value):
        if value is not None and (not value.strip() or any(ord(c) < 32 for c in value)):
            raise ValueError('Source metadata must be non-blank single-line text')
        return value


class ImportPreview(SourceInput):
    expected_revision: int = Field(strict=True, ge=0)


class ImportSource(ImportPreview):
    event_id: Identifier
    duplicate_policy: Literal['reject', 'record_separately'] = 'reject'
    duplicate_reason: str = Field(default='', max_length=1000)

    @model_validator(mode='after')
    def separate_reason(self):
        if self.duplicate_policy == 'record_separately' and not self.duplicate_reason.strip():
            raise ValueError('Recording a duplicate separately requires a provenance reason')
        return self


class Passage(Strict):
    document_id: Identifier
    start: int = Field(strict=True, ge=0)
    end: int = Field(strict=True, ge=1)
    content_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

    @model_validator(mode='after')
    def bounded(self):
        if not 0 < self.end - self.start <= MAX_BATCH_CHARS:
            raise ValueError('A passage must contain 1 to 12,000 Unicode code points')
        return self


class PassagePreview(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    passages: list[Passage] = Field(min_length=1, max_length=MAX_PASSAGES)

    @model_validator(mode='after')
    def bounded_batch(self):
        if sum(p.end-p.start for p in self.passages) > MAX_BATCH_CHARS:
            raise ValueError('Selected passages together exceed the 12,000-character review batch')
        keys = {(p.document_id,p.start,p.end) for p in self.passages}
        if len(keys) != len(self.passages):
            raise ValueError('Repeated passage in selection')
        for i,p in enumerate(self.passages):
            for q in self.passages[i+1:]:
                if p.document_id == q.document_id and p.start < q.end and q.start < p.end:
                    raise ValueError('Selected passages overlap. Choose non-overlapping ranges')
        return self


class CapturePassages(PassagePreview):
    event_id: Identifier


class RetractSource(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True, ge=0)
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator('reason')
    @classmethod
    def reason_required(cls, value):
        if not value.strip():
            raise ValueError('Retraction requires a reason')
        return value


def line_starts(text: str) -> list[int]:
    return [0] + [m.end() for m in re.finditer(r'\r\n|\r|\n', text)]


def chunks(text: str) -> list[dict]:
    """Partition without dropping/normalising characters or splitting CRLF pairs."""
    from bisect import bisect_right
    lines = line_starts(text)
    result = []
    start = 0
    while start < len(text):
        end = min(len(text), start + CHUNK_SIZE)
        if end < len(text):
            floor = start + CHUNK_SIZE // 2
            # Prefer a paragraph or line boundary. No punctuation is discarded.
            newline = text.rfind('\n', floor, end)
            if newline >= floor:
                end = newline + 1
            elif text[end-1:end+1] == '\r\n':
                end -= 1
        part = text[start:end]
        result.append({'number':len(result)+1,'start':start,'end':end,
                       'line_start':bisect_right(lines,start),
                       'line_end':bisect_right(lines,max(start,end-1)),
                       'characters':end-start,'content_sha256':text_hash(part),
                       'preview':part[:180]})
        start = end
    return result


class SourceSelection(Strict):
    start: int = Field(strict=True, ge=0)
    end: int = Field(strict=True, ge=1)

    @model_validator(mode='after')
    def bounded(self):
        if not 0 < self.end-self.start <= MAX_BATCH_CHARS:
            raise ValueError('Select 1 to 12,000 Unicode code points')
        return self
