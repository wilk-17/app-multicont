"""
EJEMPLO: Cómo proteger endpoints con autenticación JWT
Copia este código en tus APIs para proteger endpoints críticos
"""

# ============================================================================
# EJEMPLO 1: Endpoint protegido (solo requiere estar autenticado)
# ============================================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

example_api = Blueprint('example_api', __name__, url_prefix='/api/example')

@example_api.route('/protected', methods=['GET'])
@jwt_required()  # <-- Solo esta línea para proteger el endpoint
def protected_endpoint():
    """
    Endpoint protegido - Solo usuarios autenticados
    ---
    tags:
      - Example
    security:
      - Bearer: []  # <-- Agregar esto en Swagger para indicar que requiere auth
    responses:
      200:
        description: Acceso permitido
      401:
        description: No autenticado
    """
    user_id = get_jwt_identity()  # Obtener ID del usuario autenticado
    
    return jsonify({
        'success': True,
        'message': f'Hola usuario {user_id}',
        'data': 'Este endpoint está protegido'
    }), 200


# ============================================================================
# EJEMPLO 2: Endpoint que requiere rol específico (ADMIN)
# ============================================================================

from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

@example_api.route('/admin-only', methods=['POST'])
@jwt_required()
@require_role('ADMIN')  # <-- Solo usuarios con rol ADMIN
def admin_only_endpoint():
    """
    Endpoint solo para administradores
    ---
    tags:
      - Example
    security:
      - Bearer: []
    responses:
      200:
        description: Acceso permitido (ADMIN)
      403:
        description: Acceso denegado (no es ADMIN)
    """
    data = request.get_json()
    
    return jsonify({
        'success': True,
        'message': 'Operación de administrador ejecutada',
        'data': data
    }), 200


# ============================================================================
# EJEMPLO 3: Endpoint que acepta múltiples roles (ADMIN o MANAGER)
# ============================================================================

