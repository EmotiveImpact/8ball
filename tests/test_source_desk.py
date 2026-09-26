"""Original text and source-span integrity. No model inference in these tests."""
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import json
import unicodedata

import pytest
from pydantic import ValidationError
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Span
from eightball.v2.commands import Command
from eightball.v2.source_contracts import *
from eightball.v2.source_desk import SourceDesk
from eightball.store import Conflict
from eightball.models import uid,utcnow


@pytest.fixture
def setup(tmp_path):
    store=Store(str(tmp_path/'sources.db'))
    case=store.create(demo_case(),fixture=True)
    return store,SourceDesk(store),case


def request(case,text='The incident is contained.\r\nThe client has NOT accepted.\n',**kwargs):
    return ImportSource(event_id=uid(),expected_revision=case.revision,title='Original report',source='Fictional operator',text=text,**kwargs)


def imported(setup,text=None,**kwargs):
    store,desk,case=setup
    r=request(case,**({'text':text} if text is not None else {}),**kwargs)
    case,delta,doc=desk.import_source(case.id,r)
    return store,desk,case,doc,r


def cap(desk,case,doc,start=0,end=None,event_id=None):
    end=min(doc['characters'],4000) if end is None else end
    page=desk.read(case.id,doc['id'],start,end-start)
    req=CapturePassages(event_id=event_id or uid(),expected_revision=case.revision,
                        passages=[Passage(document_id=doc['id'],start=start,end=end,content_sha256=page['content_sha256'])])
    return desk.capture(case.id,req),req


@pytest.mark.parametrize('text',['text','é e\u0301 🤝 🧑🏾\u200d💻\r\n'*2000,'A'*150001,'\ufeffFirst\rSecond\r\nThird\n','Report\n\n'*24500])
def test_chunks_reconstruct_original_without_normalisation(text):
    parts=chunks(text)
    assert ''.join(text[p['start']:p['end']] for p in parts)==text
    assert parts[0]['start']==0 and parts[-1]['end']==len(text)
    assert all(1<=p['characters']<=CHUNK_SIZE for p in parts)
    assert all(text_hash(text[p['start']:p['end']])==p['content_sha256'] for p in parts)
    assert all(a['end']==b['start'] for a,b in zip(parts,parts[1:]))


def test_crlf_not_split_at_hard_boundary():
    text='a'*(CHUNK_SIZE-1)+'\r\n'+ 'b'*2000
    p=chunks(text)
    assert not any(text[x['end']-1:x['end']+1]=='\r\n' for x in p)
    assert line_starts('a\r\nb\nc\rd')==[0,3,5,7]


@pytest.mark.parametrize('text',['','  \r\n','A'*200001,'\ud800','\x00bad'])
def test_invalid_source_text_rejected(text):
    with pytest.raises(ValidationError):SourceInput(title='Report',source='Test',text=text)


@pytest.mark.parametrize('field,value',[('title',' '),('source','\nno'),('filename','bad\x00.txt')])
def test_invalid_metadata_rejected(field,value):
    data={'title':'Report','source':'Test','text':'Test','filename':'one.txt'};data[field]=value
    with pytest.raises(ValidationError):SourceInput(**data)


def test_comparison_hash_only_normalises_for_candidates():
    a='Name: José\nUnaccepted.';b='Name: Jose\u0301  Unaccepted.'
    assert comparison_hash(a)==comparison_hash(b) and text_hash(a)!=text_hash(b)
    assert comparison_hash('Not accepted')!=comparison_hash('Accepted')


def test_long_original_does_not_enter_case_evidence_or_model_context(setup):
    text='A long source.\n'*10000
    store,desk,c,doc,_=imported(setup,text)
    assert len(c.evidence)==len(setup[2].evidence) and c.observations==setup[2].observations
    assert text not in c.model_dump_json()
    assert text not in json.dumps(store.history(c.id))
    assert store.audit(c.id)['source_documents'][0]['text']==text
    assert store.audit(c.id)['valid']
    assert store.get(c.id).revision==1


