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
W,HT,DP=800,2000,550; SI=20  # costado remetido 20 mm (vuelo de techo/base)
YB0,YB1=100,118; YT0,YT1=1952,1970
TC=[80,275,470]; TW=60
SL=14; DRAW=1.5; SW=18+0.4
def side(mod,x0,right,pockets):
    pid=f'M{mod}-C{"D" if right else "I"}'
    p=Part(pid,f'Costado {"derecho" if right else "izquierdo"} · módulo {mod}',18,mod,2,
        dict(O=[x0+(W-SI-18 if right else SI),0,0],U=[0,0,1],V=[0,1,0],N=[1,0,0]))
    p.body=box(0,YB1,DP,YT0)
    for c in TC:
        p.tn(c-TW/2,YB1-18-25-5,c+TW/2,YB1,'y1'); p.tn(c-TW/2,YT0,c+TW/2,YT0+18+30,'y0')
        p.sub.append(dog_hole(c-SW/2,YB0-SL+DRAW,c+SW/2,YB0+DRAW))      # ranura de cuña inferior
        p.sub.append(dog_hole(c-SW/2,YT1-DRAW,c+SW/2,YT1-DRAW+SL))      # ranura de cuña superior
    p.pk.append(('RANURA_8MM',box(12,YB1,18,YT0),'Ranura del fondo 6 × 8 mm, cara interior'))
    for kind,a in pockets:
        if kind=='tab':
            u0,u1,v0,v1=a;p.pk.append(('CAJA_9_5MM',dog_hole(u0-TOL/2,v0-TOL/2,u1+TOL/2,v1+TOL/2),'Caja 9.5 mm, cara interior'))
        else:
            u,v=a;p.pk.append(('CAJA_9_5MM',Point(u,v).buffer(16.25,resolution=24),'Caja ⌀32.5 × 9.5 mm (tubo)'))
    if right: # espejo: al cortar boca arriba, las cajas quedan en la cara interior
        p.pk=[(l,affinity.scale(q,-1,1,origin=(DP/2,0)),d) for l,q,d in p.pk]
    p.note='Espiga pasante con cuña arriba (sobresale 30 mm: remate) y abajo (dentro del zócalo).'
    PARTS.append(p);return p
def panel_tb(mod,x0,top):
    pid=f'M{mod}-{"T" if top else "B"}'
    p=Part(pid,('Techo' if top else 'Base')+f' · módulo {mod}',18,mod,4 if top else 3,
        dict(O=[x0,YT0 if top else YB0,0],U=[1,0,0],V=[0,0,1],N=[0,1,0]))
    p.body=rbox(0,0,W,DP,0); p.body=p.body.difference(box(0,DP-20,20,DP)).union(Point(20,DP-20).buffer(20,resolution=16).intersection(box(0,DP-20,20,DP))) if False else rbox(0,0,W,DP,0)
    # esquinas frontales redondeadas R20
    fr=unary_union([box(0,0,W,DP-20),box(20,0,W-20,DP),Point(20,DP-20).buffer(20,resolution=16),Point(W-20,DP-20).buffer(20,resolution=16)])
    p.body=fr
    for xs in (SI,W-SI-18):
        for c in TC: p.sub.append(dog_hole(xs-TOL/2,c-TW/2-TOL/2,xs+18+TOL/2,c+TW/2+TOL/2))
    p.pk.append(('RANURA_8MM',box(SI+2,12,W-SI-2,18),'Ranura del fondo 6 × 8 mm, cara '+('inferior' if top else 'superior')))
    if top:  # medias cajas de mariposa en la unión de módulos
        xe=W if mod==1 else 0
        for z in (120,430):
            bt=Polygon([(0,-12.5),(-60,-25),(-60,25),(0,12.5)]) if mod==1 else Polygon([(0,-12.5),(60,-25),(60,25),(0,12.5)])
            bt=affinity.translate(bt,xe,z).buffer(0.15,join_style=2)
            p.pk.append(('CAJA_5_5MM',bt,'Media caja de mariposa 5.5 mm, cara superior'))
    PARTS.append(p);return p
def inner(mod,x0,pid,name,y,v0,v1,tabs,step,grooves=None,gface=None):
    p=Part(pid,name,18,mod,step,dict(O=[x0+SI+18-9,y,0],U=[1,0,0],V=[0,0,1],N=[0,1,0]))
    L=W-2*SI-36; p.body=box(9,v0,9+L,v1)
    for a,b in tabs: p.tn(0,a,9,b,'x1'); p.tn(9+L,a,18+L,b,'x0')
    for g in (grooves or []): p.pk.append((g[2],box(9,g[0],9+L,g[1]),gface))
    PARTS.append(p);return p
