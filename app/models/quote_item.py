from app import db

class QuoteItem(db.Model):
    __tablename__ = "quote_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    quote_id = db.Column(db.BigInteger, db.ForeignKey("quote.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)