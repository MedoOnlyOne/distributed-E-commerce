import os 
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_login import LoginManager, current_user, login_required
from distributed_ecommerce.blueprints.auth import auth
from distributed_ecommerce.blueprints.shop import shop
from db import db
from app_bcrypt import bcrypt
from distributed_ecommerce.models import User, Order, Product, Shop 

UPLOAD_FOLDER = os.path.join('.', 'images')

template_dir = os.path.join('.', 'distributed_ecommerce', 'templates')
static_dir = os.path.join('.', 'distributed_ecommerce', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(auth)
app.register_blueprint(shop)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
app.config['SECRET_KEY'] = '26b966b57eb0cdfc098a15141fdd271aedf8cd0c66a76eb240b57309aa43a058ac731f40163443d1653e8bb8b8bf5431dbd075ee2cf351250c971d516037d6ce'
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///database2.db',
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
    return User.query.get(user_id)

@app.get('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.get('/')
def home():
    return render_template('Mainpage.html')

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

        user = User.query.filter_by(username=current_user.username).first()
        user.first_name = first_name if first_name != '' else user.first_name
        user.last_name = last_name if last_name != '' else user.last_name
        user.email = email if email != '' else user.email

        db.session.commit()
        return redirect(url_for("userdashboard"))
    return render_template('userdashboard.html')

@app.route('/product/<product_id>')
def productpage(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    product_shop = Shop.query.filter_by(shop_id=product.shop_id).first()
    if product:
        return render_template('productPage.html', product=product, shop=product_shop)
    return '<h1> Error 404 <br> Product Not Found'

if __name__ == '__main__':
    app.run(debug=True)
