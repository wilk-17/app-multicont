"""
EJEMPLO DE IMPLEMENTACIÓN: Cómo proteger endpoints con decoradores

Este archivo muestra ejemplos de cómo aplicar los decoradores
de autenticación y autorización a los endpoints existentes.

NO ejecutar este script - es solo referencia visual.
"""

# ============================================
# EJEMPLO 1: Proteger Inventory Items
# ============================================
# Archivo: app/api/inventory_item_api.py

from flask_jwt_extended import jwt_required
from app.services.authorization_service import require_permission

# GET - Solo lectura (inventory:read)
@inventory_item_api.route('/', methods=['GET'])
@jwt_required()  # Requiere estar autenticado
@require_permission('inventory:read')  # Requiere permiso específico
def get_all():
    """
    Resultado:
    - ADMIN: ✅ Tiene inventory:read
    - MANAGER: ✅ Tiene inventory:read  
    - SALES: ✅ Tiene inventory:read
    - Sin token: ❌ 401 Unauthorized
    """
    ...

# POST - Crear (inventory:write)
@inventory_item_api.route('/', methods=['POST'])
@jwt_required()
@require_permission('inventory:write')
def create():
    """
    Resultado:
    - ADMIN: ✅ Tiene inventory:write
    - MANAGER: ✅ Tiene inventory:write
    - SALES: ❌ 403 Forbidden (NO tiene inventory:write)
    """
    ...

# DELETE - Eliminar (inventory:delete)
@inventory_item_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission('inventory:delete')
def delete(id):
    """
    Resultado:
    - ADMIN: ✅ Tiene inventory:delete
    - MANAGER: ❌ 403 Forbidden (NO tiene inventory:delete)
    - SALES: ❌ 403 Forbidden
    """
    ...


# ============================================
# EJEMPLO 2: Proteger Users (solo ADMIN)
# ============================================
# Archivo: app/api/user_api.py

from app.services.authorization_service import admin_required, require_permission

# GET - Ver usuarios (users:read)
@user_api.route('/', methods=['GET'])
@jwt_required()
@require_permission('users:read')
def get_all():
    """
    Resultado:
    - ADMIN: ✅ Tiene users:read
    - MANAGER: ✅ Tiene users:read
    - SALES: ❌ 403 Forbidden (NO tiene users:read)
    """
    ...

# POST - Crear usuarios (users:write)
@user_api.route('/', methods=['POST'])
@jwt_required()
@require_permission('users:write')
def create():
    """
    Resultado:
    - ADMIN: ✅ Tiene users:write
    - MANAGER: ❌ 403 Forbidden (NO tiene users:write)
    - SALES: ❌ 403 Forbidden
    """
    ...

# DELETE - Eliminar usuarios (solo ADMIN)
@user_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()  # Atajo para requiere rol ADMIN
def delete(id):
    """
    Resultado:
    - ADMIN: ✅ Es ADMIN
    - MANAGER: ❌ 403 Forbidden
    - SALES: ❌ 403 Forbidden
    """
    ...


# ============================================
# EJEMPLO 3: Proteger Quotes
# ============================================
# Archivo: app/api/quote_api.py

# GET - Ver cotizaciones (sales:read)
@quote_api.route('/', methods=['GET'])
@jwt_required()
@require_permission('sales:read')
def get_all():
    """
    Resultado:
    - ADMIN: ✅ Tiene sales:read
    - MANAGER: ✅ Tiene sales:read
    - SALES: ✅ Tiene sales:read
    """
    ...

# POST - Crear cotización (sales:create_quote)
@quote_api.route('/', methods=['POST'])
@jwt_required()
@require_permission('sales:create_quote')
def create():
    """
    Resultado:
    - ADMIN: ✅ Tiene sales:create_quote
    - MANAGER: ✅ Tiene sales:create_quote
    - SALES: ✅ Tiene sales:create_quote (¡SALES puede crear!)
    """
    ...

# DELETE - Eliminar cotización (sales:delete)
@quote_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission('sales:delete')
def delete(id):
    """
    Resultado:
    - ADMIN: ✅ Tiene sales:delete
    - MANAGER: ✅ Tiene sales:delete
    - SALES: ❌ 403 Forbidden (NO tiene sales:delete)
    """
    ...


