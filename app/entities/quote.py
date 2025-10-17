"""Quote Entity"""
from datetime import datetime
from app import db

class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    quotation_lines = db.relationship("QuotationLine", backref="quote", lazy=True)
    sales_orders = db.relationship("SalesOrder", backref="quote", lazy=True)
    
    def __init__(self, customer_name, date, total=0, status='pending'):
        self.customer_name = customer_name
        self.date = date
        self.total = total
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'customer_name': self.customer_name,
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total) if self.total else 0,
            'status': self.status
        }
