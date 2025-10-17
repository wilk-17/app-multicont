"""Employee Entity"""
from datetime import datetime
from app import db

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    person_id = db.Column(db.BigInteger, db.ForeignKey("person.id"), nullable=False)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branch.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    hire_date = db.Column(db.Date)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    assignments = db.relationship("Assignment", backref="employee", lazy=True)
    
    def __init__(self, person_id, branch_id, hire_date=None, status='active'):
        self.person_id = person_id
        self.branch_id = branch_id
        self.hire_date = hire_date
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'person_id': str(self.person_id),
            'branch_id': str(self.branch_id),
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'status': self.status
        }
