"""
EmployeeHandler - Use Case Layer (Refactored with BaseHandler)
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import joinedload
from app.entities.employee import Employee
from app.use_cases.base_handler import BaseHandler


class EmployeeHandler(BaseHandler):
    """
    Handler para gestionar operaciones con employees.
    
    Hereda CRUD genérico de BaseHandler.
    """
    
    def __init__(self):
        """Inicializa con el modelo Employee."""
        super().__init__(Employee)
    
    # Métodos específicos del dominio Employee
    
    def get_by_branch(self, branch_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista empleados de una sucursal específica.
        
        Args:
            branch_id (int): ID de la sucursal
            page (int): Número de página
            per_page (int): Items por página
        
        Returns:
            dict: Resultado paginado con empleados de la sucursal
        """
        return self.list_all(page=page, per_page=per_page, branch_id=branch_id)
    
    def list_all_with_branch(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista empleados con eager loading de sucursal (optimizado para evitar N+1).
        
        Args:
            page (int): Número de página
            per_page (int): Items por página
            status (str): Filtrar por status
        
        Returns:
            dict: Resultado paginado con empleados y sucursales cargadas
        """
        query = Employee.query
        
        # Eager load branch para evitar N+1 queries
        if hasattr(Employee, 'branch'):
            query = query.options(joinedload(Employee.branch))
        
        if status and hasattr(Employee, 'status'):
            query = query.filter_by(status=status)
        
        if hasattr(Employee, 'creation_date'):
            query = query.order_by(Employee.creation_date.desc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def activate(self, id: int) -> Optional[Employee]:
        """Activa un empleado."""
        return self.update(id, status='active')
    
    def deactivate(self, id: int) -> Optional[Employee]:
        """Desactiva un empleado."""
        return self.update(id, status='inactive')
