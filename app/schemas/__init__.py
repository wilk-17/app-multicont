"""
Schemas Module - Marshmallow Validation Schemas
Centraliza todas las importaciones de schemas de validación.
"""
from .quote_schema import (
    quote_create_schema,
    quote_update_schema,
    quote_response_schema,
    quotes_response_schema
)
from .invoice_schema import (
    invoice_create_schema,
    invoice_update_schema,
    invoice_response_schema,
    invoices_response_schema
)
from .inventory_item_schema import (
    inventory_item_create_schema,
    inventory_item_update_schema,
    stock_operation_schema,
    inventory_item_response_schema,
    inventory_items_response_schema
)
from .sales_order_schema import (
    sales_order_create_schema,
    sales_order_update_schema,
    sales_order_response_schema,
    sales_orders_response_schema
)
from .user_schema import (
    user_create_schema,
    user_update_schema,
    password_change_schema,
    user_response_schema,
    users_response_schema
)
from .employee_schema import (
    employee_create_schema,
    employee_update_schema,
    employee_response_schema,
    employees_response_schema
)

__all__ = [
    # Quote schemas
    'quote_create_schema',
    'quote_update_schema',
    'quote_response_schema',
    'quotes_response_schema',
    
    # Invoice schemas
    'invoice_create_schema',
    'invoice_update_schema',
    'invoice_response_schema',
    'invoices_response_schema',
    
    # Inventory schemas
    'inventory_item_create_schema',
    'inventory_item_update_schema',
    'stock_operation_schema',
    'inventory_item_response_schema',
    'inventory_items_response_schema',
    
    # Sales Order schemas
    'sales_order_create_schema',
    'sales_order_update_schema',
    'sales_order_response_schema',
    'sales_orders_response_schema',
    
    # User schemas
    'user_create_schema',
    'user_update_schema',
    'password_change_schema',
    'user_response_schema',
    'users_response_schema',
    
    # Employee schemas
    'employee_create_schema',
    'employee_update_schema',
    'employee_response_schema',
    'employees_response_schema',
]
