"""
Dashboard API - Endpoint consolidado para dashboards
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app import db
from app.entities.user import User
from app.entities.inventory_item import InventoryItem
from app.entities.quote import Quote
from app.entities.sales_order import SalesOrder
from app.entities.invoice import Invoice
from app.entities.employee import Employee

dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')


@dashboard_api.route('/', methods=['GET'])
def get_dashboard():
    """
    Obtiene datos consolidados para el dashboard principal
    ---
    tags:
      - Dashboard
    parameters:
      - name: period
        in: query
        type: string
        enum: [day, week, month, year]
        default: month
        description: Período de tiempo para las métricas
    responses:
      200:
        description: Datos completos del dashboard
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                summary:
                  type: object
                  description: Resumen de métricas principales
                charts:
                  type: object
                  description: Datos para gráficos
                recent_activity:
                  type: array
                  description: Actividad reciente
    """
    try:
        period = request.args.get('period', 'month', type=str)
        
        # Calcular fecha de inicio según período
        now = datetime.utcnow()
        if period == 'day':
            start_date = now - timedelta(days=1)
        elif period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:  # month
            start_date = now - timedelta(days=30)
        
        # SUMMARY - Métricas principales
        summary = {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(status='active').count(),
            'total_employees': Employee.query.count(),
            'total_inventory_items': InventoryItem.query.count(),
            'low_stock_items': InventoryItem.query.filter(InventoryItem.quantity < 10).count(),
            'total_quotes': Quote.query.filter(Quote.creation_date >= start_date).count(),
            'total_sales': SalesOrder.query.filter(SalesOrder.creation_date >= start_date).count(),
            'total_invoices': Invoice.query.filter(Invoice.creation_date >= start_date).count(),
            'total_revenue': float(
                db.session.query(func.sum(Invoice.total))
                .filter(Invoice.creation_date >= start_date)
                .scalar() or 0
            )
        }
        
        # CHARTS - Datos para gráficos
        # 1. Ventas por mes (últimos 12 meses)
        sales_by_month = db.session.query(
            extract('year', SalesOrder.date).label('year'),
            extract('month', SalesOrder.date).label('month'),
            func.sum(SalesOrder.total).label('total')
        ).filter(
            SalesOrder.date >= (now - timedelta(days=365))
        ).group_by('year', 'month').order_by('year', 'month').all()
        
        # 2. Top 5 productos más vendidos
        # (Esto requeriría una consulta más compleja con sales_order_items)
        
        # 3. Estado de cotizaciones
        quotes_by_status = db.session.query(
            Quote.status,
            func.count(Quote.id).label('count')
        ).group_by(Quote.status).all()
        
        charts = {
            'sales_by_month': [
                {
                    'year': int(year),
                    'month': int(month),
                    'total': float(total) if total else 0
                }
                for year, month, total in sales_by_month
            ],
            'quotes_by_status': [
                {'status': status, 'count': count}
                for status, count in quotes_by_status
            ]
        }
        
        # RECENT ACTIVITY - Actividad reciente
        recent_quotes = Quote.query.order_by(Quote.creation_date.desc()).limit(5).all()
        recent_orders = SalesOrder.query.order_by(Quote.creation_date.desc()).limit(5).all()
        
        recent_activity = {
            'quotes': [
                {
                    'id': str(q.id),
                    'customer_name': q.customer_name,
                    'total': float(q.total),
                    'date': q.date.isoformat() if q.date else None,
                    'status': q.status
                }
                for q in recent_quotes
            ],
            'orders': [
                {
                    'id': str(o.id),
                    'total': float(o.total),
                    'date': o.date.isoformat() if o.date else None,
                    'status': o.status
                }
                for o in recent_orders
            ]
        }
        
        # ALERTS - Alertas del sistema
        alerts = []
        
        # Alerta de stock bajo
        low_stock_count = InventoryItem.query.filter(InventoryItem.quantity < 10).count()
        if low_stock_count > 0:
            alerts.append({
                'type': 'warning',
                'message': f'{low_stock_count} productos con stock bajo',
                'action': '/api/inventory_items?status=low_stock'
            })
        
        # Alerta de cotizaciones pendientes
        pending_quotes = Quote.query.filter_by(status='pending').count()
        if pending_quotes > 5:
            alerts.append({
                'type': 'info',
                'message': f'{pending_quotes} cotizaciones pendientes por revisar',
                'action': '/api/quotes?status=pending'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'summary': summary,
                'charts': charts,
                'recent_activity': recent_activity,
                'alerts': alerts,
                'period': period,
                'start_date': start_date.isoformat(),
                'generated_at': now.isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboard_api.route('/kpis', methods=['GET'])
def get_kpis():
    """
    Obtiene KPIs (Key Performance Indicators) del negocio
    ---
    tags:
      - Dashboard
    """
    try:
        now = datetime.utcnow()
        last_month = now - timedelta(days=30)
        prev_month = now - timedelta(days=60)
        
        # Ventas este mes vs mes anterior
        current_sales = float(
            db.session.query(func.sum(SalesOrder.total))
            .filter(SalesOrder.creation_date >= last_month)
            .scalar() or 0
        )
        
        previous_sales = float(
            db.session.query(func.sum(SalesOrder.total))
            .filter(
                SalesOrder.creation_date >= prev_month,
                SalesOrder.creation_date < last_month
            )
            .scalar() or 0
        )
        
        sales_growth = ((current_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0
        
        # Tasa de conversión (Cotizaciones -> Órdenes)
        quotes_count = Quote.query.filter(Quote.creation_date >= last_month).count()
        orders_count = SalesOrder.query.filter(SalesOrder.creation_date >= last_month).count()
        conversion_rate = (orders_count / quotes_count * 100) if quotes_count > 0 else 0
        
        # Valor promedio de orden
        avg_order_value = float(
            db.session.query(func.avg(SalesOrder.total))
            .filter(SalesOrder.creation_date >= last_month)
            .scalar() or 0
        )
        
        return jsonify({
            'success': True,
            'data': {
                'current_month_sales': current_sales,
                'previous_month_sales': previous_sales,
                'sales_growth_percentage': round(sales_growth, 2),
                'conversion_rate': round(conversion_rate, 2),
                'average_order_value': round(avg_order_value, 2),
                'total_customers': Quote.query.distinct(Quote.customer_name).count()
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
