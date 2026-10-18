// Contenido del ropero: presupuesto, comparación, pasos de armado, compras.
window.BUDGET=[
 // [partida, cantidad, precio unitario, nota, verificado]
 ['Triplay de pino 18 mm, 122×244','3 hojas',801,'Casco, división, repisas, zócalo · cotización Triplay Market',1],
 ['Triplay de pino 5 mm, 122×244','3 hojas',233,'Fondo 13–14 y tapas de puerta 28–29 · cotización Triplay Market',1],
 ['Cortes en Triplay Market','lote',52,'Pendiente de confirmar',0],
 ['Pino seco 19×63 (1×3), 2.44 m','8 tablas',75,'Bastidores y listón',0],
 ['Kit carros Ducloset doble 45 kg (Ducasse)','1 kit',389,'Home Depot · 4 carros, tope y guía al piso; NO incluye riel',1],
 ['Riel U-20 acero galvanizado 2 m (Ducasse)','1 pz',226,'Se corta a 1564 · Casa Ikeda / herrajeras',0],
 ['Tubo FIX Ø25, 2.4 m','1 pz',125,'Salen 3 tubos de 765',1],
 ['Soportes (bridas) para tubo Ø25','6 pz',15,'',0],
 ['Tornillería y grapas (lista exacta en Compras)','lote',340,'Pocket, #8, #6, clavos y grapas',0],
 ['Resistol 850 (cola blanca)','1 L',160,'',0],
 ['Yute en rollo, sin tratar','≈4 m²',120,'Frente de las 2 puertas',0],
 ['Cubrecanto de pino','11 m',12,'Cantos frontales',0],
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
 {t:'Compra el kit de carros y el riel',d:'Compra el kit Ducloset Doble 45 kg y el riel U-20 de 2 m (el kit no lo trae). Altura de puerta ya confirmada con la ficha: H = 1914 − 38 (arriba) − 10 (abajo) = 1866 mm, con 10 mm de ajuste. Puertas de ≈25 mm de grueso: usa la placa invertida del kit (sistema de 60 mm).',n:[],f:[],tools:['Cinta métrica','Calculadora'],min:30},
 {t:'Rotula, lija y sella las piezas',d:'Escribe el número a lápiz en cada pieza (cara que no se ve). Lija con 120 y luego 220. Aplica sellador en todos los cantos, en caras interiores, en el fondo (13–14) y en las tapas de puerta por ambas caras. Deja secar según el envase.',n:[],f:[],tools:['Lijadora o taco','Lija 120 y 220','Brocha','Lápiz'],min:240},
 {t:'Perfora pockets y agujeros de soportes',d:'Con la plantilla pocket, perfora los agujeros ocultos en techo (cara superior), piso (cara inferior), división (cara derecha), repisa, zapatera y entrepaño 41 (cara inferior) y en la cara interior del zócalo 08, 09, 10 y 12 (bolsillo hacia arriba, para fijar el piso). Regla: ningún bolsillo en cara exterior de costados, en el piso visible ni en el frente; ver ficha de cada pieza. En los costados marca y perfora los soportes de tubo a 270 mm del frente; en la división (482 de fondo) a 205 mm de su canto frontal, que es la misma línea. Alturas al centro del tubo: izquierda 1900 y 980; derecha 1630.',n:[],f:[],tools:['Taladro','Plantilla pocket (Kreg o similar)','Broca escalonada pocket','Escuadra','Cinta métrica'],min:90},
 {t:'Arma el zócalo',d:'Une frente 08 y atrás 09 con los travesaños 10, 11 y 12 (extremos y centro) usando cola y un tornillo pocket por extremo. El frente queda remetido 50 mm. Comprueba la escuadra midiendo diagonales.',n:[8,9,10,11,12],f:[],tools:['Taladro','Desarmador / punta Phillips','Prensas','Escuadra','Cola Resistol 850'],min:45},
 {t:'Arma la caja: costados, techo y piso',d:'Con el mueble acostado, une techo 03 y piso 04 a los costados 01 y 02 con cola y pockets (4 por lado; en el piso el primero va a 90 del frente para librar el zócalo). El piso queda a 50 mm del suelo, encima del zócalo. Mide las dos diagonales: deben ser iguales.',n:[1,2,3,4],f:[],tools:['Taladro','Desarmador / punta Phillips','Prensas','Escuadra','Cinta métrica','Cola Resistol 850'],min:60},
 {t:'Coloca la división central',d:'Mete la división 05 al centro: 773 mm libres a cada lado. Fíjala con cola y 3 pockets arriba y 3 abajo, todos en la cara derecha de la división (la plantilla Kreg no llega al centro del techo). Usa un taco de 773 como separador para que quede paralela.',n:[5],f:[],tools:['Taladro','Prensas','Cinta métrica','Taco separador 773 mm'],min:30},
 {t:'Repisa, zapatera y entrepaño rigidizador',d:'Repisa 06 (461 de fondo) con la cara superior a 1700 mm del suelo; zapatera 07 (331 de fondo) con la cara superior a 270 mm. Van 19 mm menos profundas para librar el listón 15: apóyalas atrás, contra el listón; su frente queda 67 mm detrás del frente del mueble, fuera del carril de las puertas. 2 pockets por lado en la cara inferior. En el lado izquierdo, coloca el entrepaño rigidizador 41 con la cara inferior a 1035 mm, al ras de atrás (482 de fondo, frente 65 mm detrás del frente del mueble; 3 pockets por lado): amarra costado 01 y división a media altura y deja ~43 mm de paso para el gancho del tubo de 980.',n:[6,7,41],f:[],tools:['Taladro','Nivel','Prensas','Cinta métrica'],min:40},
 {t:'Listón y fondo',d:'Fija el listón 15 vertical centrado a 1210 mm del lado izquierdo, al ras de atrás: 2 tornillos #8 × 1½″ desde arriba del techo y 2 desde abajo del piso (pretaladra la testa a 3 mm). Coloca el fondo de triplay de pino de 5 mm: grande 13 desde la izquierda y tira 14 a la derecha; la unión cae sobre el listón. Tornillo #6 × 5/8″ cada ~185 mm (75 en total). Revisa diagonales antes de atornillar. Ventilación Ø25 en 2 filas a 140 y 1810 del canto inferior. El fondo total queda en 552 mm.',n:[15,13,14],f:[],tools:['Taladro','Desarmador','Broca Ø25 (ventilación)','Escuadra'],min:50},
 {t:'Levanta la caja y siéntala en el zócalo',d:'Entre dos personas, para el mueble y siéntalo sobre el zócalo, ya nivelado con cuñas en su sitio (deja 1–2 cm de la pared). Fíjalo desde dentro del zócalo: 20 tornillos pocket en los bolsillos de la cara interior de 08 y 09 (8 c/u) y de 10 y 12 (2 c/u), bolsillo hacia arriba, mordiendo la cara inferior del piso. El piso del ropero queda limpio, sin una sola pija a la vista. Tip: es más cómodo con la caja acostada sobre su espalda, presentando el zócalo contra el piso y luego levantando todo junto.',n:[],f:[8,9,10,11,12,4],tools:['Nivel','Cuñas niveladoras','Taladro','Ayudante'],min:30},
 {t:'Tubos para colgar',d:'Atornilla los soportes y coloca los tubos: 30 a 1900 mm y 31 a 980 mm en el lado izquierdo (prendas cortas, dos niveles); 32 a 1630 mm en el lado derecho (prendas largas; deja ~40 mm libres bajo la repisa para el gancho). Alturas al centro del tubo. Mide el claro real antes de cortar el tubo.',n:[30,31,32],f:[],tools:['Taladro','Desarmador','Segueta para metal','Nivel'],min:30},
 {t:'Riel doble bajo el techo',d:'Corta el riel U-20 a 1564 mm y atorníllalo bajo el techo 03, al frente, a escuadra con los costados. Tornillo #8 × 3/4″ (no más largo: el techo es de 18 mm). Eje del riel a 30 mm del canto frontal del techo; 6 tornillos a 40, 340, 640, 940, 1240 y 1524 mm del costado izquierdo (plantilla 03). Carriles a 33 mm entre centros.',n:[],f:[3],x:['riel'],tools:['Taladro','Segueta para metal','Escuadra','Desarmador'],min:30},
 {t:'Bastidores y tapas caladas',d:'Largueros de 1866. Une largueros 16–19 y travesaños 20–27 a media madera (63 × 9.5 mm) con cola y 2 tornillos #6 × 5/8″ por cruce (uno de 3/4″ traspasaría). Arriba, abajo y dos intermedios por puerta (a H/3 y 2H/3). Prensa en escuadra y deja secar 24 h. Mientras, cala las tapas 28 y 29 con la plantilla de ventanas: barreno Ø10 en cada esquina (radio 5), regla-guía prensada, caladora con hoja fina por dentro de la línea y cara buena abajo; lija los bordes. Cada tapa queda como un marco plano de 63 mm con 3 ventanas de 676 de ancho que calzan con los huecos del bastidor.',n:[16,17,18,19,20,21,22,23,24,25,26,27,28,29],f:[],tools:['Sierra','Caladora con hoja fina','Taladro y broca Ø10','Formón','Prensas','Regla-guía','Escuadra','Cola Resistol 850'],min:240},
 {t:'Yute sobre el bastidor',d:'Corta el yute 20 mm más grande por lado que cada hueco (39: 567.5 × 716, ×4; 40: 599 × 716, ×2). Tiéndelo sobre la cara frontal del bastidor y engrápalo con grapa de 8 mm cada 30 mm, a 10 mm por fuera del borde del hueco, del centro de cada lado hacia las esquinas y bien tenso. Las grapas quedan ocultas bajo la tapa calada.',n:[39,40],f:[16,17,18,19],tools:['Engrapadora de tapicero','Tijeras','Cúter'],min:120},
 {t:'Tapa calada sobre el yute',d:'Pon Resistol 850 sobre el margen de yute y el bastidor, presenta la tapa calada 28 (A) o 29 (B) con las ventanas alineadas a los huecos y prénsala con listones-calza cada ~300 mm (o peso parejo) 24 h. Sin grapas ni pijas en la cara frontal: la puerta queda limpia. Sin junquillo: el canto lijado de la ventana remata el yute. Puertas planas de ≈25 mm (19 + 1 + 5) y ≈7 kg.',n:[28,29],f:[16,17,18,19,39,40],tools:['Engrapadora','Cola Resistol 850','Prensas'],min:60},
 {t:'Acabado: linaza y cera de abeja',d:'En caras visibles, cantos de los bastidores y tapas caladas: linaza en capa delgada, retira el exceso a los 15 min y deja secar 24–48 h. Luego cera de abeja y pule. El yute se queda sin tratar. ⚠ Los trapos con linaza pueden autoincendiarse: extiéndelos a secar o mételos en agua.',n:[],f:[1,2,3,16,17,18,19,28,29],tools:['Trapo de algodón','Guantes','Paño para pulir'],min:90},
 {t:'Cuelga las puertas y ajusta',d:'Monta los carros en las puertas y cuélgalas en el riel doble: la Puerta A en el carril del frente (abre deslizando a la derecha) y la Puerta B en el carril de atrás (abre deslizando a la izquierda). Al cerrar se traslapan 40 mm al centro con 8 mm de juego entre puertas, coloca la guía inferior y ajusta la altura hasta que corran parejas.',n:[],f:[16,17,18,19,28,29],tools:['Desarmador','Llave del kit','Nivel'],min:45},
];
window.BUY=[['Kit Ducloset doble 45 kg (Ducasse, Home Depot): 4 carros + tope + guía al piso','$389'],['Riel U-20 acero galvanizado 2 m (Ducasse) — el kit no lo trae','≈$226'],['Alternativa: riel U-20 aluminio 2 m (Madercenter, cortar a 1564)','$342.91'],['Tubo FIX Ø25, 2.4 m (salen 3 × 765)','$125'],['Triplay de pino 18 mm 122×244 – 3 hojas','$801 c/u'],['Triplay de pino 5 mm 122×244 – 3 hojas (fondo + tapas caladas de puerta)','$233 c/u'],['Pino seco 19×63 (1×3) 2.44 m – 8 tablas (7 puertas + 1 listón 15)',''],['Yute en rollo ≈ 4 m² (sin tratar)',''],['Cubrecanto de pino ≈ 10 m',''],['Resistol 850 – 1 L',''],['Sellador para madera',''],['Aceite de linaza cocida',''],['Cera de abeja (pasta)',''],['Lija 120 y 220',''],['Cuñas niveladoras para zócalo','']];
// Ferretería con nombres como se piden en México. [nombre, cómo pedirlo, ícono]
window.FER_MX=[
 ['Tornillo para unión oculta Kreg, rosca gruesa, 1¼″ (cabeza plana con arandela)','«Tornillo Kreg de bolsillo de 1¼ pulgada, rosca gruesa, para madera blanda/triplay.» Caja de 100 (Home Depot: pasillo de herramienta Kreg).','kreg'],
 ['Pija para madera cabeza plana #8 × 1½″','«Pija para madera, cabeza plana (avellanada), punta de cruz, del 8 por pulgada y media.» Por pieza o bolsita.','pija'],
 ['Pija para madera cabeza plana #6 × 5/8″','«Pija para madera cabeza plana del 6 por cinco octavos.» Bolsa de 100 (fondo y puertas).','pija'],
 ['Pija para madera cabeza plana #8 × 5/8″','«Pija cabeza plana del 8 por cinco octavos» (para soportes de tubo y guía de piso).','pija'],
 ['Pija para madera cabeza plana #8 × ¾″ (para el riel)','«Pija cabeza plana del 8 por tres cuartos.» Confirma con los agujeros del riel antes de comprar.','pija'],
 ['Grapa para engrapadora de tapicero 8 mm (5/16″)','«Grapa de tapicería de 8 mm» para el yute.','grapa'],
 ['Riel corredizo para clóset, colgante doble, aluminio (kit con 4 carretillas y topes)','«Kit de riel corredizo doble para puertas de clóset de madera, que aguante 15 kg o más por puerta.» Ej.: Ducasse Ducloset doble 45 kg.','riel'],
 ['Guía de piso para puerta corrediza','«Guía inferior para puerta corrediza de clóset» (normalmente viene en el kit).','guia'],
 ['Soporte para tubo de clóset ⌀25 mm (brida)','«Soporte o brida para tubo de clóset de una pulgada.» Cerrado (O) en un lado y abierto (U) en el otro para poder sacar el tubo.','soporte'],
 ['Tubo de clóset ⌀25 mm (1″) de 2.4 m','«Tubo para clóset de una pulgada, 2.40 m» (FIX, cromado o redondo de acero).','tubo'],
 ['Pegamento blanco para madera (Resistol 850)','«Resistol 850, 1 litro.»','cola'],
 ['Plantilla Kreg para bolsillos (incluye broca escalonada 3/8″ con tope y punta cuadrada #2)','«Plantilla Kreg Pocket-Hole Jig» (Kreg 320 o 520). Trae la broca con su collar.','kreg'],
 ['Brocas para madera 1.5, 2 y 3 mm + avellanador 8 mm + sierra copa 1″ (25 mm)','«Brocas para madera de 1.5, 2 y 3 mm, un avellanador y una sierra copa de 1 pulgada con su mandril.»','broca'],
];
window.FER_ICON={
 kreg:'<path d="M6 30h30" stroke="#1F2A2E" stroke-width="3"/><path d="M14 14l16 16" stroke="#D9502B" stroke-width="5" stroke-linecap="round"/><circle cx="12" cy="12" r="5" fill="#fff" stroke="#1F2A2E" stroke-width="2"/>',
 pija:'<path d="M6 21h6l4-5v10l-4-5" fill="#6B7B78"/><path d="M16 18h16l6 3-6 3H16z" fill="#6B7B78"/><path d="M19 18l2 6M23 18l2 6M27 18l2 6M31 18l2 6" stroke="#fff" stroke-width="1"/>',
 clavo:'<path d="M8 21h28l4 0" stroke="#6B7B78" stroke-width="3"/><path d="M36 19l6 2-6 2z" fill="#6B7B78"/>',
 grapa:'<path d="M10 30V14h24v16" fill="none" stroke="#6B7B78" stroke-width="3"/>',
 riel:'<rect x="4" y="12" width="40" height="7" fill="#AEB8B5" stroke="#1F2A2E"/><circle cx="14" cy="23" r="4" fill="#1F2A2E"/><circle cx="32" cy="23" r="4" fill="#1F2A2E"/>',
 guia:'<path d="M6 30h36M14 30V22h20v8" fill="none" stroke="#1F2A2E" stroke-width="2.5"/>',
 soporte:'<circle cx="24" cy="22" r="9" fill="none" stroke="#1F2A2E" stroke-width="3"/><rect x="10" y="32" width="28" height="5" fill="#6B7B78"/>',
 tubo:'<rect x="4" y="18" width="40" height="9" rx="4.5" fill="#AEB8B5" stroke="#1F2A2E"/>',
 cola:'<rect x="16" y="14" width="16" height="24" rx="3" fill="#fff" stroke="#1F2A2E" stroke-width="2"/><path d="M21 14l3-7 3 7" fill="#D9502B"/>',
 broca:'<path d="M6 22h14" stroke="#1F2A2E" stroke-width="5"/><path d="M20 22h20" stroke="#6B7B78" stroke-width="3"/><path d="M22 19l4 6M28 19l4 6M34 19l4 6" stroke="#fff" stroke-width="1.2"/>'};
