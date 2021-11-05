from flask import Blueprint, render_template, redirect, url_for
import forms
from db import db
from app_bcrypt import bcrypt
from models.User import User
from flask_login import login_required, login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LogInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            return render_template('login.html', form=form, error_message="Incorrect password")
        return render_template('login.html', form=form, error_message="Incorrect username")

    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        created_user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password, )
        db.session.add(created_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)
