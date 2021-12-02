from flask import Blueprint, render_template, redirect, url_for, request
import uuid
from distributed_ecommerce.blueprints.auth import login
from distributed_ecommerce.forms.AddProductForm import AddProductForm
from db import db
from distributed_ecommerce.models import User, Product, Shop
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename


shop = Blueprint('shop', __name__, template_folder='templates')

@login_required
@shop.get('/shop')
def dashboard():
    shop = current_user.shop
    products = Product.query.filter_by(shop_id=shop.shop_id).all()
    
    return render_template('shopdashboard.html',shop=shop, products=products)

@login_required
@shop.get('/shop/<shop_id>')
def shop_view(shop_id):
    shop = Shop.query.get(shop_id)
    if shop:
        user = User.query.get(shop.user_id)
        products = shop.products        
        return render_template('shop.html', shop=shop, shop_owner=user, products=products)
    return 'Error 404.<br> Shop not found'

@login_required
@shop.route('/shop/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = AddProductForm()
    if form.validate_on_submit():
        # get the user's shop.
        shop = Shop.query.filter_by(user_id=current_user.user_id).first()
        # get the image
        image = form.image.data
        image_name = secure_filename(image.filename)

        # craete product
        created_product = Product(product_name=form.product_name.data, category=form.category.data, quantity=form.quantity.data, price=form.price.data, description=form.description.data, image=image_name, shop_id=shop.shop_id)
        db.session.add(created_product)
        db.session.commit()

        # save the image
        image.save(os.path.join(os.getcwd(), 'images', image_name))

        return redirect(url_for('productpage', product_id=created_product.product_id))
    return render_template('addproduct.html', form=form)

@login_required
@shop.get('/shop/orders')
def orders():
    return render_template('shoporders.html')
