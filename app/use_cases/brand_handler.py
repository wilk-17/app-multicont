"""
BrandHandler - Use Case Layer
Gestiona marcas de productos con validaciones de integridad.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app import db
from app.entities.brand import Brand
from app.use_cases.base_handler import BaseHandler


class BrandHandler(BaseHandler):
    """Handler para gestión de marcas de productos con validación de unicidad."""
    
    def __init__(self):
        super().__init__(Brand)
    
    def create(self, name: str, description: Optional[str] = None, **kwargs) -> Brand:
        """
        Crear una nueva marca con validación de unicidad.
        
        Args:
            name: Nombre de la marca (único)
            description: Descripción opcional
            **kwargs: Otros campos opcionales
            
        Returns:
            Brand: Objeto Brand creado
            
        Raises:
            ValueError: Si la marca ya existe
        """
        existing = self.get_by_name(name)
        if existing:
            raise ValueError(f"Brand with name '{name}' already exists")
        
        return super().create(name=name, description=description, **kwargs)
    
    def get_by_name(self, name: str) -> Optional[Brand]:
        """
        Obtener marca por nombre.
        
        Args:
            name: Nombre de la marca
            
        Returns:
            Brand o None si no existe
        """
        return Brand.query.filter_by(name=name).first()
    
    def list_all_with_items(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista marcas con eager loading de items para evitar N+1 queries.
        
        Args:
            page: Número de página
            per_page: Items por página
            
        Returns:
            Dict con items, total, page, per_page, total_pages
        """
        query = Brand.query.options(joinedload(Brand.items))
        query = query.order_by(Brand.name.asc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, brand_id: int, **kwargs) -> Brand:
        """
        Actualizar marca con validación de unicidad de nombre.
        
        Args:
            brand_id: ID de la marca
            **kwargs: Campos a actualizar (name, description)
            
        Returns:
            Brand actualizado
            
        Raises:
            ValueError: Si la marca no existe o nombre duplicado
        """
        brand = self.get(brand_id)
        if not brand:
            raise ValueError(f"Brand with id {brand_id} not found")
        
        # Validar nombre único si se está actualizando
        if 'name' in kwargs and kwargs['name'] != brand.name:
            existing = self.get_by_name(kwargs['name'])
            if existing:
                raise ValueError(f"Brand with name '{kwargs['name']}' already exists")
        
        return super().update(brand_id, **kwargs)
    
    def delete(self, brand_id: int) -> bool:
        """
        Eliminar marca verificando que no tenga items asociados.
        
        Args:
            brand_id: ID de la marca
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValueError: Si la marca tiene items asociados
        """
        brand = self.get(brand_id)
        if not brand:
            raise ValueError(f"Brand with id {brand_id} not found")
        
        # Verificar si tiene items asociados
        from app.entities.inventory_item import InventoryItem
        items_count = InventoryItem.query.filter_by(brand_id=brand_id).count()
        if items_count > 0:
            raise ValueError(f"Cannot delete brand: {items_count} inventory items are associated")
        
        return super().delete(brand_id)
    
    def get_brands_with_items_count(self) -> list:
        """
        Obtiene todas las marcas con el conteo de items de cada una.
        
        Returns:
            Lista de marcas con metadata de conteo
        """
        from app.entities.inventory_item import InventoryItem
        
        brands = Brand.query.all()
        result = []
        
        for brand in brands:
            items_count = InventoryItem.query.filter_by(brand_id=brand.id).count()
            brand_dict = brand.to_dict() if hasattr(brand, 'to_dict') else {'id': brand.id, 'name': brand.name}
            brand_dict['items_count'] = items_count
            result.append(brand_dict)
        
        return result
