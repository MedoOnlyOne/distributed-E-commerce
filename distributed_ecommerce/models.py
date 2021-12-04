import datetime
import uuid 
from db import db
from flask_login import UserMixin

class User1(db.Model, UserMixin):
    __tablename__ = 'Users1'
    user_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    first_name = db.Column(db.String(length=255), nullable=False)
    last_name = db.Column(db.String(length=255), nullable=False)
    address = db.Column(db.String(length=3000), nullable=False)
    phone_code = db.Column(db.String(length=5), nullable=False)
    phone_number = db.Column(db.String(length=25), nullable=False)
    balance = db.Column(db.Integer(), default=0)
    
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.user_id}, {self.first_name}, {self.last_name}')"

class User2(db.Model, UserMixin):
    __tablename__ = 'Users2'
    __bind_key__ = 'db2'
    user_id = db.Column(db.String(length=36), db.ForeignKey('Users1.user_id'), primary_key=True)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    
    shop = db.relationship('Shop2', backref='owner_user', uselist=False) #One-To-One Relationship
    cart = db.relationship('Cart2', backref='owner_user', uselist=False) #One-To-One Relationship
    orders = db.relationship('Order2', backref='owner_user') #One-To-Many Relationship
    
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.user_id}, {self.username}, {self.email}')"
        
#Many-To-Many Relationship
order_product = db.Table('order_product',
    db.Column('order_id', db.String(length=36), db.ForeignKey('Orders2.order_id')),
    db.Column('product_id', db.String(length=36), db.ForeignKey('Products2.product_id')),
    db.Column('quantity', db.Integer(), default=1),
    info={'bind_key': 'db2'}
)

#Many-To-Many Relationship
cart_product = db.Table('cart_product',
    db.Column('cart_id', db.String(length=36), db.ForeignKey('Carts2.cart_id')),
    db.Column('product_id', db.String(length=36), db.ForeignKey('Products2.product_id')),
    db.Column('quantity', db.Integer(), default=1),
    info={'bind_key': 'db2'}
)

class Order1(db.Model):
    __tablename__ = 'Orders1'
    order_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    total_price = db.Column(db.Integer(), default=0)
    order_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    shipping_address = db.Column(db.String(length=255), nullable=False)
    buyer_phone_number = db.Column(db.String(length=25), nullable=False)
    
    def get_id(self):
        return self.order_id

    def __repr__(self):
        return f"Order('{self.order_id}, {self.total_price}, {self.order_date}')"

class Order2(db.Model):
    __tablename__ = 'Orders2'
    __bind_key__ = 'db2'
    order_id = db.Column(db.String(length=36), db.ForeignKey('Orders1.order_id'), primary_key=True)
    is_ordered = db.Column(db.Boolean(), default=False)
    is_delivered = db.Column(db.Boolean(), default=False)
    
    user_id = db.Column(db.String(length=36), db.ForeignKey('Users2.user_id'))
    products = db.relationship('Product2', secondary=order_product, backref=db.backref('orders', lazy='dynamic')) 
    
    def get_id(self):
        return self.order_id

    def __repr__(self):
        return f"Order('{self.order_id}, {self.is_delivered}')"
        

class Cart1(db.Model):
    __tablename__ = 'Carts1'
    cart_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)

    def get_id(self):
        return self.cart_id

    def __repr__(self):
        return f"Cart('{self.cart_id}')"

class Cart2(db.Model):
    __tablename__ = 'Carts2'
    __bind_key__ = 'db2'
    cart_id = db.Column(db.String(length=36), db.ForeignKey('Carts1.cart_id'), primary_key=True)
    
    user_id = db.Column(db.String(length=36), db.ForeignKey('Users2.user_id'))
    products = db.relationship('Product2', secondary=cart_product, backref=db.backref('cart', lazy='dynamic')) 

    def get_id(self):
        return self.cart_id

    def __repr__(self):
        return f"Cart('{self.cart_id}')"


class Product1(db.Model):
    __tablename__ = 'Products1'
    product_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    product_name = db.Column(db.String(length=255), nullable=False)
    category = db.Column(db.String(length=255), nullable=False)
    price = db.Column(db.Integer() , default=0)
    quantity = db.Column(db.Integer(), default=0)
    quantity_in_cart = db.Column(db.Integer(), default=0)
    description = db.Column(db.String(length=3000), nullable=False)
    image = db.Column(db.String(length=1000), nullable=False)
    
    def get_id(self):
        return self.product_id

    def __repr__(self):
        return f"Product('{self.product_id}, {self.product_name}, {self.category}, {self.price}, {self.quantity}, {self.description}')"


class Product2(db.Model):
    __tablename__ = 'Products2'
    __bind_key__ = 'db2'
    product_id = db.Column(db.String(length=36), db.ForeignKey('Products1.product_id'), primary_key=True)
    
    shop_id = db.Column(db.String(length=36), db.ForeignKey('Shops2.shop_id'))

    def get_id(self):
        return self.product_id

    def __repr__(self):
        return f"Product('{self.product_id}, {self.shop_id}')"

class Shop1(db.Model):
    __tablename__ = 'Shops1'
    shop_id = db.Column(db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    shop_name = db.Column(db.String(length=255), nullable=False, unique=True)
    remaining_prods_num = db.Column(db.Integer(), default=0)
    sold_prods_num = db.Column(db.Integer(), default=0)
    
    def get_id(self):
        return self.shop_id

    def __repr__(self):
        return f"Shop('{self.shop_id}, {self.shop_name}')"

class Shop2(db.Model):
    __tablename__ = 'Shops2'
    __bind_key__ = 'db2'
    shop_id = db.Column(db.String(length=36), db.ForeignKey('Shops1.shop_id'), primary_key=True)
    
    user_id = db.Column(db.String(length=36), db.ForeignKey('Users2.user_id'))
    products = db.relationship('Product2', backref='shop') #One-To-Many Relationship
    
    def get_id(self):
        return self.shop_id

    def __repr__(self):
        return f"Shop('{self.shop_id}, {self.user_id}')"
