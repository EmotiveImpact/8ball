"""Opt-in native Experiential decision transport, independent of chat generation.

No store access, retries, redirects, automatic fan-out or execution. Caller
permission and provider pricing/routing checks precede every real request.
"""
import json
import math
import os
import re

import httpx

from endstate.intelligence.decisions import DecisionInput, validate_choice
from .compatible import _contains_credential
from .hosted import HostedFailure, HostedSetupRequired, _hash, json_object

ORIGIN = 'https://api.experientiallabs.ai'
MAX_REQUEST_BYTES = 20000
MAX_RESPONSE_BYTES = 128000


def payload_for(request: DecisionInput):
    request = DecisionInput.model_validate(request.model_dump(mode='python'))
    if request.model == 'gpt-6-luna-decisions':
        return '/v1/decisions', {'model': request.model, 'input': request.state,
            'questions': [{'type': 'choice', 'name': q.id, 'instructions': q.instructions,
                           'choices': [{'value': k, 'description': v} for k, v in q.criteria.items()]} for q in request.questions]}
    return '/v1/systemone', {'model': request.model, 'state': request.state,
        'questions': {q.id: {'type': 'choice', 'instructions': q.instructions, 'criteria': q.criteria} for q in request.questions}}


def validate_response(request: DecisionInput, response):
    if response.get('refusal') is not None or response.get('status') in ('refused','failed','incomplete'):
        raise ValueError('Decision refused or incomplete')
    model = response.get('model')
    valid_model = model == request.model
    if request.model == 'jev-latest':
        valid_model = valid_model or isinstance(model,str) and re.fullmatch(r'jev-[0-9]+\.[0-9]+\.[0-9]+',model) is not None
    if request.model == 'gpt-6-luna-decisions':
        valid_model = valid_model or model == 'gpt-6-luna'
    if not valid_model:
        raise ValueError('Unexpected served model')
    answers = response.get('answers')
    if request.model == 'gpt-6-luna-decisions':
        if not isinstance(answers, list) or len(answers) != len(request.questions):
            raise ValueError('Unexpected answers')
        mapped = {}
        for item, question in zip(answers,request.questions):
            if not isinstance(item,dict) or item.get('name') != question.id:
                raise ValueError('Unexpected answer name or order')
            values = item.get('probabilities')
            if not isinstance(values,list) or any(not isinstance(p,dict) or set(p) != {'value','probability'} or not isinstance(p['value'],str) for p in values):
                raise ValueError('Invalid decision distribution')
            if len({p['value'] for p in values}) != len(values):
                raise ValueError('Repeated decision option')
            mapped[question.id] = {k:v for k,v in item.items() if k != 'name'}
            mapped[question.id]['probabilities'] = {p['value']:p['probability'] for p in values}
        answers = mapped
    if not isinstance(answers,dict) or set(answers) != {q.id for q in request.questions}:
        raise ValueError('Missing or unexpected question answer')
    normalized = {q.id:validate_choice(answers[q.id],q) for q in request.questions}
    usage = response.get('usage')
    if not isinstance(usage,dict) or not usage:
        raise ValueError('Missing usage')
    for key in ('input_tokens','output_tokens','total_tokens','prompt_tokens','completion_tokens'):
        if key in usage and (type(usage[key]) is not int or usage[key] < 0):
            raise ValueError('Invalid usage')
    if 'input_tokens' not in usage or 'output_tokens' not in usage:
        raise ValueError('Missing token usage')
    if 'total_tokens' in usage and usage['total_tokens'] != usage['input_tokens'] + usage['output_tokens']:
        raise ValueError('Inconsistent total usage')
    for key in ('cost','cost_nano_usd','estimated_cost_nano_usd'):
        if key in usage and (type(usage[key]) not in (int,float) or not math.isfinite(usage[key]) or usage[key] < 0):
            raise ValueError('Invalid reported cost')
    return {'requested_model':request.model,'served_model':model,'answers':normalized,'usage':usage,
            'facts_attested':False,'execution_authorized':False,'advisory_only':True,
            'notice':'Reported confidence is not a calibrated real-world success probability or independent evidence.'}


class DecisionSession:
    def __init__(self, *, allow_external: bool, client=None):
        if allow_external is not True:
            raise HostedSetupRequired('Explicit external permission is required for decision models')
        token = os.getenv('EXPERIENTIAL_API_KEY','').strip()
        if not 20 <= len(token) <= 4096 or any(ord(c) < 33 or ord(c) > 126 for c in token):
            raise HostedSetupRequired('Configure EXPERIENTIAL_API_KEY securely first')
        self._token, self._client, self._used = token, client, False
        self.receipt = {'inference_calls':0,'automatic_retries':False,'automatic_fallback':False,
                        'gateway_fallback_verified':False,'charge_status':'not_started'}
        self.response = None

    def ask(self, request: DecisionInput):
        if self._used:
            raise HostedSetupRequired('This single-request session has already been used; no retry was made')
        request = DecisionInput.model_validate(request.model_dump(mode='python'))
        endpoint, payload = payload_for(request)
        body = json.dumps(payload,ensure_ascii=False,allow_nan=False).encode()
        if len(body) > MAX_REQUEST_BYTES or _contains_credential(body.decode(),self._token):
            raise HostedSetupRequired('Invalid or oversized decision input; no request was made')
        self._used = True
        self.receipt.update({'inference_calls':1,'request_sha256':_hash(payload),'requested_model':request.model,
                             'endpoint':ORIGIN+endpoint,'charge_status':'unknown','status':'started'})
        client = self._client or httpx.Client(timeout=httpx.Timeout(60,connect=10),follow_redirects=False)
        try:
            with client.stream('POST',ORIGIN+endpoint,headers={'Authorization':'Bearer '+self._token,'Content-Type':'application/json'},
                               content=body,follow_redirects=False,timeout=httpx.Timeout(60,connect=10)) as response:
                self.receipt['http_status'] = response.status_code
                if not 200 <= response.status_code < 300:
                    raise HostedFailure('decision_http_'+str(response.status_code))
                raw = bytearray()
                for chunk in response.iter_bytes():
                    raw.extend(chunk)
                    if len(raw) > MAX_RESPONSE_BYTES:
                        raise HostedFailure('decision_response_too_large')
            text = raw.decode('utf-8')
            if _contains_credential(text,self._token):
                raise HostedFailure('decision_credential_reflection')
            data = json_object(text)
            self.response = data
            self.receipt['response_sha256'] = _hash(data)
            result = validate_response(request,data)
            self.receipt.update({'status':'validated_advisory','served_model':result['served_model'],'usage':result['usage']})
            return result
        except (httpx.HTTPError,UnicodeError,ValueError,TypeError,KeyError,RecursionError) as exc:
            self.receipt['status'] = 'failed_validation_or_transport'
            raise HostedFailure('decision_invalid_response_or_transport') from None
        except HostedFailure:
            self.receipt['status'] = 'failed'
            raise
        finally:
            if self._client is None:
                client.close()
