"""
QuoteItemHandler - Use Case Layer
Gestiona items de cotización.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.quote_item import QuoteItem
from app.use_cases.base_handler import BaseHandler


class QuoteItemHandler(BaseHandler):
    """Handler para gestionar operaciones con items de cotización."""
    
    def __init__(self):
        super().__init__(QuoteItem)
    
    def get_by_quote(self, quote_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todos los items de una cotización específica.
        
        Args:
            quote_id: ID de la cotización
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con items paginados
        """
        query = QuoteItem.query.filter_by(quote_id=quote_id)
        query = query.order_by(QuoteItem.id)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_by_inventory_item(self, item_id: int) -> list:
        """
        Obtiene todas las cotizaciones que incluyen un item específico.
        
        Args:
            item_id: ID del item de inventario
        
        Returns:
            Lista de quote items
        """
        return QuoteItem.query.filter_by(inventory_item_id=item_id).all()
    
    def calculate_total(self, quote_id: int) -> float:
        """
        Calcula el total de todos los items de una cotización.
        
        Args:
            quote_id: ID de la cotización
        
        Returns:
            Total calculado
        """
        from sqlalchemy import func
        total = QuoteItem.query.filter_by(quote_id=quote_id).with_entities(
            func.sum(QuoteItem.quantity * QuoteItem.unit_price)
        ).scalar()
        return float(total) if total else 0.0
