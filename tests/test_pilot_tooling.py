import json
from pathlib import Path
import subprocess
import sys

import pytest
from pydantic import ValidationError

from eightball.operations.readiness import FictionalPilot, PilotObservation, summarize_pilot


def observation(**kwargs):
    values = dict(id='fictional-observation', participant_id='fictional-operator', dimension='safety',
                  outcome='pass', severity='critical', correction_count=0)
    values.update(kwargs)
    return PilotObservation(**values)


def study(observations=()):
    return FictionalPilot(fictional=True, protocol_id='fictional-protocol',
                          participants=('fictional-operator',), observations=tuple(observations))


def test_empty_study_not_a_pilot_pass():
    report = summarize_pilot(study())
    assert report['status'] == 'blocked' and len(report['missing_dimensions']) == 4


def test_recorded_fictional_study_never_validates_real_usefulness_or_acceptance():
    observations = [observation(id=f'fictional-{d}', dimension=d, correction_count=2, decision_seconds=15)
                    for d in ('safety', 'confidentiality', 'corrections', 'usefulness')]
    report = summarize_pilot(study(observations))
    assert report['status'] == 'fictional_observations_recorded'
    assert report['correction_count'] == 8 and report['observed_decision_seconds'] == [15] * 4
    assert not report['pilot_accepted'] and not report['wider_release_authorized']
    assert not report['usefulness_validated'] and not report['real_participants']


@pytest.mark.parametrize('outcome', ['fail', 'unknown'])
def test_negative_and_unknown_preserved_not_treated_as_false_or_pass(outcome):
    report = summarize_pilot(study([observation(outcome=outcome)]))
    assert report['status'] == 'blocked'
    key = 'failed_observations' if outcome == 'fail' else 'unknown_observations'
    assert report[key] == ['fictional-observation']
    if outcome == 'fail':
        assert report['unresolved_critical_or_high'] == ['fictional-observation']


def test_resolution_reference_does_not_erase_original_failed_observation():
    report = summarize_pilot(study([observation(outcome='fail', resolution_evidence_sha256='a' * 64)]))
    assert report['unresolved_critical_or_high'] == []
    assert report['failed_observations'] == ['fictional-observation'] and report['status'] == 'blocked'


def test_real_participant_and_unlisted_or_duplicate_records_rejected():
    with pytest.raises(ValidationError):
        observation(participant_id='real-person')
    with pytest.raises(ValidationError):
        FictionalPilot(fictional=False, protocol_id='fictional-study', participants=('real-person',))
    with pytest.raises(ValueError):
        summarize_pilot(study([observation(participant_id='fictional-other')]))
    with pytest.raises(ValueError):
        summarize_pilot(study([observation(), observation()]))


def test_pilot_cli_validates_actual_input_and_blocks_missing_dimensions(tmp_path):
    path = tmp_path / 'pilot.json'
    path.write_text(study([observation(outcome='fail')]).model_dump_json())
    result = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/operations/check.py'), 'pilot', str(path)],
                             capture_output=True, text=True)
    assert result.returncode == 1
    assert json.loads(result.stdout)['unresolved_critical_or_high'] == ['fictional-observation']
