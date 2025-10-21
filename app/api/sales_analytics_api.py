"""
Sales Analytics API - Endpoints especializados para análisis de ventas, 
facturación por empleado/sede, análisis por marca, comparación con metas
"""
from flask import Blueprint, request
from sqlalchemy import func, and_, or_, extract
from datetime import datetime, date, timedelta
from app import db, cache
from app.entities.invoice import Invoice
from app.entities.invoice_item import InvoiceItem
from app.entities.sales_order import SalesOrder
from app.entities.quote import Quote
from app.entities.employee import Employee
from app.entities.branch import Branch
from app.entities.inventory_item import InventoryItem
from app.entities.brand import Brand
from app.entities.sales_goal import SalesGoal
from flask_jwt_extended import jwt_required
from app.services.authorization_service import require_role
from app.api.helpers import (
    success_response,
    error_response
)

sales_analytics_api = Blueprint('sales_analytics_api', __name__, url_prefix='/api/analytics')


def parse_date(date_str):
    """Helper para parsear fechas"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None


@sales_analytics_api.route('/invoicing/by_employee', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def invoicing_by_employee():
    """
    Facturación por empleado (vendedor) en un periodo
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
      - name: end_date
        in: query
        type: string
        format: date
        required: true
      - name: employee_id
        in: query
        type: integer
        description: Filtrar por empleado específico (opcional)
    responses:
      200:
        description: Facturación por empleado
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
                properties:
                  employee_id:
                    type: integer
                  employee_name:
                    type: string
                  branch_id:
                    type: integer
                  branch_name:
                    type: string
                  total_invoiced:
                    type: number
                  invoice_count:
                    type: integer
    """
    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    employee_id = request.args.get('employee_id', None, type=int)
    
    if not start_date or not end_date:
        return error_response('start_date and end_date are required', 400)
    
    try:
        # Query principal: agregar facturación por empleado
        query = db.session.query(
            Invoice.employee_id,
            func.sum(Invoice.total).label('total_invoiced'),
            func.count(Invoice.id).label('invoice_count')
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date,
                Invoice.employee_id.isnot(None)
            )
        ).group_by(Invoice.employee_id)
        
        if employee_id:
            query = query.filter(Invoice.employee_id == employee_id)
        
        results = query.all()
        
        # Enriquecer con datos de empleado y sucursal
        data = []
        for row in results:
            employee = Employee.query.get(row.employee_id)
            if employee:
                branch = Branch.query.get(employee.branch_id)
                
                data.append({
                    'employee_id': row.employee_id,
                    'employee_name': f"{employee.first_name} {employee.last_name}" if employee else "Unknown",
                    'branch_id': employee.branch_id,
                    'branch_name': getattr(branch, 'name', 'Unknown') if hasattr(Branch, 'name') else f"Branch {employee.branch_id}",
                    'total_invoiced': float(row.total_invoiced) if row.total_invoiced else 0,
                    'invoice_count': row.invoice_count
                })
        
        # Ordenar por total facturado descendente
        data.sort(key=lambda x: x['total_invoiced'], reverse=True)
        
        return success_response(data, 'Facturación por empleado obtenida', 200)
    
    except Exception as e:
        return error_response(str(e), 500)


@sales_analytics_api.route('/invoicing/by_branch', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def invoicing_by_branch():
    """
    Facturación por sucursal en un periodo
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
      - name: end_date
        in: query
        type: string
        format: date
        required: true
      - name: branch_id
        in: query
        type: integer
        description: Filtrar por sucursal específica (opcional)
    responses:
      200:
        description: Facturación por sucursal
    """
    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    branch_id = request.args.get('branch_id', None, type=int)
    
    if not start_date or not end_date:
        return error_response('start_date and end_date are required', 400)
    
    try:
        # Join Invoice → Employee → Branch
        query = db.session.query(
            Employee.branch_id,
            func.sum(Invoice.total).label('total_invoiced'),
            func.count(Invoice.id).label('invoice_count'),
            func.count(func.distinct(Invoice.employee_id)).label('employee_count')
        ).join(
            Employee, Invoice.employee_id == Employee.id
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date
            )
        ).group_by(Employee.branch_id)
        
        if branch_id:
            query = query.filter(Employee.branch_id == branch_id)
        
        results = query.all()
        
        # Enriquecer con datos de sucursal
        data = []
        for row in results:
            branch = Branch.query.get(row.branch_id)
            
            data.append({
                'branch_id': row.branch_id,
                'branch_name': getattr(branch, 'name', 'Unknown') if (branch and hasattr(Branch, 'name')) else f"Branch {row.branch_id}",
                'total_invoiced': float(row.total_invoiced) if row.total_invoiced else 0,
                'invoice_count': row.invoice_count,
                'employee_count': row.employee_count
            })
        
        # Ordenar por total facturado descendente
        data.sort(key=lambda x: x['total_invoiced'], reverse=True)
        
        return success_response(data, 'Datos obtenidos exitosamente', 200)
    
    except Exception as e:
        return error_response(str(e), 500)


@sales_analytics_api.route('/invoicing/by_brand', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def invoicing_by_brand():
    """
    Facturación por marca de producto en un periodo
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
      - name: end_date
        in: query
        type: string
        format: date
        required: true
      - name: brand_id
        in: query
        type: integer
        description: Filtrar por marca específica (opcional)
    responses:
      200:
        description: Facturación por marca
    """
    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    brand_id = request.args.get('brand_id', None, type=int)
    
    if not start_date or not end_date:
        return error_response('start_date and end_date are required', 400)
    
    try:
        # Join Invoice → InvoiceItem → InventoryItem → Brand
        query = db.session.query(
            InventoryItem.brand_id,
            func.sum(InvoiceItem.quantity * InvoiceItem.price).label('total_invoiced'),
            func.sum(InvoiceItem.quantity).label('total_quantity'),
            func.count(func.distinct(InvoiceItem.invoice_id)).label('invoice_count')
        ).select_from(Invoice).join(
            InvoiceItem, Invoice.id == InvoiceItem.invoice_id
        ).join(
            InventoryItem, InvoiceItem.item_id == InventoryItem.id
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date,
                InventoryItem.brand_id.isnot(None)
            )
        ).group_by(InventoryItem.brand_id)
        
        if brand_id:
            query = query.filter(InventoryItem.brand_id == brand_id)
        
        results = query.all()
        
        # Enriquecer con datos de marca
        data = []
        for row in results:
            brand = Brand.query.get(row.brand_id)
            
            data.append({
                'brand_id': row.brand_id,
                'brand_name': brand.name if brand else "Unknown",
                'total_invoiced': float(row.total_invoiced) if row.total_invoiced else 0,
                'total_quantity': row.total_quantity,
                'invoice_count': row.invoice_count
            })
        
        # Ordenar por total facturado descendente
        data.sort(key=lambda x: x['total_invoiced'], reverse=True)
        
        return success_response(data, 'Datos obtenidos exitosamente', 200)
    
    except Exception as e:
        return error_response(str(e), 500)


@sales_analytics_api.route('/quotes/by_brand', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def quotes_by_brand():
    """
    Cotizaciones por marca de producto en un periodo
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
      - name: end_date
        in: query
        type: string
        format: date
        required: true
      - name: brand_id
        in: query
        type: integer
        description: Filtrar por marca específica (opcional)
    responses:
      200:
        description: Cotizaciones por marca
    """
    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    brand_id = request.args.get('brand_id', None, type=int)
    
    if not start_date or not end_date:
        return error_response('start_date and end_date are required', 400)
    
    try:
        # Importar QuoteItem
        from app.entities.quote_item import QuoteItem
        
        # Join Quote → QuoteItem → InventoryItem → Brand
        query = db.session.query(
            InventoryItem.brand_id,
            func.count(func.distinct(QuoteItem.quote_id)).label('quote_count'),
            func.sum(QuoteItem.quantity).label('total_quantity')
        ).select_from(Quote).join(
            QuoteItem, Quote.id == QuoteItem.quote_id
        ).join(
            InventoryItem, QuoteItem.item_id == InventoryItem.id
        ).filter(
            and_(
                Quote.date >= start_date,
                Quote.date <= end_date,
                InventoryItem.brand_id.isnot(None)
            )
        ).group_by(InventoryItem.brand_id)
        
        if brand_id:
            query = query.filter(InventoryItem.brand_id == brand_id)
        
        results = query.all()
        
        # Enriquecer con datos de marca
        data = []
        for row in results:
            brand = Brand.query.get(row.brand_id)
            
            data.append({
                'brand_id': row.brand_id,
                'brand_name': brand.name if brand else "Unknown",
                'quote_count': row.quote_count,
                'total_quantity': row.total_quantity
            })
        
        # Ordenar por cantidad de cotizaciones descendente
        data.sort(key=lambda x: x['quote_count'], reverse=True)
        
        return success_response(data, 'Datos obtenidos exitosamente', 200)
    
    except Exception as e:
        return error_response(str(e), 500)


@sales_analytics_api.route('/goals/vs_actual', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def goals_vs_actual():
    """
    Comparación de metas vs facturación real
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: period_type
        in: query
        type: string
        enum: [monthly, quarterly, yearly]
        required: true
      - name: reference_date
        in: query
        type: string
        format: date
        description: Fecha de referencia (default hoy)
      - name: employee_id
        in: query
        type: integer
        description: Filtrar por empleado (opcional)
      - name: branch_id
        in: query
        type: integer
        description: Filtrar por sucursal (opcional)
    responses:
      200:
        description: Metas vs facturación real
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
                properties:
                  goal_id:
                    type: integer
                  scope_type:
                    type: string
                    enum: [employee, branch]
                  scope_id:
                    type: integer
                  scope_name:
                    type: string
                  period_type:
                    type: string
                  start_date:
                    type: string
                  end_date:
                    type: string
                  target_amount:
                    type: number
                  actual_amount:
                    type: number
                  achievement_percentage:
                    type: number
                  status:
                    type: string
                    enum: [exceeded, on_track, at_risk, failed]
    """
    period_type = request.args.get('period_type', 'monthly', type=str)
    reference_date = parse_date(request.args.get('reference_date')) or date.today()
    employee_id = request.args.get('employee_id', None, type=int)
    branch_id = request.args.get('branch_id', None, type=int)
    
    if period_type not in ['monthly', 'quarterly', 'yearly']:
        return error_response('period_type must be monthly, quarterly, or yearly', 400)
    
    try:
        # Obtener metas activas para la fecha de referencia
        goals_query = SalesGoal.query.filter(
            and_(
                SalesGoal.start_date <= reference_date,
                SalesGoal.end_date >= reference_date,
                SalesGoal.period_type == period_type
            )
        )
        
        if employee_id:
            goals_query = goals_query.filter(SalesGoal.employee_id == employee_id)
        if branch_id:
            goals_query = goals_query.filter(SalesGoal.branch_id == branch_id)
        
        goals = goals_query.all()
        
        data = []
        for goal in goals:
            # Calcular facturación real en el periodo de la meta
            if goal.employee_id:
                # Meta por empleado
                actual_query = db.session.query(
                    func.sum(Invoice.total)
                ).filter(
                    and_(
                        Invoice.employee_id == goal.employee_id,
                        Invoice.invoice_date >= goal.start_date,
                        Invoice.invoice_date <= goal.end_date
                    )
                )
                actual_amount = actual_query.scalar() or 0
                
                # Obtener nombre del empleado
                employee = Employee.query.get(goal.employee_id)
                scope_name = f"{employee.first_name} {employee.last_name}" if employee else "Unknown"
                scope_type = "employee"
                scope_id = goal.employee_id
                
            elif goal.branch_id:
                # Meta por sucursal (sumar todos los empleados de la sucursal)
                actual_query = db.session.query(
                    func.sum(Invoice.total)
                ).join(
                    Employee, Invoice.employee_id == Employee.id
                ).filter(
                    and_(
                        Employee.branch_id == goal.branch_id,
                        Invoice.invoice_date >= goal.start_date,
                        Invoice.invoice_date <= goal.end_date
                    )
                )
                actual_amount = actual_query.scalar() or 0
                
                branch = Branch.query.get(goal.branch_id)
                scope_name = getattr(branch, 'name', f"Branch {goal.branch_id}") if branch else "Unknown"
                scope_type = "branch"
                scope_id = goal.branch_id
            
            # Calcular porcentaje de logro
            target_amount = float(goal.target_amount)
            actual_amount = float(actual_amount)
            achievement_percentage = (actual_amount / target_amount * 100) if target_amount > 0 else 0
            
            # Determinar estado
            if achievement_percentage >= 100:
                status = "exceeded"
            elif achievement_percentage >= 80:
                status = "on_track"
            elif achievement_percentage >= 50:
                status = "at_risk"
            else:
                status = "failed"
            
            data.append({
                'goal_id': goal.id,
                'scope_type': scope_type,
                'scope_id': scope_id,
                'scope_name': scope_name,
                'period_type': goal.period_type,
                'start_date': goal.start_date.isoformat(),
                'end_date': goal.end_date.isoformat(),
                'target_amount': target_amount,
                'actual_amount': actual_amount,
                'achievement_percentage': round(achievement_percentage, 2),
                'status': status
            })
        
        # Ordenar por porcentaje de logro descendente
        data.sort(key=lambda x: x['achievement_percentage'], reverse=True)
        
        return success_response(data, 'Datos obtenidos exitosamente', 200)
    
    except Exception as e:
        return error_response(str(e), 500)


@sales_analytics_api.route('/sales/summary', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def sales_summary():
    """
    Resumen consolidado de ventas en un periodo
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
      - name: end_date
        in: query
        type: string
        format: date
        required: true
    responses:
      200:
        description: Resumen consolidado
    """
    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    
    if not start_date or not end_date:
        return error_response('start_date and end_date are required', 400)
    
    try:
        # Total de facturación
        total_invoiced = db.session.query(
            func.sum(Invoice.total)
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date
            )
        ).scalar() or 0
        
        # Cantidad de facturas
        invoice_count = db.session.query(
            func.count(Invoice.id)
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date
            )
        ).scalar() or 0
        
        # Cotizaciones generadas
        quote_count = db.session.query(
            func.count(Quote.id)
        ).filter(
            and_(
                Quote.date >= start_date,
                Quote.date <= end_date
            )
        ).scalar() or 0
        
        # Órdenes de venta
        sales_order_count = db.session.query(
            func.count(SalesOrder.id)
        ).filter(
            and_(
                SalesOrder.order_date >= start_date,
                SalesOrder.order_date <= end_date
            )
        ).scalar() or 0
        
        # Empleados activos en ventas
        active_employees = db.session.query(
            func.count(func.distinct(Invoice.employee_id))
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date,
                Invoice.employee_id.isnot(None)
            )
        ).scalar() or 0
        
        # Ticket promedio
        avg_invoice = float(total_invoiced) / invoice_count if invoice_count > 0 else 0
        
        # Tasa de conversión quote → invoice (aproximada)
        conversion_rate = (invoice_count / quote_count * 100) if quote_count > 0 else 0
        
        summary_data = {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'total_invoiced': float(total_invoiced),
            'invoice_count': invoice_count,
            'quote_count': quote_count,
            'sales_order_count': sales_order_count,
            'active_employees': active_employees,
            'avg_invoice_amount': round(avg_invoice, 2),
            'conversion_rate': round(conversion_rate, 2)
        }
        
        return success_response(summary_data, 'Resumen de ventas obtenido', 200)
    
    except Exception as e:
        return error_response(str(e), 500)


@sales_analytics_api.route('/top_performers', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
@cache.cached(timeout=600, query_string=True)
def top_performers():
    """
    Top empleados vendedores en un periodo
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
      - name: end_date
        in: query
        type: string
        format: date
        required: true
      - name: limit
        in: query
        type: integer
        default: 10
        description: Número de top performers a retornar
    responses:
      200:
        description: Top vendedores
    """
    start_date = parse_date(request.args.get('start_date'))
    end_date = parse_date(request.args.get('end_date'))
    limit = request.args.get('limit', 10, type=int)
    
    if not start_date or not end_date:
        return error_response('start_date and end_date are required', 400)
    
    try:
        # Top por facturación total
        results = db.session.query(
            Invoice.employee_id,
            func.sum(Invoice.total).label('total_invoiced'),
            func.count(Invoice.id).label('invoice_count')
        ).filter(
            and_(
                Invoice.invoice_date >= start_date,
                Invoice.invoice_date <= end_date,
                Invoice.employee_id.isnot(None)
            )
        ).group_by(
            Invoice.employee_id
        ).order_by(
            func.sum(Invoice.total).desc()
        ).limit(limit).all()
        
        data = []
        rank = 1
        for row in results:
            employee = Employee.query.get(row.employee_id)
            branch = Branch.query.get(employee.branch_id) if employee else None
            
            data.append({
                'rank': rank,
                'employee_id': row.employee_id,
                'employee_name': f"{employee.first_name} {employee.last_name}" if employee else "Unknown",
                'branch_id': employee.branch_id if employee else None,
                'branch_name': getattr(branch, 'name', 'Unknown') if (branch and hasattr(Branch, 'name')) else f"Branch {employee.branch_id if employee else ''}",
                'total_invoiced': float(row.total_invoiced),
                'invoice_count': row.invoice_count,
                'avg_invoice': float(row.total_invoiced) / row.invoice_count if row.invoice_count > 0 else 0
            })
            rank += 1
        
        return success_response(data, 'Datos obtenidos exitosamente', 200)
    
    except Exception as e:
        return error_response(str(e), 500)
