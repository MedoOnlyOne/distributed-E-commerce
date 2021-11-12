from wtforms.fields.core import DateTimeField
from db import db
import uuid 
import datetime

#Many-To-Many Relationship
order_product = db.Table('order_product',
    db.Column('order_id', db.String, db.ForeignKey('order.order_id')),
    db.Column('product_id', db.String, db.ForeignKey('product.product_id'))
)

class Order(db.Model):
    __tablename__ = 'ORDERS'
    order_id = db.Column('id', db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    total_price = db.Column(db.Integer(), default=1)
    order_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    shipping_address = db.Column(db.String(length=255), nullable=False)
    delivered = db.Column(db.Boolean(), default=True)
    
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    products = db.relationship('Product', secondary=order_product, backref=db.backref('orders', lazy='dynamic')) 
    
    def get_id(self):
        return self.order_id

    def __repr__(self):
        return f"Order('{self.order_id}, {self.total_price}, {self.order_date}')"
        