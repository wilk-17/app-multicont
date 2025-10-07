from app import db

class Organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    historical_name = db.Column(db.String(200), nullable=False)
    current_name = db.Column(db.String(200), nullable=False)

    branches = db.relationship("Branch", backref="organization", lazy=True)