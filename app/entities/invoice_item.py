"""InvoiceItem Entity"""
from datetime import datetime
from app import db

class InvoiceItem(db.Model):
    __tablename__ = "invoice_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.BigInteger, db.ForeignKey("invoice.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, invoice_id, item_id, quantity, price):
        self.invoice_id = invoice_id
        self.item_id = item_id
        self.quantity = quantity
        self.price = price
        self.creation_date = datetime.utcnow()
    
    @property
    def subtotal(self):
        return float(self.quantity * self.price) if self.price else 0
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'invoice_id': str(self.invoice_id),
            'item_id': str(self.item_id),
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'subtotal': self.subtotal
        }
