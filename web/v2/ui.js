// All untrusted text goes through esc(). No source/model HTML is interpreted.
export const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const $=s=>document.querySelector(s);
export const pretty=v=>String(v??'').replaceAll('_',' ').replace(/^./,c=>c.toUpperCase());
export const gbp=n=>new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP',maximumFractionDigits:0}).format(n);
export const duration=n=>n===null?'Unspecified':n<60?`${Math.round(n)}m`:`${Number((n/60).toFixed(1))}h`;
export const date=v=>v?new Date(v).toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}):'Not set';
export const localDate=v=>{const d=new Date(v);return new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,16);};
export const badge=(s,label)=>`<span class="badge ${esc(s)}">${esc(label??pretty(s))}</span>`;
export const button=(label,action,primary=false,attrs='')=>`<button type="button" class="button ${primary?'primary':''}" data-action="${esc(action)}" ${attrs}>${label}</button>`;
export const note=text=>`<p class="note">${esc(text)}</p>`;
export const icon=(name)=>{const paths={command:'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z',room:'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18ZM12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z',map:'M5 5l14 1-4 13L5 5Zm0 0v14h10M19 6 5 19',routes:'M4 19V5h6M4 12h10l5 5M10 2l3 3-3 3M16 17h3v-3',evidence:'M6 3h8l4 4v14H6V3Zm8 0v5h4M9 12h6M9 16h6',people:'M16 21v-3c0-4-12-4-12 0v3M10 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM17 4c5 1 5 6 0 7M19 15c2 0 3 2 3 5',actions:'m4 12 5 5L20 6',questions:'M9 8c0-4 7-4 7 0 0 3-4 3-4 6M12 18v1M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Z',decisions:'M4 4h6v6H4zM14 14h6v6h-6zM7 10v7h7M10 7h7v7',changes:'M20 7a9 9 0 1 0 1 8M20 2v5h-5M12 7v5l3 3',timeline:'M5 2v20M5 5h15M5 12h10M5 19h15',review:'M4 3h12v6M4 3v18h12v-7M8 7h4M8 11h3m4 1 2 2 5-6',playbooks:'M3 4h8v17H3zM13 4h8v17h-8zM6 8h2M16 8h2',models:'M8 4h8v16H8zM4 8h4M4 12h4M4 16h4M16 8h4M16 12h4M16 16h4M11 1v3M14 1v3M11 20v3M14 20v3',brief:'M4 4h16v16H4zM8 8h8M8 12h8M8 16h4',settings:'M12 3v18M3 12h18',lock:'M6 10h12v11H6zM8 10V6c0-5 8-5 8 0v4',search:'M10 3a7 7 0 1 0 0 14 7 7 0 0 0 0-14Zm5 12 6 6',plus:'M12 4v16M4 12h16',arrow:'M4 12h16m-6-6 6 6-6 6',close:'m5 5 14 14M19 5 5 19'};return `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${paths[name]??paths.room}"/></svg>`;};
export const S={cases:[],current:null,tab:'command',proposals:[],history:null,plays:[],providers:null,changes:[],map:null,mapView:'outcome',sort:'fewest_unknowns',scenario:null,comparison:null,selectedRoutes:new Set(),busy:false,epoch:0};
export const ctitle=id=>S.current?.case.graph.conditions.find(c=>c.id===id)?.title??id;
export const atitle=id=>S.current?.case.graph.actions.find(a=>a.id===id)?.title??id;
export const actorName=id=>S.current?.case.actors.find(a=>a.id===id)?.name??id;
export const expr=e=>{if(e.op==='atom')return `${e.value?'':'NOT '}${ctitle(e.condition_id)}`;if(!e.args.length)return 'No prerequisites';return `(${e.args.map(expr).join(e.op==='all'?' AND ':' OR ')})`;};
export const field=(label,name,value='',type='text',attrs='')=>`<label class="field"><span>${esc(label)}</span><input name="${esc(name)}" value="${esc(value)}" type="${type}" ${attrs}></label>`;
export const textarea=(label,name,value='',attrs='')=>`<label class="field"><span>${esc(label)}</span><textarea name="${esc(name)}" ${attrs}>${esc(value)}</textarea></label>`;
export const select=(label,name,items,value='',attrs='')=>`<label class="field"><span>${esc(label)}</span><select name="${esc(name)}" ${attrs}>${items.map(([v,t])=>`<option value="${esc(v)}" ${v===value?'selected':''}>${esc(t)}</option>`).join('')}</select></label>`;
export const options=objects=>objects.map(x=>[x.id,x.title??x.name??x.question]);
export const heading=(k,t,p,buttons='')=>`<div class="page-heading"><div><span class="kicker">${esc(k)}</span><h1>${esc(t)}</h1><p>${esc(p)}</p></div><div class="toolbar">${buttons}</div></div>`;
export const empty=(title,text,actions='')=>`<section class="panel empty"><span class="empty-symbol">${icon('room')}</span><h2>${esc(title)}</h2><p>${esc(text)}</p><div class="toolbar">${actions}</div></section>`;
export const warning=(text,tone='')=>`<div class="notice ${esc(tone)}">${esc(text)}</div>`;
export const provenance=p=>p?`${badge('reported',pretty(p.origin))}${p.references?.map(s=>`<blockquote>${esc(s.quote)}<small>${esc(s.evidence_id)} · characters ${s.start}–${s.end}</small></blockquote>`).join('')??''}${p.note?note(p.note):''}`:'';
export function saveFile(name,value,type='application/json'){const b=new Blob([type==='application/json'?JSON.stringify(value,null,2):value],{type});const u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
let timer;
export function toast(text,error=false){const el=$('#toast');el.textContent=text;el.className='visible'+(error?' error':'');clearTimeout(timer);timer=setTimeout(()=>el.className='',6500);}
let previousFocus;
export function closeModal(){$('#modal').innerHTML='';$('#app').inert=false;if(previousFocus?.isConnected)previousFocus.focus();}
export function modal(title,body,wide=false){previousFocus=document.activeElement;$('#app').inert=true;$('#modal').innerHTML=`<div class="backdrop"><section class="dialog ${wide?'wide':''}" role="dialog" aria-modal="true" aria-label="${esc(title)}"><header><h2>${esc(title)}</h2><button type="button" data-action="close" class="icon-button" aria-label="Close dialog">${icon('close')}</button></header><div class="dialog-body">${body}</div></section></div>`;setTimeout(()=>$('.dialog input,.dialog select,.dialog textarea,.dialog button')?.focus(),0);}
