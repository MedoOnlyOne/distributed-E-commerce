from app import db
from flask_login import UserMixin
from utils.GUID import GUID
import uuid 

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    user_id = db.Column(GUID, default=uuid.uuid4, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Integer(), default=0)
    
    # Show how the user is displayed when printed on the console
    def __repr__(self):
        return f"User('{self.user_id}, {self.first_name}, {self.last_name}, {self.username}, {self.email}')"