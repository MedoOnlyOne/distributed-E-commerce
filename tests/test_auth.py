import os
import tempfile

import pytest

from app import app, create_all
from .auth_util import signup, login, logout

@pytest.fixture
def client():
    db1_fd, db1_path = tempfile.mkstemp()
    db2_fd, db2_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db1_path}'
    app.config['SQLALCHEMY_BINDS'] = {
        'db2': f'sqlite:///{db2_path}',
    }
    with app.app_context():
        with app.test_request_context():
            with app.test_client() as client:
                create_all()
                yield client
    os.close(db1_fd)
    os.close(db2_fd)
    os.unlink(db1_path)
    os.unlink(db2_path)

def test_empty_db(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'About'in response.data

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
    assert b'My shop' in response.data and b'My Account' in response.data and b'Mohamed' in response.data and b'Rady' in response.data

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
    assert b'Login' in response.data
    response = client.get('/userdashboard')
    assert b'Login' in response.data
