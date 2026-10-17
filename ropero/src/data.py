import json
Y0=78  # canto inferior de puerta: piso 68 + 10
H=1866  # Ducloset doble: techo inf. 1982 − 38 (ficha) − (piso 68 + 10 holgura) = 1866
P=[]  # no, letra, nombre, L, W, T, material, canto(bool front long edge), nota, thumb rects [x,y,w,h]
def add(n,letra,nom,L,W,T,mat,canto,nota,th):
    for i in range(n): P.append(dict(no=len(P)+1,l=letra,n=nom+(f' {i+1}' if n>1 else ''),L=L,W=W,T=T,mat=mat,c=canto,nota=nota,th=th[i] if isinstance(th[0],list) else th))
add(2,'A','Costado',2000,547,18,'Triplay pino 18 mm',1,'Soportes de tubo al centro del tubo, a 270 del frente (costado izq.: 1900 y 980; der.: 1630). Sin pocket en cara exterior.',[[0,0,18,2000],[1582,0,18,2000]])
add(1,'B','Techo',1564,547,18,'Triplay pino 18 mm',1,'Pocket en cara superior: 4 por lado (60, 215, 370, 487 del frente). Los 3 de la división van en la división. Riel atornillado debajo, al frente.',[18,1982,1564,18])
add(1,'C','Piso',1564,547,18,'Triplay pino 18 mm',1,'Pocket en cara inferior: 4 por lado (90, 230, 370, 487 del frente). Asienta sobre el zócalo.',[18,50,1564,18])
add(1,'D','División central',1914,482,18,'Triplay pino 18 mm',1,'Centrada: 773 libres a cada lado. Fondo 482: canto trasero al ras de atrás y frente 65 mm detrás del frente del mueble, para librar las dos puertas (zona de riel 60 mm). Pocket 3 arriba + 3 abajo en la cara derecha (60, 241, 422 de su canto frontal). Soportes de tubo a 205 de su canto frontal (= 270 del frente del mueble). Alturas: izq. 1900 y 980, der. 1630.',[791,68,18,1914])
add(1,'E','Repisa superior der.',773,461,18,'Triplay pino 18 mm',1,'Cara superior a 1700 del piso. Fondo 461 (19 menos para librar el listón 15); se apoya contra el listón (frente 67 mm detrás del frente del mueble). Pocket 2 por lado en cara inferior (60 del frente y 60 de atrás).',[809,1682,773,18])
add(1,'F','Zapatera der.',773,331,18,'Triplay pino 18 mm',1,'Cara superior a 270 del piso. Fondo 331 (19 menos para librar el listón 15). Pocket 2 por lado (60 del frente y 60 de atrás).',[809,252,773,18])
add(1,'G','Zócalo frente',1564,50,18,'Triplay pino 18 mm',1,'Remetido 50 mm del frente.',[18,0,1564,50])
add(1,'G','Zócalo atrás',1564,50,18,'Triplay pino 18 mm',0,'Al ras de atrás.',[18,0,1564,50])
add(3,'H','Zócalo travesaño',461,50,18,'Triplay pino 18 mm',0,'Entre zócalos: extremos y centro. 1 pocket por extremo.',[[18,0,18,50],[791,0,18,50],[1564,0,18,50]])
add(1,'I','Fondo grande',1950,1220,5,'Triplay pino 5 mm',0,'Desde la izquierda. Tornillo #6 × 5/8" (ver plantilla). Ventilación Ø25 en 2 filas a 140 y 1810 del canto inferior, a ≥30 de cualquier tornillo.',[0,50,1220,1950])
add(1,'I','Fondo tira',1950,380,5,'Triplay pino 5 mm',0,'Completa a 1600 por la derecha. La unión cae sobre el listón 15.',[1220,50,380,1950])
add(1,'P','Listón de unión del fondo',1914,63,19,'Pino seco 19×63',0,'Vertical por dentro, entre piso y techo, centrado a 1220 del lado izq. (cara de atrás al ras de los costados, por delante del fondo). Las dos piezas del fondo se atornillan a él.',[1189,68,63,1914])
add(4,'J','Puerta larguero',H,63,19,'Pino seco 19×63',0,'Media madera 63×9.5 en ambos extremos + 2 intermedias a H/3 y 2H/3 (recalcular con H real). 2 tornillos #6 × 5/8" + cola por cruce. H = 1866 (riel Ducloset doble: 38 arriba + 10 abajo). Intermedias a 622 y 1244 del canto inferior.',[[18,Y0,63,H],[757,Y0,63,H],[780,Y0,63,H],[1519,Y0,63,H]])
add(8,'K','Puerta travesaño',802,63,19,'Pino seco 19×63',0,'Largo total 802; media madera 63 largo × 9.5 prof. en cada extremo. 4 por puerta: sup., inf. y 2 intermedios.',[[18,Y0,802,63],[18,Y0+H-63,802,63],[18,Y0+H/3-31.5,802,63],[18,Y0+2*H/3-31.5,802,63],[780,Y0,802,63],[780,Y0+H-63,802,63],[780,Y0+H/3-31.5,802,63],[780,Y0+2*H/3-31.5,802,63]])
add(2,'L','Puerta tapa',H,802,5,'Triplay pino 5 mm',0,'Tapa calada: triplay de pino 5 mm, cara buena al frente, con 3 ventanas de 676 de ancho recortadas con caladora (iguales a los huecos del bastidor; esquinas con radio 5). Va encima del yute, que queda 5 mm hundido. Pegada (Resistol 850) y engrapada al bastidor cada 50 (grapa 14 mm). Plana, sin rebajo ni junquillo. Altura = H.',[[18,Y0,802,H],[780,Y0,802,H]])
add(3,'M','Tubo Ø25',765,25,25,'Tubo acero (FIX 2.4 m)',0,'Medir claro real (773) y descontar los soportes. Al centro del tubo: izq. 1900 y 980; der. 1630 (deja ~40 libres bajo la repisa para el gancho). Sale de 1 tubo de 2.4 m (3×765 + cortes).',[[18,1896,773,8],[18,976,773,8],[809,1626,773,8]])
# Puertas: tapa calada de 5 mm sobre yute (3 ventanas por puerta); sin junquillo. Piezas 33–38 retiradas (números reservados).
OPN=[(63,H/3-31.5),(H/3+31.5,2*H/3-31.5),(2*H/3+31.5,H-63)]
def jq(no_name,L,W,T,mat,nota,pp,l='N'):
    P.append(dict(no=len(P)+1,l=l,n=no_name,L=L,W=W,T=T,mat=mat,c=0,nota=nota,th=pp[0],pp=pp,q=len(pp)))
