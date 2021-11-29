from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, SubmitField

class CheckoutForm(FlaskForm):
    address = StringField(u'Address', [InputRequired()])
    phone_number = StringField(u'Phone Number', [InputRequired(), Length(min=11, max=11)])
    submit = SubmitField('Continue')