"""Hosted transport contracts using HTTP doubles; no live inference evidence."""
from copy import deepcopy
from hashlib import sha256
import importlib
import json
import socket

import httpx
import pytest

from eightball.v2 import compatible
from eightball.v2.compatible import CompatibleSession, configuration_status, settings
from eightball.v2.hosted import HostedFailure, HostedSetupRequired, strict_schema

TOKEN = 'fixture_api_key_not_a_live_credential'
BASE = 'https://api.fixture.example/v1'
MODEL = 'fixture/Exact-Model'
SCHEMA = {'type': 'object', 'properties': {'items': {
    'type': 'array', 'items': {'type': 'string'}, 'default': []}}}


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch):
    for key in ('EIGHTBALL_API_KEY', 'EIGHTBALL_API_BASE_URL', 'EIGHTBALL_API_MODEL',
                'EIGHTBALL_API_PROVIDER', 'EIGHTBALL_API_ROUTING_PROVIDER'):
        monkeypatch.delenv(key, raising=False)


def configure(monkeypatch, base=BASE, provider='fixture-provider'):
    for key, value in {'EIGHTBALL_API_KEY': TOKEN, 'EIGHTBALL_API_BASE_URL': base,
                       'EIGHTBALL_API_MODEL': MODEL, 'EIGHTBALL_API_PROVIDER': provider}.items():
        monkeypatch.setenv(key, value)


def envelope(output=None):
    return {'model': 'fixture-served-model-20261016', 'choices': [
        {'finish_reason': 'stop', 'message': {'role': 'assistant',
                                             'content': json.dumps(output if output is not None else {'items': []})}}],
        'usage': {'prompt_tokens': 20, 'completion_tokens': 10, 'total_tokens': 30}}


def client(response=None, handler=None):
    requests = []
    def handle(request):
        requests.append(request)
        return handler(request) if handler else (response if response is not None else httpx.Response(200, json=envelope()))
    return httpx.Client(transport=httpx.MockTransport(handle)), requests


def test_import_and_configuration_never_resolve_or_contact_endpoint(monkeypatch):
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *_args, **_kw: pytest.fail('Unexpected DNS'))
    monkeypatch.setattr(httpx.Client, 'send', lambda *_args, **_kw: pytest.fail('Unexpected HTTP'))
    importlib.reload(compatible)
    status = configuration_status()
    assert status['configuration_state'] == 'not_configured' and not status['configured']
    assert set(status['missing_settings']) == {'EIGHTBALL_API_BASE_URL', 'EIGHTBALL_API_MODEL',
                                               'EIGHTBALL_API_PROVIDER', 'EIGHTBALL_API_KEY'}
    configure(monkeypatch)
    status = configuration_status()
    assert status['configuration_state'] == 'configured_not_tested'
    assert status['endpoint_host'] == 'api.fixture.example'
    assert not status['credentials_validated'] and not status['live_inference_verified']
    assert TOKEN not in json.dumps(status) and TOKEN not in repr(settings())


@pytest.mark.parametrize('permission', [False, None, 'true', 1])
def test_external_permission_must_be_explicit_boolean(monkeypatch, permission):
    configure(monkeypatch); cl, requests = client()
    with pytest.raises(HostedSetupRequired):
        CompatibleSession(allow_external=permission, client=cl)
    assert not requests


@pytest.mark.parametrize('base', [
    'http://api.fixture.example/v1', 'file:///v1', '//api.fixture.example/v1',
    'https://user:secret@api.fixture.example/v1', 'https://api.fixture.example/v1?key=secret',
    'https://api.fixture.example/v1#secret', 'https://api.fixture.example:8443/v1',
    'https://localhost/v1', 'https://api.localhost/v1', 'https://api.local/v1',
    'https://metadata.google.internal/v1', 'https://instance-data.ec2.internal/v1',
    'https://api.intranet/v1', 'https://api.private.example/v1',
    'https://127.0.0.1/v1', 'https://10.0.0.1/v1', 'https://169.254.169.254/v1',
    'https://8.8.8.8/v1', 'https://[::1]/v1', 'https://[2606:4700:4700::1111]/v1',
    'https://2130706433/v1', 'https://0x7f000001/v1', 'https://127.1/v1',
    'https://127.0.0.1.nip.io/v1', 'https://api.localtest.me/v1',
    'https://api.fixture.example./v1', 'https://api.fixture.example/v1/../admin',
    'https://api.fixture.example/v1/%2e%2e/admin', 'https://api.fixture.example/v1//admin',
    'https://api.fixture.example/v1//',
    'https://api.fixture.example/v1\\admin', 'https://api.fixture.example/\nadmin',
    'https://api.fixture.example/v1/chat/completions',
])
def test_unsafe_or_ambiguous_urls_fail_before_http(monkeypatch, base):
    configure(monkeypatch, base); cl, requests = client()
    with pytest.raises(HostedSetupRequired):
        CompatibleSession(allow_external=True, client=cl)
    assert not requests and not configuration_status()['configured']


