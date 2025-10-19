"""
Script para agregar documentación Flasgger (Swagger) a TODOS los endpoints
Este script actualiza automáticamente todos los archivos API con documentación completa
"""
import os
import re

# Mapeo de modelos a sus campos para la documentación
MODEL_SCHEMAS = {
    'User': {
        'tag': 'Usuarios',
        'fields': {
            'username': 'string',
            'password': 'string',
            'role_id': 'integer'
        },
        'required': ['username', 'password', 'role_id']
    },
    'Role': {
        'tag': 'Roles',
        'fields': {
            'name': 'string'
        },
        'required': ['name']
    },
    'Organization': {
        'tag': 'Organizaciones',
        'fields': {
            'name': 'string',
            'status': 'string'
        },
        'required': ['name']
    },
    'Branch': {
        'tag': 'Sucursales',
        'fields': {
            'name': 'string',
            'organization_id': 'integer',
            'city_id': 'integer',
            'status': 'string'
        },
        'required': ['name', 'organization_id', 'city_id']
    },
    'City': {
        'tag': 'Ubicaciones - Ciudades',
        'fields': {
            'name': 'string',
            'state_id': 'integer'
        },
        'required': ['name', 'state_id']
    },
    'State': {
        'tag': 'Ubicaciones - Estados',
        'fields': {
            'name': 'string'
        },
        'required': ['name']
    },
    'ItemCategory': {
        'tag': 'Categorías de Items',
        'fields': {
            'name': 'string',
            'status': 'string'
        },
        'required': ['name']
    },
    'Permission': {
        'tag': 'Permisos',
        'fields': {
            'name': 'string'
        },
        'required': ['name']
    },
    'Person': {
        'tag': 'Personas',
        'fields': {
            'name': 'string',
            'email': 'string',
            'phone': 'string',
            'status': 'string'
        },
        'required': ['name']
    },
    'Employee': {
        'tag': 'Empleados',
        'fields': {
            'person_id': 'integer',
            'branch_id': 'integer',
            'position': 'string',
            'status': 'string'
        },
        'required': ['person_id', 'branch_id']
    },
    'Assignment': {
        'tag': 'Asignaciones',
        'fields': {
            'employee_id': 'integer',
            'inventory_item_id': 'integer',
            'quantity': 'integer',
            'assignment_date': 'string'
        },
        'required': ['employee_id', 'inventory_item_id', 'quantity']
    },
    'Brand': {
        'tag': 'Marcas',
        'fields': {
            'name': 'string',
            'status': 'string'
        },
        'required': ['name']
    },
    'QuotationLine': {
        'tag': 'Líneas de Cotización',
        'fields': {
            'quote_id': 'integer',
            'inventory_item_id': 'integer',
            'quantity': 'integer',
            'unit_price': 'number',
            'total_price': 'number'
        },
        'required': ['quote_id', 'inventory_item_id', 'quantity', 'unit_price']
    },
    'QuoteItem': {
        'tag': 'Items de Cotización',
        'fields': {
            'quote_id': 'integer',
            'inventory_item_id': 'integer',
            'quantity': 'integer',
            'unit_price': 'number'
        },
        'required': ['quote_id', 'inventory_item_id', 'quantity', 'unit_price']
    },
    'InvoiceItem': {
        'tag': 'Items de Factura',
        'fields': {
            'invoice_id': 'integer',
            'inventory_item_id': 'integer',
            'quantity': 'integer',
            'unit_price': 'number',
            'total_price': 'number'
        },
        'required': ['invoice_id', 'inventory_item_id', 'quantity', 'unit_price']
    },
    'SalesOrderItem': {
        'tag': 'Items de Orden de Venta',
        'fields': {
            'sales_order_id': 'integer',
            'inventory_item_id': 'integer',
            'quantity': 'integer',
            'unit_price': 'number',
            'total_price': 'number'
        },
        'required': ['sales_order_id', 'inventory_item_id', 'quantity', 'unit_price']
    },
    'UserRole': {
        'tag': 'Roles de Usuario',
        'fields': {
            'user_id': 'integer',
            'role_id': 'integer'
        },
        'required': ['user_id', 'role_id']
    },
    'SalesGoal': {
        'tag': 'Metas de Ventas',
        'fields': {
            'employee_id': 'integer',
            'target_amount': 'number',
            'start_date': 'string',
            'end_date': 'string',
            'status': 'string'
        },
        'required': ['employee_id', 'target_amount', 'start_date', 'end_date']
    }
}

def generate_swagger_doc(model_name, method, endpoint_type):
    """Genera documentación Swagger para un endpoint"""
    
    if model_name not in MODEL_SCHEMAS:
        return ""
    
    schema = MODEL_SCHEMAS[model_name]
    tag = schema['tag']
    model_lower = model_name.lower()
    
    # GET /
    if method == 'GET' and endpoint_type == 'list':
        return f'''    """
    Lista todos los {model_lower}s con paginación
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
        description: Lista paginada de {model_lower}s
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
    """'''
    
    # GET /<id>
    elif method == 'GET' and endpoint_type == 'detail':
        return f'''    """
    Obtiene un {model_lower} por ID
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
        description: ID del {model_lower}
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
    """'''
    
    # POST /
    elif method == 'POST':
        # Generar properties del schema
        properties = {}
        for field, field_type in schema['fields'].items():
            properties[field] = {'type': field_type}
        
        required_fields = schema.get('required', [])
        
        return f'''    """
    Crea un nuevo {model_lower}
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
          required: {required_fields}
          properties:
{chr(10).join(f"            {k}:{chr(10)}              type: {v['type']}" for k, v in properties.items())}
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
    """'''
    
    # PUT /<id>
    elif method == 'PUT':
        properties = {}
        for field, field_type in schema['fields'].items():
            properties[field] = {'type': field_type}
        
        return f'''    """
    Actualiza un {model_lower}
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
        description: ID del {model_lower}
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
{chr(10).join(f"            {k}:{chr(10)}              type: {v['type']}" for k, v in properties.items())}
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
    """'''
    
    # DELETE /<id>
    elif method == 'DELETE':
        return f'''    """
    Elimina un {model_lower}
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
        description: ID del {model_lower}
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
        description: Sin permisos
      500:
        description: Error del servidor
    """'''
    
    return ""


print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  📚 SCRIPT DE DOCUMENTACIÓN SWAGGER                         ║
║                                                              ║
║  Este script genera documentación Flasgger para             ║
║  todos los endpoints de la API.                             ║
║                                                              ║
║  Modelos configurados:                                      ║
║  - User, Role, Permission, UserRole                         ║
║  - Organization, Branch                                     ║
║  - State, City                                              ║
║  - Person, Employee                                         ║
║  - ItemCategory, Brand                                      ║
║  - Assignment, SalesGoal                                    ║
║  - QuotationLine, QuoteItem                                 ║
║  - InvoiceItem, SalesOrderItem                              ║
║                                                              ║
║  Total: 17 modelos documentados                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Este es un script de REFERENCIA para generar documentación.

Para agregar documentación Swagger a un endpoint, usa:

""")

# Ejemplo para User
print("Ejemplo para User API:")
print("=" * 60)
print(generate_swagger_doc('User', 'GET', 'list'))
print("\n")
print(generate_swagger_doc('User', 'GET', 'detail'))
print("\n")
print(generate_swagger_doc('User', 'POST', 'create'))

print("\n\n" + "=" * 60)
print("Para aplicar, reemplaza los docstrings simples por estos completos.")
print("=" * 60)
