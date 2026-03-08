# Changelog

## [1.2.0] - 2026-03-08

### Nuevas Funcionalidades

#### Indicadores de Conexión Dinámicos (LED con Pulso)
- Reemplazados los indicadores estáticos `🟢` por LEDs circulares CSS con efecto de **respiración suave** (sine wave).
- Cuando `score.html` o `card.html` se conectan por WebSocket, el LED correspondiente cambia de rojo fijo a verde con pulso suave.
- Al desconectarse, el LED vuelve a rojo fijo.
- Los clientes WebSocket ahora usan paths identificativos: `/score`, `/intro`, `/card` para distinguir las conexiones.
- El servidor WS emite el path del cliente en las señales `client_connected` y `client_disconnected`.

#### Checkboxes con Palomita ✓
- Los checkboxes ahora muestran una palomita blanca (✓) sobre fondo azul al estar marcados, en vez de un cuadro sólido.
- Creado archivo SVG `hwctool/view/check_white.svg` para el icono del checkmark.
- Actualizado en ambos temas (dark y light).

### Mejoras de Interfaz

#### Valores por Defecto de Tasks
- `Show Team Names` — activado por defecto ✅
- `Show Flags` — activado por defecto ✅
- `Show Game Type` (Display Type) — desactivado por defecto ⬜

#### Settings
- Botón `Copy Intro URL` deshabilitado (intro no disponible actualmente).
- URLs de `Copy Score` y `Copy Card` verificadas correctas.

#### Dropdowns con Fondo Sólido
- Todas las listas desplegables (`QComboBox`) ahora usan fondo sólido opaco (no transparente).
- Añadido hover effect y padding a los items del dropdown.
- Aplicado en ambos temas (dark: `#313244`, light: `#ffffff`).

### Correcciones de Estabilidad

#### Apagado Limpio del Servidor WebSocket
- `_shutdown()` ya no llama `loop.stop()` internamente — ahora se llama con `call_soon_threadsafe()` después de completar la coroutine.
- Eliminado el error `Event loop stopped before Future completed` que aparecía al cerrar la app.

#### Apagado Limpio del Servidor HTTP
- `httpd.shutdown()` ahora se ejecuta en un thread auxiliar con timeout de 2 segundos.
- Eliminado el bloqueo indefinido y `KeyboardInterrupt` al cerrar la app.

#### Silenciado Logger de websockets
- Silenciado el logger interno de la librería `websockets` para evitar `UnicodeEncodeError` en consolas Windows.

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
