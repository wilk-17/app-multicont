"""
Person API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.person_handler import PersonHandler

person_api = Blueprint('person_api', __name__, url_prefix='/api/persons')
handler = PersonHandler()

@person_api.route('/', methods=['GET'])
def get_all():
    """
    Lista todas las personas con paginación
    ---
    tags:
      - Personas
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Número de página
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Personas por página
    responses:
      200:
        description: Lista de personas
      500:
        description: Error del servidor
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

@person_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Obtiene una persona por ID
    ---
    tags:
      - Personas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Persona encontrada
      404:
        description: Persona no encontrada
    """
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'Persona no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@person_api.route('/', methods=['POST'])
def create():
    """
    Crea una nueva persona
    ---
    tags:
      - Personas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
          properties:
            first_name:
              type: string
              example: "Juan"
            last_name:
              type: string
              example: "Pérez"
            dni:
              type: string
              example: "12345678"
            address:
              type: string
              example: "Calle 123"
            phone:
              type: string
              example: "+1234567890"
            city_id:
              type: integer
              example: 1
    responses:
      201:
        description: Persona creada exitosamente
      400:
        description: Datos inválidos
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['first_name', 'last_name']):
            return jsonify({
                'success': False,
                'error': 'Campos requeridos: first_name, last_name'
            }), 400
        obj = handler.create(**data)
        return jsonify({'success': True, 'message': 'Persona creada exitosamente', 'data': obj.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@person_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Actualiza una persona
    ---
    tags:
      - Personas
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
            first_name:
              type: string
            last_name:
              type: string
            dni:
              type: string
            address:
              type: string
            phone:
              type: string
            city_id:
              type: integer
    responses:
      200:
        description: Persona actualizada exitosamente
      404:
        description: Persona no encontrada
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        obj = handler.update(id, **data)
        return jsonify({'success': True, 'message': 'Persona actualizada exitosamente', 'data': obj.to_dict()}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@person_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Elimina una persona
    ---
    tags:
      - Personas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Persona eliminada exitosamente
      404:
        description: Persona no encontrada
    """
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({'success': True, 'message': 'Persona eliminada exitosamente'}), 200
        return jsonify({'success': False, 'error': 'Persona no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
