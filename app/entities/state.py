"""State Entity"""
from datetime import datetime
from app import db

class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    cities = db.relationship("City", backref="state", lazy=True)
    
    def __init__(self, description, code, status='active'):
        self.description = description
        self.code = code
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'description': self.description,
            'code': self.code,
            'status': self.status,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }
