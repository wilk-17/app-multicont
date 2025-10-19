"""
OrganizationHandler - Use Case Layer (Refactored with BaseHandler)
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.organization import Organization
from app.use_cases.base_handler import BaseHandler


class OrganizationHandler(BaseHandler):
    """
    Handler para gestionar operaciones con organizations.
    
    Hereda CRUD genérico de BaseHandler.
    """
    
    def __init__(self):
        """Inicializa con el modelo Organization."""
        super().__init__(Organization)
    
    # Métodos específicos del dominio Organization
    
    def get_by_name(self, name: str) -> Optional[Organization]:
        """
        Busca una organización por nombre actual.
        
        Args:
            name (str): Nombre de la organización
        
        Returns:
            Organization: Organización encontrada o None
        """
        if hasattr(Organization, 'current_name'):
            return Organization.query.filter_by(current_name=name).first()
        return None
    
    def list_all_with_branches(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista organizaciones con eager loading de sucursales (optimizado).
        
        Args:
            page (int): Número de página
            per_page (int): Items por página
        
        Returns:
            dict: Resultado paginado con organizaciones y sucursales cargadas
        """
        query = Organization.query
        
        # Eager load branches para evitar N+1 queries
        if hasattr(Organization, 'branches'):
            query = query.options(joinedload(Organization.branches))
        
        if hasattr(Organization, 'creation_date'):
            query = query.order_by(Organization.creation_date.desc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def activate(self, id: int) -> Optional[Organization]:
        """Activa una organización."""
        return self.update(id, status='active')
    
    def deactivate(self, id: int) -> Optional[Organization]:
        """Desactiva una organización."""
        return self.update(id, status='inactive')
