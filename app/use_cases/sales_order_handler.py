"""
SalesOrderHandler - Use Case Layer (Refactored with BaseHandler)
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.sales_order import SalesOrder
from app.use_cases.base_handler import BaseHandler


class SalesOrderHandler(BaseHandler):
    """
    Handler para gestionar operaciones con sales orders.
    
    Hereda CRUD genérico de BaseHandler.
    """
    
    def __init__(self):
        """Inicializa con el modelo SalesOrder."""
        super().__init__(SalesOrder)
    
    # Métodos específicos del dominio SalesOrder
    
    def list_all_with_items(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista órdenes con eager loading de items (optimizado para evitar N+1).
        
        Args:
            page (int): Número de página
            per_page (int): Items por página
            status (str): Filtrar por status
        
        Returns:
            dict: Resultado paginado con órdenes e items cargados
        """
        query = SalesOrder.query
        
        # Eager load items para evitar N+1 queries
        if hasattr(SalesOrder, 'items'):
            query = query.options(joinedload(SalesOrder.items))
        
        if status and hasattr(SalesOrder, 'status'):
            query = query.filter_by(status=status)
        
        if hasattr(SalesOrder, 'creation_date'):
            query = query.order_by(SalesOrder.creation_date.desc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def confirm(self, id: int) -> Optional[SalesOrder]:
        """Confirma una orden de venta."""
        return self.update(id, status='confirmed')
    
    def ship(self, id: int) -> Optional[SalesOrder]:
        """Marca una orden como enviada."""
        return self.update(id, status='shipped')
    
    def deliver(self, id: int) -> Optional[SalesOrder]:
        """Marca una orden como entregada."""
        return self.update(id, status='delivered')
    
    def cancel(self, id: int) -> Optional[SalesOrder]:
        """Cancela una orden de venta."""
        return self.update(id, status='cancelled')
