# Ropero CNC: genera piezas, anidado, DXF, SVG y datos de la página
import json, math, os
from shapely.geometry import box, Point, Polygon
from shapely.ops import unary_union
from shapely import affinity
import rectpack, ezdxf
OUT='/workspace/studio/ropero-cnc'; R=3.0; D=R/math.sqrt(2); TOL=0.3
def rbox(x0,y0,x1,y1,r):
    return box(x0+r,y0+r,x1-r,y1-r).buffer(r,resolution=16) if r>0 else box(x0,y0,x1,y1)
def dog_hole(x0,y0,x1,y1):
    h=box(x0,y0,x1,y1); c=[Point(x0+D,y0+D),Point(x1-D,y0+D),Point(x0+D,y1-D),Point(x1-D,y1-D)]
    return unary_union([h]+[p.buffer(R,resolution=16) for p in c])
def tenon(x0,y0,x1,y1,root):  # root: 'y0','y1','x0','x1' lado unido al cuerpo
    t=box(x0,y0,x1,y1)
    if root=='y0': cs=[(x0,y0,1,-1),(x1,y0,-1,-1)]
    elif root=='y1': cs=[(x0,y1,1,1),(x1,y1,-1,1)]
    elif root=='x0': cs=[(x0,y0,-1,1),(x0,y1,-1,-1)]
    else: cs=[(x1,y0,1,1),(x1,y1,1,-1)]
    return t,[Point(cx-sx*D,cy-sy*D).buffer(R,resolution=16) for cx,cy,sx,sy in cs]
class Part:
    def __init__(s,id,name,t,mod,step,pose,group=None):
        s.id,s.name,s.t,s.mod,s.step,s.pose=id,name,t,mod,step,pose;s.add=[];s.sub=[];s.pk=[];s.body=None;s.group=group or id;s.note=''
    def tn(s,x0,y0,x1,y1,root):
        t,c=tenon(x0,y0,x1,y1,root);s.add.append(t);s.sub+=c
    def geom(s):
        g=unary_union([s.body]+s.add)
        for h in s.sub: g=g.difference(h)
        return g
PARTS=[]
# ---------- constantes (mm) ----------
W,HT,DP=800,2000,550; SI=20  # costado remetido 20 mm (vuelo lateral de techo/base)
YB0,YB1=100,118; YT0,YT1=1952,1970
TW=60; SDO=550; SDI=476      # costados exteriores 550 (las puertas corren entre ellos), centrales 476
TCO=[70,275,480]; TCI=[70,240,410]
BG=(6,12)                    # ranura del fondo, pegada atrás para ganar fondo útil
RZ=476                       # riel: z 476-550 · ranura B 500-520 · ranura A 524-544
XL,XR=SI+18,1600-SI-18       # caras interiores de los costados exteriores
OPEN=XR-XL; DOOR_W=(OPEN+18)/2; DOOR_H=1810; DY=130
KX=[400,1200]; ROD_Z=245
SL=14; DRAW=1.5; SW=18+0.4
def side(mod,x0,right,pockets,outer):
    sd,tc=(SDO,TCO) if outer else (SDI,TCI)
    pid=f'M{mod}-C{"D" if right else "I"}'
    p=Part(pid,f'Costado {"exterior" if outer else "central"} {"derecho" if right else "izquierdo"} · módulo {mod}',18,mod,2,
        dict(O=[x0+(W-SI-18 if right else SI),0,0],U=[0,0,1],V=[0,1,0],N=[1,0,0]))
    p.body=box(0,YB1,sd,YT0)
    for c in tc:
        p.tn(c-TW/2,YB1-18-25-5,c+TW/2,YB1,'y1'); p.tn(c-TW/2,YT0,c+TW/2,YT0+18+30,'y0')
        p.sub.append(dog_hole(c-SW/2,YB0-SL+DRAW,c+SW/2,YB0+DRAW))
        p.sub.append(dog_hole(c-SW/2,YT1-DRAW,c+SW/2,YT1-DRAW+SL))
    p.pk.append(('RANURA_8MM',box(BG[0],YB1,BG[1],YT0),'Ranura del fondo 6 × 8 mm, cara interior'))
    pk=list(pockets)
    if outer: pk+=[('tab',(488,538,YB1,YB1+18)),('tab',(488,538,YT0-18,YT0))]
    for kind,a in pk:
        if kind=='tab':
            u0,u1,v0,v1=a;p.pk.append(('CAJA_9_5MM',dog_hole(u0-TOL/2,v0-TOL/2,u1+TOL/2,v1+TOL/2),'Caja 9.5 mm, cara interior'))
        else:
            u,v=a;p.pk.append(('CAJA_9_5MM',Point(u,v).buffer(16.25,resolution=24),'Caja ⌀32.5 × 9.5 mm (tubo)'))
    if right: p.pk=[(l,affinity.scale(q,-1,1,origin=(sd/2,0)),d) for l,q,d in p.pk]
    p.note=('Costado exterior de 55 cm: las puertas corren entre los dos costados exteriores; cajas para las pestañas de los rieles al frente. ' if outer else 'Costado central de 47.6 cm: termina antes de los rieles para que las puertas pasen por delante. ')+'Espiga pasante con cuña arriba (remate visible) y abajo (dentro del zócalo).'
    p.tc=tc;PARTS.append(p);return p
