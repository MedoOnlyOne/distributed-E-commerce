import os 
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from distributed_ecommerce.blueprints.auth import auth
from db import db
from app_bcrypt import bcrypt
from distributed_ecommerce.models.User import User

template_dir = os.path.join('.', 'distributed_ecommerce', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(auth)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '26b966b57eb0cdfc098a15141fdd271aedf8cd0c66a76eb240b57309aa43a058ac731f40163443d1653e8bb8b8bf5431dbd075ee2cf351250c971d516037d6ce'

bcrypt.init_app(app)
db.init_app(app)

def setup_database():
    with app.app_context():
        db.create_all()

def drop_all():
    with app.app_context():
        db.drop_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.get('/')
def home():
    return render_template('index.html')
@app.get('/contactus')
def contactus():
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run(debug=True)
