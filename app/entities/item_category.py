"""ItemCategory Entity"""
from datetime import datetime
from app import db

class ItemCategory(db.Model):
    __tablename__ = "item_category"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200))
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description
        }
