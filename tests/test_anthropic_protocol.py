"""Native Messages software contracts; controlled responses, no actual inference."""
from copy import deepcopy
from datetime import timedelta
import json
from pathlib import Path

import httpx
import pytest

from eightball.v2.compatible import CompatibleSession, anthropic_schema, configuration_status, settings
from eightball.v2.contracts import Case, Evidence, utcnow
from eightball.v2.hosted import HostedFailure, HostedSetupRequired, strict_schema
from eightball.v2.intelligence import propose

KEY = 'fictional_anthropic_protocol_key'
MODEL = 'claude-sonnet-4-6'
SCHEMA = {'type': 'object', 'properties': {'items': {'type': 'array', 'maxItems': 4,
    'items': {'type': 'string', 'minLength': 2, 'maxLength': 180}}}}


@pytest.fixture(autouse=True)
def configure(monkeypatch):
    for name, value in {'EIGHTBALL_API_BASE_URL': 'https://api.anthropic.com/v1',
        'EIGHTBALL_API_PROVIDER': 'anthropic', 'EIGHTBALL_API_MODEL': MODEL,
        'EIGHTBALL_API_KEY': KEY, 'EIGHTBALL_API_PROTOCOL': 'anthropic_messages'}.items():
        monkeypatch.setenv(name, value)
    monkeypatch.delenv('EIGHTBALL_API_ROUTING_PROVIDER', raising=False)


def envelope(output=None):
    return {'type': 'message', 'role': 'assistant', 'model': MODEL,
        'content': [{'type': 'text', 'text': json.dumps(output if output is not None else {'items': []})}],
        'stop_reason': 'end_turn', 'usage': {'input_tokens': 30, 'output_tokens': 20}}


def test_native_requires_explicit_protocol_and_exact_endpoint(monkeypatch):
    assert settings().endpoint == 'https://api.anthropic.com/v1/messages'
    assert configuration_status()['api_protocol'] == 'anthropic_messages'
    monkeypatch.delenv('EIGHTBALL_API_PROTOCOL')
    assert settings().endpoint.endswith('/chat/completions')
    assert settings().api_protocol == 'openai_compatible'
    monkeypatch.setenv('EIGHTBALL_API_PROTOCOL', 'anthropic_messages')
    for name, value in [('EIGHTBALL_API_BASE_URL', 'https://other.example/v1'),
                        ('EIGHTBALL_API_PROVIDER', 'another'), ('EIGHTBALL_API_PROTOCOL', 'auto')]:
        with monkeypatch.context() as change:
            change.setenv(name, value)
            with pytest.raises(HostedSetupRequired): settings()
            assert configuration_status()['configuration_state'] == 'invalid_configuration'
    with pytest.raises(HostedSetupRequired, match='permission'):
        CompatibleSession(allow_external=False)


def test_native_wire_contract_and_exact_retained_text():
    sent = []
    text = '{\n  "items": ["exact fictional text"]\n}'
    response = envelope();response['content'][0]['text'] = text
    def respond(request):
        sent.append(request)
        return httpx.Response(200, json=response)
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        session = CompatibleSession(allow_external=True, client=client)
        output, model = session.generate(SCHEMA, 'Bounded instructions.', {'source': 'Fictional.'})
    request = sent[0];payload = json.loads(request.content)
    assert str(request.url) == 'https://api.anthropic.com/v1/messages'
    assert request.headers['x-api-key'] == KEY and 'authorization' not in request.headers
    assert request.headers['anthropic-version'] == '2023-06-01'
    assert request.headers['accept-encoding'] == 'identity'
    assert payload['model'] == MODEL and payload['stream'] is False and payload['max_tokens'] == 4096
    assert payload['messages'] == [{'role': 'user', 'content': '{"source": "Fictional."}'}]
    assert 'maxLength' in payload['system']
    assert 'response_format' not in payload and 'tools' not in payload and 'temperature' not in payload
    wire = payload['output_config']['format']
    assert wire['type'] == 'json_schema' and wire['schema']['additionalProperties'] is False
    item = wire['schema']['properties']['items']
    assert 'maxItems' not in item and 'maxItems' in item['description']
    assert 'maxLength' not in item['items'] and 'maxLength' in item['items']['description']
    call = session.receipt['calls'][0]
    assert output == json.loads(text) and model == MODEL
    assert call['raw_content'] == text and call['native_stop_reason'] == 'end_turn'
    assert call['finish_reason'] == 'stop' and call['usage']['total_tokens'] == 50
    assert call['schema_sha256'] != call['wire_schema_sha256']
    assert session.receipt['api_protocol'] == call['api_protocol'] == 'anthropic_messages'
    assert KEY not in json.dumps(session.receipt)
    assert len(sent) == 1


def test_schema_translation_preserves_named_properties_and_original_constraints():
    schema = {'type': 'object', 'properties': {'minimum': {'type': 'integer', 'minimum': 1},
        'maxLength': {'type': 'array', 'minItems': 2, 'items': {'type': 'string', 'maxLength': 3}},
        'optional': {'anyOf': [{'type': 'number', 'exclusiveMaximum': 10}, {'type': 'null'}]}}}
    before = deepcopy(schema)
    wire = anthropic_schema(strict_schema(schema))
    assert schema == before and set(wire['properties']) == set(schema['properties'])
    assert 'minimum' not in wire['properties']['minimum']
    assert 'minItems' not in wire['properties']['maxLength']
    assert 'exclusiveMaximum' not in wire['properties']['optional']['anyOf'][0]


