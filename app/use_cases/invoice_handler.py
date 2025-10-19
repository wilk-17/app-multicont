"""
InvoiceHandler - Use Case Layer (Refactored with BaseHandler)
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.invoice import Invoice
from app.use_cases.base_handler import BaseHandler


class InvoiceHandler(BaseHandler):
    """
    Handler para gestionar operaciones con invoices.
    
    Hereda CRUD genérico de BaseHandler.
    """
    
    def __init__(self):
        """Inicializa con el modelo Invoice."""
        super().__init__(Invoice)
    
    # Métodos específicos del dominio Invoice
    
    def list_all_with_items(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista facturas con eager loading de items (optimizado para evitar N+1).
        
        Args:
            page (int): Número de página
            per_page (int): Items por página
            status (str): Filtrar por status
        
        Returns:
            dict: Resultado paginado con facturas e items cargados
        """
        query = Invoice.query
        
        # Eager load items para evitar N+1 queries
        if hasattr(Invoice, 'items'):
            query = query.options(joinedload(Invoice.items))
        
        if status and hasattr(Invoice, 'status'):
            query = query.filter_by(status=status)
        
        if hasattr(Invoice, 'creation_date'):
            query = query.order_by(Invoice.creation_date.desc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def mark_as_paid(self, id: int) -> Optional[Invoice]:
        """Marca una factura como pagada."""
        return self.update(id, status='paid')
    
    def mark_as_pending(self, id: int) -> Optional[Invoice]:
        """Marca una factura como pendiente."""
        return self.update(id, status='pending')
    
    def mark_as_cancelled(self, id: int) -> Optional[Invoice]:
        """Marca una factura como cancelada."""
        return self.update(id, status='cancelled')
    
    def get_by_customer(self, customer_name: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista facturas de un cliente específico.
        
        Args:
            customer_name (str): Nombre del cliente
            page (int): Número de página
            per_page (int): Items por página
        
        Returns:
            dict: Resultado paginado con facturas del cliente
        """
        query = Invoice.query
        
        if hasattr(Invoice, 'customer_name'):
            query = query.filter(Invoice.customer_name.ilike(f'%{customer_name}%'))
        
        if hasattr(Invoice, 'creation_date'):
            query = query.order_by(Invoice.creation_date.desc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
