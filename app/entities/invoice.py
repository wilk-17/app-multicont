"""Invoice Entity"""
from datetime import datetime
from app import db

class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sales_order_id = db.Column(db.BigInteger, db.ForeignKey("sales_order.id"), nullable=False)
    quotation_line_id = db.Column(db.BigInteger, db.ForeignKey("quotation_line.id"))
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    invoice_items = db.relationship("InvoiceItem", backref="invoice", lazy=True)
    
    def __init__(self, sales_order_id, date, total=0, quotation_line_id=None, status='pending'):
        self.sales_order_id = sales_order_id
        self.quotation_line_id = quotation_line_id
        self.date = date
        self.total = total
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'sales_order_id': str(self.sales_order_id),
            'quotation_line_id': str(self.quotation_line_id) if self.quotation_line_id else None,
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total) if self.total else 0,
            'status': self.status
        }
