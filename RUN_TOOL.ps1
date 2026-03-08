# Script de inicio para Halo Wars 2 Casting Tool
# Ejecutar este script en PowerShell si el archivo .bat no funciona.

Set-Location $PSScriptRoot

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO HALO WARS 2 CASTING TOOL" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "[ERROR] No se encontró el entorno virtual (.venv) en: $PSScriptRoot" -ForegroundColor Red
    Write-Host "Por favor, asegúrate de que el entorno virtual esté instalado."
    Read-Host "Presiona Enter para salir..."
    exit 1
}

Write-Host "[INFO] Ejecutando programa..." -ForegroundColor Green
python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] El programa se cerró con un error (Código: $LASTEXITCODE)." -ForegroundColor Red
    Write-Host "Revisa el archivo 'app.log' para más detalles."
    Read-Host "Presiona Enter para salir..."
}
