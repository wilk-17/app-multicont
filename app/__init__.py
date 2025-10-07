from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from .config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="API Multicont",
    version="1.0",
    description="Documentación Swagger para endpoints RESTful"
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Importar modelos para que Migrate los detecte
    from .models.organization import Organization
    from .models.branch import Branch
    from .models.state import State
    from .models.city import City
    from .models.person import Person
    from .models.employee import Employee
    from .models.role import Role
    from .models.user import User
    from .models.permission import Permission
    from .models.user_role import UserRole
    from .models.item_category import ItemCategory
    from .models.inventory_item import InventoryItem
    from .models.assignment import Assignment
    from .models.quote import Quote
    from .models.quotation_line import QuotationLine
    from .models.quote_item import QuoteItem
    from .models.sales_order import SalesOrder
    from .models.sales_order_item import SalesOrderItem
    from .models.invoice import Invoice
    from .models.invoice_item import InvoiceItem

    # Registrar namespace RESTX
    from .routes import (
        user_ns, role_ns, person_ns, employee_ns, organization_ns, branch_ns,
        state_ns, city_ns, permission_ns, user_role_ns, assignment_ns,
        inventory_item_ns, quote_ns, quotation_line_ns, quote_item_ns,
        sales_order_ns, sales_order_item_ns, invoice_ns, invoice_item_ns
    )
    api.add_namespace(user_ns)
    api.add_namespace(role_ns)
    api.add_namespace(person_ns)
    api.add_namespace(employee_ns)
    api.add_namespace(organization_ns)
    api.add_namespace(branch_ns)
    api.add_namespace(state_ns)
    api.add_namespace(city_ns)
    api.add_namespace(permission_ns)
    api.add_namespace(user_role_ns)
    api.add_namespace(assignment_ns)
    api.add_namespace(inventory_item_ns)
    api.add_namespace(quote_ns)
    api.add_namespace(quotation_line_ns)
    api.add_namespace(quote_item_ns)
    api.add_namespace(sales_order_ns)
    api.add_namespace(sales_order_item_ns)
    api.add_namespace(invoice_ns)
    api.add_namespace(invoice_item_ns)
