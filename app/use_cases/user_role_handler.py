"""
UserRoleHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.user_role import UserRole

class UserRoleHandler:
    """Handler para gestionar operaciones con user roles."""
    
    def create(self, **kwargs) -> UserRole:
        """Crea un nuevo rol de usuario."""
        try:
            obj = UserRole(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear rol de usuario: {str(e)}")
    
    def get(self, id: int) -> Optional[UserRole]:
        """Obtiene un rol de usuario por ID."""
        return UserRole.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista user roles con paginación."""
        query = UserRole.query
        if status and hasattr(UserRole, 'status'):
            query = query.filter_by(status=status)
        if hasattr(UserRole, 'creation_date'):
            query = query.order_by(UserRole.creation_date.desc())
        else:
            query = query.order_by(UserRole.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> UserRole:
        """Actualiza un rol de usuario."""
        obj = UserRole.query.get(id)
        if not obj:
            raise ValueError(f"UserRole con ID '{id}' no existe")
        try:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar: {str(e)}")
    
    def delete(self, id: int) -> bool:
        """Elimina un rol de usuario."""
        obj = UserRole.query.get(id)
        if not obj:
            return False
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar: {str(e)}")
    
    def count(self, status: Optional[str] = None) -> int:
        """Cuenta user roles."""
        query = UserRole.query
        if status and hasattr(UserRole, 'status'):
            query = query.filter_by(status=status)
        return query.count()
