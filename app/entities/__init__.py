"""
Entities - Domain Models Layer
Contiene las entidades de dominio con lógica de negocio pura.
"""
from .user import User
from .role import Role
from .person import Person
from .employee import Employee
from .organization import Organization
from .branch import Branch
from .state import State
from .city import City
from .permission import Permission
from .user_role import UserRole
from .item_category import ItemCategory
from .inventory_item import InventoryItem
from .assignment import Assignment
from .quote import Quote
from .quotation_line import QuotationLine
from .quote_item import QuoteItem
from .sales_order import SalesOrder
from .sales_order_item import SalesOrderItem
from .invoice import Invoice
from .invoice_item import InvoiceItem

__all__ = [
    'User', 'Role', 'Person', 'Employee', 'Organization', 'Branch',
    'State', 'City', 'Permission', 'UserRole', 'ItemCategory',
    'InventoryItem', 'Assignment', 'Quote', 'QuotationLine', 'QuoteItem',
    'SalesOrder', 'SalesOrderItem', 'Invoice', 'InvoiceItem'
]
