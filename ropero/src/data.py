import json
H=1880
P=[]  # no, letra, nombre, L, W, T, material, canto(bool front long edge), nota, thumb rects [x,y,w,h]
def add(n,letra,nom,L,W,T,mat,canto,nota,th):
    for i in range(n): P.append(dict(no=len(P)+1,l=letra,n=nom+(f' {i+1}' if n>1 else ''),L=L,W=W,T=T,mat=mat,c=canto,nota=nota,th=th[i] if isinstance(th[0],list) else th))
add(2,'A','Costado',2000,547,18,'Triplay pino 18 mm',1,'Agujeros soportes de tubo (costado izq.: 1900 y 980; der.: 1650) a 270 del frente. Sin pocket en cara exterior.',[[0,0,18,2000],[1582,0,18,2000]])
add(1,'B','Techo',1564,547,18,'Triplay pino 18 mm',1,'Pocket en cara superior (4 por lado + 3 a la división). Riel atornillado debajo, al frente.',[18,1982,1564,18])
add(1,'C','Piso',1564,547,18,'Triplay pino 18 mm',1,'Pocket en cara inferior (4 por lado + 3 a la división). Asienta sobre el zócalo.',[18,50,1564,18])
add(1,'D','División central',1914,547,18,'Triplay pino 18 mm',1,'Centrada: 773 libres a cada lado. Pocket 3 arriba + 3 abajo. Agujeros soportes tubo.',[791,68,18,1914])
add(1,'E','Repisa superior der.',773,480,18,'Triplay pino 18 mm',1,'Cara superior a 1700 del piso. Pegada al fondo. Pocket 2 por lado en cara inferior.',[809,1682,773,18])
add(1,'F','Zapatera der.',773,350,18,'Triplay pino 18 mm',1,'Cara superior a 270 del piso. Pegada al fondo. Pocket 2 por lado.',[809,252,773,18])
add(1,'G','Zócalo frente',1564,50,18,'Triplay pino 18 mm',1,'Remetido 50 mm del frente.',[18,0,1564,50])
add(1,'G','Zócalo atrás',1564,50,18,'Triplay pino 18 mm',0,'Al ras de atrás.',[18,0,1564,50])
add(3,'H','Zócalo travesaño',458,50,18,'Triplay pino 18 mm',0,'Entre zócalos: extremos y centro. 1 pocket por extremo.',[[18,0,18,50],[791,0,18,50],[1564,0,18,50]])
add(1,'I','Fondo grande',1950,1220,3,'Triplay 3 mm',0,'Desde la izquierda. Ventilación: agujeros Ø25 cada 150 arriba y abajo. Tornillo 1" cada 200.',[0,50,1220,1950])
add(1,'I','Fondo tira',1950,380,3,'Triplay 3 mm',0,'Completa a 1600 por la derecha. La unión cae sobre el listón 15.',[1220,50,380,1950])
add(1,'P','Listón de unión del fondo',1914,63,19,'Pino seco 19×63',0,'Vertical por dentro, entre piso y techo, centrado a 1220 del lado izq. (cara de atrás al ras). Las dos piezas del fondo se atornillan a él.',[1189,68,63,1914])
add(4,'J','Puerta larguero',H,63,19,'Pino seco 19×63',0,'Media madera 63×9.5 en ambos extremos + 2 intermedias a H/3 y 2H/3. H = 1914 − descuento del riel (≈1880). NO CORTAR hasta tener el riel.',[[18,68,63,H],[757,68,63,H],[780,68,63,H],[1519,68,63,H]])
add(8,'K','Puerta travesaño',802,63,19,'Pino seco 19×63',0,'Largo total 802; media madera 63 largo × 9.5 prof. en cada extremo. 4 por puerta: sup., inf. y 2 intermedios.',[[18,68,802,63],[18,68+H-63,802,63],[18,68+H/3-31,802,63],[18,68+2*H/3-31,802,63],[780,68,802,63],[780,68+H-63,802,63],[780,68+H/3-31,802,63],[780,68+2*H/3-31,802,63]])
add(2,'L','Puerta tapa',H,802,3,'Triplay 3 mm',0,'Pegada y engrapada a todo el bastidor cada 100. Yute encima. Altura = H.',[[18,68,802,H],[780,68,802,H]])
add(3,'M','Tubo Ø25',765,25,25,'Tubo acero (FIX 2.4 m)',0,'Medir claro real (773) y descontar los soportes. Izq. a 1900 y 980; der. a 1650. Sale de 1 tubo de 2.4 m (3×765 + cortes).',[[18,1896,773,8],[18,976,773,8],[809,1646,773,8]])
jth=[]
for dx in (18,780):
    jth+= [[dx,68,12,H],[dx+790,68,12,H],[dx,68+H-12,802,12],[dx,68,802,12]]
