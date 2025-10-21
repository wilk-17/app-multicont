"""SalesOrderItem Entity"""
from datetime import datetime
from app import db

class SalesOrderItem(db.Model):
    __tablename__ = "sales_order_item"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sales_order_id = db.Column(db.BigInteger, db.ForeignKey("sales_order.id"), nullable=False)
    item_id = db.Column(db.BigInteger, db.ForeignKey("inventory_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def __init__(self, sales_order_id=None, item_id=None, quantity=None):
        self.sales_order_id = sales_order_id
        self.item_id = item_id
        self.quantity = quantity
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'sales_order_id': str(self.sales_order_id),
            'item_id': str(self.item_id),
            'quantity': self.quantity
        }
