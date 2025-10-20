"""
AssignmentHandler - Use Case Layer
Gestiona asignaciones de items de inventario a empleados con trazabilidad completa.
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import joinedload
from app.entities.assignment import Assignment
from app.use_cases.base_handler import BaseHandler
from app import db


class AssignmentHandler(BaseHandler):
    """Handler para gestionar operaciones con asignaciones."""
    
    def __init__(self):
        super().__init__(Assignment)
    
    def get_by_employee(self, employee_id: int, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene todas las asignaciones de un empleado específico.
        
        Args:
            employee_id: ID del empleado
            page: Número de página
            per_page: Items por página
            status: Filtrar por status (active, returned, lost)
        
        Returns:
            Dict con asignaciones paginadas
        """
        query = Assignment.query.filter_by(employee_id=employee_id)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Assignment.creation_date.desc() if hasattr(Assignment, 'creation_date') else Assignment.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_employee_history(self, employee_id: int) -> Dict[str, Any]:
        """
        Obtiene historial completo de asignaciones del empleado.
        
        Returns:
            Dict con estadísticas y asignaciones agrupadas por status
        """
        all_assignments = Assignment.query.filter_by(employee_id=employee_id).all()
        
        active = [a for a in all_assignments if a.status == 'active']
        returned = [a for a in all_assignments if a.status == 'returned']
        lost = [a for a in all_assignments if a.status == 'lost']
        
        return {
            'employee_id': employee_id,
            'summary': {
                'total_assignments': len(all_assignments),
                'active_count': len(active),
                'returned_count': len(returned),
                'lost_count': len(lost)
            },
            'active': [a.to_dict() for a in active],
            'returned': [a.to_dict() for a in returned],
            'lost': [a.to_dict() for a in lost]
        }
    
    def mark_returned(self, assignment_id: int, condition: str = 'good', notes: Optional[str] = None) -> Assignment:
        """Marca una asignación como devuelta"""
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            raise ValueError("Assignment not found")
        
        assignment.mark_returned(condition=condition, notes=notes)
        db.session.commit()
        return assignment
    
    def mark_lost(self, assignment_id: int, notes: Optional[str] = None) -> Assignment:
        """Marca una asignación como perdida"""
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            raise ValueError("Assignment not found")
        
        assignment.mark_lost(notes=notes)
        db.session.commit()
        return assignment
    
    def get_by_item(self, inventory_item_id: int) -> List[Assignment]:
        """
        Obtiene todas las asignaciones de un item de inventario específico.
        
        Args:
            inventory_item_id: ID del item de inventario
        
        Returns:
            Lista de asignaciones del item
        """
        return Assignment.query.filter_by(item_id=inventory_item_id).all()
    
    def list_all_with_relations(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista asignaciones con empleado e item (eager loading).
        
        Args:
            page: Número de página
            per_page: Items por página
            status: Filtrar por status
        
        Returns:
            Dict con asignaciones paginadas incluyendo relaciones
        """
        query = Assignment.query.options(
            joinedload(Assignment.employee),
            joinedload(Assignment.inventory_item)
        )
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Assignment.creation_date.desc() if hasattr(Assignment, 'creation_date') else Assignment.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
