from . import db

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)