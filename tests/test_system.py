import json
from .auth_util import signup, login, logout
from .shop_util import add_product
from . import client
from distributed_ecommerce.forms import CheckoutForm
from distributed_ecommerce.models import User1, User2, Product2, Cart2

def test_system(client):
    response = signup(client, **{
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
    user = User2.query.filter_by(username='nabil').first()
    assert user is not None
    assert response.status_code == 200
    response = logout(client)
    assert response.status_code == 200
    response = login(client, 'nabil', '12345678')
    assert response.status_code == 200
    assert b'Incorrect username' not in response.data
    assert b'Incorrect password' not in response.data
    add_product(client, **{
        'product_name': 'T-shirt',
        'quantity': 10,
        'price': 100,
        'description': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'category': 'Others',
    })
    assert response.status_code == 200
    product = Product2.query.all()[0]
    assert product is not None
    product_id = product.product_id
    user = User2.query.filter_by(email='midorady9999@gmail.com').first()
    assert product in user.shop.products
    
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
    response = client.put('/product/addtocart', data=json.dumps({
        'product_id': product_id,
    }), content_type='application/json', follow_redirects=True)
    
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    response = client.put('/product/addtoshop', data=json.dumps({
        'product_id': product_id,
    }), content_type='application/json', follow_redirects=True)
    
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    response = client.post('/userdashboard', data={
        'balance': 10000
    }, follow_redirects=True)
    assert response.status_code == 200

    buyer = User1.query.filter_by(last_name="Medhat").first()
    assert buyer.balance == 10000

    form = CheckoutForm(address='xxxxxxxxxx', phone_number='01111111111')

    response = client.post('checkout', data=form.data, follow_redirects=True)
    buyer = User1.query.filter_by(last_name="Medhat").first()
    assert buyer.balance == 10000 - 100
    assert response.status_code == 200

    seller = User2.query.filter_by(username='nabil').first()
    seller = User1.query.get(seller.user_id)
    assert seller.balance == 100
