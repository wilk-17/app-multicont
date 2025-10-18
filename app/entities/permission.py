"""Permission Entity"""
from datetime import datetime
from app import db

class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, name):
        self.name = name
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name
        }
