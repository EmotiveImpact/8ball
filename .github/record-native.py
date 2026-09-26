from pathlib import Path
import json

ROOT=Path.cwd()
DATE='2026-09-26'
CODE='14c57907d26ea914e372e544bba4b0bd3988f5dc'
TREE='1560ec43e469953884df6df50206057b903a9c70'
EID='EV-NATIVE-CLOSEOUT'
RECEIPT='docs/evidence/native-closeout-2026-09-26.json'
SESSION='docs/delivery/sessions/2026-09-26-native-acceptance-receipt.md'
RUN='https://github.com/EmotiveImpact/8ball/actions/runs/36219154611'
counts={'legacy':27,'workspace':51,'providers':15,'connections':38,'studio':44,'sources':39,'insights':40,'grounding':26,'plan_review':33,'accessibility':36,'courses':29}
assert sum(counts.values())==378
receipt={
 'date':DATE,'scope':'Cumulative native software acceptance; not complete V0.2 or model quality',
 'code_commit':CODE,'code_tree':TREE,'workflow_run':36219154611,'workflow_url':RUN,
 'artifact_id':10898327762,'artifact_sha256':'abd0d2bdaf269412af328c72e0ef216468ff1c98c4d3b4491ebdbceac3ee870b',
 'report_path':'acceptance/20260926T045349Z-20489cf2/report.json',
 'report_sha256':'95b837a075f9f5a518169eed0057f8e427633603447dd5cf12afee1dde2f8c7b',
 'source_fingerprint':'85564c0b223a33a7c1076e02d1f68c8c1694c702ad865f0cbe865fd3b9ad37e4',
 'artifact_crc_verified':True,'source_and_evidence_inspection_passed':True,
 'code_tests':938,'installed_kernel_tests':938,'native_browser_checks':378,'browser_suites':counts,
 'native_browser':True,'structural_fixtures_passed':8,'model_calls':0,
 'independent_quality_review':False,'human_screen_reader_review':False,
 'full_v02_accepted':False,'merged':False,'deployed':False,
 'scoped_tasks_verified':['B02-13','ES01-05'],
 'limits':['Native Chromium on Linux with real loopback HTTP; not every browser or supported OS.',
 'Provider paths use controlled responses for integration, not actual model quality.',
 'The internal package passes compatibility scope; no public supported SDK release.',
 'Research, new domains and optional feature expansion remain frozen.']}
