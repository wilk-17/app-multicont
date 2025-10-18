"""City Entity"""
from datetime import datetime
from app import db

class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20))
    state_id = db.Column(db.BigInteger, db.ForeignKey("state.id"), nullable=False)
    
    def __init__(self, description, state_id, code=None):
        self.description = description
        self.code = code
        self.state_id = state_id
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'description': self.description,
            'code': self.code,
            'state_id': str(self.state_id)
        }
