const fmt=n=>'$'+Math.round(n).toLocaleString('es-MX');
const qty=b=>{const q=parseFloat(b[1].replace('≈',''));return isNaN(q)?1:q};
const lineTot=b=>b[2]*qty(b);
const TOT=BUDGET.reduce((a,b)=>a+lineTot(b),0);
const MIN=STEPS.reduce((a,s)=>a+s.min,0);
document.getElementById('tot').textContent=fmt(TOT)+' MXN';
document.getElementById('stats').innerHTML=[[P.length,'piezas numeradas'],[STEPS.length,'pasos de armado'],['≈'+Math.round(MIN/60)+' h','de trabajo · 2 fines de semana con secados'],[fmt(TOT),'MXN en materiales']].map(([a,b])=>`<div class="stat"><b>${a}</b><span>${b}</span></div>`).join('');
document.getElementById('budget').innerHTML=`<thead><tr><th>Partida</th><th>Cant.</th><th class="n">Subtotal</th></tr></thead><tbody>${BUDGET.map(b=>`<tr><td>${b[0]} ${b[4]?'<span class="tag">verificado</span>':''}${b[3]?`<div class="small">${b[3]}</div>`:''}</td><td style="white-space:nowrap">${b[1]}${qty(b)>1&&b[1]!=='lote'?`<div class="small">${fmt(b[2])} c/u</div>`:''}</td><td class="n">${fmt(lineTot(b))}</td></tr>`).join('')}</tbody><tfoot><tr><td colspan="2">Total materiales</td><td class="n">${fmt(TOT)}</td></tr></tfoot>`;
document.getElementById('compare').innerHTML=COMPARE.map((c,i)=>{const p=c[2]===null?TOT:c[2];const pr=Array.isArray(p)?fmt(p[0])+'–'+fmt(p[1]).slice(1):fmt(p);return`<div class="card" style="${i?'':'border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)'}"><div class="small">${c[1]}</div><h3 style="margin-top:4px">${c[0]}</h3><div style="font-size:26px;font-weight:700;letter-spacing:-.02em">${pr}</div><div class="small">${c[3]}</div></div>`}).join('');
// Armado
let cur=+localStorage.getItem('ropero_cur')||0;
const done=i=>!!localStorage.getItem('ropero_step_'+i);
const nm=n=>`<li><span class="num">${nn(n)}</span>${pz(n).n} <span class="small">· ${dims(pz(n))}</span></li>`;
function prog(){const d=STEPS.filter((_,i)=>done(i)).length;document.getElementById('bar').style.width=(100*d/STEPS.length)+'%';document.getElementById('progt').textContent=`${d} de ${STEPS.length} pasos terminados`;
 document.getElementById('dots').innerHTML=STEPS.map((_,i)=>`<button class="${i===cur?'on':''} ${done(i)?'dn':''}" onclick="goStep(${i})" aria-label="Paso ${i+1}">${i+1}</button>`).join('')}
function card(s,i){const pcs=[...s.n,...(s.f||[])];return`<p class="eyebrow" style="margin:0 0 4px">Paso ${i+1} de ${STEPS.length} · ≈${s.min} min</p><h3 style="font-size:20px">${s.t}</h3><p style="margin:6px 0 12px">${s.d}</p>
 <div class="small" style="font-weight:600;color:var(--ink)">${s.n.length?'Piezas nuevas':pcs.length?'Piezas involucradas':'Piezas'}</div>${pcs.length||s.x?`<ul class="list">${pcs.map(nm).join('')}${(s.x||[]).includes('riel')?'<li><span class="num">R</span>Riel doble de aluminio <span class="small">· 1564 mm</span></li>':''}</ul>`:'<p class="small" style="margin:4px 0">Ninguna todavía.</p>'}
 <div class="small" style="font-weight:600;color:var(--ink);margin-top:12px">Herramienta</div><div style="margin-top:6px">${s.tools.map(t=>`<span class="tool">${t}</span>`).join('')}</div>`}
function goStep(i){cur=Math.max(0,Math.min(STEPS.length-1,i));localStorage.setItem('ropero_cur',cur);const s=STEPS[cur];
 document.getElementById('stepcard').innerHTML=card(s,cur)+`<label class="done-ck"><input type="checkbox" id="dck" ${done(cur)?'checked':''}> Paso terminado</label>`;
 document.getElementById('dck').onchange=e=>{localStorage.setItem('ropero_step_'+cur,e.target.checked?'1':'');prog();if(e.target.checked&&cur<STEPS.length-1)setTimeout(()=>goStep(cur+1),350)};
 document.getElementById('prev').disabled=cur===0;document.getElementById('next').disabled=cur===STEPS.length-1;prog();
 if(window.__asm)window.__asm.show(cur,STEPS)}
