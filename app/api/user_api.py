"""
User API - REST Endpoints con validación Marshmallow
Blueprint de Flask para operaciones REST con usuarios.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from app.use_cases.user_handler import UserHandler
from app.schemas import (
    user_create_schema,
    user_update_schema,
    password_change_schema,
    user_response_schema,
    users_response_schema
)
from app.utils.decorators import require_role
from app.utils.security import hash_password

# Crear blueprint para la API de usuarios
user_api = Blueprint('user_api', __name__, url_prefix='/api/users')

# Instancia del handler
user_handler = UserHandler()


@user_api.route('/', methods=['GET'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def get_all_users():
    """
    Consulta todos los usuarios con paginación
    ---
    tags:
      - Usuarios
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
        description: Usuarios por página
    responses:
      200:
        description: Lista de usuarios con información de paginación
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                total:
                  type: integer
                page:
                  type: integer
                per_page:
                  type: integer
                total_pages:
                  type: integer
      500:
        description: Error del servidor
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = user_handler.list_users(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in result['users']],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/role/<int:role_id>', methods=['GET'])
def get_users_by_role(role_id):
    """
    Consulta usuarios filtrados por rol
    ---
    tags:
      - Usuarios
    parameters:
      - name: role_id
        in: path
        type: integer
        required: true
        description: ID del rol
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
        description: Lista de usuarios del rol especificado
      500:
        description: Error del servidor
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = user_handler.get_users_by_role(role_id=role_id, page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in result['users']],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/username/<username>', methods=['GET'])
def get_user_by_username(username):
    """
    Consulta un usuario por username
    ---
    tags:
      - Usuarios
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: Nombre de usuario a buscar
    responses:
      200:
        description: Usuario encontrado
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        user = user_handler.get_user_by_username(username)
        if user:
            return jsonify({
                'success': True,
                'data': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Usuario con username "{username}" no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    """
    Consulta un usuario por ID
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del usuario a buscar
    responses:
      200:
        description: Usuario encontrado
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        user = user_handler.get_user(id)
        if user:
            return jsonify({
                'success': True,
                'data': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Usuario con ID "{id}" no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN')
def create_user():
    """
    Crea un nuevo usuario con validación automática
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
            - email
          properties:
            username:
              type: string
              minLength: 4
              maxLength: 50
              example: "juan_perez"
            email:
              type: string
              format: email
              example: "juan@example.com"
            password:
              type: string
              minLength: 8
              example: "Password123!"
              description: Mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número, 1 especial
            full_name:
              type: string
              example: "Juan Pérez"
            phone:
              type: string
              example: "+34612345678"
            employee_id:
              type: integer
              example: 1
    responses:
      201:
        description: Usuario creado exitosamente
      400:
        description: Datos inválidos o usuario ya existe
      500:
        description: Error del servidor
    """
    try:
        # Validar datos con Marshmallow
        validated_data = user_create_schema.load(request.get_json())
        
        # Hashear la contraseña antes de guardar
        validated_data['password'] = hash_password(validated_data['password'])
        
        # Crear usuario
        user = user_handler.create_user(**validated_data)
        
        # Serializar respuesta
        result = user_response_schema.dump(user)
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': result
        }), 201
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@user_api.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_role('ADMIN')
def update_user(id):
    """
    Actualiza un usuario con validación automática
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              minLength: 4
              maxLength: 50
            email:
              type: string
              format: email
            full_name:
              type: string
            phone:
              type: string
            status:
              type: string
              enum: [active, inactive, suspended]
    responses:
      200:
        description: Usuario actualizado exitosamente
      400:
        description: Datos inválidos
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        # Validar datos con Marshmallow
        validated_data = user_update_schema.load(request.get_json())
        
        if not validated_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        # Actualizar usuario
        user = user_handler.update_user(id, **validated_data)
        
        # Serializar respuesta
        result = user_response_schema.dump(user)
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': result
        }), 200
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@user_api.route('/<int:id>/password', methods=['PUT'])
@jwt_required()
@require_role('ADMIN')
def update_password(id):
    """
    Actualiza la contraseña de un usuario con validación
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - current_password
            - new_password
            - confirm_password
          properties:
            current_password:
              type: string
              example: "OldPassword123!"
            new_password:
              type: string
              minLength: 8
              example: "NewPassword123!"
              description: Mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número, 1 especial
            confirm_password:
              type: string
              example: "NewPassword123!"
    responses:
      200:
        description: Contraseña actualizada exitosamente
      400:
        description: Datos inválidos o contraseñas no coinciden
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        # Validar datos con Marshmallow
        validated_data = password_change_schema.load(request.get_json())
        
        # Verificar que las contraseñas coinciden
        if validated_data['new_password'] != validated_data['confirm_password']:
            return jsonify({
                'success': False,
                'error': 'Las contraseñas no coinciden'
            }), 400
        
        # Hashear la nueva contraseña
        password_hashed = hash_password(validated_data['new_password'])
        user = user_handler.update_password(id, password_hashed)
        
        # Serializar respuesta
        result = user_response_schema.dump(user)
        
        return jsonify({
            'success': True,
            'message': 'Contraseña actualizada exitosamente',
            'data': result
        }), 200
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@user_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete_user(id):
    """
    Elimina un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Usuario eliminado exitosamente
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        deleted = user_handler.delete_user(id)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': f'Usuario con ID "{id}" eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Usuario con ID "{id}" no encontrado'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/count', methods=['GET'])
def count_users():
    """
    Cuenta total de usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Total de usuarios
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                total:
                  type: integer
      500:
        description: Error del servidor
    """
    try:
        total = user_handler.count_users()
        return jsonify({
            'success': True,
            'data': {
                'total': total
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
