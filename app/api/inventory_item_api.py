"""
InventoryItem API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.inventory_item_handler import InventoryItemHandler

inventory_item_api = Blueprint('inventory_item_api', __name__, url_prefix='/api/inventory_items')
handler = InventoryItemHandler()

@inventory_item_api.route('/', methods=['GET'])
def get_all():
    """Lista todos los inventory items con paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None, type=str)
        result = handler.list_all(page=page, per_page=per_page, status=status)
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

@inventory_item_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """Obtiene un item de inventario por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@inventory_item_api.route('/', methods=['POST'])
def create():
    """Crea un nuevo item de inventario"""
    try:
        data = request.get_json()
        obj = handler.create(**data)
        return jsonify({'success': True, 'message': 'Creado exitosamente', 'data': obj.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@inventory_item_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """Actualiza un item de inventario"""
    try:
        data = request.get_json()
        obj = handler.update(id, **data)
        return jsonify({'success': True, 'message': 'Actualizado exitosamente', 'data': obj.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@inventory_item_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Elimina un item de inventario"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Eliminado exitosamente'}), 200
        return jsonify({'success': False, 'error': 'No encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
