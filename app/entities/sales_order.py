"""SalesOrder Entity"""
from datetime import datetime
from app import db

class SalesOrder(db.Model):
    __tablename__ = "sales_order"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=True)  # Vendedor responsable
    
    def __init__(self, quote_id, date, total=0, employee_id=None):
        self.quote_id = quote_id
        self.date = date
        self.total = total
        self.employee_id = employee_id
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quote_id': str(self.quote_id),
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total) if self.total else 0,
            'employee_id': str(self.employee_id) if self.employee_id else None
        }
