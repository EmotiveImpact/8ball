"""Controlled reproductions of the October security findings; no live providers."""
import json
from types import SimpleNamespace
from urllib.parse import quote

import httpx
import ntpath
import pytest
from fastapi.testclient import TestClient
from starlette import staticfiles

from eightball.api import make_app
from eightball.commands import Command
from eightball.providers import ProviderUnavailable, jev_classify, ollama_extract
from eightball.store import Store as LegacyStore
from eightball.v2.intelligence import ollama_json
from eightball.v2.store import Store


@pytest.mark.parametrize('prefix', ['/', '/v2/'])
@pytest.mark.parametrize('method', ['GET', 'HEAD'])
@pytest.mark.parametrize('path', [
    r'\\attacker.invalid\share\file.txt', r'\??\UNC\attacker.invalid\share\file.txt',
    r'\\?\UNC\attacker.invalid\share\file.txt', r'//attacker.invalid\share/file.txt',
    'C:/Windows/file.txt', 'prefix/C:/Windows/file.txt', 'Z:asset.txt',
])
def test_unsafe_static_urls_never_reach_windows_resolution(tmp_path, monkeypatch, prefix, method, path):
    app = make_app(LegacyStore(str(tmp_path/'case.db')), 'fixture-token-'+'x'*32)
    resolved = []
    def fail_resolution(path):
        resolved.append(str(path))
        raise AssertionError('Untrusted path reached filesystem resolution')
    # Only the static module sees Windows path operations; no SMB or OS change.
    path_ops = SimpleNamespace(normpath=ntpath.normpath, join=ntpath.join,
                               realpath=fail_resolution, abspath=ntpath.abspath,
                               commonpath=ntpath.commonpath)
    monkeypatch.setattr(staticfiles, 'os', SimpleNamespace(path=path_ops, stat=staticfiles.os.stat))
    response = TestClient(app).request(method, prefix+quote(path, safe='/'))
    assert response.status_code == 404
    assert not resolved


def test_static_controls_remain_available_and_contained(tmp_path):
    from pathlib import Path
    app = make_app(LegacyStore(str(tmp_path/'case.db')), 'fixture-token-'+'x'*32)
    client = TestClient(app)
    for path in ('/', '/app.js', '/v2/', '/v2/app.js', '/v2/ui.js'):
        response = client.get(path)
        assert response.status_code == 200
        assert "frame-ancestors 'none'" in response.headers['content-security-policy']
        assert response.headers['cache-control'] == 'no-store'
        assert client.head(path).status_code == 200
    assert client.get('/v2', follow_redirects=False).status_code in (301, 307)
    assert client.get('/v2/%2e%2e/%2e%2e/requirements.txt').status_code == 404
    assert client.get('/v2/%255c%255cattacker.invalid/share/file.txt').status_code == 404
    # A normal nested URL remains valid; escaping symlinks remain denied.
    assets = tmp_path/'assets'
    (assets/'nested').mkdir(parents=True)
    (assets/'nested'/'control.txt').write_text('control')
    outside = tmp_path/'outside.txt'
    outside.write_text('not public')
    (assets/'escape.txt').symlink_to(outside)
    static = next(route.app for route in app.routes if getattr(route, 'name', None) == 'v2-web')
    static.directory = Path(assets)
    static.all_directories = [str(assets)]
    assert client.get('/v2/nested/control.txt').text == 'control'
    assert client.get('/v2/escape.txt').status_code == 404


class Chunks(httpx.SyncByteStream):
    def __init__(self, chunks):
        self.chunks, self.consumed, self.closed = chunks, 0, False
    def __iter__(self):
        for chunk in self.chunks:
            self.consumed += 1
            yield chunk
    def close(self):
        self.closed = True


def invoke(provider, client):
    if provider == 'jev':
        return jev_classify('Fictional source', allow_external=True, client=client)
    if provider == 'legacy':
        return ollama_extract('Fictional source', [{'id':'source'}], client=client)
    return ollama_json({}, 'Fixture only', {}, client=client)


@pytest.mark.parametrize('provider,limit', [('jev', 200_000), ('legacy', 200_000), ('v2', 500_000)])
@pytest.mark.parametrize('headers', [{}, {'content-length':'1'}])
def test_provider_aborts_oversized_stream_before_consuming_tail(monkeypatch, provider, limit, headers):
    monkeypatch.setenv('TYPESAFE_API_KEY', 'fixture-only')
    stream = Chunks([b'x'*limit, b'x', b'never consume this'])
    with httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200, headers=headers, stream=stream))) as client:
        with pytest.raises(ProviderUnavailable):
            invoke(provider, client)
    assert stream.closed and stream.consumed == 2