@pytest.mark.parametrize('name,value', [
    ('EIGHTBALL_API_KEY', 'bad\nheader'), ('EIGHTBALL_API_KEY', 'short'),
    ('EIGHTBALL_API_MODEL', 'https://other.example/model'), ('EIGHTBALL_API_MODEL', 'model:auto'),
    ('EIGHTBALL_API_MODEL', '../secret'), ('EIGHTBALL_API_MODEL', 'namespace//model'),
    ('EIGHTBALL_API_MODEL', 'openrouter/auto'), ('EIGHTBALL_API_MODEL', 'auto'),
    ('EIGHTBALL_API_PROVIDER', 'auto'), ('EIGHTBALL_API_PROVIDER', 'cheapest'),
    ('EIGHTBALL_API_PROVIDER', 'bad/provider'), ('EIGHTBALL_API_PROVIDER', 'Provider\nsecret'),
    ('EIGHTBALL_API_ROUTING_PROVIDER', 'Alibaba'),
])
def test_invalid_settings_fail_without_a_request(monkeypatch, name, value):
    configure(monkeypatch); monkeypatch.setenv(name, value)
    cl, requests = client()
    with pytest.raises(HostedSetupRequired): CompatibleSession(allow_external=True, client=cl)
    assert not requests and not configuration_status()['configured']