# ---------- módulos ----------
def module(mod,x0,kind):
    pk=[]
    R1=(460,550,475,535)
    pk+=[('tab',(475,535,YB1,YB1+18)),('tab',(475,535,YT0-18,YT0))]
    if kind=='larga':
        pk+=[('tab',(80,160,1650,1668)),('tab',(300,380,1650,1668)),('rod',(234,1590)),
             ('tab',(60,120,260,278)),('tab',(350,410,170,188))]
    else:
        pk+=[('rod',(234,1840)),('rod',(234,1000))]
    side(mod,x0,False,pk); side(mod,x0,True,pk)
    panel_tb(mod,x0,False); panel_tb(mod,x0,True)
    inner(mod,x0,f'M{mod}-RI','Riel inferior de puertas · módulo '+str(mod),YB1,460,550,[(475,535)],2,[(490,510,'RANURA_6MM'),(520,540,'RANURA_6MM')],'2 ranuras 20 × 6 mm, cara superior')
    inner(mod,x0,f'M{mod}-RS','Riel superior de puertas · módulo '+str(mod),YT0-18,460,550,[(475,535)],2,[(490,510,'RANURA_14MM'),(520,540,'RANURA_14MM')],'2 ranuras 20 × 14 mm, cara inferior')
    if kind=='larga':
        inner(mod,x0,f'M{mod}-E','Entrepaño sombrerero · módulo '+str(mod),1650,20,445,[(80,160),(300,380)],2)
        inner(mod,x0,f'M{mod}-Z1','Listón zapatera trasero · módulo '+str(mod),260,40,140,[(60,120)],2)
        inner(mod,x0,f'M{mod}-Z2','Listón zapatera frontal · módulo '+str(mod),170,330,430,[(350,410)],2)
    # fondo 5 mm
    b=Part(f'M{mod}-F','Fondo 5 mm · módulo '+str(mod),5,mod,4,dict(O=[x0+SI+10,YB1-8,12],U=[1,0,0],V=[0,1,0],N=[0,0,1]))
    b.body=box(0,0,W-2*SI-20,YT0-YB1+16);PARTS.append(b)
    # zócalo
    for i,xc in enumerate((100,682)):
        c=Part(f'M{mod}-X{i+1}','Travesaño de zócalo · módulo '+str(mod),18,mod,1,dict(O=[x0+xc,0,0],U=[0,0,1],V=[0,1,0],N=[1,0,0]),group=f'M{mod}-X')
        c.body=unary_union([box(20,0,520,100)])
        c.body=rbox(20,0,520,100,0)
        for zr in (30,482): c.sub.append(dog_hole(zr-TOL/2,20-TOL/2,zr+18+TOL/2,80+TOL/2))
        PARTS.append(c)
    for i,zr in enumerate((30,482)):
        r=Part(f'M{mod}-L{i+1}',('Larguero de zócalo trasero' if i==0 else 'Larguero de zócalo frontal')+' · módulo '+str(mod),18,mod,1,dict(O=[x0,0,zr],U=[1,0,0],V=[0,1,0],N=[0,0,1]),group=f'M{mod}-L')
        r.body=box(118,0,682,100); r.tn(75,20,118,80,'x1'); r.tn(682,20,725,80,'x0')
        r.sub.append(dog_hole(100-SL+DRAW,50-SW/2,100+DRAW,50+SW/2)); r.sub.append(dog_hole(700-DRAW,50-SW/2,700-DRAW+SL,50+SW/2))
        PARTS.append(r)
    # puertas
    for k,(dx,z,hside) in enumerate(((0,521,'I'),(347,491,'D'))):
        d=Part(f'M{mod}-P{"AB"[k]}',f'Puerta {"frontal" if k==0 else "trasera"} · módulo {mod}',18,mod,6,dict(O=[x0+SI+18+dx,130,z],U=[1,0,0],V=[0,1,0],N=[0,0,1]))
        d.body=rbox(0,0,377,1810,6)
        d.sub+=[rbox(70,160,307,610,40),rbox(70,700,307,1700,40)]
        hx=35 if k==0 else 342
        d.sub.append(unary_union([box(hx-14,845,hx+14,1015),Point(hx,845).buffer(14,resolution=24),Point(hx,1015).buffer(14,resolution=24)]))
        for (a,b2) in ((160,610),(700,1700)): d.pk.append(('CAJA_6MM',rbox(60,a-10,317,b2+10,50).difference(rbox(70,a,307,b2,40)),'Rebaje 10 × 6 mm cara trasera (asiento del panel de yute)'))
        PARTS.append(d)
        for j,(a,b2) in enumerate(((160,610),(700,1700))):
            ins=Part(f'M{mod}-Y{"AB"[k]}{j+1}',f'Panel de yute {"inferior" if j==0 else "superior"} · puerta {"frontal" if k==0 else "trasera"} · módulo {mod}',5,mod,6,dict(O=[x0+SI+18+dx+60,130+a-10,z+1],U=[1,0,0],V=[0,1,0],N=[0,0,1]),group='Y'+str(j+1))
            ins.body=rbox(0,0,257,b2-a+20,50);ins.jute=True;PARTS.append(ins)
