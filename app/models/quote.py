from app import db

class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False)

    quotation_lines = db.relationship("QuotationLine", backref="quote", lazy=True)
    sales_orders = db.relationship("SalesOrder", backref="quote", lazy=True)