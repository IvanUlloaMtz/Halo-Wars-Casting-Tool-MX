# Halo Wars 2 Casting Tool MX

Herramienta profesional de casting para Halo Wars 2. Controla overlays en OBS mediante una interfaz sencilla.

## Características
- **Control de Marcador**: Gestiona nombres, equipos, y puntajes.
- **Overlays Animados**: Intro de jugadores y marcador superior con animaciones fluidas (GSAP).
- **Hotkeys Globales**: Control rápido con el teclado (F5-F8).
- **Conexión en Tiempo Real**: Comunicación inmediata entre la GUI y OBS vía WebSockets.

## Instalación

1. **Requisitos**: Python 3.8 o superior.
2. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Ejecuta el script principal:
```bash
python main.py
```

## Configuración en OBS

1. Abre OBS Studio.
2. Agrega una nueva fuente de tipo **Browser Source** (Navegador).
3. Marca la casilla "Local file" (Archivo local).
4. Selecciona el archivo overlay deseado:
   - **Intro**: `casting_html/intro.html`
   - **Marcador**: `casting_html/score.html`
5. Ajusta el tamaño (Width/Height) y CSS personalizado si es necesario.

## Uso

1. Llena los datos de los jugadores en la pestaña "Control de Partida".
2. Usa los botones o las teclas rápidas para mostrar la información:
   - **F5**: Mostrar Intro Jugador 1
   - **F6**: Mostrar Intro Jugador 2
   - **F7**: Actualizar/Mostrar Marcador
   - **F8**: Ocultar Todo (Reset)

## Configuración Avanzada

El archivo `config.json` se generará automáticamente en la carpeta raíz al iniciar por primera vez. Puedes editarlo para cambiar hotkeys y puertos.
