"""ItemCategory Entity"""
from datetime import datetime
from app import db

class ItemCategory(db.Model):
    __tablename__ = "item_category"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship("InventoryItem", backref="category", lazy=True)
    
    def __init__(self, name, description=None, status='active'):
        self.name = name
        self.description = description
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'status': self.status
        }
