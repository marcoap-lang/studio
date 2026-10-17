# Plantillas 1:1 v5 · guía + hojas por pieza + PDFs por paso
import math, os
INK,GREY,SAGE,ACC,BG='#1F2A2E','#6B7B78','#DCE3DC','#D9502B','#F4F3EE'
SUP='#3E7C6B'
PW,PH=215.9,279.4; MX=8; TOP=42; CW=PW-2*MX; CH=196; OV=12
VIS={'03s':'cara oculta (arriba del techo)','03i':'cara oculta (abajo del techo, al frente)','04i':'cara oculta (abajo del piso)','05d':'cara buena (derecha, se ve por dentro)','05i':'cara buena (izquierda, se ve por dentro)','01':'cara buena (interior)','02':'cara buena (interior)','06':'cara oculta (abajo)','41':'cara oculta (abajo)','07':'cara oculta (abajo)','10':'cara oculta (interior del zócalo)','16':'cara oculta (frente del bastidor, bajo la tapa)'}
def E(s):return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def T(x,y,t,fs,c=INK,a='start',w=500,fam='Inter',extra=''):return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{fs}" fill="{c}" text-anchor="{a}" font-weight="{w}" font-family="{fam},system-ui,sans-serif" {extra}>{E(t)}</text>'
def L(x1,y1,x2,y2,w=.4,c=INK,d=''):return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}" {f"stroke-dasharray=\"{d}\"" if d else ""}/>'
def bitd(h):
    if h['k']=='pocket':return 'Broca Kreg ⌀3/8″ (9.5 mm)'
    if h['k']=='vent':return 'Sierra copa ⌀25 mm'
    return 'Broca ⌀'+h['bit'].replace('guía ','')
def depthd(h):
    if h['k']=='pocket':return 'Prof.: collar Kreg en 3/4″ (18 mm)'
    if h['k']=='vent':return 'Prof.: pasado (6 mm)'
    d=h['depth'].split(' ')[0];return f'Prof. {d} mm · bandera de cinta a {d} mm de la punta'
def sym(k,x,y,toward=1,cross=True):
    o=''
    if k=='pocket':
        w=9.5;l=22;x0=x-l if toward<0 else x
        o+=f'<rect x="{x0 if toward>0 else x-l:.2f}" y="{y-w/2:.2f}" width="{l}" height="{w}" rx="{w/2}" fill="{ACC}" fill-opacity=".18" stroke="{ACC}" stroke-width=".5"/>'
        o+=f'<path d="M{x+(l-3)*toward:.2f} {y:.2f}l{-3*toward:.2f} -2.2v4.4z" fill="{ACC}"/>'
        r=3
    elif k=='screw':o+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="#fff" stroke="{INK}" stroke-width=".6"/>';r=3.2
    elif k=='support':o+=f'<path d="M{x:.2f} {y-4.5:.2f}l4.5 4.5l-4.5 4.5l-4.5 -4.5z" fill="#fff" stroke="{SUP}" stroke-width=".7"/>';r=4.5
    else:o+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="12.5" fill="none" stroke="{GREY}" stroke-width=".6" stroke-dasharray="1.5 1"/>';r=12.5
    # cruz de centro para puntear
    if not cross:return o
    o+=L(x-r-3,y,x+r+3,y,.25)+L(x,y-r-3,x,y+r+3,.25)+f'<circle cx="{x:.2f}" cy="{y:.2f}" r=".5" fill="{INK}"/>'
    return o
COLK={'pocket':ACC,'screw':INK,'support':SUP,'vent':GREY}
NAMEK={'pocket':'Pocket (bolsillo Kreg)','screw':'Tornillo directo','support':'Soporte de tubo (centro)','vent':'Ventilación'}
def legend(y,kinds):
    o=T(MX,y,'Leyenda:',2.8,w=700);x=MX+15
    for k in ['pocket','screw','support','vent']:
        if k not in kinds:continue
        o+=sym(k,x+3,y-1,1,False) if k!='vent' else f'<circle cx="{x+3}" cy="{y-1}" r="2.5" fill="none" stroke="{GREY}" stroke-width=".6" stroke-dasharray="1 .7"/>'
        o+=T(x+(28 if k=='pocket' else 9),y,NAMEK[k],2.6,COLK[k],w=600);x+=(70 if k=='pocket' else 46)
    return o