def test_preview_read_search_are_read_only_and_not_secretly_complete(setup):
    store,desk,c=setup;r=request(c,'First\n'+'marker\n'*10000)
    before=store.audit(c.id)
    assert desk.preview_import(c.id,ImportPreview(**r.model_dump(exclude={'event_id','duplicate_policy','duplicate_reason'})))['persisted'] is False
    assert store.audit(c.id)==before
    c,_,doc=desk.import_source(c.id,r);before=store.audit(c.id)
    p=desk.read(c.id,doc['id']);assert p['partial'] and p['next_start'] is not None
    found=desk.search(c.id,doc['id'],'marker');assert found['truncated'] and len(found['matches'])==50
    assert store.audit(c.id)==before


def test_unicode_excerpt_lineage_and_composed_quote_offsets(setup):
    text='🤝' * 19 + '\r\nThe client has NOT accepted.\r\n'
    store,desk,c,doc,_=imported(setup,text)
    (c,_,ids),_=cap(desk,c,doc,21,len(text))
    e=c.evidence[-1];assert e.text==text[21:]
    origin=desk.origin(c.id,ids[0]);assert origin['passage']['start']==21
    start=e.text.index('NOT');quote=e.text[start:start+12]
    resolved=desk.resolve_span(c.id,Span(evidence_id=e.id,start=start,end=start+12,quote=quote))
    assert text[resolved['original_start']:resolved['original_end']]==quote
    assert c.evidence[-1].status=='unreviewed' and c.observations==setup[2].observations
    assert store.audit(c.id)['valid']


def test_invalid_quote_never_maps_to_original(setup):
    _,desk,c,doc,_=imported(setup)
    (c,_,ids),_=cap(desk,c,doc)
    with pytest.raises(ValueError):desk.resolve_span(c.id,Span(evidence_id=ids[0],start=0,end=3,quote='BAD'))


def test_legacy_direct_excerpt_has_no_invented_original(setup):
    _,desk,c=setup
    assert desk.origin(c.id,c.evidence[0].id)['linked'] is False


def test_retraction_propagates_and_preserves_text_and_observations(setup):
    store,desk,c,doc,_=imported(setup,'Written continuation agreement accepted.')
    (c,_,ids),_=cap(desk,c,doc)
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='review_evidence',payload={'evidence_id':ids[0],'status':'reviewed'}))
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='observe',payload={'evidence_id':ids[0],'condition_id':'retained','value':True,'rationale':'Fictional confirmation'}))
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='metadata',payload={'status':'closed'}))
    observations=list(c.observations)
    c,d=desk.retract(c.id,doc['id'],RetractSource(event_id=uid(),expected_revision=c.revision,reason='Wrong attachment'))
    assert c.evidence[-1].status=='retracted' and c.status=='active' and c.observations==observations
    assert desk.read(c.id,doc['id'])['text']=='Written continuation agreement accepted.'
    assert store.audit(c.id)['valid']
    with pytest.raises(ValueError):desk.selection(c.id,doc['id'],SourceSelection(start=0,end=10))
    with pytest.raises(ValueError):store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='review_evidence',payload={'evidence_id':ids[0],'status':'reviewed'}))


def test_exact_duplicate_requires_explicit_provenance_choice(setup):
    store,desk,c,doc,_=imported(setup)
    r=request(c)
    with pytest.raises(Conflict):desk.import_source(c.id,r)
    assert store.get(c.id).revision==1
    r=ImportSource(**{**r.model_dump(),'duplicate_policy':'record_separately','duplicate_reason':'Same attachment received independently from another sender'})
    c,_,second=desk.import_source(c.id,r)
    assert second['id']!=doc['id'] and c.revision==2 and store.audit(c.id)['valid']
    assert len(desk.index(c.id)['documents'])==2


def test_whitespace_duplicate_is_labelled_candidate_not_merged(setup):
    _,desk,c,doc,_=imported(setup,'New\r\naccount status.')
    p=desk.preview_import(c.id,ImportPreview(**request(c,'New account  status.').model_dump(exclude={'event_id','duplicate_policy','duplicate_reason'})))
    assert p['duplicates'][0]['kind']=='normalised_whitespace_candidate'
    assert desk.read(c.id,doc['id'])['text']=='New\r\naccount status.'


