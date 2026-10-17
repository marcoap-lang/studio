import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R
from matplotlib.backends.backend_pdf import PdfPages
T=18
def dim(ax,x1,y1,x2,y2,t,off=0,v=False,fs=7):
    ax.annotate('',(x1,y1),(x2,y2),arrowprops=dict(arrowstyle='<->',lw=.6))
    mx,my=(x1+x2)/2,(y1+y2)/2
    ax.text(mx+(off if v else 0),my+(0 if v else off),t,fontsize=fs,ha='center',va='center',rotation=90 if v else 0,bbox=dict(fc='white',ec='none',pad=.5))
def box(ax,x,y,w,h,fc='#e9d8b4',**k): ax.add_patch(R((x,y),w,h,fc=fc,ec='k',lw=.7,**k))
def front(ax):
    box(ax,0,0,T,2000);box(ax,1600-T,0,T,2000);box(ax,T,2000-T,1564,T);box(ax,T,50,1564,T)
    box(ax,T+50*0,0,1564,50,fc='#bfa77a',hatch='//')
    box(ax,791,68,T,1914)
    for y in (1900,980): ax.plot([T,791],[y,y],lw=3,c='gray')
    box(ax,809,1700-T,773,T); ax.plot([809,1582],[1650,1650],lw=3,c='gray')
    box(ax,809,270-T,773,T)
    ax.add_patch(R((T,1955),1564,27,fc='#cfd8dc',ec='k',lw=.5)); ax.text(800,1968,'riel doble ≤5 cm',fontsize=6,ha='center')
    dim(ax,0,-120,1600,-120,'1600 exterior');dim(ax,T,-60,791,-60,'773 libre',fs=6);dim(ax,809,-60,1582,-60,'773 libre',fs=6)
    dim(ax,-130,0,-130,2000,'2000 exterior',v=True,off=0)
    for x,y,t in [(350,1900,'tubo 1900'),(150,980,'tubo 980'),(300,0,'')]:
        if t: dim(ax,x,0,x,y,t,v=True)
    for x,y,t in [(1000,1650,'tubo 1650'),(1300,1700,'repisa 1700 (cara sup.)'),(1450,270,'zapatera 270')]:
        dim(ax,x,0,x,y,t,v=True)
    dim(ax,1700,0,1700,50,'zócalo 50',v=True,off=40,fs=6)
    ax.text(400,1450,'IZQ: prenda corta\n2 tubos',ha='center',fontsize=8);ax.text(1195,1200,'DER: prenda larga',ha='center',fontsize=8)
    ax.text(1195,150,'zapatos (base)',ha='center',fontsize=7);ax.text(1195,330,'zapatos',ha='center',fontsize=7)
    ax.set_xlim(-250,1850);ax.set_ylim(-200,2100);ax.set_aspect('equal');ax.axis('off')
    ax.set_title('1) Alzado frontal (sin puertas) – cotas en mm – escala gráfica',fontsize=10)
