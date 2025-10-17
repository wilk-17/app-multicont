"""SalesOrder Entity"""
from datetime import datetime
from app import db

class SalesOrder(db.Model):
    __tablename__ = "sales_order"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    invoices = db.relationship("Invoice", backref="sales_order", lazy=True)
    sales_order_items = db.relationship("SalesOrderItem", backref="sales_order", lazy=True)
    
    def __init__(self, quote_id, date, total=0, status='pending'):
        self.quote_id = quote_id
        self.date = date
        self.total = total
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quote_id': str(self.quote_id),
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total) if self.total else 0,
            'status': self.status
        }
