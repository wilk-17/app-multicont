"""
BranchHandler - Use Case Layer
Gestiona sucursales con relaciones a organizaciones.
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.branch import Branch
from app.use_cases.base_handler import BaseHandler


class BranchHandler(BaseHandler):
    """Handler para gestionar operaciones con sucursales (branches)."""
    
    def __init__(self):
        super().__init__(Branch)
    
    def list_all_with_organization(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista branches con eager loading de organization para evitar N+1 queries.
        
        Args:
            page: Número de página
            per_page: Items por página
            status: Filtrar por estado (opcional)
        
        Returns:
            Dict con items, total, page, per_page, total_pages
        """
        query = Branch.query.options(joinedload(Branch.organization))
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(Branch.creation_date.desc() if hasattr(Branch, 'creation_date') else Branch.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_by_organization(self, organization_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todas las sucursales de una organización.
        
        Args:
            organization_id: ID de la organización
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con sucursales paginadas
        """
        query = Branch.query.filter_by(organization_id=organization_id)
        query = query.order_by(Branch.creation_date.desc() if hasattr(Branch, 'creation_date') else Branch.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def activate(self, id: int) -> Branch:
        """Activa una sucursal."""
        return self.update(id, status='active')
    
    def deactivate(self, id: int) -> Branch:
        """Desactiva una sucursal."""
        return self.update(id, status='inactive')
