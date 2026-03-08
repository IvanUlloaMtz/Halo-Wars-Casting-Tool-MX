@echo off
SETLOCAL EnableExtensions
TITLE Halo Wars 2 Casting Tool

:: Asegurar que el directorio de trabajo es el del script
cd /d "%~dp0"

echo ===========================================
echo   INICIANDO HALO WARS 2 CASTING TOOL
echo ===========================================
echo.

:: Verificar si existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] No se encontro el entorno virtual (.venv) en:
    echo %CD%
    echo.
    echo Por favor, asegúrate de que el entorno virtual esté instalado.
    echo Puedes intentar ejecutar: python -m venv .venv
    pause
    exit /b 1
)

:: Activar entorno virtual y ejecutar
echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate.bat

echo [INFO] Ejecutando programa...
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] El programa se cerro con un error (Codigo: %ERRORLEVEL%).
    echo Revisa el archivo 'app.log' para mas detalles.
    pause
)

exit /b %ERRORLEVEL%
