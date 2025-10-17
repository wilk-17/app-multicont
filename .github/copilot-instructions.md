# AI Coding Agent Instructions - Multicont Flask API (Clean Architecture)

## Project Overview
Sistema de gestión empresarial con **Clean Architecture** (Hexagonal Architecture) implementada en Flask + PostgreSQL. La aplicación maneja organizaciones, sucursales, empleados, inventario, cotizaciones, órdenes de venta y facturación.

### Tech Stack
- **Backend**: Flask 2.3+
- **Database**: PostgreSQL con SQLAlchemy ORM
- **Migrations**: Flask-Migrate (Alembic)
- **API Docs**: Flasgger (Swagger UI)
- **Architecture**: Clean Architecture con separación en capas

## Architecture Overview

### Estructura de 3 Capas

```
app/
├── entities/        # DOMAIN LAYER - Modelos de dominio (DB Models)
│   ├── user.py
│   ├── organization.py
│   └── ...
├── use_cases/       # APPLICATION LAYER - Lógica de negocio (Handlers)
│   ├── user_handler.py
│   ├── organization_handler.py
│   └── ...
├── api/             # PRESENTATION LAYER - REST Endpoints (Blueprints)
│   ├── user_api.py
│   ├── organization_api.py
│   ├── metrics_api.py
│   └── dashboard_api.py
├── models/          # LEGACY - No usar, migrado a entities/
├── routes.py        # LEGACY - No usar, migrado a api/
└── config.py        # Configuración de la aplicación
```

### Flujo de Datos
```
HTTP Request → API Blueprint → Handler (Use Case) → Entity (Domain Model) → Database
                    ↓              ↓                      ↓
               Validación    Lógica Negocio        Lógica Dominio
```

## Key Architectural Principles

### 1. Entities (Domain Models)
**Ubicación**: `app/entities/{model_name}.py`

**Responsabilidades**:
- Hereda de `db.Model` (SQLAlchemy)
- Define esquema de base de datos
- Contiene lógica de dominio pura (métodos de negocio)
- Método `to_dict()` para serialización JSON

**Patrón estándar**:
```python
from datetime import datetime
from app import db

class ModelName(db.Model):
    __tablename__ = "model_name"
    
    # Columnas
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    children = db.relationship("ChildModel", backref="parent", lazy=True)
    
    def __init__(self, name, status='active'):
        self.name = name
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    # Lógica de dominio
    def activate(self):
        self.status = 'active'
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'status': self.status,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }
```

### 2. Use Cases (Handlers)
**Ubicación**: `app/use_cases/{model_name}_handler.py`

**Responsabilidades**:
- Lógica de aplicación y casos de uso
- Interacción con `db.session` (transacciones)
- Validaciones de negocio
- Paginación y filtros
- Manejo de excepciones

**Métodos estándar**:
- `create(**kwargs)` - Crear entidad
- `get(id)` - Obtener por ID
- `list_all(page, per_page, status)` - Listar con paginación
- `update(id, **kwargs)` - Actualizar entidad
- `delete(id)` - Eliminar entidad
- `count(status)` - Contar registros

**Patrón de paginación**:
```python
def list_all(self, page=1, per_page=10, status=None):
    query = Model.query
    if status:
        query = query.filter_by(status=status)
    query = query.order_by(Model.creation_date.desc())
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': paginated.items,
        'total': paginated.total,
        'page': paginated.page,
        'per_page': paginated.per_page,
        'total_pages': paginated.pages
    }
```

### 3. API Endpoints (Blueprints)
**Ubicación**: `app/api/{model_name}_api.py`

**Responsabilidades**:
- Definir rutas HTTP
- Parsear request (query params, JSON body)
- Llamar al handler correspondiente
- Formatear respuesta JSON
- Documentación Swagger

