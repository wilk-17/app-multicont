"""State Entity"""
from app import db

class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    
    def __init__(self, description, code):
        self.description = description
        self.code = code
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'description': self.description,
            'code': self.code
        }
