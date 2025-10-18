"""
SalesGoal Entity - Metas de Ventas
Permite al administrador establecer metas mensuales, trimestrales y anuales
por empleado (vendedor) o por sucursal
"""
from datetime import datetime
from app import db


class SalesGoal(db.Model):
    """
    Meta de ventas asignada por el administrador.
    Puede ser por empleado individual o por sucursal completa.
    Soporta periodos: mensual, trimestral, anual
    """
    __tablename__ = "sales_goal"
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    # Alcance de la meta (uno de los dos debe ser nulo)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=True)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branch.id"), nullable=True)
    
    # Periodo y fechas
    period_type = db.Column(db.String(20), nullable=False)  # 'monthly', 'quarterly', 'yearly'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Meta de ventas en dinero
    target_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Metadatos
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by_user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=True)
    
    def __init__(self, period_type, start_date, end_date, target_amount, 
                 employee_id=None, branch_id=None, created_by_user_id=None):
        self.employee_id = employee_id
        self.branch_id = branch_id
        self.period_type = period_type
        self.start_date = start_date
        self.end_date = end_date
        self.target_amount = target_amount
        self.created_by_user_id = created_by_user_id
        self.creation_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'employee_id': str(self.employee_id) if self.employee_id else None,
            'branch_id': str(self.branch_id) if self.branch_id else None,
            'period_type': self.period_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'target_amount': float(self.target_amount) if self.target_amount else 0,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'created_by_user_id': str(self.created_by_user_id) if self.created_by_user_id else None
        }
    
    def __repr__(self):
        scope = f"Employee {self.employee_id}" if self.employee_id else f"Branch {self.branch_id}"
        return f'<SalesGoal {scope} - {self.period_type}: ${self.target_amount}>'
