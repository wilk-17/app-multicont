from . import db

class InvoiceItem(db.Model):
    __tablename__ = "invoice_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.BigInteger, db.ForeignKey("invoice.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)