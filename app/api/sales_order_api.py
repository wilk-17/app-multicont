"""
SalesOrder API - REST Endpoints con validación Marshmallow
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.sales_order_handler import SalesOrderHandler
from app.schemas import (
    sales_order_create_schema,
    sales_order_update_schema,
    sales_order_response_schema,
    sales_orders_response_schema
)
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

sales_order_api = Blueprint('sales_order_api', __name__, url_prefix='/api/sales_orders')
handler = SalesOrderHandler()

@sales_order_api.route('/', methods=['GET'])
@jwt_required()
def get_all():
    """Lista todos los sales orders con paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        result = handler.list_all(page=page, per_page=per_page)
        
        # Serializar con Marshmallow
        serialized_items = sales_orders_response_schema.dump(result['items'])
        
        return jsonify({
            'success': True,
            'data': {
                'items': serialized_items,
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_order_api.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    """Obtiene una orden de venta por ID"""
    try:
        obj = handler.get(id)
        if obj:
            result = sales_order_response_schema.dump(obj)
            return jsonify({'success': True, 'data': result}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_order_api.route('/', methods=['POST'])
@jwt_required()
def create():
    """Crea una nueva orden de venta con validación automática"""
    try:
        # Validar datos con Marshmallow
        validated_data = sales_order_create_schema.load(request.get_json())
        
        # Crear orden
        obj = handler.create(**validated_data)
        
        # Serializar respuesta
        result = sales_order_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Orden de venta creada exitosamente',
            'data': result
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@sales_order_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """Actualiza una orden de venta con validación automática"""
    try:
        # Validar datos con Marshmallow
        validated_data = sales_order_update_schema.load(request.get_json())
        
        if not validated_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        # Actualizar orden
        obj = handler.update(id, **validated_data)
        
        # Serializar respuesta
        result = sales_order_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Orden de venta actualizada exitosamente',
            'data': result
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@sales_order_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """Elimina un orden de venta"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
