# 🚀 Setup Rápido - Multicont Flask API

## Activar Entorno Virtual

### Windows PowerShell
```powershell
# Si aparece error de políticas, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Verificar activación (debe mostrar (venv) en el prompt)
python -c "import sys; print('✓ Virtual env activo' if 'venv' in sys.executable else '✗ No activado')"
```

### Windows CMD
```cmd
venv\Scripts\activate.bat
```

### Linux/Mac
```bash
source venv/bin/activate
```

## Verificar Instalación

```powershell
# Ver paquetes instalados
pip list

# Verificar Flask
python -c "import flask; print(f'Flask {flask.__version__}')"

# Verificar SQLAlchemy
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__}')"
```

## Configuración de Base de Datos

1. **Crear archivo `.env`** (copiar desde `.env.example`):
```powershell
Copy-Item .env.example .env
```

2. **Editar `.env`** con tus credenciales:
```env
DATABASE_URL=postgresql+psycopg2://postgres:TU_PASSWORD@localhost:5432/multicont_db
SECRET_KEY=genera-una-clave-secreta-aqui
FLASK_ENV=development
FLASK_APP=run.py
```

3. **Generar SECRET_KEY** (opcional):
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

## Inicializar Base de Datos

```powershell
# Crear base de datos en PostgreSQL primero
# psql -U postgres -c "CREATE DATABASE multicont_db;"

# Crear migraciones (si no existen)
flask db init

# Generar migración
flask db migrate -m "Refactor to Clean Architecture"

# Aplicar migraciones
flask db upgrade
```

## Ejecutar Aplicación

```powershell
# Modo desarrollo
python run.py

# O usando Flask CLI
flask run

# Con debug activo
$env:FLASK_DEBUG=1; flask run
```

La API estará en: `http://127.0.0.1:5000`
Swagger UI: `http://127.0.0.1:5000/api/docs/`

## Testing

```powershell
# Ejecutar tests
pytest

# Con coverage
pytest --cov=app

# Verbose con detalles
pytest -v --cov=app --cov-report=html
```

## Desactivar Entorno Virtual

```powershell
deactivate
```

## Reinstalar Dependencias

Si necesitas reinstalar todo:
```powershell
# Limpiar cache de pip
pip cache purge

# Reinstalar
pip install -r requirements.txt --force-reinstall
```

## Agregar Nuevas Dependencias

```powershell
# Instalar nuevo paquete
pip install nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt
```

## Troubleshooting

### Error: "execution of scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
```

### Error: "No module named 'flask'"
```powershell
# Verificar que el venv está activo
python -c "import sys; print(sys.executable)"
# Debe mostrar la ruta del venv, no la instalación global

# Reinstalar Flask
pip install Flask==2.3.3
```

### Error: "could not connect to server"
- Verificar que PostgreSQL está corriendo
- Verificar credenciales en `.env`
- Verificar que la base de datos existe

### Error de migraciones
```powershell
# Reset migraciones (¡CUIDADO! borra datos)
flask db downgrade base
flask db upgrade
```

## Scripts Útiles

### Crear datos de prueba
```powershell
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Context ready')"
```

### Ver estructura de BD
```powershell
flask shell
>>> from app import db
>>> db.metadata.tables.keys()
```

---

**Próximos pasos**: Ver `README.md` para documentación completa de la API
