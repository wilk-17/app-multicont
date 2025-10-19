"""
Script para actualizar MASIVAMENTE la documentación Swagger de TODOS los endpoints
Actualiza automáticamente role_api, branch_api, city_api, state_api, etc.
"""
import os
import re

# Definición completa de templates Swagger por modelo
SWAGGER_TEMPLATES = {
    'role': {
        'tag': 'Roles',
        'singular': 'rol',
        'plural': 'roles',
        'model_name': 'Role',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "MANAGER"
              description: Nombre del rol""",
        'update_schema': """          properties:
            name:
              type: string
              description: Nombre del rol"""
    },
    'organization': {
        'tag': 'Organizaciones',
        'singular': 'organización',
        'plural': 'organizaciones',
        'model_name': 'Organization',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "Empresa ABC"
            status:
              type: string
              example: "active"
              enum: [active, inactive]""",
        'update_schema': """          properties:
            name:
              type: string
            status:
              type: string
              enum: [active, inactive]"""
    },
    'branch': {
        'tag': 'Sucursales',
        'singular': 'sucursal',
        'plural': 'sucursales',
        'model_name': 'Branch',
        'create_schema': """          required:
            - name
            - organization_id
            - city_id
          properties:
            name:
              type: string
              example: "Sucursal Norte"
            organization_id:
              type: integer
              example: 1
            city_id:
              type: integer
              example: 1
            status:
              type: string
              example: "active"
              enum: [active, inactive]""",
        'update_schema': """          properties:
            name:
              type: string
            organization_id:
              type: integer
            city_id:
              type: integer
            status:
              type: string
              enum: [active, inactive]"""
    },
    'city': {
        'tag': 'Ubicaciones - Ciudades',
        'singular': 'ciudad',
        'plural': 'ciudades',
        'model_name': 'City',
        'create_schema': """          required:
            - name
            - state_id
          properties:
            name:
              type: string
              example: "Bogotá"
            state_id:
              type: integer
              example: 1""",
        'update_schema': """          properties:
            name:
              type: string
            state_id:
              type: integer"""
    },
    'state': {
        'tag': 'Ubicaciones - Estados/Departamentos',
        'singular': 'estado',
        'plural': 'estados',
        'model_name': 'State',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "Cundinamarca"
            code:
              type: string
              example: "CUN"
              description: Código del departamento""",
        'update_schema': """          properties:
            name:
              type: string
            code:
              type: string"""
    },
    'item_category': {
        'tag': 'Categorías de Items',
        'singular': 'categoría',
        'plural': 'categorías',
        'model_name': 'ItemCategory',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "Electrónicos"
            status:
              type: string
              example: "active"
              enum: [active, inactive]""",
        'update_schema': """          properties:
            name:
              type: string
            status:
              type: string
              enum: [active, inactive]"""
    },
    'permission': {
        'tag': 'Permisos',
        'singular': 'permiso',
        'plural': 'permisos',
        'model_name': 'Permission',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "inventory:write"
              description: Nombre del permiso (usar formato modulo:accion)""",
        'update_schema': """          properties:
            name:
              type: string
              description: Nombre del permiso"""
    },
    'person': {
        'tag': 'Personas',
        'singular': 'persona',
        'plural': 'personas',
        'model_name': 'Person',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "Juan Pérez"
            email:
              type: string
              example: "juan@example.com"
            phone:
              type: string
              example: "+57 300 123 4567"
            status:
              type: string
              example: "active"
              enum: [active, inactive]""",
        'update_schema': """          properties:
            name:
              type: string
            email:
              type: string
            phone:
              type: string
            status:
              type: string
              enum: [active, inactive]"""
    },
    'employee': {
        'tag': 'Empleados',
        'singular': 'empleado',
        'plural': 'empleados',
        'model_name': 'Employee',
        'create_schema': """          required:
            - person_id
            - branch_id
          properties:
            person_id:
              type: integer
              example: 1
            branch_id:
              type: integer
              example: 1
            position:
              type: string
              example: "Vendedor"
            status:
              type: string
              example: "active"
              enum: [active, inactive]""",
        'update_schema': """          properties:
            person_id:
              type: integer
            branch_id:
              type: integer
            position:
              type: string
            status:
              type: string
              enum: [active, inactive]"""
    },
    'assignment': {
        'tag': 'Asignaciones',
        'singular': 'asignación',
        'plural': 'asignaciones',
        'model_name': 'Assignment',
        'create_schema': """          required:
            - employee_id
            - inventory_item_id
            - quantity
          properties:
            employee_id:
              type: integer
              example: 1
            inventory_item_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 5
            assignment_date:
              type: string
              format: date
              example: "2025-10-19"
            status:
              type: string
              example: "active"
              enum: [active, returned, lost]""",
        'update_schema': """          properties:
            employee_id:
              type: integer
            inventory_item_id:
              type: integer
            quantity:
              type: integer
            assignment_date:
              type: string
              format: date
            status:
              type: string
              enum: [active, returned, lost]"""
    },
    'brand': {
        'tag': 'Marcas',
        'singular': 'marca',
        'plural': 'marcas',
        'model_name': 'Brand',
        'create_schema': """          required:
            - name
          properties:
            name:
              type: string
              example: "Dell"
            status:
              type: string
              example: "active"
              enum: [active, inactive]""",
        'update_schema': """          properties:
            name:
              type: string
            status:
              type: string
              enum: [active, inactive]"""
    },
    'quotation_line': {
        'tag': 'Líneas de Cotización',
        'singular': 'línea de cotización',
        'plural': 'líneas de cotización',
        'model_name': 'QuotationLine',
        'create_schema': """          required:
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
              example: 10
            unit_price:
              type: number
              example: 150000.00
            total_price:
              type: number
              example: 1500000.00
              description: Se calcula automáticamente""",
        'update_schema': """          properties:
            quote_id:
              type: integer
            inventory_item_id:
              type: integer
            quantity:
              type: integer
            unit_price:
              type: number
            total_price:
              type: number"""
    },
    'quote_item': {
        'tag': 'Items de Cotización',
        'singular': 'item de cotización',
        'plural': 'items de cotización',
        'model_name': 'QuoteItem',
        'create_schema': """          required:
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
              example: 200000.00""",
        'update_schema': """          properties:
            quote_id:
              type: integer
            inventory_item_id:
              type: integer
            quantity:
              type: integer
            unit_price:
              type: number"""
    },
    'invoice_item': {
        'tag': 'Items de Factura',
        'singular': 'item de factura',
        'plural': 'items de factura',
        'model_name': 'InvoiceItem',
        'create_schema': """          required:
            - invoice_id
            - inventory_item_id
            - quantity
            - unit_price
          properties:
            invoice_id:
              type: integer
              example: 1
            inventory_item_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 3
            unit_price:
              type: number
              example: 350000.00
            total_price:
              type: number
              example: 1050000.00
              description: Se calcula automáticamente""",
        'update_schema': """          properties:
            invoice_id:
              type: integer
            inventory_item_id:
              type: integer
            quantity:
              type: integer
            unit_price:
              type: number
            total_price:
              type: number"""
    },
    'sales_order_item': {
        'tag': 'Items de Orden de Venta',
        'singular': 'item de orden',
        'plural': 'items de orden',
        'model_name': 'SalesOrderItem',
        'create_schema': """          required:
            - sales_order_id
            - inventory_item_id
            - quantity
            - unit_price
          properties:
            sales_order_id:
              type: integer
              example: 1
            inventory_item_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 7
            unit_price:
              type: number
              example: 280000.00
            total_price:
              type: number
              example: 1960000.00
              description: Se calcula automáticamente""",
        'update_schema': """          properties:
            sales_order_id:
              type: integer
            inventory_item_id:
              type: integer
            quantity:
              type: integer
            unit_price:
              type: number
            total_price:
              type: number"""
    },
    'user_role': {
        'tag': 'Roles de Usuario',
        'singular': 'rol de usuario',
        'plural': 'roles de usuario',
        'model_name': 'UserRole',
        'create_schema': """          required:
            - user_id
            - role_id
          properties:
            user_id:
              type: integer
              example: 1
            role_id:
              type: integer
              example: 2""",
        'update_schema': """          properties:
            user_id:
              type: integer
            role_id:
              type: integer"""
    },
    'sales_goal': {
        'tag': 'Metas de Ventas',
        'singular': 'meta de ventas',
        'plural': 'metas de ventas',
        'model_name': 'SalesGoal',
        'create_schema': """          required:
            - employee_id
            - target_amount
            - start_date
            - end_date
          properties:
            employee_id:
              type: integer
              example: 1
            target_amount:
              type: number
              example: 50000000.00
              description: Monto objetivo en COP
            start_date:
              type: string
              format: date
              example: "2025-10-01"
            end_date:
              type: string
              format: date
              example: "2025-12-31"
            status:
              type: string
              example: "active"
              enum: [active, completed, cancelled]""",
        'update_schema': """          properties:
            employee_id:
              type: integer
            target_amount:
              type: number
            start_date:
              type: string
              format: date
            end_date:
              type: string
              format: date
            status:
              type: string
              enum: [active, completed, cancelled]"""
    }
}

