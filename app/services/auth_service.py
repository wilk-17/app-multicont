"""
Authentication Service
Maneja la lógica de autenticación JWT y gestión de tokens
"""
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.entities.user import User
from app.entities.role import Role
from app import db


class AuthService:
    """Servicio de autenticación con JWT."""
    
    # Tiempo de expiración de tokens
    ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea una contraseña usando werkzeug.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            str: Hash de la contraseña
        """
        return generate_password_hash(password, method='pbkdf2:sha256')
    
    @staticmethod
    def verify_password(password_hash: str, password: str) -> bool:
        """
        Verifica una contraseña contra su hash.
        
        Args:
            password_hash: Hash almacenado
            password: Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def authenticate(username: str, password: str) -> dict:
        """
        Autentica un usuario y genera tokens JWT.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            dict: Información del usuario y tokens o None si falla
            
        Raises:
            ValueError: Si las credenciales son inválidas
        """
        # Buscar usuario
        user = User.query.filter_by(username=username).first()
        
        if not user:
            raise ValueError("Usuario o contraseña incorrectos")
        
        # Verificar contraseña
        if not AuthService.verify_password(user.password, password):
            raise ValueError("Usuario o contraseña incorrectos")
        
        # Obtener rol
        role = Role.query.get(user.role_id)
        if not role:
            raise ValueError("Rol de usuario no encontrado")
        
        # Crear claims adicionales para el token
        additional_claims = {
            'role': role.name,
            'user_id': user.id,
            'username': user.username
        }
        
        # Generar tokens
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims,
            expires_delta=AuthService.ACCESS_TOKEN_EXPIRES
        )
        
        refresh_token = create_refresh_token(
            identity=user.id,
            additional_claims=additional_claims,
            expires_delta=AuthService.REFRESH_TOKEN_EXPIRES
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'role': role.name
            }
        }
    
    @staticmethod
    def refresh_access_token() -> dict:
        """
        Genera un nuevo access token usando el refresh token.
        
        Returns:
            dict: Nuevo access token
        """
        # Obtener identidad del token actual
        current_user_id = get_jwt_identity()
        jwt_data = get_jwt()
        
        # Crear nuevo access token con los mismos claims
        additional_claims = {
            'role': jwt_data.get('role'),
            'user_id': jwt_data.get('user_id'),
            'username': jwt_data.get('username')
        }
        
        access_token = create_access_token(
            identity=current_user_id,
            additional_claims=additional_claims,
            expires_delta=AuthService.ACCESS_TOKEN_EXPIRES
        )
        
        return {'access_token': access_token}
    
    @staticmethod
    def get_current_user() -> dict:
        """
        Obtiene información del usuario actual desde el token JWT.
        
        Returns:
            dict: Información del usuario actual
        """
        jwt_data = get_jwt()
        user_id = get_jwt_identity()
        
        # Buscar usuario completo
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        role = Role.query.get(user.role_id)
        
        return {
            'id': str(user.id),
            'username': user.username,
            'role': role.name if role else None,
            'role_id': str(user.role_id)
        }
    
    @staticmethod
    def get_user_role() -> str:
        """
        Obtiene el rol del usuario actual desde el token JWT.
        
        Returns:
            str: Nombre del rol
        """
        jwt_data = get_jwt()
        return jwt_data.get('role', None)
    
    @staticmethod
    def get_user_id() -> int:
        """
        Obtiene el ID del usuario actual desde el token JWT.
        
        Returns:
            int: ID del usuario
        """
        return int(get_jwt_identity())
