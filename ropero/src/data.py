import json
H=1880
P=[]  # no, letra, nombre, L, W, T, material, canto(bool front long edge), nota, thumb rects [x,y,w,h]
def add(n,letra,nom,L,W,T,mat,canto,nota,th):
    for i in range(n): P.append(dict(no=len(P)+1,l=letra,n=nom+(f' {i+1}' if n>1 else ''),L=L,W=W,T=T,mat=mat,c=canto,nota=nota,th=th[i] if isinstance(th[0],list) else th))
add(2,'A','Costado',2000,547,18,'Triplay pino 18 mm',1,'Soportes de tubo al centro del tubo, a 270 del frente (costado izq.: 1900 y 980; der.: 1630). Sin pocket en cara exterior.',[[0,0,18,2000],[1582,0,18,2000]])
add(1,'B','Techo',1564,547,18,'Triplay pino 18 mm',1,'Pocket en cara superior: 4 por lado (60, 215, 370, 487 del frente). Los 3 de la división van en la división. Riel atornillado debajo, al frente.',[18,1982,1564,18])
add(1,'C','Piso',1564,547,18,'Triplay pino 18 mm',1,'Pocket en cara inferior: 4 por lado (90, 230, 370, 487 del frente). Asienta sobre el zócalo.',[18,50,1564,18])
add(1,'D','División central',1914,547,18,'Triplay pino 18 mm',1,'Centrada: 773 libres a cada lado. Pocket 3 arriba + 3 abajo en la cara derecha (60, 273.5, 487 del frente). Soportes de tubo: izq. 1900 y 980, der. 1630.',[791,68,18,1914])
add(1,'E','Repisa superior der.',773,461,18,'Triplay pino 18 mm',1,'Cara superior a 1700 del piso. Fondo 461 (19 menos para librar el listón 15); se apoya contra el listón. Pocket 2 por lado en cara inferior (60 del frente y 60 de atrás).',[809,1682,773,18])
add(1,'F','Zapatera der.',773,331,18,'Triplay pino 18 mm',1,'Cara superior a 270 del piso. Fondo 331 (19 menos para librar el listón 15). Pocket 2 por lado (60 del frente y 60 de atrás).',[809,252,773,18])
add(1,'G','Zócalo frente',1564,50,18,'Triplay pino 18 mm',1,'Remetido 50 mm del frente.',[18,0,1564,50])
add(1,'G','Zócalo atrás',1564,50,18,'Triplay pino 18 mm',0,'Al ras de atrás.',[18,0,1564,50])
add(3,'H','Zócalo travesaño',461,50,18,'Triplay pino 18 mm',0,'Entre zócalos: extremos y centro. 1 pocket por extremo.',[[18,0,18,50],[791,0,18,50],[1564,0,18,50]])
add(1,'I','Fondo grande',1950,1220,6,'Triplay 6 mm',0,'Desde la izquierda. Tornillo #6 × 5/8" (ver plantilla). Ventilación Ø25 en 2 filas a 140 y 1810 del canto inferior, a ≥30 de cualquier tornillo.',[0,50,1220,1950])
add(1,'I','Fondo tira',1950,380,6,'Triplay 6 mm',0,'Completa a 1600 por la derecha. La unión cae sobre el listón 15.',[1220,50,380,1950])
add(1,'P','Listón de unión del fondo',1914,63,19,'Pino seco 19×63',0,'Vertical por dentro, entre piso y techo, centrado a 1220 del lado izq. (cara de atrás al ras de los costados, por delante del fondo). Las dos piezas del fondo se atornillan a él.',[1189,68,63,1914])
add(4,'J','Puerta larguero',H,63,19,'Pino seco 19×63',0,'Media madera 63×9.5 en ambos extremos + 2 intermedias a H/3 y 2H/3 (recalcular con H real). 2 tornillos #6 × 5/8" + cola por cruce. H = 1914 − descuento del riel (≈1880). NO CORTAR hasta tener el riel.',[[18,68,63,H],[757,68,63,H],[780,68,63,H],[1519,68,63,H]])
add(8,'K','Puerta travesaño',802,63,19,'Pino seco 19×63',0,'Largo total 802; media madera 63 largo × 9.5 prof. en cada extremo. 4 por puerta: sup., inf. y 2 intermedios.',[[18,68,802,63],[18,68+H-63,802,63],[18,68+H/3-31,802,63],[18,68+2*H/3-31,802,63],[780,68,802,63],[780,68+H-63,802,63],[780,68+H/3-31,802,63],[780,68+2*H/3-31,802,63]])
add(2,'L','Puerta tapa',H,802,3,'Triplay 3 mm',0,'Triplay de 3 mm con cara buena: queda a la vista en las franjas del bastidor (encerada). Pegada y engrapada a todo el bastidor cada 50 (grapa 10 mm). Encima van 3 paneles de yute. Altura = H.',[[18,68,802,H],[780,68,802,H]])
add(3,'M','Tubo Ø25',765,25,25,'Tubo acero (FIX 2.4 m)',0,'Medir claro real (773) y descontar los soportes. Al centro del tubo: izq. 1900 y 980; der. 1630 (deja ~40 libres bajo la repisa para el gancho). Sale de 1 tubo de 2.4 m (3×765 + cortes).',[[18,1896,773,8],[18,976,773,8],[809,1626,773,8]])
# Puertas opción 3: 3 paneles de yute por puerta, junquillo en los 4 lados de cada panel
OPN=[(63,H/3-31.5),(H/3+31.5,2*H/3-31.5),(2*H/3+31.5,H-63)]
def jq(no_name,L,W,T,mat,nota,pp,l='N'):
    P.append(dict(no=len(P)+1,l=l,n=no_name,L=L,W=W,T=T,mat=mat,c=0,nota=nota,th=pp[0],pp=pp,q=len(pp)))
