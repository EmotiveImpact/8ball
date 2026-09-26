import {S,$,esc,icon,field,textarea,select,options,date,badge,button,modal,closeModal,note,warning,toast,saveFile} from './ui.js';
import {sourceDisplayMap,sourceOriginalRange,sourceSelectionCount,addSourcePassage,sourceWirePassages,SOURCE_SELECTION_LIMIT} from './source-model.js';

let sourceContext=null,sourceImportDraft=null,sourceRequestSequence=0;
const sourceUid=()=>crypto.randomUUID?.()??Array.from(crypto.getRandomValues(new Uint8Array(16)),b=>b.toString(16).padStart(2,'0')).join('');
const sourceNumber=n=>Number(n).toLocaleString('en-GB');
const sourceButton=(label,action,attrs='',primary=false)=>`<button type="button" class="button ${primary?'primary':''}" data-source-action="${esc(action)}" ${attrs}>${label}</button>`;
const sourceStamp=()=>({caseId:S.current?.case.id,epoch:S.epoch,revision:S.current?.case.revision});
const sourceStillCurrent=s=>s.caseId===S.current?.case.id&&s.epoch===S.epoch;
const sourceBase=()=>`/cases/${encodeURIComponent(S.current.case.id)}/sources`;
function sourceState(){
  if(!S.sourceDesk||S.sourceDesk.caseId!==S.current?.case.id)S.sourceDesk={caseId:S.current?.case.id,index:null,page:null,selected:[],matches:[],query:'',open:false,loadError:null};
  return S.sourceDesk;
}
export function clearSourceDesk(){sourceRequestSequence++;sourceImportDraft=null;S.sourceDesk=null;}
export function mountSourceReader(){
  const reader=$('#sd-reader');if(reader&&S.sourceDesk?.page)reader.value=sourceDisplayMap(S.sourceDesk.page.text).text;
}
export function sourceOriginButton(evidenceId){return sourceButton('Source origin','origin',`data-id="${esc(evidenceId)}"`);}
export function sourceDeskLauncher(){return sourceButton('Source Desk '+icon('arrow'),'open');}

