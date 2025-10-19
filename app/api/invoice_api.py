"""
Invoice API - REST Endpoints con validación Marshmallow
Gestiona facturas con eager loading de items y validación automática.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.invoice_handler import InvoiceHandler
from app.schemas import (
    invoice_create_schema,
    invoice_update_schema,
    invoice_response_schema,
    invoices_response_schema
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

invoice_api = Blueprint('invoice_api', __name__, url_prefix='/api/invoices')
handler = InvoiceHandler()

@invoice_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todas las facturas con eager loading de items
    ---
    tags:
      - Facturas
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
        enum: [paid, pending, cancelled]
        description: Filtrar por estado de pago
    responses:
      200:
        description: Lista de facturas con items cargados (evita N+1 queries)
      401:
        description: No autenticado
    """
    try:
        page, per_page = parse_pagination_params(request)
        status = request.args.get('status')
        
        # Usar eager loading para evitar N+1 queries
        result = handler.list_all_with_items(page=page, per_page=per_page, status=status)
        serialized_items = invoices_response_schema.dump(result['items'])
        
        return paginated_response(
            items=serialized_items,
            total=result['total'],
            page=result['page'],
            per_page=result['per_page'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        return error_response(str(e), 500)

@invoice_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene una factura por ID
    ---
    tags:
      - Facturas
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Factura encontrada
      404:
        description: Factura no encontrada
    """
    try:
        obj = handler.get(id)
        if obj:
            result = invoice_response_schema.dump(obj)
            return success_response(result)
        return error_response('Factura no encontrada', 404)
    except Exception as e:
        return error_response(str(e), 500)

@invoice_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    """
    Crea una nueva factura (ADMIN o MANAGER)
    ---
    tags:
      - Facturas
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
            - invoice_date
            - total
          properties:
            customer_name:
              type: string
              example: "Acme Corp"
            invoice_date:
              type: string
              format: date
              example: "2024-10-15"
            due_date:
              type: string
              format: date
            total:
              type: number
              example: 1500.00
            status:
              type: string
              enum: [paid, pending, cancelled]
              default: pending
    responses:
      201:
        description: Factura creada
      400:
        description: Datos inválidos
      403:
        description: Sin permisos
    """
    try:
        validated_data = invoice_create_schema.load(request.get_json())
        obj = handler.create(**validated_data)
        cache.delete_memoized(get_all)
        
        result = invoice_response_schema.dump(obj)
        return success_response(
            data=result,
            message='Factura creada exitosamente',
            status_code=201
        )
    except ValidationError as e:
        return error_response('Datos de validación incorrectos', 400, errors=e.messages)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@invoice_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza una factura
    ---
    tags:
      - Facturas
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
        description: Factura actualizada
      404:
        description: No encontrada
    """
    try:
        validated_data = invoice_update_schema.load(request.get_json())
        if not validated_data:
            return error_response('No se proporcionaron datos para actualizar', 400)
        
        obj = handler.update(id, **validated_data)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        result = invoice_response_schema.dump(obj)
        return success_response(data=result, message='Factura actualizada exitosamente')
    except ValidationError as e:
        return error_response('Datos de validación incorrectos', 400, errors=e.messages)
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@invoice_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina una factura (Solo ADMIN)
    ---
    tags:
      - Facturas
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Factura eliminada
      404:
        description: No encontrada
    """
    try:
        deleted = handler.delete(id)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        if deleted:
            return success_response(message='Factura eliminada exitosamente')
        return error_response('Factura no encontrada', 404)
    except Exception as e:
        return error_response(str(e), 500)
