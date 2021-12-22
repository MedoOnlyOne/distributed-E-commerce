from flask import Blueprint, render_template, redirect, url_for, request
import flask
import uuid
from distributed_ecommerce.blueprints.auth import login
from distributed_ecommerce.forms.AddProductForm import AddProductForm
from db import db
from distributed_ecommerce.models import User1, User2, Product1, Product2, Shop1, Shop2
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename


shop = Blueprint('shop', __name__, template_folder='templates')

@shop.get('/shop')
@login_required
def dashboard():
    shop = current_user.shop
    products = shop.products
    
    for p in products:
        product = Product1.query.filter_by(product_id=p.product_id).first()
        p.product_name = product.product_name
        p.category = product.category
        p.price = product.price
        p.quantity = product.quantity
        p.quantity_in_cart = product.quantity_in_cart
        p.description = product.description
        p.image = product.image
    
    response = flask.Response(render_template('shopdashboard.html',shop=shop, products=products))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@shop.get('/shop/<shop_id>')
def shop_view(shop_id):
    shop = Shop2.query.get(shop_id)
    if shop:
        shop1 = Shop1.query.get(shop_id)
        shop.shop_name = shop1.shop_name
        user = User2.query.get(shop.user_id)
        products = shop.products
        for product in products:
            p = Product1.query.get(product.product_id)
            product.product_name = p.product_name
            product.price = p.price
            product.image = p.image
            product.description = p.description
            product.category = p.category
            product.quantity = p.quantity

        response = flask.Response(render_template('shop.html', shop=shop, shop_owner=user, products=products))
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 200
        return response
    
    response = flask.Response('Error 404.<br> Shop not found')
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 404
    return response

@shop.get('/shop/addproduct')
@login_required
def addproduct():
    form = AddProductForm()
    response = flask.Response(render_template('addproduct.html', form=form))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@shop.post('/shop/addproduct')
@login_required
def postaddproduct():
    form = AddProductForm()
    if form.validate_on_submit():
        # get the user's shop.
        shop = Shop2.query.filter_by(user_id=current_user.user_id).first()

        # get the image
        image = form.image.data
        image_name = secure_filename(image.filename)

        # craete product
        created_product1 = Product1(product_id=str(uuid.uuid4()),product_name=form.product_name.data, category=form.category.data, quantity=form.quantity.data, price=form.price.data, description=form.description.data, image=image_name)
        created_product2 = Product2(product_id=created_product1.product_id, user_id=current_user.user_id)
        shop.products.append(created_product2)
        db.session.add(created_product1)
        db.session.add(created_product2)
        db.session.commit()

        # save the image
        image.save(os.path.join(os.getcwd(), 'images', image_name))

        response = redirect(url_for('productpage', product_id=created_product1.product_id))
        response.is_redirectrd = True
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 302
        return response

    response = flask.Response(render_template('addproduct.html', form=form))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@shop.get('/shop/orders')
@login_required
def orders():
    response = flask.Response(render_template('shoporders.html'))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response
