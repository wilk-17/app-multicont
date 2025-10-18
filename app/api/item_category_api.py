"""
ItemCategory API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.item_category_handler import ItemCategoryHandler

item_category_api = Blueprint('item_category_api', __name__, url_prefix='/api/item_categories')
handler = ItemCategoryHandler()

@item_category_api.route('/', methods=['GET'])
def get_all():
    """
    Lista todas las categorías de items
    ---
    tags:
      - Categorías
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Lista de categorías
    """
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

@item_category_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Obtiene una categoría por ID
    ---
    tags:
      - Categorías
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Categoría encontrada
      404:
        description: Categoría no encontrada
    """
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'Categoría no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@item_category_api.route('/', methods=['POST'])
def create():
    """
    Crea una nueva categoría
    ---
    tags:
      - Categorías
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: "Electrónica"
    responses:
      201:
        description: Categoría creada exitosamente
      400:
        description: Datos inválidos
    """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo requerido: name'
            }), 400
        obj = handler.create(**data)
        return jsonify({'success': True, 'message': 'Categoría creada exitosamente', 'data': obj.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@item_category_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Actualiza una categoría
    ---
    tags:
      - Categorías
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
    responses:
      200:
        description: Categoría actualizada exitosamente
      404:
        description: Categoría no encontrada
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        obj = handler.update(id, **data)
        return jsonify({'success': True, 'message': 'Categoría actualizada exitosamente', 'data': obj.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@item_category_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Elimina una categoría
    ---
    tags:
      - Categorías
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Categoría eliminada exitosamente
      404:
        description: Categoría no encontrada
    """
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Categoría eliminada exitosamente'}), 200
        return jsonify({'success': False, 'error': 'Categoría no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