def test_linked_revision_does_not_retract_or_rewrite_earlier_source(setup):
    store,desk,c,doc,_=imported(setup,'Version one.')
    c,_,other=desk.import_source(c.id,request(c,'Version two.',previous_document_id=doc['id']))
    assert other['previous_document_id']==doc['id']
    assert desk.read(c.id,doc['id'])['document']['status']=='active'
    assert store.audit(c.id)['valid']


def test_import_and_capture_retries_are_idempotent(setup):
    store,desk,c,doc,r=imported(setup)
    again,delta,_=desk.import_source(c.id,r);assert again==c and delta['duplicate']
    (c,_,ids),cr=cap(desk,c,doc)
    again,delta,same=desk.capture(c.id,cr);assert again==c and same==ids and delta['duplicate']
    assert store.audit(c.id)['valid']


def test_reused_event_key_for_different_content_is_rejected(setup):
    store,desk,c,doc,r=imported(setup)
    with pytest.raises(Conflict):desk.import_source(c.id,r.model_copy(update={'text':'Other content'}))
    assert store.get(c.id).revision==1


def test_stale_import_and_selection_leave_case_unchanged(setup):
    store,desk,c,doc,_=imported(setup)
    old=request(setup[2],'Other text')
    with pytest.raises(Conflict):desk.import_source(c.id,old)
    p=desk.read(c.id,doc['id'])
    with pytest.raises(Conflict):desk.capture(c.id,CapturePassages(event_id=uid(),expected_revision=0,passages=[Passage(document_id=doc['id'],start=0,end=p['end'],content_sha256=p['content_sha256'])]))
    assert store.get(c.id)==c


def test_same_passage_not_created_twice(setup):
    store,desk,c,doc,_=imported(setup);(c,_,_),_=cap(desk,c,doc)
    with pytest.raises(Conflict):cap(desk,c,doc)
    assert store.get(c.id)==c


def test_retraction_retry_is_idempotent(setup):
    store,desk,c,doc,_=imported(setup);r=RetractSource(event_id=uid(),expected_revision=c.revision,reason='Wrong version')
    c,_=desk.retract(c.id,doc['id'],r);again,d=desk.retract(c.id,doc['id'],r)
    assert c==again and d['duplicate']


def test_batch_capture_is_atomic_on_bad_later_passage(setup):
    store,desk,c,doc,_=imported(setup,'a'*9000)
    ps=[Passage(document_id=doc['id'],start=0,end=4000,content_sha256=text_hash('a'*4000)),
        Passage(document_id=doc['id'],start=4000,end=8000,content_sha256='f'*64)]
    before=store.audit(c.id)
    with pytest.raises(Conflict):desk.capture(c.id,CapturePassages(event_id=uid(),expected_revision=c.revision,passages=ps))
    assert store.audit(c.id)==before


def test_cross_case_documents_and_sources_rejected(setup):
    store,desk,c,doc,_=imported(setup)
    other=store.create(demo_case(),fixture=True)
    with pytest.raises(KeyError):desk.read(other.id,doc['id'])
    with pytest.raises(KeyError):desk.search(other.id,doc['id'],'incident')
    with pytest.raises(KeyError):desk.import_source(other.id,request(other,'Other content.',previous_document_id=doc['id']))
    p=Passage(document_id=doc['id'],start=0,end=3,content_sha256=text_hash('The'))
    with pytest.raises(KeyError):desk.capture(other.id,CapturePassages(event_id=uid(),expected_revision=0,passages=[p]))


def test_concurrent_import_one_revision_winner(setup):
    store,desk,c=setup
    def write(i):
        try:desk.import_source(c.id,request(c,'Original '+str(i)));return 'ok'
        except Conflict:return 'conflict'
    with ThreadPoolExecutor(max_workers=2) as p:assert sorted(p.map(write,[1,2]))==['conflict','ok']
    assert store.get(c.id).revision==1 and store.audit(c.id)['valid']


