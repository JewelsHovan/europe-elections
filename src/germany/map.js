(() => {
'use strict';
const D=JSON.parse(document.getElementById('elec-data').textContent), G=JSON.parse(document.getElementById('geo-data').textContent);
const P=D.parties, rows=D.rows, byId=Object.fromEntries(rows.map(d=>[d.c,d]));
const COLORS={Union:'#373f54',AfD:'#4654a5',SPD:'#c65856',Greens:'#429273',Left:'#9a6aba',FDP:'#d5a64b',BSW:'#b35d77',SSW:'#55a9ae',Other:'#818793'};
const NS='http://www.w3.org/2000/svg';
const polls={average:D.poll, forsa:{Union:19,AfD:26,SPD:14,Greens:16,Left:12,FDP:4,BSW:3,SSW:.2,Other:5.8}, insa:{Union:19,AfD:29.5,SPD:14.5,Greens:14.5,Left:10,FDP:4,BSW:3.5,SSW:.2,Other:4.8}};
const state={layer:'projection',party:'AfD',poll:'average',afd:27.9,sel:null};
function target(){let q={...polls[state.poll]};const move=state.afd-q.AfD;q.AfD+=move;q.Union-=move;return q}
function model(d,kind,q=target()){
 const source=kind==='f'?d.f:d.s;
 const raw=P.map((p,i)=>{
   if (kind==='f' && (!source[i] || p==='Other')) return source[i];
   return Math.max(0,source[i]+(q[p]-D.base[p]));
 });
 const sum=raw.reduce((a,b)=>a+b,0);
 return raw.map(v=>sum?100*v/sum:0);
}
function winner(a){const order=[...a.keys()].sort((x,y)=>a[y]-a[x]||x-y);return {key:P[order[0]],margin:a[order[0]]-a[order[1]],value:a[order[0]],second:P[order[1]]}}
const pct=x=>x.toFixed(1)+'%',signed=x=>(x>=0?'+':'')+x.toFixed(1);
const color=p=>COLORS[p];
const bin=(v,stops,colors)=>colors[stops.findIndex(s=>v<s)===-1?colors.length-1:stops.findIndex(s=>v<s)];
const L={
 projection:{label:'Projected first-vote lead',desc:'Modelled Erststimme leader from national second-vote polling swings applied to each 2025 local first-vote share. A leader is not necessarily a seat.',color:d=>color(winner(model(d,'f')).key),info:d=>`${winner(model(d,'f')).key} +${pct(winner(model(d,'f')).margin)}`},
 result:{label:'2025 first-vote winner',desc:'Actual 2025 Erststimme pluralities. A plurality did not necessarily become a seat under the second-vote coverage rule.',color:d=>color(d.w),info:d=>`${d.w} +${pct(winner(d.f).margin)}`},
 share:{label:'2025 second-vote share',desc:'Actual 2025 Zweitstimme share for the chosen party. These votes determine proportional representation.',color:d=>bin(d.s[P.indexOf(state.party)],[10,20,30,40],['#e2e6ef','#b3c2d6','#768eae','#49658e','#263f6c']),info:d=>`${state.party} ${pct(d.s[P.indexOf(state.party)])}`},
 change:{label:'Change since 2021',desc:'Actual 2025 minus 2021 Zweitstimme share in points, using the official 2021 vote recast onto 2025 boundaries. BSW had no 2021 comparison.',color:d=>state.party==='BSW'?'#6b7280':bin(d.s[P.indexOf(state.party)]-d.p[P.indexOf(state.party)],[-5,-1,1,5],['#277d73','#91bbb0','#a9adb9','#9c94c6','#6556a2']),info:d=>state.party==='BSW'?'BSW: no 2021 comparison':`${state.party} ${signed(d.s[P.indexOf(state.party)]-d.p[P.indexOf(state.party)])} pts`},
 battle:{label:'Battleground range',desc:'The first-vote winner with AfD 26% versus 29.5% nationally; Union moves inversely and other parties stay at six-poll average. Purple: a different leader across the range.',color:d=>{let lo=winner(model(d,'f',range(26))).key,hi=winner(model(d,'f',range(29.5))).key;return lo===hi?(lo==='AfD'?'#43529b':lo==='Union'?'#4a5467':'#7d9083'):(hi==='AfD'?'#aa79c5':'#dda15a')},info:d=>`${winner(model(d,'f',range(26))).key} at 26% → ${winner(model(d,'f',range(29.5))).key} at 29.5%`}
};
function range(v){let q={...D.poll};q.Union-=v-D.poll.AfD;q.AfD=v;return q}
function legend(){let vals=[];
 if(['projection','result'].includes(state.layer))vals=['Union','AfD','SPD','Greens','Left','FDP','BSW','SSW'].map(p=>[color(p),p]);
 else if(state.layer==='share')vals=[['#e2e6ef','under 10%'],['#b3c2d6','10–20'],['#768eae','20–30'],['#49658e','30–40'],['#263f6c','40+']];
 else if(state.layer==='change')vals=state.party==='BSW'?[['#6b7280','No 2021 BSW comparison']]:[['#277d73','fell 5+ pts'],['#91bbb0','fell 1–5'],['#a9adb9','within 1'],['#9c94c6','rose 1–5'],['#6556a2','rose 5+']];
 else vals=[['#43529b','AfD in both'],['#4a5467','Union in both'],['#7d9083','Other in both'],['#aa79c5','changes to AfD'],['#dda15a','changes to another party']];
 document.getElementById('legend').innerHTML=vals.map(([c,s])=>`<span><i class="sw" style="background:${c}"></i>${s}</span>`).join('');
}
const svg=document.getElementById('map');svg.setAttribute('viewBox',`0 0 ${G.w} ${G.h}`);
const shapes={};
for(const d of rows){const el=document.createElementNS(NS,'path');el.setAttribute('d',G.paths[d.c]);el.setAttribute('class','wk');el.setAttribute('fill-rule','evenodd');el.dataset.c=d.c;const title=document.createElementNS(NS,'title');title.textContent=`${d.c} ${d.n}`;el.append(title);svg.append(el);shapes[d.c]=el}
// Remove the static map only once interactive paths are ready.
for(const el of document.querySelectorAll('.static-only'))el.remove();document.documentElement.classList.add('js');
const layers=document.getElementById('layers');
for(const [k,item] of Object.entries(L)){const btn=document.createElement('button');btn.type='button';btn.textContent=item.label;btn.dataset.layer=k;btn.addEventListener('click',()=>{state.layer=k;render()});layers.append(btn)}
const party=document.getElementById('party');for(const p of P.slice(0,-1)){const opt=document.createElement('option');opt.value=p;opt.textContent=p;party.append(opt)}party.value=state.party;
party.addEventListener('change',()=>{state.party=party.value;render()});
const pick=document.getElementById('pick'),names=document.getElementById('names'),search=document.getElementById('search');
for(const d of [...rows].sort((a,b)=>a.n.localeCompare(b.n,'de'))){const s=`${d.c} ${d.n}`,opt=document.createElement('option');opt.value=d.c;opt.textContent=s;pick.append(opt);const suggestion=document.createElement('option');suggestion.value=s;names.append(suggestion)}
pick.addEventListener('change',()=>select(pick.value||null));
search.addEventListener('change',()=>{const v=search.value.toLowerCase().trim(),match=rows.find(d=>v===d.c||v===`${d.c} ${d.n}`.toLowerCase())||rows.find(d=>v && `${d.c} ${d.n}`.toLowerCase().includes(v));if(match)select(match.c)});
const slider=document.getElementById('nat');slider.addEventListener('input',()=>{state.afd=+slider.value;render()});
for(const btn of document.querySelectorAll('[data-preset]'))btn.addEventListener('click',()=>{state.poll=btn.dataset.preset;state.afd=polls[state.poll].AfD;slider.value=state.afd;state.layer='projection';render()});
const tip=document.getElementById('tip');
svg.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse')return;const c=e.target.closest('path')?.dataset.c;if(!c){tip.hidden=true;return}tip.hidden=false;tip.textContent=`${c} ${byId[c].n}: ${L[state.layer].info(byId[c])}`;const b=document.getElementById('mapwrap').getBoundingClientRect();tip.style.left=Math.max(0,Math.min(e.clientX-b.left+10,b.width-tip.offsetWidth-10))+'px';tip.style.top=(e.clientY-b.top+14)+'px'});
svg.addEventListener('mouseleave',()=>tip.hidden=true);
svg.addEventListener('click',e=>{const c=e.target.closest('path')?.dataset.c;if(c){select(c);if(matchMedia('(max-width:980px)').matches)document.getElementById('panel').scrollIntoView({behavior:'smooth',block:'nearest'})}});
function select(c){state.sel=c;pick.value=c||'';search.value=c?`${c} ${byId[c].n}`:'';for(const [id,el] of Object.entries(shapes))el.classList.toggle('selected',id===c);renderPanel()}
function bar(p,v){return `<div class="pb"><span>${p}</span><span class="pt"><span style="width:${Math.min(100,Math.max(0,v)*2)}%;background:${color(p)}"></span></span><span class="num">${pct(v)}</span></div>`}
function renderPanel(){const el=document.getElementById('panel'),d=byId[state.sel];if(!d){const count={};for(const row of rows){const p=winner(model(row,'f')).key;count[p]=(count[p]||0)+1}el.innerHTML=`<p class="muted">Select a Wahlkreis to compare its 2025 votes with this scenario.</p><h3>First-vote leaders in this model</h3><div class="table-wrap"><table class="compact"><thead><tr><th>Party</th><th class="num">Wahlkreise</th></tr></thead><tbody>${Object.entries(count).sort((a,b)=>b[1]-a[1]).map(([p,n])=>`<tr><td><i class="sw" style="background:${color(p)}"></i>${p}</td><td class="num">${n}</td></tr>`).join('')}</tbody></table></div><p class="small muted">The Bundestag has 630 seats, apportioned principally by the second vote. These counts are not seats.</p>`;return}
 const win25=winner(d.f),project=winner(model(d,'f')),second=winner(d.s),now=model(d,'s');
 el.innerHTML=`<h3>${d.n} <span class="muted">(${d.c})</span></h3><p class="small muted">${D.states[d.r]} · ${d.e.toLocaleString('en')} eligible · ${pct(d.t)} turnout in 2025</p>
 <div class="kv"><span>Projected Erststimme leader at AfD ${pct(state.afd)} nationally</span><strong><i class="sw" style="background:${color(project.key)}"></i>${project.key} ${pct(project.value)}</strong><span class="muted">+${pct(project.margin)} over ${project.second}; modelled, not a seat</span></div>
 <div class="kv"><span>2025 Erststimme winner</span><strong>${win25.key} ${pct(win25.value)}</strong><span class="muted">+${pct(win25.margin)} over ${win25.second}</span></div>
 <div class="kv"><span>2025 Zweitstimme leader</span><strong>${second.key} ${pct(second.value)}</strong><span class="muted">Party votes determine proportional representation</span></div>
 <h4>2025 first vote · candidates by party</h4>${P.filter((p,i)=>d.f[i]>0).map(p=>bar(p,d.f[P.indexOf(p)])).join('')}
 <h4>2025 second vote · party lists</h4>${P.map(p=>bar(p,d.s[P.indexOf(p)])).join('')}
 <h4>2021 second vote · recast on 2025 boundaries</h4>${P.filter((p,i)=>d.p[i]>0).map(p=>bar(p,d.p[P.indexOf(p)])).join('')}
 <h4>Second-vote model</h4>${P.map(p=>bar(p,now[P.indexOf(p)])).join('')}
 <p class="small muted">“Other” groups minor parties and any independent first-vote candidates. A missing 2025 local candidate stays absent in this model. 2021 BSW did not exist.</p><button id="clear" type="button">Clear selection</button>`;
 document.getElementById('clear').addEventListener('click',()=>select(null));
}
function regions(){const q=target(),groups={};for(const d of rows)(groups[d.r]??=[]).push(d);
 document.getElementById('regions-body').innerHTML=Object.entries(D.states).sort((a,b)=>a[1].localeCompare(b[1],'de')).map(([code,name])=>{const ds=groups[code],votes=ds.reduce((a,d)=>a+d.v,0),avg=(f)=>ds.reduce((a,d)=>a+d.v*f(d),0)/votes,old=avg(d=>d.s[1]),proj=avg(d=>model(d,'s',q)[1]),count={};for(const d of ds){const w=winner(model(d,'f',q)).key;count[w]=(count[w]||0)+1}const other=Object.entries(count).filter(([p])=>p!=='AfD').sort((a,b)=>b[1]-a[1]).map(([p,n])=>`${p} ${n}`).join(', ');return `<tr><td>${name}</td><td class="num">${ds.length}</td><td class="num">${pct(old)}</td><td class="num">${pct(proj)}</td><td class="num"><strong>${count.AfD||0}</strong></td><td class="small">${other||'—'}</td></tr>`}).join('');
 document.getElementById('regions-scen').textContent=`AfD ${pct(state.afd)}, Union ${pct(q.Union)} nationally`;
}
function render(){const q=target();for(const d of rows)shapes[d.c].setAttribute('fill',L[state.layer].color(d));
 for(const btn of layers.children)btn.setAttribute('aria-pressed',btn.dataset.layer===state.layer?'true':'false');
 for(const btn of document.querySelectorAll('[data-preset]'))btn.setAttribute('aria-pressed',state.poll===btn.dataset.preset&&state.afd===polls[state.poll].AfD?'true':'false');
 document.getElementById('nat-out').textContent=pct(state.afd);document.getElementById('union-out').textContent=`Union ${pct(q.Union)}`;
 document.getElementById('scenario-controls').classList.toggle('dim',!['projection','battle'].includes(state.layer));
 document.getElementById('layer-desc').textContent=L[state.layer].desc;legend();renderPanel();regions();
}
const swings=rows.filter(d=>winner(model(d,'f',range(26))).key!==winner(model(d,'f',range(29.5))).key);
document.getElementById('swing-count').textContent=`${swings.length} of 299 first-vote leaders differ between those endpoints (mostly Union-to-AfD in the model).`;
render();
})();
