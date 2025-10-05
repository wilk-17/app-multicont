from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from .config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="API Multicont",
    version="1.0",
    description="Documentación Swagger para endpoints RESTful"
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Importar modelos para que Migrate los detecte
    from . import models

    # Registrar namespace RESTX
    from .routes import user_ns
    api.add_namespace(user_ns)

    return app
