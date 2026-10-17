# Genera holes.js (caras, agujeros, uniones por paso) y plantillas/index.html (1:1, carta)
import json, math
U=json.load(open('/workspace/ropero/uniones.json'))
D=json.load(open('/workspace/ropero/data.json'));P=D['P'];H=D['H']
PK=dict(k='pocket',bit='Kreg escalonada 3/8″',cs='—',depth='collar a 3/4″ (18 mm)',screw='#8 × 1¼″ pocket rondana')
SD=dict(k='screw',bit='guía 3 mm',cs='avellanar 8 mm',depth='40 mm',screw='#8 × 1½″ cabeza plana')
SU=dict(k='support',bit='guía 3 mm',cs='—',depth='14 mm (tope)',screw='#8 × 5/8″ cabeza plana')
BK=dict(k='screw',bit='guía 2 mm',cs='avellanado ligero',depth='16 mm',screw='#6 × 5/8″ cabeza plana')
DR=dict(k='screw',bit='guía 2 mm',cs='avellanar al ras',depth='16 mm',screw='#6 × 5/8″ cabeza plana')
RL=dict(k='screw',bit='guía 3 mm',cs='avellanar al ras',depth='16 mm',screw='#8 × 3/4″ cabeza plana')
WN=dict(k='win',bit='Ø10 mm',cs='—',depth='pasado',screw='— (arranque de caladora)')
VT=dict(k='vent',bit='sierra copa Ø25',cs='—',depth='pasado',screw='— (ventilación)')
F=[]
def face(id,no,name,L,W,xr,yr,holes,tpl=True,pend=None,mirror=False,count=1,cut=None):
    for h_ in holes: h_['xd']=round(L-h_['x'],1) if mirror else h_['x']
    F.append(dict(id=id,no=no,name=name,L=L,W=W,xr=xr,yr=yr,h=holes,tpl=tpl,pend=pend,mirror=mirror,count=count,cut=cut))
def hs(spec,u,pts): return [dict(x=round(x,1),y=round(y,1),u=u,**spec) for x,y in pts]
ends=lambda L,ys:[(20,y) for y in ys]+[(L-20,y) for y in ys]
face('03s',3,'Techo · cara superior',1564,547,'canto izquierdo (visto de frente)','canto frontal',
     hs(PK,'U02',ends(1564,[60,215,370,487]))+hs(SD,'U08',[(1186,537.5),(1219,537.5)]))
face('03i',3,'Techo · cara inferior (riel U-20)',1564,547,'canto izquierdo','canto frontal',hs(RL,'U15',[(40,30),(340,30),(640,30),(940,30),(1240,30),(1524,30)]))
face('04i',4,'Piso · cara inferior',1564,547,'canto izquierdo (visto de frente)','canto frontal',
     hs(PK,'U03',ends(1564,[90,230,370,487]))+hs(SD,'U08',[(1186,537.5),(1219,537.5)]),mirror=True)
xs=[50,250,450,650,914,1114,1314,1514]
face('04s',4,'Piso · cara superior (fijación al zócalo)',1564,547,'canto izquierdo','canto frontal',
     hs(SD,'U11',[(x,59) for x in xs]+[(x,538) for x in xs]+[(9,150),(9,400),(1555,150),(1555,400)]),tpl=False)
face('05d',5,'División · cara derecha',1914,482,'canto inferior','canto frontal',
     hs(PK,'U04',[(1894,y) for y in (60,241,422)])+hs(PK,'U05',[(20,y) for y in (60,241,422)])+hs(SU,'U13',[(1630-68,205)]),mirror=True)
face('05i',5,'División · cara izquierda',1914,482,'canto inferior','canto frontal',hs(SU,'U13',[(1832,205),(912,205)]))
face('01',1,'Costado 01 · cara interior',2000,547,'canto inferior (suelo)','canto frontal',hs(SU,'U12',[(1900,270),(980,270)]),mirror=True)
face('02',2,'Costado 02 · cara interior',2000,547,'canto inferior (suelo)','canto frontal',hs(SU,'U14',[(1630,270)]))
face('06',6,'Repisa 06 · cara inferior',773,461,'canto izquierdo','canto frontal',hs(PK,'U06',ends(773,[60,401])),mirror=True)
face('41',41,'Entrepaño 41 · cara inferior',773,482,'canto izquierdo','canto frontal',hs(PK,'U26',ends(773,[60,241,422])),mirror=True)
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
     hs(DR,'U18',[(s+a,b) for s in sq for a,b in ((20,20),(43,43))]),count=4)
