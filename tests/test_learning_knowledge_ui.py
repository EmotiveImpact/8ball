"""Node/fake-DOM component checks only; not native accessibility acceptance."""
from pathlib import Path
import shutil
import subprocess

import pytest


MODULE = (Path(__file__).resolve().parents[1] / 'web/v2/intelligence-knowledge.js').as_uri()
HARNESS = r'''
import assert from 'node:assert/strict';
import {mountKnowledge} from 'MODULE';
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.listeners = {}; this.attributes = {}; this.value = ''; this.classList = {add(){}, remove(){}}; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(key, value) { this.attributes[key] = value; }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  reportValidity() { return true; }
  focus() { this.focused = true; }
}
globalThis.document = {createElement: tag => new Element(tag)};
const root = new Element('main');
const flatten = el => [el, ...el.children.flatMap(flatten)];
const find = (tag, text) => flatten(root).find(el => el.tag === tag && (text === undefined || el.textContent === text));
const tick = () => new Promise(resolve => setImmediate(resolve));
const preventDefault = () => {};
const item = {item_id:'one', version:2, draft_sha256:'a'.repeat(64), review_status:'unreviewed',
  draft:{title:'<script>source()</script>', kind:'playbook', summary:'Not verified', assumptions:['May not apply'],
  authority_requirements:['Check mandate'], confirmation_criteria:['Direct evidence'], limitations:['Example only'], sources:[], graph:{}}};
const data = {revision:4, case_revision:8, item, history:[], retired:false};
'''.replace('MODULE', MODULE)


CHECKS = {
    'empty_checked_scope_and_access_error': r'''
let fail = false;
mountKnowledge(root, {search: async () => { if(fail) throw Error('not surfaced'); return {items:[]}; }});
await tick(); assert.match(find('p').textContent, /Hypotheses/);
assert(flatten(root).some(el => /not a global negative/.test(el.textContent)));
fail = true; await find('form').listeners.submit({preventDefault});
assert(flatten(root).some(el => /Unable to load/.test(el.textContent)));
''',
    'review_is_exact_explicit_and_never_automatic': r'''
const writes = [];
mountKnowledge(root, {search:async () => ({items:[item]}), read:async () => data, write:async (...args) => writes.push(args)});
await tick(); assert.equal(writes.length, 0);
await find('button', `${item.draft.title} · v2 · unreviewed`).listeners.click();
assert.equal(find('h3').textContent, '<script>source()</script>');
assert(find('h3').focused);
find('select').value = 'needs_changes'; find('textarea').value = 'Missing current authority';
flatten(root).filter(el => el.tag === 'input')[1].value = 'Fictional engineering test';
const reviewForm = flatten(root).filter(el => el.tag === 'form')[1];
await reviewForm.listeners.submit({preventDefault});
assert.equal(writes.length, 1);
assert.deepEqual(writes[0][1].review, {version:2,draft_sha256:'a'.repeat(64),verdict:'needs_changes',rationale:'Missing current authority',specialist_scope:'Fictional engineering test'});
assert.equal(writes[0][1].expected_revision, 4); assert.equal(writes[0][1].expected_case_revision, 8);
assert(!flatten(root).some(el => 'innerHTML' in el));
''',
    'late_response_after_dispose_cannot_render_or_write': r'''
let resolveSearch; let writes = 0;
const dispose = mountKnowledge(root, {search:() => new Promise(resolve => resolveSearch = resolve), write:async () => writes++});
dispose(); resolveSearch({items:[item]}); await tick();
assert.deepEqual(root.children, []); assert.equal(writes, 0);
''',
    'superseded_search_cannot_replace_newer_results': r'''
const pending = [];
mountKnowledge(root, {search:() => new Promise(resolve => pending.push(resolve))});
const newer = find('form').listeners.submit({preventDefault});
pending[1]({items:[]}); await newer;
pending[0]({items:[item]}); await tick();
assert(!find('button', `${item.draft.title} · v2 · unreviewed`));
''',
    'failed_review_is_not_retried_or_claimed_successful': r'''
let writes = 0;
mountKnowledge(root, {search:async () => ({items:[item]}), read:async () => data, write:async () => {writes++; throw Error('409');}});
await tick(); await find('button', `${item.draft.title} · v2 · unreviewed`).listeners.click();
const reviewForm = flatten(root).filter(el => el.tag === 'form')[1];
await reviewForm.listeners.submit({preventDefault}); await tick();
assert.equal(writes, 1); assert(find('button', 'Record review of this version').disabled);
assert(flatten(root).some(el => /not confirmed/.test(el.textContent)));
''',
    'retired_reference_has_no_review_command': r'''
mountKnowledge(root, {search:async () => ({items:[item]}), read:async () => ({...data,retired:true})});
await tick(); await find('button', `${item.draft.title} · v2 · unreviewed`).listeners.click();
assert(!find('button', 'Record review of this version'));
''',
}


@pytest.mark.parametrize('name', CHECKS)
def test_isolated_knowledge_component(name):
    node = shutil.which('node')
    if not node:
        pytest.skip('Node required for component contract checks')
    result = subprocess.run([node, '--input-type=module', '-e', HARNESS + CHECKS[name]],
                            capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
