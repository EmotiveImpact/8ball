"""Offline structural-regression bench and an UNFILLED human review sheet.

This does not call a model, choose a provider, or claim independent expert labels.
The original live-model acceptance fixture file remains unchanged.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from endstate.contracts import PlanningSnapshot, Condition, Action, Effect, Graph, Objective, atom, all_of
from endstate.primitives import Evidence, Observation
from endstate.plan_review import inspect_plan, Inspection, Stress, RUBRIC, RUBRIC_VERSION

CLOCK = datetime(2026, 9, 24, 9, tzinfo=timezone.utc)


def example():
    return PlanningSnapshot(id='engineering_fixture', deadline=CLOCK + timedelta(days=1), budget=3000,
        graph=Graph(conditions=[Condition(id=i, title=t, confirmation=p) for i, t, p in [
            ('scope', 'Issue understood', 'Review the recorded customer report'),
            ('remedy', 'A remedy is available', 'Authorised owner confirms the available remedy'),
            ('resolved', 'Customer accepts resolution', 'Written customer confirmation of the delivered remedy')]],
            actions=[Action(id='scope',title='Review issue',owner='Lead',purpose='Establish issue scope',effects=[Effect(condition_id='scope')],minutes=20),
                     Action(id='repair',title='Repair the service',owner='Engineer',purpose='Restore service',requires=atom('scope'),effects=[Effect(condition_id='remedy')],minutes=60,cost=500),
                     Action(id='replace',title='Offer approved alternative',owner='Lead',purpose='Provide an authorised alternative',requires=atom('scope'),effects=[Effect(condition_id='remedy')],minutes=30,cost=800),
                     Action(id='verify',title='Verify resolution with customer',owner='Lead',purpose='Obtain customer confirmation',requires=atom('remedy'),effects=[Effect(condition_id='resolved')],minutes=20,contingent=True,wait_minutes=None)],
            objectives=[Objective(id='resolve',title='Resolve issue with customer confirmation',success=atom('resolved'))]))


def build_case(case_id):
    s=example()
    s.id=case_id
    if case_id=='missing-outcome':s.graph.objectives=[]
    elif case_id=='zero-budget':s.budget=0
    elif case_id=='completed-not-confirmed':s.completed.append('verify')
    elif case_id=='contradictory-evidence':
        for eid,value in [('first',True),('second',False)]:
            s.evidence.append(Evidence(id=eid,title='Fictional source '+eid,source='Author-created test',text='Conflicting fixture assertion.',status='reviewed',added_at=CLOCK))
            s.observations.append(Observation(id=eid,condition_id='scope',evidence_id=eid,value=value,rationale='Engineering fixture only',added_at=CLOCK))
    elif case_id=='destructive-effect':
        s.budget=900  # Cannot afford both a destructive route and a later second remedy.
        s.graph.actions[-1].effects.append(Effect(condition_id='remedy',value=False))
        s.graph.objectives[0].success=all_of('resolved','remedy')
    elif case_id=='expired-deadline':s.deadline=CLOCK-timedelta(minutes=1)
    elif case_id=='wrong-but-valid-outcome':
        # A deliberate semantic defect. The inspector MUST NOT certify this as correct.
        s.graph.conditions[-1].title='An offer was sent'
        s.graph.conditions[-1].confirmation='Outbound message is recorded'
        s.graph.actions[-1].title='Record the outbound offer'
        s.graph.actions[-1].purpose='Record sending, not acceptance'
        s.graph.actions[-1].contingent=False
        s.graph.actions[-1].wait_minutes=0
    return PlanningSnapshot.model_validate(s.model_dump(mode='python'))


def run_bench(output):
    manifest_path=ROOT/'evals/plan-review-cases.json'
    raw=manifest_path.read_bytes();manifest=json.loads(raw)
    rows=[];review_sheet=[]
    for fixture in manifest['cases']:
        case=build_case(fixture['id']);before=case.model_dump(mode='json')
        report=inspect_plan(case,Inspection(as_of=CLOCK,scenarios=[Stress(**x) for x in fixture.get('scenarios',[])]))
        rules={f['rule'] for f in report['flags']}
        passed=(set(fixture['expected_rules'])<=rules and not (set(fixture.get('forbidden_rules',[]))&rules)
                and not report['semantics_verified'] and not report['execution_authorised']
                and before==case.model_dump(mode='json'))
        rows.append({'id':fixture['id'],'structural_checks_passed':passed,'report':report})
        review_sheet.append({'fixture_id':fixture['id'],'requested_outcome':fixture['requested_outcome'],
                             'source_text':fixture['source_text'],'review_focus':fixture['review_focus'],
                             'candidate_snapshot':before,
                             'rubric':[{'criterion':r['id'],'verdict':None,'rationale':None,'reviewer':None} for r in RUBRIC]})
    result={'fixture_sha256':hashlib.sha256(raw).hexdigest(),'fixture_scope':manifest['scope'],
            'rubric_version':RUBRIC_VERSION,'actual_model_inference':False,'independent_review_completed':False,
            'structural_checks_passed':sum(r['structural_checks_passed'] for r in rows),'total':len(rows),
            'quality_gate':'NOT_ASSESSED','production_model_selected':False,'results':rows}
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    (output/'structural-review-report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (output/'human-review-sheet.json').write_text(json.dumps({'fixture_sha256':result['fixture_sha256'],'status':'UNREVIEWED',
       'notice':'Author-created engineering examples, not independent expert judgements. Do not fill in labels with a model and describe them as human validation.',
       'reviews':review_sheet},indent=2),encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts/quality')
    args=parser.parse_args()
    report=run_bench(args.output)
    print(f"Structural regression: {report['structural_checks_passed']}/{report['total']}; model quality NOT ASSESSED. Human review sheet is unfilled.")
    if report['structural_checks_passed']!=report['total']:sys.exit(1)
