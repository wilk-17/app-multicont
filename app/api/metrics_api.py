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
    """Obtiene métricas de usuarios"""
    try:
        total = User.query.count()
        # status may not exist on User model depending on schema sync
        active = User.query.filter_by(status='active').count() if hasattr(User, 'status') else 0
        inactive = User.query.filter_by(status='inactive').count() if hasattr(User, 'status') else 0
        suspended = User.query.filter_by(status='suspended').count() if hasattr(User, 'status') else 0

        # Usuarios creados el último mes (if creation_date exists)
        last_month = datetime.utcnow() - timedelta(days=30)
        growth = User.query.filter(User.creation_date >= last_month).count() if hasattr(User, 'creation_date') else 0

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
    """Obtiene métricas de inventario"""
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
    """Obtiene métricas de ventas"""
    try:
        # Cotizaciones
        total_quotes = Quote.query.count()
        pending_quotes = Quote.query.filter_by(status='pending').count() if hasattr(Quote, 'status') else 0

        # Órdenes de venta
        total_orders = SalesOrder.query.count()
        total_sales = db.session.query(func.sum(SalesOrder.total)).scalar() or 0

        # Facturas
        total_invoices = Invoice.query.count()
        total_invoiced = db.session.query(func.sum(Invoice.total)).scalar() or 0

        # Ventas del último mes
        last_month = datetime.utcnow() - timedelta(days=30)
        sales_last_month_q = db.session.query(func.sum(SalesOrder.total))
        if hasattr(SalesOrder, 'creation_date'):
            sales_last_month_q = sales_last_month_q.filter(SalesOrder.creation_date >= last_month)
        sales_last_month = sales_last_month_q.scalar() or 0

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
    """Obtiene métricas de empleados"""
    try:
        total_employees = Employee.query.count()
        active_employees = Employee.query.filter_by(status='active').count() if hasattr(Employee, 'status') else 0
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
    """Obtiene un resumen de todas las métricas principales"""
    try:
        # Consolidar todas las métricas
        data = {
            'users': {
                'total': User.query.count(),
                'active': User.query.filter_by(status='active').count() if hasattr(User, 'status') else 0
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
                'active': Employee.query.filter_by(status='active').count() if hasattr(Employee, 'status') else 0
            },
            'timestamp': datetime.utcnow().isoformat()
        }

        return jsonify({
            'success': True,
            'data': data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
