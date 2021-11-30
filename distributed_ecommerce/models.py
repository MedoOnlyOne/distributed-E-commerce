import datetime
import uuid 
from db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    __bind_key__ = 'users'
    user_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    first_name = db.Column(db.String(length=255), nullable=False)
    last_name = db.Column(db.String(length=255), nullable=False)
    address = db.Column(db.String(length=3000), nullable=False)
    phone_code = db.Column(db.String(length=5), nullable=False)
    phone_number = db.Column(db.String(length=25), nullable=False)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    balance = db.Column(db.Integer(), default=0)
    
    shop = db.relationship('Shop', backref='owner_user', uselist=False) #One-To-One Relationship
    cart = db.relationship('Cart', backref='owner_user', uselist=False) #One-To-One Relationship
    orders = db.relationship('Order', backref='owner_user') #One-To-Many Relationship
    
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.user_id}, {self.first_name}, {self.last_name}, {self.username}, {self.email}')"
        
#Many-To-Many Relationship
order_product = db.Table('order_product',
    db.Column('order_id', db.String(length=36), db.ForeignKey('Orders.order_id')),
    db.Column('product_id', db.String(length=36), db.ForeignKey('Products.product_id')),
)

#Many-To-Many Relationship
cart_product = db.Table('cart_product',
    db.Column('cart_id', db.String(length=36), db.ForeignKey('Carts.cart_id')),
    db.Column('product_id', db.String(length=36), db.ForeignKey('Products.product_id')),
)

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    total_price = db.Column(db.Integer(), default=0)
    order_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    shipping_address = db.Column(db.String(length=255), nullable=False)
    buyer_phone_number = db.Column(db.String(length=11), nullable=False)
    is_ordered = db.Column(db.Boolean(), default=False)
    is_delivered = db.Column(db.Boolean(), default=False)
    
    user_id = db.Column(db.String(length=36), db.ForeignKey('Users.user_id'))
    products = db.relationship('Product', secondary=order_product, backref=db.backref('orders', lazy='dynamic')) 
    
    def get_id(self):
        return self.order_id

    def __repr__(self):
        return f"Order('{self.order_id}, {self.total_price}, {self.order_date}, {self.is_delivered}')"
        


class Cart(db.Model):
    __tablename__ = 'Carts'
    cart_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)

    user_id = db.Column(db.String(length=36), db.ForeignKey('Users.user_id'))
    products = db.relationship('Product', secondary=cart_product, backref=db.backref('cart', lazy='dynamic')) 

    def get_id(self):
        return self.cart_id

    def __repr__(self):
        return f"Cart('{self.cart_id}')"



class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    product_name = db.Column(db.String(length=255), nullable=False)
    category = db.Column(db.String(length=255), nullable=False)
    # color = db.Column(db.String(length=255), nullable=False)
    price = db.Column(db.Integer() , default=0)
    quantity = db.Column(db.Integer(), default=0)
    quantity_incart = db.Column(db.Integer(), default=0)
    description = db.Column(db.String(length=3000), nullable=False)
    # status = db.Column(db.Boolean(), default=True)
    # discount = db.Column(db.Integer(), default=0)
    # image = db.Column(db.LargeBinary())
    image = db.Column(db.String(length=1000), nullable=False)
    
    shop_id = db.Column(db.String(length=36), db.ForeignKey('Shops.shop_id'))

    def get_id(self):
        return self.product_id

    def __repr__(self):
        return f"Product('{self.product_id}, {self.product_name}, {self.category}, {self.price}, {self.quantity}, {self.description}')"



class Shop(db.Model):
    __tablename__ = 'Shops'
    shop_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    shop_name = db.Column(db.String(length=255), nullable=False, unique=True)
    remaining_prods_num = db.Column(db.Integer(), default=0)
    sold_prods_num = db.Column(db.Integer(), default=0)
    
    user_id = db.Column(db.String(length=36), db.ForeignKey('Users.user_id'))
    products = db.relationship('Product', backref='shop') #One-To-Many Relationship
    
    def get_id(self):
        return self.shop_id

    def __repr__(self):
        return f"Shop('{self.shop_id}, {self.shop_name}')"