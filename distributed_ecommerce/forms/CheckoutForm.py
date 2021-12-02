from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, SubmitField

class CheckoutForm(FlaskForm):
    address = StringField(u'Address', [InputRequired(), Length(min=3, max=3000)])
    phone_number = StringField(u'Phone Number', [InputRequired(), Length(min=7, max=25)])
    submit = SubmitField('Complete Order')