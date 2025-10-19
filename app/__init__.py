"""
Multicont Flask API - Clean Architecture
Aplicación Flask con arquitectura en capas (Entities, Use Cases, API)
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .config import DevelopmentConfig

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


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

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
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
            "description": "API RESTful para sistema de gestión empresarial con arquitectura en capas",
            "version": "2.0.0",
            "contact": {
                "name": "Multicont Development Team"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header usando Bearer scheme. Ejemplo: 'Bearer {token}'"
            }
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