JN='Inglete 45° en las 4 esquinas de cada panel; clavo sin cabeza 1" cada ~150 (30 de cada extremo), sobre el yute y el borde del bastidor. Largo final a medida del hueco.'
for dx,dn in ((18,'A'),(780,'B')):
    xl,xr=dx+63,dx+802-63-12
    jq(f'Puerta {dn} · junquillo vertical, paneles bajo y alto (×4)',532,12,15,'Pino (rajado de tabla 1×3)',JN,[[x,68+o[0],12,o[1]-o[0]] for o in (OPN[0],OPN[2]) for x in (xl,xr)])
    jq(f'Puerta {dn} · junquillo vertical, panel medio (×2)',564,12,15,'Pino (rajado de tabla 1×3)',JN,[[x,68+OPN[1][0],12,OPN[1][1]-OPN[1][0]] for x in (xl,xr)])
    jq(f'Puerta {dn} · junquillo horizontal (×6)',676,12,15,'Pino (rajado de tabla 1×3)',JN,[[dx+63,68+y,676,12] for o in OPN for y in (o[0],o[1]-12)])
YN='Yute sin tratar, 20 mm más por lado que el hueco. Cola Resistol 850 sobre la tapa + grapa 8 mm cada 30, a 6 del borde del hueco (queda bajo el junquillo).'
jq('Yute · paneles bajo y alto, ambas puertas (×4)',572,716,1,'Yute sin tratar',YN,[[dx+63,68+o[0],676,o[1]-o[0]] for dx in (18,780) for o in (OPN[0],OPN[2])],l='Y')
jq('Yute · panel medio, ambas puertas (×2)',604,716,1,'Yute sin tratar',YN,[[dx+63,68+OPN[1][0],676,OPN[1][1]-OPN[1][0]] for dx in (18,780)],l='Y')
JNAMES={16:'Puerta A · larguero izq.',17:'Puerta A · larguero der.',18:'Puerta B · larguero izq.',19:'Puerta B · larguero der.',20:'Puerta A · travesaño inferior',21:'Puerta A · travesaño superior',22:'Puerta A · travesaño intermedio bajo',23:'Puerta A · travesaño intermedio alto',24:'Puerta B · travesaño inferior',25:'Puerta B · travesaño superior',26:'Puerta B · travesaño intermedio bajo',27:'Puerta B · travesaño intermedio alto',28:'Puerta A (frente) · tapa',29:'Puerta B (atrás) · tapa'}
for k,v in JNAMES.items(): P[k-1]['n']=v
add(1,'Q','Entrepaño rigidizador izq.',773,547,18,'Triplay pino 18 mm',1,'Fijo, sección izquierda. Cara inferior a 1035 del suelo (cara superior 1053): deja ~43 libres sobre el tubo de 980 para el gancho y ~847 bajo el tubo de 1900 para camisas. A media altura rigidiza costado 01 y división 05. Pocket 3 por lado en cara inferior (60, 273.5, 487 del frente). Pieza 41.',[18,1035,773,18])
K=3
num=lambda l:[p['no'] for p in P if p['l']==l]
A=num('A');J=num('J');Kk=num('K');Ll=num('L');I=num('I');N=num('N');H_=num('H');G=num('G')
SHEETS=[
 dict(t='Hoja 1 · Triplay pino 18 mm',W=1220,H=2440,p=[(A[0],0,0,547,2000),(A[1],550,0,547,2000)]),
 dict(t='Hoja 2 · Triplay pino 18 mm',W=1220,H=2440,p=[(5,0,0,547,1914),(3,550,0,547,1564),(6,550,1567,461,773)]),
 dict(t='Hoja 3 · Triplay pino 18 mm',W=1220,H=2440,p=[(4,0,0,547,1564),(7,0,1567,331,773),(G[0],550,0,50,1564),(G[1],603,0,50,1564)]+[(h,656+53*i,0,50,461) for i,h in enumerate(H_)]+[(41,550,1567,547,773)]),
 dict(t='Hoja 4 · Triplay 6 mm',W=1220,H=2440,p=[(I[0],0,0,1220,1950)]),
 dict(t='Hoja 5 · Triplay 6 mm',W=1220,H=2440,p=[(I[1],0,0,380,1950)]),
 dict(t='Hoja 6 · Triplay 3 mm',W=1220,H=2440,p=[(Ll[0],0,0,802,H)]),
 dict(t='Hoja 7 · Triplay 3 mm',W=1220,H=2440,p=[(Ll[1],0,0,802,H)]),
]
BOARDS=[[(j,H)] for j in J]+[[(k,802) for k in Kk[0:3]],[(k,802) for k in Kk[3:6]],[(k,802) for k in Kk[6:8]],[(15,1914)],
 'Tabla 1×3 extra 1: rajar en 4 tiras ~12×15 × 2440 → tira 1 y 2: 4 × 532 c/u (33, 36); tira 3: 4 × 564 (34, 37); tira 4: 3 × 676 (35/38)',
 'Tabla 1×3 extra 2: 4 tiras → tiras 1–3: 3 × 676 c/u (resto de 35/38); tira 4 de repuesto']
