from . import db

class ItemCategory(db.Model):
    __tablename__ = "item_category"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)

    items = db.relationship("InventoryItem", backref="category", lazy=True)