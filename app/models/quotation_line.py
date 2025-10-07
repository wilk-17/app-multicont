from app import db

class QuotationLine(db.Model):
    __tablename__ = "quotation_line"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)

    inventory_item = db.relationship("InventoryItem", backref="quotation_lines", lazy=True)
    invoices = db.relationship("Invoice", backref="quotation_line", lazy=True)