def panel_tb(mod,x0,top,sides):
    pid=f'M{mod}-{"T" if top else "B"}'
    p=Part(pid,('Techo' if top else 'Base')+f' · módulo {mod}',18,mod,4 if top else 3,
        dict(O=[x0,YT0 if top else YB0,0],U=[1,0,0],V=[0,0,1],N=[0,1,0]))
    p.body=unary_union([box(0,0,W,DP-20),box(20,0,W-20,DP),Point(20,DP-20).buffer(20,resolution=16),Point(W-20,DP-20).buffer(20,resolution=16)])
    for xs,tc in ((SI,sides[0]),(W-SI-18,sides[1])):
        for c in tc: p.sub.append(dog_hole(xs-TOL/2,c-TW/2-TOL/2,xs+18+TOL/2,c+TW/2+TOL/2))
    p.pk.append(('RANURA_8MM',box(SI+2,BG[0],W-SI-2,BG[1]),'Ranura del fondo 6 × 8 mm, cara '+('inferior' if top else 'superior')))
    if top:
        p.sub.append(dog_hole(400-TW/2-TOL/2,RZ+2-TOL/2,400+TW/2+TOL/2,RZ+20+TOL/2))
        xe=W if mod==1 else 0
        for z in (120,430):
            bt=Polygon([(0,-12.5),(-60,-25),(-60,25),(0,12.5)]) if mod==1 else Polygon([(0,-12.5),(60,-25),(60,25),(0,12.5)])
            p.pk.append(('CAJA_5_5MM',affinity.translate(bt,xe,z).buffer(0.15,join_style=2),'Media caja de mariposa 5.5 mm, cara superior'))
    PARTS.append(p);return p
def inner(mod,x0,pid,name,y,v0,v1,tabs,step):
    p=Part(pid,name,18,mod,step,dict(O=[x0+SI+18-9,y,0],U=[1,0,0],V=[0,0,1],N=[0,1,0]))
    L=W-2*SI-36; p.body=box(9,v0,9+L,v1)
    for a,b in tabs: p.tn(0,a,9,b,'x1'); p.tn(9+L,a,18+L,b,'x0')
    PARTS.append(p);return p
