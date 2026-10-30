"""Manual, explicitly authorised hosted evaluation of the SAME frozen fixtures.

No private case database is opened. This script is never an automatic CI step.
Configuration and the --allow-hosted flag are required before any network call.
A valid JSON response is not an independent model-quality result.
"""
from datetime import timedelta
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from eightball.v2.hosted import settings, HostedSetupRequired
from eightball.v2.compatible import settings as compatible_settings
from eightball.v2.contracts import Case, Evidence, utcnow
from eightball.v2.intelligence import propose, PROMPT_VERSION as INTAKE_PROMPT_VERSION
from eightball.v2.commands import merge_object
from eightball.v2.planner import plan
from endstate.compilation import COMPILER_VERSION, PROMPT_VERSION as GRAPH_PROMPT_VERSION
from scripts.acceptance import source_manifest, output_directory

FIXTURES_SHA256='6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3'
RUNNER_VERSION='hosted-frozen-generation.v2'


class EvaluationInterrupted(BaseException):
    def __init__(self, signum):
        self.signum=signum


class SourceEvidenceInvalid(ValueError):
    """A fixed safe diagnostic: source inspection must not expose local paths."""


def inspect_source(report, point):
    """Bind every admitted fixture and the final receipt to one source tree.

    A later successful inspection cannot erase an earlier drift or inspection
    failure. Completed provider responses remain in the same failed receipt.
    """
    try:
        current=source_manifest()
    except Exception as exc:
        report['source_unchanged_during_run']=False
        report['source_checks'].append({'point':point,'status':'inspection_failed',
                                        'error_type':type(exc).__name__})
        if point=='finish':report['source_at_finish']=None
        raise SourceEvidenceInvalid('Source inspection failed; no further fixture may start.') from None
    same=report['source']==current
    report['source_checks'].append({'point':point,'status':'matched' if same else 'changed',
                                    'sha256':current['sha256']})
    report['source_unchanged_during_run']=same and report['source_unchanged_during_run'] is not False
    if point=='finish':report['source_at_finish']=current
    if not same:
        raise SourceEvidenceInvalid('Source changed during the run; no further fixture may start.')


def source_commit():
    """Identity only; the complete manifest also binds uncommitted source bytes."""
    try:
        result=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=ROOT,
                              capture_output=True,text=True,timeout=10,check=True)
        value=result.stdout.strip()
        return value if len(value) in (40,64) and all(c in '0123456789abcdef' for c in value) else None
    except (OSError,subprocess.SubprocessError):
        return None


