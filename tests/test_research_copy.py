"""Source-copy checks never execute upstream code or contact the network."""
import pytest

from research import sources


@pytest.fixture
def preserved(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, 'ROOT', tmp_path)
    target = tmp_path / 'research/external/owner/project'
    target.mkdir(parents=True)
    (target / '.git').write_text('gitdir: unused-fixture')
    record = {'repository': 'owner/project', 'path': 'research/external/owner/project',
              'url': 'https://github.com/owner/project.git', 'commit': 'a' * 40,
              'omitted_model_files': [], 'nested_submodules': [],
              'license_notices': [], 'lfs_pointer_files': []}
    calls = []

    def git(path, *args):
        calls.append(args)
        if args == ('config', '--get', 'remote.origin.url'):
            return record['url']
        if args == ('remote', 'get-url', 'origin'):
            return 'https://environment-proxy.example/owner/project.git'
        if args == ('rev-parse', '--verify', 'HEAD'):
            return record['commit']
        if args[:2] == ('ls-files', '--stage'):
            return '160000 ' + record['commit'] + ' 0\t' + record['path']
        return ''

    monkeypatch.setattr(sources, 'git', git)
    return record, calls, git


def test_verification_checks_stored_origin_not_environment_url_rewrite(preserved):
    record, calls, _ = preserved
    sources.verify(record)
    assert ('config', '--get', 'remote.origin.url') in calls
    assert ('remote', 'get-url', 'origin') not in calls


def test_population_preserves_pin_with_environment_url_rewrite(preserved):
    record, calls, _ = preserved
    sources.populate(record)
    assert ('config', '--get', 'remote.origin.url') in calls
    assert ('checkout', '--detach', record['commit']) in calls
    assert not any(call[0] == 'fetch' for call in calls)


@pytest.mark.parametrize('action', [sources.populate, sources.verify])
def test_wrong_stored_origin_is_still_rejected(preserved, monkeypatch, action):
    record, _, original = preserved
    def git(path, *args):
        if args == ('config', '--get', 'remote.origin.url'):
            return 'https://elsewhere.example/owner/project.git'
        return original(path, *args)
    monkeypatch.setattr(sources, 'git', git)
    with pytest.raises(ValueError, match='Unexpected origin'):
        action(record)


@pytest.mark.parametrize('path', ['../outside.pt', '/outside.pt', 'bad\nname.pt'])
def test_model_omission_cannot_escape_source_boundary(preserved, path):
    record, _, _ = preserved
    record['omitted_model_files'] = [{'path': path}]
    with pytest.raises(ValueError, match='Invalid model-file omission'):
        sources.checked_repository(record)
