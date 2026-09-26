"""Read-only graph projection/layout tests, executed by Node on the actual module.
These tests do not stand in for browser interaction or model-quality evaluation.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import subprocess

import pytest
from eightball.v2.playbooks import demo_case
from eightball.v2.planner import plan

ROOT=Path(__file__).resolve().parents[1]
MODULE=(ROOT/'web/v2/graph-model.js').as_uri()

CHECKS={
'grid_pins_preserved': "const h={nodes:Array.from({length:130},(_,i)=>({key:'a'+i,label:'Actor '+i})),links:[]};const l=graphLayout(h,'network',{a1:{x:320,y:250}});assert.deepEqual(l.positions.a1,{x:320,y:250});",
'answer_with_retracted_support_needs_review': "c.questions[0].status='answered';c.questions[0].evidence_ids=['e_customer'];c.evidence.find(e=>e.id==='e_customer').status='retracted';assert.equal(graphProject(c,p).index.get('question:q_authority').state,'needs_review');",
'decision_with_retracted_support_needs_review': "c.decisions[0].selected='mediate';c.decisions[0].evidence_ids=['e_customer'];c.evidence.find(e=>e.id==='e_customer').status='retracted';assert.equal(graphProject(c,p).index.get('decision:escalation').state,'needs_review');",
'retracted_provenance_links_are_historical': "c.claims.push({id:'q',statement:'Reported assertion',status:'recorded_claim',provenance:{references:[{evidence_id:'e_customer',start:0,end:2,quote:'We'}]}});c.evidence.find(e=>e.id==='e_customer').status='retracted';assert(graphProject(c,p).links.find(l=>l.to==='claim:q').historical);",
'layout_does_not_mutate_graph_objects': "const before=JSON.stringify(g);graphLayout(g);assert.equal(JSON.stringify(g),before);",

'projection_does_not_mutate_inputs': "const before=JSON.stringify(input);graphProject(c,p);assert.equal(JSON.stringify(input),before);",
'no_fabricated_or_cross_case_nodes': "assert.equal(g.missing.length,0);assert(g.nodes.every(n=>!n.key.includes('othercase')));assert(g.links.every(l=>g.index.has(l.from)&&g.index.has(l.to)));",
'namespaced_identity': "c.actors[0].id='investigate';const h=graphProject(c,p);assert(h.index.has('actor:investigate'));assert(h.index.has('action:investigate'));assert.notEqual(h.index.get('actor:investigate'),h.index.get('action:investigate'));",
'intended_effect_is_not_evidence': "const links=g.links.filter(l=>l.from==='action:direct'&&l.to==='condition:retained');assert.equal(links[0].kind,'intended');assert.equal(links[0].label,'intends true');assert.equal(g.index.get('condition:retained').state,'unknown');",
'negative_guard_is_explicit': "assert(g.links.some(l=>l.from==='condition:refused'&&l.to==='action:staged'&&l.label==='guard: false'));",
'and_or_expressions_not_rewritten': "assert.equal(g.index.get('action:mediated').object.requires.op,'all');assert(g.index.get('action:mediated').object.requires.args.some(x=>x.op==='any'));",
'case_wide_constraint_scope': "c.constraints[0].action_ids=[];const h=graphProject(c,p);assert.equal(h.links.filter(l=>l.from==='constraint:no_speculation').length,c.graph.actions.length);",
'active_evidence_links': "const h=graphVisible(g);assert(h.links.some(l=>l.kind==='observation'));assert(h.links.every(l=>!l.historical));",
'retracted_source_support_is_not_active': "c.evidence[0].status='retracted';const h=graphProject(c,p);assert(h.links.filter(l=>l.from==='evidence:e_preserve'&&l.kind==='observation').every(l=>l.historical));assert(!graphVisible(h).links.some(l=>l.from==='evidence:e_preserve'&&l.kind==='observation'));",
'superseded_observation_retained_as_history': "c.observations.push({...c.observations[0],id:'new-observation',value:false,supersedes:[c.observations[0].id]});const h=graphProject(c,p);const a=h.links.find(l=>l.reference===c.observations[0].id);assert(a.historical);assert(graphVisible(h,{history:true}).links.some(l=>l.reference===a.reference));",
'duplicate_observation_links_preserve_provenance': "c.observations.push({...c.observations[0],id:'independent-attestation',supersedes:[]});const h=graphProject(c,p);assert.equal(h.links.filter(l=>l.from==='evidence:e_preserve'&&l.to==='condition:records').length,2);",
'provenance_is_actual_source_link': "c.claims.push({id:'claim1',statement:'Source assertion',status:'recorded_claim',provenance:{references:[{evidence_id:'e_customer',start:0,end:2,quote:'We'}]}});const h=graphProject(c,p);assert(h.links.some(l=>l.from==='evidence:e_customer'&&l.to==='claim:claim1'&&l.kind==='provenance'));",
'unknown_references_reported_without_fabrication': "c.graph.conditions[0].actor_id='nonexistent';const h=graphProject(c,p);assert.equal(h.missing.length,1);assert(!h.index.has('actor:nonexistent'));",
'local_depth_one': "const focus='actor:coo';const h=graphVisible(g,{scope:'local',selected:focus,depth:1});const allowed=graphNeighbourKeys(graphVisible(g),focus);assert(h.nodes.every(n=>n.key===focus||allowed.has(n.key)));",
'local_depth_two_expands': "const x=graphVisible(g,{scope:'local',selected:'actor:coo',depth:1}),y=graphVisible(g,{scope:'local',selected:'actor:coo',depth:2});assert(y.nodes.length>x.nodes.length);",
'empty_local_selection': "assert.equal(graphVisible(g,{scope:'local',selected:'missing'}).nodes.length,0);",
'case_insensitive_search': "const h=graphVisible(g,{query:'CUSTOMER COO'});assert(h.nodes.some(n=>n.key==='actor:coo'));",
'search_has_no_dangling_edges': "const h=graphVisible(g,{query:'report'}),k=new Set(h.nodes.map(n=>n.key));assert(h.links.every(l=>k.has(l.from)&&k.has(l.to)));",
'filter_types': "const h=graphVisible(g,{kinds:['actor']});assert.equal(h.nodes.length,c.actors.length);assert(h.links.every(l=>l.from.startsWith('actor:')&&l.to.startsWith('actor:')));",
'all_filters_off_is_empty': "assert.equal(graphVisible(g,{kinds:[]}).nodes.length,0);",
'node_count_matches_real_records': "const n=c.actors.length+c.graph.conditions.length+c.graph.actions.length+c.graph.objectives.length+c.evidence.length+c.claims.length+c.events.length+c.decisions.length+c.questions.length+c.constraints.length+c.resources.length;assert.equal(g.nodes.length,n);",
'deterministic_network_positions': "assert.deepEqual(graphLayout(g),graphLayout(g));",
'deterministic_flow_positions': "assert.deepEqual(graphLayout(g,'outcome'),graphLayout(g,'outcome'));",
'finite_bounded_positions': "for(const v of Object.values(graphLayout(g).positions)){assert(Number.isFinite(v.x)&&Number.isFinite(v.y));assert(v.x>=0&&v.x<=1200&&v.y>=0&&v.y<=740);}",
'pinned_position_is_preserved': "const h=graphLayout(g,'network',{'actor:coo':{x:700,y:400}});assert.deepEqual(h.positions['actor:coo'],{x:700,y:400});",
'non_finite_pin_ignored': "const h=graphLayout(g,'network',{'actor:coo':{x:NaN,y:Infinity}});assert(Number.isFinite(h.positions['actor:coo'].x));",
'cycle_safe_outcome_layout': "const h={nodes:[{key:'a',label:'A'},{key:'b',label:'B'}],links:[{from:'a',to:'b',kind:'prerequisite'},{from:'b',to:'a',kind:'intended'}]};const l=graphLayout(h,'outcome');assert.equal(l.positions.a.x,l.positions.b.x);",
'flow_preserves_directed_order': "const h={nodes:[{key:'a',label:'A'},{key:'b',label:'B'},{key:'c',label:'C'}],links:[{from:'a',to:'b',kind:'prerequisite'},{from:'b',to:'c',kind:'intended'}]};const l=graphLayout(h,'outcome');assert(l.positions.a.x<l.positions.b.x&&l.positions.b.x<l.positions.c.x);",
'large_case_bounded_fallback': "const h={nodes:Array.from({length:130},(_,i)=>({key:'a'+i,label:'Actor '+i})),links:[]};assert(graphLayout(h).fallback);assert.equal(Object.keys(graphLayout(h).positions).length,130);",
'empty_layout_valid': "const h=graphLayout({nodes:[],links:[]});assert.equal(Object.keys(h.positions).length,0);",
'new_case_does_not_reuse_previous_nodes': "const c2=structuredClone(c);c2.id='othercase';c2.actors=[];c2.relationships=[];const h=graphProject(c2,p);assert(!h.nodes.some(n=>n.kind==='actor'));assert.equal(h.caseId,'othercase');",
'label_text_retained_not_interpreted': "c.actors[0].name='<script>window.injected=1</script>';const h=graphProject(c,p);assert.equal(h.index.get('actor:'+c.actors[0].id).label,c.actors[0].name);",
}

@pytest.mark.parametrize('name',list(CHECKS))
def test_graph_model(name):
    assert shutil.which('node'), 'Node is required for graph module validation'
    c=demo_case(datetime(2026,9,23,12,tzinfo=timezone.utc))
    data={'case':c.model_dump(mode='json'),'plan':plan(c,datetime(2026,9,23,12,tzinfo=timezone.utc))}
    code=f"import assert from 'node:assert/strict';import fs from 'node:fs';import {{graphProject,graphVisible,graphLayout,graphNeighbourKeys}} from {json.dumps(MODULE)};const input=JSON.parse(fs.readFileSync(0,'utf8')),c=input.case,p=input.plan,g=graphProject(c,p);"+CHECKS[name]
    result=subprocess.run(['node','--input-type=module','-e',code],input=json.dumps(data),capture_output=True,text=True,timeout=15)
    assert result.returncode==0,result.stderr
