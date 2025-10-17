# Script de Activación Rápida - Multicont Flask API
# Ejecutar con: .\activate.ps1

Write-Host "🚀 Activando entorno virtual Multicont Flask API..." -ForegroundColor Cyan

# Cambiar política de ejecución para este proceso
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

# Verificar activación
$pythonPath = python -c "import sys; print(sys.executable)"
if ($pythonPath -like "*venv*") {
    Write-Host "✓ Entorno virtual activado correctamente" -ForegroundColor Green
    Write-Host "  Python: $pythonPath" -ForegroundColor Gray
    
    # Mostrar información del ambiente
    Write-Host "`n📦 Paquetes principales instalados:" -ForegroundColor Yellow
    python -c "import flask, sqlalchemy, flasgger; print(f'  • Flask {flask.__version__}'); print(f'  • SQLAlchemy {sqlalchemy.__version__}'); print(f'  • Flasgger {flasgger.__version__}')"
    
    Write-Host "`n💡 Comandos útiles:" -ForegroundColor Cyan
    Write-Host "  python run.py              # Ejecutar aplicación" -ForegroundColor Gray
    Write-Host "  flask db migrate -m 'msg'  # Crear migración" -ForegroundColor Gray
    Write-Host "  flask db upgrade           # Aplicar migraciones" -ForegroundColor Gray
    Write-Host "  pytest                     # Ejecutar tests" -ForegroundColor Gray
    Write-Host "  deactivate                 # Desactivar entorno virtual" -ForegroundColor Gray
    
    Write-Host "`n🌐 Endpoints principales:" -ForegroundColor Cyan
    Write-Host "  http://127.0.0.1:5000              # API principal" -ForegroundColor Gray
    Write-Host "  http://127.0.0.1:5000/api/docs/    # Swagger UI" -ForegroundColor Gray
    
} else {
    Write-Host "✗ Error: El entorno virtual no se activó correctamente" -ForegroundColor Red
    Write-Host "  Python actual: $pythonPath" -ForegroundColor Gray
}
