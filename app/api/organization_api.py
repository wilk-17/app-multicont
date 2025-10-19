"""
Organization API - REST Endpoints
Gestiona organizaciones con eager loading de sucursales.
"""
from flask import Blueprint, request, jsonify
from app.use_cases.organization_handler import OrganizationHandler
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.utils.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

organization_api = Blueprint('organization_api', __name__, url_prefix='/api/organizations')
handler = OrganizationHandler()

@organization_api.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todas las organizaciones con eager loading de sucursales
    ---
    tags:
      - Organizaciones
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
    responses:
      200:
        description: Lista de organizaciones con sucursales cargadas
      401:
        description: No autenticado
      500:
        description: Error del servidor
    """
    try:
        page, per_page = parse_pagination_params(request)
        result = handler.list_all_with_branches(page=page, per_page=per_page)
        
        return paginated_response(
            items=[item.to_dict() for item in result['items']],
            total=result['total'],
            page=result['page'],
            per_page=result['per_page'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        return error_response(str(e), 500)

@organization_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene una organización por ID
    ---
    tags:
      - Organizaciones
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Organización encontrada
      404:
        description: No encontrada
    """
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('Organización no encontrada', 404)
    except Exception as e:
        return error_response(str(e), 500)

@organization_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN')
def create():
    """
    Crea una nueva organización (Solo ADMIN)
    ---
    tags:
      - Organizaciones
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - current_name
            - legal_name
          properties:
            current_name:
              type: string
              example: "TechCorp"
            legal_name:
              type: string
              example: "TechCorp S.A."
            tax_id:
              type: string
              example: "B12345678"
            address:
              type: string
            phone:
              type: string
            email:
              type: string
              format: email
    responses:
      201:
        description: Organización creada
      400:
        description: Datos inválidos
      401:
        description: No autenticado
      403:
        description: Sin permisos
    """
    try:
        data = request.get_json()
        obj = handler.create(**data)
        cache.delete_memoized(get_all)
        
        return success_response(
            data=obj.to_dict(),
            message='Organización creada exitosamente',
            status_code=201
        )
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@organization_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza una organización (ADMIN o MANAGER)
    ---
    tags:
      - Organizaciones
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
        description: Organización actualizada
      404:
        description: No encontrada
    """
    try:
        data = request.get_json()
        obj = handler.update(id, **data)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        return success_response(
            data=obj.to_dict(),
            message='Organización actualizada exitosamente'
        )
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@organization_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina una organización (Solo ADMIN)
    ---
    tags:
      - Organizaciones
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Organización eliminada
      404:
        description: No encontrada
    """
    try:
        deleted = handler.delete(id)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        if deleted:
            return success_response(message='Organización eliminada exitosamente')
        return error_response('Organización no encontrada', 404)
    except Exception as e:
        return error_response(str(e), 500)
