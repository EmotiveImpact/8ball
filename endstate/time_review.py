"""Explicit civil-time interpretation, not natural-language date guessing.

Use the configured IANA timezone database. Reject gaps and require a choice for
folds; never replace an ambiguous source date with the machine's current date.
"""
from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Literal
from pydantic import Field, field_validator, model_validator
from .primitives import Strict


class TimeInterpretation(Strict):
    basis: Literal['absolute', 'relative_days'] = 'absolute'
    calendar_date: str | None = None
    anchor_date: str | None = None
    day_offset: int | None = Field(default=None, strict=True, ge=-366, le=366)
    anchor_reason: str = Field(default='', max_length=1000)
    wall_time: str = Field(pattern=r'^([01][0-9]|2[0-3]):[0-5][0-9]$')
    time_zone: str = Field(min_length=1, max_length=80)
    zone_reason: str = Field(min_length=3, max_length=1000)
    fold: int | None = Field(default=None, strict=True, ge=0, le=1)

    @field_validator('calendar_date', 'anchor_date')
    @classmethod
    def exact_date(cls, value):
        if value is not None:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                raise ValueError('Use an explicit ISO calendar date: YYYY-MM-DD')
            date.fromisoformat(value)
        return value

    @field_validator('time_zone', 'zone_reason')
    @classmethod
    def not_blank(cls, value):
        if value != value.strip() or not value.strip():
            raise ValueError('Timezone and its stated basis must be explicit, non-blank values')
        return value

    @model_validator(mode='after')
    def basis_fields(self):
        if self.basis == 'absolute':
            if self.calendar_date is None or self.anchor_date is not None or self.day_offset is not None or self.anchor_reason:
                raise ValueError('An absolute date needs calendar_date only, not a relative anchor')
        elif self.calendar_date is not None or self.anchor_date is None or self.day_offset is None or len(self.anchor_reason.strip()) < 3:
            raise ValueError('A relative date needs an explicit anchor date, day offset and reason; no implicit today')
        return self


def interpret_time(spec: TimeInterpretation) -> dict:
    """Return all real instants for this wall clock time, plus any required review."""
    spec = TimeInterpretation.model_validate(spec.model_dump())
    # Reject timezone abbreviations except explicit UTC. They are not globally
    # unambiguous locations and can accidentally stand in for missing context.
    if spec.time_zone != 'UTC' and ('/' not in spec.time_zone or spec.time_zone.startswith(('posix/', 'right/'))):
        raise ValueError('Choose an IANA location such as Europe/London, or UTC; do not use BST/EST abbreviations')
    try:
        zone = ZoneInfo(spec.time_zone)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError('Timezone is unavailable. Choose an installed IANA zone; this system may require the tzdata package') from None
    try:
        civil_date = (date.fromisoformat(spec.calendar_date) if spec.basis == 'absolute' else
                      date.fromisoformat(spec.anchor_date) + timedelta(days=spec.day_offset))
        civil = datetime.fromisoformat(civil_date.isoformat() + 'T' + spec.wall_time)
    except (OverflowError, ValueError):
        raise ValueError('The interpreted calendar date is out of range') from None
    options = []
    seen = set()
    try:
        for fold in (0, 1):
            aware = civil.replace(tzinfo=zone, fold=fold)
            utc = aware.astimezone(timezone.utc)
            returned = utc.astimezone(zone)
            if returned.replace(tzinfo=None) != civil:
                continue  # Nonexistent local time: do not shift it into existence.
            stamp = utc.isoformat()
            if stamp in seen:
                continue
            seen.add(stamp)
            options.append({'fold': fold, 'utc': stamp, 'local': aware.isoformat(),
                            'zone_name': aware.tzname(), 'offset_seconds': int(aware.utcoffset().total_seconds())})
    except (OverflowError, ValueError):
        raise ValueError('Timezone conversion is out of supported range') from None
    if not options:
        status, selected = 'nonexistent', None
    elif len(options) > 1 and spec.fold is None:
        status, selected = 'ambiguous', None
    elif len(options) == 1:
        if spec.fold is not None:
            raise ValueError('This time is not ambiguous. Remove the fold choice rather than silently ignoring it')
        status, selected = 'resolved', options[0]
    else:
        status, selected = 'resolved', next(o for o in options if o['fold'] == spec.fold)
    return {'status': status, 'calendar_date': civil_date.isoformat(), 'wall_time': spec.wall_time,
            'time_zone': spec.time_zone, 'basis': spec.model_dump(mode='json'),
            'options': options, 'selected': selected,
            'notice': 'An explicit operator interpretation of source wording, not an automatically verified deadline.'}
