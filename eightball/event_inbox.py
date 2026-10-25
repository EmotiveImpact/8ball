"""Durable local event inbox owned by the host, separate from case commands.

Callers must establish access and supply the trusted matter scope. This module
neither polls connectors nor runs inference, mutates a case or replays actions.
SQLite is a development implementation, not production tenant isolation.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import sqlite3

from endstate.events import IncomingEvent, EventReceipt


def _body(event: IncomingEvent) -> str:
    return json.dumps(event.model_dump(mode='json'), sort_keys=True,
                      ensure_ascii=False, separators=(',', ':'), allow_nan=False)


class EventConflict(ValueError):
    pass


class EventInbox:
    def __init__(self, path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('''CREATE TABLE IF NOT EXISTS incoming_events (
                organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL,
                source_id TEXT NOT NULL, event_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, received_at TEXT NOT NULL,
                body TEXT NOT NULL, digest TEXT NOT NULL,
                PRIMARY KEY(organisation_id,matter_id,source_id,event_id),
                UNIQUE(organisation_id,matter_id,sequence))''')

    @staticmethod
    def _receipt(row) -> EventReceipt:
        sequence, received_at, body, digest = row
        if sha256(body.encode()).hexdigest() != digest:
            raise EventConflict('Stored incoming event failed integrity verification')
        return EventReceipt(event=IncomingEvent.model_validate_json(body),
                            sequence=sequence, received_at=datetime.fromisoformat(received_at),
                            content_sha256=digest)

    def append(self, event: IncomingEvent, *, organisation_id: str, matter_id: str) -> EventReceipt:
        if (event.organisation_id, event.matter_id) != (organisation_id, matter_id):
            raise EventConflict('Event does not match the authorised matter scope')
        body = _body(event)
        digest = sha256(body.encode()).hexdigest()
        key = (organisation_id, matter_id, event.source_id, event.event_id)
        with sqlite3.connect(self.path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('''SELECT sequence,received_at,body,digest FROM incoming_events
                WHERE organisation_id=? AND matter_id=? AND source_id=? AND event_id=?''', key).fetchone()
            if old:
                receipt = self._receipt(old)
                if old[2] != body:
                    raise EventConflict('An existing event identity has different content')
                return receipt
            sequence = db.execute('''SELECT COALESCE(MAX(sequence),0)+1 FROM incoming_events
                WHERE organisation_id=? AND matter_id=?''', key[:2]).fetchone()[0]
            received = datetime.now(timezone.utc).isoformat()
            db.execute('INSERT INTO incoming_events VALUES (?,?,?,?,?,?,?,?)',
                       (*key, sequence, received, body, digest))
            return self._receipt((sequence, received, body, digest))

    def read(self, *, organisation_id: str, matter_id: str, after: int = 0,
             limit: int = 100) -> list[EventReceipt]:
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError('Invalid inbox page')
        with sqlite3.connect(self.path) as db:
            rows = db.execute('''SELECT sequence,received_at,body,digest FROM incoming_events
                WHERE organisation_id=? AND matter_id=? AND sequence>? ORDER BY sequence LIMIT ?''',
                (organisation_id, matter_id, after, limit)).fetchall()
        receipts = [self._receipt(row) for row in rows]
        if any((r.event.organisation_id, r.event.matter_id) != (organisation_id, matter_id) for r in receipts):
            raise EventConflict('Stored event scope does not match its inbox')
        return receipts
