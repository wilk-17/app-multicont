"""Assignment Entity"""
from datetime import datetime
from app import db

class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)
    returned_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default='assigned')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, employee_id, item_id, assigned_date, status='assigned'):
        self.employee_id = employee_id
        self.item_id = item_id
        self.assigned_date = assigned_date
        self.status = status
        self.creation_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'employee_id': str(self.employee_id),
            'item_id': str(self.item_id),
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'returned_date': self.returned_date.isoformat() if self.returned_date else None,
            'status': self.status
        }
