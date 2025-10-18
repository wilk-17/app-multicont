"""
Quote API - REST Endpoints
Gestiona las cotizaciones del sistema
"""
from flask import Blueprint, request, jsonify
from app.use_cases.quote_handler import QuoteHandler

quote_api = Blueprint('quote_api', __name__, url_prefix='/api/quotes')
handler = QuoteHandler()

@quote_api.route('/', methods=['GET'])
def get_all():
    """
    Lista todas las cotizaciones con paginación
    ---
    tags:
      - Cotizaciones
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
        description: Cotizaciones por página
    responses:
      200:
        description: Lista de cotizaciones
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                items:
                  type: array
                  items:
                    $ref: '#/definitions/Quote'
                total:
                  type: integer
                page:
                  type: integer
                per_page:
                  type: integer
                total_pages:
                  type: integer
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

@quote_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Obtiene una cotización por ID
    ---
    tags:
      - Cotizaciones
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la cotización
    responses:
      200:
        description: Cotización encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/Quote'
      404:
        description: Cotización no encontrada
      500:
        description: Error del servidor
    """
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({'success': True, 'data': obj.to_dict()}), 200
        return jsonify({'success': False, 'error': 'Cotización no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@quote_api.route('/', methods=['POST'])
def create():
    """
    Crea una nueva cotización
    ---
    tags:
      - Cotizaciones
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - date
            - total
          properties:
            customer_name:
              type: string
              example: "Empresa ABC S.A."
              description: Nombre del cliente
            date:
              type: string
              format: date
              example: "2025-01-15"
              description: Fecha de la cotización
            total:
              type: number
              format: double
              example: 1500.50
              description: Total de la cotización
    responses:
      201:
        description: Cotización creada exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Quote'
      400:
        description: Datos inválidos o faltantes
        schema:
          type: object
          properties:
            success:
              type: boolean
            error:
              type: string
      500:
        description: Error del servidor
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data or not all(k in data for k in ['customer_name', 'date', 'total']):
            return jsonify({
                'success': False,
                'error': 'Campos requeridos: customer_name, date, total'
            }), 400
        
        obj = handler.create(**data)
        return jsonify({
            'success': True,
            'message': 'Cotización creada exitosamente',
            'data': obj.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@quote_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Actualiza una cotización
    ---
    tags:
      - Cotizaciones
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la cotización
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_name:
              type: string
              description: Nombre del cliente
            date:
              type: string
              format: date
              description: Fecha de la cotización
            total:
              type: number
              format: double
              description: Total de la cotización
    responses:
      200:
        description: Cotización actualizada exitosamente
      400:
        description: Datos inválidos
      404:
        description: Cotización no encontrada
      500:
        description: Error del servidor
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        obj = handler.update(id, **data)
        return jsonify({
            'success': True,
            'message': 'Cotización actualizada exitosamente',
            'data': obj.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@quote_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Elimina una cotización
    ---
    tags:
      - Cotizaciones
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la cotización
    responses:
      200:
        description: Cotización eliminada exitosamente
      404:
        description: Cotización no encontrada
      500:
        description: Error del servidor
    """
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Cotización eliminada exitosamente'
            }), 200
        return jsonify({
            'success': False,
            'error': 'Cotización no encontrada'
        }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
