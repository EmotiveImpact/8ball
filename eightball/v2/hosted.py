"""Opt-in Hugging Face Inference Providers transport.

No default model, automatic provider routing, retries, model downloads, key files
or network activity at import/configuration time. Credentials never enter a case,
request body, browser response or model trace. The transport has no store access.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
import os
import re
import time
from typing import Any

import httpx

from ..providers import ProviderUnavailable

HF_ENDPOINT = 'https://router.huggingface.co/v1/chat/completions'
MAX_REQUEST_BYTES = 150_000
MAX_RESPONSE_BYTES = 500_000
MAX_OUTPUT_TOKENS = 4096
_AUTOMATIC = {'auto', 'fastest', 'cheapest', 'preferred'}


class HostedSetupRequired(ValueError):
    """Operator configuration error, not an attempted model call."""


class HostedFailure(ProviderUnavailable):
    def __init__(self, code: str):
        self.code = code
        super().__init__('Hosted analysis did not complete (' + code + '). No case state changed.')


@dataclass(frozen=True)
class HostedSettings:
    token: str = field(repr=False)
    model: str
    provider: str

    @property
    def routed_model(self) -> str:
        return self.model + ':' + self.provider


def settings() -> HostedSettings:
    token = os.getenv('HF_TOKEN', '').strip()
    model = os.getenv('EIGHTBALL_HF_MODEL', '').strip()
    provider = os.getenv('EIGHTBALL_HF_PROVIDER', '').strip()
    if not token or not model or not provider:
        raise HostedSetupRequired('Set HF_TOKEN, EIGHTBALL_HF_MODEL and EIGHTBALL_HF_PROVIDER on the server first. No hosted request was made.')
    if not 8 <= len(token) <= 4096 or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise HostedSetupRequired('HF_TOKEN has an invalid format. No hosted request was made.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}/[A-Za-z0-9][A-Za-z0-9_.-]{0,95}', model):
        raise HostedSetupRequired('EIGHTBALL_HF_MODEL must be an explicit namespace/model identifier, without a URL or routing suffix.')
    if provider in _AUTOMATIC or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', provider):
        raise HostedSetupRequired('Choose one explicit EIGHTBALL_HF_PROVIDER. Automatic routing policies are not enabled.')
    return HostedSettings(token, model, provider)


def configuration_status() -> dict:
    """Presence/format only. Never claims authentication or inference succeeded."""
    missing = [name for name in ('HF_TOKEN', 'EIGHTBALL_HF_MODEL', 'EIGHTBALL_HF_PROVIDER')
               if not os.getenv(name, '').strip()]
    try:
        configured = settings()
    except HostedSetupRequired:
        return {'configured': False, 'configuration_state': 'not_configured' if missing else 'invalid_configuration',
                'missing_settings': missing, 'credentials_validated': False,
                'live_inference_verified': False, 'model': None, 'routing_provider': None}
    return {'configured': True, 'configuration_state': 'configured_not_tested',
            'missing_settings': [], 'credentials_validated': False,
            'live_inference_verified': False, 'model': configured.model,
            'routing_provider': configured.provider}


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def strict_schema(schema: dict) -> dict:
    """Detach the schema and make optional/defaulted properties explicit.

    The internal Pydantic contract is still validated afterwards. Unsupported
    provider/schema combinations fail; we never downgrade to unstructured text.
    """
    result = json.loads(json.dumps(schema, allow_nan=False))
    def visit(node):
        if isinstance(node, dict):
            node.pop('default', None)
            if node.get('type') == 'object' or 'properties' in node:
                node['additionalProperties'] = False
                node['required'] = list(node.get('properties', {}))
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
    visit(result)
    return result


def _pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('Duplicate JSON key')
        value[key] = item
    return value


def _constant(_):
    raise ValueError('Non-finite JSON number')


def json_object(raw: str | bytes) -> dict:
    value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object')
    # Also reject overflow such as 1e999, which parse_constant does not see.
    json.dumps(value, allow_nan=False)
    return value


class HuggingFaceSession:
    """One operator-authorised analysis, possibly containing two draft stages."""
    def __init__(self, *, allow_external: bool, client=None):
        if allow_external is not True:
            raise HostedSetupRequired('Explicit permission is required before sending selected case context to Hugging Face and the chosen provider.')
        self._settings = settings()  # Freeze routing and credentials for this analysis.
        self._client = client
        self.calls: list[dict] = []

    @property
    def receipt(self) -> dict:
        return {'transport': 'huggingface_inference_providers',
                'requested_model': self._settings.model, 'routing_provider': self._settings.provider,
                'automatic_routing': False, 'explicit_operator_permission': True,
                'calls': json.loads(json.dumps(self.calls, allow_nan=False))}

    def generate(self, schema: dict, instructions: str, context: dict) -> tuple[dict, str]:
        prepared = strict_schema(schema)
        payload = {'model': self._settings.routed_model, 'stream': False,
                   'temperature': 0, 'max_tokens': MAX_OUTPUT_TOKENS,
                   'response_format': {'type': 'json_schema', 'json_schema': {
                       'name': 'endstate_proposal', 'strict': True, 'schema': prepared}},
                   'messages': [
                       {'role': 'system', 'content': instructions + '\nReturn one JSON object matching the supplied schema. No tools, markdown or external actions.\n' + json.dumps(prepared)},
                       {'role': 'user', 'content': json.dumps(context, ensure_ascii=False, allow_nan=False)}]}
        body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode()
        if len(body) > MAX_REQUEST_BYTES:
            raise HostedSetupRequired('Selected context and schema exceed the hosted request limit. No request was made.')
        started = time.perf_counter()
        call = {'input_sha256': _hash(context), 'schema_sha256': _hash(prepared),
                'instructions_sha256': _hash(instructions), 'max_output_tokens': MAX_OUTPUT_TOKENS,
                'status': 'started'}
        self.calls.append(call)
        try:
            if self._client is None:
                with httpx.Client(follow_redirects=False, trust_env=False,
                                  timeout=httpx.Timeout(120, connect=10)) as client:
                    content = self._request(client, body, call)
            else:
                content = self._request(self._client, body, call)
            envelope = json_object(content)
            choices = envelope.get('choices')
            if not isinstance(choices, list) or len(choices) != 1:
                raise HostedFailure('invalid_choices')
            choice = choices[0]
            if not isinstance(choice, dict) or choice.get('finish_reason') != 'stop':
                raise HostedFailure('incomplete_or_refused')
            message = choice.get('message')
            if (not isinstance(message, dict) or message.get('role') != 'assistant'
                    or message.get('tool_calls') or message.get('function_call') or message.get('refusal')
                    or not isinstance(message.get('content'), str)):
                raise HostedFailure('unsupported_response')
            model = envelope.get('model')
            if not isinstance(model, str) or not 1 <= len(model) <= 180:
                raise HostedFailure('missing_model_identity')
            output = json_object(message['content'])
            usage = envelope.get('usage', {})
            if usage is None:
                usage = {}
            if not isinstance(usage, dict):
                raise HostedFailure('invalid_usage')
            tokens = {key: usage[key] for key in ('prompt_tokens', 'completion_tokens', 'total_tokens') if key in usage}
            if any(type(n) is not int or n < 0 for n in tokens.values()):
                raise HostedFailure('invalid_usage')
            call.update(status='response_received', served_model=model, usage=tokens,
                        response_sha256=_hash(output), finish_reason='stop')
            return output, model
        except HostedFailure as exc:
            call.update(status='failed', error_code=exc.code)
            raise
        except httpx.TimeoutException:
            call.update(status='failed', error_code='timeout')
            raise HostedFailure('timeout') from None
        except httpx.HTTPError:
            call.update(status='failed', error_code='transport_error')
            raise HostedFailure('transport_error') from None
        except (ValueError, TypeError, KeyError, RecursionError):
            call.update(status='failed', error_code='invalid_json')
            raise HostedFailure('invalid_json') from None
        finally:
            call['elapsed_ms'] = round((time.perf_counter() - started) * 1000, 2)

    def _request(self, client, body: bytes, call: dict) -> bytes:
        # Both application and transport authorisation are required. Endpoint is
        # fixed; user/model content cannot turn this into a general HTTP client.
        with client.stream('POST', HF_ENDPOINT, content=body,
                           headers={'Authorization': 'Bearer ' + self._settings.token,
                                    'Content-Type': 'application/json', 'Accept': 'application/json'},
                           follow_redirects=False, timeout=httpx.Timeout(120, connect=10)) as response:
            call['http_status'] = response.status_code
            if response.status_code != 200:
                code = {401: 'authentication_failed', 403: 'permission_denied', 402: 'billing_required',
                        429: 'rate_limited'}.get(response.status_code, 'provider_rejected_request')
                # Deliberately do not store or echo the error body.
                raise HostedFailure(code)
            chunks = []
            size = 0
            for chunk in response.iter_bytes():
                size += len(chunk)
                if size > MAX_RESPONSE_BYTES:
                    raise HostedFailure('response_too_large')
                chunks.append(chunk)
            return b''.join(chunks)
