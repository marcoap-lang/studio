import sys;sys.argv=['x'];exec(open('/workspace/studio/ropero-cnc/src/gen.py').read().split('# ---------- anidado')[0])
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
def polys(g): return [g] if g.geom_type=='Polygon' else list(g.geoms)
def draw(c,g,ox,oy,fill=None):
    for pg in polys(g):
        for ring in [pg.exterior]+list(pg.interiors):
            pts=list(ring.coords);pth=c.beginPath();pth.moveTo((pts[0][0]+ox)*mm,(pts[0][1]+oy)*mm)
            for x,y in pts[1:]: pth.lineTo((x+ox)*mm,(y+oy)*mm)
            pth.close();c.drawPath(pth,stroke=1,fill=0)
c=canvas.Canvas('/workspace/studio/ropero-cnc/plantillas/plantillas_ropero_cnc.pdf',pagesize=letter)
def head(t,sub):
    c.setFont('Helvetica-Bold',13);c.drawString(15*mm,265*mm,'STRATE STUDIO · ROPERO CNC · '+t);c.setFont('Helvetica',9);c.drawString(15*mm,259*mm,sub)
    c.rect(15*mm,15*mm,50*mm,10*mm);c.setFont('Helvetica',7);c.drawString(15*mm,11*mm,'Mide este cuadro: debe dar 50 × 10 mm. Imprime al 100 % (sin "ajustar a página").')
c.setLineWidth(0.6)
# 1 cuña x6, mariposa x2, taravilla x8
head('CUÑA, MARIPOSA Y TARAVILLA','1:1 · Usa estas para revisar las piezas del CNC o para cortar cuñas de repuesto a mano.')
for i in range(6): draw(c,WEDGE,20,35+i*26);c.setFont('Helvetica',7);pass
c.drawString(20*mm,190*mm,'Cuña 80 × 10-18 · triplay 18 mm · veta a lo largo (x6 de muestra)');draw(c,BOW,20,205);c.drawString(20*mm,200*mm,'Mariposa 120 × 50 (cintura 25) · 5 mm · caja 5.5 mm de profundidad, +0.15 por lado')
for i in range(8): draw(c,TARA,120+(i%2)*50,40+(i//2)*24)
c.drawString(120*mm,138*mm,'Taravilla 44 × 16 · 5 mm · perno de madera diam. 6')
c.showPage()
# 2 espiga, ranura de cuña y caja
head('ESPIGA, MORTAJA Y RANURA DE CUÑA','1:1 · Calibrador de holgura: corta esta hoja en el CNC de prueba (retazo 18 mm) antes de la producción.')
sp=Part('t','t',18,0,0,None);sp.body=box(0,0,140,40)
sp.tn(40,40,100,88,'y0');sp.sub.append(dog_hole(70-SW/2,58.5,70+SW/2,72.5))
draw(c,sp.geom(),30,40);c.setFont('Helvetica',8);c.drawString(30*mm,35*mm,'Espiga 60 × 18 (sobresale 30) · ranura 18.4 × 14 con 1.5 mm de tiro · dog-bones diam. 6')
mo=box(0,0,140,90).difference(dog_hole(40-TOL/2,36-TOL/2,58+TOL/2,96-TOL/2 if False else 36+60+TOL/2).union(dog_hole(40-.15,15,58+.15,75.3)))
mo=box(0,0,140,90).difference(dog_hole(61-.15,14.85,79.15,75.15))
draw(c,mo,30,140);c.drawString(30*mm,135*mm,'Mortaja en techo/base 18.3 × 60.3 (holgura 0.3) con dog-bones diam. 6')
c.showPage()
# 3 jaladera y esquina de ventana
head('JALADERA CALADA Y ESQUINA DE VENTANA','1:1 · Para revisar el calado de las puertas y lijar los radios.')
h=unary_union([box(-14,0,14,170),Point(0,0).buffer(14,resolution=24),Point(0,170).buffer(14,resolution=24)])
draw(c,h,40,62);c.drawString(25*mm,40*mm,'Jaladera 28 × 198 (centro a 35 mm del canto)')
win=rbox(0,0,150,150,40).intersection(box(0,0,110,110));q=box(-12,-12,90,90);draw(c,rbox(0,0,237,300,40).intersection(q),110,60);draw(c,rbox(-10,-10,247,310,50).intersection(q),110,60)
c.drawString(95*mm,40*mm,'Ventana R40 · rebaje trasero R50 (10 × 6 mm) · panel de yute R50')
c.showPage()
head('COLA DE MILANO DEL BASTIDOR DE PUERTA','1:1 · Travesaño o parteluz (abajo) y su caja en el larguero (arriba). Holgura 0.15 por lado y alivios de fresa diam. 6.')
tab=unary_union([box(0,0,60,60),dt_tab(60,30,1)]);draw(c,tab,30,60)
lg=box(0,0,60,120).difference(dt_tab(0,60,1).buffer(0.15,join_style=2));draw(c,affinity.translate(lg,-0,0),110,40)
c.setFont('Helvetica',8);c.drawString(30*mm,50*mm,'Cola: 20 de largo, 40 en la raíz, 52 en la punta');c.drawString(110*mm,35*mm,'Caja en el canto interior del larguero (80 mm)')
c.showPage();c.save()