**Rutas estándar**:
- `GET /api/{resource}/` - Listar con paginación (`?page=1&per_page=10&status=active`)
- `GET /api/{resource}/<int:id>` - Obtener por ID
- `POST /api/{resource}/` - Crear nuevo
- `PUT /api/{resource}/<int:id>` - Actualizar
- `DELETE /api/{resource}/<int:id>` - Eliminar

**Formato de respuesta JSON estándar**:
```python
# Éxito
{
    "success": true,
    "data": {...},
    "message": "Operación exitosa"
}

# Error
{
    "success": false,
    "error": "Descripción del error"
}

# Paginación
{
    "success": true,
    "data": {
        "items": [...],
        "total": 100,
        "page": 1,
        "per_page": 10,
        "total_pages": 10
    }
}
```

## Developer Workflows

### Instalación y Setup
```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos (crear .env)
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here

# Inicializar migraciones (si no existe migrations/)
flask db init

# Crear y aplicar migraciones
flask db migrate -m "Initial migration"
flask db upgrade
```

### Ejecutar la aplicación
```bash
python run.py
# App corre en http://127.0.0.1:5000
# Swagger UI en http://127.0.0.1:5000/api/docs/
```

### Agregar Nuevo Modelo (Checklist Completo)

1. **Crear Entity** en `app/entities/{model_name}.py`
   - Heredar de `db.Model`
   - Definir `__tablename__`, columnas, relaciones
   - Método `__init__`, métodos de dominio, `to_dict()`

2. **Crear Handler** en `app/use_cases/{model_name}_handler.py`
   - Importar entity
   - Implementar CRUD: `create`, `get`, `list_all`, `update`, `delete`
   - Manejar transacciones con `db.session`

3. **Crear API Blueprint** en `app/api/{model_name}_api.py`
   - Crear Blueprint con `url_prefix='/api/{resources}'`
   - Instanciar handler
   - Definir endpoints RESTful
   - Agregar docstrings para Swagger

4. **Registrar en `app/__init__.py`**
   ```python
   # Dentro de create_app(), after imports:
   from .entities.{model_name} import ModelName  # Para Alembic
   from .api.{model_name}_api import {model_name}_api  # Para Flask
   
   # Dentro de blueprints list:
   app.register_blueprint({model_name}_api)
   ```

5. **Crear y aplicar migración**
   ```bash
   flask db migrate -m "Add ModelName"
   flask db upgrade
   ```

### Testing
```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=app tests/
```

## Database Conventions

### Tipos de Datos Estándar
- **IDs**: `db.BigInteger` con `autoincrement=True`
- **Foreign Keys**: `db.BigInteger, ForeignKey("table.id")`
- **Dinero**: `db.Numeric(12, 2)` para totales, `db.Numeric(10, 2)` para precios
- **Status**: `db.String(20)` con default `'active'`
- **Fechas**: `db.Date` para fechas, `db.DateTime` con `default=datetime.utcnow` para timestamps
- **Strings**: `db.String(length)` con longitud apropiada
- **Unique constraints**: Agregar `unique=True` a columna
- **Indexes**: Agregar `index=True` a columnas de búsqueda frecuente

### Relaciones SQLAlchemy
```python
# One-to-Many (el más común)
parent = db.relationship("Child", backref="parent", lazy=True)

# Many-to-One (implícito por ForeignKey)
parent_id = db.Column(db.BigInteger, ForeignKey("parent.id"))

# Cascade delete
children = db.relationship("Child", backref="parent", cascade="all, delete-orphan")
```

## API Features

### Paginación
Todos los endpoints `GET /` soportan:
- `?page=1` - Número de página (default: 1)
- `?per_page=10` - Items por página (default: 10)
- `?status=active` - Filtrar por status (si el modelo lo tiene)

### Métricas y Dashboard
- **GET `/api/metrics/users`** - Estadísticas de usuarios
- **GET `/api/metrics/inventory`** - Métricas de inventario
- **GET `/api/metrics/sales`** - Métricas de ventas
- **GET `/api/metrics/employees`** - Métricas de empleados
- **GET `/api/metrics/summary`** - Resumen consolidado

