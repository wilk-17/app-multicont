"""
InvoiceItemHandler - Use Case Layer
Gestiona items de factura.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.invoice_item import InvoiceItem
from app.use_cases.base_handler import BaseHandler


class InvoiceItemHandler(BaseHandler):
    """Handler para gestionar operaciones con items de factura."""
    
    def __init__(self):
        super().__init__(InvoiceItem)
    
    def get_by_invoice(self, invoice_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todos los items de una factura específica.
        
        Args:
            invoice_id: ID de la factura
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con items paginados
        """
        query = InvoiceItem.query.filter_by(invoice_id=invoice_id)
        query = query.order_by(InvoiceItem.id)
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
        Obtiene todas las facturas que incluyen un item específico.
        
        Args:
            item_id: ID del item de inventario
        
        Returns:
            Lista de invoice items
        """
        return InvoiceItem.query.filter_by(inventory_item_id=item_id).all()
    
    def calculate_total(self, invoice_id: int) -> float:
        """
        Calcula el total de todos los items de una factura.
        
        Args:
            invoice_id: ID de la factura
        
        Returns:
            Total calculado
        """
        from sqlalchemy import func
        total = InvoiceItem.query.filter_by(invoice_id=invoice_id).with_entities(
            func.sum(InvoiceItem.quantity * InvoiceItem.unit_price)
        ).scalar()
        return float(total) if total else 0.0