export function sourceDeskView(){
  const st=sourceState();if(!st.open)return '';
  const docs=st.index?.documents??[],p=st.page,doc=p?.document,selected=st.selected;
  const captured=docs.reduce((n,d)=>n+d.passage_count,0),count=sourceSelectionCount(selected);
  return `<section class="sd-workspace" aria-label="Source Desk"><header class="sd-heading"><div><span class="kicker">EVIDENCE / SOURCE DESK</span><h1>Keep the original. Use what matters.</h1><p>Read, select and trace source material without confusing a document with proof.</p></div><div class="toolbar">${sourceButton('Back to evidence','evidence')}${sourceButton('Import text source','import','',true)}</div></header>
  <div class="sd-summary"><div><strong>${sourceNumber(docs.length)}</strong><span>Stored text originals</span></div><div><strong>${sourceNumber(captured)}</strong><span>Traceable evidence passages</span></div><div><strong>200,000</strong><span>Character limit per original</span></div><div><strong>Human review</strong><span>No automatic analysis or verification</span></div></div>
  ${st.loadError?warning(st.loadError):''}
  <div class="sd-layout"><aside class="sd-library"><header><h2>Source library</h2><span class="badge">${docs.length} record${docs.length===1?'':'s'}</span></header><div class="sd-library-list">${docs.length?docs.map(d=>`<button type="button" class="sd-document ${doc?.id===d.id?'selected':''}" data-source-action="document" data-id="${esc(d.id)}" aria-pressed="${doc?.id===d.id}"><div class="meta"><span class="kicker">TEXT ORIGINAL</span>${badge(d.status,d.status==='retracted'?'Retracted':'Stored')}</div><h3>${esc(d.title)}</h3><p>${esc(d.source)}</p><small>${sourceNumber(d.characters)} characters · ${date(d.created_at)}</small><div class="sd-coverage">${sourceNumber(d.captured_characters)} characters captured as excerpts${d.previous_document_id?' · Linked revision':''}</div></button>`).join(''):`<div class="sd-empty"><span class="empty-symbol">${icon('evidence')}</span><h3>No originals stored yet.</h3><p>Import a UTF-8 text document. Existing evidence remains untouched.</p>${sourceButton('Add first original','import','',true)}</div>`}</div></aside>
  <section class="sd-reading"><header class="sd-reader-head"><div><span class="kicker">${doc?'ORIGINAL TEXT / UNMODIFIED':'DOCUMENT READER'}</span><h2>${esc(doc?.title??'Select a source')}</h2>${doc?`<p>${esc(doc.source)} · ${sourceNumber(doc.characters)} characters</p>`:''}</div>${doc?badge(doc.status,doc.status==='retracted'?'Historical / retracted':'Stored, not verified'):''}</header>
  ${p?`<div class="sd-document-meta"><span class="mono" title="${esc(doc.content_sha256)}">SHA-256 ${esc(doc.content_sha256.slice(0,16))}…</span><small>${esc(doc.filename??'Pasted text')} · Original retained in full</small></div>
  ${doc.previous_document_id?`<div class="sd-version-link">Linked to an earlier source. Neither version is automatically superseded. ${sourceButton('Open earlier original','document',`data-id="${esc(doc.previous_document_id)}"`)}</div>`:''}
  ${doc.status==='retracted'?warning('Retracted source. Existing passages are historical and cannot support live conditions. '+doc.retraction_reason):''}
  ${doc.warnings?.map(w=>warning(w,'neutral')).join('')??''}
  <form class="sd-search" data-source-form="search"><label class="sr-only" for="sd-query">Search original text</label><input id="sd-query" name="query" type="search" required minlength="2" maxlength="200" value="${esc(st.query)}" placeholder="Find a phrase in this original…"><button type="submit" class="button">Find</button></form>
  ${st.matches.length?`<div class="sd-search-results" aria-label="Search results">${st.matches.map(m=>`<button type="button" data-source-action="search-hit" data-start="${m.context_start}" data-end="${m.context_end}"><b>Position ${m.start}</b> ${esc(m.context)}</button>`).join('')}${st.searchTruncated?note('First 50 matches shown. Refine the search.'):''}</div>`:''}
  <div class="sd-passages"><label>Passage <select data-source-select="chunk" aria-label="Choose source passage">${!p.chunks.some(ch=>ch.start===p.start&&ch.end===p.end)?`<option value="${p.start}:${p.end}" selected>Selected span: ${p.start} to ${p.end}</option>`:''}${p.chunks.map(ch=>`<option value="${ch.start}:${ch.end}" ${ch.start===p.start&&ch.end===p.end?'selected':''}>${ch.number}. Lines ${ch.line_start} to ${ch.line_end} · ${sourceNumber(ch.characters)} characters</option>`).join('')}</select></label><span>${sourceNumber(p.start)} to ${sourceNumber(p.end)} of ${sourceNumber(doc.characters)}</span></div>
  <label class="sd-text-label" for="sd-reader">Original text, lines ${p.line_start} to ${p.line_end}. Select text to capture an exact passage.</label><textarea id="sd-reader" class="sd-reader" readonly spellcheck="false" wrap="soft"></textarea>
  <div class="sd-read-controls"><div class="toolbar">${sourceButton('Use selected text','select-text',doc.status==='retracted'?'disabled':'',true)}${sourceButton('Use displayed passage','select-page',doc.status==='retracted'?'disabled':'')}</div><span>${p.partial?'Showing part of the original, not the whole document.':'Showing the full original.'}</span></div>
  <div class="sd-original-actions">${sourceButton('Export original text','export')}${doc.status==='active'?sourceButton('Retract original','retract'):''}</div>`:`<div class="sd-empty"><h3>The original stays separate from the plan.</h3><p>Only passages you deliberately capture become unreviewed evidence. Model analysis is a separate action.</p></div>`}
  </section><aside class="sd-selection"><header><span class="kicker">YOUR REVIEW BATCH</span><h2>Selected passages</h2></header><div class="sd-budget"><strong>${sourceNumber(count)} <small>/ 12,000</small></strong><p>Characters prepared for evidence review. Nothing has been sent to a model.</p></div><div class="sd-cart">${selected.length?selected.map((x,i)=>`<article class="sd-cart-item"><div class="meta"><b>${esc(x.title)}</b><button class="icon-button" data-source-action="remove" data-index="${i}" aria-label="Remove passage ${i+1}">${icon('close')}</button></div><span class="mono">${x.start}:${x.end} · ${sourceNumber(x.end-x.start)} chars</span><p>${esc(Array.from(x.text).slice(0,180).join(''))}${x.end-x.start>180?'…':''}</p></article>`).join(''):`<div class="sd-cart-empty">Select the passages that matter. Their original locations and hashes stay attached.</div>`}</div><div class="sd-cart-footer">${sourceButton('Review selected passages','preview-capture',selected.length?'':'disabled',true)}${sourceButton('Clear selection','clear',selected.length?'':'disabled')}<p class="note">Capture does not verify a fact. Review the source and attest its condition separately.</p></div></aside></div></section>`;
}

