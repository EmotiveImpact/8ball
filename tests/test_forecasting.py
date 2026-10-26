"""Forecast measurement contracts, not evidence that any model can predict."""
from datetime import datetime, timedelta, timezone
import hashlib
import json

import pytest

from endstate.forecasting import Forecast, Resolution, evaluate, forecast_digest
from evals.prediction_bench import ROOT, prepare, run

CLOCK = datetime(2026, 10, 1, tzinfo=timezone.utc)


def forecast(id='one', probability=0.8, **changes):
    data = dict(id=id, event='Delivery is confirmed before the horizon', as_of=CLOCK,
                horizon=CLOCK + timedelta(days=1), input_sha256='a' * 64,
                predictor='controlled_test_fixture', probability=probability,
                abstention_reason='Insufficient information' if probability is None else None)
    return Forecast(**(data | changes))


def resolution(f, value=True, **changes):
    return Resolution(**(dict(forecast_id=f.id, forecast_sha256=forecast_digest(f), value=value,
                              available_at=CLOCK + timedelta(days=2), source_reference='Fictional fixture',
                              source_sha256='b' * 64, basis='synthetic') | changes))


def score(fs, rs):
    return evaluate(fs, rs, as_of=CLOCK + timedelta(days=3))


def test_scoring_uses_resolved_probabilities_and_reports_abstention_separately():
    fs = [forecast(), forecast('two', 0.1), forecast('three', None)]
    rs = [resolution(fs[0]), resolution(fs[1], False), resolution(fs[2])]
    before = [f.model_dump_json() for f in fs], [r.model_dump_json() for r in rs]
    report = score(fs, rs)
    assert report['brier'] == pytest.approx(0.025)
    assert report['fixed_half_baseline_brier_same_subset'] == 0.25
    assert report['coverage'] == 2 / 3
    assert (report['predicted'], report['abstained'], report['resolved'], report['scored']) == (2, 1, 3, 2)
    assert before == ([f.model_dump_json() for f in fs], [r.model_dump_json() for r in rs])
    assert not report['predictive_quality_approved'] and not report['facts_attested'] and not report['execution_authorized']


def test_unknown_outcome_is_not_false_or_an_incorrect_forecast():
    fs = [forecast(), forecast('two', 0), forecast('three', None)]
    report = score(fs, [resolution(fs[1], False)])
    assert report['scored'] == 1 and report['brier'] == 0
    assert report['resolved'] == 1 and report['unresolved'] == 2
    assert report['rows'][0]['value'] is None and report['rows'][0]['brier'] is None
    assert report['rows'][1]['value'] is False
    assert report['rows'][2]['abstention_reason'] and not report['rows'][2]['resolved']


def test_no_predictions_or_outcomes_never_becomes_perfect_accuracy():
    f = forecast(probability=None)
    empty = score([f], [])
    resolved = score([f], [resolution(f)])
    assert empty['brier'] is None and empty['coverage'] == 0 and empty['basis'] is None
    assert empty['fixed_half_baseline_brier_all_resolved'] is None
    assert resolved['brier'] is None and resolved['fixed_half_baseline_brier_same_subset'] is None
    assert resolved['fixed_half_baseline_brier_all_resolved'] == 0.25


@pytest.mark.parametrize('probability', [-0.1, 1.1, float('nan'), float('inf'), True, '0.6'])
def test_invalid_probabilities_are_rejected(probability):
    with pytest.raises(ValueError):
        forecast(probability=probability)


@pytest.mark.parametrize('change', [
    {'horizon': CLOCK}, {'horizon': CLOCK - timedelta(seconds=1)},
    {'as_of': CLOCK.replace(tzinfo=None)}, {'horizon': CLOCK.replace(tzinfo=None)},
    {'input_sha256': 'invalid'}, {'event': ' '}, {'predictor': ' '},
    {'probability': None, 'abstention_reason': None}, {'abstention_reason': 'But also confident'},
    {'probability': None, 'abstention_reason': ' '}, {'execution_authorized': True},
])
def test_invalid_forecast_contract(change):
    with pytest.raises(ValueError):
        forecast(**change)


@pytest.mark.parametrize('change', [
    {'available_at': CLOCK}, {'available_at': CLOCK + timedelta(days=4)},
    {'forecast_sha256': 'c' * 64}, {'forecast_id': 'missing'},
])
def test_wrong_or_unavailable_resolutions_fail_closed(change):
    f = forecast()
    with pytest.raises(ValueError):
        score([f], [resolution(f, **change)])


@pytest.mark.parametrize('value', [None, 0, 1, 'false'])
def test_resolution_requires_explicit_boolean(value):
    with pytest.raises(ValueError):
        resolution(forecast(), value)


def test_duplicate_and_empty_sets_are_rejected():
    f = forecast()
    for fs, rs in [([], []), ([f, f], []), ([f, forecast('two')], [resolution(f), resolution(f)]),
                   ([f], [resolution(f), resolution(f)])]:
        with pytest.raises(ValueError):
            score(fs, rs)


def test_synthetic_results_cannot_inflate_observed_scores():
    fs = [forecast(), forecast('two')]
    with pytest.raises(ValueError, match='separate evaluations'):
        score(fs, [resolution(fs[0]), resolution(fs[1], basis='observed')])


def test_invalid_and_future_evaluation_clocks():
    f = forecast()
    for now in [CLOCK.replace(tzinfo=None), CLOCK - timedelta(seconds=1)]:
        with pytest.raises(ValueError):
            evaluate([f], [], as_of=now)


def test_mutated_forecasts_cannot_bypass_validation_or_reuse_old_resolution():
    f = forecast()
    r = resolution(f)
    f.probability = 0.3
    with pytest.raises(ValueError, match='different forecast'):
        score([f], [r])
    f.__dict__['probability'] = -1
    with pytest.raises(ValueError):
        score([f], [])


def test_predictions_are_separate_from_labels_and_conditional_plans_remain_non_authoritative():
    manifest = json.loads((ROOT / 'evals/prediction-cases.json').read_text())
    fs, plans = prepare(manifest)
    assert len(fs) == len(plans) == 6
    for i in (0, 2, 4):
        assert fs[i].input_sha256 == fs[i + 1].input_sha256
    assert all(f.probability is None and f.predictor == 'not_configured' for f in fs)
    assert all(p['route_count'] and p['conditional'] and p['unknown_waits'] == [['attempt']]
               and p['approval_preserved'] and p['input_unchanged'] and not p['outcome_evidenced'] for p in plans)


def test_bench_preserves_frozen_inputs_and_does_not_claim_predictive_success(tmp_path):
    output = tmp_path / 'diagnostic'
    result = run(output)
    raw = (output / 'forecasts-before-outcomes.json').read_bytes()
    assert result['forecast_artifact_sha256'] == hashlib.sha256(raw).hexdigest()
    assert result['status'] == 'no_empirical_predictor'
    assert not result['empirical_prediction_tested'] and not result['actual_model_inference']
    assert result['evaluation']['coverage'] == 0 and result['evaluation']['scored'] == 0
    assert result['evaluation']['brier'] is None
    assert all(row['probability'] is None for row in json.loads(raw)['forecasts'])
    with pytest.raises(FileExistsError):
        run(output)
