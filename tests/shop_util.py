import io
from werkzeug.datastructures import FileStorage
from distributed_ecommerce.forms import AddProductForm

def add_product(client, product_name, quantity, price, category, description):
    image = FileStorage(stream=io.BytesIO(b"abcdef"), filename='test.jpg')
    form = AddProductForm(product_name=product_name, quantity=quantity, price=price, category=category, description=description, image=image)    
    return client.post('/shop/addproduct', data=form.data, follow_redirects=True, content_type='multipart/form-data')
