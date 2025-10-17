"""Organization Entity"""
from datetime import datetime
from app import db

class Organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    historical_name = db.Column(db.String(200), nullable=False)
    current_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    branches = db.relationship("Branch", backref="organization", lazy=True)
    
    def __init__(self, historical_name, current_name, status='active'):
        self.historical_name = historical_name
        self.current_name = current_name
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'historical_name': self.historical_name,
            'current_name': self.current_name,
            'status': self.status,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'update_date': self.update_date.isoformat() if self.update_date else None
        }
