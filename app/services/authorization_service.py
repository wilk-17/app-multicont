"""
Authorization Service
Maneja permisos y autorización basada en roles (RBAC)
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from app.entities.role import Role
from app.entities.permission import Permission
from app import db


# Matriz de permisos por rol
ROLE_PERMISSIONS = {
    'ADMIN': [
        # Inventario
        'inventory:read', 'inventory:write', 'inventory:delete', 'inventory:manage',
        # Ventas
        'sales:read', 'sales:create_quote', 'sales:approve_quote',
        'sales:create_order', 'sales:create_invoice', 'sales:delete',
        # Reportes
        'reports:read', 'reports:export', 'dashboard:view',
        # Usuarios
        'users:read', 'users:write', 'users:delete',
        # Admin
        'admin:all'
    ],
    'MANAGER': [
        # Inventario
        'inventory:read', 'inventory:write',
        # Ventas
        'sales:read', 'sales:create_quote', 'sales:approve_quote',
        'sales:create_order', 'sales:create_invoice', 'sales:delete',
        # Reportes
        'reports:read', 'reports:export', 'dashboard:view',
        # Usuarios
        'users:read'
    ],
    'SALES': [
        # Inventario
        'inventory:read',
        # Ventas
        'sales:read', 'sales:create_quote',
        # Reportes
        'dashboard:view'
    ]
}


class AuthorizationService:
    """Servicio de autorización basado en roles y permisos."""
    
    @staticmethod
    def get_user_permissions(role_name: str) -> list:
        """
        Obtiene los permisos de un rol específico.
        
        Args:
            role_name: Nombre del rol (ADMIN, MANAGER, SALES)
            
        Returns:
            list: Lista de permisos del rol
        """
        return ROLE_PERMISSIONS.get(role_name, [])
    
    @staticmethod
    def has_permission(role_name: str, permission: str) -> bool:
        """
        Verifica si un rol tiene un permiso específico.
        
        Args:
            role_name: Nombre del rol
            permission: Permiso a verificar (ej: 'inventory:write')
            
        Returns:
            bool: True si el rol tiene el permiso
        """
        user_permissions = AuthorizationService.get_user_permissions(role_name)
        return permission in user_permissions or 'admin:all' in user_permissions
    
    @staticmethod
    def has_any_permission(role_name: str, permissions: list) -> bool:
        """
        Verifica si un rol tiene al menos uno de los permisos listados.
        
        Args:
            role_name: Nombre del rol
            permissions: Lista de permisos a verificar
            
        Returns:
            bool: True si tiene al menos un permiso
        """
        user_permissions = AuthorizationService.get_user_permissions(role_name)
        return any(perm in user_permissions for perm in permissions) or 'admin:all' in user_permissions
    
    @staticmethod
    def has_all_permissions(role_name: str, permissions: list) -> bool:
        """
        Verifica si un rol tiene todos los permisos listados.
        
        Args:
            role_name: Nombre del rol
            permissions: Lista de permisos a verificar
            
        Returns:
            bool: True si tiene todos los permisos
        """
        user_permissions = AuthorizationService.get_user_permissions(role_name)
        if 'admin:all' in user_permissions:
            return True
        return all(perm in user_permissions for perm in permissions)


# ============================================================
# DECORADORES DE AUTORIZACIÓN
# ============================================================

def require_permission(permission: str):
    """
    Decorador que requiere un permiso específico.
    
    Args:
        permission: Permiso requerido (ej: 'inventory:write')
        
    Usage:
        @require_permission('inventory:write')
        def create_product():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt_data = get_jwt()
            role = jwt_data.get('role')
            
            if not role:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo determinar el rol del usuario'
                }), 403
            
            if not AuthorizationService.has_permission(role, permission):
                return jsonify({
                    'success': False,
                    'error': f'No tienes permiso para realizar esta acción. Permiso requerido: {permission}',
                    'required_permission': permission,
                    'your_role': role
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permissions: list):
    """
    Decorador que requiere al menos uno de los permisos listados.
    
    Args:
        permissions: Lista de permisos (el usuario debe tener al menos uno)
        
    Usage:
        @require_any_permission(['sales:read', 'sales:create_quote'])
        def view_sales():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt_data = get_jwt()
            role = jwt_data.get('role')
            
            if not role:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo determinar el rol del usuario'
                }), 403
            
            if not AuthorizationService.has_any_permission(role, permissions):
                return jsonify({
                    'success': False,
                    'error': f'No tienes permiso para realizar esta acción. Requieres al menos uno de estos permisos: {", ".join(permissions)}',
                    'required_permissions': permissions,
                    'your_role': role
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_role(roles):
    """
    Decorador que requiere un rol específico o lista de roles.
    
    Args:
        roles: Rol requerido (str) o lista de roles permitidos (list)
        
    Usage:
        @require_role('ADMIN')
        def admin_only():
            ...
            
        @require_role(['ADMIN', 'MANAGER'])
        def manager_or_admin():
            ...
    """
    # Convertir a lista si es string
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt_data = get_jwt()
            user_role = jwt_data.get('role')
            
            if not user_role:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo determinar el rol del usuario'
                }), 403
            
            if user_role not in roles:
                return jsonify({
                    'success': False,
                    'error': f'Acceso denegado. Roles permitidos: {", ".join(roles)}',
                    'required_roles': roles,
                    'your_role': user_role
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required():
    """
    Decorador que requiere rol ADMIN.
    
    Usage:
        @admin_required()
        def delete_user():
            ...
    """
    return require_role('ADMIN')


def manager_or_admin():
    """
    Decorador que requiere rol MANAGER o ADMIN.
    
    Usage:
        @manager_or_admin()
        def approve_quote():
            ...
    """
    return require_role(['ADMIN', 'MANAGER'])