def test_strict_request_auth_receipt_and_configuration_freeze(monkeypatch):
    configure(monkeypatch); cl, requests = client()
    session = CompatibleSession(allow_external=True, client=cl)
    for key, value in {'EIGHTBALL_API_BASE_URL': 'https://other.example/collect',
                       'EIGHTBALL_API_MODEL': 'changed', 'EIGHTBALL_API_PROVIDER': 'changed',
                       'EIGHTBALL_API_KEY': 'other_fixture_key'}.items():
        monkeypatch.setenv(key, value)
    schema = deepcopy(SCHEMA)
    output, served = session.generate(schema, 'Extract', {'sources': ['Fictional']})
    assert output == {'items': []} and served == 'fixture-served-model-20261016'
    assert schema == SCHEMA and len(requests) == 1
    request = requests[0]; payload = json.loads(request.content)
    assert str(request.url) == BASE + '/chat/completions'
    assert request.headers['authorization'] == 'Bearer ' + TOKEN
    assert TOKEN not in request.content.decode()
    assert payload['model'] == MODEL and not payload['stream']
    assert payload['max_tokens'] == 4096 and payload['temperature'] == 0
    assert payload['response_format']['type'] == 'json_schema'
    assert payload['response_format']['json_schema'] == {
        'name': 'endstate_proposal', 'strict': True, 'schema': strict_schema(SCHEMA)}
    assert 'enable_thinking' not in payload and 'provider' not in payload
    receipt = session.receipt
    assert receipt['transport'] == 'openai_compatible' and receipt['requested_model'] == MODEL
    assert receipt['api_provider'] == receipt['routing_provider'] == 'fixture-provider'
    assert receipt['endpoint_host'] == 'api.fixture.example' and not receipt['automatic_routing']
    call = receipt['calls'][0]
    assert call['served_model'] == served and call['usage']['total_tokens'] == 30
    assert call['status'] == 'response_received' and call['http_status'] == 200
    assert call['instructions_sha256'] == sha256(json.dumps('Extract', ensure_ascii=False,
        sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert all(len(call[key]) == 64 for key in ('input_sha256', 'schema_sha256', 'response_sha256'))
    assert call['elapsed_ms'] >= 0 and TOKEN not in json.dumps(receipt)
    receipt['calls'][0]['status'] = 'tampered'
    assert session.receipt['calls'][0]['status'] == 'response_received'


def test_success_retains_exact_assistant_text_without_envelope_or_headers(monkeypatch):
    configure(monkeypatch)
    raw = ' \n{\r\n  "items" : ["café", "\\u00e9", "e\u0301", "雪"]\r\n}\t '
    data = envelope(); data['choices'][0]['message']['content'] = raw
    # Unknown provider fields and HTTP headers must never become raw evidence.
    data['provider_debug'] = 'OUTER_ENVELOPE_SENTINEL ' + TOKEN
    body = json.dumps(data, ensure_ascii=False).encode()
    cl, requests = client(httpx.Response(200, content=body, headers={
        'X-Provider-Debug': 'HEADER_SENTINEL ' + TOKEN,
        'Set-Cookie': 'private=' + TOKEN}))
    session = CompatibleSession(allow_external=True, client=cl)
    output, _ = session.generate(SCHEMA, 'Extract', {'sources': ['Fictional']})
    assert output == {'items': ['café', 'é', 'e\u0301', '雪']} and len(requests) == 1
    call = session.receipt['calls'][0]
    assert call['status'] == 'response_received' and call['raw_content'] == raw
    assert call['raw_content_sha256'] == sha256(raw.encode()).hexdigest()
    assert call['response_body_sha256'] == sha256(body).hexdigest()
    assert call['response_body_bytes'] == len(body)
    assert call['response_sha256'] == compatible._hash(output)
    assert call['raw_content_sha256'] != call['response_sha256']
    assert call['raw_content_sha256'] != call['response_body_sha256']
    assert 'raw_content_omitted' not in call
    serialized = json.dumps(session.receipt, ensure_ascii=False)
    assert all(secret not in serialized for secret in (TOKEN, 'OUTER_ENVELOPE_SENTINEL', 'HEADER_SENTINEL'))
    assert all(key not in call for key in ('response_body', 'envelope', 'headers', 'cookies'))


@pytest.mark.parametrize('host', ['dashscope.aliyuncs.com', 'dashscope-intl.aliyuncs.com', 'dashscope-us.aliyuncs.com'])
def test_only_exact_dashscope_hosts_disable_thinking(monkeypatch, host):
    configure(monkeypatch, 'https://' + host + '/compatible-mode/v1', 'alibaba')
    cl, requests = client(); session = CompatibleSession(allow_external=True, client=cl)
    session.generate({}, 'test', {})
    assert json.loads(requests[0].content)['enable_thinking'] is False
    assert session.receipt['calls'][0]['enable_thinking'] is False


def test_dashscope_lookalike_does_not_receive_vendor_options(monkeypatch):
    configure(monkeypatch, 'https://dashscope.aliyuncs.com.other.example/v1', 'alibaba')
    cl, requests = client(); CompatibleSession(allow_external=True, client=cl).generate({}, 'test', {})
    assert 'enable_thinking' not in json.loads(requests[0].content)


def test_openrouter_requires_an_explicit_pinned_provider_no_fallbacks(monkeypatch):
    configure(monkeypatch, 'https://openrouter.ai/api/v1', 'openrouter')
    assert 'EIGHTBALL_API_ROUTING_PROVIDER' in configuration_status()['missing_settings']
    with pytest.raises(HostedSetupRequired): settings()
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', 'Alibaba')
    cl, requests = client(); session = CompatibleSession(allow_external=True, client=cl)
    session.generate({}, 'test', {})
    assert json.loads(requests[0].content)['provider'] == {
        'order': ['Alibaba'], 'only': ['Alibaba'],
        'allow_fallbacks': False, 'require_parameters': True}
    assert session.receipt['routing_provider'] == 'Alibaba'


def test_openrouter_explicit_free_catalog_model_preserves_identity_and_pin(monkeypatch):
    configure(monkeypatch, 'https://openrouter.ai/api/v1', 'openrouter')
    # A fictional catalog slug tests the protocol, not live availability.
    model = 'qwen/fixture-model:free'
    monkeypatch.setenv('EIGHTBALL_API_MODEL', model)
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', 'Fixture Provider')
    status = configuration_status()
    assert status['configuration_state'] == 'configured_not_tested'
    assert status['model'] == model and not status['live_inference_verified']
    response = envelope(); response['model'] = model
    cl, requests = client(httpx.Response(200, json=response))
    session = CompatibleSession(allow_external=True, client=cl)
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'qwen/changed-paid-model')
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', 'Other Provider')
    output, served_model = session.generate(SCHEMA, 'Extract', {'sources': ['Fictional']})
    assert output == {'items': []} and served_model == model and len(requests) == 1
    payload = json.loads(requests[0].content)
    assert str(requests[0].url) == 'https://openrouter.ai/api/v1/chat/completions'
    assert payload['model'] == model
    assert payload['provider'] == {'order': ['Fixture Provider'], 'only': ['Fixture Provider'],
                                   'allow_fallbacks': False, 'require_parameters': True}
    assert payload['response_format']['type'] == 'json_schema'
    assert payload['response_format']['json_schema']['strict'] is True
    assert session.receipt['requested_model'] == session.receipt['calls'][0]['served_model'] == model
    assert session.receipt['routing_provider'] == 'Fixture Provider'
    assert not session.receipt['automatic_routing']
    assert TOKEN not in json.dumps(session.receipt)


@pytest.mark.parametrize('model', ['openrouter/free', 'OpenRouter/Free',
    'openrouter/free:free', 'openrouter/auto', 'openrouter/auto:free'])
def test_openrouter_model_routers_are_rejected_before_http(monkeypatch, model):
    configure(monkeypatch, 'https://openrouter.ai/api/v1', 'openrouter')
    monkeypatch.setenv('EIGHTBALL_API_MODEL', model)
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', 'Fixture Provider')
    cl, requests = client()
    with pytest.raises(HostedSetupRequired):
        CompatibleSession(allow_external=True, client=cl)
    assert not requests and not configuration_status()['configured']


@pytest.mark.parametrize('model', ['qwen/model:nitro', 'qwen/model:free:nitro',
    'qwen/model:nitro:free', 'qwen/model:free:free', 'qwen/model:FREE',
    'qwen/model:free/extra', 'qwen/model:free?key=x', 'qwen/model:free#x',
    'qwen/model%3afree', 'model:free', 'owner/group/model:free', '../model:free',
    'qwen//model:free', 'qwen/' + 'm' * 171 + ':free'])
def test_openrouter_free_exception_does_not_enable_suffix_or_identifier_abuse(monkeypatch, model):
    configure(monkeypatch, 'https://openrouter.ai/api/v1', 'openrouter')
    monkeypatch.setenv('EIGHTBALL_API_MODEL', model)
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', 'Fixture Provider')
    cl, requests = client()
    with pytest.raises(HostedSetupRequired):
        CompatibleSession(allow_external=True, client=cl)
    assert not requests and not configuration_status()['configured']


@pytest.mark.parametrize('base', [BASE, 'https://api.openrouter.ai/api/v1',
    'https://openrouter.ai.other.example/api/v1'])
def test_free_catalog_suffix_is_not_enabled_for_other_hosts(monkeypatch, base):
    configure(monkeypatch, base)
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'qwen/fixture-model:free')
    cl, requests = client()
    with pytest.raises(HostedSetupRequired):
        CompatibleSession(allow_external=True, client=cl)
    assert not requests and not configuration_status()['configured']


