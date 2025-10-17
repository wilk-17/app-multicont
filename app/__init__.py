"""
Multicont Flask API - Clean Architecture
Aplicación Flask con arquitectura en capas (Entities, Use Cases, API)
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from .config import DevelopmentConfig

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()


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

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar Swagger/Flasgger para documentación API
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
    
    Swagger(app, config=swagger_config, template=swagger_template)

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
        from .api.metrics_api import metrics_api
        from .api.dashboard_api import dashboard_api

        # Registrar blueprints
        blueprints = [
            user_api, role_api, person_api, employee_api, organization_api,
            branch_api, state_api, city_api, permission_api, user_role_api,
            item_category_api, inventory_item_api, assignment_api, quote_api,
            quotation_line_api, quote_item_api, sales_order_api, sales_order_item_api,
            invoice_api, invoice_item_api, metrics_api, dashboard_api
        ]
        
        for blueprint in blueprints:
            app.register_blueprint(blueprint)

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
