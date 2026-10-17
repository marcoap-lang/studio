// Contenido del ropero: presupuesto, comparación, pasos de armado, compras.
window.BUDGET=[
 // [partida, cantidad, precio unitario, nota, verificado]
 ['Triplay de pino 18 mm, 122×244','3 hojas',735,'Casco, división, repisas, zócalo',1],
 ['Triplay 6 mm, 122×244','2 hojas',380,'Fondo 13 y tira 14',0],
 ['Triplay 3 mm, 122×244','2 hojas',230,'Tapas de puerta 28–29',0],
 ['Pino seco 19×63 (1×3), 2.44 m','10 tablas',75,'Bastidores, listón y junquillos',0],
 ['Kit carros Ducloset doble 45 kg (Ducasse)','1 kit',389,'Home Depot',1],
 ['Tubo FIX Ø25, 2.4 m','1 pz',125,'Salen 3 tubos de 765',1],
 ['Soportes (bridas) para tubo Ø25','6 pz',15,'',0],
 ['Tornillería y grapas (lista exacta en Compras)','lote',340,'Pocket, #8, #6, clavos y grapas',0],
 ['Resistol 850 (cola blanca)','1 L',160,'',0],
 ['Yute en rollo, sin tratar','≈4 m²',120,'Frente de las 2 puertas',0],
 ['Cubrecanto de pino','10 m',12,'Cantos frontales',0],
 ['Sellador para madera (1 capa)','1 L',260,'Cantos, interior y fondo',0],
 ['Aceite de linaza cocida','1 L',180,'',0],
 ['Cera de abeja en pasta','1 lata 250 g',220,'',0],
 ['Lijas 120/220 y cuñas niveladoras','lote',140,'',0],
 ['Imprevistos (≈10 %)','—',0,'Cortes extra, brocas, fletes menores',0],
];
{const b=window.BUDGET,q=x=>{const n=parseFloat(String(x[1]).replace('≈',''));return isNaN(n)?1:n};const s=b.slice(0,-1).reduce((a,x)=>a+x[2]*q(x),0);b[b.length-1][2]=Math.round(s*0.1/10)*10;}
window.COMPARE=[
 ['Este ropero (hecho por ti)','Pino y triplay de pino, puertas de yute, cera de abeja',null,'Medidas exactas, madera real, reparable'],
 ['Madesa Mónaco',"MDP (aglomerado) con melamina",6929,'Precio similar, pero aglomerado: se hincha con la humedad de Boca'],
 ['IKEA PAX / HASVIK','Aglomerado y fibra, puertas corredizas',12900,'Casi el doble y sin madera maciza'],
 ['Pino + ratán hecho a mano (Etsy)','Madera maciza artesanal',[16000,40000],'No hay oferta local; importación'],
];
window.LUMBER=[
 ['Herrajes y Triplay del Sur','Boca del Río · corte de hojas','https://wa.me/522292666085','WhatsApp 229 266 6085'],
 ['TriplayMARKET Veracruz','Corte de hojas de triplay','tel:+522299392135','Llamar 229 939 2135'],
 ['Maderería Malibrán','Tablas de pino 19×63 (1×3)',null,'Ir en persona'],
];
// Paso: t título, d instrucción, n piezas nuevas, f piezas a resaltar sin animar, x extras 3D (riel), tools, min (minutos), cam
window.STEPS=[
 {t:'Compra el riel y confirma la altura de las puertas',d:'Antes de cortar nada de las puertas, compra el kit de carros y el riel. Lee la ficha del fabricante: la altura de la puerta es H = 1914 − descuento del riel (≈1880). Hasta tener ese número NO cortes las piezas 16–19 ni 28–29.',n:[],f:[],tools:['Cinta métrica','Calculadora'],min:30},
 {t:'Rotula, lija y sella las piezas',d:'Escribe el número a lápiz en cada pieza (cara que no se ve). Lija con 120 y luego 220. Aplica sellador en todos los cantos, en caras interiores, en el fondo (13–14) y en las tapas de puerta por ambas caras. Deja secar según el envase.',n:[],f:[],tools:['Lijadora o taco','Lija 120 y 220','Brocha','Lápiz'],min:240},
 {t:'Perfora pockets y agujeros de soportes',d:'Con la plantilla pocket, perfora los agujeros ocultos en techo, piso, división, repisa y zapatera (ver ficha de cada pieza). En los costados y la división marca y perfora los soportes de tubo a 270 mm del frente: izquierda 1900 y 980; derecha 1650.',n:[],f:[],tools:['Taladro','Plantilla pocket (Kreg o similar)','Broca escalonada pocket','Escuadra','Cinta métrica'],min:90},
 {t:'Arma el zócalo',d:'Une frente 08 y atrás 09 con los travesaños 10, 11 y 12 (extremos y centro) usando cola y un tornillo pocket por extremo. El frente queda remetido 50 mm. Comprueba la escuadra midiendo diagonales.',n:[8,9,10,11,12],f:[],tools:['Taladro','Desarmador / punta Phillips','Prensas','Escuadra','Cola Resistol 850'],min:45},
 {t:'Arma la caja: costados, techo y piso',d:'Con el mueble acostado, une techo 03 y piso 04 a los costados 01 y 02 con cola y pockets (4 por lado; en el piso el primero va a 90 del frente para librar el zócalo). El piso queda a 50 mm del suelo, encima del zócalo. Mide las dos diagonales: deben ser iguales.',n:[1,2,3,4],f:[],tools:['Taladro','Desarmador / punta Phillips','Prensas','Escuadra','Cinta métrica','Cola Resistol 850'],min:60},
 {t:'Coloca la división central',d:'Mete la división 05 al centro: 773 mm libres a cada lado. Fíjala con cola y 3 pockets arriba y 3 abajo, todos en la cara derecha de la división (la plantilla Kreg no llega al centro del techo). Usa un taco de 773 como separador para que quede paralela.',n:[5],f:[],tools:['Taladro','Prensas','Cinta métrica','Taco separador 773 mm'],min:30},
 {t:'Repisa y zapatera (lado derecho)',d:'Repisa 06 (461 de fondo) con la cara superior a 1700 mm del suelo; zapatera 07 (331 de fondo) con la cara superior a 270 mm. Van 19 mm menos profundas para librar el listón 15: alinéalas al frente. 2 pockets por lado en la cara inferior.',n:[6,7],f:[],tools:['Taladro','Nivel','Prensas','Cinta métrica'],min:40},
 {t:'Listón y fondo',d:'Fija el listón 15 vertical a 1220 mm del lado izquierdo, al ras de atrás: 2 tornillos #8 × 1½″ desde arriba del techo y 2 desde abajo del piso (pretaladra la testa a 3 mm). Coloca el fondo de triplay de 6 mm: grande 13 desde la izquierda y tira 14 a la derecha; la unión cae sobre el listón. Tornillo #6 × 5/8″ cada ~185 mm (75 en total). Revisa diagonales antes de atornillar. Ventilación Ø25 en 2 filas a 140 y 1810 del canto inferior. El fondo total queda en 553 mm.',n:[15,13,14],f:[],tools:['Taladro','Desarmador','Broca Ø25 (ventilación)','Escuadra'],min:50},
 {t:'Levanta la caja y siéntala en el zócalo',d:'Entre dos personas, para el mueble y siéntalo sobre el zócalo, ya nivelado con cuñas en su sitio (deja 1–2 cm de la pared). Fíjalo con 20 tornillos #8 × 1½″ desde la cara superior del piso (frente, atrás y travesaños 10 y 12). El travesaño 11 queda bajo la división y no se atornilla desde arriba.',n:[],f:[8,9,10,11,12,4],tools:['Nivel','Cuñas niveladoras','Taladro','Ayudante'],min:30},
 {t:'Tubos para colgar',d:'Atornilla los soportes y coloca los tubos: 30 a 1900 mm y 31 a 980 mm en el lado izquierdo (prendas cortas, dos niveles); 32 a 1630 mm en el lado derecho (prendas largas; deja ~40 mm libres bajo la repisa para el gancho). Alturas al centro del tubo. Mide el claro real antes de cortar el tubo.',n:[30,31,32],f:[],tools:['Taladro','Desarmador','Segueta para metal','Nivel'],min:30},
 {t:'Riel doble bajo el techo',d:'Corta el riel U-20 a 1564 mm y atorníllalo bajo el techo 03, al frente, a escuadra con los costados. Tornillo #8 × 3/4″ (no más largo: el techo es de 18 mm). Agujeros según la ficha del riel comprado. Es angosto (≤5 cm) para no perder fondo útil.',n:[],f:[3],x:['riel'],tools:['Taladro','Segueta para metal','Escuadra','Desarmador'],min:30},
 {t:'Bastidores de las puertas',d:'Con H ya confirmada, une largueros 16–19 y travesaños 20–27 a media madera (63 × 9.5 mm) con cola y 2 tornillos #6 × 5/8″ por cruce (uno de 3/4″ traspasaría). Arriba, abajo y dos intermedios por puerta (a H/3 y 2H/3). Prensa en escuadra y deja secar 24 h.',n:[16,17,18,19,20,21,22,23,24,25,26,27],f:[],tools:['Sierra o caladora','Formón','Prensas','Escuadra','Cola Resistol 850'],min:180},
 {t:'Tapas de triplay en las puertas',d:'Pega y engrapa las tapas 28 y 29 a todo el bastidor con grapa de 10 mm cada 50 mm, al centro del bastidor. Quedan puertas ligeras de ≈22 mm y 7–8 kg.',n:[28,29],f:[],tools:['Engrapadora','Cola Resistol 850','Rodillo o espátula'],min:40},
 {t:'Yute y junquillos',d:'Pega el yute (sin tratar) y engrápalo del centro hacia afuera, bien tenso. Remata con los junquillos 33–40 cortados a inglete de 45°, clavados con clavo sin cabeza.',n:[33,34,35,36,37,38,39,40],f:[],tools:['Engrapadora','Ingletadora o caja de ingletes','Martillo','Botador','Tijeras'],min:120},
 {t:'Acabado: linaza y cera de abeja',d:'En caras visibles, bastidores y junquillos: linaza en capa delgada, retira el exceso a los 15 min y deja secar 24–48 h. Luego cera de abeja y pule. El yute se queda sin tratar. ⚠ Los trapos con linaza pueden autoincendiarse: extiéndelos a secar o mételos en agua.',n:[],f:[1,2,3,16,17,18,19,33,34,35,36,37,38,39,40],tools:['Trapo de algodón','Guantes','Paño para pulir'],min:90},
 {t:'Cuelga las puertas y ajusta',d:'Monta los carros en las puertas, cuélgalas en el riel (puerta 1 al frente, puerta 2 atrás, traslape 40 mm), coloca la guía inferior y ajusta la altura hasta que corran parejas.',n:[],f:[16,17,18,19,28,29],tools:['Desarmador','Llave del kit','Nivel'],min:45},
];
window.BUY=[['Riel colgante doble ≤5 cm + 4 carros + guía inferior (Ducasse Ducloset doble 45 kg, Home Depot)','$389'],['Alternativa: riel U-20 aluminio 2 m (Madercenter, cortar a 1564)','$342.91'],['Tubo FIX Ø25, 2.4 m (salen 3 × 765)','$125'],['Triplay de pino 18 mm 122×244 – 3 hojas','$735 c/u'],['Triplay 6 mm 122×244 – 2 hojas (fondo)',''],['Triplay 3 mm 122×244 – 2 hojas (tapas de puerta)',''],['Pino seco 19×63 (1×3) 2.44 m – 8 tablas (7 puertas + 1 listón 15)',''],['Pino 1×3 2.44 m extra para junquillos – 2 tablas',''],['Yute en rollo ≈ 4 m² (sin tratar)',''],['Cubrecanto de pino ≈ 10 m',''],['Resistol 850 – 1 L',''],['Sellador para madera',''],['Aceite de linaza cocida',''],['Cera de abeja (pasta)',''],['Lija 120 y 220',''],['Cuñas niveladoras para zócalo','']];
