"""Explicit read-only probe of the configured local Ollama runtime.

Never pulls, loads or executes a model; never enumerates installed model names
back to the browser. An unreachable service does not prove it is uninstalled.
"""
import os
import httpx
from endstate.primitives import utcnow


def local_status(client=None) -> dict:
    model = os.getenv('EIGHTBALL_OLLAMA_MODEL', 'qwen3.5:4b')
    result = {'checked_at': utcnow().isoformat(), 'runtime': 'unreachable',
              'runtime_version': None, 'configured_model': model,
              'model_present': None, 'model_loaded': 'not_checked',
              'inference_performed': False, 'download_started': False,
              'quality_approved': False}
    def read(c, path):
        with c.stream('GET', 'http://127.0.0.1:11434' + path, timeout=2,
                      follow_redirects=False) as response:
            response.raise_for_status()
            buffer = bytearray()
            for chunk in response.iter_bytes():
                buffer.extend(chunk)
                if len(buffer) > 500000:
                    raise ValueError('Runtime metadata too large')
            import json
            value = json.loads(buffer)
            if not isinstance(value, dict):
                raise ValueError('Invalid metadata')
            return value
    def probe(c):
        info = read(c, '/api/version')
        version = info.get('version')
        if not isinstance(version, str) or not 1 <= len(version) <= 80:
            raise ValueError('Invalid version')
        result.update(runtime='running', runtime_version=version)
        tags = read(c, '/api/tags').get('models')
        if not isinstance(tags, list):
            raise ValueError('Invalid model inventory')
        canonical = model if ':' in model else model + ':latest'
        matches = [t for t in tags if isinstance(t, dict)
                   and (t.get('name') == canonical or t.get('model') == canonical)]
        result['model_present'] = bool(matches)
        result['note'] = ('Configured model weights are listed locally. Accuracy and inference have not been tested by this check.'
                          if matches else 'Ollama is running but the configured model is not listed. No download was started.')
    try:
        if client is not None:
            probe(client)
        else:
            with httpx.Client(trust_env=False, follow_redirects=False, timeout=2) as c:
                probe(c)
    except (httpx.HTTPError, ValueError, TypeError, RecursionError):
        result['note'] = ('Ollama is reachable but model inventory could not be verified.'
                          if result['runtime'] == 'running' else
                          'The local Ollama service could not be reached. It may be stopped or not installed.')
    return result
