"""
InvoiceItemHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.invoice_item import InvoiceItem

class InvoiceItemHandler:
    """Handler para gestionar operaciones con invoice items."""
    
    def create(self, **kwargs) -> InvoiceItem:
        """Crea un nuevo item de factura."""
        try:
            obj = InvoiceItem(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear item de factura: {str(e)}")
    
    def get(self, id: int) -> Optional[InvoiceItem]:
        """Obtiene un item de factura por ID."""
        return InvoiceItem.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista invoice items con paginación."""
        query = InvoiceItem.query
        if status and hasattr(InvoiceItem, 'status'):
            query = query.filter_by(status=status)
        query = query.order_by(InvoiceItem.creation_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> InvoiceItem:
        """Actualiza un item de factura."""
        obj = InvoiceItem.query.get(id)
        if not obj:
            raise ValueError(f"InvoiceItem con ID '{id}' no existe")
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
        """Elimina un item de factura."""
        obj = InvoiceItem.query.get(id)
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
        """Cuenta invoice items."""
        query = InvoiceItem.query
        if status and hasattr(InvoiceItem, 'status'):
            query = query.filter_by(status=status)
        return query.count()
