from flask import render_template, redirect, url_for
from Distributed_Ecommerce import app, db, bcrypt
from .forms import SignUpForm, LogInForm
from .models.User import User

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        
        # login the user

        return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # craete a user
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)