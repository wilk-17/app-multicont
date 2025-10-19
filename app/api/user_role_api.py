"""
User Role API - REST Endpoints
"""
from flask import Blueprint, request
from app.use_cases.user_role_handler import UserRoleHandler
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

user_role_api = Blueprint('user_role_api', __name__, url_prefix='/api/user-roles')
handler = UserRoleHandler()

@user_role_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """Lista todos los rol de usuarios con paginación"""
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

@user_role_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """Obtiene un rol de usuario por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('Rol de usuario no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@user_role_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    """Crea un nuevo rol de usuario"""
    try:
        data = request.get_json()
        # Invalidar cache
        cache.delete_memoized(get_all)
        obj = handler.create(**data)
        return success_response(obj.to_dict(), 'Rol de usuario creado exitosamente', 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@user_role_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """Actualiza un rol de usuario"""
    try:
        data = request.get_json()
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        obj = handler.update(id, **data)
        return success_response(obj.to_dict(), 'Rol de usuario actualizado exitosamente')
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)

@user_role_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """Elimina un rol de usuario"""
    try:
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        deleted = handler.delete(id)
        if deleted:
            return success_response(message='Rol de usuario eliminado exitosamente')
        return error_response('Rol de usuario no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
