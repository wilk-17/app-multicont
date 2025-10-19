"""
InventoryItem API - REST Endpoints con validación Marshmallow
Gestiona items de inventario con stock control y validación automática.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.use_cases.inventory_item_handler import InventoryItemHandler
from app.schemas import (
    inventory_item_create_schema,
    inventory_item_update_schema,
    inventory_item_response_schema,
    inventory_items_response_schema
)
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

inventory_item_api = Blueprint('inventory_item_api', __name__, url_prefix='/api/inventory_items')
handler = InventoryItemHandler()

@inventory_item_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todos los items de inventario con paginación y cache (5 min)
    ---
    tags:
      - Inventory Items
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
        enum: [active, inactive]
        description: Filtrar por estado
    responses:
      200:
        description: Lista paginada de items de inventario
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                items:
                  type: array
                  items:
                    $ref: '#/definitions/InventoryItem'
                total:
                  type: integer
                  example: 150
                page:
                  type: integer
                  example: 1
                per_page:
                  type: integer
                  example: 10
                total_pages:
                  type: integer
                  example: 15
      500:
        description: Error interno del servidor
    """
    try:
        page, per_page = parse_pagination_params()
        status = request.args.get('status')
        result = handler.list_all(page=page, per_page=per_page, status=status)
        
        # Serializar con Marshmallow
        serialized_items = inventory_items_response_schema.dump(result['items'])
        
        paginated_data = {
            'items': serialized_items,
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages']
        }
        
        return paginated_response(paginated_data)
    except Exception as e:
        return error_response(str(e), 500)

@inventory_item_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene un item de inventario por ID
    ---
    tags:
      - Inventory Items
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del item de inventario
    responses:
      200:
        description: Item de inventario encontrado
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              $ref: '#/definitions/InventoryItem'
      404:
        description: Item no encontrado
      500:
        description: Error del servidor
    """
    try:
        obj = handler.get(id)
        if obj:
            result = inventory_item_response_schema.dump(obj)
            return success_response(result)
        return error_response('Item de inventario no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@inventory_item_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    """
    Crea un nuevo item de inventario con validación automática (ADMIN o MANAGER)
    ---
    tags:
      - Inventory Items
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - sku
            - quantity
            - unit_price
          properties:
            name:
              type: string
              example: "Laptop Dell XPS 15"
              description: Nombre del item
            sku:
              type: string
              example: "DELL-XPS-15-001"
              description: SKU único del producto
            description:
              type: string
              example: "Laptop profesional con pantalla 4K"
            quantity:
              type: integer
              example: 50
              description: Cantidad en stock
            unit_price:
              type: number
              format: float
              example: 1299.99
              description: Precio unitario
            category_id:
              type: integer
              example: 1
              description: ID de la categoría
            branch_id:
              type: integer
              example: 1
              description: ID de la sucursal
    responses:
      201:
        description: Item creado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Item de inventario creado exitosamente"
            data:
              $ref: '#/definitions/InventoryItem'
      400:
        description: Datos inválidos
      500:
        description: Error del servidor
    """
    try:
        # Validar datos con Marshmallow
        validated_data = inventory_item_create_schema.load(request.get_json())
        
        # Crear item
        obj = handler.create(**validated_data)
        
        # Invalidar cache
        
        # Serializar respuesta
        result = inventory_item_response_schema.dump(obj)
        
        return success_response(
            data=result,
            message='Item de inventario creado exitosamente',
            status_code=201
        )
        
    except ValidationError as e:
        return error_response(
            f'Datos de validación incorrectos: {e.messages}',
            status_code=400
        )
        
    except ValueError as e:
        return error_response(str(e), 400)
        
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@inventory_item_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza un item de inventario con validación automática (ADMIN o MANAGER)
    ---
    tags:
      - Inventory Items
    security:
      - Bearer: []
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
            quantity:
              type: integer
            unit_price:
              type: number
            status:
              type: string
              enum: [active, inactive]
    responses:
      200:
        description: Item actualizado exitosamente
      400:
        description: Datos inválidos
      404:
        description: Item no encontrado
      500:
        description: Error del servidor
    """
    try:
        # Validar datos con Marshmallow
        validated_data = inventory_item_update_schema.load(request.get_json())
        
        if not validated_data:
            return error_response('No se proporcionaron datos para actualizar', 400)
        
        # Actualizar item
        obj = handler.update(id, **validated_data)
        
        # Invalidar cache
        
        # Serializar respuesta
        result = inventory_item_response_schema.dump(obj)
        
        return success_response(
            data=result,
            message='Item de inventario actualizado exitosamente'
        )
        
    except ValidationError as e:
        return error_response(
            f'Datos de validación incorrectos: {e.messages}',
            status_code=400
        )
        
    except ValueError as e:
        return error_response(str(e), 404)
        
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@inventory_item_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina un item de inventario (SOLO ADMIN)
    ---
    tags:
      - Inventory Items
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del item a eliminar
    responses:
      200:
        description: Item eliminado exitosamente
      404:
        description: Item no encontrado
      500:
        description: Error del servidor
    """
    try:
        deleted = handler.delete(id)
        
        # Invalidar cache
        
        if deleted:
            return success_response(message='Item de inventario eliminado exitosamente')
        return error_response('Item de inventario no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
