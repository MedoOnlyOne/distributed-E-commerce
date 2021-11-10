import os 
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from distributed_ecommerce.blueprints.auth import auth
from db import db
from app_bcrypt import bcrypt
from distributed_ecommerce.models.User import User

template_dir = os.path.join('.', 'distributed_ecommerce', 'templates')
static_dir = os.path.join('.', 'distributed_ecommerce', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
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
if __name__ == '__main__':
    app.run(debug=True)
