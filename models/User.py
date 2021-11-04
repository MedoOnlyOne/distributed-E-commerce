from app import db
from flask_login import UserMixin
from utils.GUID import GUID
import uuid 

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    user_id = db.Column(GUID, default=uuid.uuid4, primary_key=True)
    first_name = db.Column(db.String(length=255), nullable=False)
    last_name = db.Column(db.String(length=255), nullable=False)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    balance = db.Column(db.Integer(), default=0)
    