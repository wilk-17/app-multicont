"""
Authentication API - Endpoints de autenticación
Login, Logout, Refresh Token, User Info
"""
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from app.use_cases.user_handler import UserHandler
from app.utils.security import verify_password
from app.entities.role import Role
from app.entities.permission import Permission
from app.api.helpers import (
    success_response,
    error_response,
    validate_required_fields
)
from app import cache

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')
user_handler = UserHandler()


@auth_api.route('/login', methods=['POST'])
def login():
    """
    Login de usuario y generación de tokens JWT
    ---
    tags:
      - Autenticación
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "ana"
            password:
              type: string
              example: "ana123"
    responses:
      200:
        description: Login exitoso
        schema:
          type: object
          properties:
            success:
              type: boolean
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              type: object
              properties:
                id:
                  type: string
                username:
                  type: string
                role:
                  type: string
                role_id:
                  type: string
      401:
        description: Credenciales inválidas
    """
    data = request.get_json()
    
    # Validar campos requeridos
    is_valid, missing = validate_required_fields(data, ['username', 'password'])
    if not is_valid:
        return error_response(f'Campos requeridos: {", ".join(missing)}', 400)
    
    username = data['username']
    password = data['password']
    
    try:
        # Buscar usuario por username
        user = user_handler.get_user_by_username(username)
        
        if not user:
            return error_response('Usuario o contraseña incorrectos', 401)
        
        # Verificar contraseña
        if not verify_password(password, user.password):
            return error_response('Usuario o contraseña incorrectos', 401)
        
        # Obtener rol del usuario
        role = Role.query.get(user.role_id)
        role_name = role.name if role else 'UNKNOWN'
        
        # Obtener permisos del rol (simplificado - expandir según tu modelo)
        # En una implementación completa, consultar la tabla de permisos
        permissions = []
        if role_name == 'ADMIN':
            permissions = ['ADMIN_ALL', 'READ_REPORTS', 'WRITE_QUOTES', 'APPROVE_ORDERS']
        elif role_name == 'MANAGER':
            permissions = ['READ_REPORTS', 'WRITE_QUOTES', 'APPROVE_ORDERS']
        elif role_name == 'SALES':
            permissions = ['READ_REPORTS', 'WRITE_QUOTES']
        
        # Claims adicionales para el JWT
        additional_claims = {
            'role': role_name,
            'role_id': str(user.role_id),
            'permissions': permissions
        }
        
        # Crear tokens
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        
        # Invalidar caché de usuarios al hacer login
        cache.delete_memoized(user_handler.get_user)
        
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'role': role_name,
                'role_id': str(user.role_id)
            }
        }
        
        return success_response(response_data, f'Bienvenido, {username}!', 200)
        
    except Exception as e:
        return error_response(f'Error en el login: {str(e)}', 500)


@auth_api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Renovar access token usando refresh token
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    responses:
      200:
        description: Token renovado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            access_token:
              type: string
      401:
        description: Token inválido o expirado
    """
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Mantener los claims adicionales
        additional_claims = {
            'role': claims.get('role'),
            'role_id': claims.get('role_id'),
            'permissions': claims.get('permissions', [])
        }
        
        # Crear nuevo access token
        new_access_token = create_access_token(
            identity=current_user_id,
            additional_claims=additional_claims
        )
        
        response_data = {'access_token': new_access_token}
        return success_response(response_data, 'Token renovado exitosamente', 200)
        
    except Exception as e:
        return error_response(f'Error al renovar token: {str(e)}', 500)


@auth_api.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """
    Obtener información del usuario autenticado
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    responses:
      200:
        description: Información del usuario
        schema:
          type: object
          properties:
            success:
              type: boolean
            user:
              type: object
      401:
        description: No autenticado
    """
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Obtener usuario completo de la BD
        user = user_handler.get_user(int(current_user_id))
        
        if not user:
            return error_response('Usuario no encontrado', 404)
        
        user_data = {
            **user.to_dict(),
            'role': claims.get('role'),
            'permissions': claims.get('permissions', [])
        }
        
        return success_response(user_data, 'Información del usuario obtenida', 200)
        
    except Exception as e:
        return error_response(f'Error al obtener información: {str(e)}', 500)


@auth_api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout del usuario (cliente debe eliminar token)
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    responses:
      200:
        description: Logout exitoso
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
    """
    # En una implementación más completa, agregar el token a una blacklist
    # Por ahora, el logout es manejado en el cliente eliminando el token
    
    return success_response(None, 'Sesión cerrada exitosamente', 200)


@auth_api.route('/validate', methods=['GET'])
@jwt_required()
def validate_token():
    """
    Validar si el token actual es válido
    ---
    tags:
      - Autenticación
    security:
      - Bearer: []
    responses:
      200:
        description: Token válido
        schema:
          type: object
          properties:
            success:
              type: boolean
            valid:
              type: boolean
            user_id:
              type: string
            role:
              type: string
      401:
        description: Token inválido
    """
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        validation_data = {
            'valid': True,
            'user_id': current_user_id,
            'role': claims.get('role'),
            'permissions': claims.get('permissions', [])
        }
        
        return success_response(validation_data, 'Token válido', 200)
        
    except Exception as e:
        return error_response(f'Token inválido: {str(e)}', 401)
