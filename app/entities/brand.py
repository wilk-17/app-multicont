"""
Brand Entity - Marcas de productos
Permite categorizar productos por marca para análisis de ventas
"""
from datetime import datetime
from app import db


class Brand(db.Model):
    """
    Marca de productos para tracking y análisis de ventas.
    Ejemplos: Samsung, Apple, Sony, etc.
    """
    __tablename__ = "brand"
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    inventory_items = db.relationship("InventoryItem", backref="brand", lazy=True)
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.creation_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }
    
    def __repr__(self):
        return f'<Brand {self.name}>'
