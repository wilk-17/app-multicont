"""Employee Entity"""
from datetime import datetime
from app import db

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    person_id = db.Column(db.BigInteger, db.ForeignKey("person.id"), nullable=False)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branch.id"), nullable=False)
    
    def __init__(self, person_id, branch_id):
        self.person_id = person_id
        self.branch_id = branch_id
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'person_id': str(self.person_id),
            'branch_id': str(self.branch_id)
        }
