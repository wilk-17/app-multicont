"""
Employee API - REST Endpoints con validación Marshmallow
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.employee_handler import EmployeeHandler
from app.schemas import (
    employee_create_schema,
    employee_update_schema,
    employee_response_schema,
    employees_response_schema
)

employee_api = Blueprint('employee_api', __name__, url_prefix='/api/employees')
handler = EmployeeHandler()

@employee_api.route('/', methods=['GET'])
def get_all():
    """Lista todos los employees con paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        result = handler.list_all(page=page, per_page=per_page)
        
        # Serializar con Marshmallow
        serialized_items = employees_response_schema.dump(result['items'])
        
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

@employee_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """Obtiene un empleado por ID"""
    try:
        obj = handler.get(id)
        if obj:
            result = employee_response_schema.dump(obj)
            return jsonify({'success': True, 'data': result}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@employee_api.route('/', methods=['POST'])
def create():
    """Crea un nuevo empleado con validación automática"""
    try:
        # Validar datos con Marshmallow
        validated_data = employee_create_schema.load(request.get_json())
        
        # Crear empleado
        obj = handler.create(**validated_data)
        
        # Serializar respuesta
        result = employee_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Empleado creado exitosamente',
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

@employee_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """Actualiza un empleado con validación automática"""
    try:
        # Validar datos con Marshmallow
        validated_data = employee_update_schema.load(request.get_json())
        
        if not validated_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        # Actualizar empleado
        obj = handler.update(id, **validated_data)
        
        # Serializar respuesta
        result = employee_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Empleado actualizado exitosamente',
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

@employee_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Elimina un empleado"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
