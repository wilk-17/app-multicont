"""Branch Entity"""
from datetime import datetime
from app import db

class Branch(db.Model):
    __tablename__ = "branch"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.BigInteger, db.ForeignKey("organization.id"), nullable=False)
    city_id = db.Column(db.BigInteger, db.ForeignKey("city.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    employees = db.relationship("Employee", backref="branch", lazy=True)
    
    def __init__(self, organization_id, city_id, status='active'):
        self.organization_id = organization_id
        self.city_id = city_id
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'organization_id': str(self.organization_id),
            'city_id': str(self.city_id),
            'status': self.status
        }
