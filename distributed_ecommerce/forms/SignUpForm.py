from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email, ValidationError
from wtforms import StringField, PasswordField, TextAreaField, SubmitField

from distributed_ecommerce.models import User, Shop

def validate_username(form, username):
    existing_user = User.query.filter_by(username=username.data).first()
    if existing_user:
        raise ValidationError('This username already exists')

def validate_shop_name(form, shop_name):
    existing_shop = Shop.query.filter_by(shop_name=shop_name.data).first()
    if existing_shop:
        raise ValidationError('This shop already exists')

def validate_email(form, email):
    existing_user = User.query.filter_by(email=email.data).first()
    if existing_user:
        raise ValidationError('This email already exists')

class SignUpForm(FlaskForm):
    first_name = StringField(u'First Name', [InputRequired(), Length(min=3, max=255)])
    last_name = StringField(u'Last Name', [InputRequired(), Length(min=3, max=255)])
    email = StringField(u'Email', [InputRequired(), Email('Please enter a proper email'), Length(max=255), validate_email])
    username = StringField(u'Username', [InputRequired(), Length(min=3, max=255), validate_username])
    shop_name = StringField(u'shop name', [InputRequired(), Length(min=3, max=255), validate_shop_name])
    phone_code = StringField(u'Phone code', [InputRequired(), Length(min=2, max=5)])
    phone_number = StringField(u'Phone number', [InputRequired(), Length(min=7, max=25)])
    address = TextAreaField(u'Address', [InputRequired(), Length(min=3, max=3000)])
    password = PasswordField(u'Password', [InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField(u'Confirm password', [InputRequired(), Length(min=8, max=255)])
    submit = SubmitField('Sign Up')  
