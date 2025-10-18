"""
City API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.city_handler import CityHandler

city_api = Blueprint('city_api', __name__, url_prefix='/api/cities')
handler = CityHandler()

@city_api.route('/', methods=['GET'])
def get_all():
    """Lista todos los cities con paginación"""
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

@city_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """Obtiene un ciudad por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@city_api.route('/', methods=['POST'])
def create():
    """Crea un nuevo ciudad"""
    try:
        data = request.get_json()
        obj = handler.create(**data)
        return jsonify({'success': True, 'message': 'Creado exitosamente', 'data': obj.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@city_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """Actualiza un ciudad"""
    try:
        data = request.get_json()
        obj = handler.update(id, **data)
        return jsonify({'success': True, 'message': 'Actualizado exitosamente', 'data': obj.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@city_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Elimina un ciudad"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