def generate_full_api_file(api_key, template):
    """Genera el contenido completo de un archivo API con documentación Swagger"""
    
    tag = template['tag']
    singular = template['singular']
    plural = template['plural']
    model_name = template['model_name']
    create_schema = template['create_schema']
    update_schema = template['update_schema']
    
    # Determinar el nombre del handler
    handler_name = f"{model_name}Handler"
    
    # Determinar el nombre del blueprint
    blueprint_name = f"{api_key}_api"
    
    content = f'''"""
{model_name} API - REST Endpoints con documentación Swagger completa
"""
from flask import Blueprint, request
from app.use_cases.{api_key}_handler import {handler_name}
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

{blueprint_name} = Blueprint('{blueprint_name}', __name__, url_prefix='/api/{plural}')
handler = {handler_name}()

@{blueprint_name}.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todos los {plural} con paginación
    ---
    tags:
      - {tag}
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
        description: Lista paginada de {plural}
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
                    $ref: '#/definitions/{model_name}'
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
    """
    Obtiene un {singular} por ID
    ---
    tags:
      - {tag}
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del {singular}
    responses:
      200:
        description: {model_name} encontrado
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/{model_name}'
      404:
        description: {model_name} no encontrado
      401:
        description: No autenticado
      500:
        description: Error del servidor
    """
    try:
        obj = handler.get(id)
        if obj:
            return success_response(obj.to_dict())
        return error_response('{model_name} no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@{blueprint_name}.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    """
    Crea un nuevo {singular}
    ---
    tags:
      - {tag}
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
{create_schema}
    responses:
      201:
        description: {model_name} creado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/{model_name}'
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
        cache.delete_memoized(get_all)
        obj = handler.create(**data)
        return success_response(obj.to_dict(), '{model_name} creado exitosamente', 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@{blueprint_name}.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def update(id):
    """
    Actualiza un {singular}
    ---
    tags:
      - {tag}
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del {singular}
      - name: body
        in: body
        required: true
        schema:
          type: object
{update_schema}
    responses:
      200:
        description: {model_name} actualizado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              $ref: '#/definitions/{model_name}'
            message:
              type: string
      404:
        description: {model_name} no encontrado
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
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        obj = handler.update(id, **data)
        return success_response(obj.to_dict(), '{model_name} actualizado exitosamente')
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)

@{blueprint_name}.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    """
    Elimina un {singular}
    ---
    tags:
      - {tag}
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del {singular} a eliminar
    responses:
      200:
        description: {model_name} eliminado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: {model_name} no encontrado
      401:
        description: No autenticado
      403:
        description: Sin permisos (solo ADMIN)
      500:
        description: Error del servidor
    """
    try:
        # Invalidar cache
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        deleted = handler.delete(id)
        if deleted:
            return success_response(message='{model_name} eliminado exitosamente')
        return error_response('{model_name} no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
'''
    
    return content


