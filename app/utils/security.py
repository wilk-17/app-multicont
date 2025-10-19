"""
Security Utilities - Hash de passwords y JWT
Funciones para seguridad de autenticación
"""
import bcrypt
from datetime import timedelta


def hash_password(password: str) -> str:
    """
    Genera hash de una contraseña usando bcrypt
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
        
    Example:
        >>> hashed = hash_password("mi_password_123")
        >>> print(hashed)
        $2b$12$...
    """
    # Convertir password a bytes
    password_bytes = password.encode('utf-8')
    # Generar salt y hashear (12 rondas por defecto)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Retornar como string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash almacenado en la BD
        
    Returns:
        bool: True si la contraseña es correcta
        
    Example:
        >>> hashed = hash_password("mi_password_123")
        >>> verify_password("mi_password_123", hashed)
        True
        >>> verify_password("password_incorrecta", hashed)
        False
    """
    try:
        # Convertir a bytes
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        # Verificar
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


# Configuración de JWT
JWT_SECRET_KEY = "tu-clave-secreta-muy-segura-cambiar-en-produccion"  # TODO: Mover a .env
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expira en 24 horas
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expira en 30 días


def get_jwt_config():
    """
    Obtiene la configuración de JWT para Flask
    
    Returns:
        dict: Configuración de JWT
    """
    return {
        'JWT_SECRET_KEY': JWT_SECRET_KEY,
        'JWT_ACCESS_TOKEN_EXPIRES': JWT_ACCESS_TOKEN_EXPIRES,
        'JWT_REFRESH_TOKEN_EXPIRES': JWT_REFRESH_TOKEN_EXPIRES,
        'JWT_TOKEN_LOCATION': ['headers'],
        'JWT_HEADER_NAME': 'Authorization',
        'JWT_HEADER_TYPE': 'Bearer'
    }
