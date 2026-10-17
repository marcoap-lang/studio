const $=s=>document.querySelector(s);
const pz=n=>P[n-1];
function canto(p){return p.c?'cubrecanto en canto frontal (largo '+p.L+')':'sin cubrecanto'}
function dims(p){return p.l==='J'||p.l==='L'?`H≈${p.L} × ${p.W} × ${p.T}`:`${p.L} × ${p.W} × ${p.T}`}
// sheet svg
function sheetSVG(s,wpx){const sc=wpx/(s.W+260);let o=`<svg viewBox="-200 -60 ${s.W+260} ${s.H+200}" width="100%" style="max-width:${wpx}px"><defs><pattern id="hx" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M0 0L40 40M40 0L0 40" stroke="#aaa" stroke-width="3"/></pattern></defs>`;
 o+=`<rect x="0" y="0" width="${s.W}" height="${s.H}" fill="url(#hx)" stroke="#000" stroke-width="6"/>`;
 for(const[n,x,y,w,h] of s.p){const p=pz(n),Y=s.H-y-h;o+=`<rect x="${x}" y="${Y}" width="${w}" height="${h}" fill="#e9d8b4" stroke="#000" stroke-width="4"/>`;
  if(p.c){const long=w>h; o+= long?`<line x1="${x}" y1="${Y+h}" x2="${x+w}" y2="${Y+h}" stroke="#d00" stroke-width="16"/>`:`<line x1="${x}" y1="${Y}" x2="${x}" y2="${Y+h}" stroke="#d00" stroke-width="16"/>`}
  if(w>=200)o+=`<text x="${x+w/2}" y="${Y+h/2}" text-anchor="middle" font-size="110" font-weight="700">${String(n).padStart(2,'0')}</text><text x="${x+w/2}" y="${Y+h/2+110}" text-anchor="middle" font-size="70">${Math.max(w,h)}×${Math.min(w,h)}</text>`;
  else o+=`<text transform="translate(${x+w/2+20},${Y+h/2}) rotate(-90)" text-anchor="middle" font-size="44" font-weight="700">${String(n).padStart(2,'0')} · ${Math.max(w,h)}×${Math.min(w,h)}</text>`}
 o+=`<text x="${s.W/2}" y="${s.H+90}" text-anchor="middle" font-size="70">${s.W}</text><text transform="translate(-80,${s.H/2}) rotate(-90)" text-anchor="middle" font-size="70">${s.H}</text></svg>`;return o}
function boardSVG(b,i){let o=`<svg viewBox="-10 -10 2460 200" width="100%"><rect x="0" y="0" width="2440" height="180" fill="url(#hx)" stroke="#000" stroke-width="4"/>`;let x=0;
 for(const[n,l] of b){o+=`<rect x="${x}" y="0" width="${l}" height="180" fill="#e9d8b4" stroke="#000" stroke-width="4"/><text x="${x+l/2}" y="120" text-anchor="middle" font-size="100" font-weight="700">${String(n).padStart(2,'0')} · ${l}</text>`;x+=l+3}
 return o+`</svg>`}
// thumbnail
const BASE=[[0,0,18,2000],[1582,0,18,2000],[18,1982,1564,18],[18,50,1564,18],[791,68,18,1914],[809,1682,773,18],[809,252,773,18],[18,0,1564,50]];
function thumb(nums,w=90){let o=`<svg viewBox="-20 -20 1640 2040" width="${w}">`;for(const r of BASE)o+=`<rect x="${r[0]}" y="${2000-r[1]-r[3]}" width="${r[2]}" height="${r[3]}" fill="#eee" stroke="#999" stroke-width="6"/>`;
 for(const n of nums){const r=pz(n).th,big=r[2]>300&&r[3]>300;o+=`<rect x="${r[0]}" y="${2000-r[1]-r[3]}" width="${r[2]}" height="${r[3]}" fill="#d00" fill-opacity="${big?.3:.9}" stroke="#d00" stroke-width="8"/>`}return o+'</svg>'}
// piece drawing
function pieceSVG(p){const L=p.L,W=p.W,s=Math.max(L,W);let o=`<svg viewBox="${-s*.2} ${-W-s*.05} ${L+s*.25} ${W+s*.2}" width="100%" style="max-height:140px">`;
 o+=`<rect x="0" y="${-W}" width="${L}" height="${W}" fill="${p.l==='M'?'#ccc':'#e9d8b4'}" stroke="#000" stroke-width="${s/300}"/>`;
 if(p.c)o+=`<line x1="0" y1="0" x2="${L}" y2="0" stroke="#d00" stroke-width="${s/60}"/>`;
 const dot=(x,y,f)=>o+=`<circle cx="${x}" cy="${-y}" r="${s/140}" fill="${f?'#000':'#fff'}" stroke="#000" stroke-width="${s/500}"/>`;
 if('BCD'.includes(p.l))for(let i=1;i<=4;i++){dot(30,W*i/5,1);dot(L-30,W*i/5,1)}
 if('EF'.includes(p.l))for(const y of[60,W-60]){dot(25,y,1);dot(L-25,y,1)}
 if(p.l==='A')for(const x of[980,1900,1650])dot(x,270,0);
 if('GH'.includes(p.l)){dot(20,W/2,1);dot(L-20,W/2,1)}
 if(p.l==='I')for(const x of[100,L-100])for(let y=100;y<W;y+=150)dot(x,y,0);
 if(p.l==='J')for(const x of[0,L-63,L/3-31,2*L/3-31])o+=`<rect x="${x}" y="${-W}" width="63" height="${W}" fill="#b89a5e" stroke="#000" stroke-width="${s/500}"/>`;
 if(p.l==='K')for(const x of[0,L-63])o+=`<rect x="${x}" y="${-W}" width="63" height="${W}" fill="#b89a5e" stroke="#000" stroke-width="${s/500}"/>`;
 const fs=s/14;o+=`<text x="${L/2}" y="${s*.11}" text-anchor="middle" font-size="${fs}">${p.l==='J'||p.l==='L'?'H≈':''}${L}</text><text x="${-s*.02}" y="${-W/2}" text-anchor="end" dominant-baseline="middle" font-size="${fs}">${W}</text></svg>`;return o}
const nn=n=>String(n).padStart(2,'0');
function waText(){let t='*ROPERO 160×200×55 – Lista de corte (mm)*\nCorte de sierra 3 mm. Escribir el NÚMERO en cada pieza. C = cubrecanto en canto frontal.\n';
 D.S.forEach(s=>{t+=`\n*${s.t}*\n`;s.p.forEach(([n])=>{const p=pz(n);t+=`${nn(n)} ${p.n}: ${dims(p)}${p.c?' (C)':''}\n`})});
 t+='\n*Pino seco 19×63 (1×3) – tablas 2440*\n';D.B.forEach((b,i)=>{t+=`T${i+1}: `+(typeof b==='string'?b:b.map(([n,l])=>`${nn(n)}=${l}`).join(' + '))+'\n'});
 t+='\n⚠ Piezas 16-19 (largueros) y 28-29 (tapas): altura H pendiente. NO CORTAR hasta comprar el riel y confirmar H = 1914 − descuento del fabricante.';return t}
function copyWA(){const t=waText();const ok=()=>{$('#cp').textContent='✔ Copiado'};if(navigator.clipboard&&isSecureContext)navigator.clipboard.writeText(t).then(ok,fb);else fb();function fb(){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();ok()}}
