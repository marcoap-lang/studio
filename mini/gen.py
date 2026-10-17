import json,html
X=json.load(open('/workspace/ropero/extras.json'));XB={e['id']:e for e in X}
M18,M5,CANTO=801/2.9768,233/2.9768,12
def P(i,b,jute=False): e=XB.get(i);return dict(id=i,b=b,t=e['T'] if e else 18,jute=jute)
PROJ={
'buro':dict(n='Buró Pino & Yute',no='02',cat='Recámara',pref='B',size=[360,518,355],
 lead='36 × 51.8 × 35.5 cm. Buró abierto de triplay de pino con fondo forrado de yute, a juego con el ropero. Sale de los sobrantes de sus hojas.',
 chips=['Triplay de pino 18 mm','Fondo 5 mm con yute','Cubrecanto de pino','Linaza y cera de abeja'],
 parts=[P('B03',[0,0,5,18,500,350]),P('B04',[342,0,5,18,500,350]),P('B07',[18,0,5,324,50,18]),P('B06',[18,0,307,324,50,18]),P('B02',[18,50,5,324,18,350]),P('B01',[0,500,5,360,18,350]),P('B05',[0,0,0,360,500,5]),dict(id='yute',b=[18,68,5,324,432,1],t=1,jute=True)],
 steps=[dict(t='Lija y cubrecanto',d='Lija todas las piezas con grano 120 y luego 180. Pega el cubrecanto con plancha (sin vapor, temperatura media) en el canto frontal de B01, B02, B03 y B04. Recorta el sobrante con cúter y lija el borde a 45°.',n=['B01','B02','B03','B04'],tools=['Plancha','Cúter o recortador de cubrecanto','Lija 120 y 180'],hw=[],min=30),
  dict(t='Perfora los bolsillos (Kreg)',d='Con la plantilla Kreg ajustada a 3/4″ (18 mm): B01 y B02, 2 bolsillos por lado en la cara inferior, a 60 mm del frente y de atrás. Zoclos B06 y B07, 1 bolsillo por extremo en la cara de atrás.',n=['B01','B02','B06','B07'],tools=['Taladro','Plantilla Kreg + broca escalonada 3/8″'],hw=[],min=20),
  dict(t='Base y zoclos',d='Atornilla la base B02 entre los costados con su cara superior a 68 mm del piso (usa un taco separador de 50 mm bajo la base). El zoclo de atrás B07 va al ras de atrás; el de frente B06 queda remetido 30 mm. Cola + tornillo pocket.',n=['B03','B04','B02','B06','B07'],tools=['Taladro','Prensas','Escuadra','Taco separador 50 mm'],hw=['8 tornillos pocket #8 × 1¼″','Cola blanca'],min=30),
  dict(t='Cubierta',d='Coloca la cubierta B01 encima de los costados, al ras atrás y a los lados, y atorníllala desde abajo por los bolsillos. Revisa escuadra midiendo las diagonales del frente.',n=['B01'],tools=['Taladro','Prensas','Escuadra'],hw=['4 tornillos pocket #8 × 1¼″','Cola blanca'],min=15),
  dict(t='Fondo con yute',d='Corta el yute 20 mm más grande que la cara frontal del fondo B05. Pégalo con Resistol 850 y engrápalo por la orilla con grapa de 8 mm cada 30 mm (quedará oculto). Atornilla el fondo por detrás a costados, cubierta y base con #6 × 5/8″ cada 120 mm: eso deja el mueble a escuadra.',n=['B05','yute'],tools=['Engrapadora de tapicero','Taladro con broca 2 mm','Desarmador'],hw=['14 tornillos #6 × 5/8″','Grapas 8 mm','Yute (sobrante del ropero)'],min=30),
  dict(t='Acabado',d='Aplica aceite de linaza con trapo, deja secar 24 h, lija suave con 320 y pule con cera de abeja. Pon 4 topes de fieltro abajo.',n=[],tools=['Trapo de algodón','Lija 320'],hw=['Linaza y cera (sobrante del ropero)','4 topes de fieltro'],min=30)],
 buy=[('Cubrecanto de pino 19 mm (incluido en el pedido del ropero)','Ya va en el pedido de Triplay Market: 1.7 m de los 26.6 m.','—'),('Tornillo pocket #8 × 1¼″ cabeza de rondana, rosca gruesa','«Tornillo para bolsillo Kreg de 1¼ pulgada, rosca gruesa» (bolsa de 100 alcanza para los 3 muebles).','$95 la bolsa'),('Pija para madera #6 × 5/8″ cabeza plana','«Pija cabeza plana del 6 por cinco octavos».','$25'),('Topes de fieltro autoadheribles','«Fieltro autoadherible redondo de 2 cm».','$25')],
 extra=[('Cubrecanto 1.7 m','',CANTO*1.7),('Tornillería (parte proporcional)','',45),('Topes de fieltro','',25)]),
'repisa':dict(n='Repisa de pared',no='03',cat='Recámara · Pared',pref='R',size=[936,400,150],
 lead='93.6 × 40 × 15 cm. Repisa de 3 entrepaños de triplay de pino que se cuelga de un listón oculto. Sale de los sobrantes del ropero.',
 chips=['Triplay de pino 18 mm','3 entrepaños','Listón de colgar oculto','Linaza y cera de abeja'],
 parts=[P('R04',[0,0,0,18,400,150]),P('R05',[918,0,0,18,400,150]),P('R01',[18,0,0,900,18,150]),P('R02',[18,191,0,900,18,150]),P('R03',[18,382,0,900,18,150]),P('R06',[18,322,0,900,60,18])],
 steps=[dict(t='Lija y cubrecanto',d='Lija con 120 y 180. Cubrecanto en el canto frontal de los 3 entrepaños (R01–R03) y de los 2 costados (R04, R05).',n=['R01','R02','R03','R04','R05'],tools=['Plancha','Cúter','Lija 120 y 180'],hw=[],min=30),
  dict(t='Bolsillos',d='Kreg a 3/4″: cada entrepaño lleva 2 bolsillos por extremo en la cara inferior (a 30 mm del frente y de atrás). El listón R06, 1 bolsillo por extremo.',n=['R01','R02','R03','R06'],tools=['Taladro','Plantilla Kreg'],hw=[],min=20),
  dict(t='Arma el cuerpo',d='Marca en los costados la cara inferior de cada entrepaño: 0, 191 y 382 mm. Atornilla R01 (abajo), R02 y R03 (arriba, al ras) con cola y tornillo pocket. Revisa escuadra.',n=['R04','R05','R01','R02','R03'],tools=['Taladro','Prensas','Escuadra','Flexómetro'],hw=['12 tornillos pocket #8 × 1¼″','Cola blanca'],min=30),
  dict(t='Listón de colgar',d='Mete el listón R06 de canto bajo el entrepaño superior, al ras de atrás. Atorníllalo a los costados por sus bolsillos y al entrepaño con 3 pijas #8 × 1¼″ desde arriba del listón (pretaladra 3 mm).',n=['R06'],tools=['Taladro','Broca 3 mm'],hw=['2 tornillos pocket #8 × 1¼″','3 pijas #8 × 1¼″'],min=15),
  dict(t='Acabado',d='Linaza, 24 h de secado, lija 320 y cera de abeja.',n=[],tools=['Trapo','Lija 320'],hw=['Linaza y cera (sobrante del ropero)'],min=20),
  dict(t='Cuélgala',d='Pon la repisa contra la pared y marca 3 puntos a través del listón R06 (centro y a 100 mm de cada costado). Taquete de 5/16″ y pija #10 × 2½″ en muro de block o concreto; en tablaroca usa taquete mariposa. Nivela antes de apretar. Carga sugerida: 8 kg por entrepaño.',n=[],tools=['Taladro con broca para concreto 5/16″','Nivel','Desarmador'],hw=['3 taquetes 5/16″','3 pijas #10 × 2½″'],min=20)],
 buy=[('Cubrecanto de pino 19 mm (incluido en el pedido del ropero)','3.5 m de los 26.6 m.','—'),('Tornillo pocket #8 × 1¼″ (misma bolsa que el buró)','«Tornillo para bolsillo Kreg de 1¼ pulgada».','—'),('Pija para madera #8 × 1¼″ cabeza plana','«Pija cabeza plana del 8 por una y cuarto».','$25'),('Taquete de plástico 5/16″ + pija #10 × 2½″','«Taquete de 5/16 con su pija del 10 de dos y media» (para concreto o block). En tablaroca: «taquete mariposa».','$30')],
 extra=[('Cubrecanto 3.5 m','',CANTO*3.5),('Tornillería (parte proporcional)','',40),('Taquetes y pijas de pared','',30)]),
'banca':dict(n='Banca zapatera',no='04',cat='Entrada · Recámara',pref='Z',size=[760,398,331],
 lead='76 × 39.8 × 33.1 cm. Banca baja de tablas de triplay de pino para sentarse a ponerse los zapatos y guardarlos debajo. Sale de los sobrantes del ropero.',
 chips=['Triplay de pino 18 mm','Asiento de 3 tablas','Cubrecanto en ambos cantos','Linaza y cera de abeja'],
 parts=[P('Z04',[0,0,59.5,18,380,212]),P('Z05',[742,0,59.5,18,380,212]),P('Z06',[18,60,59.5,724,100,18]),P('Z01',[0,380,0,760,18,105]),P('Z02',[0,380,113,760,18,105]),P('Z03',[0,380,226,760,18,105])],
 steps=[dict(t='Lija y cubrecanto',d='Lija con 120 y 180. Cubrecanto en los DOS cantos largos de cada tabla del asiento (Z01–Z03), en el canto frontal de los costados (Z04, Z05) y del travesaño Z06. Redondea un poco las esquinas de las tablas con lija.',n=['Z01','Z02','Z03','Z04','Z05','Z06'],tools=['Plancha','Cúter','Lija 120 y 180'],hw=[],min=40),
  dict(t='Bolsillos',d='Kreg a 3/4″: travesaño Z06, 2 bolsillos por extremo. Cada tabla del asiento, 2 bolsillos por extremo en la cara inferior, a 25 mm de cada canto largo.',n=['Z06','Z01','Z02','Z03'],tools=['Taladro','Plantilla Kreg'],hw=[],min=20),
  dict(t='Costados y travesaño',d='Atornilla el travesaño Z06 entre los costados, al ras de atrás y a 60 mm del piso. Cola + tornillo pocket. Revisa escuadra.',n=['Z04','Z05','Z06'],tools=['Taladro','Prensas','Escuadra'],hw=['4 tornillos pocket #8 × 1¼″','Cola blanca'],min=20),
  dict(t='Asiento',d='Coloca las 3 tablas sobre los costados, al ras de los lados, con 8 mm de separación entre ellas (usa 2 tacos de 8 mm) y 59.5 mm de vuelo al frente y atrás. Atorníllalas desde abajo por sus bolsillos con cola.',n=['Z01','Z02','Z03'],tools=['Taladro','Prensas','Tacos separadores 8 mm','Flexómetro'],hw=['12 tornillos pocket #8 × 1¼″','Cola blanca'],min=25),
  dict(t='Acabado',d='Linaza, 24 h de secado, lija 320, cera de abeja. Topes de fieltro bajo los costados.',n=[],tools=['Trapo','Lija 320'],hw=['Linaza y cera (sobrante del ropero)','4 topes de fieltro'],min=25)],
 buy=[('Cubrecanto de pino 19 mm (incluido en el pedido del ropero)','6.1 m de los 26.6 m.','—'),('Tornillo pocket #8 × 1¼″ (misma bolsa)','«Tornillo para bolsillo Kreg de 1¼ pulgada».','—'),('Topes de fieltro autoadheribles','«Fieltro autoadherible de 2 cm».','$25')],
 extra=[('Cubrecanto 6.1 m','',CANTO*6.04),('Tornillería (parte proporcional)','',40),('Topes de fieltro','',25)]),
}
HEAD=open('/workspace/studio/ropero/index.html').read().split('<body>')[0]
for key,p in PROJ.items():
    ps=[e for e in X if e['id'].startswith(p['pref'])]
    a18=sum(e['L']*e['W'] for e in ps if e['T']==18)/1e6;a5=sum(e['L']*e['W'] for e in ps if e['T']==5)/1e6
    share=a18*M18+a5*M5;ext=sum(v for *_,v in p['extra']);canto=sum(sum(e['band']) for e in ps)/1000
    mins=sum(s['min'] for s in p['steps'])
    for s in p['steps']: s['hw']=s['hw'] or []
    data=dict(size=p['size'],parts=p['parts'],steps=[dict(n=s['n']) for s in p['steps']])
    head=HEAD.replace('<title>Ropero de pino y yute · Strate Studio</title>',f"<title>{p['n']} · Strate Studio</title>")
    import re
    head=head.replace('href="style.css"','href="../ropero/style.css"')
    head=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{html.escape(p["lead"])}">',head)
    rows=''.join(f"<tr><td><b>{e['id']}</b></td><td>{e['n']}</td><td>{e['L']} × {e['W']} × {e['T']}</td><td>{' + '.join(map(str,e['band'])) or '—'}</td><td>Hoja {e['s']}</td></tr>" for e in ps)
    bud=''.join(f"<tr><td>{a}</td><td style='text-align:right'>${v:,.0f}</td></tr>" for a,_,v in p['extra'])
    steps=''.join(f'''<div class="card stp" data-i="{i}" style="margin-top:12px"><label class="ck" style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" data-k="{key}_s{i}"><div style="flex:1"><p class="eyebrow" style="margin:0">Paso {i+1} · {s['min']} min</p><h3 style="margin:2px 0 6px">{s['t']}</h3></div></label>
<p style="margin:0 0 8px">{s['d']}</p><div class="small"><b>Piezas:</b> {', '.join(s['n']) or '—'} · <b>Herramienta:</b> {', '.join(s['tools'])}{(' · <b>Tornillería y material:</b> '+', '.join(s['hw'])) if s['hw'] else ''}</div><button class="btn ghost" style="margin-top:8px;padding:6px 12px" onclick="show({i})">Ver en 3D</button></div>''' for i,s in enumerate(p['steps']))
    buy=''.join(f'''<label class="ck card" style="display:flex;gap:10px;margin-top:8px"><input type="checkbox" data-k="{key}_b{i}"><div><b>{a}</b><div class="small">Cómo pedirlo: {b}</div><div class="small">{c}</div></div></label>''' for i,(a,b,c) in enumerate(p['buy']))
    page=f'''{head}<body>
<header class="top"><div class="in"><a class="brand" href="../">Strate <span>Studio</span></a><nav><a href="#resumen">Resumen</a><a href="#presupuesto">Presupuesto</a><a href="#armado">Armado</a><a href="#compras">Compras</a></nav></div></header>
<main class="wrap">
<section class="hero"><p class="eyebrow">Proyecto {p['no']} · {p['cat']}</p><h1>{p['n']}</h1>
<p class="lead">{p['lead']}</p><div class="chips">{''.join(f'<span class="chip">{c}</span>' for c in p['chips'])}</div>
<p class="eyebrow" style="margin-top:22px">Modelo 3D</p><div class="stage" id="v3"><span class="hint">Gira con el dedo · pellizca para acercar</span></div>
<div class="row" style="gap:8px;margin-top:8px;flex-wrap:wrap"><button class="btn ghost" style="padding:6px 12px" onclick="show(-1)">Terminado</button><span class="small" id="cap">Mueble terminado</span></div></section>
<section class="blk" id="resumen"><p class="eyebrow">Resumen</p><h2>Lo que vas a construir</h2>
<div class="grid g4" style="margin-top:16px"><div class="card stat"><b>{len(ps)}</b><span>piezas de triplay</span></div><div class="card stat"><b>{len(p['steps'])}</b><span>pasos</span></div><div class="card stat"><b>≈{round(mins/60+.25,1)} h</b><span>de trabajo (+24 h secado)</span></div><div class="card stat"><b>{canto:.2f} m</b><span>de cubrecanto</span></div></div>
<div class="card" style="margin-top:14px"><h3>Piezas (salen de los sobrantes del ropero)</h3><div style="overflow-x:auto"><table class="list" style="width:100%;font-size:14px"><tr><th>#</th><th>Pieza</th><th>Medida (mm)</th><th>Cubrecanto</th><th>Hoja</th></tr>{rows}</table></div>
<p class="small" style="margin-bottom:0">Ya están acomodadas en el <a href="../ropero/esquema_corte.pdf">esquema de corte</a> del ropero: mismas 6 hojas, sin hojas ni cortes extra (el corte se cobra por hoja).</p></div></section>
<section class="blk" id="presupuesto"><p class="eyebrow">Presupuesto</p><h2>≈ ${ext:,.0f} MXN extra</h2>
<p class="small">Precios estimados en MXN, Veracruz, octubre 2026. El triplay ya está pagado con el ropero.</p>
<div class="card"><table class="list" style="width:100%"><tr><th>Partida</th><th style="text-align:right">Subtotal</th></tr>{bud}<tr><td><b>Total a desembolsar</b></td><td style="text-align:right"><b>${ext:,.0f}</b></td></tr>
<tr><td class="small">Valor del triplay de sobrante ({a18:.2f} m² de 18 mm{f' + {a5:.2f} m² de 5 mm' if a5 else ''}), ya incluido en las hojas del ropero</td><td class="small" style="text-align:right">${share:,.0f}</td></tr></table></div></section>
<section class="blk" id="armado"><p class="eyebrow">Armado</p><h2>Paso a paso</h2><p class="small">Marca cada paso al terminarlo; se guarda en tu teléfono. «Ver en 3D» resalta en naranja las piezas del paso.</p>{steps}</section>
<section class="blk" id="compras"><p class="eyebrow">Compras</p><h2>Lista de compras</h2>{buy}
<p class="small" style="margin-top:10px">Cola blanca (Resistol 850), linaza, cera de abeja, yute y grapas: los mismos del ropero; alcanza el sobrante.</p></section>
</main>
<footer><div class="wrap">Strate Studio · <a href="../ropero/">Ropero Pino &amp; Yute</a> · <a href="../ropero/esquema_corte.pdf">Esquema de corte (PDF)</a> · <a href="#" onclick="print();return false">Imprimir</a></div></footer>
<script>document.querySelectorAll('input[data-k]').forEach(c=>{{const k='strate_'+c.dataset.k;c.checked=!!localStorage.getItem(k);c.onchange=()=>localStorage.setItem(k,c.checked?'1':'')}});
const STEPT={json.dumps([s['t'] for s in p['steps']],ensure_ascii=False)};window.show=i=>{{window.__v&&window.__v.step(i);document.getElementById('cap').textContent=i<0?'Mueble terminado':'Paso '+(i+1)+' · '+STEPT[i];document.getElementById('v3').scrollIntoView({{behavior:'smooth',block:'center'}})}};</script>
<script type="module">import {{viewer}} from '../mini/mini.js';window.__v=viewer(document.getElementById('v3'),{json.dumps(data,ensure_ascii=False)});</script>
</body></html>'''
    import os;os.makedirs(f'/workspace/studio/{key}',exist_ok=True);open(f'/workspace/studio/{key}/index.html','w').write(page)
    print(key,len(ps),'piezas · extra $',round(ext),'· canto',canto)
json.dump({k:dict(n=v['n'],no=v['no'],cat=v['cat'],size=v['size'],piezas=len([e for e in X if e['id'].startswith(v['pref'])]),pasos=len(v['steps']),ext=round(sum(x[2] for x in v['extra']))) for k,v in PROJ.items()},open('/workspace/studio/mini/projects.json','w'),ensure_ascii=False)
