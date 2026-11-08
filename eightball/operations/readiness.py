"""Bounded evidence consumption and fictional study analysis; no sign-offs."""
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from .contracts import Strict


class Evidence(Strict):
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,100}$')
    capability: Literal['onboarding', 'support', 'terms', 'brand_licence', 'operating_owner',
                        'security', 'accessibility', 'recovery', 'model_policy',
                        'customer_acceptance', 'pilot', 'advertised_capabilities']
    environment: str = Field(pattern=r'^[A-Za-z0-9_.-]{1,100}$')
    kind: Literal['software', 'human', 'independent', 'legal', 'owner']
    status: Literal['passed', 'failed', 'blocked', 'unknown']
    path: str = Field(min_length=1, max_length=512)
    sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    source_commit: str = Field(pattern=r'^[a-f0-9]{40}$')
    recorded_at: datetime


class ReadinessManifest(Strict):
    source_commit: str = Field(pattern=r'^[a-f0-9]{40}$')
    environments: tuple[Annotated[str, Field(pattern=r'^[A-Za-z0-9_.-]{1,100}$')], ...] = Field(min_length=1, max_length=20)
    evidence: tuple[Evidence, ...] = Field(default=(), max_length=500)


CAPABILITIES = {
    'onboarding': {'software', 'human'}, 'support': {'software', 'owner'},
    'terms': {'legal'}, 'brand_licence': {'legal'}, 'operating_owner': {'owner'},
    'security': {'software', 'independent'}, 'accessibility': {'software', 'human'},
    'recovery': {'software', 'owner'}, 'model_policy': {'owner', 'independent'},
    'customer_acceptance': {'human'}, 'pilot': {'human', 'independent'},
    'advertised_capabilities': {'software', 'owner'},
}


def evaluate_readiness(manifest: ReadinessManifest, *, root, now: datetime,
                       maximum_age_seconds=30 * 86400):
    if (now.tzinfo is None or now.utcoffset() is None
            or type(maximum_age_seconds) is not int or maximum_age_seconds < 0):
        raise ValueError('Aware clock and nonnegative freshness policy required')
    if len(set(manifest.environments)) != len(manifest.environments):
        raise ValueError('Environments must be unique')
    if len({e.id for e in manifest.evidence}) != len(manifest.evidence):
        raise ValueError('Evidence IDs must be unique')
    root = Path(root).resolve(strict=True)
    observations = []
    for evidence in manifest.evidence:
        reason = None
        path = Path(evidence.path)
        if path.is_absolute() or '..' in path.parts:
            reason = 'unsafe_path'
        else:
            candidate = (root / path).resolve()
            if not candidate.is_relative_to(root):
                reason = 'unsafe_path'
            elif not candidate.is_file():
                reason = 'missing_artifact'
            elif candidate.stat().st_size > 10_000_000:
                reason = 'artifact_too_large'
            elif sha256(candidate.read_bytes()).hexdigest() != evidence.sha256:
                reason = 'artifact_digest_mismatch'
        if evidence.source_commit != manifest.source_commit:
            reason = 'source_mismatch'
        if evidence.recorded_at.tzinfo is None or evidence.recorded_at.utcoffset() is None:
            reason = 'unknown_timestamp'
        elif not 0 <= (now - evidence.recorded_at).total_seconds() <= maximum_age_seconds:
            reason = 'stale_or_future_evidence'
        if evidence.status != 'passed':
            reason = 'not_passed'
        observations.append({'id': evidence.id, 'capability': evidence.capability,
                             'environment': evidence.environment, 'kind': evidence.kind,
                             'artifact_consistent': reason is None, 'reason': reason,
                             'authenticity_verified': False})
    gaps = []
    for environment in manifest.environments:
        for capability, kinds in CAPABILITIES.items():
            for kind in sorted(kinds):
                if not any(o['artifact_consistent'] and o['environment'] == environment
                           and o['capability'] == capability and o['kind'] == kind for o in observations):
                    gaps.append({'environment': environment, 'capability': capability, 'kind': kind})
    return {'status': 'blocked' if gaps else 'evidence_supplied_pending_authentication',
            'gaps': gaps, 'evidence': observations, 'artifact_consistency_only': True,
            'human_decisions_authenticated': False, 'release_authorized': False,
            'deployment_authorized': False, 'real_pilot_authorized': False}


class PilotObservation(Strict):
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,100}$')
    participant_id: str = Field(pattern=r'^fictional-[A-Za-z0-9_-]{1,80}$')
    dimension: Literal['usefulness', 'safety', 'corrections', 'confidentiality']
    outcome: Literal['pass', 'fail', 'unknown']
    severity: Literal['critical', 'high', 'medium', 'low']
    correction_count: int = Field(ge=0, le=10000)
    decision_seconds: int | None = Field(default=None, ge=0, le=86400)
    resolution_evidence_sha256: str | None = Field(default=None, pattern=r'^[a-f0-9]{64}$')


class FictionalPilot(Strict):
    fictional: Literal[True]
    protocol_id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,100}$')
    participants: tuple[Annotated[str, Field(pattern=r'^fictional-[A-Za-z0-9_-]{1,80}$')], ...] = Field(min_length=1, max_length=100)
    observations: tuple[PilotObservation, ...] = Field(default=(), max_length=10000)


def summarize_pilot(study: FictionalPilot):
    if (len(set(study.participants)) != len(study.participants)
            or any(not p.startswith('fictional-') for p in study.participants)
            or len({o.id for o in study.observations}) != len(study.observations)
            or any(o.participant_id not in study.participants for o in study.observations)):
        raise ValueError('Unique fictional participants and observations required')
    missing = [{'participant_id': p, 'dimension': d} for p in study.participants
               for d in ('usefulness', 'safety', 'corrections', 'confidentiality')
               if not any(o.participant_id == p and o.dimension == d for o in study.observations)]
    failed = [o.id for o in study.observations if o.outcome == 'fail']
    unknown = [o.id for o in study.observations if o.outcome == 'unknown']
    unresolved = [o.id for o in study.observations if o.outcome == 'fail'
                  and o.severity in ('critical', 'high') and o.resolution_evidence_sha256 is None]
    return {'status': 'blocked' if missing or failed or unknown else 'fictional_observations_recorded',
            'missing_dimensions': missing, 'failed_observations': failed,
            'unknown_observations': unknown, 'unresolved_critical_or_high': unresolved,
            'correction_count': sum(o.correction_count for o in study.observations),
            'observed_decision_seconds': [o.decision_seconds for o in study.observations
                                          if o.decision_seconds is not None],
            'real_participants': False, 'usefulness_validated': False,
            'pilot_accepted': False, 'wider_release_authorized': False}
