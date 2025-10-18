"""
ItemCategoryHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.item_category import ItemCategory

class ItemCategoryHandler:
    """Handler para gestionar operaciones con item categories."""
    
    def create(self, **kwargs) -> ItemCategory:
        """Crea un nuevo categoría."""
        try:
            obj = ItemCategory(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear categoría: {str(e)}")
    
    def get(self, id: int) -> Optional[ItemCategory]:
        """Obtiene un categoría por ID."""
        return ItemCategory.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista item categories con paginación."""
        query = ItemCategory.query
        if status and hasattr(ItemCategory, 'status'):
            query = query.filter_by(status=status)
        if hasattr(ItemCategory, 'creation_date'):
            query = query.order_by(ItemCategory.creation_date.desc())
        else:
            query = query.order_by(ItemCategory.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> ItemCategory:
        """Actualiza un categoría."""
        obj = ItemCategory.query.get(id)
        if not obj:
            raise ValueError(f"ItemCategory con ID '{id}' no existe")
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
        """Elimina un categoría."""
        obj = ItemCategory.query.get(id)
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
        """Cuenta item categories."""
        query = ItemCategory.query
        if status and hasattr(ItemCategory, 'status'):
            query = query.filter_by(status=status)
        return query.count()
