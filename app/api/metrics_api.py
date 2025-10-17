"""
Metrics API - Sistema de Métricas de Negocio
"""
from flask import Blueprint, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db
from app.entities.user import User
from app.entities.inventory_item import InventoryItem
from app.entities.quote import Quote
from app.entities.sales_order import SalesOrder
from app.entities.invoice import Invoice
from app.entities.employee import Employee
from app.entities.organization import Organization

metrics_api = Blueprint('metrics_api', __name__, url_prefix='/api/metrics')


@metrics_api.route('/users', methods=['GET'])
def get_user_metrics():
    """
    Obtiene métricas de usuarios
    ---
    tags:
      - Métricas
    responses:
      200:
        description: Estadísticas de usuarios
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                total_users:
                  type: integer
                active_users:
                  type: integer
                inactive_users:
                  type: integer
                suspended_users:
                  type: integer
                growth_last_month:
                  type: integer
    """
    try:
        total = User.query.count()
        active = User.query.filter_by(status='active').count()
        inactive = User.query.filter_by(status='inactive').count()
        suspended = User.query.filter_by(status='suspended').count()
        
        # Usuarios creados el último mes
        last_month = datetime.utcnow() - timedelta(days=30)
        growth = User.query.filter(User.creation_date >= last_month).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_users': total,
                'active_users': active,
                'inactive_users': inactive,
                'suspended_users': suspended,
                'growth_last_month': growth
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@metrics_api.route('/inventory', methods=['GET'])
def get_inventory_metrics():
    """
    Obtiene métricas de inventario
    ---
    tags:
      - Métricas
    """
    try:
        total_items = InventoryItem.query.count()
        total_value = db.session.query(func.sum(InventoryItem.quantity * InventoryItem.price)).scalar() or 0
        low_stock = InventoryItem.query.filter(InventoryItem.quantity < 10).count()
        out_of_stock = InventoryItem.query.filter(InventoryItem.quantity == 0).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_items': total_items,
                'total_inventory_value': float(total_value),
                'low_stock_items': low_stock,
                'out_of_stock_items': out_of_stock
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@metrics_api.route('/sales', methods=['GET'])
def get_sales_metrics():
    """
    Obtiene métricas de ventas
    ---
    tags:
      - Métricas
    """
    try:
        # Cotizaciones
        total_quotes = Quote.query.count()
        pending_quotes = Quote.query.filter_by(status='pending').count()
        
        # Órdenes de venta
        total_orders = SalesOrder.query.count()
        total_sales = db.session.query(func.sum(SalesOrder.total)).scalar() or 0
        
        # Facturas
        total_invoices = Invoice.query.count()
        total_invoiced = db.session.query(func.sum(Invoice.total)).scalar() or 0
        
        # Ventas del último mes
        last_month = datetime.utcnow() - timedelta(days=30)
        sales_last_month = db.session.query(func.sum(SalesOrder.total))\
            .filter(SalesOrder.creation_date >= last_month)\
            .scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_quotes': total_quotes,
                'pending_quotes': pending_quotes,
                'total_sales_orders': total_orders,
                'total_sales_amount': float(total_sales),
                'total_invoices': total_invoices,
                'total_invoiced_amount': float(total_invoiced),
                'sales_last_month': float(sales_last_month)
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@metrics_api.route('/employees', methods=['GET'])
def get_employee_metrics():
    """
    Obtiene métricas de empleados
    ---
    tags:
      - Métricas
    """
    try:
        total_employees = Employee.query.count()
        active_employees = Employee.query.filter_by(status='active').count()
        total_organizations = Organization.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_employees': total_employees,
                'active_employees': active_employees,
                'total_organizations': total_organizations
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@metrics_api.route('/summary', methods=['GET'])
def get_metrics_summary():
    """
    Obtiene un resumen de todas las métricas principales
    ---
    tags:
      - Métricas
    responses:
      200:
        description: Resumen completo de métricas del sistema
    """
    try:
        # Consolidar todas las métricas
        data = {
            'users': {
                'total': User.query.count(),
                'active': User.query.filter_by(status='active').count()
            },
            'inventory': {
                'total_items': InventoryItem.query.count(),
                'low_stock': InventoryItem.query.filter(InventoryItem.quantity < 10).count()
            },
            'sales': {
                'total_quotes': Quote.query.count(),
                'total_orders': SalesOrder.query.count(),
                'total_invoices': Invoice.query.count(),
                'total_revenue': float(db.session.query(func.sum(Invoice.total)).scalar() or 0)
            },
            'employees': {
                'total': Employee.query.count(),
                'active': Employee.query.filter_by(status='active').count()
            },
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
