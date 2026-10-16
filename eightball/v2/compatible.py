"""Explicit, opt-in hosted OpenAI-compatible structured-output transport.

Configuration is server-owned and frozen per analysis. URL checks constrain its
format, not DNS resolution or remote trust: deployment egress and secret-host
policy remain responsible for permitting the selected endpoint. Status checks
never resolve a hostname or contact a provider. Managed proxy/CA settings apply.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import ipaddress
import json
import os
import re
import time
from urllib.parse import urlsplit

import httpx

from .hosted import (HostedFailure, HostedSetupRequired, MAX_OUTPUT_TOKENS,
                     MAX_REQUEST_BYTES, MAX_RESPONSE_BYTES, _hash, json_object,
                     strict_schema)

_REQUIRED = ('EIGHTBALL_API_BASE_URL', 'EIGHTBALL_API_MODEL',
             'EIGHTBALL_API_PROVIDER', 'EIGHTBALL_API_KEY')
_AUTOMATIC = {'auto', 'automatic', 'fastest', 'cheapest', 'preferred', 'default'}
_PRIVATE_LABELS = {'localhost', 'localdomain', 'local', 'internal', 'intranet',
                   'private', 'lan', 'home', 'onion', 'metadata', 'instance-data'}
_DNS_ALIASES = ('nip.io', 'sslip.io', 'localtest.me', 'lvh.me')
_DASHSCOPE_HOSTS = {'dashscope.aliyuncs.com', 'dashscope-intl.aliyuncs.com',
                    'dashscope-us.aliyuncs.com'}
_MODEL = re.compile(r'[A-Za-z0-9][A-Za-z0-9._/-]{0,179}')
_SERVED_MODEL = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:/@-]{0,179}')


def _contains_credential(content: str, token: str) -> bool:
    # Redaction only, never acceptance/repair. Conservatively recognize JSON
    # escapes even in rejected/truncated text, so evidence cannot encode a key.
    escapes = {'"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f',
               'n': '\n', 'r': '\r', 't': '\t'}
    decoded = re.sub(r'\\(u[0-9a-fA-F]{4}|["\\/bfnrt])',
                     lambda m: chr(int(m[1][1:], 16)) if m[1].startswith('u') else escapes[m[1]], content)
    if token in content or token in decoded:
        return True
    try:
        pending = [json.loads(content)]
    except (ValueError, TypeError, RecursionError):
        return False
    while pending:
        value = pending.pop()
        if isinstance(value, str) and token in value:
            return True
        if isinstance(value, dict):
            pending.extend(value.keys())
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
    return False


@dataclass(frozen=True)
class CompatibleSettings:
    token: str = field(repr=False)
    model: str
    provider: str
    endpoint: str
    endpoint_host: str
    routing_provider: str | None = None


def _endpoint(base: str) -> tuple[str, str]:
    # Reject parser normalization, encoded path tricks and alternate literal IP
    # spellings. Only a DNS hostname and simple, absolute API base path qualify.
    if (not 1 <= len(base) <= 2048 or any(ord(c) < 33 or ord(c) > 126 for c in base)
            or any(c in base for c in ('\\', '%', '?', '#'))):
        raise HostedSetupRequired('EIGHTBALL_API_BASE_URL must be a hosted HTTPS API base URL without credentials, query or fragment.')
    try:
        url = urlsplit(base)
        host = url.hostname or ''
        port = url.port
    except ValueError:
        raise HostedSetupRequired('EIGHTBALL_API_BASE_URL is not a valid hosted HTTPS API base URL.') from None
    if (url.scheme != 'https' or url.username is not None or url.password is not None
            or port not in (None, 443) or not host or host.endswith('.')
            or len(host) > 253):
        raise HostedSetupRequired('Choose a hosted HTTPS DNS endpoint on port 443, without URL credentials.')
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise HostedSetupRequired('IP literal endpoints are not enabled for hosted analysis.')
    labels = host.split('.')
    if (len(labels) < 2 or not re.fullmatch(r'[A-Za-z]{2,63}', labels[-1])
            or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label)
                   for label in labels)
            or any(label in _PRIVATE_LABELS for label in labels)
            or any(host == suffix or host.endswith('.' + suffix) for suffix in _DNS_ALIASES)):
        raise HostedSetupRequired('Choose a hosted DNS endpoint; local, private-style and metadata hostnames are not enabled.')
    path = url.path.rstrip('/')
    if (len(path) > 240 or '//' in url.path or (path and not path.startswith('/'))
            or any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', part)
                   or part in {'.', '..'} for part in path.split('/')[1:])
            or path.endswith('/chat/completions')):
        raise HostedSetupRequired('EIGHTBALL_API_BASE_URL must be an API base path, without encoded, empty or relative path segments; omit /chat/completions.')
    return 'https://' + host + path + '/chat/completions', host


def settings() -> CompatibleSettings:
    values = {name: os.getenv(name, '').strip() for name in _REQUIRED}
    if any(not value for value in values.values()):
        raise HostedSetupRequired('Set EIGHTBALL_API_BASE_URL, EIGHTBALL_API_MODEL, EIGHTBALL_API_PROVIDER and EIGHTBALL_API_KEY on the server first. No hosted request was made.')
    token, model, provider = (values['EIGHTBALL_API_KEY'], values['EIGHTBALL_API_MODEL'],
                              values['EIGHTBALL_API_PROVIDER'])
    if not 8 <= len(token) <= 4096 or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise HostedSetupRequired('EIGHTBALL_API_KEY has an invalid format. No hosted request was made.')
    if (not _MODEL.fullmatch(model) or any(part in {'', '.', '..'} for part in model.split('/'))
            or model.lower() in _AUTOMATIC or model.lower() == 'openrouter/auto'):
        raise HostedSetupRequired('EIGHTBALL_API_MODEL must be one explicit model identifier, without a URL or automatic routing suffix.')
    if provider in _AUTOMATIC or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', provider):
        raise HostedSetupRequired('Choose one explicit EIGHTBALL_API_PROVIDER identity; automatic routing is not enabled.')
    endpoint, host = _endpoint(values['EIGHTBALL_API_BASE_URL'])
    routing = os.getenv('EIGHTBALL_API_ROUTING_PROVIDER', '').strip()
    if host == 'openrouter.ai':
        if (provider != 'openrouter' or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9 ._-]{0,79}', routing)
                or routing.lower() in _AUTOMATIC):
            raise HostedSetupRequired('OpenRouter requires EIGHTBALL_API_PROVIDER=openrouter and one explicit EIGHTBALL_API_ROUTING_PROVIDER; automatic provider routing is not enabled.')
    elif routing or provider == 'openrouter':
        raise HostedSetupRequired('EIGHTBALL_API_ROUTING_PROVIDER is only supported for the exact openrouter.ai endpoint.')
    return CompatibleSettings(token, model, provider, endpoint, host, routing or None)


def configuration_status() -> dict:
    """Local presence/format only; not DNS, authentication or model validation."""
    missing = [name for name in _REQUIRED if not os.getenv(name, '').strip()]
    if (os.getenv('EIGHTBALL_API_PROVIDER', '').strip() == 'openrouter'
            and not os.getenv('EIGHTBALL_API_ROUTING_PROVIDER', '').strip()):
        missing.append('EIGHTBALL_API_ROUTING_PROVIDER')
    status = {'configured': False, 'configuration_state': 'not_configured' if missing else 'invalid_configuration',
              'missing_settings': missing, 'credentials_validated': False,
              'live_inference_verified': False, 'model': None, 'api_provider': None,
              'routing_provider': None, 'endpoint_host': None}
    try:
        configured = settings()
    except HostedSetupRequired:
        return status
    status.update(configured=True, configuration_state='configured_not_tested',
                  model=configured.model, api_provider=configured.provider,
                  routing_provider=configured.routing_provider or configured.provider,
                  endpoint_host=configured.endpoint_host)
    return status


class CompatibleSession:
    """One operator-authorized hosted analysis; no store or command access."""
    def __init__(self, *, allow_external: bool, client=None):
        if allow_external is not True:
            raise HostedSetupRequired('Explicit permission is required before sending selected case context to the configured hosted API provider.')
        self._settings = settings()
        self._client = client
        self.calls: list[dict] = []

    @property
    def receipt(self) -> dict:
        return {'transport': 'openai_compatible', 'api_provider': self._settings.provider,
                'endpoint_host': self._settings.endpoint_host,
                'requested_model': self._settings.model,
                'routing_provider': self._settings.routing_provider or self._settings.provider,
                'automatic_routing': False, 'explicit_operator_permission': True,
                'calls': json.loads(json.dumps(self.calls, allow_nan=False))}

    def generate(self, schema: dict, instructions: str, context: dict) -> tuple[dict, str]:
        prepared = strict_schema(schema)
        payload = {'model': self._settings.model, 'stream': False,
                   'temperature': 0, 'max_tokens': MAX_OUTPUT_TOKENS,
                   'response_format': {'type': 'json_schema', 'json_schema': {
                       'name': 'endstate_proposal', 'strict': True, 'schema': prepared}},
                   'messages': [
                       {'role': 'system', 'content': instructions + '\nReturn one JSON object matching the supplied schema. No tools, markdown or external actions.\n' + json.dumps(prepared)},
                       {'role': 'user', 'content': json.dumps(context, ensure_ascii=False, allow_nan=False)}]}
        if self._settings.endpoint_host in _DASHSCOPE_HOSTS:
            # DashScope's non-streaming Qwen thinking mode is incompatible with
            # this bounded JSON-only contract. Never send this vendor option to
            # another endpoint or silently retry with weaker output settings.
            payload['enable_thinking'] = False
        if self._settings.routing_provider:
            payload['provider'] = {'order': [self._settings.routing_provider],
                                   'only': [self._settings.routing_provider],
                                   'allow_fallbacks': False, 'require_parameters': True}
        body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode()
        if len(body) > MAX_REQUEST_BYTES:
            raise HostedSetupRequired('Selected context and schema exceed the hosted request limit. No request was made.')
        started = time.perf_counter()
        call = {'input_sha256': _hash(context), 'schema_sha256': _hash(prepared),
                'instructions_sha256': _hash(instructions), 'max_output_tokens': MAX_OUTPUT_TOKENS,
                'status': 'started'}
        if self._settings.endpoint_host in _DASHSCOPE_HOSTS:
            call['enable_thinking'] = False
        self.calls.append(call)
        assistant_content = None
        try:
            if self._client is None:
                # Inherit the managed runtime's proxy and trusted CA settings.
                with httpx.Client(follow_redirects=False, trust_env=True,
                                  timeout=httpx.Timeout(120, connect=10)) as client:
                    content = self._request(client, body, call)
            else:
                content = self._request(self._client, body, call)
            call.update(response_body_sha256=sha256(content).hexdigest(),
                        response_body_bytes=len(content))
            envelope = json_object(content)
            model = envelope.get('model')
            valid_model = (isinstance(model, str) and _SERVED_MODEL.fullmatch(model)
                           and self._settings.token not in model)
            if valid_model:
                call['served_model'] = model
            choices = envelope.get('choices')
            if not isinstance(choices, list) or len(choices) != 1:
                raise HostedFailure('invalid_choices')
            choice = choices[0]
            if not isinstance(choice, dict):
                raise HostedFailure('invalid_choices')
            message = choice.get('message')
            if (not isinstance(message, dict) or message.get('role') != 'assistant'
                    or not isinstance(message.get('content'), str)):
                raise HostedFailure('unsupported_response')
            assistant_content = message['content']
            try:
                raw_content = assistant_content.encode()
            except UnicodeEncodeError:
                # Escaped lone surrogates are not durable UTF-8 source text.
                # The exact envelope bytes remain identified by their hash.
                call['raw_content_omitted'] = 'invalid_unicode'
                assistant_content = None
                raise HostedFailure('invalid_json') from None
            call['raw_content_sha256'] = sha256(raw_content).hexdigest()
            if choice.get('finish_reason') != 'stop':
                raise HostedFailure('incomplete_or_refused')
            if message.get('tool_calls') or message.get('function_call') or message.get('refusal'):
                raise HostedFailure('unsupported_response')
            if not valid_model:
                raise HostedFailure('missing_model_identity')
            if _contains_credential(assistant_content, self._settings.token):
                raise HostedFailure('credential_in_response')
            output = json_object(assistant_content)
            usage = envelope.get('usage')
            if usage is None:
                usage = {}
            if not isinstance(usage, dict):
                raise HostedFailure('invalid_usage')
            tokens = {key: usage[key] for key in ('prompt_tokens', 'completion_tokens', 'total_tokens') if key in usage}
            if any(type(n) is not int or n < 0 for n in tokens.values()):
                raise HostedFailure('invalid_usage')
            call.update(status='response_received', usage=tokens,
                        response_sha256=_hash(output), finish_reason='stop')
            return output, model
        except HostedFailure as exc:
            call.update(status='failed', error_code=exc.code)
            self._retain_rejection(call, assistant_content)
            raise
        except httpx.TimeoutException:
            call.update(status='failed', error_code='timeout')
            raise HostedFailure('timeout') from None
        except httpx.HTTPError:
            call.update(status='failed', error_code='transport_error')
            raise HostedFailure('transport_error') from None
        except (ValueError, TypeError, KeyError, RecursionError):
            call.update(status='failed', error_code='invalid_json')
            self._retain_rejection(call, assistant_content)
            raise HostedFailure('invalid_json') from None
        finally:
            call['elapsed_ms'] = round((time.perf_counter() - started) * 1000, 2)

    def _retain_rejection(self, call: dict, content: str | None) -> None:
        if content is None:
            if 'response_body_sha256' in call:
                call.setdefault('raw_content_omitted', 'no_attested_assistant_content')
            return
        if _contains_credential(content, self._settings.token):
            call['raw_content_omitted'] = 'contains_configured_credential'
        else:
            # The whole response stream already passed MAX_RESPONSE_BYTES.
            # Preserve the exact text, without JSON repair or prose stripping.
            call['raw_content'] = content

    def _request(self, client, body: bytes, call: dict) -> bytes:
        with client.stream('POST', self._settings.endpoint, content=body,
                           headers={'Authorization': 'Bearer ' + self._settings.token,
                                    'Content-Type': 'application/json', 'Accept': 'application/json'},
                           follow_redirects=False, timeout=httpx.Timeout(120, connect=10)) as response:
            call['http_status'] = response.status_code
            if response.status_code != 200:
                code = {401: 'authentication_failed', 403: 'permission_denied', 402: 'billing_required',
                        429: 'rate_limited'}.get(response.status_code, 'provider_rejected_request')
                raise HostedFailure(code)  # Never read/store/echo an error body.
            chunks = []
            size = 0
            for chunk in response.iter_bytes():
                size += len(chunk)
                if size > MAX_RESPONSE_BYTES:
                    raise HostedFailure('response_too_large')
                chunks.append(chunk)
            return b''.join(chunks)
