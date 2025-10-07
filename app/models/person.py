from . import db

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    city_id = db.Column(db.BigInteger, db.ForeignKey("city.id"))

    employees = db.relationship("Employee", backref="person", lazy=True)