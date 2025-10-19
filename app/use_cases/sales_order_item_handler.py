"""
SalesOrderItemHandler - Use Case Layer
Gestiona items de orden de venta.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.sales_order_item import SalesOrderItem
from app.use_cases.base_handler import BaseHandler


class SalesOrderItemHandler(BaseHandler):
    """Handler para gestionar operaciones con items de orden de venta."""
    
    def __init__(self):
        super().__init__(SalesOrderItem)
    
    def get_by_order(self, order_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todos los items de una orden de venta específica.
        
        Args:
            order_id: ID de la orden de venta
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con items paginados
        """
        query = SalesOrderItem.query.filter_by(sales_order_id=order_id)
        query = query.order_by(SalesOrderItem.id)
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
        Obtiene todas las órdenes de venta que incluyen un item específico.
        
        Args:
            item_id: ID del item de inventario
        
        Returns:
            Lista de sales order items
        """
        return SalesOrderItem.query.filter_by(inventory_item_id=item_id).all()
    
    def calculate_total(self, order_id: int) -> float:
        """
        Calcula el total de todos los items de una orden de venta.
        
        Args:
            order_id: ID de la orden de venta
        
        Returns:
            Total calculado
        """
        from sqlalchemy import func
        total = SalesOrderItem.query.filter_by(sales_order_id=order_id).with_entities(
            func.sum(SalesOrderItem.quantity * SalesOrderItem.unit_price)
        ).scalar()
        return float(total) if total else 0.0
