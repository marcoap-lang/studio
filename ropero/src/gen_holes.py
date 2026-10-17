# Genera holes.js (caras, agujeros, uniones por paso) y plantillas/index.html (1:1, carta)
import json, math
U=json.load(open('/workspace/ropero/uniones.json'))
D=json.load(open('/workspace/ropero/data.json'));P=D['P'];H=D['H']
PK=dict(k='pocket',bit='Kreg escalonada 3/8″',cs='—',depth='collar a 3/4″ (18 mm)',screw='#8 × 1¼″ pocket rondana')
SD=dict(k='screw',bit='guía 3 mm',cs='avellanar 8 mm',depth='40 mm',screw='#8 × 1½″ cabeza plana')
SU=dict(k='support',bit='guía 3 mm',cs='—',depth='14 mm (tope)',screw='#8 × 5/8″ cabeza plana')
BK=dict(k='screw',bit='guía 2 mm',cs='avellanado ligero',depth='16 mm',screw='#6 × 5/8″ cabeza plana')
DR=dict(k='screw',bit='guía 2 mm',cs='avellanar al ras',depth='16 mm',screw='#6 × 5/8″ cabeza plana')
VT=dict(k='vent',bit='sierra copa Ø25',cs='—',depth='pasado',screw='— (ventilación)')
F=[]
def face(id,no,name,L,W,xr,yr,holes,tpl=True,pend=None,mirror=False,count=1):
    for h_ in holes: h_['xd']=round(L-h_['x'],1) if mirror else h_['x']
    F.append(dict(id=id,no=no,name=name,L=L,W=W,xr=xr,yr=yr,h=holes,tpl=tpl,pend=pend,mirror=mirror,count=count))
def hs(spec,u,pts): return [dict(x=round(x,1),y=round(y,1),u=u,**spec) for x,y in pts]
ends=lambda L,ys:[(20,y) for y in ys]+[(L-20,y) for y in ys]
face('03s',3,'Techo · cara superior',1564,547,'canto izquierdo (visto de frente)','canto frontal',
     hs(PK,'U02',ends(1564,[60,215,370,487]))+hs(SD,'U08',[(1186,537.5),(1219,537.5)]))
face('03i',3,'Techo · cara inferior (riel)',1564,547,'canto izquierdo','canto frontal',[],pend='Riel: agujeros según ficha del riel comprado. Tornillo #8 × 3/4″, guía 3 mm, máx. 16 mm de profundidad. Pendiente: medir riel comprado.')
face('04i',4,'Piso · cara inferior',1564,547,'canto izquierdo (visto de frente)','canto frontal',
     hs(PK,'U03',ends(1564,[90,230,370,487]))+hs(SD,'U08',[(1186,537.5),(1219,537.5)]),mirror=True)
xs=[50,250,450,650,914,1114,1314,1514]
face('04s',4,'Piso · cara superior (fijación al zócalo)',1564,547,'canto izquierdo','canto frontal',
     hs(SD,'U11',[(x,59) for x in xs]+[(x,538) for x in xs]+[(9,150),(9,400),(1555,150),(1555,400)]),tpl=False)
face('05d',5,'División · cara derecha',1914,547,'canto inferior','canto frontal',
     hs(PK,'U04',[(1894,y) for y in (60,273.5,487)])+hs(PK,'U05',[(20,y) for y in (60,273.5,487)])+hs(SU,'U13',[(1630-68,270)]),mirror=True)
face('05i',5,'División · cara izquierda',1914,547,'canto inferior','canto frontal',hs(SU,'U13',[(1832,270),(912,270)]))
face('01',1,'Costado 01 · cara interior',2000,547,'canto inferior (suelo)','canto frontal',hs(SU,'U12',[(1900,270),(980,270)]),mirror=True)
face('02',2,'Costado 02 · cara interior',2000,547,'canto inferior (suelo)','canto frontal',hs(SU,'U14',[(1630,270)]))
face('06',6,'Repisa 06 · cara inferior',773,461,'canto izquierdo','canto frontal',hs(PK,'U06',ends(773,[60,401])),mirror=True)
face('07',7,'Zapatera 07 · cara inferior',773,331,'canto izquierdo','canto frontal',hs(PK,'U07',ends(773,[60,271])),mirror=True)
face('10',10,'Travesaños 10, 11 y 12 · cara interior',461,50,'canto trasero','canto inferior',hs(PK,'U01',[(20,25),(441,25)]),count=3)
hb=[50+185*i for i in range(11)]
def vents(W,cols):
    out=[]
    for y in (140,1810):
        x=75
        while x<W-20:
            if all(abs(x-c)>=42.5 for c in cols): out.append((x,y))
            x+=150
    return out
