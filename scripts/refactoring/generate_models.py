"""
Script para generar automáticamente entities, handlers y APIs
para todos los modelos del sistema.
"""
import os

# Definición de todos los modelos con sus campos
MODELS = {
    'Person': {
        'fields': [
            ('dni', 'String(50)', True, 'unique=True'),
            ('first_name', 'String(120)', False),
            ('last_name', 'String(120)', False),
            ('address', 'String(200)', True),
            ('phone', 'String(50)', True),
            ('city_id', 'BigInteger, ForeignKey("city.id")', True),
        ],
        'relationships': [('employees', 'Employee', 'person')],
    },
    'Organization': {
        'fields': [
            ('historical_name', 'String(200)', False),
            ('current_name', 'String(200)', False),
        ],
        'relationships': [('branches', 'Branch', 'organization')],
    },
    'Branch': {
        'fields': [
            ('organization_id', 'BigInteger, ForeignKey("organization.id")', False),
            ('city_id', 'BigInteger, ForeignKey("city.id")', False),
        ],
        'relationships': [('employees', 'Employee', 'branch')],
    },
    'State': {
        'fields': [
            ('description', 'String(120)', False),
            ('code', 'String(20)', False, 'unique=True'),
        ],
        'relationships': [('cities', 'City', 'state')],
    },
    'City': {
        'fields': [
            ('description', 'String(120)', False),
            ('code', 'String(20)', True, 'unique=True'),
            ('state_id', 'BigInteger, ForeignKey("state.id")', False),
        ],
        'relationships': [
            ('persons', 'Person', 'city'),
            ('branches', 'Branch', 'city'),
        ],
    },
    'Employee': {
        'fields': [
            ('person_id', 'BigInteger, ForeignKey("person.id")', False),
            ('branch_id', 'BigInteger, ForeignKey("branch.id")', False),
        ],
        'relationships': [('assignments', 'Assignment', 'employee')],
    },
    'Permission': {
        'fields': [
            ('name', 'String(120)', False, 'unique=True'),
            ('description', 'String(200)', True),
        ],
        'relationships': [],
    },
    'UserRole': {
        'fields': [
            ('user_id', 'BigInteger, ForeignKey("user.id")', False),
            ('role_id', 'BigInteger, ForeignKey("role.id")', False),
        ],
        'relationships': [],
    },
    'ItemCategory': {
        'fields': [
            ('name', 'String(120)', False),
            ('description', 'String(200)', True),
        ],
        'relationships': [('items', 'InventoryItem', 'category')],
    },
    'InventoryItem': {
        'fields': [
            ('name', 'String(200)', False),
            ('description', 'String(200)', True),
            ('quantity', 'Integer', False),
            ('price', 'Numeric(10, 2)', False),
            ('category_id', 'BigInteger, ForeignKey("item_category.id")', True),
        ],
        'relationships': [
            ('assignments', 'Assignment', 'inventory_item'),
            ('invoice_items', 'InvoiceItem', 'inventory_item'),
            ('sales_order_items', 'SalesOrderItem', 'inventory_item'),
            ('quote_items', 'QuoteItem', 'inventory_item'),
        ],
    },
    'Assignment': {
        'fields': [
            ('employee_id', 'BigInteger, ForeignKey("employee.id")', False),
            ('item_id', 'BigInteger, ForeignKey("inventory_item.id")', False),
            ('assigned_date', 'Date', False),
        ],
        'relationships': [],
    },
    'Quote': {
        'fields': [
            ('customer_name', 'String(200)', False),
            ('date', 'Date', False),
            ('total', 'Numeric(12, 2)', False),
        ],
        'relationships': [
            ('quotation_lines', 'QuotationLine', 'quote'),
            ('sales_orders', 'SalesOrder', 'quote'),
        ],
    },
    'QuotationLine': {
        'fields': [
            ('quote_id', 'BigInteger, ForeignKey("quote.id")', False),
            ('description', 'String(200)', True),
            ('quantity', 'Integer', False),
            ('price', 'Numeric(10, 2)', False),
            ('item_id', 'BigInteger, ForeignKey("inventory_item.id")', False),
        ],
        'relationships': [
            ('inventory_item', 'InventoryItem', 'quotation_lines', False),  # many-to-one
            ('invoices', 'Invoice', 'quotation_line'),
        ],
    },
    'QuoteItem': {
        'fields': [
            ('quote_id', 'BigInteger, ForeignKey("quote.id")', False),
            ('item_id', 'BigInteger, ForeignKey("inventory_item.id")', False),
            ('quantity', 'Integer', False),
        ],
        'relationships': [],
    },
    'SalesOrder': {
        'fields': [
            ('quote_id', 'BigInteger, ForeignKey("quote.id")', False),
            ('date', 'Date', False),
            ('total', 'Numeric(12, 2)', False),
        ],
        'relationships': [
            ('invoices', 'Invoice', 'sales_order'),
            ('sales_order_items', 'SalesOrderItem', 'sales_order'),
        ],
    },
    'SalesOrderItem': {
        'fields': [
            ('sales_order_id', 'BigInteger, ForeignKey("sales_order.id")', False),
            ('item_id', 'BigInteger, ForeignKey("inventory_item.id")', False),
            ('quantity', 'Integer', False),
        ],
        'relationships': [],
    },
    'Invoice': {
        'fields': [
            ('sales_order_id', 'BigInteger, ForeignKey("sales_order.id")', False),
            ('quotation_line_id', 'BigInteger, ForeignKey("quotation_line.id")', True),
            ('date', 'Date', False),
            ('total', 'Numeric(12, 2)', False),
        ],
        'relationships': [('invoice_items', 'InvoiceItem', 'invoice')],
    },
    'InvoiceItem': {
        'fields': [
            ('invoice_id', 'BigInteger, ForeignKey("invoice.id")', False),
            ('item_id', 'BigInteger, ForeignKey("inventory_item.id")', False),
            ('quantity', 'Integer', False),
            ('price', 'Numeric(10, 2)', False),
        ],
        'relationships': [],
    },
}

print("Configuración de modelos cargada. Total:", len(MODELS))
print("Modelos:", list(MODELS.keys()))