export async function refreshSourceDeskIndex(){
  const stamp=sourceStamp(),index=await sourceContext.api(sourceBase());
  if(sourceStillCurrent(stamp)){const st=sourceState();st.index=index;const d=index.documents.find(d=>d.id===st.page?.document.id);if(d)st.page.document={...st.page.document,...d};}
}
async function sourceOpenDocument(documentId,start=0,end=null){
  const stamp=sourceStamp(),seq=++sourceRequestSequence;const st=sourceState();
  let result=await sourceContext.api(sourceBase()+'/'+encodeURIComponent(documentId)+`?start=${start}&limit=${end===null?4000:end-start}`);
  if(!sourceStillCurrent(stamp)||seq!==sourceRequestSequence||S.tab!=='evidence')return;
  const chunk=result.chunks.find(c=>c.start===start);
  if(end===null&&chunk&&chunk.end!==result.end){
    result=await sourceContext.api(sourceBase()+'/'+encodeURIComponent(documentId)+`?start=${start}&limit=${chunk.end-start}`);
  }
  if(!sourceStillCurrent(stamp)||seq!==sourceRequestSequence)return;
  if(S.tab!=='evidence')return;
  st.page=result;st.loadError=null;sourceContext.render();
}
async function sourceOpen(){
  const stamp=sourceStamp();S.tab='evidence';sourceState().open=true;sourceContext.render();
  await refreshSourceDeskIndex();if(!sourceStillCurrent(stamp)||S.tab!=='evidence')return;
  const st=sourceState();sourceContext.render();
  const candidate=st.page?.document.id??st.index?.documents[0]?.id;
  if(candidate)await sourceOpenDocument(candidate,st.page?.start??0,st.page?.end??null);
}
async function sourceAfterWrite(result,stamp){
  if(!sourceStillCurrent(stamp))return;
  S.current=result;S.history=null;S.scenario=null;S.selectedRoutes.clear();
  await sourceContext.refreshCases();if(!sourceStillCurrent(stamp))return;
  const proposals=await sourceContext.api(`/cases/${stamp.caseId}/proposals`);
  if(!sourceStillCurrent(stamp))return;S.proposals=proposals;
  await refreshSourceDeskIndex();if(!sourceStillCurrent(stamp))return;closeModal();sourceContext.render();
}
async function sourceWrite(path,body,stamp){
  if(!sourceStillCurrent(stamp))throw new Error('Case changed. Reopen this source operation.');
  if(S.busy)throw new Error('Another case change is being saved.');
  S.busy=true;document.body.classList.add('is-busy');
  try{return await sourceContext.api(path,body);}
  finally{S.busy=false;document.body.classList.remove('is-busy');}
}
function sourceImportForm(){
  sourceImportDraft={stamp:sourceStamp(),loaded:null,request:null,preview:null,eventId:sourceUid()};
  const docs=sourceState().index?.documents??[];
  modal('Import a text original',`<p class="note">Store the exact text as supplied, then select reviewable passages. Up to 200,000 Unicode characters and 800,000 UTF-8 bytes. No OCR or binary documents in this build.</p><form data-source-form="import-preview"><div class="form-grid">${field('Document title','title','','text','required maxlength="180"')}${field('Source / sender / author','source','','text','required maxlength="180"')}<div class="full">${field('UTF-8 .txt or .md file (optional)','file','','file','accept=".txt,.md,text/plain,text/markdown" data-source-file')}<p class="note" id="sd-file-note">No file loaded. Paste text below or choose a UTF-8 file.</p>${sourceButton('Use pasted text instead','paste-mode')}${textarea('Original text','text','','required maxlength="200000" data-source-paste')}${select('Link to an earlier version (optional)','previous_document_id',[['','No earlier version'],...docs.map(d=>[d.id,d.title])])}</div></div><div class="form-actions"><button class="button primary" type="submit">Check source & duplicates</button></div></form>`,true);
}
function sourceImportReview(){
  const {request,preview}=sourceImportDraft;
  modal('Review this source import',`<span class="kicker">ORIGINAL TEXT / NO CASE FACTS VERIFIED</span><h3>${esc(request.title)}</h3><p class="note">${esc(request.source)} · ${sourceNumber(preview.characters)} characters · ${preview.chunks} passages</p><p class="sd-hash mono">SHA-256 ${esc(preview.content_sha256)}</p>${preview.warnings.map(w=>warning(w,'neutral')).join('')}${preview.duplicates.length?warning('Matching text already exists. It is not automatically merged or silently imported again.')+preview.duplicates.map(d=>`<div class="row"><div><h3>${esc(d.title)}</h3><p>${esc(d.source)} · ${d.kind==='exact_text'?'Exact text match':'Whitespace-normalised candidate, not an identity decision'}</p></div>${badge(d.status)}</div>`).join(''):warning('No exact or whitespace-normalised match in this case. This is not a semantic duplicate check.','neutral')}<form data-source-form="import-commit">${preview.duplicates.length?`<label class="check"><input type="checkbox" name="record_separately" required><span>Record this as a separate source. Keep all previous sources and their attribution.</span></label><div class="spacer"></div>${textarea('Why is this a distinct source?','duplicate_reason','','required maxlength="1000"')}`:''}${request.previous_document_id?note('An earlier version will be linked, not retracted or overwritten.'):''}<p class="note">The full original stays outside model requests. Only separately captured excerpts may later be selected for analysis.</p><div class="form-actions"><button type="submit" class="button primary">Store text original</button></div></form>`,true);
}
async function sourceSelect(all){
  const st=sourceState(),p=st.page;if(!p)return;
  if(p.document.status!=='active')throw new Error('Retracted text is historical and cannot provide new evidence.');
  const reader=$('#sd-reader');const range=all?{start:p.start,end:p.end}:sourceOriginalRange(p.text,p.start,reader.selectionStart,reader.selectionEnd);
  if(range.end-range.start+sourceSelectionCount(st.selected)>SOURCE_SELECTION_LIMIT)throw new Error('Keep this review batch within 12,000 characters.');
  const stamp=sourceStamp();const part=await sourceContext.api(sourceBase()+'/'+p.document.id+'/selection',range);
  if(!sourceStillCurrent(stamp)||S.tab!=='evidence')return;
  st.selected=addSourcePassage(st.selected,{document_id:p.document.id,start:part.start,end:part.end,content_sha256:part.content_sha256,text:part.text,title:p.document.title});
  sourceContext.render();toast('Passage selected. No case change or model request.');
}
async function sourceCapturePreview(){
  const st=sourceState(),stamp=sourceStamp();
  const request={expected_revision:stamp.revision,passages:sourceWirePassages(st.selected)};
  const result=await sourceContext.api(sourceBase()+'/passages/preview',request);
  if(!sourceStillCurrent(stamp))return;
  st.capture={stamp,request,eventId:sourceUid()};
  modal('Capture exact evidence passages',`${warning('Only these passages will be added as unreviewed evidence. No condition becomes true and no AI request is made.','neutral')}${result.passages.map(p=>`<section class="sd-capture-preview"><h3>${esc(p.title)}</h3><p class="note">Original positions ${p.start} to ${p.end} · ${esc(p.source)}</p><pre>${esc(p.text)}</pre>${p.same_text_evidence_ids.length?warning('The same text already appears in another evidence excerpt. This capture preserves its separate source; it will not merge records.'):''}</section>`).join('')}<form data-source-form="capture-commit"><div class="form-actions"><button type="submit" class="button primary">Add ${result.passages.length} unreviewed excerpt${result.passages.length===1?'':'s'}</button></div></form>`,true);
}
async function sourceOrigin(eid){
  const stamp=sourceStamp(),result=await sourceContext.api(sourceBase()+'/origin/'+encodeURIComponent(eid));
  if(!sourceStillCurrent(stamp))return;
  if(!result.linked){modal('Source origin',note(result.notice));return;}
  const d=result.document,p=result.passage;
  modal('Trace this evidence to the original',`${badge(d.status,d.status==='retracted'?'Historical original':'Stored original')}<h3>${esc(d.title)}</h3><p class="note">${esc(d.source)} · Original positions ${p.start} to ${p.end}</p><div class="source-text">${esc(result.text)}</div><p class="sd-hash mono">Original SHA-256 ${esc(d.content_sha256)}</p><p class="note">The excerpt and its original-text span match. A matching hash is not proof of the source’s truth.</p><div class="form-actions">${sourceButton('Open original at this passage','jump-origin',`data-id="${esc(d.id)}" data-start="${p.start}" data-end="${p.end}"`,true)}</div>`,true);
}
async function sourceAction(action,el){
  const st=sourceState();
  if(action==='open'){await sourceOpen();return;}
  if(action==='evidence'){st.open=false;sourceContext.render();return;}
  if(action==='import'){const stamp=sourceStamp();await refreshSourceDeskIndex();if(sourceStillCurrent(stamp)&&S.tab==='evidence')sourceImportForm();return;}
  if(action==='paste-mode'){
    if(!sourceImportDraft)return;
    sourceImportDraft.loaded=null;sourceImportDraft.fileError=null;
    const form=document.querySelector('form[data-source-form="import-preview"]');if(!form)return;
    form.elements.file.value='';form.elements.text.value='';form.elements.text.readOnly=false;
    $('#sd-file-note').textContent='Paste the text to store. Browser paste line endings are retained as received.';
    form.elements.text.focus();return;
  }
  if(action==='document'){st.query='';st.matches=[];await sourceOpenDocument(el.dataset.id);return;}
  if(action==='search-hit'){await sourceOpenDocument(st.page.document.id,Number(el.dataset.start),Number(el.dataset.end));return;}
  if(action==='select-text'||action==='select-page'){await sourceSelect(action==='select-page');return;}
  if(action==='clear'){st.selected=[];st.capture=null;sourceContext.render();return;}
  if(action==='remove'){st.selected=st.selected.filter((_,i)=>i!==Number(el.dataset.index));st.capture=null;sourceContext.render();return;}
  if(action==='preview-capture'){await sourceCapturePreview();return;}
  if(action==='origin'){await sourceOrigin(el.dataset.id);return;}
  if(action==='jump-origin'){closeModal();S.tab='evidence';st.open=true;await refreshSourceDeskIndex();await sourceOpenDocument(el.dataset.id,Number(el.dataset.start),Number(el.dataset.end));return;}
  if(action==='retract'){
    const d=st.page.document;st.retraction={stamp:sourceStamp(),id:d.id,eventId:sourceUid()};
    modal('Retract this original and linked excerpts',warning('Every linked evidence excerpt will be retracted in one transaction. Conditions supported only by those excerpts will lose support. Original text and observations remain in the history.')+`<h3>${esc(d.title)}</h3><form data-source-form="retract">${textarea('Reason for retraction','reason','','required maxlength="1000"')}<div class="form-actions"><button type="submit" class="button primary">Confirm source retraction</button></div></form>`);return;
  }
  if(action==='export'){
    const d=st.page.document,stamp=sourceStamp();let text='';
    // Explicit bounded pages. Never claim an exported visible page is the full file.
    for(let start=0;start<d.characters;){const p=await sourceContext.api(sourceBase()+'/'+d.id+`?start=${start}&limit=12000`);if(!sourceStillCurrent(stamp))return;text+=p.text;start=p.end;}
    saveFile('8BALL-original-'+d.id.slice(0,8)+'.txt',text,'text/plain;charset=utf-8');toast('Full stored UTF-8 text exported.');return;
  }
}
async function sourceSubmit(form){
  const fd=new FormData(form),v=Object.fromEntries(fd),st=sourceState();
  if(form.dataset.sourceForm==='import-preview'){
    const draft=sourceImportDraft;if(!draft||!sourceStillCurrent(draft.stamp))throw new Error('Reopen import for the current case.');
    if(draft.fileError)throw new Error(draft.fileError);
    const text=draft.loaded?.text??v.text;
    draft.request={title:v.title,source:v.source,text,filename:draft.loaded?.filename??null,previous_document_id:v.previous_document_id||null,expected_revision:draft.stamp.revision};
    draft.preview=await sourceContext.api(sourceBase()+'/preview',draft.request);
    if(sourceStillCurrent(draft.stamp)&&sourceImportDraft===draft&&form.isConnected)sourceImportReview();return;
  }
  if(form.dataset.sourceForm==='import-commit'){
    const d=sourceImportDraft;if(!d)throw new Error('Review an import first.');
    const result=await sourceWrite(`/cases/${d.stamp.caseId}/sources/import`,{...d.request,event_id:d.eventId,duplicate_policy:fd.has('record_separately')?'record_separately':'reject',duplicate_reason:v.duplicate_reason??''},d.stamp);
    await sourceAfterWrite(result,d.stamp);if(!sourceStillCurrent(d.stamp))return;
    sourceImportDraft=null;sourceState().open=true;S.tab='evidence';await sourceOpenDocument(result.document.id);toast('Original stored unchanged. Select passages for evidence review.');return;
  }
  if(form.dataset.sourceForm==='search'){
    const stamp=sourceStamp(),doc=st.page.document.id,seq=++sourceRequestSequence;
    const result=await sourceContext.api(sourceBase()+'/'+doc+'/search?q='+encodeURIComponent(v.query));
    if(!sourceStillCurrent(stamp)||seq!==sourceRequestSequence||st.page.document.id!==doc)return;
    st.query=v.query;st.matches=result.matches;st.searchTruncated=result.truncated;sourceContext.render();if(!result.matches.length)toast('No literal matches in this original.');return;
  }
  if(form.dataset.sourceForm==='capture-commit'){
    const capture=st.capture;if(!capture)throw new Error('Review the selected passages first.');
    const result=await sourceWrite(`/cases/${capture.stamp.caseId}/sources/passages`,{...capture.request,event_id:capture.eventId},capture.stamp);
    await sourceAfterWrite(result,capture.stamp);if(!sourceStillCurrent(capture.stamp))return;
    st.selected=[];st.capture=null;st.open=false;sourceContext.render();toast('Excerpts added as unreviewed evidence. No facts were attested.');return;
  }
  if(form.dataset.sourceForm==='retract'){
    const r=st.retraction;if(!r)throw new Error('Reopen the retraction review.');
    const result=await sourceWrite(`/cases/${r.stamp.caseId}/sources/${r.id}/retract`,{event_id:r.eventId,expected_revision:r.stamp.revision,reason:v.reason},r.stamp);
    await sourceAfterWrite(result,r.stamp);if(!sourceStillCurrent(r.stamp))return;
    st.selected=st.selected.filter(p=>p.document_id!==r.id);await sourceOpenDocument(r.id);toast('Original and linked evidence retracted. History preserved.');return;
  }
}
export function bindSourceDesk(context){
  sourceContext=context;
  document.addEventListener('click',async e=>{const el=e.target.closest('[data-source-action]');if(!el)return;e.preventDefault();try{await sourceAction(el.dataset.sourceAction,el);}catch(error){toast(error.message,true);}});
  document.addEventListener('change',async e=>{
    try{
      if(e.target.matches('[data-source-select="chunk"]')){const [start,end]=e.target.value.split(':').map(Number);await sourceOpenDocument(sourceState().page.document.id,start,end);}
      if(e.target.matches('[data-source-file]')){
        const f=e.target.files[0],form=e.target.form,draft=sourceImportDraft;
        draft.loaded=null;draft.fileError='The selected file has not been read successfully. Choose a valid UTF-8 file or switch to pasted text.';form.elements.text.value='';form.elements.text.readOnly=false;
        if(!f){draft.fileError=null;return;}
        if(!/\.(txt|md)$/i.test(f.name)||f.size>800000)throw new Error('Choose a UTF-8 .txt or .md file of at most 800,000 bytes.');
        const raw=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(await f.arrayBuffer());
        if(Array.from(raw).length>200000)throw new Error('This original exceeds 200,000 Unicode characters.');
        if(!sourceStillCurrent(draft.stamp)||!form.isConnected||sourceImportDraft!==draft)return;
        draft.loaded={text:raw,filename:f.name};draft.fileError=null;form.elements.text.value=raw;form.elements.text.readOnly=true;
        $('#sd-file-note').textContent=`${f.name}: ${sourceNumber(Array.from(raw).length)} characters. File text and line endings retained; the field is a read-only preview.`;
      }
    }catch(error){toast(error.message,true);}
  });
  document.addEventListener('submit',async e=>{const form=e.target;if(!form.dataset.sourceForm)return;e.preventDefault();const submit=form.querySelector('[type="submit"]');if(submit)submit.disabled=true;try{await sourceSubmit(form);}catch(error){toast(error.message,true);}finally{if(submit?.isConnected)submit.disabled=false;}});
}
