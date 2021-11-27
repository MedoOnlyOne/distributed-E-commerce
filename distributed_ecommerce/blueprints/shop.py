from flask import Blueprint, render_template, redirect, url_for
import uuid
from distributed_ecommerce.blueprints.auth import login
import distributed_ecommerce.forms as forms
from db import db
from distributed_ecommerce.models import Product, Shop
from flask_login import login_required, current_user
from forms import 

shop = Blueprint('shop', __name__, template_folder='templates')

@login_required
@shop.get('/shop')
def dashboard():
    shop = current_user.shop
    return render_template('shopdashboard.html', shop=shop)

@login_required
@shop.route('/shop/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = forms.AddProductForm()
    if form.validate_on_submit():
        created_product = Product(product_id=str(uuid.uuid4()), product_name=form.produc_name.data )
        db.session.add(created_product)
        db.session.commit()
        return redirect(url_for('productpage', product_id=created_product.product_id))
    
    return render_template('addproduct.html')

@login_required
@shop.get('/shop/orders')
def orders():
    return render_template('shoporders.html')
    