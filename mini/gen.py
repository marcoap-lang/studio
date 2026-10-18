# Genera /buro/, /repisa/, /banca/ al nivel del ropero: 3D por paso, resumen, presupuesto, comparación,
# paso a paso marcable con lámina de detalle y plantillas 1:1 por paso (PDF).
import json,html,os,re,math
X=json.load(open('/workspace/ropero/extras.json'));XB={e['id']:e for e in X}
M18,M5=801/2.9768,233/2.9768;CANTO=8.23
# --- herrajes (nombres de ferretería mexicana)
PK=dict(k='pocket',bit='Kreg escalonada 3/8″',cs='—',depth='collar a 3/4″ (18 mm)',screw='#8 × 1¼″ pocket rondana')
FD=dict(k='screw',bit='guía 2 mm',cs='avellanado ligero',depth='16 mm',screw='#6 × 5/8″ cabeza plana')
TP=dict(k='screw',bit='guía 3 mm',cs='avellanar 8 mm',depth='32 mm',screw='#8 × 1¼″ cabeza plana')
MU=dict(k='screw',bit='pasado 5 mm (pared: concreto 5/16″)',cs='—',depth='pasado 18 mm',screw='#10 × 2½″ + taquete 5/16″')
def P(i,b,jute=False): e=XB.get(i);return dict(id=i,b=b,t=e['T'] if e else 18,jute=jute)
def J(id,piezas,tornillo,cantidad,guia,av,prof,cara,pos,herr,nota=''):return dict(id=id,piezas=piezas,tornillo=tornillo,cantidad=cantidad,broca_guia=guia,broca_avellanado=av,profundidad=prof,cara=cara,pos=pos,herr=herr,nota=nota)
KREG='Plantilla Kreg + broca escalonada 3/8″ con collar a 3/4″; punta cuadrada #2'
PROJ={
'buro':dict(n='Buró Pino & Yute',no='02',cat='Recámara',pref='B',size=[360,518,355],
 lead='36 × 51.8 × 35.5 cm. Buró abierto de triplay de pino con fondo forrado de yute, a juego con el ropero. Sus piezas van en las mismas 6 hojas del pedido.',
 chips=['Triplay de pino 18 mm','Fondo 5 mm con yute','Cubrecanto de pino','Linaza y cera de abeja'],
 parts=[P('B03',[0,0,5,18,500,350]),P('B04',[342,0,5,18,500,350]),P('B07',[18,0,5,324,50,18]),P('B06',[18,0,307,324,50,18]),P('B02',[18,50,5,324,18,350]),P('B05',[0,0,0,360,500,5]),dict(id='yute',b=[18,68,5,324,432,1],t=1,jute=True),P('B01',[0,500,0,360,18,355])],
 faces=[dict(id='B02i',no='B02',name='Base B02 · cara inferior',L=324,W=350,xr='canto izquierdo (visto de frente)',yr='canto frontal',h=[('J1',PK,[(20,60),(20,290),(304,60),(304,290)])],mirror=True),
  dict(id='B06',no='B06',name='Zoclos B06 y B07 · cara trasera',L=324,W=50,xr='extremo izquierdo',yr='canto inferior',h=[('J2',PK,[(20,25),(304,25)])],count=2),
  dict(id='B03',no='B03',name='Costados B03 y B04 · cara interior',L=500,W=350,xr='canto inferior (suelo)',yr='canto frontal',h=[('J4',PK,[(480,60),(480,290)])],count=2,vis='cara interior (la que mira al hueco)'),
  dict(id='B05',no='B05',name='Fondo B05 · cara trasera',L=360,W=500,xr='canto izquierdo (visto por detrás)',yr='canto inferior (suelo)',h=[('J3',FD,[(9,y) for y in (30,150,270,390,480)]+[(351,y) for y in (30,150,270,390,480)]+[(100,25),(260,25),(100,59),(260,59)])],mirror=True)],
 joints=[J('J1',['B02','B03','B04'],'Tornillo pocket #8 × 1¼″ rosca gruesa',4,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara inferior de la base B02 (queda en el hueco del zoclo, no se ve)',['2 por extremo, a 60 mm del frente y de atrás, a 20 mm del canto'],KREG),
  J('J2',['B06','B07','B03','B04'],'Tornillo pocket #8 × 1¼″ rosca gruesa',4,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara trasera de los zoclos B06 y B07 (miran hacia dentro, bajo la base)',['1 por extremo, al centro de los 50 mm de alto'],KREG),
  J('J3',['B05','B03','B04','B02','B07'],'Pija para madera #6 × 5/8″ cabeza plana',14,'2 mm','avellanado ligero','16 mm','Cara trasera del fondo B05 (la que va contra la pared)',['Costados: a 9 mm de cada orilla, a 30, 150, 270, 390 y 480 del suelo','Zoclo trasero: 2 a 25 mm del suelo; base: 2 a 59 mm (centro de su canto)'],'Taladro, broca 2 mm, avellanador, desarmador'),
  J('J4',['B03','B04','B01'],'Tornillo pocket #8 × 1¼″ rosca gruesa',4,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara interior de los costados B03 y B04, arriba',['2 por costado, a 60 y 290 mm del frente, el bolsillo apuntando hacia arriba (a la cubierta)'],KREG,'Quedan pegados bajo la cubierta, por dentro: de frente no se ven. Ninguna pija atraviesa la cubierta: su cara superior queda limpia.'),
  J('J5',['yute','B05'],'Grapa para engrapadora de tapicero 8 mm (5/16″)',60,'—','—','—','Cara frontal del fondo B05',['Cada 30 mm por la orilla, a 10 mm del borde, del centro hacia las esquinas'],'Engrapadora de tapicero')],
 steps=[dict(t='Lija y cubrecanto',d='Lija todas las piezas con grano 120 y luego 180. Pega el cubrecanto con plancha (sin vapor, temperatura media) en el canto frontal de B01, B02, B03 y B04. Recorta el exceso con cúter y lija el borde a 45°.',n=['B01','B02','B03','B04'],j=[],tools=['Plancha','Cúter o recortador de cubrecanto','Lija 120 y 180'],min=30),
  dict(t='Perfora los bolsillos (Kreg)',d='Con la plantilla Kreg en 3/4″ (18 mm) y las plantillas 1:1 de este paso: base B02, 2 bolsillos por extremo en la cara inferior; zoclos B06 y B07, 1 por extremo en la cara trasera; costados B03 y B04, 2 arriba en la cara interior para la cubierta.',n=[],f=['B02','B06','B07','B03','B04'],j=['J1','J2','J4'],tools=['Taladro','Plantilla Kreg + broca escalonada 3/8″','Punzón','Cinta masking'],min=25),
  dict(t='Base y zoclos',d='Atornilla la base B02 entre los costados con su cara superior a 68 mm del suelo (taco separador de 50 mm bajo la base). El zoclo trasero B07 va al ras de atrás; el frontal B06 queda remetido 30 mm. Cola + tornillo pocket. Revisa la escuadra.',n=['B03','B04','B02','B06','B07'],j=['J1','J2'],tools=['Taladro','Prensas','Escuadra','Taco separador 50 mm','Resistol 850'],min=30),
  dict(t='Fondo con yute',d='Corta el yute 20 mm más grande que el hueco (364 × 472 mm). Pégalo con Resistol 850 a la cara frontal del fondo B05 y engrápalo por la orilla cada 30 mm. Atornilla el fondo por detrás a costados, base y zoclo trasero con #6 × 5/8″ (plantilla del paso): deja el mueble a escuadra. La cubierta va después y tapa su canto superior.',n=['B05','yute'],j=['J5','J3'],tools=['Engrapadora de tapicero','Tijeras','Taladro con broca 2 mm','Avellanador','Desarmador'],min=35),
  dict(t='Cubierta',d='Coloca la cubierta B01 (360 × 355) encima de los costados, al ras a los lados y al ras de la cara trasera del fondo. Atorníllala desde abajo, por los bolsillos de la cara interior de los costados (bolsillo hacia arriba), con cola: ninguna pija atraviesa la cara superior. Revisa las diagonales del frente.',n=['B01'],j=['J4'],tools=['Taladro','Prensas','Escuadra','Resistol 850'],min=15),
  dict(t='Acabado',d='Aceite de linaza con trapo en capa delgada, retira el exceso a los 15 min y deja secar 24 h. Lija suave con 320 y pule con cera de abeja. El yute se queda sin tratar. Pon 4 topes de fieltro abajo. ⚠ Extiende los trapos con linaza a secar: pueden autoincendiarse.',n=[],j=[],tools=['Trapo de algodón','Lija 320','Guantes'],min=30)],
 hw=[('Tornillo pocket #8 × 1¼″ rosca gruesa (Kreg)','«Tornillo para bolsillo Kreg de 1¼ pulgada, rosca gruesa». Bolsa de 100 para los 3 muebles.',12,607/100),('Pija para madera #6 × 5/8″ cabeza plana','«Pija cabeza plana del 6 por cinco octavos» (caja de 100, Hillman en Home Depot).',14,132/100),('Grapa para engrapadora de tapicero 8 mm (5/16″)','«Grapa T50 de 5/16» (la misma caja del ropero).',60,75/1250),('Topes de fieltro autoadheribles','«Fieltro autoadherible de 2 cm».',4,25/4),('Resistol 850','La misma botella del ropero (≈50 g).',1,10),('Yute','≈0.2 m² del mismo rollo del ropero.',1,15),('Linaza y cera de abeja','Parte proporcional del ropero.',1,30)],
 compare=[('Hacerlo tú',None,'Triplay de pino 18 mm, cubrecanto y acabado natural.'),('Buró de pino macizo','≈$2,200–3,800','Mueblerías y tiendas departamentales (referencia aproximada).'),('Buró de melamina armable','≈$900–1,600','Tiendas de autoservicio (referencia aproximada); no es madera.'),('Buró de carpintero a medida','≈$3,000–5,000','Taller local en triplay o pino (referencia aproximada).')]),
'repisa':dict(n='Repisa de pared',no='03',cat='Recámara · Pared',pref='R',size=[936,400,150],
 lead='93.6 × 40 × 15 cm. Repisa de 3 entrepaños de triplay de pino que se cuelga de un listón oculto. Sus piezas van en las mismas 6 hojas del pedido.',
 chips=['Triplay de pino 18 mm','3 entrepaños','Listón de colgar oculto','Linaza y cera de abeja'],
 parts=[P('R04',[0,0,0,18,400,150]),P('R05',[918,0,0,18,400,150]),P('R01',[18,0,0,900,18,150]),P('R02',[18,191,0,900,18,150]),P('R03',[18,382,0,900,18,150]),P('R06',[18,322,0,900,60,18])],
 faces=[dict(id='R01',no='R01',name='Entrepaños R01, R02 y R03 · cara inferior',L=900,W=150,xr='extremo izquierdo (visto de frente)',yr='canto frontal',h=[('J1',PK,[(20,30),(20,120),(880,30),(880,120)])],count=3,mirror=True),
  dict(id='R06',no='R06',name='Listón R06 · cara trasera (contra la pared)',L=900,W=60,xr='extremo izquierdo (visto por detrás)',yr='canto inferior',h=[('J2',PK,[(20,30),(880,30)]),('J4',MU,[(100,30),(450,30),(800,30)])],mirror=True),
  dict(id='R06b',no='R06',name='Listón R06 · cara trasera · bolsillos hacia arriba (a R03)',L=900,W=60,xr='extremo izquierdo (visto por detrás)',yr='canto inferior',h=[('J3',PK,[(275,40),(625,40)])],mirror=True)],
 joints=[J('J1',['R01','R02','R03','R04','R05'],'Tornillo pocket #8 × 1¼″ rosca gruesa',12,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara inferior de cada entrepaño (bolsillo hacia el costado)',['2 por extremo, a 30 mm del frente y de atrás'],KREG,'R02 y R03 quedan ocultos. R01 es el único cuya cara inferior se ve desde abajo: sus 4 bolsillos se tapan con tapón Kreg de pino (cola, cortar al ras y lijar).'),
  J('J2',['R06','R04','R05'],'Tornillo pocket #8 × 1¼″ rosca gruesa',2,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara trasera del listón R06',['1 por extremo, al centro de sus 60 mm'],KREG),
  J('J3',['R06','R03'],'Tornillo pocket #8 × 1¼″ rosca gruesa',2,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara trasera del listón R06 (contra la pared), bolsillo apuntando hacia arriba',['A 275 y 625 del extremo izquierdo, a 40 del canto inferior; el tornillo sale por el canto superior del listón y muerde la cara inferior de R03'],KREG,'Antes eran 3 pijas desde la cara superior de R03, que se veían. Ahora la cara superior queda limpia.'),
  J('J4',['R06'],'Taquete de plástico 5/16″ + pija #10 × 2½″',3,'5 mm en el listón; 5/16″ para concreto en el muro','—','pasado el listón; 60 mm en el muro','Listón R06 (de la repisa al muro)',['A 100 mm de cada extremo y al centro (450), a media altura del listón'],'Taladro con broca para concreto 5/16″, broca para madera 3/8″, nivel, desarmador','La cara frontal del listón se ve al fondo del nivel superior: cajea Ø3/8″ × 6 mm en cada barreno para hundir la cabeza y tápalo con tapón de madera 3/8″ (cortado de taquete/varilla), apenas con una gota de cola para poder sacarlo si mudas la repisa. En tablaroca usa taquete mariposa.')],
 steps=[dict(t='Lija y cubrecanto',d='Lija con 120 y 180. Cubrecanto en el canto frontal de los 3 entrepaños (R01–R03) y de los 2 costados (R04, R05).',n=['R01','R02','R03','R04','R05'],j=[],tools=['Plancha','Cúter','Lija 120 y 180'],min=30),
  dict(t='Bolsillos y barrenos',d='Kreg en 3/4″ con las plantillas 1:1: cada entrepaño, 2 bolsillos por extremo en la cara inferior; el listón R06, 1 por extremo y 2 al centro (a 275 y 625, bolsillo hacia arriba para R03), todos en su cara trasera, la que va contra la pared. Marca también los 3 barrenos de muro del listón y cajéalos Ø3/8″ × 6 mm por la cara frontal. Ningún bolsillo va en cara superior ni frontal.',n=[],f=['R01','R02','R03','R06'],j=['J1','J2','J3','J4'],tools=['Taladro','Plantilla Kreg','Broca 3 y 5 mm','Punzón','Cinta masking'],min=25),
  dict(t='Arma el cuerpo',d='Marca en los costados la cara inferior de cada entrepaño: 0, 191 y 382 mm. Atornilla R01 (abajo), R02 y R03 (arriba, al ras) con cola y tornillo pocket; los bolsillos siempre en la cara inferior. Revisa escuadra. Pega tapones Kreg de pino en los 4 bolsillos de R01 (el único que se ve desde abajo); cuando seque, córtalos al ras con serrucho japonés o formón y lija 180.',n=['R04','R05','R01','R02','R03'],j=['J1'],tools=['Taladro','Prensas','Escuadra','Flexómetro','Resistol 850','Tapones Kreg de pino','Serrucho japonés o formón'],min=40),
  dict(t='Listón de colgar',d='Mete el listón R06 de canto bajo el entrepaño superior, al ras de atrás. Atorníllalo a los costados por sus bolsillos y fíjalo a R03 con cola y 2 tornillos pocket desde los bolsillos de su cara trasera, que suben hacia la cara inferior del entrepaño. La cara superior de R03 queda limpia.',n=['R06'],j=['J2','J3'],tools=['Taladro','Punta cuadrada #2','Resistol 850'],min=15),
  dict(t='Acabado',d='Linaza en capa delgada, 24 h de secado, lija 320 y cera de abeja. ⚠ Extiende los trapos con linaza a secar.',n=[],j=[],tools=['Trapo','Lija 320','Guantes'],min=20),
  dict(t='Cuélgala',d='Pon la repisa contra la pared, nivélala y marca los 3 puntos a través del listón. Atornilla con la cabeza hundida en el cajeado de 3/8″ y tápalo con tapón de madera de 3/8″ (cortado al ras y lijado). Taquete de 5/16″ y pija #10 × 2½″ en muro de block o concreto; en tablaroca usa taquete mariposa. Carga sugerida: 8 kg por entrepaño.',n=[],f=['R06'],j=['J4'],tools=['Taladro con broca para concreto 5/16″','Nivel','Desarmador'],min=20)],
 hw=[('Tornillo pocket #8 × 1¼″ rosca gruesa (Kreg)','«Tornillo para bolsillo Kreg de 1¼ pulgada» (misma bolsa que el buró).',16,607/100),('Tapones Kreg de pino para bolsillo (bolsa de 50)','«Kreg P-PIN, tapones de pino para pocket hole». Para los 4 bolsillos de R01; sobran para retoques.',1,330),('Broca para madera 3/8″ (punta de centro) + varilla/taquete de madera 3/8″','«Broca de 3/8 para madera y una varilla de madera de 3/8» para los 3 tapones del listón.',1,95),('Taquete de plástico 5/16″ + pija #10 × 2½″','«Taquete de 5/16 con su pija del 10 de dos y media» (paquete).',3,10),('Resistol 850','La misma botella del ropero.',1,10),('Linaza y cera de abeja','Parte proporcional del ropero.',1,25)],
 compare=[('Hacerla tú',None,'Triplay de pino 18 mm con listón oculto.'),('Repisa de pino de 3 niveles','≈$900–1,800','Tiendas departamentales y en línea (referencia aproximada).'),('Repisas flotantes (3 pzas)','≈$600–1,200','Melamina o MDF (referencia aproximada).'),('Repisa a medida de carpintero','≈$1,500–2,500','Taller local (referencia aproximada).')]),
'banca':dict(n='Banca zapatera',no='04',cat='Entrada · Recámara',pref='Z',size=[760,398,331],
 lead='76 × 39.8 × 33.1 cm. Banca baja de tablas de triplay de pino para sentarse a ponerse los zapatos y guardarlos debajo. Sus piezas van en las mismas 6 hojas del pedido.',
 chips=['Triplay de pino 18 mm','Asiento de 3 tablas','Cubrecanto en ambos cantos','Linaza y cera de abeja'],
 parts=[P('Z04',[0,0,59.5,18,380,212]),P('Z05',[742,0,59.5,18,380,212]),P('Z06',[18,60,59.5,724,100,18]),P('Z01',[0,380,0,760,18,105]),P('Z02',[0,380,113,760,18,105]),P('Z03',[0,380,226,760,18,105])],
 faces=[dict(id='Z06',no='Z06',name='Travesaño Z06 · cara trasera',L=724,W=100,xr='extremo izquierdo (visto por detrás)',yr='canto inferior',h=[('J1',PK,[(20,25),(20,75),(704,25),(704,75)])],mirror=True),
  dict(id='Z04',no='Z04',name='Costados Z04 y Z05 · cara interior',L=380,W=212,xr='canto inferior (suelo)',yr='canto frontal',h=[('J2',PK,[(360,22.75),(360,106),(360,189.25)])],count=2,vis='cara interior (la que mira al hueco)')],
 joints=[J('J1',['Z06','Z04','Z05'],'Tornillo pocket #8 × 1¼″ rosca gruesa',4,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara trasera del travesaño Z06 (contra la pared)',['2 por extremo, a 25 y 75 mm de su canto inferior'],KREG,'Si la banca queda exenta (sin pared atrás), tapa estos 4 bolsillos con tapón Kreg de pino (misma bolsa de la repisa).'),
  J('J2',['Z04','Z05','Z01','Z02','Z03'],'Tornillo pocket #8 × 1¼″ rosca gruesa',6,'Kreg escalonada 3/8″','—','collar a 3/4″ (18 mm)','Cara interior de los costados, arriba',['3 por costado, uno por tabla: a 22.75, 106 y 189.25 mm del canto frontal, el bolsillo apuntando hacia arriba (quedan bajo el asiento, por dentro)'],KREG,'Ninguna pija atraviesa las tablas del asiento: su cara superior queda limpia.')],
 steps=[dict(t='Lija y cubrecanto',d='Lija con 120 y 180. Cubrecanto en los DOS cantos largos de cada tabla del asiento (Z01–Z03), en el canto frontal de los costados (Z04, Z05) y del travesaño Z06. Redondea un poco las esquinas de las tablas con lija.',n=['Z01','Z02','Z03','Z04','Z05','Z06'],j=[],tools=['Plancha','Cúter','Lija 120 y 180'],min=40),
  dict(t='Bolsillos',d='Kreg en 3/4″ con las plantillas 1:1: travesaño Z06, 2 bolsillos por extremo en su cara trasera; costados Z04 y Z05, 3 bolsillos arriba en la cara interior (uno por tabla del asiento).',n=[],f=['Z06','Z04','Z05'],j=['J1','J2'],tools=['Taladro','Plantilla Kreg','Punzón','Cinta masking'],min=20),
  dict(t='Costados y travesaño',d='Atornilla el travesaño Z06 entre los costados, al ras de atrás y a 60 mm del suelo. Cola + tornillo pocket. Revisa escuadra.',n=['Z04','Z05','Z06'],j=['J1'],tools=['Taladro','Prensas','Escuadra','Resistol 850'],min=20),
  dict(t='Asiento',d='Coloca las 3 tablas sobre los costados, al ras de los lados, con 8 mm de separación (2 tacos de 8 mm) y 59.5 mm de vuelo al frente y atrás. Atorníllalas desde abajo, por los bolsillos de la cara interior de los costados, con cola: el asiento queda sin una sola pija a la vista.',n=['Z01','Z02','Z03'],j=['J2'],tools=['Taladro','Prensas','Tacos separadores 8 mm','Flexómetro','Resistol 850'],min=25),
  dict(t='Acabado',d='Linaza, 24 h de secado, lija 320, cera de abeja. Topes de fieltro bajo los costados. ⚠ Extiende los trapos con linaza a secar.',n=[],j=[],tools=['Trapo','Lija 320','Guantes'],min=25)],
 hw=[('Tornillo pocket #8 × 1¼″ rosca gruesa (Kreg)','«Tornillo para bolsillo Kreg de 1¼ pulgada» (misma bolsa).',10,607/100),('Topes de fieltro autoadheribles','«Fieltro autoadherible de 2 cm».',4,25/4),('Resistol 850','La misma botella del ropero.',1,10),('Linaza y cera de abeja','Parte proporcional del ropero.',1,30)],
 compare=[('Hacerla tú',None,'Triplay de pino 18 mm, asiento de tablas.'),('Banca zapatera de madera','≈$1,800–3,200','Tiendas departamentales y en línea (referencia aproximada).'),('Banca zapatera de melamina','≈$900–1,500','Autoservicio (referencia aproximada).'),('Banca a medida de carpintero','≈$2,500–4,000','Taller local (referencia aproximada).')]),
}
# ---------- plantillas 1:1 (reutiliza el motor del ropero) ----------
src=open('/workspace/studio/ropero/src/gen_tpl.py').read().split('\nTF=')[0]
class N(str):
    def __format__(s,spec):return str(s)
def mk_tpl(key,p):
    ns={}
    s=src.replace("'STRATE STUDIO · ROPERO PINO & YUTE'","BRAND")
    s=re.sub(r"\n    g2.append\(f'<rect x=\"\{MX\}\" y=\"\{y\}\" width=\"\{CW\}\" height=\"26\".*?\n","\n",s)
    s=re.sub(r"'Sierra copa ⌀25 \(ventilación del fondo\)',","",s)
    full=open('/workspace/studio/ropero/src/gen_tpl.py').read()
    s+='\n'+re.search(r"\nCSS='''.*?'''",full,re.S).group(0)+'\n'+re.search(r"\nHEAD=.*",full).group(0)+'\n'
    exec(s,ns);ns['BRAND']='STRATE STUDIO · '+p['n'].upper()
    F=[]
    for f in p['faces']:
        hl=[]
        for u,spec,pts in f['h']:
            for x,y in pts:hl.append(dict(x=x,y=y,xd=round(f['L']-x,1) if f.get('mirror') else x,u=u,**spec))
        F.append(dict(id=f['id'],no=N(f['no']),name=f['name'],L=f['L'],W=f['W'],xr=f['xr'],yr=f['yr'],h=hl,tpl=True,pend=None,mirror=f.get('mirror',False),count=f.get('count',1),cut=None))
        ns['VIS'][f['id']]=f.get('vis',f['name'].split(' · ')[-1])
    SH={f['id']:ns['sheets_of'](f) for f in F}
    def build(fs,step):
        pages=ns['guide']();tot=2+sum(len(SH[f['id']]) for f in fs);pn=2
        for f in fs:
            n=len(SH[f['id']])
            for k,s_ in enumerate(SH[f['id']],1):pn+=1;pages.append(ns['sheet_svg'](f,s_,k,n,pn,tot,step))
        return pages
    OUT=f'/workspace/studio/{key}/plantillas/';os.makedirs(OUT,exist_ok=True)
    for fn in os.listdir(OUT):os.remove(OUT+fn)
    HEAD=ns['HEAD'];steppdf={}
    for i,st in enumerate(p['steps']):
        fs=[f for f in F if any(h['u'] in st['j'] for h in f['h'])]
        if not fs or not (i==1 or st['t'].startswith('Fondo')):continue
        pages=build(fs,i+1);nn=f'{i+1:02d}'
        steppdf[i]=dict(file=f'plantillas_paso_{nn}.pdf',html=f'paso_{nn}.html',pages=len(pages),fs=fs)
        open(OUT+f'paso_{nn}.html','w').write(HEAD.replace('{t}',f'Plantillas paso {i+1} · {p["n"]}')+f'<div class="intro"><h1>Plantillas · paso {i+1}</h1><a class="b" href="plantillas_paso_{nn}.pdf">Descargar PDF ({len(pages)} hojas)</a><a class="b g" href="./">Todas las plantillas</a></div>'+''.join(pages)+'</body></html>')
    pages=build(F,None)
    stp=''.join(f'<li><a href="{v["file"]}">Paso {i+1} · {html.escape(p["steps"][i]["t"])}</a> — {v["pages"]} hojas ({", ".join(f["no"] for f in v["fs"])}) · <a href="{v["html"]}">ver</a></li>' for i,v in sorted(steppdf.items()))
    body=f'''<div class="intro"><p style="color:#D9502B;font-weight:600;letter-spacing:.14em;font-size:12px;text-transform:uppercase;margin:0">Strate Studio · {html.escape(p["n"])}</p><h1>Plantillas de perforación 1:1</h1>
<p>Hojas carta a escala real para marcar cada bolsillo y tornillo sin medir. Las 2 primeras hojas son la guía ilustrada.</p>
<p class="w"><b>Imprime al 100 % («Tamaño real»), sin ajustar.</b> Mide la regla de 10 cm de cada hoja antes de usarla.</p>
<a class="b" href="plantillas_{key}.pdf">PDF completo ({len(pages)} hojas)</a><a class="b g" href="../#armado">← Volver al armado</a>
<h3>Por paso de armado</h3><ul>{stp}</ul></div>'''
    open(OUT+'index.html','w').write(HEAD.replace('{t}',f'Plantillas 1:1 · {p["n"]} · Strate Studio')+body+''.join(pages)+'</body></html>')
    return {i:v['file'] for i,v in steppdf.items()},{i:v['html'] for i,v in steppdf.items()},F
# ---------- páginas ----------
HEAD=open('/workspace/studio/ropero/index.html').read().split('<body>')[0]
fmt=lambda v:'$'+f'{round(v):,}'
meta={}
for key,p in PROJ.items():
    ps=[e for e in X if e['id'].startswith(p['pref'])]
    a18=sum(e['L']*e['W'] for e in ps if e['T']==18)/1e6;a5=sum(e['L']*e['W'] for e in ps if e['T']==5)/1e6
    canto=sum(sum(e['band']) for e in ps)/1000
    bud=[(f'Triplay de pino 18 mm (parte proporcional de las hojas del pedido: {a18:.2f} m²)','',a18*M18)]
    if a5:bud.append((f'Triplay de pino 5 mm ({a5:.2f} m²)','',a5*M5))
    if canto:bud.append((f'Cubrecanto de pino 19 mm ({canto:.1f} m)','',canto*CANTO))
    bud+=[(a,b,q*u) for a,b,q,u in p['hw']]
    tot=sum(v for *_,v in bud)
    pdfs,htmls,F=mk_tpl(key,p)
    faces=[dict(id=f['id'],no=str(f['no']),name=f['name'],L=f['L'],W=f['W'],mirror=f['mirror'],h=[dict(x=h['x'],y=h['y'],xd=h['xd'],k=h['k'],u=h['u']) for h in f['h']]) for f in F]
    names={e['id']:dict(n=e['n'],d=f"{e['L']} × {e['W']} × {e['T']}") for e in ps};names['yute']=dict(n='Yute (sin tratar)',d='364 × 472')
    D=dict(key=key,size=p['size'],parts=p['parts'],steps=[dict(t=s['t'],d=s['d'],n=s['n'],f=s.get('f',[]),j=s['j'],tools=s['tools'],min=s['min']) for s in p['steps']],joints={j['id']:j for j in p['joints']},faces=faces,names=names,pdf={str(k):v for k,v in pdfs.items()},
           budget=[[a,b,round(v)] for a,b,v in bud],total=round(tot),compare=p['compare'],hw=[[a,b,q] for a,b,q,u in p['hw']],pieces=[[e['id'],e['n'],e['L'],e['W'],e['T'],' + '.join(map(str,e['band'])) or '—',e['s']] for e in ps])
    mins=sum(s['min'] for s in p['steps'])
    head=HEAD.replace('<title>Ropero de pino y yute · Strate Studio</title>',f"<title>{p['n']} · Strate Studio</title>").replace('href="style.css"','href="../ropero/style.css"')
    head=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{html.escape(p["lead"])}">',head)
    page=f'''{head}<body>
<header class="top"><div class="in"><a class="brand" href="../">Strate <span>Studio</span></a><nav><a href="#resumen">Resumen</a><a href="#presupuesto">Presupuesto</a><a href="#armado">Armado</a><a href="#taller">Taller</a></nav></div></header>
<main class="wrap">
<section class="hero"><p class="eyebrow">Proyecto {p['no']} · {p['cat']}</p><h1>{p['n']}</h1>
<p class="lead">{p['lead']}</p><div class="chips">{''.join(f'<span class="chip">{c}</span>' for c in p['chips'])}</div>
<p class="eyebrow" style="margin-top:22px">Modelo 3D</p><div class="stage" id="hero"><span class="hint">Gira con el dedo · pellizca para acercar</span></div></section>
<section class="blk" id="resumen"><p class="eyebrow">Resumen</p><h2>Lo que vas a construir</h2>
<div class="grid g4" style="margin-top:16px" id="stats"></div>
<div class="card" style="margin-top:14px"><h3>Piezas de triplay</h3><div style="overflow-x:auto"><table class="list" style="width:100%;font-size:14px" id="pieces"></table></div>
<p class="small" style="margin-bottom:0">Van en el <a href="../ropero/esquema_corte.pdf">esquema de corte</a> del pedido junto con el ropero: mismas 6 hojas.</p></div></section>
<section class="blk" id="presupuesto"><p class="eyebrow">Presupuesto</p><h2>≈ <span id="tot"></span> MXN</h2>
<p class="small">Precios estimados en MXN, octubre 2026. El triplay se calcula por la parte de hoja que ocupa este mueble.</p>
<div class="card" style="margin-top:14px;overflow-x:auto"><table id="budget"></table></div>
<h3 style="margin-top:28px">¿Y si lo compro hecho?</h3><div class="grid g2" id="compare" style="margin-top:10px"></div></section>
<section class="blk" id="armado"><p class="eyebrow">Armado</p><h2>Paso a paso en 3D</h2>
<p class="small">En naranja lo nuevo de cada paso; en salvia lo que ya armaste. Debajo, la lámina con cada tornillo, broca y profundidad, y el PDF de <a href="plantillas/">plantillas 1:1</a> del paso. Marca cada paso al terminarlo: se guarda en este teléfono.</p>
<div class="prog" style="margin:14px 0 6px"><i id="bar"></i></div><div class="small" id="progt"></div>
<div class="asm" style="margin-top:12px"><div class="stage" id="asm3d"><span class="hint">Gira · acerca</span></div>
<div><div class="stepnav"><button class="btn ghost" id="prev">← Anterior</button><button class="btn" id="next">Siguiente →</button></div><div class="card" id="stepcard"></div><div id="plate"></div><div class="dots" id="dots"></div></div></div>
<div class="printonly" id="printsteps"></div></section>
<section class="blk" id="taller"><p class="eyebrow">Taller</p><h2>Compras y ferretería</h2><p class="small">Nombres como los entienden en Home Depot y ferreterías de México. Márcalos al comprarlos.</p><div class="card" id="buy"></div></section>
</main>
<footer><div class="wrap">Strate Studio · <a href="plantillas/">Plantillas 1:1</a> · <a href="plantillas/plantillas_{key}.pdf">Plantillas (PDF)</a> · <a href="../ropero/esquema_corte.pdf">Esquema de corte (PDF)</a> · <a href="#" onclick="print();return false">Imprimir</a></div></footer>
<script>window.M={json.dumps(D,ensure_ascii=False)};</script>
<script src="../mini/page.js"></script>
<script type="module">import {{viewer}} from '../mini/mini.js';const m=window.M;viewer(document.getElementById('hero'),m);window.__asm=viewer(document.getElementById('asm3d'),m);window.dispatchEvent(new Event('asm-ready'));</script>
</body></html>'''
    open(f'/workspace/studio/{key}/index.html','w').write(page)
    meta[key]=dict(n=p['n'],no=p['no'],cat=p['cat'],size=p['size'],piezas=len(ps),pasos=len(p['steps']),ext=round(tot),htmls=htmls)
    print(key,len(ps),'piezas · total',round(tot),'· pdfs',pdfs)
json.dump(meta,open('/workspace/studio/mini/projects.json','w'),ensure_ascii=False)