pages=[]
with PdfPages('ropero_tecnico.pdf') as pdf:
    # page1 cover+front
    f=plt.figure(figsize=(8.27,11.69));f.text(.5,.965,'ROPERO 160 × 200 × 55 cm – Plano técnico para maderería',ha='center',fontsize=14,weight='bold')
    f.text(.5,.945,'Triplay de pino 18 mm (exterior) · Fondo 3 mm ventilado · 2 puertas corredizas de yute colgantes · Boca del Río, Ver. · Oct 2026',ha='center',fontsize=7.5)
    front(f.add_axes([.03,.05,.94,.87]));pdf.savefig(f)
    g=plt.figure(figsize=(8,9));front(g.add_subplot(111));g.savefig('preview.png',dpi=130,bbox_inches='tight')
    # page2 side + door
    f=plt.figure(figsize=(8.27,11.69));ax=f.add_axes([.05,.55,.9,.38])
    box(ax,0,0,3,2000,fc='#999');box(ax,3,50,547,T);box(ax,3,1982,547,T)
    ax.add_patch(R((3,68),487,1914,fc='#eef5ee',ec='none'));ax.text(250,1000,'zona gancho\n≈487 libre',ha='center',fontsize=8)
    ax.add_patch(R((490,1955),50,27,fc='#cfd8dc',ec='k'));ax.add_patch(R((497,80),22,1870,fc='#d9c38f',ec='k',lw=.5));ax.add_patch(R((522,80),22,1870,fc='#d9c38f',ec='k',lw=.5))
    box(ax,56,0,18,50,fc='#bfa77a');box(ax,526,0,18,50,fc='#bfa77a')
    ax.plot([250,250],[1650,1600],c='gray');ax.add_patch(R((30,1640),450,12,fc='gray'))
    dim(ax,0,-80,550,-80,'550 total');dim(ax,0,2080,3,2080,'3',fs=6);dim(ax,3,2150,490,2150,'≈487 gancho (+10 holgura)',fs=6);dim(ax,490,2080,550,2080,'≈50 riel+puertas',fs=6)
    ax.text(560,1000,'2 puertas 22 mm\n(holgura 1 cm)',fontsize=7);ax.text(-20,25,'zócalo remetido 50',fontsize=6,ha='right')
    ax.set_xlim(-200,800);ax.set_ylim(-150,2250);ax.set_aspect('equal');ax.axis('off');ax.set_title('2) Corte lateral – desglose de fondo: 550 − 3 fondo − 50 riel − 10 holgura ≈ 487 libre',fontsize=9)
    ax=f.add_axes([.05,.05,.9,.45]);H=1880
    for x in (0,802-63): box(ax,x,0,63,H)
    for y in (0,H-63,H/3-31,2*H/3-31): box(ax,63,y,802-126,63,fc='#d9c38f')
    ax.add_patch(R((0,0),802,H,fill=False,ec='brown',lw=1.5,ls='--'))
    dim(ax,0,-70,802,-70,'802 (= (1564+40)/2, traslape 40)');dim(ax,-90,0,-90,H,'H puerta (≈1880, CONFIRMAR con riel)',v=True)
    ax.text(1000,H*.7,'Bastidor pino seco 19×63 mm\nuniones a media madera + cola\n2 travesaños intermedios\nTriplay 3 mm pegado+engrapado\nYute pegado, engrapado del centro\nhacia afuera; junquillo perimetral\nEspesor ≈22 mm · peso ≈7–8 kg (est.)\nCarros colgantes atornillados arriba\nGuía inferior al piso (puntual)',fontsize=7.5,va='top')
    ax.text(1000,H*.2,'Altura de puerta:\nH = vano interior 1914\n  − descuento de carro/riel\n    según ficha del fabricante\nNO cortar antes de tener el riel.',fontsize=8,color='darkred',va='top')
    ax.set_xlim(-250,1800);ax.set_ylim(-150,H+100);ax.set_aspect('equal');ax.axis('off');ax.set_title('3) Detalle de puerta (×2) – vista frontal sin yute',fontsize=9)
    pdf.savefig(f)
    # page3 cutlist + nesting
    import textwrap as tw, json as _j
    DD=_j.load(open('/workspace/ropero/data.json'));PP=DD['P']
    f=plt.figure(figsize=(8.27,11.69));f.text(.5,.97,'4) Despiece numerado (mm) – escribir el número en cada pieza',ha='center',fontsize=12,weight='bold')
    rows=[[f"{p['no']:02d}",p['l'],p['n'],('H≈' if p['l'] in 'JL' else '')+str(p['L']),str(p['W']),str(p['T']),p['mat'],'frente' if p['c'] else '—'] for p in PP]
    ax=f.add_axes([.03,.30,.94,.66]);ax.axis('off');t=ax.table(cellText=rows,colLabels=['No.','Letra','Pieza','Largo','Ancho','Esp.','Material','Canto'],loc='center',cellLoc='center',colWidths=[.06,.06,.3,.08,.07,.06,.25,.08]);t.auto_set_font_size(False);t.set_fontsize(6.6);t.scale(1,1.12)
    for (r,c),cell in t.get_celld().items():
        if r>0 and rows[r-1][1] in 'JL' and c==3: cell.set_text_props(color='darkred',weight='bold')
    notes=['Comprobación: 18+1564+18 = 1600 ancho · 50 zócalo + 18 piso + 1914 + 18 techo = 2000 alto · 547 + 3 fondo = 550 fondo · 18+773+18+773+18 = 1600 · fondo 1220+380 = 1600 · puertas (1564+40)/2 = 802.',
     'Libre para gancho ≈ 550 − 3 fondo − 50 riel − 10 holgura = 487.',
     'NO CORTAR 16-19 (largueros) ni 28-29 (tapas) hasta comprar el riel: H = 1914 − descuento del riel según ficha (≈1880 orientativo). Travesaños K (20-27): 802 de largo total con media madera de 63 de largo × 9.5 de profundidad en cada extremo. 4 por puerta.',
     'Fondo de 3 mm en dos piezas: 13 (1220 de ancho, desde la izquierda) + 14 (380). La unión cae sobre el listón vertical 15 (pino 19×63) a 1220 del lado izquierdo.',
     'Junquillos 33-40 se rajan de 2 tablas 1×3 extra (tiras ≈12×15). Tubos 30-32 salen de un tubo FIX de 2.4 m.',
     'MATERIAL: Triplay pino 18 mm = 3 hojas · Triplay 3 mm = 3 hojas · Pino seco 19×63 (1×3) = 8 tablas de 2.44 m + 2 tablas extra para junquillo.']
    f.text(.05,.28,'\n\n'.join(tw.fill(n,115) for n in notes),fontsize=7.4,va='top')
    pdf.savefig(f)
    def sheet(ax,s):
        W,Hs=s['W'],s['H']
        ax.add_patch(R((0,0),W,Hs,fc='white',ec='k',lw=1.2,hatch='xx'))
        for n,x,y,w,h in s['p']:
            ax.add_patch(R((x,y),w,h,fc='#e9d8b4',ec='k',lw=.8))
            p=PP[n-1]
            if p['c']:
                if w>h: ax.plot([x,x+w],[y,y],c='red',lw=3)
                else: ax.plot([x,x],[y,y+h],c='red',lw=3)
            if w>=200: ax.text(x+w/2,y+h/2,f'{n:02d}\n{max(w,h)}×{min(w,h)}',ha='center',va='center',fontsize=9,weight='bold')
            else: ax.text(x+w/2,y+h/2,f'{n:02d} · {max(w,h)}×{min(w,h)}',ha='center',va='center',fontsize=5.5,rotation=90,weight='bold')
        ax.annotate('',(0,-60),(W,-60),arrowprops=dict(arrowstyle='<->',lw=.7));ax.text(W/2,-120,f'{W}',ha='center',fontsize=8)
        ax.annotate('',(-60,0),(-60,Hs),arrowprops=dict(arrowstyle='<->',lw=.7));ax.text(-110,Hs/2,f'{Hs}',va='center',rotation=90,fontsize=8)
        ax.set_xlim(-180,W+40);ax.set_ylim(-200,Hs+40);ax.set_aspect('equal');ax.axis('off');ax.set_title(s['t'],fontsize=9)
    S=DD['S']
    for i in range(0,len(S),2):
        f=plt.figure(figsize=(8.27,11.69));f.text(.5,.965,'4b) Acomodo en hoja 1220 × 2440 mm (sierra 3 mm · rayado = desperdicio · rojo = cubrecanto)',ha='center',fontsize=10,weight='bold')
        for j,s in enumerate(S[i:i+2]): sheet(f.add_axes([.03+j*.48,.12,.46,.8]),s)
        f.text(.05,.07,'Medidas en mm. Números = piezas del despiece. Hoja 5/6: piezas 28-29 con altura H pendiente del riel.',fontsize=7)
        pdf.savefig(f)
    f=plt.figure(figsize=(8.27,11.69));f.text(.5,.965,'4c) Pino seco 19×63 (1×3) – tablas de 2440 mm',ha='center',fontsize=11,weight='bold')
    ax=f.add_axes([.08,.35,.86,.58]);ax.axis('off');y=0
    for r,b in enumerate(DD['B']):
        if isinstance(b,str): ax.text(0,y+60,f'T{r+1}: '+b,fontsize=7.5);y-=300;continue
        ax.add_patch(R((0,y),2440,150,fc='white',ec='k',hatch='xx'));x=0
        for n,l in b: ax.add_patch(R((x,y),l,150,fc='#e9d8b4',ec='k'));ax.text(x+l/2,y+75,f'{n:02d} · {l}',ha='center',va='center',fontsize=8,weight='bold');x+=l+3
        ax.text(-40,y+75,f'T{r+1}',ha='right',va='center',fontsize=8);y-=300
    ax.set_xlim(-250,2500);ax.set_ylim(y,250);ax.set_aspect('equal')
    f.text(.08,.32,'Alto de tabla exagerado para leer. Sierra 3 mm. 16-19 = H≈1880: confirmar con el riel.',fontsize=7.5,color='darkred')
    pdf.savefig(f)
    # page4 text
    f=plt.figure(figsize=(8.27,11.69));txt='''5) HERRAJES Y CONSUMIBLES (sin precios)
• Riel colgante doble de aluminio ≤5 cm, ≥15 kg/puerta, 2 m (cortar a 1564) + kit de carros para 2 puertas + guía al piso — 1 juego
• Tubo cromado/acero Ø25 mm — 3 tramos de ~0.8 m (o 1 de 3 m) · Soportes (bridas) Ø25 — 6 pz
• Tornillo pocket (Kreg) 1-1/4" rosca gruesa — ~100 pz · Tornillo 1" para fondo — ~40 pz
• Cola PVA exterior (tipo D3) — 1 L · Grapas 1/4"–5/16" para engrapadora — 1 caja
• Yute en rollo — ~2 × (0.90 × 2.00 m) ≈ 4 m² con sobrante · Pegamento de contacto o cola para tela
• Junquillo de pino ~10×10 mm — ≈ 2 × 2 × (0.80+1.88) ≈ 11 m (+10%)
• Sellador (cantos, fondo, interior, tapas de puerta ambas caras) · Aceite de linaza cocida + cera de abeja (caras vistas y bastidores) · Lija 120/220
• Cubrecanto de pino para frentes — ≈ 10 m · Niveladores/cuñas para zócalo — 4–6 pz
• Broca 25 mm (o 8–10 mm) para agujeros de ventilación en el fondo

6) PROCESO DE ARMADO
1. Comprar el riel primero; leer la ficha y calcular H de puerta.
2. Cortar piezas según despiece; marcar cada una con su letra.
3. Taladrar agujeros pocket en caras ocultas (cara superior de techo, cara inferior de piso, cara exterior que irá contra pared).
4. Lijar; aplicar sellador en cantos, fondo, caras interiores y tapas de puerta (ambas caras) antes de armar. Caras vistas y bastidores: linaza cocida + cera al final. Yute sin tratar.
5. Armar el zócalo (G + H) en escuadra, pegado y atornillado; nivelarlo en sitio con cuñas.
6. Unir piso C y techo B a los costados A con cola + pocket; revisar escuadra midiendo diagonales.
7. Colocar la división D al centro (773 libres a cada lado).
8. Colocar repisa E (cara sup. a 1700) y zapatera F (cara sup. a 270) en la sección derecha.
9. Atornillar el listón 15 vertical a 1220 del lado izq. (al ras de atrás). Perforar ventilación en fondo 13 y 14, sellar y atornillar; la unión 13/14 cae sobre el listón 15.
10. Sentar el casco sobre el zócalo (zócalo remetido 50 mm al frente) y fijarlo.
11. Instalar soportes y tubos: izquierda a 1900 y 980; derecha a 1650.
12. Atornillar el riel doble bajo el techo, al frente, a escuadra.
13. Puertas: armar bastidor a media madera con cola; pegar y engrapar triplay 3 mm; sellar ambas caras; pegar yute y engrapar del centro hacia afuera; clavar junquillo.
14. Montar carros y colgar puertas; ajustar altura y guía al piso; revisar traslape de 40 mm.

7) NOTAS IMPORTANTES
• Comprar el riel ANTES de cortar las puertas: H = 1914 − descuento del fabricante.
• Humedad de Boca: sellar todo (caras, cantos, fondo, bastidores) y ventilar el fondo; separar 1–2 cm de la pared.
• Nivelar el zócalo antes de montar el casco; si no está nivelado las puertas corren solas.
• Fondo libre para ganchos ≈48.7 cm: justo para gancho estándar de 45 cm.
• Peso por puerta ≈7–8 kg (estimado); el riel debe declarar ≥15 kg por puerta.'''
    import textwrap as tw
    txt='\n'.join(tw.fill(l,105,subsequent_indent='   ') for l in txt.split('\n'))
    f.text(.05,.97,txt,fontsize=7.6,va='top');pdf.savefig(f)
    import numpy as np
    TH={'A':[(0,0,18,2000),(1582,0,18,2000)],'B':[(18,1982,1564,18)],'C':[(18,50,1564,18)],'D':[(791,68,18,1914)],
        'E':[(809,1682,773,18)],'F':[(809,252,773,18)],'G':[(18,0,1564,50)],'H':[(18,0,1564,50)],'I':[(0,50,1600,1950)],
        'J':[(18,68,63,1900),(739,68,63,1900),(780,68,63,1900),(1519,68,63,1900)],'K':[(18,68,802,63),(780,68,802,63),(18,1905,802,63),(780,1905,802,63)],
        'L':[(18,68,802,1900),(780,68,802,1900)],'P':[(1189,68,63,1914)],'M':[(18,1900,773,8),(18,980,773,8),(809,1650,773,8)]}
    C=[('A','Costado',2,2000,547,18,'Triplay pino 18 mm','Canto en el largo frontal (2000).','Pocket: NO en cara exterior visible. Agujeros 5 mm p/ soportes de tubo (izq. de un costado: a 1900 y 980; der.: a 1650), a ~270 del frente. Pegan techo, piso.','L1'),
       ('B','Techo',1,1564,547,18,'Triplay pino 18 mm','Canto en el largo frontal (1564).','Pocket en cara SUPERIOR: 4 por lado hacia costados, 3 hacia división. Riel atornillado debajo, al frente.','L1'),
       ('C','Piso (base)',1,1564,547,18,'Triplay pino 18 mm','Canto en el largo frontal (1564).','Pocket en cara INFERIOR: 4 por lado hacia costados, 3 hacia división. Asienta sobre zócalo.','L1'),
       ('D','División central',1,1914,547,18,'Triplay pino 18 mm','Canto en el largo frontal (1914).','Centrada: 773 libres a cada lado. Pocket arriba/abajo (3+3) en cara derecha. Agujeros soportes tubos.','L1'),
       ('E','Repisa superior der.',1,773,480,18,'Triplay pino 18 mm','Canto en el largo frontal (773).','Cara superior a 1700 del piso. Pocket en cara inferior: 2 por lado. Pegada al fondo (deja 64 al frente p/ riel).','L1'),
       ('F','Zapatera der.',1,773,350,18,'Triplay pino 18 mm','Canto en el largo frontal (773).','Cara superior a 270 del piso. Pocket en cara inferior: 2 por lado. Pegada al fondo.','L1'),
       ('G','Zócalo frente / atrás',2,1564,50,18,'Triplay pino 18 mm','Solo la pieza del frente (G1): canto en un largo.','Frente remetido 50 mm. Unión a travesaños H con pocket por cara interior.','L1'),
       ('H','Zócalo travesaño',3,458,50,18,'Triplay pino 18 mm','Sin canto (oculto).','Entre G frente y G atrás: uno en cada extremo y uno al centro. 1 pocket por extremo.',''),
       ('I','Fondo 13 y 14',2,1950,1220,3,'Triplay 3 mm','Sin canto. Sellador ambas caras.','Piezas 13 (1950×1220) y 14 (1950×380). Ventilación: agujeros Ø25 cada ~150 arriba y abajo. Unión sobre el listón 15 (pino 19×63×1914) a 1220 del lado izq.',''),
       ('J','Puerta: larguero',4,'H',63,19,'Pino seco 19×63','Sin canto (cubre junquillo).','Media madera 63×9.5 en ambos extremos + 2 cajas intermedias a H/3 y 2H/3. Largo H = 1914 − descuento riel (≈1880).',''),
       ('K','Puerta: travesaño',8,802,63,19,'Pino seco 19×63','Sin canto.','Media madera 63×9.5 en ambos extremos. 4 por puerta (sup., inf., 2 intermedios). Cola + 2 grapas/tornillos por unión.',''),
       ('L','Puerta: tapa triplay',2,'H',802,3,'Triplay 3 mm','Sin canto; junquillo perimetral sobre el yute.','Pegada y engrapada a todo el bastidor cada ~100 mm. Yute encima, engrapado del centro hacia afuera.',''),
       ('P','Listón unión del fondo',1,1914,63,19,'Pino seco 19×63','Sin canto.','Vertical por dentro entre piso y techo, a 1220 del lado izq., cara trasera al ras. Las piezas 13 y 14 del fondo se atornillan a él.',''),
       ('M','Tubo cromado Ø25',3,'≈765','Ø25','—','Acero cromado + 2 soportes c/u','—','Medir claro real (773) y descontar soportes según fabricante. Izq.: 1900 y 980. Der.: 1650.','')]
    for p0 in range(0,len(C),6):
        f=plt.figure(figsize=(8.27,11.69));f.text(.5,.975,'8) Ficha por pieza'+(' (cont.)' if p0 else ''),ha='center',fontsize=13,weight='bold')
        f.text(.5,.958,'Rojo grueso = canto (cubrecanto) · ● = pocket (tornillo oculto) · ○ = agujero · mm',ha='center',fontsize=7.5,color='darkred')
        for k,c in enumerate(C[p0:p0+6]):
            L,n,q,lg,an,e,mat,can,nota,cf=c;col,row=k%2,k//2
            x0,y0=.04+col*.48,.655-row*.31
            f.patches.append(R((x0,y0),.44,.29,transform=f.transFigure,fill=False,ec='k',lw=.8))
            _ns=[p['no'] for p in PP if p['l']==L];f.text(x0+.01,y0+.27,f'{L}  {n}   ·  No. '+(f'{_ns[0]:02d}' if len(_ns)==1 else f'{_ns[0]:02d}–{_ns[-1]:02d}'),fontsize=10,weight='bold')
            f.text(x0+.01,y0+.25,f'Cant.: {q}   ·   {lg} × {an} × {e} mm   ·   {mat}',fontsize=7)
            ax=f.add_axes([x0+.01,y0+.08,.27,.16]);ax.axis('off')
            lv=1880 if lg=='H' else (765 if isinstance(lg,str) else lg); av=25 if isinstance(an,str) else an
            if L=='M':
                ax.add_patch(R((0,0),lv,av,fc='silver',ec='k'));ax.text(lv/2,-60,str(lg),ha='center',fontsize=7)
            else:
                ax.add_patch(R((0,0),lv,av,fc='#e9d8b4',ec='k',lw=.8))
                if cf=='L1': ax.plot([0,lv],[0,0],c='red',lw=4)
                if L in 'BCD':
                    for xx in ([60,lv/3,2*lv/3,lv-60] if L!='D' else []): pass
                    for yy in np.linspace(70,av-70,4): ax.plot([18,lv-18],[yy,yy],ls='',marker='.')
                    for yy in np.linspace(70,av-70,4): ax.plot([30],[yy],'ko',ms=2.5);ax.plot([lv-30],[yy],'ko',ms=2.5)
                if L in 'EF':
                    for yy in (60,av-60): ax.plot([25,lv-25],[yy,yy],'ko',ms=2.5,ls='')
                if L=='A':
                    for xx in (980,1900,1650): ax.plot([xx],[av-270],'o',mfc='white',mec='k',ms=3)
                if L=='I':
                    for yy in (100,lv-100):
                        for xx in np.arange(100,av,150): ax.plot([yy],[xx],'o',mfc='white',mec='k',ms=2.5)
                if L=='J':
                    for xx in (0,lv-63,lv/3-31,2*lv/3-31): ax.add_patch(R((xx,0),63,av,fc='#b89a5e',ec='k',lw=.4))
                if L=='K':
                    for xx in (0,lv-63): ax.add_patch(R((xx,0),63,av,fc='#b89a5e',ec='k',lw=.4))
                if L in 'GH':
                    for xx in (20,lv-20): ax.plot([xx],[av/2],'ko',ms=2.5)
                ax.text(lv/2,-0.12*max(lv,av)*.35-av*.05,f'{lg}',ha='center',va='top',fontsize=7)
                ax.text(-0.02*lv,av/2,f'{an}',ha='right',va='center',fontsize=7)
            ax.set_xlim(-0.12*lv,lv*1.03);ax.set_ylim(-0.25*max(lv,av)*.35-av*.2,max(av*1.1,lv*.35));ax.set_aspect('equal')
            t=f.add_axes([x0+.30,y0+.08,.13,.16]);t.axis('off')
            for r in [(0,0,18,2000),(1582,0,18,2000),(18,1982,1564,18),(18,50,1564,18),(791,68,18,1914),(809,1682,773,18),(809,252,773,18),(18,0,1564,50)]:
                t.add_patch(R(r[:2],r[2],r[3],fc='#eee',ec='#999',lw=.3))
            for r in TH[L]: t.add_patch(R(r[:2],r[2],r[3],fc='red',ec='red',alpha=.35 if L in 'IL' else .9))
            t.set_xlim(-20,1620);t.set_ylim(-20,2020);t.set_aspect('equal');t.set_title('ubicación',fontsize=6)
            import textwrap
            f.text(x0+.01,y0+.065,'Canto: '+can,fontsize=6.5,color='darkred')
            f.text(x0+.01,y0+.055,textwrap.fill(nota,72),fontsize=6.3,va='top')
        pdf.savefig(f)