# ============================================
# EJEMPLO 4: Proteger Sales Orders
# ============================================
# Archivo: app/api/sales_order_api.py

# POST - Crear orden de venta (sales:create_order)
@sales_order_api.route('/', methods=['POST'])
@jwt_required()
@require_permission('sales:create_order')
def create():
    """
    Resultado:
    - ADMIN: ✅ Tiene sales:create_order
    - MANAGER: ✅ Tiene sales:create_order
    - SALES: ❌ 403 Forbidden (NO tiene sales:create_order)
    
    SALES puede crear cotizaciones, pero NO órdenes de venta.
    """
    ...


# ============================================
# EJEMPLO 5: Proteger Invoices
# ============================================
# Archivo: app/api/invoice_api.py

# POST - Crear factura (sales:create_invoice)
@invoice_api.route('/', methods=['POST'])
@jwt_required()
@require_permission('sales:create_invoice')
def create():
    """
    Resultado:
    - ADMIN: ✅ Tiene sales:create_invoice
    - MANAGER: ✅ Tiene sales:create_invoice
    - SALES: ❌ 403 Forbidden (NO tiene sales:create_invoice)
    """
    ...


# ============================================
# EJEMPLO 6: Usar múltiples permisos (OR)
# ============================================
from app.services.authorization_service import require_any_permission

@some_api.route('/special', methods=['GET'])
@jwt_required()
@require_any_permission(['admin:all', 'reports:export'])
def special_endpoint():
    """
    Requiere AL MENOS UNO de los permisos listados
    
    Resultado:
    - ADMIN: ✅ Tiene admin:all Y reports:export
    - MANAGER: ✅ Tiene reports:export
    - SALES: ❌ 403 Forbidden (no tiene ninguno)
    """
    ...


# ============================================
# EJEMPLO 7: Usar roles en lugar de permisos
# ============================================
from app.services.authorization_service import require_role, manager_or_admin

# Opción 1: Un solo rol
@some_api.route('/admin-only', methods=['POST'])
@jwt_required()
@require_role('ADMIN')
def admin_only():
    """Solo ADMIN puede acceder"""
    ...

# Opción 2: Múltiples roles
@some_api.route('/managers', methods=['GET'])
@jwt_required()
@require_role(['ADMIN', 'MANAGER'])
def managers():
    """ADMIN o MANAGER pueden acceder"""
    ...

# Opción 3: Atajo para MANAGER o ADMIN
@some_api.route('/approve', methods=['POST'])
@jwt_required()
@manager_or_admin()  # Atajo equivalente a require_role(['ADMIN', 'MANAGER'])
def approve():
    """ADMIN o MANAGER pueden acceder"""
    ...


# ============================================
# EJEMPLO 8: Endpoint sin protección (público)
# ============================================

@public_api.route('/health', methods=['GET'])
def health_check():
    """
    NO tiene @jwt_required() ni @require_permission()
    
    Cualquiera puede acceder, incluso sin token.
    Útil para health checks, info pública, etc.
    """
    return {'status': 'ok'}


# ============================================
# RESUMEN DE DECORADORES DISPONIBLES
# ============================================

"""
1. @jwt_required()
   - Requiere token JWT válido
   - Sin token → 401 Unauthorized

2. @require_permission('permiso')
   - Requiere permiso específico
   - Sin permiso → 403 Forbidden
   - Valida automáticamente admin:all (ADMIN siempre pasa)

3. @require_any_permission(['perm1', 'perm2'])
   - Requiere AL MENOS UNO de los permisos
   - Sin ninguno → 403 Forbidden

4. @require_role('ADMIN')
   - Requiere rol específico
   - Puede ser string o lista: ['ADMIN', 'MANAGER']

5. @admin_required()
   - Atajo para require_role('ADMIN')
   - Solo ADMIN

6. @manager_or_admin()
   - Atajo para require_role(['ADMIN', 'MANAGER'])
   - ADMIN o MANAGER
"""


# ============================================
# ORDEN DE DECORADORES (IMPORTANTE)
# ============================================

