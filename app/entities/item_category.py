"""ItemCategory Entity"""
from app import db

class ItemCategory(db.Model):
    __tablename__ = "item_category"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    
    def __init__(self, name):
        self.name = name
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name
        }
