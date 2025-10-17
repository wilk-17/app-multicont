"""City Entity"""
from datetime import datetime
from app import db

class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True)
    state_id = db.Column(db.BigInteger, db.ForeignKey("state.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    persons = db.relationship("Person", backref="city", lazy=True)
    branches = db.relationship("Branch", backref="city", lazy=True)
    
    def __init__(self, description, state_id, code=None, status='active'):
        self.description = description
        self.code = code
        self.state_id = state_id
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'description': self.description,
            'code': self.code,
            'state_id': str(self.state_id),
            'status': self.status
        }
