import re
import os
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, regexp
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SelectField, SubmitField, FileField

class AddProductForm(FlaskForm):
    product_name = StringField(u'Product name', [InputRequired(), Length(min=3, max=255)])
    category = SelectField(u'Category', choices=[('clothing', 'Clothing'), ('tvs', 'TVs'), ('home_applicanes', 'Home Applicanes'), ('furniture', 'Furniture'), ('electronics', 'Electronics'), ('others', 'Others')])
    remaining_in_stock = IntegerField(u'Remaining in stock', [InputRequired()])
    price = DecimalField(u'Remaining in stock', [InputRequired()])
    description = TextAreaField(u'Description', [InputRequired()], Length(min=3, max=255))
    image = FileField(u'Product image', [regexp(u'^[^/\\]\.(jpg|jpeg|png)$')])
    submit = SubmitField('Add product')

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

def upload(request):
    form = AddProductForm(request.POST)
    if form.image.data:
        image_data = request.FILES[form.image.name].read()
        open(os.path.join(../../images, form.image.data), 'w').write(image_data)

    