def ruler(y):
    o=L(MX,y,MX+100,y,.4)
    for i in range(0,101):
        h=3 if i%10==0 else (2 if i%5==0 else 1.1);o+=L(MX+i,y,MX+i,y-h,.18 if i%10 else .3)
    o+=T(MX,y-4,'0',2.4)+T(MX+100,y-4,'10 cm',2.4,a='middle')
    o+=T(MX+106,y-1.5,'Imprime al 100 % («Tamaño real»), sin ajustar. Esta regla mide 10 cm.',2.6,w=600)
    return o
# ---------- hojas ----------
def zones(f):
    h=f['h']
    if not h:return [(0,min(f['L'],180),0,min(f['W'],150),[])]
    cl=[]
    for p in h:
        hit=[c for c in cl if any(math.hypot(p['xd']-q['xd'],p['y']-q['y'])<=200 for q in c)]
        cl=[c for c in cl if c not in hit]+[[p]+[q for c in hit for q in c]]
    out=[]
    for g in sorted(cl,key=lambda g:(min(p['xd'] for p in g),min(p['y'] for p in g))):
        x0=min(p['xd'] for p in g)-30;x1=max(p['xd'] for p in g)+70;y0=min(p['y'] for p in g)-30;y1=max(p['y'] for p in g)+30
        if x0<140:x0=0
        if y0<140:y0=0
        if f['L']-x1<140:x1=f['L']
        if f['W']-y1<140:y1=f['W']
        out.append((max(0,x0),min(f['L'],x1),max(0,y0),min(f['W'],y1),g))
    return out
def sheets_of(f):
    out=[];seam=[0]
    for zi,(x0,x1,y0,y1,g) in enumerate(zones(f)):
        w,h=x1-x0,y1-y0
        nx=max(1,math.ceil((w-OV)/(CW-OV)));ny=max(1,math.ceil((h-OV)/(CH-OV)))
        lettersH={};lettersV={}
        for j in range(ny):
            for i in range(nx-1): lettersH[(i,j)]=chr(65+seam[0]%26);seam[0]+=1
        for j in range(ny-1):
            for i in range(nx): lettersV[(i,j)]=chr(65+seam[0]%26);seam[0]+=1
        for j in range(ny):
            for i in range(nx):
                tx0=x0+i*(CW-OV);ty0=y0+j*(CH-OV)
                out.append(dict(z=zi,nz=None,i=i,j=j,nx=nx,ny=ny,x0=tx0,y0=ty0,x1=min(tx0+CW,x1),y1=min(ty0+CH,y1),zone=(x0,x1,y0,y1),LH=lettersH,LV=lettersV))
    for s in out:s['nz']=len(set(t['z'] for t in out))
    return out
def thumb(f,s,x,y,w,h):
    sc=min(w/f['L'],h/f['W']);W,H=f['L']*sc,f['W']*sc;ox,oy=x+(w-W)/2,y+(h-H)/2
    o=f'<rect x="{ox:.2f}" y="{oy:.2f}" width="{W:.2f}" height="{H:.2f}" fill="#E8C99A" stroke="{INK}" stroke-width=".35"/>'
    for hl in f['h']:o+=f'<circle cx="{ox+hl["xd"]*sc:.2f}" cy="{oy+H-hl["y"]*sc:.2f}" r=".45" fill="{COLK[hl["k"]]}"/>'
    o+=f'<rect x="{ox+s["x0"]*sc:.2f}" y="{oy+H-s["y1"]*sc:.2f}" width="{max(.8,(s["x1"]-s["x0"])*sc):.2f}" height="{max(.8,(s["y1"]-s["y0"])*sc):.2f}" fill="{ACC}" fill-opacity=".35" stroke="{ACC}" stroke-width=".5"/>'
    o+=T(ox,oy+H+3,'ref. X' if not f['mirror'] else '',1.9,GREY)+T(ox+W,oy+H+3,'ref. X' if f['mirror'] else '',1.9,GREY,a='end')
    return o
