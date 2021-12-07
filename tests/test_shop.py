import re
from . import client
from .auth_util import signup, login, logout
from .shop_util import add_product
from distributed_ecommerce.models import Product1
def test_add_product(client):
    signup(client, **{
        'first_name': 'Mohamed',
        'last_name': 'Rady',
        'email': 'midorady9999@gmail.com',
        'username': 'nabil',
        'password': '12345678',
        'confirm_password': '12345678',
        'shop_name': 'Nabil shop',
        'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'phone_code': '+20',
        'phone_number': '1110269393',
    })
    response = add_product(client, **{
        'product_name': 'T-shirt',
        'quantity': 10,
        'price': 100,
        'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'category': 'Others',
    })
    assert response.status_code == 200
    assert b'T-shirt' in response.data
    assert b'Add to Cart' in response.data

def test_remove_product(client):
    signup(client, **{
        'first_name': 'Mohamed',
        'last_name': 'Rady',
        'email': 'midorady9999@gmail.com',
        'username': 'nabil',
        'password': '12345678',
        'confirm_password': '12345678',
        'shop_name': 'Nabil shop',
        'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'phone_code': '+20',
        'phone_number': '1110269393',
    })
    response = add_product(client, **{
        'product_name': 'T-shirt',
        'quantity': 10,
        'price': 100,
        'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'category': 'Others',
    })
    product_id = Product1.query.all()[0].product_id
    response = client.get(f'/product/remove/{product_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Your shop doesn't have any products yet" in response.data