def module(mod,x0,kind):
    pk=[]
    if kind=='larga':
        pk+=[('tab',(80,160,1650,1668)),('tab',(320,400,1650,1668)),('rod',(ROD_Z,1590)),('tab',(60,120,260,278)),('tab',(370,430,170,188))]
    else:
        pk+=[('rod',(ROD_Z,1840)),('rod',(ROD_Z,1000))]
    a=side(mod,x0,False,pk,mod==1); b=side(mod,x0,True,pk,mod==2)
    panel_tb(mod,x0,False,(a.tc,b.tc)); panel_tb(mod,x0,True,(a.tc,b.tc))
    if kind=='larga':
        inner(mod,x0,f'M{mod}-E','Entrepaño sombrerero · módulo '+str(mod),1650,20,465,[(80,160),(320,400)],2)
        inner(mod,x0,f'M{mod}-Z1','Listón zapatera trasero · módulo '+str(mod),260,40,140,[(60,120)],2)
        inner(mod,x0,f'M{mod}-Z2','Listón zapatera frontal · módulo '+str(mod),170,350,450,[(370,430)],2)
    b=Part(f'M{mod}-F','Fondo 5 mm · módulo '+str(mod),5,mod,4,dict(O=[x0+SI+10,YB1-8,BG[0]+0.5],U=[1,0,0],V=[0,1,0],N=[0,0,1]))
    b.body=box(0,0,W-2*SI-20,YT0-YB1+16);PARTS.append(b)
    for i,xc in enumerate((100,682)):
        c=Part(f'M{mod}-X{i+1}','Travesaño de zócalo · módulo '+str(mod),18,mod,1,dict(O=[x0+xc,0,0],U=[0,0,1],V=[0,1,0],N=[1,0,0]),group=f'M{mod}-X')
        c.body=box(20,0,520,100)
        for zr in (30,482): c.sub.append(dog_hole(zr-TOL/2,20-TOL/2,zr+18+TOL/2,80+TOL/2))
        PARTS.append(c)
    for i,zr in enumerate((30,482)):
        r=Part(f'M{mod}-L{i+1}','Larguero de zócalo · módulo '+str(mod),18,mod,1,dict(O=[x0,0,zr],U=[1,0,0],V=[0,1,0],N=[0,0,1]),group=f'M{mod}-L')
        r.body=box(118,0,682,100); r.tn(75,20,118,80,'x1'); r.tn(682,20,725,80,'x0')
        r.sub.append(dog_hole(100-SL+DRAW,50-SW/2,100+DRAW,50+SW/2)); r.sub.append(dog_hole(700-DRAW,50-SW/2,700-DRAW+SL,50+SW/2))
        PARTS.append(r)
module(1,0,'larga');module(2,800,'corta')
# ---------- rieles de una pieza entre costados exteriores ----------
def rail(pid,name,y,gl,gface,keys):
    p=Part(pid,name,18,0,6,dict(O=[XL-9,y,0],U=[1,0,0],V=[0,0,1],N=[0,1,0]))
    p.body=box(9,RZ,9+OPEN,DP); p.tn(0,488,9,538,'x1'); p.tn(9+OPEN,488,18+OPEN,538,'x0')
    for z0 in (500,524): p.pk.append((gl,box(9,z0,9+OPEN,z0+20),gface))
    if keys:
        for xc in KX: p.sub.append(dog_hole(xc-(XL-9)-TW/2-TOL/2,RZ+2-TOL/2,xc-(XL-9)+TW/2+TOL/2,RZ+20+TOL/2))
    p.note='Una sola pieza de %.0f mm (cabe a lo largo de la hoja). Pestañas de 9 mm en las cajas de los costados exteriores.'%(OPEN+18)
    PARTS.append(p)
rail('RI','Riel inferior (una pieza)',YB1,'RANURA_6MM','2 ranuras 20 × 6 mm, cara superior',False)
rail('RS','Riel superior (una pieza)',YT0-18,'RANURA_14MM','2 ranuras 20 × 14 mm, cara inferior',True)
KEYS=[]
for xc in KX:
    p=Part(f'LL{len(KEYS)+1}','Llave colgante del riel superior',18,0,6,dict(O=[xc,0,RZ+2],U=[1,0,0],V=[0,1,0],N=[0,0,1]),group='LL')
    p.body=box(-50,YT0-36,50,YT0-18); p.tn(-TW/2,YT0-18,TW/2,YT1+30,'y0')
    p.sub.append(dog_hole(-SW/2,YT1-DRAW,SW/2,YT1-DRAW+SL)); PARTS.append(p); KEYS.append(xc)
# ---------- puertas de bastidor (largueros, travesaños y parteluz con cola de milano en el plano) ----------
ST,MU=80,70; TR=[(0,160),(610,700),(1700,DOOR_H)]; ROWS=[(160,610),(700,1700)]
DTL,DT0,DT1=20,40,52   # cola: largo 20, ancho 40 en la raíz y 52 en la punta
def dt_tab(xr,yc,dirx):   # cola que sale de un canto vertical en x=xr hacia dirx
    return Polygon([(xr,yc-DT0/2),(xr+dirx*DTL,yc-DT1/2),(xr+dirx*DTL,yc+DT1/2),(xr,yc+DT0/2)])