OPN=D['OPN']
wpts=[(a+5,63+5) for a,b in OPN]+[(b-5,63+5) for a,b in OPN]+[(a+5,739-5) for a,b in OPN]+[(b-5,739-5) for a,b in OPN]
face('28v',28,'Tapas caladas 28–29 · cara buena (ventanas)',H,802,'canto inferior','canto izquierdo',hs(WN,'U27',wpts),count=2,cut=[(a,b,63,739) for a,b in OPN])
U['uniones'].append({"id":"U27","piezas":[28,29],"tipo":"corte","tornillo":"— (corte con caladora)","broca_guia":"Broca Ø10 mm para arrancar","broca_avellanado":None,"profundidad_mm":"pasado","cantidad":12,"posiciones_mm":[f"3 ventanas de 676 de ancho por tapa, de 63 a 739 desde el canto izquierdo; de {a:g} a {b:g} desde el canto inferior" for a,b in OPN]+["Barreno Ø10 en cada esquina, con el centro a 5 mm de los dos lados (da el radio 5 de la esquina)"],"cara":"Cara buena de las tapas 28 y 29","paso_armado":"12 · Bastidores y tapas caladas"})
U['uniones'].append({"id":"U26","piezas":[41,1,5],"tipo":"pocket","tornillo":"Pocket rosca gruesa #8 x 1-1/4\" (32 mm), cabeza de rondana","broca_guia":"Broca escalonada Kreg 3/8\" (plantilla y collar ajustados a 3/4\" / 18 mm)","broca_avellanado":None,"profundidad_mm":"según collar Kreg para 3/4\"","cantidad":6,"posiciones_mm":["3 por extremo: 60, 241 y 422 desde su canto frontal (entrepaño de 482)","Cara inferior a 1035 del suelo (967 desde canto inferior de la división; 1035 en costado 01)"],"cara":"Cara inferior del entrepaño 41","paso_armado":"7 · Repisa, zapatera y entrepaño rigidizador","nota":"Cola PVA exterior. Rigidiza costado 01 y división a media altura."})
U_by={u['id']:u for u in U['uniones']}
# uniones por paso
steps={}
for u in U['uniones']:
    n=int(u['paso_armado'].split('·')[0])-1; steps.setdefault(n,[]).append(u['id'])
steps[2]=['U01','U02','U03','U04','U05','U06','U07','U26','U12','U13','U14']  # paso 3: perforar
fix={'U15':{'tornillo':'#8 × 3/4″ (19 mm) cabeza plana — confirmar con ficha del riel'},
     'U18':{'tornillo':'#6 × 5/8″ (16 mm) cabeza plana'},'U19':{'tornillo':'#6 × 5/8″ (16 mm) cabeza plana'},
     'U06':{'posiciones_mm':['2 por extremo: 60 y 401 desde canto frontal (repisa de 461)','Cara superior a 1700 del suelo; se apoya contra el listón 15']},
     'U07':{'posiciones_mm':['2 por extremo: 60 y 271 desde canto frontal (zapatera de 331)','Cara superior a 270 del suelo']},
     'U13':{'posiciones_mm':['Cara izquierda: soportes 30 y 31 a 205 del canto frontal de la división (= 270 del frente del mueble); 1832 y 912 desde canto inferior (=1900 y 980 del suelo)','Cara derecha: soporte 32 a 205 del canto frontal de la división (= 270 del frente del mueble); 1562 desde canto inferior (=1630 del suelo)']},
     'U14':{'posiciones_mm':['Soporte tubo 32: 270 desde canto frontal, 1630 desde canto inferior (centro del tubo)']},
     'U20':{'posiciones_mm':['A 31.5 del canto exterior (centro del bastidor), perímetro y 2 travesaños intermedios, cada 50']},
     'U01':{'posiciones_mm':['1 bolsillo por extremo de cada travesaño (461 mm), centrado a 25 del canto inferior']}}
for k,v in fix.items(): U_by[k].update(v)
FER=U['ferreteria']
for f_ in FER:
    if f_['articulo'].startswith('Tornillo pocket'): f_['neto']+=6; f_['comprar']=46
for f_ in FER:
    if f_['articulo'].startswith('Tornillo #8 x 3/4'): f_['articulo']='Tornillo #8 × 3/4″ (19 mm) cabeza plana para riel — confirmar con ficha'
    f_['articulo']=f_['articulo'].replace(' (acordado #8 x 1\"; ver C08)','')

for uid,door,fr in (('U22','A',[16,17,20,21,22,23]),('U23','B',[18,19,24,25,26,27])):
    U_by[uid].update(piezas=fr+[39,40],cantidad=245,tornillo='Grapa 8 mm (yute)',posiciones_mm=[f'Puerta {door}: yute sobre la cara frontal del bastidor; grapas a 10 mm por fuera del borde de cada hueco, cada 30, del centro de cada lado hacia las esquinas (quedan bajo la tapa calada)'],cara=f'Cara frontal del bastidor de la Puerta {door}',paso_armado='13 · Yute sobre el bastidor')
for uid in ('U20','U21'):
    U_by[uid].update(tornillo='Grapa tapicera 14 mm (9/16″) + Resistol 850',paso_armado='14 · Tapa calada sobre el yute',posiciones_mm=['A 31.5 del canto exterior (centro del bastidor) y sobre los 2 travesaños intermedios, cada 50; pasa la tapa de 5 mm y el margen de yute'])
for uid in ('U24','U25'): U_by.pop(uid,None)
FER[:]=[f_ for f_ in FER if not f_['articulo'].startswith('Clavo sin cabeza')]
steps={}
for u in U_by.values():
    n=int(u['paso_armado'].split('·')[0])-1; steps.setdefault(n,[]).append(u['id'])
steps[2]=['U01','U02','U03','U04','U05','U06','U07','U26','U12','U13','U14']
for f_ in FER:
    if f_['articulo'].startswith('Grapa 8 mm'): f_['neto']=490; f_['comprar']=540
open('/workspace/studio/ropero/holes.js','w').write('window.FACES='+json.dumps(F,ensure_ascii=False)+';\nwindow.UNI='+json.dumps(U_by,ensure_ascii=False)+';\nwindow.STEPU='+json.dumps(steps)+';\nwindow.FER='+json.dumps(FER,ensure_ascii=False)+';\n')
exec(open('/workspace/studio/ropero/src/gen_tpl.py').read())
