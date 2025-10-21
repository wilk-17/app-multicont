"""Quote Entity"""
from datetime import datetime
from app import db

class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=True)  # Vendedor responsable
    
    # Relación con líneas de cotización (cascade delete)
    lines = db.relationship("QuotationLine", backref="quote", cascade="all, delete-orphan", lazy=True)
    
    def __init__(self, customer_name, date, total=0, employee_id=None):
        self.customer_name = customer_name
        self.date = date
        self.total = total
        self.employee_id = employee_id
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'customer_name': self.customer_name,
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total) if self.total else 0,
            'employee_id': str(self.employee_id) if self.employee_id else None
        }
