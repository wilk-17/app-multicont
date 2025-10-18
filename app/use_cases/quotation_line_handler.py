"""
QuotationLineHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.quotation_line import QuotationLine

class QuotationLineHandler:
    """Handler para gestionar operaciones con quotation lines."""
    
    def create(self, **kwargs) -> QuotationLine:
        """Crea un nuevo línea de cotización."""
        try:
            obj = QuotationLine(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear línea de cotización: {str(e)}")
    
    def get(self, id: int) -> Optional[QuotationLine]:
        """Obtiene un línea de cotización por ID."""
        return QuotationLine.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista quotation lines con paginación."""
        query = QuotationLine.query
        if status and hasattr(QuotationLine, 'status'):
            query = query.filter_by(status=status)
        if hasattr(QuotationLine, 'creation_date'):
            query = query.order_by(QuotationLine.creation_date.desc())
        else:
            query = query.order_by(QuotationLine.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> QuotationLine:
        """Actualiza un línea de cotización."""
        obj = QuotationLine.query.get(id)
        if not obj:
            raise ValueError(f"QuotationLine con ID '{id}' no existe")
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
        """Elimina un línea de cotización."""
        obj = QuotationLine.query.get(id)
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
        """Cuenta quotation lines."""
        query = QuotationLine.query
        if status and hasattr(QuotationLine, 'status'):
            query = query.filter_by(status=status)
        return query.count()
