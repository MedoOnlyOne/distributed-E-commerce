from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.widgets.core import Input

from models.User import User

def validate_username(form, username):
    existing_user = User.query.filter_by(username=username.data).first()
    if existing_user:
        raise ValidationError('This username already exists')

def validate_email(form, email):
    existing_user = User.query.filter_by(email=email.data).first()
    if existing_user:
        raise ValidationError('This email already exists')

class SignUpForm(FlaskForm):
    first_name = StringField(u'First name', [InputRequired(), Length(min=3, max=255)])
    last_name = StringField(u'Last Name', [InputRequired(), Length(min=3, max=255)])
    email = StringField(u'Email', [InputRequired(), Email('Please enter a proper email'), Length(max=255), validate_email])
    username = StringField(u'Username', [InputRequired(), Length(min=3, max=255), validate_username])
    password = PasswordField(u'Password', [InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField(u'Confirm Password', [InputRequired(), Length(min=8, max=255), EqualTo('password')])
    submit = SubmitField('Sign Up')  
    