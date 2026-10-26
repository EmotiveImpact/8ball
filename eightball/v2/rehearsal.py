"""Local, append-only assumption briefs; never case commands or model calls."""
from datetime import datetime, timedelta
import json

from pydantic import AwareDatetime, Field, model_validator

from endstate.rehearsal import Branch, Draft, VERSION, changed_fields, coverage, validate_references
from .contracts import Case, Identifier, Strict
from .plan_review import assessment, reference_catalogue, TTL_MINUTES
from endstate.scenarios import Scenario, compare as compare_scenario
from .planner import to_snapshot
from ..models import utcnow
from ..store import Conflict, canonical, digest

MAX_BYTES = 131072
MAX_HISTORY = 100
Hash = str


class Trial(Branch):
    scenario: Scenario

    @model_validator(mode='after')
    def explicit_overlay(self):
        s = self.scenario
        if not (s.budget is not None or s.deadline is not None or s.conditions or s.unavailable_actions or s.resource_starts or s.decisions):
            raise ValueError('Each branch needs an explicit hypothetical overlay')
        if len(set(s.unavailable_actions)) != len(s.unavailable_actions):
            raise ValueError('Repeated unavailable action')
        return self


class Prepare(Draft):
    expected_revision: int = Field(strict=True, ge=0)
    branches: list[Trial] = Field(default_factory=list, max_length=3)
    predecessor_sha256: Hash | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')


class Save(Strict):
    event_id: Identifier
    expected_sequence: int = Field(strict=True, ge=0)
    as_of: AwareDatetime
    brief_sha256: Hash = Field(pattern=r'^[0-9a-f]{64}$')
    draft: Prepare


def reference_hashes(case):
    values = {'case:desired_outcome': case.desired_outcome, 'case:summary': case.summary}
    for kind, objects in [('objective', case.graph.objectives), ('condition', case.graph.conditions),
                          ('action', case.graph.actions), ('source', case.evidence), ('actor', case.actors),
                          ('constraint', case.constraints), ('decision', case.decisions)]:
        values.update({kind + ':' + obj.id: obj.model_dump(mode='json') for obj in objects})
    return {ref: digest(value) for ref, value in values.items()}


def prepare(case, request: Prepare, as_of, predecessor=None):
    request = Prepare.model_validate(request.model_dump(mode='python'))
    if request.expected_revision != case.revision:
        raise Conflict('The case changed. Reopen the challenge against the live snapshot.')
    validate_references(request, {ref['id'] for ref in reference_catalogue(case)})
    if request.predecessor_sha256 != (predecessor or {}).get('brief_sha256'):
        raise Conflict('The predecessor brief is missing or changed')
    if predecessor:
        original = Prepare.model_validate(predecessor['draft'])
        if original.perspectives != request.perspectives or original.contributions != request.contributions:
            raise ValueError('Rechecks preserve original perspectives and contributions; start a separate brief for new declarations')
        if original.perspectives_not_applicable_reason != request.perspectives_not_applicable_reason:
            raise ValueError('Rechecks preserve the original perspective coverage declaration')
    baseline = assessment(case, [], as_of)
    trials = []
    for branch in request.branches:
        if branch.scenario.expected_revision != case.revision:
            raise Conflict('Every branch must use the same live case revision')
        if set(branch.scenario.unavailable_actions) & set(case.completed):
            raise ValueError('A scenario cannot remove completed history')
        if any(not a.enabled for a in case.graph.actions if a.id in branch.scenario.unavailable_actions):
            raise ValueError('A scenario cannot remove an already disabled action')
        comparison = compare_scenario(to_snapshot(case), branch.scenario, as_of)
        result, manifest = comparison['result'], comparison['manifest']
        trials.append({'id': branch.id, 'hypothetical': True, 'persisted': False,
                       'validation': 'valid', 'result': result, 'manifest': manifest,
                       'manifest_sha256': digest(manifest), 'baseline': comparison['baseline'],
                       'compatible_change': result['constraint_compatible'] - baseline['inspection']['baseline']['constraint_compatible']})
    refs = reference_hashes(case)
    reconsideration = None
    if predecessor:
        old = predecessor['reference_hashes']
        reconsideration = {'previous_revision': predecessor['case_revision'],
                          'changed_references': sorted(ref for ref in old.keys() | refs.keys() if old.get(ref) != refs.get(ref)),
                          'baseline_changed': predecessor['baseline']['inspection']['baseline'] != baseline['inspection']['baseline'],
                          'branch_changes': changed_fields(predecessor['draft']['branches'], request.model_dump(mode='json')['branches']),
                          'semantics_verified': False,
                          'notice': 'Changed records and calculations require human review; no hypothesis was confirmed or disproved.'}
    body = {'contract_version': VERSION, 'case_id': case.id, 'case_revision': case.revision,
            'snapshot_sha256': digest(case.model_dump(mode='json')), 'as_of': as_of.isoformat(),
            'expires_at': (as_of + timedelta(minutes=TTL_MINUTES)).isoformat(),
            'draft': request.model_dump(mode='json'), 'baseline': baseline, 'branches': trials,
            'reference_hashes': refs, 'coverage': coverage(request), 'reconsideration': reconsideration,
            'hypothetical': True, 'facts_attested': False, 'execution_authorised': False,
            'live_case_changed': False, 'artifact_persisted': False,
            'provider': None, 'model': None, 'adapter_version': None, 'inference_calls': 0,
            'cost_not_incurred': True,
            'tasks': [{'role_task_id': p.id, 'attempt_id': 'operator-declaration', 'state': 'declared'} for p in request.perspectives],
            'notice': 'Hypothetical operator declarations, not generated stakeholder behavior, predictions, consent or independent review. Nothing is applied to the live case.'}
    result = {**body, 'brief_sha256': digest(body)}
    if len(canonical(result).encode('utf-8')) > MAX_BYTES:
        raise ValueError('Challenge exceeds the 128 KiB artifact limit; reduce the declared scope')
    return result


