"""
SalesOrderHandler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.sales_order import SalesOrder

class SalesOrderHandler:
    """Handler para gestionar operaciones con sales orders."""
    
    def create(self, **kwargs) -> SalesOrder:
        """Crea un nuevo orden de venta."""
        try:
            obj = SalesOrder(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear orden de venta: {str(e)}")
    
    def get(self, id: int) -> Optional[SalesOrder]:
        """Obtiene un orden de venta por ID."""
        return SalesOrder.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista sales orders con paginación."""
        query = SalesOrder.query
        if status and hasattr(SalesOrder, 'status'):
            query = query.filter_by(status=status)
        if hasattr(SalesOrder, 'creation_date'):
            query = query.order_by(SalesOrder.creation_date.desc())
        else:
            query = query.order_by(SalesOrder.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id: int, **kwargs) -> SalesOrder:
        """Actualiza un orden de venta."""
        obj = SalesOrder.query.get(id)
        if not obj:
            raise ValueError(f"SalesOrder con ID '{id}' no existe")
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
        """Elimina un orden de venta."""
        obj = SalesOrder.query.get(id)
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
        """Cuenta sales orders."""
        query = SalesOrder.query
        if status and hasattr(SalesOrder, 'status'):
            query = query.filter_by(status=status)
        return query.count()