(ROOT/RECEIPT).write_text(json.dumps(receipt,indent=2)+'\n')
(ROOT/SESSION).write_text(f'''# Native software acceptance receipt

26 September 2026. 8BALL remains 0.2.0-alpha.8; ENDSTATE internal package remains 0.1.0a2.

The Source Desk correction is published at `{CODE}`, exact tree `{TREE}`. [GitHub native run]({RUN}) passed 938 code tests, the same 938 tests against the installed ENDSTATE package, all eleven native browser suites (378 checks), schemas, compilation, JavaScript, generated documents and eight structural fixtures. Artifact 10898327762 was downloaded, its hash verified and the complete source/evidence report inspected against the exact corrected tree. See [receipt](../../evidence/native-closeout-2026-09-26.json).

## Scoped acceptance decisions

B02-13 is verified for guided graph authoring: native Studio checks cover nested rules, false guards, response branches, isolated drafts, preview, explicit commit, stale-state rejection and keyboard escape; broader human accessibility remains B02-16. ES01-05 is verified for the documented internal core compatibility scope: current code and cross-domain fixtures, isolated installed-wheel checks, schemas and all cumulative native app suites pass. This does not release a public SDK or accept V0.2.

B02-10/14 still need professional multi-source identity/date interpretation review. B02-09/11/12 still need genuine provider outputs and independent quality judgement. B02-15 still needs selected-real-provider lifecycle evidence. B02-16 still needs human screen-reader and supported-platform review. B02-19/20 retain visual/accessibility and representative dense-case operator review. Optional insight/course owner acceptance and security/event prerequisites remain unchanged. B02-18 stays blocked.

## Delivery and continuity

The application fix is on the existing development branch. This follow-up only records observed evidence, refreshes misleading local-only status text and closes two supported scopes. Historical failures and changelog entries remain intact. No runtime, test, fixture or required acceptance criterion is changed here. Keep PR #2 draft; no main merge, release tag or deployment. No separate research is adopted. Work from the actual branch rather than stacking old ZIP patches.

## Emergence Review

ER-01 through ER-15 were considered. The concrete lesson remains EM-035/EM-053/EM-051: asynchronous UI state and operator orientation require response-order tests and source-bound evidence. Native execution adds HTTP, browser-policy and real download coverage that the bridge alone could not establish. Green software tests do not supply independent judgement or model accuracy. No new feature or required task is added. All 71 discoveries remain retained; candidates stay visible for later owner review.
''')
p=ROOT/'docs/delivery/progress.json';v=json.loads(p.read_text())
v['updated_on']=DATE
v['repository'].update(inspected_code_commit=CODE,inspected_code_tree=TREE,status_as_of=DATE)
v.pop('unpublished_checkpoint',None)
v['evidence'][EID]={'kind':'native_software_acceptance','path':RECEIPT,'code_commit':CODE,'url':RUN,'result':'938 code and 938 installed-kernel checks; all 11 native Chromium suites pass (378 checks). Artifact and source-bound evidence verified. No actual model, independent professional or human accessibility acceptance.'}
updates={
 'B02-09':(['Actual-model graph generation and semantic quality gate remain unaccepted; this native software run used controlled provider responses.'],'Configure the selected provider and run the unchanged generation fixtures without catalogue substitution or human repair counting as model success.'),
 'B02-10':(['Independent multi-source identity/date usefulness review remains outstanding.','No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed.'],'Evaluate multi-source identity/date workflows with professional fixtures; preserve exact source and preview/apply boundaries.'),
 'B02-11':(['Independent reviewer labels, approved prospective protocol and actual-provider comparison are not completed.'],'Obtain protocol/label approval and run the preserved real-provider gate; native software acceptance is not semantic approval.'),
 'B02-12':(['Full real-provider and genuinely human twenty-step journey remains unperformed; controlled-response native integration is not that journey.'],'Run the actual-provider integration with authorised service/token and collect independent human review.'),
 'B02-13':([], 'Preserve the verified guided-authoring scope; broader human/platform accessibility remains B02-16.'),
 'B02-14':(['Independent multi-source identity/date usefulness review remains outstanding.','No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed.'],'Complete professional source/reconciliation review; keep native original/excerpt/export and request-order regressions.'),
 'B02-15':(['Lifecycle behaviour with the selected real inference provider remains unverified.'],'Verify cancellation, stale results and runtime status with the actual selected provider; never recall already-billed work by implication.'),
 'B02-16':(['Human screen-reader and supported-browser/OS review remains outstanding; Linux/Chromium native software tests passed.'],'Complete the recorded human accessibility and supported-platform review, not another UI feature.'),
 'B02-19':(['Owner visual review and broader human accessibility acceptance remain outstanding.'],'Review the current black workspace without expanding scope; preserve passing native controls.'),
 'B02-20':(['Representative dense-case operator usability and broader accessibility review remain outstanding.'],'Review realistic graph density and operator comprehension; native graph controls/audit invariants now pass.'),
 'ES01-05':([], 'Internal reusable-core compatibility scope verified. Maintain regression coverage; public SDK/commercial release and other platforms remain separate.'),
 'B02-21':(['Operator acceptance remains outstanding; the complete native insight journey now passes.'],'Perform owner/fixer insight review without changing evidence/authority semantics.'),
 'B03-07':(['Secure identity/full mandate and durable event prerequisites remain unaccepted.','Independent operator acceptance remains outstanding; native local workflow passes.'],'Preserve existing local course work; defer remaining optional expansion under the owner freeze.'),
 'ES02-06':(['Original durable event prerequisites remain unaccepted.','Independent operator acceptance remains outstanding; native local workflow passes.'],'Preserve bounded local calculations; defer optional durable-event expansion under the owner freeze.')}
for t in v['tasks']:
 if t['id'] in updates:
  t['blockers'],t['next_action']=updates[t['id']]
  t.update(updated_on=DATE,owner='ChatGPT',working_branch='feat/situation-intelligence-v2',base_commit=CODE)
  if EID not in t['evidence']:t['evidence'].append(EID)
  if t['id'] in ['B02-13','ES01-05']:t['status']='verified'
