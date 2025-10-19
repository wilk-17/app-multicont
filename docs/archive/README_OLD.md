# 🏢 Multicont Flask API - Clean Architecture

Sistema de gestión empresarial con **Clean Architecture** implementado en Flask + PostgreSQL. Especializado en **análisis de metas de ventas** con tracking por empleado, sucursal y marca.

## 🚀 Características Principales

- ✅ **Sistema de Metas de Ventas** (mensual, trimestral, anual)
- ✅ **Analytics Avanzados** (7 endpoints especializados)
- ✅ **Clean Architecture** (3 capas: Entities, Use Cases, API)
- ✅ **21 Modelos de Dominio** completamente implementados
- ✅ **6 Marcas de Productos** (Omron, ING, Gefran, Weidmüller, Rice-Lake, Optec)
- ✅ **Dataset Completo** poblado (Q2-Q3 2025, $140M facturados)
- ✅ **Paginación** en todos los endpoints de lista
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

6. **Poblar base de datos con dataset completo** (OPCIONAL)
```bash
python populate_database.py
```

Esto crea:
- 5 Estados y 20 Ciudades
- 7 Organizaciones y 5 Sucursales
- 15 Empleados y 10 Usuarios
- 6 Marcas y 60 Items de inventario
- 12 Cotizaciones y 10 Facturas ($140M facturados)
- 18 Metas de ventas retroactivas

7. **Verificar datos poblados** (OPCIONAL)
```bash
python verify_data.py
```

8. **Crear metas retroactivas para análisis** (OPCIONAL)
```bash
python create_retroactive_goals.py
```

9. **Ejecutar aplicación**
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

#### 🏷️ Marcas
- `GET /api/brands/` - Listar marcas
- `POST /api/brands/` - Crear marca
- `GET /api/brands/<id>` - Obtener marca
- `GET /api/brands/search?name=Omron` - Buscar por nombre

#### 🎯 Metas de Ventas
- `GET /api/sales_goals/` - Listar metas
- `POST /api/sales_goals/` - Crear meta
- `GET /api/sales_goals/current` - Metas actuales
- `GET /api/sales_goals/by_employee/<id>` - Metas de empleado
- `GET /api/sales_goals/by_branch/<id>` - Metas de sucursal

#### 📊 Analytics (CORE FEATURE)
- `GET /api/analytics/invoicing/by_employee` - Facturación por empleado
- `GET /api/analytics/invoicing/by_branch` - Facturación por sucursal
- `GET /api/analytics/invoicing/by_brand` - Facturación por marca
- `GET /api/analytics/quotes/by_brand` - Cotizaciones por marca
- `GET /api/analytics/goals/vs_actual` - **Metas vs Ventas Reales** ⭐
- `GET /api/analytics/sales/summary` - Resumen consolidado
- `GET /api/analytics/top_performers` - Ranking de vendedores

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
- [ ] Poblar InvoiceItems para análisis por marca
- [ ] Tests unitarios para todos los handlers
- [ ] Tests de integración para APIs
- [ ] Frontend Dashboard (Vue.js/React recomendado)
- [ ] Docker y docker-compose
- [ ] CI/CD con GitHub Actions
- [ ] Rate limiting en endpoints públicos

## 📖 Documentación Adicional

- **RESUMEN_EJECUTIVO.md** - Estado del proyecto y dataset poblado
- **POBLACION_BASE_DATOS_COMPLETA.md** - Guía completa de población
- **SISTEMA_METAS_VENTAS_COMPLETO.md** - Documentación técnica (600+ líneas)
- **IMPLEMENTACION_COMPLETA.md** - Quick reference y checklist
- **ANALISIS_CRUD_Y_RECOMENDACIONES_VISTAS.md** - Estrategia CRUD

## 🎯 Quick Start para Analytics

### 1. Poblar base de datos
```bash
python populate_database.py
python create_retroactive_goals.py
```

### 2. Iniciar servidor
```bash
python run.py
```

### 3. Probar endpoint principal
```bash
curl "http://127.0.0.1:5000/api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-04-01&end_date=2025-09-30"
```

### 4. Ver en Swagger UI
Abrir: `http://127.0.0.1:5000/api/docs/`

Buscar sección **analytics** y probar endpoints interactivamente.

## 📊 Análisis Disponibles

### Metas vs Actual
Compara metas de ventas configuradas contra facturación real:
- **Porcentaje de cumplimiento** calculado automáticamente
- **Status dinámico**: exceeded (≥100%), on_track (80-99%), at_risk (50-79%), failed (<50%)
- **Filtros**: Por período (monthly/quarterly/yearly), empleado o sucursal

### Top Performers
Ranking de vendedores por volumen de ventas:
- Ordenado de mayor a menor facturación
- Incluye número de facturas y total vendido
- Filtrable por rango de fechas

### Resumen de Ventas
KPIs consolidados del negocio:
- Total facturado y cotizado
- Número de facturas y cotizaciones
- Ticket promedio
- Tasa de conversión (cotizaciones → facturas)

## 🏆 Dataset Completo Incluido

El sistema incluye un dataset realista de 6 meses:

- **Período**: Abril - Septiembre 2025
- **Total Facturado**: $140,040,000 COP
- **Facturas**: 10 registros
- **Cotizaciones**: 12 registros
- **Empleados**: 15 distribuidos en 5 sucursales
- **Marcas**: 6 (60 items de inventario)
- **Metas**: 18 configuradas (13 mensuales + 5 trimestrales)

### Top 3 Vendedores
1. 🥇 Jorge Nieto: $39,350,000
2. 🥈 Ana García: $30,200,000
3. 🥉 Gloria Vega: $19,300,000

### Métricas Clave
- Crecimiento Q2→Q3: +49.0%
- Tasa de conversión: ~80%
- Ticket promedio: $14,004,000

## 📝 Licencia

[Especificar licencia]

## 👥 Contribuidores

- [Tu nombre]

## 📞 Contacto

Para preguntas o sugerencias, contactar a [email]

---

**Clean Architecture** inspirada en: Robert C. Martin (Uncle Bob) y Alistair Cockburn (Hexagonal Architecture)
