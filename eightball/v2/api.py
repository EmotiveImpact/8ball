"""Local V0.2 API. Same auth boundary as V0.1; never a multi-tenant service."""
from datetime import timedelta
from threading import BoundedSemaphore
from pydantic import ValidationError, Field, AwareDatetime
from fastapi import APIRouter, Depends, HTTPException, Query
from . import VERSION
from .contracts import *
from .commands import Command
from .store import Store
from .playbooks import demo_case, make_case, list_playbooks, get_playbook
from .planner import plan, briefing, question_priorities
from .services import detail, Scenario, simulate, migrate_legacy, client_brief, action_brief, situation_map
from .intelligence import propose, retrieve, provider_status, validate_request
from ..store import Conflict, digest
from ..models import utcnow
from ..providers import ProviderUnavailable


class Intake(Strict):
    title: Title
    client: Title
    summary: Text
    desired_outcome: Title
    deadline: AwareDatetime
    budget: Count = 10000
    playbook: Identifier | None = None


class Analyse(Strict):
    expected_revision: int = Field(strict=True,ge=0)
    provider: Literal['rules','playbook','ollama','jev','gliclass']
    purpose: Literal['extract','graph','questions','judgement']
    source_ids: list[Identifier] = Field(default_factory=list,max_length=40)
    playbook_id: Identifier | None = None
    allow_external: bool = Field(default=False,strict=True)


class Choice(Strict):
    id: Identifier
    disposition: Literal['accepted','edited','rejected']
    object: dict | None = None


class Review(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True,ge=0)
    choices: list[Choice] = Field(default_factory=list,max_length=100)


class Compare(Strict):
    revision: int = Field(strict=True,ge=0)
    route_ids: list[Identifier] = Field(min_length=2,max_length=4)


class Search(Strict):
    query: str = Field(min_length=1,max_length=300)
    types: list[Literal['evidence','claim','event','actor','condition','decision','question']] | None = None
    limit: int = Field(default=10,strict=True,ge=1,le=30)


SORT=Literal['fewest_unknowns','fastest','lowest_cost','fewest_external','least_irreversible','operator_risk']