names=['vertical izq.','vertical der.','superior','inferior']
for i in range(8):
    d=i//4+1;v=i%4<2
    P.append(dict(no=len(P)+1,l='N',n=f'Junquillo puerta {d} {names[i%4]}',L=H if v else 802,W=12,T=15,mat='Pino (rajado de tabla 1×3)',c=0,nota='Inglete 45° en esquinas; clavar con clavo sin cabeza sobre el yute. Largo final a medida.',th=jth[i]))
K=3
num=lambda l:[p['no'] for p in P if p['l']==l]
A=num('A');J=num('J');Kk=num('K');Ll=num('L');I=num('I');N=num('N');H_=num('H');G=num('G')
SHEETS=[
 dict(t='Hoja 1 · Triplay pino 18 mm',W=1220,H=2440,p=[(A[0],0,0,547,2000),(A[1],550,0,547,2000)]),
 dict(t='Hoja 2 · Triplay pino 18 mm',W=1220,H=2440,p=[(5,0,0,547,1914),(3,550,0,547,1564),(6,550,1567,480,773)]),
 dict(t='Hoja 3 · Triplay pino 18 mm',W=1220,H=2440,p=[(4,0,0,547,1564),(7,0,1567,350,773),(G[0],550,0,50,1564),(G[1],603,0,50,1564)]+[(h,656+53*i,0,50,458) for i,h in enumerate(H_)]),
 dict(t='Hoja 4 · Triplay 3 mm',W=1220,H=2440,p=[(I[0],0,0,1220,1950)]),
 dict(t='Hoja 5 · Triplay 3 mm',W=1220,H=2440,p=[(I[1],0,0,380,1950),(Ll[0],383,0,802,H)]),
 dict(t='Hoja 6 · Triplay 3 mm',W=1220,H=2440,p=[(Ll[1],0,0,802,H)]),
]
BOARDS=[[(j,H)] for j in J]+[[(k,802) for k in Kk[0:3]],[(k,802) for k in Kk[3:6]],[(k,802) for k in Kk[6:8]],[(15,1914)],
 'Tabla 1×3 extra: rajar en tiras ~12×15 → 4 tiras de 2440 para junquillos verticales (piezas %s)'%', '.join(map(str,[N[0],N[1],N[4],N[5]])),
 'Tabla 1×3 extra: rajar en tiras → junquillos horizontales 802 (piezas %s), 3 por tira'%', '.join(map(str,[N[2],N[3],N[6],N[7]]))]
# checks
assert 18+1564+18==1600 and 50+18+1914+18==2000 and 547+3==550 and 18+773+18+773+18==1600 and 1220+380==1600
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
assert sorted(cut)==[p['no'] for p in P if p['l'] not in 'MN'],set(p['no'] for p in P)-set(cut)
json.dump(dict(P=P,S=SHEETS,B=BOARDS,H=H),open('data.json','w'),ensure_ascii=False)
print(len(P),'pieces OK')
