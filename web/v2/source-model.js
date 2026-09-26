// Pure Source Desk helpers. Preserve original code-point offsets across textarea
// newline normalisation and JavaScript UTF-16 indexing. No case writes here.
export const SOURCE_SELECTION_LIMIT=12000;
export function sourceDisplayMap(raw){
  const chars=Array.from(raw),boundaries=[0];let display='';let position=0;
  for(let i=0;i<chars.length;){
    let c=chars[i],step=1;
    if(c==='\r'){c='\n';if(chars[i+1]==='\n')step=2;}
    display+=c;
    for(let j=1;j<c.length;j++)boundaries[position+j]=null; // Inside a surrogate pair.
    position+=c.length;i+=step;boundaries[position]=i;
  }
  return {text:display,boundaries,originalCharacters:chars.length};
}
export function sourceOriginalRange(raw,base,startUTF16,endUTF16){
  const map=sourceDisplayMap(raw);
  if(!Number.isInteger(base)||base<0||!Number.isInteger(startUTF16)||!Number.isInteger(endUTF16)||
     startUTF16<0||endUTF16<=startUTF16||endUTF16>=map.boundaries.length||
     map.boundaries[startUTF16]===null||map.boundaries[endUTF16]===null){
    throw new Error('Select a complete passage without splitting a Unicode character.');
  }
  return {start:base+map.boundaries[startUTF16],end:base+map.boundaries[endUTF16]};
}
export function sourceSelectionCount(passages){return passages.reduce((n,p)=>n+p.end-p.start,0);}
export function addSourcePassage(passages,candidate){
  if(!Number.isInteger(candidate.start)||!Number.isInteger(candidate.end)||candidate.start<0||candidate.end<=candidate.start)throw new Error('Invalid source selection.');
  if(passages.length>=12)throw new Error('Use no more than 12 passages in a review batch.');
  if(sourceSelectionCount(passages)+candidate.end-candidate.start>SOURCE_SELECTION_LIMIT)throw new Error('Keep this batch within 12,000 characters.');
  if(passages.some(p=>p.document_id===candidate.document_id&&p.start<candidate.end&&candidate.start<p.end))throw new Error('This passage overlaps your current selection.');
  return [...passages,candidate];
}
export function sourceWirePassages(passages){return passages.map(({document_id,start,end,content_sha256})=>({document_id,start,end,content_sha256}));}