# checks
assert 18+1564+18==1600 and 50+18+1914+18==2000 and 547+6==553 and 18+773+18+773+18==1600 and 1220+380==1600
for s in SHEETS:
    for no,x,y,w,h in s['p']:
        p=P[no-1]; assert sorted([w,h])==sorted([p['L'],p['W']]),(no,w,h); assert x+w<=s['W'] and y+h<=s['H'],no
    r=s['p']
    for i in range(len(r)):
        for j in range(i+1,len(r)):
            a,b=r[i],r[j]; assert a[1]+a[3]+K<=b[1]+1e-9 or b[1]+b[3]+K<=a[1]+1e-9 or a[2]+a[4]+K<=b[2] or b[2]+b[4]+K<=a[2],(a,b)
for b in BOARDS:
    if isinstance(b,list): assert sum(l for _,l in b)+K*(len(b)-1)<=2440
cut=[n for s in SHEETS for n,*_ in s['p']]+[n for b in BOARDS if isinstance(b,list) for n,_ in b]
assert sorted(cut)==sorted(p['no'] for p in P if p['l'] not in 'MNY'),set(p['no'] for p in P)-set(cut)
json.dump(dict(P=P,S=SHEETS,B=BOARDS,H=H),open('data.json','w'),ensure_ascii=False)
print(len(P),'pieces OK')
