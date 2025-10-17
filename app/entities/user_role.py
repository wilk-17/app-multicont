"""UserRole Entity"""
from datetime import datetime
from app import db

class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
        self.creation_date = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'role_id': str(self.role_id),
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }
