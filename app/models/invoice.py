from app import db

class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sales_order_id = db.Column(db.BigInteger, db.ForeignKey("sales_order.id"), nullable=False)
    quotation_line_id = db.Column(db.BigInteger, db.ForeignKey("quotation_line.id"))
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(12, 2), nullable=False)

    invoice_items = db.relationship("InvoiceItem", backref="invoice", lazy=True)
