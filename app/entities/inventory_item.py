"""InventoryItem Entity"""
from datetime import datetime
from app import db

class InventoryItem(db.Model):
    __tablename__ = "inventory_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey("item_category.id"))
    brand_id = db.Column(db.BigInteger, db.ForeignKey("brand.id"), nullable=True)
    
    def __init__(self, name, price, quantity=0, description=None, category_id=None, brand_id=None):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.category_id = category_id
        self.brand_id = brand_id
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'category_id': str(self.category_id) if self.category_id else None,
            'brand_id': str(self.brand_id) if self.brand_id else None
        }
