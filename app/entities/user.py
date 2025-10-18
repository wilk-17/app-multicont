"""
User Entity - Domain Model
Representa un usuario del sistema con lógica de negocio pura.
"""
from datetime import datetime
from app import db


class User(db.Model):
    """Entidad Usuario con lógica de dominio."""
    
    __tablename__ = "user"
    
    # Columnas de base de datos
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), nullable=False)
    
    # Relaciones
    roles = db.relationship("UserRole", backref="user", lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, username: str, password: str, role_id: int):
        """
        Inicializa un usuario.
        
        Args:
            username: Nombre de usuario único.
            password: Contraseña (ya debe venir hasheada).
            role_id: ID del rol asociado.
            status: Estado del usuario (default: 'active').
        """
        self.username = username
        self.password = password
        self.role_id = role_id
    
    
    def update_password(self, new_password: str) -> None:
        """
        Actualiza la contraseña del usuario.
        
        Args:
            new_password: Nueva contraseña (ya hasheada).
        """
        self.password = new_password
    
    def to_dict(self) -> dict:
        """
        Convierte el usuario a diccionario para serialización JSON.
        
        Returns:
            dict: Representación del usuario.
        """
        return {
            'id': str(self.id),
            'username': self.username,
            'role_id': str(self.role_id)
        }
    
    def __repr__(self) -> str:
        """Representación en string del usuario."""
        return f"User(id={self.id}, username='{self.username}')"
