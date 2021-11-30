from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import uuid
from distributed_ecommerce.blueprints.auth import login
from distributed_ecommerce.forms.CheckoutForm import CheckoutForm
from db import db
from distributed_ecommerce.models import Product, Shop, User, Order, Cart
from flask_login import login_required, current_user
import os
import json

order = Blueprint('order', __name__, template_folder='templates')



@login_required
@order.route('/cart')
def cart():
    # get cart's products
    cart = current_user.cart
    products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()
    # calculate order total price and add its products
    total_price = 0
    products_list = []
    for product in products:
        products_list.append(product) 
        quantity = product.quantity_incart
        total_price += (product.price * quantity)
    return render_template('cart.html', cart=cart, total_price=total_price)


@login_required
@order.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # get cart's products
    cart = current_user.cart
    products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()
    # calculate order total price and add its products
    total_price = 0
    products_list = []
    for product in products:
        products_list.append(product) 
        quantity = product.quantity_incart
        total_price += (product.price * quantity)
    
    form = CheckoutForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # create order
        created_order = Order(order_id=order.order_id, shipping_address = form.address.data, buyer_phone_number = form.phone_number, is_ordered = True, is_delivered = True, total_price = total_price, products=products_list)
        current_user.balance -= total_price
        db.session.add(created_order)
        db.session.commit()

        #empty cart
        for product in products:
            product_temp = Product.query.get(product.product_id)
            products.remove(product)
            shop = Shop.query.filter_by(shop_id=product_temp.shop_id).first()
            user = User.query.filter_by(user_id=shop.user_id)
            user.balance += (product_temp.price * product_temp.quantity_incart)
            product_temp.quantity_incart = 0

            if product_temp.quantity == 0:
                db.session.delete(product_temp)    
            db.session.commit()

        return redirect(url_for('ConfirmOrder', order_id=created_order.order_id))
    return render_template('checkout.html', form=form, cart=cart, total_price=total_price)


@login_required
@order.get('/confirm')
def confirm():
    return render_template('ConfirmOrder.html')


@login_required
@order.route('/dec_product', methods=['POST'])
def dec_product():
    product = json.loads(request.data)
    product_id = product['product_id']
    product = Product.query.get(product.product_id)
    
    # get cart's products
    cart = current_user.cart
    products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()

    for product in products:
        if product.product_id == product_id:
            product.quantity_incart = product.quantity_incart - 1
            product.quantity = product.quantity + 1
            db.session.commit()
    
    return jsonify ({})

@login_required
@order.route('/inc_product', methods=['POST'])
def inc_product():
    product = json.loads(request.data)
    product_id = product['product_id']
    product = Product.query.get(product.product_id)
    
    # get cart's products
    cart = current_user.cart
    products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()

    for product in products:
        if product.product_id == product_id:
            if product.quantity >= 1:
                product.quantity_incart = product.quantity_incart + 1
                product.quantity = product.quantity - 1
                db.session.commit()
    
    return jsonify ({})