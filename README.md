# Studio
Sitio de proyectos de muebles y diseño: https://studio.strate.lat (GitHub Pages).

## Agregar un proyecto
1. Crear carpeta `/<proyecto>/` con su `index.html` (autocontenido, sin dependencias externas) y archivos (PDF, etc.).
2. Guardar fuentes para regenerar en `/<proyecto>/src/`.
3. En `index.html` (raíz) copiar un bloque `<a class="card">` y cambiar enlace, título, descripción y miniatura SVG.
4. `git add -A && git commit -m "Nuevo proyecto" && git push` — Pages publica en ~1 min.

## Ropero (regenerar)
`cd ropero/src && python3 data.py` (genera data.json con verificaciones), luego insertar data.json en `app_tpl.html` (reemplazar `__DATA__`) → `ropero/index.html`. PDF: `g.py` (rutas en /workspace/ropero; ajustar).
