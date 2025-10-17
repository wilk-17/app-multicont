# 🏢 Multicont Flask API - Clean Architecture

Sistema de gestión empresarial con **Clean Architecture** implementado en Flask + PostgreSQL. Maneja organizaciones, sucursales, empleados, inventario, cotizaciones, órdenes de venta y facturación.

## 🚀 Características

- ✅ **Clean Architecture** (3 capas: Entities, Use Cases, API)
- ✅ **19 Modelos de Dominio** completamente implementados
- ✅ **Paginación** en todos los endpoints de lista
- ✅ **Métricas y Dashboard** para KPIs de negocio
- ✅ **Swagger UI** interactivo (Flasgger)
- ✅ **PostgreSQL** con SQLAlchemy ORM
- ✅ **Migraciones** con Flask-Migrate (Alembic)

## 📁 Estructura del Proyecto

```
app/
├── entities/          # 🎯 Domain Models (Lógica de dominio)
│   ├── user.py
│   ├── organization.py
│   ├── inventory_item.py
│   └── ...
│
├── use_cases/         # 💼 Application Logic (Handlers)
│   ├── user_handler.py
│   ├── organization_handler.py
│   └── ...
│
├── api/               # 🌐 REST Endpoints (Blueprints)
│   ├── user_api.py
│   ├── metrics_api.py
│   ├── dashboard_api.py
│   └── ...
│
├── config.py          # ⚙️ Configuración
└── __init__.py        # 🏗️ Application Factory
```

## 🔧 Instalación

### Prerrequisitos
- Python 3.9+
- PostgreSQL 12+
- pip

### Setup

1. **Clonar repositorio**
```bash
git clone https://github.com/wilk-17/app-multicont.git
cd app-multicont
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crear archivo `.env` en la raíz:
```env
DATABASE_URL=postgresql+psycopg2://postgres:tu_password@localhost:5432/nombre_db
SECRET_KEY=tu-secret-key-aqui
FLASK_ENV=development
```

5. **Inicializar base de datos**
```bash
# Crear migraciones (si no existen)
flask db init

# Generar migración inicial
flask db migrate -m "Initial migration"

# Aplicar migraciones
flask db upgrade
```

6. **Ejecutar aplicación**
```bash
python run.py
```

La API estará disponible en: `http://127.0.0.1:5000`

## 📚 Documentación API

### Swagger UI
Acceder a: `http://127.0.0.1:5000/api/docs/`

Documentación interactiva con todos los endpoints, schemas y posibilidad de probar directamente.

### Endpoints Principales

#### 👤 Usuarios
- `GET /api/users/?page=1&per_page=10` - Listar usuarios
- `GET /api/users/<id>` - Obtener usuario
- `POST /api/users/` - Crear usuario
- `PUT /api/users/<id>/activate` - Activar usuario
- `GET /api/users/statistics` - Estadísticas de usuarios

#### 🏢 Organizaciones
- `GET /api/organizations/` - Listar organizaciones
- `POST /api/organizations/` - Crear organización
- `PUT /api/organizations/<id>` - Actualizar
- `DELETE /api/organizations/<id>` - Eliminar

#### 📦 Inventario
- `GET /api/inventory_items/?status=active` - Items de inventario
- `POST /api/inventory_items/` - Agregar item
- `PUT /api/inventory_items/<id>` - Actualizar item

#### 💰 Ventas
- `GET /api/quotes/` - Cotizaciones
- `GET /api/sales_orders/` - Órdenes de venta
- `GET /api/invoices/` - Facturas

#### 📊 Métricas y Dashboard
- `GET /api/metrics/users` - Métricas de usuarios
- `GET /api/metrics/inventory` - Métricas de inventario
- `GET /api/metrics/sales` - Métricas de ventas
- `GET /api/metrics/summary` - Resumen general
- `GET /api/dashboard/?period=month` - Dashboard completo
- `GET /api/dashboard/kpis` - KPIs del negocio

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app

# Verbose
pytest -v
```

## 🏗️ Arquitectura

### Clean Architecture (3 Capas)

```
┌─────────────────────────────────────────┐
│         API Layer (Blueprints)          │  ← Flask Routes
│  - Parsing requests                     │
│  - JSON responses                       │
│  - Swagger docs                         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Use Cases Layer (Handlers)         │  ← Business Logic
│  - CRUD operations                      │
│  - Validation                           │
│  - Transactions                         │
│  - Pagination                           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Entities Layer (Models)           │  ← Domain Logic
│  - SQLAlchemy models                    │
│  - Domain methods                       │
│  - Relationships                        │
└─────────────────────────────────────────┘
```

### Flujo de Datos
```
HTTP Request → API → Handler → Entity → Database
                ↓        ↓         ↓
            Routing  Business  Domain
                    Logic     Logic
```

## 📈 Modelos de Negocio

### Flujo de Ventas
```
Quote (Cotización)
    ↓
QuotationLine (Líneas de cotización)
    ↓
SalesOrder (Orden de venta)
    ↓
Invoice (Factura)
    ↓
InvoiceItem (Items facturados)
```

### Estructura Organizacional
```
Organization (Organización)
    ↓
Branch (Sucursal)
    ↓
Employee (Empleado)
    ↓
Assignment (Asignación de items)
```

## 🔑 Convenciones de Código

### Responses JSON Estándar
```json
// Éxito
{
  "success": true,
  "data": {...},
  "message": "Operación exitosa"
}

// Error
{
  "success": false,
  "error": "Descripción del error"
}

// Con paginación
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

### Paginación
Todos los endpoints de lista soportan:
- `?page=1` - Número de página
- `?per_page=10` - Items por página
- `?status=active` - Filtro por estado

## 🛠️ Desarrollo

### Agregar Nuevo Modelo

1. Crear entity en `app/entities/`
2. Crear handler en `app/use_cases/`
3. Crear API en `app/api/`
4. Registrar en `app/__init__.py`
5. Crear migración: `flask db migrate -m "Add Model"`
6. Aplicar: `flask db upgrade`

Ver `.github/copilot-instructions.md` para guía completa.

### Generar Handlers/APIs Automáticamente

Usa el script generador:
```bash
python generate_refactor_files.py
```

## 📦 Dependencias Principales

- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Migrate 4.0.5
- PostgreSQL (psycopg2-binary)
- Flasgger (Swagger UI)

Ver `requirements.txt` para lista completa.

## 🚧 Pendientes / TODOs

- [ ] Implementar hash de passwords (bcrypt/werkzeug)
- [ ] Agregar JWT authentication
- [ ] Sistema de permisos por roles
- [ ] Tests unitarios para todos los handlers
- [ ] Tests de integración para APIs
- [ ] Docker y docker-compose
- [ ] CI/CD con GitHub Actions
- [ ] Rate limiting en endpoints públicos

## 📝 Licencia

[Especificar licencia]

## 👥 Contribuidores

- [Tu nombre]

## 📞 Contacto

Para preguntas o sugerencias, contactar a [email]

---

**Clean Architecture** inspirada en: Robert C. Martin (Uncle Bob) y Alistair Cockburn (Hexagonal Architecture)
