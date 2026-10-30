"""Package command budgets do not bypass failures or trigger retries."""
import subprocess
from types import SimpleNamespace

import pytest

from scripts.build_endstate import run


@pytest.mark.parametrize('timeout', [None, 600])
def test_package_command_budget(monkeypatch, tmp_path, timeout):
    calls = []

    def command(args, **options):
        calls.append((args, options))
        return SimpleNamespace(returncode=0, stdout='verified', stderr='')

    monkeypatch.setattr(subprocess, 'run', command)
    options = {} if timeout is None else {'timeout': timeout}
    assert run(['offline-fixture'], tmp_path, **options) == 'verified'
    assert calls == [(['offline-fixture'], dict(cwd=tmp_path, env=None, text=True,
                    capture_output=True, timeout=120 if timeout is None else timeout))]


@pytest.mark.parametrize('timed_out', [False, True])
def test_package_failure_is_not_retried_or_reported_as_success(monkeypatch, tmp_path, timed_out):
    calls = []

    def command(args, **options):
        calls.append(args)
        if timed_out:
            raise subprocess.TimeoutExpired(args, options['timeout'])
        return SimpleNamespace(returncode=1, stdout='partial result', stderr='failed assertion')

    monkeypatch.setattr(subprocess, 'run', command)
    with pytest.raises(subprocess.TimeoutExpired if timed_out else RuntimeError):
        run(['offline-fixture'], tmp_path, timeout=600)
    assert calls == [['offline-fixture']]
