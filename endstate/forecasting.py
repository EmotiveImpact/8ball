"""Score time-bound binary forecasts; never establish facts or action authority."""
from datetime import datetime
import hashlib
import json
from typing import Annotated, Literal

from pydantic import AwareDatetime, Field, model_validator

from .primitives import Identifier, Strict

VERSION = 'endstate.forecast-evaluation.v1'
Digest = Annotated[str, Field(pattern=r'^[0-9a-f]{64}$')]
Statement = Annotated[str, Field(min_length=1, max_length=1500, pattern=r'\S')]
Probability = Annotated[float, Field(strict=True, ge=0, le=1, allow_inf_nan=False)]


class Forecast(Strict):
    id: Identifier
    event: Statement
    as_of: AwareDatetime
    horizon: AwareDatetime
    input_sha256: Digest
    predictor: Statement
    probability: Probability | None = None
    abstention_reason: Statement | None = None

    @model_validator(mode='after')
    def bounded(self):
        if self.horizon <= self.as_of:
            raise ValueError('Forecast horizon must follow its information cutoff')
        if (self.probability is None) != (self.abstention_reason is not None):
            raise ValueError('Supply either a probability or an explicit abstention reason')
        return self


def forecast_digest(forecast: Forecast):
    forecast = Forecast.model_validate(forecast.model_dump(mode='python'))
    raw = json.dumps(forecast.model_dump(mode='json'), sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


class Resolution(Strict):
    forecast_id: Identifier
    forecast_sha256: Digest
    value: bool = Field(strict=True)
    available_at: AwareDatetime
    source_reference: Statement
    source_sha256: Digest
    basis: Literal['synthetic', 'observed']


def evaluate(forecasts: list[Forecast], resolutions: list[Resolution], *, as_of: datetime):
    if as_of.tzinfo is None or as_of.utcoffset() is None:
        raise ValueError('Evaluation clock must be timezone-aware')
    if not 1 <= len(forecasts) <= 10000 or len(resolutions) > len(forecasts):
        raise ValueError('Invalid evaluation size')
    forecasts = [Forecast.model_validate(f.model_dump(mode='python')) for f in forecasts]
    resolutions = [Resolution.model_validate(r.model_dump(mode='python')) for r in resolutions]
    by_id = {f.id: f for f in forecasts}
    outcomes = {r.forecast_id: r for r in resolutions}
    if len(by_id) != len(forecasts) or len(outcomes) != len(resolutions) or not outcomes.keys() <= by_id.keys():
        raise ValueError('Unknown or repeated forecast identifier')
    bases = {r.basis for r in resolutions}
    if len(bases) > 1:
        raise ValueError('Synthetic and observed outcomes require separate evaluations')
    if any(f.as_of > as_of for f in forecasts):
        raise ValueError('Forecast is later than the evaluation clock')
    for resolution in resolutions:
        forecast = by_id[resolution.forecast_id]
        if resolution.forecast_sha256 != forecast_digest(forecast):
            raise ValueError('Resolution refers to a different forecast')
        if not forecast.horizon <= resolution.available_at <= as_of:
            raise ValueError('Resolution is premature or unavailable at the evaluation cutoff')
    rows = []
    for forecast in forecasts:
        resolution = outcomes.get(forecast.id)
        scored = resolution is not None and forecast.probability is not None
        rows.append({'id': forecast.id, 'forecast_sha256': forecast_digest(forecast),
                     'probability': forecast.probability, 'abstention_reason': forecast.abstention_reason,
                     'resolved': resolution is not None, 'value': resolution.value if resolution else None,
                     'source_reference': resolution.source_reference if resolution else None,
                     'source_sha256': resolution.source_sha256 if resolution else None,
                     'brier': (forecast.probability - int(resolution.value)) ** 2 if scored else None,
                     'fixed_half_baseline_brier': (0.5 - int(resolution.value)) ** 2 if resolution else None})
    scored_rows = [r for r in rows if r['brier'] is not None]
    resolved_rows = [r for r in rows if r['resolved']]
    predicted = sum(f.probability is not None for f in forecasts)
    return {'version': VERSION, 'as_of': as_of.isoformat(), 'basis': next(iter(bases), None),
            'total': len(forecasts), 'predicted': predicted, 'abstained': len(forecasts) - predicted,
            'coverage': predicted / len(forecasts), 'resolved': len(resolutions),
            'unresolved': len(forecasts) - len(resolutions), 'scored': len(scored_rows),
            'brier': sum(r['brier'] for r in scored_rows) / len(scored_rows) if scored_rows else None,
            'fixed_half_baseline_brier_same_subset': 0.25 if scored_rows else None,
            'fixed_half_baseline_brier_all_resolved': 0.25 if resolved_rows else None,
            'rows': rows, 'facts_attested': False, 'execution_authorized': False,
            'predictive_quality_approved': False,
            'notice': 'Lower Brier is better on resolved forecasts. Coverage and missing outcomes remain separate. '
                      'A fixed 0.5 baseline is not a trained predictor. Caller-supplied outcome references are not independently verified; '
                      'hashes bind bytes but do not prove input cutoff integrity, prospective registration or calibration.'}
