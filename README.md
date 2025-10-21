# 🏢 Multicont - Sistema de Gestión Empresarial# 🏢 Multicont - Sistema de Gestión Empresarial# 🏢 Multicont - Sistema de Gestión Empresarial con Clean Architecture



[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)

[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

[![Tests](https://img.shields.io/badge/Tests-369/369%20RBAC-brightgreen.svg)]()

[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-blueviolet.svg)]()[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)

[![License](https://img.shields.io/badge/License-Academic-blue.svg)]()

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue.svg)](https://www.postgresql.org/)[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue.svg)](https://www.postgresql.org/)

**Versión**: 2.0.0  

**Fecha**: 21 de Octubre de 2025  [![JWT](https://img.shields.io/badge/JWT-Enabled-orange.svg)](https://jwt.io/)[![JWT](https://img.shields.io/badge/JWT-Enabled-orange.svg)](https://jwt.io/)

**Arquitectura**: Clean Architecture (Hexagonal)  

**Stack**: Flask + PostgreSQL + SQLAlchemy + JWT + RBAC + pytest  [![RBAC](https://img.shields.io/badge/RBAC-100%25-success.svg)]()[![RBAC](https://img.shields.io/badge/RBAC-Complete-red.svg)]()

**Estado**: ✅ Producción

[![Tests](https://img.shields.io/badge/Tests-90/90%20RBAC-brightgreen.svg)]()[![Tests](https://img.shields.io/badge/Tests-111%20passing-brightgreen.svg)]()

---

[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-blueviolet.svg)]()[![Coverage](https://img.shields.io/badge/Coverage-37.69%25-yellow.svg)]()

## 🎯 Descripción del Proyecto

[![License](https://img.shields.io/badge/License-Academic-blue.svg)]()[![Team](https://img.shields.io/badge/Team-Wilker%20%26%20Daniel-blueviolet.svg)]()

**Multicont** es un sistema integral de gestión empresarial con **Clean Architecture** que implementa control total sobre operaciones de negocio: organizaciones, sucursales, empleados, inventario, cotizaciones, órdenes de venta y facturación.

[![License](https://img.shields.io/badge/License-Academic-blue.svg)]()

### ✨ Características Principales

**Versión**: 1.0.0  

- 🏗️ **Clean Architecture (3 Capas)**: Entities (Domain) → Use Cases (Business Logic) → API (Presentation)

- 🔐 **Sistema RBAC Completo**: JWT + bcrypt + 3 roles (ADMIN, MANAGER, SALES)**Arquitectura**: Clean Architecture (Hexagonal)  **Versión**: 3.0.0  

- ✅ **100% Tests RBAC**: 369/369 tests pasando (123 endpoints × 3 roles)

- 📊 **Analytics Avanzados**: Dashboard, KPIs, métricas de ventas/inventario/empleados**Stack**: Flask + PostgreSQL + SQLAlchemy + JWT + RBAC + Marshmallow + pytest  **Arquitectura**: Clean Architecture (Hexagonal) + DRY Pattern  

- 📝 **Validación Marshmallow**: Schemas en todos los endpoints

- 📚 **Swagger UI**: Documentación interactiva completa en `/api/docs/`**Estado**: ✅ Producción**Stack**: Flask + PostgreSQL + SQLAlchemy + JWT + RBAC + Marshmallow + pytest

- 🗂️ **22 Entidades ORM**: Completamente relacionadas

- 🔄 **Migraciones Alembic**: Control de versiones de base de datos

- 📄 **Paginación**: En todos los endpoints de listado

------

---



## 📋 Tabla de Contenidos

## 🎯 Descripción## 🎯 Descripción del Proyecto

- [Estructura del Proyecto](#-estructura-del-proyecto)

- [Arquitectura](#️-arquitectura-clean-architecture)

- [Requisitos](#-requisitos-del-sistema)

- [Instalación](#-instalación)**Multicont** es un sistema integral de gestión empresarial con **Clean Architecture** que implementa control total sobre operaciones de negocio: organizaciones, sucursales, empleados, inventario, cotizaciones, órdenes de venta y facturación.**Multicont** es un sistema integral de gestión empresarial desarrollado completamente con **Clean Architecture**, diseñado para empresas que necesitan control total sobre su operación. Este proyecto académico implementa las mejores prácticas de desarrollo backend con Python/Flask.

- [Configuración](#️-configuración)

- [Base de Datos](#️-base-de-datos)

- [Ejecución](#-ejecución)

- [Testing](#-testing)### ✨ Características Principales### ✨ Características Destacadas

- [Autenticación y RBAC](#-autenticación-y-rbac)

- [Endpoints de la API](#-endpoints-de-la-api)

- [Documentación](#-documentación)

- [Equipo](#-equipo-de-desarrollo)- 🏗️ **Clean Architecture (3 Capas)**: Entities (Domain) → Use Cases (Business) → API (Presentation)- 🏗️ **Clean Architecture (3 Capas)**: Entities → Use Cases → API



---- 🔐 **Sistema RBAC Completo**: JWT + bcrypt + 4 roles (ADMIN, MANAGER, SALES, VIEWER)- 🔐 **Sistema RBAC Completo**: Roles, permisos y JWT authentication (100% tests passing)



## 📁 Estructura del Proyecto- ✅ **100% Tests RBAC**: 90/90 tests pasando (30 por rol)- 📊 **Analytics de Ventas**: 15+ endpoints con métricas avanzadas



```- 📊 **Analytics Avanzados**: Dashboard, KPIs, métricas de ventas/inventario/empleados- ✅ **Testing Infrastructure**: 111 tests con pytest (37.69% coverage)

app-multicont/

├── app/                         # 💻 Aplicación principal (Clean Architecture)- 📝 **Validación Marshmallow**: Schemas en todos los endpoints- 📝 **Validación Robusta**: Marshmallow schemas en todos los endpoints

│   ├── __init__.py              # Factory de Flask con blueprints

│   ├── config.py                # Configuración (DB, JWT, CORS)- 🎯 **BaseHandler DRY**: Sin duplicación de código- 🎯 **BaseHandler DRY**: Sin repetición de código en 22 handlers

│   │

│   ├── entities/                # 🔷 CAPA 1 - Modelos de Dominio (22 entidades)- 📚 **Swagger UI**: Documentación interactiva en `/api/docs/`- 📚 **Swagger UI**: Documentación interactiva completa

│   │   ├── user.py              # Usuario con RBAC

│   │   ├── role.py              # Roles del sistema- 🗂️ **23 Entidades ORM**: Completamente implementadas- 🗂️ **21 Entidades de Dominio**: Completamente implementadas con ORM

│   │   ├── permission.py        # Permisos granulares

│   │   ├── organization.py      # Organizaciones- 🔄 **Migraciones Alembic**: Control de versiones de BD- 🔄 **Migraciones Alembic**: Control total de versiones de BD

│   │   ├── branch.py            # Sucursales

│   │   ├── person.py            # Personas (clientes/empleados)- 📄 **Paginación**: En todos los endpoints de listado- 🚀 **Production Ready**: Deployment guide completo

│   │   ├── employee.py          # Empleados

│   │   ├── inventory_item.py    # Items de inventario

│   │   ├── assignment.py        # Asignaciones a empleados

│   │   ├── quote.py             # Cotizaciones------- ✅ **Paginación** en todos los endpoints de lista

│   │   ├── quotation_line.py    # Líneas de cotización

│   │   ├── sales_order.py       # Órdenes de venta

│   │   ├── invoice.py           # Facturas

│   │   └── ... (22 entidades total)## 📁 Estructura del Proyecto- ✅ **Swagger UI** interactivo (Flasgger)

│   │

│   ├── use_cases/               # ⚙️ CAPA 2 - Lógica de Negocio (20 handlers)

│   │   ├── base_handler.py      # Handler base con DRY pattern

│   │   ├── user_handler.py      # Lógica de usuarios```## 📋 Tabla de Contenidos- ✅ **PostgreSQL** con SQLAlchemy ORM

│   │   ├── organization_handler.py

│   │   ├── inventory_item_handler.pyapp-multicont/

│   │   └── ... (20 handlers total)

│   │├── app/                    # Aplicación principal- ✅ **Migraciones** con Flask-Migrate (Alembic)

│   ├── api/                     # 🌐 CAPA 3 - REST API (24 blueprints)

│   │   ├── user_api.py          # Endpoints de usuarios│   ├── entities/           # CAPA 1 - Modelos de Dominio (DB Models)

│   │   ├── role_api.py          # Endpoints de roles

│   │   ├── organization_api.py  # Endpoints de organizaciones│   │   ├── user.py- [Descripción](#-descripción)

│   │   ├── inventory_item_api.py

│   │   ├── sales_analytics_api.py  # 7 endpoints de analytics│   │   ├── organization.py

│   │   ├── metrics_api.py       # 5 endpoints de métricas

│   │   ├── dashboard_api.py     # Dashboard principal│   │   ├── inventory_item.py- [Características](#-características)## 📁 Estructura del Proyecto

│   │   └── ... (24 APIs total)

│   ││   │   └── ... (23 modelos)

│   ├── schemas/                 # 📝 Validación Marshmallow

│   │   ├── user_schemas.py│   ├── use_cases/          # CAPA 2 - Lógica de Negocio (Handlers)- [Arquitectura](#-arquitectura)

│   │   ├── organization_schemas.py

│   │   └── ... (22 schemas)│   │   ├── base_handler.py

│   │

│   ├── services/                # 🔧 Servicios auxiliares│   │   ├── user_handler.py- [Requisitos](#-requisitos)```

│   │   ├── authorization_service.py  # Decorador @require_role()

│   │   └── authentication_service.py  # Login, JWT, validación│   │   └── ... (20 handlers)

│   │

│   └── utils/                   # 🛠️ Utilidades│   ├── api/                # CAPA 3 - Endpoints REST (Blueprints)- [Instalación Rápida](#-instalación-rápida)app/

│       ├── security.py          # Hashing bcrypt

│       ├── cache.py             # Cache de sesiones│   │   ├── user_api.py

│       └── validators.py        # Validadores personalizados

││   │   ├── metrics_api.py- [Configuración](#-configuración)├── entities/          # 🎯 Domain Models (Lógica de dominio)

├── migrations/                  # 🗄️ Migraciones Alembic

│   └── versions/                # 5 migraciones (23 tablas)│   │   └── ... (20 APIs)

│

├── tests/                       # 🧪 Tests automatizados│   ├── schemas/            # Validación con Marshmallow- [Uso de la API](#-uso-de-la-api)│   ├── user.py

│   ├── integration/             # Tests de integración

│   │   ├── test_rbac_simple.py             # 90 tests RBAC (30 × 3 roles)│   ├── utils/              # Utilidades (security, cache, etc.)

│   │   ├── test_rbac_exhaustive_interactive.py  # 369 tests (123 × 3)

│   │   └── test_rbac_endpoints.py│   ├── services/           # Servicios externos- [Endpoints Principales](#-endpoints-principales)│   ├── organization.py

│   └── unit/                    # Tests unitarios

│       └── test_assignment_tracking.py  # 7 tests tracking│   └── config.py           # Configuración

│

├── scripts/                     # 🛠️ Scripts auxiliares├── migrations/             # Migraciones Alembic- [Autenticación JWT](#-autenticación-jwt)│   ├── inventory_item.py

│   ├── setup/                   # Scripts de instalación

│   │   ├── populate_rbac_data.py  # Poblar roles y permisos├── tests/                  # Tests automatizados

│   │   └── generate_secret_keys.py

│   ├── maintenance/             # Mantenimiento de BD│   ├── integration/        # Tests RBAC (90 tests)- [Testing](#-testing)│   └── ...

│   │   └── check_database.py

│   └── testing/                 # Scripts de testing│   └── unit/               # Tests unitarios

│       └── test_all_endpoints_all_roles.py  # Test exhaustivo original

│├── scripts/                # Scripts auxiliares- [Seguridad](#-seguridad)│

├── docs/                        # 📚 Documentación completa

│   ├── INDEX.md                 # Índice de toda la documentación│   ├── setup/              # Scripts de instalación

│   ├── academic/                # Documentación académica

│   │   ├── METODOLOGIA_RAD.md│   ├── maintenance/        # Scripts de mantenimiento- [Deployment](#-deployment)├── use_cases/         # 💼 Application Logic (Handlers)

│   │   ├── ALCANCE_DEL_PROYECTO.md

│   │   ├── AUDITORIA_REQUISITOS.md│   ├── testing/            # Scripts de testing

│   │   └── requirements/

│   ├── business/                # Documentación de negocio│   └── database/           # Scripts de BD- [Estructura del Proyecto](#-estructura-del-proyecto)│   ├── user_handler.py

│   │   ├── REGLAS_DE_NEGOCIO.md

│   │   └── wireframes/├── docs/                   # Documentación completa

│   ├── architecture/            # Documentación de arquitectura

│   │   └── diagrams/            # Diagramas UML│   ├── INDEX.md            # 📋 Índice de documentación- [Scripts Útiles](#-scripts-útiles)│   ├── organization_handler.py

│   ├── technical/               # Documentación técnica

│   │   ├── api/│   ├── academic/           # Docs académicos (RAD, Alcance, etc.)

│   │   │   ├── EJEMPLOS_USO_API.md

│   │   │   └── MODELO_NEGOCIO_RBAC.md│   ├── business/           # Reglas de negocio, wireframes- [Contribuir](#-contribuir)│   └── ...

│   │   └── guides/

│   │       ├── AUTHENTICATION_GUIDE.md│   ├── architecture/       # Diagramas UML

│   │       ├── TESTING_GUIDE.md

│   │       └── DEPLOYMENT.md│   └── technical/          # Guías técnicas, API docs- [FAQ](#-faq)│

│   └── summaries/               # Resúmenes ejecutivos

│├── run.py                  # Punto de entrada

├── .env                         # ⚙️ Variables de entorno (NO en git)

├── .env.example                 # Template de configuración├── requirements.txt        # Dependencias├── api/               # 🌐 REST Endpoints (Blueprints)

├── .gitignore                   # Archivos ignorados por git

├── pytest.ini                   # Configuración de pytest├── pytest.ini              # Configuración pytest

├── requirements.txt             # Dependencias Python

├── run.py                       # 🚀 Punto de entrada de la aplicación└── .env                    # Variables de entorno---│   ├── user_api.py

├── README.md                    # Este archivo

├── INDEX_INICIO.md              # Guía de inicio rápido```

└── REORGANIZACION_COMPLETADA.md # Detalle de reorganización

```│   ├── metrics_api.py



------



## 🏗️ Arquitectura: Clean Architecture## 🎯 Descripción│   ├── dashboard_api.py



### Flujo de Datos (3 Capas)## 🏗️ Arquitectura Clean (3 Capas)



```│   └── ...

HTTP Request

    ↓### Flujo de Datos

┌─────────────────────────────────────────┐

│  CAPA 3: API (Presentation Layer)      │**Multicont** es un sistema integral de gestión empresarial desarrollado con **Clean Architecture**, diseñado para empresas que necesitan control completo sobre:│

│  - Blueprints Flask                     │

│  - Validación de entrada (Marshmallow)  │```

│  - Manejo de errores HTTP               │

│  - Documentación Swagger                │HTTP Request → API Blueprint → Handler (Use Case) → Entity (Domain Model) → Database├── config.py          # ⚙️ Configuración

└─────────────────┬───────────────────────┘

                  ↓                    ↓              ↓                      ↓

┌─────────────────────────────────────────┐

│  CAPA 2: Use Cases (Business Logic)    │               Validación    Lógica Negocio        Lógica Dominio- 👥 **Gestión Organizacional**: Organizaciones, sucursales, empleados└── __init__.py        # 🏗️ Application Factory

│  - Handlers con lógica de negocio      │

│  - Transacciones de BD (db.session)    │```

│  - Validaciones de negocio             │

│  - Paginación y filtros                │- 📦 **Control de Inventario**: Productos, categorías, marcas, stock en tiempo real```

└─────────────────┬───────────────────────┘

                  ↓### 1️⃣ Entities (Domain Layer)

┌─────────────────────────────────────────┐

│  CAPA 1: Entities (Domain Models)      │**Ubicación**: `app/entities/`- 💰 **Ciclo de Ventas Completo**: Cotizaciones → Órdenes → Facturas

│  - Modelos SQLAlchemy (ORM)            │

│  - Lógica de dominio pura              │

│  - Relaciones entre entidades          │

│  - Métodos de negocio                  │- Modelos SQLAlchemy (hereda de `db.Model`)- 📊 **Analytics y Metas**: KPIs, métricas de ventas, metas por empleado/sucursal## 🔧 Instalación

└─────────────────┬───────────────────────┘

                  ↓- Lógica de dominio pura

              PostgreSQL

```- Método `to_dict()` para serialización- 🔐 **Seguridad Empresarial**: JWT, RBAC, auditoría de cambios



### Principios Implementados



- ✅ **Separación de responsabilidades**: Cada capa tiene un propósito claro**Ejemplo**:- 🌐 **API RESTful**: 24 endpoints documentados con Swagger### Prerrequisitos

- ✅ **Independencia de frameworks**: Lógica de negocio independiente de Flask

- ✅ **Testeable**: Cada capa se puede probar independientemente```python

- ✅ **DRY (Don't Repeat Yourself)**: BaseHandler elimina código duplicado

- ✅ **SOLID**: Principios de diseño orientado a objetosclass InventoryItem(db.Model):- Python 3.9+

- ✅ **Dependency Injection**: Handlers reciben dependencias

    __tablename__ = "inventory_item"

---

    id = db.Column(db.BigInteger, primary_key=True)### ¿Por qué Multicont?- PostgreSQL 12+

## 🔧 Requisitos del Sistema

    name = db.Column(db.String(200), nullable=False)

### Software Necesario

    quantity = db.Column(db.Integer, default=0)- pip

- **Python**: 3.10+ (recomendado: 3.13)

- **PostgreSQL**: 12+ (recomendado: 16+)    

- **pip**: 23.0+

- **Git**: 2.40+    def add_stock(self, amount):✅ **Clean Architecture** - Código mantenible y testeable  



### Dependencias Principales        self.quantity += amount



``````✅ **Seguridad Robusta** - JWT + bcrypt + RBAC  ### Setup

Flask==3.1.0

Flask-SQLAlchemy==3.1.1

Flask-Migrate==4.0.7

Flask-JWT-Extended==4.7.1### 2️⃣ Use Cases (Application Layer)✅ **Escalable** - PostgreSQL + SQLAlchemy ORM  

Flask-CORS==5.0.0

flask-marshmallow==1.2.1**Ubicación**: `app/use_cases/`

marshmallow-sqlalchemy==1.1.0

psycopg2-binary==2.9.10✅ **Documentación Auto-generada** - Swagger UI incluido  1. **Clonar repositorio**

bcrypt==4.2.1

flasgger==0.9.7.1- Lógica de aplicación y casos de uso

pytest==8.3.3

pytest-cov==6.0.0- Interacción con `db.session`✅ **Listo para Producción** - Migraciones, logs, error handling  ```bash

requests==2.32.3

python-dotenv==1.0.1- Métodos estándar: `create()`, `get()`, `list_all()`, `update()`, `delete()`

```

git clone https://github.com/wilk-17/app-multicont.git

---

**Ejemplo**:

## 🚀 Instalación

```python---cd app-multicont

### 1. Clonar el Repositorio

class InventoryItemHandler(BaseHandler):

```bash

git clone https://github.com/wilk-17/app-multicont.git    model = InventoryItem```

cd app-multicont

```    



### 2. Crear Entorno Virtual    def add_stock(self, id, amount):## ✨ Características



**Windows:**        item = self.get(id)

```powershell

python -m venv .venv        item.add_stock(amount)2. **Crear entorno virtual**

.venv\Scripts\activate

```        db.session.commit()



**Linux/Mac:**        return item### Backend API```bash

```bash

python3 -m venv .venv```

source .venv/bin/activate

```python -m venv venv



### 3. Instalar Dependencias### 3️⃣ API (Presentation Layer)



```bash**Ubicación**: `app/api/`| Módulo | Funcionalidades |

pip install -r requirements.txt

```



### 4. Configurar PostgreSQL- Flask Blueprints con rutas RESTful|--------|----------------|# Windows



Crear una base de datos en PostgreSQL:- Parseo de request/response



```sql- Documentación Swagger| **Autenticación** | Login JWT, refresh tokens, roles (ADMIN/MANAGER/SALES) |venv\Scripts\activate

CREATE DATABASE multicont;

CREATE USER multicont_user WITH PASSWORD 'tu_password_seguro';

GRANT ALL PRIVILEGES ON DATABASE multicont TO multicont_user;

```**Rutas estándar**:| **Organizaciones** | Multi-organización, sucursales, jerarquías |



---- `GET /api/{resource}/` - Listar con paginación



## ⚙️ Configuración- `GET /api/{resource}/<int:id>` - Obtener por ID| **Empleados** | Gestión de personal, asignación de items |# Linux/Mac



### 1. Crear archivo `.env`- `POST /api/{resource}/` - Crear



Copiar el template y editar:- `PUT /api/{resource}/<int:id>` - Actualizar| **Inventario** | Stock en tiempo real, alertas de bajo stock, categorías |source venv/bin/activate



```bash- `DELETE /api/{resource}/<int:id>` - Eliminar

cp .env.example .env

```| **Cotizaciones** | Creación, líneas de items, conversión a órdenes |```



### 2. Editar `.env` con tus credenciales---



```env| **Órdenes de Venta** | Gestión completa, reducción automática de stock |

# Base de Datos

DATABASE_URL=postgresql+psycopg2://multicont_user:tu_password@localhost:5432/multicont## 🚀 Instalación y Setup



# JWT| **Facturación** | Generación de facturas, items facturados |3. **Instalar dependencias**

SECRET_KEY=tu_clave_secreta_muy_segura_aqui

JWT_SECRET_KEY=otra_clave_jwt_diferente_aqui### Requisitos Previos



# Flask| **Metas de Ventas** | Metas mensuales/trimestrales/anuales, tracking |```bash

FLASK_APP=run.py

FLASK_ENV=development- Python 3.10+



# Otros- PostgreSQL 12+| **Analytics** | Dashboard con métricas, reportes de ventas |pip install -r requirements.txt

SQLALCHEMY_TRACK_MODIFICATIONS=False

```- pip



⚠️ **IMPORTANTE**: Nunca subir `.env` a git. Está en `.gitignore`.- virtualenv```



---



## 🗄️ Base de Datos### Paso 1: Clonar el Repositorio### Seguridad Implementada



### Estructura de Tablas (23 entidades)



``````bash4. **Configurar variables de entorno**

users                    # Usuarios del sistema (RBAC)

roles                    # Roles (ADMIN, MANAGER, SALES)git clone https://github.com/wilk-17/app-multicont.git

permissions              # Permisos granulares

organizations            # Organizaciones/empresascd app-multicont- 🔒 **Password Hashing**: Bcrypt con 12 rounds

branches                 # Sucursales

persons                  # Personas (base para empleados/clientes)```

employees                # Empleados

states                   # Estados/departamentos- 🔒 **JWT Authentication**: Tokens con expiración configurableCrear archivo `.env` en la raíz:

cities                   # Ciudades

item_categories          # Categorías de items### Paso 2: Crear Entorno Virtual

item_brands              # Marcas de items

inventory_items          # Items de inventario- 🔒 **RBAC**: Control de acceso basado en roles```env

assignments              # Asignaciones de items a empleados

quotes                   # Cotizaciones```bash

quotation_lines          # Líneas de cotización

sales_orders             # Órdenes de venta# Windows- 🔒 **Secrets Management**: Variables de entorno (.env)DATABASE_URL=postgresql+psycopg2://postgres:tu_password@localhost:5432/nombre_db

sales_order_items        # Items de órdenes

invoices                 # Facturaspython -m venv .venv

invoice_items            # Items de facturas

sales_goals              # Metas de ventas.venv\Scripts\activate- 🔒 **Input Validation**: Esquemas Marshmallow (Fase 3)SECRET_KEY=tu-secret-key-aqui

quote_items              # Items de cotización (legacy)

user_roles               # Tabla pivote user-role (legacy)

```

# Linux/Mac- 🔒 **Rate Limiting**: Protección contra fuerza bruta (Fase 5)FLASK_ENV=development

### Migraciones

python3 -m venv .venv

#### Inicializar migraciones (solo si no existe `/migrations`)

source .venv/bin/activate- 🔒 **CORS**: Configurado para frontend Angular```

```bash

flask db init```

```



#### Aplicar migraciones existentes

### Paso 3: Instalar Dependencias

```bash

flask db upgrade### API Features5. **Inicializar base de datos**

```

```bash

#### Crear nueva migración (después de cambios en entities/)

pip install -r requirements.txt```bash

```bash

flask db migrate -m "Descripción del cambio"```

flask db upgrade

```- ✅ Paginación en todos los listados (`?page=1&per_page=10`)# Crear migraciones (si no existen)



#### Revertir última migración### Paso 4: Configurar Base de Datos



```bash- ✅ Filtros por status y fechasflask db init

flask db downgrade

```Crear archivo `.env` en la raíz:



### Poblar Datos Iniciales (RBAC)- ✅ Respuestas JSON estandarizadas



```bash```env

python scripts/setup/populate_rbac_data.py

```DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/multicont- ✅ Códigos HTTP apropiados (200, 201, 400, 401, 403, 404, 500)# Generar migración inicial



**Esto crea**:SECRET_KEY=tu-secret-key-aqui

- 3 roles (ADMIN, MANAGER, SALES)

- 15+ permisosJWT_SECRET_KEY=tu-jwt-secret-aqui- ✅ Swagger UI interactivo en `/api/docs/`flask db migrate -m "Initial migration"

- 3 usuarios de prueba:

  - `admin` / `admin123` (ADMIN)FLASK_ENV=development

  - `manager` / `manager123` (MANAGER)

  - `sales` / `sales123` (SALES)DEBUG=True- ✅ Error handling robusto



---```



## 🏃 Ejecución- ✅ Logging de operaciones# Aplicar migraciones



### Iniciar el ServidorO generar claves automáticamente:



```bashflask db upgrade

python run.py

``````bash



**Output esperado:**python scripts/setup/generate_secret_keys.py---```

```

 * Running on http://127.0.0.1:5000```

 * Debug mode: on

```



### Verificar que funciona### Paso 5: Crear Base de Datos



**Swagger UI** (Documentación Interactiva):## 🏗️ Arquitectura6. **Poblar base de datos con dataset completo** (OPCIONAL)

```

http://127.0.0.1:5000/api/docs/```bash

```

# Crear BD en PostgreSQL```bash

**Endpoint de prueba**:

```bashpsql -U postgres

curl http://127.0.0.1:5000/api/auth/validate

```CREATE DATABASE multicont;### Clean Architecture (3 Capas)python populate_database.py



---\q



## 🧪 Testing``````



### Tests RBAC (Recomendado)



#### Test Exhaustivo Interactivo (123 endpoints × 3 roles = 369 tests)### Paso 6: Aplicar Migraciones```



```bash

python tests/integration/test_rbac_exhaustive_interactive.py

``````bash┌─────────────────────────────────────────────────────────┐Esto crea:



**Output esperado:**flask db upgrade

```

✓ ADMIN    - 123/123 tests pasados (100.0%)```│                   PRESENTATION LAYER                     │- 5 Estados y 20 Ciudades

✓ MANAGER  - 123/123 tests pasados (100.0%)

✓ SALES    - 123/123 tests pasados (100.0%)

────────────────────────────────────────────

TOTAL GLOBAL - 369/369 tests pasados (100.0%)Este comando crea 23 tablas:│              API Endpoints (Flask Blueprints)            │- 7 Organizaciones y 5 Sucursales



🎉 ¡PERFECTO! Todos los tests pasaron (100%)- user, role, permission, user_role

```

- organization, branch, employee, assignment│  ┌──────────┬──────────┬──────────┬──────────────────┐  │- 15 Empleados y 10 Usuarios

#### Test RBAC Simple (90 tests)

- inventory_item, item_category, brand

```bash

python tests/integration/test_rbac_simple.py- quote, quotation_line, sales_order, sales_order_item, invoice, invoice_item│  │  Auth    │ Quotes   │ Invoices │  Analytics       │  │- 6 Marcas y 60 Items de inventario

```

- person, city, state

### Tests con pytest

│  │   API    │   API    │   API    │  24 APIs total   │  │- 12 Cotizaciones y 10 Facturas ($140M facturados)

```bash

# Todos los tests### Paso 7: Poblar Datos de Prueba (Opcional)

pytest

│  └──────────┴──────────┴──────────┴──────────────────┘  │- 18 Metas de ventas retroactivas

# Con verbosidad

pytest -v```bash



# Con coveragepython scripts/setup/populate_rbac_data.py│                           ↓                              │

pytest --cov=app tests/

```

# Test específico

pytest tests/unit/test_assignment_tracking.py -v├─────────────────────────────────────────────────────────┤7. **Verificar datos poblados** (OPCIONAL)

```

Crea:

### Scripts de Testing Auxiliares

- 8 usuarios con roles RBAC (ana, bruno, carla, diego, elena, felipe, gloria, hugo)│                  APPLICATION LAYER                       │```bash

```bash

# Test exhaustivo original (123 endpoints)- 1 organización con 1 sucursal

python scripts/testing/test_all_endpoints_all_roles.py

```- 8 empleados│           Use Cases / Business Logic (Handlers)          │python verify_data.py



---- 5 marcas y 8 items de inventario



## 🔐 Autenticación y RBAC- 1 Quote, 1 SalesOrder, 1 Invoice│  ┌──────────┬──────────┬──────────┬──────────────────┐  │```



### Sistema de Roles- 4 Permissions



| Rol       | Permisos                                      | Color   |│  │  Quote   │ Invoice  │  Sales   │   Inventory      │  │

|-----------|-----------------------------------------------|---------|

| **ADMIN** | Acceso total (CRUD completo en todos los recursos) | 🔴 Rojo |### Paso 8: Ejecutar Servidor

| **MANAGER** | CRUD en mayoría de recursos (excepto usuarios/roles) | 🟡 Amarillo |

| **SALES** | Lectura general + CRUD en cotizaciones         | 🟢 Verde |│  │ Handler  │ Handler  │ Handler  │  22 Handlers     │  │8. **Crear metas retroactivas para análisis** (OPCIONAL)



### Flujo de Autenticación```bash



#### 1. Login (Obtener Token JWT)python run.py│  └──────────┴──────────┴──────────┴──────────────────┘  │```bash



```bash```

curl -X POST http://127.0.0.1:5000/api/auth/login \

  -H "Content-Type: application/json" \│                           ↓                              │python create_retroactive_goals.py

  -d '{

    "username": "admin",Servidor corriendo en: **http://127.0.0.1:5000**  

    "password": "admin123"

  }'Swagger UI: **http://127.0.0.1:5000/api/docs/**├─────────────────────────────────────────────────────────┤```

```



**Respuesta:**

```json---│                    DOMAIN LAYER                          │

{

  "success": true,

  "data": {

    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",## 🧪 Testing│         Entities (Domain Models + Business Logic)        │9. **Ejecutar aplicación**

    "user": {

      "id": 1,

      "username": "admin",

      "role": "ADMIN"### Ejecutar Tests RBAC│  ┌──────────┬──────────┬──────────┬──────────────────┐  │```bash

    }

  }

}

``````bash│  │  Quote   │ Invoice  │  Sales   │   Employee       │  │python run.py



#### 2. Usar Token en Requestspython tests/integration/test_rbac_simple.py



```bash```│  │  Entity  │  Entity  │  Order   │  22 Entities     │  │```

curl -X GET http://127.0.0.1:5000/api/users/ \

  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

```

**Resultado esperado**: `90/90 tests passed (100.0%)`│  └──────────┴──────────┴──────────┴──────────────────┘  │

#### 3. Validar Token



```bash

curl -X GET http://127.0.0.1:5000/api/auth/validate \### Ejecutar Tests Unitarios│                           ↓                              │La API estará disponible en: `http://127.0.0.1:5000`

  -H "Authorization: Bearer TU_TOKEN_AQUI"

```



#### 4. Logout```bash├─────────────────────────────────────────────────────────┤



```bashpytest

curl -X POST http://127.0.0.1:5000/api/auth/logout \

  -H "Authorization: Bearer TU_TOKEN_AQUI"```│            DATABASE (PostgreSQL + SQLAlchemy)            │## 📚 Documentación API

```



### Matriz de Permisos (Resumen)

### Tests con Coverage└─────────────────────────────────────────────────────────┘

| Recurso            | ADMIN | MANAGER | SALES |

|--------------------|-------|---------|-------|

| **Usuarios**       | CRUD  | R       | R     |

| **Roles**          | CRUD  | R       | R     |```bash```### Swagger UI

| **Organizaciones** | CRUD  | CRU     | R     |

| **Sucursales**     | CRUD  | CRU     | R     |pytest --cov=app tests/

| **Empleados**      | CRUD  | CRU     | R     |

| **Inventario**     | CRUD  | CRU     | R     |```Acceder a: `http://127.0.0.1:5000/api/docs/`

| **Asignaciones**   | CRUD  | CRU     | R     |

| **Cotizaciones**   | CRUD  | CRU     | CRUD  |

| **Órdenes**        | CRUD  | CR      | -     |

| **Facturas**       | CRUD  | CR      | -     |### Verificar Setup### Flujo de Request

| **Analytics**      | R     | R       | -     |



**Leyenda**: C=Create, R=Read, U=Update, D=Delete

```bashDocumentación interactiva con todos los endpoints, schemas y posibilidad de probar directamente.

---

python scripts/setup/check_setup.py

## 🌐 Endpoints de la API

``````

### Resumen por Categoría (123 endpoints)



#### 🔐 Autenticación (4 endpoints)

- `POST /api/auth/login` - Login con username/password---1. HTTP Request → 2. API Blueprint → 3. Handler (Use Case) → 4. Entity (Domain) → 5. Database### Endpoints Principales

- `GET /api/auth/validate` - Validar token JWT

- `POST /api/auth/logout` - Cerrar sesión

- `GET /api/auth/me` - Usuario actual

## 🔐 Autenticación y RBAC                        ↓                    ↓                        ↓

#### 👥 Gestión de Usuarios (5 endpoints)

- `GET /api/users/` - Listar usuarios (paginado)

- `GET /api/users/<id>` - Obtener usuario

- `POST /api/users/` - Crear usuario (ADMIN)### Login                   Validación         Lógica Negocio           Lógica Dominio#### 👤 Usuarios

- `PUT /api/users/<id>` - Actualizar usuario (ADMIN)

- `DELETE /api/users/<id>` - Eliminar usuario (ADMIN)



#### 🎭 Roles y Permisos (10 endpoints)```bash                   - `GET /api/users/?page=1&per_page=10` - Listar usuarios

- `GET /api/roles/` - Listar roles

- `POST /api/roles/` - Crear rol (ADMIN)curl -X POST http://127.0.0.1:5000/api/auth/login \

- `GET /api/permisos/` - Listar permisos

- `POST /api/permisos/` - Crear permiso (ADMIN)  -H "Content-Type: application/json" \← 6. JSON Response ← 7. to_dict() ← 8. Commit ← 9. Save- `GET /api/users/<id>` - Obtener usuario

- ... (CRUD completo)

  -d '{"username": "ana", "password": "password123"}'

#### 🏢 Organizaciones (5 endpoints)

- `GET /api/organizaciones/` - Listar organizaciones``````- `POST /api/users/` - Crear usuario

- `POST /api/organizaciones/` - Crear organización (ADMIN/MANAGER)

- ... (CRUD completo)



#### 📍 Sucursales (5 endpoints)**Response**:- `PUT /api/users/<id>/activate` - Activar usuario

- `GET /api/sucursales/` - Listar sucursales

- `POST /api/sucursales/` - Crear sucursal (ADMIN/MANAGER)```json

- ... (CRUD completo)

{### Principios Aplicados- `GET /api/users/statistics` - Estadísticas de usuarios

#### 👤 Personas y Empleados (10 endpoints)

- `GET /api/personas/` - Listar personas  "success": true,

- `GET /api/empleados/` - Listar empleados

- `POST /api/empleados/` - Crear empleado (ADMIN/MANAGER)  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",

- ... (CRUD completo)

  "user": {

#### 📦 Inventario (15 endpoints)

- `GET /api/inventory_items/` - Listar items    "id": "1",- ✅ **Separation of Concerns**: Cada capa tiene responsabilidad única#### 🏢 Organizaciones

- `POST /api/inventory_items/` - Crear item (ADMIN/MANAGER)

- `GET /api/categorías/` - Listar categorías    "username": "ana",

- `GET /api/marcas/` - Listar marcas

- ... (CRUD completo)    "role": "ADMIN"- ✅ **Dependency Inversion**: Capas externas dependen de las internas- `GET /api/organizations/` - Listar organizaciones



#### 🔖 Asignaciones (8 endpoints)  }

- `GET /api/asignaciones/` - Listar asignaciones

- `GET /api/asignaciones/employee/<id>/history` - Historial de empleado}- ✅ **Single Responsibility**: Cada clase/función hace una cosa- `POST /api/organizations/` - Crear organización

- `POST /api/asignaciones/` - Crear asignación (ADMIN/MANAGER)

- `PUT /api/asignaciones/<id>/return` - Marcar como devuelta```

- `PUT /api/asignaciones/<id>/lost` - Reportar como perdida

- ... (CRUD completo)- ✅ **DRY (Don't Repeat Yourself)**: Código reutilizable- `PUT /api/organizations/<id>` - Actualizar



#### 📋 Cotizaciones (15 endpoints)### Usar Token

- `GET /api/quotes/` - Listar cotizaciones

- `POST /api/quotes/` - Crear cotización (TODOS)- ✅ **SOLID Principles**: Código mantenible y extensible- `DELETE /api/organizations/<id>` - Eliminar

- `GET /api/items de cotización/` - Items de cotización

- `GET /api/líneas de cotización/` - Líneas de cotización```bash

- ... (CRUD completo)

curl -X GET http://127.0.0.1:5000/api/users/ \

#### 🛒 Órdenes de Venta (10 endpoints)

- `GET /api/sales_orders/` - Listar órdenes (ADMIN/MANAGER)  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

- `POST /api/sales_orders/` - Crear orden (ADMIN/MANAGER)

- `GET /api/items de orden/` - Items de orden```---#### 📦 Inventario

- ... (CRUD completo)



#### 🧾 Facturas (10 endpoints)

- `GET /api/invoices/` - Listar facturas (ADMIN/MANAGER)### Roles y Permisos- `GET /api/inventory_items/?status=active` - Items de inventario

- `POST /api/invoices/` - Crear factura (ADMIN/MANAGER)

- `GET /api/items de factura/` - Items de factura

- ... (CRUD completo)

| Rol      | Usuarios | Ventas | Inventario | Organizaciones |## 📦 Requisitos- `POST /api/inventory_items/` - Agregar item

#### 🎯 Metas de Ventas (5 endpoints)

- `GET /api/metas de ventas/` - Listar metas|----------|----------|--------|------------|----------------|

- `POST /api/metas de ventas/` - Crear meta (ADMIN/MANAGER)

- ... (CRUD completo)| ADMIN    | CRUD     | CRUD   | CRUD       | CRUD           |- `PUT /api/inventory_items/<id>` - Actualizar item



#### 📊 Analytics (7 endpoints - ADMIN/MANAGER)| MANAGER  | Read     | CRUD   | CRUD       | Read           |

- `GET /api/analytics/sales/summary` - Resumen de ventas

- `GET /api/analytics/invoicing/by_employee` - Facturación por empleado| SALES    | Read     | CRUD   | Read       | Read           |### Software Necesario

- `GET /api/analytics/invoicing/by_branch` - Facturación por sucursal

- `GET /api/analytics/invoicing/by_brand` - Facturación por marca| VIEWER   | Read     | Read   | Read       | Read           |

- `GET /api/analytics/quotes/by_brand` - Cotizaciones por marca

- `GET /api/analytics/goals/vs_actual` - Metas vs real#### 💰 Ventas

- `GET /api/analytics/top_performers` - Top performers

---

#### 📈 Métricas (5 endpoints)

- `GET /api/metrics/users` - Métricas de usuarios| Software | Versión Mínima | Recomendada |- `GET /api/quotes/` - Cotizaciones

- `GET /api/metrics/inventory` - Métricas de inventario

- `GET /api/metrics/sales` - Métricas de ventas## 📊 Endpoints Principales

- `GET /api/metrics/employees` - Métricas de empleados

- `GET /api/metrics/summary` - Resumen consolidado|----------|----------------|-------------|- `GET /api/sales_orders/` - Órdenes de venta



#### 📊 Dashboard (2 endpoints)### Autenticación

- `GET /api/dashboard/?period=month` - Dashboard principal

- `GET /api/dashboard/kpis` - KPIs del negocio- `POST /api/auth/login` - Login con JWT| **Python** | 3.10 | 3.11+ |- `GET /api/invoices/` - Facturas



### Ejemplos de Uso- `POST /api/auth/register` - Registro de usuario



#### Paginación- `GET /api/auth/me` - Perfil del usuario| **PostgreSQL** | 12 | 15+ |



Todos los endpoints de lista soportan paginación:



```bash### Gestión| **pip** | 21.0 | Latest |#### 🏷️ Marcas

GET /api/users/?page=1&per_page=10&status=active

```- `GET /api/users/` - Listar usuarios



**Respuesta:**- `GET /api/organizaciones/` - Listar organizaciones| **virtualenv** | - | Latest |- `GET /api/brands/` - Listar marcas

```json

{- `GET /api/sucursales/` - Listar sucursales

  "success": true,

  "data": {- `GET /api/empleados/` - Listar empleados- `POST /api/brands/` - Crear marca

    "items": [...],

    "total": 100,- `GET /api/inventory_items/` - Listar inventario

    "page": 1,

    "per_page": 10,### Dependencias Python Principales- `GET /api/brands/<id>` - Obtener marca

    "total_pages": 10

  }### Ventas

}

```- `GET /api/quotes/` - Listar cotizaciones- `GET /api/brands/search?name=Omron` - Buscar por nombre



#### Crear Organización- `GET /api/sales_orders/` - Listar órdenes de venta



```bash- `GET /api/invoices/` - Listar facturas```

curl -X POST http://127.0.0.1:5000/api/organizaciones/ \

  -H "Authorization: Bearer TU_TOKEN" \

  -H "Content-Type: application/json" \

  -d '{### AnalyticsFlask==3.1.0                  # Framework web#### 🎯 Metas de Ventas

    "historical_name": "Empresa ABC",

    "current_name": "ABC Corp"- `GET /api/metrics/summary` - Resumen de todas las métricas

  }'

```- `GET /api/metrics/sales` - Métricas de ventasFlask-SQLAlchemy==3.1.1       # ORM- `GET /api/sales_goals/` - Listar metas



#### Dashboard con Periodo- `GET /api/metrics/inventory` - Métricas de inventario



```bash- `GET /api/dashboard/?period=month` - Dashboard con KPIsFlask-Migrate==4.0.5          # Migraciones DB- `POST /api/sales_goals/` - Crear meta

curl "http://127.0.0.1:5000/api/dashboard/?period=month" \

  -H "Authorization: Bearer TU_TOKEN"

```

**Ver todos los endpoints**: http://127.0.0.1:5000/api/docs/Flask-JWT-Extended==4.7.1     # Autenticación JWT- `GET /api/sales_goals/current` - Metas actuales

**Periodos válidos**: `day`, `week`, `month`, `year`



---

---psycopg2-binary==2.9.9        # Driver PostgreSQL- `GET /api/sales_goals/by_employee/<id>` - Metas de empleado

## 📚 Documentación



### Documentación Interactiva

## 📝 Ejemplos de Usobcrypt==5.0.0                 # Password hashing- `GET /api/sales_goals/by_branch/<id>` - Metas de sucursal

**Swagger UI**: http://127.0.0.1:5000/api/docs/



- Probar todos los endpoints directamente desde el navegador

- Ver schemas de request/response### PaginaciónFlasgger==0.9.7.1             # Swagger UI

- Autenticación JWT integrada



### Documentación Completa

```bashpython-dotenv==1.0.0          # Variables de entorno#### 📊 Analytics (CORE FEATURE)

Ver [docs/INDEX.md](docs/INDEX.md) para el índice completo de documentación organizada por categorías:

curl "http://127.0.0.1:5000/api/users/?page=1&per_page=10&status=active"

- **📚 Académica**: Metodología RAD, Alcance, Requisitos

- **💼 Negocio**: Reglas de negocio, Wireframes```marshmallow==3.22.0           # Validación (Fase 3)- `GET /api/analytics/invoicing/by_employee` - Facturación por empleado

- **🏗️ Arquitectura**: Diagramas UML, Fases de implementación

- **🔧 Técnica**: Guías de API, Testing, Deployment

- **📊 Resúmenes**: Reportes ejecutivos, Análisis

**Response**:```- `GET /api/analytics/invoicing/by_branch` - Facturación por sucursal

### Guías Principales

```json

- [AUTHENTICATION_GUIDE.md](docs/technical/guides/AUTHENTICATION_GUIDE.md) - Guía de JWT y RBAC

- [TESTING_GUIDE.md](docs/technical/guides/TESTING_GUIDE.md) - Guía de testing{- `GET /api/analytics/invoicing/by_brand` - Facturación por marca

- [DEPLOYMENT.md](docs/technical/guides/DEPLOYMENT.md) - Guía de deployment

- [EJEMPLOS_USO_API.md](docs/technical/api/EJEMPLOS_USO_API.md) - Ejemplos con curl  "success": true,



---  "data": {Ver `requirements.txt` completo.- `GET /api/analytics/quotes/by_brand` - Cotizaciones por marca



## 🛠️ Scripts Auxiliares    "items": [...],



### Setup (Instalación)    "total": 100,- `GET /api/analytics/goals/vs_actual` - **Metas vs Ventas Reales** ⭐



```bash    "page": 1,

# Poblar roles, permisos y usuarios RBAC

python scripts/setup/populate_rbac_data.py    "per_page": 10,---- `GET /api/analytics/sales/summary` - Resumen consolidado



# Generar secret keys seguras    "total_pages": 10

python scripts/setup/generate_secret_keys.py

  }- `GET /api/analytics/top_performers` - Ranking de vendedores

# Verificar instalación

python scripts/setup/check_setup.py}

```

```## 🚀 Instalación Rápida

### Maintenance (Mantenimiento)



```bash

# Verificar estado de la base de datos### Crear Item de Inventario## 🧪 Testing

python scripts/maintenance/check_database.py

```



### Testing```bash### Método 1: Instalación Manual (Recomendado)



```bashcurl -X POST http://127.0.0.1:5000/api/inventory_items/ \

# Test exhaustivo original (123 endpoints × 3 roles)

python scripts/testing/test_all_endpoints_all_roles.py  -H "Authorization: Bearer TOKEN" \```bash

```

  -H "Content-Type: application/json" \

---

  -d '{```bash# Ejecutar todos los tests

## 🎓 Cumplimiento de Requisitos Académicos

    "name": "Laptop Dell XPS 15",

### Metodología RAD

    "quantity": 10,# 1. Clonar repositoriopytest

✅ **Fase 1 - Requerimientos**: Ver [REQUERIMIENTOS_FUNCIONALES.md](docs/academic/requirements/REQUERIMIENTOS_FUNCIONALES.md)  

✅ **Fase 2 - Planificación**: Ver [METODOLOGIA_RAD.md](docs/academic/METODOLOGIA_RAD.md)      "unit_price": 3500000,

✅ **Fase 3 - Ejecución**: Código fuente en `app/` (Clean Architecture)  

✅ **Fase 4 - Testing**: 369 tests RBAC (100% pasando)      "brand_id": 1,git clone https://github.com/wilk-17/app-multicont.git



### Auditoría de Requisitos    "category_id": 1



Ver [AUDITORIA_REQUISITOS.md](docs/academic/AUDITORIA_REQUISITOS.md) para cumplimiento detallado:  }'cd app-multicont# Con coverage



- ✅ **ORM**: 22 entidades con SQLAlchemy (100%)```

- ✅ **Controladores**: 20 handlers validados (100%)

- ✅ **Interfaces CRUD**: 24 APIs RESTful (100%)pytest --cov=app

- ✅ **Paginación**: Todos los endpoints de lista (100%)

- ✅ **Funciones Principales**: Wireframes + Modelo de Negocio (100%)### Dashboard de Métricas

- ✅ **Reportes**: Dashboard + Analytics + Métricas (100%)

- ✅ **Configuración**: .env + config.py (100%)# 2. Crear entorno virtual

- ✅ **Usuarios-Permisos**: RBAC + JWT + bcrypt (100%)

- ✅ **Llaveros**: Secret keys + JWT keys (100%)```bash



**Cumplimiento Total: 100%** 🎉curl "http://127.0.0.1:5000/api/dashboard/?period=month" \python -m venv venv# Verbose



---  -H "Authorization: Bearer TOKEN"



## 👥 Equipo de Desarrollo```pytest -v



| Nombre          | Rol                              | Responsabilidades                  |

|-----------------|----------------------------------|------------------------------------|

| **Wilker**      | Backend Developer & DB Architect | Clean Architecture, Base de Datos  |---# Windows```

| **Daniel**      | Backend Developer & Test Engineer| Testing, RBAC, Validaciones        |



### Contribuciones

## 📚 Documentación Completavenv\Scripts\activate

- **Wilker**: 

  - Diseño de Clean Architecture (3 capas)

  - Implementación de 22 entidades ORM

  - Migraciones Alembic (23 tablas)**Ver índice completo**: [docs/INDEX.md](docs/INDEX.md)## 🏗️ Arquitectura

  - BaseHandler con DRY pattern

  - Documentación técnica



- **Daniel**:### Para Desarrolladores# Linux/Mac

  - Sistema RBAC completo (JWT + bcrypt)

  - 369 tests automatizados (100% passing)- [AUTHENTICATION_GUIDE.md](docs/technical/guides/AUTHENTICATION_GUIDE.md) - Guía de autenticación JWT

  - Schemas Marshmallow (validación)

  - Analytics y Dashboard- [TESTING_GUIDE.md](docs/technical/guides/TESTING_GUIDE.md) - Guía de testingsource venv/bin/activate### Clean Architecture (3 Capas)

  - Guías de testing

- [EJEMPLOS_USO_API.md](docs/technical/api/EJEMPLOS_USO_API.md) - Ejemplos de uso

---



## 📊 Estadísticas del Proyecto

### Para Evaluadores Académicos

- **Líneas de código Python**: ~15,000+

- **Entidades de dominio**: 22- [AUDITORIA_REQUISITOS.md](docs/academic/AUDITORIA_REQUISITOS.md) - ✅ **Cumplimiento de requisitos**# 3. Instalar dependencias```

- **Handlers de negocio**: 20

- **APIs RESTful**: 24 blueprints- [METODOLOGIA_RAD.md](docs/academic/METODOLOGIA_RAD.md) - Evidencia de metodología RAD

- **Endpoints totales**: 123

- **Tests automatizados**: 369 (100% passing)- [ALCANCE_DEL_PROYECTO.md](docs/academic/ALCANCE_DEL_PROYECTO.md) - Alcance del proyectopip install -r requirements.txt┌─────────────────────────────────────────┐

- **Migraciones**: 5 aplicadas (23 tablas)

- **Documentación**: 50+ archivos organizados- [PLANTEAMIENTO_PROYECTO.docx](docs/PLANTEAMIENTO_PROYECTO.docx) - Documento académico APA 7

- **Archivos legacy eliminados**: 54 (85 MB liberados)

│         API Layer (Blueprints)          │  ← Flask Routes

---

### Para Product Owners

## 🔗 Enlaces Útiles

- [REGLAS_DE_NEGOCIO.md](docs/business/REGLAS_DE_NEGOCIO.md) - Reglas de negocio# 4. Configurar PostgreSQL│  - Parsing requests                     │

- **Repositorio**: https://github.com/wilk-17/app-multicont

- **Documentación completa**: [docs/INDEX.md](docs/INDEX.md)- [WIREFRAMES.md](docs/business/wireframes/WIREFRAMES.md) - Wireframes del sistema

- **Guía de inicio**: [INDEX_INICIO.md](INDEX_INICIO.md)

- **Auditoría de requisitos**: [docs/academic/AUDITORIA_REQUISITOS.md](docs/academic/AUDITORIA_REQUISITOS.md)- [DIAGRAMAS.md](docs/architecture/diagrams/DIAGRAMAS.md) - Diagramas UMLpsql -U postgres│  - JSON responses                       │



---



## 📝 Changelog---CREATE DATABASE multicont_db;│  - Swagger docs                         │



### [2.0.0] - 2025-10-21



#### ✨ Agregado## 🛠️ Scripts Auxiliares\q└──────────────┬──────────────────────────┘

- Test exhaustivo interactivo (369 tests con 100% éxito)

- Sistema RBAC completo validado en 123 endpoints

- README completamente renovado y actualizado

### Setup               │

#### 🔧 Mejorado

- Limpieza de 54 archivos legacy (85 MB liberados)- `scripts/setup/check_setup.py` - Verificar configuración del proyecto

- Estructura de proyecto optimizada

- Documentación completamente reorganizada- `scripts/setup/generate_secret_keys.py` - Generar claves secretas# 5. Generar claves secretas┌──────────────▼──────────────────────────┐



#### 🗑️ Eliminado- `scripts/setup/populate_rbac_data.py` - Poblar datos de prueba RBAC

- `app/models/` (reemplazado por `app/entities/`)

- `app/routes.py` (reemplazado por `app/api/`)python scripts/generate_secret_keys.py│      Use Cases Layer (Handlers)         │  ← Business Logic

- Scripts de testing obsoletos (11 archivos)

- Documentos MD legacy en raíz (7 archivos)### Mantenimiento

- Archivos temporales (6 archivos .txt)

- Scripts de mantenimiento legacy (4 archivos)- `scripts/maintenance/check_database.py` - Verificar estado de la base de datos│  - CRUD operations                      │

- Tests legacy (2 archivos)

- 15 scripts Python obsoletos en raíz



### [1.0.0] - 2025-10-19### Testing# 6. Configurar .env│  - Validation                           │



#### ✨ Lanzamiento Inicial- `scripts/testing/verification/verify_rbac.py` - Verificar compliance RBAC (80 endpoints)

- Clean Architecture implementada

- 22 entidades de dominiocopy .env.example .env│  - Transactions                         │

- Sistema RBAC básico

- Swagger UI integrado---



---# Editar .env con tus configuraciones y claves generadas│  - Pagination                           │



## 📄 Licencia## 🎓 Cumplimiento de Requisitos Académicos



Este proyecto es de uso académico.  └──────────────┬──────────────────────────┘

**Prohibida su distribución o uso comercial sin autorización.**

✅ **Metodología RAD**: Requerimientos + Planificación + Ejecución + Testing  

---

✅ **ORM**: SQLAlchemy con 23 modelos  # 7. Ejecutar migraciones               │

## 🙏 Agradecimientos

✅ **Controladores**: 20 handlers validados (100% RBAC)  

- **Flask Community** - Por la excelente documentación

- **SQLAlchemy** - Por el ORM robusto✅ **Interfaces CRUD**: 20 APIs con Swagger UI  flask db upgrade┌──────────────▼──────────────────────────┐

- **pytest** - Por el framework de testing

- **Marshmallow** - Por la validación de datos✅ **Paginación**: En todos los endpoints de listado  



---✅ **Funciones Principales**: Wireframes + Modelo de Negocio  │       Entities Layer (Models)           │  ← Domain Logic



**Desarrollado con ❤️ por el equipo Wilker & Daniel**  ✅ **Reportes**: Dashboard + Métricas + KPIs  

**2025 © Todos los derechos reservados**

✅ **Configuración**: .env + config.py  # 8. Poblar base de datos (opcional)│  - SQLAlchemy models                    │

✅ **Usuarios-Permisos**: RBAC completo (90/90 tests)  

⚠️ **Llaveros**: Secret keys (70% - falta vault producción)python scripts/database/populate_db_validated.py│  - Domain methods                       │



**Cumplimiento Global**: **97%** (9/9 componentes implementados)│  - Relationships                        │



Ver detalles: [docs/academic/AUDITORIA_REQUISITOS.md](docs/academic/AUDITORIA_REQUISITOS.md)# 9. Ejecutar aplicación└─────────────────────────────────────────┘



---python run.py```



## 🤝 Equipo de Desarrollo



- **Wilker** - Backend Developer & Database Architect# 10. Abrir Swagger UI### Flujo de Datos

- **Daniel** - Backend Developer & Testing Engineer

# http://127.0.0.1:5000/api/docs/```

---

```HTTP Request → API → Handler → Entity → Database

## 📄 Licencia

                ↓        ↓         ↓

Este proyecto es de uso académico.

### Método 2: Script Automatizado (Windows)            Routing  Business  Domain

---

                    Logic     Logic

## 🔗 Enlaces Útiles

```powershell```

- **Swagger UI**: http://127.0.0.1:5000/api/docs/

- **Repositorio**: https://github.com/wilk-17/app-multicont# Ejecutar script de setup

- **Documentación**: [docs/INDEX.md](docs/INDEX.md)

.\start_server.bat## 📈 Modelos de Negocio

---

```

**Última actualización**: 19 de Octubre de 2025  

**Versión**: 1.0.0  ### Flujo de Ventas

**Estado**: ✅ Producción

### Verificar Instalación```

Quote (Cotización)

```bash    ↓

# Test de conexión a BDQuotationLine (Líneas de cotización)

python scripts/check_setup.py    ↓

SalesOrder (Orden de venta)

# Test de API    ↓

curl http://127.0.0.1:5000/Invoice (Factura)

```    ↓

InvoiceItem (Items facturados)

Deberías ver:```

```json

{### Estructura Organizacional

  "message": "API Multicont - Clean Architecture",```

  "version": "2.0.0",Organization (Organización)

  "documentation": "/api/docs/"    ↓

}Branch (Sucursal)

```    ↓

Employee (Empleado)

---    ↓

Assignment (Asignación de items)

## ⚙️ Configuración```



### Variables de Entorno (.env)## 🔑 Convenciones de Código



**Obligatorias** (sin estas la app no inicia):### Responses JSON Estándar

```json

```bash// Éxito

# Base de datos{

DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/multicont_db  "success": true,

  "data": {...},

# Claves secretas (generar con scripts/generate_secret_keys.py)  "message": "Operación exitosa"

SECRET_KEY=tu-secret-key-generada}

JWT_SECRET_KEY=tu-jwt-secret-generada

```// Error

{

**Opcionales** (con defaults):  "success": false,

  "error": "Descripción del error"

```bash}

# Ambiente

FLASK_ENV=development                # development | production | testing// Con paginación

FLASK_DEBUG=1                        # 1 (True) | 0 (False){

  "success": true,

# JWT  "data": {

JWT_ACCESS_TOKEN_HOURS=24            # Duración token acceso (horas)    "items": [...],

JWT_REFRESH_TOKEN_DAYS=30            # Duración refresh token (días)    "total": 100,

    "page": 1,

# CORS (Frontend Angular)    "per_page": 10,

FRONTEND_URL=http://localhost:4200    "total_pages": 10

CORS_ORIGINS=http://localhost:4200,http://localhost:3000  }

}

# Logging```

SQLALCHEMY_ECHO=False                # Mostrar queries SQL en consola

LOG_LEVEL=INFO                       # DEBUG | INFO | WARNING | ERROR### Paginación

```Todos los endpoints de lista soportan:

- `?page=1` - Número de página

### Generar Claves Secretas Seguras- `?per_page=10` - Items por página

- `?status=active` - Filtro por estado

```bash

# Método 1: Script incluido## 🛠️ Desarrollo

python scripts/generate_secret_keys.py

### Agregar Nuevo Modelo

# Método 2: Python directo

python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"1. Crear entity en `app/entities/`

python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"2. Crear handler en `app/use_cases/`

3. Crear API en `app/api/`

# Método 3: OpenSSL (Linux/Mac)4. Registrar en `app/__init__.py`

openssl rand -base64 325. Crear migración: `flask db migrate -m "Add Model"`

```6. Aplicar: `flask db upgrade`



### Configuración de PostgreSQLVer `.github/copilot-instructions.md` para guía completa.



```sql### Generar Handlers/APIs Automáticamente

-- Crear usuario y base de datos

CREATE USER multicont_user WITH PASSWORD 'tu_password_seguro';Usa el script generador:

CREATE DATABASE multicont_db OWNER multicont_user;```bash

GRANT ALL PRIVILEGES ON DATABASE multicont_db TO multicont_user;python generate_refactor_files.py

```

-- Verificar conexión

\c multicont_db## 📦 Dependencias Principales

\dt

```- Flask 2.3.3

- Flask-SQLAlchemy 3.0.5

---- Flask-Migrate 4.0.5

- PostgreSQL (psycopg2-binary)

## 🎮 Uso de la API- Flasgger (Swagger UI)



### 1. Acceder a Swagger UIVer `requirements.txt` para lista completa.



Abrir en navegador: **http://127.0.0.1:5000/api/docs/**## 🚧 Pendientes / TODOs



En Swagger UI puedes:- [ ] Implementar hash de passwords (bcrypt/werkzeug)

- 📖 Ver todos los endpoints disponibles- [ ] Agregar JWT authentication

- ▶️ Probar requests directamente- [ ] Sistema de permisos por roles

- 📋 Ver schemas de datos- [ ] Poblar InvoiceItems para análisis por marca

- 🔒 Autenticarte con JWT- [ ] Tests unitarios para todos los handlers

- 📥 Descargar especificación OpenAPI- [ ] Tests de integración para APIs

- [ ] Frontend Dashboard (Vue.js/React recomendado)

### 2. Login (Obtener Token JWT)- [ ] Docker y docker-compose

- [ ] CI/CD con GitHub Actions

**Endpoint**: `POST /api/auth/login`- [ ] Rate limiting en endpoints públicos



```bash## 📖 Documentación Adicional

curl -X POST http://127.0.0.1:5000/api/auth/login \

  -H "Content-Type: application/json" \- **RESUMEN_EJECUTIVO.md** - Estado del proyecto y dataset poblado

  -d '{- **POBLACION_BASE_DATOS_COMPLETA.md** - Guía completa de población

    "username": "admin",- **SISTEMA_METAS_VENTAS_COMPLETO.md** - Documentación técnica (600+ líneas)

    "password": "admin123"- **IMPLEMENTACION_COMPLETA.md** - Quick reference y checklist

  }'- **ANALISIS_CRUD_Y_RECOMENDACIONES_VISTAS.md** - Estrategia CRUD

```

## 🎯 Quick Start para Analytics

**Response**:

```json### 1. Poblar base de datos

{```bash

  "success": true,python populate_database.py

  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",python create_retroactive_goals.py

  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",```

  "user": {

    "id": "1",### 2. Iniciar servidor

    "username": "admin",```bash

    "role": "ADMIN",python run.py

    "permissions": ["READ_USERS", "WRITE_USERS", ...]```

  }

}### 3. Probar endpoint principal

``````bash

curl "http://127.0.0.1:5000/api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-04-01&end_date=2025-09-30"

### 3. Usar Token en Requests```



```bash### 4. Ver en Swagger UI

# Guardar token en variableAbrir: `http://127.0.0.1:5000/api/docs/`

TOKEN="tu-access-token-aqui"

Buscar sección **analytics** y probar endpoints interactivamente.

# Hacer request autenticado

curl -X GET http://127.0.0.1:5000/api/quotes/ \## 📊 Análisis Disponibles

  -H "Authorization: Bearer $TOKEN"

```### Metas vs Actual

Compara metas de ventas configuradas contra facturación real:

### 4. Ejemplo: Crear Cotización- **Porcentaje de cumplimiento** calculado automáticamente

- **Status dinámico**: exceeded (≥100%), on_track (80-99%), at_risk (50-79%), failed (<50%)

```bash- **Filtros**: Por período (monthly/quarterly/yearly), empleado o sucursal

curl -X POST http://127.0.0.1:5000/api/quotes/ \

  -H "Authorization: Bearer $TOKEN" \### Top Performers

  -H "Content-Type: application/json" \Ranking de vendedores por volumen de ventas:

  -d '{- Ordenado de mayor a menor facturación

    "customer_name": "Empresa ABC S.A.S.",- Incluye número de facturas y total vendido

    "date": "2025-10-19",- Filtrable por rango de fechas

    "employee_id": 1,

    "total": 2500000### Resumen de Ventas

  }'KPIs consolidados del negocio:

```- Total facturado y cotizado

- Número de facturas y cotizaciones

**Response**:- Ticket promedio

```json- Tasa de conversión (cotizaciones → facturas)

{

  "success": true,## 🏆 Dataset Completo Incluido

  "message": "Creado exitosamente",

  "data": {El sistema incluye un dataset realista de 6 meses:

    "id": "45",

    "customer_name": "Empresa ABC S.A.S.",- **Período**: Abril - Septiembre 2025

    "date": "2025-10-19",- **Total Facturado**: $140,040,000 COP

    "total": 2500000.0,- **Facturas**: 10 registros

    "employee_id": "1"- **Cotizaciones**: 12 registros

  }- **Empleados**: 15 distribuidos en 5 sucursales

}- **Marcas**: 6 (60 items de inventario)

```- **Metas**: 18 configuradas (13 mensuales + 5 trimestrales)



### 5. Listar con Paginación### Top 3 Vendedores

1. 🥇 Jorge Nieto: $39,350,000

```bash2. 🥈 Ana García: $30,200,000

curl -X GET "http://127.0.0.1:5000/api/quotes/?page=2&per_page=20" \3. 🥉 Gloria Vega: $19,300,000

  -H "Authorization: Bearer $TOKEN"

```### Métricas Clave

- Crecimiento Q2→Q3: +49.0%

**Response**:- Tasa de conversión: ~80%

```json- Ticket promedio: $14,004,000

{

  "success": true,## 📝 Licencia

  "data": {

    "items": [...],[Especificar licencia]

    "total": 150,

    "page": 2,## 👥 Contribuidores

    "per_page": 20,

    "total_pages": 8- [Tu nombre]

  }

}## 📞 Contacto

```

Para preguntas o sugerencias, contactar a [email]

### Usuarios de Prueba (después de poblar BD)

---

| Username | Password | Rol | Permisos |

|----------|----------|-----|----------|**Clean Architecture** inspirada en: Robert C. Martin (Uncle Bob) y Alistair Cockburn (Hexagonal Architecture)

| admin | admin123 | ADMIN | Todos |
| manager | manager123 | MANAGER | Gestión + Ventas |
| vendedor1 | vendedor123 | SALES | Cotizaciones + Lectura |

---

## 📚 Endpoints Principales

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Login y obtener tokens | No |
| POST | `/api/auth/refresh` | Renovar access token | Refresh Token |
| POST | `/api/auth/logout` | Cerrar sesión (blacklist) | JWT |

### Cotizaciones (Quotes)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/quotes/` | Listar cotizaciones | JWT |
| GET | `/api/quotes/<id>` | Obtener por ID | JWT |
| POST | `/api/quotes/` | Crear cotización | ADMIN, MANAGER, SALES |
| PUT | `/api/quotes/<id>` | Actualizar | ADMIN, MANAGER |
| DELETE | `/api/quotes/<id>` | Eliminar | ADMIN, MANAGER |

### Órdenes de Venta

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/sales-orders/` | Listar órdenes | JWT |
| POST | `/api/sales-orders/` | Crear orden | ADMIN, MANAGER |
| PUT | `/api/sales-orders/<id>` | Actualizar | ADMIN, MANAGER |
| DELETE | `/api/sales-orders/<id>` | Eliminar | ADMIN |

### Facturas (Invoices)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/invoices/` | Listar facturas | JWT |
| GET | `/api/invoices/<id>` | Obtener por ID | JWT |
| POST | `/api/invoices/` | Crear factura | ADMIN, MANAGER |
| PUT | `/api/invoices/<id>` | Actualizar | ADMIN, MANAGER |
| DELETE | `/api/invoices/<id>` | Eliminar | ADMIN |

### Inventario

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/inventory-items/` | Listar items | JWT |
| GET | `/api/inventory-items/<id>` | Obtener por ID | JWT |
| POST | `/api/inventory-items/` | Crear item | ADMIN, MANAGER |
| PUT | `/api/inventory-items/<id>` | Actualizar | ADMIN, MANAGER |
| DELETE | `/api/inventory-items/<id>` | Eliminar | ADMIN |

### Analytics

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/api/analytics/sales` | Métricas de ventas | JWT |
| GET | `/api/analytics/inventory` | Métricas de inventario | JWT |
| GET | `/api/analytics/employees` | Métricas de empleados | JWT |
| GET | `/api/analytics/dashboard?period=month` | Dashboard completo | JWT |

### Otros Módulos

- `/api/organizations/` - Gestión de organizaciones
- `/api/branches/` - Sucursales
- `/api/employees/` - Empleados
- `/api/users/` - Usuarios del sistema
- `/api/roles/` - Roles y permisos
- `/api/sales-goals/` - Metas de ventas
- `/api/brands/` - Marcas de productos
- `/api/item-categories/` - Categorías de items

**Total**: 24 blueprints API

---

## 🔐 Autenticación JWT

### Flujo de Autenticación

```
1. Usuario → POST /api/auth/login {username, password}
2. API valida credenciales con bcrypt
3. API genera access_token + refresh_token
4. Usuario recibe tokens + info del user
5. Usuario almacena tokens (localStorage/sessionStorage)
6. Usuario incluye token en requests: Authorization: Bearer {token}
7. API valida token en cada request con @jwt_required()
8. API verifica rol con @require_role('ADMIN')
9. Si token expira → usar refresh_token en /api/auth/refresh
```

### Estructura del Token JWT

```json
{
  "sub": 1,                    // User ID
  "role": "ADMIN",             // Rol del usuario
  "role_id": 1,                // ID del rol
  "permissions": [             // Permisos específicos
    "READ_USERS",
    "WRITE_USERS",
    "DELETE_USERS",
    ...
  ],
  "exp": 1729375200,           // Timestamp de expiración
  "iat": 1729288800            // Timestamp de emisión
}
```

### Decoradores de Autorización

```python
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role, require_permission

# Solo requiere autenticación
@jwt_required()
def protected_route():
    pass

# Requiere rol específico
@jwt_required()
@require_role('ADMIN')
def admin_only():
    pass

# Requiere uno de varios roles
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def admin_or_manager():
    pass

# Requiere permiso específico
@jwt_required()
@require_permission('WRITE_QUOTES')
def create_quote():
    pass
```

### Renovar Token (Refresh)

```bash
curl -X POST http://127.0.0.1:5000/api/auth/refresh \
  -H "Authorization: Bearer $REFRESH_TOKEN"
```

**Response**:
```json
{
  "success": true,
  "access_token": "nuevo-access-token..."
}
```

---

## 🧪 Testing

### Configurar Entorno de Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov pytest-flask

# Crear archivo pytest.ini (ya incluido)
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con verbose
pytest -v

# Con coverage
pytest --cov=app tests/

# Tests específicos
pytest tests/test_auth.py -v

# Generar reporte HTML
pytest --cov=app --cov-report=html tests/
# Abrir: htmlcov/index.html
```

### Escribir Tests (Ejemplo)

```python
# tests/test_api/test_quote_api.py
import pytest
from datetime import date

def test_create_quote_success(client, admin_token):
    """Test crear cotización exitosamente."""
    response = client.post('/api/quotes/', 
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'customer_name': 'Cliente Test',
            'date': date.today().isoformat(),
            'employee_id': 1,
            'total': 100000
        }
    )
    
    assert response.status_code == 201
    assert response.json['success'] == True
    assert 'id' in response.json['data']

def test_create_quote_without_auth(client):
    """Test crear cotización sin autenticación debe fallar."""
    response = client.post('/api/quotes/', json={})
    assert response.status_code == 401
```

### Coverage Objetivo

🎯 **Meta**: 80%+ de cobertura de código

---

## 🔒 Seguridad

### Medidas Implementadas

#### 1. Password Security
- ✅ Bcrypt hashing (12 rounds)
- ✅ Salt generado automáticamente
- ✅ Nunca se almacenan passwords en texto plano
- ✅ Verificación segura con timing attack protection

#### 2. JWT Authentication
- ✅ Tokens firmados con HS256
- ✅ Expiración configurable (24h access, 30d refresh)
- ✅ Claims personalizados (role, permissions)
- ✅ Token blacklist para logout (Fase 5)

#### 3. Role-Based Access Control
- ✅ 3 roles: ADMIN, MANAGER, SALES
- ✅ Decorador `@require_role()` en 54 endpoints
- ✅ Permisos granulares con `@require_permission()`
- ✅ Jerarquía de roles respetada

#### 4. Environment Security
- ✅ Secrets en `.env` (no commiteados)
- ✅ Validación obligatoria al inicio
- ✅ Claves generadas criptográficamente
- ✅ `.gitignore` protege archivos sensibles

#### 5. Input Validation (Fase 3)
- ⏳ Schemas Marshmallow para validación
- ⏳ Whitelist de campos permitidos
- ⏳ Type checking y constraints
- ⏳ Sanitización de input

#### 6. Rate Limiting (Fase 5)
- ⏳ Límite de intentos de login (5/min)
- ⏳ Rate limit general (100 req/min)
- ⏳ Protección contra DDoS
- ⏳ Flask-Limiter configurado

### Mejores Prácticas

```python
# ❌ NUNCA
password = "admin123"  # Password en código
JWT_SECRET = "secret"  # Secret hardcodeado

# ✅ SIEMPRE
from app.utils.security import hash_password
hashed = hash_password(password)

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY requerida")
```

### Checklist de Seguridad

- [x] Passwords hasheadas con bcrypt
- [x] JWT secret en variable de entorno
- [x] Database credentials en .env
- [x] CORS configurado
- [ ] Rate limiting implementado
- [ ] Input validation con schemas
- [ ] Token blacklist funcional
- [ ] Audit logging activado
- [ ] HTTPS en producción
- [ ] Security headers configurados

---

## 🚢 Deployment

### Preparación para Producción

#### 1. Actualizar Configuración

```bash
# .env (producción)
FLASK_ENV=production
DEBUG=False
SQLALCHEMY_ECHO=False

# Generar nuevas claves para producción
python scripts/generate_secret_keys.py
```

#### 2. Instalar Gunicorn

```bash
pip install gunicorn
```

#### 3. Ejecutar con Gunicorn

```bash
# Con 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Con configuración avanzada
gunicorn -w 4 \
  --bind 0.0.0.0:5000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  "app:create_app()"
```

#### 4. Configurar Nginx (Reverse Proxy)

```nginx
# /etc/nginx/sites-available/multicont
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /var/www/multicont/static;
        expires 30d;
    }
}
```

#### 5. HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

#### 6. Servicio Systemd

```ini
# /etc/systemd/system/multicont.service
[Unit]
Description=Multicont Flask API
After=network.target postgresql.service

[Service]
User=www-data
WorkingDirectory=/var/www/multicont
Environment="PATH=/var/www/multicont/venv/bin"
ExecStart=/var/www/multicont/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable multicont
sudo systemctl start multicont
sudo systemctl status multicont
```

### Docker (Opcional)

Ver `docs/DEPLOYMENT.md` para configuración completa con Docker.

---

## 📂 Estructura del Proyecto

```
app-multicont/
├── app/                          # Aplicación principal
│   ├── __init__.py               # Factory + config Swagger
│   ├── config.py                 # Configuración por ambiente
│   │
│   ├── entities/                 # DOMAIN LAYER (22 archivos)
│   │   ├── user.py               # Usuario con métodos de dominio
│   │   ├── quote.py              # Cotización
│   │   ├── invoice.py            # Factura
│   │   ├── inventory_item.py     # Item con stock management
│   │   └── ...                   # Otros modelos
│   │
│   ├── use_cases/                # APPLICATION LAYER (22 archivos)
│   │   ├── user_handler.py       # Lógica de negocio de usuarios
│   │   ├── quote_handler.py      # Lógica de cotizaciones
│   │   └── ...                   # Otros handlers
│   │
│   ├── api/                      # PRESENTATION LAYER (24 archivos)
│   │   ├── auth_api.py           # Endpoints de autenticación
│   │   ├── quote_api.py          # Endpoints de cotizaciones
│   │   ├── sales_analytics_api.py # Endpoints de analytics
│   │   └── ...                   # Otros blueprints
│   │
│   ├── utils/                    # Utilidades transversales
│   │   ├── security.py           # Hash bcrypt + JWT config
│   │   ├── decorators.py         # @require_role, @require_permission
│   │   ├── exceptions.py         # Excepciones personalizadas
│   │   └── validators.py         # Validadores (Fase 3)
│   │
│   └── schemas/                  # Marshmallow schemas (Fase 3)
│       ├── quote_schema.py
│       ├── invoice_schema.py
│       └── ...
│
├── migrations/                   # Alembic migrations
│   ├── versions/
│   │   ├── 78a49736b3ac_initial.py
│   │   └── ...
│   └── env.py
│
├── tests/                        # Suite de pruebas
│   ├── conftest.py               # Fixtures pytest
│   ├── test_auth.py              # Tests de autenticación
│   ├── test_api/                 # Tests de endpoints
│   │   ├── test_quote_api.py
│   │   └── ...
│   ├── test_entities/            # Tests de modelos
│   └── test_handlers/            # Tests de use cases
│
├── scripts/                      # Scripts utilitarios
│   ├── generate_secret_keys.py   # Generador de claves
│   ├── check_setup.py            # Verificar configuración
│   ├── database/
│   │   ├── populate_db_validated.py  # Población de BD
│   │   └── create_retroactive_goals.py
│   ├── utils/
│   │   └── verify_models.py      # Verificar modelos
│   └── legacy/                   # Scripts ya ejecutados
│
├── docs/                         # Documentación
│   ├── ARQUITECTURA.md           # Clean Architecture explicada
│   ├── API_REFERENCE.md          # Referencia de API
│   ├── SECURITY.md               # Políticas de seguridad
│   ├── DEPLOYMENT.md             # Guía de deployment
│   └── archive/                  # Docs históricas
│
├── .env.example                  # Template de configuración
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias Python
├── requirements-dev.txt          # Deps de desarrollo (Fase 4)
├── pytest.ini                    # Config de pytest (Fase 4)
├── run.py                        # Entry point de la app
├── README.md                     # Este archivo
├── CHANGELOG.md                  # Historial de cambios (Fase 6)
├── FRONTEND_ANGULAR.md           # Guía de frontend Angular
├── ANALISIS_EXHAUSTIVO_Y_PLAN_MEJORA.md  # Plan de mejoras
└── RESUMEN_MEJORAS_APLICADAS.md  # Resumen de cambios
```

---

## 🛠️ Scripts Útiles

### Generador de Claves Seguras

```bash
python scripts/generate_secret_keys.py
```

### Verificar Setup

```bash
python scripts/check_setup.py
```

### Poblar Base de Datos

```bash
# Población completa con datos colombianos
python scripts/database/populate_db_validated.py

# Resultado:
# - 6 estados
# - 29 ciudades
# - 16 organizaciones
# - 23 sucursales
# - 50 personas
# - 38 empleados
# - 26 usuarios
# - 63 items inventario
# - 32 cotizaciones
# - 25 órdenes
# - 22 facturas
```

### Verificar Modelos

```bash
python scripts/utils/verify_models.py
```

### Migraciones

```bash
# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir última migración
flask db downgrade

# Ver historial
flask db history
```

---

## 🤝 Contribuir

### Workflow de Desarrollo

1. **Fork** el repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Hacer cambios y commit: `git commit -am 'Add nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear **Pull Request**

### Estándares de Código

#### Python
- ✅ **PEP 8** compliance
- ✅ **Type hints** en todas las funciones
- ✅ **Docstrings** en Google style
- ✅ Nombres descriptivos (snake_case para funciones)
- ✅ Clases en PascalCase

#### Arquitectura
- ✅ Respetar **Clean Architecture**
- ✅ Entities → Use Cases → API
- ✅ No skip de capas
- ✅ Lógica de negocio en handlers
- ✅ Lógica de dominio en entities

#### Testing
- ✅ Tests para nuevas features
- ✅ Coverage mínimo 80%
- ✅ Tests unitarios + integración
- ✅ Fixtures reutilizables

### Herramientas de Desarrollo

```bash
# Instalar tools
pip install black flake8 mypy pylint

# Formatear código
black app/

# Lint
flake8 app/
pylint app/

# Type checking
mypy app/
```

---

## ❓ FAQ

### ¿Cómo reseteo la base de datos?

```bash
# Método 1: Revertir todas las migraciones
flask db downgrade base
flask db upgrade

# Método 2: Desde PostgreSQL
psql -U postgres
DROP DATABASE multicont_db;
CREATE DATABASE multicont_db;
\q
flask db upgrade
```

### ¿Cómo agrego un nuevo modelo?

1. Crear entity en `app/entities/nuevo_modelo.py`
2. Crear handler en `app/use_cases/nuevo_modelo_handler.py`
3. Crear API en `app/api/nuevo_modelo_api.py`
4. Registrar blueprint en `app/__init__.py`
5. Crear migración: `flask db migrate -m "Add NuevoModelo"`
6. Aplicar: `flask db upgrade`

### ¿Cómo cambio el puerto de la aplicación?

```bash
# Opción 1: Variable de entorno
PORT=8000 python run.py

# Opción 2: Editar run.py
app.run(port=8000)
```

### ¿Cómo agrego un nuevo rol?

1. Insertar en tabla `role`: `INSERT INTO role (name) VALUES ('NUEVO_ROL');`
2. Agregar permisos en tabla `permission`
3. Usar en decorador: `@require_role('NUEVO_ROL')`

### ¿Swagger no muestra mi endpoint?

Verifica:
1. Blueprint registrado en `app/__init__.py`
2. Ruta inicia con `/api/`
3. Reiniciar aplicación
4. Limpiar cache del navegador

### ¿Cómo habilito HTTPS en desarrollo?

```bash
# Generar certificado self-signed
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365

# Ejecutar con SSL
python run.py --ssl
```

---

## � Testing con pytest

### Ejecución de Tests

```bash
# Ejecutar todos los tests
pytest

# Con coverage report
pytest --cov=app --cov-report=html
start htmlcov/index.html

# Solo tests de autenticación
pytest -m auth -v

# Solo tests rápidos
pytest -m "unit and not slow"
```

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures globales
├── test_auth.py             # Autenticación (20 tests)
├── test_validation.py       # Validación Marshmallow (48 tests)
├── test_handlers.py         # Use cases (28 tests)
└── test_entities.py         # Domain models (15 tests)
```

### Cobertura Actual

| Módulo | Coverage |
|--------|----------|
| app/config.py | 90% ⭐ |
| app/entities/ | 71% ✅ |
| app/use_cases/ | 19-23% ⚠️ |
| **TOTAL** | **37.69%** 🎯 |

📄 Ver documentación completa en **FASE_4_TESTING.md**

---

## �📞 Soporte y Recursos

### Documentación

- 📄 **Este README**: Guía completa de uso
- 📄 **FRONTEND_ANGULAR.md**: Setup de Angular
- 📄 **ANALISIS_EXHAUSTIVO_Y_PLAN_MEJORA.md**: Plan de desarrollo
- 📄 **Swagger UI**: http://127.0.0.1:5000/api/docs/

### Enlaces Útiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### Issues y Bugs

- **GitHub Issues**: [Issues](https://github.com/wilk-17/app-multicont/issues)
- **Email**: soporte@multicont.com (ficticio)

---

## 📄 Licencia

Este proyecto es **privado** y pertenece a **Multicont**.  
Todos los derechos reservados © 2025

---

## 👥 Equipo de Desarrollo

Este proyecto fue desarrollado colaborativamente por:

- **Wilker** (@wilk-17) - Backend Lead & Architect
  - 🏗️ Clean Architecture & Fundamentos
  - 🔐 Sistema JWT + RBAC completo
  - 📝 Validación Marshmallow
  - ♻️ Refactoring DRY (BaseHandler)
  - 🧪 Testing Infrastructure (111 tests)

- **Daniel** - Backend Developer & Business Logic
  - 📊 Sistema Analytics & Metas de Ventas
  - 💾 Población de Base de Datos ($140M simulados)
  - 🏷️ Sistema de Marcas
  - 🗂️ Organización del Proyecto
  - ⚙️ Scripts de Configuración & Verificación

**📄 Aportes Detallados**: Ver [`APORTES_EQUIPO.md`](./APORTES_EQUIPO.md) para un desglose completo de las contribuciones de cada desarrollador (50% cada uno).

---

## 🎓 Agradecimientos

- Inspirado en Clean Architecture de Robert C. Martin
- Arquitectura Hexagonal de Alistair Cockburn
- Comunidad de Flask y SQLAlchemy

---

## 📊 Estado del Proyecto

- ✅ **Backend API**: 95% completo
- ✅ **Autenticación**: 100% funcional
- ✅ **Base de Datos**: Poblada y lista
- ⏳ **Validación**: En progreso (Fase 3)
- ⏳ **Testing**: En progreso (Fase 4)
- ❌ **Frontend**: Documentado, no implementado

---

## 🚀 Quick Start (TL;DR)

```bash
# Clone + Setup
git clone https://github.com/wilk-17/app-multicont.git && cd app-multicont
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# Configure
python scripts/generate_secret_keys.py
copy .env.example .env
# Editar .env con claves generadas

# Database
flask db upgrade
python scripts/database/populate_db_validated.py

# Run
python run.py
# http://127.0.0.1:5000/api/docs/
```

---

**🎉 ¡Listo para desarrollar con Multicont!**

Para comenzar de inmediato:
1. Ejecutar: `python run.py`
2. Abrir: http://127.0.0.1:5000/api/docs/
3. Login con `admin` / `admin123`
4. ¡Explorar la API!

---

**Última actualización**: 19 de Octubre, 2025  
**Versión del README**: 3.0.0 - Documentación de equipo completa  
**Desarrolladores**: Wilker & Daniel - Proyecto Académico 2025
