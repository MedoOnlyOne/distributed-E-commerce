from distributed_ecommerce.forms import LogInForm
from distributed_ecommerce.forms import SignUpForm

def login(client, username, password):
    form = LogInForm(username=username, password=password)
    return client.post('/login', data=form.data, follow_redirects=True)

def logout(client):
    return client.post('/logout', follow_redirects=True)

def signup(client, first_name, last_name, email, username, password, confirm_password, shop_name, address, phone_code, phone_number):
    form = SignUpForm(first_name=first_name, last_name=last_name, email=email, username=username, password=password, confirm_password=confirm_password, shop_name=shop_name, address=address, phone_code=phone_code, phone_number=phone_number)
    return client.post('/signup', data=form.data, follow_redirects=True)
