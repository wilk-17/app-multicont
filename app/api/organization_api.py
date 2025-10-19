"""
Organization API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.organization_handler import OrganizationHandler
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

organization_api = Blueprint('organization_api', __name__, url_prefix='/api/organizations')
handler = OrganizationHandler()

@organization_api.route('/', methods=['GET'])
@jwt_required()
def get_all():
    """Lista todos los organizations con paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        result = handler.list_all(page=page, per_page=per_page)
        return jsonify({
            'success': True,
            'data': {
                'items': [item.to_dict() for item in result['items']],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@organization_api.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    """Obtiene un organización por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@organization_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN')
def create():
    """Crea un nuevo organización"""
    try:
        data = request.get_json()
        obj = handler.create(**data)
        return jsonify({'success': True, 'message': 'Creado exitosamente', 'data': obj.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@organization_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """Actualiza un organización"""
    try:
        data = request.get_json()
        obj = handler.update(id, **data)
        return jsonify({'success': True, 'message': 'Actualizado exitosamente', 'data': obj.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@organization_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """Elimina un organización"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