document.getElementById('prev').onclick=()=>goStep(cur-1);document.getElementById('next').onclick=()=>goStep(cur+1);
document.getElementById('replay').onclick=()=>goStep(cur);
window.addEventListener('asm-ready',()=>goStep(cur));goStep(cur);
document.getElementById('printsteps').innerHTML=STEPS.map((s,i)=>`<div class="card" style="margin:8px 0">${card(s,i)}</div>`).join('');
// Taller
const TABS=[['mad','Maderería'],['pie','Piezas'],['com','Compras'],['aca','Acabado']];
let m='';
m+=`<div class="pane" data-s="mad"><div class="warn">⚠ <b>Piezas 16–19 y 28–29 (altura H): NO CORTAR</b> hasta comprar el riel. H = 1914 − descuento del riel según ficha (≈${H} orientativo).</div>
<div class="grid g2" style="margin-bottom:14px">${LUMBER.map(l=>`<div class="card"><h3>${l[0]}</h3><div class="small">${l[1]}</div>${l[2]?`<a class="btn ${l[2].startsWith('https')?'wa':'ghost'}" style="margin-top:10px" href="${l[2]}" target="_blank" rel="noopener">${l[3]}</a>`:`<div class="small" style="margin-top:8px">${l[3]}</div>`}</div>`).join('')}</div>
<button class="btn wa" id="cp" onclick="copyWA()" style="width:100%;margin-bottom:10px">Copiar lista de corte para WhatsApp</button>
<p class="small">Corte de sierra 3 mm · rayado = desperdicio · <span class="c">rojo = cubrecanto</span> · escribir el número en cada pieza.</p>`;
D.S.forEach(s=>{m+=`<div class="card" style="margin-bottom:14px"><h3>${s.t}</h3>${sheetSVG(s,420)}<table><tr><th>#</th><th>Pieza</th><th>Medida</th><th>Canto</th></tr>${s.p.map(([n])=>{const p=pz(n);return`<tr><td><span class="num">${nn(n)}</span></td><td>${p.n}</td><td>${dims(p)}</td><td>${p.c?'<span class=c>frente</span>':'—'}</td></tr>`}).join('')}</table></div>`});
m+=`<div class="card"><h3>Pino seco 19×63 (1×3) · tablas de 2440</h3><p class=small>Alto exagerado para leer; corte de sierra 3 mm.</p>${D.B.map((b,i)=>`<p class="small"><b>T${i+1}</b></p>`+(typeof b==='string'?`<p>${b}</p>`:boardSVG(b,i))).join('')}</div></div>`;
m+=`<div class="pane" data-s="pie"><div class="grid g2">${P.map(p=>`<div class="card"><h3><span class="num">${nn(p.no)}</span>${p.n}</h3><div class="small">${dims(p)} mm · ${p.mat}</div><div class="row"><div style="flex:1">${pieceSVG(p)}</div>${thumb([p.no],70)}</div><div class="small"><span class="c">Canto:</span> ${canto(p)}</div><div class="small">${p.nota}</div></div>`).join('')}</div><p class="small">● pocket (tornillo oculto) · ○ agujero · café = media madera</p></div>`;
m+=`<div class="pane" data-s="com"><div class="card">${BUY.map((b,i)=>{const k='ropero_buy_'+i;return`<label class="ck"><input type="checkbox" ${localStorage.getItem(k)?'checked':''} onchange="localStorage.setItem('${k}',this.checked?'1':'')"><div>${b[0]} ${b[1]?`<b>${b[1]}</b>`:''}</div></label>`}).join('')}<p class="small">Compra el riel antes de cortar las puertas. Precios pueden cambiar.</p></div></div>`;
m+=`<div class="pane" data-s="aca"><div class="card" style="margin-bottom:14px"><h3>Plan de acabado</h3><table>
<tr><td><b>Sellador</b></td><td>Todos los cantos, fondo (13–14), caras interiores del casco y tapas de puerta 28–29 por ambas caras. Antes de armar.</td></tr>
<tr><td><b>Linaza cocida + cera de abeja</b></td><td>Caras visibles (exterior de costados, frente, techo), bastidores 16–27 y junquillos 33–40. Linaza en capa delgada, retirar exceso a los 15 min, secar 24–48 h; luego cera y pulir.</td></tr>
<tr><td><b>Yute</b></td><td>Sin tratar.</td></tr></table></div>
<div class="card"><h3>Mantenimiento</h3><p style="margin:0">• Cera de abeja cada 3–4 meses.<br>• Aceite de linaza 1 vez al año.<br>• Humedad de Boca: deja 1–2 cm de la pared y no tapes los agujeros de ventilación del fondo.<br>• ⚠ Los trapos con linaza pueden autoincendiarse: extiéndelos a secar o mételos en agua.</p></div></div>`;
document.getElementById('panes').innerHTML=m;
document.getElementById('tabs').innerHTML=TABS.map(([id,t])=>`<button data-t="${id}" onclick="tab('${id}')">${t}</button>`).join('');
function tab(id){document.querySelectorAll('.pane').forEach(s=>s.classList.toggle('on',s.dataset.s===id));document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.t===id))}
tab('mad');