face('13',13,'Fondo grande 13 · cara trasera',1220,1950,'canto izquierdo del mueble','canto inferior',
     hs(BK,'U09',[(9,y) for y in hb]+[(800,y) for y in hb]+[(1205,y) for y in hb]+[(50+186.67*i,9) for i in range(7)]+[(50+186.67*i,1941) for i in range(7)])+hs(VT,'C14',vents(1220,[9,800,1205])),tpl=False,mirror=True)
face('14',14,'Fondo tira 14 · cara trasera',380,1950,'canto izquierdo de la tira','canto inferior',
     hs(BK,'U10',[(16,y) for y in hb]+[(371,y) for y in hb]+[(x,9) for x in (50,190,330)]+[(x,1941) for x in (50,190,330)])+hs(VT,'C14',vents(380,[16,371])),tpl=False,mirror=True)
sq=[0,H/3-31.5,2*H/3-31.5,H-63]
face('16',16,'Largueros 16–19 · cara frontal (medias maderas)',H,63,'canto inferior','canto exterior',
     hs(DR,'U18',[(s+a,b) for s in sq for a,b in ((20,20),(43,43))]),pend='Altura H pendiente: medir riel comprado y recalcular (H/3, 2H/3).',count=4)
U_by={u['id']:u for u in U['uniones']}
# uniones por paso
steps={}
for u in U['uniones']:
    n=int(u['paso_armado'].split('·')[0])-1; steps.setdefault(n,[]).append(u['id'])
steps[2]=['U01','U02','U03','U04','U05','U06','U07','U12','U13','U14']  # paso 3: perforar
fix={'U15':{'tornillo':'#8 × 3/4″ (19 mm) cabeza plana — confirmar con ficha del riel'},
     'U18':{'tornillo':'#6 × 5/8″ (16 mm) cabeza plana'},'U19':{'tornillo':'#6 × 5/8″ (16 mm) cabeza plana'},
     'U06':{'posiciones_mm':['2 por extremo: 60 y 401 desde canto frontal (repisa de 461)','Cara superior a 1700 del suelo; se apoya contra el listón 15']},
     'U07':{'posiciones_mm':['2 por extremo: 60 y 271 desde canto frontal (zapatera de 331)','Cara superior a 270 del suelo']},
     'U13':{'posiciones_mm':['Cara izquierda: soportes 30 y 31 a 270 del frente; 1832 y 912 desde canto inferior (=1900 y 980 del suelo)','Cara derecha: soporte 32 a 270 del frente; 1562 desde canto inferior (=1630 del suelo)']},
     'U14':{'posiciones_mm':['Soporte tubo 32: 270 desde canto frontal, 1630 desde canto inferior (centro del tubo)']},
     'U20':{'posiciones_mm':['A 31.5 del canto exterior (centro del bastidor), perímetro y 2 travesaños intermedios, cada 50']},
     'U01':{'posiciones_mm':['1 bolsillo por extremo de cada travesaño (461 mm), centrado a 25 del canto inferior']}}
for k,v in fix.items(): U_by[k].update(v)
FER=U['ferreteria']
for f_ in FER:
    if f_['articulo'].startswith('Tornillo #8 x 3/4'): f_['articulo']='Tornillo #8 × 3/4″ (19 mm) cabeza plana para riel — confirmar con ficha'
    f_['articulo']=f_['articulo'].replace(' (acordado #8 x 1\"; ver C08)','')
open('/workspace/studio/ropero/holes.js','w').write('window.FACES='+json.dumps(F,ensure_ascii=False)+';\nwindow.UNI='+json.dumps(U_by,ensure_ascii=False)+';\nwindow.STEPU='+json.dumps(steps)+';\nwindow.FER='+json.dumps(FER,ensure_ascii=False)+';\n')
# ---------- plantillas 1:1 ----------
PW,PH=215.9,279.4; M=10; HEAD=22; CW,CH=PW-2*M, PH-2*M-HEAD-8
def clusters(h):
    cl=[]
    for p in h:
        hit=[c for c in cl if any(math.hypot(p['xd']-q['xd'],p['y']-q['y'])<=200 for q in c)]
        new=[p]+[q for c in hit for q in c]; cl=[c for c in cl if c not in hit]+[new]
    return cl
