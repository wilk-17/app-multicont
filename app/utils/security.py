"""
Security Utilities - Hash de passwords y JWT
Funciones para seguridad de autenticación
"""
import os
import bcrypt
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


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


# Configuración de JWT desde variables de entorno
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY no configurada. "
        "Agregar JWT_SECRET_KEY=<tu-secret-key> en archivo .env"
    )

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_HOURS', '24')))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_DAYS', '30')))


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
