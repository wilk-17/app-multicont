"""
InventoryItemHandler - Use Case Layer (Refactored with BaseHandler)
"""
from typing import Optional, Dict, Any
from app.entities.inventory_item import InventoryItem
from app.use_cases.base_handler import BaseHandler


class InventoryItemHandler(BaseHandler):
    """
    Handler para gestionar operaciones con inventory items.
    
    Hereda CRUD genérico de BaseHandler.
    """
    
    def __init__(self):
        """Inicializa con el modelo InventoryItem."""
        super().__init__(InventoryItem)
    
    # Métodos específicos del dominio InventoryItem
    
    def get_low_stock_items(self, threshold: int = 10, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene items con stock bajo.
        
        Args:
            threshold (int): Cantidad mínima de stock
            page (int): Número de página
            per_page (int): Items por página
        
        Returns:
            dict: Resultado paginado con items de stock bajo
        """
        query = InventoryItem.query.filter(InventoryItem.quantity < threshold)
        query = query.order_by(InventoryItem.quantity.asc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def add_stock(self, id: int, quantity: int) -> Optional[InventoryItem]:
        """
        Añade stock a un item.
        
        Args:
            id (int): ID del item
            quantity (int): Cantidad a añadir
        
        Returns:
            InventoryItem: Item actualizado o None
        """
        item = self.get(id)
        if not item:
            return None
        
        current_quantity = getattr(item, 'quantity', 0)
        return self.update(id, quantity=current_quantity + quantity)
    
    def remove_stock(self, id: int, quantity: int) -> Optional[InventoryItem]:
        """
        Remueve stock de un item.
        
        Args:
            id (int): ID del item
            quantity (int): Cantidad a remover
        
        Returns:
            InventoryItem: Item actualizado o None
        
        Raises:
            ValueError: Si no hay suficiente stock
        """
        item = self.get(id)
        if not item:
            return None
        
        current_quantity = getattr(item, 'quantity', 0)
        if current_quantity < quantity:
            raise ValueError(f"Stock insuficiente. Disponible: {current_quantity}, Requerido: {quantity}")
        
        return self.update(id, quantity=current_quantity - quantity)
