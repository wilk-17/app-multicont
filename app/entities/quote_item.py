"""QuoteItem Entity"""
from datetime import datetime
from app import db

class QuoteItem(db.Model):
    __tablename__ = "quote_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, quote_id, item_id, quantity):
        self.quote_id = quote_id
        self.item_id = item_id
        self.quantity = quantity
        self.creation_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quote_id': str(self.quote_id),
            'item_id': str(self.item_id),
            'quantity': self.quantity
        }
