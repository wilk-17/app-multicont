"""SalesOrder Entity"""
from datetime import datetime
from app import db

class SalesOrder(db.Model):
    __tablename__ = "sales_order"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(200), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con items (cascade delete)
    items = db.relationship("SalesOrderItem", backref="sales_order", cascade="all, delete-orphan", lazy=True)
    
    def __init__(self, customer_name, order_date, total=0, status='pending', employee_id=None, quote_id=None):
        self.customer_name = customer_name
        self.order_date = order_date
        self.total = total
        self.status = status
        self.employee_id = employee_id
        self.quote_id = quote_id
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'customer_name': self.customer_name,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'total': float(self.total) if self.total else 0,
            'status': self.status,
            'employee_id': str(self.employee_id) if self.employee_id else None,
            'quote_id': str(self.quote_id) if self.quote_id else None,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'update_date': self.update_date.isoformat() if self.update_date else None
        }