module(1,0,'larga');module(2,800,'corta')
# cuñas (3D + corte)
WEDGE=Polygon([(0,0),(80,0),(80,18),(0,10)])
wedges=[]
for mod,x0 in ((1,0),(2,800)):
    for right in (False,True):
        xo=x0+(W-5 if right else 5); ux=-1 if right else 1
        for c in TC:
            wedges.append(dict(O=[xo,YT1,c-9],U=[ux,0,0],V=[0,1,0],N=[0,0,1],step=4,mod=mod))
            wedges.append(dict(O=[xo,YB0,c-9],U=[ux,0,0],V=[0,-1,0],N=[0,0,1],step=3,mod=mod))
    for xc,ux in ((100,-1),(700,1)):
        for zr in (30,482):
            wedges.append(dict(O=[x0+xc,41,zr+9-30],U=[0,0,1],V=[ux,0,0],N=[0,1,0],step=1,mod=mod))
for i,w in enumerate(wedges):
    p=Part(f'CU{i+1:02d}','Cuña',18,w['mod'],w['step'],dict(O=w['O'],U=w['U'],V=w['V'],N=w['N']),group='CU');p.body=WEDGE;PARTS.append(p)
for i in range(4):  # cuñas de repuesto
    p=Part(f'CU{len(wedges)+i+1:02d}','Cuña (repuesto)',18,0,None,None,group='CU');p.body=WEDGE;PARTS.append(p)
# mariposas (5 mm) y taravillas (5 mm)
BOW=unary_union([Polygon([(0,-12.5),(60,-25),(60,25),(0,12.5)]),Polygon([(0,-12.5),(-60,-25),(-60,25),(0,12.5)])])
BOW=affinity.translate(BOW,60,25)
for i,z in enumerate((120,430)):
    p=Part(f'MA{i+1}','Mariposa de unión entre módulos',5,0,5,dict(O=[800-60,YT1-5.5+5,z-25],U=[1,0,0],V=[0,0,1],N=[0,1,0]),group='MA');p.body=BOW;PARTS.append(p)
TARA=rbox(0,0,44,16,8).difference(Point(8,8).buffer(3.1,resolution=16))
for i in range(32):
    p=Part(f'TA{i+1:02d}','Taravilla (gira a mano y sujeta el panel de yute)',5,0,6,None,group='TA');p.body=TARA;PARTS.append(p)
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
            c=it['g'].representative_point();b=it['g'].bounds;fs=min(13,(b[2]-b[0])*sc/4.2,(b[3]-b[1])*sc/1.6)
            o+=f'<text x="{c.x*sc:.1f}" y="{(SHH-c.y)*sc:.1f}" font-size="{fs:.1f}" text-anchor="middle" dominant-baseline="middle" font-weight="700" fill="#1F2A2E">{p.id}</text>'
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
GN={'M1-X':'Travesaño de zócalo · módulo 1','M2-X':'Travesaño de zócalo · módulo 2','M1-L':'Larguero de zócalo (trasero y frontal) · módulo 1','M2-L':'Larguero de zócalo (trasero y frontal) · módulo 2','Y1':'Panel de yute inferior (removible)','Y2':'Panel de yute superior (removible)','CU':'Cuña (incluye 4 de repuesto)'}
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
rods=[dict(mod=1,x=SI+18,y=1590,z=234),dict(mod=2,x=800+SI+18,y=1840,z=234),dict(mod=2,x=800+SI+18,y=1000,z=234)]
m3d=[dict(id=p.id,g=p.group,name=p.name,t=p.t,step=p.step,pose=p.pose,shape=poly_js(p.g),jute=getattr(p,'jute',False)) for p in PARTS if p.pose]
n18=len([s for s in sheets if s['t']==18]);n5=len(sheets)-n18
stats=dict(sheets18=n18,sheets5=n5,pieces=len(PARTS),pieces_main=len([p for p in PARTS if p.group not in('CU','TA','MA')]),wedges=len(groups['CU']),cut_m=round(cut_len/1000,1),pk_m2=round(pk_area/1e6,3),gr_m=round(gr_len/1000,1))
json.dump(dict(rods=rods,rodL=W-2*SI-36+18,stats=stats,cut=cut,m3d=m3d,sheets=sheet_svgs,sheetinfo=[dict(t=s['t'],n=len(s['items']),use=round(sum(i['g'].area for i in s['items'])/(SHW*SHH)*100)) for s in sheets]),open(f'{OUT}/data.json','w'),ensure_ascii=False)
print(stats,[ (s['t'],len(s['items'])) for s in sheets])
