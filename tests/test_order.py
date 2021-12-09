import json
from .auth_util import signup, login, logout
from .shop_util import add_product
from . import client
from distributed_ecommerce.forms import CheckoutForm
from distributed_ecommerce.models import User1, User2, Product2, Cart2

def test_add_to_cart(client):
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
    add_product(client, **{
        'product_name': 'T-shirt',
        'quantity': 10,
        'price': 100,
        'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'category': 'Others',
    })
    product = Product2.query.all()[0]
    product_id = product.product_id
    logout(client)
    response = signup(client, **{
        'first_name': 'Mohamed',
        'last_name': 'Medhat',
        'email': 'example@example.com',
        'username': 'medhat',
        'password': '12345678',
        'confirm_password': '12345678',
        'shop_name': 'Medhat shop',
        'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'phone_code': '+20',
        'phone_number': '111111111',
    })
    print(response.data)
    product = Product2.query.all()[0]
    product_id = product.product_id
    response = client.put('/product/addtocart', data=json.dumps({
        'product_id': product_id,
    }), content_type='application/json', follow_redirects=True)
    user = User2.query.filter_by(email='example@example.com').first()
    cart = user.cart

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert product in cart.products

# def test_add_to_cart(client):
#     signup(client, **{
#         'first_name': 'Mohamed',
#         'last_name': 'Rady',
#         'email': 'midorady9999@gmail.com',
#         'username': 'nabil',
#         'password': '12345678',
#         'confirm_password': '12345678',
#         'shop_name': 'Nabil shop',
#         'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
#         'phone_code': '+20',
#         'phone_number': '1110269393',
#     })
#     add_product(client, **{
#         'product_name': 'T-shirt',
#         'quantity': 10,
#         'price': 100,
#         'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
#         'category': 'Others',
#     })
    # product_id = Product1.query.all()[0].product_id
    # response = client.put('/product/addtocart', data=json.dumps({
    #     'product_id': product_id,
    # }), content_type='application/json', follow_redirects=True)
#     assert response.status_code == 200
#     assert response.json['status'] == 'success'
#     cart = 
    

def test_add_to_shop(client):
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
    add_product(client, **{
        'product_name': 'T-shirt',
        'quantity': 10,
        'price': 100,
        'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'category': 'Others',
    })
    product = Product2.query.all()[0]
    product_id = product.product_id
    logout(client)
    signup(client, **{
        'first_name': 'Mohamed',
        'last_name': 'Medhat',
        'email': '3M@test.com',
        'username': 'Medo_3M',
        'password': '123456789',
        'confirm_password': '123456789',
        'shop_name': '3M Store',
        'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'phone_code': '+20',
        'phone_number': '1111111111',
    })
    response = client.put('/product/addtoshop', data=json.dumps({
        'product_id': product_id,
    }), content_type='application/json', follow_redirects=True)

    user = User2.query.filter_by(email='3M@test.com').first()
    shop = user.shop

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert product in user.shop.products

def test_checkout(client):
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
    add_product(client, **{
        'product_name': 'T-shirt',
        'quantity': 10,
        'price': 100,
        'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'category': 'Others',
    })
    product_id = Product2.query.all()[0].product_id
    logout(client)
    signup(client, **{
        'first_name': 'Mohamed',
        'last_name': 'Medhat',
        'email': '3M@test.com',
        'username': 'Medo_3M',
        'password': '123456789',
        'confirm_password': '123456789',
        'shop_name': '3M Store',
        'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'phone_code': '+20',
        'phone_number': '1111111111',
    })
    response = client.put('/product/addtocart', data=json.dumps({
        'product_id': product_id,
    }), content_type='application/json', follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    response = client.post('/userdashboard', data={
        'balance': 10000
    }, follow_redirects=True)
    assert response.status_code == 200

    user2 = User2.query.filter_by(username = "Medo_3M").first()
    user_id = user2.user_id
    user1 = User1.query.get(user_id)
    assert user1.balance == 10000

    form = CheckoutForm(address='xxxxxxxxxx', phone_number='01111111111')

    response = client.post('checkout', data=form.data, follow_redirects=True)
    user1 = User1.query.get(user_id)
    assert user1.balance == 10000 - 100
    assert response.status_code == 200
