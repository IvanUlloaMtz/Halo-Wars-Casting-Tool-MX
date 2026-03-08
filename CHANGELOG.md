# Changelog

## [1.1.0] - 2026-03-08

### Correcciones del Marcador (Scoreboard)

#### Imágenes de Líderes
- Ajustada la altura de `.leader-img-small` de `75px` a `62px` para que quepa dentro del contenedor del marcador de `70px`.
- Ajustada la altura de `.team-size-3 .leader-img-small` de `65px` a `55px` para modos 3v3.
- Añadido `margin-top: -1px` a `.leader-img-small` para mejorar la alineación vertical.

#### Eliminación del Líder "Endure"
- Eliminada la entrada inexistente "Endure" de la lista `LEADERS` en `matchdata.py`.
- Eliminada la entrada "Endure" del diccionario `LEADER_MAP` en `matchdata.py`.

#### Corrección de Bucle Infinito de Imágenes
- Corregido un bucle infinito en `score.js` y `card.js` donde el fallback de imágenes (webp → png → placeholder) se repetía indefinidamente si el placeholder tampoco existía.
- Creados archivos `placeholder.webp` y `placeholder.png` transparentes en `casting_html/leaders/` para evitar errores 404.

#### Posición de "SERIES WINNER"
- Movida la etiqueta "SERIES WINNER" de arriba (`bottom: 100%`) a debajo del marcador (`top: 100%; margin-top: 22px`) para que sea visible y no estorbe al historial de partidas.
- Invertido `border-radius` de `3px 3px 0 0` a `0 0 3px 3px` para que encaje visualmente debajo.

#### Diseño Simétrico `/\` del Marcador
- Invertida la inclinación (`skewX`) del equipo azul (P2) de `-20deg` a `+20deg` para crear una forma simétrica tipo `/\` en el centro del marcador.
- Añadidas reglas CSS de inversión para `.p2-side`, `#p2-score-block`, su contenido interno, historial y etiqueta de victoria.
- Creada animación `bounce-in-p2` dedicada para la etiqueta de victoria del equipo azul con skew invertido.
- Calibrada la posición del bloque azul usando `translateX(-8px)` dentro del `transform` para compensar el desplazamiento visual causado por la inclinación invertida.

#### Cache-Bust del CSS
- Actualizado el query param de versión del CSS en `score.html` de `?v=20260305` a `?v=20260308`.
- Nota: el servidor HTTP ya inyecta timestamps dinámicos automáticamente (ver `http_server.py`).
