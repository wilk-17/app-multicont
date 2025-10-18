"""
Brand Handler - Lógica de negocio para marcas de productos
"""
from app import db
from app.entities.brand import Brand


class BrandHandler:
    """Handler para gestión de marcas de productos"""
    
    def create(self, name, description=None):
        """
        Crear una nueva marca
        
        Args:
            name: Nombre de la marca (único)
            description: Descripción opcional
            
        Returns:
            Brand: Objeto Brand creado
            
        Raises:
            ValueError: Si la marca ya existe
        """
        existing = Brand.query.filter_by(name=name).first()
        if existing:
            raise ValueError(f"Brand with name '{name}' already exists")
        
        brand = Brand(name=name, description=description)
        db.session.add(brand)
        db.session.commit()
        return brand
    
    def get(self, brand_id):
        """
        Obtener marca por ID
        
        Args:
            brand_id: ID de la marca
            
        Returns:
            Brand o None si no existe
        """
        return Brand.query.get(brand_id)
    
    def get_by_name(self, name):
        """
        Obtener marca por nombre
        
        Args:
            name: Nombre de la marca
            
        Returns:
            Brand o None si no existe
        """
        return Brand.query.filter_by(name=name).first()
    
    def list_all(self, page=1, per_page=10):
        """
        Listar todas las marcas con paginación
        
        Args:
            page: Número de página
            per_page: Items por página
            
        Returns:
            dict con items, total, page, per_page, total_pages
        """
        query = Brand.query.order_by(Brand.name.asc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, brand_id, **kwargs):
        """
        Actualizar marca
        
        Args:
            brand_id: ID de la marca
            **kwargs: Campos a actualizar (name, description)
            
        Returns:
            Brand actualizado
            
        Raises:
            ValueError: Si la marca no existe o nombre duplicado
        """
        brand = Brand.query.get(brand_id)
        if not brand:
            raise ValueError(f"Brand with id {brand_id} not found")
        
        # Validar nombre único si se está actualizando
        if 'name' in kwargs and kwargs['name'] != brand.name:
            existing = Brand.query.filter_by(name=kwargs['name']).first()
            if existing:
                raise ValueError(f"Brand with name '{kwargs['name']}' already exists")
        
        # Actualizar campos permitidos
        for key, value in kwargs.items():
            if hasattr(brand, key) and key != 'id':
                setattr(brand, key, value)
        
        db.session.commit()
        return brand
    
    def delete(self, brand_id):
        """
        Eliminar marca
        
        Args:
            brand_id: ID de la marca
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValueError: Si la marca no existe o tiene items asociados
        """
        brand = Brand.query.get(brand_id)
        if not brand:
            raise ValueError(f"Brand with id {brand_id} not found")
        
        # Verificar si tiene items asociados
        from app.entities.inventory_item import InventoryItem
        items_count = InventoryItem.query.filter_by(brand_id=brand_id).count()
        if items_count > 0:
            raise ValueError(f"Cannot delete brand: {items_count} inventory items are associated")
        
        db.session.delete(brand)
        db.session.commit()
        return True
    
    def count(self):
        """
        Contar total de marcas
        
        Returns:
            int: Total de marcas
        """
        return Brand.query.count()
