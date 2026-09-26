"""Manual, explicitly authorised HF evaluation of the SAME four frozen fixtures.

No private case database is opened. This script is never an automatic CI step.
Configuration and the --allow-hosted flag are required before any network call.
A valid JSON response is not an independent model-quality result.
"""
from datetime import timedelta
from hashlib import sha256
from pathlib import Path
import argparse
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from eightball.v2.hosted import settings, HostedSetupRequired
from eightball.v2.contracts import Case, Evidence, utcnow
from eightball.v2.intelligence import propose
from eightball.v2.commands import merge_object
from eightball.v2.planner import plan

FIXTURES_SHA256='6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3'


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-hosted',action='store_true',help='Authorise sending the fixed fictional fixtures to the configured HF provider; usage may be billed.')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts/huggingface')
    args=parser.parse_args(argv)
    if not args.allow_hosted:
        parser.error('--allow-hosted is required; no request has been made')
    try:
        configured=settings()
    except HostedSetupRequired as exc:
        print(str(exc),file=sys.stderr)
        return 2
    fixtures=json.loads((ROOT/'evals/generation-cases.json').read_text())
    if sha256(json.dumps(fixtures).encode()).hexdigest()!=FIXTURES_SHA256:
        raise ValueError('Frozen fixture identity changed; do not silently replace the evaluation gate')
    args.output.mkdir(parents=True,exist_ok=True)
    report={'provider':'huggingface','requested_model':configured.model,'routing_provider':configured.provider,
            'fixture_sha256':FIXTURES_SHA256,'planned_fixtures':len(fixtures),'results':[],
            'actual_hosted_requests':False,'production_approved':False,
            'independent_semantic_benchmark':False,
            'limitations':['Four familiar engineering fixtures, not independent quality validation.',
                          'No template fallback, automatic retries or provider switching.',
                          'Model and reviewer quality must be assessed separately from structural validation.']}
    for title,text,purpose,desired in fixtures:
        c=Case(title=title,client='Fictional evaluation only',summary=text,desired_outcome=desired,
               deadline=utcnow()+timedelta(days=3),budget=10000,
               evidence=[Evidence(id='source',title='Fictional fixture',source='Frozen evaluation set',text=text)])
        before=c.model_dump(mode='json');started=time.perf_counter()
        result={'title':title,'purpose':purpose,'source':text,'desired_outcome':desired}
        try:
            p=propose(c,'huggingface',purpose,['source'],allow_external=True)
            result.update(status='valid_proposal',proposal=p.model_dump(mode='json'),proposal_count=len(p.items))
            report['actual_hosted_requests'] |= bool(p.raw_output['transport']['calls'])
            if purpose=='graph':
                data=c.model_dump(mode='json')
                for item in p.items:merge_object(data,item.kind,item.object)
                projected=Case.model_validate(data);routes=plan(projected)
                result.update(candidate_routes=len(routes['routes']),outcome_evidenced=routes['outcome_evidenced'],
                              all_actions_need_approval=all(a.approval_required for a in projected.graph.actions),
                              exact_human_outcome_preserved=all(o.title==desired for o in projected.graph.objectives))
        except Exception as exc:
            trace=getattr(exc,'trace',{})
            result.update(status='rejected_or_unavailable',error_type=type(exc).__name__,trace=trace)
            report['actual_hosted_requests'] |= bool(trace.get('transport',{}).get('calls'))
        result.update(seconds=round(time.perf_counter()-started,3),live_state_unchanged=before==c.model_dump(mode='json'))
        report['results'].append(result)
        report['completed_fixtures']=len(report['results'])
        report['all_live_states_unchanged']=all(r['live_state_unchanged'] for r in report['results'])
        (args.output/'huggingface-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        print(f"{title}: {result['status']} ({result['seconds']} seconds)",flush=True)
    graph=next(r for r in report['results'] if r['purpose']=='graph')
    passed=(all(r['status']=='valid_proposal' and r['live_state_unchanged'] for r in report['results'])
            and graph.get('candidate_routes',0)>=2 and not graph.get('outcome_evidenced',True)
            and graph.get('all_actions_need_approval') and graph.get('exact_human_outcome_preserved'))
    report['structural_gate_passed']=bool(passed)
    (args.output/'huggingface-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return 0 if passed else 1


if __name__=='__main__':
    raise SystemExit(main())
