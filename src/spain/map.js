(() => {
const D=JSON.parse(document.getElementById('elec-data').textContent), G=JSON.parse(document.getElementById('geo-data').textContent);
const by=Object.fromEntries(D.map(d=>[d.c,d]));
const national={PP:8160837,PSOE:7821718,Vox:3057000,SUMAR:3044996}, total=24688087;
const presets={private:{PP:32.5,PSOE:26.2,Vox:17.6,SUMAR:6.4,Podemos:3.3,SALF:2.0},cis:{PP:25.5,PSOE:31,Vox:16.6,SUMAR:5.7,Podemos:3.7,SALF:1.8},right:{PP:33.9,PSOE:25.7,Vox:19.2,SUMAR:5.7,Podemos:3.3,SALF:2},actual:{PP:100*national.PP/total,PSOE:100*national.PSOE/total,Vox:100*national.Vox/total,SUMAR:100*national.SUMAR/total,Podemos:0,SALF:0}};
const colors={PP:'#4b94ce',PSOE:'#d54d4a',Vox:'#569d64',SUMAR:'#b668a9',Podemos:'#8257a8',SALF:'#858d5e',ERC:'#dda450',Junts:'#e9c66f','EH Bildu':'#87b09d','EAJ-PNV':'#96af93',BNG:'#8ab2be',CCa:'#e2bd68',UPN:'#74a0d5'};
const col=p=>colors[p]||'#888b94', fmt=v=>v.toFixed(1), esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state={preset:'private',vox:17.6,layer:'actual',selected:'28'};
// Actual D'Hondt: 3% of valid ballots INCLUDING blanks; single-seat African constituencies use plurality.
function award(v,valid,m){
 if(m===1){let winner=Object.keys(v).sort((a,b)=>v[b]-v[a]||a.localeCompare(b))[0];return {[winner]:1};}
 const q=[];for(const [p,n] of Object.entries(v))if(n>=valid*.03)for(let k=1;k<=m;k++)q.push([n/k,p]);
 q.sort((a,b)=>b[0]-a[0]||a[1].localeCompare(b[1]));let s={};for(const [,p] of q.slice(0,m))s[p]=(s[p]||0)+1;return s;
}
function project(d,params=presets[state.preset],vox=state.vox){
 if(params===presets.actual&&Math.abs(vox-presets.actual.Vox)<.001)return {v:d.v,s:d.s,valid:d.valid};
 const v={...d.v};
 for(const p of ['PP','PSOE','Vox','SUMAR'])v[p]=(d.v[p]||0)*(p==='Vox'?vox:params[p])/(100*national[p]/total);
 v.Podemos=(d.v.SUMAR||0)*params.Podemos/(100*national.SUMAR/total);
 v.SALF=(d.v.Vox||0)*params.SALF/(100*national.Vox/total);
 const valid=Object.values(v).reduce((a,b)=>a+b,0)+d.blank;
 return {v,s:award(v,valid,d.m),valid};
}
let calc={}, totals={};
const rank=Object.keys(colors);
function winner(v){return Object.entries(v).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]))[0][0]}
function lastSeat(d,r){
 if(d.m===1){let x=Object.entries(r.v).sort((a,b)=>b[1]-a[1]);return [x[0][0],x[1][0],(x[0][1]-x[1][1])/r.valid*100];}
 let win=[],lose=[];for(const [p,n] of Object.entries(r.v))if(n>=r.valid*.03){let s=r.s[p]||0;if(s)win.push([n/s,p]);lose.push([n/(s+1),p]);}
 win.sort((a,b)=>a[0]-b[0]);lose=lose.filter(x=>x[1]!==win[0][1]);lose.sort((a,b)=>b[0]-a[0]);return [win[0][1],lose[0]?.[1]||'other list',(win[0][0]-(lose[0]?.[0]||0))/r.valid*100];
}
function changes(d){let lo=project(d,presets.private,16),hi=project(d,presets.private,20);let parties=new Set([...Object.keys(lo.s),...Object.keys(hi.s)]);return [...parties].filter(p=>(lo.s[p]||0)!==(hi.s[p]||0)).map(p=>`${p} ${lo.s[p]||0}→${hi.s[p]||0}`).join(', ');}
const layerLabels={proj:'Projected last seat',actual:'2023 winner',share:'2023 party share',shift:'PP change 2019→23',battle:'Battleground seats'};
const svg=document.getElementById('map');svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${G.w} ${G.h}`);
const ns='http://www.w3.org/2000/svg', shapes={};
for(const [c,path] of Object.entries(G.paths)){let el=document.createElementNS(ns,'path');el.setAttribute('d',path);el.setAttribute('class','province');el.dataset.c=c;el.setAttribute('tabindex','0');el.setAttribute('role','button');el.setAttribute('aria-label',by[c].n);svg.append(el);shapes[c]=el;el.addEventListener('click',()=>select(c));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(c)}});}
for(const [text,x,y] of [['Canary Islands (inset)',42,455],['Ceuta',299,507],['Melilla',365,507]]){let t=document.createElementNS(ns,'text');t.setAttribute('x',x);t.setAttribute('y',y);t.setAttribute('class','maplabel');t.textContent=text;svg.append(t);}
const pick=document.getElementById('pick');for(const d of [...D].sort((a,b)=>a.n.localeCompare(b.n)))pick.add(new Option(d.n+' · '+d.m+' seats',d.c));
pick.addEventListener('change',()=>select(pick.value));
function select(c){if(!by[c])return;state.selected=c;pick.value=c;renderPanel();for(const [k,el] of Object.entries(shapes))el.classList.toggle('sel',k===c);}
function refresh(){calc=Object.fromEntries(D.map(d=>[d.c,project(d)]));totals={};for(const r of Object.values(calc))for(const [p,n] of Object.entries(r.s))totals[p]=(totals[p]||0)+n;render();}
function render(){
 const pp=(totals.PP||0)+(totals.Vox||0), left=['PSOE','SUMAR','Podemos','ERC','Junts','EH Bildu','EAJ-PNV','BNG','CCa'].reduce((n,p)=>n+(totals[p]||0),0);
 document.getElementById('seats').innerHTML=`<strong>PP + Vox ${pp}</strong> <span class="muted">/ 176 for a majority</span> · PSOE-led potential support ${left} <span class="muted">(includes Junts, PNV and CCa; not a guaranteed bloc)</span> · Others ${350-pp-left}`;
 document.getElementById('seatbar').innerHTML=`<span style="width:${pp/350*100}%;background:${col('PP')}"></span><span style="width:${left/350*100}%;background:${col('PSOE')}"></span><i style="left:${176/350*100}%" title="176-seat majority line"></i>`;
 document.getElementById('party-seats').textContent=['PP','Vox','PSOE','SUMAR','Podemos','ERC','Junts','EH Bildu','EAJ-PNV','BNG','CCa','UPN','SALF'].filter(p=>totals[p]).map(p=>`${p} ${totals[p]}`).join(' · ');
 const view=document.getElementById('share-party').value;
 for(const d of D){let r=calc[d.c], p=shapes[d.c], v=r.v;let color;
 if(state.layer==='proj'){let [win,lose,margin]=lastSeat(d,r);color= margin<.45?'#d9b97a':col(win);}
 if(state.layer==='actual')color=col(d.w);
 if(state.layer==='share'){let n=100*(d.v[view]||0)/d.valid;color=col(view);p.style.opacity=(.2+Math.min(.8,n/45)).toFixed(2);}
 else p.style.opacity='1';
 if(state.layer==='shift'){let diff=100*(d.v.PP||0)/d.valid-(d.p19.PP||0);color=diff>=10?'#165786':diff>=5?'#448dbd':diff>=0?'#a0c6e2':diff>=-5?'#e4c5a4':'#aa6d59';}
 if(state.layer==='battle')color=changes(d)?'#936bb9':'#464c56';
 p.setAttribute('fill',color);p.setAttribute('aria-label',`${d.n}: ${state.layer==='battle'?(changes(d)||'no change within Vox 16–20%'):state.layer==='share'?view+' '+fmt(100*(d.v[view]||0)/d.valid)+'%':state.layer==='shift'?'PP change '+fmt(100*(d.v.PP||0)/d.valid-(d.p19.PP||0))+' points':state.layer==='actual'?d.w+' leads 2023 by '+fmt((Object.values(d.v).sort((a,b)=>b-a)[0]-Object.values(d.v).sort((a,b)=>b-a)[1])/d.valid*100)+' pts':lastSeat(d,r).slice(0,2).join(' vs ')}`);
 p.querySelector('title')?.remove();let title=document.createElementNS(ns,'title');title.textContent=p.getAttribute('aria-label');p.append(title);
 }
 const legend=document.getElementById('legend');
 legend.innerHTML=state.layer==='battle'?`<span><b class="sw" style="background:#936bb9"></b> Seat allocation changes as Vox moves 16–20%</span><span><b class="sw" style="background:#464c56"></b> No seat changes</span>`:
 state.layer==='shift'?['PP −5 or lower','−5 to 0','0 to +5','+5 to +10','+10 or more'].map((s,i)=>`<span><b class="sw" style="background:${['#aa6d59','#e4c5a4','#a0c6e2','#448dbd','#165786'][i]}"></b>${s} points</span>`).join(''):
 state.layer==='share'?`<span><b class="sw" style="background:${col(view)}"></b> ${view} vote share in 2023; darker = higher</span>`:
 Object.entries(colors).slice(0,13).map(([p,c])=>`<span><b class="sw" style="background:${c}"></b>${p}</span>`).join('')+(state.layer==='proj'?'<span><b class="sw" style="background:#d9b97a"></b>Last-seat gap under 0.45 points of valid vote</span>':'');
 document.getElementById('layer-desc').textContent={proj:'Map colour = party taking the marginal (last allocated) seat; gold = a very small quotient gap. All 350 seats reallocated on every change.',actual:'Party with the most votes in each of the 52 constituencies in July 2023.',share:'Actual 2023 vote share; select a party to change the shading.',shift:'PP share of valid votes in July 2023 minus November 2019; this is not a uniform party-system swing.',battle:'Purple constituencies change at least one seat as Vox ranges from 16% to 20%, with other private-average targets fixed.'}[state.layer];
 document.getElementById('share-party').hidden=state.layer!=='share';
 document.querySelectorAll('#layers button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.layer===state.layer));
 renderPanel();renderRegions();renderBattle();
}
function renderPanel(){let d=by[state.selected],r=calc[d.c];if(!r)return;let v=r.v;let parties=[...new Set([...Object.keys(d.v),...Object.keys(v)])].sort((a,b)=>(v[b]||0)-(v[a]||0));
 let last=lastSeat(d,r), top=Object.entries(d.v).sort((a,b)=>b[1]-a[1]), margin=(top[0][1]-top[1][1])/d.valid*100;
 document.getElementById('panel').innerHTML=`<h3>${esc(d.n)}</h3><div class="muted">${esc(d.r)} · ${d.m} ${d.m===1?'seat':'seats'} · valid ballots in 2023: ${d.valid.toLocaleString('en-GB')}</div><p class="panel-note"><strong>2023 winner:</strong> ${esc(top[0][0])} by ${fmt(margin)} pts over ${esc(top[1][0])}.<br><strong>2023 seats:</strong> ${Object.entries(d.s).map(([p,n])=>esc(p)+' '+n).join(' · ')}<br><strong>Scenario:</strong> ${Object.entries(r.s).map(([p,n])=>esc(p)+' '+n).join(' · ')}<br><strong>Last seat:</strong> ${esc(last[0])} over ${esc(last[1])}, quotient gap ≈ ${fmt(last[2])} pts of valid votes.</p><h4>Votes by list</h4><div class="table-wrap"><table class="compact"><thead><tr><th>Party</th><th class="num">2023 votes</th><th class="num">2023 %</th><th class="num">Projected %</th><th class="num">Seats</th></tr></thead><tbody>${parties.map(p=>`<tr><td><b class="sw" style="background:${col(p)}"></b>${esc(p)}</td><td class="num">${(d.v[p]||0).toLocaleString('en-GB')}</td><td class="num">${fmt(100*(d.v[p]||0)/d.valid)}</td><td class="num">${fmt(100*(v[p]||0)/r.valid)}</td><td class="num">${r.s[p]||'—'}</td></tr>`).join('')}</tbody></table></div><p class="small muted">PP share changed ${fmt(100*(d.v.PP||0)/d.valid-d.p19.PP)} pts since Nov 2019. ${changes(d)?'Vox 16–20% seat changes: '+esc(changes(d))+'.':'No seat changes in the Vox 16–20% test.'}</p>`;}
function renderRegions(){let grouped={};for(const d of D){let g=grouped[d.r]||(grouped[d.r]={m:0,pp:0,left:0,other:0,oldPP:0,oldPSOE:0});let s=calc[d.c].s;g.m+=d.m;g.pp+=(s.PP||0)+(s.Vox||0);g.left+=['PSOE','SUMAR','Podemos','ERC','Junts','EH Bildu','EAJ-PNV','BNG','CCa'].reduce((a,p)=>a+(s[p]||0),0);g.oldPP+=d.s.PP||0;g.oldPSOE+=d.s.PSOE||0;}
 document.getElementById('regions-body').innerHTML=Object.entries(grouped).sort((a,b)=>b[1].m-a[1].m).map(([name,g])=>`<tr><td>${esc(name)}</td><td class="num">${g.m}</td><td class="num">${g.oldPP} / ${g.oldPSOE}</td><td class="num">${g.pp}</td><td class="num">${g.left}</td><td class="num">${g.m-g.pp-g.left}</td></tr>`).join('');}
function renderBattle(){let arr=D.map(d=>({d,last:lastSeat(d,calc[d.c]),flip:changes(d)})).sort((a,b)=>a.last[2]-b.last[2]);document.getElementById('battle-list').innerHTML=arr.filter(x=>x.flip).slice(0,12).map(x=>`<li><button type="button" class="linkbutton" data-pick="${x.d.c}">${esc(x.d.n)}</button> (${x.d.m} seats): ${esc(x.flip)}; current last seat ${esc(x.last[0])} over ${esc(x.last[1])}, ${fmt(x.last[2])}-pt quotient gap.</li>`).join('')||'<li>No seats change in this Vox range; try another preset.</li>';
 document.querySelectorAll('[data-pick]').forEach(b=>b.onclick=()=>{select(b.dataset.pick);document.getElementById('map-section').scrollIntoView({behavior:'smooth'});});}
for(const [key,label] of Object.entries(layerLabels)){let b=document.createElement('button');b.type='button';b.dataset.layer=key;b.textContent=label;b.onclick=()=>{state.layer=key;render()};document.getElementById('layers').append(b);}
for(const b of document.querySelectorAll('[data-preset]'))b.onclick=()=>{state.preset=b.dataset.preset;state.vox=presets[state.preset].Vox;document.getElementById('vox').value=state.vox;updateControls();refresh()};
function updateControls(){document.getElementById('vox-out').textContent=fmt(state.vox)+'%';document.querySelectorAll('[data-preset]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.preset===state.preset));}
document.getElementById('vox').addEventListener('input',e=>{state.vox=Number(e.target.value);updateControls();refresh()});
document.getElementById('share-party').addEventListener('change',render);
updateControls();refresh();select('28');
})();