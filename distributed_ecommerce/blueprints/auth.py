from flask import Blueprint, render_template, redirect, url_for
import flask
import uuid
import distributed_ecommerce.forms as forms
from db import db
from app_bcrypt import bcrypt
from distributed_ecommerce.models import User1, User2, Shop1, Shop2, Cart1, Cart2
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.get('/login')
def login():
    form = forms.LogInForm()
    response = flask.Response(render_template('login.html', form=form))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@auth.post('/login')
def postlogin():
    form = forms.LogInForm()

    if form.validate_on_submit():
        user = User2.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                response = redirect(url_for('home'))
                response.is_redirectrd = True
                response.headers['Content-Type'] = 'text/html'
                response.headers['status_code'] = 302
                return response

            response = flask.Response(render_template('login.html', form=form, message="Incorrect password"))
            response.headers['Content-Type'] = 'text/html'
            response.headers['status_code'] = 200
            return response
        
        response = flask.Response(render_template('login.html', form=form, message="Incorrect username"))
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 200
        return response

    response = flask.Response(render_template('login.html', form=form))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@auth.get('/logout')
@login_required
def logout():
    logout_user()
    response = redirect(url_for('home'))
    response.is_redirectrd = True
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 302
    return response
    

@auth.get('/signup')
def signup():
    form = forms.SignUpForm()
    if current_user.is_authenticated:
        response = redirect(url_for('home'))
        response.is_redirectrd = True
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 302
        return response
    response = flask.Response(render_template('signup.html', form=form))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@auth.post('/signup')
def postsignup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        created_user1 = User1(user_id=str(uuid.uuid4()), first_name=form.first_name.data, last_name=form.last_name.data, address=form.address.data, phone_code=form.phone_code.data, phone_number=form.phone_number.data)
        created_user2 = User2(username=form.username.data, email=form.email.data, password=hashed_password, user_id=created_user1.user_id)
        created_shop1 = Shop1(shop_id=str(uuid.uuid4()), shop_name=form.shop_name.data)
        created_shop2 = Shop2(user_id=created_user1.user_id, shop_id=created_shop1.shop_id)
        created_cart1 = Cart1(cart_id=str(uuid.uuid4()))
        created_cart2 = Cart2(cart_id=created_cart1.cart_id, user_id=created_user1.user_id)
        
        db.session.add(created_user1)
        db.session.add(created_shop1)
        db.session.add(created_cart1)

        db.session.add(created_user2)
        db.session.add(created_shop2)
        db.session.add(created_cart2)
        
        db.session.commit()
        
        login_user(created_user2)
        response = redirect(url_for('home'))
        response.is_redirectrd = True
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 302
        return response
    if current_user.is_authenticated:
        response = redirect(url_for('home'))
        response.is_redirectrd = True
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 302
        return response
    response = flask.Response(render_template('signup.html', form=form))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response
