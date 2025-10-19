"""
AssignmentHandler - Use Case Layer
Gestiona asignaciones de items de inventario a empleados.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import joinedload
from app.entities.assignment import Assignment
from app.use_cases.base_handler import BaseHandler


class AssignmentHandler(BaseHandler):
    """Handler para gestionar operaciones con asignaciones."""
    
    def __init__(self):
        super().__init__(Assignment)
    
    def get_by_employee(self, employee_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtiene todas las asignaciones de un empleado específico.
        
        Args:
            employee_id: ID del empleado
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con asignaciones paginadas
        """
        query = Assignment.query.filter_by(employee_id=employee_id)
        query = query.order_by(Assignment.creation_date.desc() if hasattr(Assignment, 'creation_date') else Assignment.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_by_item(self, inventory_item_id: int) -> List[Assignment]:
        """
        Obtiene todas las asignaciones de un item de inventario específico.
        
        Args:
            inventory_item_id: ID del item de inventario
        
        Returns:
            Lista de asignaciones del item
        """
        return Assignment.query.filter_by(inventory_item_id=inventory_item_id).all()
    
    def list_all_with_relations(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista asignaciones con empleado e item (eager loading).
        
        Args:
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con asignaciones paginadas incluyendo relaciones
        """
        query = Assignment.query.options(
            joinedload(Assignment.employee),
            joinedload(Assignment.inventory_item)
        )
        query = query.order_by(Assignment.creation_date.desc() if hasattr(Assignment, 'creation_date') else Assignment.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
