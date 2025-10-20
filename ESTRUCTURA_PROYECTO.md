# 📁 Estructura del Proyecto - MultiCont Flask API

## 🎯 Organización General

Este documento describe la estructura organizada del proyecto después de la reorganización del 19 de octubre, 2025.

---

## 📂 Estructura de Carpetas

```
MultiContGit/
├── 📄 README.md                      # Documentación principal del proyecto
├── 📄 requirements.txt               # Dependencias Python
├── 📄 pytest.ini                     # Configuración de pytest
├── 📄 .env.example                   # Plantilla de variables de entorno
├── 📄 .gitignore                     # Archivos ignorados por git
│
├── 🚀 run.py                         # Script principal para iniciar servidor
├── 🚀 run_for_testing.py             # Script para iniciar en modo testing
├── 🚀 run_migration.bat              # Batch para ejecutar migraciones (Windows)
├── 🚀 start_server.bat               # Batch para iniciar servidor (Windows)
├── 🚀 activate.ps1                   # Script PowerShell para activar venv
├── 🚀 simplex_gui.py                 # GUI para método simplex (legacy)
│
├── 📁 app/                           # ✨ APLICACIÓN PRINCIPAL
│   ├── __init__.py                   # Inicialización de Flask app
│   ├── config.py                     # Configuración de la aplicación
│   │
│   ├── 📁 entities/                  # Modelos de dominio (DB Models)
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── branch.py
│   │   ├── employee.py
│   │   ├── inventory_item.py
│   │   ├── quote.py
│   │   ├── sales_order.py
│   │   ├── invoice.py
│   │   └── ... (21 entidades en total)
│   │
│   ├── 📁 use_cases/                 # Handlers (Lógica de negocio)
│   │   ├── base_handler.py           # ⭐ BaseHandler con patrón DRY
│   │   ├── user_handler.py
│   │   ├── organization_handler.py
│   │   ├── employee_handler.py
│   │   └── ... (22 handlers en total)
│   │
│   ├── 📁 api/                       # REST API Endpoints (Blueprints)
│   │   ├── helpers.py                # ⭐ Funciones helper para APIs
│   │   ├── auth_api.py               # Autenticación JWT
│   │   ├── user_api.py
│   │   ├── organization_api.py
│   │   ├── sales_analytics_api.py
│   │   └── ... (24 APIs en total)
│   │
│   ├── 📁 services/                  # Servicios de aplicación
│   │   ├── auth_service.py           # Servicio de autenticación
│   │   └── authorization_service.py  # ⭐ Servicio RBAC
│   │
│   ├── 📁 schemas/                   # Marshmallow Schemas (Validación)
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── employee_schema.py
│   │   ├── inventory_item_schema.py
│   │   ├── invoice_schema.py
│   │   ├── quote_schema.py
│   │   └── sales_order_schema.py
│   │
│   └── 📁 utils/                     # Utilidades
│       ├── decorators.py             # Decoradores JWT/RBAC
│       ├── security.py               # Funciones de seguridad
│       ├── exceptions.py             # ⭐ Excepciones personalizadas
│       └── helpers.py                # Funciones helper generales
│
├── 📁 migrations/                    # Migraciones de base de datos (Alembic)
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── 📁 versions/
│       ├── 78a49736b3ac_migración_inicial.py
│       └── 26d14f6f6172_inserta_datos.py
│
├── 📁 tests/                         # 🧪 SUITE DE TESTS
│   ├── __init__.py
│   ├── conftest.py                   # Configuración pytest + fixtures
│   │
│   ├── 📁 integration/               # Tests de integración
│   │   ├── test_final.py
│   │   ├── test_marshmallow_validation.py
│   │   ├── test_rbac_endpoints.py
│   │   ├── test_rbac_simple.py
│   │   └── test_server.py
│   │
│   ├── 📁 unit/                      # Tests unitarios (vacío, listo para usar)
│   │
│   ├── test_api_endpoints.py        # Tests de endpoints API
│   ├── test_auth.py                  # Tests de autenticación
│   ├── test_auth_system.py           # Tests del sistema de auth
│   ├── test_entities.py              # Tests de entidades
│   ├── test_handlers.py              # Tests de handlers
│   ├── test_validation.py            # Tests de validación
│   ├── test_analytics_endpoints.py   # Tests de analytics
│   ├── test_sales_analytics_data.py  # Tests de datos de ventas
│   ├── test_login_quick.py           # Test rápido de login
│   └── verify_data.py                # Verificación de datos
│
├── 📁 scripts/                       # 🛠️ SCRIPTS DE UTILIDAD
│   │
│   ├── 📁 database/                  # Scripts de base de datos
│   │   ├── populate_complete_database.py
│   │   ├── populate_database_final.py    # ⭐ Población completa
│   │   ├── populate_permissions.py
│   │   ├── seed_complete_database.py
│   │   ├── clear_database.py
│   │   ├── hash_user_passwords.py
│   │   ├── create_retroactive_goals.py
│   │   ├── populate_database.py
│   │   ├── populate_database_complete.py
│   │   └── populate_db_validated.py
│   │
│   ├── 📁 fixes/                     # Scripts de correcciones
│   │   ├── fix_apis.py
│   │   ├── fix_cache_delete_memoized.py
│   │   ├── fix_paginated_response.py
│   │   ├── fix_pagination_params.py
│   │   ├── fix_sales_analytics.py
│   │   ├── diagnose_500_errors.py
│   │   └── diagnose_delete_errors.py
│   │
│   ├── 📁 refactoring/               # Scripts de refactorización
│   │   ├── refactor_apis_batch.py
│   │   ├── refactor_remaining_apis.py
│   │   ├── add_swagger_docs.py
│   │   ├── update_all_apis_swagger.py   # ⭐ Update masivo de Swagger
│   │   ├── generate_models.py
│   │   └── generate_refactor_files.py
│   │
│   ├── 📁 verification/              # Scripts de verificación
│   │   ├── verify_api.py
│   │   ├── verify_empty_db.py
│   │   ├── verify_rbac.py
│   │   └── preview_goals_vs_actual.py
│   │
│   ├── 📁 legacy/                    # Scripts legacy (no eliminar)
│   │   ├── activate_auth_system.py
│   │   ├── fix_imports.py
│   │   ├── hash_existing_passwords.py
│   │   └── protect_endpoints_auto.py
│   │
│   ├── 📁 utils/                     # Utilidades
│   │   └── verify_models.py
│   │
│   ├── check_setup.py
│   └── generate_secret_keys.py
│
├── 📁 docs/                          # 📚 DOCUMENTACIÓN
│   │
│   ├── 📁 guides/                    # Guías de uso
│   │   ├── AUTHENTICATION_GUIDE.md   # ⭐ Guía de autenticación JWT
│   │   ├── TESTING_GUIDE.md          # ⭐ Guía de testing
│   │   ├── GUIA_TESTING_MANUAL.md
│   │   ├── DEPLOYMENT.md             # ⭐ Guía de despliegue (909 líneas)
│   │   └── FRONTEND_ANGULAR.md       # ⭐ Integración con Angular
│   │
│   ├── 📁 api/                       # Documentación de API
│   │   ├── API_VERIFICATION_REPORT.md
│   │   ├── ANALYSIS_SWAGGER_MISSING.md
│   │   ├── SWAGGER_ENDPOINTS_FIXED.md
│   │   ├── REFACTORING_SUMMARY.md
│   │   ├── RBAC_FIX_SUMMARY.md
│   │   ├── MODELO_NEGOCIO_RBAC.md    # ⭐ Modelo de roles y permisos
│   │   ├── EJEMPLOS_USO_API.md
│   │   ├── EJEMPLO_PROTEGER_ENDPOINTS.py
│   │   └── EXAMPLES_PROTECT_ENDPOINTS.py
│   │
│   ├── 📁 phases/                    # Documentación por fases
│   │   ├── FASE_3_SCHEMAS_MARSHMALLOW.md
│   │   ├── FASE_4_TESTING.md
│   │   └── FASE_5_REFACTORING.md     # ⭐ Refactoring DRY
│   │
│   ├── 📁 summaries/                 # Resúmenes ejecutivos
│   │   ├── RESUMEN_EJECUTIVO.md      # ⭐ Resumen principal del proyecto
│   │   ├── RESUMEN_EJECUTIVO_PROGRESO.md
│   │   ├── RESUMEN_FINAL_RBAC.md
│   │   ├── RESUMEN_MEJORAS_APLICADAS.md
│   │   ├── ANALISIS_EXHAUSTIVO_Y_PLAN_MEJORA.md
│   │   └── MEJORAS_COVERAGE.md
│   │
│   └── 📁 archive/                   # Documentación antigua
│       ├── README_OLD.md
│       ├── ANALISIS_CRUD_Y_RECOMENDACIONES_VISTAS.md
│       ├── ANALISIS_REQUERIMIENTOS_CORTE.md
│       ├── ROADMAP_IMPLEMENTACION.md
│       ├── SISTEMA_AUTENTICACION_JWT.md
│       └── SISTEMA_METAS_VENTAS_COMPLETO.md
│
├── 📁 reports/                       # Reportes generados
│
├── 📁 venv/                          # Entorno virtual Python
│
└── 📁 .github/                       # GitHub workflows
    └── copilot-instructions.md       # Instrucciones para GitHub Copilot

```