def read_rows(db, case_id):
    return [dict(row) for row in db.execute('SELECT * FROM v2_rehearsals WHERE case_id=? ORDER BY sequence', (case_id,))]


def export_rows(rows, case_id, events=None):
    if not rows:
        return None
    previous, records, known, event_ids = None, [], {}, set()
    snapshots = {e['revision']: e['state_hash'] for e in events} if events is not None else None
    try:
        if len(rows) > MAX_HISTORY:
            raise ValueError('Challenge history limit exceeded')
        for sequence, row in enumerate(rows, 1):
            record = json.loads(row['record'])
            brief = record['brief']
            draft = Prepare.model_validate(brief['draft'])
            content = {k: v for k, v in brief.items() if k != 'brief_sha256'}
            if (sequence != row['sequence'] or sequence != record['sequence']
                    or record['case_id'] != case_id or row['case_id'] != case_id or brief['case_id'] != case_id
                    or record['event_id'] != row['event_id'] or record['previous_hash'] != previous
                    or record['event_id'] in event_ids
                    or digest(record) != row['hash'] or digest(content) != brief['brief_sha256']
                    or brief['contract_version'] != VERSION or draft.expected_revision != brief['case_revision']
                    or draft.predecessor_sha256 is not None and draft.predecessor_sha256 not in known
                    or snapshots is not None and snapshots.get(brief['case_revision']) != brief['snapshot_sha256']):
                raise ValueError('Invalid challenge history')
            as_of = datetime.fromisoformat(brief['as_of'])
            recorded_at = datetime.fromisoformat(record['recorded_at'])
            saved = Save(event_id=record['event_id'], expected_sequence=sequence-1, as_of=as_of,
                         brief_sha256=brief['brief_sha256'], draft=draft)
            if (digest(saved.model_dump(mode='json')) != record['request_hash']
                    or not as_of <= recorded_at <= as_of + timedelta(minutes=TTL_MINUTES)
                    or brief['coverage'] != coverage(draft)
                    or brief['hypothetical'] is not True or brief['facts_attested'] is not False
                    or brief['execution_authorised'] is not False or brief['live_case_changed'] is not False
                    or brief['provider'] is not None or brief['model'] is not None or brief['inference_calls'] != 0
                    or record['artifact_persisted'] is not True or record['live_case_changed'] is not False
                    or record['actor'] != 'local-operator'
                    or len(canonical(brief).encode('utf-8')) > MAX_BYTES):
                raise ValueError('Invalid challenge metadata')
            if events is not None:
                snapshot = Case.model_validate(next(e['state_after'] for e in events if e['revision'] == brief['case_revision']))
                if prepare(snapshot, draft, as_of, known.get(draft.predecessor_sha256)) != brief:
                    raise ValueError('Challenge failed deterministic replay')
            records.append({**record, 'hash': row['hash']})
            previous = row['hash']; known[brief['brief_sha256']] = brief; event_ids.add(record['event_id'])
    except (ValueError, KeyError, TypeError, AttributeError, StopIteration):
        return {'valid': False, 'records': [], 'error': 'Assumption challenge history failed verification'}
    return {'valid': True, 'records': records, 'head_hash': previous,
            'authority': 'Local derived-artifact integrity only; not independently anchored evidence or action approval.'}


