"""
UserRole API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.user_role_handler import UserRoleHandler

user_role_api = Blueprint('user_role_api', __name__, url_prefix='/api/user_roles')
handler = UserRoleHandler()

@user_role_api.route('/', methods=['GET'])
def get_all():
    """Lista todos los user roles con paginación"""
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

@user_role_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """Obtiene un rol de usuario por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_role_api.route('/', methods=['POST'])
def create():
    """Crea un nuevo rol de usuario"""
    try:
        data = request.get_json()
        obj = handler.create(**data)
        return jsonify({'success': True, 'message': 'Creado exitosamente', 'data': obj.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_role_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """Actualiza un rol de usuario"""
    try:
        data = request.get_json()
        obj = handler.update(id, **data)
        return jsonify({'success': True, 'message': 'Actualizado exitosamente', 'data': obj.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_role_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Elimina un rol de usuario"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
