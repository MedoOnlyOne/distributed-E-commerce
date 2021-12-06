from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField, SubmitField

class LogInForm(FlaskForm):
    username = StringField(u'Username', [InputRequired(), Length(min=3, max=255, message='Must be at least 3 characters long')])
    password = PasswordField(u'Password', [InputRequired(), Length(min=8, max=255, message='Must be at least 3 characters long')])
    submit = SubmitField('Login')   
    