---

## 🎯 Descripción de Carpetas Principales

### 1. **app/** - Aplicación Principal
La aplicación Flask siguiendo **Clean Architecture** (Hexagonal Architecture):
- **entities/**: Modelos de dominio (21 entidades SQLAlchemy)
- **use_cases/**: Lógica de negocio (22 handlers, todos heredan de BaseHandler)
- **api/**: Endpoints REST (24 APIs con Flask Blueprints)
- **services/**: Servicios de aplicación (Auth, Authorization RBAC)
- **schemas/**: Validación de datos con Marshmallow (6 módulos)
- **utils/**: Utilidades compartidas (decorators, security, exceptions, helpers)

### 2. **tests/** - Suite de Tests
- **integration/**: Tests de integración end-to-end
- **unit/**: Tests unitarios (preparado para expansión)
- Tests organizados: API, Auth, Entities, Handlers, Validation
- **conftest.py**: Configuración de pytest con fixtures
- **111 tests totales** con 37.69% de cobertura

### 3. **scripts/** - Scripts de Utilidad
- **database/**: Población, seeding, limpieza de BD
- **fixes/**: Scripts para corregir problemas específicos
- **refactoring/**: Herramientas de refactorización masiva
- **verification/**: Scripts de verificación de sistema
- **legacy/**: Scripts antiguos (mantener para referencia)

### 4. **docs/** - Documentación
- **guides/**: Guías prácticas (Auth, Testing, Deployment, Frontend)
- **api/**: Documentación técnica de API y RBAC
- **phases/**: Documentación de fases del proyecto
- **summaries/**: Resúmenes ejecutivos y análisis
- **archive/**: Documentación obsoleta (no eliminar)

### 5. **migrations/** - Migraciones de Base de Datos
- Alembic migrations para PostgreSQL
- Historial completo de cambios de esquema

---

## 🚀 Comandos Principales

### Desarrollo
```bash
# Activar entorno virtual (Windows)
.\activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Copiar .env.example a .env y configurar

# Iniciar servidor de desarrollo
python run.py

# Iniciar servidor en modo testing
python run_for_testing.py
```

### Base de Datos
```bash
# Población completa de base de datos
python scripts/database/populate_database_final.py

# Seeding completo
python scripts/database/seed_complete_database.py

# Limpiar base de datos
python scripts/database/clear_database.py

# Crear migración
flask db migrate -m "descripción"

# Aplicar migraciones
flask db upgrade
```

### Testing
```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_auth.py
pytest tests/integration/test_rbac_endpoints.py

# Test rápido de login
python tests/test_login_quick.py
```

### Verificación
```bash
# Verificar API completa
python scripts/verification/verify_api.py

# Verificar sistema RBAC
python scripts/verification/verify_rbac.py

# Verificar base de datos vacía
python scripts/verification/verify_empty_db.py
```

---

## 📊 Arquitectura del Proyecto

### Clean Architecture (3 Capas)

```
┌─────────────────────────────────────────┐
│     PRESENTATION LAYER (API)            │
│  ┌─────────────────────────────────┐   │
│  │  Flask Blueprints (24 APIs)     │   │
│  │  - auth_api, user_api, etc.     │   │
│  │  - Swagger documentation        │   │
│  │  - JWT decorators               │   │
│  └─────────────────────────────────┘   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│   APPLICATION LAYER (USE CASES)         │
│  ┌─────────────────────────────────┐   │
│  │  Handlers (22 handlers)         │   │
│  │  - BaseHandler (DRY)            │   │
│  │  - Business Logic               │   │
│  │  - Validation                   │   │
│  └─────────────────────────────────┘   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      DOMAIN LAYER (ENTITIES)            │
│  ┌─────────────────────────────────┐   │
│  │  SQLAlchemy Models (21)         │   │
│  │  - Domain logic                 │   │
│  │  - Database schema              │   │
│  │  - Relationships                │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Flujo de Datos

```
HTTP Request → API Blueprint → Schema Validation → Handler → Entity → Database
                    ↓              ↓                  ↓         ↓
             JWT Auth       Marshmallow      Business Logic  ORM
             RBAC Check     Validation       Transactions    PostgreSQL
```

---

## 🔑 Características Principales

### ✅ Implementado (100%)

1. **Clean Architecture** - 3 capas bien definidas
2. **JWT Authentication** - Sistema completo con refresh tokens
3. **RBAC (Role-Based Access Control)** - Roles y permisos granulares
4. **Marshmallow Validation** - Validación en todos los endpoints
5. **BaseHandler DRY** - Sin repetición de código
6. **Swagger UI** - Documentación interactiva completa
7. **Exception Handling** - Manejo de errores profesional
8. **Testing Infrastructure** - 111 tests con pytest
9. **Database Migrations** - Alembic con historial completo
10. **Sales Analytics** - 15+ endpoints de métricas
11. **Sales Goals System** - Gestión de metas de ventas
12. **Brand Management** - Sistema de marcas

---

## 🎓 Requerimientos Académicos Cumplidos

✅ **ORM**: SQLAlchemy con 21 entidades  
✅ **Controllers**: 24 APIs con Flask Blueprints  
✅ **CRUD Completo**: Todas las entidades  
✅ **Paginación**: Estandarizada en todos los endpoints  
✅ **Reportes**: Sales analytics completo  
✅ **Autenticación**: JWT con bcrypt  
✅ **Autorización**: RBAC con roles y permisos  
✅ **Validación**: Marshmallow schemas  
✅ **Testing**: 111 tests unitarios e integración  
✅ **Documentación**: Swagger UI + 15+ docs MD  
✅ **Clean Architecture**: 3 capas separadas  
✅ **Seguridad**: bcrypt, JWT, RBAC, CORS  
✅ **Deployment Ready**: DEPLOYMENT.md completo  

---

## 📞 Acceso Rápido a Documentación Importante

### Para Empezar
1. **README.md** - Visión general del proyecto
2. **docs/guides/AUTHENTICATION_GUIDE.md** - Cómo usar JWT
3. **docs/guides/TESTING_GUIDE.md** - Cómo ejecutar tests

### Para Desarrollo
4. **docs/summaries/RESUMEN_EJECUTIVO.md** - Estado del proyecto
5. **docs/phases/FASE_5_REFACTORING.md** - Entender refactoring
6. **docs/api/MODELO_NEGOCIO_RBAC.md** - Modelo de permisos

### Para Despliegue
7. **docs/guides/DEPLOYMENT.md** - Guía completa (909 líneas)
8. **docs/guides/FRONTEND_ANGULAR.md** - Integración frontend

---

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask 2.3+
- **Database**: PostgreSQL con SQLAlchemy ORM
- **Auth**: Flask-JWT-Extended + bcrypt
- **Validation**: Marshmallow
- **Testing**: pytest + pytest-cov + pytest-flask
- **Migrations**: Flask-Migrate (Alembic)
- **API Docs**: Flasgger (Swagger UI)
- **Cache**: Flask-Caching
- **CORS**: Flask-CORS

---

## 📈 Estadísticas del Proyecto

- **Total Archivos Python**: ~150 archivos
- **Líneas de Código**: ~35,000 líneas
- **Entidades**: 21 modelos de dominio
- **Handlers**: 22 use cases
- **APIs**: 24 endpoints RESTful
- **Tests**: 111 tests (37.69% coverage)
- **Documentación**: 15+ archivos MD
- **Scripts**: 30+ utilidades

---

**Última actualización**: 19 de Octubre, 2025  
**Estado**: ✅ PROYECTO COMPLETAMENTE ORGANIZADO Y FUNCIONAL