def dt_tab_v(yr,xc,diry):
    return Polygon([(xc-DT0/2,yr),(xc-DT1/2,yr+diry*DTL),(xc+DT1/2,yr+diry*DTL),(xc+DT0/2,yr)])
def socket(tab,dirv):
    s=tab.buffer(0.15,join_style=2);b=tab.bounds
    return s
WIN=[]
for k,(x,z) in enumerate(((XL,525),(XR-DOOR_W,501))):
    Wd=DOOR_W;mx=Wd/2
    cols=[(ST,mx-MU/2),(mx+MU/2,Wd-ST)]
    rb=unary_union([box(c0-10,a-10,c1+10,b2+10).difference(box(c0,a,c1,b2)) for c0,c1 in cols for a,b2 in ROWS])
    pose=dict(O=[x,DY,z],U=[1,0,0],V=[0,1,0],N=[0,0,1]);tag="AB"[k];dn='izquierda, carril frontal' if k==0 else 'derecha, carril trasero'
    tabs_st=[]
    trs=[]
    for i,(a,b2) in enumerate(TR):
        yc=(a+b2)/2;t=Part(f'P{tag}-T{i+1}',f'Travesaño {["inferior","central","superior"][i]} · puerta {dn}',18,0,7,pose,group=f'PT{i+1}')
        t.body=box(ST,a,Wd-ST,b2);t.add+=[dt_tab(ST,yc,-1),dt_tab(Wd-ST,yc,1)];tabs_st+=[dt_tab(ST,yc,-1),dt_tab(Wd-ST,yc,1)]
        trs.append(t)
    for j,(a,b2) in enumerate(ROWS):
        m=Part(f'P{tag}-M{j+1}',f'Parteluz {["inferior","superior"][j]} · puerta {dn}',18,0,7,pose,group=f'PM{j+1}')
        m.body=box(mx-MU/2,a,mx+MU/2,b2);ta,tb=dt_tab_v(a,mx,-1),dt_tab_v(b2,mx,1);m.add+=[ta,tb]
        trs[j].sub.append(ta.buffer(0.15,join_style=2));trs[j+1].sub.append(tb.buffer(0.15,join_style=2))
        for P_ in (trs[j],trs[j+1]):
            for tt in (ta,tb):
                for cx,cy in list(tt.exterior.coords)[1:3]: P_.sub.append(Point(cx,cy).buffer(3,resolution=12))
        m.pk.append(('CAJA_6MM',m.body.intersection(rb),'Rebaje 10 × 6 mm, cara trasera'));PARTS.append(m)
    for i,(u0,u1) in enumerate(((0,ST),(Wd-ST,Wd))):
        s=Part(f'P{tag}-L{i+1}',f'Larguero {["izquierdo","derecho"][i]} · puerta {dn}',18,0,7,pose,group='PL')
        s.body=box(u0,0,u1,DOOR_H)
        for tt in tabs_st:
            if (tt.bounds[0]<u1 and tt.bounds[2]>u0):
                s.sub.append(tt.buffer(0.15,join_style=2))
                for cx,cy in list(tt.exterior.coords)[1:3]: s.sub.append(Point(cx,cy).buffer(3,resolution=12))
        outer_edge=(k==0 and i==0) or (k==1 and i==1)
        if outer_edge:
            hx=(u0+u1)/2;s.sub.append(unary_union([box(hx-14,845,hx+14,1015),Point(hx,845).buffer(14,resolution=24),Point(hx,1015).buffer(14,resolution=24)]))
            s.note='Lleva la jaladera calada de 28 × 198 mm.'
        s.pk.append(('CAJA_6MM',s.body.intersection(rb),'Rebaje 10 × 6 mm, cara trasera'));PARTS.append(s)
    for t in trs:
        t.pk.append(('CAJA_6MM',t.body.intersection(rb),'Rebaje 10 × 6 mm, cara trasera'));t.note='Cola de milano en cada extremo: entra de canto en el larguero, con Resistol.';PARTS.append(t)
    for ci,(c0,c1) in enumerate(cols):
        for j,(a,b2) in enumerate(ROWS):
            ins=Part(f'Y{tag}{ci+1}{j+1}',f'Panel de yute {"inferior" if j==0 else "superior"}',5,0,7,dict(O=[x+c0-9.5,DY+a-9.5,z+1],U=[1,0,0],V=[0,1,0],N=[0,0,1]),group='Y'+str(j+1))
            ins.body=rbox(0,0,c1-c0+19,b2-a+19,3);ins.jute=True;PARTS.append(ins)
