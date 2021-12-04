import os 
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_login import LoginManager, current_user, login_required
from distributed_ecommerce.blueprints.auth import auth
from distributed_ecommerce.blueprints.shop import shop
from distributed_ecommerce.blueprints.order import order
from db import db
from app_bcrypt import bcrypt
from distributed_ecommerce.models import User1, User2, Order1, Order2, Cart1, Cart2, Product1, Product2, Shop1, Shop2 

UPLOAD_FOLDER = os.path.join('.', 'images')

template_dir = os.path.join('.', 'distributed_ecommerce', 'templates')
static_dir = os.path.join('.', 'distributed_ecommerce', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(auth)
app.register_blueprint(shop)
app.register_blueprint(order)
# app.register_blueprint(home)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
app.config['SECRET_KEY'] = '26b966b57eb0cdfc098a15141fdd271aedf8cd0c66a76eb240b57309aa43a058ac731f40163443d1653e8bb8b8bf5431dbd075ee2cf351250c971d516037d6ce'
app.config['SQLALCHEMY_BINDS'] = {
    'db2': 'sqlite:///database2.db',
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bcrypt.init_app(app)
db.init_app(app)

def create_all(*args, **kwargs):
    with app.app_context():
        db.create_all(*args, **kwargs)

def drop_all(*args, **kwargs):
    with app.app_context():
        db.drop_all(*args, **kwargs)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    user1 = User1.query.filter_by(user_id=user_id).first()
    user  = User2.query.get(user_id)
    if not user1 or not user:
        return None
    user.first_name = user1.first_name
    user.last_name = user1.last_name
    user.address = user1.address
    user.phone_code = user1.phone_code
    user.phone_number = user1.phone_number
    user.balance = user1.balance
    return user

@app.get('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.get('/')
def home():
    shops1 = Shop1.query.all()
    shops2 = Shop2.query.all()
    for shop in shops2:
        for sh in shops1:
            if sh.shop_id == shop.shop_id:
                prodcuts = []
                for product in shop.products:
                    p = Product1.query.get(product.product_id)
                    prodcuts.append(p)
                sh.products = prodcuts
                break

    return render_template('Mainpage.html', shops=shops1)

@app.get('/contactus')
def contactus():
    return render_template('contactus.html')

@login_required
@app.route('/userdashboard', methods=['GET', 'POST'])
def userdashboard():
    if request.method == "POST":
        first_name = request.form.get("first_name","")
        last_name = request.form.get("last_name", "")
        email = request.form.get("email", "")
        phone_code = request.form.get("code", "")
        phone_number = request.form.get("num", "")
        address = request.form.get("address", "")
        balance = float(request.form.get("balance", ""))

        user1 = User1.query.filter_by(user_id=current_user.user_id).first()
        user2 = User2.query.filter_by(user_id=current_user.user_id).first()

        user1.first_name = first_name if first_name != '' else user1.first_name
        user1.last_name = last_name if last_name != '' else user1.last_name
        user1.phone_code = phone_code if phone_code != '' else user1.phone_code
        user1.phone_number = phone_number if phone_number != '' else user1.phone_number
        user1.address = address if address != '' else user1.address
        user1.balance = balance if balance != '' else user1.balance
        user2.email = email if email != '' else user2.email

        db.session.commit()
        return redirect(url_for("userdashboard"))
    return render_template('userdashboard.html')

@app.get('/product/<product_id>')
def productpage(product_id):
    product1 = Product1.query.filter_by(product_id=product_id).first()
    product2 = Product2.query.filter_by(product_id=product_id).first()
    product_shop = Shop2.query.filter_by(shop_id=product2.shop_id).first()
    shop = Shop1.query.get(product_shop.shop_id)
    product_owner = product_shop.owner_user
    in_cart = current_user.is_authenticated and product2 in current_user.cart.products
    cart_disabled = in_cart or product1.quantity == 0 or product_owner == current_user
    cart_disabled = 'disabled' if cart_disabled else ''
    if product1:
        return render_template('productpage.html', product=product1, shop=shop, cart_disabled=cart_disabled)
    return '<h1> Error 404 <br> Product Not Found'

@login_required
@app.route('/product/edit/<product_id>', methods=['GET', 'POST'])
def editproduct(product_id):
    product = Product1.query.filter_by(product_id=product_id).first()
    if request.method == "POST":
        product_name = request.form.get("product","")
        category = request.form.get("cat","")
        quantity = request.form.get("quantity","")
        price = request.form.get("price","")
        description = request.form.get("description","")

        product.product_name = product_name if product_name != '' else product.product_name
        product.category = category if category != '' else product.category
        product.quantity = quantity if quantity != '' else product.quantity
        product.price = price if price != '' else product.price
        product.description = description if description != '' else product.description

        db.session.commit()
        return redirect(url_for("shop.dashboard"))
    
    else:
        if product:
            return render_template('editproduct.html', product=product)
        return '<h1> Error 404 <br> Product Not Found'


@login_required
@app.route('/product/remove/<product_id>')
def removeproduct(product_id):
    product1 = Product1.query.filter_by(product_id=product_id).first()
    product2 = Product2.query.filter_by(product_id=product_id).first()
    db.session.delete(product1)
    db.session.delete(product2)
    db.session.commit()
    return redirect(url_for("shop.dashboard"))


if __name__ == '__main__':
    app.run(debug=True)
