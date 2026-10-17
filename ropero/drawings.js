// Dibujos técnicos SVG · Tinta y Salvia. Líneas 1.5px tinta, cotas 0.75px, números en círculo naranja.
const INK='#1F2A2E',GREY='#6B7B78',SAGE='#DCE3DC',ACC='#D9502B',PINE='#E8C99A',JUTE='#C9AE7C';
const NS='vector-effect="non-scaling-stroke"';
const ln=(x1,y1,x2,y2,w=1.5,c=INK,extra='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}" ${NS} ${extra}/>`;
const rc=(x,y,w,h,fill='none',sw=1.5,c=INK,extra='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${c}" stroke-width="${sw}" ${NS} ${extra}/>`;
const tx=(x,y,t,fs,o={})=>`<text x="${x}" y="${y}" font-size="${fs}" fill="${o.c||INK}" text-anchor="${o.a||'middle'}" font-family="Inter,system-ui,sans-serif" font-weight="${o.w||500}" ${o.r?`transform="rotate(${o.r} ${x} ${y})"`:''} dominant-baseline="middle">${t}</text>`;
const bub=(x,y,n,r)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${ACC}"/>${tx(x,y+r*.05,n,r*1.15,{c:'#fff',w:700})}`;
function dimH(x1,x2,y,t,fs){const a=fs*.35;return ln(x1,y,x2,y,.75)+ln(x1,y-a,x1,y+a,.75)+ln(x2,y-a,x2,y+a,.75)+tx((x1+x2)/2,y-fs*.7,t,fs,{c:GREY})}
function dimV(y1,y2,x,t,fs){const a=fs*.35;return ln(x,y1,x,y2,.75)+ln(x-a,y1,x+a,y1,.75)+ln(x-a,y2,x+a,y2,.75)+tx(x-fs*.8,(y1+y2)/2,t,fs,{c:GREY,r:-90})}
// Vista frontal con puertas de yute (pino y yute solo como material)
function frontSVG(){const Y=y=>2000-y;let o=`<svg viewBox="-130 -60 1790 2200" width="100%" role="img" aria-label="Vista frontal del ropero"><defs><pattern id="jt" width="22" height="22" patternUnits="userSpaceOnUse"><rect width="22" height="22" fill="${JUTE}"/><path d="M0 11H22M11 0V22" stroke="#A88E5F" stroke-width="3" opacity=".55"/></pattern></defs>`;
 o+=rc(0,0,1600,2000,PINE);o+=rc(18,Y(50),1564,50,'#D9B784',.75);
 for(const [x,w] of [[18,802],[780,802]]){o+=rc(x,Y(68+1880),w,1880,PINE);o+=rc(x+63,Y(68+1880-63),w-126,1880-126,'url(#jt)',.75);o+=ln(x+w/2+(x<500?300:-300),Y(1050),x+w/2+(x<500?300:-300),Y(850),6)}
 o+=rc(18,Y(1982),1564,32,'#C8CFCC',.75);
 o+=dimH(0,1600,2070,'160 cm',72)+dimV(0,2000,-40,'200 cm',72);return o+'</svg>'}
// Distribución interior real
function interiorSVG(){const Y=y=>2000-y,fs=66;let o=`<svg viewBox="-260 -40 2100 2260" width="100%" role="img" aria-label="Distribución interior">`;
 o+=rc(18,Y(1982),773,1914,SAGE,0)+rc(809,Y(1982),773,1914,SAGE,0);
 o+=rc(0,0,1600,2000,'none');o+=rc(0,0,18,2000,'#fff')+rc(1582,0,18,2000,'#fff')+rc(18,0,1564,18,'#fff')+rc(18,Y(68),1564,18,'#fff')+rc(791,Y(1982),18,1914,'#fff');
 o+=rc(809,Y(1700),773,18,'#fff')+rc(809,Y(270),773,18,'#fff')+rc(18,Y(1053),773,18,'#fff');
 const rod=(x1,x2,y)=>ln(x1+30,Y(y),x2-30,Y(y),7,INK)+`<circle cx="${x1+30}" cy="${Y(y)}" r="9" fill="${INK}"/><circle cx="${x2-30}" cy="${Y(y)}" r="9" fill="${INK}"/>`;
 o+=rod(18,791,1900)+rod(18,791,980)+rod(809,1582,1630);
 o+=tx(404,Y(1500),'Prenda corta',fs,{c:ACC,w:600})+tx(404,Y(600),'Prenda corta',fs,{c:ACC,w:600})+tx(404,Y(1120),'Entrepaño 105',fs*.8,{c:GREY,w:600})+tx(1195,Y(1850),'Repisa',fs,{c:ACC,w:600})+tx(1195,Y(1100),'Prenda larga',fs,{c:ACC,w:600})+tx(1195,Y(170),'Zapatos',fs,{c:ACC,w:600})+tx(1195,Y(400),'Zapatos',fs,{c:ACC,w:600});
 for(const [x,y,t] of [[-70,1900,'190'],[-90,980,'98']])o+=dimV(Y(0),Y(y),x-(t==='98'?80:0),t,fs);
 for(const [x,y,t] of [[1690,1700,'170'],[1800,1630,'163']])o+=dimV(Y(0),Y(y),x,t,fs);
 o+=dimV(Y(0),Y(270),1590+0,'',0);
 o+=dimH(0,1600,2120,'160 cm · fondo 55.3',fs);return o+'</svg>'}
// Lámina de detalle por paso
const TOOL={pocket:'Plantilla Kreg + taladro + punta cuadrada #2',tornillo_directo:'Taladro + broca guía + avellanador + desarmador',grapa:'Engrapadora',riel:'Taladro + broca 3 mm + desarmador'};
function toolOf(u){if(/Clavo/.test(u.tornillo))return 'Martillo + botador (o taladro con broca 1.5 mm)';return TOOL[u.tipo]||'Taladro'}
function faceSVG(f,ids,num,maxw){const pad=Math.max(f.L,f.W)*.12,fs=Math.max(f.L,f.W)/28;const W=f.L+pad*2,H=f.W+pad*2.2;
 let o=`<svg viewBox="${-pad} ${-pad} ${W} ${H}" width="100%" style="max-width:${maxw}px;max-height:300px;display:block">`;
 o+=rc(0,0,f.L,f.W,'#FBF8F2');
 // canto de referencia en grueso
 const rx=f.mirror?f.L:0;o+=ln(rx,0,rx,f.W,3)+ln(0,f.W,f.L,f.W,3);
 o+=tx(rx+(f.mirror?-fs*.6:fs*.6),f.W/2,'ref. X',fs*.8,{c:GREY,r:-90});o+=tx(f.L/2,f.W+fs*.9,'ref. Y · '+f.yr,fs*.8,{c:GREY});
 const done={};
 for(const h of f.h){const act=ids.includes(h.u);const x=h.xd,y=f.W-h.y,r=h.k==='vent'?12.5:Math.max(f.L,f.W)/150;
  o+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${act?ACC:'#fff'}" stroke="${act?ACC:GREY}" stroke-width=".75" ${NS}/>`;
  if(act&&!done[h.u]){done[h.u]=1;const bx=Math.min(Math.max(x+fs*1.6,-pad*.4),f.L+pad*.5),by=Math.max(y-fs*1.6,-pad*.5);o+=ln(x,y,bx,by,.75,ACC)+bub(bx,by,num[h.u],fs*.75)}}
 o+=dimH(0,f.L,-pad*.45,f.L+' mm',fs*.75);return o+'</svg>'}
function plateHTML(i){const ids=(STEPU[i]||[]).filter(id=>UNI[id]);if(!ids.length)return`<div class="plate"><div class="plate-h">Lámina del paso ${i+1}</div><p class="small" style="margin:0">Este paso no lleva tornillos ni herrajes.</p></div>`;
 const num={};ids.forEach((id,k)=>num[id]=k+1);
 const faces=FACES.filter(f=>f.h.some(h=>ids.includes(h.u)));
 let o=`<div class="plate"><div class="plate-h">Lámina del paso ${i+1} · dónde va cada tornillo</div>`;
 o+=faces.map(f=>`<figure><figcaption><span class="num">${String(f.no).padStart(2,'0')}</span>${f.name}${f.pend?' <span class="tag warn-t">pendiente</span>':''}</figcaption>${faceSVG(f,ids,num,520)}${f.tpl?`<a class="tpl" href="plantillas/#p${String(f.no).padStart(2,'0')}">Plantilla 1:1 para imprimir →</a>`:'<span class="small">Sin plantilla: marca con escuadra y cinta.</span>'}</figure>`).join('');
 const pend=FACES.filter(f=>f.pend&&ids.some(id=>(UNI[id].piezas||[]).includes(f.no)&&UNI[id].tipo==='riel'));
 o+=pend.map(f=>`<div class="warn"><b>${f.name}:</b> ${f.pend}</div>`).join('');
 o+=`<ol class="callouts">${ids.map(id=>{const u=UNI[id];return`<li><span class="bub">${num[id]}</span><div><b>${u.tornillo}</b> · <b>${u.cantidad}</b> pz<div class="small">${u.cara}</div><div class="small">${(u.posiciones_mm||[]).join(' · ')}</div><div class="spec"><span>Broca guía: ${u.broca_guia||'—'}</span><span>Avellanado: ${u.broca_avellanado||'—'}</span><span>Profundidad: ${u.profundidad_mm} ${typeof u.profundidad_mm==='number'?'mm':''}</span><span>Herramienta: ${toolOf(u)}</span></div>${u.nota?`<div class="small">${u.nota}</div>`:''}</div></li>`}).join('')}</ol>`;
 const agg={};ids.forEach(id=>{const u=UNI[id];const k=u.tornillo.split(' — ')[0];agg[k]=(agg[k]||0)+(typeof u.cantidad==='number'?u.cantidad:0)||agg[k]||u.cantidad});
 o+=`<div class="hw"><b>Herrajes de este paso</b><ul>${Object.entries(agg).map(([k,v])=>`<li>${k} — <b>${v}</b></li>`).join('')}</ul></div></div>`;return o}
