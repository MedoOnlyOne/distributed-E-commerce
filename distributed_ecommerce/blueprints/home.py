from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import uuid
from distributed_ecommerce.blueprints.auth import login
from db import db
from distributed_ecommerce.models import Product, Shop, User, Cart
from flask_login import login_required, current_user
import os
import json

home = Blueprint('home', __name__, template_folder='templates')

@login_required
@home.route('/')
def browse_products():
    # get all products of all users
    clothing = Product.query.filter(Product.category == "Clothing").all()
    tvs = Product.query.filter(Product.category == "TVs").all()
    electronics = Product.query.filter(Product.category == "Electronics").all()
    homeappliances = Product.query.filter(Product.category == "Home Appliances").all()
    furniture = Product.query.filter(Product.category == "Furniture").all()
    others = Product.query.filter(Product.category == "Others").all()

    return render_template('Mainpage.html', clothing=clothing, tvs=tvs, electronics=electronics, homeappliances=homeappliances, furniture=furniture, others=others)
