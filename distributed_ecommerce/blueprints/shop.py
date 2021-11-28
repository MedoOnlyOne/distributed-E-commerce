from flask import Blueprint, render_template, redirect, url_for
import uuid
from distributed_ecommerce.blueprints.auth import login
from distributed_ecommerce.forms.AddProductForm import AddProductForm
from db import db
from distributed_ecommerce.models import Product, Shop
from flask_login import login_required, current_user

shop = Blueprint('shop', __name__, template_folder='templates')

@login_required
@shop.get('/shop')
def dashboard():
    shop = current_user.shop
    return render_template('shopdashboard.html', shop=shop)

@login_required
@shop.route('/shop/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = AddProductForm()
    if form.validate_on_submit():
        # get the user's shop.
        shop = Shop.query.filter_by(user_id=current_user.user_id).first()
        created_product = Product(product_name=form.product_name.data, category=form.category.data, quantity=form.quantity.data, price=form.price.data, description=form.description.data, image=form.image.data, shop_id=shop.shop_id)
        db.session.add(created_product)
        db.session.commit()
        return redirect(url_for('productpage', product_id=created_product.product_id))
    return render_template('addproduct.html', form=form)

@login_required
@shop.get('/shop/orders')
def orders():
    return render_template('shoporders.html')
    