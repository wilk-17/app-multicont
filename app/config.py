import os
from dotenv import load_dotenv

# Carga variables desde .env si existe
load_dotenv()

class BaseConfig:
    """Configuración base para todos los ambientes."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    
    # Secret key para sesiones y CSRF
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError(
            "SECRET_KEY no configurada. "
            "Agregar SECRET_KEY=<tu-secret-key> en archivo .env"
        )


class DevelopmentConfig(BaseConfig):
    """Configuración para desarrollo local."""
    DEBUG = True
    TESTING = False
    
    # Database URL obligatoria
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError(
            "DATABASE_URL no configurada. "
            "Agregar DATABASE_URL=postgresql+psycopg2://user:password@host:5432/dbname en .env"
        )
    
    # Habilitar SQL logging en desarrollo
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"


class ProductionConfig(BaseConfig):
    """Configuración para producción."""
    DEBUG = False
    TESTING = False
    
    # Database URL obligatoria
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL no configurada en producción")
    
    # Deshabilitar SQL logging en producción
    SQLALCHEMY_ECHO = False


class TestingConfig(BaseConfig):
    """Configuración para tests automatizados."""
    DEBUG = True
    TESTING = True
    
    # Usar SQLite en memoria para tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    
    # Deshabilitar protección CSRF en tests
    WTF_CSRF_ENABLED = False