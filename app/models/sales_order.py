from app import db

class SalesOrder(db.Model):
    __tablename__ = "sales_order"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False)

    invoices = db.relationship("Invoice", backref="sales_order", lazy=True)
    sales_order_items = db.relationship("SalesOrderItem", backref="sales_order", lazy=True)