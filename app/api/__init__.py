"""
API - Presentation Layer
Contiene los blueprints de Flask para los endpoints REST.
"""
from .user_api import user_api
from .role_api import role_api
from .person_api import person_api
from .employee_api import employee_api
from .organization_api import organization_api
from .branch_api import branch_api
from .state_api import state_api
from .city_api import city_api
from .permission_api import permission_api
from .user_role_api import user_role_api
from .item_category_api import item_category_api
from .inventory_item_api import inventory_item_api
from .assignment_api import assignment_api
from .quote_api import quote_api
from .quotation_line_api import quotation_line_api
from .quote_item_api import quote_item_api
from .sales_order_api import sales_order_api
from .sales_order_item_api import sales_order_item_api
from .invoice_api import invoice_api
from .invoice_item_api import invoice_item_api
from .metrics_api import metrics_api
from .dashboard_api import dashboard_api

__all__ = [
    'user_api', 'role_api', 'person_api', 'employee_api',
    'organization_api', 'branch_api', 'state_api', 'city_api',
    'permission_api', 'user_role_api', 'item_category_api',
    'inventory_item_api', 'assignment_api', 'quote_api',
    'quotation_line_api', 'quote_item_api', 'sales_order_api',
    'sales_order_item_api', 'invoice_api', 'invoice_item_api',
    'metrics_api', 'dashboard_api'
]
