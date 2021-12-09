from app import app, create_all
from .auth_util import signup, login, logout

from . import client

def test_empty_db(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'About' in response.data

def test_login_no_account(client):
    response = login(client, 'nabil', '12345678')
    assert response.status_code == 200
    assert b'Incorrect username' in response.data

def test_signup_no_account(client):
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
    assert response.status_code == 200

def test_logout(client):
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
    assert response.status_code == 200
    response = logout(client)
    assert response.status_code == 200
    response = client.get('/userdashboard', follow_redirects=True)
    print(response.data)
    assert b'Login' in response.data
