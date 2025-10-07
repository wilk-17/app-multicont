from . import db

class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    cities = db.relationship("City", backref="state", lazy=True)