import os 
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import flask
from flask_login import LoginManager, current_user, login_required
from werkzeug.wrappers import response
from distributed_ecommerce.blueprints.auth import auth
from distributed_ecommerce.blueprints.shop import shop
from distributed_ecommerce.blueprints.order import order
from db import db
from app_bcrypt import bcrypt
from distributed_ecommerce.models import User1, User2, Order1, Order2, Cart1, Cart2, Product1, Product2, Shop1, Shop2, Transaction1, Transaction2
from random import randrange

UPLOAD_FOLDER = os.path.join('.', 'images')

template_dir = os.path.join('.', 'distributed_ecommerce', 'templates')
static_dir = os.path.join('.', 'distributed_ecommerce', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(auth)
app.register_blueprint(shop)
app.register_blueprint(order)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '26b966b57eb0cdfc098a15141fdd271aedf8cd0c66a76eb240b57309aa43a058ac731f40163443d1653e8bb8b8bf5431dbd075ee2cf351250c971d516037d6ce'

if 'mode' in os.environ and os.environ['mode'] == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@db1/dsproject'
    app.config['SQLALCHEMY_BINDS'] = {
        'db2': 'mysql+pymysql://root:12345678@db2/dsproject',
    }
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
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

@login_manager.unauthorized_handler
def unauthorized_callback():
       return redirect('/login?next=' + request.path)

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
    current_user_products_in_cart = []
    if current_user.is_authenticated:
        for p in current_user.cart.products:
            current_user_products_in_cart.append(p.product_id)
    print(current_user_products_in_cart)
    for shop in shops2:
        for sh in shops1:
            if sh.shop_id == shop.shop_id:
                prodcuts = []
                if len(shop.products) <= 3:
                    for product in shop.products:
                        p = Product1.query.get(product.product_id)
                        p2 = Product2.query.get(product.product_id)
                        p.user_id = p2.user_id
                        prodcuts.append(p)
                else:
                    random_products_indexes = []
                    for i in range(3):
                        x = randrange(len(shop.products))
                        while x in random_products_indexes:
                            x = randrange(len(shop.products))
                        random_products_indexes.append(x)
                        p = Product1.query.get(shop.products[random_products_indexes[i]].product_id)
                        p2 = Product2.query.get(shop.products[random_products_indexes[i]].product_id)
                        p.user_id = p2.user_id
                        prodcuts.append(p)
                sh.products = prodcuts
                break
    response = flask.Response(render_template('Mainpage.html', shops=shops1, current_user_products_in_cart=current_user_products_in_cart))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@app.get('/contactus')
def contactus():
    response = flask.Response(render_template('contactus.html'))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@app.get('/userdashboard')
@login_required
def userdashboard():
    response = flask.Response(render_template('userdashboard.html'))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@app.post('/userdashboard')
@login_required
def postuserdashboard():
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

    response = redirect(url_for('userdashboard'))
    response.is_redirectrd = True
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 302
    return response

@app.get('/product/<product_id>')
def productpage(product_id):
    product1 = Product1.query.filter_by(product_id=product_id).first()
    product2 = Product2.query.filter_by(product_id=product_id).first()
    if not product1 or not product2:
        return '<h1> Error 404 <br> Product Not Found'
    shops = product2.shops
    product_shop = shops[0]
    shop = Shop1.query.get(product_shop.shop_id)
    product_owner = product_shop.owner_user
    in_cart = current_user.is_authenticated and product2 in current_user.cart.products
    in_shop = current_user.is_authenticated and product2 in current_user.shop.products
    cart_disabled = not current_user.is_authenticated or in_cart or product1.quantity == 0 or product_owner.user_id == current_user.user_id
    cart_disabled = 'disabled' if cart_disabled else ''
    add_to_shop_disabled = not current_user.is_authenticated or in_shop or product_owner.user_id == current_user.user_id
    add_to_shop_disabled = 'disabled' if add_to_shop_disabled else ''
    response = flask.Response(render_template('productpage.html', product=product1, shop=shop, cart_disabled=cart_disabled, add_to_shop_disabled=add_to_shop_disabled))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

@app.get('/product/edit/<product_id>')
@login_required
def editproduct(product_id):
    product = Product1.query.filter_by(product_id=product_id).first()
    if product:
        response = flask.Response(render_template('editproduct.html', product=product))
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 200
        return response
        
    response = flask.Response('<h1> Error 404 <br> Product Not Found')
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 404
    return response

@app.put('/product/edit/<product_id>')
@login_required
def posteditproduct(product_id):
    product = Product1.query.filter_by(product_id=product_id).first()
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
    response = redirect(url_for("shop.dashboard"))
    response.is_redirectrd = True
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 302
    return response

@app.get('/product/remove/<product_id>')
@login_required
def removeproduct(product_id):
    product1 = Product1.query.filter_by(product_id=product_id).first()
    if not product1:
        response = redirect(url_for('auth.login'))
        response.is_redirectrd = True
        response.headers['Content-Type'] = 'text/html'
        response.headers['status_code'] = 302
        return response
    product2 = Product2.query.filter_by(product_id=product_id).first()
    db.session.delete(product1)
    db.session.delete(product2)
    db.session.commit()
    response = redirect(url_for("shop.dashboard"))
    response.is_redirectrd = True
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 302
    return response

@app.get('/report')
@login_required
def getreport():
    transaction1 = Transaction1.query.all()
    transaction2 = Transaction2.query.all()
    transactions = []
    for t1 in transaction1:
        for t2 in transaction2:
            if t1.transaction_id != t2.transaction_id:
                continue
            product = Product1.query.filter_by(product_id=t2.product_id).first()
            product2 = Product2.query.filter_by(product_id=t2.product_id).first()
            owner = Shop2.query.filter_by(user_id=product2.user_id).first()
            owner_shop = Shop1.query.filter_by(shop_id=owner.shop_id).first()

            add_to_shop = True if (t1.transaction_type == "Add to shop") else False
            new_shop = None
            buyer = None
            quantity = None
            cost = None
            if add_to_shop:
                new_shop = Shop1.query.filter_by(shop_id=t2.new_shop).first()
            else:
                buyer = User2.query.filter_by(user_id=t2.buyer).first()
                quantity = t2.quantity
                cost = quantity * product.price
            t = {
                "type": t1.transaction_type,
                "product":product.product_name,
                "owner": owner_shop.shop_name,
                "new_shop": None if not new_shop else new_shop.shop_name,
                "buyer": None if not buyer else buyer.username,
                "quantity": None if not quantity else quantity,
                "cost": None if not cost else cost
            }
            transactions.append(t)
            break
    response = flask.Response(render_template('report.html', report=transactions, all=True))
    response.headers['Content-Type'] = 'text/html'
    response.headers['status_code'] = 200
    return response

if __name__ == '__main__':
    if 'mode' in os.environ and os.environ['mode'] == 'production':
        create_all()
    app.run(host='0.0.0.0', debug=True)
