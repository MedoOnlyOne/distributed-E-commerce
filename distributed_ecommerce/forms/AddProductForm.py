import re
import os
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SelectField, SubmitField, FileField, validators

class AddProductForm(FlaskForm):
    product_name = StringField(u'Product name', [InputRequired()])
    category = SelectField(u'Category', choices=[('clothing', 'Clothing'), ('tvs', 'TVs'), ('home_applicanes', 'Home Applicanes'), ('furniture', 'Furniture'), ('electronics', 'Electronics'), ('others', 'Others')])
    quantity = IntegerField(u'Quantity', [InputRequired()])
    price = DecimalField(u'Price', [InputRequired()])
    description = TextAreaField(u'Description', [InputRequired()])
    image = FileField(u'Product image', [validators.regexp(r'^[^/\\]\.(jpg|jpeg|png)$')])
    submit = SubmitField('Add product')

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

def upload(request):
    form = AddProductForm(request.POST)
    if form.image.data:
        image_data = request.FILES[form.image.name].read()
        open(os.path.join('..', '..', 'images', form.image.data), 'w').write(image_data)

    