def router(store:Store,legacy,authorised):
    r=APIRouter(prefix='/api/v2',dependencies=[Depends(authorised)])
    model_slot=BoundedSemaphore(1)

    @r.get('/status')
    def status():return {'version':VERSION,'mode':'local-single-operator','live_external_actions':False,**provider_status()}

    @r.get('/cases')
    def cases():
        return [{'id':c.id,'title':c.title,'client':c.client,'summary':c.summary,'desired_outcome':c.desired_outcome,
                 'status':c.status,'priority':c.priority,'deadline':c.deadline,'revision':c.revision,'updated_at':c.updated_at,
                 'sources':len(c.evidence),'decisions_pending':sum(d.selected is None for d in c.decisions)} for c in store.list()]

    @r.post('/cases',status_code=201)
    def create(body:Intake):return store.create(make_case(**body.model_dump())).model_dump(mode='json')

    @r.post('/demo',status_code=201)
    def demo():return store.create(demo_case(),fixture=True).model_dump(mode='json')

    @r.get('/cases/{case_id}')
    def case_detail(case_id:str,sort_by:SORT='fewest_unknowns'):return detail(store.get(case_id),sort_by)

    @r.post('/cases/{case_id}/commands')
    def command(case_id:str,body:Command):
        case,delta=store.change(case_id,body)
        return {**detail(case),'changes':delta}

    @r.post('/cases/{case_id}/plan')
    def plan_case(case_id:str,sort_by:SORT='fewest_unknowns'):
        case=store.get(case_id);p=plan(case,sort_by=sort_by)
        return {'plan':p,'briefing':briefing(case,p),'persisted':False}

    @r.get('/cases/{case_id}/map')
    def graph(case_id:str,view:Literal['outcome','people','evidence']='outcome'):
        case=store.get(case_id);return situation_map(case,plan(case),view)

    @r.get('/cases/{case_id}/questions')
    def questions(case_id:str):
        case=store.get(case_id);return question_priorities(case,plan(case))

    @r.get('/cases/{case_id}/actions/{action_id}')
    def action(case_id:str,action_id:str):return action_brief(store.get(case_id),action_id)

    @r.get('/cases/{case_id}/changes')
    def deltas(case_id:str):
        return [e for e in store.history(case_id)['events'] if e.get('changes')]

    @r.get('/cases/{case_id}/history')
    def history(case_id:str):return store.history(case_id)

    @r.get('/cases/{case_id}/export')
    def export(case_id:str):return store.audit(case_id)

    @r.get('/cases/{case_id}/client-brief')
    def brief(case_id:str):return client_brief(store.get(case_id))

    @r.post('/cases/{case_id}/compare')
    def compare(case_id:str,body:Compare):
        case=store.get(case_id)
        if case.revision!=body.revision:raise Conflict('Reload before comparing routes')
        plans=plan(case)['routes'];by_id={p['id']:p for p in plans}
        if len(set(body.route_ids))!=len(body.route_ids) or not set(body.route_ids)<=by_id.keys():raise ValueError('Select two to four different current routes')
        selected=[by_id[i] for i in body.route_ids]
        shared=set(selected[0]['actions']).intersection(*(set(p['actions']) for p in selected[1:]))
        return {'revision':case.revision,'routes':selected,'shared_actions':sorted(shared),
                'unique_actions':{p['id']:sorted(set(p['actions'])-shared) for p in selected},'note':'No success probabilities or automatic selection'}

    @r.post('/cases/{case_id}/simulate')
    def scenario(case_id:str,body:Scenario):return simulate(store.get(case_id),body)

    @r.post('/cases/{case_id}/search')
    def search(case_id:str,body:Search):return retrieve(store.get(case_id),body.query,body.types,body.limit)

    @r.get('/cases/{case_id}/proposals')
    def proposals(case_id:str):return store.proposals(case_id)

    @r.post('/cases/{case_id}/analyse')
    def analyse(case_id:str,body:Analyse):
        case=store.get(case_id)
        if body.expected_revision!=case.revision:raise Conflict('Reload before analysing this case')
        validate_request(case,body.provider,body.purpose,body.source_ids,playbook_id=body.playbook_id,allow_external=body.allow_external)
        if len(store.proposals(case_id))>=200:raise ValueError('Local proposal limit reached')
        if not model_slot.acquire(blocking=False):raise HTTPException(429,'Another analysis is already running. Try again after it finishes.')
        try:
            proposal=propose(case,body.provider,body.purpose,body.source_ids,playbook_id=body.playbook_id,allow_external=body.allow_external)
            store.save_proposal(proposal)
            return {'proposal':proposal.model_dump(mode='json'),'live_state_changed':False}
        except (ProviderUnavailable,ValidationError,ValueError) as exc:
            if not isinstance(exc,ProviderUnavailable) and body.provider in ('rules','playbook'):raise
            failed=Proposal(case_id=case_id,base_revision=case.revision,provider=body.provider,model='unavailable',purpose=body.purpose,
                            source_ids=body.source_ids,output_hash=digest({'failed':True}),latency_ms=0,status='failed',
                            note='Provider unavailable or response failed validation. No model output was accepted. Retry or continue manually.')
            store.save_proposal(failed)
            raise HTTPException(503,failed.note) from None
        finally:model_slot.release()

    @r.post('/cases/{case_id}/proposals/{proposal_id}/review')
    def review(case_id:str,proposal_id:str,body:Review):
        case,delta=store.review(case_id,proposal_id,body.event_id,body.expected_revision,[c.model_dump(exclude_none=True) for c in body.choices])
        return {**detail(case),'changes':delta}

    @r.get('/playbooks')
    def playbooks():return list_playbooks()

    @r.get('/playbooks/{playbook_id}')
    def playbook(playbook_id:str):
        package=get_playbook(playbook_id)
        return {k:(v.model_dump(mode='json') if hasattr(v,'model_dump') else [x.model_dump(mode='json') for x in v]) for k,v in package.items()}

    @r.get('/legacy')
    def legacy_cases():return [{'id':c.id,'title':c.title,'revision':c.revision} for c in legacy.list()]

    @r.post('/legacy/{legacy_id}/import')
    def import_case(legacy_id:str):return migrate_legacy(store,legacy,legacy_id).model_dump(mode='json')

    return r
