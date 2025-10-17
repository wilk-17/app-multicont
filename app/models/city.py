from app import db

class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True)
    state_id = db.Column(db.BigInteger, db.ForeignKey("state.id"), nullable=False)

    persons = db.relationship("Person", backref="city", lazy=True)
    branches = db.relationship("Branch", backref="city", lazy=True)