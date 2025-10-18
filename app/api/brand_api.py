"""
Brand API - REST endpoints para marcas de productos
"""
from flask import Blueprint, request, jsonify
from app.use_cases.brand_handler import BrandHandler

brand_api = Blueprint('brand_api', __name__, url_prefix='/api/brands')
handler = BrandHandler()


@brand_api.route('/', methods=['GET'])
def list_brands():
    """
    Listar todas las marcas
    ---
    tags:
      - Brand
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
        description: Lista de marcas
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
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


@brand_api.route('/<int:id>', methods=['GET'])
def get_brand(id):
    """
    Obtener marca por ID
    ---
    tags:
      - Brand
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Marca encontrada
      404:
        description: Marca no encontrada
    """
    brand = handler.get(id)
    if brand:
        return jsonify({'success': True, 'data': brand.to_dict()}), 200
    return jsonify({'success': False, 'error': 'Brand not found'}), 404


@brand_api.route('/name/<string:name>', methods=['GET'])
def get_brand_by_name(name):
    """
    Obtener marca por nombre
    ---
    tags:
      - Brand
    parameters:
      - name: name
        in: path
        type: string
        required: true
    responses:
      200:
        description: Marca encontrada
      404:
        description: Marca no encontrada
    """
    brand = handler.get_by_name(name)
    if brand:
        return jsonify({'success': True, 'data': brand.to_dict()}), 200
    return jsonify({'success': False, 'error': 'Brand not found'}), 404


@brand_api.route('/', methods=['POST'])
def create_brand():
    """
    Crear nueva marca
    ---
    tags:
      - Brand
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
              example: Samsung
            description:
              type: string
              example: Fabricante de electrónicos
    responses:
      201:
        description: Marca creada exitosamente
      400:
        description: Datos inválidos o marca duplicada
    """
    data = request.get_json()
    
    # Validar campos requeridos
    if not data or 'name' not in data:
        return jsonify({'success': False, 'error': 'Field "name" is required'}), 400
    
    try:
        brand = handler.create(
            name=data['name'],
            description=data.get('description')
        )
        return jsonify({
            'success': True,
            'data': brand.to_dict(),
            'message': 'Brand created successfully'
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@brand_api.route('/<int:id>', methods=['PUT'])
def update_brand(id):
    """
    Actualizar marca
    ---
    tags:
      - Brand
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
            description:
              type: string
    responses:
      200:
        description: Marca actualizada exitosamente
      400:
        description: Datos inválidos
      404:
        description: Marca no encontrada
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    try:
        brand = handler.update(id, **data)
        return jsonify({
            'success': True,
            'data': brand.to_dict(),
            'message': 'Brand updated successfully'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@brand_api.route('/<int:id>', methods=['DELETE'])
def delete_brand(id):
    """
    Eliminar marca
    ---
    tags:
      - Brand
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Marca eliminada exitosamente
      404:
        description: Marca no encontrada
      409:
        description: Marca tiene items asociados
    """
    try:
        handler.delete(id)
        return jsonify({
            'success': True,
            'message': 'Brand deleted successfully'
        }), 200
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg:
            return jsonify({'success': False, 'error': error_msg}), 404
        else:
            return jsonify({'success': False, 'error': error_msg}), 409
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@brand_api.route('/count', methods=['GET'])
def count_brands():
    """
    Contar total de marcas
    ---
    tags:
      - Brand
    responses:
      200:
        description: Total de marcas
    """
    try:
        total = handler.count()
        return jsonify({'success': True, 'data': {'total': total}}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
