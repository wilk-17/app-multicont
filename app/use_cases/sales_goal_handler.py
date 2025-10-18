"""
SalesGoal Handler - Lógica de negocio para metas de ventas
"""
from datetime import datetime, date
from app import db
from app.entities.sales_goal import SalesGoal
from sqlalchemy import and_, or_


class SalesGoalHandler:
    """Handler para gestión de metas de ventas"""
    
    def create(self, period_type, start_date, end_date, target_amount, 
               employee_id=None, branch_id=None, created_by_user_id=None):
        """
        Crear una nueva meta de ventas
        
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
        
        goal = SalesGoal(
            period_type=period_type,
            start_date=start_date,
            end_date=end_date,
            target_amount=target_amount,
            employee_id=employee_id,
            branch_id=branch_id,
            created_by_user_id=created_by_user_id
        )
        
        db.session.add(goal)
        db.session.commit()
        return goal
    
    def get(self, goal_id):
        """Obtener meta por ID"""
        return SalesGoal.query.get(goal_id)
    
    def list_all(self, page=1, per_page=10, period_type=None, employee_id=None, branch_id=None):
        """
        Listar metas con filtros
        
        Args:
            page: Número de página
            per_page: Items por página
            period_type: Filtrar por tipo de periodo
            employee_id: Filtrar por empleado
            branch_id: Filtrar por sucursal
            
        Returns:
            dict con items paginados
        """
        query = SalesGoal.query
        
        if period_type:
            query = query.filter_by(period_type=period_type)
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if branch_id:
            query = query.filter_by(branch_id=branch_id)
        
        query = query.order_by(SalesGoal.start_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def get_current_goals(self, reference_date=None):
        """
        Obtener metas activas para una fecha específica
        
        Args:
            reference_date: Fecha de referencia (default: hoy)
            
        Returns:
            list de SalesGoal activos
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
    
    def get_goals_by_employee(self, employee_id, period_type=None):
        """
        Obtener todas las metas de un empleado
        
        Args:
            employee_id: ID del empleado
            period_type: Filtrar por tipo de periodo (opcional)
            
        Returns:
            list de SalesGoal
        """
        query = SalesGoal.query.filter_by(employee_id=employee_id)
        if period_type:
            query = query.filter_by(period_type=period_type)
        return query.order_by(SalesGoal.start_date.desc()).all()
    
    def get_goals_by_branch(self, branch_id, period_type=None):
        """
        Obtener todas las metas de una sucursal
        
        Args:
            branch_id: ID de la sucursal
            period_type: Filtrar por tipo de periodo (opcional)
            
        Returns:
            list de SalesGoal
        """
        query = SalesGoal.query.filter_by(branch_id=branch_id)
        if period_type:
            query = query.filter_by(period_type=period_type)
        return query.order_by(SalesGoal.start_date.desc()).all()
    
    def update(self, goal_id, **kwargs):
        """
        Actualizar meta de ventas
        
        Args:
            goal_id: ID de la meta
            **kwargs: Campos a actualizar
            
        Returns:
            SalesGoal actualizado
            
        Raises:
            ValueError: Si validaciones fallan
        """
        goal = SalesGoal.query.get(goal_id)
        if not goal:
            raise ValueError(f"SalesGoal with id {goal_id} not found")
        
        # Validaciones según campos actualizados
        if 'period_type' in kwargs and kwargs['period_type'] not in ['monthly', 'quarterly', 'yearly']:
            raise ValueError("period_type must be 'monthly', 'quarterly', or 'yearly'")
        
        if 'target_amount' in kwargs and kwargs['target_amount'] <= 0:
            raise ValueError("target_amount must be positive")
        
        # Actualizar campos permitidos
        allowed_fields = ['period_type', 'start_date', 'end_date', 'target_amount', 
                          'employee_id', 'branch_id']
        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(goal, key):
                setattr(goal, key, value)
        
        db.session.commit()
        return goal
    
    def delete(self, goal_id):
        """
        Eliminar meta de ventas
        
        Args:
            goal_id: ID de la meta
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValueError: Si la meta no existe
        """
        goal = SalesGoal.query.get(goal_id)
        if not goal:
            raise ValueError(f"SalesGoal with id {goal_id} not found")
        
        db.session.delete(goal)
        db.session.commit()
        return True
    
    def count(self, employee_id=None, branch_id=None):
        """
        Contar metas con filtros
        
        Args:
            employee_id: Filtrar por empleado (opcional)
            branch_id: Filtrar por sucursal (opcional)
            
        Returns:
            int: Total de metas
        """
        query = SalesGoal.query
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if branch_id:
            query = query.filter_by(branch_id=branch_id)
        return query.count()