# ---------- cuñas ----------
WEDGE=Polygon([(0,0),(80,0),(80,18),(0,10)])
wedges=[]
for p in [q for q in PARTS if q.id.startswith('M') and '-C' in q.id]:
    right=p.id.endswith('D');x0=800 if p.mod==2 else 0
    xo=x0+(W-5 if right else 5); ux=-1 if right else 1
    for c in p.tc:
        wedges.append(dict(O=[xo,YT1,c-9],U=[ux,0,0],V=[0,1,0],N=[0,0,1],step=4,mod=p.mod))
        wedges.append(dict(O=[xo,YB0,c-9],U=[ux,0,0],V=[0,-1,0],N=[0,0,1],step=3,mod=p.mod))
for mod,x0 in ((1,0),(2,800)):
    for xc,ux in ((100,-1),(700,1)):
        for zr in (30,482):
            wedges.append(dict(O=[x0+xc,41,zr+9-30],U=[0,0,1],V=[ux,0,0],N=[0,1,0],step=1,mod=mod))
for xc in KEYS: wedges.append(dict(O=[xc+9,YT1,RZ+11-31.25],U=[0,0,1],V=[0,1,0],N=[-1,0,0],step=6,mod=0))
for i,w in enumerate(wedges):
    p=Part(f'CU{i+1:02d}','Cuña',18,w['mod'],w['step'],dict(O=w['O'],U=w['U'],V=w['V'],N=w['N']),group='CU');p.body=WEDGE;PARTS.append(p)
for i in range(4):
    p=Part(f'CU{len(wedges)+i+1:02d}','Cuña (repuesto)',18,0,None,None,group='CU');p.body=WEDGE;PARTS.append(p)
BOW=unary_union([Polygon([(0,-12.5),(60,-25),(60,25),(0,12.5)]),Polygon([(0,-12.5),(-60,-25),(-60,25),(0,12.5)])])
BOW=affinity.translate(BOW,60,25)
for i,z in enumerate((120,430)):
    p=Part(f'MA{i+1}','Mariposa de unión entre módulos',5,0,6,dict(O=[800-60,YT1-5.5+5,z-25],U=[1,0,0],V=[0,0,1],N=[0,1,0]),group='MA');p.body=BOW;PARTS.append(p)
TARA=rbox(0,0,44,16,8).difference(Point(8,8).buffer(3.1,resolution=16))
for i in range(32):
    p=Part(f'TA{i+1:02d}','Taravilla (gira a mano y sujeta el panel de yute)',5,0,7,None,group='TA');p.body=TARA;PARTS.append(p)