def checkpoint(report, directory, report_name):
    """Retain every checkpoint; atomically refresh this run's current report."""
    report['checkpoint_number']=report.get('checkpoint_number',0)+1
    report['checkpoint_at']=utcnow().isoformat()
    raw=(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
    snapshots=directory/'checkpoints'
    snapshots.mkdir(exist_ok=True)
    # Exclusive creation preserves earlier partial/failed/successful receipts.
    with (snapshots/f"{report['checkpoint_number']:06d}.json").open('xb') as handle:
        handle.write(raw);handle.flush();os.fsync(handle.fileno())
    temporary=directory/('.'+report_name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        with temporary.open('xb') as handle:
            handle.write(raw);handle.flush();os.fsync(handle.fileno())
        os.replace(temporary,directory/report_name)
    finally:
        temporary.unlink(missing_ok=True)


def main(argv=None, *, default_provider='huggingface'):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-hosted',action='store_true',help='Authorise sending the fixed fictional fixtures to the selected hosted provider; usage may be billed.')
    parser.add_argument('--provider',choices=['huggingface','openai_compatible'],default=default_provider)
    parser.add_argument('--output',type=Path,help='Output root; each invocation creates a new run directory.')
    args=parser.parse_args(argv)
    if not args.allow_hosted:
        parser.error('--allow-hosted is required; no request has been made')
    if args.output is None:
        args.output=ROOT/('artifacts/huggingface' if args.provider=='huggingface' else 'artifacts/compatible')
    try:
        configured=settings() if args.provider=='huggingface' else compatible_settings()
    except HostedSetupRequired as exc:
        print(str(exc),file=sys.stderr)
        return 2
    fixtures=json.loads((ROOT/'evals/generation-cases.json').read_text())
    if sha256(json.dumps(fixtures).encode()).hexdigest()!=FIXTURES_SHA256:
        raise ValueError('Frozen fixture identity changed; do not silently replace the evaluation gate')
    started_at=utcnow()
    run_id=started_at.strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:12]
    directory=output_directory(args.output)/run_id
    directory.mkdir(parents=True,exist_ok=False)
    report={'schema_version':2,'runner_version':RUNNER_VERSION,'run_id':run_id,
            'started_at':started_at.isoformat(),'status':'running','complete':False,
            'source':source_manifest(),'source_commit':source_commit(),
            'source_at_finish':None,'source_unchanged_during_run':None,'source_checks':[],
            'versions':{'intake_prompt':INTAKE_PROMPT_VERSION,'graph_prompt':GRAPH_PROMPT_VERSION,
                        'compiler':COMPILER_VERSION,'python':sys.version.split()[0]},
            'provider':args.provider,'requested_model':configured.model,
            'routing_provider':getattr(configured,'routing_provider',None) or configured.provider,
            'fixture_sha256':FIXTURES_SHA256,
            'fixture_file_sha256':sha256((ROOT/'evals/generation-cases.json').read_bytes()).hexdigest(),
            'planned_fixtures':len(fixtures),'started_fixtures':0,'completed_fixtures':0,
            'results':[],'active_fixture':None,'structural_gate_passed':None,
            'actual_hosted_requests':False,'production_approved':False,
            'independent_semantic_benchmark':False,'automatic_retry':False,
            'limitations':['Four familiar engineering fixtures, not independent quality validation.',
                          'No template fallback, automatic retries or provider switching.',
                          'Model and reviewer quality must be assessed separately from structural validation.',
                          'Checkpoints bracket fixtures, not individual internal staged provider calls.',
                          'A hard kill retains the last checkpoint; an in-flight response may not be recoverable.']}
    if args.provider=='openai_compatible':
        report['endpoint_host']=configured.endpoint_host
    report_name='huggingface-report.json' if args.provider=='huggingface' else 'compatible-report.json'
    checkpoint(report,directory,report_name)
    print('Report: '+str(directory/report_name),flush=True)
    previous_signal=None;signal_installed=False
    try:
        # SIGTERM and Ctrl-C checkpoint without replaying any paid request.
        # A non-main-thread embedding cannot install process signal handlers.
        try:
            previous_signal=signal.getsignal(signal.SIGTERM)
            def terminate(signum,frame):raise EvaluationInterrupted(signum)
            signal.signal(signal.SIGTERM,terminate);signal_installed=True
        except ValueError:
            pass
        for index,(title,text,purpose,desired) in enumerate(fixtures):
            inspect_source(report,'before_fixture_'+str(index))
            c=Case(title=title,client='Fictional evaluation only',summary=text,desired_outcome=desired,
                   deadline=utcnow()+timedelta(days=3),budget=10000,
                   evidence=[Evidence(id='source',title='Fictional fixture',source='Frozen evaluation set',text=text)])
            before=c.model_dump(mode='json');started=time.perf_counter()
            result={'fixture_index':index,'title':title,'purpose':purpose,'source':text,'desired_outcome':desired,
                    'source_sha256':sha256(text.encode()).hexdigest(),
                    'outcome_sha256':sha256(desired.encode()).hexdigest(),
                    'fixture_input_sha256':sha256(json.dumps(fixtures[index],ensure_ascii=False).encode()).hexdigest(),
                    'started_at':utcnow().isoformat()}
            report['active_fixture']={**result,'status':'request_not_yet_returned',
                'transport_evidence_status':'In-flight request/staged responses may not be recoverable until propose returns.'}
            report['started_fixtures']+=1
            checkpoint(report,directory,report_name)
            try:
                p=propose(c,args.provider,purpose,['source'],allow_external=True)
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
            result.update(seconds=round(time.perf_counter()-started,3),finished_at=utcnow().isoformat(),
                          live_state_unchanged=before==c.model_dump(mode='json'))
            report['results'].append(result);report['active_fixture']=None
            report['completed_fixtures']=len(report['results'])
            report['all_live_states_unchanged']=all(r['live_state_unchanged'] for r in report['results'])
            checkpoint(report,directory,report_name)
            print(f"{title}: {result['status']} ({result['seconds']} seconds)",flush=True)
        graph=next(r for r in report['results'] if r['purpose']=='graph')
        passed=(all(r['status']=='valid_proposal' and r['live_state_unchanged'] for r in report['results'])
                and graph.get('candidate_routes',0)>=2 and not graph.get('outcome_evidenced',True)
                and graph.get('all_actions_need_approval') and graph.get('exact_human_outcome_preserved'))
        report.update(structural_gate_passed=bool(passed),complete=True)
        inspect_source(report,'before_result')
        report['status']='passed' if passed else 'failed'
    except SourceEvidenceInvalid as exc:
        report.update(status='failed',complete=len(report['results'])==len(fixtures),
                      reason=str(exc))
        if report['structural_gate_passed'] is None:report['structural_gate_passed']=False
    except BaseException as exc:
        interrupted=isinstance(exc,(KeyboardInterrupt,SystemExit,EvaluationInterrupted))
        report.update(status='interrupted' if interrupted else 'aborted',complete=False,
                      structural_gate_passed=False,
                      interruption={'error_type':type(exc).__name__,
                                    'signal':getattr(exc,'signum',None),
                                    'request_may_have_completed_without_returned_trace':report['active_fixture'] is not None})
        if report['active_fixture'] is not None:report['active_fixture']['status']=report['status']
        if isinstance(exc,EvaluationInterrupted):raise SystemExit(128+exc.signum) from None
        raise
    finally:
        if signal_installed:signal.signal(signal.SIGTERM,previous_signal)
        try:
            inspect_source(report,'finish')
        except SourceEvidenceInvalid as exc:
            # Keep an interrupted/aborted status; source_checks records the failure.
            if report['status'] not in ('interrupted','aborted'):report['status']='failed'
            report.setdefault('reason',str(exc))
        report['finished_at']=utcnow().isoformat()
        checkpoint(report,directory,report_name)
    return 0 if report['status']=='passed' else 1


if __name__=='__main__':
    raise SystemExit(main())
