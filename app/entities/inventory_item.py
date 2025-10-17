"""InventoryItem Entity"""
from datetime import datetime
from app import db

class InventoryItem(db.Model):
    __tablename__ = "inventory_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey("item_category.id"))
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    assignments = db.relationship("Assignment", backref="inventory_item", lazy=True)
    invoice_items = db.relationship("InvoiceItem", backref="inventory_item", lazy=True)
    sales_order_items = db.relationship("SalesOrderItem", backref="inventory_item", lazy=True)
    quote_items = db.relationship("QuoteItem", backref="inventory_item", lazy=True)
    
    def __init__(self, name, price, quantity=0, description=None, category_id=None, status='active'):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.category_id = category_id
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def add_stock(self, amount):
        """Agrega stock al inventario"""
        self.quantity += amount
        self.update_date = datetime.utcnow()
    
    def remove_stock(self, amount):
        """Remueve stock del inventario"""
        if self.quantity >= amount:
            self.quantity -= amount
            self.update_date = datetime.utcnow()
            return True
        return False
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'category_id': str(self.category_id) if self.category_id else None,
            'status': self.status
        }
