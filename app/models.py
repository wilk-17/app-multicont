from . import db

# =========================================================
# ORGANIZACIONES Y SUCURSALES
# =========================================================
class Organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    historical_name = db.Column(db.String(200), nullable=False)
    current_name = db.Column(db.String(200), nullable=False)

    branches = db.relationship("Branch", backref="organization", lazy=True)


class Branch(db.Model):
    __tablename__ = "branch"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.BigInteger, db.ForeignKey("organization.id"), nullable=False)
    city_id = db.Column(db.BigInteger, db.ForeignKey("city.id"), nullable=False)

    employees = db.relationship("Employee", backref="branch", lazy=True)


# =========================================================
# GEOGRAFÍA
# =========================================================
class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    cities = db.relationship("City", backref="state", lazy=True)


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True)
    state_id = db.Column(db.BigInteger, db.ForeignKey("state.id"), nullable=False)

    persons = db.relationship("Person", backref="city", lazy=True)
    branches = db.relationship("Branch", backref="city", lazy=True)


# =========================================================
# PERSONAS Y EMPLEADOS
# =========================================================
class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    city_id = db.Column(db.BigInteger, db.ForeignKey("city.id"))

    employees = db.relationship("Employee", backref="person", lazy=True)


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    person_id = db.Column(db.BigInteger, db.ForeignKey("person.id"), nullable=False)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branch.id"), nullable=False)

    assignments = db.relationship("Assignment", backref="employee", lazy=True)


# =========================================================
# ROLES, USUARIOS Y PERMISOS
# =========================================================
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), nullable=False)

    roles = db.relationship("UserRole", backref="user", lazy=True)


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), nullable=False)


# =========================================================
# INVENTARIO
# =========================================================
class ItemCategory(db.Model):
    __tablename__ = "item_category"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)

    items = db.relationship("InventoryItem", backref="category", lazy=True)


class InventoryItem(db.Model):
    __tablename__ = "inventory_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey("item_category.id"))

    assignments = db.relationship("Assignment", backref="inventory_item", lazy=True)
    invoice_items = db.relationship("InvoiceItem", backref="inventory_item", lazy=True)
    sales_order_items = db.relationship("SalesOrderItem", backref="inventory_item", lazy=True)
    quote_items = db.relationship("QuoteItem", backref="inventory_item", lazy=True)


class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)


# =========================================================
# COTIZACIONES Y VENTAS
# =========================================================
class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False)

    quotation_lines = db.relationship("QuotationLine", backref="quote", lazy=True)
    sales_orders = db.relationship("SalesOrder", backref="quote", lazy=True)


class QuotationLine(db.Model):
    __tablename__ = "quotation_line"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)

    inventory_item = db.relationship("InventoryItem", backref="quotation_lines", lazy=True)
    invoices = db.relationship("Invoice", backref="quotation_line", lazy=True)


class QuoteItem(db.Model):
    __tablename__ = "quote_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class SalesOrder(db.Model):
    __tablename__ = "sales_order"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False)

    invoices = db.relationship("Invoice", backref="sales_order", lazy=True)
    sales_order_items = db.relationship("SalesOrderItem", backref="sales_order", lazy=True)


class SalesOrderItem(db.Model):
    __tablename__ = "sales_order_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sales_order_id = db.Column(db.BigInteger, db.ForeignKey("sales_order.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sales_order_id = db.Column(db.BigInteger, db.ForeignKey("sales_order.id"), nullable=False)
    quotation_line_id = db.Column(db.BigInteger, db.ForeignKey("quotation_line.id"))
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False)

    invoice_items = db.relationship("InvoiceItem", backref="invoice", lazy=True)


class InvoiceItem(db.Model):
    __tablename__ = "invoice_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.BigInteger, db.ForeignKey("invoice.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
