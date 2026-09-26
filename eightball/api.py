"""Single-operator, loopback-only alpha API. Do not deploy as an agency SaaS."""
import hmac
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pydantic import Field, AwareDatetime, ValidationError, StrictBool
from . import __version__
from .models import Strict, Title, Text, Identifier, Evidence, Observation, Situation, utcnow
from .commands import Command
from .store import Store, Conflict
from .engine import plan, difference
from .seed import create_case
from .providers import jev_classify, gliclass_classify, ollama_extract, ProviderUnavailable
from .v2.request_limits import BoundedRequestBody, body_limit


class Intake(Strict):
    title: Title
    client: Title
    summary: Text
    desired_outcome: Title
    template: Literal['retention', 'recovery'] = 'retention'
    budget: int = Field(default=7000, strict=True, ge=0, le=100000000)
    deadline: AwareDatetime


class Simulation(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    budget: int | None = Field(default=None, strict=True, ge=0, le=100000000)
    deadline: AwareDatetime | None = None
    conditions: dict[Identifier, StrictBool] = Field(default_factory=dict)


class Advice(Strict):
    evidence_id: Identifier
    provider: Literal['jev', 'gliclass', 'ollama']
    allow_external: bool = Field(default=False, strict=True)


def make_app(store: Store, token: str) -> FastAPI:
    if len(token) < 32:
        raise ValueError('Use an operator token of at least 32 characters')
    app = FastAPI(title='8BALL local alpha', version=__version__, docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1', 'localhost', 'testserver'])

    @app.middleware('http')
    async def boundary(request: Request, call_next):
        origin = request.headers.get('origin')
        if origin and origin.rstrip('/') != str(request.base_url).rstrip('/'):
            return JSONResponse({'detail': 'Cross-origin requests are not allowed'}, status_code=403)
        if request.method in ('POST', 'PUT', 'PATCH'):
            try:
                length = int(request.headers.get('content-length', '-1'))
            except ValueError:
                length = -1
            limit=body_limit(request.url.path)
            if length < 0 or length > limit:
                return JSONResponse({'detail': f'Request needs Content-Length of at most {limit} bytes'}, status_code=413)
            if request.headers.get('content-type', '').split(';')[0] != 'application/json':
                return JSONResponse({'detail': 'JSON requests only'}, status_code=415)
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        return response

    def authorised(request: Request):
        supplied = request.headers.get('authorization', '')
        if not hmac.compare_digest(supplied, 'Bearer ' + token):
            raise HTTPException(401, 'An operator token is required')

    def load(case_id):
        try:
            return store.get(case_id)
        except KeyError:
            raise HTTPException(404, 'Situation not found') from None

    @app.get('/api/health')
    def health():
        return {'version': __version__, 'mode': 'local-single-operator', 'live_ai_default': False}

    @app.get('/api/cases', dependencies=[Depends(authorised)])
    def cases():
        return [{'id': c.id, 'title': c.title, 'client': c.client, 'desired_outcome': c.desired_outcome,
                 'deadline': c.deadline, 'revision': c.revision} for c in store.list()]

    @app.post('/api/cases', dependencies=[Depends(authorised)], status_code=201)
    def intake(body: Intake):
        if len(store.list()) >= 200:
            raise HTTPException(422, 'Local alpha case limit reached')
        return store.create(create_case(**body.model_dump())).model_dump(mode='json')

    @app.post('/api/demo', dependencies=[Depends(authorised)], status_code=201)
    def demo():
        if len(store.list()) >= 200:
            raise HTTPException(422, 'Local alpha case limit reached')
        return store.create(create_case()).model_dump(mode='json')

    @app.get('/api/cases/{case_id}', dependencies=[Depends(authorised)])
    def detail(case_id: str):
        case = load(case_id)
        return {'case': case.model_dump(mode='json'), 'plan': plan(case)}

    @app.post('/api/cases/{case_id}/events', dependencies=[Depends(authorised)])
    def command(case_id: str, body: Command):
        try:
            case, changes = store.change(case_id, body)
            return {'case': case.model_dump(mode='json'), 'plan': plan(case), 'changes': changes}
        except KeyError:
            raise HTTPException(404, 'Situation not found') from None
        except Conflict as exc:
            raise HTTPException(409, str(exc)) from None
        except (ValidationError, ValueError) as exc:
            # Pydantic errors can include input values; never return those verbatim.
            detail = 'Invalid command payload or graph references' if isinstance(exc, ValidationError) else str(exc)
            raise HTTPException(422, detail) from None

    @app.post('/api/cases/{case_id}/simulate', dependencies=[Depends(authorised)])
    def simulate(case_id: str, body: Simulation):
        case = load(case_id)
        if body.expected_revision != case.revision:
            raise HTTPException(409, 'Reload before simulating this situation')
        if len(case.evidence) + len(body.conditions) > 200 or len(case.observations) + len(body.conditions) > 1000:
            raise HTTPException(422, 'Scenario exceeds the local evidence or observation limit')
        clone = case.model_copy(deep=True)
        known = {c.id for c in case.graph.conditions}
        if not set(body.conditions) <= known:
            raise HTTPException(422, 'Unknown hypothetical condition')
        if body.budget is not None:
            clone.budget = body.budget
        if body.deadline is not None:
            clone.deadline = body.deadline
        clone.approvals = {}
        for cid, value in body.conditions.items():
            e = Evidence(title='Scenario assumption', source='Sandbox only', text='Hypothetical state, not case evidence.', status='reviewed')
            clone.evidence.append(e)
            clone.observations.append(Observation(condition_id=cid, evidence_id=e.id, value=value,
                rationale='Hypothetical state for scenario comparison', supersedes=[o.id for o in clone.observations if o.condition_id == cid]))
        clone = Situation.model_validate(clone.model_dump())
        now = utcnow()
        before, after = plan(case, now), plan(clone, now)
        return {'simulation': True, 'persisted': False, 'base_revision': case.revision,
                'plan': after, 'changes': difference(before, after)}

    @app.get('/api/cases/{case_id}/export', dependencies=[Depends(authorised)])
    def export(case_id: str):
        load(case_id)
        audit = store.audit(case_id)
        return {'format': 'eightball-case-v1', 'version': __version__, **audit}

    @app.post('/api/cases/{case_id}/advice', dependencies=[Depends(authorised)])
    def advice(case_id: str, body: Advice):
        case = load(case_id)
        evidence = next((e for e in case.evidence if e.id == body.evidence_id), None)
        if not evidence or evidence.status == 'retracted':
            raise HTTPException(422, 'Select a non-retracted evidence source')
        # Small input bounds are deliberate. No silent truncation or whole-case export.
        if len(evidence.text) > 6000:
            raise HTTPException(422, 'Choose a source excerpt of at most 6000 characters')
        try:
            if body.provider == 'jev':
                result = jev_classify(evidence.text, allow_external=body.allow_external)
            elif body.provider == 'gliclass':
                result = gliclass_classify(evidence.text)
            else:
                result = ollama_extract(evidence.text, [c.model_dump(mode='json') for c in case.graph.conditions])
            return {**result, 'case_revision': case.revision, 'evidence_id': evidence.id,
                    'persisted': False, 'case_state_changed': False}
        except ProviderUnavailable as exc:
            raise HTTPException(503, str(exc)) from None

    from .v2.api import router as v2_router
    from .v2.store import Store as V2Store
    from fastapi.exceptions import RequestValidationError

    @app.exception_handler(RequestValidationError)
    async def request_validation_error(request, exc):
        return JSONResponse({'detail': 'Invalid request fields', 'fields': [list(e['loc']) for e in exc.errors()]},status_code=422)

    @app.exception_handler(Conflict)
    async def conflict_error(request, exc):
        return JSONResponse({'detail': str(exc)},status_code=409)

    @app.exception_handler(KeyError)
    async def missing_error(request, exc):
        return JSONResponse({'detail': 'Case or object not found'},status_code=404)

    @app.exception_handler(ValueError)
    async def value_error(request, exc):
        return JSONResponse({'detail': 'Invalid fields or references' if isinstance(exc,ValidationError) else str(exc)},status_code=422)

    v2_routes = v2_router(V2Store(store.path),store,authorised)
    app.state.analysis_jobs = v2_routes.analysis_jobs
    app.include_router(v2_routes)
    web = Path(__file__).resolve().parent.parent / 'web'
    app.mount('/v2', StaticFiles(directory=web / 'v2', html=True), name='v2-web')
    app.mount('/', StaticFiles(directory=web, html=True), name='web')
    app.add_middleware(BoundedRequestBody)
    return app