@pytest.mark.parametrize('pin', [None, 'auto', 'A,B'])
def test_explicit_free_catalog_model_still_requires_valid_provider_pin(monkeypatch, pin):
    configure(monkeypatch, 'https://openrouter.ai/api/v1', 'openrouter')
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'qwen/fixture-model:free')
    if pin is not None:
        monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', pin)
    cl, requests = client()
    with pytest.raises(HostedSetupRequired):
        CompatibleSession(allow_external=True, client=cl)
    assert not requests and not configuration_status()['configured']


@pytest.mark.parametrize('pin', ['auto', 'fastest', 'cheapest', 'A,B', 'A\nB'])
def test_openrouter_automatic_or_multiple_route_settings_are_rejected(monkeypatch, pin):
    configure(monkeypatch, 'https://openrouter.ai/api/v1', 'openrouter')
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', pin)
    with pytest.raises(HostedSetupRequired): settings()


def test_default_client_preserves_managed_proxy_and_ca_settings(monkeypatch):
    configure(monkeypatch); cl, requests = client(); options = []
    monkeypatch.setenv('HTTPS_PROXY', 'http://proxy.fixture.example:8080')
    monkeypatch.setenv('SSL_CERT_FILE', '/fictional/managed-ca.pem')
    def make_client(**kwargs):
        options.append(kwargs)
        return cl
    monkeypatch.setattr(compatible.httpx, 'Client', make_client)
    CompatibleSession(allow_external=True).generate({}, 'test', {})
    assert len(requests) == 1 and options[0]['trust_env'] is True
    assert options[0]['follow_redirects'] is False
    assert 'proxy' not in options[0] and 'verify' not in options[0]