@pytest.mark.parametrize('provider', ['jev', 'legacy', 'v2'])
def test_provider_error_status_does_not_read_error_body(monkeypatch, provider):
    monkeypatch.setenv('TYPESAFE_API_KEY', 'fixture-only')
    stream = Chunks([b'private error body']*100)
    with httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(503, stream=stream))) as client:
        with pytest.raises(ProviderUnavailable) as exc:
            invoke(provider, client)
    assert stream.closed and stream.consumed == 0
    assert 'private error body' not in str(exc.value)


@pytest.mark.parametrize('provider,limit', [('legacy', 200_000), ('v2', 500_000)])
def test_exact_provider_limit_and_multibyte_content_are_preserved(provider, limit):
    envelope = {'message':{'content':json.dumps({'proposals':[]})}, 'done':True}
    raw = json.dumps(envelope, ensure_ascii=False).encode()
    raw += b' '*(limit-len(raw))
    stream = Chunks([raw[:100], raw[100:]])
    with httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200, stream=stream))) as client:
        assert invoke(provider, client) is not None
    assert stream.closed and stream.consumed == 2
    envelope['message']['content'] = json.dumps({'proposals':[], 'text':'é'}, ensure_ascii=False)
    if provider == 'v2':
        stream = Chunks([json.dumps(envelope, ensure_ascii=False).encode()])
        with httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200, stream=stream))) as client:
            assert invoke(provider, client)[0]['text'] == 'é'


def test_legacy_import_uses_the_same_snapshot_as_its_verified_lineage(tmp_path, monkeypatch):
    legacy = LegacyStore(str(tmp_path/'case.db'))
    store = Store(legacy.path)
    app = make_app(legacy, 'fixture-token-'+'x'*32)
    client = TestClient(app, headers={'Authorization':'Bearer '+'fixture-token-'+'x'*32})
    old = client.post('/api/demo', json={}).json()
    original = legacy.audit
    verified = []
    def audit_then_concurrent_edit(case_id):
        snapshot = original(case_id)
        verified.append(snapshot)
        legacy.change(case_id, Command(event_id='concurrent-budget', expected_revision=snapshot['case']['revision'],
            kind='constraints', payload={'budget':123, 'deadline':snapshot['case']['deadline']}))
        return snapshot
    monkeypatch.setattr(legacy, 'audit', audit_then_concurrent_edit)
    response = client.post('/api/v2/legacy/'+old['id']+'/import', json={})
    assert response.status_code == 200, response.text
    imported = response.json()
    audit = store.audit(imported['id'])
    assert imported['budget'] == verified[0]['case']['budget'] == old['budget']
    assert audit['legacy_lineage'] == verified[0]
    assert audit['valid'] and imported['approvals'] == []
    assert legacy.get(old['id']).budget == 123 and original(old['id'])['valid']
    monkeypatch.setattr(legacy, 'audit', original)
    assert client.post('/api/v2/legacy/'+old['id']+'/import', json={}).json()['id'] == imported['id']


@pytest.mark.parametrize('provider', ['jev', 'legacy', 'v2'])
@pytest.mark.parametrize('encoding', ['gzip', 'deflate', 'gzip, gzip', 'br'])
def test_provider_rejects_compressed_bodies_before_decompression(monkeypatch, provider, encoding):
    import gzip
    monkeypatch.setenv('TYPESAFE_API_KEY', 'fixture-only')
    stream = Chunks([gzip.compress(b'x'*1_000_000)])
    def respond(request):
        assert request.headers['accept-encoding'] == 'identity'
        return httpx.Response(200, headers={'content-encoding':encoding}, stream=stream)
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        with pytest.raises(ProviderUnavailable):invoke(provider, client)
    assert stream.closed and stream.consumed == 0


def test_generation_recorder_preserves_bounded_response_and_failed_reads():
    from evals.live_generation import Recorder
    complete = {'message':{'content':'{"proposals":[]}'}, 'done':True}
    for raw, expected in ((json.dumps(complete).encode(), complete),
                          (b'x'*500001, {'unreadable_response':True})):
        recorder = Recorder()
        recorder.client.close()
        stream = Chunks([raw])
        recorder.client = httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200, stream=stream)))
        try:
            if expected == complete:
                assert invoke('v2', recorder) is not None
            else:
                with pytest.raises(ProviderUnavailable):invoke('v2', recorder)
            assert recorder.responses == [expected] and stream.closed
        finally:recorder.client.close()
