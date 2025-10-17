from app import db

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