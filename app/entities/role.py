"""
Role Entity - Domain Model
"""
from datetime import datetime
from app import db


class Role(db.Model):
    """Entidad Rol del sistema."""
    
    __tablename__ = "role"
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    users = db.relationship("User", backref="role", lazy=True)
    
    def __init__(self, name: str, description: str = None, status: str = 'active'):
        self.name = name
        self.description = description
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    def activate(self) -> None:
        self.status = 'active'
        self.update_date = datetime.utcnow()
    
    def inactivate(self) -> None:
        self.status = 'inactive'
        self.update_date = datetime.utcnow()
    
    def is_active(self) -> bool:
        return self.status == 'active'
    
    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'update_date': self.update_date.isoformat() if self.update_date else None
        }
    
    def __repr__(self) -> str:
        return f"Role(id={self.id}, name='{self.name}', status='{self.status}')"
