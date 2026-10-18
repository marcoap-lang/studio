// Página de mueble chico (buró, repisa, banca) al nivel del ropero
const fmt=n=>'$'+Math.round(n).toLocaleString('es-MX');
const S=M.steps,K=M.key,MIN=S.reduce((a,s)=>a+s.min,0);
const $=id=>document.getElementById(id);
$('tot').textContent=fmt(M.total);
$('stats').innerHTML=[[M.pieces.length,'piezas de triplay'],[S.length,'pasos de armado'],['≈'+(Math.round(MIN/30)/2)+' h','de trabajo (+24 h de secado)'],[fmt(M.total),'MXN en materiales']].map(([a,b])=>`<div class="stat"><b>${a}</b><span>${b}</span></div>`).join('');
$('pieces').innerHTML='<tr><th>#</th><th>Pieza</th><th>Medida (mm)</th><th>Cubrecanto</th><th>Hoja</th></tr>'+M.pieces.map(p=>`<tr><td><b>${p[0]}</b></td><td>${p[1]}</td><td>${p[2]} × ${p[3]} × ${p[4]}</td><td>${p[5]}</td><td>${p[6]}</td></tr>`).join('');
$('budget').innerHTML=`<thead><tr><th>Partida</th><th class="n">Subtotal</th></tr></thead><tbody>${M.budget.map(b=>`<tr><td>${b[0]}${b[1]?`<div class="small">${b[1]}</div>`:''}</td><td class="n">${fmt(b[2])}</td></tr>`).join('')}</tbody><tfoot><tr><td>Total materiales</td><td class="n">${fmt(M.total)}</td></tr></tfoot>`;
$('compare').innerHTML=M.compare.map((c,i)=>`<div class="card" style="${i?'':'border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)'}"><h3 style="margin-top:4px">${c[0]}</h3><div style="font-size:26px;font-weight:700;letter-spacing:-.02em">${c[1]===null?fmt(M.total):c[1]}</div><div class="small">${c[2]}</div></div>`).join('');
const nm=id=>{const p=M.names[id]||{n:id,d:''};return`<li><span class="num">${id}</span>${p.n} <span class="small">· ${p.d}</span></li>`};
let cur=+localStorage.getItem(K+'_cur')||0;const done=i=>!!localStorage.getItem(K+'_step_'+i);
function prog(){const d=S.filter((_,i)=>done(i)).length;$('bar').style.width=(100*d/S.length)+'%';$('progt').textContent=`${d} de ${S.length} pasos terminados`;
 $('dots').innerHTML=S.map((_,i)=>`<button class="${i===cur?'on':''} ${done(i)?'dn':''}" onclick="goStep(${i})" aria-label="Paso ${i+1}">${i+1}</button>`).join('')}
function card(s,i){const pcs=[...s.n,...s.f];const pf=M.pdf[i];return`<p class="eyebrow" style="margin:0 0 4px">Paso ${i+1} de ${S.length} · ≈${s.min} min</p><h3 style="font-size:20px">${s.t}</h3><p style="margin:6px 0 12px">${s.d}</p>
 <div class="small" style="font-weight:600;color:var(--ink)">${s.n.length?'Piezas nuevas':'Piezas involucradas'}</div>${pcs.length?`<ul class="list">${pcs.map(nm).join('')}</ul>`:'<p class="small" style="margin:4px 0">Todas las del mueble.</p>'}
 <div class="small" style="font-weight:600;color:var(--ink);margin-top:12px">Herramienta</div><div style="margin-top:6px">${s.tools.map(t=>`<span class="tool">${t}</span>`).join('')}</div>${pf?`<a class="btn" style="margin-top:12px;width:100%" href="plantillas/${pf}" target="_blank" rel="noopener">Plantillas de este paso (PDF 1:1)</a>`:''}`}