@pytest.mark.parametrize('status,code', [(301, 'provider_rejected_request'), (302, 'provider_rejected_request'),
    (400, 'provider_rejected_request'), (401, 'authentication_failed'), (402, 'billing_required'),
    (403, 'permission_denied'), (429, 'rate_limited'), (500, 'provider_rejected_request'), (503, 'provider_rejected_request')])
def test_no_retry_redirect_fallback_or_sensitive_error_echo(monkeypatch, status, code):
    configure(monkeypatch)
    cl, requests = client(httpx.Response(status, text='SourceSecret ' + TOKEN,
                                       headers={'Location': 'https://other.example/?key=' + TOKEN}))
    session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure) as caught: session.generate({}, 'test', {})
    assert caught.value.code == code and len(requests) == 1
    assert TOKEN not in str(caught.value) and 'SourceSecret' not in json.dumps(session.receipt)
    assert session.receipt['calls'][0]['status'] == 'failed'


@pytest.mark.parametrize('change', [
    lambda r: r['choices'][0].update(finish_reason='length'),
    lambda r: r['choices'][0].update(finish_reason='content_filter'),
    lambda r: r['choices'][0]['message'].update(refusal='no'),
    lambda r: r['choices'][0]['message'].update(tool_calls=[{'function': 'do-it'}]),
    lambda r: r['choices'][0]['message'].update(function_call={'name': 'do-it'}),
    lambda r: r['choices'][0]['message'].update(role='user'),
    lambda r: r['choices'][0]['message'].update(content={'items': []}),
    lambda r: r['choices'][0]['message'].update(content='```json\n{}\n```'),
    lambda r: r['choices'][0]['message'].update(content='{"x":1,"x":2}'),
    lambda r: r['choices'][0]['message'].update(content='{"x":NaN}'),
    lambda r: r['choices'][0]['message'].update(content='{"x":1e999}'),
    lambda r: r['choices'][0]['message'].update(content='[]'),
    lambda r: r.update(choices=[]), lambda r: r.update(choices=[{}, {}]),
    lambda r: r.update(model=None), lambda r: r.update(model='bad\nidentity'),
    lambda r: r.update(usage=[]), lambda r: r.update(usage={'completion_tokens': True}),
    lambda r: r.update(usage={'total_tokens': -1}), lambda r: r.update(usage={'prompt_tokens': 1.5}),
])
def test_incomplete_refused_malformed_or_invalid_usage_fails(monkeypatch, change):
    configure(monkeypatch); data = envelope(); change(data)
    cl, requests = client(httpx.Response(200, json=data))
    session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure): session.generate({}, 'test', {})
    assert len(requests) == 1 and session.receipt['calls'][0]['status'] == 'failed'


@pytest.mark.parametrize('raw', ['not JSON', '{"model":"x","model":"y"}', '{"x":Infinity}'])
def test_invalid_envelope_has_no_repair_or_text_fallback(monkeypatch, raw):
    configure(monkeypatch); cl, requests = client(httpx.Response(200, text=raw))
    session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure, match='invalid_json'):
        session.generate({}, 'test', {})
    assert len(requests) == 1
    call = session.receipt['calls'][0]
    assert call['response_body_sha256'] == sha256(raw.encode()).hexdigest()
    assert call['response_body_bytes'] == len(raw.encode())
    assert call['raw_content_omitted'] == 'no_attested_assistant_content'
    assert 'raw_content' not in call


@pytest.mark.parametrize('finish', ['stop', 'length'])
def test_original_rejected_assistant_text_and_identity_are_retained(monkeypatch, finish):
    configure(monkeypatch); raw = '```json\n{"items":["broken"],}\n```'
    data = envelope(); data['choices'][0]['message']['content'] = raw
    data['choices'][0]['finish_reason'] = finish
    cl, _ = client(httpx.Response(200, json=data)); session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure): session.generate({}, 'test', {})
    call = session.receipt['calls'][0]
    assert call['raw_content'] == raw and call['raw_content_sha256'] == sha256(raw.encode()).hexdigest()
    assert call['served_model'] == data['model']
    assert call['error_code'] == ('invalid_json' if finish == 'stop' else 'incomplete_or_refused')
    assert call['elapsed_ms'] >= 0


