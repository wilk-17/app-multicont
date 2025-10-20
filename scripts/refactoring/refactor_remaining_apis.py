"""
Script Final de Refactorización de APIs
Refactoriza las 17 APIs restantes con helpers + caching (sin YAML docs)
"""

import os
import re

# APIs a refactorizar (quedan 17 después de branch_api)
APIS = [
    'person_api', 'role_api', 'permission_api', 'item_category_api',
    'brand_api', 'quotation_line_api', 'quote_item_api', 'invoice_item_api',
    'sales_order_item_api', 'state_api', 'city_api', 'assignment_api',
    'user_role_api', 'sales_goal_api', 'user_api', 'auth_api', 'metrics_api'
]

API_DIR = os.path.join(os.path.dirname(__file__), 'app', 'api')

TEMPLATE = """\"\"\"
{title} API - REST Endpoints
\"\"\"
from flask import Blueprint, request
from app.use_cases.{handler_name} import {handler_class}
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

{blueprint_name} = Blueprint('{blueprint_name}', __name__, url_prefix='/api/{url_prefix}')
handler = {handler_class}()

@{blueprint_name}.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    \"\"\"Lista todos los {resource_name}s con paginación\"\"\"
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

@{blueprint_name}.route('/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_by_id(id):
    \"\"\"Obtiene un {resource_name} por ID\"\"\"
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('{resource_name_cap} no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@{blueprint_name}.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    \"\"\"Crea un nuevo {resource_name}\"\"\"
    try:
        data = request.get_json()
        # Invalidar cache
        cache.delete_memoized(get_all)
        obj = handler.create(**data)
        return success_response(obj.to_dict(), '{resource_name_cap} creado exitosamente', 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@{blueprint_name}.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    \"\"\"Actualiza un {resource_name}\"\"\"
    try:
        data = request.get_json()
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        obj = handler.update(id, **data)
        return success_response(obj.to_dict(), '{resource_name_cap} actualizado exitosamente')
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)

@{blueprint_name}.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    \"\"\"Elimina un {resource_name}\"\"\"
    try:
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        deleted = handler.delete(id)
        if deleted:
            return success_response(message='{resource_name_cap} eliminado exitosamente')
        return error_response('{resource_name_cap} no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
"""

API_METADATA = {
    'person_api': {'handler': 'person_handler', 'class': 'PersonHandler', 'resource': 'persona', 'resource_cap': 'Persona', 'url': 'persons', 'title': 'Person'},
    'role_api': {'handler': 'role_handler', 'class': 'RoleHandler', 'resource': 'rol', 'resource_cap': 'Rol', 'url': 'roles', 'title': 'Role'},
    'permission_api': {'handler': 'permission_handler', 'class': 'PermissionHandler', 'resource': 'permiso', 'resource_cap': 'Permiso', 'url': 'permissions', 'title': 'Permission'},
    'item_category_api': {'handler': 'item_category_handler', 'class': 'ItemCategoryHandler', 'resource': 'categoría', 'resource_cap': 'Categoría', 'url': 'item-categories', 'title': 'Item Category'},
    'brand_api': {'handler': 'brand_handler', 'class': 'BrandHandler', 'resource': 'marca', 'resource_cap': 'Marca', 'url': 'brands', 'title': 'Brand'},
    'quotation_line_api': {'handler': 'quotation_line_handler', 'class': 'QuotationLineHandler', 'resource': 'línea de cotización', 'resource_cap': 'Línea de cotización', 'url': 'quotation-lines', 'title': 'Quotation Line'},
    'quote_item_api': {'handler': 'quote_item_handler', 'class': 'QuoteItemHandler', 'resource': 'item de cotización', 'resource_cap': 'Item de cotización', 'url': 'quote-items', 'title': 'Quote Item'},
    'invoice_item_api': {'handler': 'invoice_item_handler', 'class': 'InvoiceItemHandler', 'resource': 'item de factura', 'resource_cap': 'Item de factura', 'url': 'invoice-items', 'title': 'Invoice Item'},
    'sales_order_item_api': {'handler': 'sales_order_item_handler', 'class': 'SalesOrderItemHandler', 'resource': 'item de orden', 'resource_cap': 'Item de orden', 'url': 'sales-order-items', 'title': 'Sales Order Item'},
    'state_api': {'handler': 'state_handler', 'class': 'StateHandler', 'resource': 'estado', 'resource_cap': 'Estado', 'url': 'states', 'title': 'State'},
    'city_api': {'handler': 'city_handler', 'class': 'CityHandler', 'resource': 'ciudad', 'resource_cap': 'Ciudad', 'url': 'cities', 'title': 'City'},
    'assignment_api': {'handler': 'assignment_handler', 'class': 'AssignmentHandler', 'resource': 'asignación', 'resource_cap': 'Asignación', 'url': 'assignments', 'title': 'Assignment'},
    'user_role_api': {'handler': 'user_role_handler', 'class': 'UserRoleHandler', 'resource': 'rol de usuario', 'resource_cap': 'Rol de usuario', 'url': 'user-roles', 'title': 'User Role'},
    'sales_goal_api': {'handler': 'sales_goal_handler', 'class': 'SalesGoalHandler', 'resource': 'meta de venta', 'resource_cap': 'Meta de venta', 'url': 'sales-goals', 'title': 'Sales Goal'},
    'user_api': {'handler': 'user_handler', 'class': 'UserHandler', 'resource': 'usuario', 'resource_cap': 'Usuario', 'url': 'users', 'title': 'User'},
}


def refactor_api(api_name):
    """Refactoriza un API específico"""
    
    file_path = os.path.join(API_DIR, f'{api_name}.py')
    
    if not os.path.exists(file_path):
        print(f"⚠️  {api_name}.py NO EXISTE")
        return False
    
    if api_name not in API_METADATA:
        print(f"⚠️  {api_name} NO TIENE METADATA - saltando")
        return False
    
    meta = API_METADATA[api_name]
    
    print(f"🔧 Refactorizando {api_name}.py...")
    
    # Generar nuevo contenido
    new_content = TEMPLATE.format(
        title=meta['title'],
        handler_name=meta['handler'],
        handler_class=meta['class'],
        blueprint_name=api_name,
        url_prefix=meta['url'],
        resource_name=meta['resource'],
        resource_name_cap=meta['resource_cap']
    )
    
    # Escribir archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {api_name}.py REFACTORIZADO")
    return True


def main():
    print("=" * 70)
    print("REFACTORIZACIÓN FINAL DE APIs".center(70))
    print("=" * 70)
    print(f"\n📋 APIs a refactorizar: {len(APIS)}\n")
    
    success_count = 0
    skipped_count = 0
    
    for api_name in APIS:
        if refactor_api(api_name):
            success_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 70)
    print("✅ REFACTORIZACIÓN COMPLETA".center(70))
    print("=" * 70)
    print(f"\n📊 Resultado:")
    print(f"   ✅ APIs refactorizadas: {success_count}")
    print(f"   ⚠️  APIs saltadas: {skipped_count}")
    print(f"\n🎉 Total: {success_count}/{len(APIS)} completadas!")
    print("\n🚀 Próximo paso: verificar errores y commit\n")


if __name__ == '__main__':
    main()
