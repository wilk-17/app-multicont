"""
Permission API - REST Endpoints con documentación Swagger completa
"""
from flask import Blueprint, request
from app.use_cases.permission_handler import PermissionHandler
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

permission_api = Blueprint('permission_api', __name__, url_prefix='/api/permisos')
handler = PermissionHandler()

@permission_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todos los permisos con paginación
    ---
    tags:
      - Permisos
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
        description: Lista paginada de permisos
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
                    $ref: '#/definitions/Permission'
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

@permission_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene un permiso por ID
    ---
    tags:
      - Permisos
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del permiso
    responses:
      200:
        description: Permission encontrado
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/Permission'
      404:
        description: Permission no encontrado
      401:
        description: No autenticado
      500:
        description: Error del servidor
    """
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('Permission no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@permission_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN')
def create():
    """
    Crea un nuevo permiso (SOLO ADMIN)
    ---
    tags:
      - Permisos
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
          properties:
            name:
              type: string
              example: "inventory:write"
              description: Nombre del permiso (usar formato modulo:accion)
    responses:
      201:
        description: Permission creado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/Permission'
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
        return success_response(obj.to_dict(), 'Permission creado exitosamente', 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@permission_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN')
def update(id):
    """
    Actualiza un permiso (SOLO ADMIN)
    ---
    tags:
      - Permisos
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del permiso
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre del permiso
    responses:
      200:
        description: Permission actualizado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/Permission'
            message:
              type: string
      404:
        description: Permission no encontrado
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
        return success_response(obj.to_dict(), 'Permission actualizado exitosamente')
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)

@permission_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina un permiso
    ---
    tags:
      - Permisos
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del permiso a eliminar
    responses:
      200:
        description: Permission eliminado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: Permission no encontrado
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
            return success_response(message='Permission eliminado exitosamente')
        return error_response('Permission no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
