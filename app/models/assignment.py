from app import db

class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.BigInteger, db.ForeignKey("employee.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)