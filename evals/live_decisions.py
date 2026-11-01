"""One explicit native decision smoke call on a fixed fictional code-review case.

This is connectivity/contract evidence, not semantic or product acceptance.
No auto-retry, loop, repair, fallback or case access. Review each receipt before
invoking another model. Account pricing/free entitlement is operator-confirmed.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from uuid import uuid4

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from endstate.intelligence.decisions import DecisionInput
from eightball.v2.decision_models import DecisionSession, ORIGIN


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',required=True,choices=['jev-latest','clef-flash','gpt-6-luna-decisions'])
    p.add_argument('--allow-external',action='store_true')
    p.add_argument('--confirm-free-entitlement',action='store_true')
    p.add_argument('--allow-metered-smoke',action='store_true',help='Owner permits this single bounded call; caller tracks the shared spending budget')
    args = p.parse_args()
    if not args.allow_external or not (args.confirm_free_entitlement or args.allow_metered_smoke):
        p.error('Explicit external permission and free-entitlement confirmation or metered-call permission are required')
    request = DecisionInput(model=args.model,state='Fictional code review. Task: reject an empty project name before writing a record. The new empty-name unit test and existing creation tests pass. No integration tests were run. A human decides whether to merge; this answer cannot merge or authorise anything.',
        questions=[{'id':'review','instructions':'Does the supplied evidence support accepting this change, or does it need further review? Treat missing evidence as a reason to review.',
                    'criteria':{'accept':'The described change meets the task and supplied tests cover its relevant behavior.',
                                'review':'Evidence is missing, the tests are insufficient, or the change may be incorrect.'}}])
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid4().hex[:8]
    out = ROOT/'artifacts'/'decisions'/stamp
    out.mkdir(parents=True)
    report = {'fixture':'fictional-empty-name-review-v1','model':args.model,'independent_quality_acceptance':False,
              'owner_confirmed_free_entitlement':args.confirm_free_entitlement,'metered_smoke_authorized':args.allow_metered_smoke,'provider_hard_cap_verified':False,
              'permission':'One explicitly selected model; no retries, fallback or execution','inference_calls':0}
    session = None
    try:
        with httpx.Client(timeout=20,follow_redirects=False,headers={'Authorization':'Bearer '+os.environ['EXPERIENTIAL_API_KEY']}) as client:
            key = client.get(ORIGIN+'/api/v1/key');key.raise_for_status()
            summary = key.json()['data']
            report['key_before'] = {k:summary.get(k) for k in ('usage','usage_daily','limit','is_free_tier')}
            routing = client.get(ORIGIN+'/api/models/'+args.model+'/waterfall');routing.raise_for_status()
            chain = routing.json()
            rungs = chain.get('override') if chain.get('override') is not None else chain.get('served_default')
            if not isinstance(rungs,list) or len(rungs) != 1 or rungs[0].get('target_kind') != 'deployment' or rungs[0].get('funding') != 'platform':
                raise ValueError('Single platform-funded route is not verified; no inference sent')
            report['routing_preflight'] = {'rungs':1,'provider':rungs[0]['provider'],'model':rungs[0]['provider_model_id'],
                'default_revision':chain['default_revision'],'override_revision':chain['override_revision'],
                'notice':'Observed immediately before dispatch, not an atomic provider-side pin.'}
        session = DecisionSession(allow_external=True)
        report['result'] = session.ask(request)
        report['status'] = 'validated_advisory_response'
    except Exception as exc:
        report['status'] = 'failed'
        report['error_type'] = type(exc).__name__
    finally:
        if session:
            report['transport'] = session.receipt
            report['inference_calls'] = session.receipt['inference_calls']
            if session.response is not None:
                (out/'fictional-response.json').write_text(json.dumps(session.response,indent=2,allow_nan=False))
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        (out/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False))
        print(json.dumps({'report':str(out/'report.json'),**report},indent=2,allow_nan=False))
    return 0 if report['status'] == 'validated_advisory_response' else 1


if __name__ == '__main__':
    raise SystemExit(main())
