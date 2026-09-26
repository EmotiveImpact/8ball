"""Execute pure draft-editing tests on the actual JavaScript module."""
from pathlib import Path
import json,subprocess
import pytest
from eightball.v2.playbooks import demo_case

MODULE=(Path(__file__).resolve().parents[1]/'web/v2/studio-model.js').as_uri()
CHECKS={
 'detached_copy': "const before=JSON.stringify(c);studioCreate(d,'conditions','new');assert.equal(JSON.stringify(c),before);assert(studioDirty(d));",
 'unchanged_baseline': "assert.equal(studioDirty(d),false);assert.equal(d.baseRevision,c.revision);",
 'create_defaults_not_verified': "const a=studioCreate(d,'actions','new');assert.equal(a.approval_required,true);assert.equal(a.wait_minutes,null);assert.equal(a.effects.length,0);assert.equal(c.graph.actions.some(x=>x.id==='new'),false);",
 'duplicate_ids_rejected': "assert.throws(()=>studioCreate(d,'conditions','records'));",
 'select_new': "studioCreate(d,'conditions','new');assert.equal(studioSelected(d).id,'new');",
 'undo_redo': "studioCreate(d,'conditions','new');studioHistory(d,'undo');assert(!studioDirty(d));studioHistory(d,'redo');assert(studioDirty(d));assert(d.graph.conditions.some(x=>x.id==='new'));",
 'undo_bounded': "for(let n=0;n<40;n++)studioCreate(d,'conditions','new'+n);assert.equal(d.undo.length,30);",
 'edit_invalidates_preview': "d.preview={ok:true};d.selection={collection:'actions',id:'investigate'};studioChangeField(d,'cost',500);assert.equal(d.preview,null);",
 'undo_invalidates_preview': "studioCreate(d,'conditions','new');d.preview={ok:true};studioHistory(d,'undo');assert.equal(d.preview,null);",
 'no_op_preserves_preview': "d.preview={ok:true};d.selection={collection:'actions',id:'investigate'};studioChangeField(d,'cost',studioSelected(d).cost);assert(d.preview);",
 'redo_cleared_after_edit': "studioCreate(d,'conditions','n');studioHistory(d,'undo');studioCreate(d,'conditions','x');assert.equal(d.redo.length,0);",
 'observed_title_locked': "d.selection={collection:'conditions',id:'records'};assert.throws(()=>studioChangeField(d,'title','new'));",
 'observed_confirmation_locked': "d.selection={collection:'conditions',id:'records'};assert.throws(()=>studioChangeField(d,'confirmation','different'));",
 'observed_date_editable': "d.selection={collection:'conditions',id:'records'};studioChangeField(d,'due_at','2026-09-25T12:00:00Z');assert.equal(studioSelected(d).due_at,'2026-09-25T12:00:00Z');",
 'completed_action_locked': "d.baseCase.completed=['investigate'];d.selection={collection:'actions',id:'investigate'};assert.throws(()=>studioChangeField(d,'cost',1));",
 'referenced_removal_refused': "assert.throws(()=>studioRemove(d,'conditions','records'));",
 'remove_unused_condition': "studioCreate(d,'conditions','unused');studioRemove(d,'conditions','unused');assert(!d.graph.conditions.some(x=>x.id==='unused'));",
 'remove_completed_action_refused': "d.baseCase.completed=['investigate'];assert.throws(()=>studioRemove(d,'actions','investigate'));",
 'false_stays_boolean': "d.selection={collection:'actions',id:'investigate'};studioChangeField(d,'guard',studioAtom('refused'));studioChangeField(d,'guard.value',false);assert.equal(studioSelected(d).guard.value,false);",
 'nested_expression_edit': "d.selection={collection:'actions',id:'investigate'};studioChangeField(d,'requires',{...studioGroup('all'),args:[{...studioGroup('any'),args:[studioAtom('a'),studioAtom('b')]}]});studioChangeField(d,'requires.args.0.args.1.value',false);assert.equal(studioSelected(d).requires.args[0].args[1].value,false);",
 'bad_path_rejected': "assert.throws(()=>studioSet(d.graph,'__proto__.x',true));assert.throws(()=>studioSet(d.graph,'constructor.x',true));assert.equal({}.x,undefined);",
 'missing_path_rejected': "assert.throws(()=>studioSet(d.graph,'actions.999.title','bad'));",
 'different_cases_detached': "const other=createStudioDraft({...c,id:'other'});studioCreate(d,'conditions','private');assert(!other.graph.conditions.some(x=>x.id==='private'));",
 'side_effect_not_observation': "d.selection={collection:'actions',id:'investigate'};studioChangeField(d,'side_effects',['A possible issue']);assert.deepEqual(d.baseCase.observations,c.observations);",
 'unsupported_collection_rejected': "assert.throws(()=>studioCreate(d,'observations','x'));",
}
@pytest.mark.parametrize('name',list(CHECKS))
def test_studio_model(name):
    c=demo_case().model_dump(mode='json')
    code=f"import assert from 'node:assert/strict';import * as m from {json.dumps(MODULE)};const {{createStudioDraft,studioCreate,studioDirty,studioHistory,studioSelected,studioChangeField,studioRemove,studioAtom,studioGroup,studioSet}}=m;const c={json.dumps(c)};const d=createStudioDraft(c);"+CHECKS[name]
    r=subprocess.run(['node','--input-type=module','-e',code],capture_output=True,text=True,timeout=10)
    assert r.returncode==0,r.stderr