@pytest.mark.parametrize('raw', [
    'not JSON ' + TOKEN, json.dumps({'secret': TOKEN}),
    json.dumps({'items': [TOKEN]}),
    json.dumps({'items': [TOKEN]}).replace('_', '\\u005f'),
    json.dumps({'secret': TOKEN}).replace('_', '\\u005f'),
    json.dumps({TOKEN: ['nested']}).replace('_', '\\u005f'),
    '{"secret":"' + TOKEN.replace('_', '\\u005f') + '",',
])
def test_reflected_key_is_omitted_and_never_returned_as_parsed_output(monkeypatch, raw):
    configure(monkeypatch); data = envelope(); data['choices'][0]['message']['content'] = raw
    cl, _ = client(httpx.Response(200, json=data)); session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure, match='credential_in_response') as caught:
        session.generate({}, 'test', {})
    call = session.receipt['calls'][0]
    assert 'raw_content' not in call and call['raw_content_omitted'] == 'contains_configured_credential'
    assert call['raw_content_sha256'] == sha256(raw.encode()).hexdigest()
    assert TOKEN not in json.dumps(session.receipt) and TOKEN not in str(caught.value)


def test_truncated_escaped_credential_is_not_retained_as_raw_evidence(monkeypatch):
    configure(monkeypatch); data = envelope()
    raw = '{"secret":"' + TOKEN.replace('_', '\\u005f')
    data['choices'][0].update(finish_reason='length')
    data['choices'][0]['message']['content'] = raw
    cl, _ = client(httpx.Response(200, json=data)); session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure, match='incomplete_or_refused'): session.generate({}, 'test', {})
    call = session.receipt['calls'][0]
    assert call['raw_content_omitted'] == 'contains_configured_credential' and 'raw_content' not in call
    assert call['raw_content_sha256'] == sha256(raw.encode()).hexdigest()


def test_non_utf8_assistant_unicode_is_omitted_without_breaking_receipt(monkeypatch):
    configure(monkeypatch); data = envelope(); data['choices'][0]['message']['content'] = 'unpaired\ud800'
    body = json.dumps(data).encode()
    cl, _ = client(httpx.Response(200, content=body)); session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure, match='invalid_json'): session.generate({}, 'test', {})
    call = session.receipt['calls'][0]
    assert call['raw_content_omitted'] == 'invalid_unicode' and 'raw_content' not in call
    assert call['response_body_sha256'] == sha256(body).hexdigest()
    json.dumps(session.receipt, ensure_ascii=False).encode()


@pytest.mark.parametrize('usage', [None, {}])
def test_absent_usage_is_reported_without_invented_token_counts(monkeypatch, usage):
    configure(monkeypatch); data = envelope(); data['usage'] = usage
    cl, _ = client(httpx.Response(200, json=data)); session = CompatibleSession(allow_external=True, client=cl)
    session.generate({}, 'test', {})
    assert session.receipt['calls'][0]['usage'] == {}


@pytest.mark.parametrize('exception,code', [(httpx.ReadTimeout, 'timeout'), (httpx.ConnectError, 'transport_error')])
def test_network_failure_does_not_echo_exception_or_retry(monkeypatch, exception, code):
    configure(monkeypatch)
    def fail(request): raise exception('SourceSecret ' + TOKEN, request=request)
    cl, requests = client(handler=fail); session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure) as caught: session.generate({}, 'test', {})
    assert caught.value.code == code and len(requests) == 1
    assert TOKEN not in str(caught.value) and 'SourceSecret' not in json.dumps(session.receipt)
    assert session.receipt['calls'][0]['elapsed_ms'] >= 0


def test_request_and_streamed_response_limits(monkeypatch):
    configure(monkeypatch); cl, requests = client()
    session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedSetupRequired): session.generate({}, 'test', {'source': 'x' * 160000})
    assert not requests and not session.receipt['calls']
    class Oversized(httpx.SyncByteStream):
        def __iter__(self):
            yield b'x' * 250001
            yield b'x' * 250000
            pytest.fail('Read beyond response limit')
    cl, requests = client(httpx.Response(200, stream=Oversized()))
    session = CompatibleSession(allow_external=True, client=cl)
    with pytest.raises(HostedFailure, match='response_too_large'): session.generate({}, 'test', {})
    assert len(requests) == 1 and session.receipt['calls'][0]['error_code'] == 'response_too_large'
