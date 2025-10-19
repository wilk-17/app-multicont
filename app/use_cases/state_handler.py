"""
StateHandler - Use Case Layer
Gestiona estados/departamentos geográficos.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import joinedload
from app.entities.state import State
from app.use_cases.base_handler import BaseHandler


class StateHandler(BaseHandler):
    """Handler para gestionar operaciones con estados."""
    
    def __init__(self):
        super().__init__(State)
    
    def get_by_name(self, name: str) -> Optional[State]:
        """
        Obtiene un estado por su nombre.
        
        Args:
            name: Nombre del estado
        
        Returns:
            State o None si no existe
        """
        return State.query.filter_by(name=name).first()
    
    def list_all_with_cities(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista estados con sus ciudades (eager loading).
        
        Args:
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con estados paginados incluyendo ciudades
        """
        query = State.query.options(joinedload(State.cities))
        query = query.order_by(State.name)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def search_by_name(self, search_term: str) -> List[State]:
        """
        Busca estados por nombre (búsqueda parcial).
        
        Args:
            search_term: Término de búsqueda
        
        Returns:
            Lista de estados que coinciden
        """
        return State.query.filter(
            State.name.ilike(f'%{search_term}%')
        ).order_by(State.name).all()
