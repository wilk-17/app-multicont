from . import db


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)