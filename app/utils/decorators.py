"""
Authentication Decorators - Decoradores para proteger endpoints
Funciones decoradoras para autorización basada en roles y permisos
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from app.entities.user import User
from app.entities.role import Role


def jwt_required_custom(fn):
    """
    Decorador personalizado que requiere JWT válido
    Similar a @jwt_required() pero con manejo de errores personalizado
    
    Usage:
        @app.route('/protected')
        @jwt_required_custom
        def protected_route():
            return {'message': 'Acceso permitido'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Token inválido o expirado',
                'message': str(e)
            }), 401
    return wrapper


def require_role(*allowed_roles):
    """
    Decorador que verifica que el usuario tenga uno de los roles permitidos
    
    Args:
        *allowed_roles: Lista de roles permitidos ('ADMIN', 'MANAGER', 'SALES')
        
    Usage:
        @app.route('/admin-only')
        @jwt_required()
        @require_role('ADMIN')
        def admin_route():
            return {'message': 'Solo admins'}
            
        @app.route('/admin-or-manager')
        @jwt_required()
        @require_role('ADMIN', 'MANAGER')
        def manager_route():
            return {'message': 'Admins o Managers'}
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_role = claims.get('role')
                
                if user_role not in allowed_roles:
                    return jsonify({
                        'success': False,
                        'error': f'Acceso denegado. Requiere rol: {", ".join(allowed_roles)}',
                        'user_role': user_role
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': 'Error de autorización',
                    'message': str(e)
                }), 401
        return wrapper
    return decorator


def require_permission(*required_permissions):
    """
    Decorador que verifica que el usuario tenga los permisos especificados
    
    Args:
        *required_permissions: Lista de permisos requeridos
        
    Usage:
        @app.route('/write-quotes')
        @jwt_required()
        @require_permission('WRITE_QUOTES')
        def write_quote():
            return {'message': 'Permiso para escribir cotizaciones'}
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_permissions = claims.get('permissions', [])
                
                # Verificar si el usuario tiene todos los permisos requeridos
                missing_permissions = [p for p in required_permissions if p not in user_permissions]
                
                if missing_permissions:
                    return jsonify({
                        'success': False,
                        'error': f'Permisos insuficientes. Requiere: {", ".join(missing_permissions)}',
                        'user_permissions': user_permissions
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': 'Error de autorización',
                    'message': str(e)
                }), 401
        return wrapper
    return decorator


def get_current_user():
    """
    Obtiene el usuario actual desde el JWT
    Debe llamarse dentro de un contexto con JWT válido
    
    Returns:
        User: Objeto User del usuario autenticado
        
    Usage:
        @app.route('/me')
        @jwt_required()
        def get_me():
            user = get_current_user()
            return user.to_dict()
    """
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def is_admin():
    """
    Verifica si el usuario actual es administrador
    
    Returns:
        bool: True si el usuario es admin
        
    Usage:
        @app.route('/check-admin')
        @jwt_required()
        def check():
            if is_admin():
                return {'message': 'Eres admin'}
            return {'message': 'No eres admin'}, 403
    """
    try:
        claims = get_jwt()
        return claims.get('role') == 'ADMIN'
    except:
        return False
