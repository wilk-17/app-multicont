"""
Quotation Line API - REST Endpoints
"""
from flask import Blueprint, request
from app.use_cases.quotation_line_handler import QuotationLineHandler
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

quotation_line_api = Blueprint('quotation_line_api', __name__, url_prefix='/api/quotation-lines')
handler = QuotationLineHandler()

@quotation_line_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """Lista todos los línea de cotizacións con paginación"""
    try:
        page, per_page = parse_pagination_params(request)
        result = handler.list_all(page=page, per_page=per_page)
        return paginated_response(
            items=[item.to_dict() for item in result['items']],
            total=result['total'],
            page=result['page'],
            per_page=result['per_page'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        return error_response(str(e), 500)

@quotation_line_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """Obtiene un línea de cotización por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('Línea de cotización no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@quotation_line_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    """Crea un nuevo línea de cotización"""
    try:
        data = request.get_json()
        # Invalidar cache
        cache.delete_memoized(get_all)
        obj = handler.create(**data)
        return success_response(obj.to_dict(), 'Línea de cotización creado exitosamente', 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@quotation_line_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """Actualiza un línea de cotización"""
    try:
        data = request.get_json()
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        obj = handler.update(id, **data)
        return success_response(obj.to_dict(), 'Línea de cotización actualizado exitosamente')
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)

@quotation_line_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """Elimina un línea de cotización"""
    try:
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        deleted = handler.delete(id)
        if deleted:
            return success_response(message='Línea de cotización eliminado exitosamente')
        return error_response('Línea de cotización no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
