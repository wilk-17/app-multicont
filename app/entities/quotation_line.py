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
    
    def __init__(self, quote_id=None, item_id=None, quantity=None, price=None, description=None):
        self.quote_id = quote_id
        self.item_id = item_id
        self.quantity = quantity
        self.price = price
        self.description = description
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quote_id': str(self.quote_id),
            'item_id': str(self.item_id),
            'description': self.description,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0
        }