def test_wrong_hash_does_not_capture(setup):
    store,desk,c,doc,_=imported(setup)
    with pytest.raises(Conflict):desk.capture(c.id,CapturePassages(event_id=uid(),expected_revision=c.revision,passages=[Passage(document_id=doc['id'],start=0,end=3,content_sha256='0'*64)]))


@pytest.mark.parametrize('start,end',[(0,0),(-1,5),(0,12001),(True,5),(0,'5')])
def test_invalid_selection_ranges(start,end):
    with pytest.raises(ValidationError):SourceSelection(start=start,end=end)


def test_out_of_range_selection_never_silently_truncates(setup):
    _,desk,c,doc,_=imported(setup,'Short')
    with pytest.raises(ValueError):desk.selection(c.id,doc['id'],SourceSelection(start=0,end=6))


def test_overlapping_and_over_budget_batches_rejected():
    def p(s,e):return Passage(document_id='doc',start=s,end=e,content_sha256='0'*64)
    for ps in ([p(0,5000),p(4000,8000)],[p(0,7000),p(7000,14000)],[p(0,2),p(0,2)]):
        with pytest.raises(ValidationError):PassagePreview(expected_revision=0,passages=ps)


def test_source_tampering_is_detected(setup):
    store,desk,c,doc,_=imported(setup)
    with store.connection() as db:db.execute('UPDATE v2_source_documents SET text=? WHERE case_id=?',('tampered',c.id));db.commit()
    assert not store.audit(c.id)['valid']
    with pytest.raises(ValueError):desk.read(c.id,doc['id'])


def test_source_metadata_tampering_is_detected(setup):
    store,desk,c,doc,_=imported(setup)
    with store.connection() as db:
        row=db.execute('SELECT metadata FROM v2_source_documents WHERE case_id=?',(c.id,)).fetchone()
        d=json.loads(row['metadata']);d['title']='Tampered label'
        db.execute('UPDATE v2_source_documents SET metadata=? WHERE case_id=?',(json.dumps(d),c.id));db.commit()
    assert not store.audit(c.id)['valid']


def test_deleted_original_not_ignored_in_audit(setup):
    store,desk,c,doc,_=imported(setup)
    with store.connection() as db:db.execute('DELETE FROM v2_source_documents WHERE case_id=?',(c.id,));db.commit()
    assert not store.audit(c.id)['valid']


def test_deleted_binding_is_detected(setup):
    store,desk,c,doc,_=imported(setup);(c,_,_),_=cap(desk,c,doc)
    with store.connection() as db:db.execute('DELETE FROM v2_source_passages WHERE case_id=?',(c.id,));db.commit()
    assert not store.audit(c.id)['valid']


def test_capture_coverage_is_union_not_count_or_truth(setup):
    _,desk,c,doc,_=imported(setup,'a'*10000)
    (c,_,_),_=cap(desk,c,doc,0,4000)
    (c,_,_),_=cap(desk,c,doc,3000,7000)
    index=desk.index(c.id);d=index['documents'][0]
    assert d['captured_characters']==7000 and d['passage_count']==2
    assert c.evidence[-1].status=='unreviewed'


def test_source_permissions_cannot_be_forged_on_generic_command(setup):
    store,desk,c=setup
    with pytest.raises(ValueError):store.change(c.id,Command(event_id=uid(),expected_revision=0,kind='import_source',payload={}))


def test_full_source_survives_store_restart(setup):
    store,desk,c,doc,_=imported(setup,'Immutable text 👋\r\n')
    restored=Store(store.path)
    assert SourceDesk(restored).read(c.id,doc['id'])['text']=='Immutable text 👋\r\n'
    assert restored.audit(c.id)['valid']


def test_document_limit_is_case_scoped_and_atomic(setup,monkeypatch):
    import eightball.v2.source_desk as module
    monkeypatch.setattr(module,'MAX_DOCUMENTS',1)
    store,desk,c,doc,_=imported(setup)
    with pytest.raises(ValueError,match='document limit'):desk.import_source(c.id,request(c,'A different original'))
    assert len(desk.index(c.id)['documents'])==1 and store.get(c.id).revision==1