class Rehearsals:
    def __init__(self, store):
        self.store = store

    def _context(self, db, case_id):
        case = self.store._get(db, case_id)
        events, previous = [], None
        try:
            for revision, row in enumerate(db.execute('SELECT * FROM v2_events WHERE case_id=? ORDER BY revision', (case_id,))):
                event = json.loads(row['record'])
                snapshot = Case.model_validate(event['state_after'])
                if (event['case_id'] != case_id or snapshot.id != case_id
                        or event['revision'] != revision or row['revision'] != revision or snapshot.revision != revision
                        or event['event_id'] != row['event_id'] or event['previous_hash'] != previous
                        or digest(event) != row['hash'] or digest(snapshot.model_dump(mode='json')) != event['state_hash']):
                    raise ValueError('Invalid case chain')
                previous = row['hash']; events.append(event)
            if not events or snapshot != case or len(events) != case.revision + 1:
                raise ValueError('Missing case history')
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            raise ValueError('Case history failed verification') from exc
        history = export_rows(read_rows(db, case_id), case_id, events) or {'valid': True, 'records': []}
        if not history['valid']:
            raise ValueError('Assumption challenge history failed verification')
        return case, history

    @staticmethod
    def _predecessor(history, request):
        if request.predecessor_sha256 is None:
            return None
        for record in history['records']:
            if record['brief']['brief_sha256'] == request.predecessor_sha256:
                return record['brief']
        raise Conflict('Predecessor must be a saved brief from this case')

    def view(self, case_id):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case, history = self._context(db, case_id)
            db.rollback()
        now = utcnow()
        return {**history, 'case_id': case_id, 'case_revision': case.revision, 'sequence': len(history['records']),
                'records': [{**r, 'case_changed': r['brief']['snapshot_sha256'] != digest(case.model_dump(mode='json')),
                             'time_expired': now > datetime.fromisoformat(r['brief']['expires_at'])} for r in history['records']]}

    def prepare(self, case_id, request: Prepare):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case, history = self._context(db, case_id)
            brief = prepare(case, request, utcnow(), self._predecessor(history, request))
            db.rollback()
        return {'brief': brief, 'sequence': len(history['records']), 'artifact_persisted': False}

    def save(self, case_id, request: Save):
        request = Save.model_validate(request.model_dump(mode='python'))
        request_hash = digest(request.model_dump(mode='json'))
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case, history = self._context(db, case_id)
                prior = next((r for r in history['records'] if r['event_id'] == request.event_id), None)
                if prior:
                    if prior['request_hash'] != request_hash:
                        raise Conflict('This event ID belongs to a different challenge')
                    db.rollback()
                    return {'duplicate': True, 'record': prior, 'live_case_changed': False, 'artifact_persisted': True}
                if request.expected_sequence != len(history['records']):
                    raise Conflict('Challenge history changed; refresh before saving')
                now = utcnow()
                if request.as_of > now or now > request.as_of + timedelta(minutes=TTL_MINUTES):
                    raise Conflict('Challenge calculation expired; prepare it again')
                if len(history['records']) >= MAX_HISTORY:
                    raise ValueError('Local limit of 100 saved challenge briefs reached; history remains exportable')
                brief = prepare(case, request.draft, request.as_of, self._predecessor(history, request.draft))
                if brief['brief_sha256'] != request.brief_sha256:
                    raise Conflict('Challenge digest changed; prepare it again')
                record = {'case_id': case_id, 'event_id': request.event_id, 'sequence': len(history['records']) + 1,
                          'recorded_at': now.isoformat(), 'previous_hash': history.get('head_hash'),
                          'request_hash': request_hash, 'brief': brief, 'actor': 'local-operator',
                          'artifact_persisted': True, 'live_case_changed': False}
                record_hash = digest(record)
                db.execute('INSERT INTO v2_rehearsals VALUES(?,?,?,?,?)', (case_id, request.event_id, record['sequence'], canonical(record), record_hash))
                db.commit()
                return {'duplicate': False, 'record': {**record, 'hash': record_hash}, 'live_case_changed': False, 'artifact_persisted': True}
            except Exception:
                db.rollback()
                raise
