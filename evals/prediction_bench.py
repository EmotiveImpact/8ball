"""Offline prediction-readiness diagnostic, not model inference or accuracy proof."""
from datetime import datetime
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from endstate.api import PlanRequest, calculate
from endstate.contracts import PlanningSnapshot, Graph, Condition, Action, Effect, Objective, atom
from endstate.forecasting import Forecast, Resolution, evaluate, forecast_digest


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def prepare(manifest):
    """No outcome input or provider access; missing forecast capability stays explicit."""
    forecasts, planning = [], []
    for case in manifest['cases']:
        context = {k: case[k] for k in ('event', 'known')}
        context.update(as_of=manifest['as_of'], horizon=manifest['horizon'])
        forecast = Forecast(id=case['id'], event=case['event'], as_of=manifest['as_of'],
                            horizon=manifest['horizon'], input_sha256=digest(context),
                            predictor='not_configured', abstention_reason='No empirical outcome predictor is configured. The planner returns conditional routes, not event probabilities.')
        snapshot = PlanningSnapshot(id=case['id'], deadline=forecast.horizon, graph=Graph(
            conditions=[Condition(id='confirmed', title=case['event'], confirmation='Explicit outcome evidence, not a predicted action effect')],
            actions=[Action(id='attempt', title='Attempt the fictional route', owner='Operator', purpose=case['known'],
                            minutes=15, contingent=True, wait_minutes=None, approval_required=True,
                            effects=[Effect(condition_id='confirmed')])],
            objectives=[Objective(id='goal', title=case['event'], success=atom('confirmed'))]))
        before = snapshot.model_dump_json()
        result = calculate(PlanRequest(snapshot=snapshot, as_of=forecast.as_of)).plan
        assert snapshot.model_dump_json() == before
        forecasts.append(forecast)
        planning.append({'id': case['id'], 'context_sha256': forecast.input_sha256,
                         'route_count': len(result['routes']),
                         'conditional': all(r['provisional'] for r in result['routes']),
                         'unknown_waits': [r['unknown_waits'] for r in result['routes']],
                         'approval_preserved': result['action_states']['attempt']['status'] == 'approval_required',
                         'outcome_evidenced': result['outcome_evidenced'], 'input_unchanged': True})
    return forecasts, planning


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    inputs = json.loads((ROOT / 'evals/prediction-cases.json').read_text())
    forecasts, planning = prepare(inputs)
    frozen = {'inputs_sha256': digest(inputs), 'forecasts': [f.model_dump(mode='json') for f in forecasts], 'planning': planning}
    prediction_path = output / 'forecasts-before-outcomes.json'
    prediction_path.write_text(json.dumps(frozen, indent=2) + '\n')
    prediction_hash = hashlib.sha256(prediction_path.read_bytes()).hexdigest()
    outcomes = json.loads((ROOT / 'evals/prediction-outcomes.json').read_text())
    if set(outcomes['outcomes']) != {f.id for f in forecasts}:
        raise ValueError('Outcome coverage differs from the declared diagnostic')
    resolutions = [Resolution(forecast_id=f.id, forecast_sha256=forecast_digest(f),
                              value=outcomes['outcomes'][f.id], available_at=outcomes['available_at'],
                              source_reference=outcomes['source'], source_sha256=digest(outcomes),
                              basis=outcomes['basis']) for f in forecasts]
    score = evaluate(forecasts, resolutions, as_of=datetime.fromisoformat(outcomes['available_at'].replace('Z', '+00:00')))
    report = {'status': 'no_empirical_predictor', 'actual_model_inference': False,
              'empirical_prediction_tested': False, 'forecast_artifact_sha256': prediction_hash,
              'inputs_sha256': digest(inputs), 'outcomes_sha256': digest(outcomes),
              'planning': planning, 'evaluation': score,
              'limitations': ['Six author-created possible worlds, not observed outcomes or a representative sample.',
                              'Inputs are separated from outcomes at execution time, not independently blinded to their author.',
                              'Each identical-context pair has opposite hypothetical outcomes: possible routes alone cannot settle which world occurs.',
                              'No forecast adapter is configured; the harness records missing capability, not a model decision to abstain.',
                              'Neither predictive accuracy nor calibration has been established.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New output directory; existing runs are never overwritten')
    args = parser.parse_args()
    report = run(args.output)
    print(json.dumps({k: report[k] for k in ('status', 'actual_model_inference', 'empirical_prediction_tested')}))
    score = report['evaluation']
    print(f"Forecast coverage: {score['predicted']}/{score['total']}. Prediction accuracy: NOT ASSESSED. Conditional routes are not forecasts.")
