from . import db

class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), nullable=False)