from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import forms

from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
'''
import secrets
secrets.token_hex(64)
'''
app.config['SECRET_KEY'] = '26b966b57eb0cdfc098a15141fdd271aedf8cd0c66a76eb240b57309aa43a058ac731f40163443d1653e8bb8b8bf5431dbd075ee2cf351250c971d516037d6ce'
db = SQLAlchemy(app)

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LogInForm()
    if form.validate_on_submit():
        
        # login the user

        return redirect(url_for(home))

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():

        # craete a user

        return redirect(url_for(login))
    
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
