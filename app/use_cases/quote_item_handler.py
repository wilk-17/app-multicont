"""
QuoteItemHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.quote_item import QuoteItem

class QuoteItemHandler:
    """Handler para gestionar operaciones con quote items."""
    
    def create(self, **kwargs) -> QuoteItem:
        """Crea un nuevo item de cotización."""
        try:
            obj = QuoteItem(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear item de cotización: {str(e)}")
    
    def get(self, id: int) -> Optional[QuoteItem]:
        """Obtiene un item de cotización por ID."""
        return QuoteItem.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista quote items con paginación."""
        query = QuoteItem.query
        if status and hasattr(QuoteItem, 'status'):
            query = query.filter_by(status=status)
        if hasattr(QuoteItem, 'creation_date'):
            query = query.order_by(QuoteItem.creation_date.desc())
        else:
            query = query.order_by(QuoteItem.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> QuoteItem:
        """Actualiza un item de cotización."""
        obj = QuoteItem.query.get(id)
        if not obj:
            raise ValueError(f"QuoteItem con ID '{id}' no existe")
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
        """Elimina un item de cotización."""
        obj = QuoteItem.query.get(id)
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
        """Cuenta quote items."""
        query = QuoteItem.query
        if status and hasattr(QuoteItem, 'status'):
            query = query.filter_by(status=status)
        return query.count()
