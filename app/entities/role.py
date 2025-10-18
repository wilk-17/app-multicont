"""
Role Entity - Domain Model
"""
from datetime import datetime
from app import db


class Role(db.Model):
    """Entidad Rol del sistema."""
    
    __tablename__ = "role"
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name
        }
