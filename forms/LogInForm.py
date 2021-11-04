from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.widgets.core import Input

class LogInForm(FlaskForm):
    username = StringField('username', [InputRequired(), Length(min=3, max=255)])
    password = PasswordField('password', [InputRequired(), Length(min=8, max=255)])
    submit = SubmitField('Login')    
    