for p in PARTS: p.g=p.geom()
# ---------- anidado ----------
SHW,SHH,MAR,GAP=1220,2440,10,12
sheets=[]
def nest(t):
    ps=[p for p in PARTS if p.t==t]
    for p in ps:
        b=p.g.bounds;p.bw,p.bh=b[2]-b[0],b[3]-b[1]
    for n in range(1,12):
        pk=rectpack.newPacker(mode=rectpack.PackingMode.Offline,pack_algo=rectpack.MaxRectsBssf,sort_algo=rectpack.SORT_AREA,rotation=True)
        for i,p in enumerate(ps): pk.add_rect(math.ceil(p.bw)+GAP,math.ceil(p.bh)+GAP,rid=i)
        for _ in range(n): pk.add_bin(SHW-2*MAR+GAP,SHH-2*MAR+GAP)
        pk.pack()
        if sum(len(b) for b in pk)==len(ps): break
    out=[]
    for bi,b in enumerate(pk):
        items=[]
        for r in b:
            p=ps[r.rid];rot=(round(r.width-GAP)!=math.ceil(p.bw)) or (math.ceil(p.bw)!=math.ceil(p.bh) and r.width-GAP==math.ceil(p.bh) and r.height-GAP==math.ceil(p.bw))
            g=affinity.translate(p.g,-p.g.bounds[0],-p.g.bounds[1]);pks=[(l,affinity.translate(q,-p.g.bounds[0],-p.g.bounds[1]),d) for l,q,d in p.pk]
            if rot:
                g=affinity.rotate(g,90,origin=(0,0));pks=[(l,affinity.rotate(q,90,origin=(0,0)),d) for l,q,d in pks]
                dx=-g.bounds[0];g=affinity.translate(g,dx,0);pks=[(l,affinity.translate(q,dx,0),d) for l,q,d in pks]
            g=affinity.translate(g,r.x+MAR,r.y+MAR);pks=[(l,affinity.translate(q,r.x+MAR,r.y+MAR),d) for l,q,d in pks]
            p.sheet=len(sheets)+len(out)+1
            items.append(dict(p=p,g=g,pk=pks,rot=rot))
        out.append(dict(t=t,items=items))
    return out
sheets+=nest(18);sheets+=nest(5)
# ---------- DXF ----------
doc=ezdxf.new('R2010',setup=True);msp=doc.modelspace()
for name,col in [('HOJA',8),('CORTE_EXT',1),('CALADO_INTERIOR',5),('CAJA_9_5MM',3),('CAJA_6MM',30),('CAJA_5_5MM',32),('RANURA_8MM',4),('RANURA_6MM',6),('RANURA_14MM',140),('TEXTO',7),('TRAYECTORIA_EXT_FRESA6',11),('TRAYECTORIA_INT_FRESA6',150)]:
    doc.layers.add(name,color=col)
def poly(coords,layer,ox):
    pts=[(x+ox,y) for x,y in list(coords)[:-1]];msp.add_lwpolyline(pts,close=True,dxfattribs={'layer':layer})
def polys(g):
    return [g] if g.geom_type=='Polygon' else list(g.geoms)
