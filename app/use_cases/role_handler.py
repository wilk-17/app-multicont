"""
RoleHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.role import Role

class RoleHandler:
    """Handler para gestionar operaciones con roles."""
    
    def create(self, **kwargs) -> Role:
        """Crea un nuevo rol."""
        try:
            obj = Role(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear rol: {str(e)}")
    
    def get(self, id: int) -> Optional[Role]:
        """Obtiene un rol por ID."""
        return Role.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista roles con paginación."""
        query = Role.query
        if status and hasattr(Role, 'status'):
            query = query.filter_by(status=status)
        query = query.order_by(Role.creation_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> Role:
        """Actualiza un rol."""
        obj = Role.query.get(id)
        if not obj:
            raise ValueError(f"Role con ID '{id}' no existe")
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
        """Elimina un rol."""
        obj = Role.query.get(id)
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
        """Cuenta roles."""
        query = Role.query
        if status and hasattr(Role, 'status'):
            query = query.filter_by(status=status)
        return query.count()
