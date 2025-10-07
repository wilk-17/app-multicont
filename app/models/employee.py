from . import db

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    person_id = db.Column(db.BigInteger, db.ForeignKey("person.id"), nullable=False)
    branch_id = db.Column(db.BigInteger, db.ForeignKey("branch.id"), nullable=False)

    assignments = db.relationship("Assignment", backref="employee", lazy=True)