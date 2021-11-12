from db import db
import uuid 

class Product(db.Model):
    __tablename__ = 'PRODUCTS'
    product_id = db.Column('id', db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    product_name = db.Column(db.String(length=255), nullable=False)
    category = db.Column(db.String(length=255), nullable=False)
    color = db.Column(db.String(length=255), nullable=False)
    price = db.Column(db.Integer() , default=1)
    quantity = db.Column(db.Integer(), default=1)
    status = db.Column(db.Boolean(), default=True)
    discount = db.Column(db.Integer(), default=0)
    image = db.Column(db.LargeBinary())
    
    store_id = db.Column(db.String, db.ForeignKey('store.store_id'))

    def get_id(self):
        return self.product_id

    def __repr__(self):
        return f"Product('{self.product_id}, {self.product_name}, {self.category}, {self.color}, {self.price}, {self.discount}')"
        