"""
SalesOrder API - REST Endpoints con validación Marshmallow
Gestiona órdenes de venta con eager loading de items y workflow de estados.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.sales_order_handler import SalesOrderHandler
from app.schemas import (
    sales_order_create_schema,
    sales_order_update_schema,
    sales_order_response_schema,
    sales_orders_response_schema
)
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

sales_order_api = Blueprint('sales_order_api', __name__, url_prefix='/api/sales_orders')
handler = SalesOrderHandler()

@sales_order_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todas las órdenes de venta con eager loading de items
    ---
    tags:
      - Órdenes de Venta
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: status
        in: query
        type: string
        enum: [pending, confirmed, shipped, delivered, cancelled]
        description: Filtrar por estado del pedido
    responses:
      200:
        description: Lista de órdenes con items cargados (evita N+1 queries)
      401:
        description: No autenticado
    """
    try:
        page, per_page = parse_pagination_params(request)
        status = request.args.get('status')
        
        # Usar eager loading para evitar N+1 queries
        result = handler.list_all_with_items(page=page, per_page=per_page, status=status)
        serialized_items = sales_orders_response_schema.dump(result['items'])
        
        return paginated_response(
            items=serialized_items,
            total=result['total'],
            page=result['page'],
            per_page=result['per_page'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        return error_response(str(e), 500)

@sales_order_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene una orden de venta por ID
    ---
    tags:
      - Órdenes de Venta
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Orden encontrada
      404:
        description: Orden no encontrada
    """
    try:
        obj = handler.get(id)
        if obj:
            result = sales_order_response_schema.dump(obj)
            return success_response(result)
        return error_response('Orden de venta no encontrada', 404)
    except Exception as e:
        return error_response(str(e), 500)

@sales_order_api.route('/', methods=['POST'])
@jwt_required()
def create():
    """
    Crea una nueva orden de venta
    ---
    tags:
      - Órdenes de Venta
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - order_date
            - total
          properties:
            customer_name:
              type: string
              example: "Cliente Premium S.A."
            order_date:
              type: string
              format: date
              example: "2024-10-15"
            delivery_date:
              type: string
              format: date
            total:
              type: number
              example: 2500.00
            status:
              type: string
              enum: [pending, confirmed, shipped, delivered, cancelled]
              default: pending
    responses:
      201:
        description: Orden creada exitosamente
      400:
        description: Datos inválidos
    """
    try:
        validated_data = sales_order_create_schema.load(request.get_json())
        obj = handler.create(**validated_data)
        cache.delete_memoized(get_all)
        
        result = sales_order_response_schema.dump(obj)
        return success_response(
            data=result,
            message='Orden de venta creada exitosamente',
            status_code=201
        )
    except ValidationError as e:
        return error_response('Datos de validación incorrectos', 400, errors=e.messages)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@sales_order_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza una orden de venta (ADMIN o MANAGER)
    ---
    tags:
      - Órdenes de Venta
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
    responses:
      200:
        description: Orden actualizada
      404:
        description: No encontrada
    """
    try:
        validated_data = sales_order_update_schema.load(request.get_json())
        if not validated_data:
            return error_response('No se proporcionaron datos para actualizar', 400)
        
        obj = handler.update(id, **validated_data)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        result = sales_order_response_schema.dump(obj)
        return success_response(data=result, message='Orden de venta actualizada exitosamente')
    except ValidationError as e:
        return error_response('Datos de validación incorrectos', 400, errors=e.messages)
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@sales_order_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina una orden de venta (Solo ADMIN)
    ---
    tags:
      - Órdenes de Venta
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Orden eliminada
      404:
        description: No encontrada
    """
    try:
        deleted = handler.delete(id)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        if deleted:
            return success_response(message='Orden de venta eliminada exitosamente')
        return error_response('Orden de venta no encontrada', 404)
    except Exception as e:
        return error_response(str(e), 500)