def test_total_byte_limit_includes_retracted_originals(setup,monkeypatch):
    import eightball.v2.source_desk as module
    store,desk,c,doc,_=imported(setup,'abcde')
    c,_=desk.retract(c.id,doc['id'],RetractSource(event_id=uid(),expected_revision=c.revision,reason='Test'))
    monkeypatch.setattr(module,'MAX_CASE_SOURCE_BYTES',9)
    with pytest.raises(ValueError,match='storage limit'):desk.import_source(c.id,request(c,'12345'))
    assert len(desk.index(c.id)['documents'])==1


def test_storage_error_rolls_back_all_passage_links_and_evidence(setup):
    import sqlite3
    store,desk,c,doc,_=imported(setup,'a'*8000)
    with store.connection() as db:
        db.executescript("CREATE TRIGGER reject_second BEFORE INSERT ON v2_source_passages WHEN NEW.start_offset > 0 BEGIN SELECT RAISE(ABORT,'fixture failure'); END;")
    before=store.audit(c.id)
    ps=[Passage(document_id=doc['id'],start=s,end=s+4000,content_sha256=text_hash('a'*4000)) for s in (0,4000)]
    with pytest.raises(sqlite3.IntegrityError):desk.capture(c.id,CapturePassages(event_id=uid(),expected_revision=c.revision,passages=ps))
    assert store.audit(c.id)==before


def test_import_invalidates_old_approvals_without_mutating_observations(setup):
    from eightball.v2.contracts import Approval
    store,desk,c=setup
    data=c.model_dump();data['approvals']=[Approval(action_id='preserve',revision=0,expires_at=utcnow()+timedelta(hours=1),actor='local-operator').model_dump()]
    # Build a separately anchored fixture, rather than editing production records.
    from eightball.v2.contracts import Case
    data['id']=uid();c=store.create(Case.model_validate(data),fixture=True)
    observed=list(c.observations)
    updated,_,_=desk.import_source(c.id,request(c,'Fresh source'))
    assert not updated.approvals and updated.observations==observed


def test_source_retraction_flag_cannot_be_silently_rewritten(setup):
    store,desk,c,doc,_=imported(setup)
    c,_=desk.retract(c.id,doc['id'],RetractSource(event_id=uid(),expected_revision=c.revision,reason='Historical'))
    with store.connection() as db:
        db.execute("UPDATE v2_source_documents SET status='active' WHERE case_id=?",(c.id,));db.commit()
    assert not store.audit(c.id)['source_integrity']['valid']


def test_source_identity_tampering_rejected_on_read(setup):
    store,desk,c,doc,_=imported(setup)
    with store.connection() as db:
        row=db.execute('SELECT metadata FROM v2_source_documents WHERE case_id=?',(c.id,)).fetchone()
        d=json.loads(row['metadata']);d['case_id']='another-case'
        db.execute('UPDATE v2_source_documents SET metadata=? WHERE case_id=?',(json.dumps(d),c.id));db.commit()
    with pytest.raises(ValueError,match='identity'):desk.read(c.id,doc['id'])


def test_duplicate_does_not_inherit_retracted_source_status(setup):
    store,desk,c,doc,_=imported(setup,'Repeated record')
    c,_=desk.retract(c.id,doc['id'],RetractSource(event_id=uid(),expected_revision=c.revision,reason='Wrong attribution'))
    c,_,second=desk.import_source(c.id,request(c,'Repeated record',duplicate_policy='record_separately',duplicate_reason='Independently supplied text with separate provenance'))
    assert second['status']=='active' and desk.read(c.id,doc['id'])['document']['status']=='retracted'
    assert store.audit(c.id)['valid']


def test_selection_same_text_from_distinct_documents_preserves_both_origins(setup):
    store,desk,c,doc,_=imported(setup,'Same sentence. Appendix A.')
    c,_,other=desk.import_source(c.id,request(c,'Same sentence. Appendix B.'))
    (c,_,ids1),_=cap(desk,c,doc,0,14)
    (c,_,ids2),_=cap(desk,c,other,0,14)
    assert ids1!=ids2 and desk.origin(c.id,ids1[0])['document']['id']!=desk.origin(c.id,ids2[0])['document']['id']
    assert len(store.audit(c.id)['source_passages'])==2
