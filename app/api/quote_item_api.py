"""
QuoteItem API - REST Endpoints con documentación Swagger completa
"""
from flask import Blueprint, request
from app.use_cases.quote_item_handler import QuoteItemHandler
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

quote_item_api = Blueprint('quote_item_api', __name__, url_prefix='/api/items de cotización')
handler = QuoteItemHandler()

@quote_item_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todos los items de cotización con paginación
    ---
    tags:
      - Items de Cotización
    security:
      - Bearer: []
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
        description: Items por página (máx 100)
      - name: status
        in: query
        type: string
        description: Filtrar por estado
    responses:
      200:
        description: Lista paginada de items de cotización
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
                    $ref: '#/definitions/QuoteItem'
                pagination:
                  type: object
                  properties:
                    total:
                      type: integer
                    page:
                      type: integer
                    per_page:
                      type: integer
                    total_pages:
                      type: integer
      401:
        description: No autenticado
      500:
        description: Error del servidor
    """
    try:
        page, per_page = parse_pagination_params()
        result = handler.list_all(page=page, per_page=per_page)
        paginated_data = {
            'items': [item.to_dict() for item in result['items']],
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages']
        }
        
        return paginated_response(paginated_data)
    except Exception as e:
        return error_response(str(e), 500)

@quote_item_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene un item de cotización por ID
    ---
    tags:
      - Items de Cotización
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del item de cotización
    responses:
      200:
        description: QuoteItem encontrado
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/QuoteItem'
      404:
        description: QuoteItem no encontrado
      401:
        description: No autenticado
      500:
        description: Error del servidor
    """
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('QuoteItem no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@quote_item_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER', 'SALES')
def create():
    """
    Crea un nuevo item de cotización
    ---
    tags:
      - Items de Cotización
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - quote_id
            - inventory_item_id
            - quantity
            - unit_price
          properties:
            quote_id:
              type: integer
              example: 1
            inventory_item_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 5
            unit_price:
              type: number
              example: 200000.00
    responses:
      201:
        description: QuoteItem creado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/QuoteItem'
            message:
              type: string
      400:
        description: Datos inválidos
      401:
        description: No autenticado
      403:
        description: Sin permisos
      500:
        description: Error del servidor
    """
    try:
        data = request.get_json()
        # Invalidar cache
        obj = handler.create(**data)
        return success_response(obj.to_dict(), 'QuoteItem creado exitosamente', 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@quote_item_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza un item de cotización
    ---
    tags:
      - Items de Cotización
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del item de cotización
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            quote_id:
              type: integer
            inventory_item_id:
              type: integer
            quantity:
              type: integer
            unit_price:
              type: number
    responses:
      200:
        description: QuoteItem actualizado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/QuoteItem'
            message:
              type: string
      404:
        description: QuoteItem no encontrado
      400:
        description: Datos inválidos
      401:
        description: No autenticado
      403:
        description: Sin permisos
      500:
        description: Error del servidor
    """
    try:
        data = request.get_json()
        # Invalidar cache
        obj = handler.update(id, **data)
        return success_response(obj.to_dict(), 'QuoteItem actualizado exitosamente')
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)

@quote_item_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina un item de cotización
    ---
    tags:
      - Items de Cotización
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del item de cotización a eliminar
    responses:
      200:
        description: QuoteItem eliminado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: QuoteItem no encontrado
      401:
        description: No autenticado
      403:
        description: Sin permisos (solo ADMIN)
      500:
        description: Error del servidor
    """
    try:
        # Invalidar cache
        deleted = handler.delete(id)
        if deleted:
            return success_response(message='QuoteItem eliminado exitosamente')
        return error_response('QuoteItem no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