@example_api.route('/manager-access', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')  # <-- Múltiples roles permitidos
def manager_access():
    """
    Endpoint para admins o managers
    ---
    tags:
      - Example
    security:
      - Bearer: []
    """
    from flask_jwt_extended import get_jwt
    
    claims = get_jwt()
    user_role = claims.get('role')
    
    return jsonify({
        'success': True,
        'message': f'Acceso permitido para {user_role}',
        'your_role': user_role
    }), 200


# ============================================================================
# EJEMPLO 4: Endpoint que requiere permisos específicos
# ============================================================================

from app.utils.decorators import require_permission

@example_api.route('/write-quote', methods=['POST'])
@jwt_required()
@require_permission('WRITE_QUOTES')  # <-- Requiere permiso específico
def write_quote():
    """
    Endpoint que requiere permiso WRITE_QUOTES
    ---
    tags:
      - Example
    security:
      - Bearer: []
    """
    data = request.get_json()
    
    return jsonify({
        'success': True,
        'message': 'Cotización creada',
        'quote': data
    }), 201


# ============================================================================
# EJEMPLO 5: Obtener información completa del usuario autenticado
# ============================================================================

@example_api.route('/my-info', methods=['GET'])
@jwt_required()
def my_info():
    """
    Obtener información completa del usuario actual
    ---
    tags:
      - Example
    security:
      - Bearer: []
    """
    from flask_jwt_extended import get_jwt
    from app.entities.user import User
    
    user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Obtener usuario completo de la BD
    user = User.query.get(user_id)
    
    return jsonify({
        'success': True,
        'user': {
            **user.to_dict(),
            'role': claims.get('role'),
            'permissions': claims.get('permissions', [])
        }
    }), 200


# ============================================================================
# EJEMPLO 6: Endpoint público + privado (comportamiento dual)
# ============================================================================

from flask_jwt_extended import jwt_required, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

@example_api.route('/dual', methods=['GET'])
def dual_endpoint():
    """
    Endpoint que funciona sin auth pero da más info si está autenticado
    ---
    tags:
      - Example
    parameters:
      - name: Authorization
        in: header
        type: string
        required: false
        description: Token JWT opcional
    """
    try:
        verify_jwt_in_request()
        # Usuario autenticado
        user_id = get_jwt_identity()
        return jsonify({
            'success': True,
            'message': f'Hola usuario autenticado {user_id}',
            'premium_data': 'Datos exclusivos para usuarios autenticados'
        }), 200
    except NoAuthorizationError:
        # Usuario no autenticado (también permitido)
        return jsonify({
            'success': True,
            'message': 'Hola usuario anónimo',
            'public_data': 'Datos públicos'
        }), 200


# ============================================================================
# EJEMPLO 7: Proteger CREATE pero permitir READ público
# ============================================================================

@example_api.route('/products', methods=['GET'])
def list_products():
    """
    Listar productos - Público (sin auth)
    """
    return jsonify({
        'success': True,
        'products': ['Producto 1', 'Producto 2', 'Producto 3']
    }), 200


@example_api.route('/products', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create_product():
    """
    Crear producto - Solo ADMIN o MANAGER
    """
    data = request.get_json()
    
    return jsonify({
        'success': True,
        'message': 'Producto creado',
        'product': data
    }), 201


# ============================================================================
# EJEMPLO 8: Verificar si el usuario es dueño del recurso
# ============================================================================

@example_api.route('/my-orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_my_order(order_id):
    """
    Obtener orden - Solo si pertenece al usuario actual o es ADMIN
    """
    from flask_jwt_extended import get_jwt
    from app.utils.decorators import is_admin
    
    user_id = int(get_jwt_identity())
    
    # Simular obtención de orden de la BD
    order = {
        'id': order_id,
        'user_id': 1,  # Usuario dueño de la orden
        'total': 50000
    }
    
    # Verificar que el usuario sea el dueño o sea admin
    if order['user_id'] != user_id and not is_admin():
        return jsonify({
            'success': False,
            'error': 'No tienes permiso para ver esta orden'
        }), 403
    
    return jsonify({
        'success': True,
        'order': order
    }), 200


# ============================================================================
# EJEMPLO 9: Endpoint con validación personalizada
# ============================================================================

@example_api.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Actualizar perfil - Solo el propio usuario o ADMIN
    """
    from flask_jwt_extended import get_jwt
    
    data = request.get_json()
    target_user_id = data.get('user_id')
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get('role')
    
    # Validación: Solo puede editar su propio perfil o ser ADMIN
    if target_user_id != current_user_id and current_role != 'ADMIN':
        return jsonify({
            'success': False,
            'error': 'Solo puedes editar tu propio perfil'
        }), 403
    
    # Procesar actualización...
    
    return jsonify({
        'success': True,
        'message': 'Perfil actualizado'
    }), 200


# ============================================================================
# EJEMPLO 10: Manejo de errores personalizados
# ============================================================================

@example_api.route('/critical-operation', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def critical_operation():
    """
    Operación crítica - Solo ADMIN con validación adicional
    """
    from flask_jwt_extended import get_jwt
    
    claims = get_jwt()
    permissions = claims.get('permissions', [])
    
    # Validación adicional: requiere permiso específico
    if 'ADMIN_ALL' not in permissions:
        return jsonify({
            'success': False,
            'error': 'Requiere permiso ADMIN_ALL para esta operación',
            'your_permissions': permissions
        }), 403
    
    # Ejecutar operación crítica...
    
    return jsonify({
        'success': True,
        'message': 'Operación crítica ejecutada exitosamente'
    }), 200


# ============================================================================
# RESUMEN DE USO
# ============================================================================

"""
DECORADORES DISPONIBLES:

1. @jwt_required()
   - Requiere token JWT válido
   - Cualquier usuario autenticado puede acceder

2. @jwt_required(optional=True)
   - Token opcional (endpoint funciona con o sin auth)
   - Usar verify_jwt_in_request() para detectar si hay token

3. @jwt_required(refresh=True)
   - Solo para refresh tokens (endpoint /auth/refresh)

4. @require_role('ADMIN')
   - Requiere rol específico
   - Múltiples roles: @require_role('ADMIN', 'MANAGER')

5. @require_permission('WRITE_QUOTES')
   - Requiere permiso específico
   - Múltiples permisos: @require_permission('PERM1', 'PERM2')

FUNCIONES ÚTILES:

- get_jwt_identity() → ID del usuario (string)
- get_jwt() → Claims completos del token (dict)
- is_admin() → Verifica si el usuario es admin (bool)
- get_current_user() → Objeto User completo

HEADERS EN REQUESTS:

Authorization: Bearer {access_token}

RESPUESTAS DE ERROR:

401 Unauthorized → Token inválido, expirado o no proporcionado
403 Forbidden → Token válido pero sin permisos suficientes

SWAGGER DOCUMENTATION:

Agregar en el docstring:
---
security:
  - Bearer: []
---
"""
