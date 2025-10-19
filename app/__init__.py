"""
Multicont Flask API - Clean Architecture
Aplicación Flask con arquitectura en capas (Entities, Use Cases, API)
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flasgger import Swagger
from .config import DevelopmentConfig

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()


def create_app(config_class=DevelopmentConfig):
    """
    Factory para crear la aplicación Flask con Clean Architecture.
    
    Args:
        config_class: Clase de configuración a usar (Development, Production, Testing)
    
    Returns:
        Flask app configurada
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configurar JWT
    from .utils.security import get_jwt_config
    jwt_config = get_jwt_config()
    for key, value in jwt_config.items():
        app.config[key] = value
    
    # Configurar Cache
    cache_config = {
        'CACHE_TYPE': 'SimpleCache',  # SimpleCache para desarrollo
        'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutos por defecto
        'CACHE_KEY_PREFIX': 'multicont_'
    }
    app.config.update(cache_config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    
    # Configurar Swagger/Flasgger (se inicializará más abajo
    # una vez que hayamos importado las entidades para generar definitions)
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Multicont - Clean Architecture",
            "description": """
# Sistema de Gestión Empresarial - API RESTful

## 🏗️ Arquitectura Clean (Hexagonal)
Esta API sigue los principios de **Clean Architecture** con separación en 3 capas:

- **Entities (Domain Layer)**: Modelos de dominio con lógica de negocio
- **Use Cases (Application Layer)**: Handlers con lógica de aplicación
- **API (Presentation Layer)**: Endpoints REST con validación

## 🚀 Características Principales

### Performance & Caching
- **Flask-Caching**: Cache de 5 minutos en endpoints GET
- **Eager Loading**: Prevención de N+1 queries con joinedload()
- **Paginación**: Todos los listados soportan `?page=1&per_page=10`

### Seguridad
- **JWT Authentication**: Bearer token en header `Authorization`
- **Role-Based Access**: Control de acceso por roles (ADMIN, MANAGER, USER)
- **Validación**: Marshmallow schemas automáticos en todos los endpoints

### Documentación
- **Swagger UI**: Interfaz interactiva para probar endpoints
- **OpenAPI 2.0**: Especificación completa con ejemplos
- **Auto-generated Schemas**: Definiciones desde modelos SQLAlchemy

## 📊 Módulos Disponibles

### Core Business
- **Organizations & Branches**: Gestión de organizaciones y sucursales
- **Users & Roles**: Sistema de autenticación y autorización
- **Employees**: Gestión de empleados con asignaciones

### Inventory & Products
- **Inventory Items**: Control de stock con alertas de bajo inventario
- **Item Categories**: Categorización de productos
- **Assignments**: Asignación de items a empleados

### Sales & Invoicing
- **Quotes**: Cotizaciones con líneas de items
- **Sales Orders**: Órdenes de venta con workflow de estados
- **Invoices**: Facturación con items y totales
- **Sales Analytics**: Métricas y reportes de ventas

## 🔑 Autenticación

1. **Login**: `POST /api/auth/login` con username y password
2. **Obtener Token**: Response incluye `access_token`
3. **Usar Token**: Agregar header `Authorization: Bearer {token}` en requests

Ejemplo:
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin", "password": "admin123"}'

# Usar token en requests
curl http://localhost:5000/api/inventory_items/ \\
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

## 📖 Convenciones API

### Respuestas Estándar
Todas las respuestas siguen este formato:

**Éxito**:
```json
{
  "success": true,
  "data": {...},
  "message": "Operación exitosa"
}
```

**Error**:
```json
{
  "success": false,
  "error": "Descripción del error",
  "errors": {"field": ["mensaje de validación"]}
}
```

**Paginación**:
```json
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

### Códigos HTTP
- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## 🔧 Parámetros de Query Comunes

- `page`: Número de página (default: 1)
- `per_page`: Items por página (default: 10, máx: 100)
- `status`: Filtrar por estado (active, inactive, pending, etc.)

## 💡 Tips de Performance

- Usa paginación en listados grandes
- Los endpoints GET están cacheados (5 min)
- Usa eager loading endpoints cuando necesites relaciones (ej: `/api/employees/` carga branches automáticamente)

## 📚 Recursos Adicionales

- **GitHub**: [github.com/wilk-17/app-multicont](https://github.com/wilk-17/app-multicont)
- **Deployment Guide**: Ver `DEPLOYMENT.md` para guía de producción
- **Architecture Docs**: Ver `.github/copilot-instructions.md`
            """,
            "version": "2.0.0",
            "contact": {
                "name": "Multicont Development Team",
                "email": "dev@multicont.com",
                "url": "https://github.com/wilk-17/app-multicont"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header usando Bearer scheme. Formato: `Authorization: Bearer {token}`\n\nPara obtener un token:\n1. Haz login en `POST /api/auth/login`\n2. Copia el `access_token` de la respuesta\n3. Úsalo en el header de tus requests"
            }
        },
        "tags": [
            {"name": "Autenticación", "description": "Login y gestión de tokens JWT"},
            {"name": "Usuarios", "description": "Gestión de usuarios del sistema"},
            {"name": "Roles", "description": "Roles y permisos"},
            {"name": "Organizaciones", "description": "Gestión de organizaciones y empresas"},
            {"name": "Sucursales", "description": "Sucursales por organización"},
            {"name": "Empleados", "description": "Gestión de empleados y asignaciones"},
            {"name": "Inventory Items", "description": "Control de inventario y stock"},
            {"name": "Categorías", "description": "Categorías de productos"},
            {"name": "Cotizaciones", "description": "Cotizaciones para clientes"},
            {"name": "Órdenes de Venta", "description": "Órdenes de venta con workflow"},
            {"name": "Facturas", "description": "Facturación y pagos"},
            {"name": "Analytics", "description": "Reportes y métricas de negocio"},
            {"name": "Ubicaciones", "description": "Estados y ciudades"}
        ],
        "externalDocs": {
            "description": "Documentación Completa del Proyecto",
            "url": "https://github.com/wilk-17/app-multicont/blob/main/README.md"
        }
    }

    # Importar TODAS las entidades para que Alembic las detecte
    # IMPORTANTE: Estos imports deben estar aquí para que las migraciones funcionen
    with app.app_context():
        from .entities.user import User
        from .entities.role import Role
        from .entities.person import Person
        from .entities.employee import Employee
        from .entities.organization import Organization
        from .entities.branch import Branch
        from .entities.state import State
        from .entities.city import City
        from .entities.permission import Permission
        from .entities.user_role import UserRole
        from .entities.item_category import ItemCategory
        from .entities.inventory_item import InventoryItem
        from .entities.assignment import Assignment
        from .entities.quote import Quote
        from .entities.quotation_line import QuotationLine
        from .entities.quote_item import QuoteItem
        from .entities.sales_order import SalesOrder
        from .entities.sales_order_item import SalesOrderItem
        from .entities.invoice import Invoice
        from .entities.invoice_item import InvoiceItem
        from .entities.brand import Brand
        from .entities.sales_goal import SalesGoal

        # Registrar todos los Blueprints de la API
        from .api.user_api import user_api
        from .api.role_api import role_api
        from .api.person_api import person_api
        from .api.employee_api import employee_api
        from .api.organization_api import organization_api
        from .api.branch_api import branch_api
        from .api.state_api import state_api
        from .api.city_api import city_api
        from .api.permission_api import permission_api
        from .api.user_role_api import user_role_api
        from .api.item_category_api import item_category_api
        from .api.inventory_item_api import inventory_item_api
        from .api.assignment_api import assignment_api
        from .api.quote_api import quote_api
        from .api.quotation_line_api import quotation_line_api
        from .api.quote_item_api import quote_item_api
        from .api.sales_order_api import sales_order_api
        from .api.sales_order_item_api import sales_order_item_api
        from .api.invoice_api import invoice_api
        from .api.invoice_item_api import invoice_item_api
        from .api.brand_api import brand_api
        from .api.sales_goal_api import sales_goal_api
        from .api.sales_analytics_api import sales_analytics_api
        from .api.auth_api import auth_api

        # Registrar blueprints
        blueprints = [
            user_api, role_api, person_api, employee_api, organization_api,
            branch_api, state_api, city_api, permission_api, user_role_api,
            item_category_api, inventory_item_api, assignment_api, quote_api,
            quotation_line_api, quote_item_api, sales_order_api, sales_order_item_api,
            invoice_api, invoice_item_api, brand_api, sales_goal_api, sales_analytics_api,
            auth_api
        ]
        
        for blueprint in blueprints:
            app.register_blueprint(blueprint)

        # Generar definiciones Swagger (definitions) a partir de las entidades SQLAlchemy
        # Esto permite que Swagger UI muestre todas las entidades en la sección de modelos
        try:
            from sqlalchemy import Integer, BigInteger, String, DateTime, Date, Numeric, Boolean, Float, Text

            def sa_type_to_swagger(col_type):
                name = col_type.__class__.__name__.lower()
                if 'integer' in name or 'biginteger' in name:
                    return {'type': 'integer', 'format': 'int64'}
                if 'numeric' in name or 'decimal' in name or 'float' in name:
                    return {'type': 'number', 'format': 'double'}
                if 'boolean' in name:
                    return {'type': 'boolean'}
                if 'date' in name and 'time' in name:
                    return {'type': 'string', 'format': 'date-time'}
                if 'date' in name:
                    return {'type': 'string', 'format': 'date'}
                # default to string for VARCHAR, TEXT, etc.
                return {'type': 'string'}

            definitions = {}
            # Lista de clases importadas arriba: iterar por objetos en locals()
            entity_classes = [User, Role, Person, Employee, Organization, Branch, State, City,
                              Permission, UserRole, ItemCategory, InventoryItem, Assignment,
                              Quote, QuotationLine, QuoteItem, SalesOrder, SalesOrderItem,
                              Invoice, InvoiceItem, Brand, SalesGoal]

            for cls in entity_classes:
                try:
                    props = {}
                    required = []
                    for col in cls.__table__.columns:
                        col_name = col.name
                        swagger_type = sa_type_to_swagger(col.type)
                        props[col_name] = swagger_type
                        # mark required if column is primary key or not nullable and has no default
                        if not col.nullable and not col.primary_key:
                            required.append(col_name)
                    definitions[cls.__name__] = {
                        'type': 'object',
                        'properties': props
                    }
                    if required:
                        definitions[cls.__name__]['required'] = required
                except Exception:
                    # ignore classes that are not mappable
                    continue

            # inject definitions into swagger template
            swagger_template.setdefault('definitions', {}).update(definitions)
            # Build simple JSON 'paths' entries from registered Flask rules
            # This avoids relying on YAML docstrings — each path will have minimal
            # operations (GET/POST/PUT/DELETE) with a 200 response and optional
            # schema $ref pointing to a definition when a model name can be inferred.
            paths = {}

            def plural_to_model(name: str) -> str:
                # name: e.g. 'inventory_items' -> InventoryItem
                if not name:
                    return None
                # remove possible query/params
                base = name.strip('/').split('/')[-1]
                # if it's already singular-like, try simple rules
                if base.endswith('ies'):
                    base = base[:-3] + 'y'
                elif base.endswith('s'):
                    base = base[:-1]
                parts = base.split('_')
                return ''.join(p.capitalize() for p in parts) if parts else None

            for rule in app.url_map.iter_rules():
                # consider only API routes under /api
                if not str(rule.rule).startswith('/api'):
                    continue
                path = rule.rule
                # convert flask converters '<int:id>' to swagger '{id}'
                swagger_path = ''
                i = 0
                while i < len(path):
                    if path[i] == '<':
                        j = path.find('>', i)
                        if j == -1:
                            break
                        conv = path[i+1:j]
                        # conv could be 'int:id' or 'id'
                        if ':' in conv:
                            _, var = conv.split(':', 1)
                        else:
                            var = conv
                        swagger_path += '{' + var + '}'
                        i = j+1
                    else:
                        swagger_path += path[i]
                        i += 1

                methods = [m for m in rule.methods if m in ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')]
                if not methods:
                    continue

                # attempt to infer model name from the first component after /api/
                parts = path.split('/')
                model_hint = None
                if len(parts) >= 3:
                    model_hint = plural_to_model(parts[2])

                # build path item
                path_item = {}
                for m in methods:
                    op = {
                        'tags': [model_hint] if model_hint else ['API'],
                        'summary': f'{m} {swagger_path}',
                        'responses': {
                            '200': {'description': 'Successful response'}
                        }
                    }

                    # if path has an id param, add path parameter
                    if '{id}' in swagger_path:
                        op.setdefault('parameters', []).append({
                            'name': 'id',
                            'in': 'path',
                            'required': True,
                            'type': 'integer'
                        })

                    # attach a basic schema reference when we can infer a model
                    if model_hint and model_hint in swagger_template.get('definitions', {}):
                        if m == 'GET' and '{id}' in swagger_path:
                            op['responses']['200']['schema'] = {'$ref': f"#/definitions/{model_hint}"}
                        elif m == 'GET':
                            op['responses']['200']['schema'] = {
                                'type': 'array',
                                'items': {'$ref': f"#/definitions/{model_hint}"}
                            }
                        else:
                            # for POST/PUT/PATCH return the model object
                            op['responses']['200']['schema'] = {'$ref': f"#/definitions/{model_hint}"}

                    path_item[m.lower()] = op

                paths[swagger_path] = path_item

            if paths:
                swagger_template.setdefault('paths', {}).update(paths)
        except Exception:
            # if anything fails here, do not break app init — Swagger will still run without definitions
            pass

        # Inicializar Swagger ahora que template incluye definitions
        Swagger(app, config=swagger_config, template=swagger_template)

    # Ruta de bienvenida
    @app.route('/')
    def index():
        return {
            'message': 'API Multicont - Clean Architecture',
            'version': '2.0.0',
            'documentation': '/api/docs/',
            'architecture': {
                'entities': 'Domain models with business logic',
                'use_cases': 'Application logic handlers',
                'api': 'REST API endpoints (Flask Blueprints)'
            }
        }
    
    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'error': 'Endpoint no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'success': False, 'error': 'Error interno del servidor'}, 500

    return app
