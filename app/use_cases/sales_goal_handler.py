"""
SalesGoal Handler - Lógica de negocio para metas de ventas
"""
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload
from app.entities.sales_goal import SalesGoal
from app.use_cases.base_handler import BaseHandler


class SalesGoalHandler(BaseHandler):
    """Handler para gestión de metas de ventas"""
    
    def __init__(self):
        super().__init__(SalesGoal)
    
    def create(self, period_type: str, start_date, end_date, target_amount: float, 
               employee_id: Optional[int] = None, branch_id: Optional[int] = None, 
               created_by_user_id: Optional[int] = None) -> SalesGoal:
        """
        Crear una nueva meta de ventas con validaciones de negocio.
        
        Args:
            period_type: 'monthly', 'quarterly', 'yearly'
            start_date: Fecha inicio del periodo
            end_date: Fecha fin del periodo
            target_amount: Meta en dinero
            employee_id: ID del empleado (vendedor) - opcional
            branch_id: ID de la sucursal - opcional
            created_by_user_id: ID del usuario que crea la meta (admin)
            
        Returns:
            SalesGoal creado
            
        Raises:
            ValueError: Si validaciones fallan
        """
        # Validar que se especifique employee o branch, no ambos
        if not employee_id and not branch_id:
            raise ValueError("Must specify either employee_id or branch_id")
        if employee_id and branch_id:
            raise ValueError("Cannot specify both employee_id and branch_id")
        
        # Validar periodo
        if period_type not in ['monthly', 'quarterly', 'yearly']:
            raise ValueError("period_type must be 'monthly', 'quarterly', or 'yearly'")
        
        # Validar fechas
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if end_date <= start_date:
            raise ValueError("end_date must be after start_date")
        
        # Validar monto positivo
        if target_amount <= 0:
            raise ValueError("target_amount must be positive")
        
        # Usar el create genérico de BaseHandler
        return super().create(
            period_type=period_type,
            start_date=start_date,
            end_date=end_date,
            target_amount=target_amount,
            employee_id=employee_id,
            branch_id=branch_id,
            created_by_user_id=created_by_user_id
        )
    
    def get_current_goals(self, reference_date: Optional[date] = None) -> List[SalesGoal]:
        """
        Obtener metas activas para una fecha específica.
        
        Args:
            reference_date: Fecha de referencia (default: hoy)
            
        Returns:
            Lista de SalesGoal activos
        """
        if reference_date is None:
            reference_date = date.today()
        elif isinstance(reference_date, str):
            reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
        
        return SalesGoal.query.filter(
            and_(
                SalesGoal.start_date <= reference_date,
                SalesGoal.end_date >= reference_date
            )
        ).all()
    
    def get_goals_by_employee(self, employee_id: int, period_type: Optional[str] = None, 
                              page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtener todas las metas de un empleado.
        
        Args:
            employee_id: ID del empleado
            period_type: Filtrar por tipo de periodo (opcional)
            page: Número de página
            per_page: Items por página
            
        Returns:
            Dict con metas paginadas
        """
        query = SalesGoal.query.filter_by(employee_id=employee_id)
        if period_type:
            query = query.filter_by(period_type=period_type)
        query = query.order_by(SalesGoal.start_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_goals_by_branch(self, branch_id: int, period_type: Optional[str] = None,
                            page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Obtener todas las metas de una sucursal.
        
        Args:
            branch_id: ID de la sucursal
            period_type: Filtrar por tipo de periodo (opcional)
            page: Número de página
            per_page: Items por página
            
        Returns:
            Dict con metas paginadas
        """
        query = SalesGoal.query.filter_by(branch_id=branch_id)
        if period_type:
            query = query.filter_by(period_type=period_type)
        query = query.order_by(SalesGoal.start_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, goal_id: int, **kwargs) -> SalesGoal:
        """
        Actualizar meta de ventas con validaciones.
        
        Args:
            goal_id: ID de la meta
            **kwargs: Campos a actualizar
            
        Returns:
            SalesGoal actualizado
            
        Raises:
            ValueError: Si validaciones fallan
        """
        # Validaciones según campos actualizados
        if 'period_type' in kwargs and kwargs['period_type'] not in ['monthly', 'quarterly', 'yearly']:
            raise ValueError("period_type must be 'monthly', 'quarterly', or 'yearly'")
        
        if 'target_amount' in kwargs and kwargs['target_amount'] <= 0:
            raise ValueError("target_amount must be positive")
        
        # Usar update genérico de BaseHandler
        return super().update(goal_id, **kwargs)
    
    def list_all_with_relations(self, page: int = 1, per_page: int = 10,
                                 period_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista metas con empleado y sucursal (eager loading).
        
        Args:
            page: Número de página
            per_page: Items por página
            period_type: Filtrar por tipo de periodo
        
        Returns:
            Dict con metas paginadas incluyendo relaciones
        """
        query = SalesGoal.query.options(
            joinedload(SalesGoal.employee),
            joinedload(SalesGoal.branch)
        )
        if period_type:
            query = query.filter_by(period_type=period_type)
        query = query.order_by(SalesGoal.start_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