def sheet_svg(f,s,k,n,pn,ptot,step=None):
    o=[f'<svg class="pg" viewBox="0 0 {PW} {PH}" width="{PW}mm" height="{PH}mm" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<rect width="{PW}" height="{PH}" fill="#fff"/>')
    # header
    o.append(f'<circle cx="{MX+8}" cy="{MX+8}" r="8" fill="{ACC}"/>'+T(MX+8,MX+10.6,f"{f['no']:02d}",7,'#fff','middle',700))
    o.append(T(MX+20,MX+6,f['name'].split(' · ')[0]+(f"  ×{f['count']}" if f['count']>1 else ''),5.4,w=600,fam='Fraunces'))
    o.append(T(MX+20,MX+11.5,'Cara: '+VIS.get(f['id'],f['name'].split(' · ')[-1]),3,w=600))
    o.append(T(MX+20,MX+16,('DIBUJADA EN ESPEJO: así la ves con la pieza volteada, esta cara hacia ti.' if f['mirror'] else 'Vista de frente a esta cara.'),2.6,ACC if f['mirror'] else GREY,w=600))
    o.append(T(MX+20,MX+20.5,f"X se mide desde: {f['xr']} · Y desde: {f['yr']}",2.5,GREY))
    o.append(T(MX+20,MX+25.5,f"Hoja {k} de {n} de esta pieza"+(f" · zona {s['z']+1} de {s['nz']}" if s['nz']>1 else '')+(f" · fila {s['j']+1}, columna {s['i']+1}" if s['nx']*s['ny']>1 else ''),3,w=700))
    o.append(T(PW-MX,MX+3,f"{('Paso '+str(step)+' · ') if step else ''}pág. {pn}/{ptot}",2.4,GREY,'end'))
    o.append(thumb(f,s,PW-MX-46,MX+5,46,24)+T(PW-MX-23,MX+33,'dónde va esta hoja',2.2,GREY,'middle'))
    o.append(L(MX,TOP-4,PW-MX,TOP-4,.5))
    # content mapping
    def P(x,y):return (MX+(x-s['x0']), TOP+CH-(y-s['y0']))
    o.append(f'<clipPath id="c{pn}"><rect x="{MX}" y="{TOP}" width="{CW}" height="{CH}"/></clipPath><g clip-path="url(#c{pn})">')
    # pieza (contorno + relleno suave)
    a=P(0,f['W']);b=P(f['L'],0)
    o.append(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{b[0]-a[0]:.2f}" height="{b[1]-a[1]:.2f}" fill="{BG}" stroke="{INK}" stroke-width="1"/>')
    # traslapes y cortes
    if s['i']<s['nx']-1:
        xa,_=P(s['x0']+CW-OV,0);o.append(f'<rect x="{xa:.2f}" y="{TOP}" width="{OV}" height="{CH}" fill="{SAGE}" fill-opacity=".7"/>'+T(xa+OV/2,TOP+CH/2,'TRASLAPE · aquí se encima la hoja siguiente',2.4,INK,'middle',600,extra=f'transform="rotate(-90 {xa+OV/2:.2f} {TOP+CH/2:.2f})"'))
    if s['j']<s['ny']-1:
        _,ya=P(0,s['y0']+CH-OV);ya-=OV;o.append(f'<rect x="{MX}" y="{ya:.2f}" width="{CW}" height="{OV}" fill="{SAGE}" fill-opacity=".7"/>'+T(MX+CW/2,ya+OV/2+1,'TRASLAPE · aquí se encima la hoja de arriba',2.4,INK,'middle',600))
    if s['i']>0: o.append(L(MX+.3,TOP,MX+.3,TOP+CH,.5,ACC,'2 1.2')+T(MX+2,TOP+5,'✂ recorta por aquí',2.6,ACC,w=700))
    if s['j']>0: o.append(L(MX,TOP+CH-.3,MX+CW,TOP+CH-.3,.5,ACC,'2 1.2')+T(MX+CW-2,TOP+CH-2,'✂ recorta por aquí',2.6,ACC,'end',700))
    # marcas de registro
    def reg(x,y,l):
        q=P(x,y);return f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="3.6" fill="#fff" stroke="{INK}" stroke-width=".5"/>'+L(q[0]-5,q[1],q[0]+5,q[1],.25)+L(q[0],q[1]-5,q[0],q[1]+5,.25)+T(q[0]+4.6,q[1]-3,l,3.6,INK,w=800)
    zx0,zx1,zy0,zy1=s['zone']
    for (i,j),l in s['LH'].items():
        if j==s['j'] and i in (s['i'],s['i']-1):
            xs=s['x0']+(CW-OV/2 if i==s['i'] else OV/2) if True else 0
            xs=zx0+i*(CW-OV)+CW-OV/2;ylo=zy0+j*(CH-OV);yhi=min(ylo+CH,zy1)
            for t in (.3,.7):o.append(reg(xs,ylo+(yhi-ylo)*t,l))
    for (i,j),l in s['LV'].items():
        if i==s['i'] and j in (s['j'],s['j']-1):
            ys=zy0+j*(CH-OV)+CH-OV/2;xlo=zx0+i*(CW-OV);xhi=min(xlo+CW,zx1)
            for t in (.3,.7):o.append(reg(xlo+(xhi-xlo)*t,ys,l))
    # esquinas en L
    for cx,cy in ((0,0),(f['L'],0),(0,f['W']),(f['L'],f['W'])):
        if s['x0']-1<=cx<=s['x0']+CW+1 and s['y0']-1<=cy<=s['y0']+CH+1:
            q=P(cx,cy);dx=1 if cx==0 else -1;dy=-1 if cy==0 else 1
            o.append(f'<path d="M{q[0]+dx*16:.2f} {q[1]:.2f}H{q[0]:.2f}V{q[1]+dy*16:.2f}" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
            o.append(T(q[0]+dx*3,q[1]+dy*(-2.2 if dy<0 else 4.5)*-1 if False else q[1]+(dy*20 if True else 0),'◣ esquina de la pieza: empuja aquí',2.4,ACC,'start' if dx>0 else 'end',700))
    # cantos rotulados
    for xe,isref in ((0,not f['mirror']),(f['L'],f['mirror'])):
        if s['x0']-1<=xe<=s['x0']+CW+1:
            q=P(xe,(max(s['y0'],0)+min(s['y0']+CH,f['W']))/2);dx=3.5 if xe==0 else -2
            o.append(T(q[0]+dx,q[1],('CANTO DE REFERENCIA X · '+f['xr']) if isref else 'canto opuesto',2.6,INK,'middle',700,extra=f'transform="rotate(-90 {q[0]+dx:.2f} {q[1]:.2f})"'))
    for ye,isref in ((0,True),(f['W'],False)):
        if s['y0']-1<=ye<=s['y0']+CH+1:
            q=P((max(s['x0'],0)+min(s['x0']+CW,f['L']))/2,ye);dy=-2 if ye==0 else 4
            o.append(T(q[0],q[1]+dy,('CANTO DE REFERENCIA Y · '+f['yr']) if isref else 'canto opuesto',2.6,INK,'middle',700))
    # agujeros
    vis=[h for h in f['h'] if s['x0']-0.1<=h['xd']<=s['x0']+CW+.1 and s['y0']-.1<=h['y']<=s['y0']+CH+.1]
    vis.sort(key=lambda h:(h['y'],h['xd']))
    placed=[]
    for h in vis:
        q=P(h['xd'],h['y']);toward=-1 if h['xd']>f['L']/2 else 1
        o.append(sym(h['k'],q[0],q[1],toward))
        lines=[(f"{h['u']} · {NAMEK[h['k']]}",COLK[h['k']],700),(bitd(h)+(' · '+h['cs'] if h['cs'] not in ('—','') else ''),INK,500),(depthd(h),INK,500),('Tornillo: '+h['screw'] if h['k']!='vent' else 'Sin tornillo',INK,500),(f"X {h['x']:g} · Y {h['y']:g} mm",GREY,500)]
        bw,bh=62,16.5
        cands=[(q[0]+8,q[1]-bh-3),(q[0]+8,q[1]+5),(q[0]-8-bw,q[1]-bh-3),(q[0]-8-bw,q[1]+5)]
        if h['k']=='pocket' and toward>0: cands=[(q[0]+26,q[1]-bh/2),(q[0]+8,q[1]-bh-6),(q[0]+8,q[1]+7)]+cands
        if h['k']=='pocket' and toward<0: cands=[(q[0]-26-bw,q[1]-bh/2),(q[0]-8-bw,q[1]-bh-6),(q[0]-8-bw,q[1]+7)]+cands
        best=None
        for bx,by in cands:
            bx=min(max(bx,MX+1),MX+CW-bw-1);by=min(max(by,TOP+1),TOP+CH-bh-1)
            if not any(bx<px+pw and px<bx+bw and by<py+ph and py<by+bh for px,py,pw,ph in placed):best=(bx,by);break
        if not best:best=(min(max(cands[0][0],MX+1),MX+CW-bw-1),min(max(cands[0][1],TOP+1),TOP+CH-bh-1))
        bx,by=best;placed.append((bx,by,bw,bh))
        o.append(f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bw}" height="{bh}" rx="1.2" fill="#fff" fill-opacity=".93" stroke="{COLK[h["k"]]}" stroke-width=".35"/>')
        o.append(L(q[0],q[1],bx if bx>q[0] else bx+bw,by+bh/2,.25,COLK[h['k']]))
        for li,(t,c,w) in enumerate(lines):o.append(T(bx+1.5,by+3.3+li*3.05,t,2.45,c,w=w))
    o.append('</g>')
    o.append(f'<rect x="{MX}" y="{TOP}" width="{CW}" height="{CH}" fill="none" stroke="{GREY}" stroke-width=".25" stroke-dasharray="1.5 1"/>')
    if f['pend']:
        o.append(f'<rect x="{MX+20}" y="{TOP+CH/2-14}" width="{CW-40}" height="28" rx="2" fill="#fff" stroke="{ACC}" stroke-width="1"/>'+T(PW/2,TOP+CH/2-4,'PENDIENTE: MEDIR RIEL COMPRADO',6,ACC,'middle',800)+T(PW/2,TOP+CH/2+4,f['pend'][:95],2.6,INK,'middle')+T(PW/2,TOP+CH/2+8,f['pend'][95:190],2.6,INK,'middle'))
    o.append(legend(TOP+CH+9,set(h['k'] for h in f['h']) or {'screw'}))
    o.append(T(MX,TOP+CH+15,'Punzona el centro de cada cruz con un punzón o clavo, quita la plantilla y perfora con tope de profundidad (bandera de cinta en la broca).',2.5,GREY))
    o.append(ruler(PH-MX-3))
    o.append('</svg>')
    return ''.join(o)
# ---------- guía ----------
def guide():
    g1=[f'<svg class="pg" viewBox="0 0 {PW} {PH}" width="{PW}mm" height="{PH}mm" xmlns="http://www.w3.org/2000/svg"><rect width="{PW}" height="{PH}" fill="#fff"/>']
    g1.append(T(MX,MX+4,'STRATE STUDIO · ROPERO PINO & YUTE',2.8,GREY,w=600)+T(MX,MX+16,'Cómo usar las plantillas 1:1',10,w=600,fam='Fraunces')+T(MX,MX+23,'Seis pasos. Hazlo con calma la primera vez; después es rapidísimo.',3.4,GREY))
    def box(n,x,y,w,h,title,lines):
        r=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{BG}" stroke="{SAGE}" stroke-width=".6"/><circle cx="{x+7}" cy="{y+7}" r="4.5" fill="{ACC}"/>'+T(x+7,y+8.6,str(n),4.4,'#fff','middle',700)+T(x+14,y+8.6,title,4.2,w=600,fam='Fraunces')
        for i,t in enumerate(lines):r+=T(x+5,y+16+i*4.3,t,3,INK)
        return r
    W2=(CW-6)/2;Hb=70
    # 1 imprimir
    x,y=MX,MX+30;yb=y;g1.append(box(1,x,y,W2,Hb,'Imprime a tamaño real',['Papel carta. En el diálogo elige «Tamaño real»','o «100 %». Desactiva «Ajustar a la página».']));y=yb+12
    g1.append(f'<rect x="{x+14}" y="{y+16}" width="66" height="38" rx="2" fill="#fff" stroke="{INK}" stroke-width=".5"/>'+T(x+18,y+22,'Imprimir',3,w=700))
    for i,(t,on) in enumerate((('Ajustar a la página',0),('Tamaño real (100 %)',1))):
        yy=y+30+i*9;g1.append(f'<circle cx="{x+21}" cy="{yy}" r="2.2" fill="{"#fff" if not on else ACC}" stroke="{INK}" stroke-width=".4"/>'+T(x+26,yy+1.1,t,3,INK if on else GREY,w=700 if on else 400))
    g1.append(T(x+56,y+40,'✓',6,ACC,w=800))
    # 2 regla
    x=MX+W2+6;y=yb;yb=y;g1.append(box(2,x,y,W2,Hb,'Verifica la regla',['Mide la regla de 10 cm de cada hoja con tu','flexómetro. Si no da 10 cm, no la uses.']));y=yb+12
    rr=L(x+8,y+40,x+88,y+40,.5)
    for i in range(0,81,4):rr+=L(x+8+i,y+40,x+8+i,y+37 if i%20 else y+35,.3)
    g1.append(rr+f'<rect x="{x+8}" y="{y+44}" width="80" height="8" fill="#F2D24B" stroke="{INK}" stroke-width=".4"/>'+''.join(L(x+8+i,y+44,x+8+i,y+47,.25) for i in range(0,81,4))+T(x+48,y+31,'= 10 cm',3.4,ACC,'middle',700))
    # 3 armar hojas
    x,y=MX,MX+30+Hb+6;yb=y;g1.append(box(3,x,y,W2,Hb,'Une las hojas por letras',['Recorta el margen marcado ✂ y encima la hoja','sobre la zona verde: A con A, B con B. Cinta.']));y=yb+12
    g1.append(f'<rect x="{x+10}" y="{y+16}" width="40" height="40" fill="#fff" stroke="{INK}" stroke-width=".5"/><rect x="{x+42}" y="{y+16}" width="8" height="40" fill="{SAGE}"/><rect x="{x+44}" y="{y+19}" width="40" height="40" fill="#fff" fill-opacity=".85" stroke="{INK}" stroke-width=".5"/>'+L(x+44,y+19,x+44,y+59,.6,ACC,'1.5 1'))
    for yy,l in ((y+27,'A'),(y+45,'A')):g1.append(f'<circle cx="{x+47}" cy="{yy}" r="2.4" fill="#fff" stroke="{INK}" stroke-width=".4"/>'+T(x+50,yy-2,l,3.4,w=800))
    g1.append(T(x+60,y+64,'↔',5,ACC,'middle',700))
    # 4 pegar a la pieza
    x=MX+W2+6;y=yb;yb=y;g1.append(box(4,x,y,W2,Hb,'Pega y alinea la esquina',['Cinta masking sobre la cara indicada. La L','naranja va justo contra la esquina de la pieza.']));y=yb+12
    g1.append(f'<rect x="{x+10}" y="{y+16}" width="76" height="40" fill="#E8C99A" stroke="{INK}" stroke-width=".6"/><rect x="{x+10}" y="{y+16}" width="34" height="28" fill="#fff" stroke="{INK}" stroke-width=".4"/><path d="M{x+10} {y+30}V{y+16}H{x+24}" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
    for xx,yy in ((x+40,y+18),(x+18,y+40)):g1.append(f'<rect x="{xx-5}" y="{yy-2}" width="10" height="4" fill="#F5E6B8" stroke="{GREY}" stroke-width=".3" transform="rotate(-20 {xx} {yy})"/>')
    # 5 puntear
    x,y=MX,MX+30+2*(Hb+6);yb=y;g1.append(box(5,x,y,W2,Hb,'Marca los centros',['Golpea el centro de cada cruz con punzón o','clavo y martillo. Quita la plantilla.']));y=yb+12
    g1.append(L(x+20,y+48,x+76,y+48,.5)+L(x+48,y+40,x+48,y+56,.3)+L(x+40,y+48,x+56,y+48,.3)+f'<path d="M{x+48} {y+46}L{x+45} {y+28}H{x+51}Z" fill="{GREY}"/><rect x="{x+44}" y="{y+17}" width="8" height="11" rx="1" fill="{INK}"/>')
    # 6 perforar
    x=MX+W2+6;y=yb;yb=y;g1.append(box(6,x,y,W2,Hb,'Perfora con tope',['Pon una bandera de cinta en la broca a la','profundidad indicada. Para justo al tocarla.']));y=yb+12
    g1.append(f'<rect x="{x+20}" y="{y+40}" width="60" height="14" fill="#E8C99A" stroke="{INK}" stroke-width=".5"/><rect x="{x+48}" y="{y+18}" width="4" height="30" fill="{GREY}"/><path d="M{x+52} {y+30}h12v5h-12z" fill="#F2D24B" stroke="{INK}" stroke-width=".3"/>'+T(x+66,y+33.5,'bandera',2.8,w=600)+L(x+56,y+40,x+56,y+48,.4)+T(x+58,y+47,'prof.',2.6,GREY))
    g1.append(ruler(PH-MX-3)+'</svg>')
    g2=[f'<svg class="pg" viewBox="0 0 {PW} {PH}" width="{PW}mm" height="{PH}mm" xmlns="http://www.w3.org/2000/svg"><rect width="{PW}" height="{PH}" fill="#fff"/>']
    g2.append(T(MX,MX+12,'Cómo leer una hoja',9,w=600,fam='Fraunces'))
    y=MX+24
    items=[('pocket','Pocket (bolsillo Kreg)','Centra la guía Kreg en la cruz; el bolsillo sale hacia donde apunta la flecha. Collar en 3/4″.'),
           ('screw','Tornillo directo','Broca guía del diámetro indicado y luego avellanador. La profundidad va con bandera de cinta.'),
           ('support','Soporte de tubo','La cruz es el CENTRO del soporte. Presenta el soporte centrado y marca sus 2 agujeros.'),
           ('vent','Ventilación','Sierra copa ⌀25, de lado a lado (solo en el fondo).')]
    for k,t,d in items:
        g2.append(sym(k,MX+8 if k!='pocket' else MX+4,y,1)+T(MX+34,y-1,t,3.6,COLK[k],w=700)+T(MX+34,y+4,d,2.9));y+=17
    y+=2;g2.append(T(MX,y,'Partes de la hoja',5,w=600,fam='Fraunces'));y+=8
    parts=[('Círculo naranja con número','número de pieza (está escrito a lápiz en la pieza).'),('Cara','qué cara va hacia ti. «En espejo» = la pieza está volteada (cara de abajo hacia ti).'),('Miniatura arriba a la derecha','la pieza completa; el rectángulo naranja es esta hoja.'),('L naranja','esquina real de la pieza: empújala contra la esquina del tablero.'),('Línea gruesa','canto de la pieza. «Canto de referencia» = desde donde se mide.'),('Franja verde','traslape: aquí se encima la hoja siguiente. Las letras A↔A, B↔B deben coincidir.'),('✂ línea punteada naranja','recorta el margen de la hoja por aquí antes de encimarla.'),('Etiqueta U##','número de unión; coincide con la lámina del paso en el sitio.')]
    for a,b in parts:g2.append(T(MX,y,'• '+a+':',3,w=700)+T(MX+62,y,b,3));y+=6
    y+=4;g2.append(T(MX,y,'Herramienta',5,w=600,fam='Fraunces'));y+=8
    tools=['Impresora (papel carta) y tijeras','Cinta masking','Flexómetro (para la regla de 10 cm)','Punzón o clavo + martillo','Taladro y brocas ⌀2, ⌀3 mm; avellanador ⌀8 mm','Plantilla Kreg + broca escalonada 3/8″ con collar','Sierra copa ⌀25 (ventilación del fondo)','Cinta de color para la bandera de profundidad']
    for i,t in enumerate(tools):g2.append(T(MX+(0 if i%2==0 else CW/2),y+(i//2)*6,'☐ '+t,3.1))
    y+=30
    g2.append(f'<rect x="{MX}" y="{y}" width="{CW}" height="20" rx="2" fill="#fff" stroke="{ACC}" stroke-width=".8"/>'+T(MX+4,y+7,'Hojas «PENDIENTE: MEDIR RIEL COMPRADO»',3.4,ACC,w=800)+T(MX+4,y+13,'No perfores el riel ni cortes las puertas hasta tener el riel en mano y su ficha (altura H y agujeros).',3))
    g2.append(ruler(PH-MX-3)+'</svg>')
    return [''.join(g1),''.join(g2)]
# ---------- armar documentos ----------
TF=[f for f in F if f['tpl'] or f['pend']]
SH={f['id']:sheets_of(f) for f in TF}
def faces_for_step(i):
    ids=steps.get(i,[]);fs=[f for f in TF if any(h['u'] in ids for h in f['h'])]
    if i==10:fs+= [f for f in TF if f['id']=='03i']
    return fs
def build(faces,step=None):
    pages=guide();tot=2+sum(len(SH[f['id']]) for f in faces);pn=2;anchors={}
    for f in faces:
        n=len(SH[f['id']]);anchors[f['id']]=pn+1
        for k,s in enumerate(SH[f['id']],1):pn+=1;pages.append(sheet_svg(f,s,k,n,pn,tot,step))
    return pages,anchors
CSS='''@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;background:#F4F3EE;color:#1F2A2E;font-family:Inter,system-ui,sans-serif}
svg.pg{display:block;margin:0 auto 14px;background:#fff;box-shadow:0 2px 10px #0001;break-after:page;max-width:100%;height:auto}
.intro{max-width:760px;margin:auto;padding:22px 18px}.intro h1{font-family:Fraunces,serif;font-weight:600;font-size:32px;margin:0 0 8px}.b{display:inline-block;background:#D9502B;color:#fff;border-radius:8px;padding:11px 16px;text-decoration:none;font-weight:600;margin:4px 6px 4px 0;font-size:14px}.b.g{background:#fff;color:#1F2A2E;border:1px solid #c9d2cb}
.w{background:#fff;border:1px solid #D9502B;border-left-width:4px;border-radius:10px;padding:10px 14px}.intro li{margin:5px 0}
@media print{body{background:#fff}.intro{display:none}svg.pg{margin:0;box-shadow:none;width:215.9mm;height:279.4mm;max-width:none}}'''
HEAD='<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Ccircle cx=%228%22 cy=%228%22 r=%228%22 fill=%22%23D9502B%22/%3E%3C/svg%3E"><link rel="stylesheet" href="../../fonts/fonts.css"><style>'+CSS+'</style></head><body>'
OUT='/workspace/studio/ropero/plantillas/'
for fn in os.listdir(OUT):
    if fn.startswith('paso_') :os.remove(OUT+fn)
STEPPDF={}
for i in sorted(steps)+[10]:
    fs=faces_for_step(i)
    if not fs or i in STEPPDF:continue
    pages,_=build(fs,i+1);nn=f'{i+1:02d}';STEPPDF[i]=dict(file=f'plantillas_paso_{nn}.pdf',html=f'paso_{nn}.html',pages=len(pages),faces=[f['no'] for f in fs])
    open(OUT+f'paso_{nn}.html','w').write(HEAD.replace('{t}',f'Plantillas paso {i+1} · Ropero')+f'<div class="intro"><h1>Plantillas · paso {i+1}</h1><a class="b" href="plantillas_paso_{nn}.pdf">Descargar PDF ({len(pages)} hojas)</a><a class="b g" href="./">Todas las plantillas</a></div>'+''.join(pages)+'</body></html>')
pages,anch=build(TF)
idx=''.join(f'<li id="p{f["no"]:02d}"><a href="#pg{anch[f["id"]]}">{f["no"]:02d} · {E(f["name"])}</a> — {len(SH[f["id"]])} hoja(s){" · <b style=color:#D9502B>pendiente</b>" if f["pend"] else ""}</li>' for f in TF)
stp=''.join(f'<li><a href="{v["file"]}">Paso {i+1}</a> — {v["pages"]} hojas (piezas {", ".join(f"{n:02d}" for n in v["faces"])}) · <a href="{v["html"]}">ver</a></li>' for i,v in sorted(STEPPDF.items()))
body=f'''<div class="intro"><p style="color:#D9502B;font-weight:600;letter-spacing:.14em;font-size:12px;text-transform:uppercase;margin:0">Strate Studio · Ropero</p><h1>Plantillas de perforación 1:1</h1>
<p>Hojas carta a escala real para marcar cada agujero sin medir. Las 2 primeras hojas son la guía ilustrada.</p>
<p class="w"><b>Imprime al 100 % («Tamaño real»), sin ajustar.</b> Mide la regla de 10 cm de cada hoja antes de usarla.</p>
<a class="b" href="plantillas_ropero.pdf">PDF completo ({len(pages)} hojas)</a><a class="b g" href="#" onclick="print();return false">Imprimir</a><a class="b g" href="../#armado">← Volver al armado</a>
<h3>Por paso de armado (imprime solo lo que vas a usar)</h3><ul>{stp}</ul><h3>Por pieza</h3><ul>{idx}</ul>
<p style="font-size:13px;color:#6B7B78">El fondo (13–14) y la cara superior del piso no llevan plantilla: sus tornillos se marcan con cinta y escuadra (ver lámina del paso).</p></div>'''
open(OUT+'index.html','w').write(HEAD.replace('{t}','Plantillas de perforación 1:1 · Ropero · Strate Studio')+body+''.join(f'<a id="pg{n}"></a>'+p for n,p in enumerate(pages,1))+'</body></html>')
json.dump(STEPPDF,open('/workspace/studio/ropero/src/steppdf.json','w'))
open('/workspace/studio/ropero/holes.js','a').write('window.STEPPDF='+json.dumps({k:v['file'] for k,v in STEPPDF.items()})+';\n')
print('total',len(pages),'steps',{i+1:v['pages'] for i,v in STEPPDF.items()})
