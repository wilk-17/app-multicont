"""
CityHandler - Use Case Layer
Gestiona ciudades asociadas a estados.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import joinedload
from app.entities.city import City
from app.use_cases.base_handler import BaseHandler


class CityHandler(BaseHandler):
    """Handler para gestionar operaciones con ciudades."""
    
    def __init__(self):
        super().__init__(City)
    
    def get_by_state(self, state_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todas las ciudades de un estado específico.
        
        Args:
            state_id: ID del estado
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con ciudades paginadas
        """
        query = City.query.filter_by(state_id=state_id)
        query = query.order_by(City.name)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def list_all_with_state(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista ciudades con su estado (eager loading).
        
        Args:
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con ciudades paginadas incluyendo estado
        """
        query = City.query.options(joinedload(City.state))
        query = query.order_by(City.name)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def search_by_name(self, search_term: str, state_id: Optional[int] = None) -> List[City]:
        """
        Busca ciudades por nombre (búsqueda parcial).
        
        Args:
            search_term: Término de búsqueda
            state_id: Filtrar por estado (opcional)
        
        Returns:
            Lista de ciudades que coinciden
        """
        query = City.query.filter(City.name.ilike(f'%{search_term}%'))
        if state_id:
            query = query.filter_by(state_id=state_id)
        return query.order_by(City.name).all()
