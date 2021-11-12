from db import db
import uuid 

class Store(db.Model):
    __tablename__ = 'STORES'
    store_id = db.Column('id', db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    store_name = db.Column(db.String(length=255), nullable=False, unique=True)
    remaining_prods_num = db.Column(db.Integer(), default=0)
    sold_prods_num = db.Column(db.Integer(), default=0)
    
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    products = db.relationship('Product', backref='owner_store') #One-To-Many Relationship
    
    def get_id(self):
        return self.store_id

    def __repr__(self):
        return f"Store('{self.store_id}, {self.store_name}')"
        