- **GET `/api/dashboard/?period=month`** - Dashboard principal (periods: day, week, month, year)
- **GET `/api/dashboard/kpis`** - KPIs del negocio

### Swagger Documentation
Acceder a http://127.0.0.1:5000/api/docs/ para:
- Documentación interactiva de todos los endpoints
- Probar APIs directamente desde el navegador
- Ver schemas de request/response

## Important Notes

### ⚠️ Cambios desde versión anterior
- **NO usar `app/models/` ni `app/routes.py`** - Son legacy
- **Flask-RESTX eliminado** - Ahora se usan Flask Blueprints nativos
- **Flasgger** reemplaza Swagger UI de RESTX
- Toda la lógica de negocio debe estar en **handlers**, no en APIs

### 🔐 Seguridad (Pending Implementation)
- **Passwords NO están hasheadas actualmente**
- TODO: Implementar `werkzeug.security.generate_password_hash()`
- TODO: Agregar JWT authentication
- TODO: Implementar middleware de autorización por roles

### 📊 Performance Tips
- Usar `lazy=True` en relationships para evitar N+1 queries
- Agregar `index=True` a columnas de búsqueda frecuente
- Paginar siempre en consultas grandes
- Usar `db.session.commit()` solo al final de transacciones

### 🐛 Debugging
```python
# Habilitar SQL logging
app.config['SQLALCHEMY_ECHO'] = True

# Ver queries ejecutadas
from flask import current_app
current_app.logger.debug(str(query))
```

## Project-Specific Business Rules

### Sales Flow (Flujo de Ventas)
1. **Quote** (Cotización) → Cliente solicita cotización
2. **QuotationLine** → Líneas de items en la cotización
3. **SalesOrder** (Orden de Venta) → Quote aprobada se convierte en orden
4. **Invoice** (Factura) → SalesOrder genera factura
5. **InvoiceItem** → Líneas de items facturados

### Inventory Management
- `InventoryItem.quantity` se actualiza automáticamente
- Métodos: `add_stock(amount)`, `remove_stock(amount)`
- Alertas generadas cuando `quantity < 10` (low stock)

### Organizational Hierarchy
**Organization** → **Branch** → **Employee** → **Assignment** (Asignación de items)

## Quick Reference Commands
```bash
# Desarrollo
python run.py                          # Iniciar servidor
flask db migrate -m "message"          # Crear migración
flask db upgrade                       # Aplicar migraciones
flask db downgrade                     # Revertir migración

# Generar archivos (si se necesitan más modelos)
python generate_refactor_files.py      # Genera handlers y APIs automáticamente

# Testing
pytest                                 # Ejecutar tests
pytest -v                              # Verbose
pytest --cov=app                       # Con coverage

# Base de datos
flask shell                            # Python shell con app context
```

## Example: Creating a New Feature

**Ejemplo: Agregar categoría "favorito" a InventoryItem**

1. **Modificar Entity**:
```python
# app/entities/inventory_item.py
is_favorite = db.Column(db.Boolean, default=False)

def mark_as_favorite(self):
    self.is_favorite = True
    self.update_date = datetime.utcnow()
```

2. **Crear migración**:
```bash
flask db migrate -m "Add is_favorite to inventory_item"
flask db upgrade
```

3. **Actualizar Handler**:
```python
# app/use_cases/inventory_item_handler.py
def mark_favorite(self, id):
    item = InventoryItem.query.get(id)
    if not item:
        raise ValueError("Item not found")
    item.mark_as_favorite()
    db.session.commit()
    return item
```

4. **Agregar endpoint**:
```python
# app/api/inventory_item_api.py
@inventory_item_api.route('/<int:id>/favorite', methods=['PUT'])
def mark_favorite(id):
    try:
        item = handler.mark_favorite(id)
        return jsonify({'success': True, 'data': item.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
```

---

**Architecture inspired by**: Clean Architecture (Robert C. Martin) and Hexagonal Architecture (Alistair Cockburn)