# Generar archivos
print("=" * 70)
print("GENERANDO ARCHIVOS API CON DOCUMENTACIÓN SWAGGER COMPLETA")
print("=" * 70)
print()

base_path = "c:/Users/wilke/app-multicont/app/api"

files_to_generate = [
    'role', 'organization', 'branch', 'city', 'state',
    'item_category', 'permission', 'person', 'employee',
    'assignment', 'brand', 'quotation_line', 'quote_item',
    'invoice_item', 'sales_order_item', 'user_role', 'sales_goal'
]

for api_key in files_to_generate:
    if api_key in SWAGGER_TEMPLATES:
        filename = f"{api_key}_api.py"
        filepath = os.path.join(base_path, filename)
        content = generate_full_api_file(api_key, SWAGGER_TEMPLATES[api_key])
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename} - Generado")
        except Exception as e:
            print(f"❌ {filename} - Error: {e}")

print()
print("=" * 70)
print("✅ PROCESO COMPLETADO")
print("=" * 70)
print()
print("Archivos actualizados:")
for api_key in files_to_generate:
    if api_key in SWAGGER_TEMPLATES:
        print(f"  - {api_key}_api.py")
print()
print("🔄 Reinicia el servidor Flask para ver los cambios en Swagger:")
print("   python run.py")
print()
print("📖 Swagger UI: http://127.0.0.1:5000/api/docs/")
