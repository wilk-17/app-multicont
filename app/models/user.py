from . import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), nullable=False)

    roles = db.relationship("UserRole", backref="user", lazy=True)