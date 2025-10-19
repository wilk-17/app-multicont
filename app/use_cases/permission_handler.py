"""
PermissionHandler - Use Case Layer
Gestiona permisos del sistema para control de acceso.
"""
from typing import Optional, List
from app.entities.permission import Permission
from app.use_cases.base_handler import BaseHandler


class PermissionHandler(BaseHandler):
    """Handler para gestionar operaciones con permisos."""
    
    def __init__(self):
        super().__init__(Permission)
    
    def get_by_name(self, name: str) -> Optional[Permission]:
        """
        Busca un permiso por nombre.
        
        Args:
            name: Nombre del permiso (ej: 'CREATE_USER', 'DELETE_INVOICE')
        
        Returns:
            Permission si existe, None si no
        """
        return Permission.query.filter_by(name=name).first()
    
    def get_by_module(self, module: str) -> List[Permission]:
        """
        Obtiene todos los permisos de un módulo específico.
        
        Args:
            module: Nombre del módulo (ej: 'users', 'inventory', 'sales')
        
        Returns:
            Lista de permisos del módulo
        """
        return Permission.query.filter_by(module=module).all() if hasattr(Permission, 'module') else []
    
    def get_all_permissions(self) -> List[Permission]:
        """
        Obtiene todos los permisos del sistema sin paginación.
        
        Returns:
            Lista completa de permisos
        """
        return Permission.query.order_by(Permission.name).all()
