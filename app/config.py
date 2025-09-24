import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:123456@localhost:5432/Prueba1"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
