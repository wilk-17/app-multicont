"""
QuotationLineHandler - Use Case Layer
Gestiona líneas de cotización (items en una cotización).
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.quotation_line import QuotationLine
from app.use_cases.base_handler import BaseHandler


class QuotationLineHandler(BaseHandler):
    """Handler para gestionar operaciones con líneas de cotización."""
    
    def __init__(self):
        super().__init__(QuotationLine)
    
    def get_by_quote(self, quote_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todas las líneas de una cotización específica.
        
        Args:
            quote_id: ID de la cotización
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con líneas paginadas
        """
        query = QuotationLine.query.filter_by(quote_id=quote_id)
        query = query.order_by(QuotationLine.id)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def calculate_total(self, quote_id: int) -> float:
        """
        Calcula el total de todas las líneas de una cotización.
        
        Args:
            quote_id: ID de la cotización
        
        Returns:
            Total calculado
        """
        from sqlalchemy import func
        total = QuotationLine.query.filter_by(quote_id=quote_id).with_entities(
            func.sum(QuotationLine.quantity * QuotationLine.unit_price)
        ).scalar()
        return float(total) if total else 0.0
