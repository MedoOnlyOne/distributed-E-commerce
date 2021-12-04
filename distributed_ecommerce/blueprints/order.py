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
    for product in products:
        quantity = product.quantity_in_cart
        total_price += (product.price * quantity)
    return render_template('cart.html', cart=cart, total_price=total_price)

@login_required
@order.put('/product/addtocart')
def addtocart():
    try:
        product = Product.query.get(request.json['product_id'])
        if current_user.is_authenticated:
            cart = current_user.cart
            product.quantity_in_cart += 1
            product.quantity -= 1
            cart.products.append(product)
            db.session.commit()
            return jsonify({
                'status': 'success',
            })
        return jsonify({
            'status': 'redirect',
        })
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'failed'
        }), 500

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
        quantity = product.quantity_in_cart
        total_price += (product.price * quantity)
    
    form = CheckoutForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if total_price > current_user.balance:
            return redirect(url_for('order.reject'))
        # create order
        created_order = Order(order_id=str(uuid.uuid4()), shipping_address = form.address.data, buyer_phone_number = form.phone_number.data, is_ordered = True, is_delivered = True, total_price = total_price, products=products_list, user_id = current_user.user_id)
        current_user.balance -= total_price
        db.session.add(created_order)
        db.session.commit()

        #empty cart
        for product in products:
            cart.products.remove(product)
            shop = Shop.query.filter_by(shop_id=product.shop_id).first()
            user = User.query.filter_by(user_id=shop.user_id).first()
            user.balance = user.balance + (product.price * product.quantity_in_cart)            
            shop.products.remove(product)    
            product.quantity -= product.quantity_in_cart
            product.quantity_in_cart = 0 
            shop.products.append(product)          

            if product.quantity == 0:
                db.session.delete(product)                
            
            db.session.commit()

        return redirect(url_for('order.confirm'))
    return render_template('checkout.html', form=form, cart=cart, total_price=total_price)


@login_required
@order.get('/confirm')
def confirm():
    return render_template('ConfirmOrder.html')

@login_required
@order.get('/reject')
def reject():
    return render_template('RejectOrder.html')


@login_required
@order.route('/cart/dec_product/<product_id>')
def dec_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    # get cart's products
    cart = current_user.cart
    products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()

    for productt in products:
        if productt.product_id == product_id:
            product.quantity_in_cart -= 1
            product.quantity += 1
            if product.quantity_in_cart == 0:
                cart.products.remove(product)
            db.session.commit()
    
    return redirect(url_for('order.cart'))

@login_required
@order.route('/cart/inc_product/<product_id>')
def inc_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    # get cart's products
    cart = current_user.cart
    products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()

    for productt in products:
        if productt.product_id == product_id:
            if product.quantity >= 1:
                product.quantity_in_cart += 1
                product.quantity -= 1
                db.session.commit()
    
    return redirect(url_for('order.cart'))