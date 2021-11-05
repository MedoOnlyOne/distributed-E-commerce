from db import db
from flask_login import UserMixin
import uuid 

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    user_id = db.Column('id', db.String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    first_name = db.Column(db.String(length=255), nullable=False)
    last_name = db.Column(db.String(length=255), nullable=False)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    balance = db.Column(db.Integer(), default=0)
    
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.user_id}, {self.first_name}, {self.last_name}, {self.username}, {self.email}')"
        