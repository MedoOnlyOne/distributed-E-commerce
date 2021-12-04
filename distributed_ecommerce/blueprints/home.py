from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import uuid
from distributed_ecommerce.blueprints.auth import login
from db import db
from distributed_ecommerce.models import Product1, Product2, Shop1, Shop2, User1, User2
from flask_login import login_required, current_user
import os
import json

home = Blueprint('home', __name__, template_folder='templates')

@login_required
@home.route('/')
def browse_products():
    # get all shops of all users
    shops = Shop1.query.all()
    
    return render_template('Mainpage.html', shops=shops)
