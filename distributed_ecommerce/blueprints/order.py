from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import uuid
from distributed_ecommerce.blueprints.auth import login
from distributed_ecommerce.forms.CheckoutForm import CheckoutForm
from db import db
from distributed_ecommerce.models import Product1, Product2, Shop1, Shop2, User1, User2, Order1, Order2, Cart1, Cart2, cart_product
from flask_login import login_required, current_user
import os
import json

order = Blueprint('order', __name__, template_folder='templates')

@login_required
@order.patch('/savecart')
def savecart():
    try:
        cart = current_user.cart
        products = cart.products
        quantities = request.json['quantities']
        total_price = 0
        for index, product in enumerate(products):
                product = Product1.query.get(product.product_id)
                value = 0
                if product.quantity < quantities[index]:
                    value = product.quantity
                else:
                    value = quantities[index]
                db.session.query(cart_product).filter_by(product_id=product.product_id, cart_id=cart.cart_id).update({"quantity": (value)})
                db.session.commit()
        return jsonify({
            "status": "success",
        })
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'failed'
        }), 500

@login_required
@order.route('/cart')
def cart():
    # get cart's products
    cart = current_user.cart
    # products = Product1.query.filter(Product2.cart.any(cart_id=cart.cart_id)).all()
    products = cart.products
    # calculate order total price and add its products
    total_price = 0
    returned_products = []
    stocks = []
    for product in products:
        p = Product1.query.get(product.product_id)
        quantity = db.session.query(cart_product).filter_by(product_id=p.product_id, cart_id=cart.cart_id).first().quantity
        p.quantiy_purchesed = quantity
        returned_products.append(p)
        stocks.append(p.quantity)
        total_price += (p.price * quantity)
    return render_template('cart.html', cart=cart, total_price=total_price, products=returned_products, stocks = json.dumps(stocks))

@login_required
@order.put('/product/addtocart')
def addtocart():
    try:
        product1 = Product1.query.get(request.json['product_id'])
        if current_user.is_authenticated:
            cart = current_user.cart
            product2 = Product2.query.get(request.json['product_id'])
            cart.products.append(product2)
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
    # products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()
    products = cart.products
    # calculate order total price and add its products
    total_price = 0
    products_list = []
    for product in products:
        product = Product1.query.get(product.product_id)
        quantity = db.session.query(cart_product).filter_by(product_id=product.product_id, cart_id=cart.cart_id).first().quantity
        product.quantiy_purchased = quantity
        products_list.append(product)
        total_price += (product.price * quantity)

    form = CheckoutForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if total_price > current_user.balance:
            return redirect(url_for('order.reject'))
        # create order
        created_order1 = Order1(order_id=str(uuid.uuid4()), shipping_address = form.address.data, buyer_phone_number = form.phone_number.data, total_price = total_price)
        created_order2 = Order2(order_id=created_order1.order_id, is_ordered = True, is_delivered = True, products=products, user_id = current_user.user_id)
        if current_user.balance >= total_price:
            buyer = User1.query.get(current_user.user_id)
            buyer.balance -= total_price
            db.session.add(created_order1)
            db.session.add(created_order2)
            # db.session.commit()

            #empty cart
            for product in products:
                quantity = db.session.query(cart_product).filter_by(product_id=product.product_id, cart_id=cart.cart_id).first().quantity
                # cart.products.remove(product)
                shop = Shop2.query.filter_by(shop_id=product.shop_id).first()
                user = User1.query.filter_by(user_id=shop.user_id).first()
                product = Product1.query.get(product.product_id)
                user.balance = user.balance + (product.price * quantity)            
                product.quantity -= quantity             
                
            cart.products = []
            db.session.commit()

            return redirect(url_for('order.confirm'))
        return render_template('checkout.html', form=form, cart=cart, total_price=total_price, products = products_list)
    return render_template('checkout.html', form=form, cart=cart, total_price=total_price, products = products_list)


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
    product = Product1.query.filter_by(product_id=product_id).first()
    # get cart's products
    cart = current_user.cart
    # products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()
    products = cart.products

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
    product = Product1.query.filter_by(product_id=product_id).first()
    # get cart's products
    cart = current_user.cart
    # products = Product.query.filter(Product.cart.any(cart_id=cart.cart_id)).all()
    products = cart.products

    for productt in products:
        if productt.product_id == product_id:
            if product.quantity >= 1:
                product.quantity_in_cart += 1
                product.quantity -= 1
                db.session.commit()
    
    return redirect(url_for('order.cart'))