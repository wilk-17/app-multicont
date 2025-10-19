"""
UserRoleHandler - Use Case Layer
Gestiona la relación entre usuarios y roles (tabla pivot).
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import joinedload
from app.entities.user_role import UserRole
from app.use_cases.base_handler import BaseHandler


class UserRoleHandler(BaseHandler):
    """Handler para gestionar operaciones con roles de usuario."""
    
    def __init__(self):
        super().__init__(UserRole)
    
    def get_by_user(self, user_id: int) -> List[UserRole]:
        """
        Obtiene todos los roles de un usuario específico.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Lista de UserRole del usuario
        """
        return UserRole.query.filter_by(user_id=user_id).all()
    
    def get_by_role(self, role_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todos los usuarios con un rol específico.
        
        Args:
            role_id: ID del rol
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con user_roles paginados
        """
        query = UserRole.query.filter_by(role_id=role_id)
        query = query.order_by(UserRole.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def list_all_with_relations(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista user_roles con usuario y rol (eager loading).
        
        Args:
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con user_roles paginados incluyendo relaciones
        """
        query = UserRole.query.options(
            joinedload(UserRole.user),
            joinedload(UserRole.role)
        )
        query = query.order_by(UserRole.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def user_has_role(self, user_id: int, role_id: int) -> bool:
        """
        Verifica si un usuario tiene un rol específico.
        
        Args:
            user_id: ID del usuario
            role_id: ID del rol
        
        Returns:
            True si el usuario tiene el rol, False en caso contrario
        """
        return UserRole.query.filter_by(
            user_id=user_id,
            role_id=role_id
        ).first() is not None
