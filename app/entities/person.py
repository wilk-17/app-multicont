"""Person Entity"""
from datetime import datetime
from app import db

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    city_id = db.Column(db.BigInteger, db.ForeignKey("city.id"))
    status = db.Column(db.String(20), nullable=False, default='active')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    employees = db.relationship("Employee", backref="person", lazy=True)
    
    def __init__(self, first_name, last_name, dni=None, address=None, phone=None, city_id=None, status='active'):
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.address = address
        self.phone = phone
        self.city_id = city_id
        self.status = status
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'dni': self.dni,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'address': self.address,
            'phone': self.phone,
            'city_id': str(self.city_id) if self.city_id else None,
            'status': self.status
        }