const COLK={pocket:'#D9502B',screw:'#1F2A2E'};
function faceSVG(f,ids,num){const sc=Math.min(300/f.L,170/f.W),W=f.L*sc,H=f.W*sc,pad=14;let o=`<svg viewBox="0 0 ${W+2*pad} ${H+2*pad+10}" style="width:100%;max-width:520px"><rect x="${pad}" y="${pad}" width="${W}" height="${H}" fill="#E8C99A" stroke="#1F2A2E" stroke-width="1"/>`;
 for(const h of f.h){if(!ids.includes(h.u))continue;const x=pad+h.xd*sc,y=pad+H-h.y*sc;o+=h.k==='pocket'?`<rect x="${x-(h.xd>f.L/2?9:0)}" y="${y-2.5}" width="9" height="5" rx="2.5" fill="#D9502B" fill-opacity=".3" stroke="#D9502B"/>`:`<circle cx="${x}" cy="${y}" r="3" fill="#fff" stroke="#1F2A2E"/>`;o+=`<text x="${x}" y="${y-5}" font-size="8" text-anchor="middle" fill="${COLK[h.k]}" font-weight="700">${num[h.u]}</text>`}
 o+=`<text x="${pad}" y="${H+2*pad+6}" font-size="8" fill="#6B7B78">${f.L} × ${f.W} mm${f.mirror?' · vista en espejo (pieza volteada)':''}</text></svg>`;return o}
function plateHTML(i){const ids=S[i].j.filter(id=>M.joints[id]);if(!ids.length)return`<div class="plate"><div class="plate-h">Lámina del paso ${i+1}</div><p class="small" style="margin:0">Este paso no lleva tornillos ni herrajes.</p></div>`;
 const num={};ids.forEach((id,k)=>num[id]=k+1);const faces=M.faces.filter(f=>f.h.some(h=>ids.includes(h.u)));
 let o=`<div class="plate"><div class="plate-h">Lámina del paso ${i+1} · dónde va cada tornillo</div>`;
 o+=faces.map(f=>`<figure><figcaption><span class="num">${f.no}</span>${f.name}</figcaption>${faceSVG(f,ids,num)}<a class="tpl" href="plantillas/">Plantilla 1:1 para imprimir →</a></figure>`).join('');
 o+=`<ol class="callouts">${ids.map(id=>{const u=M.joints[id];return`<li><span class="bub">${num[id]}</span><div><b>${u.tornillo}</b> · <b>${u.cantidad}</b> pz<div class="small">${u.cara}</div><div class="small">${u.pos.join(' · ')}</div><div class="spec"><span>Broca guía: ${u.broca_guia}</span><span>Avellanado: ${u.broca_avellanado}</span><span>Profundidad: ${u.profundidad}</span><span>Herramienta: ${u.herr}</span></div>${u.nota?`<div class="small">${u.nota}</div>`:''}</div></li>`}).join('')}</ol>`;
 const agg={};ids.forEach(id=>{const u=M.joints[id];agg[u.tornillo]=(agg[u.tornillo]||0)+u.cantidad});
 return o+`<div class="hw"><b>Herrajes de este paso</b><ul>${Object.entries(agg).map(([k,v])=>`<li>${k} — <b>${v}</b></li>`).join('')}</ul></div></div>`}
function goStep(i){cur=Math.max(0,Math.min(S.length-1,i));localStorage.setItem(K+'_cur',cur);
 $('stepcard').innerHTML=card(S[cur],cur)+`<label class="done-ck"><input type="checkbox" id="dck" ${done(cur)?'checked':''}> Paso terminado</label>`;
 $('dck').onchange=e=>{localStorage.setItem(K+'_step_'+cur,e.target.checked?'1':'');prog();if(e.target.checked&&cur<S.length-1)setTimeout(()=>goStep(cur+1),350)};
 $('prev').disabled=cur===0;$('next').disabled=cur===S.length-1;prog();$('plate').innerHTML=plateHTML(cur);
 if(window.__asm)window.__asm.step(cur)}
window.goStep=goStep;$('prev').onclick=()=>goStep(cur-1);$('next').onclick=()=>goStep(cur+1);
window.addEventListener('asm-ready',()=>goStep(cur));goStep(cur);
$('printsteps').innerHTML=S.map((s,i)=>`<div class="card" style="margin:8px 0">${card(s,i)}${plateHTML(i)}</div>`).join('');
$('buy').innerHTML=M.hw.map((b,i)=>{const k=K+'_buy_'+i;return`<label class="ck"><input type="checkbox" ${localStorage.getItem(k)?'checked':''} onchange="localStorage.setItem('${k}',this.checked?'1':'')"><div><b>${b[0]}</b> · ${b[2]} ${b[2]>1?'pz':''}<div class="small">Cómo pedirlo: ${b[1]}</div></div></label>`}).join('')+'<p class="small">Herramienta: taladro, plantilla Kreg con broca escalonada 3/8″, brocas de 2 y 3 mm, avellanador, prensas, escuadra, flexómetro, plancha para el cubrecanto.</p>';
