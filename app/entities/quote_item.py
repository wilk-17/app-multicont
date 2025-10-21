"""QuoteItem Entity"""
from datetime import datetime
from app import db

class QuoteItem(db.Model):
    __tablename__ = "quote_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def __init__(self, quote_id=None, item_id=None, quantity=None):
        self.quote_id = quote_id
        self.item_id = item_id
        self.quantity = quantity
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quote_id': str(self.quote_id),
            'item_id': str(self.item_id),
            'quantity': self.quantity
        }