v['next_task_ids']=['B02-09','B02-10','B02-11','B02-12','B02-15','B02-16','B02-19','B02-20','B02-18']
p.write_text(json.dumps(v,indent=2)+'\n')
p=ROOT/'docs/delivery/changelog.json';v=json.loads(p.read_text())
v['entries'].insert(0,{
 'id':'2026-09-26-native-acceptance-receipt','date':DATE,'version':'0.2.0-alpha.8',
 'title':'Native software acceptance passed; internal core and guided authoring verified','delivery':'local_unreleased',
 'task_ids':['B02-13','B02-14','B02-16','ES01-05','DOC-03','DOC-04','DOC-05'],
 'summary':'Record the published Source Desk correction and completed native evidence. This receipt begins locally and has its own publication record; runtime scope is unchanged.',
 'added':['A source-bound native acceptance receipt and scoped checklist decisions.'],
 'changed':['B02-13 and ES01-05 are verified for their documented software/compatibility scope. Remaining tasks now name actual outstanding model or human review instead of an obsolete unpushed/native blocker.'],
 'fixed':['Current README/status/handoff distinguish published alpha.8 from preserved historical local-only checkpoints.'],
 'verification':['GitHub run 36219154611: 938 code tests and 938 tests against the installed internal ENDSTATE wheel passed.','All eleven native browser suites passed: 378 checks including actual Source Desk original export.','Downloaded artifact hash and all source/evidence hashes verified. No runtime/test change in this receipt.'],
 'limitations':['V0.2 is not accepted. Actual-model quality, professional source review, human accessibility/platform and operator checks remain.','Research is separate; no main merge, release or deployment.'],
 'evidence_paths':[RECEIPT,SESSION],
 'emergence_review':{'discoveries':['Native evidence closes transport-specific gaps but not human judgement; existing EM-035/EM-053/EM-051 remain applicable.'],'risks':['Historical local-only status can mislead the next builder unless current evidence is prominent.'],'architecture_implications':['Keep source, verification, judgement and release states separate.'],'roadmap_decision':'existing_task: close supported software scopes only; preserve required model/human gates and scope freeze.','insight_ids':['EM-035','EM-053','EM-051']}})
p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
current=f'''# Current publication and native acceptance, 26 September 2026

8BALL 0.2.0-alpha.8 is published on `feat/situation-intelligence-v2`. The Source Desk correction at `{CODE}` passed all eleven native browser suites (378 checks), 938 code tests and the same 938 against the installed ENDSTATE package. [Evidence]({RECEIPT}) records exact scope, source and artifact hashes. B02-13 and ES01-05 have met their software acceptance scope; V0.2 has not. Required actual-provider, independent professional, human accessibility/platform and operator reviews remain open. No main merge, deployment or public SDK release. Deferred research remains separate.

Historical local-only text below describes earlier checkpoints, not current publication. Read the canonical checklist and newest handoff before applying any archive.

---

'''
p=ROOT/'STATUS.md';p.write_text(current+'## Historical status records\n\n'+p.read_text())
p=ROOT/'README.md';p.write_text('# 8BALL\n\n'+current.replace('# Current publication','## Current publication',1)+p.read_text().removeprefix('# 8BALL\n\n'))
p=ROOT/'docs/delivery/HANDOFF.md';p.write_text(f'''# Current closeout: published correction and native acceptance

26 September 2026. Work from the current `feat/situation-intelligence-v2` branch, not older cumulative patches. Published runtime correction: `{CODE}`, tree `{TREE}`. Native run 36219154611 passed all eleven suites (378 checks), 938 code tests and 938 installed-kernel tests. Exact artifact/source verification is recorded in `docs/evidence/native-closeout-2026-09-26.json` and `sessions/2026-09-26-native-acceptance-receipt.md`.

B02-13 guided authoring and ES01-05 internal reusable-core compatibility are now verified. V0.2 required count is 10/20; ENDSTATE V0.1 is 5/5 scoped items. These are not time or commercial-readiness percentages. Remaining actual-model, source/professional and human accessibility/operator reviews are explicit in the canonical ledger. This receipt does not perform them.

Keep PR #2 draft and preserve the research hold. No new optional screens, new domain application, main merge, deployment or version tag. This follow-up is documentation only. Historical source/evidence and the original failed native run are retained.

## Emergence Review

The original request-order discoveries are revalidated as EM-035/EM-053/EM-051. Native success is software evidence, not independent human judgement. All 71 discoveries remain retained; no new candidate becomes a required feature.

---

'''+p.read_text())
p=ROOT/'AGENTS.md';p.write_text(p.read_text().replace('It retains **all ten** browser suites.','It retains **all eleven** browser suites, including Chosen Course.'))
p=ROOT/'docs/endstate/PACKAGE.md';p.write_text(p.read_text()+f'''\n## Scoped native compatibility acceptance, 26 September 2026\n\nES01-05 is verified for the internal package compatibility scope at `{CODE}`: all 938 application/code tests against the installed wheel and all eleven native application suites passed. See [native receipt](../evidence/native-closeout-2026-09-26.json). This does not publish a supported SDK, cover untested platforms, approve model quality or release the production product.\n''')
