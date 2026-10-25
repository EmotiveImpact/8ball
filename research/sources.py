#!/usr/bin/env python3
"""Verify or populate the pinned research sources using Git only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = Path(__file__).with_name('inventory.json')
ENV = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1', GIT_TERMINAL_PROMPT='0')


def git(path, *args):
    return subprocess.run(
        ['git', '-c', 'core.hooksPath=/dev/null', '-c', 'filter.lfs.process=',
         '-c', 'filter.lfs.smudge=cat', '-c', 'filter.lfs.required=false', *args],
        cwd=path, env=ENV, check=True, capture_output=True, text=True,
    ).stdout.strip()


def checked_repository(record):
    name, commit = record['repository'], record['commit']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', name):
        raise ValueError('Invalid repository name')
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Invalid pinned commit: ' + name)
    relative = 'research/external/' + name
    url = 'https://github.com/' + name + '.git'
    if record['path'] != relative or record['url'] != url:
        raise ValueError('Unexpected research path or URL: ' + name)
    target = ROOT / relative
    if target.is_symlink() or not target.resolve().is_relative_to(ROOT / 'research/external'):
        raise ValueError('Research path escapes its source boundary: ' + name)
    for omission in record['omitted_model_files']:
        rel = Path(omission['path'])
        if rel.is_absolute() or '..' in rel.parts or '\n' in str(rel):
            raise ValueError('Invalid model-file omission: ' + name)
    return target, url, commit


def populate(record):
    target, url, commit = checked_repository(record)
    if (target / '.git').exists():
        if git(target, 'remote', 'get-url', 'origin') != url:
            raise ValueError('Unexpected origin URL; preserve checkout: ' + str(target))
        if git(target, 'status', '--porcelain=v1', '--untracked-files=all'):
            raise ValueError('Preserve modified checkout before populating: ' + str(target))
        if git(target, 'rev-parse', '--verify', 'HEAD') != commit:
            raise ValueError('Existing checkout has a different pin: ' + str(target))
    else:
        if target.exists() and any(target.iterdir()):
            raise ValueError('Refusing to overwrite existing files: ' + str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        gitdir = Path(git(ROOT, 'rev-parse', '--absolute-git-dir')) / 'modules' / record['path']
        gitdir.parent.mkdir(parents=True, exist_ok=True)
        git(ROOT, 'init', '--quiet', '--separate-git-dir=' + str(gitdir), str(target))
        for key, value in [('remote.origin.url', url), ('remote.origin.promisor', 'true'),
                           ('remote.origin.partialclonefilter', 'blob:none'),
                           ('core.autocrlf', 'false'), ('core.hooksPath', '/dev/null')]:
            git(target, 'config', key, value)
        git(target, 'fetch', '--no-tags', '--depth=1', '--filter=blob:none', 'origin', commit)
    omissions = record['omitted_model_files']
    if omissions:
        gitdir = Path(git(target, 'rev-parse', '--absolute-git-dir'))
        (gitdir / 'info').mkdir(exist_ok=True)
        (gitdir / 'info/sparse-checkout').write_text(
            '/*\n' + ''.join('!/' + row['path'] + '\n' for row in omissions), encoding='utf-8')
        git(target, 'config', 'core.sparseCheckout', 'true')
        git(target, 'config', 'core.sparseCheckoutCone', 'false')
    else:
        # Restore source omitted by an earlier sparse checkout.
        git(target, 'sparse-checkout', 'disable')
    git(target, 'checkout', '--detach', commit)
    git(target, 'read-tree', '-mu', 'HEAD')


def verify(record):
    target, url, commit = checked_repository(record)
    if not (target / '.git').exists():
        raise ValueError('Source checkout is not populated: ' + str(target))
    if git(target, 'rev-parse', '--verify', 'HEAD') != commit:
        raise ValueError('Checkout does not match its pin: ' + str(target))
    if git(target, 'remote', 'get-url', 'origin') != url:
        raise ValueError('Unexpected origin URL: ' + str(target))
    if git(target, 'status', '--porcelain=v1', '--untracked-files=all'):
        raise ValueError('Source checkout has local changes: ' + str(target))
    omitted = {row['path'] for row in record['omitted_model_files']}
    skipped = {row[2:] for row in git(target, 'ls-files', '-t', '-z').split('\0')
               if row.startswith('S ')}
    if skipped != omitted:
        raise ValueError('Unexpected sparse source omissions: ' + str(target))
    nested_paths = {row['path'] for row in record['nested_submodules']}
    for tracked in git(target, 'ls-files', '-z').split('\0'):
        if not tracked or tracked in omitted or tracked in nested_paths:
            continue
        path = target / tracked
        if not path.exists() and not path.is_symlink():
            raise ValueError('Tracked source file is missing: ' + str(path))
    staged = git(ROOT, 'ls-files', '--stage', '--', record['path']).split()
    if len(staged) != 4 or staged[:3] != ['160000', commit, '0']:
        raise ValueError('Parent Gitlink does not match its pin: ' + record['path'])
    for notice in record['license_notices']:
        path = target / notice['path']
        raw = os.readlink(path).encode() if notice['mode'] == '120000' else path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if digest != notice['git_blob']:
            raise ValueError('Changed license/notice: ' + str(target / notice['path']))
    for omission in record['omitted_model_files']:
        if (target / omission['path']).exists():
            raise ValueError('Model file unexpectedly populated: ' + str(target / omission['path']))
    for pointer in record['lfs_pointer_files']:
        path = target / pointer['path']
        with path.open('rb') as stream:
            raw = stream.read(2049)
        digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if len(raw) > 2048 or digest != pointer['git_blob']:
            raise ValueError('LFS payload/pointer differs from source-only inventory: ' + str(path))
    for nested in record['nested_submodules']:
        path = target / nested['path']
        if path.exists() and any(path.iterdir()):
            raise ValueError('Nested submodule unexpectedly initialized: ' + nested['path'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--populate', action='store_true', help='Fetch exact Git pins and copy source only')
    args = parser.parse_args()
    records = json.loads(INVENTORY.read_text(encoding='utf-8'))['repositories']
    for record in records:
        if args.populate:
            populate(record)
        verify(record)
        print(record['repository'] + ' ' + record['commit'] + ' verified')
    print(str(len(records)) + ' pinned source checkouts verified; no upstream code executed')


if __name__ == '__main__':
    main()