@pytest.mark.parametrize('change,code', [
    ({'stop_reason': 'max_tokens'}, 'incomplete_or_refused'),
    ({'stop_reason': 'refusal'}, 'incomplete_or_refused'),
    ({'stop_reason': 'tool_use'}, 'incomplete_or_refused'),
    ({'stop_reason': None}, 'incomplete_or_refused'),
    ({'model': ''}, 'missing_model_identity'),
    ({'role': 'user'}, 'unsupported_response'),
    ({'content': [{'type': 'tool_use', 'input': {}}]}, 'unsupported_response'),
    ({'content': [{'type': 'text', 'text': '{}'}, {'type': 'text', 'text': '{}'}]}, 'unsupported_response'),
    ({'content': [{'type': 'text', 'text': '```json\n{}\n```'}]}, 'invalid_json'),
    ({'content': [{'type': 'text', 'text': '{"items":[],"items":[]}'}]}, 'invalid_json'),
    ({'usage': {'input_tokens': True, 'output_tokens': 1}}, 'invalid_usage'),
    ({'content': [{'type': 'text', 'text': json.dumps({'secret': KEY})}]}, 'credential_in_response'),
])
def test_native_rejections_are_never_repaired_or_retried(change, code):
    response = envelope();response.update(change)
    seen = []
    def respond(request):
        seen.append(request)
        return httpx.Response(200, json=response)
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        session = CompatibleSession(allow_external=True, client=client)
        with pytest.raises(HostedFailure) as failure:
            session.generate(SCHEMA, 'Instructions.', {})
    assert failure.value.code == code and len(seen) == 1
    assert session.receipt['calls'][0]['status'] == 'failed'
    assert KEY not in json.dumps(session.receipt)


@pytest.mark.parametrize('status,code', [(401,'authentication_failed'), (402,'billing_required'),
    (403,'permission_denied'), (429,'rate_limited'), (302,'provider_rejected_request')])
def test_native_error_bodies_and_redirects_are_not_read(status, code):
    class Unread(httpx.SyncByteStream):
        def __iter__(self):
            pytest.fail('Error body was read')
            yield b''
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(status, stream=Unread()))) as client:
        session = CompatibleSession(allow_external=True, client=client)
        with pytest.raises(HostedFailure) as failure: session.generate(SCHEMA, '', {})
    assert failure.value.code == code


def test_native_encoded_response_is_rejected_before_decompression():
    class Unread(httpx.SyncByteStream):
        def __iter__(self):
            pytest.fail('Encoded response was read')
            yield b''
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200,
            headers={'Content-Encoding':'gzip'}, stream=Unread()))) as client:
        with pytest.raises(HostedFailure, match='unsupported_response_encoding'):
            CompatibleSession(allow_external=True, client=client).generate(SCHEMA, '', {})


def test_native_extraction_preserves_original_local_bounds_and_source_checks():
    text = 'Fictional source quotation.'
    case = Case(title='Fictional test', client='Fictional only', summary=text, desired_outcome='Review the source',
        deadline=utcnow()+timedelta(days=1), evidence=[Evidence(id='source',title='Source',source='Fixture',text=text)])
    before = case.model_dump(mode='json')
    for output in ({'items':[{'kind':'claim','text':'x'*181,'source':{'evidence_id':'source','quote':text}}]},
                   {'items':[{'kind':'claim','text':'A claim','source':{'evidence_id':'source','quote':'Invented quotation'}}]}):
        with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200,json=envelope(output)))) as client:
            with pytest.raises(ValueError):
                propose(case,'openai_compatible','extract',['source'],allow_external=True,client=client)
        assert case.model_dump(mode='json') == before


def test_native_staged_graph_runs_original_compiler_and_keeps_case_detached():
    fixture = json.loads((Path(__file__).parent/'fixtures/drafting/staged.json').read_text())
    outcome = 'Obtain enough suitable chairs and the venue manager written acceptance'
    case = Case(title='Fictional test',client='Fictional only',summary='Supplier failure.',desired_outcome=outcome,
        deadline=utcnow()+timedelta(days=1))
    fixture['frame']['target_bindings'] = [{'criterion_index':i,'target_quote':outcome}
        for i in range(len(fixture['frame']['success_criteria']))]
    responses = [fixture['frame'],fixture['routes']]
    before = case.model_dump(mode='json')
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200,json=envelope(responses.pop(0))))) as client:
        proposal = propose(case,'openai_compatible','graph',[],allow_external=True,client=client)
    assert not responses and proposal.status == 'pending'
    assert len(proposal.raw_output['transport']['calls']) == 2
    assert proposal.raw_output['transport']['api_protocol'] == 'anthropic_messages'
    assert all(item.object['approval_required'] for item in proposal.items if item.kind == 'action')
    assert case.model_dump(mode='json') == before
