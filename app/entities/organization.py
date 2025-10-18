"""Organization Entity"""
from datetime import datetime
from app import db

class Organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    historical_name = db.Column(db.String(200), nullable=False)
    current_name = db.Column(db.String(200), nullable=False)
    
    def __init__(self, historical_name, current_name):
        self.historical_name = historical_name
        self.current_name = current_name
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'historical_name': self.historical_name,
            'current_name': self.current_name
        }
