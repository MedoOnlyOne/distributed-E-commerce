from flask import Blueprint, render_template, redirect, url_for, request
import uuid
from distributed_ecommerce.blueprints.auth import login
from distributed_ecommerce.forms.CheckoutForm import CheckoutForm
from db import db
from distributed_ecommerce.models import Order, User
from flask_login import login_required, current_user
import os

order = Blueprint('order', __name__, template_folder='templates')

@login_required
@order.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # get user's info.
        user = User.query.filter_by(user_id=current_user.user_id).first()
        # create order
        created_order = Order(order_id=order.order_id, shipping_address = form.address.data, buyer_phone_number = form.phone_number, is_ordered = True, is_delivered = True)
        db.session.add(created_order)
        db.session.commit()

        return redirect(url_for('ConfirmOrder', order_id=created_order.order_id))
    return render_template('CheckoutPage.html', form=form)

@login_required
@order.get('/confirm')
def confirm():
    #total_price = Order(total_price=order.total_price)
    return render_template('ConfirmOrder.html', total_price=100)