pages=[]
for f in [f for f in F if f['tpl'] or f['pend']]:
    groups=clusters(f['h']) if f['h'] else [[]]
    for gi,g in enumerate(groups):
        if g:
            x0=min(p['xd'] for p in g)-45; x1=max(p['xd'] for p in g)+45; y0=min(p['y'] for p in g)-45; y1=max(p['y'] for p in g)+45
        else: x0,x1,y0,y1=0,160,0,120
        if x0<130:x0=0
        if y0<130:y0=0
        if f['L']-x1<130:x1=f['L']
        if f['W']-y1<130:y1=f['W']
        x0,y0=max(0,x0),max(0,y0);x1,y1=min(f['L'],x1),min(f['W'],y1)
        w,h=x1-x0,y1-y0
        rot= math.ceil(w/CW)*math.ceil(h/CH) > math.ceil(w/CH)*math.ceil(h/CW)
        tw,th=(CH,CW) if rot else (CW,CH)
        nx,ny=math.ceil(w/tw),math.ceil(h/th)
        for j in range(ny):
            for i in range(nx):
                pages.append(dict(f=f,g=gi,ng=len(groups),x0=x0+i*tw,y0=y0+j*th,tw=min(tw,x1-x0-i*tw),th=min(th,y1-y0-j*th),i=i,j=j,nx=nx,ny=ny,rot=rot,full=(x0,x1,y0,y1)))