"""
Orden correcto:

@blueprint.route(...)
@jwt_required()         # 1. Primero verificar autenticación
@require_permission()   # 2. Luego verificar permisos/roles
def endpoint():
    ...

INCORRECTO (no funciona):

@require_permission()   # ❌ NO puede verificar permisos sin JWT
@jwt_required()         # JWT debería ir primero
def endpoint():
    ...
"""


# ============================================
# EJEMPLO COMPLETO: Inventory Item API
# ============================================

"""
# app/api/inventory_item_api.py

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.use_cases.inventory_item_handler import InventoryItemHandler
from app.services.authorization_service import require_permission
from app.api.helpers import success_response, error_response

inventory_item_api = Blueprint('inventory_item_api', __name__, url_prefix='/api/inventory_items')
handler = InventoryItemHandler()

@inventory_item_api.route('/', methods=['GET'])
@jwt_required()
@require_permission('inventory:read')
def get_all():
    try:
        items = handler.list_all()
        return success_response(items, 'Listado exitoso')
    except Exception as e:
        return error_response(str(e), 500)

@inventory_item_api.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_permission('inventory:read')
def get_one(id):
    try:
        item = handler.get(id)
        if not item:
            return error_response('Item no encontrado', 404)
        return success_response(item, 'Item obtenido')
    except Exception as e:
        return error_response(str(e), 500)

@inventory_item_api.route('/', methods=['POST'])
@jwt_required()
@require_permission('inventory:write')
def create():
    try:
        data = request.get_json()
        item = handler.create(**data)
        return success_response(item, 'Item creado', 201)
    except Exception as e:
        return error_response(str(e), 400)

@inventory_item_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_permission('inventory:write')
def update(id):
    try:
        data = request.get_json()
        item = handler.update(id, **data)
        if not item:
            return error_response('Item no encontrado', 404)
        return success_response(item, 'Item actualizado')
    except Exception as e:
        return error_response(str(e), 400)

@inventory_item_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission('inventory:delete')
def delete(id):
    try:
        success = handler.delete(id)
        if not success:
            return error_response('Item no encontrado', 404)
        return success_response(None, 'Item eliminado')
    except Exception as e:
        return error_response(str(e), 500)
"""


# ============================================
# TESTING RÁPIDO EN TERMINAL
# ============================================

"""
# 1. Login
curl -X POST http://127.0.0.1:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "ana", "password": "ana123"}'

# Respuesta: copiar access_token

# 2. Usar token en requests
curl http://127.0.0.1:5000/api/inventory_items/ \\
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..."

# 3. Probar sin token (debería dar 401)
curl http://127.0.0.1:5000/api/inventory_items/

# 4. Probar con rol sin permisos (403)
# Login como diego (SALES), luego:
curl -X POST http://127.0.0.1:5000/api/inventory_items/ \\
  -H "Authorization: Bearer <diego_token>" \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Test", ...}'
# Debería dar 403 Forbidden
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  📚 EJEMPLOS DE PROTECCIÓN DE ENDPOINTS                     ║
║                                                              ║
║  Este archivo muestra cómo usar los decoradores             ║
║  de autenticación y autorización en tus endpoints.          ║
║                                                              ║
║  Decoradores disponibles:                                   ║
║  - @jwt_required()                                           ║
║  - @require_permission('permiso')                            ║
║  - @require_any_permission([...])                            ║
║  - @require_role('ROL')                                      ║
║  - @admin_required()                                         ║
║  - @manager_or_admin()                                       ║
║                                                              ║
║  Ver código arriba para ejemplos detallados.                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

⚠️  IMPORTANTE: Este archivo es SOLO REFERENCIA.
    NO ejecutarlo - copiar los ejemplos a tus archivos reales.

📂 Archivos a modificar:
   - app/api/inventory_item_api.py
   - app/api/user_api.py
   - app/api/quote_api.py
   - app/api/sales_order_api.py
   - app/api/invoice_api.py
   - ... (todos los endpoints que quieras proteger)

💡 Proceso:
   1. Importar decoradores
   2. Agregar @jwt_required() a endpoints
   3. Agregar @require_permission() según operación
   4. Probar en Swagger

🧪 Testing:
   - Login en /api/auth/login
   - Autorizar en Swagger con token
   - Probar endpoints con diferentes usuarios
   - Verificar 401 sin token, 403 sin permisos

✅ Sistema listo para usar!
""")
