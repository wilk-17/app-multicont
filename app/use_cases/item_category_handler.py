"""
ItemCategoryHandler - Use Case Layer
Gestiona categorías de productos del inventario.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.item_category import ItemCategory
from app.use_cases.base_handler import BaseHandler


class ItemCategoryHandler(BaseHandler):
    """Handler para gestionar operaciones con categorías de items."""
    
    def __init__(self):
        super().__init__(ItemCategory)
    
    def list_all_with_items(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista categorías con eager loading de items para evitar N+1 queries.
        
        Args:
            page: Número de página
            per_page: Items por página
            status: Filtrar por estado (opcional)
        
        Returns:
            Dict con items, total, page, per_page, total_pages
        """
        query = ItemCategory.query.options(joinedload(ItemCategory.items))
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(ItemCategory.name)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_by_name(self, name: str) -> Optional[ItemCategory]:
        """
        Busca una categoría por nombre.
        
        Args:
            name: Nombre de la categoría
        
        Returns:
            ItemCategory si existe, None si no
        """
        return ItemCategory.query.filter_by(name=name).first()
    
    def get_categories_with_items_count(self) -> list:
        """
        Obtiene todas las categorías con el conteo de items en cada una.
        
        Returns:
            Lista de categorías con metadata de conteo
        """
        from app.entities.inventory_item import InventoryItem
        from sqlalchemy import func
        
        categories = ItemCategory.query.outerjoin(InventoryItem).group_by(ItemCategory.id).all()
        
        result = []
        for category in categories:
            items_count = InventoryItem.query.filter_by(category_id=category.id).count()
            category_dict = category.to_dict() if hasattr(category, 'to_dict') else {'id': category.id, 'name': category.name}
            category_dict['items_count'] = items_count
            result.append(category_dict)
        
        return result
