from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from blueprints.auth import auth
from db import db
from app_bcrypt import bcrypt
from models.User import User

app = Flask(__name__)
app.register_blueprint(auth)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '26b966b57eb0cdfc098a15141fdd271aedf8cd0c66a76eb240b57309aa43a058ac731f40163443d1653e8bb8b8bf5431dbd075ee2cf351250c971d516037d6ce'

bcrypt.init_app(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.get('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
