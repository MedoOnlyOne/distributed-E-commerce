from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from utils.GUID import GUID
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    user_id = db.Column(GUID, default=uuid.uuid4, primary_key=True)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    balance = db.Column(db.Integer(), default=0)

@app.get('/')
def home():
    return "Home"

if __name__ == '__main__':
    app.run(debug=True)
