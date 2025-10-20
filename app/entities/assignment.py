"""Assignment Entity - Trazabilidad de asignaciones de items a empleados"""
from datetime import datetime, date
from app import db

class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False, default=date.today)
    
    # Trazabilidad - Nuevos campos
    status = db.Column(db.String(20), nullable=False, default='active')  # active, returned, lost
    return_date = db.Column(db.Date, nullable=True)
    condition = db.Column(db.String(50), nullable=True)  # good, damaged, missing
    notes = db.Column(db.Text, nullable=True)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, employee_id, item_id, assigned_date=None, status='active'):
        self.employee_id = employee_id
        self.item_id = item_id
        self.assigned_date = assigned_date or date.today()
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def mark_returned(self, condition='good', notes=None):
        """Marca la asignación como devuelta"""
        self.status = 'returned'
        self.return_date = date.today()
        self.condition = condition
        if notes:
            self.notes = notes
        self.update_date = datetime.utcnow()
    
    def mark_lost(self, notes=None):
        """Marca la asignación como perdida"""
        self.status = 'lost'
        self.condition = 'missing'
        if notes:
            self.notes = notes
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'employee_id': str(self.employee_id),
            'item_id': str(self.item_id),
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'status': self.status,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'condition': self.condition,
            'notes': self.notes,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'update_date': self.update_date.isoformat() if self.update_date else None
        }