def esc(s):return str(s).replace('&','&amp;').replace('<','&lt;')
def page_svg(pg,num,tot):
    f=pg['f'];rot=pg['rot']
    o=[f'<section class="pg"><div class="hd"><b class="no">{f["no"]:02d}</b><div><div class="t">{esc(f["name"])}{" ×"+str(f["count"]) if f["count"]>1 else ""}</div><div class="s">Zona {pg["g"]+1}/{pg["ng"]} · hoja {chr(65+pg["j"])}{pg["i"]+1} de {pg["ny"]}×{pg["nx"]} · X desde {esc(f["xr"])} · Y desde {esc(f["yr"])}</div></div><div class="pn">{num}/{tot}</div></div>']
    # contenido en mm: origen arriba-izq del área
    o.append(f'<svg class="c" width="{CW}mm" height="{CH}mm" viewBox="0 0 {CW} {CH}">')
    def tr(x,y):
        lx,ly=x-pg['x0'],y-pg['y0']
        if f['mirror']:pass
        return (ly,lx) if rot else (lx,CH-ly)
    def T(x,y):
        a,b=tr(x,y); return (a, b) if not rot else (a, b)
    # rect area of tile
    if rot: o.append(f'<rect x="0" y="0" width="{pg["th"]}" height="{pg["tw"]}" fill="none" stroke="#6B7B78" stroke-width=".3" stroke-dasharray="2 1.5"/>')
    else: o.append(f'<rect x="0" y="{CH-pg["th"]}" width="{pg["tw"]}" height="{pg["th"]}" fill="none" stroke="#6B7B78" stroke-width=".3" stroke-dasharray="2 1.5"/>')
    # piece edges inside tile
    def line(x1,y1,x2,y2,w=.6,c='#1F2A2E'):
        a=tr(x1,y1);b=tr(x2,y2);o.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{c}" stroke-width="{w}"/>')
    X0,Y0,X1,Y1=pg['x0'],pg['y0'],pg['x0']+pg['tw'],pg['y0']+pg['th']
    for xe,isref in ((0,not f['mirror']),(f['L'],f['mirror'])):
        if X0-0.01<=xe<=X1+0.01: line(xe,Y0,xe,Y1,1.2); a=tr(xe,(Y0+Y1)/2);o.append(f'<text x="{a[0]+3.5:.1f}" y="{a[1]:.1f}" class="el" text-anchor="middle" transform="rotate({0 if rot else -90} {a[0]+3.5:.1f} {a[1]:.1f})">{("CANTO REF. X · "+esc(f["xr"])) if isref else "canto opuesto"}</text>')
    for ye in (0,f['W']):
        if Y0-0.01<=ye<=Y1+0.01: line(X0,ye,X1,ye,1.2); a=tr((X0+X1)/2,ye);o.append(f'<text x="{a[0]:.1f}" y="{a[1]-1.5:.1f}" class="el" text-anchor="middle" transform="rotate({-90 if rot else 0} {a[0]:.1f} {a[1]-1.5:.1f})">{"CANTO REF. Y · "+esc(f["yr"]) if ye==0 else "canto opuesto"}</text>')
    # holes
    k=0
    for hl in f['h']:
        if X0-0.01<=hl['xd']<=X1+0.01 and Y0-0.01<=hl['y']<=Y1+0.01:
            a,b=tr(hl['xd'],hl['y']);r=12.5 if hl['k']=='vent' else 4
            o.append(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="{r}" fill="none" stroke="#D9502B" stroke-width=".4"/><line x1="{a-9:.2f}" y1="{b:.2f}" x2="{a+9:.2f}" y2="{b:.2f}" stroke="#1F2A2E" stroke-width=".25"/><line x1="{a:.2f}" y1="{b-9:.2f}" x2="{a:.2f}" y2="{b+9:.2f}" stroke="#1F2A2E" stroke-width=".25"/>')
            tx=a+5; anchor='start'
            if tx>CW-60: tx=a-5;anchor='end'
            ty=b-5 if b>20 else b+9
            kind={'pocket':'POCKET','support':'SOPORTE (centro)','screw':'TORNILLO','vent':'VENT.'}[hl['k']]
            o.append(f'<text x="{tx:.1f}" y="{ty:.1f}" class="hl" text-anchor="{anchor}">{kind} · X {hl["x"]:g} · Y {hl["y"]:g}</text><text x="{tx:.1f}" y="{ty+3.6:.1f}" class="hs" text-anchor="{anchor}">{esc(hl["bit"])} · {esc(hl["cs"])} · prof. {esc(hl["depth"])}</text><text x="{tx:.1f}" y="{ty+7:.1f}" class="hs" text-anchor="{anchor}">{esc(hl["screw"])}</text>')
    # tiling marks
    for (cx,cy) in ((0,0),(CW,0),(0,CH),(CW,CH)):
        o.append(f'<path d="M{cx-4} {cy}H{cx+4}M{cx} {cy-4}V{cy+4}" stroke="#1F2A2E" stroke-width=".3"/>')
    if pg['nx']>1 or pg['ny']>1: o.append(f'<text x="{CW/2}" y="4" class="hs" text-anchor="middle">Recorta por la línea punteada y une con cinta a las hojas vecinas haciendo coincidir las cruces de las esquinas</text>')
    if f['pend']: o.append(f'<rect x="{CW/2-80}" y="{CH/2-12}" width="160" height="24" fill="#fff" stroke="#D9502B" stroke-width=".8"/><text x="{CW/2}" y="{CH/2-2}" class="pd" text-anchor="middle">PENDIENTE: MEDIR RIEL COMPRADO</text><text x="{CW/2}" y="{CH/2+5}" class="hs" text-anchor="middle">{esc(f["pend"])[:110]}</text>')
    o.append('</svg>')
    o.append('<div class="ft"><svg width="110mm" height="9mm" viewBox="0 0 110 9"><line x1="0" y1="6" x2="100" y2="6" stroke="#1F2A2E" stroke-width=".4"/>'+''.join(f'<line x1="{i}" y1="{2 if i%10==0 else 4}" x2="{i}" y2="6" stroke="#1F2A2E" stroke-width=".25"/>' for i in range(0,101,5))+'<text x="0" y="1.8" class="hs">0</text><text x="100" y="1.8" class="hs" text-anchor="middle">10 cm</text></svg><span><b>Imprimir al 100 %, sin ajustar</b> (tamaño carta). Mide la regla: debe dar 10 cm exactos.</span></div></section>')
    return ''.join(o)
tot=len(pages)
idx=[]
seen=set()
for n,pg in enumerate(pages,1):
    if pg['f']['id'] not in seen: seen.add(pg['f']['id']);idx.append((pg['f'],n))
html=f'''<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plantillas de perforación 1:1 · Ropero · Strate Studio</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Ccircle cx=%228%22 cy=%228%22 r=%228%22 fill=%22%23D9502B%22/%3E%3C/svg%3E">
<link rel="stylesheet" href="../../fonts/fonts.css"><style>
@page{{size:letter;margin:0}}*{{box-sizing:border-box}}body{{margin:0;background:#F4F3EE;color:#1F2A2E;font-family:Inter,system-ui,sans-serif}}
.intro{{max-width:760px;margin:auto;padding:24px 18px}}.intro h1{{font-family:Fraunces,serif;font-weight:600;font-size:32px;margin:0 0 8px;letter-spacing:-.02em}}.intro a.b{{display:inline-block;background:#1F2A2E;color:#fff;border-radius:99px;padding:11px 18px;text-decoration:none;font-weight:600;margin:6px 8px 6px 0}}
.intro li{{margin:4px 0}}.intro .w{{background:#fff;border:1px solid #D9502B;border-radius:12px;padding:10px 14px}}
.pg{{width:215.9mm;height:279.4mm;padding:10mm;background:#fff;margin:0 auto 12px;position:relative;overflow:hidden;break-after:page;box-shadow:0 2px 10px #0001}}
.hd{{display:flex;gap:4mm;align-items:center;height:22mm;border-bottom:.3mm solid #1F2A2E}}.no{{width:13mm;height:13mm;border-radius:50%;background:#D9502B;color:#fff;display:flex;align-items:center;justify-content:center;font-size:5mm}}
.t{{font-family:Fraunces,serif;font-size:5mm;font-weight:600}}.s{{font-size:2.7mm;color:#6B7B78}}.pn{{margin-left:auto;font-size:3mm;color:#6B7B78}}
.c{{display:block;margin-top:0}}.el{{font-size:2.6px;fill:#1F2A2E;font-weight:700;letter-spacing:.1px}}.hl{{font-size:2.8px;font-weight:700;fill:#D9502B}}.hs{{font-size:2.4px;fill:#1F2A2E}}.pd{{font-size:4px;font-weight:800;fill:#D9502B}}
.ft svg{{flex:0 0 auto}}.c{{flex:none}}.ft{{position:absolute;left:10mm;bottom:6mm;display:flex;gap:4mm;align-items:flex-end;font-size:2.8mm}}
@media screen and (max-width:820px){{.pg{{transform-origin:top left;}}}}
@media print{{body{{background:#fff}}.intro{{display:none}}.pg{{margin:0;box-shadow:none}}}}
</style></head><body><div class="intro"><p style="color:#D9502B;font-weight:600;letter-spacing:.14em;font-size:12px;text-transform:uppercase;margin:0">Strate Studio · Ropero</p><h1>Plantillas de perforación 1:1</h1>
<p>Hojas tamaño carta a escala real. Pega la plantilla sobre la pieza alineando los <b>cantos de referencia</b> (línea gruesa) y perfora en cada cruz.</p>
<p class="w"><b>Imprimir al 100 %, sin ajustar</b> («Tamaño real», sin «Ajustar a la página»). Antes de usar, mide la regla de 10 cm de cada hoja.</p>
<a class="b" href="plantillas_ropero.pdf">Descargar PDF ({tot} hojas)</a><a class="b" style="background:#fff;color:#1F2A2E;border:1px solid #ccc" href="#" onclick="print();return false">Imprimir</a><a class="b" style="background:#fff;color:#1F2A2E;border:1px solid #ccc" href="../#armado">← Volver al armado</a>
<h3>Índice</h3><ul>{"".join(f'<li id="p{f["no"]:02d}"><a href="#h{n}">{f["no"]:02d} · {esc(f["name"])}</a>{" — <b style=color:#D9502B>pendiente</b>" if f["pend"] else ""} (hoja {n})</li>' for f,n in idx)}</ul>
<p style="font-size:13px;color:#6B7B78">El fondo (13–14) y la cara superior del piso no llevan plantilla: sus tornillos se marcan con cinta y escuadra (ver lámina del paso).</p></div>
{"".join(f'<a id="h{n}"></a>'+page_svg(pg,n,tot) for n,pg in enumerate(pages,1))}
</body></html>'''
open('/workspace/studio/ropero/plantillas/index.html','w').write(html)
print('pages',tot,[ (f['id'],n) for f,n in idx])
