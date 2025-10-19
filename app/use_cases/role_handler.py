"""
RoleHandler - Use Case Layer
Gestiona roles del sistema con permisos asociados.
"""
from typing import Optional
from sqlalchemy.orm import joinedload
from app.entities.role import Role
from app.use_cases.base_handler import BaseHandler


class RoleHandler(BaseHandler):
    """Handler para gestionar operaciones con roles."""
    
    def __init__(self):
        super().__init__(Role)
    
    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Busca un rol por nombre.
        
        Args:
            name: Nombre del rol (ej: 'ADMIN', 'MANAGER', 'USER')
        
        Returns:
            Role si existe, None si no
        """
        return Role.query.filter_by(name=name).first()
    
    def get_with_permissions(self, id: int) -> Optional[Role]:
        """
        Obtiene un rol con sus permisos cargados (eager loading).
        
        Args:
            id: ID del rol
        
        Returns:
            Role con permisos cargados
        """
        return Role.query.options(joinedload(Role.permissions)).filter_by(id=id).first()
    
    def get_system_roles(self) -> list:
        """
        Obtiene los roles del sistema (ADMIN, MANAGER, USER).
        
        Returns:
            Lista de roles del sistema
        """
        return Role.query.filter(Role.name.in_(['ADMIN', 'MANAGER', 'USER'])).all()
