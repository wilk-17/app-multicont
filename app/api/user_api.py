"""
User API - REST Endpoints
Blueprint de Flask para operaciones REST con usuarios.
"""
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.use_cases.user_handler import UserHandler

# Crear blueprint para la API de usuarios
user_api = Blueprint('user_api', __name__, url_prefix='/api/users')

# Instancia del handler
user_handler = UserHandler()


@user_api.route('/', methods=['GET'])
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
def create_user():
    """
    Crea un nuevo usuario
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
            - role_id
          properties:
            username:
              type: string
              example: "juan"
            password:
              type: string
              example: "secreto123"
            role_id:
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
        data = request.get_json()
        
        # Validar campos requeridos
        if not data or not all(k in data for k in ['username', 'password', 'role_id']):
            return jsonify({
                'success': False,
                'error': 'Faltan campos requeridos: username, password, role_id'
            }), 400
        
        # TODO: Aquí deberías hashear la contraseña antes de guardar
        # from werkzeug.security import generate_password_hash
        # password_hash = generate_password_hash(data['password'])
        
        user = user_handler.create_user(
            username=data['username'],
            password=data['password'],  # En producción usar password_hash
            role_id=data['role_id']
        )
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': user.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Actualiza un usuario
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
              example: "nuevo_username"
            password:
              type: string
              example: "nueva_password"
            role_id:
              type: integer
              example: 2
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
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        user = user_handler.update_user(id, **data)
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': user.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/<int:id>/password', methods=['PUT'])
def update_password(id):
    """
    Actualiza la contraseña de un usuario
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
            - new_password
          properties:
            new_password:
              type: string
              example: "nueva_contraseña123"
    responses:
      200:
        description: Contraseña actualizada exitosamente
      400:
        description: Datos inválidos
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        data = request.get_json()
        
        if not data or 'new_password' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo requerido: new_password'
            }), 400
        
        # TODO: Hashear la nueva contraseña
        user = user_handler.update_password(id, data['new_password'])
        
        return jsonify({
            'success': True,
            'message': 'Contraseña actualizada exitosamente',
            'data': user.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_api.route('/<int:id>', methods=['DELETE'])
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
