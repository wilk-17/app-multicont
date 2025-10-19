"""
Quote API - REST Endpoints (Refactored with Caching)
Gestiona las cotizaciones del sistema con validación Marshmallow.

Usa utilidades de helpers para respuestas JSON estandarizadas.
Implementa caching para mejorar performance.
"""
from flask import Blueprint, request
from marshmallow import ValidationError
from app import cache
from app.use_cases.quote_handler import QuoteHandler
from app.schemas import (
    quote_create_schema,
    quote_update_schema,
    quote_response_schema,
    quotes_response_schema
)
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)

quote_api = Blueprint('quote_api', __name__, url_prefix='/api/quotes')
handler = QuoteHandler()

@quote_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
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
        # Parsear parámetros de paginación con utilidades
        page, per_page = parse_pagination_params(default_per_page=10)
        
        # Obtener datos paginados
        result = handler.list_all(page=page, per_page=per_page)
        
        # Serializar items con Marshmallow
        serialized_items = quotes_response_schema.dump(result['items'])
        
        # Preparar datos para respuesta paginada
        paginated_data = {
            'items': serialized_items,
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages']
        }
        
        # Usar utilidad de respuesta paginada
        return paginated_response(paginated_data, "Cotizaciones obtenidas exitosamente")
    except Exception as e:
        return error_response(f"Error al listar cotizaciones: {str(e)}", 500)

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
        if not obj:
            return error_response('Cotización no encontrada', 404)
        
        # Serializar respuesta con Marshmallow
        result = quote_response_schema.dump(obj)
        return success_response(result, "Cotización obtenida exitosamente")
    except Exception as e:
        return error_response(f"Error al obtener cotización: {str(e)}", 500)

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
        
        # Invalidar cache del listado
        
        # Serializar respuesta
        result = quote_response_schema.dump(obj)
        
        return success_response(result, 'Cotización creada exitosamente', 201)
        
    except ValidationError as e:
        # Errores de validación de Marshmallow
        from flask import jsonify
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        # Errores de lógica de negocio
        return error_response(str(e), 400)
        
    except Exception as e:
        # Errores inesperados
        return error_response('Error interno del servidor', 500)

@quote_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza una cotización con validación automática (ADMIN o MANAGER)
    ---
    tags:
      - Cotizaciones
    security:
      - Bearer: []
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
            return error_response('No se proporcionaron datos para actualizar', 400)
        
        # Actualizar cotización con datos validados
        obj = handler.update(id, **validated_data)
        
        if not obj:
            return error_response('Cotización no encontrada', 404)
        
        # Invalidar cache del listado y del detalle
        
        # Serializar respuesta
        result = quote_response_schema.dump(obj)
        
        return success_response(result, 'Cotización actualizada exitosamente')
        
    except ValidationError as e:
        # Errores de validación de Marshmallow
        from flask import jsonify
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        # Cotización no encontrada
        return error_response(str(e), 404)
        
    except Exception as e:
        # Errores inesperados
        return error_response('Error interno del servidor', 500)

@quote_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina una cotización (SOLO ADMIN)
    ---
    tags:
      - Cotizaciones
    security:
      - Bearer: []
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
        if not deleted:
            return error_response('Cotización no encontrada', 404)
        
        # Invalidar cache del listado
        
        return success_response(message='Cotización eliminada exitosamente')
    except Exception as e:
        return error_response(f'Error al eliminar cotización: {str(e)}', 500)