SX=1400
for si,s in enumerate(sheets):
    ox=si*SX
    msp.add_lwpolyline([(ox,0),(ox+SHW,0),(ox+SHW,SHH),(ox,SHH)],close=True,dxfattribs={'layer':'HOJA'})
    msp.add_text(f'HOJA {si+1} · triplay {s["t"]} mm · 1220 x 2440',height=30,dxfattribs={'layer':'TEXTO'}).set_placement((ox,SHH+30))
    for it in s['items']:
        for pg in polys(it['g']):
            poly(pg.exterior.coords,'CORTE_EXT',ox)
            for h in pg.interiors: poly(h.coords,'CALADO_INTERIOR',ox)
            te=pg.buffer(R,resolution=16);ti=[Polygon(h.coords).buffer(-R,resolution=16) for h in pg.interiors]
            for q in polys(te): poly(q.exterior.coords,'TRAYECTORIA_EXT_FRESA6',ox)
            for t in ti:
                if not t.is_empty:
                    for q in polys(t): poly(q.exterior.coords,'TRAYECTORIA_INT_FRESA6',ox)
        for l,q,d in it['pk']:
            for pg in polys(q):
                poly(pg.exterior.coords,l,ox)
                for h in pg.interiors: poly(h.coords,l,ox)
        c=it['g'].representative_point() if it['p'].group not in('CU','TA','MA') else it['g'].centroid
        b=it['g'].bounds;hgt=min(28,(b[3]-b[1])*0.35,(b[2]-b[0])/max(len(it['p'].id),1)*1.1)
        msp.add_text(it['p'].id,height=max(hgt,4),dxfattribs={'layer':'TEXTO'}).set_placement((c.x+ox,c.y),align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
doc.header['$INSUNITS']=4
doc.saveas(f'{OUT}/ropero_cnc.dxf');doc.saveas('/workspace/ropero-cnc/ropero_cnc.dxf')
# ---------- medidas de trayectoria (estimación de CNC) ----------
cut_len=0;pk_area=0;gr_len=0
for s in sheets:
    for it in s['items']:
        for pg in polys(it['g']):
            cut_len+=pg.exterior.length+sum(h.length for h in pg.interiors)
        for l,q,d in it['pk']:
            if l.startswith('RANURA'): gr_len+=q.length/2
            else: pk_area+=q.area
# ---------- SVG ----------
def path(g,ox=0,oy=0,sc=1,H=0):
    d=''
    for pg in polys(g):
        for ring in [pg.exterior]+list(pg.interiors):
            cs=list(ring.coords);d+='M'+' L'.join(f'{(x+ox)*sc:.1f},{(H-(y+oy))*sc:.1f}' for x,y in cs)+'Z '
    return d
FILL={'CU':'#C98A4B','TA':'#E3C08C','MA':'#C98A4B'}
sheet_svgs=[]
for si,s in enumerate(sheets):
    sc=0.2;o=f'<svg viewBox="-4 -4 {SHW*sc+8} {SHH*sc+8}" xmlns="http://www.w3.org/2000/svg" class="sheet"><rect x="0" y="0" width="{SHW*sc}" height="{SHH*sc}" fill="#F3E3C6" stroke="#1F2A2E" stroke-width=".6"/>'
    for it in s['items']:
        p=it['p'];col='#E7C38F' if s['t']==18 else '#EBD2A6'
        if getattr(p,'jute',False): col='#CDB27E'
        col=FILL.get(p.group,col)
        o+=f'<path d="{path(it["g"],0,0,sc,SHH)}" fill="{col}" fill-rule="evenodd" stroke="#1F2A2E" stroke-width=".5"><title>{p.id} · {p.name}</title></path>'
        for l,q,d in it['pk']: o+=f'<path d="{path(q,0,0,sc,SHH)}" fill="#9C6B3C" fill-opacity=".35" stroke="none"/>'
        if p.group not in ('CU','TA','MA'):
            from shapely.ops import polylabel
            pg=max(polys(it['g']),key=lambda q:q.area);c=polylabel(pg,tolerance=1);dd=pg.boundary.distance(c);b=it['g'].bounds;vert=(b[3]-b[1])>(b[2]-b[0])*1.5
            fs=min(12,2*dd*sc*0.8,((b[3]-b[1]) if vert else (b[2]-b[0]))*sc/(0.7*len(p.id)+1));tr=f' transform="rotate(-90 {c.x*sc:.1f} {(SHH-c.y)*sc:.1f})"' if vert else ''
            o+=f'<text x="{c.x*sc:.1f}" y="{(SHH-c.y)*sc:.1f}" font-size="{fs:.1f}" text-anchor="middle" dominant-baseline="middle" font-weight="700" fill="#1F2A2E"{tr}>{p.id}</text>'
    o+='</svg>';sheet_svgs.append(o)
def part_svg(p):
    g=affinity.translate(p.g,-p.g.bounds[0],-p.g.bounds[1]);b=g.bounds;L,Wd=b[2],b[3]
    rot=Wd>L*1.3
    if rot: g=affinity.rotate(g,-90,origin=(0,0));g=affinity.translate(g,-g.bounds[0],-g.bounds[1]);b=g.bounds;L,Wd=b[2],b[3]
    sc=min(480/L,200/Wd);pad=30;Hh=Wd*sc
    pk=[]
    for l,q,d in p.pk:
        q=affinity.translate(q,-p.g.bounds[0],-p.g.bounds[1])
        if rot: q=affinity.rotate(q,-90,origin=(0,0));q=affinity.translate(q,-affinity.rotate(affinity.translate(p.g,-p.g.bounds[0],-p.g.bounds[1]),-90,origin=(0,0)).bounds[0],-affinity.rotate(affinity.translate(p.g,-p.g.bounds[0],-p.g.bounds[1]),-90,origin=(0,0)).bounds[1])
        pk.append(q)
    o=f'<svg viewBox="0 0 {L*sc+2*pad} {Hh+2*pad+14}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:560px">'
    o+=f'<path d="{path(g,pad/sc,-pad/sc,sc,Wd)}" fill="{"#CDB27E" if getattr(p,"jute",False) else "#E7C38F"}" fill-rule="evenodd" stroke="#1F2A2E" stroke-width="1"/>'
    for q in pk: o+=f'<path d="{path(q,pad/sc,-pad/sc,sc,Wd)}" fill="#9C6B3C" fill-opacity=".4"/>'
    o+=f'<line x1="{pad}" y1="{Hh+pad+8}" x2="{pad+L*sc}" y2="{Hh+pad+8}" stroke="#D9502B"/><text x="{pad+L*sc/2}" y="{Hh+pad+20}" font-size="11" text-anchor="middle" fill="#D9502B">{L:.1f}</text>'
    o+=f'<line x1="{pad-8}" y1="{pad}" x2="{pad-8}" y2="{pad+Hh}" stroke="#D9502B"/><text x="{pad-12}" y="{pad+Hh/2}" font-size="11" text-anchor="middle" fill="#D9502B" transform="rotate(-90 {pad-12} {pad+Hh/2})">{Wd:.1f}</text></svg>'
    return o
# ---------- datos ----------
def holes_desc(p):
    n=len([1 for pg in polys(p.g) for h in pg.interiors]);return n
groups={}
GN={'M1-X':'Travesaño de zócalo · módulo 1','M2-X':'Travesaño de zócalo · módulo 2','M1-L':'Larguero de zócalo (trasero y frontal) · módulo 1','M2-L':'Larguero de zócalo (trasero y frontal) · módulo 2','Y1':'Panel de yute inferior (removible)','Y2':'Panel de yute superior (removible)','CU':'Cuña (incluye 4 de repuesto)','LL':'Llave colgante del riel superior','PL':'Larguero de puerta (bastidor)','PT1':'Travesaño inferior de puerta','PT2':'Travesaño central de puerta','PT3':'Travesaño superior de puerta','PM1':'Parteluz inferior de puerta','PM2':'Parteluz superior de puerta'}
for p in PARTS:
    groups.setdefault(p.group,[]).append(p)
cut=[]
for gid,ps in groups.items():
    p=ps[0];b=p.g.bounds
    nm=GN.get(gid,p.name.split(' · módulo')[0]) if len(ps)>1 else p.name
    cut.append(dict(id=gid if len(ps)>1 else p.id,name=nm,qty=len(ps),t=p.t,L=round(b[2]-b[0],1),W=round(b[3]-b[1],1),
        holes=holes_desc(p),pk=sorted(set(d for l,q,d in p.pk)),sheets=sorted(set(q.sheet for q in ps)),svg=part_svg(p),note=p.note,members=[q.id for q in ps]))
def poly_js(g):
    out=[]
    for pg in polys(g):
        out.append([[ [round(x,1),round(y,1)] for x,y in pg.exterior.coords[:-1]]]+[[ [round(x,1),round(y,1)] for x,y in h.coords[:-1]] for h in pg.interiors])
    return out
rods=[dict(mod=1,x=SI+18,y=1590,z=ROD_Z),dict(mod=2,x=800+SI+18,y=1840,z=ROD_Z),dict(mod=2,x=800+SI+18,y=1000,z=ROD_Z)]
m3d=[dict(id=p.id,g=p.group,name=p.name,t=p.t,step=p.step,pose=p.pose,shape=poly_js(p.g),jute=getattr(p,'jute',False)) for p in PARTS if p.pose]
n18=len([s for s in sheets if s['t']==18]);n5=len(sheets)-n18
stats=dict(sheets18=n18,sheets5=n5,pieces=len(PARTS),pieces_main=len([p for p in PARTS if p.group not in('CU','TA','MA','LL')]),door_w=round(DOOR_W,1),open_w=round(OPEN-DOOR_W,1),depth_use=round(501-BG[1]),door_h=DOOR_H,wedges=len(groups['CU']),cut_m=round(cut_len/1000,1),pk_m2=round(pk_area/1e6,3),gr_m=round(gr_len/1000,1))
json.dump(dict(rods=rods,rodL=W-2*SI-36+18,stats=stats,cut=cut,m3d=m3d,sheets=sheet_svgs,sheetinfo=[dict(t=s['t'],n=len(s['items']),use=round(sum(i['g'].area for i in s['items'])/(SHW*SHH)*100)) for s in sheets]),open(f'{OUT}/data.json','w'),ensure_ascii=False)
print(stats,[ (s['t'],len(s['items'])) for s in sheets])
