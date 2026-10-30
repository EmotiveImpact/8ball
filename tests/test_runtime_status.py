"""Read-only HTTP metadata tests, not model installation or inference."""
import httpx
import pytest

from eightball.v2.runtime_status import local_status


def status(monkeypatch, models, model='fixture:4b'):
    monkeypatch.setenv('EIGHTBALL_OLLAMA_MODEL', model)
    calls = []
    def handle(request):
        calls.append((request.method, request.url.path))
        return httpx.Response(200, json={'version': '0.34.3'} if request.url.path == '/api/version' else {'models': models})
    with httpx.Client(transport=httpx.MockTransport(handle)) as client:
        result = local_status(client)
    assert calls == [('GET', '/api/version'), ('GET', '/api/tags')]
    assert result['model_loaded'] == 'not_checked'
    assert not result['inference_performed'] and not result['download_started']
    return result


def test_selected_weights_only_from_exact_matched_inventory(monkeypatch):
    result = status(monkeypatch, [{'name': 'other:4b', 'digest': 'b' * 64},
        {'name': 'fixture:4b', 'digest': 'a' * 64, 'size': 4096,
         'details': {'format': 'gguf', 'family': 'qwen', 'parameter_size': '4B',
                     'quantization_level': 'Q4_K_M', 'secret_detail': 'omit'}}])
    assert result['inventory_verified'] and result['model_present'] is True
    assert result['selected_weights'] == dict(digest='a' * 64, size_bytes=4096,
        format='gguf', family='qwen', parameter_size='4B', quantization_level='Q4_K_M')
    assert 'other' not in str(result) and 'secret_detail' not in str(result)
    assert not result['quality_approved']


@pytest.mark.parametrize('models', [None, {}, [None], [{}], [{'name': ''}],
    [{'name': 'fixture:4b'}, {'name': 'fixture:4b', 'digest': 'b' * 64}]])
def test_invalid_or_ambiguous_inventory_is_unknown_not_absent(monkeypatch, models):
    result = status(monkeypatch, models)
    assert result['runtime'] == 'running'
    assert result['model_present'] is None and not result['inventory_verified']
    assert result['selected_weights'] is None


def test_missing_metadata_never_invents_digest_version_or_weight_size(monkeypatch):
    result = status(monkeypatch, [{'name': 'fixture:4b', 'digest': 'not-a-digest', 'size': True}])
    assert result['model_present'] is True and result['selected_weights'] is None


def test_registry_port_is_not_mistaken_for_an_explicit_model_tag(monkeypatch):
    result = status(monkeypatch, [{'name': 'registry:5000/team/fixture:latest'}], 'registry:5000/team/fixture')
    assert result['model_present'] is True


def test_empty_complete_inventory_can_establish_absence_without_download(monkeypatch):
    result = status(monkeypatch, [])
    assert result['inventory_verified'] and result['model_present'] is False
