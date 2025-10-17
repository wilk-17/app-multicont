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
      - name: status
        in: query
        type: string
        enum: [active, inactive, suspended]
        description: Filtrar por estado
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
        status = request.args.get('status', None, type=str)
        
        result = user_handler.list_users(page=page, per_page=per_page, status=status)
        
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


@user_api.route('/active', methods=['GET'])
def get_active_users():
    """
    Consulta todos los usuarios activos con paginación
    ---
    tags:
      - Usuarios
    parameters:
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
        description: Lista de usuarios activos
      500:
        description: Error del servidor
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = user_handler.list_active_users(page=page, per_page=per_page)
        
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
            status:
              type: string
              enum: [active, inactive, suspended]
              default: active
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
            role_id=data['role_id'],
            status=data.get('status', 'active')
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


@user_api.route('/<int:id>/activate', methods=['PUT'])
def activate_user(id):
    """
    Activa un usuario
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
        description: Usuario activado exitosamente
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        user = user_handler.activate_user(id)
        return jsonify({
            'success': True,
            'message': f'Usuario "{user.username}" activado exitosamente',
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


@user_api.route('/<int:id>/inactivate', methods=['PUT'])
def inactivate_user(id):
    """
    Inactiva un usuario
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
        description: Usuario inactivado exitosamente
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        user = user_handler.inactivate_user(id)
        return jsonify({
            'success': True,
            'message': f'Usuario "{user.username}" inactivado exitosamente',
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


@user_api.route('/<int:id>/suspend', methods=['PUT'])
def suspend_user(id):
    """
    Suspende un usuario
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
        description: Usuario suspendido exitosamente
      404:
        description: Usuario no encontrado
      500:
        description: Error del servidor
    """
    try:
        user = user_handler.suspend_user(id)
        return jsonify({
            'success': True,
            'message': f'Usuario "{user.username}" suspendido exitosamente',
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


@user_api.route('/statistics', methods=['GET'])
def get_user_statistics():
    """
    Obtiene estadísticas de usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Estadísticas de usuarios por estado
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                active:
                  type: integer
                inactive:
                  type: integer
                suspended:
                  type: integer
                total:
                  type: integer
      500:
        description: Error del servidor
    """
    try:
        stats = user_handler.get_user_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
