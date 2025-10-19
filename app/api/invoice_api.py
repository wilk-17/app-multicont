"""
Invoice API - REST Endpoints con validación Marshmallow
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.invoice_handler import InvoiceHandler
from app.schemas import (
    invoice_create_schema,
    invoice_update_schema,
    invoice_response_schema,
    invoices_response_schema
)
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

invoice_api = Blueprint('invoice_api', __name__, url_prefix='/api/invoices')
handler = InvoiceHandler()

@invoice_api.route('/', methods=['GET'])
@jwt_required()
def get_all():
    """Lista todos los invoices con paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        result = handler.list_all(page=page, per_page=per_page)
        
        # Serializar con Marshmallow
        serialized_items = invoices_response_schema.dump(result['items'])
        
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

@invoice_api.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    """Obtiene un factura por ID"""
    try:
        obj = handler.get(id)
        if obj:
            result = invoice_response_schema.dump(obj)
            return jsonify({'success': True, 'data': result}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@invoice_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    """Crea una nueva factura con validación automática"""
    try:
        # Validar datos con Marshmallow
        validated_data = invoice_create_schema.load(request.get_json())
        
        # Crear factura
        obj = handler.create(**validated_data)
        
        # Serializar respuesta
        result = invoice_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Factura creada exitosamente',
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

@invoice_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """Actualiza una factura con validación automática"""
    try:
        # Validar datos con Marshmallow
        validated_data = invoice_update_schema.load(request.get_json())
        
        if not validated_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        # Actualizar factura
        obj = handler.update(id, **validated_data)
        
        # Serializar respuesta
        result = invoice_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Factura actualizada exitosamente',
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

@invoice_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """Elimina un factura"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
