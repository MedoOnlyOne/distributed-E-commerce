from flask import render_template, redirect, url_for
from Distributed_Ecommerce import app
from .forms import SignUpForm, LogInForm
from .models import User

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        
        # login the user

        return redirect(url_for(home))

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():

        # craete a user

        return redirect(url_for(login))
    
    return render_template('signup.html', form=form)