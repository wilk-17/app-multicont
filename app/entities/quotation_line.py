"""QuotationLine Entity"""
from datetime import datetime
from app import db

class QuotationLine(db.Model):
    __tablename__ = "quotation_line"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    inventory_item = db.relationship("InventoryItem", backref="quotation_lines", lazy=True)
    invoices = db.relationship("Invoice", backref="quotation_line", lazy=True)
    
    def __init__(self, quote_id, item_id, quantity, price, description=None):
        self.quote_id = quote_id
        self.item_id = item_id
        self.quantity = quantity
        self.price = price
        self.description = description
        self.creation_date = datetime.utcnow()
    
    @property
    def subtotal(self):
        return float(self.quantity * self.price) if self.price else 0
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quote_id': str(self.quote_id),
            'item_id': str(self.item_id),
            'description': self.description,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'subtotal': self.subtotal
        }