for i in range(33,39): P.append(dict(no=i,l='X',n='(sin uso: junquillo eliminado con la tapa calada)',L=0,W=0,T=0,mat='—',c=0,nota='Número reservado para no cambiar la numeración.',th=[0,0,0,0]))
YN='Yute sin tratar, 20 mm más por lado que el hueco. Va engrapado sobre el bastidor (grapa 8 mm cada 30, a 10 mm del borde del hueco) y queda prensado bajo la tapa calada.'
jq('Yute · paneles bajo y alto, ambas puertas (×4)',round(OPN[0][1]-OPN[0][0]+40,1),716,1,'Yute sin tratar',YN,[[dx+63,Y0+o[0],676,o[1]-o[0]] for dx in (18,780) for o in (OPN[0],OPN[2])],l='Y')
jq('Yute · panel medio, ambas puertas (×2)',round(OPN[1][1]-OPN[1][0]+40,1),716,1,'Yute sin tratar',YN,[[dx+63,Y0+OPN[1][0],676,OPN[1][1]-OPN[1][0]] for dx in (18,780)],l='Y')
JNAMES={16:'Puerta A · larguero izq.',17:'Puerta A · larguero der.',18:'Puerta B · larguero izq.',19:'Puerta B · larguero der.',20:'Puerta A · travesaño inferior',21:'Puerta A · travesaño superior',22:'Puerta A · travesaño intermedio bajo',23:'Puerta A · travesaño intermedio alto',24:'Puerta B · travesaño inferior',25:'Puerta B · travesaño superior',26:'Puerta B · travesaño intermedio bajo',27:'Puerta B · travesaño intermedio alto',28:'Puerta A (frente) · tapa calada',29:'Puerta B (atrás) · tapa calada'}
for k,v in JNAMES.items(): P[k-1]['n']=v
add(1,'Q','Entrepaño rigidizador izq.',773,482,18,'Triplay pino 18 mm',1,'Fijo, sección izquierda. Cara inferior a 1035 del suelo (cara superior 1053): deja ~43 libres sobre el tubo de 980 para el gancho y ~847 bajo el tubo de 1900 para camisas. A media altura rigidiza costado 01 y división 05. Fondo 482: al ras de atrás, frente 65 mm detrás del frente del mueble (libra las puertas). Pocket 3 por lado en cara inferior (60, 241, 422 de su canto frontal). Pieza 41.',[18,1035,773,18])
K=4
num=lambda l:[p['no'] for p in P if p['l']==l]
A=num('A');J=num('J');Kk=num('K');Ll=num('L');I=num('I');N=num('N');H_=num('H');G=num('G')
TRIM,KERF=5,4  # refilado de fábrica 5 mm por lado; disco 4 mm entre TODOS los cortes
_c=lambda i,w: TRIM+sum(w[:i])+KERF*i
SHEETS=[
 dict(t='Hoja 1 · Triplay pino 18 mm',W=1220,H=2440,p=[(A[0],5,5,547,2000),(A[1],556,5,547,2000)]),
 dict(t='Hoja 2 · Triplay pino 18 mm',W=1220,H=2440,p=[(5,5,5,482,1914),(3,506,5,547,1564),(6,506,1573,461,773)]),
 dict(t='Hoja 3 · Triplay pino 18 mm',W=1220,H=2440,p=[(4,5,5,547,1564),(7,5,1573,331,773),(G[0],556,5,50,1564),(G[1],610,5,50,1564)]+[(h,664+54*i,5,50,461) for i,h in enumerate(H_)]+[(41,556,1573,482,773)]),
 dict(t='Hoja 4 · Triplay pino 5 mm',W=1220,H=2440,p=[(I[0],0,5,1220,1950)]),
 dict(t='Hoja 5 · Triplay pino 5 mm',W=1220,H=2440,p=[(Ll[0],5,5,802,H),(I[1],811,5,380,1950)]),
 dict(t='Hoja 6 · Triplay pino 5 mm',W=1220,H=2440,p=[(Ll[1],5,5,802,H)]),
]
BOARDS=[[(j,H)] for j in J]+[[(k,802) for k in Kk[0:3]],[(k,802) for k in Kk[3:6]],[(k,802) for k in Kk[6:8]],[(15,1914)]]
# checks
assert 18+1564+18==1600 and 50+18+1914+18==2000 and 547+5==552 and 18+773+18+773+18==1600 and 1220+380==1600
for s in SHEETS:
    for no,x,y,w,h in s['p']:
        p=P[no-1]; assert sorted([w,h])==sorted([p['L'],p['W']]),(no,w,h); assert x+w<=s['W'] and y+h<=s['H'],no
        assert (x>=TRIM or w==s['W']) and y>=TRIM and (x+w<=s['W']-TRIM or w==s['W']) and y+h<=s['H']-TRIM,('refilado',no)
    r=s['p']
    for i in range(len(r)):
        for j in range(i+1,len(r)):
            a,b=r[i],r[j]; assert a[1]+a[3]+K<=b[1]+1e-9 or b[1]+b[3]+K<=a[1]+1e-9 or a[2]+a[4]+K<=b[2] or b[2]+b[4]+K<=a[2],(a,b)
for b in BOARDS:
    if isinstance(b,list): assert sum(l for _,l in b)+K*(len(b)-1)<=2440
cut=[n for s in SHEETS for n,*_ in s['p']]+[n for b in BOARDS if isinstance(b,list) for n,_ in b]
assert sorted(cut)==sorted(p['no'] for p in P if p['l'] not in 'MNYX'),set(p['no'] for p in P)-set(cut)
json.dump(dict(P=P,S=SHEETS,B=BOARDS,H=H,Y0=Y0,OPN=OPN,KERF=KERF,TRIM=TRIM),open('data.json','w'),ensure_ascii=False)
print(len(P),'pieces OK')
