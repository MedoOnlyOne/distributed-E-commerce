import re
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SelectField, SubmitField

class AddProductForm(FlaskForm):
    product_name = StringField(u'Product name', [InputRequired()])
    category = SelectField(u'Category', choices=[('others', 'Others'), ('clothing', 'Clothing'), ('tvs', 'TVs'), ('home_applicanes', 'Home Applicanes'), ('furniture', 'Furniture'), ('electronics', 'Electronics')])
    quantity = IntegerField(u'Quantity', [InputRequired()])
    price = IntegerField(u'Price', [InputRequired()])
    description = TextAreaField(u'Description', [InputRequired()])
    image = FileField(u'Product image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Add product')
    