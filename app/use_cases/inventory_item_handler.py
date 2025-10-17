"""
InventoryItemHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.inventory_item import InventoryItem

class InventoryItemHandler:
    """Handler para gestionar operaciones con inventory items."""
    
    def create(self, **kwargs) -> InventoryItem:
        """Crea un nuevo item de inventario."""
        try:
            obj = InventoryItem(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear item de inventario: {str(e)}")
    
    def get(self, id: int) -> Optional[InventoryItem]:
        """Obtiene un item de inventario por ID."""
        return InventoryItem.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista inventory items con paginación."""
        query = InventoryItem.query
        if status and hasattr(InventoryItem, 'status'):
            query = query.filter_by(status=status)
        query = query.order_by(InventoryItem.creation_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> InventoryItem:
        """Actualiza un item de inventario."""
        obj = InventoryItem.query.get(id)
        if not obj:
            raise ValueError(f"InventoryItem con ID '{id}' no existe")
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
        """Elimina un item de inventario."""
        obj = InventoryItem.query.get(id)
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
        """Cuenta inventory items."""
        query = InventoryItem.query
        if status and hasattr(InventoryItem, 'status'):
            query = query.filter_by(status=status)
        return query.count()
