from . import db

class Branch(db.Model):
    __tablename__ = "branch"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.BigInteger, db.ForeignKey("organization.id"), nullable=False)
    city_id = db.Column(db.BigInteger, db.ForeignKey("city.id"), nullable=False)

    employees = db.relationship("Employee", backref="branch", lazy=True)