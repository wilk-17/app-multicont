import os
from dotenv import load_dotenv

# Carga variables desde .env si existe
load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")  # Útil para sesiones, JWT, etc.

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:123456@localhost:5432/Prueba1"
    )
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True