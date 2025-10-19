"""
Quote API - REST Endpoints
Gestiona las cotizaciones del sistema con validación Marshmallow
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.quote_handler import QuoteHandler
from app.schemas import (
    quote_create_schema,
    quote_update_schema,
    quote_response_schema,
    quotes_response_schema
)
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

quote_api = Blueprint('quote_api', __name__, url_prefix='/api/quotes')
handler = QuoteHandler()

@quote_api.route('/', methods=['GET'])
@jwt_required()
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
        
        # Serializar respuesta con Marshmallow
        serialized_items = quotes_response_schema.dump(result['items'])
        
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

@quote_api.route('/<int:id>', methods=['GET'])
@jwt_required()
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
            # Serializar respuesta con Marshmallow
            result = quote_response_schema.dump(obj)
            return jsonify({'success': True, 'data': result}), 200
        return jsonify({'success': False, 'error': 'Cotización no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@quote_api.route('/', methods=['POST'])
@jwt_required()
def create():
    """
    Crea una nueva cotización con validación automática
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
          properties:
            customer_name:
              type: string
              minLength: 3
              maxLength: 200
              example: "Empresa ABC S.A."
              description: Nombre del cliente (3-200 caracteres)
            date:
              type: string
              format: date
              example: "2025-01-15"
              description: Fecha de la cotización (no puede ser futura)
            employee_id:
              type: integer
              example: 1
              description: ID del empleado (opcional)
            items:
              type: array
              description: Líneas de items de la cotización
              items:
                type: object
                required:
                  - inventory_item_id
                  - quantity
                  - unit_price
                properties:
                  inventory_item_id:
                    type: integer
                    minimum: 1
                    description: ID del item de inventario
                  quantity:
                    type: integer
                    minimum: 1
                    description: Cantidad del item
                  unit_price:
                    type: number
                    minimum: 0
                    description: Precio unitario
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
            errors:
              type: object
              description: Errores de validación detallados
            message:
              type: string
      500:
        description: Error del servidor
    """
    try:
        # Validar datos de entrada con Marshmallow
        validated_data = quote_create_schema.load(request.get_json())
        
        # Crear cotización con datos validados
        obj = handler.create(**validated_data)
        
        # Serializar respuesta
        result = quote_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Cotización creada exitosamente',
            'data': result
        }), 201
        
    except ValidationError as e:
        # Errores de validación de Marshmallow
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        # Errores de lógica de negocio
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        # Errores inesperados
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@quote_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    """
    Actualiza una cotización con validación automática
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
              minLength: 3
              maxLength: 200
              description: Nombre del cliente
            date:
              type: string
              format: date
              description: Fecha de la cotización (no puede ser futura)
    responses:
      200:
        description: Cotización actualizada exitosamente
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
        description: Datos inválidos
        schema:
          type: object
          properties:
            success:
              type: boolean
            errors:
              type: object
            message:
              type: string
      404:
        description: Cotización no encontrada
      500:
        description: Error del servidor
    """
    try:
        # Validar datos de entrada con Marshmallow
        validated_data = quote_update_schema.load(request.get_json())
        
        if not validated_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        # Actualizar cotización con datos validados
        obj = handler.update(id, **validated_data)
        
        # Serializar respuesta
        result = quote_response_schema.dump(obj)
        
        return jsonify({
            'success': True,
            'message': 'Cotización actualizada exitosamente',
            'data': result
        }), 200
        
    except ValidationError as e:
        # Errores de validación de Marshmallow
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        # Cotización no encontrada
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
        
    except Exception as e:
        # Errores inesperados
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@quote_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
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
